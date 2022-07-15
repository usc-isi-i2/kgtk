"""
SQLStore to support Kypher queries over KGTK graphs.
"""

from   functools import lru_cache
import copy

from   kgtk.exceptions import KGTKException
from   kgtk.kypher.utils import *


class KgtkInfoTable(object):
    """API for access to file and graph info using a fine-grained KGTK edge data model.
    """
    
    TABLE_SCHEMA = sdict[
        '_name_': '<NAME>',
        'columns': sdict[
            'node1':  sdict['_name_': 'node1',  'type': 'TEXT',],
            'label':  sdict['_name_': 'label',  'type': 'TEXT',],
            'node2':  sdict['_name_': 'node2',  'type': 'TEXT',],
            'id':     sdict['_name_': 'id',     'type': 'TEXT',],
        ],
    ]

    def __init__(self, store, table):
        """Create an info table object for 'table' stored in 'store'.
        """
        self.store = store
        self.table = table
        self.schema = copy.deepcopy(self.TABLE_SCHEMA)
        self.schema._name_ = self.table
        self.columns = self.schema.columns
        self.column_list = self.store.get_full_column_list(self.schema)
        self.init_table()

    def init_table(self):
        """If the info table doesn't exist yet, define it from its schema.
        """
        if not self.store.has_table(self.table):
            self.store.execute(self.store.get_table_definition(self.schema))
            table = self.table
            node1_idx = f'{table}_node1_idx'
            stmt = f'CREATE INDEX {node1_idx} ON {table} ({self.columns.node1._name_})'
            self.store.execute(stmt)
            label_idx = f'{table}_label_idx'
            stmt = f'CREATE INDEX {label_idx} ON {table} ({self.columns.label._name_})'
            self.store.execute(stmt)
            node2_idx = f'{table}_node2_idx'
            stmt = f'CREATE INDEX {node2_idx} ON {table} ({self.columns.node2._name_})'
            self.store.execute(stmt)

    def make_object_id(self, prefix, *keys):
        """Create a unique object ID starting with 'prefix' and based on 'keys'.
        If no 'keys' are supplied, append a new random UUID to 'prefix'.
        """
        # we only use this during DB updates, so the import overhead should be negligible:
        import shortuuid
        if len(keys) == 0:
            return prefix + shortuuid.random(22)
        else:
            return prefix + shortuuid.uuid(r'_/^^\_'.join(map(str, keys)))

    @lru_cache(maxsize=None)
    def get_edge_pattern_restriction(self, node1=None, label=None, node2=None, id=None):
        # this should be called with a True/False binding pattern
        # instead of actual values for maximum caching effectiveness:
        restrictions = []
        if node1:
            restrictions.append(f'{self.columns.node1._name_}=?')
        if label:
            restrictions.append(f'{self.columns.label._name_}=?')
        if node2:
            restrictions.append(f'{self.columns.node2._name_}=?')
        if id:
            restrictions.append(f'{self.columns.id._name_}=?')
        return ' AND '.join(restrictions)

    @lru_cache(maxsize=None)
    def get_edges_query(self, node1=None, label=None, node2=None, id=None):
        # this should be called with a True/False binding pattern
        # instead of actual values for maximum caching effectiveness:
        table = self.table
        return_columns = self.column_list
        restrictions = self.get_edge_pattern_restriction(node1, label, node2, id) or "TRUE"
        query = f'SELECT {return_columns} FROM {table} WHERE {restrictions}'
        return query        
        
    def get_edges(self, node1=None, label=None, node2=None, id=None):
        """Return an iterator generating the edges identified by the restriction pattern
        defined through the values of 'node1/label/node2/id'.
        """
        pattern = [node1, label, node2, id]
        query = self.get_edges_query(*[x is not None for x in pattern])
        return self.store.execute(query, [x for x in pattern if x is not None])

    def add_edge(self, node1, label, node2, id=None):
        """Add an edge defined by 'node1/label/node2'.  If no 'id' is provided,
        generate one based purely on the triple.  This does not check for existing
        duplicate edges and will simply append a new row to the table.
        """
        if id is None:
            id = self.make_object_id('e-', node1, label, node2)
        table = self.table
        columns = self.column_list
        stmt = f'INSERT INTO {table} ({columns}) VALUES (?,?,?,?)'
        self.store.execute(stmt, (node1, label, node2, id))

    def delete_edges(self, node1=None, label=None, node2=None, id=None):
        """Delete all edges identified by the restriction pattern
        defined through the values of 'node1/label/node2/id'.
        """
        pattern = [node1, label, node2, id]
        table = self.table
        restrictions = self.get_edge_pattern_restriction(*[x is not None for x in pattern]) or "TRUE"
        stmt = f'DELETE FROM {table} WHERE {restrictions}'
        self.store.execute(stmt, [x for x in pattern if x is not None])

    def update_edge(self, node1, label, node2, id=None):
        """Update all edges identified by 'node1/label' to have 'node2' and 'id'
        as their remaining elements.  An id will be generated if necessary.
        """
        if id is None:
            id = self.make_object_id('e-', node1, label, node2)
        table = self.table
        columns = self.get_edge_pattern_restriction(False, False, True, True)
        columns = columns.replace('=? AND ', '=?, ')
        restrictions = self.get_edge_pattern_restriction(True, True, False, False)
        stmt = f'UPDATE {table} SET {columns} WHERE {restrictions}'
        self.store.execute(stmt, (node2, id, node1, label))

    def get_values(self, node1, label):
        """Return the list of all values for 'node1/label'.
        """
        return [node2 for _, _, node2, _ in self.get_edges(node1, label)]

    def get_value(self, node1, label):
        """Return the first value for 'node1/label' or None if no such edge exists.
        """      
        for _, _, node2, _ in self.get_edges(node1, label):
            return node2
        return None
    
    def get_objects(self, node2, label):
        """Inverse to 'get_values' starting from 'node2/label' to objects 'node1'.
        """
        return [node1 for node1, _, _, _ in self.get_edges(None, label, node2)]

    def get_object(self, node2, label):
        """Inverse to 'get_value' starting from 'node2/label' to object 'node1'.
        Return None if no such edge exists.
        """
        for node1, _, _, _ in self.get_edges(None, label, node2):
            return node1
        return None

    def set_value(self, node1, label, node2):
        """Set the value of 'node1/label' to 'node2'  This deletes all preexisting
        matching edges and ensures only a single such edge exists after the operation.
        """
        self.delete_edges(node1, label)
        self.add_edge(node1, label, node2)

    def add_value(self, node1, label, node2):
        """Add a single 'node1/label/node2' edge and remove any duplicates.
        """
        self.delete_edges(node1, label, node2)
        self.add_edge(node1, label, node2)
    
    def update_value(self, node1, label, node2):
        """Change the node2 value of a 'node1/label' edge to 'node2'.
        Expects that exactly one such edge exists before the operation.
        """
        values = self.get_values(node1, label)
        if len(values) != 1:
            raise KGTKException('can only update existing single-valued edge')
        self.update_edge(node1, label, node2)
        
    def get_all_objects(self):
        """Return a list of distinct 'node1' objects in this table.
        """
        query = f'SELECT DISTINCT {self.columns.node1._name_} FROM {self.table}'
        return [node1 for (node1,) in self.store.execute(query)]
