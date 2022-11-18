"""
Obsolete info table API for access to file and graph info tables.
"""

from   functools import lru_cache

from   kgtk.exceptions import KGTKException
from   kgtk.kypher.utils import *


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


class InfoTable(object):
    """Obsolete info table API for access to file and graph info tables.
    """

    def __init__(self, store, schema):
        """Create an info table object for 'schema' stored in 'store'.
        """
        self.store = store
        self.schema = schema
        self.verified_schema = False

    def init_table(self):
        """If the info table doesn't exist yet, define it from its schema.
        """
        if not self.store.has_table(self.schema._name_):
            self.store.execute(self.store.get_table_definition(self.schema))
            self.verified_schema = True

    def clear_caches(self):
        InfoTable.get_info.cache_clear()
        InfoTable.get_all_keys.cache_clear()
        InfoTable.get_all_infos.cache_clear()

    @lru_cache(maxsize=None)
    def get_info(self, key):
        """Return a dict info structure for the row identified by 'key' in this info table,
        or None if 'key' does not exist.  All column keys will be set, but some values may be None.
        """
        if not self.verified_schema:
            self.handle_schema_update()
        table = self.schema._name_
        cols = self.schema.columns
        keycol = self.store.get_key_column(self.schema)
        query = 'SELECT %s FROM %s WHERE %s=?' % (self.store.get_full_column_list(self.schema), table, cols[keycol]._name_)
        for row in self.store.execute(query, (key,)):
            result = sdict()
            for col, val in zip(cols.keys(), row):
                result[col] = val
            return result
        return None

    def set_info(self, key, info):
        """Insert or update this info table for 'key' based on the values in 'info'.
        If a record based on 'key' already exists, update it, otherwise insert a new one.
        If a new record is inserted, any missing column values in 'info' will be set to None.
        If 'info' contains a value for the key column, that value will override 'key' which
        allows for an existing key value to be updated to a new one.
        """
        if self.get_info(key) is not None:
            self.update_info(key, info)
        else:
            # this is not really needed, since 'get_info' already checks:
            #if not self.verified_schema:
            #    self.handle_schema_update()
            table = self.schema._name_
            cols = self.schema.columns
            keycol = self.store.get_key_column(self.schema)
            key = info.get(keycol) or key
            info[keycol] = key
            columns = [cols[name] for name in info.keys()]
            collist = self.store.get_column_list(*columns)
            vallist = ','.join(['?'] * len(columns))
            stmt = 'INSERT INTO %s (%s) VALUES (%s)' % (table, collist, vallist)
            self.store.execute(stmt, list(info.values()))
            self.store.commit()
            self.clear_caches()

    def update_info(self, key, info):
        """Update an existing record in this info table for 'key' and the values in 'info'.
        Any column values undefined in 'info' will remain unaffected.
        If 'info' contains a value for the key column, that value will override 'key' which
        allows for an existing key value to be updated to a new one.
        This is a no-op if no record with 'key' exists in table 'schema'.
        """
        if not self.verified_schema:
            self.handle_schema_update()
        table = self.schema._name_
        cols = self.schema.columns
        keycol = self.store.get_key_column(self.schema)
        columns = [cols[name] for name in info.keys()]
        collist = self.store.get_column_list(*columns)
        collist = collist.replace(', ', '=?, ')
        stmt = 'UPDATE %s SET %s=? WHERE %s=?' % (table, collist, keycol)
        values = list(info.values())
        values.append(key)
        self.store.execute(stmt, values)
        self.store.commit()
        self.clear_caches()
        
    def drop_info(self, key):
        """Delete any rows identified by 'key' in this info table.
        """
        if not self.verified_schema:
            self.handle_schema_update()
        table = self.schema._name_
        cols = self.schema.columns
        keycol = self.store.get_key_column(self.schema)
        stmt = 'DELETE FROM %s WHERE %s=?' % (table, cols[keycol]._name_)
        self.store.execute(stmt, (key,))
        self.store.commit()
        self.clear_caches()

    @lru_cache(maxsize=None)
    def get_all_keys(self):
        table = self.schema._name_
        cols = self.schema.columns
        keycol = self.store.get_key_column(self.schema)
        return [key for (key,) in self.store.execute('SELECT %s FROM %s' % (keycol, table))]

    @lru_cache(maxsize=None)
    def get_all_infos(self):
        # TO DO: this generates one query per key, generalize if this becomes a performance issue
        return [self.get_info(key) for key in self.get_all_keys()]
    
    def handle_schema_update(self):
        """Check whether the schema of the info table on disk is compatible with this schema.
        If not, try to upgrade it by adding any new missing columns.  If the schema on disk is
        from a newer version of KGTK, raise an error.  This assumes that updates to info table
        schemas always only add new columns.  No other schema changes are supported.
        """
        if self.verified_schema:
            return
        table = self.schema._name_
        cols = self.schema.columns
        current_col_names = self.store.get_table_header(table)
        if len(current_col_names) == len(cols):
            self.verified_schema = True
            return
        if len(current_col_names) > len(cols):
            raise KGTKException('incompatible graph cache schema, please upgrade KGTK or delete the cache')
            
        try:
            col_names = [col._name_ for col in cols.values()]
            for cname in col_names:
                if cname not in current_col_names:
                    newcol = cols[cname]
                    stmt = 'ALTER TABLE %s ADD COLUMN %s %s' % (table, cname, newcol.type)
                    self.store.execute(stmt)
            self.verified_schema = True
        except Exception as e:
            raise KGTKException('sorry, error during schema upgrade, please remove graph cache and retry ( %s )' % repr(e))
