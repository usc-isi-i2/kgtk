"""
KGTK core SQL functions
"""

import sys
import re
from   functools import lru_cache

from   kgtk.exceptions import KGTKException
from   kgtk.kypher.utils import *
from   kgtk.kypher.functions import *
import kgtk.kypher.parser as parser


### Core functions:

# Naming convention: a suffix of _string indicates that the resulting
# value will be additionally converted to a KGTK string literal.  The
# same could generally be achieved by calling 'kgtk_stringify' explicitly.

# Regular expressions:

@lru_cache(maxsize=100)
def _get_regex(regex):
    return re.compile(regex)
    
@sqlfun(num_params=2, deterministic=True)
def kgtk_regex(x, regex):
    """Regex matcher that implements the Cypher '=~' semantics which must match the whole string.
    """
    m = isinstance(x, str) and _get_regex(regex).match(x) or None
    return m is not None and m.end() == len(x)


# NULL value utilities:

# In the KGTK file format we cannot distinguish between empty and NULL values.
# Both KGTKReader and SQLite map missing values onto empty strings, however,
# database functions as well as our KGTK user functions return NULL for undefined
# values.  These can be tested via 'IS [NOT] NULL', however, in some cases it is
# convenient to convert from one to the other for more uniform tests and queries.

@sqlfun(num_params=1, deterministic=True)
def kgtk_null_to_empty(x):
    """If 'x' is NULL map it onto the empty string, otherwise return 'x' unmodified.
    """
    if x is None:
        return ''
    else:
        return x

@sqlfun(num_params=1, deterministic=True)
def kgtk_empty_to_null(x):
    """If 'x' is the empty string, map it onto NULL, otherwise return 'x' unmodified.
    """
    if x == '':
        return None
    else:
        return x


# Python eval:

_sqlstore_module = sys.modules['kgtk.kypher.sqlstore']
_builtins_module = sys.modules['builtins']

def get_pyeval_fn(fnname):
    pos = fnname.rfind('.')
    if pos < 0:
        return getattr(_sqlstore_module, fnname, None) or getattr(_builtins_module, fnname)
    else:
        # we lookup the module name relative to this module in case somebody imported an alias:
        return getattr(getattr(_sqlstore_module, fnname[0:pos]), fnname[pos+1:])

@sqlfun(num_params=-1)
def pyeval(*expression):
    """Python-eval 'expression' and return the result (coerce value to string if necessary).
    Multiple 'expression' arguments will be concatenated first.
    """
    try:
        val = eval(''.join(expression))
        return isinstance(val, (str, int, float)) and val or str(val)
    except:
        pass

@sqlfun(num_params=-1)
def pycall(fun, *arg):
    """Python-call 'fun(arg...)' and return the result (coerce value to string if necessary).
    'fun' must name a function and may be qualified with a module imported by --import.
    """
    try:
        val = get_pyeval_fn(fun)(*arg)
        return isinstance(val, (str, int, float)) and val or str(val)
    except:
        pass


# Aggregate functions

# support SqlFunction.is_aggregate() test:
BuiltinAggregateFunction(name='avg').define()
BuiltinAggregateFunction(name='count').define()
BuiltinAggregateFunction(name='group_concat').define()
BuiltinAggregateFunction(name='max').define()
BuiltinAggregateFunction(name='min').define()
BuiltinAggregateFunction(name='sum').define()
BuiltinAggregateFunction(name='total').define()


# Special SQLite and Kypher functions:

class Cast(BuiltinFunction):
    """Implement SQLite CAST as a Kypher function (no equivalent in Cypher).
    """

    def translate_call_to_sql(self, query, expr, state):
        """Translate CAST(expr, type) to SQL.
        """
        if len(expr.args) == 2 and isinstance(expr.args[1], parser.Variable):
            arg = query.expression_to_sql(expr.args[0], state)
            typ = expr.args[1].name
            return f'{self.get_name()}({arg} AS {typ})'
        else:
            raise KGTKException("Illegal CAST expression")

Cast(name='cast').define()

class Likelihood(BuiltinFunction):
    """Special-case SQLite LIKELIHOOD translation.
    """

    def translate_call_to_sql(self, query, expr, state):
        """Translate SQLite LIKELIHOOD(expr, prob) expression to SQL which needs a compile-time constant
        for its probability argument instead of the value parameters we usually use to supply literals.
        """
        if len(expr.args) == 2 and isinstance(expr.args[1], parser.Literal) and isinstance(expr.args[1].value, (int, float)):
            arg = query.expression_to_sql(expr.args[0], state)
            prob = expr.args[1].value
            return f'{self.get_name()}({arg}, {prob})'
        else:
            raise Exception("Illegal LIKELIHOOD expression")

Likelihood(name='likelihood').define()

class Concat(BuiltinFunction):
    """Special-case Cypher's CONCAT function which is handled by SQLite's ||-operator.
    """
    
    def translate_call_to_sql(self, query, expr, state):
        """Translate CONCAT(arg...) to SQL using SQLite's ||-operator.
        """
        args = [query.expression_to_sql(arg, state) for arg in expr.args]
        return f'({" || ".join(args)})'

Concat(name='concat').define()


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

@sqlfun(num_params=2, deterministic=True)
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
