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
    parent: typing.Optional['KgtkValue'] = attr.ib(default=None)

    # Cache some properties of the value that would be expensive to
    # continuously recompute. The class is not frozen because we have these
    # cache members.
    data_type: typing.Optional[KgtkFormat.DataType] = None
    valid: typing.Optional[bool] = None

    # If this is a list, cache a KgtkValue object for each item of the list.
    list_items: typing.Optional[typing.List['KgtkValue']] = None

    # Offer the components of a string or language-qualified string:
    contents: typing.Optional[str] = None # String contents without the enclosing quotes
    lang: typing.Optional[str] = None
    suffix: typing.Optional[str] = None # Includes the leading dash.

    # Offer the components of a number or quantity:
    number: typing.Optional[str] = None # Note: not converted to int or float
    low_tolerance: typing.Optional[str] = None # Note: not converted to int or float
    high_tolerance: typing.Optional[str] = None # Note: not converted to int or float
    si_units: typing.Optional[str] = None
    wikidata_node: typing.Optional[str] = None

    # Offer the components of a location coordinates:
    latstr: typing.Optional[str] = None
    lat: typing.Optional[float] = None
    lonstr: typing.Optional[str] = None
    lon: typing.Optional[float] = None

    # Offer the components of a date and times:
    yearstr: typing.Optional[str] = None # Note: not converted to int
    year: typing.Optional[int] = None
    monthstr: typing.Optional[str] = None # Note: not converted to int
    month: typing.Optional[int] = None
    daystr: typing.Optional[str] = None # Note: not converted to int
    day: typing.Optional[int] = None
    hourstr: typing.Optional[str] = None # Note: not converted to int or float
    minutesstr: typing.Optional[str] = None # Note: not converted to int or float
    secondsstr: typing.Optional[str] = None # Note: not converted to int or float
    zonestr: typing.Optional[str] = None
    precisionstr: typing.Optional[str] = None
    iso8601basic: typing.Optional[bool] = None # True when hyphens/colons present.

    def is_valid(self)->bool:
        # Is this a valid whatever it is?
        if self.valid is not None:
            return self.valid
        else:
            return self.validate()

    def is_empty(self, validate: bool = False)->bool:
        # Is this an empty item?  If so, assume it is valid and ignore the
        # validate parameter.
        if self.data_type is not None:
            return self.data_type == KgtkFormat.DataType.EMPTY

        if len(self.value) != 0:
            return False

        # We are certain that this is an empty value.  We can be certain it is valid.
        self.data_type = KgtkFormat.DataType.EMPTY
        self.valid = True
        return True

    split_list_re: typing.Pattern = re.compile(r"(?<!\\)" + "\\" + KgtkFormat.LIST_SEPARATOR)

    def get_list_items(self)->typing.List['KgtkValue']:
        # If this is a KGTK List, return a list of KGTK values representing
        # the items in the list.  If this is not a KGTK List, return an empty list.
        if self.list_items is not None:
            return self.list_items

        # Split the KGTK list.
        values: typing.List[str] = KgtkValue.split_list_re.split(self.value)

        # Perhaps we'd like to escape the list separators instead of splitting on them?
        if self.options.escape_list_separators:
            self.value = ("\\" + KgtkFormat.LIST_SEPARATOR).join(values)
            return [ ] # Return an empty list.

        # Return an empty Python list if this is not a KGTK list.
        self.list_items: typing.List['KgtkValue'] = [ ]
        if len(values) > 1:
            # Populate list_items with a KgtkValue for each item in the list:
            item_value: str
            for item_value in values:
                self.list_items.append(KgtkValue(item_value, options=self.options, parent=self))
        return self.list_items

    def is_list(self, validate: bool = False)->bool:
        # Must test for list before anything else (except empty)!
        if self.data_type is None:
            if len(self.get_list_items()) == 0:
                return False
            # We are certain that this is a list, although we haven't checked validity.
            self.data_type = KgtkFormat.DataType.LIST
        else:
            if self.data_type != KgtkFormat.DataType.LIST:
                return False

        if not validate:
            return True
        if self.valid is not None:
            return self.valid
        
        # Validate the list.
        item: 'KgtkValue'
        for item in self.get_list_items():
            if not item.is_valid():
                # The list is invalid if any item in the list is invalid.
                self.valid = False
                return False

        # This is a valid list.
        self.valid = True
        return True

    def rebuild_list(self):
        # Called to repair a list when we've repaired a list item.
        if self.list_items is None or len(self.list_items) == 0:
            return
        
        values: typing.List[str] = []
        item: KgtkValue
        for item in self.list_items:
            values.append(item.value)
        self.value = KgtkFormat.LIST_SEPARATOR.join(values)
        

    def _is_number_or_quantity(self)->bool:
        return self.value.startswith(("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+", "-", "."))

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

    # Numeric literals with componet labeling:
    number_pat: str = r'(?P<number>{numeric})'.format(numeric=numeric_pat)

    # Tolerances
    tolerance_pat: str = r'(?:\[(?P<low_tolerance>{numeric}),(?P<high_tolerance>{numeric})\])'.format(numeric=numeric_pat)

    # SI units taken from:
    # http://www.csun.edu/~vceed002/ref/measurement/units/units.pdf
    #
    # Note: if Q were in this list, it would conflict with Wikidata nodes (below).
    si_unit_pat: str = r'(?:m|kg|s|C|K|mol|cd|F|M|A|N|ohms|V|J|Hz|lx|H|Wb|V|W|Pa)'
    si_power_pat: str = r'(?:-1|2|3)' # Might need more.
    si_combiner_pat: str = r'[./]'
    si_pat: str = r'(?P<si_units>{si_unit}{si_power}?(?:{si_combiner}{si_unit}{si_power}?)*)'.format(si_unit=si_unit_pat,
                                                                                           si_combiner=si_combiner_pat,
                                                                                           si_power=si_power_pat)
    # Wikidata nodes (for units):
    nonzero_digit_pat: str = r'[1-9]'
    wikidata_node_pat: str = r'(?P<wikidata_node>Q{nonzero_digit}{digit}*)'.format(nonzero_digit=nonzero_digit_pat,
                                                                    digit=digit_pat)

    units_pat: str = r'(?:{si}|{wikidata_node})'.format(si=si_pat,
                                                        wikidata_node=wikidata_node_pat)
    

    # This definition matches numbers or quantities.
    number_or_quantity_pat: str = r'{numeric}{tolerance}?{units}?'.format(numeric=number_pat,
                                                                          tolerance=tolerance_pat,
                                                                          units=units_pat)

    # This matches numbers or quantities.
    number_or_quantity_re: typing.Pattern = re.compile(r'^' + number_or_quantity_pat + r'$')

    # This matches numbers but not quantities.
    number_re: typing.Pattern = re.compile(r'^' + number_pat + r'$')

    def is_number_or_quantity(self, validate: bool=False)->bool:
        """
        Return True if the first character is 0-9,_,-,.
        and it is either a Python-compatible number or an enhanced
        quantity.
        """
        # If we know the specific data type, delegate the test to that data type.
        if self.data_type is not None:
            if self.data_type == KgtkFormat.DataType.NUMBER:
                return self.is_number(validate=validate)
            elif self.data_type == KgtkFormat.DataType.QUANTITY:
                return self.is_quantity(validate=validate)
            else:
                # Clear the number or quantity components:
                self.number = None
                self.low_tolerance = None
                self.high_tolerance = None
                self.si_units = None
                self.wikidata_node = None
                return False # Not a number or quantity.

        # Clear the number or quantity components:
        self.number = None
        self.low_tolerance = None
        self.high_tolerance = None
        self.si_units = None
        self.wikidata_node = None

        if not self._is_number_or_quantity():
            return False

        if not validate:
            return True

        # We cannot cache the result of this test because it would interfere
        # if we later determined the exact data type.  We could work around
        # this problem with more thought.
        m: typing.Optional[typing.Match] = KgtkValue.number_or_quantity_re.match(self.value)
        if m is None:
            return False

        # Extract the number or quantity components:
        self.number = m.group("number")
        self.low_tolerance = m.group("low_tolerance")
        self.high_tolerance = m.group("high_tolerance")
        self.si_units = m.group("si_units")
        self.wikidata_node = m.group("wikidata_node")

        if self.low_tolerance is not None or self.high_tolerance is not None or self.si_units is not None or self.wikidata_node is not None:
            # We can be certain that this is a quantity.
            self.data_type = KgtkFormat.DataType.QUANTITY
        else:
            # We can be certain that this is a number
            self.data_type = KgtkFormat.DataType.NUMBER

        self.valid = True
        return True
    
    def is_number(self, validate: bool=False)->bool:
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
                # Clear the number components:
                self.number = None
                return False

            if not validate:
                return True
            if self.valid is not None:
                return self.valid
        
        # Clear the number components:
        self.number = None

        if not self._is_number_or_quantity():
            return False
        # We don't know yet if this is a number.  It could be a quantity.

        m: typing.Optional[typing.Match] = KgtkValue.number_re.match(self.value)
        if m is None:
            return False

        # Extract the number components:
        self.number = m.group("number")

        # Now we can be certain that this is a number.
        self.data_type = KgtkFormat.DataType.NUMBER
        self.valid = True
        return True
        
    
    def is_quantity(self, validate: bool=False)->bool:
        """
        Return True if the first character is 0-9,_,-,.
        and it is an enhanced quantity.
        """
        if self.data_type is not None:
            if self.data_type != KgtkFormat.DataType.QUANTITY:
                # Clear the quantity components:
                self.number = None
                self.low_tolerance = None
                self.high_tolerance = None
                self.si_units = None
                self.wikidata_node = None
                return False
            
            if not validate:
                return True
            if self.valid is not None:
                return self.valid
        
        # Clear the quantity components:
        self.number = None
        self.low_tolerance = None
        self.high_tolerance = None
        self.si_units = None
        self.wikidata_node = None

        if not self._is_number_or_quantity():
            return False
        # We don't know yet if this is a quantity.  It could be a number.

        m: typing.Optional[typing.Match] = KgtkValue.number_or_quantity_re.match(self.value)
        if m is None:
            return False

        # Extract the quantity components:
        self.number = m.group("number")
        self.low_tolerance = m.group("low_tolerance")
        self.high_tolerance = m.group("high_tolerance")
        self.si_units = m.group("si_units")
        self.wikidata_node = m.group("wikidata_node")

        if self.low_tolerance is None and self.high_tolerance is None and self.si_units is None and self.wikidata_node is None:
            # This is a number, not a quantity
            self.data_type = KgtkFormat.DataType.NUMBER
            self.valid = True
            return False

        # Now we can be certain that this is a quantity.
        self.data_type = KgtkFormat.DataType.QUANTITY
        self.valid = True
        return True
    
    lax_string_re: typing.Pattern = re.compile(r'^"(?P<contents>.*)"$')
    strict_string_re: typing.Pattern = re.compile(r'^"(?P<contents>(?:[^"\\]|\\.)*"$)')

    def is_string(self, validate: bool = False)->bool:
        """
        Return True if the first character  is '"'.

        Strings begin and end with double quote (").  Any internal double
        quotes must be escaped with backslash (\").  Triple-double quoted
        strings are not supported by KGTK File Vormat v2.

        """
        if self.data_type is None:
            if not self.value.startswith('"'):
                # Clear the string components:
                self.contents = None
                return False
            # We are certain this is a string.  We don't yet know if it is valid.
            self.data_type = KgtkFormat.DataType.STRING
        else:
            if self.data_type != KgtkFormat.DataType.STRING:
                # Clear the string components:
                self.contents = None
                return False

        if not validate:
            return True
        if self.valid is not None:
            return self.valid
        
        # Clear the string components:
        self.contents = None
        
        # Validate the string:
        m: typing.Optional[typing.Match]
        if self.options.allow_lax_strings:
            m = KgtkValue.lax_string_re.match(self.value)
        else:
            m = KgtkValue.strict_string_re.match(self.value)
        if m is None:
            return False

        # Extract the contents components:
        self.contents = m.group("contents")

        # We are certain that this is a valid string.
        self.valid = True
        return True

    def is_structured_literal(self)->bool:
        """
        Return True if the first character  is ^@'!.
        """
        return self.value.startswith(("^", "@", "'", "!"))

    def is_symbol(self, validate: bool = False)->bool:
        """
        Return True if not a number, string, nor structured literal, nor boolean.

        The validate parameter is ignored.
        """
        if self.data_type is not None:
            return self.data_type == KgtkFormat.DataType.SYMBOL

        # Is this a symbol?  It is, if it is not something else.
        if self.is_number_or_quantity() or self.is_string() or self.is_structured_literal() or self.is_boolean():
            return False
            
        # We are certain this is a symbol.  We assume that it is valid.
        self.data_type = KgtkFormat.DataType.SYMBOL
        self.valid = True
        return True

    def is_boolean(self, validate: bool = False)->bool:
        """
        Return True if the value matches one of the special boolean symbols.

        The validate parameter is ignored.
        """
        if self.data_type is not None:
            return self.data_type == KgtkFormat.DataType.BOOLEAN

        # Is this a boolean?
        if self.value != KgtkFormat.TRUE_SYMBOL and self.value != KgtkFormat.FALSE_SYMBOL:
            return False
            
        # We are certain this is a valid boolean.
        self.data_type = KgtkFormat.DataType.BOOLEAN
        self.valid = True
        return True

    # Support two or three character language codes.  Suports hyphenated codes
    # with a country code or dialect namesuffix after the language code.
    lax_language_qualified_string_re: typing.Pattern = re.compile(r"^'(?P<contents>.*)'@(?P<lang>[a-zA-Z]{2,3}(?P<suffix>-[a-zA-Z]+)?)$")
    strict_language_qualified_string_re: typing.Pattern = re.compile(r"^'(?P<contents>(?:[^'\\]|\\.)*)'@(?P<lang_suffix>(?P<lang>[a-zA-Z]{2,3})(?P<suffix>-[a-zA-Z]+)?)$")

    def is_language_qualified_string(self, validate: bool=False)->bool:
        """
        Return True if the value looks like a language-qualified string.
        """
        if self.data_type is None:
            if not self.value.startswith("'"):
                # Clear the cached components of the language qualified string:
                self.contents = None
                self.lang = None
                self.suffix = None
                return False
            # We are certain that this is a language qualified string, although we haven't checked validity.
            self.data_type = KgtkFormat.DataType.LANGUAGE_QUALIFIED_STRING
        else:
            if self.data_type != KgtkFormat.DataType.LANGUAGE_QUALIFIED_STRING:
                # Clear the cached components of the language qualified string:
                self.contents = None
                self.lang = None
                self.suffix = None
                return False

        if not validate:
            return True
        if self.valid is not None:
            return self.valid
        
        # Clear the cached components of the language qualified string:
        self.contents = None
        self.lang = None
        self.suffix = None

        # Validate the language qualified string.
        # print("checking %s" % self.value)
        m: typing.Optional[typing.Match]
        if self.options.allow_lax_lq_strings:
            m = KgtkValue.lax_language_qualified_string_re.match(self.value)
        else:
            m = KgtkValue.strict_language_qualified_string_re.match(self.value)
        if m is None:
            # print("match failed for %s" % self.value)
            return False

        # Extract the contents, lang, and optional suffix components:
        self.contents = m.group("contents")
        self.lang = m.group("lang")
        self.suffix = m.group("suffix")

        # Extract the combined lang and suffix for use by the LanguageValidator.
        lang_suffix: str = m.group("lang_suffix")
        # print("lang: %s" % lang_suffix)

        # Validate the language code:
        if not LanguageValidator.validate(lang_suffix.lower(), options=self.options):
            # print("language validation failed for %s" % self.value)
            return False

        # We are certain that this is a valid language qualified string.
        self.valid = True
        return True

    #location_coordinates_re: typing.Pattern = re.compile(r"^@(?P<lat>[-+]?\d{3}\.\d{5})/(?P<lon>[-+]?\d{3}\.\d{5})$")
    degrees_pat: str = r'(?:[-+]?(?:\d+(?:\.\d*)?)|(?:\.\d+))'
    location_coordinates_re: typing.Pattern = re.compile(r'^@(?P<lat>{degrees})/(?P<lon>{degrees})$'.format(degrees=degrees_pat))

    def is_location_coordinates(self, validate: bool=False)->bool:
        """
        Return False if this value is a list and idx is None.
        Otherwise, return True if the value looks like valid location coordinates.

        @043.26193/010.92708
        """
        if self.data_type is None:
            if not self.value.startswith("@"):
                self.latstr = None
                self.lat = None
                self.lonstr = None
                self.lon = None
                return False
            # We are certain that this is location coordinates, although we haven't checked validity.
            self.data_type = KgtkFormat.DataType.LOCATION_COORDINATES
        else:
            if self.data_type != KgtkFormat.DataType.LOCATION_COORDINATES:
                self.latstr = None
                self.lat = None
                self.lonstr = None
                self.lon = None
                return False

        if not validate:
            return True
        if self.valid is not None:
            return self.valid
        
        # Clear the lat/lon components:
        self.latstr = None
        self.lat = None
        self.lonstr = None
        self.lon = None

        # Validate the location coordinates:
        m: typing.Optional[typing.Match] = KgtkValue.location_coordinates_re.match(self.value)
        if m is None:
            return False

        latstr: str = m.group("lat")
        self.latstr = latstr
        lonstr: str = m.group("lon")
        self.lonstr = lonstr

        # Latitude normally runs from -90 to +90:
        try:
            self.lat = float(latstr)
            if  self.lat < self.options.minimum_valid_lat or self.lat > self.options.maximum_valid_lat:
                return False
        except ValueError:
            return False

        # Longitude normally runs from -180 to +180:
        try:
            self.lon = float(lonstr)
            if self.lon < self.options.minimum_valid_lon or self.lon > self.options.maximum_valid_lon:
                return False
        except ValueError:
            return False

        # We are certain that this is valid.
        self.valid = True
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
    seconds_pat: str = r'(?P<seconds>[0-5][0-9])'

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
                                                                        
    def is_date_and_times(self, validate: bool=False)->bool:
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
        if self.data_type is None:
            if not self.value.startswith("^"):
                # Clear the cached date and times components:
                self.yearstr = None
                self.monthstr = None
                self.daystr = None
                self.hourstr = None
                self.minutesstr = None
                self.secondsstr = None
                self.year = None
                self.month = None
                self.day = None
                self.zonestr = None
                self.precisionstr = None
                self.iso8601basic = None
                return False
            # We are certain that this is location coordinates, although we haven't checked validity.
            self.data_type = KgtkFormat.DataType.DATE_AND_TIMES
        else:
            if self.data_type != KgtkFormat.DataType.DATE_AND_TIMES:
                # Clear the cached date and times components:
                self.yearstr = None
                self.monthstr = None
                self.daystr = None
                self.hourstr = None
                self.minutesstr = None
                self.secondsstr = None
                self.year = None
                self.month = None
                self.day = None
                self.zonestr = None
                self.precisionstr = None
                self.iso8601basic = None
                return False

        if not validate:
            return True
        if self.valid is not None:
            return self.valid
        
        # Clear the cached date and times components:
        self.yearstr = None
        self.monthstr = None
        self.daystr = None
        self.hourstr = None
        self.minutesstr = None
        self.secondsstr = None
        self.year = None
        self.month = None
        self.day = None
        self.zonestr = None
        self.precisionstr = None
        self.iso8601basic = None

        # Validate the date and times:
        m: typing.Optional[typing.Match] = KgtkValue.lax_date_and_times_re.match(self.value)
        if m is None:
            return False

        self.yearstr = m.group("year")
        self.monthstr = m.group("month")
        self.daystr = m.group("day")
        self.hourstr = m.group("hour")
        self.minutesstr = m.group("minutes")
        self.secondsstr = m.group("seconds")
        self.zonestr = m.group("zone")
        self.precisionstr = m.group("precision")
        self.iso8601basic = m.group("hyphen") is None

        fixup_needed: bool = False

        # Validate the year:
        if self.yearstr is None or len(self.yearstr) == 0:
            return False # Years are mandatory
        try:
            self.year: int = int(self.yearstr)
        except ValueError:
            return False
        if self.year < self.options.minimum_valid_year:
            return False
        if self.year > self.options.maximum_valid_year:
            return False

        if self.monthstr is not None:
            try:
                self.month: int = int(self.monthstr)
            except ValueError:
                return False # shouldn't happen
            if self.month == 0:
                if self.options.repair_month_or_day_zero:
                    self.month = 1
                    self.monthstr = "01"
                    fixup_needed = True
                elif not self.options.allow_month_or_day_zero:
                    return False # month 0 was disallowed.

        if self.daystr is not None:
            try:
                self.day: int = int(self.daystr)
            except ValueError:
                return False # shouldn't happen
            if self.day == 0:
                if self.options.repair_month_or_day_zero:
                    self.day = 1
                    self.daystr = "01"
                    fixup_needed = True
                elif not self.options.allow_month_or_day_zero:
                    return False # day 0 was disallowed.

        if fixup_needed:
            # Rapair a month or day zero problem.  If this value is the child
            #of a list, repair the list parent value, too.
            self.update_date_and_times()
            if self.parent is not None:
                self.parent.rebuild_list()

        # We are fairly certain that this is a valid date and times.
        self.valid = True
        return True

    def update_date_and_times(self):
        v: str = "^" + self.yearstr
        if self.monthstr is not None:
            if not self.iso8601basic:
                v += "-"
            v += self.monthstr
        if self.daystr is not None:
            if not self.iso8601basic:
                v += "-"
            v += self.daystr
        if self.hourstr is not None:
            v += "T"
            v += self.hourstr
        if self.minutesstr is not None:
            if not self.iso8601basic:
                v += ":"
            v += self.minutesstr
        if self.secondsstr is not None:
            if not self.iso8601basic:
                v += ":"
            v += self.secondsstr
        if self.zonestr is not None:
            v += self.zonestr
        if self.precisionstr is not None:
            v += "/"
            v += self.precisionstr
        self.value = v

    def is_extension(self, validate=False)->bool:
        """Return True if the first character is !

        Although we refer to the validate parameter in the code below, we
        force self.valid to False.

        """
        if self.data_type is not None:
            if not self.value.startswith("!"):
                return False
            # This is an extension, but for now, assume that all extensions are invalid.
            self.data_type = KgtkFormat.DataType.EXTENSION
            self.valid = False
        else:
            if self.data_type != KgtkFormat.DataType.EXTENSION:
                return False

        if not validate:
            return True
        if self.valid is not None:
            return self.valid
        raise ValueError("Inconsistent extension state.")

    def classify(self)->KgtkFormat.DataType:
        # Classify this KgtkValue into a KgtkDataType.
        if self.data_type is not None:
            # Return the cached value.
            return self.data_type

        # Must test for list before anything else (except empty)!
        if self.is_empty() or self.is_list():
            pass

        elif self.is_string() or self.is_language_qualified_string():
            pass

        elif self.is_number_or_quantity():
            # To determine whether this is a number or a quantity, we have
            # to validate one of them.
            if not self.is_number():
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

    def reclassify(self)->KgtkFormat.DataType:
        # Classify this KgtkValue into a KgtkDataType, ignoring any cached data_type.
        self.data_type = None
        self.valid = None
        return self.classify()

    def validate(self)->bool:
        # Validate this KgtkValue.

        # Start by classifying the KgtkValue.
        dt: KgtkFormat.DataType = self.classify()

        # If the valid flag has already been cached, return that.
        if self.valid is not None:
            return self.valid
        
        # Validate the value.
        if dt == KgtkFormat.DataType.EMPTY:
            return self.is_empty(validate=True)
        elif dt == KgtkFormat.DataType.LIST:
            return self.is_list(validate=True)
        elif dt == KgtkFormat.DataType.NUMBER:
            return self.is_number(validate=True)
        elif dt == KgtkFormat.DataType.QUANTITY:
            return self.is_quantity(validate=True)
        elif dt == KgtkFormat.DataType.STRING:
            return self.is_string(validate=True)
        elif dt == KgtkFormat.DataType.LANGUAGE_QUALIFIED_STRING:
            return self.is_language_qualified_string(validate=True)
        elif dt == KgtkFormat.DataType.LOCATION_COORDINATES:
            return self.is_location_coordinates(validate=True)
        elif dt == KgtkFormat.DataType.DATE_AND_TIMES:
            return self.is_date_and_times(validate=True)
        elif dt == KgtkFormat.DataType.EXTENSION:
            return self.is_extension(validate=True)
        elif dt == KgtkFormat.DataType.BOOLEAN:
            return self.is_boolean(validate=True)
        elif dt == KgtkFormat.DataType.SYMBOL:
            return self.is_symbol(validate=True)
        else:
            raise ValueError("Unrecognized DataType.")

    def revalidate(self, reclassify: bool=False)->bool:
        # Revalidate this KgtkValue after clearing cached values.
        if reclassify:
            self.data_type = None
        self.valid = None
        return self.validate()
        
    def describe(self)->str:
        """
        Return a string that describes this KGTK Value.
        """
        dt: KgtkFormat.DataType = self.classify()
        if dt == KgtkFormat.DataType.EMPTY:
            return "Empty" if self.is_empty(validate=True) else "Invalid Empty"
        elif dt == KgtkFormat.DataType.LIST:
            result: str = "List (" if self.is_list(validate=True) else "Invalid List ("
            kv: KgtkValue
            first: bool = True
            for kv in self.get_list_items():
                if first:
                    first = not first
                else:
                    result += KgtkFormat.LIST_SEPARATOR
                result += kv.describe()
            return result + ")"
        elif dt == KgtkFormat.DataType.NUMBER:
            return "Number" if self.is_number(validate=True) else "Invali Number"
        elif dt == KgtkFormat.DataType.QUANTITY:
            return "Quantity" if self.is_quantity(validate=True) else "Invalid Quantity"
        elif dt == KgtkFormat.DataType.STRING:
            return "String" if self.is_string(validate=True) else "Invalid String"
        elif dt == KgtkFormat.DataType.LANGUAGE_QUALIFIED_STRING:
            return "Language Qualified String (%s)" % self.lang if self.is_language_qualified_string(validate=True) else "Invalid Language Qualified String"
        elif dt == KgtkFormat.DataType.LOCATION_COORDINATES:
            return "Location Coordinates" if self.is_location_coordinates(validate=True) else "Invalid Location Coordinates"
        elif dt == KgtkFormat.DataType.DATE_AND_TIMES:
            return "Date and Times" if self.is_date_and_times(validate=True) else "Invalid Date and Times"
        elif dt == KgtkFormat.DataType.EXTENSION:
            return "Extension" if self.is_extension(validate=True) else "Invalid Extension"
        elif dt == KgtkFormat.DataType.BOOLEAN:
            return "Boolean" if self.is_boolean(validate=True) else "Invalid Boolean"
        elif dt == KgtkFormat.DataType.SYMBOL:
            return "Symbol" if self.is_symbol(validate=True) else "Invalid Symbol"
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
        kv: KgtkValue = KgtkValue(value, options=value_options)
        kv.validate()
        nv: str = kv.value
        if value == nv:
            print("%s: %s" % (value, kv.describe()), flush=True)
        else:
            print("%s => %s: %s" % (value, nv, kv.describe()), flush=True)
            

if __name__ == "__main__":
    main()
