"""
SQL function definition API
"""

import sqlite3
import copy

from   kgtk.exceptions import KGTKException


### SqlFunction API

# Provides enhanced functionality compared to original API such as:
# - forward-declarations for lazy loading of functions and support modules
# - @sqlfun decorator for easy definition
# - customizable call-translation API via 'translate_call_to_sql' needed
#   by funcions such as 'cast' or 'likelihood' or the new vector functions
# - customizable code-loading API that allows the same function to be associated
#   with different call-specific codes and closure variables (also primarily
#   needed to properly optimize vector function calls)
#
# We basically support three aspects for each SQL function:
# - definition
# - translation (default or specialized to a function or call context)
# - code generation and registration (default or specialized to a call context)
#
# TO DO:
# - handle multi-threading: the call-specific code generation should support
#   this for multiple threads as well, but the details need to be fleshed out


class SqlFunction(object):

    def __init__(self, name=None, code=None, num_params=None, deterministic=False):
        """Create a function object with 'name', 'code', specify its number of
        parameters with 'num_params' and specify whether it is 'deterministic'
        (those last three parameters mirror 'sqlite3.Cursor.create_function').
        If no 'name' is supplied it will be inferred from 'code', but at least
        one of the two needs to be supplied.  If 'num_params' is left unspecified,
        it will be inferred at code registration time which will require loading
        the 'inspect' module, so it should generally be specified to minimize
        the number of imported modules.
        """
        if name is None and code is not None:
            name = code.__name__
        if name is None:
            raise KGTKException(f'cannot determine name of SQL function')
        self.name = name
        self.code = code
        self.num_params = num_params
        self.deterministic = deterministic
        self.store = None
        self.uniquify = False

    _definitions = {}
    
    def define(self):
        """Add this instance under its current name to the global registry.
        This allows the same function definition to be used as different variants
        under different names (see also 'uniquify_name').
        """
        SqlFunction._definitions[self.get_name()] = self
        return self

    @staticmethod
    def is_defined(name):
        """Return True if a function with 'name' is already defined or forward-declared.
        """
        name = SqlFunction.normalize_name(name)
        return SqlFunction._definitions.get(name) is not None

    @staticmethod
    def declare(module_name, *func_name):
        """Declare module 'module_name' as the one containing definitions for all
        the listed function names 'func_name'.  This allows us to properly translate
        function calls without having to eagerly import them all.
        """
        for func in func_name:
            func = SqlFunction.normalize_name(func)
            if func not in SqlFunction._definitions:
                SqlFunction._definitions[func] = module_name

    @staticmethod
    def import_declared_function(name):
        """Import the forward-declared function 'name' and return it.
        Raise an error if the function is not forward-declared or cannot be found.
        """
        nname = SqlFunction.normalize_name(name)
        module = SqlFunction._definitions.get(nname)
        if not isinstance(module, str):
            raise KGTKException(f'not a forward-declared SQL function: {name}')
        # we have a proper forward-declaration to a defining module, import it:
        exec(f'import {module}')
        fun = SqlFunction._definitions.get(nname)
        if not isinstance(fun, SqlFunction):
            raise KGTKException(f'missing definition for declared SQL function: {name}')
        return fun

    @staticmethod
    def get_function(name, store=None, error=True, **kwargs):
        """Lookup a customizable copy of the function object for 'name'.
        If 'name' is undefined an error will be raised unless 'error' is False.
        The resulting object will be a new copy of the definition object which
        will not be shared by any subsequent calls to this or other functions.
        Assign 'store' as the SQL store associated with the resulting object
        and add any additional 'kwargs' as custom slots to the object.
        """
        fun = SqlFunction._definitions.get(SqlFunction.normalize_name(name))
        if fun is None:
            if error:
                raise KGTKException(f'undefind SQL function: {name}')
            return None
        elif isinstance(fun, str):
            # we have a forward-declaration to a defining module, import it
            # (any errors here are real and not subject to the 'error' flag):
            fun = SqlFunction.import_declared_function(name)
        # create a copy of the definition with some additional values filled in:
        fun = copy.copy(fun)
        fun.store = store
        for key, value in kwargs.items():
            setattr(fun, key, value)
        return fun

    @staticmethod
    def is_aggregate(name):
        """Return True if a function with 'name' is defined or forward-declared
        as an aggregation function.
        """
        # we don't use an instance method for this test, since we need to be able
        # to test this before we actually have an object in hand:
        nname = SqlFunction.normalize_name(name)
        fun = SqlFunction._definitions.get(nname)
        if isinstance(fun, str):
            # we have a forward-declaration to a defining module, import it:
            fun = SqlFunction.import_declared_function(name)
        return isinstance(fun, AggregateFunction)

    @staticmethod
    def is_virtual_graph(name):
        """Return True if a function with 'name' is defined or forward-declared
        as a virtual graph function.
        """
        # we don't use an instance method for this test, since we need to be able
        # to test this before we actually have an object in hand:
        nname = SqlFunction.normalize_name(name)
        fun = SqlFunction._definitions.get(nname)
        if isinstance(fun, str):
            # we have a forward-declaration to a defining module, import it:
            fun = SqlFunction.import_declared_function(name)
        return isinstance(fun, VirtualGraphFunction)
    
    @staticmethod
    def normalize_name(name):
        return name.lower()
    
    def get_name(self):
        """Return the normalized name of this function.
        """
        return self.normalize_name(self.name)

    def get_code(self):
        """Return the code object of this function.  This can return custom adaptations
        relative to a particular function or call context.
        """
        if self.code is None:
            raise KGTKException(f'missing code object for SQL function: {self.name}')
        return self.code

    def get_num_params(self):
        """Return the number of parameters expected by this function (-1 for variable).
        If not previously specified, infer it from the code object via 'inspect'.
        """
        if self.num_params is None:
            import inspect
            argspec = inspect.getfullargspec(self.get_code())
            if argspec.varargs or argspec.varkw:
                self.num_params = -1
            else:
                self.num_params = len(argspec.args)
        return self.num_params

    def get_deterministic(self):
        """Return whether this function is deterministic, that is, always returns the same result
        when called with the same arguments.
        """
        return self.deterministic
    
    def load(self):
        """Register the code of this function into the connection object of the associated SQL store.
        If self.uniquify is True, create a unique name derived from the functions current name.  This
        means the translator needs to access that uniquified name after 'load' was called to create
        a working translated query (see 'translate_call_to_sql').
        """
        code = self.get_code()
        determ = self.get_deterministic()
        if self.uniquify:
            self.uniquify_name()
        self.store.load_user_function(self.get_name(), self.get_num_params(), code, deterministic=determ)

    def uniquify_name(self):
        """Generate a unique name for this function based on its current name.
        """
        self.name = f'{self.get_name()}_{len(self.store.get_user_functions())}'

    def translate_call_to_sql(self, query, expr, state):
        """API method called by the query translator to translate function calls.
        This default method should suffice for most simple user-defined functions.
        """
        args = [query.expression_to_sql(arg, state) for arg in expr.args]
        distinct = expr.distinct and 'DISTINCT ' or ''
        # this will generate a possibly new name, which is why we call this here
        # so we can consider that in the function call translation generated below:
        self.load()
        return f'{self.get_name()}({distinct}{", ".join(args)})'


class AggregateFunction(SqlFunction):
    """Functions that implement aggregation operations.
    """
    def load(self):
        # TO DO: generalize this to call 'self.store.load_aggregate_function()
        #        to properly handle user-defined aggregate functions (see sqlite3 API)
        super().load()

class BuiltinFunction(SqlFunction):
    """Functions that are supported directly by the underlying database.
    These do not need to be defined or loaded.
    """

    def get_code(self):
        """Return the code object of this function which will generally be None
        for builtins, but not raise an error in this case.
        """
        return self.code

    def load(self):
        """Nothing to be done for builtins.
        """
        pass

class BuiltinAggregateFunction(BuiltinFunction, AggregateFunction):
    """Builtin functions that implement aggregation operations.
    """
    pass

class VirtualTableFunction(SqlFunction):
    """Functions that return multiple rows of values per set of inputs and
    operate like a virtual database table and not a scalar function.
    """

    # input parameters and output columns:
    params = ['arg1', 'arg2']
    columns = ['out1', 'out2']

    @staticmethod
    def initialize(vtfun, arg1, arg2='defarg2'):
        """Called by the virtual table function API when a function is called with a set of
        input parameters.  In our adaptation here, this static method becomes the implementation
        of TableFunction.initialize() on the dynamic class we create in self.get_code() below.
        """
        vtfun.arg1 = arg1
        vtfun.arg2 = arg2
        vtfun.result_rows = None

    @staticmethod
    def iterate(vtfun, idx):
        """Called by the virtual table function API when a new set of output values is requested.
        In our adaptation here, this static method becomes the implementation of TableFunction.iterate()
        on the dynamic class we create in self.get_code() below.  This just calls out to
        'vtfun.compute_result_rows()' and should generally not require any specialization on subclasses.
        """
        if vtfun.result_rows is None:
            vtfun.result_rows = vtfun.compute_result_rows()
        return next(vtfun.result_rows)

    @staticmethod
    def compute_result_rows(vtfun):
        """Compute an iterator that produces the result rows for a particular set of inputs.
        Each result row must be a tuple that has values for all output 'columns' specified above.
        Called by the default implementation of vtfun.iterate().
        """
        return iter([(vtfun.arg1, vtfun.arg2)])
    
    def get_num_params(self):
        """Return the number of parameters expected by this function (-1 for variable).
        If not previously specified, infer it from the code object via 'inspect'.
        """
        if self.num_params is None:
            self.num_params = len(self.params)
        return self.num_params

    def get_code(self):
        """Return the code object of this function.  This can return custom adaptations
        relative to a particular function or call context.  For table-valued functions
        the code object has to be represented as a class object subclassing
        playhouse.sqlite_ext.TableFunction, so we create such subclasses dynamically here.
        Custom adaptations can link to additional objects of interest such as vector stores.
        """
        if self.code is None:
            try:
                import playhouse.sqlite_ext as sqlext
            except:
                raise KGTKException(f"you need to 'pip install peewee' to use table-valued functions")
            # multiple-inheritance breaks things, so we inherit the relevant information by hand:
            self.code = type(self.get_name(), (sqlext.TableFunction,), {
                'name': self.get_name(),
                'params': self.params,
                'columns': self.columns,
                'initialize': getattr(type(self), 'initialize'),
                'iterate': getattr(type(self), 'iterate'),
                'compute_result_rows': getattr(type(self), 'compute_result_rows'),
            })
        return self.code
    
    def load(self):
        """Register the code of this function into the connection object of the associated SQL store.
        If self.uniquify is True, create a unique name derived from the functions current name.  This
        means the translator needs to access that uniquified name after 'load' was called to create
        a working translated query (see 'translate_call_to_sql').
        """
        self.uniquify_name()
        code = self.get_code()
        self.store.load_user_function(self.get_name(), self.get_num_params(), code)

    def translate_call_to_sql(self, query, clause, state):
        """Default method called by query.pattern_clause_to_sql() to translate
        a clause with a virtual graph pattern.  This primarily substitutes the
        appropriate virtual graph tables to use.
        """
        node1 = clause[0]
        rel = clause[1]
        if rel.labels is None:
            return

        # load here so we get the uniquified name registered with the connection:
        self.load()
        old_graph = node1._graph_table
        old_graph_alias = node1._graph_alias
        new_graph = self.get_name()
        # create a new alias (which is fine given we have a unique table name),
        # this will transparently handle qualified graph table names:
        new_graph_alias = state.get_table_aliases(new_graph, new_graph + '_c')[0]
        node1._graph_table = new_graph
        node1._graph_alias = new_graph_alias
        # TO DO: support this in query.py:
        #state.unregister_table_alias(old_graph, old_graph_alias)
        state.register_table_alias(new_graph, new_graph_alias)
        # prevent the generation of a label restriction based on the virtual graph name:
        rel.labels = None
        # now finish translation with standard translator:
        query.pattern_clause_to_sql(clause, new_graph_alias, state)


"""
# minimal test that uses the dummy definition provided in VirtualTableFunction:
>>> import kgtk.kypher.sqlstore as ss
>>> import kgtk.kypher.functions as fns
>>> sql_store = ss.SqliteStore('/tmp/test.sqlite3.db', loglevel=1)
>>> class TestFun(fns.VirtualTableFunction):
...     pass
... 
>>> TestFun('vtestfun').define()
>>> testfun = fns.SqlFunction.get_function('vtestfun', sql_store)
>>> testfun.load()
>>> testfun.get_name()
'vtestfun_0'
>>> list(sql_store.execute('select * from vtestfun_0(42)'))
[(42, 'defarg2')]
"""

class VirtualGraphFunction(VirtualTableFunction):
    """Functions that return multiple rows of KGTK graph edges per set of inputs.
    These functions should at a minimum take 'node1' as their input and produce
    """



# Top-level definition API:

declare = SqlFunction.declare

def sqlfun(func=None, klass=SqlFunction, name=None, num_params=None, deterministic=False):
    def sqlfun_decorator(func):
        klass(name, code=func, num_params=num_params, deterministic=deterministic).define()
        return func
    if func is None:
        # we are called directly as a function:
        return sqlfun_decorator
    else:
        # we are called as a decorator:
        return sqlfun_decorator(func)

"""
# Examples:

@sqlfun(num_params=1, deterministic=True)
def plus1(x):
    return x + 1

@sqlfun(klass=MathFunction, num_params=1, deterministic=True)
def math_sqrt(x):
    return math.sqrt(x)

CosineSimilarity('kvec_cos_sim', num_params=2, deterministic=True).define()
"""


# Forward-declarations:

declare('kgtk.kypher.funccore',
        'kgtk_regex', 'kgtk_null_to_empty', 'kgtk_empty_to_null', 'pyeval', 'pycall',
        'avg', 'count', 'group_concat', 'max', 'min', 'sum', 'total',
        'cast', 'likelihood', 'concat', 'rowid',
        'kgtk_values',
        'kgtk_is_subnode',)

declare('kgtk.kypher.funclit',
        'kgtk_string', 'kgtk_stringify', 'kgtk_unstringify',
        'kgtk_lqstring', 'kgtk_lqstring_text', 'kgtk_lqstring_text_string', 'kgtk_lqstring_lang',
        'kgtk_lqstring_lang_suffix', 'kgtk_lqstring_suffix',
        'kgtk_date', 'kgtk_date_date', 'kgtk_date_time', 'kgtk_date_and_time', 'kgtk_date_year', 'kgtk_date_month', 'kgtk_date_day',
        'kgtk_date_hour', 'kgtk_date_minutes', 'kgtk_date_seconds', 'kgtk_date_zone', 'kgtk_date_zone_string', 'kgtk_date_precision',
        'kgtk_number', 'kgtk_quantity', 'kgtk_quantity_numeral', 'kgtk_quantity_numeral_string', 'kgtk_quantity_number',
        'kgtk_quantity_number_int', 'kgtk_quantity_number_float', 'kgtk_quantity_si_units', 'kgtk_quantity_wd_units',
        'kgtk_quantity_tolerance', 'kgtk_quantity_tolerance_string', 'kgtk_quantity_low_tolerance', 'kgtk_quantity_high_tolerance',
        'kgtk_geo_coords', 'kgtk_geo_coords_lat', 'kgtk_geo_coords_long',
        'kgtk_literal', 'kgtk_symbol', 'kgtk_type',)

declare('kgtk.kypher.funcmath',
        'acos', 'acosh', 'asin', 'asinh', 'atan', 'atan2', 'atanh', 'ceil', 'ceiling', 'cos', 'cosh', 'degrees',
        'exp', 'floor', 'ln', 'log', 'log10', 'log2', 'logb', 'mod', 'pi', 'pow', 'power', 'radians',
        'sin', 'sinh', 'sqrt', 'tan', 'tanh', 'trunc',)

declare('kgtk.kypher.funcvec',
        '_kvec_get_vector', 'kvec_dot', 'kvec_dot_product', 'kvec_cos_sim', 'kvec_cosine_similarity',
        'kvec_topk_cosine_similarity', 'kvec_topk_cos_sim',
        'kvec_euclidian_distance', 'kvec_euclid_dist', 'kvec_l2_norm',
        'kvec_sim_join_controller', 'kvec_sim_join_ctrl',)
