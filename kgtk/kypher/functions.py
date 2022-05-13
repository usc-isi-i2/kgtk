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
    def is_defined(name):
        """Return True if a function with 'name' is already defined or forward-declared.
        """
        name = SqlFunction.normalize_name(name)
        return SqlFunction._definitions.get(name) is not None

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
            # we have a forward-declaration to a defining module, import it:
            exec(f'import {fun}')
            fun = SqlFunction._definitions.get(SqlFunction.normalize_name(name))
            if not isinstance(fun, SqlFunction):
                # this is a real error, since somebody declared a function that
                # is missing, so we are not considering the 'error' switch here:
                raise KGTKException(f'missing definition for SQL function: {name}')
        # create a copy of the definition with some additional values filled in:
        fun = copy.copy(fun)
        fun.store = store
        for key, value in kwargs.items():
            setattr(fun, key, value)
        return fun

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
        try:
            self.store.get_conn().create_function(self.get_name(), self.get_num_params(), code, deterministic=determ)
        except sqlite3.NotSupportedError:
            # older SQLite, try without 'deterministic':
            self.store.get_conn().create_function(self.get_name(), self.get_num_params(), code)
        # link to old API for now:
        self.store.user_functions.add(self.get_name())

    def uniquify_name(self):
        """Generate a unique name for this function based on its current name.
        """
        self.name = f'{self.get_name()}_{len(self.store.user_functions)}'

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

"""
# soon:
declare('kgtk.kypher.funcbase',
        'kgtk_regex', 'kgtk_null_to_empty', 'kgtk_empty_to_null', 'pyeval', 'pycall',
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
"""

declare('kgtk.kypher.funcvec',
        '_kvec_get_vector', 'kvec_dot', 'kvec_dot_product', 'kvec_cos_sim', 'kvec_cosine_similarity')
