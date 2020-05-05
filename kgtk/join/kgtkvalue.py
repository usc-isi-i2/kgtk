"""
Validate KGTK File data types.
"""

from argparse import ArgumentParser, Namespace
import attr
import re
import sys
import typing

from kgtk.join.kgtkformat import KgtkFormat
from kgtk.join.kgtkvalueoptions import KgtkValueOptions, DEFAULT_KGTK_VALUE_OPTIONS
from kgtk.join.languagevalidator import LanguageValidator

@attr.s(slots=True, frozen=False)
class KgtkValue(KgtkFormat):
    value: str = attr.ib(validator=attr.validators.instance_of(str))
    options: KgtkValueOptions = attr.ib(validator=attr.validators.instance_of(KgtkValueOptions), default=DEFAULT_KGTK_VALUE_OPTIONS)

    data_type: typing.Optional[KgtkFormat.DataType] = None
    valid: typing.Optional[bool] = None

    # If this is a list, prepare a KgtkValue object for each item of the list.
    list_items: typing.Optional[typing.List['KgtkValue']] = None

    def get_data_type(self)->KgtkFormat.DataType:

        if self.data_type is not None:
            pass

        elif self.is_empty() or self.is_list():
            pass

        elif self.is_string() or self.is_language_qualified_string():
            pass

        elif self.is_number_or_quantity():
            # To determine whether this is a number or a quantity, we have
            # to validate one of them.
            if not self.is_valid_number():
                # If it isn't a valid number, assume it's a quantity.
                self.data_type = KgtkFormat.DataType.QUANTITY

        elif self.is_location_coordinates():
            pass

        elif self.is_date_and_times():
            pass

        elif self.is_extension():
            pass

        elif self.is_boolean() or self.is_symbol():
            pass

        if self.data_type is not None:
            return self.data_type

        # Shouldn't get here.
        raise ValueError("Unknown data type for '%s'" % self.value)

    def is_valid(self)->bool:
        dt: KgtkFormat.DataType = self.get_data_type()
        if dt == KgtkFormat.DataType.EMPTY:
            return self.is_valid_empty()
        elif dt == KgtkFormat.DataType.LIST:
            return self.is_valid_list()
        elif dt == KgtkFormat.DataType.NUMBER:
            return self.is_valid_number()
        elif dt == KgtkFormat.DataType.QUANTITY:
            return self.is_valid_quantity()
        elif dt == KgtkFormat.DataType.STRING:
            return self.is_valid_string()
        elif dt == KgtkFormat.DataType.LANGUAGE_QUALIFIED_STRING:
            return self.is_valid_language_qualified_string()
        elif dt == KgtkFormat.DataType.LOCATION_COORDINATES:
            return self.is_valid_location_coordinates()
        elif dt == KgtkFormat.DataType.DATE_AND_TIMES:
            return self.is_valid_date_and_times()
        elif dt == KgtkFormat.DataType.EXTENSION:
            return self.is_valid_extension()
        elif dt == KgtkFormat.DataType.BOOLEAN:
            return self.is_valid_boolean()
        elif dt == KgtkFormat.DataType.SYMBOL:
            return self.is_valid_symbol()
        else:
            raise ValueError("Unrecognized DataType.")

        
    def is_empty(self)->bool:
        if self.data_type is not None:
            return self.data_type == KgtkFormat.DataType.EMPTY

        if len(self.value) != 0:
            return False

        # We are certain that this is an empty value.  We can be certain it is valid.
        self.data_type = KgtkFormat.DataType.EMPTY
        self.valid = True
        return True

    def is_valid_empty(self)->bool:
        # If it is empty, it is validly so.
        return self.is_empty()

    split_list_re: typing.Pattern = re.compile(r"(?<!\\)" + "\\" + KgtkFormat.LIST_SEPARATOR)

    def get_list(self)->typing.List['KgtkValue']:
        if self.list_items is not None:
            return self.list_items

        self.list_items: typing.List['KgtkValue'] = [ ]
        value: str
        for value in KgtkValue.split_list_re.split(self.value):
            self.list_items.append(KgtkValue(value, options=self.options))
        return self.list_items

    def is_list(self)->bool:
        if self.data_type is not None:
            return self.data_type == KgtkFormat.DataType.LIST

        if len(self.get_list()) == 1:
            return False

        # We aare certain that this is a list, although we haven't checked validity.
        self.data_type = KgtkFormat.DataType.LIST
        return True


    def is_valid_list(self)->bool:
        if not self.is_list():
            return False

        if self.valid is not None:
            return self.valid
            
        item: 'KgtkValue'
        for item in self.get_list():
            if not item.is_valid():
                # The list is invalid if any item in the list is invalid.
                self.valid = False
                return False

        # This is a valid list.
        self.valid = True
        return True

    def _is_number_or_quantity(self)->bool:
        return self.value.startswith(("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+", "-", "."))

    def is_number_or_quantity(self)->bool:
        """
        Otherwise, return True if the first character is 0-9,+,-,. .
        """
        if self.data_type is not None:
            return self.data_type == KgtkFormat.DataType.NUMBER or self.data_type == KgtkFormat.DataType.QUANTITY

        return self._is_number_or_quantity()
    
    # The following lexical analysis is based on:
    # https://docs.python.org/3/reference/lexical_analysis.html

    # The long integer suffix was part of Python 2.  It was dropped in Python 3.
    long_suffix_pat: str = r'[lL]'

    plus_or_minus_pat: str = r'[-+]'

    # Integer literals.
    #
    # Decimal integers, allowing leading zeros.
    digit_pat: str = r'[0-9]'
    decinteger_pat: str = r'(?:{digit}(?:_?{digit})*{long_suffix}?)'.format(digit=digit_pat,
                                                                            long_suffix=long_suffix_pat)
    bindigit_pat: str = r'[01]'
    bininteger_pat: str = r'(?:0[bB](":_?{bindigit})+{long_suffix})'.format(bindigit=bindigit_pat,
                                                                            long_suffix=long_suffix_pat)
    octdigit_pat: str = r'[0-7]'
    octinteger_pat: str = r'(?:0[oO](":_?{octdigit})+{long_suffix})'.format(octdigit=octdigit_pat,
                                                                            long_suffix=long_suffix_pat)
    hexdigit_pat: str = r'[0-7a-fA-F]'
    hexinteger_pat: str = r'(?:0[xX](":_?{hexdigit})+{long_suffix})'.format(hexdigit=hexdigit_pat,
                                                                            long_suffix=long_suffix_pat)
     
    integer_pat: str = r'(?:{decinteger}|{bininteger}|{octinteger}|{hexinteger})'.format(decinteger=decinteger_pat,
                                                                                        bininteger=bininteger_pat,
                                                                                        octinteger=octinteger_pat,
                                                                                        hexinteger=hexinteger_pat)

    # Floating point literals.
    digitpart_pat: str = r'(?:{digit}(?:_?{digit})*)'.format(digit=digit_pat)
    fraction_pat: str = r'(?:\.{digitpart})'.format(digitpart=digitpart_pat)
    pointfloat_pat: str = r'(?:{digitpart}?{fraction})|(?:{digitpart}\.)'.format(digitpart=digitpart_pat,
                                                                                 fraction=fraction_pat)
    exponent_pat: str = r'(?:[eE]{plus_or_minus}?{digitpart})'.format(plus_or_minus=plus_or_minus_pat,
                                                                      digitpart=digitpart_pat)
    exponentfloat_pat: str = r'(?:{digitpart}|{pointfloat}){exponent}'.format(digitpart=digitpart_pat,
                                                                              pointfloat=pointfloat_pat,
                                                                              exponent=exponent_pat)
    floatnumber_pat: str = r'(?:{pointfloat}|{exponentfloat})'.format(pointfloat=pointfloat_pat,
                                                                      exponentfloat=exponentfloat_pat)

    # Imaginary literals.
    imagnumber_pat: str = r'(?:{floatnumber}|{digitpart})[jJ]'.format(floatnumber=floatnumber_pat,
                                                                      digitpart=digitpart_pat)

    # Numeric literals.
    numeric_pat: str = r'(?:{plus_or_minus}?(?:{integer}|{floatnumber}|{imagnumber}))'.format(plus_or_minus=plus_or_minus_pat,
                                                                                              integer=integer_pat,
                                                                                              floatnumber=floatnumber_pat,
                                                                                              imagnumber=imagnumber_pat)

    # Tolerances
    tolerance_pat: str = r'(?:\[{numeric},{numeric}\])'.format(numeric=numeric_pat)

    # SI units taken from:
    # http://www.csun.edu/~vceed002/ref/measurement/units/units.pdf
    #
    # Note: if Q were in this list, it would conflict with Wikidata nodes (below).
    si_unit_pat: str = r'(?:m|kg|s|C|K|mol|cd|F|M|A|N|ohms|V|J|Hz|lx|H|Wb|V|W|Pa)'
    si_power_pat: str = r'(?:-1|2|3)' # Might need more.
    si_combiner_pat: str = r'[./]'
    si_pat: str = r'(?:{si_unit}{si_power}?(?:{si_combiner}{si_unit}{si_power}?)*)'.format(si_unit=si_unit_pat,
                                                                                           si_combiner=si_combiner_pat,
                                                                                           si_power=si_power_pat)
    # Wikidata nodes (for units):
    nonzero_digit_pat: str = r'[1-9]'
    wikidata_node_pat: str = r'(?:Q{nonzero_digit}{digit}*)'.format(nonzero_digit=nonzero_digit_pat,
                                                                    digit=digit_pat)

    units_pat: str = r'(?:{si}|{wikidata_node})'.format(si=si_pat,
                                                        wikidata_node=wikidata_node_pat)
    

    # This definition matches numbers or quantities.
    number_or_quantity_pat: str = r'{numeric}{tolerance}?{units}?'.format(numeric=numeric_pat,
                                                                          tolerance=tolerance_pat,
                                                                          units=units_pat)
    # This definition for quantity excludes plain numbers.
    quantity_pat: str = r'{numeric}(?:(?:{tolerance}{units}?)|{units})'.format(numeric=numeric_pat,
                                                                               tolerance=tolerance_pat,
                                                                               units=units_pat)
    # This matches numbers or quantities.
    number_or_quantity_re: typing.Pattern = re.compile(r'^' + number_or_quantity_pat + r'$')

    # This matches numbers but not quantities.
    number_re: typing.Pattern = re.compile(r'^' + numeric_pat + r'$')

    # This matches quantities excluding numbers.
    quantity_re: typing.Pattern = re.compile(r'^' + quantity_pat + r'$')

    def is_valid_number_or_quantity(self)->bool:
        """
        Return True if the first character is 0-9,_,-,.
        and it is either a Python-compatible number or an enhanced
        quantity.
        """
        # If we know the specific data type, delegate the test to that data type.
        if self.data_type is not None:
            if self.data_type == KgtkFormat.DataType.NUMBER:
                return self.is_valid_number()
            elif self.data_type == KgtkFormat.DataType.QUANTITY:
                return self.is_valid_quantity()
            else:
                return False # Not a number or quantity.

        if not self._is_number_or_quantity():
            return False

        # We cannot cache the result of this test because it would interfere
        # if we later determined the exact data type.  We could work around
        # this problem with more thought.
        m: typing.Optional[typing.Match] = KgtkValue.number_or_quantity_re.match(self.value)
        return m is not None
        
    
    def is_valid_number(self)->bool:
        """
        Otherwise, return True if the first character is 0-9,_,-,.
        and it is a Python-compatible number (with optional limited enhancements).

        Examples:
        1
        123
        -123
        +123
        0b101
        0o277
        0x24F
        .4
        0.4
        10.
        10.4
        10.4e10
        """
        if self.data_type is not None:
            if self.data_type != KgtkFormat.DataType.NUMBER:
                return False
            if self.valid is not None:
                return self.valid
        
        if not self._is_number_or_quantity():
            return False
        # We don't know yet if this is a number.  It could be a quantity.

        m: typing.Optional[typing.Match] = KgtkValue.number_re.match(self.value)
        if m is None:
            return False

        # Now we can be certain that this is a number.
        self.data_type = KgtkFormat.DataType.NUMBER
        self.valid = True
        return True
        
    
    def is_valid_quantity(self)->bool:
        """
        Return True if the first character is 0-9,_,-,.
        and it is an enhanced quantity.
        """
        if self.data_type is not None:
            if self.data_type != KgtkFormat.DataType.QUANTITY:
                return False
            if self.valid is not None:
                return self.valid
        
        if not self._is_number_or_quantity():
            return False
        # We don't know yet if this is a quantity.  It could be a number.

        m: typing.Optional[typing.Match] = KgtkValue.quantity_re.match(self.value)
        if m is None:
            return False

        # Now we can be certain that this is a quantity.
        self.data_type = KgtkFormat.DataType.QUANTITY
        self.valid = True
        return True
    
    def is_string(self)->bool:
        """
        Return True if the first character  is '"'.

        Strings begin and end with double quote (").  Any internal double
        quotes must be escaped with backslash (\").  Triple-double quoted
        strings are not supported by KGTK File Vormat v2.

        """
        if self.data_type is not None:
            return self.data_type == KgtkFormat.DataType.STRING
        
        if not self.value.startswith('"'):
            return False

        # We are certain this is a string.  We don't yet know if it is valid.
        self.data_type = KgtkFormat.DataType.STRING
        return True

    lax_string_re: typing.Pattern = re.compile(r'^".*"$')
    strict_string_re: typing.Pattern = re.compile(r'^"(?:[^"\\]|\\.)*"$')

    def is_valid_string(self)->bool:
        """
        Strict: return True if the first character  is '"',
        the last character is '"', and any internal '"' characters are
        escaped by backslashes.
        """
        if not self.is_string():
            return False

        if self.valid is not None:
            return self.valid

        m: typing.Optional[typing.Match]
        if self.options.allow_lax_strings:
            m = KgtkValue.lax_string_re.match(self.value)
        else:
            m = KgtkValue.strict_string_re.match(self.value)
        if m is None:
            return False

        # We are certain that this is a valid string.
        self.valid = True
        return True

    def is_structured_literal(self)->bool:
        """
        Return True if the first character  is ^@'!.
        """
        return self.value.startswith(("^", "@", "'", "!"))

    def is_symbol(self)->bool:
        """
        Return True if not a number, string, nor structured literal.
        """
        if self.data_type is not None:
            return self.data_type == KgtkFormat.DataType.SYMBOL

        if self.is_number_or_quantity() or self.is_string() or self.is_structured_literal() or self.is_boolean():
            return False
            
        # We are certain this is a symbol.  We assume, for now that it is valid.
        self.data_type = KgtkFormat.DataType.SYMBOL
        self.valid = True
        return True

    def is_valid_symbol(self)->bool:
        # If it is a suymbol, then it is valid.
        return self.is_symbol()
    
    def is_boolean(self)->bool:
        """
        return True if the value matches one of the special boolean symbols..
        """
        if self.data_type is not None:
            return self.data_type == KgtkFormat.DataType.BOOLEAN

        if self.value != KgtkFormat.TRUE_SYMBOL and self.value != KgtkFormat.FALSE_SYMBOL:
            return False
            
        # We are certain this is a valid boolean.
        self.data_type = KgtkFormat.DataType.BOOLEAN
        self.valid = True
        return True

    def is_valid_boolean(self)->bool:
        # If it is a boolean, then it is valid.
        return self.is_boolean()
    
    def is_language_qualified_string(self)->bool:
        """
        Return True if the first character is '
        """
        if self.data_type is not None:
            return self.data_type == KgtkFormat.DataType.LANGUAGE_QUALIFIED_STRING

        if not self.value.startswith("'"):
            return False

        self.data_type = KgtkFormat.DataType.LANGUAGE_QUALIFIED_STRING
        return True

    # Support two or three character language codes.  Suports hyphenated codes
    # with country codes or dialect names after a language code.
    lax_language_qualified_string_re: typing.Pattern = re.compile(r"^(?P<string>'.*')@(?P<lang>[a-zA-Z]{2,3}(?:-[a-zA-Z]+)?)$")
    strict_language_qualified_string_re: typing.Pattern = re.compile(r"^(?P<string>'(?:[^'\\]|\\.)*')@(?P<lang>[a-zA-Z]{2,3}(?:-[a-zA-Z]+)?)$")

    def is_valid_language_qualified_string(self)->bool:
        """
        Return True if the value looks like a language-qualified string.
        """
        if not self.is_language_qualified_string():
            return False

        # print("checking %s" % self.value)
        m: typing.Optional[typing.Match]
        if self.options.allow_lax_lq_strings:
            m = KgtkValue.lax_language_qualified_string_re.match(self.value)
        else:
            m = KgtkValue.strict_language_qualified_string_re.match(self.value)
        if m is None:
            # print("match failed for %s" % self.value)
            return False

        # Validate the language code:
        lang: str = m.group("lang").lower()
        # print("lang: %s" % lang)

        if not LanguageValidator.validate(lang, options=self.options):
            # print("language validation failed for %s" % self.value)
            return False

        # We are certain that this is a valid language qualified string.
        self.valid = True
        return True

    def is_location_coordinates(self)->bool:
        """
        Return True if the first character is @
        """
        if self.data_type is not None:
            return self.data_type == KgtkFormat.DataType.LOCATION_COORDINATES

        if not self.value.startswith("@"):
            return False

        self.data_type = KgtkFormat.DataType.LOCATION_COORDINATES
        return True

    #location_coordinates_re: typing.Pattern = re.compile(r"^@(?P<lat>[-+]?\d{3}\.\d{5})/(?P<lon>[-+]?\d{3}\.\d{5})$")
    degrees_pat: str = r'(?:[-+]?(?:\d+(?:\.\d*)?)|(?:\.\d+))'
    location_coordinates_re: typing.Pattern = re.compile(r'^@(?P<lat>{degrees})/(?P<lon>{degrees})$'.format(degrees=degrees_pat))

    def is_valid_location_coordinates(self)->bool:
        """
        Return False if this value is a list and idx is None.
        Otherwise, return True if the value looks like valid location coordinates.

        @043.26193/010.92708
        """
        if not self.is_location_coordinates():
            return False

        m: typing.Optional[typing.Match] = KgtkValue.location_coordinates_re.match(self.value)
        if m is None:
            return False

        # Latitude normally runs from -90 to +90:
        latstr: str = m.group("lat")
        try:
            lat: float = float(latstr)
            if  lat < self.options.minimum_valid_lat or lat > self.options.maximum_valid_lat:
                return False
        except ValueError:
            return False

        # Longitude normally runs from -180 to +180:
        lonstr: str = m.group("lon")
        try:
            lon: float = float(lonstr)
            if lon < self.options.minimum_valid_lon or lon > self.options.maximum_valid_lon:
                return False
        except ValueError:
            return False

        # We are certain that this is valid.
        self.valid = True
        return True

    def is_date_and_times(self)->bool:
        """
        Return True if the first character is ^
        """
        if self.data_type is not None:
            return self.data_type == KgtkFormat.DataType.DATE_AND_TIMES

        if not self.value.startswith("^"):
            return False

        # This is a date and times value.  We do not yet know if it si valid.
        self.data_type = KgtkFormat.DataType.DATE_AND_TIMES
        return True

    # https://en.wikipedia.org/wiki/ISO_8601
    #
    # The "lax" patterns allow month 00 and day 00, which are excluded by ISO 8601.
    # We will allow those values when requested in the code below.
    #
    # The first possible hyphen position determines whether we will parse in
    # value as a "basic" (no hyphen) or "extended" format date/time.  A
    # mixture is not permitted: either all hyphens (colons in the time
    # section) must be present, or none.
    #
    # Year-month-day
    year_pat: str = r'(?P<year>[-+]?[0-9]{4})'
    lax_month_pat: str = r'(?P<month>1[0-2]|0[0-9])'
    lax_day_pat: str = r'(?P<day>3[01]|0[0-9]|[12][0-9])'
    lax_date_pat: str = r'(?:{year}(?:(?P<hyphen>-)?{month}?(?:(?(hyphen)-){day})?)?)'.format(year=year_pat,
                                                                                              month=lax_month_pat,
                                                                                              day=lax_day_pat)
    # hour-minutes-seconds
    hour_pat: str = r'(?P<hour>2[0-3]|[01][0-9])'
    minutes_pat: str = r'(?P<minutes>[0-5][0-9])'
    seconds_pat: str = r'(?P<second>[0-5][0-9])'

    # NOTE: It might be the case that the ":" before the minutes in the time zone pattern
    # should be conditioned upon the hyphen indicator.  The Wikipedia article doesn't
    # mention this requirement.
    #
    # NOTE: This pattern accepts a wider range of offsets than actually occur.
    #
    # TODO: consult the actual standard about the colon.
    zone_pat: str = r'(?P<zone>Z|[-+][01][0-9](?::?[0-5][0-9])?)'

    time_pat: str = r'(?:{hour}(?:(?(hyphen):){minutes}(?:(?(hyphen):){seconds})?)?{zone}?)'.format(hour=hour_pat,
                                                                                                   minutes=minutes_pat,
                                                                                                   seconds=seconds_pat,
                                                                                                   zone=zone_pat)

    precision_pat: str = r'(?P<precision>[0-1]?[0-9])'

    lax_date_and_times_pat: str = r'(?:\^{date}(?:T{time})?(?:/{precision})?)'.format(date=lax_date_pat,
                                                                                      time=time_pat,
                                                                                      precision=precision_pat)
    lax_date_and_times_re: typing.Pattern = re.compile(r'^{date_and_times}$'.format(date_and_times=lax_date_and_times_pat))
                                                                        
    def is_valid_date_and_times(self)->bool:
        """
        Return True if the value looks like valid date and times
        literal based on ISO-8601.

        Valid date formats:
        YYYY
        YYYY-MM
        YYYYMMDD
        YYYY-MM-DD

        Valid date and time formats
        YYYYMMDDTHH
        YYYY-MM-DDTHH
        YYMMDDTHHMM
        YYYY-MM-DDTHH:MM
        YYMMDDTHHMMSS
        YYYY-MM-DDTHH:MM:SS

        Optional Time Zone suffix for date and time:
        Z
        +HH
        -HH
        +HHMM
        -HHMM
        +HH:MM
        -HH:MM

        NOTE: This code also accepts the following, which are disallowed by the standard:
        YYYYT...
        YYYYMM
        YYYYMMT...
        YYYY-MMT...

        Note:  IS0-8601 disallows 0 for month or day, e.g.:
        Invalid                   Correct
        1960-00-00T00:00:00Z/9    1960-01-01T00:00:00Z/9

        TODO: Support fractional time elements

        TODO: Support week dates.

        TODO: Support ordinal dates

        TODO: Support Unicode minus sign as well as ASCII minus sign.

        TODO: validate the calendar date, eg fail if 31-Apr-2020.
        """
        if not self.is_date_and_times():
            return False

        m: typing.Optional[typing.Match] = KgtkValue.lax_date_and_times_re.match(self.value)
        if m is None:
            return False

        # Validate the year:
        year_str: str = m.group("year")
        if year_str is None or len(year_str) == 0:
            return False # Years are mandatory
        try:
            year: int = int(year_str)
        except ValueError:
            return False
        if year < self.options.minimum_valid_year:
            return False
        if year > self.options.maximum_valid_year:
            return False

        month_str: str = m.group("month")
        if month_str is not None:
            try:
                month: int = int(month_str)
            except ValueError:
                return False # shouldn't happen
            if month == 0 and not self.options.allow_month_or_day_zero:
                return False # month 0 was disallowed.

        day_str: str = m.group("day")
        if day_str is not None:
            try:
                day: int = int(day_str)
            except ValueError:
                return False # shouldn't happen
            if day == 0 and not self.options.allow_month_or_day_zero:
                return False # day 0 was disallowed.

        # We are fairly certain that this is a valid date and times.
        self.valid = True
        return True

    def is_extension(self)->bool:
        """
        Return True if the first character is !
        """
        if self.data_type is not None:
            return self.data_type == KgtkFormat.DataType.EXTENSION

        if not self.value.startswith("!"):
            return False

        # This is an extension, but for now, assume that all extensions are invalid.
        self.data_type = KgtkFormat.DataType.EXTENSION
        self.valid = False
        return True

    def is_valid_extension(self)->bool:
        # For now, all extensions are invalid.
        return False

    def describe(self)->str:
        """
        Return a string that describes the value.
        """
        if self.is_list():
            result: str
            if self.is_valid_list:
                result = "List ("
            else:
                result = "Invalid List ("
            kv: KgtkValue
            first: bool = True
            for kv in self.get_list():
                if first:
                    first = not first
                else:
                    result += KgtkFormat.LIST_SEPARATOR
                result += kv.describe()
            return result + ")"

        if self.is_empty():
            return "Empty"
        elif self.is_string():
            if self.is_valid_string():
                return "String"
            else:
                return "Invalid String"
        elif self.is_number_or_quantity():
            if self.is_valid_number():
                return "Number"
            elif self.is_valid_quantity():
                return "Quantity"
            else:
                return "Invalid Number or Quantity"
        elif self.is_language_qualified_string():
            if self.is_valid_language_qualified_string():
                return "Language Qualified String"
            else:
                return "Invalid Language Qualified String"
        elif self.is_location_coordinates():
            if self.is_valid_location_coordinates():
                return "Location Coordinates"
            else:
                return "Invalid Location Coordinates"
        elif self.is_date_and_times():
            if self.is_valid_date_and_times():
                return "Date and Times"
            else:
                return "Invalid Date and Times"
        elif self.is_extension():
            return "Extension (unvalidated)"
        elif self.is_boolean():
            return "Boolean Symbol"
        elif self.is_symbol():
            return "Symbol"
        else:
            return "Unknown"
    
def main():
    """
    Test the KGTK value parser.
    """
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument(dest="values", help="The values(s) to test", type=str, nargs="+")
    parser.add_argument("-v", "--verbose", dest="verbose", help="Print additional progress messages.", action='store_true')
    parser.add_argument(      "--very-verbose", dest="very_verbose", help="Print additional progress messages.", action='store_true')
    KgtkValueOptions.add_arguments(parser)
    args: Namespace = parser.parse_args()

    # Build the value parsing option structure.
    value_options: KgtkValueOptions = KgtkValueOptions.from_args(args)

    value: str
    for value in args.values:
        print("%s: %s" % (value, KgtkValue(value, options=value_options).describe()), flush=True)

if __name__ == "__main__":
    main()
