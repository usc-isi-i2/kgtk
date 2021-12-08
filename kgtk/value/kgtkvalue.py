"""
Validate KGTK File data types.
"""

from argparse import ArgumentParser, Namespace
import attr
import datetime as dt
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
    # String contents without the enclosing quotes.  Backslash quoted sequences remain unprocessed.
    text: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)

    # String contents without the enclosing quotes.  Backslash quoted sequences have been procesed..
    decoded_text: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)

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

    DATA_TYPE_FIELD_NAME: str = "data_type"
    DATE_AND_TIMES_FIELD_NAME: str = "date_and_time"
    DECODED_TEXT_FIELD_NAME: str = "decoded_text"
    HIGH_TOLERANCE_FIELD_NAME: str = "high_tolerance"
    LANGUAGE_FIELD_NAME: str = "language"
    LANGUAGE_SUFFIX_FIELD_NAME: str = "language_suffix"
    LATITUDE_FIELD_NAME: str = "latitude"
    LIST_LEN_FIELD_NAME: str = "list_len"
    LONGITUDE_FIELD_NAME: str = "longitude"
    LOW_TOLERANCE_FIELD_NAME: str = "low_tolerance"
    NUMBER_FIELD_NAME: str = "number"
    PRECISION_FIELD_NAME: str = "precision"
    SI_UNITS_FIELD_NAME: str = "si_units"
    SYMBOL_FIELD_NAME: str = "symbol"
    TEXT_FIELD_NAME: str = "text"
    TRUTH_FIELD_NAME: str = "truth"
    UNITS_NODE_FIELD_NAME: str = "units_node"
    VALID_FIELD_NAME: str = "valid"

    FIELD_NAMES: typing.List[str] = [
        LIST_LEN_FIELD_NAME,
        DATA_TYPE_FIELD_NAME,
        VALID_FIELD_NAME,
        TEXT_FIELD_NAME,
        DECODED_TEXT_FIELD_NAME,
        LANGUAGE_FIELD_NAME,
        LANGUAGE_SUFFIX_FIELD_NAME,
        "numberstr",
        NUMBER_FIELD_NAME,
        "low_tolerancestr",
        LOW_TOLERANCE_FIELD_NAME,
        "high_tolerancestr",
        HIGH_TOLERANCE_FIELD_NAME,
        SI_UNITS_FIELD_NAME,
        UNITS_NODE_FIELD_NAME,
        "latitudestr",
        LATITUDE_FIELD_NAME,
        "longitudestr",
        LONGITUDE_FIELD_NAME,
        "date",
        "time",
        DATE_AND_TIMES_FIELD_NAME,
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
        PRECISION_FIELD_NAME,
        "iso8601extended",
        TRUTH_FIELD_NAME,
        SYMBOL_FIELD_NAME
        ]

    DEFAULT_FIELD_NAMES: typing.List[str] = [
        DATA_TYPE_FIELD_NAME,
        VALID_FIELD_NAME,
        LIST_LEN_FIELD_NAME,
        TEXT_FIELD_NAME,
        LANGUAGE_FIELD_NAME,
        LANGUAGE_SUFFIX_FIELD_NAME,
        NUMBER_FIELD_NAME,
        LOW_TOLERANCE_FIELD_NAME,
        HIGH_TOLERANCE_FIELD_NAME,
        SI_UNITS_FIELD_NAME,
        UNITS_NODE_FIELD_NAME,
        LATITUDE_FIELD_NAME,
        LONGITUDE_FIELD_NAME,
        DATE_AND_TIMES_FIELD_NAME,
        PRECISION_FIELD_NAME,
        TRUTH_FIELD_NAME,
        SYMBOL_FIELD_NAME
        ]

    OPTIONAL_DEFAULT_FIELD_NAMES: typing.List[str] = [
        LANGUAGE_SUFFIX_FIELD_NAME,
        LOW_TOLERANCE_FIELD_NAME,
        HIGH_TOLERANCE_FIELD_NAME,
        SI_UNITS_FIELD_NAME,
        UNITS_NODE_FIELD_NAME,
        PRECISION_FIELD_NAME,
        ]

    FIELD_NAME_FORMATS: typing.Mapping[str, str] = {
        LIST_LEN_FIELD_NAME: "int",
        DATA_TYPE_FIELD_NAME: "sym",
        VALID_FIELD_NAME: "bool",
        TEXT_FIELD_NAME: "str",
        DECODED_TEXT_FIELD_NAME: "str",
        LANGUAGE_FIELD_NAME: "sym",
        LANGUAGE_SUFFIX_FIELD_NAME: "sym",
        "numberstr": "str",
        NUMBER_FIELD_NAME: "num",
        "low_tolerancestr": "str",
        LOW_TOLERANCE_FIELD_NAME: "num",
        "high_tolerancestr": "str",
        HIGH_TOLERANCE_FIELD_NAME: "num",
        SI_UNITS_FIELD_NAME: "sym",
        UNITS_NODE_FIELD_NAME: "sym",
        "latitudestr": "str",
        LATITUDE_FIELD_NAME: "num",
        "longitudestr": "str",
        LONGITUDE_FIELD_NAME: "num",
        "date": "str",
        "time": "str",
        DATE_AND_TIMES_FIELD_NAME: "str",
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
        PRECISION_FIELD_NAME: "int",
        "iso8601extended": "bool",
        TRUTH_FIELD_NAME: "bool",
        SYMBOL_FIELD_NAME: "sym",
    }

    DATA_TYPE_FIELDS: typing.Mapping[str, typing.List[str]] = {
        KgtkFormat.DataType.EMPTY.lower(): [ DATA_TYPE_FIELD_NAME, VALID_FIELD_NAME ],
        KgtkFormat.DataType.LIST.lower(): [ DATA_TYPE_FIELD_NAME, VALID_FIELD_NAME, LIST_LEN_FIELD_NAME ],
        KgtkFormat.DataType.NUMBER.lower(): [ DATA_TYPE_FIELD_NAME, VALID_FIELD_NAME, "numberstr", NUMBER_FIELD_NAME ],
        KgtkFormat.DataType.QUANTITY.lower(): [ DATA_TYPE_FIELD_NAME, VALID_FIELD_NAME,
                                                "numberstr", NUMBER_FIELD_NAME,
                                                "low_tolerancestr", LOW_TOLERANCE_FIELD_NAME,
                                                "high_tolerancestr", HIGH_TOLERANCE_FIELD_NAME,
                                                SI_UNITS_FIELD_NAME, UNITS_NODE_FIELD_NAME,
        ],
        KgtkFormat.DataType.STRING.lower(): [ DATA_TYPE_FIELD_NAME, VALID_FIELD_NAME, TEXT_FIELD_NAME ],
        KgtkFormat.DataType.LANGUAGE_QUALIFIED_STRING.lower(): [ DATA_TYPE_FIELD_NAME, VALID_FIELD_NAME, TEXT_FIELD_NAME, LANGUAGE_FIELD_NAME, LANGUAGE_SUFFIX_FIELD_NAME ],
        KgtkFormat.DataType.LOCATION_COORDINATES.lower(): [ DATA_TYPE_FIELD_NAME, VALID_FIELD_NAME,
                                                            "latitudestr", LATITUDE_FIELD_NAME,
                                                            "longitudestr", LONGITUDE_FIELD_NAME,
        ],
        KgtkFormat.DataType.DATE_AND_TIMES.lower(): [ DATA_TYPE_FIELD_NAME, VALID_FIELD_NAME,
                                                      DATE_AND_TIMES_FIELD_NAME,
                                                      "date", "time",
                                                      "yearstr", "year",
                                                      "monthstr", "month",
                                                      "daystr", "day",
                                                      "hourstr", "hour",
                                                      "minutesstr", "minutes",
                                                      "secondsstr", "seconds",
                                                      "zonestr",
                                                      "precisionstr", PRECISION_FIELD_NAME,
                                                      "iso8601extended",
        ],
        KgtkFormat.DataType.EXTENSION.lower(): [ ],
        KgtkFormat.DataType.BOOLEAN.lower(): [ DATA_TYPE_FIELD_NAME, VALID_FIELD_NAME, TRUTH_FIELD_NAME ],
        KgtkFormat.DataType.SYMBOL.lower(): [ DATA_TYPE_FIELD_NAME, VALID_FIELD_NAME, SYMBOL_FIELD_NAME ],
    }

    DEFAULT_DATA_TYPE_FIELDS: typing.Mapping[str, typing.List[str]] = {
        KgtkFormat.DataType.EMPTY.lower(): [ DATA_TYPE_FIELD_NAME, VALID_FIELD_NAME ],
        KgtkFormat.DataType.LIST.lower(): [ DATA_TYPE_FIELD_NAME, VALID_FIELD_NAME, LIST_LEN_FIELD_NAME ],
        KgtkFormat.DataType.NUMBER.lower(): [ DATA_TYPE_FIELD_NAME, VALID_FIELD_NAME, NUMBER_FIELD_NAME ],
        KgtkFormat.DataType.QUANTITY.lower(): [ DATA_TYPE_FIELD_NAME, VALID_FIELD_NAME,
                                                NUMBER_FIELD_NAME,
                                                LOW_TOLERANCE_FIELD_NAME,
                                                HIGH_TOLERANCE_FIELD_NAME,
                                                SI_UNITS_FIELD_NAME,
                                                UNITS_NODE_FIELD_NAME,
        ],
        KgtkFormat.DataType.STRING.lower(): [ DATA_TYPE_FIELD_NAME, VALID_FIELD_NAME, TEXT_FIELD_NAME ],
        KgtkFormat.DataType.LANGUAGE_QUALIFIED_STRING.lower(): [ DATA_TYPE_FIELD_NAME, VALID_FIELD_NAME, TEXT_FIELD_NAME, LANGUAGE_FIELD_NAME, LANGUAGE_SUFFIX_FIELD_NAME ],
        KgtkFormat.DataType.LOCATION_COORDINATES.lower(): [ DATA_TYPE_FIELD_NAME, VALID_FIELD_NAME,
                                                            LATITUDE_FIELD_NAME,
                                                            LONGITUDE_FIELD_NAME,
        ],
        KgtkFormat.DataType.DATE_AND_TIMES.lower(): [ DATA_TYPE_FIELD_NAME, VALID_FIELD_NAME,
                                                      DATE_AND_TIMES_FIELD_NAME,
                                                      PRECISION_FIELD_NAME,
        ],
        KgtkFormat.DataType.EXTENSION.lower(): [ ],
        KgtkFormat.DataType.BOOLEAN.lower(): [ DATA_TYPE_FIELD_NAME, VALID_FIELD_NAME, TRUTH_FIELD_NAME ],
        KgtkFormat.DataType.SYMBOL.lower(): [ DATA_TYPE_FIELD_NAME, VALID_FIELD_NAME, SYMBOL_FIELD_NAME ],
    }

    def to_map(self)->typing.Mapping[str, typing.Union[str, int, float, bool]]:
        results: typing.MutableMapping[str, typing.Union[str, int, float, bool]] = { }
        results[self.LIST_LEN_FIELD_NAME] = self.list_len
        if self.data_type is not None:
            results[self.DATA_TYPE_FIELD_NAME] = self.data_type.name.lower()
        if self.valid is not None:
            results[self.VALID_FIELD_NAME] = self.valid
        if self.text is not None:
            results[self.TEXT_FIELD_NAME] = self.text
        if self.decoded_text is not None:
            results[self.DECODED_TEXT_FIELD_NAME] = self.decoded_text
        if self.language is not None:
            results[self.LANGUAGE_FIELD_NAME] = self.language
        if self.language_suffix is not None:
            results[self.LANGUAGE_SUFFIX_FIELD_NAME] = self.language_suffix
        if self.numberstr is not None:
            results["numberstr"] = self.numberstr
        if self.number is not None:
            results[self.NUMBER_FIELD_NAME] = self.number
        if self.low_tolerancestr is not None:
            results["low_tolerancestr"] = self.low_tolerancestr
        if self.low_tolerance is not None:
            results[self.LOW_TOLERANCE_FIELD_NAME] = self.low_tolerance
        if self.high_tolerancestr is not None:
            results["high_tolerancestr"] = self.high_tolerancestr
        if self.high_tolerance is not None:
            results[self.HIGH_TOLERANCE_FIELD_NAME] = self.high_tolerance
        if self.si_units is not None:
            results[self.SI_UNITS_FIELD_NAME] = self.si_units
        if self.units_node is not None:
            results[self.UNITS_NODE_FIELD_NAME] = self.units_node
        if self.latitudestr is not None:
            results["latitudestr"] = self.latitudestr
        if self.latitude is not None:
            results[self.LATITUDE_FIELD_NAME] = self.latitude
        if self.longitudestr is not None:
            results["longitudestr"] = self.longitudestr
        if self.longitude is not None:
            results[self.LONGITUDE_FIELD_NAME] = self.longitude
        if self.date is not None:
            results["date"] = self.date
        if self.time is not None:
            results["time"] = self.time
        if self.date_and_time is not None:
            results[self.DATE_AND_TIMES_FIELD_NAME] = self.date_and_time
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
            results[self.PRECISION_FIELD_NAME] = self.precision
        if self.iso8601extended is not None:
            results["iso8601extended"] = self.iso8601extended
        if self.truth is not None:
            results[self.TRUTH_FIELD_NAME] = self.truth
        if self.symbol is not None:
            results[self.SYMBOL_FIELD_NAME] = self.symbol
        return results
    
@attr.s(slots=True, frozen=False)
class KgtkValue(KgtkFormat):
    value: str = attr.ib(validator=attr.validators.instance_of(str))
    options: KgtkValueOptions = attr.ib(validator=attr.validators.instance_of(KgtkValueOptions), default=DEFAULT_KGTK_VALUE_OPTIONS)
    parse_fields: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    error_file: typing.TextIO = attr.ib(default=sys.stderr)
    verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

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

    def is_empty(self, validate: bool = False, parse_fields: bool = False)->bool:
        # Is this an empty item?  If so, assume it is valid and ignore the
        # validate parameter.
        if self.data_type is not None:
            result = self.data_type == KgtkFormat.DataType.EMPTY
            # self.valid *must* be true by now. TODO: we should check.
            if self.fields is None and parse_fields and self.valid:
                self.fields = KgtkValueFields(data_type=self.data_type, valid=self.valid)
            return result

        # Clear any fields from prior validation:
        self.fields = None

        if len(self.value) != 0:
            return False

        # We are certain that this is an empty value.  We can be certain it is valid.
        self.data_type = KgtkFormat.DataType.EMPTY
        self.valid = True
        if parse_fields or self.parse_fields:
            self.fields = KgtkValueFields(data_type=self.data_type, valid=self.valid)
        return True

    # Split on a "|" that is not preceeded by "\".  This is not completely
    # correct:  we want to split on any "|" that is not preceeded by an odd
    # number of "\".
    #
    # TODO: Find a better splitting pattern.
    #
    # Consider: re.findall, or regex.split
    #
    # On the other hand: if "\" were disallowed form symbol, then the current
    # pattern will be OK.
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
                lv1: typing.List[str] = cls.split_list(value1)
                lv1.extend(cls.split_list(value2))
                return cls.join_unique_list(lv1)
            else:
                # This is rather expensive, but will work correctly:
                lv2: typing.List[str] = cls.split_list(value1)
                lv2.append(value2)
                return cls.join_unique_list(lv2)
        if KgtkFormat.LIST_SEPARATOR in value2:
            # This is rather expensive, but will work correctly:
            lv3: typing.List[str] = cls.split_list(value2)
            lv3.append(value1)
            return cls.join_unique_list(lv3)
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

    def is_list(self, validate: bool = False, parse_fields: bool = False)->bool:
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
        if parse_fields or self.parse_fields:
            self.fields = KgtkValueFields(data_type=KgtkFormat.DataType.LIST,
                                          valid=False,
                                          list_len=len(self.get_list_items()))

        # Validate the list.
        item: 'KgtkValue'
        for item in self.get_list_items():
            if not item.is_valid():
                # The list is invalid if any item in the list is invalid.
                self.valid = False
                if self.verbose:
                    print("KgtkValue.is_list: invalid list item %s in %s" % (repr(item), repr(self.value)),
                          file=self.error_file, flush=True)
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

    # Real literals (nothing imaginary).
    real_pat: str = r'(?:{plus_or_minus}?(?:{integer}|{floatnumber}))'.format(plus_or_minus=plus_or_minus_pat,
                                                                              integer=integer_pat,
                                                                              floatnumber=floatnumber_pat)

    # Imaginary literals.
    imagnumber_pat: str = r'(?:{floatnumber}|{digitpart})[jJ]'.format(floatnumber=floatnumber_pat,
                                                                      digitpart=digitpart_pat)

    # Numeric literals.
    numeric_pat: str = r'(?:{plus_or_minus}?(?:{integer}|{floatnumber}|{imagnumber}))'.format(plus_or_minus=plus_or_minus_pat,
                                                                                              integer=integer_pat,
                                                                                              floatnumber=floatnumber_pat,
                                                                                              imagnumber=imagnumber_pat)

    # TODO: We may wish to exclude imaginary numbers in some circumstances.

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
    # 30-Jun-2020: Amandeep requested underscore and increased laxness for
    # datamart.
    
    #lax_units_node_pat: str = r'(?P<units_node>Q[0-9A-Za-z][-0-9A-Za-z]*)'
    lax_units_node_pat: str = r'(?P<units_node>Q[-_0-9A-Za-z]+)'
    

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

    def is_number_or_quantity(self, validate: bool=False, parse_fields: bool  = False)->bool:
        """
        Return True if the first character is 0-9,_,-,.
        and it is either a Python-compatible number or an enhanced
        quantity.
        """
        # If we know the specific data type, delegate the test to that data type.
        if self.data_type is not None:
            if self.data_type == KgtkFormat.DataType.NUMBER:
                return self.is_number(validate=validate, parse_fields=parse_fields)
            elif self.data_type == KgtkFormat.DataType.QUANTITY:
                return self.is_quantity(validate=validate, parse_fields=parse_fields)
            else:
                return False # Not a number or quantity.

        if not self._is_number_or_quantity():
            return False

        if not validate:
            return True

        # Clear any fields from prior validation:
        self.fields = None

        # We cannot cache the result of this test because it would interfere
        # if we later determined the exact data type.  We could work around
        # this problem with more thought.
        m: typing.Optional[typing.Match]
        if self.options.allow_lax_qnodes:
            m = KgtkValue.lax_number_or_quantity_re.match(self.value)
        else:
            m = KgtkValue.number_or_quantity_re.match(self.value)
            
        if m is None:
            if self.verbose:
                if self.options.allow_lax_qnodes:
                    print("KgtkValue.is_number_or_quantity.lax_number_or_quantity_re.match failed for %s" % (repr(self.value)),
                          file=self.error_file, flush=True)
                else:
                    print("KgtkValue.is_number_or_quantity.number_or_quantity_re.match failed for %s" % (repr(self.value)),
                          file=self.error_file, flush=True)
            self.valid = False
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
                if self.verbose:
                    print("KgtkValue.is_number_or_quantity: low tolerance is not float for %s" % (repr(self.value)),
                          file=self.error_file, flush=True)
                self.valid = False
                return False                

        high_tolerance: typing.Optional[float]
        if high_tolerancestr is None:
            high_tolerance = None
        else:
            try:
                high_tolerance = float(high_tolerancestr)
            except ValueError:
                if self.verbose:
                    print("KgtkValue.is_number_or_quantity: high tolerance is not float for %s" % (repr(self.value)),
                          file=self.error_file, flush=True)
                self.valid = False
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
        if parse_fields or self.parse_fields:
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
    
    def is_number(self, validate: bool=False, quiet: bool=False, parse_fields: bool = False)->bool:
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

            if not validate:
                return True
            if self.valid is not None:
                if not self.valid:
                    return False

                if not (self.fields is None and parse_fields):
                    return True

        # Clear any fields from prior validation:
        self.fields = None

        if not self._is_number_or_quantity():
            return False
        # We don't know yet if this is a number.  It could be a quantity.

        m: typing.Optional[typing.Match] = KgtkValue.number_re.match(self.value)
        if m is None:
            if self.verbose and not quiet:
                print("KgtkValue.number_re.match failed for %s" % (repr(self.value)),
                      file=self.error_file, flush=True)
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
        if parse_fields or self.parse_fields:
            self.fields = KgtkValueFields(data_type=self.data_type,
                                          valid=self.valid,
                                          numberstr=numberstr,
                                          number=number)
        return True
        
    
    def is_quantity(self, validate: bool=False, parse_fields: bool = False)->bool:
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
                if not self.valid:
                    return False

                if not (self.fields is None and parse_fields):
                    return True
        

        # Clear any fields from prior validation:
        self.fields = None

        if not self._is_number_or_quantity():
            return False
        # We don't know yet if this is a quantity.  It could be a number.

        m: typing.Optional[typing.Match]
        if self.options.allow_lax_qnodes:
            m = KgtkValue.lax_number_or_quantity_re.match(self.value)
        else:
            m = KgtkValue.number_or_quantity_re.match(self.value)
        if m is None:
            if self.verbose:
                if self.options.allow_lax_qnodes:
                    print("KgtkValue.is_number.lax_number_or_quantity_re.match failed for %s" % (repr(self.value)),
                          file=self.error_file, flush=True)
                else:
                    print("KgtkValue.is_number.number_or_quantity_re.match failed for %s" % (repr(self.value)),
                          file=self.error_file, flush=True)
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
                if self.verbose:
                    print("KgtkValue.is_quantity: low tolerance is not float for %s" % (repr(self.value)),
                          file=self.error_file, flush=True)
                self.valid = False
                return False                

        high_tolerance: typing.Optional[float]
        if high_tolerancestr is None:
            high_tolerance = None
        else:
            try:
                high_tolerance = float(high_tolerancestr)
            except ValueError:
                if self.verbose:
                    print("KgtkValue.is_quantity: high tolerance is not float for %s" % (repr(self.value)),
                          file=self.error_file, flush=True)
                self.valid = False
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
            if parse_fields or self.parse_fields:
                self.fields = KgtkValueFields(data_type=self.data_type,
                                              valid=self.valid,
                                              numberstr=numberstr,
                                              number=number)
            if self.verbose:
                print("KgtkValue.is_quantity: actually a number for %s" % (repr(self.value)),
                      file=self.error_file, flush=True)
            self.valid = False
            return False

        # Now we can be certain that this is a quantity.
        self.data_type = KgtkFormat.DataType.QUANTITY
        self.valid = True
        if parse_fields or self.parse_fields:
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

    def is_string(self, validate: bool = False, parse_fields: bool = False)->bool:
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
            if not self.valid:
                return False

            if not (self.fields is None and parse_fields):
                return True
        
        # Clear any fields from prior validation:
        self.fields = None

        # Validate the string:
        m: typing.Optional[typing.Match]
        if self.options.allow_lax_strings:
            m = KgtkValue.lax_string_re.match(self.value)
        else:
            m = KgtkValue.strict_string_re.match(self.value)
        if m is None:
            if self.verbose:
                if self.options.allow_lax_strings:
                    print("KgtkValue.lax_string_re.match failed for %s" % self.value, file=self.error_file, flush=True)
                else:
                    print("KgtkValue.strict_string_re.match failed for %s" % self.value, file=self.error_file, flush=True)
            self.valid = False
            return False

        # We are certain that this is a valid string.
        self.valid = True
        if parse_fields or self.parse_fields:
            self.fields = KgtkValueFields(data_type=KgtkFormat.DataType.STRING,
                                          valid=self.valid,
                                          text=m.group("text"),
                                          decoded_text=KgtkFormat.unstringify('"' + m.group("text") + '"'))
        return True

    def is_structured_literal(self)->bool:
        """
        Return True if the first character  is ^@'!.
        """
        return self.value.startswith(("^", "@", "'", "!"))

    def is_symbol(self, validate: bool = False, parse_fields: bool = False)->bool:
        """
        Return True if not a number, string, nor structured literal, nor boolean.

        The validate parameter is ignored.
        """
        if self.data_type is not None:
            if self.data_type != KgtkFormat.DataType.SYMBOL:
                return False

            if not validate:
                return True
            if self.valid is not None:
                if not self.valid:
                    return False

                if not (self.fields is None and parse_fields):
                    return True
                
        # Clear any fields from prior validation:
        self.fields = None

        # Is this a symbol?  It is, if it is not something else.
        if self.is_number_or_quantity() or self.is_string() or self.is_structured_literal() or self.is_boolean():
            return False
            
        # We are certain this is a symbol.  We assume that it is valid.
        self.data_type = KgtkFormat.DataType.SYMBOL
        self.valid = True
        if parse_fields or self.parse_fields:
            self.fields = KgtkValueFields(data_type=self.data_type,
                                          valid=self.valid,
                                          symbol=self.value,
            )
        return True

    def is_boolean(self, validate: bool = False, parse_fields: bool = False)->bool:
        """
        Return True if the value matches one of the special boolean symbols.

        The validate parameter is ignored, we always validate.
        """
        if self.data_type is not None:
            if self.data_type != KgtkFormat.DataType.BOOLEAN:
                return False

            if not validate:
                return True
            if self.valid is not None:
                if not self.valid:
                    return False

                if not (self.fields is None and parse_fields):
                    return True
                
        # Clear any fields from prior validation:
        self.fields = None

        # Is this a boolean?
        if self.value != KgtkFormat.TRUE_SYMBOL and self.value != KgtkFormat.FALSE_SYMBOL:
            return False
            
        # We are certain this is a valid boolean.
        self.data_type = KgtkFormat.DataType.BOOLEAN
        self.valid = True
        if parse_fields or self.parse_fields:
            self.fields = KgtkValueFields(data_type=self.data_type,
                                          valid=self.valid,
                                          truth=self.value == KgtkFormat.TRUE_SYMBOL)
        return True

    def is_true(self)->bool:
        """
        Return True if the value is the boolean truth symbol.
        """
        return self.value == KgtkFormat.TRUE_SYMBOL

    def is_false(self)->bool:
        """
        Return True if the value is the boolean false symbol.
        """
        return self.value == KgtkFormat.FALSE_SYMBOL

    @classmethod
    def to_boolean(cls, b: bool)->str:
        return KgtkFormat.TRUE_SYMBOL if b else KgtkFormat.FALSE_SYMBOL

    # Support two or three character language codes.  Suports hyphenated codes
    # with a country code or dialect name suffix after the language code.
    lax_language_qualified_string_re: typing.Pattern = re.compile(r"^'(?P<text>.*)'@(?P<lang_suffix>(?P<lang>[a-zA-Z]{2,3})(?P<suffix>-[a-zA-Z0-9]+)?)$")
    strict_language_qualified_string_re: typing.Pattern = re.compile(r"^'(?P<text>(?:[^'\\]|\\.)*)'@(?P<lang_suffix>(?P<lang>[a-zA-Z]{2,3})(?P<suffix>-[a-zA-Z0-9]+)?)$")
    wikidata_language_qualified_string_re: typing.Pattern = re.compile(r"^'(?P<text>(?:[^'\\]|\\.)*)'@(?P<lang_suffix>(?P<lang>[a-zA-Z]{2,})(?P<suffix>-[-a-zA-Z0-9]+)?)$")

    def is_language_qualified_string(self, validate: bool=False, parse_fields: bool = False)->bool:
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
            if not self.valid:
                return False

            if not (self.fields is None and parse_fields):
                return True
        
        # Clear any fields from prior validation:
        self.fields = None

        # Validate the language qualified string.
        # print("checking %s" % self.value)
        m: typing.Optional[typing.Match]
        if self.options.allow_wikidata_lq_strings:
            m = KgtkValue.wikidata_language_qualified_string_re.match(self.value)
        elif self.options.allow_lax_lq_strings:
            m = KgtkValue.lax_language_qualified_string_re.match(self.value)
        else:
            m = KgtkValue.strict_language_qualified_string_re.match(self.value)
        if m is None:
            if self.verbose:
                if self.options.allow_wikidata_lq_strings:
                    print("KgtkValue.wikidata_language_qualified_string_re.match failed for %s" % self.value, file=self.error_file, flush=True)
                elif self.options.allow_lax_lq_strings:
                    print("KgtkValue.lax_language_qualified_string_re.match failed for %s" % self.value, file=self.error_file, flush=True)
                else:
                    print("KgtkValue.strict_language_qualified_string_re.match failed for %s" % self.value, file=self.error_file, flush=True)
            self.valid = False
            return False

        # Extract the combined lang and suffix for use by the LanguageValidator.
        lang_and_suffix: str = m.group("lang_suffix")
        # print("lang_and_suffix: %s" % lang_and_suffix)

        # Validate the language code:
        if not self.options.allow_wikidata_lq_strings and not LanguageValidator.validate(lang_and_suffix.lower(), options=self.options):
            if self.verbose:
                print("language validation failed for %s" % self.value, file=self.error_file, flush=True)
            self.valid = False
            return False

        # We are certain that this is a valid language qualified string.
        self.valid = True
        if parse_fields or self.parse_fields:
            self.fields = KgtkValueFields(data_type=KgtkFormat.DataType.LANGUAGE_QUALIFIED_STRING,
                                          valid=self.valid,
                                          text=m.group("text"),
                                          decoded_text=KgtkFormat.unstringify(self.value),
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

    def is_location_coordinates(self, validate: bool=False, parse_fields: bool = False)->bool:
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
            if not self.valid:
                return False

            if not (self.fields is None and parse_fields):
                return True
        
        # Clear any fields from prior validation:
        self.fields = None

        # Validate the location coordinates:
        rewrite_needed: bool = False
        m: typing.Optional[typing.Match] = KgtkValue.location_coordinates_re.match(self.value)
        if m is None:
            if self.options.allow_lax_coordinates or self.options.repair_lax_coordinates:
                m = KgtkValue.lax_location_coordinates_re.match(self.value)
                if m is None:
                    if self.verbose:
                        print("KgtkValue.lax_location_coordinates_re.match failed for %s" % self.value, file=self.error_file, flush=True)
                    self.valid = False
                    return False
                rewrite_needed = self.options.repair_lax_coordinates
            else:
                if self.verbose:
                    print("KgtkValue.location_coordinates_re.match failed for %s" % self.value, file=self.error_file, flush=True)
                self.valid = False
                return False

        latstr: str = m.group("lat")
        lonstr: str = m.group("lon")

        fixup_needed: bool = False

        # Latitude normally runs from -90 to +90:
        #
        # TODO: Offer a wrapping repair for latitude, which will also affect latitude.
        try:
            lat: float = float(latstr)
            if self.options.allow_out_of_range_coordinates:
                pass
            elif lat < self.options.minimum_valid_lat:
                if self.options.clamp_minimum_lat:
                    lat = self.options.minimum_valid_lat
                    latstr = str(lat)
                    fixup_needed = True
                else:
                    if self.verbose:
                        print("KgtkValue.is_location_coordinates: lat less than minimum %f for %s" % (self.options.minimum_valid_lat, repr(self.value)),
                              file=self.error_file, flush=True)
                    self.valid = False
                    return False
            elif lat > self.options.maximum_valid_lat:
                if self.options.clamp_maximum_lat:
                    lat = self.options.maximum_valid_lat
                    latstr = str(lat)
                    fixup_needed = True
                else:
                    if self.verbose:
                        print("KgtkValue.is_location_coordinates: lat greater than maximum %f for %s" % (self.options.maximum_valid_lat, repr(self.value)),
                              file=self.error_file, flush=True)
                    self.valid = False
                    return False
            if rewrite_needed:
                latstr = self.format_degrees(lat)
                fixup_needed = True
        except ValueError:
            if self.verbose:
                print("KgtkValue.is_location_coordinates: lat is not float for %s" % (repr(self.value)),
                      file=self.error_file, flush=True)
            self.valid = False
            return False

        # Longitude normally runs from -180 to +180:
        try:
            lon: float = float(lonstr)
            if self.options.allow_out_of_range_coordinates:
                pass
            elif  lon < self.options.minimum_valid_lon:
                if self.options.modulo_repair_lon:
                    lon = self.wrap_longitude(lon)
                    lonstr = str(lon)
                    fixup_needed = True
                elif self.options.clamp_minimum_lon:
                    lon = self.options.minimum_valid_lon
                    lonstr = str(lon)
                    fixup_needed = True
                else:
                    if self.verbose:
                        print("KgtkValue.is_location_coordinates: lon less than minimum %f for %s" % (self.options.minimum_valid_lon, repr(self.value)),
                              file=self.error_file, flush=True)
                    self.valid = False
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
                    if self.verbose:
                        print("KgtkValue.is_location_coordinates: lon greater than maximum %f for %s" % (self.options.maximum_valid_lon, repr(self.value)),
                              file=self.error_file, flush=True)
                    self.valid = False
                    return False
            if rewrite_needed:
                lonstr = self.format_degrees(lon)
                fixup_needed = True
        except ValueError:
            if self.verbose:
                print("KgtkValue.is_location_coordinates: lon is not float for %s" % (repr(self.value)),
                      file=self.error_file, flush=True)
            self.valid = False
            return False

        if fixup_needed:
            # Repair a location coordinates problem.
            self.update_location_coordinates(latstr, lonstr)

        # We are certain that this is valid.
        self.valid = True
        if parse_fields or self.parse_fields:
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
    #
    # NOTE: hour 24 is valid only when minutes and seconds are 00
    # and options.allow_end_of_day is True
    hour_pat: str = r'(?P<hour>2[0-4]|[01][0-9])'
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
                                                                        
    def is_date_and_times(self, validate: bool=False, parse_fields: bool = False)->bool:
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
            if not self.valid:
                return False

            if not (self.fields is None and parse_fields):
                return True
        
        # Clear any fields from prior validation:
        self.fields = None

        # Validate the date and times:
        m: typing.Optional[typing.Match] = KgtkValue.lax_date_and_times_re.match(self.value)
        if m is None:
            if self.verbose:
                print("KgtkValue.lax_date_and_times_re.match(%s) failed." % repr(self.value), file=self.error_file, flush=True)
            self.valid = False
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

        if not iso8601extended:
            if self.options.force_iso8601_extended:
                fixup_needed = True
            elif self.options.require_iso8601_extended:
                if self.verbose:
                    print("KgtkValue.is_date_and_times: missing hyphen in %s." % repr(self.value), file=self.error_file, flush=True)
                self.valid = False
                return False

        # Validate the year:
        if yearstr is None or len(yearstr) == 0:
            if self.verbose:
                print("KgtkValue.is_date_and_times: no year in %s." % repr(self.value), file=self.error_file, flush=True)
            self.valid = False
            return False # Years are mandatory
        try:
            year: int = int(yearstr)
        except ValueError:
            if self.verbose:
                print("KgtkValue.is_date_and_times: year not int in %s." % repr(self.value), file=self.error_file, flush=True)
            self.valid = False
            return False
        if year < self.options.minimum_valid_year and not self.options.ignore_minimum_year:
            if self.options.clamp_minimum_year:
                year = self.options.minimum_valid_year
                if year >= 0:
                    yearstr = str(year).zfill(4)
                else:
                    # Minus sign *and* at least 4 digits.
                    yearstr = str(year).zfill(5)
                fixup_needed = True
            else:
                if self.verbose:
                    print("KgtkValue.is_date_and_times: year less than minimum %d: %s." % (self.options.minimum_valid_year, repr(self.value)),
                          file=self.error_file, flush=True)
                self.valid = False
                return False
        elif year > self.options.maximum_valid_year and not self.options.ignore_maximum_year:
            if self.options.clamp_maximum_year:
                year = self.options.maximum_valid_year
                if year >= 0:
                    yearstr = str(year).zfill(4)
                else:
                    # Minus sign *and* at least 4 digits.
                    yearstr = str(year).zfill(5)
                fixup_needed = True
            else:
                if self.verbose:
                    print("KgtkValue.is_date_and_times: year greater than maximum %d: %s." % (self.options.maximum_valid_year, repr(self.value)),
                          file=self.error_file, flush=True)
                self.valid = False
                return False

        month: typing.Optional[int]
        if monthstr is None:
            month = None
        else:
            try:
                month = int(monthstr)
            except ValueError:
                if self.verbose:
                    print("KgtkValue.is_date_and_times: month not int in %s." % repr(self.value), file=self.error_file, flush=True)
                self.valid = False
                return False # shouldn't happen
            if month == 0:
                if self.options.repair_month_or_day_zero:
                    month = 1
                    monthstr = "01"
                    fixup_needed = True
                elif not self.options.allow_month_or_day_zero:
                    if self.verbose:
                        print("KgtkValue.is_date_and_times: month 0 disallowed in %s." % repr(self.value), file=self.error_file, flush=True)
                    self.valid = False
                    return False # month 0 was disallowed.

        day: typing.Optional[int]
        if daystr is None:
            day = None
        else:
            try:
                day = int(daystr)
            except ValueError:
                if self.verbose:
                    print("KgtkValue.is_date_and_times: day not int in %s." % repr(self.value), file=self.error_file, flush=True)
                self.valid = False
                return False # shouldn't happen
            if day == 0:
                if self.options.repair_month_or_day_zero:
                    day = 1
                    daystr = "01"
                    fixup_needed = True
                elif not self.options.allow_month_or_day_zero:
                    if self.verbose:
                        print("KgtkValue.is_date_and_times: day 0 disallowed in %s." % repr(self.value), file=self.error_file, flush=True)
                    self.valid = False
                    return False # day 0 was disallowed.

        # Convert the time fields to ints:
        hour: typing.Optional[int]
        if hourstr is None:
            hour = None
        else:
            try:
                hour = int(hourstr)
            except ValueError:
                if self.verbose:
                    print("KgtkValue.is_date_and_times: hour not int in %s." % repr(self.value), file=self.error_file, flush=True)
                self.valid = False
                return False # shouldn't happen

        minutes: typing.Optional[int]
        if minutesstr is None:
            minutes = None
        else:
            try:
                minutes = int(minutesstr)
            except ValueError:
                if self.verbose:
                    print("KgtkValue.is_date_and_times: minutes not int in %s." % repr(self.value), file=self.error_file, flush=True)
                self.valid = False
                return False # shouldn't happen

        seconds: typing.Optional[int]
        if secondsstr is None:
            seconds = None
        else:
            try:
                seconds = int(secondsstr)
            except ValueError:
                if self.verbose:
                    print("KgtkValue.is_date_and_times: seconds not int in %s." % repr(self.value), file=self.error_file, flush=True)
                self.valid = False
                return False # shouldn't happen

        if hour is not None and hour == 24:
            if ((minutes is not None and minutes > 0) or (seconds is not None and seconds > 0)):
                if self.verbose:
                    print("KgtkValue.is_date_and_times: hour 24 and minutes or seconds not zero in %s." % repr(self.value), file=self.error_file, flush=True)
                self.valid = False
                return False # An invalid time
            if not self.options.allow_end_of_day:
                if self.verbose:
                    print("KgtkValue.is_date_and_times: end-of-day value disallowed in %s." % repr(self.value), file=self.error_file, flush=True)
                self.valid = False
                return False

        precision: typing.Optional[int]
        if precisionstr is None:
            precision = None
        else:
            try:
                precision = int(precisionstr)
            except ValueError:
                if self.verbose:
                    print("KgtkValue.is_date_and_times: precision not int in %s." % repr(self.value), file=self.error_file, flush=True)
                self.valid = False
                return False # shouldn't happen

        if fixup_needed:
            # Repair a month or day zero problem.
            self.update_date_and_times(yearstr, monthstr, daystr, hourstr, minutesstr, secondsstr, zonestr, precisionstr, iso8601extended)

        if self.options.validate_fromisoformat:
            try:
                kgtkdatestr: str = self.value[1:] # Strip the leading ^ sigil.
                isodatestr: str
                if "/" in kgtkdatestr:
                    isodatestr, _ = kgtkdatestr.split("/")
                else:
                    isodatestr = self.value
                if isodatestr.endswith("Z"): # Might there be other time zones?
                    isodatestr = isodatestr[:-1]
                _ = dt.datetime.fromisoformat(isodatestr)
            except ValueError:
                if self.verbose:
                    print("KgtkValue.is_date_and_times: datetime.fromisoformat(...) cannot parse %s." % repr(self.value),  file=self.error_file, flush=True)
                self.valid = False
                return False # might happen

        # We are fairly certain that this is a valid date and times.
        self.valid = True
        if parse_fields or self.parse_fields:
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

    def is_extension(self, validate: bool =False, parse_fields: bool =False)->bool:
        """Return True if the first character is !

        Although we refer to the validate parameter in the code below, we
        force self.valid to False.

        Note:  parse_fields is ignored at present.

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
            if not self.is_number(quiet=True):
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

    def validate(self, parse_fields: bool =  False)->bool:
        # Validate this KgtkValue.

        # Start by classifying the KgtkValue.
        dt: KgtkFormat.DataType = self.classify()

        # If the valid flag has already been cached, return that.
        if self.valid is not None:
            if not self.valid:
                return False

            if not (self.fields is None and parse_fields):
                return True

        # Clear any fields from prior validation:
        self.fields = None
        
        # Validate the value.
        if dt == KgtkFormat.DataType.EMPTY:
            return self.is_empty(validate=True, parse_fields=parse_fields)
        elif dt == KgtkFormat.DataType.LIST:
            return self.is_list(validate=True, parse_fields=parse_fields)
        elif dt == KgtkFormat.DataType.NUMBER:
            return self.is_number(validate=True, parse_fields=parse_fields)
        elif dt == KgtkFormat.DataType.QUANTITY:
            return self.is_quantity(validate=True, parse_fields=parse_fields)
        elif dt == KgtkFormat.DataType.STRING:
            return self.is_string(validate=True, parse_fields=parse_fields)
        elif dt == KgtkFormat.DataType.LANGUAGE_QUALIFIED_STRING:
            return self.is_language_qualified_string(validate=True, parse_fields=parse_fields)
        elif dt == KgtkFormat.DataType.LOCATION_COORDINATES:
            return self.is_location_coordinates(validate=True, parse_fields=parse_fields)
        elif dt == KgtkFormat.DataType.DATE_AND_TIMES:
            return self.is_date_and_times(validate=True, parse_fields=parse_fields)
        elif dt == KgtkFormat.DataType.EXTENSION:
            return self.is_extension(validate=True, parse_fields=parse_fields)
        elif dt == KgtkFormat.DataType.BOOLEAN:
            return self.is_boolean(validate=True, parse_fields=parse_fields)
        elif dt == KgtkFormat.DataType.SYMBOL:
            return self.is_symbol(validate=True, parse_fields=parse_fields)
        else:
            raise ValueError("Unrecognized DataType.")

    def do_parse_fields(self)->bool:
        # Ensure that validation has taken place and the fields have been parsed if valid.
        return self.validate(parse_fields=True)

    def revalidate(self, reclassify: bool=False, parse_fields: bool = False)->bool:
        # Revalidate this KgtkValue after clearing cached values.
        if reclassify:
            self.data_type = None
        self.valid = None
        self.fields = None
        return self.validate(parse_fields=parse_fields)
        
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
            return "Number" if self.is_number(validate=True) else "Invalid Number"
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
        kv: KgtkValue = KgtkValue(value, options=value_options, parse_fields=args.parse_fields, verbose=args.verbose)
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
