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
import copy

import sh

from   kgtk.exceptions import KGTKException
from   kgtk.kypher.utils import *
from   kgtk.kypher.kgtkinfo import KgtkInfoTable
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


# NOTES on DB names:
# - for code simplicity, we assume all internally defined and generated DB, table and
#   column names do not require SQL-quoting, while user-defined columns will need quoting
# - qualified table names needed to handle auxiliary DBs are so far only supported in
#   a very limited fashion to support read-only operation; operations that update the DB
#   do therefore not (yet) consider that table names might (need to) be qualified
    

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
    # a graph, in which case graphs should have their own external names.  The latest implementation
    # of INFO_TABLE as a schema-free KGTK table makes it easy to add new kinds of information over
    # time without invalidating the information stored in existing graph caches.

    INFO_TABLE = sdict[
        '_name_': 'kypher_master',
        'columns': sdict[
            'node1': sdict['_name_': 'node1', 'type': 'TEXT'],
            'label': sdict['_name_': 'label', 'type': 'TEXT'],
            'node2': sdict['_name_': 'node2', 'type': 'TEXT'],
            'id':    sdict['_name_': 'id',    'type': 'TEXT'],
        ],
        'without_rowid': False, # just for illustration
        'temporary': False,     # just for illustration
    ]

    def __init__(self, dbfile=None, create=False, loglevel=0,
                 conn=None, readonly=False, aux_dbfiles=None):
        """Open or create an SQLStore on the provided database file 'dbfile'
        or SQLite connection object 'conn'.  If 'dbfile' is provided and does
        not yet exist, it will only be created if 'create' is True.  Passing
        in a connection object directly provides more flexibility with creation
        options.  In that case any 'dbfile' value will be ignored and instead
        looked up directly from 'conn'.  'aux_dbfiles' can be one or more
        auxiliary DB files which will be attached to the main DB and can be
        queried in combination with tables in the main DB in read-only mode.
        """
        self.loglevel = loglevel
        self.dbfile = dbfile
        # generate a dict of db->dbfile, where we preserve the order and treat it like a path:
        self.aux_dbfiles = sdict([('db' + str(i+1), db) for i, db in enumerate(listify(aux_dbfiles))])
        self.conn = None
        self.init_conn = conn
        # for now force readonly mode if we have any auxiliary DBs; eventually we might
        # want to generalize this to still support updates to the main DB file:
        self.readonly = readonly or self.aux_dbfiles
        if not isinstance(self.init_conn, sqlite3.Connection):
            if self.init_conn is not None:
                raise KGTKException('invalid sqlite connection object: %s' % self.init_conn)
            if self.dbfile is None:
                raise KGTKException('no sqlite DB file or connection object provided')
            if not os.path.exists(self.dbfile) and (not create or readonly):
                raise KGTKException('sqlite DB file does not exist: %s' % self.dbfile)
        else:
            # finish setup for provided connection object (dbfile, aux_dbs, etc.):
            self.get_conn()
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
        if self.aux_dbfiles:
            self.infotable = MultiDbInfoTable(self, self.INFO_TABLE._name_)
        else:
            self.infotable = InfoTable(self, self.INFO_TABLE._name_)

    def describe_meta_tables(self, out=sys.stderr):
        """Describe the current content of the main internal bookkeeping tables to 'out'.
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
            if isinstance(self.init_conn, sqlite3.Connection):
                self.conn = self.init_conn
                self.dbfile = self.pragma('database_list')[0][2]
            elif self.readonly:
                self.conn = sqlite3.connect(f'file:{self.dbfile}?mode=ro', uri=True)
            else:
                self.conn = sqlite3.connect(self.dbfile)
                # use explicit transaction management via BEGIN/COMMIT:
                self.conn.isolation_level = None
            # attach any auxiliary DBs if we have them:
            for schema, dbfile in list(self.aux_dbfiles.items()):
                if not os.path.exists(dbfile):
                    # we don't want sqlite to create missing auxiliary DB files for us:
                    raise KGTKException(f'auxiliary sqlite DB file does not exist: {dbfile}')
                if os.path.realpath(dbfile) == os.path.realpath(self.dbfile):
                    # ignore any aux file that is the same as the main file so we can use wildcards more easily:
                    del self.aux_dbfiles[schema]
                    continue
                statement = f'ATTACH DATABASE {sql_quote_ident(dbfile)} AS {schema}'
                self.log(2, statement)
                self.execute(statement)
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

    READONLY_REGEX = re.compile(r'^\s*(select|explain|pragma|attach)\s', re.IGNORECASE)
    
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

    def in_transaction(self):
        """Return True if we are currently in the scope of a transaction.
        """
        return self.get_conn().in_transaction
            
    def ensure_transaction(self, type='DEFERRED'):
        """Ensure a transaction of 'type' has been started.  If we are currently
        inside a transaction, this is a no-op, which means a change of 'type'
        can only happen after a COMMIT has ended the current transaction.
        """
        if not self.in_transaction():
            self.log(2, f'BEGIN {type} TRANSACTION')
            self.execute(f'BEGIN {type} TRANSACTION')
            
    def commit(self):
        """Commit all updates of the current transaction to the database.
        This should only be called after complete and internally consistent
        top-level operations.
        """
        self.log(2, 'COMMIT updates to database...')
        if self.vector_store is not None:
            self.vector_store.commit()
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

    def get_table_dbfile(self, table_name):
        """Return the DB file where the data for 'table_name' resides.
        """
        db, table = self.parse_table_name(table_name)
        if db:
            # it must be a registered auxiliary DB:
            return self.aux_dbfiles[db]
        else:
            return self.dbfile

    def has_table(self, table_name):
        """Return True if a table with name 'table_name' exists in the store.
        """
        schema = self.MASTER_TABLE
        columns = schema.columns
        # for now we assume DB qualifiers always exist, but maybe we should test that also:
        db, table = self.parse_table_name(table_name)
        db = db + '.' if db else ''
        query = f"""SELECT COUNT(*) FROM {db}{schema._name_} WHERE {columns.name._name_}=?"""
        (cnt,) = self.execute(query, (table,)).fetchone()
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
        # for now we assume DB qualifiers always exist, but maybe we should test that also:
        db, table = self.parse_table_name(table_name)
        db = db + '.' if db else ''
        query = f"""SELECT {mcols.sql._name_} FROM {db}{master} 
                    WHERE {mcols.type._name_}='table' AND {mcols.name._name_}=?"""
        for (stmt,) in self.execute(query, (table,)):
            return stmt
        return None

    def get_table_indexes_sql(self, table_name):
        """Return the 'CREATE INDEX ... ON <table_name> ...' statements used to index this table.
        """
        master = self.MASTER_TABLE._name_
        mcols = self.MASTER_TABLE.columns
        # for now we assume DB qualifiers always exist, but maybe we should test that also:
        db, table = self.parse_table_name(table_name)
        db = db + '.' if db else ''
        query = f"""SELECT {mcols.sql._name_} FROM {db}{master} 
                    WHERE {mcols.type._name_}='index' AND {mcols.tbl_name._name_}=?"""
        return [stmt for (stmt,) in self.execute(query, (table,))]

    def sort_table(self, table_name, columns):
        """Sort the rows in table 'table_name' along one or more 'columns'.  Each column can be a simple
        column name or a full spec such as 'cast(node2 as int) desc' containing optional type coercion
        and sort directions (in which case the column name should be properly quoted if necessary).  This 
        creates a copy of 'table_name' into which the sorted rows will be inserted.  All indexes existing
        on the original table will also be recreated.  After sorting the freed up space from the original
        table and indexes is NOT automatically reclaimed.  To use it or free it either add additional
        data to the database or run the VACUUM command.  The value of sorting a table is primarily to
        create better data locality on disk, the sorted table will otherwise be identical to the original.
        NOTE: this may require 3-4x the size of the sorted table in temporary space, for that reason,
        use 'batched_sort_table' it at all possible.
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

    def batched_sort_table(self, table_name, columns, n=10, commit=True):
        """Sort the rows in table 'table_name' along one or more 'columns'.  Each column can be a simple
        column name or a full spec such as 'cast(node2 as int) desc' containing optional type coercion
        and sort directions (in which case the column name should be properly quoted if necessary).  
        This is a batched version of 'sort_table' (which see) which sorts 'n' slices of 'table_name'
        independently to reduce the amount of temporary and uncommitted space used (by default about
        10% of the size of 'table_name').  All indexes currently defined on 'table_name' will be updated
        incrementally, however, the fewer indexes defined on 'table_name', the faster this operation will be.
        If 'commit' (the default) each batch will be committed immediately after it was sorted to reduce
        the amount of temporary space needed.  If 'commit' is False, the space requirements will be similar
        to unbatched sorting.  Calling this should generally not generate any unused free space in the DB.
        The value of sorting a table is primarily to create better data locality on disk, the sorted table
        will otherwise be identical to the original.  The smaller the number of batches, the better the
        locality, however, for the cost of additional temporary space needed.
        """
        # - we tested this extensively to make sure that the sorted table is identical in content to the original
        # - locality of the batched table with n=10 seems to be generally good enough for our purposes
        
        # we look up the actual definition statement to get all the types and column features correct:
        table_def = self.get_table_definition_sql(table_name)
        if table_def is None:
            raise KGTKException(f"table '{table_name}' does not exist")
        table_ref = sql_quote_ident(table_name)
        table_columns = self.get_table_header(table_name)
        nrows = self.get_table_row_count(table_name)
        batch_size = int(nrows / n + 1.0)
        
        sorted_table = f'{table_name}_sortEd_'
        sorted_table_ref = sql_quote_ident(sorted_table)
        sorted_def = re.sub(r"""(?i)^\s*(CREATE\s+TABLE\s+)['"`]?""" + re.escape(table_name) + r"""['"`]?(\s+.*)""",
                            f'CREATE TEMPORARY TABLE {sorted_table_ref}\\2', table_def)
        if sorted_def == table_def:
            raise KGTKException(f"failed to sort '{table_name}', unexpected definition statement")
        sort_columns = [sql_quote_ident(col) if not re.search("""["` ]""", col) else col for col in listify(columns)]
        sort_stmt   = f"""INSERT INTO {sorted_table_ref} 
                          SELECT {', '.join(map(sql_quote_ident, table_columns))}
                          FROM {table_ref}
                          WHERE {table_ref}.rowid >= ? and {table_ref}.rowid < ?
                          ORDER BY {', '.join(sort_columns)}"""
        update_stmt = f"""UPDATE {table_ref}
                          SET {', '.join([f'{col} = {sorted_table_ref}.{col}' for col in map(sql_quote_ident, table_columns)])}
                          FROM {sorted_table_ref}
                          WHERE {table_ref}.rowid = ({sorted_table_ref}.rowid + ?)"""
        commit = commit and not self.in_transaction()
        start = 1
        for i in range(n):
            self.log(1, f"SORT table '{table_name}' batch {i+1} of {n}...")
            end = min(start + batch_size, nrows) + 1
            # each commit is on a single sorted batch which means if it succeeds
            # it keeps the table in a consistent state, even if things break later:
            if commit:
                self.ensure_transaction()
            self.execute(sorted_def)
            self.log(2, f'  sorting batch start={start} end={end}...')
            self.execute(sort_stmt, (start, end))
            self.log(2, '  updating table...')
            self.execute(update_stmt, (start - 1,))
            self.log(2, '  dropping temp table...')
            self.execute(f'DROP table {sorted_table_ref}')
            if commit:
                self.commit()
            start = end
            if start > nrows:
                break


    ### Schema manipulation:

    def parse_table_name(self, table_name):
        """Parse 'table_name' into its schema/DB and name components.
        If 'table_name' is unqualified, the DB component will be None.
        """
        parse = table_name.split('.', 1)
        if len(parse) == 1:
            return None, parse[0]
        else:
            return parse[0], parse[1]

    def is_qualified_table_name(self, table_name):
        """Return True if 'table_name' is qualified with a schema/DB namespace prefix.
        """
        db, table = self.parse_table_name(table_name)
        return db is not None

    def get_qualified_table_name(self, table_name, db=None, sep='.'):
        """Create a 'db'-qualified 'table_name'.  If 'db' is None, use any
        DB specified as part of 'table_name'.  Use 'sep' to separate the DB
        from the 'table_name' it qualifies.  If no DB is supplied or attached
        to 'table_name', simply return the unqualified 'table_name'.
        """
        _db, name = self.parse_table_name(table_name)
        db = db or _db
        return (db + sep if db else '') + name

    def get_unqualified_table_name(self, table_name):
        """Strip off any DB qualifiers from 'table_name' and return the result.
        """
        return self.parse_table_name(table_name)[1]
    
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
        info = self.infotable.get_file_info(file)
        if info is None and not exact:
            file = self.normalize_file_path(file)
            info = self.infotable.get_file_info(file)
        if info is None and alias is not None:
            info = self.infotable.get_file_info(alias)
        return info

    def get_normalized_file(self, file, alias=None, exact=False):
        """Return the stored normalized name of 'file' (or 'alias') or None
        if this file does not exist in the file table.
        """
        info = self.get_file_info(file, alias=alias, exact=exact)
        return info and info.file or None
        
    def set_file_info(self, _file, **kwargs):
        # TRICKY: we use '_file' so we can also use and update 'file' in 'kwargs'
        self.infotable.set_file_info(_file, kwargs)

    def update_file_info(self, _file, **kwargs):
        self.infotable.update_file_info(_file, kwargs)
        
    def drop_file_info(self, file):
        """Delete the file info record for 'file'.
        IMPORTANT: this does not delete any graph data associated with 'file'.
        """
        self.infotable.drop_file_info(file)
        
    def describe_file_info(self, file, out=sys.stderr):
        """Describe a single 'file' (or its info) to 'out'.
        """
        info = isinstance(file, dict) and file or self.get_file_info(file)
        out.write('%s:\n' % info.file)
        out.write('  size:  %s' % (info.size and format_memory_size(int(info.size)) or '???   '))
        out.write('   \tmodified:  %s' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(info.modtime))))
        out.write('   \tgraph:  %s\n' % info.graph)
        if info.comment:
            out.write('  comment:  %s\n' % info.comment)

    def describe_file_info_table(self, out=sys.stderr):
        """Describe all files in the INFO_TABLE to 'out'.
        """
        for info in self.infotable.get_all_file_infos():
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
        files = self.infotable.get_objects(table_name, InfoTable.graph)
        return [self.infotable.get_value(f, InfoTable.file) for f in files]


    ### Graph information and access:

    # TO DO: add 'bump_timestamp' so we can easily track when this graph was last used
    #        add 'update_xxx_info' methods that only change not None fields
    
    def get_graph_info(self, table_name):
        """Return a dict info structure for the graph stored in 'table_name' (there can only be one),
        or None if this graph does not exist in the graph table.  All column keys will be set
        although some values may be None.
        """
        return self.infotable.get_graph_info(table_name)

    def set_graph_info(self, table_name, **kwargs):
        self.infotable.set_graph_info(table_name, kwargs)
    
    def update_graph_info(self, table_name, **kwargs):
        self.infotable.update_graph_info(table_name, kwargs)
        
    def drop_graph_info(self, table_name):
        """Delete the graph info record for 'table_name'.
        IMPORTANT: this does not delete any graph data stored in 'table_name'.
        """
        self.infotable.drop_graph_info(table_name)

    def describe_graph_info(self, graph, out=sys.stderr):
        """Describe a single 'graph' (or its info) to 'out'.
        """
        info = isinstance(graph, dict) and graph or self.get_graph_info(graph)
        out.write('%s:\n' % info.name)
        out.write('  size:  %s' % format_memory_size(int(info.size)))
        out.write('   \tcreated:  %s\n' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(info.acctime))))
        out.write('  header:  %s\n' % info.header)

    def describe_graph_info_table(self, out=sys.stderr):
        """Describe all graphs in the INFO_TABLE to 'out'.
        """
        for info in self.infotable.get_all_graph_infos():
            self.describe_graph_info(info, out=out)

    def get_graph_table_schema(self, table_name):
        """Get a graph table schema definition for graph 'table_name'.
        """
        info = self.get_graph_info(table_name)
        header = eval(info.header)
        return self.kgtk_header_to_graph_table_schema(table_name, header)

    def get_graph_indexes(self, table_name):
        """Return the list of indexes currently defined for graph 'table_name'.
        """
        info = self.get_graph_info(table_name)
        if info is None:
            # see if 'table_name' is a defined or loaded virtual table function:
            if SqlFunction.is_virtual_graph(table_name) or table_name in self.get_user_functions():
                return []
            raise KGTKException(f"INTERNAL ERROR: missing graph info for '{table_name}'")
        indexes = [ispec.TableIndex.decode(idx) for idx in listify(info.index)]
        if self.is_qualified_table_name(table_name) and indexes:
            # record the database the tables of this index are stored in:
            db = self.parse_table_name(table_name)[0]
            for idx in indexes:
                idx.db = db
        return indexes

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
        return [idx for idx in self.get_graph_indexes(table_name) if isinstance(idx, ispec.VectorIndex)]

    def is_vector_column(self, table_name, column):
        """Return True if 'column' in 'table_name' is a vector column.
        """
        for vindex in self.get_vector_indexes(table_name):
            if column in vindex.index.columns:
                return True
        else:
            return False

    def ensure_graph_index(self, table_name, index, explain=False, commit=True):
        """Ensure a qualifying 'index' for 'table_name' already exists or gets created.
        Checks whether the existing index is at least as selective as requested, for
        example, an existing index on columns (node1, node2) will qualify even if 'index'
        has 'node1' as its only column.
        """
        if not self.has_graph_index(table_name, index):
            if self.readonly:
                return
            for col in index.get_columns():
                if self.is_vector_column(table_name, col):
                    # do not index any vector columns:
                    return
            self.ensure_transaction()
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
            ginfo.size = int(ginfo.size) + idxsize
            if not explain:
                # we may have added/deleted some, so recompute the list:
                indexes = self.get_graph_indexes(table_name) + [index]
                indexes = [ispec.TableIndex.encode(idx) for idx in indexes]
                self.update_graph_info(table_name, index=indexes)
                self.update_graph_info(table_name, size=ginfo.size)
                if commit:
                    # top-level OP, commit DB and info updates:
                    self.commit()

    def ensure_graph_index_for_columns(self, table_name, columns, unique=False, explain=False, commit=True):
        """Ensure an index for 'table_name' on 'columns' already exists or gets created.
        Checks whether the existing index is at least as selective as requested, for example,
        an existing index on columns (node1, node2) will qualify even if only node1 is requested.
        """
        index = self.get_table_index(table_name, columns, unique=unique)
        self.ensure_graph_index(table_name, index, explain=explain, commit=commit)

    def number_of_graphs(self):
        """Return the number of graphs currently stored in 'self'.
        """
        return len(self.infotable.get_objects('graph', InfoTable.type))

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
            if int(info.size) !=  os.path.getsize(file):
                return 'replace'
            if float(info.modtime) != os.path.getmtime(file):
                return 'replace'
            # don't check md5sum for now
        return 'reuse'

    def has_graph(self, file, alias=None):
        """Return True if the KGTK graph represented/named by 'file' (or its 'alias' if not None)
        has already been imported and is up-to-date (see 'determine_graph_action' for the full story).
        """
        return self.determine_graph_action(file, alias=alias, error=False) == 'reuse'

    def add_graph(self, file, alias=None, index_specs=None, append=None, commit=True):
        """Import a graph from 'file' (and optionally named by 'alias') unless a matching
        graph has already been imported earlier according to 'has_graph' (which see).
        'index_specs' is a list of index specifications relevant to the import of this graph.
        'append' can be one or more files whose data should be appended to the graph identified
        by 'file'.  If any to-be-appended file already exists in the info table, it will simply
        be ignored and the data reused.  Updating of appended data is not supported, however,
        the whole graph can be replaced with data from a new 'file'.  Appended data needs
        to match the columns of the data that it is appended to, however, no other checking
        for duplicates, etc. is performed.  Data is simply treated as if it had been appended
        to the original data file.  Reordering of columns is supported for the cost of some
        import speed.
        """
        # TO DO: make this less messy and hairy...
        graph_action = self.determine_graph_action(file, alias=alias)
        file_info = self.get_file_info(file, alias=alias)

        # determine what we have to do with the supplied file if anything:
        if graph_action == 'reuse':
            if alias is not None:
                # this allows us to do multiple renamings (no-op if we are readonly):
                self.set_file_alias(file, alias)
        if self.readonly and graph_action != 'reuse':
            raise KGTKException(f"cannot import or update {file} in read-only mode")

        # determine the graph table we are operating on:
        if graph_action != 'reuse':
            table = self.new_graph_table()
        else:
            table = file_info.graph

        # vector tables are handled in two steps, vector data import and indexing, and we have
        # to figure out whether one or both steps need to be redone upon index redefinition:
        vector_spec = self.get_vector_index_specs(table, index_specs)
        vector_spec = self.normalize_vector_index_specs(table, vector_spec) if vector_spec else None
        if graph_action == 'reuse' and vector_spec and not self.readonly:
            for idx in self.get_vector_indexes(table):
                if vector_spec.redefines_store(idx):
                    graph_action = 'replace'
                    table = self.new_graph_table()
                    vector_spec.table = table
                    break

        if graph_action != 'reuse':
            # import main data:
            self.add_graph_data(table, file, alias=alias, index_specs=index_specs, append=False)
        if graph_action == 'replace':
            # delete any old graph data *after* we replaced with new version to not lose anything in case of error:
            # TRICKY: we already pointed the new file_info.graph to the new table, so it won't be deleted here:
            self.drop_graph(file_info.graph)

        if vector_spec:
            # handle step 2 of vector index creation:
            self.ensure_graph_index(table, vector_spec, commit=False)
        if commit and self.in_transaction():
            # top-level OP, commit successful DB, index and info updates:
            if vector_spec:
                self.get_vector_store().commit()
            self.commit()

        # append any additional data files:
        for afile in listify(append):
            graph_action = self.determine_graph_action(afile)
            file_info = self.get_file_info(afile)
            if graph_action == 'replace':
                if self.readonly:
                    graph_action = 'reuse'
                else:
                    raise KGTKException(f"cannot replace {afile} in append mode")
            if graph_action == 'reuse' and file_info.graph != table:
                # each file must correspond to exactly one graph:
                raise KGTKException(f"{afile} is already in use by a different graph: {table}")
            if graph_action == 'add':
                self.add_graph_data(table, afile, index_specs=index_specs, append=True)
                if commit:
                    # top-level OP, commit successful DB and info updates:
                    self.commit()

    def add_graph_data(self, table, file, alias=None, index_specs=None, append=False):
        """Low-level implementation of 'add_graph'.  Import data for graph 'table' from 'file'
        or add it to an existing graph if 'append' is True.  Uses a fast direct import
        if possible, otherwise falls back on a 2x slower csv.reader-based import of the data.
        'index_specs' is a list of index specifications relevant to the import of this graph.
        """
        file = self.normalize_file_path(file)
        oldsize = self.get_db_size()
        vector_specs = self.get_vector_index_specs(table, index_specs)
        if len(vector_specs) > 0:
            if append:
                raise KGTKException('cannot append to vector data')
            self.ensure_transaction()
            # perform step 1 of vector data import, step 2 indexing is done by the caller:
            self.import_graph_vector_data_via_csv(table, file, index_specs=vector_specs)
        else:
            # fast import runs in a separate process at the shell level, so we cannot use it here
            # if we are currently inside a transaction on this connection, since the DB will be locked
            # TRANSACTION NOTES: this will still generally do the right thing with cleanup, even though it
            # runs in its own process and transaction handling; here are the worst things that might happen:
            # 1. the data table was created but then the import phase was interrupted somehow, and we wind
            #    up with an empty graph 'table' which will simply be ignored after that
            # 2. all the data gets imported but then something goes wrong during the info table update
            #    which means the graph table is full but will be ignored down the road; if this happens
            #    during append, the info table will have incorrect size/timestamp but otherwise be correct;
            #    the window for that is extremely small and chances for that to happen are very low
            # 3. if the data import phase gets interrupted, the database will have produced a journal file
            #    which will rollback the partial import during the next call to sqlite on this graph cache
            # so the only case that might need some cleanup is case 2 which doesn't corrupt anything
            # but just wastes space, so that could be deferred to be handled manually for now
            fast_import = False
            if not self.in_transaction():
                try:
                    # try fast shell-based import first, but if that is not applicable or supported...
                    fast_import = self.import_graph_data_via_import(table, file, append=append)
                except (KGTKException, sh.CommandNotFound):
                    pass
            self.ensure_transaction()
            if not fast_import:
                # ...fall back on CSV-based import which is more flexible but about 2x slower:
                self.import_graph_data_via_csv(table, file, append=append)
        graphsize = self.get_db_size() - oldsize
        # this isn't really needed, but we store it for now:
        header = str(self.get_table_header(table))
        if self.is_standard_input(file):
            self.set_file_info(file, size=0, modtime=time.time(), graph=table)
        else:
            self.set_file_info(file, size=os.path.getsize(file), modtime=os.path.getmtime(file), graph=table)
        if append:
            # just update changed size and access time:
            ginfo = self.get_graph_info(table)
            self.set_graph_info(table, size=int(ginfo.size)+graphsize, acctime=time.time())
        else:
            self.set_graph_info(table, header=header, size=graphsize, acctime=time.time())
        if alias is not None:
            self.set_file_alias(file, alias)
            
    def drop_graph(self, table_name):
        """Delete the graph 'table_name' and all its associated info records.
        """
        if self.readonly:
            return
        self.log(1, f'DROP graph data table {table_name}')
        # delete any remaining supporting file infos pointing to 'table_name':
        for file in self.get_graph_files(table_name):
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
        indexes = [ispec.TableIndex.encode(idx) for idx in indexes]
        ginfo.size = int(ginfo.size) - idxsize
        self.update_graph_info(table_name, index=indexes, size=ginfo.size)

    def drop_graph_indexes(self, table_name, index_type=None, commit=True):
        """Delete all indexes for graph 'table_name'.  If 'index_type' is not None,
        restrict to indexes of that type (can be a short name or a class).
        """
        self.ensure_transaction()
        if isinstance(index_type, str):
            index_type = ispec.TableIndex.get_index_type_class(index_type)
        for index in self.get_graph_indexes(table_name)[:]:
            if index_type is None or isinstance(index, index_type):
                self.drop_graph_index(table_name, index)
        if commit:
            # top-level OP, commit DB and info updates:
            self.commit()


    ### Data import:
    
    def import_graph_data_via_csv(self, table, file, append=False):
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
            column_list = ''
            if append:
                if self.has_table(table):
                    table_header = self.get_table_header(table)
                    if set(table_header) != set(header):
                        raise KGTKException('can only append data with the same set of columns')
                    if table_header != header:
                        # new data columns are in a different order, so we need an explicit column list:
                        column_list = f' ({self.get_full_column_list(self.kgtk_header_to_graph_table_schema(table, header))})'
                else:
                    append = False
            if not append:
                self.execute(self.get_table_definition(schema))
            insert = f'INSERT INTO {table}{column_list} VALUES ({",".join(["?"] * len(header))})'
            self.executemany(insert, csvreader)

    def import_graph_data_via_import(self, table, file, append=False):
        """Use the sqlite shell and its import command to import 'file' into 'table'.
        This will be about 2+ times faster and can exploit parallelism for decompression.
        This is only supported for Un*x for now and requires a named 'file'.
        Return True if the import finished successfully, raise exception otherwise.
        """
        if self.readonly:
            return True
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
            if append:
                if self.has_table(table):
                    if self.get_table_header(table) != header:
                        raise KGTKException('can only fast-append data with identical columns')
                else:
                    append = False
            if not append:
                # create the table in a separate process and not on the local connection
                # to not create any locking issues with local transactions:
                sqlite3(self.dbfile, self.get_table_definition(schema))
        
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
        return True

                
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
        # make sure we close any open files:
        vstore.close()

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
            # we could run this similar to 'get_query_plan', but we won't get all the detail to display:
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


class InfoTable(KgtkInfoTable):
    """Schema-free info table using a fine-grained KGTK edge data model.
    All node1/label/node2/id values are stored as strings, so any conversions
    of numbers, etc. need to be handled explicitly by the user of this table.
    """

    # we mostly use the old column headers as labels for simplicity:
    acctime = 'acctime'
    comment = 'comment'
    file = 'file'
    graph = 'graph'
    header = 'header'
    index = 'index'
    md5sum = 'md5sum'
    modtime = 'modtime'
    name = 'name'
    shasum = 'shasum'
    size = 'size'
    type = 'type'
    # this is a 'virtual' attribute used when reading auxiliary DBs which should never get written:
    db = 'db'

    # info object templates:
    FILE_INFO = sdict([(key, None) for key in [type, file, size, modtime, graph, comment, db]])
    GRAPH_INFO = sdict([(key, None) for key in [type, name, header, size, acctime, index, db]])

    def init_table(self):
        """If the info table doesn't exist yet, define it from its schema.
        """
        if not self.store.has_table(self.table):
            if self.store.is_qualified_table_name(self.table):
                raise KGTKException('cannot define or upgrade auxiliary DB info table: {self.table}')
            self.store.ensure_transaction()
            super().init_table()
            self.transfer_fileinfo()
            self.transfer_graphinfo()
            self.store.commit()

    def make_file_id(self, path):
        """Create a new file object ID for the file with 'path'.
        Note that this creates a new ID upon every call, regardless of 'path'.
        """
        return self.make_object_id('file-')

    def transfer_fileinfo(self):
        """Transfer information from an old-style fileinfo table.
        """
        store = self.store
        import kgtk.kypher.infotable as oldit
        if store.has_table(oldit.FILE_TABLE._name_):
            fileinfo = oldit.InfoTable(store, oldit.FILE_TABLE)
            for info in fileinfo.get_all_infos():
                self.set_file_info(info.file, info)

    def transfer_graphinfo(self):
        """Transfer information from an old-style graphinfo table.
        """
        store = self.store
        import kgtk.kypher.infotable as oldit
        if store.has_table(oldit.GRAPH_TABLE._name_):
            graphinfo = oldit.InfoTable(store, oldit.GRAPH_TABLE)
            for info in graphinfo.get_all_infos():
                # translate index list into multi-valued edge:
                info[InfoTable.index] = [ispec.TableIndex.encode(idx) for idx in ispec.TableIndex.decode(info.indexes)]
                del info['indexes']
                self.set_graph_info(info.name, info)

    # TO DO: add LRU caching and maintenance
    def get_info(self, obj, info=None):
        """Retrieve all edges that start with 'obj' and create a dict from their
        'label/node2' value pairs.  Multi-valued labels will be converted into lists.
        If 'info' is provided, populate it instead of creating a new dict.
        """
        info = info if info is not None else sdict()
        for _, key, value, _ in self.get_edges(obj):
            if info.get(key) is not None:
                info[key] = listify(info[key]) + [value]
            else:
                info[key] = value
        return info if len(info) > 0 else None

    def set_info(self, obj, info):
        """Set edge values for 'obj' based on non-null key/value pairs in 'info'.
        List values will automatically be translated into multi-valued edges.
        This coerces all values to strings to avoid precision issues with floats.
        """
        for key, value in info.items():
            if value is None:
                continue
            if not isinstance(value, str) and hasattr(value, '__iter__'):
                # we have a multi-valued attribute:
                for i, val in enumerate(value):
                    if i == 0:
                        self.set_value(obj, key, str(val))
                    else:
                        self.add_value(obj, key, str(val))
            else:
                self.set_value(obj, key, str(value))
    
    def update_info(self, obj, info):
        """Just like 'set_info' but a no-op if 'obj' does not exist in the table.
        """
        for edge in self.get_edges(obj):
            self.set_info(obj, info)
            return
    
    def drop_info(self, obj):
        """Delete all edges that have 'obj' as their node1.
        """
        self.delete_edges(obj)
        

    def get_file_info(self, path):
        """Return a dict info structure for the file with 'path' (there can only be one),
        or None if this file does not exist in the info table.  All supported keys will
        be set although some values may be None.
        """
        file = self.get_object(path, InfoTable.file)
        return self.get_info(file, info=copy.deepcopy(self.FILE_INFO)) if file is not None else None

    def set_file_info(self, path, info):
        """Set all 'info' for the file with 'path'.  Create a new file ID if necessary.
        """
        file = self.get_object(path, InfoTable.file)
        if file is None:
            # new file, generate a new object ID for it (this will be different for every call even
            # if called with the same path, which is important for files like /dev/stdin where we
            # we do not want to accidentally create an already existing file ID that points to an alias):
            file = self.make_file_id(path)
            info[InfoTable.file] = path
            # also report the type:
            info[InfoTable.type] = 'file'
        self.set_info(file, info)
    
    def update_file_info(self, path, info):
        file = self.get_object(path, InfoTable.file)
        if file is not None:
            self.update_info(file, info)
    
    def drop_file_info(self, path):
        """Delete the graph info record for the file with 'path'.
        """
        file = self.get_object(path, InfoTable.file)
        if file is not None:
            self.drop_info(file)

            
    def get_graph_info(self, graph):
        """Return a dict info structure for 'graph' (there can only be one), or None
        if this graph does not exist in the info table.  All supported keys will be set
        although some values may be None.
        """
        return self.get_info(graph, info=copy.deepcopy(self.GRAPH_INFO))

    def set_graph_info(self, graph, info):
        info[InfoTable.type] = 'graph'
        # add a default 'name' attribute:
        info[InfoTable.name] = info.get(InfoTable.name, graph)
        self.set_info(graph, info)
    
    def update_graph_info(self, graph, info):
        self.update_info(graph, info)
        
    def drop_graph_info(self, graph):
        """Delete the graph info record for 'table_name'.
        """
        self.drop_info(graph)
        
    
    def get_all_infos(self, type=None):
        infos = []
        for obj in self.get_all_objects():
            info = None
            if type == 'file':
                info = copy.deepcopy(self.FILE_INFO)
            elif type == 'graph':
                info = copy.deepcopy(self.GRAPH_INFO)
            info = self.get_info(obj, info=info)
            if type == None or info.type == type:
                infos.append(info)
        return infos

    def get_all_file_infos(self):
        return self.get_all_infos(type='file')

    def get_all_graph_infos(self):
        return self.get_all_infos(type='graph')


class MultiDbInfoTable(InfoTable):
    """Variant of 'InfoTable' that also supports limited read-only access to the
    info tables of any attached auxiliary DBs.  The main and auxiliary info tables
    are treated similar to a path.  Objects with the same name might exist in multiple
    tables, in which case the info from the first table in the path will be used.
    """

    def init_table(self):
        """If the info table doesn't exist yet, define it from its schema.
        """
        super().init_table()
        # read info tables from all auxiliary DBs:
        self.aux_infotables = sdict([(db, InfoTable(self.store, f'{db}.{self.table}')) for db in self.store.aux_dbfiles.keys()])

    def get_file_info(self, path):
        """Return a dict info structure for the file with 'path' (there can only be one).
        If file is not found in the main info table, try to find the first auxiliary info table
        where it is defined and qualify the associated graph with the respective DB prefix.
        Return None if this file does not exist in any info table.  All supported keys will
        be set although some values may be None.
        """
        info = None
        file = self.get_object(path, InfoTable.file)
        if file is None:
            for db, itable in self.aux_infotables.items():
                file = itable.get_object(path, InfoTable.file)
                if file is not None:
                    info = itable.get_info(file, info=copy.deepcopy(self.FILE_INFO))
                    if info.graph:
                        # qualify the graph with the DB prefix so we will later
                        # lookup its info from the appropriate aux info table:
                        info.graph = f'{db}.{info.graph}'
                    # record virtual DB attribute which will never get written out:
                    info.db = db
                    break
        else:
            info = self.get_info(file, info=copy.deepcopy(self.FILE_INFO))
        return info

    def get_graph_info(self, graph):
        """Return a dict info structure for 'graph' (there can only be one).  'graph' may
        be qualified in which case the info table from the respective auxiliary DB will be used.
        Return None if this graph does not exist in the relevant info table.  All supported
        keys will be set although some values may be None.  Note that this does not search
        through all info tables, since graph names by themselves are meaningless, they only
        get identity through the file(s) they are linked to.
        """
        db, table = self.store.parse_table_name(graph)
        if db is not None:
            info = self.aux_infotables[db].get_info(table, info=copy.deepcopy(self.GRAPH_INFO))
            # record virtual DB attribute which will never get written out:
            info.db = db
            return info
        else:
            return super().get_graph_info(graph)

    def set_info(self, obj, info):
        # safety precaution to make sure the db attribute never gets written out:
        info.db = None
        super().set_info(obj, info)


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
