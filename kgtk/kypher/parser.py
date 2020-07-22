"""
Cypher parser (derived from ruruki.parsers.cypher_parser.py
https://s3.amazonaws.com/artifacts.opencypher.org/cypher.ebnf
"""

import sys
import pprint

import parsley

pp = pprint.PrettyPrinter(indent=4)


CYPHER_GRAMMAR = r"""
    Cypher = WS Statement:s (WS ';')? WS -> s

    Statement = Query

    Query = RegularQuery

    RegularQuery = SingleQuery:sq SP U N I O N SP A L L SP RegularQuery:rq -> ["UnionAll", sq, rq]
                 | SingleQuery:sq SP U N I O N SP RegularQuery:rq -> ["Union", sq, rq]
                 | SingleQuery:sq

    # SingleQuery = Clause:head (WS Clause)*:tail -> ["SingleQuery", [head] + tail]

    # Clause = Match
    #        | Unwind
    #        | Merge
    #        | Create
    #        | Set
    #        | Delete
    #        | Remove
    #        | With
    #        | Return

    SingleQuery = Match?:m WS With?:w WS Return:r -> ["SingleQuery", m, w, r]

    # TODO: Not usre if I need to handle optional !!
    Match = (O P T I O N A L SP)? M A T C H WS Pattern:p (WS Where)?:w -> ["Match", p, w]

    Unwind = U N W I N D WS Expression:ex SP A S SP Variable:v -> ["Unwind", ex, v]

    Merge = M E R G E WS PatternPart:head (SP MergeAction)*:tail -> ["Merge", [head] + tail]

    MergeAction = O N SP M A T C H SP Set:s -> ["MergeActionMatch", s]
                | O N SP C R E A T E SP Set:s -> ["MergeActionCreate", s]

    Create = C R E A T E WS Pattern:p -> ["Create", p]

    Set = S E T SP SetItem:head (WS ',' WS SetItem)*:tail -> ["Set", [head] + tail]

    SetItem = PropertyExpression:pex '=' Expression:ex -> ["SetItemPropertyExpression", pex, ex]
            | Variable:v '=' Expression:ex -> ["SetItem", v, ex]
            | Variable:v '+=' Expression:ex -> ["SetItem", v, ex]
            | Variable:v NodeLabels:ex -> ["SetItem", v, ex]

    Delete = (D E T A C H SP)? D E L E T E SP Expression:head (',' WS Expression )*:tail -> ["Delete", [head] + tail]

    Remove = R E M O V E SP RemoveItem:head (WS ',' WS RemoveItem)*:tail -> ["Remove", [head] + tail]

    RemoveItem = Variable:v NodeLabels:nl -> ["RemoveItemVar", v, nl]
                | PropertyExpression:p -> ["RemoveItemPe", p]

    With = W I T H (SP D I S T I N C T)?:d SP ReturnBody:rb (Where)?:w -> ["With", d, rb, w]

    Return = R E T U R N (SP D I S T I N C T)?:d SP ReturnBody:rb -> ["Return", d, rb]

    ReturnBody = ReturnItems:ri (SP Order)?:o (SP Skip)?:s (SP Limit)?:l -> ["ReturnBody", ri, o, s, l]

    ReturnItems = ('*' | ReturnItem):head
                (WS ',' WS ReturnItem )*:tail -> ["ReturnItems", [head] + tail]

    ReturnItem = Expression:ex SP A S SP SymbolicName:s -> ["ReturnItem", ex, s]
               | Expression:ex -> ["ReturnItem", ex, None]

    Order =  O R D E R SP B Y SP SortItem:head (',' WS SortItem)*:tail -> ["Order", [head] + tail]

    Skip =  S K I P SP Expression:ex -> ["Skip", ex]

    Limit =  L I M I T SP Expression:ex -> ["Limit", ex]

    SortItem = Expression:ex (D E S C E N D I N G | D E S C) -> ["sort", ex, "desc"]
             | Expression:ex (A S C E N D I N G | A S C)? -> ["sort", ex, "asc"]

    Where = W H E R E SP Expression:ex -> ["Where", ex]

    Pattern = PatternPart:head (',' WS PatternPart)*:tail -> [head] + tail

    PatternPart = (Variable:v WS '=' WS AnonymousPatternPart:ap) -> ["PatternPart", v, ap]
                | AnonymousPatternPart:ap -> ["PatternPart", None, ap]

    AnonymousPatternPart = PatternElement

    PatternElement = (
                        NodePattern:np
                        (WS PatternElementChain)*:pec
                    ) -> ["PatternElement", np, pec]
                    | '(' PatternElement:pe ')' -> pe

    NodePattern = '(' WS
                 (
                    SymbolicName:s WS -> s
                 )?:v
                 (
                     NodeLabels:nl WS -> nl
                 )?:nl
                 (
                     Properties:p WS -> p
                 )?:p
                ')' -> ["NodePattern", s, nl, p]

    PatternElementChain = RelationshipPattern:rp WS NodePattern:np -> ["PatternElementChain", rp, np]

    RelationshipPattern = LeftArrowHead?:la WS Dash WS RelationshipDetail?:rd WS Dash WS RightArrowHead?:ra -> ["RelationshipsPattern", la, rd, ra]

    RelationshipDetail = '['
                      Variable?:v
                      '?'?:q
                      RelationshipTypes?:rt
                      ('*' RangeLiteral)?:rl WS
                      Properties?:p
                      ']' -> ["RelationshipDetail", v, q, rt, rl, p]

    Properties = MapLiteral
               | Parameter

    RelationshipTypes = ':' RelTypeName:head (WS '|' ':'? WS RelTypeName)*:tail -> ["RelationshipTypes", head] + tail

    NodeLabels = NodeLabel:head (WS NodeLabel)*:tail -> [head] + tail

    NodeLabel = ':' LabelName:n -> ["NodeLabel", n]

    RangeLiteral = (WS IntegerLiteral)?:start WS ('..' WS IntegerLiteral)?:stop WS -> slice(start, stop)

    LabelName = SymbolicName

    RelTypeName = SymbolicName

    Expression = Expression12

    Expression12 = Expression11:ex1 SP O R SP Expression12:ex2 -> ["or", ex1, ex2]
                 | Expression11

    Expression11 = Expression10:ex1 SP X O R SP Expression11:ex2 -> ["xor", ex1, ex2]
                 | Expression10

    Expression10 = Expression9:ex1 SP A N D SP Expression10:ex2 -> ["and", ex1, ex2]
                 | Expression9

    Expression9 = N O T SP Expression9:ex -> ["not", ex]
                | Expression8

    Expression8 = Expression7:ex1 WS '='  WS Expression8:ex2 -> ["eq",  ex1, ex2]
                | Expression7:ex1 WS '<>' WS Expression8:ex2 -> ["neq", ex1, ex2]
                | Expression7:ex1 WS '!=' WS Expression8:ex2 -> ["neq", ex1, ex2]
                | Expression7:ex1 WS '<'  WS Expression8:ex2 -> ["lt",  ex1, ex2]
                | Expression7:ex1 WS '>'  WS Expression8:ex2 -> ["gt",  ex1, ex2]
                | Expression7:ex1 WS '<=' WS Expression8:ex2 -> ["lte", ex1, ex2]
                | Expression7:ex1 WS '>=' WS Expression8:ex2 -> ["gte", ex1, ex2]
                | Expression7

    Expression7 = Expression6:ex1 WS '+' WS Expression7:ex2 -> ["add", ex1, ex2]
                | Expression6:ex1 WS '-' WS Expression7:ex2 -> ["sub", ex1, ex2]
                | Expression6

    Expression6 = Expression5:ex1 WS '*' WS Expression6:ex2 -> ["multi", ex1, ex2]
                | Expression5:ex1 WS '/' WS Expression6:ex2 -> ["div",   ex1, ex2]
                | Expression5:ex1 WS '%' WS Expression6:ex2 -> ["mod",   ex1, ex2]
                | Expression5

    Expression5 = Expression4:ex1 WS '^' WS Expression5:ex2 -> ["hat", ex1, ex2]
                | Expression4

    Expression4 = '+' WS Expression4
                | '-' WS Expression4:ex -> ["minus", ex]
                | Expression3

    Expression3 = Expression2:ex1
                  (
                    WS '[' Expression:prop_name ']' -> ["PropertyLookup", prop_name]
                    | WS '[' Expression?:start '..' Expression?:end ']' -> ["slice", start, end]
                    | (
                        WS '=~' -> "regex"
                        | SP I N -> "in"
                        | SP S T A R T S SP W I T H -> "starts_with"
                        | SP E N D S SP W I T H  -> "ends_with"
                        | SP C O N T A I N S  -> "contains"
                    ):operator WS Expression2:ex2 -> [operator, ex2]
                    | SP I S SP N U L L  -> ["is_null"]
                    | SP I S SP N O T SP N U L L -> ["is_not_null"]
                  )+:c -> ["Expression3", ex1, c]
                  | Expression2

    Expression2 = Atom:a (PropertyLookup | NodeLabels)+:c -> ["Expression2", a, c]
                  | Atom

    Atom = NumberLiteral
         | StringLiteral
         | Parameter
         | T R U E -> ["Literal", True]
         | F A L S E -> ["Literal", False]
         | N U L L -> ["Literal", None]
         | CaseExpression
         | C O U N T '(' '*' ')' -> ["count *"]
         | MapLiteral
         | ListComprehension
         | '['
                (
                    WS Expression:head WS
                    (',' WS Expression:item WS -> item
                    )*:tail -> [head] + tail
                    |
                    -> []
                ):ex
            ']' -> ["List", ex]
         | F I L T E R WS '(' WS FilterExpression:fex WS ')' -> ["Filter", fex]
         | E X T R A C T WS '(' WS FilterExpression:fex WS (WS '|' Expression)?:ex ')' -> ["Extract", fex, ex]
         | A L L WS '(' WS FilterExpression:fex WS ')' -> ["All", fex]
         | A N Y WS '(' WS FilterExpression:fex WS ')' -> ["Any", fex]
         | N O N E WS '(' WS FilterExpression:fex WS ')' -> ["None", fex]
         | S I N G L E WS '(' WS FilterExpression:fex WS ')' -> ["Single", fex]
         | RelationshipsPattern
         | parenthesizedExpression
         | FunctionInvocation
         | Variable

    parenthesizedExpression = '(' WS Expression:ex WS ')' -> ex

    RelationshipsPattern = NodePattern:np (WS PatternElementChain)?:pec -> ["RelationshipsPattern", np, pec]

    FilterExpression = IdInColl:i (WS Where)?:w -> ["FilterExpression", i, w]

    IdInColl = Variable:v SP I N SP Expression:ex -> ["IdInColl", v, ex]

    FunctionInvocation = FunctionName:func
                        WS '(' WS
                        (D I S T I N C T WS -> "distinct")?:distinct
                        (
                            Expression:head
                            (
                                ',' WS Expression
                            )*:tail -> [head] + tail
                        | -> []
                        ):args
                        WS ')' -> ["call", func, distinct, args]

    FunctionName = SymbolicName

    ListComprehension = '[' FilterExpression:fex (WS '|' Expression)?:ex ']' -> ["ListComprehension", fex, ex]

    # PropertyLookup = WS '.' WS ((PropertyKeyName ('?' | '!')) | PropertyKeyName)
    PropertyLookup = WS '.' WS PropertyKeyName:n -> ["PropertyLookup", n]

    CaseExpression =
                     C A S E WS
                     (Expression)?:ex
                     (WS CaseAlternatives)+:cas 
                     (WS E L S E WS Expression)?:el
                     WS E N D
                     -> ["Case", ex, cas, el]

    CaseAlternatives = W H E N WS Expression:ex1 WS T H E N WS Expression:ex2 -> [ex1, ex2]

    Variable = SymbolicName:s -> ["Variable", s]

    StringLiteral = (
                  '"' (~('"'|'\\') anything | EscapedChar)*:cs '"' -> "".join(cs)
                  | "'" (~("'"|'\\') anything | EscapedChar)*:cs "'" -> "".join(cs)
                  ):l -> ["Literal", l]

    EscapedChar = '\\'
                ('\\' -> '\\'
                | "'" -> "'"
                | '"' -> '"'
                | N -> '\n'
                | R -> '\r'
                | T -> '\t'
                | '_' -> '_'
                | '%' -> '%'
                )

    NumberLiteral = (
                  DoubleLiteral
                  | IntegerLiteral
                  ):l -> ["Literal", l]

    MapLiteral = '{' WS
                 (
                    (
                        PropertyKeyName:k WS ':' WS Expression:v -> (k, v)
                    ):head WS
                    (
                        ',' WS PropertyKeyName:k WS ':' WS Expression:v WS -> (k, v)
                    )*:tail -> [head] + tail
                 | -> []):pairs
                '}' -> ["Literal", dict(pairs)]

    Parameter = '{' WS (SymbolicName | DecimalInteger):p WS '}' -> ["Parameter", p]

    PropertyExpression = Atom:a (WS PropertyLookup)*:opts -> ["Expression", a, opts]

    PropertyKeyName = SymbolicName

    IntegerLiteral = HexInteger
                   | OctalInteger
                   | DecimalInteger

    OctalDigit = ~('8'|'9') digit

    OctalInteger = '0' <OctalDigit+>:ds -> int(ds, 8)

    HexDigit = digit | A | B | C | D | E | F

    HexInteger = '0' X <HexDigit+>:ds -> int(ds, 16)

    DecimalInteger = <digit+>:ds -> int(ds)

    DoubleLiteral = ExponentDecimalReal
                  | RegularDecimalReal

    ExponentDecimalReal = <(DecimalInteger | RegularDecimalReal) E DecimalInteger>:ds -> float(ds)

    RegularDecimalReal = <digit+ '.' digit+>:ds -> float(ds)

    SymbolicName = UnescapedSymbolicName
                 | EscapedSymbolicName

    UnescapedSymbolicName = <letter ('_' | letterOrDigit)*>

    EscapedSymbolicName = '`' (~'`' anything | "``" -> '`')*:cs '`' -> "".join(cs)

    WS = whitespace*

    SP = whitespace+

    whitespace = ' '
               | '\t'
               | '\n'
               | Comment

    Comment = "/*" (~"*/" anything)* "*/"
            | "//" (~('\r'|'\n') anything)* '\r'? ('\n'|end)

    LeftArrowHead = '<'

    RightArrowHead = '>'

    Dash = '-'

    A = 'A' | 'a'

    B = 'B' | 'b'

    C = 'C' | 'c'

    D = 'D' | 'd'

    E = 'E' | 'e'

    F = 'F' | 'f'

    G = 'G' | 'g'

    H = 'H' | 'h'

    I = 'I' | 'i'

    K = 'K' | 'k'

    L = 'L' | 'l'

    M = 'M' | 'm'

    N = 'N' | 'n'

    O = 'O' | 'o'

    P = 'P' | 'p'

    R = 'R' | 'r'

    S = 'S' | 's'

    T = 'T' | 't'

    U = 'U' | 'u'

    V = 'V' | 'v'

    W = 'W' | 'w'

    X = 'X' | 'x'

    Y = 'Y' | 'y'

    Z = 'Z' | 'z'
    """

# for now we rebuild the grammar every time we load:
Parser = parsley.makeGrammar(CYPHER_GRAMMAR, {})

"""
# if we want to use this for production, we can save the grammar as a Python file like this:
>>> import ometa.grammar
>>> cygram = ometa.grammar.OMeta.makeGrammar(cp.CYPHER_GRAMMAR)
>>> open('kgtk/cypher/cypher_grammar_compiled.py', 'w').write(cygram.__loader__.source)

# and then load it like this - there doesn't seem to be a better user API for this:
>>> import parsley
>>> import ometa.grammar
>>> import kgtk.cypher.cypher_grammar_compiled as cgc
>>> cgram = cgc.createParserClass(ometa.grammar.OMetaBase, {})
>>> wcgram = parsley.wrapGrammar(cgram)
>>> wcgram('MATCH (n1) RETURN r').Cypher()
['SingleQuery', ['Match', [['PatternPart', None, ... None, None, None]]]]
"""


"""
# 75 Output patterns:
# - there are two with varying signatures - might be a mistake
# - we are currently handling about 40

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

def normalize_object(obj):
    if hasattr(obj, 'normalize'):
        return obj.normalize()
    elif isinstance(obj, list):
        for i in range(len(obj)):
            obj[i] = normalize_object(obj[i])
        return obj
    elif isinstance(obj, dict):
        table = {}
        for key, val in obj.items():
            if key.startswith('_') or val is None:
                continue
            table[key] = normalize_object(val)
        for key, val in table.items():
            obj[key] = val
        return obj
    else:
        return obj

class QueryElement(object):
    ast_name = None

    def to_tree(self):
        return (self.__class__.__name__, object_to_tree(self.__dict__))

    def normalize(self):
        normalize_object(self.__dict__)
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
        self.properties = None
        if properties is not None:
            if properties[0] == 'Literal':
                self.properties = {key:intern_ast(query, val) for key, val in properties[1].items()}
            else:
                # parameter:
                self.properties = intern_ast(query, properties)

    def normalize(self):
        self.variable = Variable(self._query, self.variable)
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
            head = args[0]
            tail = args[1] is not None and list(args[1:]) or []
            PatternElement.__init__(self, query, head, tail)
            self.__class__ = PatternElement
            return
        left_arrow, detail, right_arrow = args
        self._query = query
        self.left_arrow = left_arrow
        self.detail = intern_ast(query, detail)
        self.right_arrow = right_arrow
        # a bidirectional arrow is legal in the grammar but not legal Cypher;
        if left_arrow and right_arrow:
            raise Exception('Illegal bidirectional arrow: %s' % str(self.normalize().to_tree()))

    def normalize(self):
        self.detail = normalize_object(self.detail)
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

    def normalize(self):
        return self.labels

class PatternElementChain(QueryElement):
    ast_name = 'PatternElementChain'

    def __init__(self, query, head, tail):
        self._query = query
        self.head = intern_ast(query, head)
        self.tail = intern_ast(query, tail)

    def normalize(self):
        return [self.head.normalize(), self.tail.normalize()]
        
class PatternElement(QueryElement):
    ast_name = 'PatternElement'

    def __init__(self, query, element, chain):
        self._query = query
        self.head = intern_ast(query, element)
        self.tail = intern_ast_list(query, chain)

    def normalize(self):
        chain = [self.head.normalize()]
        for subchain in normalize_object(self.tail):
            chain += subchain
        return chain
    
class PatternPart(QueryElement):
    ast_name = 'PatternPart'

    def __init__(self, query, variable, pattern):
        self._query = query
        # these can either be named with a variable or anonymous:
        self.variable = intern_ast(query, variable)
        self.pattern = intern_ast(query, pattern)

    def normalize(self):
        # simply rename to `PathPattern':
        return PathPattern(self._query, normalize_object(self.variable), normalize_object(self.pattern))

class PathPattern(QueryElement):

    def __init__(self, query, variable, pattern):
        self._query = query
        # these can either be named with a variable or anonymous:
        self.variable = variable
        self.pattern = pattern


# Query top level:

class Match(QueryElement):
    ast_name = 'Match'

    def __init__(self, query, pattern, where):
        self._query = query
        self.pattern = intern_ast_list(query, pattern)
        self.where = intern_ast(query, where)

class Where(QueryElement):
    ast_name = 'Where'

    def __init__(self, query, expression):
        self._query = query
        self.expression = intern_ast(query, expression)


class ReturnItem(QueryElement):
    ast_name = 'ReturnItem'

    def __init__(self, query, expression, name):
        """TO DO"""
        self._query = query
        pass

class ReturnItems(QueryElement):
    ast_name = 'ReturnItems'

    def __init__(self, query, items):
        """TO DO"""
        self._query = query
        pass

class ReturnBody(QueryElement):
    ast_name = 'ReturnBody'

    def __init__(self, query, items, order, skip, limit):
        """TO DO"""
        self._query = query
        pass

class Return(QueryElement):
    ast_name = 'Return'

    def __init__(self, query, distinct, body):
        """TO DO"""
        self._query = query
        pass


class SingleQuery(QueryElement):
    ast_name = 'SingleQuery'

    def __init__(self, query, match, with_, return_):
        """TO DO: COMPLETE"""
        self._query = query
        self.match = intern_ast(query, match)


# AST internment:

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


# Cypher query:

class CypherQuery(object):
    def __init__(self, ast=None, query_string=None):
        self.query = None
        if ast is not None:
            self.query = intern_ast(self, ast)
        elif query_string is not None:
            self.query = intern_ast(self, parse(query_string))

    def to_tree(self):
        return (self.__class__.__name__, self.query and self.query.to_tree() or None)

    def normalize(self):
        self.query = self.query.normalize()
        return self


# Top level:

def parse(query_string):
    return Parser(query_string).Cypher()

def intern(query_string):
    return CypherQuery(query_string=query_string)


# Example w/ interesting differences between node and relation patterns:
# - node patterns must have a variable (or name), relation patterns can omit it
# - node patterns can have multiple labels (and-ed), all with a prefixing colon
# - relation patterns can have alternative labels, only the first prefixed with a colon
#
# cq = cp.intern("MATCH (n:Person :Human {name: 'Bob'})-[:Loves | Adores {id: '17'}]->(n2) RETURN DISTINCT n;")

# TO DO next:
# - flesh out the TO DOs above
# - add missing pattern elements
# - expression simplification and normalization (e.g., with <-x-> patterns)
# - implement initial simple eval plans
