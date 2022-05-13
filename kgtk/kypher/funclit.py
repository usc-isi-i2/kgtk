"""
KGTK literal SQL functions
"""

import re

# this is expensive to import (120ms):
from   kgtk.value.kgtkvalue import KgtkValue
from   kgtk.exceptions import KGTKException
from   kgtk.kypher.functions import SqlFunction, sqlfun


### Literal functions:

# Strings:

@sqlfun(num_params=1, deterministic=True)
def kgtk_string(x):
    """Return True if 'x' is a KGTK plain string literal."""
    return isinstance(x, str) and x.startswith('"')

@sqlfun(num_params=1, deterministic=True)
def kgtk_stringify(x):
    """If 'x' is not already surrounded by double quotes, add them.
    """
    # TO DO: this also needs to handle escaping of some kind
    if not isinstance(x, str):
        x = str(x)
    if not (x.startswith('"') and x.endswith('"')):
        return '"' + x + '"'
    else:
        return x

@sqlfun(num_params=1, deterministic=True)
def kgtk_unstringify(x):
    """If 'x' is surrounded by double quotes, remove them.
    """
    # TO DO: this also needs to handle unescaping of some kind
    if isinstance(x, str) and x.startswith('"') and x.endswith('"'):
        return x[1:-1]
    else:
        return x


# Language-qualified strings:

@sqlfun(num_params=1, deterministic=True)
def kgtk_lqstring(x):
    """Return True if 'x' is a KGTK language-qualified string literal.
    """
    return isinstance(x, str) and x.startswith("'")

# these all return None upon failure without an explicit return:
@sqlfun(num_params=1, deterministic=True)
def kgtk_lqstring_text(x):
    """Return the text component of a KGTK language-qualified string literal.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_language_qualified_string_re.match(x)
        if m:
            return m.group('text')
        
@sqlfun(num_params=1, deterministic=True)
def kgtk_lqstring_text_string(x):
    """Return the text component of a KGTK language-qualified string literal
    as a KGTK string literal.
    """
    text = kgtk_lqstring_text(x)
    return text and ('"' + text + '"') or None

@sqlfun(num_params=1, deterministic=True)
def kgtk_lqstring_lang(x):
    """Return the language component of a KGTK language-qualified string literal.
    This is the first part not including suffixes such as 'en' in 'en-us'.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_language_qualified_string_re.match(x)
        if m:
            # not a string for easier manipulation - assumes valid lang syntax:
            return m.group('lang')
        
@sqlfun(num_params=1, deterministic=True)
def kgtk_lqstring_lang_suffix(x):
    """Return the language+suffix components of a KGTK language-qualified string literal.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_language_qualified_string_re.match(x)
        if m:
            # not a string for easier manipulation - assumes valid lang syntax:
            return m.group('lang_suffix')
        
@sqlfun(num_params=1, deterministic=True)
def kgtk_lqstring_suffix(x):
    """Return the suffix component of a KGTK language-qualified string literal.
    This is the second part if it exists such as 'us' in 'en-us', empty otherwise.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_language_qualified_string_re.match(x)
        if m:
            # not a string for easier manipulation - assumes valid lang syntax:
            return m.group('suffix')


# Date literals:

@sqlfun(num_params=1, deterministic=True)
def kgtk_date(x):
    """Return True if 'x' is a KGTK date literal.
    """
    return isinstance(x, str) and x.startswith('^')

# these all return None upon failure without an explicit return:
@sqlfun(num_params=1, deterministic=True)
def kgtk_date_date(x):
    """Return the date component of a KGTK date literal as a KGTK date.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_date_and_times_re.match(x)
        if m:
            return '^' + m.group('date')
        
@sqlfun(num_params=1, deterministic=True)
def kgtk_date_time(x):
    """Return the time component of a KGTK date literal as a KGTK date.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_date_and_times_re.match(x)
        if m:
            return '^' + m.group('time')
        
@sqlfun(num_params=1, deterministic=True)
def kgtk_date_and_time(x):
    """Return the date+time components of a KGTK date literal as a KGTK date.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_date_and_times_re.match(x)
        if m:
            return '^' + m.group('date_and_time')
        
@sqlfun(num_params=1, deterministic=True)
def kgtk_date_year(x):
    """Return the year component of a KGTK date literal as an int.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_date_and_times_re.match(x)
        if m:
            return int(m.group('year'))
        
@sqlfun(num_params=1, deterministic=True)
def kgtk_date_month(x):
    """Return the month component of a KGTK date literal as an int.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_date_and_times_re.match(x)
        if m:
            return int(m.group('month'))
        
@sqlfun(num_params=1, deterministic=True)
def kgtk_date_day(x):
    """Return the day component of a KGTK date literal as an int.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_date_and_times_re.match(x)
        if m:
            return int(m.group('day'))
        
@sqlfun(num_params=1, deterministic=True)
def kgtk_date_hour(x):
    """Return the hour component of a KGTK date literal as an int.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_date_and_times_re.match(x)
        if m:
            return int(m.group('hour'))
        
@sqlfun(num_params=1, deterministic=True)
def kgtk_date_minutes(x):
    """Return the minutes component of a KGTK date literal as an int.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_date_and_times_re.match(x)
        if m:
            return int(m.group('minutes'))
        
@sqlfun(num_params=1, deterministic=True)
def kgtk_date_seconds(x):
    """Return the seconds component of a KGTK date literal as an int.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_date_and_times_re.match(x)
        if m:
            return int(m.group('seconds'))
        
@sqlfun(num_params=1, deterministic=True)
def kgtk_date_zone(x):
    """Return the timezone component of a KGTK date literal.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_date_and_times_re.match(x)
        if m:
            return m.group('zone')
        
@sqlfun(num_params=1, deterministic=True)
def kgtk_date_zone_string(x):
    """Return the time zone component (if any) as a KGTK string.  Zones might
    look like +10:30, for example, which would be illegal KGTK numbers.
    """
    zone = kgtk_date_zone(x)
    return zone and ('"' + zone + '"') or None

@sqlfun(num_params=1, deterministic=True)
def kgtk_date_precision(x):
    """Return the precision component of a KGTK date literal as an int.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_date_and_times_re.match(x)
        if m:
            return int(m.group('precision'))


# Number and quantity literals:

SQLITE3_MAX_INTEGER = +2 ** 63 - 1
SQLITE3_MIN_INTEGER = -2 ** 63

def to_sqlite3_int(x):
    """Similar to Python 'int' but map numbers outside the 64-bit range onto their extremes.
    This is identical to what SQLite's 'cast' function does for numbers outside the range.
    """
    x = int(x)
    if x > SQLITE3_MAX_INTEGER:
        return SQLITE3_MAX_INTEGER
    elif x < SQLITE3_MIN_INTEGER:
        return SQLITE3_MIN_INTEGER
    else:
        return x

def to_sqlite3_float(x):
    """Identical to Python 'float', maps 'x' onto an 8-byte IEEE floating point number.
    """
    # TO DO: this might need more work to do the right thing at the boundaries
    #        and with infinity values, see 'sys.float_info'; seems to work
    return float(x)

def to_sqlite3_int_or_float(x):
    """Similar to Python 'int' but map numbers outside the 64-bit range onto floats.
    """
    x = int(x)
    if x > SQLITE3_MAX_INTEGER:
        return float(x)
    elif x < SQLITE3_MIN_INTEGER:
        return float(x)
    else:
        return x

@sqlfun(num_params=1, deterministic=True)
def kgtk_number(x):
    """Return True if 'x' is a dimensionless KGTK number literal.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_number_or_quantity_re.match(x)
        if m:
            return x == m.group('number')
    return False

@sqlfun(num_params=1, deterministic=True)
def kgtk_quantity(x):
    """Return True if 'x' is a dimensioned KGTK quantity literal.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_number_or_quantity_re.match(x)
        if m:
            return x != m.group('number')
    return False

# these all return None upon failure without an explicit return:
@sqlfun(num_params=1, deterministic=True)
def kgtk_quantity_numeral(x):
    """Return the numeral component of a KGTK quantity literal.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_number_or_quantity_re.match(x)
        if m:
            return m.group('number')
        
@sqlfun(num_params=1, deterministic=True)
def kgtk_quantity_numeral_string(x):
    """Return the numeral component of a KGTK quantity literal as a KGTK string.
    """
    num = kgtk_quantity_numeral(x)
    return num and ('"' + num + '"') or None

FLOAT_NUMERAL_REGEX = re.compile(r'.*[.eE]')

@sqlfun(num_params=1, deterministic=True)
def kgtk_quantity_number(x):
    """Return the number value of a KGTK quantity literal as an int or float.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_number_or_quantity_re.match(x)
        if m:
            numeral = m.group('number')
            if FLOAT_NUMERAL_REGEX.match(numeral):
                return to_sqlite3_float(numeral)
            else:
                return to_sqlite3_int_or_float(numeral)
            
@sqlfun(num_params=1, deterministic=True)
def kgtk_quantity_number_int(x):
    """Return the number value of a KGTK quantity literal as an int.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_number_or_quantity_re.match(x)
        if m:
            numeral = m.group('number')
            if FLOAT_NUMERAL_REGEX.match(numeral):
                return to_sqlite3_int(float(numeral))
            else:
                return to_sqlite3_int(numeral)
            
@sqlfun(num_params=1, deterministic=True)
def kgtk_quantity_number_float(x):
    """Return the number value component of a KGTK quantity literal as a float.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_number_or_quantity_re.match(x)
        if m:
            numeral = m.group('number')
            if FLOAT_NUMERAL_REGEX.match(numeral):
                return to_sqlite3_float(numeral)
            else:
                # because the numeral could be in octal or hex:
                return to_sqlite3_float(int(numeral))

@sqlfun(num_params=1, deterministic=True)
def kgtk_quantity_si_units(x):
    """Return the SI-units component of a KGTK quantity literal.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_number_or_quantity_re.match(x)
        if m:
            return m.group('si_units')
        
@sqlfun(num_params=1, deterministic=True)
def kgtk_quantity_wd_units(x):
    """Return the Wikidata unit node component of a KGTK quantity literal.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_number_or_quantity_re.match(x)
        if m:
            return m.group('units_node')

@sqlfun(num_params=1, deterministic=True)
def kgtk_quantity_tolerance(x):
    """Return the full tolerance component of a KGTK quantity literal.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_number_or_quantity_re.match(x)
        if m:
            lowtol = m.group('low_tolerance')
            hightol = m.group('high_tolerance')
            if lowtol and hightol:
                return '[' + lowtol + ',' + hightol + ']'
            
@sqlfun(num_params=1, deterministic=True)
def kgtk_quantity_tolerance_string(x):
    """Return the full tolerance component of a KGTK quantity literal as a KGTK string.
    """
    tol = kgtk_quantity_tolerance(x)
    return tol and ('"' + tol + '"') or None

@sqlfun(num_params=1, deterministic=True)
def kgtk_quantity_low_tolerance(x):
    """Return the low tolerance component of a KGTK quantity literal as a float.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_number_or_quantity_re.match(x)
        if m:
            lowtol = m.group('low_tolerance')
            if lowtol:
                return to_sqlite3_float(lowtol)
            
@sqlfun(num_params=1, deterministic=True)
def kgtk_quantity_high_tolerance(x):
    """Return the high tolerance component of a KGTK quantity literal as a float.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_number_or_quantity_re.match(x)
        if m:
            hightol = m.group('high_tolerance')
            if hightol:
                return to_sqlite3_float(hightol)

# kgtk_quantity_number_float('12[-0.1,+0.1]m')
# kgtk_number('0x24F') ...why does this not work?


# Geo coordinates:

@sqlfun(num_params=1, deterministic=True)
def kgtk_geo_coords(x):
    """Return True if 'x' is a KGTK geo coordinates literal.
    """
    # Assumes valid KGTK values, thus only tests for initial character:
    return isinstance(x, str) and x.startswith('@')

# these all return None upon failure without an explicit return:
@sqlfun(num_params=1, deterministic=True)
def kgtk_geo_coords_lat(x):
    """Return the latitude component of a KGTK geo coordinates literal as a float.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_location_coordinates_re.match(x)
        if m:
            return to_sqlite3_float(m.group('lat'))
        
@sqlfun(num_params=1, deterministic=True)
def kgtk_geo_coords_long(x):
    """Return the longitude component of a KGTK geo coordinates literal as a float.
    """
    if isinstance(x, str):
        m = KgtkValue.lax_location_coordinates_re.match(x)
        if m:
            return to_sqlite3_float(m.group('lon'))


# Literals and symbols:

LITERAL_REGEX = re.compile(r'''^["'^@!0-9.+-]|^True$|^False$''')

@sqlfun(num_params=1, deterministic=True)
def kgtk_literal(x):
    """Return True if 'x' is any KGTK literal.  This assumes valid literals
    and only tests the first character (except for booleans).
    """
    return isinstance(x, str) and LITERAL_REGEX.match(x) is not None


@sqlfun(num_params=1, deterministic=True)
def kgtk_symbol(x):
    """Return True if 'x' is a KGTK symbol.  This assumes valid literals
    and only tests the first character (except for booleans).
    """
    return isinstance(x, str) and LITERAL_REGEX.match(x) is None

VALUE_TYPE_REGEX = re.compile(
    '|'.join([r'(?P<string>^")',
              r"(?P<lq_string>^')",
              r'(?P<date_time>^\^)',
              r'(?P<quantity>^[0-9.+-])',
              r'(?P<geo_coord>^@)',
              r'(?P<boolean>^(True$|False$))',
              r'(?P<typed_literal>^!)',
              r'(?P<symbol>.)',
    ]))

@sqlfun(num_params=1, deterministic=True)
def kgtk_type(x):
    """Return a type description for the KGTK literal or symbol 'x'.  The returned type
    will be one of 'string', 'lq_string', 'date_time', 'quantity', 'geo_coord', 'boolean',
    'typed_literal' or 'symbol'.  This assumes valid literals and only tests the first
    character (except for booleans).
    """
    if isinstance(x, str):
        m = VALUE_TYPE_REGEX.search(x)
        if m:
            return m.lastgroup
