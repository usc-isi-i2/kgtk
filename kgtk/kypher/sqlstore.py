"""
SQLStore to support Kypher queries over KGTK graphs.
"""

import sys
import os.path
import sqlite3
# sqlite3 already loads math, so no extra cost:
import math
from   odictliteral import odict
import time
import csv
import re
from   functools import lru_cache
import pprint

import sh

# this is expensive to import (120ms), so maybe make it lazy:
from   kgtk.value.kgtkvalue import KgtkValue
from   kgtk.exceptions import KGTKException

pp = pprint.PrettyPrinter(indent=4)


### TO DO:

# o automatically run ANALYZE on tables and indexes when they get created
#   - we decided to only do this for indexes for now
# - support naming of graphs which would allow deleting of the source data
#   as well as graphs fed in from stdin
# + absolute file names are an issue when distributing the store
# - support some minimal sanity checking such as empty files, etc.
# - handle column name dealiasing and normalization
# - explanation runs outside the sqlite connection and thus does not see
#   user functions such as kgtk_stringify and friends which causes errors;
#   see if we can fix this somehow
# - support declaring and dropping of (temporary) graphs that are only used
#   once or a few times
# - allow in-memory graphs, or better, support memory-mapped IO via
#   PRAGMA mmap_size=NNN bytes, which would be transparent and usable on demand
# - support other DB maintenance ops such as drop, list, info, etc.
# - see how we could better support fine-grained querying via prepared statements
#   and persistent connections that avoid the KGTK startup overhead, or scripts
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


### Utilities

# TO DO: I am sure some form of this already exists somewhere in Craig's code

def open_to_read(file, mode='rt'):
    """Version of 'open' that is smart about different types of compressed files
    and file-like objects that are already open to read.  'mode' has to be a
    valid read mode such as 'r', 'rb' or 'rt'.
    """
    assert mode in ('r', 'rb', 'rt'), 'illegal read mode'
    enc = 't' in mode and 'utf8' or None
    if isinstance(file, str) and file.endswith('.gz'):
        import gzip
        return gzip.open(file, mode, encoding=enc)
    elif isinstance(file, str) and file.endswith('.bz2'):
        import bz2
        return bz2.open(file, mode, encoding=enc)
    elif isinstance(file, str) and file.endswith('.xz'):
        import lzma
        return lzma.open(file, mode, encoding=enc)
    elif hasattr(file, 'read'):
        return file
    else:
        return open(file, mode)

def open_to_write(file, mode='wt'):
    """Version of 'open' that is smart about different types of compressed files
    and file-like objects that are already open to write.  'mode' has to be a
    valid write mode such as 'w', 'wb' or 'wt'.
    """
    assert mode in ('w', 'wb', 'wt'), 'illegal write mode'
    enc = 't' in mode and 'utf8' or None
    if isinstance(file, str) and file.endswith('.gz'):
        import gzip
        return gzip.open(file, mode, encoding=enc)
    elif isinstance(file, str) and file.endswith('.bz2'):
        import bz2
        return bz2.open(file, mode, encoding=enc)
    elif isinstance(file, str) and file.endswith('.xz'):
        import lzma
        return lzma.open(file, mode, encoding=enc)
    elif hasattr(file, 'write'):
        return file
    else:
        return open(file, mode)

def get_cat_command(file, _piped=False):
    """Return a cat-like sh-command to copy the possibly compressed 'file' to stdout.
    """
    # This works around some cross-platform issues with similar functionality in zconcat.
    if file.endswith('.gz'):
        return sh.gunzip.bake('-c', file, _piped=_piped)
    elif file.endswith('.bz2'):
        return sh.bunzip2.bake('-c', file, _piped=_piped)
    elif file.endswith('.xz'):
        return sh.unxz.bake('-c', file, _piped=_piped)
    else:
        return sh.cat.bake(file, _piped=_piped)


### SQL Store

class SqlStore(object):
    """SQL database capable of storing one or more KGTK graph files as individual tables
    and allowing them to be queried with SQL statements.
    """
    # This is just an abstract place-holder for now.  Once we complete SqliteStore
    # and generalize this to other SQL DB(s), we'll move API-level methods up here.
    pass


def sql_quote_ident(ident):
    # - standard SQL quoting for identifiers such as table and column names is via double quotes
    # - double quotes within identifiers can be escaped via two double quotes
    # - sqlite also supports MySQL's backtick syntax and SQLServer's [] syntax
    return '"' + ident.replace('"', '""') + '"'

class sdict(odict):
    """Ordered schema dict that supports property access of its elements.
    """
    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def __setattr__(self, name, value):
        self[name] = value
        

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
    
    FILE_TABLE = sdict[
        '_name_': 'fileinfo',
        'columns': sdict[
            'file':    sdict['_name_': 'file',    'type': 'TEXT', 'key': True, 'doc': 'real path of the file containing the data'],
            'size':    sdict['_name_': 'size',    'type': 'INTEGER'],
            'modtime': sdict['_name_': 'modtime', 'type': 'FLOAT'],
            'md5sum':  sdict['_name_': 'md5sum',  'type': 'TEXT'],
            'graph':   sdict['_name_': 'graph',   'type': 'TEXT', 'doc': 'the graph defined by the data of this file'],
        ]
    ]

    GRAPH_TABLE = sdict[
        '_name_': 'graphinfo',
        'columns': sdict[
            'name':    sdict['_name_': 'name',    'type': 'TEXT', 'key': True, 'doc': 'name of the table representing this graph'],
            'shasum':  sdict['_name_': 'shasum',  'type': 'TEXT', 'doc': 'table hash computed by sqlite shasum command'],
            'header':  sdict['_name_': 'header',  'type': 'TEXT'],
            'size':    sdict['_name_': 'size',    'type': 'INTEGER', 'doc': 'total size in bytes used by this graph including indexes'],
            'acctime': sdict['_name_': 'acctime', 'type': 'FLOAT', 'doc': 'last time this graph was accessed'],
        ]
    ]

    def __init__(self, dbfile=None, create=False, loglevel=0, conn=None):
        """Open or create an SQLStore on the provided database file 'dbfile'
        or SQLite connection object 'conn'.  If 'dbfile' is provided and does
        not yet exist, it will only be created if 'create' is True.  Passing
        in a connection object directly provides more flexibility with creation
        options.  In that case any 'dbfile' value will be ignored.
        """
        self.loglevel = loglevel
        self.dbfile = dbfile
        self.conn = conn
        if not isinstance(self.conn, sqlite3.Connection):
            if self.conn is not None:
                raise KGTKException('invalid sqlite connection object: %s' % self.conn)
            if self.dbfile is None:
                raise KGTKException('no sqlite DB file or connection object provided')
            if not os.path.exists(self.dbfile) and not create:
                raise KGTKException('sqlite DB file does not exist: %s' % self.dbfile)
        self.user_functions = set()
        self.init_meta_tables()
        self.configure()

    def log(self, level, message):
        if self.loglevel >= level:
            header = '[%s sqlstore]:' % time.strftime('%Y-%m-%d %H:%M:%S')
            sys.stderr.write('%s %s\n' % (header, message))
            sys.stderr.flush()

    def init_meta_tables(self):
        if not self.has_table(self.FILE_TABLE._name_):
            self.execute(self.get_table_definition(self.FILE_TABLE))
        if not self.has_table(self.GRAPH_TABLE._name_):
            self.execute(self.get_table_definition(self.GRAPH_TABLE))

    CACHE_SIZE = 2 ** 32 # 4GB

    def configure(self):
        """Configure various settings of the store.
        """
        self.pragma('main.cache_size = %d' % int(self.CACHE_SIZE / self.pragma('page_size')))


    ### DB control:

    def get_conn(self):
        if self.conn is None:
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

    def execute(self, *args, **kwargs):
        return self.get_conn().execute(*args, **kwargs)

    def executemany(self, *args, **kwargs):
        return self.get_conn().executemany(*args, **kwargs)

    def commit(self):
        self.get_conn().commit()

    def pragma(self, expression):
        """Evaluate a PRAGMA 'expression' and return the result (if any).
        """
        res = list(self.execute('PRAGMA ' + expression))
        if len(res) == 0:
            return None
        elif len(res) == 1:
            return res[0][0]
        else:
            return res


    ### DB functions:

    USER_FUNCTIONS = {}
    AGGREGATE_FUNCTIONS = ('AVG', 'COUNT', 'GROUP_CONCAT', 'MAX', 'MIN', 'SUM', 'TOTAL')

    @staticmethod
    def register_user_function(name, num_params, func, deterministic=False):
        name = name.upper()
        SqliteStore.USER_FUNCTIONS[name] = {'name': name, 'num_params': num_params, 'func': func, 'deterministic': deterministic}

    @staticmethod
    def is_user_function(name):
        name = name.upper()
        return SqliteStore.USER_FUNCTIONS.get(name) is not None

    def load_user_function(self, name, error=True):
        name = name.upper()
        if name in self.user_functions:
            return
        elif self.is_user_function(name):
            info = self.USER_FUNCTIONS.get(name)
            # Py 3.8 or later:
            #self.get_conn().create_function(info['name'], info['num_params'], info['func'], deterministic=info['deterministic'])
            self.get_conn().create_function(info['name'], info['num_params'], info['func'])
            self.user_functions.add(name)
        elif error:
            raise KGTKException('No user-function has been registered for: ' + str(name))

    def is_aggregate_function(self, name):
        """Return True if 'name' is an aggregate function supported by this database.
        """
        return name.upper() in self.AGGREGATE_FUNCTIONS


    ### DB properties:
    
    def get_db_size(self):
        """Return the size of all currently allocated data pages in bytes.  This maybe smaller than
        the size of the database file if there were deletions that put pages back on the free list.
        Free pages can be reclaimed by running 'VACUUM', but that might require a substantial amount
        of available disk space if the current DB file is large.
        """
        return (self.pragma('page_count') - self.pragma('freelist_count')) * self.pragma('page_size')

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
        for (cnt,) in self.execute('SELECT COUNT(*) FROM %s' % table_name):
            return cnt
        return 0
    

    ### Schema manipulation:
    
    def kgtk_header_to_graph_table_schema(self, table_name, header):
        columns = sdict()
        for col in header:
            columns[col] = sdict['type': 'TEXT', '_name_': col]
        return sdict['_name_': table_name, 'columns': columns]

    def get_key_column(self, table_schema, error=True):
        """Return the name of the first column in 'schema' designated as a 'key',
        or raise an error if no key column has been designated (unless 'error' is False).
        """
        for col in table_schema.columns.values():
            if col.get('key') == True:
                return col._name_
        if error:
            raise KGTKException('no key column defined')
        return None

    def get_table_definition(self, table_schema):
        colspec = ', '.join([sql_quote_ident(col._name_) + ' ' + col.type for col in table_schema.columns.values()])
        return 'CREATE TABLE %s (%s)' % (table_schema._name_, colspec)

    def get_index_name(self, table_schema, column):
        """Return a global name for the index for 'column' on 'table_schema'.
        """
        table_name = table_schema._name_
        column_name = table_schema.columns[column]._name_
        index_name = '%s_%s_idx' % (table_name, column_name)
        return index_name

    def get_index_definition(self, table_schema, column, unique=False):
        """Return a definition statement to create an index for 'column' on 'table_schema'.
        Create a 'unique' or primary key index if 'unique' is True.  We are currently
        only considering single-column indexes, however, we might generalize this down
        the road to two-column indices such as '(node1, label)', '(label, node2)', etc.
        """
        table_name = table_schema._name_
        column_name = table_schema.columns[column]._name_
        index_name = self.get_index_name(table_schema, column)
        unique = unique and 'UNIQUE' or ''
        return 'CREATE %s INDEX %s on %s (%s)' % (
            unique, sql_quote_ident(index_name), table_name, sql_quote_ident(column_name))
    
    def has_index(self, table_schema, column):
        """Return True if table 'table_schema' has an index defined for 'column'.
        """
        table_name = table_schema._name_
        column_name = table_schema.columns[column]._name_
        index_name = '%s_%s_idx' % (table_name, column_name)
        # we just key in on the name, not the table type, given how the names are constructed:
        return self.has_table(index_name)

    def get_column_list(self, *columns):
        return ', '.join([sql_quote_ident(col._name_) for col in columns])

    def get_full_column_list(self, table_schema):
        return ', '.join([sql_quote_ident(col._name_) for col in table_schema.columns.values()])


    ### Generic record access:
    
    def get_record_info(self, schema, key):
        """Return a dict info structure for the row identified by 'key' in table 'schema',
        or None if this key does not exist in the table.  All column keys will be set
        although some values may be None.
        """
        table = schema._name_
        cols = schema.columns
        keycol = self.get_key_column(schema)
        query = 'SELECT %s FROM %s WHERE %s=?' % (self.get_full_column_list(schema), table, cols[keycol]._name_)
        for row in self.execute(query, (key,)):
            result = sdict()
            for col, val in zip(cols.keys(), row):
                result[col] = val
            return result
        return None

    def set_record_info(self, schema, info):
        table = schema._name_
        cols = schema.columns
        keycol = self.get_key_column(schema)
        key = info[keycol]
        columns = [cols[name] for name in info.keys()]
        collist = self.get_column_list(*columns)
        if self.get_record_info(schema, key) is None:
            vallist = ','.join(['?'] * len(columns))
            stmt = 'INSERT INTO %s (%s) VALUES (%s)' % (table, collist, vallist)
            self.execute(stmt, list(info.values()))
        else:
            collist = collist.replace(', ', '=?, ')
            stmt = 'UPDATE %s SET %s=? WHERE %s=?' % (table, collist, keycol)
            values = list(info.values())
            values.append(key)
            self.execute(stmt, values)
        self.commit()

    def drop_record_info(self, schema, key):
        """Delete any rows identified by 'key' in table 'schema'.
        """
        table = schema._name_
        cols = schema.columns
        keycol = self.get_key_column(schema)
        stmt = 'DELETE FROM %s WHERE %s=?' % (table, cols[keycol]._name_)
        self.execute(stmt, (key,))
        self.commit()
        

    ### File information and access:

    # Each fileinfo record is identified by a name key which defaults to the full
    # dereferenced realpath of the file from which the graph data was loaded.
    # If an alias was provided that name will be stored as the key instead.

    def normalize_file_path(self, file):
        if os.path.basename(file) in ('-', 'stdin'):
            return '/dev/stdin'
        else:
            return os.path.realpath(file)

    def is_standard_input(self, file):
        return self.normalize_file_path(file) == '/dev/stdin'
    
    def get_file_info(self, file, alias=None, exact=False):
        """Return a dict info structure for the file info for 'file' (or 'alias') or None
        if this file does not exist in the file table.  All column keys will be set in
        the result although some values may be None.  If 'exact', use 'file' as is and
        do not try to normalize it to an absolute path.
        """
        info = self.get_record_info(self.FILE_TABLE, file)
        if info is None and alias is not None:
            info = self.get_record_info(self.FILE_TABLE, alias)
        if info is None and not exact:
            file = self.normalize_file_path(file)
            info = self.get_record_info(self.FILE_TABLE, file)
        return info

    def set_file_info(self, file, size=None, modtime=None, graph=None):
        info = sdict()
        info.file = file
        info.size = size
        info.modtime = modtime
        info.graph = graph
        self.set_record_info(self.FILE_TABLE, info)

    def drop_file_info(self, file):
        """Delete the file info record for 'file'.
        IMPORTANT: this does not delete any graph data associated with 'file'.
        """
        self.drop_record_info(self.FILE_TABLE, file)

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
        # we don't have an update yet, instead we delete first and then create the new record:
        self.drop_file_info(finfo.file)
        self.set_file_info(alias, size=finfo.size, modtime=finfo.modtime, graph=finfo.graph)

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
        return self.get_record_info(self.GRAPH_TABLE, table_name)

    def set_graph_info(self, table_name, header=None, size=None, acctime=None):
        info = sdict()
        info.name = table_name
        info.header = header
        info.size = size
        info.acctime = acctime
        self.set_record_info(self.GRAPH_TABLE, info)
    
    def drop_graph_info(self, table_name):
        """Delete the graph info record for 'table_name'.
        IMPORTANT: this does not delete any graph data stored in 'table_name'.
        """
        self.drop_record_info(self.GRAPH_TABLE, table_name)

    def get_graph_table_schema(self, table_name):
        """Get a graph table schema definition for graph 'table_name'.
        """
        info = self.get_graph_info(table_name)
        header = eval(info.header)
        return self.kgtk_header_to_graph_table_schema(table_name, header)

    def ensure_graph_index(self, table_name, column, unique=False, explain=False):
        """Ensure an index for 'table_name' on 'column' already exists or gets created.
        """
        schema = self.get_graph_table_schema(table_name)
        if not self.has_index(schema, column):
            index_stmt = self.get_index_definition(schema, column, unique=unique)
            loglevel = explain and 0 or 1
            self.log(loglevel, 'CREATE INDEX on table %s column %s ...' % (table_name, column))
            # we also measure the increase in allocated disk space here:
            oldsize = self.get_db_size()
            if not explain:
                self.execute(index_stmt)
            # do this unconditionally for now, given that it only takes about 10% of creation time:
            self.log(loglevel, 'ANALYZE INDEX on table %s column %s ...' % (table_name, column))
            if not explain:
                self.execute('ANALYZE %s' % sql_quote_ident(self.get_index_name(schema, column)))
            idxsize = self.get_db_size() - oldsize
            ginfo = self.get_graph_info(table_name)
            ginfo.size += idxsize
            if not explain:
                self.set_record_info(self.GRAPH_TABLE, ginfo)

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

    def has_graph(self, file, alias=None):
        """Return True if the KGTK graph represented/named by 'file' (or its 'alias' if not None)
        has already been imported and is up-to-date.  If this returns false, an obsolete graph
        table for 'file' might exist and will have to be removed before new data gets imported.
        This returns True iff a matching file info was found (named by 'file' or 'alias'), and
        'file' is an existing regular file whose properties match exactly what was previously loaded,
        or 'file' is not an existing regular file in which case its properties cannot be checked.
        This latter case allows us to delete large files used for import without losing the ability
        to query them, or to query files by using their alias only instead of a real filename.
        """
        info = self.get_file_info(file, alias=alias)
        if info is not None:
            if self.is_standard_input(file):
                # we never reuse plain stdin, it needs to be aliased to a new name for that:
                return False
            if os.path.exists(file):
                if info.size !=  os.path.getsize(file):
                    return False
                if info.modtime != os.path.getmtime(file):
                    return False
            # don't check md5sum for now:
            return True
        return False

    def add_graph(self, file, alias=None):
        """Import a graph from 'file' (and optionally named by 'alias') unless a matching
        graph has already been imported earlier according to 'has_graph' (which see).
        """
        if self.has_graph(file, alias=alias):
            if alias is not None:
                # this allows us to do multiple renamings:
                self.set_file_alias(file, alias)
            return
        file_info = self.get_file_info(file, alias=alias)
        if file_info is not None:
            # we already have an earlier version of the file in store, delete its graph data:
            self.drop_graph(file_info.graph)
        file = self.normalize_file_path(file)
        table = self.new_graph_table()
        oldsize = self.get_db_size()
        try:
            # try fast shell-based import first, but if that is not applicable...
            self.import_graph_data_via_import(table, file)
        except (KGTKException, sh.CommandNotFound):
            # ...fall back on CSV-based import which is more flexible but about 2x slower:
            self.import_graph_data_via_csv(table, file)
        graphsize = self.get_db_size() - oldsize
        # this isn't really needed, but we store it for now - maybe use JSON-encoding instead:
        header = str(self.get_table_header(table))
        if self.is_standard_input(file):
            self.set_file_info(file, size=0, modtime=time.time(), graph=table)
        else:
            self.set_file_info(file, size=os.path.getsize(file), modtime=os.path.getmtime(file), graph=table)
        self.set_graph_info(table, header=header, size=graphsize, acctime=time.time())
        if alias is not None:
            self.set_file_alias(file, alias)

    def drop_graph(self, table_name):
        """Delete the graph 'table_name' and all its associated info records.
        """
        # delete all supporting file infos:
        for file in self.get_graph_files(table_name):
            self.log(1, 'DROP graph data table %s from %s' % (table_name, file))
            self.drop_file_info(file)
        # delete the graph info:
        self.drop_graph_info(table_name)
        # now delete the graph table and all associated indexes:
        if self.has_table(table_name):
            self.execute('DROP TABLE %s' % table_name)


    ### Data import:
    
    def import_graph_data_via_csv(self, table, file):
        """Import 'file' into 'table' using Python's csv.reader.  This is safe and properly
        handles conversion of different kinds of line endings, but 2x slower than direct import.
        """
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
        with open_to_read(file, 'r') as inp:
            #csvreader = csv.reader(inp, dialect=None, delimiter='\t', quoting=csv.QUOTE_NONE)
            header = inp.readline()
            header = isinstance(header, bytes) and header.decode('utf8') or header
            if header.endswith('\r\n'):
                # SQLite import can only handle single-character line endings,
                # if we import anyway, \r winds up in the values of the last column:
                raise KGTKException('cannot handle multi-character line endings')
            eol = header[-1]
            header = header[:-1].split('\t')
            schema = self.kgtk_header_to_graph_table_schema(table, header)
            self.execute(self.get_table_definition(schema))
            self.commit()
        
        separators = '\\t %s' % repr(eol)[1:-1] # \r or \n for EOL
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

                
    def shell(self, *commands):
        """Execute a sequence of sqlite3 shell 'commands' in a single invocation
        and return stdout and stderr as result strings.  These sqlite shell commands
        are not invokable from a connection object, they have to be entered via 'sh'.
        """
        sqlite3 = sh.Command(self.get_sqlite_cmd())
        args = []
        for cmd in commands[0:-1]:
            args.append('-cmd')
            args.append(cmd)
        args.append(self.dbfile)
        args.append(commands[-1])
        proc = sqlite3(*args)
        return proc.stdout, proc.stderr

    def explain(self, sql_query, mode='plan'):
        if mode == 'plan':
            out, err = self.shell('EXPLAIN QUERY PLAN ' + sql_query)
        elif mode == 'full':
            out, err = self.shell('EXPLAIN ' + sql_query)
        elif mode == 'expert':
            out, err = self.shell('.expert', sql_query)
        else:
            raise KGTKException('illegal explanation mode: %s' % str(mode))
        return out.decode('utf8')

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


### SQLite KGTK user functions:

# Potentially those should go into their own file, depending on
# whether we generalize this to other SQL database such as Postgres.

# Naming convention: a suffix of _string indicates that the resulting
# value will be additionally converted to a KGTK string literal.  The
# same could generally be achieved by calling 'kgtk_stringify' explicitly.

# Strings:

def kgtk_string(x):
    """Return True if 'x' is a KGTK plain string literal."""
    return isinstance(x, str) and x.startswith('"')

def kgtk_stringify(x):
    """If 'x' is not already surrounded by double quotes, add them.
    """
    # TO DO: this also needs to handle escaping of some kind
    if not isinstance(x, str):
        x = str(x)
    if not (x.startswith('"') and x.endswith('"')):
        return '"' + x + '"'
    else:
        return x

def kgtk_unstringify(x):
    """If 'x' is surrounded by double quotes, remove them.
    """
    # TO DO: this also needs to handle unescaping of some kind
    if isinstance(x, str) and x.startswith('"') and x.endswith('"'):
        return x[1:-1]
    else:
        return x
    
SqliteStore.register_user_function('kgtk_string', 1, kgtk_string, deterministic=True)
SqliteStore.register_user_function('kgtk_stringify', 1, kgtk_stringify, deterministic=True)
SqliteStore.register_user_function('kgtk_unstringify', 1, kgtk_unstringify, deterministic=True)


# Regular expressions:

@lru_cache(maxsize=100)
def _get_regex(regex):
    return re.compile(regex)
    
def kgtk_regex(x, regex):
    """Regex matcher that implements the Cypher '=~' semantics which must match the whole string.
    """
    m = isinstance(x, str) and _get_regex(regex).match(x) or None
    return m is not None and m.end() == len(x)

SqliteStore.register_user_function('kgtk_regex', 2, kgtk_regex, deterministic=True)


# Language-qualified strings:

def kgtk_lqstring(x):
    """Return True if 'x' is a KGTK language-qualified string literal.
    """
    return isinstance(x, str) and x.startswith("'")

# these all return None upon failure without an explicit return:
def kgtk_lqstring_text(x):
    """Return the text component of a KGTK language-qualified string literal.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_language_qualified_string_re.match(x)
        if m:
            return m.group('text')
        
def kgtk_lqstring_text_string(x):
    """Return the text component of a KGTK language-qualified string literal
    as a KGTK string literal.
    """
    text = kgtk_lqstring_text(x)
    return text and ('"' + text + '"') or None

def kgtk_lqstring_lang(x):
    """Return the language component of a KGTK language-qualified string literal.
    This is the first part not including suffixes such as 'en' in 'en-us'.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_language_qualified_string_re.match(x)
        if m:
            # not a string for easier manipulation - assumes valid lang syntax:
            return m.group('lang')
        
def kgtk_lqstring_lang_suffix(x):
    """Return the language+suffix components of a KGTK language-qualified string literal.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_language_qualified_string_re.match(x)
        if m:
            # not a string for easier manipulation - assumes valid lang syntax:
            return m.group('lang_suffix')
        
def kgtk_lqstring_suffix(x):
    """Return the suffix component of a KGTK language-qualified string literal.
    This is the second part if it exists such as 'us' in 'en-us', empty otherwise.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_language_qualified_string_re.match(x)
        if m:
            # not a string for easier manipulation - assumes valid lang syntax:
            return m.group('suffix')

SqliteStore.register_user_function('kgtk_lqstring', 1, kgtk_lqstring, deterministic=True)
SqliteStore.register_user_function('kgtk_lqstring_text', 1, kgtk_lqstring_text, deterministic=True)
SqliteStore.register_user_function('kgtk_lqstring_text_string', 1, kgtk_lqstring_text_string, deterministic=True)
SqliteStore.register_user_function('kgtk_lqstring_lang', 1, kgtk_lqstring_lang, deterministic=True)
SqliteStore.register_user_function('kgtk_lqstring_lang_suffix', 1, kgtk_lqstring_lang_suffix, deterministic=True)
SqliteStore.register_user_function('kgtk_lqstring_suffix', 1, kgtk_lqstring_suffix, deterministic=True)


# Date literals:

def kgtk_date(x):
    """Return True if 'x' is a KGTK date literal.
    """
    return isinstance(x, str) and x.startswith('^')

# these all return None upon failure without an explicit return:
def kgtk_date_date(x):
    """Return the date component of a KGTK date literal as a KGTK date.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_date_and_times_re.match(x)
        if m:
            return '^' + m.group('date')
        
def kgtk_date_time(x):
    """Return the time component of a KGTK date literal as a KGTK date.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_date_and_times_re.match(x)
        if m:
            return '^' + m.group('time')
        
def kgtk_date_and_time(x):
    """Return the date+time components of a KGTK date literal as a KGTK date.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_date_and_times_re.match(x)
        if m:
            return '^' + m.group('date_and_time')
        
def kgtk_date_year(x):
    """Return the year component of a KGTK date literal as an int.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_date_and_times_re.match(x)
        if m:
            return int(m.group('year'))
        
def kgtk_date_month(x):
    """Return the month component of a KGTK date literal as an int.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_date_and_times_re.match(x)
        if m:
            return int(m.group('month'))
        
def kgtk_date_day(x):
    """Return the day component of a KGTK date literal as an int.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_date_and_times_re.match(x)
        if m:
            return int(m.group('day'))
        
def kgtk_date_hour(x):
    """Return the hour component of a KGTK date literal as an int.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_date_and_times_re.match(x)
        if m:
            return int(m.group('hour'))
        
def kgtk_date_minutes(x):
    """Return the minutes component of a KGTK date literal as an int.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_date_and_times_re.match(x)
        if m:
            return int(m.group('minutes'))
        
def kgtk_date_seconds(x):
    """Return the seconds component of a KGTK date literal as an int.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_date_and_times_re.match(x)
        if m:
            return int(m.group('seconds'))
        
def kgtk_date_zone(x):
    """Return the timezone component of a KGTK date literal.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_date_and_times_re.match(x)
        if m:
            return m.group('zone')
        
def kgtk_date_zone_string(x):
    """Return the time zone component (if any) as a KGTK string.  Zones might
    look like +10:30, for example, which would be illegal KGTK numbers.
    """
    zone = kgtk_date_zone(x)
    return zone and ('"' + zone + '"') or None

def kgtk_date_precision(x):
    """Return the precision component of a KGTK date literal as an int.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_date_and_times_re.match(x)
        if m:
            return int(m.group('precision'))

SqliteStore.register_user_function('kgtk_date', 1, kgtk_date, deterministic=True)
SqliteStore.register_user_function('kgtk_date_date', 1, kgtk_date_date, deterministic=True)
SqliteStore.register_user_function('kgtk_date_time', 1, kgtk_date_time, deterministic=True)
SqliteStore.register_user_function('kgtk_date_and_time', 1, kgtk_date_and_time, deterministic=True)
SqliteStore.register_user_function('kgtk_date_year', 1, kgtk_date_year, deterministic=True)
SqliteStore.register_user_function('kgtk_date_month', 1, kgtk_date_month, deterministic=True)
SqliteStore.register_user_function('kgtk_date_day', 1, kgtk_date_day, deterministic=True)
SqliteStore.register_user_function('kgtk_date_hour', 1, kgtk_date_hour, deterministic=True)
SqliteStore.register_user_function('kgtk_date_minutes', 1, kgtk_date_minutes, deterministic=True)
SqliteStore.register_user_function('kgtk_date_seconds', 1, kgtk_date_seconds, deterministic=True)
SqliteStore.register_user_function('kgtk_date_zone', 1, kgtk_date_zone, deterministic=True)
SqliteStore.register_user_function('kgtk_date_zone_string', 1, kgtk_date_zone_string, deterministic=True)
SqliteStore.register_user_function('kgtk_date_precision', 1, kgtk_date_precision, deterministic=True)


# Number and quantity literals:

sqlite3_max_integer = +2 ** 63 - 1
sqlite3_min_integer = -2 ** 63

def to_sqlite3_int(x):
    """Similar to Python 'int' but map numbers outside the 64-bit range onto their extremes.
    This is identical to what SQLite's 'cast' function does for numbers outside the range.
    """
    x = int(x)
    if x > sqlite3_max_integer:
        return sqlite3_max_integer
    elif x < sqlite3_min_integer:
        return sqlite3_min_integer
    else:
        return x

def to_sqlite3_float(x):
    """Identical to Python 'float', maps 'x' onto an 8-byte IEEE floating point number.
    """
    # TO DO: this might need more work to do the right thing at the boundaries
    #        and with infinity values, see 'sys.float_info'; seems to work
    return float(x)

def to_sqlite3_int_or_float(x):
    """Similar to Python 'int' but map numbers outside the 64-bit range onto floats.
    """
    x = int(x)
    if x > sqlite3_max_integer:
        return float(x)
    elif x < sqlite3_min_integer:
        return float(x)
    else:
        return x


def kgtk_number(x):
    """Return True if 'x' is a dimensionless KGTK number literal.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_number_or_quantity_re.match(x)
        if m:
            return x == m.group('number')
    return False

def kgtk_quantity(x):
    """Return True if 'x' is a dimensioned KGTK quantity literal.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_number_or_quantity_re.match(x)
        if m:
            return x != m.group('number')
    return False

# these all return None upon failure without an explicit return:
def kgtk_quantity_numeral(x):
    """Return the numeral component of a KGTK quantity literal.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_number_or_quantity_re.match(x)
        if m:
            return m.group('number')
        
def kgtk_quantity_numeral_string(x):
    """Return the numeral component of a KGTK quantity literal as a KGTK string.
    """
    num = kgtk_quantity_numeral(x)
    return num and ('"' + num + '"') or None

float_numeral_regex = re.compile(r'.*[.eE]')

def kgtk_quantity_number(x):
    """Return the number value of a KGTK quantity literal as an int or float.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_number_or_quantity_re.match(x)
        if m:
            numeral = m.group('number')
            if float_numeral_regex.match(numeral):
                return to_sqlite3_float(numeral)
            else:
                return to_sqlite3_int_or_float(numeral)
            
def kgtk_quantity_number_int(x):
    """Return the number value of a KGTK quantity literal as an int.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_number_or_quantity_re.match(x)
        if m:
            numeral = m.group('number')
            if float_numeral_regex.match(numeral):
                return to_sqlite3_int(float(numeral))
            else:
                return to_sqlite3_int(numeral)
            
def kgtk_quantity_number_float(x):
    """Return the number value component of a KGTK quantity literal as a float.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_number_or_quantity_re.match(x)
        if m:
            numeral = m.group('number')
            if float_numeral_regex.match(numeral):
                return to_sqlite3_float(numeral)
            else:
                # because the numeral could be in octal or hex:
                return to_sqlite3_float(int(numeral))

def kgtk_quantity_si_units(x):
    """Return the SI-units component of a KGTK quantity literal.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_number_or_quantity_re.match(x)
        if m:
            return m.group('si_units')
        
def kgtk_quantity_wd_units(x):
    """Return the Wikidata unit node component of a KGTK quantity literal.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_number_or_quantity_re.match(x)
        if m:
            return m.group('units_node')

def kgtk_quantity_tolerance(x):
    """Return the full tolerance component of a KGTK quantity literal.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_number_or_quantity_re.match(x)
        if m:
            lowtol = m.group('low_tolerance')
            hightol = m.group('high_tolerance')
            if lowtol and hightol:
                return '[' + lowtol + ',' + hightol + ']'
            
def kgtk_quantity_tolerance_string(x):
    """Return the full tolerance component of a KGTK quantity literal as a KGTK string.
    """
    tol = kgtk_quantity_tolerance(x)
    return tol and ('"' + tol + '"') or None

def kgtk_quantity_low_tolerance(x):
    """Return the low tolerance component of a KGTK quantity literal as a float.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_number_or_quantity_re.match(x)
        if m:
            lowtol = m.group('low_tolerance')
            if lowtol:
                return to_sqlite3_float(lowtol)
            
def kgtk_quantity_high_tolerance(x):
    """Return the high tolerance component of a KGTK quantity literal as a float.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_number_or_quantity_re.match(x)
        if m:
            hightol = m.group('high_tolerance')
            if hightol:
                return to_sqlite3_float(hightol)

SqliteStore.register_user_function('kgtk_number', 1, kgtk_number, deterministic=True)
SqliteStore.register_user_function('kgtk_quantity', 1, kgtk_quantity, deterministic=True)
SqliteStore.register_user_function('kgtk_quantity_numeral', 1, kgtk_quantity_numeral, deterministic=True)
SqliteStore.register_user_function('kgtk_quantity_numeral_string', 1, kgtk_quantity_numeral_string, deterministic=True)
SqliteStore.register_user_function('kgtk_quantity_number', 1, kgtk_quantity_number, deterministic=True)
SqliteStore.register_user_function('kgtk_quantity_number_int', 1, kgtk_quantity_number_int, deterministic=True)
SqliteStore.register_user_function('kgtk_quantity_number_float', 1, kgtk_quantity_number_float, deterministic=True)
SqliteStore.register_user_function('kgtk_quantity_si_units', 1, kgtk_quantity_si_units, deterministic=True)
SqliteStore.register_user_function('kgtk_quantity_wd_units', 1, kgtk_quantity_wd_units, deterministic=True)
SqliteStore.register_user_function('kgtk_quantity_tolerance', 1, kgtk_quantity_tolerance, deterministic=True)
SqliteStore.register_user_function('kgtk_quantity_tolerance_string', 1, kgtk_quantity_tolerance_string, deterministic=True)
SqliteStore.register_user_function('kgtk_quantity_low_tolerance', 1, kgtk_quantity_low_tolerance, deterministic=True)
SqliteStore.register_user_function('kgtk_quantity_high_tolerance', 1, kgtk_quantity_high_tolerance, deterministic=True)

# kgtk_quantity_number_float('12[-0.1,+0.1]m')
# kgtk_number('0x24F') ...why does this not work?


# Geo coordinates:

def kgtk_geo_coords(x):
    """Return True if 'x' is a KGTK geo coordinates literal.
    """
    # Assumes valid KGTK values, thus only tests for initial character:
    return isinstance(x, str) and x.startswith('@')

# these all return None upon failure without an explicit return:
def kgtk_geo_coords_lat(x):
    """Return the latitude component of a KGTK geo coordinates literal as a float.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_location_coordinates_re.match(x)
        if m:
            return to_sqlite3_float(m.group('lat'))
        
def kgtk_geo_coords_long(x):
    """Return the longitude component of a KGTK geo coordinates literal as a float.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_location_coordinates_re.match(x)
        if m:
            return to_sqlite3_float(m.group('lon'))

SqliteStore.register_user_function('kgtk_geo_coords', 1, kgtk_geo_coords, deterministic=True)
SqliteStore.register_user_function('kgtk_geo_coords_lat', 1, kgtk_geo_coords_lat, deterministic=True)
SqliteStore.register_user_function('kgtk_geo_coords_long', 1, kgtk_geo_coords_long, deterministic=True)


# Literals:

literal_regex = re.compile(r'''^["'^@!0-9.+-]|^True$|^False$''')

def kgtk_literal(x):
    """Return True if 'x' is any KGTK literal.  This assumes valid literals
    and only tests the first character (except for booleans).
    """
    return isinstance(x, str) and literal_regex.match(x) is not None

SqliteStore.register_user_function('kgtk_literal', 1, kgtk_literal, deterministic=True)


# NULL value utilities:

# In the KGTK file format we cannot distinguish between empty and NULL values.
# Both KGTKReader and SQLite map missing values onto empty strings, however,
# database functions as well as our KGTK user functions return NULL for undefined
# values.  These can be tested via 'IS [NOT] NULL', however, in some cases it is
# convenient to convert from one to the other for more uniform tests and queries.

def kgtk_null_to_empty(x):
    """If 'x' is NULL map it onto the empty string, otherwise return 'x' unmodified.
    """
    if x is None:
        return ''
    else:
        return x

def kgtk_empty_to_null(x):
    """If 'x' is the empty string, map it onto NULL, otherwise return 'x' unmodified.
    """
    if x == '':
        return None
    else:
        return x

SqliteStore.register_user_function('kgtk_null_to_empty', 1, kgtk_null_to_empty, deterministic=True)
SqliteStore.register_user_function('kgtk_empty_to_null', 1, kgtk_empty_to_null, deterministic=True)


# Math:

# Temporary Python implementation of SQLite math built-ins until they become standardly available.
# Should happen once SQLite3 3.35.0 is used by Python - or soon thereafter.  Once we've determined
# the cutoff point we can make the function registration dependent on 'sqlite3.version'.
# User-defined functions override built-ins, which means this should work even after math built-ins
# come online - we hope.

def math_acos(x):
    """"Implement the SQLite3 math built-in 'acos' via Python.
    """
    try:
        return math.acos(x)
    except:
        pass

def math_acosh(x):
    """Implement the SQLite3 math built-in 'acosh' via Python.
    """
    try:
        return math.acosh(x)
    except:
        pass

def math_asin(x):
    """Implement the SQLite3 math built-in 'asin' via Python.
    """
    try:
        return math.asin(x)
    except:
        pass

def math_asinh(x):
    """Implement the SQLite3 math built-in 'asinh' via Python.
    """
    try:
        return math.asinh(x)
    except:
        pass

def math_atan(x):
    """Implement the SQLite3 math built-in 'atan' via Python.
    """
    try:
        return math.atan(x)
    except:
        pass

def math_atan2(x, y):
    """Implement the SQLite3 math built-in 'atan2' via Python.
    """
    try:
        return math.atan2(y, x) # flips args
    except:
        pass

def math_atanh(x):
    """Implement the SQLite3 math built-in 'atanh' via Python.
    """
    try:
        return math.atanh(x)
    except:
        pass

# alias: ceiling(X)
def math_ceil(x):
    """Implement the SQLite3 math built-in 'ceil' via Python.
    """
    try:
        return math.ceil(x)
    except:
        pass

def math_cos(x):
    """Implement the SQLite3 math built-in 'cos' via Python.
    """
    try:
        return math.cos(x)
    except:
        pass

def math_cosh(x):
    """Implement the SQLite3 math built-in 'cosh' via Python.
    """
    try:
        return math.cosh(x)
    except:
        pass

def math_degrees(x):
    """Implement the SQLite3 math built-in 'degrees' via Python.
    Convert value X from radians into degrees. 
    """
    try:
        return math.degrees(x)
    except:
        pass

def math_exp(x):
    """Implement the SQLite3 math built-in 'exp' via Python.
    """
    try:
        return math.exp(x)
    except:
        pass

def math_floor(x):
    """Implement the SQLite3 math built-in 'floor' via Python.
    """
    try:
        return math.floor(x)
    except:
        pass

# NOTE: naming and invocation of logarithm functions is different from
# standard SQL or Python math for that matter (more like Postgres).

def math_ln(x):
    """Implement the SQLite3 math built-in 'ln' via Python.
    """
    try:
        return math.log(x)
    except:
        pass

# alias: log(X)
def math_log10(x):
    """Implement the SQLite3 math built-in 'log10' via Python.
    """
    try:
        return math.log10(x)
    except:
        pass

def math_logb(b, x):
    """Implement the SQLite3 math built-in 'log(b,x)' via Python.
    NOTE: this uses a different name, since we cannot support optionals
    (which would require special handling in the query translator).
    This means the function needs to stay even if we use the real built-ins.
    """
    try:
        return math.log(x, b)
    except:
        pass

def math_log2(x):
    """Implement the SQLite3 math built-in 'log2' via Python.
    """
    try:
        return math.log2(x)
    except:
        pass

def math_mod(x, y):
    """Implement the SQLite3 math built-in 'mod' via Python.
    """
    try:
        return math.fmod(x, y) # preferred over 'x % y' for floats
    except:
        pass

def math_pi():
    """Implement the SQLite3 math built-in 'pi' via Python.
    """
    return math.pi

# alias: power(X,Y)
def math_pow(x, y):
    """Implement the SQLite3 math built-in 'pow' via Python.
    """
    try:
        return math.pow(x, y)
    except:
        pass

def math_radians(x):
    """Implement the SQLite3 math built-in 'radians' via Python.
    """
    try:
        return math.radians(x)
    except:
        pass

def math_sin(x):
    """Implement the SQLite3 math built-in 'sin' via Python.
    """
    try:
        return math.sin(x)
    except:
        pass

def math_sinh(x):
    """Implement the SQLite3 math built-in 'sinh' via Python.
    """
    try:
        return math.sinh(x)
    except:
        pass

def math_sqrt(x):
    """Implement the SQLite3 math built-in 'sqrt' via Python.
    """
    try:
        return math.sqrt(x)
    except:
        pass

def math_tan(x):
    """Implement the SQLite3 math built-in 'tan' via Python.
    """
    try:
        return math.tan(x)
    except:
        pass

def math_tanh(x):
    """Implement the SQLite3 math built-in 'tanh' via Python.
    """
    try:
        return math.tanh(x)
    except:
        pass

def math_trunc(x):
    """Implement the SQLite3 math built-in 'trunc' via Python.
    """
    try:
        return math.trunc(x)
    except:
        pass

SqliteStore.register_user_function('acos', 1, math_acos, deterministic=True)
SqliteStore.register_user_function('acosh', 1, math_acosh, deterministic=True)
SqliteStore.register_user_function('asin', 1, math_asin, deterministic=True)
SqliteStore.register_user_function('asinh', 1, math_asinh, deterministic=True)
SqliteStore.register_user_function('atan', 1, math_atan, deterministic=True)
SqliteStore.register_user_function('atan2', 2, math_atan2, deterministic=True)
SqliteStore.register_user_function('atanh', 1, math_atanh, deterministic=True)
SqliteStore.register_user_function('ceil', 1, math_ceil, deterministic=True)
SqliteStore.register_user_function('ceiling', 1, math_ceil, deterministic=True)
SqliteStore.register_user_function('cos', 1, math_cos, deterministic=True)
SqliteStore.register_user_function('cosh', 1, math_cosh, deterministic=True)
SqliteStore.register_user_function('degrees', 1, math_degrees, deterministic=True)
SqliteStore.register_user_function('exp', 1, math_exp, deterministic=True)
SqliteStore.register_user_function('floor', 1, math_floor, deterministic=True)
SqliteStore.register_user_function('ln', 1, math_ln, deterministic=True)
SqliteStore.register_user_function('log', 1, math_log10, deterministic=True)
SqliteStore.register_user_function('log10', 1, math_log10, deterministic=True)
SqliteStore.register_user_function('log2', 1, math_log2, deterministic=True)
# this one needs to stay if we conditionalize on availability of real math built-ins:
SqliteStore.register_user_function('logb', 2, math_logb, deterministic=True)
SqliteStore.register_user_function('mod', 2, math_mod, deterministic=True)
SqliteStore.register_user_function('pi', 0, math_pi, deterministic=True)
SqliteStore.register_user_function('pow', 2, math_pow, deterministic=True)
SqliteStore.register_user_function('power', 2, math_pow, deterministic=True)
SqliteStore.register_user_function('radians', 1, math_radians, deterministic=True)
SqliteStore.register_user_function('sin', 1, math_sin, deterministic=True)
SqliteStore.register_user_function('sinh', 1, math_sinh, deterministic=True)
SqliteStore.register_user_function('sqrt', 1, math_sqrt, deterministic=True)
SqliteStore.register_user_function('tan', 1, math_tan, deterministic=True)
SqliteStore.register_user_function('tanh', 1, math_tanh, deterministic=True)
SqliteStore.register_user_function('trunc', 1, math_trunc, deterministic=True)


### Experimental transitive taxonomy relation indexing:

@lru_cache(maxsize=1000)
def kgtk_decode_taxonomy_node_intervals(intervals):
    """Decode a difference-encoded list of 'intervals' into a numpy array with full intervals.
    """
    # expensive imports we don't want to run unless needed, lru cache will eliminate repeat overhead:
    import gzip, binascii, numpy
    if intervals[0] == 'z':
        intervals = gzip.decompress(binascii.a2b_base64(intervals[1:])).decode()
    intervals = intervals.replace(';', ',0,')
    if intervals.endswith(','):
        intervals = intervals[0:-1]
    intervals = list(map(int, intervals.split(',')))
    # we special-case single intervals and binary search on more than one interval:
    if len(intervals) > 2:
        # add sentinel, so we always have a sort insertion point before the end of the array:
        intervals.append(0)
    intervals = numpy.array(intervals, dtype=numpy.int32)
    # decode difference encoding:
    for i in range(1, len(intervals)):
        intervals[i] += intervals[i-1]
    if len(intervals) > 2:
        # initialize sentinel:
        intervals[-1] = 2**31 - 1
    return intervals

# timing on 2.5M calls:
# - just call and return: Q123: 0.95s, Q5: 1.05s
# - int(label):           Q123: 1.38s, Q5: 1.45s
# - decode intervals:     Q123: 1.68s, Q5: 2.12s
# - single int range:     Q123: 3.10s, Q5: 2.20s
# - single int >=,<=:     Q123: 2.60s, Q5: 2.20s
# - range shortcut:       Q123: 2.60s, Q5: 2.20s
# - searchsorted:         Q123: 2.60s, Q5: 4.90s
# - result1:              Q123: 2.60s, Q5:11.10s
# - result2: (wrong)      Q123: 2.60s, Q5: 6.95s
# - result3:              Q123: 2.60s, Q5:10.80s 
# - result4: (wrong)      Q123: 2.60s, Q5: 6.30s
# - result5:              Q123: 2.60s, Q5: 6.60s
# - bool(result5)         Q123: 2.60s, Q5: 6.70s

def kgtk_is_subnode(label, encoded_intervals):
    """Return True if 'label' is contained in one of the encoded 'intervals'.
    'intervals' is a flat list of sorted, closed integer intervals.
    """
    # NOTE: it took us a while to optimize this properly; the crucial bit was
    # to use 'int' to cast array elements before comparing them via >=,<= and ==
    label = int(label)
    # cached lookup is fast, trying to use a shorter key string (e.g., edge ID) does not help:
    intervals = kgtk_decode_taxonomy_node_intervals(encoded_intervals)
    # check single interval shortcut:
    if len(intervals) == 2:
        # "casting" to int first significantly speeds things up (also beats 'range'):
        return label >= int(intervals[0]) and label <= int(intervals[1])
    i = intervals.searchsorted(label)
    # this runs on lists but is 3x slower, not sure why, it says there is a C-implementation:
    #i = bisect.bisect_left(intervals, label)
    #result1 = (i & 1) or (i < len(intervals) and intervals[i] == label)
    #result2 = (i & 1) or (i < len(intervals) and intervals[i] is label)
    #result3 = (i & 1) or (intervals[i] == label)
    #result4 = (i & 1) or (intervals[i] is label)
    # "casting" to int first gives us a much faster equality test:
    result5 = (i & 1) or (int(intervals[i]) == label)
    #sys.stderr.write('%s  %s  %s\n' % (label, intervals, result))
    # TO DO: figure out whether we should add this to all predicates above:
    return bool(result5)

SqliteStore.register_user_function('kgtk_is_subnode', 2, kgtk_is_subnode, deterministic=True)
