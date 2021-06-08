"""
Kypher parser (derived from ruruki.parsers.cypher_parser.py).
https://s3.amazonaws.com/artifacts.opencypher.org/cypher.ebnf
"""

import sys
import os
import os.path
import pprint
import parsley
import ometa.grammar
from   kgtk.kypher.grammar import KYPHER_GRAMMAR

pp = pprint.PrettyPrinter(indent=4)


# TO DO:
# - flesh out the TO DOs below
# - add missing pattern elements
# + expression simplification and normalization (e.g., with <-x-> patterns)
# + add implied clauses (e.g., from properties)
#   - handled by query translator instead
# - handle match-pattern OR-expansion (from undirected arrows and multiple relation labels)
#   - possibly also handle this by query translator (if at all)
# - handle restrictions and unsupported elements more consistently and pervasively


GRAMMAR_FILE = os.path.join(os.path.dirname(sys.modules['kgtk.kypher.grammar'].__file__), 'grammar.py')
COMPILED_GRAMMAR_FILE = os.path.join(os.path.dirname(GRAMMAR_FILE), 'grammar_compiled.py')

def compile_grammar():
    # if we want to use this for production, we can save the grammar as a Python file like this:
    cygram = ometa.grammar.OMeta.makeGrammar(KYPHER_GRAMMAR)
    with open(COMPILED_GRAMMAR_FILE, 'w') as out:
        out.write(cygram.__loader__.source)

def load_grammar(compile=True):
    if compile:
        # re/compile if necessary:
        if not os.path.exists(COMPILED_GRAMMAR_FILE) or \
           os.path.getmtime(GRAMMAR_FILE) > os.path.getmtime(COMPILED_GRAMMAR_FILE):
            compile_grammar()
        # load it like this - there doesn't seem to be a better user API available:
        import kgtk.kypher.grammar_compiled as cgc
        cgram = cgc.createParserClass(ometa.grammar.OMetaBase, {})
        return parsley.wrapGrammar(cgram)
    else:
        # rebuild the grammar from scratch:
        return parsley.makeGrammar(KYPHER_GRAMMAR, {})

Parser = load_grammar()


"""
# The grammar has 75 output patterns:
# - there are two with varying signatures - might be a mistake
# - we are currently handling about 40
# - we should redo this from scratch (see grammar notes) - maybe later

["All", fex] ["Any", fex] ["Case", ex, cas, el] ["Create", p]
["Delete", [head] + tail] ["Expression", a, opts] ["Expression2", a, c]
["Expression3", ex1, c] ["Extract", fex, ex] ["Filter", fex]
["FilterExpression", i, w] ["IdInColl", v, ex] ["Limit", ex] ["List", ex]
["ListComprehension", fex, ex] ["Literal", l] ["Match", p, w]
["Merge", [head] + tail] ["MergeActionCreate", s] ["MergeActionMatch", s]
["NodeLabel", n] ["NodePattern", s, nl, p] ["None", fex] ["Order", [head] + tail]
["Parameter", p] ["PatternElement", np, pec] ["PatternElementChain", rp, np]
["PatternPart", v, ap] ["PropertyLookup", prop_name]
["RelationshipDetail", v, q, rt, rl, p] ["RelationshipTypes", head]

["RelationshipsPattern", la, rd, ra]  <<--
["RelationshipsPattern", np, pec]     <<--

["Remove", [head] + tail] ["RemoveItemPe", p] ["RemoveItemVar", v, nl]
["Return", d, rb] ["ReturnBody", ri, o, s, l] ["ReturnItem", ex, None]
["ReturnItem", ex, s] ["ReturnItems", [head] + tail] ["Set", [head] + tail]
["SetItem", v, ex] ["SetItemPropertyExpression", pex, ex] ["Single", fex]

["SingleQuery", [head] + tail]        <<--
["SingleQuery", m, w, r]              <<--

["Skip", ex] ["Union", sq, rq] ["UnionAll", sq, rq] ["Unwind", ex, v]
["Variable", s] ["Where", ex] ["With", d, rb, w] ["add", ex1, ex2]
["and", ex1, ex2] ["call", func, distinct, args] ["count *"] 
["div", ex1, ex2] ["eq", ex1, ex2] ["gt", ex1, ex2] ["gte", ex1, ex2]
["hat", ex1, ex2] ["is_not_null"] ["is_null"] ["lt", ex1, ex2]
["lte", ex1, ex2] ["minus", ex] ["mod", ex1, ex2] ["multi", ex1, ex2]
["neq", ex1, ex2] ["not", ex] ["or", ex1, ex2] ["slice", start, end]
["sort", ex, dir] ["sub", ex1, ex2] ["xor", ex1, ex2]
"""


### Parse tree utilities

def object_to_tree(obj):
    if hasattr(obj, 'to_tree'):
        return obj.to_tree()
    elif isinstance(obj, list):
        return [object_to_tree(elt) for elt in obj]
    elif isinstance(obj, dict):
        table = {}
        for key, val in obj.items():
            if key.startswith('_') or val is None:
                continue
            table[key] = object_to_tree(val)
        return table
    else:
        return obj

def simplify_object(obj):
    if hasattr(obj, 'simplify'):
        return obj.simplify()
    elif isinstance(obj, list):
        for i in range(len(obj)):
            obj[i] = simplify_object(obj[i])
        return obj
    elif isinstance(obj, dict):
        table = {}
        for key, val in obj.items():
            if key.startswith('_') or val is None:
                continue
            table[key] = simplify_object(val)
        for key, val in table.items():
            obj[key] = val
        return obj
    else:
        return obj

def has_element(obj, test):
    """Return True if any of the `QueryElement's in `obj'
    or any of their recursive subelements satisfy `test'.
    """
    if isinstance(obj, QueryElement):
        return test(obj) or has_element(obj.__dict__, test)
    elif isinstance(obj, list):
        for elt in obj:
            if has_element(elt, test):
                return True
    elif isinstance(obj, dict):
        for elt in obj.values():
            if has_element(elt, test):
                return True
    return False


### Object representation for Kypher ASTs (Abstract Syntax Trees)

class QueryElement(object):
    ast_name = None

    def to_tree(self):
        return (self.__class__.__name__, object_to_tree(self.__dict__))

    def simplify(self):
        simplify_object(self.__dict__)
        return self


# Atoms:

class Literal(QueryElement):
    ast_name = 'Literal'
    
    def __init__(self, query, value):
        self._query = query
        self.value = value
    
class Variable(QueryElement):
    ast_name = 'Variable'

    def __init__(self, query, name):
        self._query = query
        self.name = name
        query.variables[name] = self

class AnonymousVariable(Variable):
    pass

class Parameter(QueryElement):
    ast_name = 'Parameter'
    
    def __init__(self, query, name):
        self._query = query
        self.name = name


# Arithmetic:

class Add(QueryElement):
    ast_name = 'add'

    def __init__(self, query, arg1, arg2):
        self._query = query
        self.arg1 = intern_ast(query, arg1)
        self.arg2 = intern_ast(query, arg2)

class Sub(QueryElement):
    ast_name = 'sub'

    def __init__(self, query, arg1, arg2):
        self._query = query
        self.arg1 = intern_ast(query, arg1)
        self.arg2 = intern_ast(query, arg2)

class Minus(QueryElement):
    ast_name = 'minus'

    def __init__(self, query, arg):
        self._query = query
        self.arg = intern_ast(query, arg)

class Multi(QueryElement):
    ast_name = 'multi'

    def __init__(self, query, arg1, arg2):
        self._query = query
        self.arg1 = intern_ast(query, arg1)
        self.arg2 = intern_ast(query, arg2)

class Div(QueryElement):
    ast_name = 'div'

    def __init__(self, query, arg1, arg2):
        self._query = query
        self.arg1 = intern_ast(query, arg1)
        self.arg2 = intern_ast(query, arg2)

class Mod(QueryElement):
    ast_name = 'mod'

    def __init__(self, query, arg1, arg2):
        self._query = query
        self.arg1 = intern_ast(query, arg1)
        self.arg2 = intern_ast(query, arg2)

class Hat(QueryElement):
    ast_name = 'hat'

    def __init__(self, query, arg1, arg2):
        self._query = query
        self.arg1 = intern_ast(query, arg1)
        self.arg2 = intern_ast(query, arg2)


# Comparison:

class Eq(QueryElement):
    ast_name = 'eq'

    def __init__(self, query, arg1, arg2):
        self._query = query
        self.arg1 = intern_ast(query, arg1)
        self.arg2 = intern_ast(query, arg2)

class Neq(QueryElement):
    ast_name = 'neq'

    def __init__(self, query, arg1, arg2):
        self._query = query
        self.arg1 = intern_ast(query, arg1)
        self.arg2 = intern_ast(query, arg2)

class Lt(QueryElement):
    ast_name = 'lt'

    def __init__(self, query, arg1, arg2):
        self._query = query
        self.arg1 = intern_ast(query, arg1)
        self.arg2 = intern_ast(query, arg2)

class Gt(QueryElement):
    ast_name = 'gt'

    def __init__(self, query, arg1, arg2):
        self._query = query
        self.arg1 = intern_ast(query, arg1)
        self.arg2 = intern_ast(query, arg2)

class Lte(QueryElement):
    ast_name = 'lte'

    def __init__(self, query, arg1, arg2):
        self._query = query
        self.arg1 = intern_ast(query, arg1)
        self.arg2 = intern_ast(query, arg2)

class Gte(QueryElement):
    ast_name = 'gte'

    def __init__(self, query, arg1, arg2):
        self._query = query
        self.arg1 = intern_ast(query, arg1)
        self.arg2 = intern_ast(query, arg2)


# Boolean operators and conditionals:

class Not(QueryElement):
    ast_name = 'not'

    def __init__(self, query, arg):
        self._query = query
        self.arg = intern_ast(query, arg)

class And(QueryElement):
    ast_name = 'and'

    def __init__(self, query, arg1, arg2):
        self._query = query
        self.arg1 = intern_ast(query, arg1)
        self.arg2 = intern_ast(query, arg2)

class Or(QueryElement):
    ast_name = 'or'

    def __init__(self, query, arg1, arg2):
        self._query = query
        self.arg1 = intern_ast(query, arg1)
        self.arg2 = intern_ast(query, arg2)

class Xor(QueryElement):
    ast_name = 'xor'

    def __init__(self, query, arg1, arg2):
        self._query = query
        self.arg1 = intern_ast(query, arg1)
        self.arg2 = intern_ast(query, arg2)

class Case(QueryElement):
    ast_name = 'Case'

    def __init__(self, query, test, conditions, otherwise):
        self._query = query
        self.test = intern_ast(query, test)
        self.conditions = [(intern_ast(query, when), intern_ast(query, then_)) for when, then_ in conditions]
        self.otherwise = intern_ast(query, otherwise)


# Expressions:

class Expression(QueryElement):
    ast_name = 'Expression'

    def __init__(self, query, arg, options):
        self._query = query
        self.arg = intern_ast(query, arg)
        self.options = intern_ast(query, options)

class Expression2(QueryElement):
    ast_name = 'Expression2'

    def __init__(self, query, arg1, arg2):
        self._query = query
        self.arg1 = intern_ast(query, arg1)
        self.arg2 = intern_ast(query, arg2)

class Expression3(QueryElement):
    ast_name = 'Expression3'

    def __init__(self, query, arg1, op_and_arg2):
        self._query = query
        self.arg1 = intern_ast(query, arg1)
        op_and_arg2 = op_and_arg2[0]
        self.operator = op_and_arg2[0]
        self.arg2 = len(op_and_arg2) >= 2 and intern_ast(query, op_and_arg2[1]) or None

class PropertyLookup(QueryElement):
    ast_name = 'PropertyLookup'

    def __init__(self, query, property):
        self._query = query
        self.property = property

class Call(QueryElement):
    ast_name = 'call'

    def __init__(self, query, func, distinct, args):
        self._query = query
        self.function = func
        self.distinct = distinct is not None
        self.args = intern_ast_list(query, args)


# Lists:

class List(QueryElement):
    ast_name = 'List'

    def __init__(self, query, elements):
        self._query = query
        self.elements = intern_ast_list(query, elements)


# Patterns:

class NodeLabel(QueryElement):
    ast_name = 'NodeLabel'

    def __init__(self, query, name):
        self._query = query
        self.name = name

class NodePattern(QueryElement):
    ast_name = 'NodePattern'

    def __init__(self, query, name, labels, properties):
        self._query = query
        self.variable = name
        self.labels = intern_ast_list(query, labels)
        self.graph = None
        self.properties = None
        if properties is not None:
            if properties[0] == 'Literal':
                self.properties = {key:intern_ast(query, val) for key, val in properties[1].items()}
            else:
                # parameter:
                self.properties = intern_ast(query, properties)

    def simplify(self):
        self.variable = Variable(self._query, self.variable)
        if self.labels is not None:
            self.labels = [lab.name for lab in self.labels]
        return self

    def is_anonymous(self):
        return self.variable is None or self.variable.name is None

    def normalize_term(self, implied_clauses):
        # TO DO: handle implied clauses from properties
        query = self._query
        labels = self.labels
        assert labels is None or len(labels) == 1, 'Multiple node labels are not allowed'
        if self.is_anonymous():
            self.variable = query.create_anonymous_variable()
        return self

class RelationshipPattern(QueryElement):
    ast_name = 'RelationshipsPattern' # note the extra 's'

    def __init__(self, query, *args):
        if len(args) == 2:
            # KLUDGE: `RelationshipsPattern' is one of two outputs that get invoked with incongruent signatures:
            # - normal case: ["RelationshipsPattern", la, rd, ra]
            # - WHERE case:  ["RelationshipsPattern", np, pec]
            # We handle this here with a "change class" to `PatternElement' which is what it should be.
            # TO DO: clean this up, but it will do for now:
            #        make this return a PathPattern to make normalization work similar to MATCH
            head = args[0]
            tail = args[1] is not None and list(args[1:]) or []
            PatternElement.__init__(self, query, head, tail)
            self.__class__ = PatternElement
            return
        left_arrow, detail, right_arrow = args
        self._query = query
        self.left_arrow = left_arrow
        self.detail = intern_ast(query, detail)
        self.labels = None
        self.right_arrow = right_arrow
        # a bidirectional arrow is legal in the grammar but not legal Cypher;
        if left_arrow and right_arrow:
            raise Exception('Illegal bidirectional arrow: %s' % str(self.simplify().to_tree()))

    def simplify(self):
        self.detail = simplify_object(self.detail)
        self.variable = self.detail and self.detail.variable or None
        self.qualifier = self.detail and self.detail.qualifier or None
        # multiple labels amount to an OR in KGTK which we are addressing later:
        self.labels = self.detail and self.detail.labels or None
        self.range_ = self.detail and self.detail.range_ or None
        self.properties = self.detail and self.detail.properties or None
        # a non-directional relation amounts to an OR in KGTK which we are addressing later:
        self.arrow = (self.left_arrow or '') + '--' + (self.right_arrow or '')
        delattr(self, 'left_arrow')
        delattr(self, 'right_arrow')
        delattr(self, 'detail')
        return self

    def is_anonymous(self):
        return self.variable is None or self.variable.name is None
    
    def normalize_term(self, implied_clauses):
        # TO DO: handle implied clauses from properties
        query = self._query
        labels = self.labels
        arrow = self.arrow
        assert labels is None or len(labels) == 1, 'Multiple relationship labels are not (yet) allowed'
        assert arrow != '--', 'Undirected relationships are not (yet) allowed'
        if self.is_anonymous():
            self.variable = query.create_anonymous_variable()
        return self

class RelationshipDetail(QueryElement):
    ast_name = 'RelationshipDetail'

    def __init__(self, query, variable, qualifier, types, range_, properties):
        self._query = query
        self.variable = intern_ast(query, variable)
        self.qualifier = qualifier
        self.labels = intern_ast(query, types)
        self.range_ = range_
        self.properties = None
        if properties is not None:
            if properties[0] == 'Literal':
                self.properties = {key:intern_ast(query, val) for key, val in properties[1].items()}
            else:
                # parameter:
                self.properties = intern_ast(query, properties)

class RelationshipTypes(QueryElement):
    ast_name = 'RelationshipTypes'

    def __init__(self, query, *types):
        self._query = query
        self.labels = types

    def simplify(self):
        return self.labels

class PatternElementChain(QueryElement):
    ast_name = 'PatternElementChain'

    def __init__(self, query, head, tail):
        self._query = query
        self.head = intern_ast(query, head)
        self.tail = intern_ast(query, tail)

    def simplify(self):
        return [self.head.simplify(), self.tail.simplify()]
        
class PatternElement(QueryElement):
    ast_name = 'PatternElement'

    def __init__(self, query, element, chain):
        self._query = query
        self.head = intern_ast(query, element)
        self.tail = intern_ast_list(query, chain)
        self.graph = None

    def simplify(self):
        chain = [self.head.simplify()]
        chain[0].graph = self.graph
        for subchain in simplify_object(self.tail):
            chain += subchain
        return chain
    
class PatternPart(QueryElement):
    ast_name = 'PatternPart'

    def __init__(self, query, variable, pattern):
        self._query = query
        # these can either be named with a variable or anonymous:
        self.variable = intern_ast(query, variable)
        self.pattern = intern_ast(query, pattern)

    def simplify(self):
        # simply rename to `PathPattern':
        return PathPattern(self._query, simplify_object(self.variable), simplify_object(self.pattern))

class GraphPatternPart(QueryElement):
    ast_name = 'GraphPatternPart'

    def __init__(self, query, graph, pattern):
        self._query = query
        # we have a pattern prefixed with a graph variable:
        self.graph = intern_ast(query, graph)
        self.pattern = intern_ast(query, pattern)

    def simplify(self):
        # simply rename to `PathPattern' and set graph variable:
        pattern = PathPattern(self._query, None, simplify_object(self.pattern))
        pattern.graph = simplify_object(self.graph)
        return pattern

class GraphRelationshipsPattern(PatternElement):
    ast_name = 'GraphRelationshipsPattern'

    def __init__(self, query, graph, head, tail):
        # this is a variant of RelationshipPattern where we don't have the ambiguity:
        super().__init__(query, head, [tail])
        self.graph = intern_ast(query, graph)

class PathPattern(QueryElement):

    def __init__(self, query, variable, pattern):
        self._query = query
        # these can either be named with a variable or anonymous:
        self.variable = variable
        self.pattern = pattern
        self.graph = None

    def normalize_clauses(self):
        # Path patterns are either N, N-R-N, or N-R-N-R-...-R-N for two or more relations.
        # We normalize them onto a single or list of implicitly conjoined N-R-N path patterns.
        # Assumes simplification has been run.
        query = self._query
        pattern = self.pattern
        graph = self.graph
        num_elements = len(pattern)
        if num_elements == 3:
            if pattern[1].arrow == '<--':
                # normalize onto forward direction:
                head = pattern[0]
                pattern[0] = pattern[2]
                pattern[2] = head
                pattern[1].arrow = '-->'
            pattern[0].graph = graph
            return self
        elif num_elements == 1:
            pattern[0].graph = graph
            relpat = RelationshipPattern(query, None, None, None)
            relpat.arrow = '-->'
            relpat.variable = query.create_anonymous_variable()
            self.pattern.append(relpat)
            nodepat = NodePattern(query, None, None, None)
            nodepat.variable = query.create_anonymous_variable()
            self.pattern.append(nodepat)
            return self
        else:
            assert num_elements >= 5 and num_elements % 2 == 1, 'Unexpected number of path pattern elements'
            norm_patterns = []
            while len(pattern) >= 3:
                subpat = PathPattern(query, self.variable, pattern[0:3])
                subpat.graph = graph
                norm_patterns.append(subpat.normalize_clauses())
                # we create a connecting variable node, but we do not copy any of the other attributes if any,
                # since those might result in additional clauses which we only want to create once:
                conn_nodepat = pattern[2]
                if conn_nodepat.is_anonymous():
                    conn_nodepat.variable = query.create_anonymous_variable()
                nodepat = NodePattern(query, None, None, None)
                nodepat.variable = conn_nodepat.variable
                nodepat.graph = graph
                conn_nodepat = nodepat
                pattern = [conn_nodepat] + pattern[3:]
            return norm_patterns

    def normalize_terms(self, implied_clauses):
        query = self._query
        pattern = self.pattern
        assert len(pattern) == 3, 'Unnormalized path pattern'
        pattern[0] = pattern[0].normalize_term(implied_clauses)
        pattern[1] = pattern[1].normalize_term(implied_clauses)
        pattern[2] = pattern[2].normalize_term(implied_clauses)

    def normalize(self):
        # this gives us either a single or list of normalized N-R-N PathPattern's:
        clauses = self.normalize_clauses()
        if not hasattr(clauses, '__iter__'):
            clauses = [clauses]
        norm_clauses = []
        for clause in clauses:
            norm_clauses.append(clause)
            clause.normalize_terms(norm_clauses)
        return norm_clauses


# Query top level clauses:

class StrictMatch(QueryElement):
    ast_name = 'StrictMatch'

    def __init__(self, query, pattern, where):
        self._query = query
        self.pattern = intern_ast_list(query, pattern)
        self.where = intern_ast(query, where)
        self.default_graph = None
        self.pattern_clauses = None

    def normalize(self):
        """Compute a list of [<NodePattern ...> <RelationshipPattern --> ...> <NodePattern ...>] clauses
        where each pattern element has a named or anonymous variable and optional single label.  All
        property elements have been translated into additional normalized match clauses.  Also propagates
        graph information which defaults to 'self.default_graph'.
        """
        if self.pattern_clauses is None:
            self.pattern_clauses = []
            current_graph = self.default_graph
            for pathpat in self.pattern:
                for normpath in pathpat.normalize():
                    normpath = normpath.pattern
                    current_graph = normpath[0].graph or current_graph
                    normpath[0].graph = current_graph
                    self.pattern_clauses.append(normpath)
        return self

    def get_pattern_clauses(self, default_graph=None):
        self.default_graph=default_graph
        return self.normalize().pattern_clauses

    def get_where_clause(self):
        return self.normalize().where

class OptionalMatch(StrictMatch):
    ast_name = 'OptionalMatch'

class Where(QueryElement):
    ast_name = 'Where'

    def __init__(self, query, expression):
        self._query = query
        self.expression = intern_ast(query, expression)

class Match(QueryElement):
    ast_name = 'Match'

    def __init__(self, query, strict, *optionals):
        self._query = query
        self.strict = intern_ast(query, strict)
        self.optionals = [intern_ast(query, opt) for opt in optionals]

class Skip(QueryElement):
    ast_name = 'Skip'

    def __init__(self, query, expression):
        self._query = query
        self.expression = intern_ast(query, expression)

class Limit(QueryElement):
    ast_name = 'Limit'

    def __init__(self, query, expression):
        self._query = query
        self.expression = intern_ast(query, expression)

class Order(QueryElement):
    ast_name = 'Order'

    def __init__(self, query, items):
        self._query = query
        self.items = intern_ast(query, items)

class SortItem(QueryElement):
    ast_name = 'sort'

    def __init__(self, query, expression, direction):
        self._query = query
        self.expression = intern_ast(query, expression)
        self.direction = direction

class ReturnItem(QueryElement):
    ast_name = 'ReturnItem'

    def __init__(self, query, expression, name):
        self._query = query
        self.name = name
        self.expression = intern_ast(query, expression)

class ReturnItems(QueryElement):
    ast_name = 'ReturnItems'

    def __init__(self, query, items):
        self._query = query
        self.items = []
        if len(items) > 0 and items[0] == '*':
            self.items.append(ReturnItem(query, Variable(query, '*'), None))
            items = items[1:]
        if len(items) > 0:
            items = intern_ast(query, items)
        self.items += items

class ReturnBody(QueryElement):
    ast_name = 'ReturnBody'

    def __init__(self, query, items, order, skip, limit):
        self._query = query
        self.items = intern_ast(query, items)
        self.order = intern_ast(query, order)
        self.skip = intern_ast(query, skip)
        self.limit = intern_ast(query, limit)

    def simplify(self):
        self.items = self.items.items
        return self

class Return(QueryElement):
    ast_name = 'Return'

    def __init__(self, query, distinct, body):
        self._query = query
        self.distinct = distinct is not None
        self.body = intern_ast(query, body)

    def simplify(self):
        body = self.body.simplify()
        self.items = body.items
        self.order = body.order
        self.skip = body.skip
        self.limit = body.limit
        delattr(self, 'body')
        return self

class With(Return):
    ast_name = 'With'

    def __init__(self, query, distinct, body, where):
        self._query = query
        self.distinct = distinct is not None
        self.body = intern_ast(query, body)
        self.where = intern_ast(query, where)
        

class SingleQuery(QueryElement):
    ast_name = 'SingleQuery'

    def __init__(self, query, match, with_, return_):
        self._query = query
        self.match = intern_ast(query, match)
        self.with_ = intern_ast(query, with_)
        self.return_ = intern_ast(query, return_)


### AST internment:

def build_ast_name_table():
    table = {}
    module = sys.modules[SingleQuery.__module__]
    for elt in dir(module):
        elt = getattr(module, elt)
        if hasattr(elt, 'ast_name'):
            table[getattr(elt, 'ast_name')] = elt
    return table

AST_NAME_TABLE = build_ast_name_table()

def intern_ast(query, ast):
    if ast is None:
        return None
    elif isinstance(ast, QueryElement):
        return ast
    elif isinstance(ast, list) and len(ast) > 0:
        if isinstance(ast[0], list):
            return [intern_ast(query, elt) for elt in ast]
        else:
            klass = AST_NAME_TABLE.get(ast[0])
            if klass is not None:
                return klass(query, *ast[1:])
    raise Exception('Unhandled expression type: %s' % ast)

def intern_ast_list(query, ast_list):
    if ast_list is None:
        return None
    elif isinstance(ast_list, list):
        return [intern_ast(query, ast) for ast in ast_list]
    raise Exception('Unhandled list type: %s' % ast_list)


### Kypher query:

class KypherQuery(object):
    def __init__(self, query_string):
        self.query = None
        self.variables = {}
        self.simplified = False
        self.parse = Parser(query_string)
        self.query = intern_ast(self, self.parse.Kypher())

    def to_tree(self):
        return (self.__class__.__name__, self.query and self.query.to_tree() or None)

    def simplify(self):
        """Simplifies the structure of the interned parse tree to get rid of unneeded
        elements and nesting that are simply an artifact of the grammar specification.
        """
        if not self.simplified:
            self.query = self.query.simplify()
            self.simplified = True
        return self

    def get_match_clause(self):
        """Return the strict match clause of this query (currently we require exactly one).
        """
        assert isinstance(self.query, SingleQuery), 'Only single-match queries are supported, no unions'
        match_clause = self.simplify().query.match.strict
        assert isinstance(match_clause, StrictMatch), 'Missing strict match clause'
        return match_clause

    def get_optional_match_clauses(self):
        """Return the optional match clauses of this query (zero or more).
        """
        assert isinstance(self.query, SingleQuery), 'Only single-match queries are supported, no unions'
        optional_clauses = self.simplify().query.match.optionals
        return optional_clauses

    def get_with_clause(self):
        assert isinstance(self.query, SingleQuery), 'Only single-match queries are supported, no unions'
        self.simplify()
        with_ = self.query.with_
        return with_

    def get_return_clause(self):
        assert isinstance(self.query, SingleQuery), 'Only single-match queries are supported, no unions'
        self.simplify()
        ret = self.query.return_
        return ret

    def get_order_clause(self):
        ret = self.get_return_clause()
        order = ret and ret.order or None
        return order

    def get_skip_clause(self):
        ret = self.get_return_clause()
        skip = ret and ret.skip or None
        return skip

    def get_limit_clause(self):
        ret = self.get_return_clause()
        limit = ret and ret.limit or None
        return limit

    def create_anonymous_variable(self):
        i = 1
        while True:
            varname = '_x%04d' % i
            if varname not in self.variables:
                var = AnonymousVariable(self, varname)
                self.variables[varname] = var
                return var
            i += 1


### Top level:

def parse(query_string):
    return Parser(query_string).Kypher()

def intern(query_string):
    return KypherQuery(query_string)


# Example w/ interesting differences between node and relation patterns:
# - node patterns can have multiple labels (and-ed), all with a prefixing colon
# - relation patterns can have alternative labels, only the first prefixed with a colon
#
# cq = cp.intern("MATCH (n:Person :Human {name: 'Bob'})-[:Loves | Adores {id: '17'}]->(n2) RETURN DISTINCT n;")
