"""
Cypher queries over KGTK graphs.
"""

import sys
import os
import os.path
import pprint
import tempfile
import sqlite3
from odictliteral import odict

import sh

import kgtk.cypher.parser as parser

pp = pprint.PrettyPrinter(indent=4)


### NOTES, TO DO:

# - not sure if kgtk join does what we need, since it always creates an edge file it seems
#   that adds additional edges to the end
# - what we want - I think - is the regular Unix join which creates a wide file adding columns
#   similar to what we get with an SQL relational join


TMP_DIR = '/tmp'       # this should be configurable

def make_temp_file(prefix='kgtk.'):
    return tempfile.mkstemp(dir=TMP_DIR, prefix=prefix)[1]

def grep_regex_quote(value):
    # TO DO: WRITE ME.
    return value


class PatternElement(object):
    
    def get_grep_pattern(self):
        raise Exception('not implemented')

    def to_tree(self):
        return (self.__class__.__name__, parser.object_to_tree(self.__dict__))


class Variable(PatternElement):
    
    def __init__(self, name):
        self.name = name

    def get_grep_pattern(self, group=None):
        if group is not None:
            return '\\%d' % group
        else:
            return '\(.*\)'

class Literal(PatternElement):
    
    def __init__(self, value):
        self.value = value

    def get_grep_pattern(self):
        return grep_regex_quote(self.value)

class TuplePattern(object):
    """Simple tuple pattern implemented as a dictionary of 
    implicitly conjoined column_name->pattern_element entries.
    """
    
    def __init__(self, pattern=None):
        self.pattern = pattern or {}

    def to_tree(self):
        return parser.object_to_tree(self.pattern)

    def get_restriction(self, name):
        return self.pattern.get(name)

    def set_restriction(self, name, restr):
        self.pattern[name] = restr

    def get_grep_pattern(self, columns):
        """Convert `match_pattern' into a grep pattern to match
        it against a file-based tuple with `columns'.
        """
        pattern = []
        variables = []
        has_restriction = False
        for col in columns:
            restriction = self.get_restriction(col)
            if restriction is None:
                pat = '.*'
            elif isinstance(restriction, Variable):
                varname = restriction.name
                if varname in variables:
                    pat = restriction.get_grep_pattern(variables.index(varname) + 1)
                    has_restriction = True
                else:
                    variables.append(varname)
                    pat = restriction.get_grep_pattern()
            elif isinstance(restriction, Literal):
                pat = restriction.get_grep_pattern()
                has_restriction = True
            else:
                raise Exception('Unhandled match restriction: %s' % restriction)
            pattern.append(pat)
        if not has_restriction:
            # all columns are either None or unique variables:
            return None
        else:
            return '^' + '\t'.join(pattern) + '$'

"""
>>> pat = cq.TuplePattern({'node1': cq.Variable('?x'), 'label': cq.Literal('loves')})
>>> pat.get_grep_pattern(['node1', 'label', 'node2', 'id'])
'^\\(.*\\)\tloves\t.*\t.*$'
>>> pat2 = cq.TuplePattern({'node1': cq.Variable('?x'), 'label': cq.Literal('loves'), 'node2': cq.Variable('?x')})
>>> pat2.get_grep_pattern(['node1', 'label', 'node2', 'id'])
'^\\(.*\\)\tloves\t\\1\t.*$'
>>> pat3 = cq.TuplePattern({'node1': cq.Variable('?x')})
>>> 
"""


class DataTable(object):
    """Data table representing a KGTK graph which might be implemented by a file,
    Pandas data frame, database table or other.
    """
    
    def __init__(self, db, columns):
        self.db = db
        self.column_names = columns

    def get_default_join_column(self, other):
        assert isinstance(other, DataTable), 'argument needs to be a DataTable'
        for col1 in self.column_names:
            if col1 in other.column_names:
                return col1
        return None

    def get_join_column_positions(self, other, column):
        """Return the zero-based positions of `column' in `self' and `other'.
        """
        assert isinstance(other, DataTable), 'argument needs to be a DataTable'
        return self.column_names.index(column), other.column_names.index(column)

class FileDataTable(DataTable):
    """Data table implemented by a tab-separated text file.
    """
    
    def __init__(self, file, columns, header=False, sortcol=None):
        self.db = file
        self.column_names = columns
        self.header=header
        self.sortcol=sortcol  # element in `columns'

    def describe(self):
        if not self.header:
            print(self.column_names)
        with open(self.db, 'rt') as inp:
            for line in inp:
                sys.stdout.write(line)

    def filter(self, pattern):
        """Run a filter operation on `self' based on the restrictions in
        `pattern' and return a new FileDataTable describing the result.
        """
        grep_pattern = pattern.get_grep_pattern(self.column_names)
        if grep_pattern is None:
            # pattern doesn't have any restrictions:
            return self
        result_graph = make_temp_file()
        if self.header:
            sh.grep(sh.tail('-n', '+2', self.db), '-G', '-h', grep_pattern, _out=result_graph)
        else:
            sh.grep('-G', '-h', grep_pattern, self.db, _out=result_graph)
        return FileDataTable(result_graph, self.column_names)

    def join(self, other, column=None):
        """Run a join operation on `self' and `other' and return a new table describing the result.
        Use `column' to join, otherwise use the first shared column name found.
        """
        assert isinstance(other, FileDataTable), 'second table needs to be also a FileDataTable'
        column = column or self.get_default_join_column(other)
        assert column is not None and column in self.column_names and column in other.column_names, 'disconnected join'
        
        pos1, pos2 = self.get_join_column_positions(other, column)
        # TO DO: think about this since it potentially repeates column names:
        join_columns = self.column_names[:] + other.column_names[0:pos2] + other.column_names[pos2 + 1:]

        sorted_graph1 = make_temp_file()
        sorted_graph2 = make_temp_file()
        pos1, pos2 = pos1 + 1, pos2 + 1

        if self.header:
            sh.sort(sh.tail('-n', '+2', self.db), '-t', '\t', '-k', '%d,%d' % (pos1, pos1), _out=sorted_graph1)
        else:
            sh.sort('-t', '\t', '-k', '%d,%d' % (pos1, pos1), self.db, _out=sorted_graph1)
        if other.header:
            sh.sort(sh.tail('-n', '+2', other.db), '-t', '\t', '-k', '%d,%d' % (pos2, pos2), _out=sorted_graph2)
        else:
            sh.sort('-t', '\t', '-k', '%d,%d' % (pos2, pos2), other.db, _out=sorted_graph2)

        join_graph = make_temp_file()
        sh.join('-1', str(pos1), '-2', str(pos2), sorted_graph1, sorted_graph2, _out=join_graph)
        return FileDataTable(join_graph, join_columns, sortcol=pos1)

"""
>>> ft1 = cq.FileDataTable('/home/hans/Projects/kgtk/code/kgtk/kgtk/cypher/.work/file1.tsv', ['node1', 'label', 'node2', 'id'], header=True)
>>> ft2 = cq.FileDataTable('/home/hans/Projects/kgtk/code/kgtk/kgtk/cypher/.work/file2.tsv', ['node1', 'label', 'node2', 'id'], header=True)
>>> pat = cq.TuplePattern({'node1': cq.Variable('?x'), 'label': cq.Literal('loves')})
>>> ft1.filter(pat)
<kgtk.cypher.query.FileDataTable object at 0x7f5a25a79490>
>>> ft1.join(ft2, 'node1')
<kgtk.cypher.query.FileDataTable object at 0x7f5a25705910>
"""

def query_clause_to_tuple_pattern(clause):
    node1 = clause[0]
    rel = clause[1]
    node2 = clause[2]
    pattern = TuplePattern()
    if node1.labels is not None:
        pattern.set_restriction('node1', Literal(node1.labels[0]))
    else:
        pattern.set_restriction('node1', Variable(node1.variable.name))
    if node2.labels is not None:
        pattern.set_restriction('node2', Literal(node2.labels[0]))
    else:
        pattern.set_restriction('node2', Variable(node2.variable.name))
    if rel.labels is not None:
        pattern.set_restriction('label', Literal(rel.labels[0]))
    pattern.set_restriction('id', Variable(rel.variable.name))
    return pattern

def run_test_match_query(graph, query):
    query = 'MATCH ' + query + ' RETURN r;'
    clauses = parser.intern(query).get_match_clauses()
    tuple_query = [query_clause_to_tuple_pattern(clause) for clause in clauses]
    print('Normalized clauses:')
    pp.pprint(parser.object_to_tree(clauses))
    print('\nTuple clauses:')
    pp.pprint(parser.object_to_tree(tuple_query))
    graph_table = FileDataTable(graph, ['node1', 'label', 'node2', 'id'], header=True)
    result = execute_query(graph_table, tuple_query)
    print('\nResult:')
    result.describe()
    return result

def execute_query(graph_table, tuple_query):
    n_clauses = len(tuple_query)
    i = 1
    result = graph_table.filter(tuple_query[0])
    while i < n_clauses:
        clause = graph_table.filter(tuple_query[i])
        result = result.join(clause)
        i += 1
    return result

# Using properties to restrict on "wide" columns:
#
# Example - unrestricted:
#
#    (a)-[:loves]->(b)
#
# Example - qualified:
#
#    (a {nationality: "Austria"})-[:loves]->(b)
#
# This could mean:
#    {'node1': <Variable a>, 'node1;nationality': "Austria", 'label': "loves", 'node2': <Variable b>}
#
#    (a)-[:loves {graph: "g1"}]->(b)
#
# This could mean:
#    {'node1': <Variable a>, 'label': "loves", 'graph': "g1", 'node2': <Variable b>}
#
# Assumption: if we access something via a property, it will always be accessed via a column,
# not via a normalized edge; if data has mixed representation for some edges, it has to be
# normalized one way or the other first for the query to get all results.  If not, it will
# only pick up the representation used in the query, other edges will be ignored.
#
# For structured literals, we assume their fields are implied/virtual wide columns that aren't
# materialized.  For example:
#
#    (id)-[:P580]->(time {`kgtk:year`: year})
#    where year <= 2010
#
# which would be the same as (if we named the accessors like our column names):
#
#    (id)-[:P580]->(time)
#    where kgtk_year(time) <= 2010


class SqlStore(object):
    """SQL database capable of storing one or more KGTK graph files as individual tables
    and allowing them to be queried with SQL statements.
    """
    pass

# Quoting:
# - standard SQL quoting for identifiers such as table and columnames is via double quotes
# - double quotes within identifiers can be escaped via two double quotes
# - sqlite also supports MySQL's backtick syntax and SQLServer's [] syntax

class pdict(odict):
    """Ordered dict that supports property access of its elements.
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

    MASTER_TABLE = 'sqlite_master'
    FILE_TABLE   = 'fileinfo'
    GRAPH_TABLE  = 'graphinfo'

    FILE_TABLE_SCHEMA = odict[
        'file': 'TEXT',       # this should be a real path
        'size': 'INTEGER',
        'modtime': 'FLOAT',
        'imptime': 'TEXT',
        'md5sum': 'TEXT',
    ]

    GRAPH_TABLE_SCHEMA = odict[
        'name': 'TEXT',       # name of the table
        'file': 'TEXT',       # there could be multiple
        'sha256sum': 'TEXT',  # computed by sqlite3 shasum cmd
        'header': 'TEXT',
        'size': 'INTEGER',    # total size in bytes used by this graph including indexes
    ]
    
    def __init__(self, dbfile, create=False):
        if not os.path.exists(dbfile) and not create:
            raise Exception('sqlite3 DB file does not exist: %s' % dbfile)
        self.dbfile = dbfile
        self.conn = None
        self.init_meta_tables()

    def get_conn(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.dbfile)
        return self.conn

    def get_sqlite_cmd(self):
        # TO DO: this should look more intelligently to find it in the python install path
        # e.g., check `sys.prefix/bin', `sys.exec_prefix/bin' or do a `which sqlite3';
        # if we use a conda environment we get it automatically.
        return 'sqlite3'

    def close(self):
        if self.conn is not None:
            self.conn.close()

    def get_db_size(self):
        return os.path.getsize(self.dbfile)

    def execute(self, *args, **kwargs):
        return self.get_conn().execute(*args, **kwargs)

    def has_table(self, table_name):
        """Return True if a table with name `table_name' exists in the store.
        """
        query = """select count(*) from %s where name=?""" % self.MASTER_TABLE
        (cnt,) = self.execute(query, (table_name,)).fetchone()
        return cnt > 0

    def get_table_definition(self, table, schema):
        colspec = ', '.join(['"' + col + '" ' + typ for col, typ in schema.items()])
        return 'CREATE TABLE %s (%s)' % (table, colspec)
    
    def init_meta_tables(self):
        if not self.has_table(self.FILE_TABLE):
            self.execute(self.get_table_definition(self.FILE_TABLE, self.FILE_TABLE_SCHEMA))
        if not self.has_table(self.GRAPH_TABLE):
            self.execute(self.get_table_definition(self.GRAPH_TABLE, self.GRAPH_TABLE_SCHEMA))

    def has_graph(self, file):
        """Return True if the KGTK graph represented by `file' has already been imported.
        """
        file = os.path.realpath(file)
        query = 'SELECT size, modtime, md5sum from %s where file=?' % self.FILE_TABLE
        for size, modtime, md5sum in self.execute(query, (file,)):
            if size !=  os.path.getsize(file):
                return False
            if modtime != os.path.getmtime(file):
                return False
            # don't check md5sum for now:
            return True
        return False

    def file_to_table(self, file):
        """Return a table name to be used for the graph represented by file.
        """
        file = os.path.realpath(file)
        return 'g%d' % abs(hash(file))

    def add_graph(self, file):
        if self.has_graph(file):
            return
        table = self.file_to_table(file)
        # TO DO: complete me:
        sh.time(self.get_sqlite_cmd(),)
