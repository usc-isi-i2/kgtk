import sys
import pprint
import tempfile

import sh

from kgtk.cypher.parser import *

pp = pprint.PrettyPrinter(indent=4)


TMP_DIR = '/tmp'       # this should be configurable

def make_temp_file(prefix='kgtk.'):
    return tempfile.mkstemp(dir=TMP_DIR, prefix=prefix)[1]

def grep_regex_quote(value):
    # TO DO: WRITE ME.
    return value


class MatchClause(QueryElement):
    def __init__(self, graph, columns, header=False, sortcol=None):
        self.graph = graph         # a normalized KGTK edge file to run over
        self.columns = columns     # a list of Literal, Variable or None elements
        self.header = header       # file has a header row
        self.sort_column = sortcol # file is sorted by that column (1-based)

    def filter(self):
        """Run a filter operation on `self' based on the restrictions in
        `self.columns' and return a new clause describing the result.
        """
        pattern = []
        variables = []
        has_restriction = False
        for col in self.columns:
            if col is None:
                pat = '.*'
            elif isinstance(col, Variable):
                varname = col.name
                if varname in variables:
                    pat = '\\%d' % (variables.index(varname) + 1)
                    has_restriction = True
                else:
                    variables.append(varname)
                    pat = '\(.*\)'
            elif isinstance(col, Literal):
                value = col.value
                pat = grep_regex_quote(value)
                has_restriction = True
            else:
                raise Exception('Unhandled column description: %s' % col)
            pattern.append(pat)
        if not has_restriction:
            # all columns are either None or unique variables:
            return self
        
        grep_pattern = '^' + '\t'.join(pattern) + '$'
        result_graph = make_temp_file()
        if self.header:
            sh.grep(sh.tail('-n', '+2', self.graph), '-G', '-h', grep_pattern, _out=result_graph)
        else:
            sh.grep('-G', '-h', grep_pattern, self.graph, _out=result_graph)

        return MatchClause(result_graph, self.columns)

    def join(self, other, joinvar=None):
        """Run a join operation on `self' and `other' and return a new clause describing the result.
        Use `joinvar' to join, otherwise use the first shared variable found.
        """
        # - not sure if kgtk join does what we need, since it always creates an edge file it seems
        #   that adds additional edges to the end
        # - what we want - I think - is the regular Unix join which creates a wide file adding columns
        if joinvar is None:
            for col1 in self.columns:
                if isinstance(col1, Variable):
                    for col2 in other.columns:
                        if isinstance(col2, Variable) and col1.name == col2.name:
                            joinvar = col2
                            break
                    if joinvar is not None:
                        break
        if joinvar is None:
            raise Exception('disconnected join')
        for col1, pos in zip(self.columns, range(len(self.columns))):
            if isinstance(col1, Variable) and col1.name == joinvar.name:
                pos1 = pos + 1
                break
        for col2, pos in zip(other.columns, range(len(other.columns))):
            if isinstance(col2, Variable) and col2.name == joinvar.name:
                pos2 = pos + 1
                break

        sorted_graph1 = make_temp_file()
        sorted_graph2 = make_temp_file()
        if self.header:
            sh.sort(sh.tail('-n', '+2', self.graph), '-t', '\t', '-k', '%d,%d' % (pos1, pos1), _out=sorted_graph1)
        else:
            sh.sort('-t', '\t', '-k', '%d,%d' % (pos1, pos1), self.graph, _out=sorted_graph1)
        if other.header:
            sh.sort(sh.tail('-n', '+2', other.graph), '-t', '\t', '-k', '%d,%d' % (pos2, pos2), _out=sorted_graph2)
        else:
            sh.sort('-t', '\t', '-k', '%d,%d' % (pos2, pos2), other.graph, _out=sorted_graph2)

        join_graph = make_temp_file()
        join_columns = other.columns[:]
        join_columns.remove(joinvar)
        join_columns = self.columns[:] + join_columns
        sh.join('-1', str(pos1), '-2', str(pos2), sorted_graph1, sorted_graph2, _out=join_graph)
        return MatchClause(join_graph, join_columns, sortcol=pos1)
