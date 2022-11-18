"""
KGTK math SQL functions
"""

import sys
# sqlite3 already loads math, so no extra cost:
import math
import re
from   functools import lru_cache

from   kgtk.exceptions import KGTKException
from   kgtk.kypher.utils import *
from   kgtk.kypher.functions import SqlFunction, sqlfun


### Math functions:

# Temporary Python implementation of SQLite math built-ins until they become standardly available.
# Should happen once SQLite3 3.35.0 is used by Python - or soon thereafter.  Once we've determined
# the cutoff point we can make the function registration dependent on 'sqlite3.version'.
# User-defined functions override built-ins, which means this should work even after math built-ins
# come online - we hope.

@sqlfun(name='acos', num_params=1, deterministic=True)
def math_acos(x):
    """Implement the SQLite3 math built-in 'acos' via Python.
    """
    try:
        return math.acos(x)
    except:
        pass

@sqlfun(name='acosh', num_params=1, deterministic=True)
def math_acosh(x):
    """Implement the SQLite3 math built-in 'acosh' via Python.
    """
    try:
        return math.acosh(x)
    except:
        pass

@sqlfun(name='asin', num_params=1, deterministic=True)
def math_asin(x):
    """Implement the SQLite3 math built-in 'asin' via Python.
    """
    try:
        return math.asin(x)
    except:
        pass

@sqlfun(name='asinh', num_params=1, deterministic=True)
def math_asinh(x):
    """Implement the SQLite3 math built-in 'asinh' via Python.
    """
    try:
        return math.asinh(x)
    except:
        pass

@sqlfun(name='atan', num_params=1, deterministic=True)
def math_atan(x):
    """Implement the SQLite3 math built-in 'atan' via Python.
    """
    try:
        return math.atan(x)
    except:
        pass

@sqlfun(name='atan2', num_params=2, deterministic=True)
def math_atan2(x, y):
    """Implement the SQLite3 math built-in 'atan2' via Python.
    """
    try:
        return math.atan2(y, x) # flips args
    except:
        pass

@sqlfun(name='atanh', num_params=1, deterministic=True)
def math_atanh(x):
    """Implement the SQLite3 math built-in 'atanh' via Python.
    """
    try:
        return math.atanh(x)
    except:
        pass

@sqlfun(name='ceil', num_params=1, deterministic=True)
def math_ceil(x):
    """Implement the SQLite3 math built-in 'ceil' via Python.
    """
    try:
        return math.ceil(x)
    except:
        pass

# alias: ceiling(X)
SqlFunction(name='ceiling', code=math_ceil, num_params=1, deterministic=True).define()
    
@sqlfun(name='cos', num_params=1, deterministic=True)
def math_cos(x):
    """Implement the SQLite3 math built-in 'cos' via Python.
    """
    try:
        return math.cos(x)
    except:
        pass

@sqlfun(name='cosh', num_params=1, deterministic=True)
def math_cosh(x):
    """Implement the SQLite3 math built-in 'cosh' via Python.
    """
    try:
        return math.cosh(x)
    except:
        pass

@sqlfun(name='degrees', num_params=1, deterministic=True)
def math_degrees(x):
    """Implement the SQLite3 math built-in 'degrees' via Python.
    Convert value X from radians into degrees. 
    """
    try:
        return math.degrees(x)
    except:
        pass

@sqlfun(name='exp', num_params=1, deterministic=True)
def math_exp(x):
    """Implement the SQLite3 math built-in 'exp' via Python.
    """
    try:
        return math.exp(x)
    except:
        pass

@sqlfun(name='floor', num_params=1, deterministic=True)
def math_floor(x):
    """Implement the SQLite3 math built-in 'floor' via Python.
    """
    try:
        return math.floor(x)
    except:
        pass

# NOTE: naming and invocation of logarithm functions is different from
# standard SQL or Python math for that matter (more like Postgres).

@sqlfun(name='ln', num_params=1, deterministic=True)
def math_ln(x):
    """Implement the SQLite3 math built-in 'ln' via Python.
    """
    try:
        return math.log(x)
    except:
        pass

@sqlfun(name='log10', num_params=1, deterministic=True)
def math_log10(x):
    """Implement the SQLite3 math built-in 'log10' via Python.
    """
    try:
        return math.log10(x)
    except:
        pass

# alias: log(X)
SqlFunction(name='log', code=math_log10, num_params=1, deterministic=True).define()

# this one needs to stay if we conditionalize on availability of real math built-ins:
@sqlfun(name='logb', num_params=2, deterministic=True)
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

@sqlfun(name='log2', num_params=1, deterministic=True)
def math_log2(x):
    """Implement the SQLite3 math built-in 'log2' via Python.
    """
    try:
        return math.log2(x)
    except:
        pass

@sqlfun(name='mod', num_params=2, deterministic=True)
def math_mod(x, y):
    """Implement the SQLite3 math built-in 'mod' via Python.
    """
    try:
        return math.fmod(x, y) # preferred over 'x % y' for floats
    except:
        pass

@sqlfun(name='pi', num_params=0, deterministic=True)
def math_pi():
    """Implement the SQLite3 math built-in 'pi' via Python.
    """
    return math.pi

@sqlfun(name='pow', num_params=2, deterministic=True)
def math_pow(x, y):
    """Implement the SQLite3 math built-in 'pow' via Python.
    """
    try:
        return math.pow(x, y)
    except:
        pass

# alias: power(X,Y)
SqlFunction(name='power', code=math_pow, num_params=2, deterministic=True).define()

@sqlfun(name='radians', num_params=1, deterministic=True)
def math_radians(x):
    """Implement the SQLite3 math built-in 'radians' via Python.
    """
    try:
        return math.radians(x)
    except:
        pass

@sqlfun(name='sin', num_params=1, deterministic=True)
def math_sin(x):
    """Implement the SQLite3 math built-in 'sin' via Python.
    """
    try:
        return math.sin(x)
    except:
        pass

@sqlfun(name='sinh', num_params=1, deterministic=True)
def math_sinh(x):
    """Implement the SQLite3 math built-in 'sinh' via Python.
    """
    try:
        return math.sinh(x)
    except:
        pass

@sqlfun(name='sqrt', num_params=1, deterministic=True)
def math_sqrt(x):
    """Implement the SQLite3 math built-in 'sqrt' via Python.
    """
    try:
        return math.sqrt(x)
    except:
        pass

@sqlfun(name='tan', num_params=1, deterministic=True)
def math_tan(x):
    """Implement the SQLite3 math built-in 'tan' via Python.
    """
    try:
        return math.tan(x)
    except:
        pass

@sqlfun(name='tanh', num_params=1, deterministic=True)
def math_tanh(x):
    """Implement the SQLite3 math built-in 'tanh' via Python.
    """
    try:
        return math.tanh(x)
    except:
        pass

@sqlfun(name='trunc', num_params=1, deterministic=True)
def math_trunc(x):
    """Implement the SQLite3 math built-in 'trunc' via Python.
    """
    try:
        return math.trunc(x)
    except:
        pass
