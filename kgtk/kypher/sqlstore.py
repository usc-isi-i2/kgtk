"""
SQLStore to support Kypher queries over KGTK graphs.
"""

import sys
import os
import os.path
import sqlite3
import time
import csv
import io
import re
from   functools import lru_cache
import itertools

import sh

from   kgtk.exceptions import KGTKException
from   kgtk.kypher.utils import *
import kgtk.kypher.infotable as oldit
import kgtk.kypher.indexspec as ispec
from   kgtk.kypher.functions import SqlFunction


### TO DO:

# o automatically run ANALYZE on tables and indexes when they get created
#   - we decided to only do this for indexes for now
# - support naming of graphs which would allow deleting of the source data
#   as well as graphs fed in from stdin
# + absolute file names are an issue when distributing the store
# - support some minimal sanity checking such as empty files, etc.
# - handle column name dealiasing and normalization
# o explanation runs outside the sqlite connection and thus does not see
#   user functions such as kgtk_stringify and friends which causes errors;
#   fixed for --explain
# - support declaring and dropping of (temporary) graphs that are only used
#   once or a few times
# - allow in-memory graphs, or better, support memory-mapped IO via
#   PRAGMA mmap_size=NNN bytes, which would be transparent and usable on demand
# o support other DB maintenance ops such as drop, list, info, etc.
# - check for version of sqlite3, since older versions do not support ascii mode
# - protect graph data import from failure or aborts through transactions
# - handle table/index creation locking when we might have parallel invocations,
#   but it looks like sqlite already does that for us
# - provide some symbolic graph size classification (small/medium/large/xlarge)
#   and implement table optimizations based on those categories
# - support bump_timestamp or similar to better keep track of what's been used
# - improve table definitions to define core columns as required to be not null
# - full LRU cache maintainance, but maybe abandon the whole LRU concept and
#   call it a store and not a cache
# + complete literal accessor functions
# + handle VACUUM and/or AUTO_VACUUM when graph tables get deleted
#   - actually no, that requires a lot of extra space, so require to do that manually


### SQL Store

class SqlStore(object):
    """SQL database capable of storing one or more KGTK graph files as individual tables
    and allowing them to be queried with SQL statements.
    """
    # This is just an abstract place-holder for now.  Once we complete SqliteStore
    # and generalize this to other SQL DB(s), we'll move API-level methods up here.
    pass


class SqliteStore(SqlStore):
    """SQL store implemented via sqlite3 (which is supported as a Python builtin library.
    """

    MASTER_TABLE = sdict[
        '_name_': 'sqlite_master',
        'columns': sdict[
            # not sure about the real types of these, but that shouldn't matter:
            'type':     sdict['_name_': 'type',     'type': 'TEXT'],
            'name':     sdict['_name_': 'name',     'type': 'TEXT'],
            'tbl_name': sdict['_name_': 'tbl_name', 'type': 'TEXT'],
            'rootpage': sdict['_name_': 'rootpage', 'type': 'INTEGER'],
            'sql':      sdict['_name_': 'sql',      'type': 'TEXT'],
        ]
    ]

    # Files contain KGTK data defining graphs, and graphs are SQL tables representing that data.
    # They are represented as separate object types, but for now the association is 1-1 where each
    # file points to the graph it defines and each graph is named by its associated file.
    # However, in the future we might redefine this association, e.g., multiple files could define
    # a graph, in which case graphs should have their own external names.  This is the main reason
    # these object types are represented in separate tables, even though we could use just a single one.
    # Over time we will need to store additional information in these tables.  The current implementation
    # allows for transparent addition of new columns without invalidating existing graph cache DBs.
    # No other changes such as renaming or deleting columns are supported (see 'InfoTable.handle_schema_update()').

    FILE_TABLE = sdict[
        '_name_': 'fileinfo',
        'columns': sdict[
            'file':    sdict['_name_': 'file',    'type': 'TEXT', 'key': True, 'doc': 'real path of the file containing the data'],
            'size':    sdict['_name_': 'size',    'type': 'INTEGER'],
            'modtime': sdict['_name_': 'modtime', 'type': 'FLOAT'],
            'md5sum':  sdict['_name_': 'md5sum',  'type': 'TEXT', 'default': None], # just for illustration of defaults
            'graph':   sdict['_name_': 'graph',   'type': 'TEXT', 'doc': 'the graph defined by the data of this file'],
            'comment': sdict['_name_': 'comment', 'type': 'TEXT', 'doc': 'comment describing the data of this file'],
        ],
        'without_rowid': False, # just for illustration
        'temporary': False,     # just for illustration
    ]

    GRAPH_TABLE = sdict[
        '_name_': 'graphinfo',
        'columns': sdict[
            'name':    sdict['_name_': 'name',    'type': 'TEXT', 'key': True, 'doc': 'name of the table representing this graph'],
            'shasum':  sdict['_name_': 'shasum',  'type': 'TEXT', 'doc': 'table hash computed by sqlite shasum command'],
            'header':  sdict['_name_': 'header',  'type': 'TEXT'],
            'size':    sdict['_name_': 'size',    'type': 'INTEGER', 'doc': 'total size in bytes used by this graph including indexes'],
            'acctime': sdict['_name_': 'acctime', 'type': 'FLOAT', 'doc': 'last time this graph was accessed'],
            'indexes': sdict['_name_': 'indexes', 'type': 'TEXT',  'doc': 'list of sdicts for indexes defined on this graph'],
        ],
        'without_rowid': False,
        'temporary': False,
    ]

    def __init__(self, dbfile=None, create=False, loglevel=0, conn=None, readonly=False):
        """Open or create an SQLStore on the provided database file 'dbfile'
        or SQLite connection object 'conn'.  If 'dbfile' is provided and does
        not yet exist, it will only be created if 'create' is True.  Passing
        in a connection object directly provides more flexibility with creation
        options.  In that case any 'dbfile' value will be ignored and instead
        looked up directly from 'conn'.
        """
        self.loglevel = loglevel
        self.dbfile = dbfile
        self.conn = conn
        self.readonly = readonly
        if not isinstance(self.conn, sqlite3.Connection):
            if self.conn is not None:
                raise KGTKException('invalid sqlite connection object: %s' % self.conn)
            if self.dbfile is None:
                raise KGTKException('no sqlite DB file or connection object provided')
            if not os.path.exists(self.dbfile) and (not create or readonly):
                raise KGTKException('sqlite DB file does not exist: %s' % self.dbfile)
        else:
            self.dbfile = self.pragma('database_list')[0][2]
        self.user_functions = set()
        self.vector_store = None
        self.init_meta_tables()
        self.configure()
        # run this right after 'configure()' since it is not thread
        # safe and later calls might lead to undefined behavior;
        # also we might need it for distinct or order-by queries:
        self.configure_temp_dir()

    def log(self, level, message):
        if self.loglevel >= level:
            header = '[%s sqlstore]:' % time.strftime('%Y-%m-%d %H:%M:%S')
            sys.stderr.write('%s %s\n' % (header, message))
            sys.stderr.flush()

    def init_meta_tables(self):
        self.fileinfo = oldit.InfoTable(self, self.FILE_TABLE)
        self.graphinfo = oldit.InfoTable(self, self.GRAPH_TABLE)
        self.fileinfo.init_table()
        self.graphinfo.init_table()

    def describe_meta_tables(self, out=sys.stderr):
        """Describe the current content of the internal bookkeeping tables to 'out'.
        """
        out.write('Graph Cache:\n')
        out.write('DB file: %s\n' % self.dbfile)
        out.write('  size:  %s' % format_memory_size(self.get_db_size()))
        out.write('   \tfree:  %s' % format_memory_size(self.get_db_free_size()))
        out.write('   \tmodified:  %s\n' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(self.dbfile))))
        out.write('\n')
        out.write('KGTK File Information:\n')
        self.describe_file_info_table(out=out)
        out.write('\n')
        out.write('Graph Table Information:\n')
        self.describe_graph_info_table(out=out)

    # TO DO: consider reducing this or making it configurable, since its effect on runtime
    #        seems to be small (5-10%) compared to the memory it additionally consumes:
    CACHE_SIZE = 2 ** 32            #  4GB
    #CACHE_SIZE = 2 ** 34           # 16GB
    #CACHE_SIZE = 2 ** 34 + 2 ** 33 # 24GB

    def configure(self):
        """Configure various settings of the store.
        """
        #self.pragma('main.page_size = 65536') # for zfs only
        self.pragma('main.cache_size = %d' % int(self.CACHE_SIZE / self.pragma('page_size')))

    def configure_temp_dir(self):
        """Configure the SQLite temp directory to be in the same location as the database file,
        unless that is explicitly overridden by a different settings from SQLITE_TMPDIR.
        This tries to avoid disk-full errors when large files are imported and indexed, since
        standard temp directories are usually located in smaller OS disk partitions.
        """
        # 'temp_store_directory' is deprecated and might not be available, but there is no good
        # alternative except SQLITE_TMPDIR, so we try anyway and report just a warning if --debug:
        try:
            if not self.pragma('temp_store_directory') and not os.getenv('SQLITE_TMPDIR') and self.dbfile:
                tmpdir = os.path.dirname(os.path.realpath(self.dbfile))
                self.pragma(f'temp_store_directory={sql_quote_ident(tmpdir)}')
        except:
            self.log(1, "WARN: cannot set 'pragma temp_store_directory', set SQLITE_TMPDIR envar instead if needed")


    ### DB control:

    def get_conn(self):
        if self.conn is None:
            if self.readonly:
                self.conn = sqlite3.connect(f'file:{self.dbfile}?mode=ro', uri=True)
            else:
                self.conn = sqlite3.connect(self.dbfile)
        return self.conn

    def get_sqlite_cmd(self):
        # TO DO: this should look more intelligently to find it in the python install path
        # e.g., check 'sys.prefix/bin', 'sys.exec_prefix/bin' or do a 'which sqlite3';
        # if we use a conda environment we get it automatically.
        return 'sqlite3'

    def close(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None
            self.user_functions = set()

    READONLY_REGEX = re.compile(r'^\s*(select|pragma)\s', re.IGNORECASE)
    
    def is_readonly_statement(self, statement):
        """Return True if the SQL 'statement' does not update the database.
        """
        return self.READONLY_REGEX.search(statement) is not None

    def execute(self, *args, **kwargs):
        if self.readonly and not self.is_readonly_statement(args[0]):
            # do nothing and return empty cursor:
            return sqlite3.Cursor(self.get_conn())
        else:
            return self.get_conn().execute(*args, **kwargs)

    def executemany(self, *args, **kwargs):
        if self.readonly and not self.is_readonly_statement(args[0]):
            # do nothing and return empty cursor:
            return sqlite3.Cursor(self.get_conn())
        else:
            return self.get_conn().executemany(*args, **kwargs)

    def commit(self):
        self.get_conn().commit()

    def pragma(self, expression):
        """Evaluate a PRAGMA 'expression' and return the result (if any).
        """
        res = list(self.execute('PRAGMA ' + expression))
        if len(res) == 0:
            return None
        elif len(res) == 1 and len(res[0]) == 1:
            return res[0][0]
        else:
            return res


    ### DB functions:

    @staticmethod
    def register_user_function(name, num_params, func, deterministic=False):
        """Old-style user function registration API, supported for backwards compatibility.
        """
        from kgtk.kypher.functions import SqlFunction
        SqlFunction(name, code=func, num_params=num_params, deterministic=deterministic).define()

    def load_user_function(self, name, num_params, func, deterministic=False):
        """Load the specified function 'name' into the current connection.
        Follows the sqlite3 API (which see).
        """
        conn = self.get_conn()
        try:
            if isinstance(func, type) and hasattr(func, 'register'):
                # we have a table-valued function described by a class object:
                func.register(conn)
            elif not deterministic:
                # try to avoid an error by not using the deterministic flag:
                conn.create_function(name, num_params, func)
            else:
                conn.create_function(name, num_params, func, deterministic=True)
        except sqlite3.NotSupportedError:
            # older SQLite, define it without 'deterministic':
            self.store.get_conn().create_function(name, num_params, func)
        # remember the function names we've loaded so far:
        self.user_functions.add(name)

    def load_aggregate_function(self, name, num_params, aggregate_class):
        """Load the specified aggregate function 'name' into the current connection.
        Follows the sqlite3 API (which see).
        """
        conn = self.get_conn()
        conn.create_aggregate(name, num_params, aggregate_class)
        self.user_functions.add(name)

    def get_user_functions(self):
        """Return the names of all user functions loaded into the current connection.
        """
        return self.user_functions


    ### DB properties and operations:
    
    def get_db_size(self):
        """Return the size of all currently allocated data pages in bytes.  This maybe smaller than
        the size of the database file if there were deletions that put pages back on the free list.
        Free pages can be reclaimed by running 'VACUUM', but that might require a substantial amount
        of available disk space if the current DB file is large.
        """
        return (self.pragma('page_count') - self.pragma('freelist_count')) * self.pragma('page_size')

    def get_db_free_size(self):
        """Return the size of all currently allocated but free data pages in bytes.
        """
        return self.pragma('freelist_count') * self.pragma('page_size')

    def has_table(self, table_name):
        """Return True if a table with name 'table_name' exists in the store.
        """
        schema = self.MASTER_TABLE
        columns = schema.columns
        query = """SELECT COUNT(*) FROM %s WHERE %s=?""" % (schema._name_, columns.name._name_)
        (cnt,) = self.execute(query, (table_name,)).fetchone()
        return cnt > 0

    def get_table_header(self, table_name):
        """Return the column names of 'table_name' as a list.  For graph tables, this list will be
        isomorphic to the parsed header line of the corresponding KGTK file.
        """
        result = self.execute('SELECT * FROM %s LIMIT 0' % table_name)
        return [col[0] for col in result.description]

    def get_table_row_count(self, table_name):
        for (cnt,) in self.execute('SELECT MAX(rowid) FROM %s' % table_name):
            return cnt or 0  # need to handle case of empty table without any rowids
        return 0

    def has_table_column(self, table_name, column_name):
        """Return True if table 'table_name' exists and has a column 'column_name'.
        """
        return self.has_table(table_name) and column_name in self.get_table_header(table_name)

    def get_table_definition_sql(self, table_name):
        """Return the 'CREATE TABLE <table_name> ...' statement used to create this table.
        """
        master = self.MASTER_TABLE._name_
        mcols = self.MASTER_TABLE.columns
        query = f"""SELECT {mcols.sql._name_} FROM {master} 
                    WHERE {mcols.type._name_}='table' AND {mcols.name._name_}=?"""
        for (stmt,) in self.execute(query, (table_name,)):
            return stmt
        return None

    def get_table_indexes_sql(self, table_name):
        """Return the 'CREATE INDEX ... ON <table_name> ...' statements used to index this table.
        """
        master = self.MASTER_TABLE._name_
        mcols = self.MASTER_TABLE.columns
        query = f"""SELECT {mcols.sql._name_} FROM {master} 
                    WHERE {mcols.type._name_}='index' AND {mcols.tbl_name._name_}=?"""
        return [stmt for (stmt,) in self.execute(query, (table_name,))]

    def sort_table(self, table_name, columns):
        """Sort the rows in table 'table_name' along one or more 'columns'.  Each column can be a simple
        column name or a full spec such as 'cast(node2 as int) desc' containing optional type coercion
        and sort directions (in which case the column name should be properly quoted if necessary).  This 
        creates a copy of 'table_name' into which the sorted rows will be inserted.  All indexes existing
        on the original table will also be recreated.  After sorting the freed up space from the original
        table and indexes is NOT automatically reclaimed.  To use it or free it either add additional
        data to the database or run the VACUUM command.  The value of sorting a table is primarily to
        create better data locality on disk, the sorted table will otherwise be identical to the original.
        """
        # we look up the actual definition statement to get all the types and column features correct:
        table_def = self.get_table_definition_sql(table_name)
        if table_def is None:
            raise KGTKException(f"table '{table_name}' does not exist")
        index_defs = self.get_table_indexes_sql(table_name)
        table_columns = self.get_table_header(table_name)
        sorted_table = f'{table_name}_sortEd_'
        sorted_def = re.sub(r"""(?i)^\s*(CREATE\s+TABLE\s+)['"`]?""" + re.escape(table_name) + r"""['"`]?(\s+.*)""",
                            f'\\1{sql_quote_ident(sorted_table)}\\2', table_def)
        if sorted_def == table_def:
            raise KGTKException(f"failed to sort '{table_name}', unexpected definition statement")
        sort_columns = [sql_quote_ident(col) if not re.search("""["` ]""", col) else col for col in listify(columns)]
        sort_stmt = f"""INSERT INTO {sql_quote_ident(sorted_table)} 
                        SELECT {', '.join(map(sql_quote_ident, table_columns))}
                        FROM {sql_quote_ident(table_name)}
                        ORDER BY {', '.join(sort_columns)}"""
        self.log(1, f"SORT table '{table_name}'...")
        self.execute(sorted_def)
        self.execute(sort_stmt)
        # ensure these counts are the same:
        if self.get_table_row_count(table_name) != self.get_table_row_count(sorted_table):
            raise KGTKException(f"something went wrong during sorting of '{table_name}' into '{sorted_table}'")
        self.log(1, f"DROP unsorted table '{table_name}'...")
        self.execute(f'DROP table {sql_quote_ident(table_name)}')
        # this can take some time on large tables:
        self.execute(f'ALTER TABLE {sql_quote_ident(sorted_table)} RENAME TO {sql_quote_ident(table_name)}')
        for index_def in index_defs:
            self.log(1, f"RE-CREATE index '{index_def}'...")
            self.execute(index_def)
        self.commit()


    ### Schema manipulation:
    
    def kgtk_header_to_graph_table_schema(self, table_name, header):
        columns = sdict()
        for col in header:
            columns[col] = sdict['type': 'TEXT', '_name_': col]
        return sdict['_name_': table_name, 'columns': columns]

    def get_key_column(self, table_schema, error=True):
        """Return the name of the first column in 'schema' designated as a 'key',
        or raise an error if no key column has been designated (unless 'error' is False).
        This should only be used for single-key tables such as info tables.
        """
        for col in table_schema.columns.values():
            if col.get('key') == True:
                return col._name_
        if error:
            raise KGTKException('no key column defined')
        return None

    def get_table_definition(self, table_schema):
        """Generate an SQLite table definition for 'table_schema'.  Requires each column
        to have at least a 'type' property.  Optional 'default' properties will be translated
        into appropriate 'DEFAULT <value>' column constraints.  One or more columns with a
        'key' property will be translated into a 'PRIMARY KEY (col...)' constraint.  If there
        is more than one column with a key, they will be sorted by their values to order them.
        A 'without_rowid' property on the table will produce a 'WITHOUT ROWID' table (which
        requires a primary key to be legal!).  For some simple attribute tables such as 'labels',
        etc. that only index on 'node1' those might be more space efficient than regular tables.
        """
        colspecs = []
        keys = []
        for col in table_schema.columns.values():
            spec = sql_quote_ident(col._name_) + ' ' + col.type
            dflt = col.get('default')
            if dflt is not None:
                dflt = isinstance(dflt, (int, float)) and '{:+g}'.format(dflt) or '"%s"' % dflt
                spec += ' DEFAULT ' + dflt
            key = col.get('key')
            key and keys.append((col._name_, key))
            colspecs.append(spec)
        if len(keys) > 0:
            keys.sort(key=lambda x: x[1])
            keys = 'PRIMARY KEY (%s)' % ', '.join(map(lambda x: x[0], keys))
            colspecs.append(keys)
        temp = table_schema.get('temporary') and ' TEMPORARY' or ''
        norowid = table_schema.get('without_rowid') and ' WITHOUT ROWID' or ''
        return f'CREATE{temp} TABLE {table_schema._name_} ({", ".join(colspecs)}){norowid}'

    def get_table_index(self, table_or_schema, columns, unique=False):
        """Return a TableIndex object for an index on 'columns' for 'table_or_schema'.
        Create a unique or primary key index if 'unique' is True.
        """
        columns = [columns] if isinstance(columns, str) else columns # coerce to list
        index_spec = f'index: {", ".join([sql_quote_ident(col) for col in columns])}'
        if unique:
            index_spec += '//unique'
        return ispec.TableIndex(table_or_schema, index_spec)

    def get_column_list(self, *columns):
        return ', '.join([sql_quote_ident(col._name_) for col in columns])

    def get_full_column_list(self, table_schema):
        return ', '.join([sql_quote_ident(col._name_) for col in table_schema.columns.values()])


    ### File information and access:

    # Each fileinfo record is identified by a name key which defaults to the full
    # dereferenced realpath of the file from which the graph data was loaded.
    # If an alias was provided that name will be stored as the key instead.

    def normalize_file_path(self, file):
        # for stdin we key in on full filenames for now to also support 'stdin' as an alias:
        if file in ('-', '/dev/stdin'):
            return '/dev/stdin'
        else:
            return os.path.realpath(file)

    def is_standard_input(self, file):
        return self.normalize_file_path(file) == '/dev/stdin'

    def is_input_alias_name(self, name):
        """Return true if 'name' is a legal input alias.  We require aliases to not
        contain any path separators to distinguish them from file names which are
        stored as absolute pathnames in the file info table.
        """
        return name.find(os.sep) < 0
    
    def is_input_file_name(self, name):
        return not self.is_input_alias_name(name)

    def get_file_info(self, file, alias=None, exact=False):
        """Return a dict info structure for the file info for 'file' (or 'alias') or None
        if this file does not exist in the file table.  All column keys will be set in
        the result although some values may be None.  If 'exact', use 'file' as is and
        do not try to normalize it to an absolute path.  Matches based on 'file' will
        have preference over matches based on 'alias', for example, a file named 'graph'
        will match the entry for '/data/graph' (if that is its full name) before it
        matches an entry named by the alias 'mygraph', for example.
        """
        info = self.fileinfo.get_info(file)
        if info is None and not exact:
            file = self.normalize_file_path(file)
            info = self.fileinfo.get_info(file)
        if info is None and alias is not None:
            info = self.fileinfo.get_info(alias)
        return info

    def get_normalized_file(self, file, alias=None, exact=False):
        """Return the stored normalized name of 'file' (or 'alias') or None
        if this file does not exist in the file table.
        """
        info = self.get_file_info(file, alias=alias, exact=exact)
        return info and info.file or None
        
    def set_file_info(self, _file, **kwargs):
        # TRICKY: we use '_file' so we can also use and update 'file' in 'kwargs'
        self.fileinfo.set_info(_file, kwargs)

    def update_file_info(self, _file, **kwargs):
        self.fileinfo.update_info(_file, kwargs)
        
    def drop_file_info(self, file):
        """Delete the file info record for 'file'.
        IMPORTANT: this does not delete any graph data associated with 'file'.
        """
        self.fileinfo.drop_info(file)
        
    def describe_file_info(self, file, out=sys.stderr):
        """Describe a single 'file' (or its info) to 'out'.
        """
        info = isinstance(file, dict) and file or self.get_file_info(file)
        out.write('%s:\n' % info.file)
        out.write('  size:  %s' % (info.size and format_memory_size(info.size) or '???   '))
        out.write('   \tmodified:  %s' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(info.modtime)))
        out.write('   \tgraph:  %s\n' % info.graph)
        if info.comment:
            out.write('  comment:  %s\n' % info.comment)

    def describe_file_info_table(self, out=sys.stderr):
        """Describe all files in the FILE_TABLE to 'out'.
        """
        for info in self.fileinfo.get_all_infos():
            self.describe_file_info(info, out=out)

    def set_file_alias(self, file, alias):
        """Set the file column of the file info identified by 'file' (or 'alias') to 'alias'.
        Raises an error if no relevant file info could be found, or if 'alias' is already
        used in a different file info (in which case it wouldn't be a unique key anymore).
        """
        finfo = self.get_file_info(file, alias=alias)
        if finfo is None:
            raise KGTKException('cannot set alias for non-existent file: %s' % file)
        ainfo = self.get_file_info(alias, exact=True)
        if ainfo is not None and ainfo != finfo:
            # this can happen if we imported 'file' without an alias, then another file
            # with 'alias', and then we try to associate 'alias' to 'file':
            raise KGTKException('alias %s is already in use for different file' % alias)
        # update current file name to 'alias':
        self.update_file_info(finfo.file, file=alias)

    def set_file_comment(self, file, comment):
        """Set the comment property for 'file'.
        """
        # We might need some text normalization here:
        self.update_file_info(file, comment=comment)

    def get_file_graph(self, file):
        """Return the graph table name created from the data of 'file'.
        """
        return self.get_file_info(file).graph

    def get_graph_files(self, table_name):
        """Return the list of all files whose data is represented by 'table_name'.
        Generally, there will only be one, but it is possible that different versions
        of a file (e.g., compressed vs. uncompressed) created the same underlying data
        which we could detect by running a sha hash command on the resulting tables.
        """
        schema = self.FILE_TABLE
        table = schema._name_
        cols = schema.columns
        keycol = self.get_key_column(schema)
        query = 'SELECT %s FROM %s WHERE %s=?' % (cols.file._name_, table, cols.graph._name_)
        return [file for (file,) in self.execute(query, (table_name,))]


    ### Graph information and access:

    # TO DO: add 'bump_timestamp' so we can easily track when this graph was last used
    #        add 'update_xxx_info' methods that only change not None fields
    
    def get_graph_info(self, table_name):
        """Return a dict info structure for the graph stored in 'table_name' (there can only be one),
        or None if this graph does not exist in the graph table.  All column keys will be set
        although some values may be None.
        """
        return self.graphinfo.get_info(table_name)

    def set_graph_info(self, table_name, **kwargs):
        self.graphinfo.set_info(table_name, kwargs)
    
    def update_graph_info(self, table_name, **kwargs):
        self.graphinfo.update_info(table_name, kwargs)
        
    def drop_graph_info(self, table_name):
        """Delete the graph info record for 'table_name'.
        IMPORTANT: this does not delete any graph data stored in 'table_name'.
        """
        self.graphinfo.drop_info(table_name)

    def describe_graph_info(self, graph, out=sys.stderr):
        """Describe a single 'graph' (or its info) to 'out'.
        """
        info = isinstance(graph, dict) and graph or self.get_graph_info(graph)
        out.write('%s:\n' % info.name)
        out.write('  size:  %s' % format_memory_size(info.size))
        out.write('   \tcreated:  %s\n' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(info.acctime)))
        out.write('  header:  %s\n' % info.header)

    def describe_graph_info_table(self, out=sys.stderr):
        """Describe all graphs in the GRAPH_TABLE to 'out'.
        """
        for info in self.graphinfo.get_all_infos():
            self.describe_graph_info(info, out=out)

    def get_graph_table_schema(self, table_name):
        """Get a graph table schema definition for graph 'table_name'.
        """
        info = self.get_graph_info(table_name)
        header = eval(info.header)
        return self.kgtk_header_to_graph_table_schema(table_name, header)

    def get_graph_indexes(self, table_name):
        """Return the list of indexes currently defined for graph 'table_name'.
        This will lookup from the 'indexes' column of the corresponding graph info,
        but will also be backwards-compatible and use the SQLite master table if needed.
        """
        info = self.get_graph_info(table_name)
        if info is None:
            # see if 'table_name' is a defined or loaded virtual table function:
            if SqlFunction.is_virtual_graph(table_name) or table_name in self.get_user_functions():
                return []
            raise KGTKException(f"INTERNAL ERROR: missing graph info for '{table_name}'")
        indexes = info.indexes
        if indexes is None:
            # we have an old-style graph info table that just got updated, retrieve index definitions
            # from the master table and store them (maybe the 'sql:...' mode should support parsing those):
            schema = self.MASTER_TABLE
            columns = schema.columns
            query = (f"""SELECT {columns.name._name_}, {columns.sql._name_} FROM {schema._name_}""" +
                     f""" WHERE {columns.type._name_}="index" and {columns.tbl_name._name_}=?""")
            indexes = [ispec.TableIndex(table_name, 'sql: ' + idx_sql) for _, idx_sql in self.execute(query, (table_name,))]
            indexes = ispec.TableIndex.encode(indexes)
            self.set_graph_info(table_name, indexes=indexes)
        return ispec.TableIndex.decode(indexes)

    def has_graph_index(self, table_name, index):
        """Return True if graph 'table_name' has an index that subsumes 'index'.
        """
        for idx in self.get_graph_indexes(table_name):
            if idx.subsumes(index) and not index.redefines(idx):
                return True
        else:
            return False

    def get_vector_indexes(self, table_name):
        """Return the list of vector indexes currently defined for graph 'table_name'.
        """
        info = self.get_graph_info(table_name)
        if info is None:
            # see if 'table_name' is a defined or loaded virtual table function:
            if SqlFunction.is_virtual_graph(table_name) or table_name in self.get_user_functions():
                return []
            raise KGTKException(f"INTERNAL ERROR: missing graph info for '{table_name}'")
        indexes = info.indexes
        return [idx for idx in ispec.TableIndex.decode(indexes) if isinstance(idx, ispec.VectorIndex)]

    def is_vector_column(self, table_name, column):
        """Return True if 'column' in 'table_name' is a vector column.
        """
        for vindex in self.get_vector_indexes(table_name):
            if column in vindex.index.columns:
                return True
        else:
            return False

    def ensure_graph_index(self, table_name, index, explain=False):
        """Ensure a qualifying 'index' for 'table_name' already exists or gets created.
        Checks whether the existing index is at least as selective as requested, for
        example, an existing index on columns (node1, node2) will qualify even if 'index'
        has 'node1' as its only column.
        """
        if not self.has_graph_index(table_name, index):
            if self.readonly:
                return
            loglevel = 0 if explain else 1
            indexes = self.get_graph_indexes(table_name)
            # delete anything that is redefined by this 'index':
            for idx in indexes[:]:
                if index.redefines(idx) and not explain:
                    self.drop_graph_index(table_name, idx)
            indexes = self.get_graph_indexes(table_name)
            # we also measure the increase in allocated disk space here:
            oldsize = self.get_db_size()
            index.create_index(self, explain=explain)
            idxsize = self.get_db_size() - oldsize
            ginfo = self.get_graph_info(table_name)
            ginfo.size += idxsize
            if not explain:
                # we may have added/deleted some, so recompute the list:
                indexes = self.get_graph_indexes(table_name)
                indexes = ispec.TableIndex.encode(indexes + [index])
                self.update_graph_info(table_name, indexes=indexes)
                self.update_graph_info(table_name, size=ginfo.size)
                self.commit()

    def ensure_graph_index_for_columns(self, table_name, columns, unique=False, explain=False):
        """Ensure an index for 'table_name' on 'columns' already exists or gets created.
        Checks whether the existing index is at least as selective as requested, for example,
        an existing index on columns (node1, node2) will qualify even if only node1 is requested.
        """
        index = self.get_table_index(table_name, columns, unique=unique)
        self.ensure_graph_index(table_name, index, explain=explain)

    def number_of_graphs(self):
        """Return the number of graphs currently stored in 'self'.
        """
        return self.get_table_row_count(self.GRAPH_TABLE._name_)

    def new_graph_table(self):
        """Return a new table name to be used for representing a graph.
        """
        graphid = (self.number_of_graphs() + 1)
        # search for an open ID (we might have gaps due to deletions):
        while True:
            table = 'graph_%d' % graphid
            if not self.has_table(table):
                return table
            graphid += 1

    def determine_graph_action(self, file, alias=None, error=True):
        """Determine which action to perform for the KGTK graph indicated by input 'file' (or 'alias').
        Returns one of 'add', 'replace', 'reuse' or 'error'.  Raises an exception for error cases in
        case 'error' was set to True (the default).

        Returns 'add' if no matching file info based on 'file/alias' could be found, in which case
        the data needs to be newly imported.

        Returns 'reuse' if a matching file info was found and 'file' is an existing regular file whose
        properties match exactly what was previously loaded, or is not an existing regular file in which
        case its properties cannot be checked.  This latter case allows us to delete large input files
        after import without losing the ability to query them, or to query files by using their alias
        instead of a real filename.

        Returns 'replace' if a matching file info was found and 'file' is an existing regular file
        whose properties do not match what was previously loaded, or if 'file' names standard input.
        If so an obsolete graph table for 'file' will have to be removed before new data gets imported.

        Checks for errors such as invalid alias names, aliases that are already in use for other
        inputs, and cases where an existing file might conflict with an existing input alias.
        """
        if alias is not None and not self.is_input_alias_name(alias):
            if error:
                raise KGTKException(f'invalid input alias name: {alias}')
            else:
                return 'error'
        
        info = self.get_file_info(file, alias=alias)
        if info is None:
            return 'add'
        
        is_aliased = self.is_input_alias_name(info.file)
        defines_alias = alias is not None
        if defines_alias:
            alias_info = self.get_file_info(alias, exact=True)
            if alias_info is not None and info.file != alias_info.file:
                if error:
                    raise KGTKException(f"input alias '{alias}' already in use")
                else:
                    return 'error'
        
        if self.is_standard_input(file):
            # we never reuse plain stdin, it needs to be aliased to a new name for that:
            return 'replace'
        
        if os.path.exists(file):
            if is_aliased and not defines_alias:
                if error:
                    raise KGTKException(f"input '{file}' conflicts with existing alias; "+
                                        f"to replace use explicit '--as {info.file}'")
                else:
                    return 'error'
            if info.size !=  os.path.getsize(file):
                return 'replace'
            if info.modtime != os.path.getmtime(file):
                return 'replace'
            # don't check md5sum for now
        return 'reuse'

    def has_graph(self, file, alias=None):
        """Return True if the KGTK graph represented/named by 'file' (or its 'alias' if not None)
        has already been imported and is up-to-date (see 'determine_graph_action' for the full story).
        """
        return self.determine_graph_action(file, alias=alias, error=False) == 'reuse'

    def add_graph(self, file, alias=None, index_specs=None):
        """Import a graph from 'file' (and optionally named by 'alias') unless a matching
        graph has already been imported earlier according to 'has_graph' (which see).
        'index_specs' is a list of index specifications relevant to the import of this graph.
        """
        graph_action = self.determine_graph_action(file, alias=alias)
        if graph_action == 'reuse':
            if alias is not None:
                # this allows us to do multiple renamings (no-op if we are readonly):
                self.set_file_alias(file, alias)
            return
        file_info = self.get_file_info(file, alias=alias)
        if graph_action == 'replace':
            # we already have an earlier version of the file in store:
            if self.readonly:
                # reuse it:
                return
            else:
                # delete its graph data before importing new version:
                self.drop_graph(file_info.graph)
        if self.readonly:
            raise KGTKException(f"cannot import {file} in read-only mode")
        file = self.normalize_file_path(file)
        table = self.new_graph_table()
        oldsize = self.get_db_size()
        vector_specs = self.get_vector_index_specs(table, index_specs)
        indexes = []
        if len(vector_specs) > 0:
            indexes += self.import_graph_vector_data_via_csv(table, file, index_specs=vector_specs)
        else:
            try:
                # try fast shell-based import first, but if that is not applicable...
                self.import_graph_data_via_import(table, file)
            except (KGTKException, sh.CommandNotFound):
                # ...fall back on CSV-based import which is more flexible but about 2x slower:
                self.import_graph_data_via_csv(table, file)
        graphsize = self.get_db_size() - oldsize
        # this isn't really needed, but we store it for now:
        header = str(self.get_table_header(table))
        if self.is_standard_input(file):
            self.set_file_info(file, size=0, modtime=time.time(), graph=table)
        else:
            self.set_file_info(file, size=os.path.getsize(file), modtime=os.path.getmtime(file), graph=table)
        # FIXME: this is incorrect, since the vector index hasn't been (completely) created yet, but for
        # now we need it to get correct query translations; but this needs a more general approach, since
        # it also doesn't do the right thing for redefinitions of vector indexes
        indexes = ispec.TableIndex.encode(indexes)
        self.set_graph_info(table, header=header, size=graphsize, acctime=time.time(), indexes=indexes)
        if alias is not None:
            self.set_file_alias(file, alias)

    def drop_graph(self, table_name):
        """Delete the graph 'table_name' and all its associated info records.
        """
        if self.readonly:
            return
        # delete all supporting file infos:
        for file in self.get_graph_files(table_name):
            self.log(1, 'DROP graph data table %s from %s' % (table_name, file))
            self.drop_file_info(file)
        # delete the graph info:
        self.drop_graph_info(table_name)
        # now delete the graph table and all associated indexes:
        if self.has_table(table_name):
            self.execute('DROP TABLE %s' % table_name)

    def drop_graph_index(self, table_name, index):
        """Delete 'index' for graph 'table_name' and its associated info records.
        """
        if self.readonly:
            return
        ginfo = self.get_graph_info(table_name)
        indexes = self.get_graph_indexes(table_name)
        if index not in indexes:
            raise KGTKException(f'No such index for {table_name}: {index}]')
        oldsize = self.get_db_size()
        index.drop_index(self, explain=False)
        idxsize = oldsize - self.get_db_size()
        # we might have updated them, so recompute the list:
        indexes = self.get_graph_indexes(table_name)
        indexes.remove(index)
        ginfo.size -= idxsize
        self.update_graph_info(table_name, indexes=ispec.TableIndex.encode(indexes), size=ginfo.size)

    def drop_graph_indexes(self, table_name, index_type=None):
        """Delete all indexes for graph 'table_name'.  If 'index_type' is not None,
        restrict to indexes of that type (can be a short name or a class).
        """
        if isinstance(index_type, str):
            index_type = ispec.TableIndex.get_index_type_class(index_type)
        for index in self.get_graph_indexes(table_name)[:]:
            if index_type is None or isinstance(index, index_type):
                self.drop_graph_index(table_name, index)


    ### Data import:
    
    def import_graph_data_via_csv(self, table, file):
        """Import 'file' into 'table' using Python's csv.reader.  This is safe and properly
        handles conversion of different kinds of line endings, but 2x slower than direct import.
        """
        if self.readonly:
            return
        self.log(1, 'IMPORT graph via csv.reader into table %s from %s ...' % (table, file))
        if self.is_standard_input(file):
            file = sys.stdin
        with open_to_read(file) as inp:
            csvreader = csv.reader(inp, dialect=None, delimiter='\t', quoting=csv.QUOTE_NONE)
            header = next(csvreader)
            schema = self.kgtk_header_to_graph_table_schema(table, header)
            self.execute(self.get_table_definition(schema))
            insert = 'INSERT INTO %s VALUES (%s)' % (table, ','.join(['?'] * len(header)))
            self.executemany(insert, csvreader)
            self.commit()

    def import_graph_data_via_import(self, table, file):
        """Use the sqlite shell and its import command to import 'file' into 'table'.
        This will be about 2+ times faster and can exploit parallelism for decompression.
        This is only supported for Un*x for now and requires a named 'file'.
        """
        if self.readonly:
            return
        if os.name != 'posix':
            raise KGTKException("not yet implemented for this OS: '%s'" % os.name)
        # generalizing this to work for stdin would be possible, but it would significantly complicate
        # matters, since we also have to check for multi-char line endings at which point we can't
        # simply abort to 'import_graph_data_via_csv' but would have to buffer and resupply the read data:
        if not isinstance(file, str) or not os.path.exists(file) or self.is_standard_input(file):
            raise KGTKException('only implemented for existing, named files')
        # make sure we have the Unix commands we need:
        catcmd = get_cat_command(file, _piped=True)
        tail = sh.Command('tail')
        sqlite3 = sh.Command(self.get_sqlite_cmd())
        isplain = os.path.basename(catcmd._path) == b'cat'
        
        # This is slightly more messy than we'd like it to be: sqlite can create a table definition
        # for a non-existing table from the header row, but it doesn't seem to handle just any weird
        # column name we give it there, so we read the header and create the table ourselves;
        # however, sqlite doesn't have an option to then skip the header, so we need to use 'tail';
        # also, eventually we might want to supply more elaborate table defs such as 'without rowid';
        # finally, we have to guard against multi-character line-endings which can't be handled right:
        with open_to_read(file, 'rt') as inp:
            #csvreader = csv.reader(inp, dialect=None, delimiter='\t', quoting=csv.QUOTE_NONE)
            header = inp.readline()
            if inp.newlines != '\n':
                # SQLite import can only handle single-character line endings, if we import anyway,
                # \r winds up in the values of the last column; we also can't handle \r by itself
                # (which should be rare - not used since MacOS X), since that will not work with 'tail'.
                # We could handle both cases by mapping to \n with 'tr', but that introduces an extra
                # pipe and command complication - maybe later:
                raise KGTKException('unsupported line endings')
            header = header[:-1].split('\t')
            schema = self.kgtk_header_to_graph_table_schema(table, header)
            self.execute(self.get_table_definition(schema))
            self.commit()
        
        separators = '\\t \\n'
        args = ['-cmd', '.mode ascii', '-cmd', '.separator ' + separators,
                self.dbfile, '.import /dev/stdin %s' % table]

        self.log(1, 'IMPORT graph directly into table %s from %s ...' % (table, file))
        try:
            if isplain:
                tailproc = tail('-n', '+2', file, _piped=True)
            else:
                tailproc = tail(catcmd(), '-n', '+2', _piped=True)
            # we run this asynchronously, so we can kill it in the cleanup clause:
            sqlproc = sqlite3(tailproc, *args, _bg=True)
            sqlproc.wait()
        finally:
            # make sure we kill this process in case we had a user interrupt, however,
            # getting this condition right so we don't hang and don't break was tricky,
            # since there is various machinery under the hood which leads to additional
            # waiting (we can't call is_alive or access sqlproc.exit_code):
            if sqlproc is not None and sqlproc.process.exit_code is None:
                sqlproc.terminate()

                
    # we need to be able to comfortably fit that many un/parsed vectors into RAM:
    VECTOR_IMPORT_CHUNKSIZE = 100000

    def get_vector_store(self):
        if self.vector_store is None:
            import kgtk.kypher.vecstore as vs
            self.vector_store = vs.MasterVectorStore(self)
        return self.vector_store

    def get_vector_index_specs(self, graph, index_specs):
        vector_specs = []
        for index_spec in listify(index_specs):
            index_spec = ispec.get_normalized_index_mode(index_spec)
            if isinstance(index_spec, list):
                for spec in index_spec:
                    spec = ispec.TableIndex(graph, spec)
                    if isinstance(spec, ispec.VectorIndex):
                        vector_specs.append(spec)
        return vector_specs

    def normalize_vector_index_specs(self, graph, index_specs):
        """Normalize all 'index_specs' for 'graph' into a single one containing all the
        relevant information.  This is somewhat different than other index specs, since
        we assume there can be at most one index per vector column of each graph.
        """
        index_specs = listify(index_specs)
        if len(index_specs) == 0:
            # use this as the default, even though 'index_specs' shouldn't be empty:
            index_specs = [ispec.TableIndex(graph, 'vector: node2/fmt=auto')]
        vector_spec = index_specs[0]
        for ospec in index_specs[1:]:
            # merge and override from any subsequent specs:
            for col, spec in ospec.index.columns.items():
                vector_spec.index.columns[col] = spec
        return vector_spec

    def import_graph_vector_data_via_csv(self, table, file, index_specs=None):
        """Import 'file' into 'table' using Python's csv.reader.  Parses and stores any vector columns
        in binary format into the respective vector cache and blanks out the corresponding source field(s).
        """
        if self.readonly:
            return
        self.log(1, f'IMPORT graph vectors into table {table} and associated vector cache from {file}')
        if self.is_standard_input(file):
            file = sys.stdin

        vector_spec = self.normalize_vector_index_specs(table, index_specs)
        vector_columns = list(vector_spec.index.columns.keys())
        vstore = self.get_vector_store()
        
        with open_to_read(file) as inp:
            csvreader = csv.reader(inp, dialect=None, delimiter='\t', quoting=csv.QUOTE_NONE)
            header = next(csvreader)
            schema = self.kgtk_header_to_graph_table_schema(table, header)

            for vcol in vector_columns:
                if vcol not in header:
                    raise KGTKException(f"vector column '{vcol}' does not exist in {file}")
            for vcol in vector_columns:
                colvs = vstore.get_vector_store(table, vcol, index_spec=vector_spec)
                schema = colvs.get_graph_table_schema(schema)
                # TO DO: maybe rename and defer the drop until after import is successfully completed:
                colvs.drop_store_data()
            
            insert = None
            while True:
                chunk = list(itertools.islice(csvreader, self.VECTOR_IMPORT_CHUNKSIZE))
                for vcol in vector_columns:
                    colvs = vstore.get_vector_store(table, vcol)
                    chunk = colvs.import_vectors(header.index(vcol), chunk)
                    
                # if vector-adapted 'schema' is not None, add remaining/reformatted data fields to the graph cache:
                if schema is not None and insert is None:
                    insert = f'INSERT INTO {table} VALUES ({",".join(["?"] * len(schema.columns))})'
                    # defer this until we added some vectors to the cache in case anything goes wrong:
                    self.execute(self.get_table_definition(schema))
                if len(chunk) == 0:
                    break
                if schema is not None:
                    self.executemany(insert, chunk)

        vstore.commit()
        self.commit()
        return [vector_spec]

    def vector_column_to_sql(self, table, column, table_alias=None):
        """Return an SQL expression that can be used to generate the actual vectors
        corresponding to the vector-indexed 'column' variable of 'table'.
        """
        return self.get_vector_store().vector_column_to_sql(table, column, table_alias=table_alias)
    
                
    def shell(self, *commands):
        """Execute a sequence of sqlite3 shell 'commands' in a single invocation
        and return stdout and stderr as result strings.  These sqlite shell commands
        are not invokable from a connection object, they have to be entered via 'sh'.
        """
        # we can't easily guard this for readonly use, so for now we have
        # to rely on the fact that it is only used safely within this module:
        sqlite3 = sh.Command(self.get_sqlite_cmd())
        args = []
        for cmd in commands[0:-1]:
            args.append('-cmd')
            args.append(cmd)
        args.append(self.dbfile)
        args.append(commands[-1])
        proc = sqlite3(*args)
        return proc.stdout, proc.stderr

    def explain(self, sql_query, parameters=None, mode='plan'):
        """Generate a query execution plan explanation for 'sql_query' and return it as a string.
        If the query contains any parameter place holders, a set of actual 'parameters' needs to
        be supplied.  'mode' needs to be one of 'plan' (the default), 'full' or 'expert'.  Except
        for 'plan' mode, 'sql_query' may not contain any KGTK user function references.
        """
        if mode == 'plan':
            plan = self.get_query_plan(sql_query, parameters)
            return self.get_query_plan_description(plan)
        # for the other two modes we use an SQLite shell command which doesn't require parameters:
        elif mode == 'full':
            out, err = self.shell('EXPLAIN ' + sql_query)
        elif mode == 'expert':
            out, err = self.shell('.expert', sql_query)
        else:
            raise KGTKException('illegal explanation mode: %s' % str(mode))
        return out.decode('utf8')

    def get_query_plan(self, sql_query, parameters=None):
        """Return a list of query plan steps for 'sql_query' and 'parameters'.
        Each step is a tuple of id, parent_id and description string.
        """
        explain_cmd = 'EXPLAIN QUERY PLAN ' + sql_query
        parameters = parameters is not None and parameters or ()
        plan = []
        for node, parent, aux, desc in self.execute(explain_cmd, parameters):
            plan.append((node, parent, desc))
        return plan

    def get_query_plan_description(self, plan):
        """Return a textual description of a query 'plan' generated by 'get_query_plan'.
        This closely mirrors the top-level rendering of SQLite, but not exactly so.
        """
        node_depths = {}
        out = io.StringIO()
        out.write('QUERY PLAN\n')
        for node, parent, desc in plan:
            depth = node_depths.get(node)
            if depth is None:
                depth = node_depths.get(parent, 0) + 1
                node_depths[node] = depth
            out.write('|  ' * (depth-1))
            out.write('|--')
            out.write(desc)
            out.write('\n')
        return out.getvalue()

    def suggest_indexes(self, sql_query):
        explanation = self.explain(sql_query, mode='expert')
        indexes = []
        index_regex = re.compile(r'\s*CREATE\s+INDEX\s+(?P<name>[^\s]+)'
                                 + r'\s+ON\s+(?P<table>[^\s(]+)'
                                 + r'\s*\(\s*(?P<columns>[^\s,)]+(\s*,\s*[^\s,)]+)*)\s*\)',
                                 re.IGNORECASE)
        split_regex = re.compile(r'\s*,\s*')
        for line in explanation.splitlines():
            m = index_regex.match(line)
            if m is not None:
                name = m['name']
                table = m['table']
                columns = m['columns']
                columns = split_regex.split(columns)
                indexes.append((name, table, columns))
        return indexes


### Experiments:

"""
>>> store = cq.SqliteStore('/data/tmp/store.db', create=True)
>>> store.add_graph('kgtk/tests/data/kypher/graph.tsv')

>>> cq.pp.pprint(list(store.execute('select * from graph_1')))
[   ('Hans', 'loves', 'Molly', 'e11'),
    ('Otto', 'loves', 'Susi', 'e12'),
    ('Joe', 'friend', 'Otto', 'e13'),
    ('Joe', 'loves', 'Joe', 'e14'),
    ('Hans', 'name', '"Hans"', 'e21'),
    ('Otto', 'name', '"Otto"', 'e22'),
    ('Joe', 'name', '"Joe"', 'e23'),
    ('Molly', 'name', '"Molly"', 'e24'),
    ('Susi', 'name', '"Susi"', 'e25')]

>>> cq.pp.pprint(list(store.execute('select * from fileinfo')))
[   (   'kgtk/tests/data/kypher/graph.tsv',
        205,
        1597353182.1801062,
        None,
        None)]
>>> cq.pp.pprint(list(store.execute('select * from graphinfo')))
[   (   'graph_1',
        None,
        "['node1', 'label', 'node2', 'id']",
        4096,
        1598648612.7562318)]

>>> store.close()
"""

"""
# Large DB times and sizes:
#
# Summary:
# - Wikidata edges file, 1.15B edges, 16GB compressed, 78GB DB size, 20min import, 4.5min analyze
# - index on node1 column, 16.5min, 22GB DB growth, 1.25min analyze
# - analyze adds about 10% run/import time for index, 20% run/import time for table
# - full 4-column index doubles DB size, increases import time by 3.3x
# Optimizations:
# - we might be able to build a covering index for 'id' to save storage for one index
# - we could use 'id' as the primary key and build a 'without rowid' table
# - we could build two-column indexes: (node1, label), (label, node2), (node2, label)
# - we might forgo analyzing tables and only do it on indexes

# Wikidata edges file (1.15B edges):
> ls -l $EDGES
-rw-r--r-- 1 hans isdstaff 16379491562 Aug 14 18:12 /data/kgtk/wikidata/run3/wikidata-20200803-all-edges.tsv.gz

# Import:
> time kgtk --debug query -i $EDGES --graph-cache /data/tmp/store.db --limit 10
IMPORT graph data into table graph_1 from /data/kgtk/wikidata/run3/wikidata-20200803-all-edges.tsv.gz
  ..............
1517.701u 167.970s 20:14.79 138.7%	0+0k 29045920+153711296io 0pf+0w

# DB size:
> ls -l /data/tmp/store.db 
-rw-r--r-- 1 hans isdstaff 78699548672 Sep 11 00:00 /data/tmp/store.db

# Analyze graph table:
> time sqlite3 /data/tmp/store.db 'analyze graph_1'
30.410u 75.243s 4:23.90 40.0%	0+0k 153709096+40io 3pf+0w

# DB size:
> ls -l /data/tmp/store.db 
-rw-r--r-- 1 hans isdstaff 78699552768 Sep 11 09:39 /data/tmp/store.db

# Index creation on node1:
> time kgtk --debug query -i $EDGES --graph-cache /data/tmp/store.db \
       --match "edge: (p:Q52353442)-[r]->(y)" \
       --limit 1000
CREATE INDEX on table graph_1 column node1
  .............
699.576u 106.269s 16:30.38 81.3%	0+0k 190371536+104441192io 3424pf+0w

# DB size:
> ls -l /data/tmp/store.db 
-rw-r--r-- 1 hans isdstaff 100584587264 Sep 11 11:15 /data/tmp/store.db

# Analyze index:
> time sqlite3 /data/tmp/store.db 'analyze graph_1_node1_idx'
68.563u 6.544s 1:15.24 99.8%	0+0k 19904088+48io 0pf+0w
"""
