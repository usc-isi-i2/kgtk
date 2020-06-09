"""
Validate KGTK File data types.
"""

from argparse import ArgumentParser, Namespace
import attr
import math
import re
import sys
import typing

from kgtk.kgtkformat import KgtkFormat
from kgtk.value.kgtkvalueoptions import KgtkValueOptions, DEFAULT_KGTK_VALUE_OPTIONS
from kgtk.value.languagevalidator import LanguageValidator


@attr.s(slots=True, frozen=False)
class KgtkValueFields():
    data_type: KgtkFormat.DataType = attr.ib(validator=attr.validators.instance_of(KgtkFormat.DataType))
    valid: bool = attr.ib(validator=attr.validators.instance_of(bool))

    # The following members offer access to the components (fields) of a
    # KgtkValue.  They are accessible immediately after validating the
    # contents of the KgtkValue object when kgtk_value.parse_fields is True.
    #
    # obj.is_valid() return True
    # obj.validate() returns True
    # obj.revalidate() returns True
    # obj.is_language_qualified_string(validate=True) returns True
    #... etc.
    #
    # The fields may be accessed directly from this object or they may be
    # obtained as a map via obj.get_fields()

    # >0 if this is a list.
    list_len: int = attr.ib(validator=attr.validators.instance_of(int), default=0)

    # Offer the components of a string or language-qualified string, after validating the item.
    # String contents without the enclosing quotes
    text: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)

    # 2- or 3-character language code code without suffix.
    language: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)

    # The language code suffix, including the leading dash.
    language_suffix: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)

    # Offer the components of a number or quantity, after validating the item.
    numberstr: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    number: typing.Optional[typing.Union[int, float]] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of((int, float))), default=None)

    low_tolerancestr: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    low_tolerance: typing.Optional[float] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(float)), default=None)

    high_tolerancestr: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    high_tolerance: typing.Optional[float] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(float)), default=None)

    si_units: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)

    units_node: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)

    # Offer the components of a location coordinates, after validaating the item:
    latitudestr: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    latitude: typing.Optional[float] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(float)), default=None)

    longitudestr: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    longitude: typing.Optional[float] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(float)), default=None)

    # Offer the components of a date and times, after validating the item:
    date: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    time: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None) # includes timezone
    date_and_time: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None) # includes timezone
    
    yearstr: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    year: typing.Optional[int] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)), default=None)

    monthstr: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    month: typing.Optional[int] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)), default=None)

    daystr: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    day: typing.Optional[int] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)), default=None)
    
    hourstr: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    hour: typing.Optional[int] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)), default=None)

    minutesstr: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    minutes: typing.Optional[int] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)), default=None)
    
    secondsstr: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    seconds: typing.Optional[int] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)), default=None)
    
    # Z or [-+]HH or [-+]HHMM or [-+]HH:MM
    zonestr: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    
    precisionstr: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    precision: typing.Optional[int] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)), default=None)
    
    # True when hyphens/colons are present.
    iso8601extended: typing.Optional[bool] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(bool)), default=None)

    # Offer the contents of a boolean, after validating the item:
    truth: typing.Optional[bool] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(bool)), default=None)

    # Everything else must be a symbol.
    symbol: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)

    # TODO: Reorganize these lists and dicts into a structure.

    FIELD_NAMES: typing.List[str] = [
        "list_len",
        "data_type",
        "valid",
        "text",
        "language",
        "language_suffix",
        "numberstr",
        "number",
        "low_tolerancestr",
        "low_tolerance",
        "high_tolerancestr",
        "high_tolerance",
        "si_units",
        "units_node",
        "latitudestr",
        "latitude",
        "longitudestr",
        "longitude",
        "date",
        "time",
        "date_and_time",
        "yearstr",
        "year",
        "monthstr",
        "month",
        "daystr",
        "day",
        "hourstr",
        "hour",
        "minutesstr",
        "minutes",
        "secondsstr",
        "seconds",
        "zonestr",
        "precisionstr",
        "precision",
        "iso8601extended",
        "truth",
        "symbol"
        ]

    DEFAULT_FIELD_NAMES: typing.List[str] = [
        "data_type",
        "valid",
        "list_len",
        "text",
        "language",
        "language_suffix",
        "number",
        "low_tolerance",
        "high_tolerance",
        "si_units",
        "units_node",
        "latitude",
        "longitude",
        "date_and_time",
        "precision",
        "truth",
        "symbol"
        ]

    FIELD_NAME_FORMATS: typing.Mapping[str, str] = {
        "list_len": "int",
        "data_type": "sym",
        "valid": "bool",
        "text": "str",
        "language": "sym",
        "language_suffix": "sym",
        "numberstr": "str",
        "number": "num",
        "low_tolerancestr": "str",
        "low_tolerance": "num",
        "high_tolerancestr": "str",
        "high_tolerance": "num",
        "si_units": "sym",
        "units_node": "sym",
        "latitudestr": "str",
        "latitude": "num",
        "longitudestr": "str",
        "longitude": "num",
        "date": "str",
        "time": "str",
        "date_and_time": "str",
        "yearstr": "str",
        "year": "int",
        "monthstr": "str",
        "month": "int",
        "daystr": "str",
        "day": "int",
        "hourstr": "str",
        "hour": "int",
        "minutesstr": "str",
        "minutes": "int",
        "secondsstr": "str",
        "seconds": "int",
        "zonestr": "str",
        "precisionstr": "str",
        "precision": "int",
        "iso8601extended": "bool",
        "truth": "bool",
        "symbol": "sym",
    }

    DATA_TYPE_FIELDS: typing.Mapping[str, typing.List[str]] = {
        KgtkFormat.DataType.EMPTY.lower(): [ "data_type", "valid" ],
        KgtkFormat.DataType.LIST.lower(): [ "data_type", "valid", "list_len" ],
        KgtkFormat.DataType.NUMBER.lower(): [ "data_type", "valid", "numberstr", "number" ],
        KgtkFormat.DataType.QUANTITY.lower(): [ "data_type", "valid",
                                                "numberstr", "number",
                                                "low_tolerancestr", "low_tolerance",
                                                "high_tolerancestr", "high_tolerance",
                                                "si_units", "units_node",
        ],
        KgtkFormat.DataType.STRING.lower(): [ "data_type", "valid", "text" ],
        KgtkFormat.DataType.LANGUAGE_QUALIFIED_STRING.lower(): [ "data_type", "valid", "text", "language", "language_suffix" ],
        KgtkFormat.DataType.LOCATION_COORDINATES.lower(): [ "data_type", "valid",
                                                            "latitudestr", "latitude",
                                                            "longitudestr", "longitude",
        ],
        KgtkFormat.DataType.DATE_AND_TIMES.lower(): [ "data_type", "valid",
                                                      "date_and_time",
                                                      "date", "time",
                                                      "yearstr", "year",
                                                      "monthstr", "month",
                                                      "daystr", "day",
                                                      "hourstr", "hour",
                                                      "minutesstr", "minutes",
                                                      "secondsstr", "seconds",
                                                      "zonestr",
                                                      "precisionstr", "precision",
                                                      "iso8601extended",
        ],
        KgtkFormat.DataType.EXTENSION.lower(): [ ],
        KgtkFormat.DataType.BOOLEAN.lower(): [ "data_type", "valid", "truth" ],
        KgtkFormat.DataType.SYMBOL.lower(): [ "data_type", "valid", "symbol" ],
    }

    DEFAULT_DATA_TYPE_FIELDS: typing.Mapping[str, typing.List[str]] = {
        KgtkFormat.DataType.EMPTY.lower(): [ "data_type", "valid" ],
        KgtkFormat.DataType.LIST.lower(): [ "data_type", "valid", "list_len" ],
        KgtkFormat.DataType.NUMBER.lower(): [ "data_type", "valid", "number" ],
        KgtkFormat.DataType.QUANTITY.lower(): [ "data_type", "valid",
                                                "number",
                                                "low_tolerance",
                                                "high_tolerance",
                                                "si_units",
                                                "units_node",
        ],
        KgtkFormat.DataType.STRING.lower(): [ "data_type", "valid", "text" ],
        KgtkFormat.DataType.LANGUAGE_QUALIFIED_STRING.lower(): [ "data_type", "valid", "text", "language", "language_suffix" ],
        KgtkFormat.DataType.LOCATION_COORDINATES.lower(): [ "data_type", "valid",
                                                            "latitude",
                                                            "longitude",
        ],
        KgtkFormat.DataType.DATE_AND_TIMES.lower(): [ "data_type", "valid",
                                                      "date_and_time",
                                                      "precision",
        ],
        KgtkFormat.DataType.EXTENSION.lower(): [ ],
        KgtkFormat.DataType.BOOLEAN.lower(): [ "data_type", "valid", "truth" ],
        KgtkFormat.DataType.SYMBOL.lower(): [ "data_type", "valid", "symbol" ],
    }

    def to_map(self)->typing.Mapping[str, typing.Union[str, int, float, bool]]:
        results: typing.MutableMapping[str, typing.Union[str, int, float, bool]] = { }
        results["list_len"] = self.list_len
        if self.data_type is not None:
            results["data_type"] = self.data_type.name.lower()
        if self.valid is not None:
            results["valid"] = self.valid
        if self.text is not None:
            results["text"] = self.text
        if self.language is not None:
            results["language"] = self.language
        if self.language_suffix is not None:
            results["language_suffix"] = self.language_suffix
        if self.numberstr is not None:
            results["numberstr"] = self.numberstr
        if self.number is not None:
            results["number"] = self.number
        if self.low_tolerancestr is not None:
            results["low_tolerancestr"] = self.low_tolerancestr
        if self.low_tolerance is not None:
            results["low_tolerance"] = self.low_tolerance
        if self.high_tolerancestr is not None:
            results["high_tolerancestr"] = self.high_tolerancestr
        if self.high_tolerance is not None:
            results["high_tolerance"] = self.high_tolerance
        if self.si_units is not None:
            results["si_units"] = self.si_units
        if self.units_node is not None:
            results["units_node"] = self.units_node
        if self.latitudestr is not None:
            results["latitudestr"] = self.latitudestr
        if self.latitude is not None:
            results["latitude"] = self.latitude
        if self.longitudestr is not None:
            results["longitudestr"] = self.longitudestr
        if self.longitude is not None:
            results["longitude"] = self.longitude
        if self.date is not None:
            results["date"] = self.date
        if self.time is not None:
            results["time"] = self.time
        if self.date_and_time is not None:
            results["date_and_time"] = self.date_and_time
        if self.yearstr is not None:
            results["yearstr"] = self.yearstr
        if self.year is not None:
            results["year"] = self.year
        if self.monthstr is not None:
            results["monthstr"] = self.monthstr
        if self.month is not None:
            results["month"] = self.month
        if self.daystr is not None:
            results["daystr"] = self.daystr
        if self.day is not None:
            results["day"] = self.day
        if self.hourstr is not None:
            results["hourstr"] = self.hourstr
        if self.hour is not None:
            results["hour"] = self.hour
        if self.minutesstr is not None:
            results["minutesstr"] = self.minutesstr
        if self.minutes is not None:
            results["minutes"] = self.minutes
        if self.secondsstr is not None:
            results["secondsstr"] = self.secondsstr
        if self.seconds is not None:
            results["seconds"] = self.seconds
        if self.zonestr is not None:
            results["zonestr"] = self.zonestr
        if self.precisionstr is not None:
            results["precisionstr"] = self.precisionstr
        if self.precision is not None:
            results["precision"] = self.precision
        if self.iso8601extended is not None:
            results["iso8601extended"] = self.iso8601extended
        if self.truth is not None:
            results["truth"] = self.truth
        if self.symbol is not None:
            results["symbol"] = self.symbol
        return results
    
@attr.s(slots=True, frozen=False)
class KgtkValue(KgtkFormat):
    value: str = attr.ib(validator=attr.validators.instance_of(str))
    options: KgtkValueOptions = attr.ib(validator=attr.validators.instance_of(KgtkValueOptions), default=DEFAULT_KGTK_VALUE_OPTIONS)
    parse_fields: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    # The current fields when available:
    # fields: typing.Optional[KgtkValueFields] = attr.ib(attr.validators.instance_of(KgtkValueFields), default=None, init=False)
    fields: typing.Optional[KgtkValueFields] = attr.ib(default=None, init=False)

    # TODO: proper validation.
    parent: typing.Optional['KgtkValue'] = attr.ib(default=None)

    # Has this value been repaired?
    repaired: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    # Cache some properties of the value that would be expensive to
    # continuously recompute.
    data_type: typing.Optional[KgtkFormat.DataType] = None
    valid: typing.Optional[bool] = None

    # If this is a list, cache a KgtkValue object for each item of the list.
    #
    # Note: Please do not access this list directly.  Use get_list_items().
    list_items: typing.Optional[typing.List['KgtkValue']] = None

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
        if self.parse_fields:
            self.fields = KgtkValueFields(data_type=self.data_type, valid=self.valid)
        return True

    split_list_re: typing.Pattern = re.compile(r"(?<!\\)" + "\\" + KgtkFormat.LIST_SEPARATOR)

    @classmethod
    def split_list(cls, value: str)->typing.List[str]:
        return KgtkValue.split_list_re.split(value)

    @classmethod
    def join_list(cls, values: typing.List[str])->str:
        return KgtkFormat.LIST_SEPARATOR.join(values)

    @classmethod
    def join_sorted_list(cls, values: typing.List[str])->str:
        return KgtkFormat.LIST_SEPARATOR.join(sorted(values))

    @classmethod
    def join_unique_list(cls, values: typing.List[str])->str:
        if len(values) == 0:
            return ""
        elif len(values) == 1:
            return values[0]

        # There are alternatives to the following.
        #
        # TODO: Perform  timing study using typical KGTK lists.
        return KgtkFormat.LIST_SEPARATOR.join(sorted(list(set(values))))

    @classmethod
    def merge_values(cls, value1: str, value2: str)->str:
        # Merge two KGTK values eliminating duplicates.  Each value might be a list.
        #
        # This routine is potentially expensive.  Callers might be optimized
        # to minimize its use by building a local list, then calling
        # join_unique_list().
        if len(value1) == 0:
            return value2
        if len(value2) == 0:
            return value1
        if value1 == value2:
            return value1
        if KgtkFormat.LIST_SEPARATOR in value1:
            if KgtkFormat.LIST_SEPARATOR in value2:
                # This is rather expensive, but will work correctly:
                return cls.join_unique_list(cls.split_list(value1).extend(cls.split_list(value2)))
            else:
                # This is rather expensive, but will work correctly:
                lv: typing.List[str] = cls.split_list(value1)
                lv.append(value2)
                return cls.join_unique_list(lv)
        if KgtkFormat.LIST_SEPARATOR in value2:
            # This is rather expensive, but will work correctly:
            lv2: typing.List[str] = cls.split_list(value2)
            lv2.append(value1)
            return cls.join_unique_list(lv2)
        if value1 < value2:
            return KgtkFormat.LIST_SEPARATOR.join((value1, value2))
        else:
            return KgtkFormat.LIST_SEPARATOR.join((value2, value1))
                                                                      
    @classmethod
    def escape_list_separators(cls, values: typing.List[str])->str:
        return ("\\" + KgtkFormat.LIST_SEPARATOR).join(values)

    def get_list_items(self)->typing.List['KgtkValue']:
        # If this is a KGTK List, return a list of KGTK values representing
        # the items in the list.  If this is not a KGTK List, return an empty list.
        #
        # Note:  This is the only routine that should touch self.list_items.
        if self.list_items is not None:
            return self.list_items

        # Split the KGTK list.
        values: typing.List[str] = self.split_list(self.value)

        # Perhaps we'd like to escape the list separators instead of splitting on them?
        if self.options.escape_list_separators:
            self.value = self.escape_list_separators(values)
            return [ ] # Return an empty list.

        # Return an empty Python list if this is not a KGTK list.
        self.list_items: typing.List['KgtkValue'] = [ ]
        if len(values) > 1:
            # Populate list_items with a KgtkValue for each item in the list:
            item_value: str
            for item_value in values:
                self.list_items.append(KgtkValue(item_value, options=self.options, parse_fields=self.parse_fields, parent=self))
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
        
        # We will save the list length even if invalid.
        if self.parse_fields:
            self.fields = KgtkValueFields(data_type=KgtkFormat.DataType.LIST,
                                          valid=False,
                                          list_len=len(self.get_list_items()))

        # Validate the list.
        item: 'KgtkValue'
        for item in self.get_list_items():
            if not item.is_valid():
                # The list is invalid if any item in the list is invalid.
                self.valid = False
                return False

        # This is a valid list.
        self.valid = True
        if self.parse_fields:
            self.fields = KgtkValueFields(data_type=KgtkFormat.DataType.LIST,
                                          valid=self.valid,
                                          list_len=len(self.get_list_items()))
        return True

    def rebuild_list(self):
        # Called to repair a list when we've repaired a list item.
        list_items: typng.List[KgtkValues] = self.get_list_items()
        if list_items is None or len(list_items) == 0:
            return
        
        values: typing.List[str] = []
        item: KgtkValue
        for item in list_items:
            values.append(item.value)
            self.repaired = self.repaired or item.repaired
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

    # Numeric literals with component labeling:
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
    #
    # https://www.wikidata.org/wiki/Wikidata:Identifiers
    #
    #    "Each Wikidata entity is identified by an entity ID, which is a number prefixed by a letter."
    nonzero_digit_pat: str = r'[1-9]'
    units_node_pat: str = r'(?P<units_node>Q{nonzero_digit}{digit}*)'.format(nonzero_digit=nonzero_digit_pat,
                                                                             digit=digit_pat)
    lax_units_node_pat: str = r'(?P<units_node>Q[0-9A-Za-z][-0-9A-Za-z]*)'
    

    units_pat: str = r'(?:{si}|{units_node})'.format(si=si_pat,
                                                     units_node=units_node_pat)

    lax_units_pat: str = r'(?:{si}|{units_node})'.format(si=si_pat,
                                                         units_node=lax_units_node_pat)
    

    # This definition matches numbers or quantities.
    number_or_quantity_pat: str = r'{numeric}{tolerance}?{units}?'.format(numeric=number_pat,
                                                                          tolerance=tolerance_pat,
                                                                          units=units_pat)

    lax_number_or_quantity_pat: str = r'{numeric}{tolerance}?{units}?'.format(numeric=number_pat,
                                                                              tolerance=tolerance_pat,
                                                                              units=lax_units_pat)

    # This matches numbers or quantities.
    number_or_quantity_re: typing.Pattern = re.compile(r'^' + number_or_quantity_pat + r'$')

    lax_number_or_quantity_re: typing.Pattern = re.compile(r'^' + lax_number_or_quantity_pat + r'$')

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
                return False # Not a number or quantity.

        if not self._is_number_or_quantity():
            return False

        if not validate:
            return True

        # We cannot cache the result of this test because it would interfere
        # if we later determined the exact data type.  We could work around
        # this problem with more thought.
        m: typing.Optional[typing.Match]
        if self.options.allow_lax_qnodes:
            m = KgtkValue.lax_number_or_quantity_re.match(self.value)
        else:
            m = KgtkValue.number_or_quantity_re.match(self.value)
            
        if m is None:
            return False

        # Extract the number or quantity components:
        numberstr: typing.Optional[str] = m.group("number")
        low_tolerancestr: typing.Optional[str] = m.group("low_tolerance")
        high_tolerancestr: typing.Optional[str] = m.group("high_tolerance")
        si_units: typing.Optional[str] = m.group("si_units")
        units_node: typing.Optional[str] = m.group("units_node")

        low_tolerance: typing.Optional[float]
        if low_tolerancestr is None:
            low_tolerance = None
        else:
            try:
                low_tolerance = float(low_tolerancestr)
            except ValueError:
                return False                

        high_tolerance: typing.Optional[float]
        if high_tolerancestr is None:
            high_tolerance = None
        else:
            try:
                high_tolerance = float(high_tolerancestr)
            except ValueError:
                return False                

        # For convenience, convert the numeric part to int or float:
        #
        # TODO: go to this extra work only when requested?
        if numberstr is None:
            raise ValueError("Missing numeric part")
        n: str = numberstr.lower()
        number: typing.Union[float, int]
        if "." in n or ("e" in n and not n.startswith("0x")):
            number = float(n)
        else:
            number = int(n)

        if low_tolerancestr is not None or high_tolerancestr is not None or si_units is not None or units_node is not None:
            # We can be certain that this is a quantity.
            self.data_type = KgtkFormat.DataType.QUANTITY
        else:
            # We can be certain that this is a number
            self.data_type = KgtkFormat.DataType.NUMBER

        self.valid = True
        if self.parse_fields:
            self.fields = KgtkValueFields(data_type=self.data_type,
                                          valid=self.valid,
                                          numberstr=numberstr,
                                          number=number,
                                          low_tolerancestr=low_tolerancestr,
                                          low_tolerance=low_tolerance,
                                          high_tolerancestr=high_tolerancestr,
                                          high_tolerance=high_tolerance,
                                          si_units=si_units,
                                          units_node=units_node)
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
                self.numberstr = None
                return False

            if not validate:
                return True
            if self.valid is not None:
                return self.valid
        
        # Clear the number components:
        self.numberstr = None

        if not self._is_number_or_quantity():
            return False
        # We don't know yet if this is a number.  It could be a quantity.

        m: typing.Optional[typing.Match] = KgtkValue.number_re.match(self.value)
        if m is None:
            return False

        # Extract the number components:
        numberstr: str = m.group("number")

        # For convenience, convert the numeric part to int or float:
        #
        # TODO: go to this extra work only when requested?
        if numberstr is None:
            raise ValueError("Missing numeric part")
        n: str = numberstr.lower()
        number: typing.Union[float, int]
        if "." in n or ("e" in n and not n.startswith("0x")):
            number = float(n)
        else:
            number = int(n)

        # Now we can be certain that this is a number.
        self.data_type = KgtkFormat.DataType.NUMBER
        self.valid = True
        if self.parse_fields:
            self.fields = KgtkValueFields(data_type=self.data_type,
                                          valid=self.valid,
                                          numberstr=numberstr,
                                          number=number)
        return True
        
    
    def is_quantity(self, validate: bool=False)->bool:
        """
        Return True if the first character is 0-9,_,-,.
        and it is an enhanced quantity.
        """
        if self.data_type is not None:
            if self.data_type != KgtkFormat.DataType.QUANTITY:
                return False
            
            if not validate:
                return True
            if self.valid is not None:
                return self.valid
        
        if not self._is_number_or_quantity():
            return False
        # We don't know yet if this is a quantity.  It could be a number.

        m: typing.Optional[typing.Match]
        if self.options.allow_lax_qnodes:
            m = KgtkValue.lax_number_or_quantity_re.match(self.value)
        else:
            m = KgtkValue.number_or_quantity_re.match(self.value)
        if m is None:
            return False

        # Extract the quantity components:
        numberstr:str = m.group("number")
        low_tolerancestr:str = m.group("low_tolerance")
        high_tolerancestr:str = m.group("high_tolerance")
        si_units:str = m.group("si_units")
        units_node:str = m.group("units_node")

        low_tolerance: typing.Optional[float]
        if low_tolerancestr is None:
            low_tolerance = None
        else:
            try:
                low_tolerance = float(low_tolerancestr)
            except ValueError:
                return False                

        high_tolerance: typing.Optional[float]
        if high_tolerancestr is None:
            high_tolerance = None
        else:
            try:
                high_tolerance = float(high_tolerancestr)
            except ValueError:
                return False                

        # For convenience, convert the numeric part to int or float:
        #
        # TODO: go to this extra work only when requested?
        if numberstr is None:
            raise ValueError("Missing numeric part")
        n: str = numberstr.lower()
        number: typing.Union[float, int]
        if "." in n or ("e" in n and not n.startswith("0x")):
            number = float(n)
        else:
            number = int(n)

        if low_tolerancestr is None and high_tolerancestr is None and si_units is None and units_node is None:
            # This is a number, not a quantity
            self.data_type = KgtkFormat.DataType.NUMBER
            self.valid = True
            if self.parse_fields:
                self.fields = KgtkValueFields(data_type=self.data_type,
                                              valid=self.valid,
                                              numberstr=numberstr,
                                              number=number)
            return False

        # Now we can be certain that this is a quantity.
        self.data_type = KgtkFormat.DataType.QUANTITY
        self.valid = True
        if self.parse_fields:
            self.fields = KgtkValueFields(data_type=self.data_type,
                                          valid=self.valid,
                                          numberstr=numberstr,
                                          number=number,
                                          low_tolerancestr=low_tolerancestr,
                                          low_tolerance=low_tolerance,
                                          high_tolerancestr=high_tolerancestr,
                                          high_tolerance=high_tolerance,
                                          si_units=si_units,
                                          units_node=units_node)
        return True
    
    lax_string_re: typing.Pattern = re.compile(r'^"(?P<text>.*)"$')
    strict_string_re: typing.Pattern = re.compile(r'^"(?P<text>(?:[^"\\]|\\.)*)"$')

    def is_string(self, validate: bool = False)->bool:
        """
        Return True if the first character  is '"'.

        Strings begin and end with double quote (").  Any internal double
        quotes must be escaped with backslash (\").  Triple-double quoted
        strings are not supported by KGTK File Vormat v2.

        """
        if self.data_type is None:
            if not self.value.startswith('"'):
                return False
            # We are certain this is a string.  We don't yet know if it is valid.
            self.data_type = KgtkFormat.DataType.STRING
        else:
            if self.data_type != KgtkFormat.DataType.STRING:
                return False

        if not validate:
            return True
        if self.valid is not None:
            return self.valid
        
        # Validate the string:
        m: typing.Optional[typing.Match]
        if self.options.allow_lax_strings:
            m = KgtkValue.lax_string_re.match(self.value)
        else:
            m = KgtkValue.strict_string_re.match(self.value)
        if m is None:
            return False

        # We are certain that this is a valid string.
        self.valid = True
        if self.parse_fields:
            self.fields = KgtkValueFields(data_type=KgtkFormat.DataType.STRING,
                                          valid=self.valid,
                                          text=m.group("text"))
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
        if self.parse_fields:
            self.fields = KgtkValueFields(data_type=self.data_type,
                                          valid=self.valid,
                                          symbol=self.value,
            )
        return True

    def is_boolean(self, validate: bool = False)->bool:
        """
        Return True if the value matches one of the special boolean symbols.

        The validate parameter is ignored, we always validate.
        """
        if self.data_type is not None:
            return self.data_type == KgtkFormat.DataType.BOOLEAN

        # Is this a boolean?
        if self.value != KgtkFormat.TRUE_SYMBOL and self.value != KgtkFormat.FALSE_SYMBOL:
            return False
            
        # We are certain this is a valid boolean.
        self.data_type = KgtkFormat.DataType.BOOLEAN
        self.valid = True
        if self.parse_fields:
            self.fields = KgtkValueFields(data_type=self.data_type,
                                          valid=self.valid,
                                          truth=self.value == KgtkFormat.TRUE_SYMBOL)
        return True

    # Support two or three character language codes.  Suports hyphenated codes
    # with a country code or dialect name suffix after the language code.
    lax_language_qualified_string_re: typing.Pattern = re.compile(r"^'(?P<text>.*)'@(?P<lang_suffix>(?P<lang>[a-zA-Z]{2,3})(?P<suffix>-[a-zA-Z]+)?)$")
    strict_language_qualified_string_re: typing.Pattern = re.compile(r"^'(?P<text>(?:[^'\\]|\\.)*)'@(?P<lang_suffix>(?P<lang>[a-zA-Z]{2,3})(?P<suffix>-[a-zA-Z]+)?)$")

    def is_language_qualified_string(self, validate: bool=False)->bool:
        """
        Return True if the value looks like a language-qualified string.
        """
        if self.data_type is None:
            if not self.value.startswith("'"):
                return False
            # We are certain that this is a language qualified string, although we haven't checked validity.
            self.data_type = KgtkFormat.DataType.LANGUAGE_QUALIFIED_STRING
        else:
            if self.data_type != KgtkFormat.DataType.LANGUAGE_QUALIFIED_STRING:
                return False

        if not validate:
            return True
        if self.valid is not None:
            return self.valid
        
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

        # Extract the combined lang and suffix for use by the LanguageValidator.
        lang_and_suffix: str = m.group("lang_suffix")
        # print("lang_and_suffix: %s" % lang_and_suffix)

        # Validate the language code:
        if not LanguageValidator.validate(lang_and_suffix.lower(), options=self.options):
            # print("language validation failed for %s" % self.value)
            return False

        # We are certain that this is a valid language qualified string.
        self.valid = True
        if self.parse_fields:
            self.fields = KgtkValueFields(data_type=KgtkFormat.DataType.LANGUAGE_QUALIFIED_STRING,
                                          valid=self.valid,
                                          text=m.group("text"),
                                          language=m.group("lang"),
                                          language_suffix=m.group("suffix"))
        return True

    #location_coordinates_re: typing.Pattern = re.compile(r"^@(?P<lat>[-+]?\d{3}\.\d{5})/(?P<lon>[-+]?\d{3}\.\d{5})$")
    degrees_pat: str = r'(?:[-+]?(?:\d+(?:\.\d*)?)|(?:\.\d+))'
    location_coordinates_re: typing.Pattern = re.compile(r'^@(?P<lat>{degrees})/(?P<lon>{degrees})$'.format(degrees=degrees_pat))

    # The lax degrees pattern allows scientific notation, but not numbers iin
    # other bases or imaginary numbers.
    lax_degrees_pat: str = r'(?:{plus_or_minus}?(?:{integer}|{floatnumber}))'.format(plus_or_minus=plus_or_minus_pat,
                                                                                     integer=decinteger_pat,
                                                                                     floatnumber=floatnumber_pat)
    lax_location_coordinates_re: typing.Pattern = re.compile(r'^@(?P<lat>{degrees})/(?P<lon>{degrees})$'.format(degrees=lax_degrees_pat))

    def format_degrees(self, num: float)->str:
        return '{:011.6f}'.format(num)

    def is_location_coordinates(self, validate: bool=False)->bool:
        """
        Return False if this value is a list and idx is None.
        Otherwise, return True if the value looks like valid location coordinates.

        @043.26193/010.92708
        """
        if self.data_type is None:
            if not self.value.startswith("@"):
                return False
            # We are certain that this is location coordinates, although we haven't checked validity.
            self.data_type = KgtkFormat.DataType.LOCATION_COORDINATES
        else:
            if self.data_type != KgtkFormat.DataType.LOCATION_COORDINATES:
                return False

        if not validate:
            return True
        if self.valid is not None:
            return self.valid
        
        # Validate the location coordinates:
        rewrite_needed: bool = False
        m: typing.Optional[typing.Match] = KgtkValue.location_coordinates_re.match(self.value)
        if m is None:
            if self.options.allow_lax_coordinates or self.options.repair_lax_coordinates:
                m = KgtkValue.lax_location_coordinates_re.match(self.value)
                if m is None:
                    return False
                rewrite_needed = self.options.repair_lax_coordinates
            else:
                return False

        latstr: str = m.group("lat")
        lonstr: str = m.group("lon")

        fixup_needed: bool = False

        # Latitude normally runs from -90 to +90:
        #
        # TODO: Offer a wrapping repair for latitude, which will also affect latitude.
        try:
            lat: float = float(latstr)
            if  lat < self.options.minimum_valid_lat:
                if self.options.clamp_minimum_lat:
                    lat = self.options.minimum_valid_lat
                    latstr = str(lat)
                    fixup_needed = True
                else:
                    return False
            elif lat > self.options.maximum_valid_lat:
                if self.options.clamp_maximum_lat:
                    lat = self.options.maximum_valid_lat
                    latstr = str(lat)
                    fixup_needed = True
                else:
                    return False
            elif rewrite_needed:
                latstr = self.format_degrees(lat)
                fixup_needed = True
        except ValueError:
            return False

        # Longitude normally runs from -180 to +180:
        try:
            lon: float = float(lonstr)
            if  lon < self.options.minimum_valid_lon:
                if self.options.modulo_repair_lon:
                    lon = self.wrap_longitude(lon)
                    lonstr = str(lon)
                    fixup_needed = True
                elif self.options.clamp_minimum_lon:
                    lon = self.options.minimum_valid_lon
                    lonstr = str(lon)
                    fixup_needed = True
                else:
                    return False
            elif lon > self.options.maximum_valid_lon:
                if self.options.modulo_repair_lon:
                    lon = self.wrap_longitude(lon)
                    lonstr = str(lon)
                    fixup_needed = True
                elif self.options.clamp_maximum_lon:
                    lon = self.options.maximum_valid_lon
                    lonstr = str(lon)
                    fixup_needed = True
                else:
                    return False
            elif rewrite_needed:
                lonstr = self.format_degrees(lon)
                fixup_needed = True
        except ValueError:
            return False

        if fixup_needed:
            # Repair a location coordinates problem.
            self.update_location_coordinates(latstr, lonstr)

        # We are certain that this is valid.
        self.valid = True
        if self.parse_fields:
            self.fields = KgtkValueFields(data_type=KgtkFormat.DataType.LOCATION_COORDINATES,
                                          valid=self.valid,
                                          latitudestr=latstr,
                                          latitude=lat,
                                          longitudestr=lonstr,
                                          longitude=lon)
        return True

    def update_location_coordinates(self, latstr: str, lonstr: str):
        self.value = "@" + latstr + "/" + lonstr

        # If this value is the child of a list, repair the list parent value.
        if self.parent is not None:
            self.parent.rebuild_list()

    def wrap_longitude(self, lon: float)->float:
        # Result:
        # -360.0 <= longitude_reduced <=- 360.0
        # Credit: https://stackoverflow.com/questions/13368525/modulus-to-limit-latitude-and-longitude-values
        lon_reduced: float = math.fmod(lon, 360.0)

        if lon_reduced > 180.0:
                lon_reduced -= 360.0
        elif lon_reduced <= -180.0:
            lon_reduced += 360.0

        return lon_reduced

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
    month_pat: str = r'(?P<month>1[0-2]|0[1-9])'
    day_pat: str = r'(?P<day>3[01]|0[1-9]|[12][0-9])'
    date_pat: str = r'(?:{year}(?:(?P<hyphen>-)?{month}?(?:(?(hyphen)-){day})?)?)'.format(year=year_pat,
                                                                                          month=month_pat,
                                                                                          day=day_pat)

    lax_year_pat: str = r'(?P<year>[-+]?[0-9]{4}(?:[0-9]+(?=-))?)' # Extra digits must by followed by hyphen.
    lax_month_pat: str = r'(?P<month>1[0-2]|0[0-9])'
    lax_day_pat: str = r'(?P<day>3[01]|0[0-9]|[12][0-9])'
    lax_date_pat: str = r'(?P<date>(?:{year}(?:(?P<hyphen>-)?{month}?(?:(?(hyphen)-){day})?)?))'.format(year=lax_year_pat,
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

    time_pat: str = r'(?P<time>(?:{hour}(?:(?(hyphen):){minutes}(?:(?(hyphen):){seconds})?)?{zone}?))'.format(hour=hour_pat,
                                                                                                              minutes=minutes_pat,
                                                                                                              seconds=seconds_pat,
                                                                                                              zone=zone_pat)

    precision_pat: str = r'(?P<precision>[0-1]?[0-9])'

    lax_date_and_times_pat: str = r'(?:\^(?P<date_and_time>{date}(?:T{time})?)(?:/{precision})?)'.format(date=lax_date_pat,
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
        YYYY-
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
                return False
            # We are certain that this is location coordinates, although we haven't checked validity.
            self.data_type = KgtkFormat.DataType.DATE_AND_TIMES
        else:
            if self.data_type != KgtkFormat.DataType.DATE_AND_TIMES:
                return False

        if not validate:
            return True
        if self.valid is not None:
            return self.valid
        
        # Clear the cached date and times components:

        # Validate the date and times:
        m: typing.Optional[typing.Match] = KgtkValue.lax_date_and_times_re.match(self.value)
        if m is None:
            return False

        date: typing.Optional[str] = m.group("date")
        time: typing.Optional[str] = m.group("time")
        date_and_time: typing.Optional[str] = m.group("date_and_time")

        yearstr: typing.Optional[str] = m.group("year")
        monthstr: typing.Optional[str] = m.group("month")
        daystr: typing.Optional[str] = m.group("day")
        hourstr: typing.Optional[str] = m.group("hour")
        minutesstr: typing.Optional[str] = m.group("minutes")
        secondsstr: typing.Optional[str] = m.group("seconds")
        zonestr: typing.Optional[str] = m.group("zone")
        precisionstr: typing.Optional[str] = m.group("precision")
        iso8601extended: bool = m.group("hyphen") is not None

        fixup_needed: bool = False

        # Validate the year:
        if yearstr is None or len(yearstr) == 0:
            return False # Years are mandatory
        try:
            year: int = int(yearstr)
        except ValueError:
            return False
        if year < self.options.minimum_valid_year:
            if self.options.clamp_minimum_year:
                year = self.options.minimum_valid_year
                if year >= 0:
                    yearstr = str(year).zfill(4)
                else:
                    # Minus sign *and* at least 4 digits.
                    yearstr = str(year).zfill(5)
                fixup_needed = True
            else:
                return False
        elif year > self.options.maximum_valid_year:
            if self.options.clamp_maximum_year:
                year = self.options.maximum_valid_year
                if year >= 0:
                    yearstr = str(year).zfill(4)
                else:
                    # Minus sign *and* at least 4 digits.
                    yearstr = str(year).zfill(5)
                fixup_needed = True
            else:
                return False

        month: typing.Optional[int]
        if monthstr is None:
            month = None
        else:
            try:
                month = int(monthstr)
            except ValueError:
                return False # shouldn't happen
            if month == 0:
                if self.options.repair_month_or_day_zero:
                    month = 1
                    monthstr = "01"
                    fixup_needed = True
                elif not self.options.allow_month_or_day_zero:
                    return False # month 0 was disallowed.

        day: typing.Optional[int]
        if daystr is None:
            day = None
        else:
            try:
                day = int(daystr)
            except ValueError:
                return False # shouldn't happen
            if day == 0:
                if self.options.repair_month_or_day_zero:
                    day = 1
                    daystr = "01"
                    fixup_needed = True
                elif not self.options.allow_month_or_day_zero:
                    return False # day 0 was disallowed.

        # Convert the time fields to ints:
        hour: typing.Optional[int]
        if hourstr is None:
            hour = None
        else:
            try:
                hour = int(hourstr)
            except ValueError:
                return False # shouldn't happen

        minutes: typing.Optional[int]
        if minutesstr is None:
            minutes = None
        else:
            try:
                minutes = int(minutesstr)
            except ValueError:
                return False # shouldn't happen

        seconds: typing.Optional[int]
        if secondsstr is None:
            seconds = None
        else:
            try:
                seconds = int(secondsstr)
            except ValueError:
                return False # shouldn't happen

        precision: typing.Optional[int]
        if precisionstr is None:
            precision = None
        else:
            try:
                precision = int(precisionstr)
            except ValueError:
                return False # shouldn't happen

        if fixup_needed:
            # Repair a month or day zero problem.
            self.update_date_and_times(yearstr, monthstr, daystr, hourstr, minutesstr, secondsstr, zonestr, precisionstr, iso8601extended)

        # We are fairly certain that this is a valid date and times.
        self.valid = True
        if self.parse_fields:
            self.fields = KgtkValueFields(data_type=KgtkFormat.DataType.DATE_AND_TIMES,
                                          valid=self.valid,
                                          date=date,
                                          time=time,
                                          date_and_time=date_and_time,
                                          yearstr=yearstr,
                                          monthstr=monthstr,
                                          daystr=daystr,
                                          hourstr=hourstr,
                                          minutesstr=minutesstr,
                                          secondsstr=secondsstr,
                                          year=year,
                                          month=month,
                                          day=day,
                                          hour=hour,
                                          minutes=minutes,
                                          seconds=seconds,
                                          zonestr=zonestr,
                                          precisionstr=precisionstr,
                                          precision=precision,
                                          iso8601extended=iso8601extended,
            )
        return True

    def update_date_and_times(self,
                              yearstr: str,
                              monthstr: typing.Optional[str],
                              daystr: typing.Optional[str],
                              hourstr: typing.Optional[str],
                              minutesstr: typing.Optional[str],
                              secondsstr: typing.Optional[str],
                              zonestr: typing.Optional[str],
                              precisionstr: typing.Optional[str],
                              iso8601extended: bool):
        v: str = "^" + yearstr
        if monthstr is not None:
            if iso8601extended:
                v += "-"
            v += monthstr
        if daystr is not None:
            if iso8601extended:
                v += "-"
            v += daystr
        if hourstr is not None:
            v += "T"
            v += hourstr
        if minutesstr is not None:
            if iso8601extended:
                v += ":"
            v += minutesstr
        if secondsstr is not None:
            if iso8601extended:
                v += ":"
            v += secondsstr
        if zonestr is not None:
            v += zonestr
        if precisionstr is not None:
            v += "/"
            v += precisionstr
        self.value = v
        self.repaired = True

        # If this value is the child of a list, repair the list parent value.
        if self.parent is not None:
            self.parent.rebuild_list()

    def is_extension(self, validate=False)->bool:
        """Return True if the first character is !

        Although we refer to the validate parameter in the code below, we
        force self.valid to False.

        """
        if self.data_type is None:
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
        self.fields = None
        return self.classify()

    def validate(self)->bool:
        # Validate this KgtkValue.

        # Start by classifying the KgtkValue.
        dt: KgtkFormat.DataType = self.classify()

        # If the valid flag has already been cached, return that.
        if self.valid is not None:
            return self.valid

        # Clear any fields from prior validation:
        self.fields = None
        
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
        self.fields = None
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
            return "Language Qualified String" if self.is_language_qualified_string(validate=True) else "Invalid Language Qualified String"
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

    def get_field_map(self)->typing.Mapping[str, typing.Union[str, int, float, bool]]:
        if self.fields is None:
            return { }
        else:
            return self.fields.to_map()

def main():
    """
    Test the KGTK value parser.
    """
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument(dest="values", help="The values(s) to test", type=str, nargs="+")
    parser.add_argument("-p", "--parse-fields", dest="parse_fields", help="Print additional progress messages.", action='store_true')
    parser.add_argument("-v", "--verbose", dest="verbose", help="Print additional progress messages.", action='store_true')
    parser.add_argument(      "--very-verbose", dest="very_verbose", help="Print additional progress messages.", action='store_true')
    KgtkValueOptions.add_arguments(parser)
    args: Namespace = parser.parse_args()

    # Build the value parsing option structure.
    value_options: KgtkValueOptions = KgtkValueOptions.from_args(args)

    value: str
    for value in args.values:
        kv: KgtkValue = KgtkValue(value, options=value_options, parse_fields=args.parse_fields)
        kv.validate()
        if value == kv.value:
            print("%s: %s" % (value, kv.describe()), flush=True)
        else:
            print("%s => %s: %s" % (value, kv.value, kv.describe()), flush=True)

        if args.verbose:
            fields: typing.Mapping[str, typing.Any] = kv.get_field_map()
            for key in sorted(fields.keys()):
                print("%s: %s" % (key, str(fields[key])))
            list_items: typing.List[KgtkValue] = kv.get_list_items()
            item: KghtValue
            for item in list_items:
                print("...")
                fields = item.get_fields()
                for key in sorted(fields.keys()):
                    print("... %s: %s" % (key, str(fields[key])))
                

if __name__ == "__main__":
    main()
