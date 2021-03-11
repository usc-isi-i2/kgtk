"""
Validate property patterns..
"""

from argparse import ArgumentParser, Namespace
import attr
import copy
import datetime as dt
from enum import Enum
from pathlib import Path
import re
import sys
import typing

from kgtk.kgtkformat import KgtkFormat
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderMode, KgtkReaderOptions
from kgtk.io.kgtkwriter import KgtkWriter
from kgtk.utils.argparsehelpers import optional_bool
from kgtk.value.kgtkvalue import KgtkValue, KgtkValueFields
from kgtk.value.kgtkvalueoptions import KgtkValueOptions

# TODO: verify that the automatically created __eq__, __lt__, etc.
# methods do the same thing a the hand-generated ones.
@attr.s(slots=True, frozen=True, eq=False, order=False, str=False, repr=False, hash=False)
class PropertyPatternDate:
    year: int = attr.ib()
    month: int = attr.ib()
    day: int = attr.ib()
    hour: int = attr.ib()
    minutes: int = attr.ib()
    seconds: int = attr.ib()
    
    @classmethod
    def new(cls, year: int, month: int, day: int, hour: int, minutes: int, seconds: int)->'PropertyPatternDate':
        # Python3 supports bigint

        if month == 0:
            month = 1

        if day == 0:
            day = 1

        return cls(year, month, day, hour, minutes, seconds)

    @classmethod
    def from_kv(cls, kv: KgtkValue)->'PropertyPatternDate':
        if not kv.is_date_and_times(validate=True):
            raise ValueError("Value '%s' is not a date_and_times value" % (kv.value))
        if kv.fields is None:
            raise ValueError("Value '%s' has no fields" % (kv.value))
        if kv.fields.year is None:
            raise ValueError("Value '%s' has no year" % (kv.value))
        if kv.fields.month is None:
            raise ValueError("Value '%s' has no month" % (kv.value))
        if kv.fields.day is None:
            raise ValueError("Value '%s' has no day" % (kv.value))
        if kv.fields.hour is None:
            raise ValueError("Value '%s' has no hour" % (kv.value))
        if kv.fields.minutes is None:
            raise ValueError("Value '%s' has no minutes" % (kv.value))
        if kv.fields.seconds is None:
            raise ValueError("Value '%s' has no seconds" % (kv.value))
        if kv.fields.zonestr is None:
            raise ValueError("Value '%s' has no timezone" % (kv.value))
        if kv.fields.zonestr != "Z":
            raise ValueError("Value '%s' timezone is not Z" % (kv.value))
        return cls.new(kv.fields.year,
                       kv.fields.month,
                       kv.fields.day,
                       kv.fields.hour,
                       kv.fields.minutes,
                       kv.fields.seconds)

    def __str__(self)->str:
        return "%04d-%02d-%02dT%02d:%02d:%02dZ" % (self.year, self.month, self.day, self.hour, self.minutes, self.seconds)

    def __repr__(self)->str:
        return "%04d-%02d-%02dT%02d:%02d:%02dZ" % (self.year, self.month, self.day, self.hour, self.minutes, self.seconds)

    def __lt__(self, other: 'PropertyPatternDate')->bool:
        if self.year < other.year:
            return True
        if self.year > other.year:
            return False
        if self.month < other.month:
            return True
        if self.month > other.month:
            return False
        if self.day < other.day:
            return True
        if self.day > other.day:
            return False
        if self.hour < other.hour:
            return True
        if self.hour > other.hour:
            return False
        if self.minutes < other.minutes:
            return True
        if self.minutes > other.minutes:
            return False
        if self.seconds < other.seconds:
            return True
        if self.seconds > other.seconds:
            return False
        return False

    def __le__(self, other: 'PropertyPatternDate')->bool:
        if self.year < other.year:
            return True
        if self.year > other.year:
            return False
        if self.month < other.month:
            return True
        if self.month > other.month:
            return False
        if self.day < other.day:
            return True
        if self.day > other.day:
            return False
        if self.hour < other.hour:
            return True
        if self.hour > other.hour:
            return False
        if self.minutes < other.minutes:
            return True
        if self.minutes > other.minutes:
            return False
        if self.seconds < other.seconds:
            return True
        if self.seconds > other.seconds:
            return False
        return True

    def __eq__(self, other: object)->bool:
        if not isinstance(other, PropertyPatternDate):
            return NotImplemented
        return \
            self.year == other.year and \
            self.month == other.month and \
            self.day == other.day  and \
            self.hour == other.hour and \
            self.minutes == other.minutes and \
            self.seconds == other.seconds

    def __ne__(self, other: object)->bool:
        if not isinstance(other, PropertyPatternDate):
            return NotImplemented
        return \
            self.year != other.year or \
            self.month != other.month or \
            self.day != other.day  or \
            self.hour != other.hour or \
            self.minutes != other.minutes or \
            self.seconds != other.seconds

    def __gt__(self, other: 'PropertyPatternDate')->bool:
        if self.year > other.year:
            return True
        if self.year < other.year:
            return False
        if self.month > other.month:
            return True
        if self.month < other.month:
            return False
        if self.day > other.day:
            return True
        if self.day < other.day:
            return False
        if self.hour > other.hour:
            return True
        if self.hour < other.hour:
            return False
        if self.minutes > other.minutes:
            return True
        if self.minutes < other.minutes:
            return False
        if self.seconds > other.seconds:
            return True
        if self.seconds < other.seconds:
            return False
        return False

    def __ge__(self, other: 'PropertyPatternDate')->bool:
        if self.year > other.year:
            return True
        if self.year < other.year:
            return False
        if self.month > other.month:
            return True
        if self.month < other.month:
            return False
        if self.day > other.day:
            return True
        if self.day < other.day:
            return False
        if self.hour > other.hour:
            return True
        if self.hour < other.hour:
            return False
        if self.minutes > other.minutes:
            return True
        if self.minutes < other.minutes:
            return False
        if self.seconds > other.seconds:
            return True
        if self.seconds < other.seconds:
            return False
        return True


    def __hash__(self)->int:
        if self.year >= 0:
            return ((((self.year * 100 + self.month) * 100 + self.day) *100 + self.hour) * 100 + self.minutes) + self.seconds
        else:
            return -((((((-self.year) * 100 + self.month) * 100 + self.day) *100 + self.hour) * 100 + self.minutes) + self.seconds)

@attr.s(slots=True, frozen=True)
class PropertyPattern:

    class Action(Enum):
        NOT_IN_COLUMNS = "not_in_columns"

        NODE1_TYPE = "node1_type"
        NODE1_IS_VALID = "node1_is_valid"
        NODE1_ALLOW_LIST = "node1_allow_list"
        NODE1_VALUES = "node1_values"
        NODE1_PATTERN = "node1_pattern"

        LABEL_PATTERN = "label_pattern"
        LABEL_ALLOW_LIST = "label_allow_list"

        NODE2_COLUMN = "node2_column"
        NODE2_ALLOW_LIST = "node2_allow_list"
        NODE2_TYPE = "node2_type"
        NODE2_NOT_TYPE = "node2_not_type"
        NODE2_IS_VALID = "node2_is_valid"
        NODE2_VALUES = "node2_values"
        NODE2_NOT_VALUES = "node2_not_values"
        NODE2_PATTERN = "node2_pattern"
        NODE2_NOT_PATTERN = "node2_not_pattern"
        NODE2_BLANK = "node2_blank"
        NODE2_NOT_BLANK = "node2_not_blank"
        NODE2_CHAIN = "node2_chain"

        NODE2_FIELD_OP = "node2_field_op" # one or more operation symbols
        FIELD_NAME = "field_name" # one or more field names
        FIELD_VALUES = "field_values"
        FIELD_NOT_VALUES = "field_not_values"
        FIELD_PATTERN = "field_pattern"
        FIELD_NOT_PATTERN = "field_not_pattern"
        FIELD_BLANK = "field_blank"
        FIELD_NOT_BLANK = "field_not_blank"

        MINVAL = "minval" # GE
        MAXVAL = "maxval" # LE
        GREATER_THAN = "greater_than" # GT
        LESS_THAN = "less_than" # LT
        EQUAL_TO = "equal_to" # EQ, may take a list of numbers
        NOT_EQUAL_TO = "not_equal_to" # NE, may take a list of numbers

        MINDATE = "mindate"
        MAXDATE = "maxdate"
        GREATER_THAN_DATE = "greater_than_date" # GT
        LESS_THAN_DATE = "less_than_date" # LT
        EQUAL_TO_DATE = "equal_to_date" # EQ, may take a list of dates
        NOT_EQUAL_TO_DATE = "not_equal_to_date" # NE, may take a list of dates

        ID_ALLOW_LIST = "id_allow_list"
        ID_PATTERN = "id_pattern"
        ID_NOT_PATTERN = "id_not_pattern"
        ID_BLANK = "id_blank"
        ID_NOT_BLANK = "id_not_blank"
        ID_CHAIN = "id_chain"

        MUSTOCCUR = "mustoccur"
        MINOCCURS = "minoccurs"
        MAXOCCURS = "maxoccurs"

        GROUPBYPROP = "groupbyprop"
        
        ISA = "isa"
        SWITCH = "switch"
        NEXTCASE = "nextcase"
        MATCHES = "matches"
        UNKNOWN = "unknown"
        REJECT = "reject"

        DATATYPE = "datatype"
        PROPERTY = "property"

        MINDISTINCT = "mindistinct"
        MAXDISTINCT = "maxdistinct"

        REQUIRES = "requires"
        PROHIBITS = "prohibits"

        def __lt__(self, other)->bool:
            """
            THis conceit allow the actions to be sorted, which can simplify debugging.
            """
            if self.__class__ is other.__class__:
                return self.value < other.value
            return NotImplemented
        
    # TODO: create validators where missing:
    prop_or_datatype: str = attr.ib(validator=attr.validators.instance_of(str))
    action: Action = attr.ib()
    intval: typing.Optional[int] = attr.ib()
    patterns: typing.List[typing.Pattern] = attr.ib()
    numbers: typing.List[float] = attr.ib()
    column_names: typing.List[str] = attr.ib()
    values: typing.List[str] = attr.ib()
    truth: bool = attr.ib()
    datetimes: typing.List[PropertyPatternDate] = attr.ib()

    # Even though the object is frozen, we can still alter lists.
    column_idxs: typing.List[int] = attr.ib(factory=list)

    @classmethod
    def new(cls,
            node1_value: KgtkValue,
            label_value: KgtkValue,
            node2_value: KgtkValue,
            old_ppat: typing.Optional['PropertyPattern'],
            rownum: int = 0,
    )->'PropertyPattern':
        prop_or_datatype = node1_value.value
        try:
            action: PropertyPattern.Action = cls.Action(label_value.value)
        except ValueError as e:
            raise ValueError("Filter row %d: %s: not a valid Property Pattern action." % (rownum, label_value.value))

        kv: KgtkValue
        
        intval: typing.Optional[int] = None
        patterns: typing.List[typing.Pattern] = [ ]
        numbers: typing.List[float] = [ ]
        column_names: typing.List[str] = [ ]
        values: typing.List[str] = [ ]
        truth: bool = False
        datetimes: typing.List[PropertyPatternDate] = [ ]

        if action in (cls.Action.NODE1_PATTERN,
                      cls.Action.NODE2_PATTERN,
                      cls.Action.NODE2_NOT_PATTERN,
                      cls.Action.FIELD_PATTERN,
                      cls.Action.FIELD_NOT_PATTERN,
                      cls.Action.LABEL_PATTERN,
                      cls.Action.MATCHES):
            if node2_value.is_string(validate=True):
                if node2_value.fields is None:
                    raise ValueError("Filter row %d: %s: Node2 has no fields" % (rownum, action.value)) # TODO: better complaint
                if node2_value.fields.text is None:
                    raise ValueError("Filter row %d: %s: Node2 has no text" % (rownum, action.value)) # TODO: better complaint
                # print("pattern=%s" % repr(node2_value.fields.decoded_text), file=sys.stderr, flush=True)
                patterns.append(re.compile(node2_value.fields.decoded_text))
            elif node2_value.is_list():
                for kv in node2_value.get_list_items():
                    if not kv.is_string(validate=True):
                        raise ValueError("Filter row %d: %s: List value '%s' is not a string" % (rownum, action.value, kv.value)) # TODO: better complaint
                    if kv.fields is None:
                        raise ValueError("Filter row %d: %s: Node2 list value '%s' has no fields" % (rownum, action.value, kv.value)) # TODO: better complaint
                    if kv.fields.text is None:
                        raise ValueError("Filter row %d: %s: Node2 list value '%s' has no text" % (rownum, action.value, kv.value)) # TODO: better complaint
                    patterns.append(re.compile(kv.fields.text))
            else:
                raise ValueError("Filter row %d: %s: Value '%s' is not a string" % (rownum, action.value, node2_value.value)) # TODO: better complaint

            # Merge any existing patterns, then removed duplicates:
            if old_ppat is not None and len(old_ppat.patterns) > 0:
                patterns.extend(old_ppat.patterns)
            patterns = list(set(patterns))

        elif action in (cls.Action.MINOCCURS,
                        cls.Action.MAXOCCURS,
                        cls.Action.MINDISTINCT,
                        cls.Action.MAXDISTINCT):
            if not node2_value.is_number(validate=True):
                raise ValueError("Filter row %d: %s: Node2 is not numeric" % (rownum, action.value)) # TODO: better complaint
            if node2_value.fields is None:
                raise ValueError("Filter row %d: %s: Node2 has no fields" % (rownum, action.value)) # TODO: better complaint
            if node2_value.fields.number is None:
                raise ValueError("Filter row %d: %s: Node2 has no number" % (rownum, action.value)) # TODO: better complaint
            intval = int(node2_value.fields.number)

        elif action in (cls.Action.MINVAL,
                        cls.Action.MAXVAL,
                        cls.Action.GREATER_THAN,
                        cls.Action.LESS_THAN,
                        cls.Action.EQUAL_TO,
                        cls.Action.NOT_EQUAL_TO):
            if node2_value.is_number_or_quantity(validate=True):
                if node2_value.fields is None:
                    raise ValueError("Filter row %d: %s: Node2 has no fields" % (rownum, action.value)) # TODO: better complaint
                if node2_value.fields.number is None:
                    raise ValueError("Filter row %d: %s: Node2 has no number" % (rownum, action.value)) # TODO: better complaint
                numbers.append(float(node2_value.fields.number))

            elif node2_value.is_list():
                for kv in node2_value.get_list_items():
                    if not kv.is_number_or_quantity(validate=True):
                        raise ValueError("Filter row %d: %s: List value '%s' is not a number or quantity" % (rownum, action.value, kv.value)) # TODO: better complaint
                    if kv.fields is None:
                        raise ValueError("Filter row %d: %s: Node2 list value '%s' has no fields" % (rownum, action.value, kv.value)) # TODO: better complaint
                    if kv.fields.number is None:
                        raise ValueError("Filter row %d: %s: Node2 list value '%s' has no number" % (rownum, action.value, kv.value)) # TODO: better complaint
                    numbers.append(float(kv.fields.number))

            else:
                raise ValueError("Filter row %d: %s: Value '%s' is not a number or quantity" % (rownum, action.value, node2_value.value)) # TODO: better complaint

            # Merge any existing numbers, then removed duplicates and sort:
            if old_ppat is not None and len(old_ppat.numbers) > 0:
                numbers.extend(old_ppat.numbers)
            numbers = sorted(list(set(numbers)))

            if action in (cls.Action.MINVAL,
                          cls.Action.MAXVAL,
                          cls.Action.GREATER_THAN,
                          cls.Action.LESS_THAN) and len(numbers) > 1:
                raise ValueError("Filter row %d: %s: only one value is allowed: %s" % (rownum, action.value, node2_value.value)) # TODO: better complaint

        elif action in (cls.Action.MINDATE,
                        cls.Action.MAXDATE,
                        cls.Action.GREATER_THAN_DATE,
                        cls.Action.LESS_THAN_DATE,
                        cls.Action.EQUAL_TO_DATE,
                        cls.Action.NOT_EQUAL_TO_DATE):
            if node2_value.is_date_and_times(validate=True):
                try: 
                    datetimes.append(PropertyPatternDate.from_kv(node2_value))
                except ValueError as e:
                    raise ValueError("Filter row %d: %s: %s" % (rownum, action.value, e.args[0]))

            elif node2_value.is_list():
                for kv in node2_value.get_list_items():
                    if not kv.is_date_and_times(validate=True):
                        raise ValueError("Filter row %d: %s: List value '%s' is not a date_and_times value" % (rownum, action.value, kv.value)) # TODO: better complaint
                    try: 
                        datetimes.append(PropertyPatternDate.from_kv(kv))
                    except ValueError as e:
                        raise ValueError("Filter row %d: %s: %s" % (rownum, action.value, e.args[0]))

            else:
                raise ValueError("Filter row %d: %s: Value '%s' is not a date_and_times value" % (rownum, action.value, node2_value.value)) # TODO: better complaint

            # Merge any existing numbers, then removed duplicates and sort:
            if old_ppat is not None and len(old_ppat.datetimes) > 0:
                datetimes.extend(old_ppat.datetimes)
            datetimes = sorted(list(set(datetimes)))

            if action in(cls.Action.MINDATE,
                         cls.Action.MAXDATE,
                         cls.Action.GREATER_THAN_DATE,
                         cls.Action.LESS_THAN_DATE,
            ) and len(datetimes) > 1:
                raise ValueError("Filter row %d: %s: only one value is allowed: %s" % (rownum, action.value, node2_value.value)) # TODO: better complaint

        elif action in (cls.Action.NOT_IN_COLUMNS,):
            # TODO: validate that the column names are valid and get their indexes.
            if node2_value.is_symbol():
                column_names.append(node2_value.value)
            elif node2_value.is_list():
                for kv in node2_value.get_list_items():
                    if kv.is_symbol():
                        column_names.append(kv.value)
                    else:
                        raise ValueError("Filter row %d: %s: List value is not a symbol" % (rownum, action.value)) # TODO: better complaint
            else:
                raise ValueError("Filter row %d: %s: Value '%s' is not a symbol or list of symbols" % (rownum, action.value, node2_value.value)) # TODO: better complaint
            # TODO: validate that the column names are valid and get their indexes.

            # Merge any existing column names, then removed duplicates and sort:
            if old_ppat is not None and len(old_ppat.column_names) > 0:
                column_names.extend(old_ppat.column_names)
            column_names = sorted(list(set(column_names)))

        elif action in (
                # cls.Action.LABEL_COLUM,
                cls.Action.NODE2_COLUMN,
        ):
            if label_value.is_symbol():
                column_names.append(node2_value.value)
            else:
                raise ValueError("Filter row %d: %s:Value is not a symbol" % (rownum, action.value)) # TODO: better complaint
            # TODO: validate that the column names are valid and get their indexes.

        elif action in (cls.Action.NODE1_TYPE,
                        cls.Action.NODE2_TYPE,
                        cls.Action.NODE2_NOT_TYPE,
                        cls.Action.NODE2_FIELD_OP,
                        cls.Action.ISA,
                        cls.Action.SWITCH,
                        cls.Action.NEXTCASE,
                        cls.Action.REQUIRES,
                        cls.Action.PROHIBITS):
            if node2_value.is_symbol():
                values.append(node2_value.value)
            elif node2_value.is_list():
                for kv in node2_value.get_list_items():
                    if kv.is_symbol():
                        values.append(kv.value)
                    else:
                        raise ValueError("Filter row %d: %s: List value is not a symbol" % (rownum, action.value)) # TODO: better complaint
            else:
                raise ValueError("Filter row %d: %s: Value '%s' is not a symbol or list of symbols" % (rownum, action.value, node2_value.value)) # TODO: better complaint

            # Merge any existing values, then removed duplicates and sort:
            if old_ppat is not None and len(old_ppat.values) > 0:
                values.extend(old_ppat.values)
            values = sorted(list(set(values)))

        elif action in (cls.Action.FIELD_NAME,):
            if node2_value.is_symbol():
                if node2_value.value not in KgtkValueFields.FIELD_NAMES:
                    raise ValueError("Filter row %d: %s: %s is not a known field name." % (rownum, action.value, node2_value.value))

                values.append(node2_value.value)
            elif node2_value.is_list():
                for kv in node2_value.get_list_items():
                    if kv.is_symbol():
                        if kv.value not in KgtkValueFields.FIELD_NAMES:
                            raise ValueError("Filter row %d: %s: %s is not a known field name." % (rownum, action.value, kv.value))
                        values.append(kv.value)
                    else:
                        raise ValueError("Filter row %d: %s: List value is not a symbol" % (rownum, action.value)) # TODO: better complaint
            else:
                raise ValueError("Filter row %d: %s: Value '%s' is not a symbol or list of symbols" % (rownum, action.value, node2_value.value)) # TODO: better complaint

            # Merge any existing values, then removed duplicates and sort:
            if old_ppat is not None and len(old_ppat.values) > 0:
                values.extend(old_ppat.values)
            values = sorted(list(set(values)))

                        
        elif action in (cls.Action.NODE1_VALUES,
                        cls.Action.NODE2_VALUES,
                        cls.Action.NODE2_NOT_VALUES,
                        cls.Action.NODE2_CHAIN,
                        cls.Action.ID_CHAIN):
            if node2_value.is_list():
                for kv in node2_value.get_list_items():
                    values.append(kv.value)
            else:
                values.append(node2_value.value)

            # Merge any existing values, then removed duplicates and sort:
            if old_ppat is not None and len(old_ppat.values) > 0:
                values.extend(old_ppat.values)
            values = sorted(list(set(values)))

        elif action in (cls.Action.FIELD_VALUES,
                        cls.Action.FIELD_NOT_VALUES):
            if node2_value.is_list():
                for kv in node2_value.get_list_items():
                    if kv.is_string(validate=True):
                        if kv.fields is None:
                            raise ValueError("Filter row %d: %s: Node2 has no fields" % (rownum, action.value)) # TODO: better complaint
                        if kv.fields.text is None:
                            raise ValueError("Filter row %d: %s: Node2 has no text" % (rownum, action.value)) # TODO: better complaint
                        values.append(kv.fields.text)
                    else:
                        values.append(kv.value)
            else:
                if node2_value.is_string(validate=True):
                    if node2_value.fields is None:
                        raise ValueError("Filter row %d: %s: Node2 has no fields" % (rownum, action.value)) # TODO: better complaint
                    if node2_value.fields.text is None:
                        raise ValueError("Filter row %d: %s: Node2 has no text" % (rownum, action.value)) # TODO: better complaint
                    values.append(node2_value.fields.text)
                else:
                    values.append(node2_value.value)

            # Merge any existing values, then removed duplicates and sort:
            if old_ppat is not None and len(old_ppat.values) > 0:
                values.extend(old_ppat.values)
            values = sorted(list(set(values)))

        elif action in (cls.Action.NODE1_ALLOW_LIST,
                        cls.Action.LABEL_ALLOW_LIST,
                        cls.Action.NODE2_ALLOW_LIST,
                        cls.Action.ID_ALLOW_LIST,
                        cls.Action.MUSTOCCUR,
                        cls.Action.UNKNOWN,
                        cls.Action.REJECT,
                        cls.Action.PROPERTY,
                        cls.Action.DATATYPE,
                        cls.Action.GROUPBYPROP,
                        cls.Action.NODE2_BLANK,
                        cls.Action.NODE2_NOT_BLANK,
                        cls.Action.FIELD_BLANK,
                        cls.Action.FIELD_NOT_BLANK,
                        cls.Action.NODE1_IS_VALID,
                        cls.Action.NODE2_IS_VALID):
            if node2_value.is_boolean(validate=True) and node2_value.fields is not None and node2_value.fields.truth is not None:
                truth = node2_value.fields.truth
            else:
                raise ValueError("Filter row %d: %s: Value '%s' is not a boolean" % (rownum, action.value, node2_value.value)) # TODO: better complaint

        return cls(prop_or_datatype, action, intval, patterns, numbers, column_names, values, truth, datetimes)

@attr.s(slots=True, frozen=True)
class PropertyPatternFactory:
    # Indices in the property pattern file:
    node1_idx: int = attr.ib(validator=attr.validators.instance_of(int))
    label_idx: int = attr.ib(validator=attr.validators.instance_of(int))
    node2_idx: int = attr.ib(validator=attr.validators.instance_of(int))

    value_options: KgtkValueOptions = attr.ib(validator=attr.validators.instance_of(KgtkValueOptions))

    verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    very_verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    def from_row(self,
                 rownum: int,
                 row: typing.List[str],
                 old_ppat: typing.Optional[PropertyPattern]=None,
    )->PropertyPattern:
        node1_value: KgtkValue = KgtkValue(row[self.node1_idx], options=self.value_options, parse_fields=True)
        label_value: KgtkValue = KgtkValue(row[self.label_idx], options=self.value_options, parse_fields=True)
        node2_value: KgtkValue = KgtkValue(row[self.node2_idx], options=self.value_options, parse_fields=True)

        node1_value.validate()
        label_value.validate()
        node2_value.validate()

        return PropertyPattern.new(node1_value, label_value, node2_value, old_ppat, rownum=rownum)

@attr.s(slots=True, frozen=True)
class PropertyPatternLists:
    node1_patterns: typing.List[PropertyPattern] = attr.ib()
    label_patterns: typing.List[PropertyPattern] = attr.ib()
    node2_patterns: typing.List[PropertyPattern] = attr.ib()
    id_patterns: typing.List[PropertyPattern] = attr.ib()

    field_patterns: typing.List[PropertyPattern] = attr.ib()
    isa_or_switch_patterns: typing.List[PropertyPattern] = attr.ib()

    node2_column_name: typing.Optional[str] = attr.ib()
    nextcase: typing.Optional[str] = attr.ib()

    node1_allow_list: bool = attr.ib()
    label_allow_list: bool = attr.ib()
    node2_allow_list: bool = attr.ib()
    id_allow_list: bool = attr.ib()

    not_in_columns: typing.List[str] = attr.ib()

    field_names: typing.Optional[typing.List[str]] = attr.ib()

    @classmethod
    def new(cls,
            actionmap: typing.Mapping[PropertyPattern.Action, PropertyPattern],
    )->'PropertyPatternLists':

        node1_patterns: typing.List[PropertyPattern] = list()
        label_patterns: typing.List[PropertyPattern] = list()
        node2_patterns: typing.List[PropertyPattern] = list()
        id_patterns: typing.List[PropertyPattern] = list()

        field_patterns: typing.List[PropertyPattern] = list()
        isa_or_switch_patterns: typing.List[PropertyPattern] = list()
        node2_column_name: typing.Optional[str] = None
        nextcase: typing.Optional[str] = None
        
        node1_allow_list: bool = False
        label_allow_list: bool = False
        node2_allow_list: bool = False
        id_allow_list: bool = False

        not_in_columns: typing.List[str] = list()
        
        field_names: typing.Optional[typing.List[str]] = None

        action: PropertyPattern.Action
        for action in sorted(actionmap.keys()):
            pp: PropertyPattern = actionmap[action]
            
            if action in (PropertyPattern.Action.NODE1_TYPE,
                          PropertyPattern.Action.NODE1_IS_VALID,
                          PropertyPattern.Action.NODE1_VALUES,
                          PropertyPattern.Action.NODE1_PATTERN,
                          PropertyPattern.Action.MINOCCURS,
                          PropertyPattern.Action.MAXOCCURS):
                node1_patterns.append(pp)

            elif action in (PropertyPattern.Action.REJECT, # This is a stretch.
                            PropertyPattern.Action.LABEL_PATTERN):
                label_patterns.append(pp)

            elif action in (PropertyPattern.Action.NODE2_CHAIN,
                            PropertyPattern.Action.NODE2_TYPE,
                            PropertyPattern.Action.NODE2_NOT_TYPE,
                            PropertyPattern.Action.NODE2_IS_VALID,
                            PropertyPattern.Action.NODE2_VALUES,
                            PropertyPattern.Action.NODE2_NOT_VALUES,
                            PropertyPattern.Action.NODE2_PATTERN,
                            PropertyPattern.Action.NODE2_NOT_PATTERN,
                            PropertyPattern.Action.NODE2_BLANK,
                            PropertyPattern.Action.NODE2_NOT_BLANK,
                            PropertyPattern.Action.MINDATE,
                            PropertyPattern.Action.MAXDATE,
                            PropertyPattern.Action.GREATER_THAN_DATE,
                            PropertyPattern.Action.LESS_THAN_DATE,
                            PropertyPattern.Action.EQUAL_TO_DATE,
                            PropertyPattern.Action.NOT_EQUAL_TO_DATE,
                            PropertyPattern.Action.NODE2_FIELD_OP,
                            PropertyPattern.Action.MINDISTINCT,
                            PropertyPattern.Action.MAXDISTINCT):
                node2_patterns.append(pp)

            elif action in (PropertyPattern.Action.MINVAL,
                            PropertyPattern.Action.MAXVAL,
                            PropertyPattern.Action.GREATER_THAN,
                            PropertyPattern.Action.LESS_THAN,
                            PropertyPattern.Action.EQUAL_TO,
                            PropertyPattern.Action.NOT_EQUAL_TO):
                node2_patterns.append(pp)
                field_patterns.append(pp)

            elif action in (PropertyPattern.Action.FIELD_VALUES,
                            PropertyPattern.Action.FIELD_NOT_VALUES,
                            PropertyPattern.Action.FIELD_PATTERN,
                            PropertyPattern.Action.FIELD_NOT_PATTERN,
                            PropertyPattern.Action.FIELD_BLANK,
                            PropertyPattern.Action.FIELD_NOT_BLANK):
                field_patterns.append(pp)

            elif action in (PropertyPattern.Action.ID_CHAIN,
                            PropertyPattern.Action.ID_PATTERN,
                            PropertyPattern.Action.ID_NOT_PATTERN,
                            PropertyPattern.Action.ID_BLANK,
                            PropertyPattern.Action.ID_NOT_BLANK):
                id_patterns.append(pp)

            elif action  == PropertyPattern.Action.NODE2_COLUMN:
                node2_column_name = pp.column_names[0]

            elif action == PropertyPattern.Action.NEXTCASE:
                nextcase = pp.values[0]

            elif action in (PropertyPattern.Action.ISA,
                            PropertyPattern.Action.SWITCH):
                isa_or_switch_patterns.append(pp)

            elif action == PropertyPattern.Action.NODE1_ALLOW_LIST:
                node1_allow_list = pp.truth

            elif action == PropertyPattern.Action.LABEL_ALLOW_LIST:
                label_allow_list = pp.truth

            elif action == PropertyPattern.Action.NODE2_ALLOW_LIST:
                node2_allow_list = pp.truth

            elif action == PropertyPattern.Action.ID_ALLOW_LIST:
                id_allow_list = pp.truth

            elif action == PropertyPattern.Action.NOT_IN_COLUMNS:
                not_in_columns = pp.column_names.copy()

            elif action == PropertyPattern.Action.FIELD_NAME:
                field_names = pp.values.copy()

        return cls(node1_patterns, label_patterns, node2_patterns, id_patterns,
                   field_patterns, isa_or_switch_patterns, node2_column_name, nextcase,
                   node1_allow_list, label_allow_list, node2_allow_list, id_allow_list,
                   not_in_columns, field_names)

@attr.s(slots=True, frozen=True)
class PropertyPatterns:
    lists: typing.Mapping[str, PropertyPatternLists] = attr.ib()
    matches: typing.Mapping[str, typing.List[typing.Pattern]] = attr.ib()
    mustoccur: typing.Set[str] = attr.ib()
    occurs: typing.Set[str] = attr.ib()
    distinct: typing.Set[str] = attr.ib()
    groupbyprop: typing.Set[str] = attr.ib()
    unknown: typing.Set[str] = attr.ib()
    requires: typing.Mapping[str, typing.Set[str]] = attr.ib()
    prohibits: typing.Mapping[str, typing.Set[str]] = attr.ib()
    interesting: typing.Set[str] = attr.ib()
    chain_targets: typing.Set[str] = attr.ib()
    not_in_columns: bool = attr.ib()
    do_occurs: bool = attr.ib()

    @classmethod
    def load(cls, kr: KgtkReader,
             value_options: KgtkValueOptions,
             error_file: typing.TextIO = sys.stderr,
             verbose: bool = False,
             very_verbose: bool = False,
    )->'PropertyPatterns':
        patmap: typing.MutableMapping[str, typing.MutableMapping[PropertyPattern.Action, PropertyPattern]] = { }
        matches: typing.MutableMapping[str, typing.List[typing.Pattern]] = { }
        mustoccur: typing.Set[str] = set()
        occurs: typing.Set[str] = set()
        distinct: typing.Set[str] = set()
        groupbyprop: typing.Set[str] = set()
        unknown: typing.Set[str] = set()
        requires: typing.MutableMapping[str, typing.Set[str]] = dict()
        prohibits: typing.MutableMapping[str, typing.Set[str]] = dict()
        interesting: typing.Set[str] = set()
        chain_targets: typing.Set[str] = set()
        not_in_columns: bool = False

        if kr.node1_column_idx < 0:
            raise ValueError("node1 column missing from property pattern file")
        if kr.label_column_idx < 0:
            raise ValueError("label column missing from property pattern file")
        if kr.node2_column_idx < 0:
            raise ValueError("node2 column missing from property pattern file")

        ppf: PropertyPatternFactory = PropertyPatternFactory(kr.node1_column_idx,
                                                             kr.label_column_idx,
                                                             kr.node2_column_idx,
                                                             value_options,
                                                             verbose=verbose,
                                                             very_verbose=very_verbose,
        )

        prop_or_datatype: str

        rownum: int
        row: typing.List[str]
        for rownum, row in enumerate(kr, 1):
            pp: PropertyPattern = ppf.from_row(rownum, row)
            prop_or_datatype = pp.prop_or_datatype
            if prop_or_datatype not in patmap:
                patmap[prop_or_datatype] = { }

            action: PropertyPattern.Action = pp.action
            if action in patmap[prop_or_datatype]:
                # Rebuild the property pattern, merging lists from the prior property pattern.
                # Non-list fields will be silently overwritten.
                pp = ppf.from_row(rownum, row, old_ppat=patmap[prop_or_datatype][action])
            patmap[prop_or_datatype][action] = pp
                
            if very_verbose:
                print("loaded %s->%s" % (prop_or_datatype, action.value), file=error_file, flush=True)
            if action == PropertyPattern.Action.MATCHES and len(pp.patterns) > 0:
                matches[prop_or_datatype] = pp.patterns

            elif action == PropertyPattern.Action.MUSTOCCUR and pp.truth:
                mustoccur.add(prop_or_datatype)
                occurs.add(prop_or_datatype)

            elif action == PropertyPattern.Action.MINOCCURS:
                occurs.add(prop_or_datatype)

            elif action == PropertyPattern.Action.MAXOCCURS:
                occurs.add(prop_or_datatype)

            elif action == PropertyPattern.Action.MINDISTINCT:
                distinct.add(prop_or_datatype)

            elif action == PropertyPattern.Action.MAXDISTINCT:
                distinct.add(prop_or_datatype)

            elif action == PropertyPattern.Action.GROUPBYPROP and pp.truth:
                groupbyprop.add(prop_or_datatype)

            elif action == PropertyPattern.Action.UNKNOWN and pp.truth:
                unknown.add(prop_or_datatype)

            elif action == PropertyPattern.Action.REQUIRES and len(pp.values) > 0:
                requires_set: typing.Set[str] = set(pp.values)
                requires[prop_or_datatype] = requires_set
                interesting.add(prop_or_datatype)
                interesting.update(requires_set)

            elif action == PropertyPattern.Action.PROHIBITS and len(pp.values) > 0:
                prohibits_set: typing.Set[str] = set(pp.values)
                prohibits[prop_or_datatype] = prohibits_set
                interesting.add(prop_or_datatype)
                interesting.update(prohibits_set)

            elif action == PropertyPattern.Action.NODE2_CHAIN and len(pp.values) > 0:
                node2_chain_target_set: typing.Set[str] = set(pp.values)
                chain_targets.update(node2_chain_target_set)
                interesting.update(node2_chain_target_set)

            elif action == PropertyPattern.Action.ID_CHAIN and len(pp.values) > 0:
                id_chain_target_set: typing.Set[str] = set(pp.values)
                chain_targets.update(id_chain_target_set)
                interesting.update(id_chain_target_set)
                
            elif action == PropertyPattern.Action.NOT_IN_COLUMNS:
                not_in_columns = True

        listmap: typing.MutableMapping[str, PropertyPatternLists] = dict()
        for prop_or_datatype in sorted(patmap.keys()):
            listmap[prop_or_datatype] = PropertyPatternLists.new(patmap[prop_or_datatype])

        return cls(lists=listmap,
                   matches=matches,
                   mustoccur=mustoccur,
                   occurs=occurs,
                   distinct=distinct,
                   groupbyprop=groupbyprop,
                   unknown=unknown,
                   requires=requires,
                   prohibits=prohibits,
                   interesting=interesting,
                   chain_targets=chain_targets,
                   not_in_columns=not_in_columns,
                   do_occurs=len(occurs) > 0,
        )

@attr.s(slots=True, frozen=False)
class PropertyPatternValidator:
    ISA_SCOREBOARD_TYPE = typing.List[str]
    OCCURS_SCOREBOARD_TYPE = typing.Optional[typing.MutableMapping[str, typing.MutableMapping[str, int]]]
    INTERESTING_SCOREBOARD_TYPE = typing.Optional[typing.MutableMapping[str, typing.Set[str]]]
    DISTINCT_SCOREBOARD_TYPE = typing.Optional[typing.MutableMapping[str, typing.Set[str]]]
    ROW_TYPE =  typing.List[str]
    ROW_GROUP_TYPE = typing.List[typing.Tuple[int, ROW_TYPE]]
    MAPPED_ROW_GROUPS_TYPE = typing.MutableMapping[str, ROW_GROUP_TYPE]
    COMPLAINT_LIST_TYPE = typing.List[str]

    class ChainSuspensionException(Exception):
        pass

    pps: PropertyPatterns = attr.ib()

    column_names: typing.List[str] = attr.ib()
    column_name_map: typing.Mapping[str, int] = attr.ib()

    # These are the indexes in the input file:
    node1_idx: int = attr.ib()
    label_idx: int = attr.ib()
    node2_idx: int = attr.ib()
    id_idx: int =  attr.ib()

    value_options: KgtkValueOptions = attr.ib()

    grouped_input: bool = attr.ib(default=False)
    reject_node1_groups: bool = attr.ib(default=False)
    no_complaints: bool = attr.ib(default=False) # True is good when rejects are expected.
    complain_immediately: bool = attr.ib(default=False) # True is good for debugging.
    isa_column_idx: int = attr.ib(default=-1)

    autovalidate: bool = attr.ib(default=True)

    error_file: typing.TextIO = attr.ib(default=sys.stderr)
    verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    very_verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    # The datatype inheritance scoreboard, used to detect loops.  It starts
    # fresh for each new row, and contains only the currently evaluated
    # datatype for ISA multiple inheritance.  This is a list instead of a set
    # because we expect it to be short.
    isa_current_scoreboard: ISA_SCOREBOARD_TYPE = attr.ib(factory=list)

    # The next datatype inheritance scoreboard records all of the datatypes,
    # including multiple inheritance.  It starts fresh for each row. We will build
    # a list first, then deduplicate it at the end.
    isa_full_scoreboard: ISA_SCOREBOARD_TYPE = attr.ib(factory=list)

    # Finally, we build a human-oriented representation of the inheritance tree.
    # It starts fresh for each row.  We will build it as a list, which we will join
    # when done, this supposedly being more efficient than concatenation.
    isa_tree_scoreboard: ISA_SCOREBOARD_TYPE = attr.ib(factory=list)

    # The occurance counting scoreboard:
    # node1->prop->count
    # This scoreboard is cleared for each new node1_group.
    occurs_scoreboard: OCCURS_SCOREBOARD_TYPE = attr.ib(default=None)

    # The cache of occurs limits after ISA and GROUPBY:
    # prop->limit
    #
    # Note: this might not work as desired if SWITCH implies
    # conflicting values.
    minoccurs_limits: typing.MutableMapping[str, typing.Optional[int]] = attr.ib(factory=dict)
    maxoccurs_limits: typing.MutableMapping[str, typing.Optional[int]] = attr.ib(factory=dict)

    # The distinct value counting scoreboard:
    # prop->set(values)
    #
    # This scoreboard is saved before possible chain suspensions, and is
    # restored when a suspension takes place.  This requires an unfrozen object.
    distinct_scoreboard: DISTINCT_SCOREBOARD_TYPE = attr.ib(default=None)

    # The distinct limits after ISA and GROUPBY:
    # prop->limit
    #
    # Note: this might not work as desired if SWITCH implies
    # conflicting values.
    mindistinct_limits: typing.MutableMapping[str, typing.Optional[int]] = attr.ib(factory=dict)
    maxdistinct_limits: typing.MutableMapping[str, typing.Optional[int]] = attr.ib(factory=dict)

    # Retain interesting properties or datatypes for requires/prohibits analysis and chaining:
    # node1->set(prop_or_datatype)
    # This scoreboard is cleared for each new node1_group.
    interesting_scoreboard: INTERESTING_SCOREBOARD_TYPE = attr.ib(default=None)

    # Chaining between node1 groups:
    # node1->set(prop_or_datatype)
    # This scoreboard is not cleared, but it gets content only when chaining is needed.
    chain_target_scoreboard: typing.MutableMapping[str, typing.Optional[typing.Set[str]]] = attr.ib(factory=dict)

    # The suspended row groups.
    # node1->row_group
    # row_group: list[tuple[rownum, row]]
    #
    # This requires an unfrozen object.
    suspended_row_groups: typing.Optional['PropertyPatternValidator.MAPPED_ROW_GROUPS_TYPE'] = attr.ib(default=None)
    new_suspended_row_groups: typing.Optional['PropertyPatternValidator.MAPPED_ROW_GROUPS_TYPE'] = attr.ib(default=None)

    # It's easier to keep these counters here rather than passing them around:
    input_row_count: int = attr.ib(default=0)
    valid_row_count: int = attr.ib(default=0)
    output_row_count: int = attr.ib(default=0)
    reject_row_count: int = attr.ib(default=0)

    complaints: 'PropertyPatternValidator.COMPLAINT_LIST_TYPE' = attr.ib(factory=list)

    action_dispatcher: typing.MutableMapping[PropertyPattern.Action,
                                             typing.Callable[[int, KgtkValue, str, PropertyPattern, str], bool]] = attr.ib(factory=dict)

    @classmethod
    def new(cls,
            pps: PropertyPatterns,
            kr: KgtkReader,
            grouped_input: bool,
            reject_node1_groups: bool,
            no_complaints: bool,
            complain_immediately: bool,
            isa_column_idx: int,
            autovalidate: bool,
            value_options: KgtkValueOptions,
            error_file: typing.TextIO,
            verbose: bool,
            very_verbose: bool)->'PropertyPatternValidator':
        ppv: 'PropertyPatternValidator' = PropertyPatternValidator(pps,
                                                                   kr.column_names.copy(),
                                                                   copy.copy(kr.column_name_map),
                                                                   kr.node1_column_idx,
                                                                   kr.label_column_idx,
                                                                   kr.node2_column_idx,
                                                                   kr.id_column_idx,
                                                                   grouped_input=grouped_input,
                                                                   reject_node1_groups=reject_node1_groups,
                                                                   no_complaints=no_complaints,
                                                                   complain_immediately=complain_immediately,
                                                                   isa_column_idx=isa_column_idx,
                                                                   autovalidate=autovalidate,
                                                                   value_options=value_options,
                                                                   error_file=error_file,
                                                                   verbose=verbose,
                                                                   very_verbose=very_verbose)
        ppv.setup_action_dispatch()
        return ppv

    def grouse(self, complaint: str, immediately: bool = False):
        if self.complain_immediately or immediately:
            # For better debugging, complain immediately:
            print("%s" % complaint, file=self.error_file, flush=True)
        else:
            self.complaints.append(complaint)

    def show_complaints(self):
        complaint: str
        if not self.no_complaints:
            for complaint in self.complaints:
                print("%s" % complaint, file=self.error_file, flush=True)
        self.complaints.clear()

    def clear_node1_group(self):
        self.isa_current_scoreboard.clear()
        self.isa_full_scoreboard.clear()
        self.isa_tree_scoreboard.clear()
        self.occurs_scoreboard = None
        self.interesting_scoreboard = None
        self.complaints.clear()

    def validate_not_in_columns(self, rownum: int, row: typing.List[str])->bool:
        """
        Check each column of the row to see if the contents violates a not_in relationship.
        """
        result: bool = True
        idx: int
        column_name: str
        for idx, column_name in enumerate(self.column_names):
            cell_value: str = row[idx]
            # print("Row %d: idx=%d column_name=%s cell_value=%s" % (rownum, idx, column_name, cell_value), file=self.error_file, flush=True)
            cell_value_lists: typing.Optional[PropertyPatternLists] = self.pps.lists.get(cell_value)
            if cell_value_lists is not None:
                # print("len(cell_value_patterns) = %d" % len(cell_value_patterns), file=self.error_file, flush=True)
                column_names: typing.List[str] = cell_value_lists.not_in_columns
                # print("NOT_IN columns: %s" % " ".join(column_names), file=self.error_file, flush=True)
                if column_name in column_names:
                    print("Row %d: Found '%s' in column '%s', which is prohibited." % (rownum, cell_value, column_name), file=self.error_file, flush=True)
                    result = False
        return result

    def validate_valid(self, rownum: int, value: KgtkValue, prop_or_datatype: str, pp: PropertyPattern, who: str)->bool:
        if pp.truth:
            if not value.is_valid():
                self.grouse("Row %d: the %s value '%s' is not a valid KGTK value." % (rownum, who, value.value))
                return False
        else:
            if value.is_valid():
                self.grouse("Row %d: the %s value '%s' is a valid KGTK value, we expected otherwise." % (rownum, who, value.value))
                return False
        return True

    def validate_type(self, rownum: int, value: KgtkValue, prop_or_datatype: str, pp: PropertyPattern, who: str)->bool:
        type_list: typing.List[str] = pp.values
        type_name: str = value.classify().lower()
        if type_name not in type_list:
            self.grouse("Row %d: the %s KGTK datatype '%s' is not in the list of allowed %s types for %s: %s" % (rownum, who, type_name, who, prop_or_datatype,
                                                                                                                 KgtkFormat.LIST_SEPARATOR.join(type_list)))
            return False
        return True

    def validate_not_type(self, rownum: int, value: KgtkValue, prop_or_datatype: str, pp: PropertyPattern, who: str)->bool:
        type_list: typing.List[str] = pp.values
        type_name: str = value.classify().lower()
        if type_name in type_list:
            self.grouse("Row %d: the %s KGTK datatype '%s' is in the list of disallowed %s types for %s: %s" % (rownum, who, type_name, who, prop_or_datatype,
                                                                                                                KgtkFormat.LIST_SEPARATOR.join(type_list)))
            return False
        return True

    def validate_value(self, rownum: int, kgtk_value: KgtkValue, prop_or_datatype: str, pp: PropertyPattern, who: str)->bool:
        return self.validate_value_string(rownum, kgtk_value.value, prop_or_datatype, pp, who)

    def validate_value_string(self, rownum: int, item: str, prop_or_datatype: str, pp: PropertyPattern, who: str)->bool:
        if item not in pp.values:
            self.grouse("Row %d: the %s value '%s' is not in the list of allowed %s values for %s: %s" % (rownum, who, item, who, prop_or_datatype,
                                                                                                          KgtkFormat.LIST_SEPARATOR.join(pp.values)))
            return False
        return True        

    def validate_not_value(self, rownum: int, kgtk_value: KgtkValue, prop_or_datatype: str, pp: PropertyPattern, who: str)->bool:
        return self.validate_not_value_string(rownum, kgtk_value.value, prop_or_datatype, pp, who)

    def validate_not_value_string(self, rownum: int, item: str, prop_or_datatype: str, pp: PropertyPattern, who: str)->bool:
        if item in pp.values:
            self.grouse("Row %d: the %s value '%s' is in the list of disallowed %s values for %s: %s" % (rownum, who, item, who, prop_or_datatype,
                                                                                                         KgtkFormat.LIST_SEPARATOR.join(pp.values)))
            return False
        return True        

    def validate_pattern(self, rownum: int, kgtk_value: KgtkValue, prop_or_datatype: str, pp: PropertyPattern, who: str)->bool:
        return self.validate_pattern_string(rownum, kgtk_value.value, prop_or_datatype, pp, who)

    def validate_pattern_string(self, rownum: int, item: str, prop_or_datatype: str, pp: PropertyPattern, who: str)->bool:
        if len(pp.patterns) == 0:
            raise ValueError("Missing %s pattern for %s" % (who, prop_or_datatype))

        success: bool = False
        pattern: typing.Pattern
        for pattern in pp.patterns:
            match: typing.Optional[typing.Match] = pattern.fullmatch(item)
            if match:
                success = True
                break
        if success:
            return True

        self.grouse("Row %d: the %s value '%s' does not match the inclusion %s pattern(s) for %s" % (rownum, who, item, who, prop_or_datatype))
        return False

    def validate_not_pattern(self, rownum: int, kgtk_value: KgtkValue, prop_or_datatype: str, pp: PropertyPattern, who: str)->bool:
        return self.validate_not_pattern_string(rownum, kgtk_value.value, prop_or_datatype, pp, who)

    def validate_not_pattern_string(self, rownum: int, item: str, prop_or_datatype: str, pp: PropertyPattern, who: str)->bool:
        if len(pp.patterns) == 0:
            raise ValueError("Missing %s pattern for %s" % (who, prop_or_datatype))

        success: bool = False
        pattern: typing.Pattern
        for pattern in pp.patterns:
            match: typing.Optional[typing.Match] = pattern.fullmatch(item)
            if match:
                success = True
                break

        if not success:
            return True

        self.grouse("Row %d: the %s value '%s' matches the exclusion %s pattern(s) for %s" % (rownum, who, item, who, prop_or_datatype))
        return False

    def validate_blank(self, rownum: int, value: KgtkValue, prop_or_datatype: str, pp: PropertyPattern, who: str)->bool:
        if pp.truth:
            if not value.is_empty():
                self.grouse("Row %d: the %s value '%s' is not blank for %s" % (rownum, who, value.value, prop_or_datatype,))
                return False
        else:
            if value.is_empty():
                self.grouse("Row %d: the %s value '%s' is blank for %s" % (rownum, who, value.value, prop_or_datatype,))
                return False
        return True        

    def validate_not_blank(self, rownum: int, value: KgtkValue, prop_or_datatype: str, pp: PropertyPattern, who: str)->bool:
        if pp.truth:
            if value.is_empty():
                self.grouse("Row %d: the %s value '%s' is blank for %s" % (rownum, who, value.value, prop_or_datatype,))
                return False
        else:
            if not value.is_empty():
                self.grouse("Row %d: the %s value '%s' is not blank for %s" % (rownum, who, value.value, prop_or_datatype,))
                return False
        return True        

    def validate_field_not_blank(self, rownum: int, value: str, prop_or_datatype: str, truth: bool, who: str)->bool:
        if truth:
            if len(value) == 0:
                self.grouse("Row %d: the %s value '%s' is blank for %s" % (rownum, who, value, prop_or_datatype,))
                return False
        else:
            if len(value) != 0:
                self.grouse("Row %d: the %s value '%s' is not blank for %s" % (rownum, who, value, prop_or_datatype,))
                return False
        return True        

    def validate_minval(self, rownum: int,  node2_value: KgtkValue, prop_or_datatype: str, pp: PropertyPattern, who: str)->bool:
        if not node2_value.is_number_or_quantity(validate=True):
            return False

        if node2_value.fields is None:
            return False

        if node2_value.fields.number is None:
            return False
        number: float = float(node2_value.fields.number)

        return self.validate_minval_number(rownum, prop_or_datatype, pp.numbers[0], number)

    def validate_minval_number(self, rownum: int, prop_or_datatype: str, minval: float, number: float)->bool:
        if number < minval:
            self.grouse("Row %d: prop_or_datatype %s value %f is less than minval %f." % (rownum, prop_or_datatype, number, minval))
            return False
        return True

    def validate_maxval(self, rownum: int, node2_value: KgtkValue, prop_or_datatype: str, pp: PropertyPattern, who: str)->bool:
        if not node2_value.is_number_or_quantity(validate=True):
            return False

        if node2_value.fields is None:
            return False

        if node2_value.fields.number is None:
            return False
        number: float = float(node2_value.fields.number)

        return self.validate_maxval_number(rownum, prop_or_datatype, pp.numbers[0], number)

    def validate_maxval_number(self, rownum: int, prop_or_datatype: str, maxval: float, number: float)->bool:
        if number > maxval:
            self.grouse("Row %d: prop_or_datatype %s value %f is greater than maxval %f." % (rownum, prop_or_datatype, number, maxval))
            return False
        return True

    def validate_greater_than(self, rownum: int, node2_value: KgtkValue, prop_or_datatype: str, pp: PropertyPattern, who: str)->bool:
        if not node2_value.is_number_or_quantity(validate=True):
            return False

        if node2_value.fields is None:
            return False

        if node2_value.fields.number is None:
            return False
        number: float = float(node2_value.fields.number)
        return self.validate_greater_than_number(rownum, prop_or_datatype, pp.numbers[0], number)

    def validate_greater_than_number(self, rownum: int, prop_or_datatype: str, minval: float, number: float)->bool:
        if number <= minval:
            self.grouse("Row %d: prop_or_datatype %s value %f is not greater than %f." % (rownum, prop_or_datatype, number, minval))
            return False
        return True

    def validate_less_than(self, rownum: int, node2_value: KgtkValue, prop_or_datatype: str, pp: PropertyPattern, who: str)->bool:
        if not node2_value.is_number_or_quantity(validate=True):
            return True

        if node2_value.fields is None:
            return True

        if node2_value.fields.number is None:
            return True

        number: float = float(node2_value.fields.number)
        return self.validate_less_than_number(rownum, prop_or_datatype, pp.numbers[0], number)

    def validate_less_than_number(self, rownum: int, prop_or_datatype: str, maxval: float, number: float)->bool:
        if number >= maxval:
            self.grouse("Row %d: prop_or_datatype %s value %f is not less than %f." % (rownum, prop_or_datatype, number, maxval))
            return False
        return True

    def validate_equal_to(self, rownum: int, node2_value: KgtkValue, prop_or_datatype: str, pp: PropertyPattern, who: str)->bool:
        if not node2_value.is_number_or_quantity(validate=True):
            self.grouse("Row %d: prop_or_datatype %s value %f is not a number or quantity." % (rownum, prop_or_datatype, number))
            return False

        if node2_value.fields is None:
            self.grouse("Row %d: prop_or_datatype %s value %f is missing the parsed fields." % (rownum, prop_or_datatype, number))
            return False

        if node2_value.fields.number is None:
            self.grouse("Row %d: prop_or_datatype %s value %f is missing the number field." % (rownum, prop_or_datatype, number))
            return False

        number: float = float(node2_value.fields.number)
        return self.validate_equal_to_number(rownum, prop_or_datatype, pp.numbers, number)

    def validate_equal_to_number(self, rownum: int, prop_or_datatype: str, value_list: typing.List[float], number: float)->bool:
        value: float
        for value in value_list:
            if number == value:
                return True

        self.grouse("Row %d: prop_or_datatype %s value %f is not equal to %s." % (rownum, prop_or_datatype, number, ", ".join(["%f" % a for a in value_list])))
        return False

    def validate_not_equal_to(self, rownum: int, node2_value: KgtkValue, prop_or_datatype: str, pp: PropertyPattern, who: str)->bool:
        if not node2_value.is_number_or_quantity(validate=True):
            self.grouse("Row %d: prop_or_datatype %s value %f is not a number or quantity." % (rownum, prop_or_datatype, number))
            return False

        if node2_value.fields is None:
            self.grouse("Row %d: prop_or_datatype %s value %f is missing the parsed fields." % (rownum, prop_or_datatype, number))
            return False

        if node2_value.fields.number is None:
            self.grouse("Row %d: prop_or_datatype %s value %f is missing the number field." % (rownum, prop_or_datatype, number))
            return False

        number: float = float(node2_value.fields.number)
        return self.validate_not_equal_to_number(rownum, prop_or_datatype, pp.numbers, number)

    def validate_not_equal_to_number(self, rownum: int, prop_or_datatype: str, value_list: typing.List[float], number: float)->bool:
        value: float
        for value in value_list:
            if number == value:
                self.grouse("Row %d: prop_or_datatype %s value %f is equal to %s." % (rownum, prop_or_datatype, number, ", ".join(["%f" % a for a in value_list])))
                return False
        return True

    def convert_date(self, rownum: int, prop_or_datatype: str, node2_value: KgtkValue)->typing.Optional[PropertyPatternDate]:

        if not node2_value.is_date_and_times(validate=True):
            self.grouse("Row %d: prop_or_datatype %s value %s is not a date and times" % (rownum, prop_or_datatype, node2_value.value))
            return None

        try:
            return PropertyPatternDate.from_kv(node2_value)
        except ValueError as e:
            self.grouse("Row %d: prop_or_datatype %s: %s." % (rownum, prop_or_datatype, e.args[0]))
            return None

    def validate_mindate(self,
                         rownum: int,
                         node2_value: KgtkValue,
                         prop_or_datatype: str,
                         pp: PropertyPattern,
                         who: str,
        )->bool:
        dtvalue: typing.Optional[PropertyPatternDate] = self.convert_date(rownum, prop_or_datatype, node2_value)
        if dtvalue is None:
            return False

        if dtvalue >= pp.datetimes[0]:
            return True

        self.grouse("Row %d: prop_or_datatype %s value %s is less than mindate %s." % (rownum, prop_or_datatype, str(dtvalue), str(pp.datetimes[0])))
        return False

    def validate_maxdate(self,
                         rownum: int,
                         node2_value: KgtkValue,
                         prop_or_datatype: str,
                         pp: PropertyPattern,
                         who: str,
        )->bool:
        dtvalue: typing.Optional[PropertyPatternDate] = self.convert_date(rownum, prop_or_datatype, node2_value)
        if dtvalue is None:
            return False

        if dtvalue <= pp.datetimes[0]:
            return True
                
        self.grouse("Row %d: prop_or_datatype %s value %s is greater than maxdate %s." % (rownum, prop_or_datatype, str(dtvalue), str(pp.datetimes[0])))
        return False

    def validate_greater_than_date(self,
                                   rownum: int,
                                   node2_value: KgtkValue,
                                   prop_or_datatype: str,
                                   pp: PropertyPattern,
                                   who: str,
        )->bool:
        dtvalue: typing.Optional[PropertyPatternDate] = self.convert_date(rownum, prop_or_datatype, node2_value)
        if dtvalue is None:
            return False

        if dtvalue > pp.datetimes[0]:
            return True

        self.grouse("Row %d: prop_or_datatype %s value %s is not greater than %s." % (rownum, prop_or_datatype, str(dtvalue), str(pp.datetimes[0])))
        return False

    def validate_less_than_date(self,
                                rownum: int,
                                node2_value: KgtkValue,
                                prop_or_datatype: str,
                                pp: PropertyPattern,
                                who: str,
    )->bool:
        dtvalue: typing.Optional[PropertyPatternDate] = self.convert_date(rownum, prop_or_datatype, node2_value)
        if dtvalue is None:
            return False

        if dtvalue < pp.datetimes[0]:
            return True

        self.grouse("Row %d: prop_or_datatype %s value %s is not less than %s." % (rownum, prop_or_datatype, str(dtvalue), str(pp.datetimes[0])))
        return False

    def validate_equal_to_date(self,
                               rownum: int,
                               node2_value: KgtkValue,
                               prop_or_datatype: str,
                               pp: PropertyPattern,
                               who: str,
        )->bool:
        dtvalue: typing.Optional[PropertyPatternDate] = self.convert_date(rownum, prop_or_datatype, node2_value)
        if dtvalue is None:
            return False

        date: PropertyPatternDate
        for date in pp.datetimes:
            if dtvalue == date:
                return True
                
        self.grouse("Row %d: prop_or_datatype %s value %s is not equal to %s." % (rownum,
                                                                                  prop_or_datatype,
                                                                                  str(dtvalue),
                                                                                  ", ".join([str(date) for date in pp.datetimes])))
        return False

    def validate_not_equal_to_date(self,
                                   rownum: int,
                                   node2_value: KgtkValue,
                                   prop_or_datatype: str,
                                   pp: PropertyPattern,
                                   who: str,
    )->bool:
        dtvalue: typing.Optional[PropertyPatternDate] = self.convert_date(rownum, prop_or_datatype, node2_value)
        if dtvalue is None:
            return False

        date: PropertyPatternDate
        for date in pp.datetimes:
            if dtvalue == date:
                self.grouse("Row %d: prop_or_datatype %s value %s is equal to %s." % (rownum, prop_or_datatype, str(dtvalue), str(date)))
                return False

        return True

    def validate_chain(self, rownum: int, node2_value: KgtkValue, prop_or_datatype: str, pp: PropertyPattern, who: str)->bool:
        remote_node1: str = node2_value.value
        if remote_node1 not in self.chain_target_scoreboard:
            if self.suspended_row_groups is not None:
                if remote_node1 not in self.suspended_row_groups:
                    self.grouse("Row %d: remote node1 '%s' not found" % (rownum, remote_node1))
                    return False
            raise PropertyPatternValidator.ChainSuspensionException("Row %d: remote node1 '%s' is not ready." % (rownum, remote_node1));

        remote_datatypes: typing.Optional[typing.Set[str]] = self.chain_target_scoreboard[remote_node1]
        if remote_datatypes is None:
            self.grouse("Row %d: datatype '%s': remote node1 '%s' has no relevant datatypes'" % (rownum,
                                                                                                 KgtkFormat.LIST_SEPARATOR.join(pp.values),
                                                                                                 remote_node1))
            return False

        test_value: str
        for test_value in pp.values:
            if test_value in remote_datatypes:
                return True

        self.grouse("Row %d: datatype '%s' not in remote node1 '%s' datatypes '%s'" % (rownum,
                                                                                       KgtkFormat.LIST_SEPARATOR.join(pp.values),
                                                                                       remote_node1,
                                                                                       KgtkFormat.LIST_SEPARATOR.join(remote_datatypes)))
        return False

    def validate_field_op(self,
                          rownum: int,
                          node2_value: KgtkValue,
                          prop_or_datatype: str,
                          pp1: PropertyPattern,
                          who: str,
    )->bool:
        who = who + "_field"
        node2_value.validate()
        if node2_value.fields is None:
            self.grouse("Row %d: no fields for prop/datatype %s op %s: %s" % (rownum, prop_or_datatype, ", ".join(pp1.values), node2_value.value))
            return False
        field_value_map: typing.Mapping[str, typing.Union[str, int, float, bool]] = node2_value.fields.to_map()

        result: bool = True

        new_datatype: str
        for new_datatype in pp1.values:
            lists: PropertyPatternLists = self.pps.lists[new_datatype]
            if lists.field_names is None:
                self.grouse("Row %d: no field name for field op in %s." % (rownum, new_datatype))
                result = False
                continue
            
            field_name: str
            for field_name in lists.field_names:
                field_value: typing.Union[str, int, float, bool]
                if field_name not in field_value_map:
                    # self.grouse("Row %d: no field value for field %s in %s." % (rownum, field_name, new_datatype))
                    # result = False
                    # continue
                    field_value = "" # We can test with field_blank
                else:
                    field_value = field_value_map[field_name]

                pp: PropertyPattern
                for pp in lists.field_patterns:
                    action: PropertyPattern.Action = pp.action

                    if action == PropertyPattern.Action.FIELD_VALUES:
                        result &= self.validate_value_string(rownum, str(field_value), prop_or_datatype, pp, who)

                    elif action == PropertyPattern.Action.FIELD_NOT_VALUES:
                        result &= self.validate_not_value_string(rownum, str(field_value), prop_or_datatype, pp, who)

                    elif action == PropertyPattern.Action.FIELD_PATTERN:
                        result &= self.validate_pattern_string(rownum, str(field_value), prop_or_datatype, pp, who)

                    elif action == PropertyPattern.Action.FIELD_NOT_PATTERN:
                        result &= self.validate_not_pattern_string(rownum, str(field_value), prop_or_datatype, pp, who)

                    elif action ==  PropertyPattern.Action.FIELD_BLANK:
                        if isinstance(field_value, (str)):
                            result &= self.validate_field_not_blank(rownum, field_value, prop_or_datatype, not pp.truth, who)
                        else:
                            self.grouse("Row %d: field %s in %s is not a string." % (rownum, field_name, new_datatype))
                            result = False
                            
                    elif action == PropertyPattern.Action.FIELD_NOT_BLANK:
                        if isinstance(field_value, (str)):
                            result &= self.validate_field_not_blank(rownum, field_value, prop_or_datatype, pp.truth, who)
                        else:
                            self.grouse("Row %d: field %s in %s is not a string." % (rownum, field_name, new_datatype))
                            result = False

                    elif action == PropertyPattern.Action.MINVAL:
                        if isinstance(field_value, (int, float)):
                            result &= self.validate_minval_number(rownum, prop_or_datatype, pp.numbers[0], float(field_value))
                        else:
                            self.grouse("Row %d: field %s in %s is not a number." % (rownum, field_name, new_datatype))
                            result = False

                    elif action == PropertyPattern.Action.MAXVAL:
                        if isinstance(field_value, (int, float)):
                            result &= self.validate_maxval_number(rownum, prop_or_datatype, pp.numbers[0], float(field_value))
                        else:
                            self.grouse("Row %d: field %s in %s is not a number." % (rownum, field_name, new_datatype))
                            result = False

                    elif action == PropertyPattern.Action.GREATER_THAN:
                        if isinstance(field_value, (int, float)):
                            result &= self.validate_greater_than_number(rownum, prop_or_datatype, pp.numbers[0], float(field_value))
                        else:
                            self.grouse("Row %d: field %s in %s is not a number." % (rownum, field_name, new_datatype))
                            result = False

                    elif action == PropertyPattern.Action.LESS_THAN:
                        if isinstance(field_value, (int, float)):
                            result &= self.validate_less_than_number(rownum, prop_or_datatype, pp.numbers[0], float(field_value))
                        else:
                            self.grouse("Row %d: field %s in %s is not a number." % (rownum, field_name, new_datatype))
                            result = False

                    elif action == PropertyPattern.Action.EQUAL_TO:
                        if isinstance(field_value, (int, float)):
                            result &= self.validate_equal_to_number(rownum, prop_or_datatype, pp.numbers, float(field_value))
                        else:
                            self.grouse("Row %d: field %s in %s is not a number." % (rownum, field_name, new_datatype))
                            result = False

                    elif action == PropertyPattern.Action.NOT_EQUAL_TO:
                        if isinstance(field_value, (int, float)):
                            result &= self.validate_not_equal_to_number(rownum, prop_or_datatype, pp.numbers, float(field_value))
                        else:
                            self.grouse("Row %d: field %s in %s is not a number." % (rownum, field_name, new_datatype))
                            result = False

        return result

    def validate_node1(self,
                       rownum: int,
                       node1: str,
                       prop_or_datatype: str,
                       orig_prop: str,
                       node1_patterns: typing.List[PropertyPattern],
                       node1_allow_list: bool,
    )->bool:
        if prop_or_datatype not in self.pps.occurs and len(node1_patterns) == 0:
            return True

        node1_value = KgtkValue(node1, options=self.value_options, parse_fields=True)
        if self.autovalidate:
            if not node1_value.validate():
                self.grouse("Row %d: the node1 value '%s' is not valid KGTK." % (rownum, node1_value.value))
                return False

        return self.validate_node1_value(rownum, node1_value, prop_or_datatype, orig_prop, node1_patterns, node1_allow_list)

    def validate_node1_value(self,
                             rownum: int,
                             node1_value: KgtkValue,
                             prop_or_datatype: str,
                             orig_prop: str,
                             node1_patterns: typing.List[PropertyPattern],
                             node1_allow_list: bool,
    )->bool:
        result: bool = True

        if node1_value.is_list():
            if not node1_allow_list:
                self.grouse("Row %d: The node1 value '%s' is not allowed to be a list." % (rownum, node1_value.value))
                return False

            # Validate each item on the list seperately.
            list_item: KgtkValue
            for list_item in node1_value.get_list_items():
                result &= self.validate_node1_value(rownum, list_item, prop_or_datatype, orig_prop, node1_patterns, False)
            return result

        minoccurs_limit: typing.Optional[int] = None
        maxoccurs_limit: typing.Optional[int] = None

        pp: PropertyPattern
        for pp in node1_patterns:
            action: PropertyPattern.Action = pp.action
            action_method:  typing.Optional[typing.Callable[[int, KgtkValue, str, PropertyPattern, str], bool]] = self.action_dispatcher.get(action)
            if action_method is not None:
                result &= action_method(rownum, node1_value, prop_or_datatype, pp, "node1")

            elif action == PropertyPattern.Action.MINOCCURS:
                minoccurs_limit = pp.intval

            elif action == PropertyPattern.Action.MAXOCCURS:
                maxoccurs_limit = pp.intval

        if prop_or_datatype in self.pps.occurs:
            node1: str = node1_value.value
            groupby: str = orig_prop if prop_or_datatype in self.pps.groupbyprop else prop_or_datatype
            if groupby not in self.minoccurs_limits:
                self.minoccurs_limits[groupby] = minoccurs_limit
            if groupby not in self.maxoccurs_limits:
                self.maxoccurs_limits[groupby] = maxoccurs_limit
                
            if self.occurs_scoreboard is None:
                self.occurs_scoreboard = dict()

            if node1 not in self.occurs_scoreboard:
                self.occurs_scoreboard[node1] = { }
            if groupby in self.occurs_scoreboard[node1]:
                self.occurs_scoreboard[node1][groupby] += 1
            else:
                self.occurs_scoreboard[node1][groupby] = 1

        return result

    def validate_node2(self,
                       rownum: int,
                       node2: str,
                       prop_or_datatype: str,
                       orig_prop: str,
                       node2_patterns: typing.List[PropertyPattern],
                       node2_allow_list: bool,
    )->bool:
        node2_value = KgtkValue(node2, options=self.value_options, parse_fields=True)
        if self.autovalidate:
            if not node2_value.validate():
                self.grouse("Row %d: the node2 value '%s' is not valid KGTK." % (rownum, node2_value.value))
                return False
        return self.validate_node2_value(rownum, node2_value, prop_or_datatype, orig_prop, node2_patterns, node2_allow_list)
                
    def validate_node2_value(self,
                             rownum: int,
                             node2_value: KgtkValue,
                             prop_or_datatype: str,
                             orig_prop: str,
                             node2_patterns: typing.List[PropertyPattern],
                             node2_allow_list: bool,
    )->bool:
        result: bool = True

        if node2_value.is_list():
            if not node2_allow_list:
                self.grouse("Row %d: The node2 value '%s' is not allowed to be a list." % (rownum, node2_value.value))
                return False

            # Validate each item on the list seperately.
            list_item: KgtkValue
            for list_item in node2_value.get_list_items():
                result &= self.validate_node2_value(rownum, list_item, prop_or_datatype, orig_prop, node2_patterns, False)
            return result

        mindistinct_limit: typing.Optional[int] = None
        maxdistinct_limit: typing.Optional[int] = None

        pp: PropertyPattern
        for pp in node2_patterns:
            action: PropertyPattern.Action = pp.action
            action_method:  typing.Optional[typing.Callable[[int, KgtkValue, str, PropertyPattern, str], bool]] = self.action_dispatcher.get(action)
            if action_method is not None:
                result &= action_method(rownum, node2_value, prop_or_datatype, pp, "node2")

            elif action == PropertyPattern.Action.MINDISTINCT:
                mindistinct_limit = pp.intval

            elif action == PropertyPattern.Action.MAXDISTINCT:
                mindistinct_limit = pp.intval

        if prop_or_datatype in self.pps.distinct:
            groupby: str = orig_prop if prop_or_datatype in self.pps.groupbyprop else prop_or_datatype
            if groupby not in self.mindistinct_limits:
                self.mindistinct_limits[groupby] = mindistinct_limit
                
            if groupby not in self.maxdistinct_limits:
                self.maxdistinct_limits[groupby] = maxdistinct_limit
                
            if self.distinct_scoreboard is None:
                self.distinct_scoreboard = dict()
            if groupby not in self.distinct_scoreboard:
                self.distinct_scoreboard[groupby] = set()
            self.distinct_scoreboard[groupby].add(node2_value.value)
                
        return result

    def validate_id(self,
                    rownum: int,
                    id_item: str,
                    prop_or_datatype: str,
                    orig_prop: str,
                    id_patterns: typing.List[PropertyPattern],
                    id_allow_list: bool,
    )->bool:

        if len(id_patterns) == 0:
            return True

        id_value = KgtkValue(id_item, options=self.value_options, parse_fields=True)
        if self.autovalidate:
            if not id_value.validate():
                self.grouse("Row %d: the id value '%s' is not valid KGTK." % (rownum, id_value.value))
                return False

        return self.validate_id_value(rownum, id_value, prop_or_datatype, orig_prop, id_patterns, id_allow_list)

    def setup_action_dispatch(self):
        self.action_dispatcher[PropertyPattern.Action.NODE1_TYPE] = self.validate_type
        self.action_dispatcher[PropertyPattern.Action.NODE1_IS_VALID] = self.validate_valid
        self.action_dispatcher[PropertyPattern.Action.NODE1_VALUES] = self.validate_value
        self.action_dispatcher[PropertyPattern.Action.NODE1_PATTERN] = self.validate_pattern

        self.action_dispatcher[PropertyPattern.Action.NODE2_TYPE] = self.validate_type
        self.action_dispatcher[PropertyPattern.Action.NODE2_NOT_TYPE] = self.validate_not_type
        self.action_dispatcher[PropertyPattern.Action.NODE2_IS_VALID] = self.validate_valid
        self.action_dispatcher[PropertyPattern.Action.NODE2_VALUES] = self.validate_value
        self.action_dispatcher[PropertyPattern.Action.NODE2_NOT_VALUES] = self.validate_not_value
        self.action_dispatcher[PropertyPattern.Action.NODE2_PATTERN] = self.validate_pattern
        self.action_dispatcher[PropertyPattern.Action.NODE2_NOT_PATTERN] = self.validate_not_pattern
        self.action_dispatcher[PropertyPattern.Action.NODE2_BLANK] = self.validate_blank
        self.action_dispatcher[PropertyPattern.Action.NODE2_NOT_BLANK] = self.validate_not_blank
        self.action_dispatcher[PropertyPattern.Action.MINVAL] = self.validate_minval
        self.action_dispatcher[PropertyPattern.Action.MAXVAL] = self.validate_maxval
        self.action_dispatcher[PropertyPattern.Action.GREATER_THAN] = self.validate_greater_than
        self.action_dispatcher[PropertyPattern.Action.LESS_THAN] = self.validate_less_than
        self.action_dispatcher[PropertyPattern.Action.EQUAL_TO] = self.validate_equal_to
        self.action_dispatcher[PropertyPattern.Action.NOT_EQUAL_TO] = self.validate_not_equal_to
        self.action_dispatcher[PropertyPattern.Action.MINDATE] = self.validate_mindate
        self.action_dispatcher[PropertyPattern.Action.MAXDATE] = self.validate_maxdate
        self.action_dispatcher[PropertyPattern.Action.GREATER_THAN_DATE] = self.validate_greater_than_date
        self.action_dispatcher[PropertyPattern.Action.LESS_THAN_DATE] = self.validate_less_than_date
        self.action_dispatcher[PropertyPattern.Action.EQUAL_TO_DATE] = self.validate_equal_to_date
        self.action_dispatcher[PropertyPattern.Action.NOT_EQUAL_TO_DATE] = self.validate_not_equal_to_date
        self.action_dispatcher[PropertyPattern.Action.NODE2_FIELD_OP] = self.validate_field_op
        self.action_dispatcher[PropertyPattern.Action.NODE2_CHAIN] = self.validate_chain

        self.action_dispatcher[PropertyPattern.Action.ID_CHAIN] = self.validate_chain
        self.action_dispatcher[PropertyPattern.Action.ID_PATTERN] = self.validate_pattern
        self.action_dispatcher[PropertyPattern.Action.ID_NOT_PATTERN] = self.validate_not_pattern
        self.action_dispatcher[PropertyPattern.Action.ID_BLANK] = self.validate_blank
        self.action_dispatcher[PropertyPattern.Action.ID_NOT_BLANK] = self.validate_not_blank


    def validate_id_value(self,
                          rownum: int,
                          id_value: KgtkValue,
                          prop_or_datatype: str,
                          orig_prop: str,
                          id_patterns: typing.List[PropertyPattern],
                          id_allow_list: bool)->bool:
        result: bool = True

        if id_value.is_list():
            if not id_allow_list:
                self.grouse("Row %d: The id value '%s' is not allowed to be a list." % (rownum, id_value.value))
                return False

            # Validate each item on the list seperately.
            list_item: KgtkValue
            for list_item in id_value.get_list_items():
                result &= self.validate_id_value(rownum, list_item, prop_or_datatype, orig_prop, id_patterns, False)
            return result

        pp: PropertyPattern
        for pp in id_patterns:
            action: PropertyPattern.Action = pp.action
            action_method:  typing.Optional[typing.Callable[[int, KgtkValue, str, PropertyPattern, str], bool]] = self.action_dispatcher.get(action)
            if action_method is not None:
                result &= action_method(rownum, id_value, prop_or_datatype, pp, "id")

        return result

    def validate_isa(self, rownum: int, row: typing.List[str], prop_or_datatype: str, orig_prop: str, new_datatypes: typing.List[str])->bool:
        """
        Verify that the current record conforms to one or more datatypes.
        This introduces datatype inheritance for pattern properties.
        If multiple datatypes are specified, the row must conform to all of them.

        If you want a row to conform to one of several datatypes, use SWITCH.
        """
        save_isa_current_scoreboard: PropertyPatternValidator.ISA_SCOREBOARD_TYPE = self.isa_current_scoreboard.copy()

        build_tree: bool = self.isa_column_idx >= 0
        if build_tree and len(new_datatypes) > 1:
            self.isa_tree_scoreboard.append("->(")

        result: bool = True # Everying's good until we discover otherwise.
        first: bool = True
        new_datatype: str
        for new_datatype in new_datatypes:
            # print("row %d: new_datatype: %s isa_tree: %s" % (rownum, repr(new_datatype), repr(self.isa_tree_scoreboard)), file=sys.stderr, flush=True) # ***
            if new_datatype in self.isa_current_scoreboard:
                self.grouse("Row %d: isa loop detected with %s." % (rownum, new_datatype))
                return False

            if build_tree and len(new_datatypes) > 1:
                if first:
                    first = False
                else:
                    self.isa_tree_scoreboard.append(", ")

            valid: bool
            matched: bool
            valid, matched = self.validate_prop_or_datatype(rownum, row, new_datatype, orig_prop)
            result &= valid

            # The current ISA scoreboard is reset after each datatype to
            # prevent false loop detection, either here or in SWITCH.
            self.isa_current_scoreboard = save_isa_current_scoreboard.copy()
            
        if build_tree and len(new_datatypes) > 1:
            self.isa_tree_scoreboard.append(")")

        return result

    def validate_switch(self,
                        rownum: int, row: typing.List[str],
                        prop_or_datatype: str,
                        orig_prop: str,
                        new_datatypes: typing.List[str])->bool:

        # Save the scoreboards to prevent failed cases from permanently
        # changing the scoreboards.
        #
        # TODO: Can this be made cheaper?
        save_isa_current_scoreboard: PropertyPatternValidator.ISA_SCOREBOARD_TYPE = self.isa_current_scoreboard.copy()
        save_isa_full_scoreboard: PropertyPatternValidator.ISA_SCOREBOARD_TYPE = self.isa_full_scoreboard.copy()
        save_isa_tree_scoreboard: typing.Optional[PropertyPatternValidator.ISA_SCOREBOARD_TYPE] = \
            None if self.isa_column_idx < 0 else self.isa_tree_scoreboard.copy()
        save_occurs_scoreboard: PropertyPatternValidator.OCCURS_SCOREBOARD_TYPE = \
            copy.deepcopy(self.occurs_scoreboard) if self.occurs_scoreboard is not None else None
        save_interesting_scoreboard: PropertyPatternValidator.INTERESTING_SCOREBOARD_TYPE = \
            copy.deepcopy(self.interesting_scoreboard) if self.interesting_scoreboard is not None else None
        save_distinct_scoreboard: PropertyPatternValidator.DISTINCT_SCOREBOARD_TYPE = None
        if self.distinct_scoreboard is not None and len(self.pps.chain_targets) > 0:
            save_distinct_scoreboard = copy.deepcopy(self.distinct_scoreboard)

        save_complaints: PropertyPatternValidator.COMPLAINT_LIST_TYPE = self.complaints
        self.complaints = [ ]

        new_datatype: str
        for new_datatype in new_datatypes:

            while True: # Start of NEXTCASE loop
                if new_datatype in self.isa_current_scoreboard:
                    self.grouse("Row %d: isa loop detected with %s." % (rownum, new_datatype))
                    return False

                valid: bool
                matched: bool
                valid, matched = self.validate_prop_or_datatype(rownum, row, new_datatype, orig_prop)
                if valid:
                    # TODO: SWITCH and ISA need to coorporate on the isa_tree, or we should
                    # prohibit having both for the same datatype.
                    self.complaints = save_complaints # Forget any complaints on failed cases
                    self.isa_current_scoreboard = save_isa_current_scoreboard.copy()
                    return True

                # The case failed, restore the scoreboards.
                #
                # TODO: Can this be made cheaper?
                self.isa_current_scoreboard = save_isa_current_scoreboard.copy()
                self.isa_full_scoreboard = save_isa_full_scoreboard.copy()
                if save_isa_tree_scoreboard is not None:
                    self.isa_tree_scoreboard = save_isa_tree_scoreboard.copy()
                self.occurs_scoreboard = copy.deepcopy(save_occurs_scoreboard) if save_occurs_scoreboard is not None else None
                self.interesting_scoreboard = copy.deepcopy(save_interesting_scoreboard) if save_interesting_scoreboard is not None else None
                if self.distinct_scoreboard is None:
                    self.distinct_scoreboard = None
                else:
                    self.distinct_scoreboard = copy.deepcopy(save_distinct_scoreboard)

                newlists: typing.Optional[PropertyPatternLists] = self.pps.lists.get(new_datatype)
                if newlists is None:
                    break # no NEXTCASE
                    
                nextcase: typing.Optional[str] = newlists.nextcase
                if nextcase is None:
                    break # no NEXTCASE

                new_datatype = nextcase
                
        save_complaints.extend(self.complaints) # Retain all complaints from failed cases.
        self.complaints = save_complaints
        self.grouse("Row %d: no switch case succeeded for %s." % (rownum, prop_or_datatype))
        return False

    def get_node2_idx(self,
                      rownum: int,
                      prop_or_datatype: str,
                      column_name: typing.Optional[str],
    )->int:
        if column_name is None:
            return self.node2_idx

        if column_name in self.column_name_map:
            return self.column_name_map[column_name]
        else:
            self.grouse("Row %d: prop_or_datatype: '%s' node2 column name '%s' not found in input file." % (rownum, prop_or_datatype, column_name))
            return -1

    def validate_prop_or_datatype(self, rownum: int, row: typing.List[str], prop_or_datatype: str, orig_prop: str)->typing.Tuple[bool, bool]:
        # returns result, matched
        result: bool = True # Everying's good until we discover otherwise.

        lists: typing.Optional[PropertyPatternLists] = self.pps.lists.get(prop_or_datatype)
        if lists is None:
            return result, False
            
        self.isa_current_scoreboard.append(prop_or_datatype)
        self.isa_full_scoreboard.append(prop_or_datatype)

        if self.isa_column_idx >= 0:
            if len(self.isa_tree_scoreboard) > 0 and self.isa_tree_scoreboard[-1] not in ("->(", ", "):
                self.isa_tree_scoreboard.append("->")
            self.isa_tree_scoreboard.append(prop_or_datatype)

        action: PropertyPattern.Action

        if len(lists.label_patterns) > 0:
            pp: PropertyPattern
            for pp in lists.label_patterns:
                # TODO: Put this is a seperate method.

                # TODO: Implement lists.label_allow_list?
                action = pp.action
            
                if action == PropertyPattern.Action.REJECT and pp.truth:
                    result = False
                    self.grouse("Row %d: rejecting property '%s' based on '%s'." % (rownum, row[self.label_idx], prop_or_datatype))

                elif action == PropertyPattern.Action.LABEL_PATTERN:
                    result &= self.validate_pattern_string(rownum, row[self.label_idx], prop_or_datatype, pp, "label")

        if self.pps.do_occurs or len(lists.node1_patterns) > 0:
            result &= self.validate_node1(rownum, row[self.node1_idx], prop_or_datatype, orig_prop, lists.node1_patterns, lists.node1_allow_list)

        node2_idx: int = self.get_node2_idx(rownum, prop_or_datatype, lists.node2_column_name)
        if node2_idx >= 0:
            result &= self.validate_node2(rownum, row[node2_idx], prop_or_datatype, orig_prop, lists.node2_patterns, lists.node2_allow_list)
        else:
            result = False

        if len(lists.id_patterns) > 0:
            if self.id_idx >= 0:
                result &= self.validate_id(rownum, row[self.id_idx], prop_or_datatype, orig_prop, lists.id_patterns, lists.id_allow_list)
            else:
                # Set result to FALSE if there are ID operators but the ID column is missing.
                result = False
                
        if len(lists.isa_or_switch_patterns) > 0:
            for pp in lists.isa_or_switch_patterns:
                action = pp.action
            
                if action == PropertyPattern.Action.ISA:
                    result &= self.validate_isa(rownum, row, prop_or_datatype, orig_prop, pp.values)

                elif action == PropertyPattern.Action.SWITCH:
                    result &= self.validate_switch(rownum, row, prop_or_datatype, orig_prop, pp.values)

        return result, True

    def validate_row(self, rownum: int, row: 'PropertyPatternValidator.ROW_TYPE')->bool:
        result: bool = True # Everying's good until we discover otherwise.
        matched_any: bool = False

        self.isa_current_scoreboard.clear()
        self.isa_full_scoreboard.clear()
        self.isa_tree_scoreboard.clear()
        if len(self.pps.mustoccur) > 0:
            self.setup_mustoccur(rownum, row)

        if self.pps.not_in_columns:
            result &= self.validate_not_in_columns(rownum, row)

        prop: str = row[self.label_idx]

        valid: bool
        matched: bool
        valid, matched = self.validate_prop_or_datatype(rownum, row, prop, prop)
        result &= valid
        matched_any |= matched

    
        if len(self.pps.matches) > 0:
            datatype: str
            for datatype in sorted(self.pps.matches.keys()):
                matches_pattern: typing.Pattern
                for matches_pattern in self.pps.matches[datatype]:
                    if matches_pattern.fullmatch(prop):
                        valid, matched = self.validate_prop_or_datatype(rownum, row, datatype, prop)
                        result &= valid
                        matched_any |= matched

        if not matched_any:
            unknown_datatype: str
            for unknown_datatype in self.pps.unknown:
                valid, matched = self.validate_prop_or_datatype(rownum, row, unknown_datatype, prop)
                result &= valid

        if len(self.pps.interesting) > 0:
            if self.interesting_scoreboard is None:
                self.interesting_scoreboard = dict()
            node1: str = row[self.node1_idx]
            if node1 in self.interesting_scoreboard:
                self.interesting_scoreboard[node1].update(set(self.isa_full_scoreboard).intersection(self.pps.interesting))
            else:
                self.interesting_scoreboard[node1] = set(self.isa_full_scoreboard).intersection(self.pps.interesting)

        return result

    def setup_mustoccur(self, rownum: int, row: 'PropertyPatternValidator.ROW_TYPE'):
        if len(self.pps.mustoccur) == 0:
            return

        if self.occurs_scoreboard is None:
            self.occurs_scoreboard = dict()

        prop_or_datatype: str
        for prop_or_datatype in self.pps.mustoccur:
            node1 = row[self.node1_idx]
            if node1 not in self.occurs_scoreboard:
                self.occurs_scoreboard[node1] = { }
            if prop_or_datatype not in self.occurs_scoreboard[node1]:
                self.occurs_scoreboard[node1][prop_or_datatype] = 0

    def report_occurance_violations(self, immediately: bool = True)->bool:
        """
        Print a line when a minoccurs or maxoccurs violation happened. The results are
        ordered by node1 value, then by property.
        """
        if self.occurs_scoreboard is None:
            return True

        result: bool = True
        limit: typing.Optional[int]
        node1: str
        for node1 in sorted(self.occurs_scoreboard.keys()):
            propcounts: typing.Mapping[str, int] = self.occurs_scoreboard[node1]
            prop_or_datatype: str
            for prop_or_datatype in sorted(propcounts.keys()):
                count: int = propcounts[prop_or_datatype]

                if prop_or_datatype in self.pps.mustoccur and count == 0:
                    self.grouse("Property or datatype '%s' did not occur for node1 '%s'." % (prop_or_datatype, node1), immediately=immediately)
                    result = False                    
                    
                elif prop_or_datatype in self.minoccurs_limits:
                    limit = self.minoccurs_limits[prop_or_datatype]
                    if limit is not None and count < limit:
                        self.grouse("Property or datatype '%s' occured %d times for node1 '%s', minimum is %d." % (prop_or_datatype, count, node1, limit),
                                    immediately=immediately)
                        result = False

                if prop_or_datatype in self.maxoccurs_limits:
                    limit = self.maxoccurs_limits[prop_or_datatype]
                    if limit is not None and count > limit:
                        self.grouse("Property or datatype '%s' occured %d times for node1 '%s', maximum is %d." % (prop_or_datatype, count, node1, limit),
                                    immediately=immediately)
                        result = False
        return result

    def report_interesting_violations(self, immediately: bool = True)->bool:
        """
        Print a line when a requires or prohibits violation happened. The results are
        ordered by node1 value, then by property.
        """
        if self.interesting_scoreboard is None:
            return True

        result: bool = True
        limit: typing.Optional[int]
        node1: str
        for node1 in sorted(self.interesting_scoreboard.keys()):
            interesting_set: typing.Set[str] = self.interesting_scoreboard[node1]

            prop_or_datatype: str
            for prop_or_datatype in sorted(self.pps.requires.keys()):
                if prop_or_datatype in interesting_set:
                    missing_set: typing.Set[str] = self.pps.requires[prop_or_datatype].difference(interesting_set)
                    if len(missing_set) > 0:
                        self.grouse("Node '%s': Property or datatype '%s' requires %s." % (node1, prop_or_datatype, ", ".join(sorted(list(missing_set)))),
                                    immediately=immediately)
                        result = False                    
            for prop_or_datatype in sorted(self.pps.prohibits.keys()):
                if prop_or_datatype in interesting_set:
                    prohibited_set: typing.Set[str] = self.pps.prohibits[prop_or_datatype].intersection(interesting_set)
                    if len(prohibited_set) > 0:
                        self.grouse("Node '%s': Property or datatype '%s' prohibits %s." % (node1, prop_or_datatype, ", ".join(sorted(list(prohibited_set)))),
                                    immediately=immediately)
                        result = False                    
        return result

    def report_distinct_violations(self, immediately: bool = True)->bool:
        """
        Print a line when a mindistinct or maxdistinct violation happened. The results are
        grouped by property, then by node2 value.

        result: True if no problems, False if violations occured.
        """
        if self.distinct_scoreboard is None:
            return True

        result: bool = True
        prop_or_datatype: str
        for prop_or_datatype in sorted(self.distinct_scoreboard.keys()):
            count: int = len(self.distinct_scoreboard[prop_or_datatype])

            if prop_or_datatype in self.mindistinct_limits:
                limit = self.mindistinct_limits[prop_or_datatype]
                if limit is not None and count < limit:
                    self.grouse("Property or datatype '%s' has %d distinct node2 values, minimum is %d." % (prop_or_datatype, count, limit),
                                immediately=immediately)
                    result = False

            if prop_or_datatype in self.maxdistinct_limits:
                limit = self.maxdistinct_limits[prop_or_datatype]
                if limit is not None and count > limit:
                    self.grouse("Property or datatype '%s' has %d distinct node2 values, maximum is %d." % (prop_or_datatype, count, limit),
                                immediately=immediately)
                    result = False
        return result

    def build_isa_tree(self,
                       isa_tree_scoreboard: 'PropertyPatternValidator.ISA_SCOREBOARD_TYPE',
    )->str:
        """
        Build an ISA tree.

        """
        if len(isa_tree_scoreboard) > 0:
            return "".join(isa_tree_scoreboard)
        else:
            return ""

    def maybe_add_isa_column(self,
                             row: 'PropertyPatternValidator.ROW_TYPE',
                             isa_tree_scoreboard: 'PropertyPatternValidator.ISA_SCOREBOARD_TYPE',
    )->'PropertyPatternValidator.ROW_TYPE':
        """
        Add an ISA chain to the output file.  Unfortunately, this doesn't capture
        the complexity of the ISA tree when multiple inheritance takes place.

        """
        if self.isa_column_idx < 0:
            return row
        row = row.copy()
        isa_tree: str = self.build_isa_tree(isa_tree_scoreboard)
        if self.isa_column_idx < len(row):
            row[self.isa_column_idx] = isa_tree
        else:
            row.append(isa_tree)
        return row

    def process_node1_group(self,
                            row_group: 'PropertyPatternValidator.ROW_GROUP_TYPE',
                            node1: str,
                            okw: typing.Optional[KgtkWriter] = None,
                            rkw: typing.Optional[KgtkWriter] = None,
    )->bool:
        result: bool = True

        self.clear_node1_group()

        save_isa_tree_scoreboards: typing.MutableMapping[int, 'PropertyPatternValidator.ISA_SCOREBOARD_TYPE'] = dict()

        row_number: int
        row: PropertyPatternValidator.ROW_TYPE
        for row_number, row in row_group:
            result &= self.validate_row(row_number, row)
            # print("row %d: isa_tree_scoreboard %s" % (row_number, repr(self.isa_tree_scoreboard)), file=sys.stderr, flush=True) # ***
            save_isa_tree_scoreboards[row_number] = self.isa_tree_scoreboard.copy()

        self.show_complaints()
        result &= self.report_occurance_violations()
        result &= self.report_interesting_violations()

        if result:
            if self.interesting_scoreboard is None:
                self.chain_target_scoreboard[node1] = None
            else:
                interesting_stuff: typing.Set[str] = self.interesting_scoreboard[node1].intersection(self.pps.chain_targets)
                if len(interesting_stuff) > 0:
                    self.chain_target_scoreboard[node1] = interesting_stuff
                else:
                    self.chain_target_scoreboard[node1] = None

            self.valid_row_count += len(row_group)
            if okw is not None:
                for row_num, row in row_group:
                    # print("valid: row %d: isa_tree_scodeboard %s" % (row_num, repr(save_isa_tree_scoreboards[row_num])), file=sys.stderr, flush=True) # ***
                    row = self.maybe_add_isa_column(row, save_isa_tree_scoreboards[row_num])
                    okw.write(row)
                    self.output_row_count += 1
        else:
            if rkw is not None:
                for row_num, row in row_group:
                    # print("reject: row %d: isa_tree_scodeboard %s" % (row_num, repr(save_isa_tree_scoreboards[row_num])), file=sys.stderr, flush=True) # ***
                    row = self.maybe_add_isa_column(row, save_isa_tree_scoreboards[row_num])
                    rkw.write(row)
                    self.reject_row_count += 1
        return result

    def process_pregrouped(self,
                           ikr: KgtkReader,
                           okw: typing.Optional[KgtkWriter] = None,
                           rkw: typing.Optional[KgtkWriter] = None,
    ):
        self.start_new_suspended_row_groups()

        row_group: 'PropertyPatternValidator.ROW_GROUP_TYPE' = [ ]
        row_num: int
        previous_node1: typing.Optional[str] = None
        node1: typing.Optional[str] = None
        result: bool
        row: 'PropertyPatternValidator.ROW_TYPE'
        for row in ikr:
            self.input_row_count += 1
            node1 = row[self.node1_idx]
            if previous_node1 is not None and node1 != previous_node1:
                # We need to save the distinct scoreboard and restore it
                # on suspension. This could be expensive.
                #
                # TODO: Find a better way to do this.
                save_distinct_scoreboard: PropertyPatternValidator.DISTINCT_SCOREBOARD_TYPE = None
                if self.distinct_scoreboard is not None and len(self.pps.chain_targets) > 0:
                    save_distinct_scoreboard = copy.deepcopy(self.distinct_scoreboard)
                try:
                    self.process_node1_group(row_group, node1, okw, rkw)
                except PropertyPatternValidator.ChainSuspensionException as e:
                    self.suspend_row_group(node1, row_group)
                    self.distinct_scoreboard = save_distinct_scoreboard
                row_group.clear()
            row_group.append((self.input_row_count, row))

        if len(row_group) > 0 and node1 is not None:
            # Process the last group of rows.
            #
            # Note: the only time we wouldn't get here is if the input file
            # has no data rows.
            # We need to save the distinct scoreboard and restore it
            # on suspension. This could be expensive.
            #
            # TODO: Find a better way to do this.
            save_distinct_scoreboard2: PropertyPatternValidator.DISTINCT_SCOREBOARD_TYPE = None
            if self.distinct_scoreboard is not None and len(self.pps.chain_targets) > 0:
                save_distinct_scoreboard2 = copy.deepcopy(self.distinct_scoreboard)
            try:
                self.process_node1_group(row_group, node1, okw, rkw)
            except PropertyPatternValidator.ChainSuspensionException as e:
                self.suspend_row_group(node1, row_group)
                self.distinct_scoreboard = save_distinct_scoreboard2
                
        self.process_suspended_row_groups(okw, rkw)

    def process_sort_and_group(self,
                               ikr: KgtkReader,
                               okw: typing.Optional[KgtkWriter] = None,
                               rkw: typing.Optional[KgtkWriter] = None,
    ):
        self.start_new_suspended_row_groups()
        
        row_groups: 'PropertyPatternValidator.MAPPED_ROW_GROUPS_TYPE' = dict()
        node1: str
        row: 'PropertyPatternValidator.ROW_TYPE'
        for row in ikr:
            self.input_row_count += 1
            node1 = row[self.node1_idx]
            if node1 in row_groups:
                row_groups[node1].append((self.input_row_count, row))
            else:
                row_groups[node1] = [(self.input_row_count, row)]

        row_num: int
        for node1 in sorted(row_groups.keys()):
            row_group: 'PropertyPatternValidator.ROW_GROUP_TYPE' = row_groups[node1]
            # We need to save the distinct scoreboard and restore it
            # on suspension. This could be expensive.
            #
            # TODO: Find a better way to do this.
            save_distinct_scoreboard: 'PropertyPatternValidator.DISTINCT_SCOREBOARD_TYPE' = None
            if self.distinct_scoreboard is not None and len(self.pps.chain_targets) > 0:
                save_distinct_scoreboard = copy.deepcopy(self.distinct_scoreboard)
            try:
                self.process_node1_group(row_group, node1, okw, rkw)
            except PropertyPatternValidator.ChainSuspensionException as e:
                self.suspend_row_group(node1, row_group)
                self.distinct_scoreboard = save_distinct_scoreboard

        self.process_suspended_row_groups(okw, rkw)

    def start_new_suspended_row_groups(self):
        self.new_suspended_row_groups = dict()

    def suspend_row_group(self, node1: str, row_group: 'PropertyPatternValidator.ROW_GROUP_TYPE'):
        """This code could spill the suspended row groups to an output fle if there
        are too many of the, but we'de need to sort the external file before
        processing it.

        """
        if self.new_suspended_row_groups is None:
            self.start_new_suspended_row_groups()
        if self.new_suspended_row_groups is not None:
            self.new_suspended_row_groups[node1] = row_group

    def process_suspended_row_groups(self,
                                     okw: typing.Optional[KgtkWriter] = None,
                                     rkw: typing.Optional[KgtkWriter] = None,
    ):
        if self.new_suspended_row_groups is None:
            return
        if len(self.new_suspended_row_groups) == 0:
            return
        
        row_num: int
        row_group: 'PropertyPatternValidator.ROW_GROUP_TYPE'
        node1: str
        row: 'PropertyPatternValidator.ROW_TYPE'
        old_count: typing.Optional[int] = None

        # Stop when we don't have any more suspended row groups, or when the
        # number of suspended row groups stops decreasing.
        while len(self.new_suspended_row_groups) > 0 and (old_count is None or old_count > len(self.new_suspended_row_groups)):
            old_count = len(self.new_suspended_row_groups)
            self.suspended_row_groups = self.new_suspended_row_groups
            self.start_new_suspended_row_groups()
            for node1 in sorted(self.suspended_row_groups.keys()):
                row_group = self.suspended_row_groups[node1]
                # We need to save the distinct scoreboard and restore it
                # on suspension. This could be expensive.
                #
                # TODO: Find a better way to do this.
                save_distinct_scoreboard: PropertyPatternValidator.DISTINCT_SCOREBOARD_TYPE = None
                if self.distinct_scoreboard is not None:
                    save_distinct_scoreboard = copy.copy(self.distinct_scoreboard)
                try:
                    self.process_node1_group(row_group, node1, okw, rkw)
                except PropertyPatternValidator.ChainSuspensionException as e:
                    self.suspend_row_group(node1, row_group)
                    self.distinct_scoreboard = save_distinct_scoreboard

        if len(self.new_suspended_row_groups) > 0:
            self.grouse("There were %d unprocessed row groups due to unresolved chain requests." % (len(self.new_suspended_row_groups)), immediately=True)

            for node1 in sorted(self.new_suspended_row_groups.keys()):
                row_group = self.new_suspended_row_groups[node1]
                self.grouse("Node1 '%s': %d rows not processed due to unresolved chain requests." % (node1, len(row_group)), immediately=True)
            
                if rkw is not None:
                    for row_num, row in row_group:
                        row = self.maybe_add_isa_column(row, [])
                        rkw.write(row)
                        self.reject_row_count += 1

    def process_ungrouped(self,
                          ikr: KgtkReader,
                          okw: typing.Optional[KgtkWriter] = None,
                          rkw: typing.Optional[KgtkWriter] = None,
    ):        
        row: 'PropertyPatternValidator.ROW_TYPE'
        for row in ikr:
            self.input_row_count += 1
            result: bool = self.validate_row(self.input_row_count, row)
            self.show_complaints()
            if result:
                self.valid_row_count += 1
                if okw is not None:
                    row = self.maybe_add_isa_column(row, self.isa_tree_scoreboard)
                    okw.write(row)
                    self.output_row_count += 1
            else:
                if rkw is not None: 
                    row = self.maybe_add_isa_column(row, self.isa_tree_scoreboard)
                    rkw.write(row)
                    self.reject_row_count += 1

        self.report_occurance_violations()
        self.report_interesting_violations()

    def process(self,
                ikr: KgtkReader,
                okw: typing.Optional[KgtkWriter] = None,
                rkw: typing.Optional[KgtkWriter] = None,
    ):
        if self.reject_node1_groups:
            if self.grouped_input:
                self.process_pregrouped(ikr, okw, rkw)
            else:
                self.process_sort_and_group(ikr, okw, rkw)
        else:
            self.process_ungrouped(ikr, okw, rkw)
                
        self.report_distinct_violations()

def main():
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument("-i", "--input-file", dest="input_file", help="The input file to validate. (default stdin)", type=Path, default="-")
    parser.add_argument(      "--pattern-file", dest="pattern_file", help="The property pattern file to load.", type=Path, required=True)
    parser.add_argument("-o", "--output-file", dest="output_file", help="The output file for good records. (optional)", type=Path)
    parser.add_argument(      "--reject-file", dest="reject_file", help="The output file for bad records. (optional)", type=Path)

    parser.add_argument(      "--presorted", dest="grouped_input",
                              help="Indicate that the input has been presorted (or at least pregrouped) on the node1 column. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False, metavar="True|False")

    parser.add_argument(      "--process-node1-groups", dest="reject_node1_groups",
                              help="When True, process all records for the same node1 value " +
                              "together. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=True, metavar="True|False")

    parser.add_argument(      "--no-complaints", dest="no_complaints",
                              help="When true, do not print complaints (when rejects are expected). (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False, metavar="True|False")

    parser.add_argument(      "--complain-immediately", dest="complain_immediately",
                              help="When true, print complaints immediately (for debugging). (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False, metavar="True|False")

    parser.add_argument(      "--add-isa-column", dest="add_isa_column",
                              help="When true, add an ISA column to the output and reject files. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False, metavar="True|False")

    parser.add_argument(      "--isa-column-name", dest="isa_column_name", default="isa;node2",
                              help="The name for the ISA column. (default %(default)s)")

    parser.add_argument(      "--autovalidate", dest="autovalidate",
                              help="When true, validate node1 and node2 values before testing them. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=True, metavar="True|False")

    KgtkReader.add_debug_arguments(parser, expert=True)
    KgtkReaderOptions.add_arguments(parser, expert=True)
    KgtkValueOptions.add_arguments(parser)
    args: Namespace = parser.parse_args()

    error_file: typing.TextIO = sys.stdout if args.errors_to_stdout else sys.stderr

    # Build the option structures.
    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_args(args)
    value_options: KgtkValueOptions = KgtkValueOptions.from_args(args)

    pkr: KgtkReader = KgtkReader.open(args.pattern_file,
                                     error_file=error_file,
                                     mode=KgtkReaderMode.EDGE,
                                     options=reader_options,
                                     value_options=value_options,
                                     verbose=args.verbose,
                                     very_verbose=args.very_verbose)

    pps: PropertyPatterns = PropertyPatterns.load(pkr,
                                                  value_options,
                                                  error_file=error_file,
                                                  verbose=args.verbose,
                                                  very_verbose=args.very_verbose,
    )

    ikr: KgtkReader = KgtkReader.open(args.input_file,
                                      error_file=error_file,
                                      mode=KgtkReaderMode.EDGE,
                                      options=reader_options,
                                      value_options=value_options,
                                      verbose=args.verbose,
                                      very_verbose=args.very_verbose)

    output_column_names: typing.List[str] = [ ]
    isa_column_idx: int = -1
    if args.output_file is not None:
        output_column_names = ikr.column_names.copy()
        if args.add_isa_column:
            if args.isa_column_name in output_column_names:
                isa_column_idx = output_column_names.index(args.isa_column_name)
            else:
                isa_column_idx = len(output_column_names)
                output_column_names.append(args.isa_column_name)

    ppv: PropertyPatternValidator = PropertyPatternValidator.new(pps,
                                                                 ikr,
                                                                 grouped_input=args.grouped_input,
                                                                 reject_node1_groups=args.reject_node1_groups,
                                                                 no_complaints=args.no_complaints,
                                                                 complain_immediately=args.complain_immediately,
                                                                 isa_column_idx=isa_column_idx,
                                                                 autovalidate=args.autovalidate,
                                                                 value_options=value_options,
                                                                 error_file=error_file,
                                                                 verbose=args.verbose,
                                                                 very_verbose=args.very_verbose)
    okw: KgtkWriter = None
    if args.output_file is not None:
        okw = KgtkWriter.open(output_column_names, args.output_file)

    rkw: KgtkWriter = None
    if args.reject_file is not None:
        rkw = KgtkWriter.open(output_column_names, args.reject_file)
        

    ppv.process(ikr, okw, rkw)

    print("Read %d input rows, %d valid." % (ppv.input_row_count, ppv.valid_row_count), file=error_file, flush=True)
    if okw is not None:
        print("Wrote %d output rows." % (ppv.output_row_count), file=error_file, flush=True)
    if rkw is not None:
        print("Wrote %d reject rows." % (ppv.reject_row_count), file=error_file, flush=True)

    ikr.close()
    pkr.close()
    if okw is not None:
        okw.close()
    if rkw is not None:
        rkw.close()

if __name__ == "__main__":
    main()
