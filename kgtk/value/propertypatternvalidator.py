"""
Validate property patterns..
"""

from argparse import ArgumentParser, Namespace
import attr
import copy
from enum import Enum
from pathlib import Path
import re
import sys
import typing

from kgtk.kgtkformat import KgtkFormat
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderMode, KgtkReaderOptions
from kgtk.io.kgtkwriter import KgtkWriter
from kgtk.value.kgtkvalue import KgtkValue
from kgtk.value.kgtkvalueoptions import KgtkValueOptions

@attr.s(slots=True, frozen=True)
class PropertyPattern:
    class Action(Enum):
        NODE1_TYPE = "node1_type"
        NODE1_ALLOW_LIST = "node1_allow_list"
        NODE1_VALUES = "node1_values"
        NODE1_PATTERN = "node1_pattern"

        NODE2_COLUMN = "node2_column"
        NODE2_ALLOW_LIST = "node2_allow_list"
        NODE2_TYPE = "node2_type"
        NODE2_NOT_TYPE = "node2_not_type"
        NODE2_VALUES = "node2_values"
        NODE2_NOT_VALUES = "node2_not_values"
        NODE2_PATTERN = "node2_pattern"
        NODE2_NOT_PATTERN = "node2_not_pattern"

        NOT_IN = "not_in"

        # LABEL_COLUM = "label_column"
        MINVAL = "minval" # GE
        MAXVAL = "maxval" # LE
        GREATER_THAN = "greater_than" # GT
        LESS_THAN = "less_than" # LT
        EQUAL_TO = "equal_to" # EQ, may take a list of numbers
        NOT_EQUAL_TO = "not_equal_to" # NE, may take a list of numbers

        MUSTOCCUR = "mustoccur"
        MINOCCURS = "minoccurs"
        MAXOCCURS = "maxoccurs"

        GROUPBYPROP = "groupbyprop"
        
        ISA = "isa"
        SWITCH = "switch"
        MATCHES = "matches"
        LABEL_PATTERN = "label_pattern"
        UNKNOWN = "unknown"
        REJECT = "reject"

        MINDISTINCT = "mindistinct"
        MAXDISTINCT = "maxdistinct"

        REQUIRES = "requires"
        PROHIBITS = "prohibits"

        MINDATE = "mindate"
        MAXDATE = "maxdate"
        
    # TODO: create validators where missing:
    prop_or_datatype: str = attr.ib(validator=attr.validators.instance_of(str))
    action: Action = attr.ib()
    pattern: typing.Optional[typing.Pattern] = attr.ib()
    intval: typing.Optional[int] = attr.ib()
    numbers: typing.List[float] = attr.ib()
    column_names: typing.List[str] = attr.ib()
    values: typing.List[str] = attr.ib()
    truth: bool = attr.ib()

    # Even though the object is frozen, we can still alter lists.
    column_idxs: typing.List[int] = attr.ib(factory=list)

    @classmethod
    def new(cls, node1_value: KgtkValue, label_value: KgtkValue, node2_value: KgtkValue)->'PropertyPattern':
        prop_or_datatype = node1_value.value
        action: PropertyPattern.Action = cls.Action(label_value.value)

        kv: KgtkValue
        
        pattern: typing.Optional[typing.Pattern] = None
        intval: typing.Optional[int] = None
        numbers: typing.List[float] = [ ]
        column_names: typing.List[str] = [ ]
        values: typing.List[str] = [ ]
        truth: bool = False

        if action in (cls.Action.NODE1_PATTERN,
                      cls.Action.NODE2_PATTERN,
                      cls.Action.NODE2_NOT_PATTERN,
                      cls.Action.LABEL_PATTERN,
                      cls.Action.MATCHES):
            if node2_value.fields is None:
                raise ValueError("%s: Node2 has no fields" % (action.value)) # TODO: better complaint
            if node2_value.fields.text is None:
                raise ValueError("%s: Node2 has no text" % (action.value)) # TODO: better complaint
                
            pattern = re.compile(node2_value.fields.text)

        elif action in (cls.Action.MINOCCURS,
                        cls.Action.MAXOCCURS,
                        cls.Action.MINDISTINCT,
                        cls.Action.MAXDISTINCT):
            if node2_value.fields is None:
                raise ValueError("%s: Node2 has no fields" % (action.value)) # TODO: better complaint
            if node2_value.fields.number is None:
                raise ValueError("%s: Node2 has no number" % (action.value)) # TODO: better complaint
            intval = int(node2_value.fields.number)

        elif action in(cls.Action.MINVAL,
                       cls.Action.MAXVAL,
                       cls.Action.GREATER_THAN,
                       cls.Action.LESS_THAN,
        ):
            if node2_value.is_number_or_quantity():
                if node2_value.fields is None:
                    raise ValueError("%s: Node2 has no fields" % (action.value)) # TODO: better complaint
                if node2_value.fields.number is None:
                    raise ValueError("%s: Node2 has no number" % (action.value)) # TODO: better complaint
                numbers.append(float(node2_value.fields.number))
            else:
                raise ValueError("%s: Value '%s' is not a number or quantity" % (action.value, node2_value.value)) # TODO: better complaint

        elif action in (cls.Action.EQUAL_TO,
                        cls.Action.NOT_EQUAL_TO,):
            if node2_value.is_number_or_quantity():
                if node2_value.fields is None:
                    raise ValueError("%s: Node2 has no fields" % (action.value)) # TODO: better complaint
                if node2_value.fields.number is None:
                    raise ValueError("%s: Node2 has no number" % (action.value)) # TODO: better complaint
                numbers.append(float(node2_value.fields.number))
            elif node2_value.is_list():
                for kv in node2_value.get_list_items():
                    if kv.is_number_or_quantity():
                        if kv.fields is None:
                            raise ValueError("%s: Node2  list element has no fields" % (action.value)) # TODO: better complaint
                        if kv.fields.number is None:
                            raise ValueError("%s: Node2 list element has no number" % (action.value)) # TODO: better complaint
                        numbers.append(float(kv.fields.number))
                    else:
                        raise ValueError("%s: List value is not a number" % (action.value)) # TODO: better complaint
            else:
                raise ValueError("%s: Value '%s' is not a number or list of numbers" % (action.value, node2_value.value)) # TODO: better complaint

        elif action in (cls.Action.NOT_IN,):
            # TODO: validate that the column names are valid and get their indexes.
            if node2_value.is_symbol():
                column_names.append(node2_value.value)
            elif node2_value.is_list():
                for kv in node2_value.get_list_items():
                    if kv.is_symbol():
                        column_names.append(kv.value)
                    else:
                        raise ValueError("%s: List value is not a symbol" % (action.value)) # TODO: better complaint
            else:
                raise ValueError("%s: Value '%s' is not a symbol or list of symbols" % (action.value, node2_value.value)) # TODO: better complaint
            # TODO: validate that the column names are valid and get their indexes.

        elif action in (
                # cls.Action.LABEL_COLUM,
                cls.Action.NODE2_COLUMN,
        ):
            if label_value.is_symbol():
                column_names.append(node2_value.value)
            else:
                raise ValueError("%s:Value is not a symbol" % (action.value)) # TODO: better complaint
            # TODO: validate that the column names are valid and get their indexes.

        elif action in (cls.Action.NODE1_TYPE,
                        cls.Action.NODE2_TYPE,
                        cls.Action.NODE2_NOT_TYPE,
                        cls.Action.ISA,
                        cls.Action.SWITCH,
                        cls.Action.REQUIRES,
                        cls.Action.PROHIBITS,
        ):
            if node2_value.is_symbol():
                values.append(node2_value.value)
            elif node2_value.is_list():
                for kv in node2_value.get_list_items():
                    if kv.is_symbol():
                        values.append(kv.value)
                    else:
                        raise ValueError("%s: List value is not a symbol" % (action.value)) # TODO: better complaint
            else:
                raise ValueError("%s: Value '%s' is not a symbol or list of symbols" % (action.value, node2_value.value)) # TODO: better complaint

        elif action in (cls.Action.NODE1_VALUES,
                        cls.Action.NODE2_VALUES,
                        cls.Action.NODE2_NOT_VALUES,
        ):
            if node2_value.is_list():
                for kv in node2_value.get_list_items():
                    values.append(kv.value)
            else:
                values.append(node2_value.value)

        elif action in (cls.Action.NODE1_ALLOW_LIST,
                      cls.Action.NODE2_ALLOW_LIST,
                      cls.Action.MUSTOCCUR,
                      cls.Action.UNKNOWN,
                      cls.Action.REJECT,
                      cls.Action.GROUPBYPROP,
        ):
            if node2_value.is_boolean() and node2_value.fields is not None and node2_value.fields.truth is not None:
                truth = node2_value.fields.truth
            else:
                raise ValueError("%s: Value '%s' is not a boolean" % (action.value, node2_value.value)) # TODO: better complaint

        return cls(prop_or_datatype, action, pattern, intval, numbers, column_names, values, truth)

@attr.s(slots=True, frozen=True)
class PropertyPatternFactory:
    # Indices in the property pattern file:
    node1_idx: int = attr.ib(validator=attr.validators.instance_of(int))
    label_idx: int = attr.ib(validator=attr.validators.instance_of(int))
    node2_idx: int = attr.ib(validator=attr.validators.instance_of(int))

    value_options: KgtkValueOptions = attr.ib(validator=attr.validators.instance_of(KgtkValueOptions))

    verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    very_verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    def from_row(self, row: typing.List[str])->'PropertyPattern':
        node1_value: KgtkValue = KgtkValue(row[self.node1_idx], options=self.value_options, parse_fields=True)
        label_value: KgtkValue = KgtkValue(row[self.label_idx], options=self.value_options, parse_fields=True)
        node2_value: KgtkValue = KgtkValue(row[self.node2_idx], options=self.value_options, parse_fields=True)

        node1_value.validate()
        label_value.validate()
        node2_value.validate()

        return PropertyPattern.new(node1_value, label_value, node2_value)

@attr.s(slots=True, frozen=True)
class PropertyPatterns:
    patterns: typing.Mapping[str, typing.Mapping[PropertyPattern.Action, PropertyPattern]] = attr.ib()
    matches: typing.Mapping[str, typing.Pattern] = attr.ib()
    mustoccur: typing.Set[str] = attr.ib()
    occurs: typing.Set[str] = attr.ib()
    distinct: typing.Set[str] = attr.ib()
    groupbyprop: typing.Set[str] = attr.ib()
    unknown: typing.Set[str] = attr.ib()
    requires: typing.Mapping[str, typing.Set[str]] = attr.ib()
    prohibits: typing.Mapping[str, typing.Set[str]] = attr.ib()
    interesting: typing.Set[str] = attr.ib()

    @classmethod
    def load(cls, kr: KgtkReader,
             value_options: KgtkValueOptions,
             error_file: typing.TextIO = sys.stderr,
             verbose: bool = False,
             very_verbose: bool = False,
    )->'PropertyPatterns':
        patmap: typing.MutableMapping[str, typing.MutableMapping[PropertyPattern.Action, PropertyPattern]] = { }
        matches: typing.MutableMapping[str, typing.Pattern] = { }
        mustoccur: typing.Set[str] = set()
        occurs: typing.Set[str] = set()
        distinct: typing.Set[str] = set()
        groupbyprop: typing.Set[str] = set()
        unknown: typing.Set[str] = set()
        requires: typing.MutableMapping[str, typing.Set[str]] = dict()
        prohibits: typing.MutableMapping[str, typing.Set[str]] = dict()
        interesting: typing.Set[str] = set()
        
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

        row: typing.List[str]
        for row in kr:
            pp: PropertyPattern = ppf.from_row(row)
            prop_or_datatype: str = pp.prop_or_datatype
            if prop_or_datatype not in patmap:
                patmap[prop_or_datatype] = { }
            action: PropertyPattern.Action = pp.action
            if action in patmap[prop_or_datatype]:
                raise ValueError("Duplicate action record in (%s)" % "|".join(row))
            patmap[prop_or_datatype][action] = pp
            if very_verbose:
                print("loaded %s->%s" % (prop_or_datatype, action.value), file=error_file, flush=True)
            if action == PropertyPattern.Action.MATCHES and pp.pattern is not None:
                matches[prop_or_datatype] = pp.pattern
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

        return cls(patterns=patmap,
                   matches=matches,
                   mustoccur=mustoccur,
                   occurs=occurs,
                   distinct=distinct,
                   groupbyprop=groupbyprop,
                   unknown=unknown,
                   requires=requires,
                   prohibits=prohibits,
                   interesting=interesting,
        )

    def lookup(self, prop: str, action: PropertyPattern.Action)->typing.Optional[PropertyPattern]:
        if prop in self.patterns:
            if action in self.patterns[prop]:
                return self.patterns[prop][action]
        return None
        

@attr.s(slots=True, frozen=True)
class PropertyPatternValidator:
    pps: PropertyPatterns = attr.ib()

    column_names: typing.List[str] = attr.ib()
    column_name_map: typing.Mapping[str, int] = attr.ib()

    # These are the indexes in the input file:
    node1_idx: int = attr.ib()
    label_idx: int = attr.ib()
    node2_idx: int = attr.ib()

    value_options: KgtkValueOptions = attr.ib()

    error_file: typing.TextIO = attr.ib(default=sys.stderr)
    verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    very_verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    # We clear this set, getting around frozen attribute.
    isa_scoreboard: typing.Set[str] = attr.ib(factory=set)

    # The occurance counting scoreboard:
    # node1->prop->count
    occurs_scoreboard: typing.MutableMapping[str, typing.MutableMapping[str, int]] = attr.ib(factory=dict)

    # The occurs limits after ISA and GROUPBY:
    # prop->limit
    minoccurs_limits: typing.MutableMapping[str, typing.Optional[int]] = attr.ib(factory=dict)
    maxoccurs_limits: typing.MutableMapping[str, typing.Optional[int]] = attr.ib(factory=dict)

    # The distinct value counting scoreboard:
    # prop->set(values)
    distinct_scoreboard: typing.MutableMapping[str, typing.Set[str]] = attr.ib(factory=dict)

    # The distinct limits after ISA and GROUPBY:
    # prop->limit
    mindistinct_limits: typing.MutableMapping[str, typing.Optional[int]] = attr.ib(factory=dict)
    maxdistinct_limits: typing.MutableMapping[str, typing.Optional[int]] = attr.ib(factory=dict)

    # Retain interesting properties or datatypes for requires/prohibits analysis:
    # node1->set(prop_or_datatype)
    interesting_scoreboard: typing.MutableMapping[str, typing.Set[str]] = attr.ib(factory=dict)

    def validate_not_in(self, rownum: int, row: typing.List[str])->bool:
        """
        Check each column of the row to see if the contents violates a not_in relationship.
        """
        result: bool = True
        idx: int
        column_name: str
        for idx, column_name in enumerate(self.column_names):
            thing: str = row[idx]
            # print("Row %d: idx=%d column_name=%s thing=%s" % (rownum, idx, column_name, thing), file=self.error_file, flush=True)
            if thing in self.pps.patterns:
                thing_patterns: typing.Mapping[PropertyPattern.Action, PropertyPattern] = self.pps.patterns[thing]
                # print("len(thing_patterns) = %d" % len(thing_patterns), file=self.error_file, flush=True)
                if PropertyPattern.Action.NOT_IN in thing_patterns:
                    column_names: typing.List[str] = thing_patterns[PropertyPattern.Action.NOT_IN].column_names
                    # print("NOT_IN columns: %s" % " ".join(column_names), file=self.error_file, flush=True)
                    if column_name in column_names:
                        print("Row %d: Found '%s' in column '%s', which is prohibited." % (rownum, thing, column_name), file=self.error_file, flush=True)
                        result = False
        return result

    def validate_type(self, rownum: int, value: KgtkValue, prop_or_datatype: str, type_list: typing.List[str], who: str, invert: bool=False)->bool:
        if value.data_type is None:
            print("Row %d: the %s value '%s' KGTK type is missing." % (rownum, who, value.value), file=self.error_file, flush=True)
            return False # regardless of invert flag

        type_name: str = value.data_type.lower()
        if not invert:
            if type_name not in type_list:
                print("Row %d: the %s KGTK datatype '%s' is not in the list of allowed %s types for %s: %s" % (rownum, who, type_name, who, prop_or_datatype,
                                                                                                               KgtkFormat.LIST_SEPARATOR.join(type_list)),
                      file=self.error_file, flush=True)
                return False
        else:
            if type_name in type_list:
                print("Row %d: the %s KGTK datatype '%s' is in the list of disallowed %s types for %s: %s" % (rownum, who, type_name, who, prop_or_datatype,
                                                                                                               KgtkFormat.LIST_SEPARATOR.join(type_list)),
                       file=self.error_file, flush=True)
                return False
        return True

    def validate_value(self, rownum: int, value: KgtkValue, prop_or_datatype: str, value_list: typing.List[str], who: str, invert: bool=False)->bool:
        if not invert:
            if value.value not in value_list:
                print("Row %d: the %s value '%s' is not in the list of allowed %s values for %s: %s" % (rownum, who, value.value, who, prop_or_datatype,
                                                                                                KgtkFormat.LIST_SEPARATOR.join(value_list)),
                      file=self.error_file, flush=True)
                return False
        else:
            if value.value in value_list:
                print("Row %d: the %s value '%s' is in the list of disallowed %s values for %s: %s" % (rownum, who, value.value, who, prop_or_datatype,
                                                                                                KgtkFormat.LIST_SEPARATOR.join(value_list)),
                      file=self.error_file, flush=True)
                return False
        return True        

    def validate_pattern(self, rownum: int, item: str, prop_or_datatype: str, pattern: typing.Optional[typing.Pattern], who: str, invert: bool=False)->bool:
        if pattern is None:
            raise ValueError("Missing %s pattern for %s" % (who, prop_or_datatype))

        match: typing.Optional[typing.Match] = pattern.fullmatch(item)

        if not invert:
            if not match:
                print("Row %d: the %s value '%s' does not match the inclusion %s pattern for %s" % (rownum, who, item, who, prop_or_datatype),
                      file=self.error_file, flush=True)
                return False
        else:
            if match:
                print("Row %d: the %s value '%s' matches the exclusion %s pattern for %s" % (rownum, who, item, who, prop_or_datatype),
                      file=self.error_file, flush=True)
                return False
        return True

    def validate_minval(self, rownum: int, prop_or_datatype: str, minval: float, node2_value: KgtkValue)->bool:
        if not node2_value.is_number_or_quantity():
            return False
        
        if node2_value.fields is None:
            return False
        
        if node2_value.fields.number is None:
            return False
        number: float = float(node2_value.fields.number)

        if number < minval:
            print("Row: %d: prop_or_datatype %s value %f is less than minval %f." % (rownum, prop_or_datatype, number, minval), file=self.error_file, flush=True)
            return False
        return True

    def validate_maxval(self, rownum: int, prop_or_datatype: str, maxval: float, node2_value: KgtkValue)->bool:
        if not node2_value.is_number_or_quantity():
            return False
        
        if node2_value.fields is None:
            return False
        
        if node2_value.fields.number is None:
            return False
        number: float = float(node2_value.fields.number)

        if number > maxval:
            print("Row: %d: prop_or_datatype %s value %f is greater than maxval %f." % (rownum, prop_or_datatype, number, maxval), file=self.error_file, flush=True)
            return False
        return True

    def validate_greater_than(self, rownum: int, prop_or_datatype: str, minval: float, node2_value: KgtkValue)->bool:
        if not node2_value.is_number_or_quantity():
            return False
        
        if node2_value.fields is None:
            return False
        
        if node2_value.fields.number is None:
            return False
        number: float = float(node2_value.fields.number)

        if number <= minval:
            print("Row: %d: prop_or_datatype %s value %f is not greater than %f." % (rownum, prop_or_datatype, number, minval), file=self.error_file, flush=True)
            return False
        return True

    def validate_less_than(self, rownum: int, prop_or_datatype: str, maxval: float, node2_value: KgtkValue)->bool:
        if not node2_value.is_number_or_quantity():
            return True
        
        if node2_value.fields is None:
            return True
        
        if node2_value.fields.number is None:
            return True
        number: float = float(node2_value.fields.number)

        if number >= maxval:
            print("Row: %d: prop_or_datatype %s value %f is not less than %f." % (rownum, prop_or_datatype, number, maxval), file=self.error_file, flush=True)
            return False
        return True

    def validate_equal_to(self, rownum: int, prop_or_datatype: str, value_list: typing.List[float], node2_value: KgtkValue)->bool:
        if not node2_value.is_number_or_quantity():
            return True
        
        if node2_value.fields is None:
            return True
        
        if node2_value.fields.number is None:
            return True
        number: float = float(node2_value.fields.number)

        value: float
        for value in value_list:
            if number == value:
                return True

        print("Row: %d: prop_or_datatype %s value %f is not equal to %s." % (rownum, prop_or_datatype, number, ", ".join(["%f" % a for a in value_list])),
                                                                             file=self.error_file, flush=True)
        return False

    def validate_not_equal_to(self, rownum: int, prop_or_datatype: str, value_list: typing.List[float], node2_value: KgtkValue)->bool:
        if not node2_value.is_number_or_quantity():
            return True
        
        if node2_value.fields is None:
            return True
        
        if node2_value.fields.number is None:
            return True
        number: float = float(node2_value.fields.number)

        value: float
        for value in value_list:
            if number != value:
              print("Row: %d: prop_or_datatype %s value %f is equal to %s." % (rownum, prop_or_datatype, number, ", ".join(["%f" % a for a in value_list])),
                                                                               file=self.error_file, flush=True)
              return False
        return True

    def validate_node1(self,
                       rownum: int,
                       node1: str,
                       prop_or_datatype: str,
                       orig_prop: str,
                       pats: typing.Mapping[PropertyPattern.Action, PropertyPattern])->bool:
        node1_value = KgtkValue(node1, options=self.value_options, parse_fields=True)
        if node1_value.validate():
            return self.validate_node1_value(rownum, node1_value, prop_or_datatype, orig_prop, pats)
        else:
            print("Row %d: the node1 value '%s' is not valid KGTK." % (rownum, node1_value.value), file=self.error_file, flush=True)
            return False

    def validate_node1_value(self,
                             rownum: int,
                             node1_value: KgtkValue,
                             prop_or_datatype: str,
                             orig_prop: str,
                             pats: typing.Mapping[PropertyPattern.Action, PropertyPattern])->bool:
        result: bool = True

        if node1_value.is_list():
            if PropertyPattern.Action.NODE1_ALLOW_LIST in pats and pats[PropertyPattern.Action.NODE1_ALLOW_LIST].truth:
                # Validate each item on the list seperately.
                list_item: KgtkValue
                for list_item in node1_value.get_list_items():
                    result &= self.validate_node1_value(rownum, list_item, prop_or_datatype, orig_prop, pats)
                return result
            else:
                print("Row %d: The node1 value '%s' is not allowed to be a list." % (rownum, node1_value.value), file=self.error_file, flush=True)
                return False

        if PropertyPattern.Action.NODE1_TYPE in pats:
            result &= self.validate_type(rownum, node1_value, prop_or_datatype, pats[PropertyPattern.Action.NODE1_TYPE].values, "node1")

        if PropertyPattern.Action.NODE1_VALUES in pats:
            result &= self.validate_value(rownum, node1_value, prop_or_datatype, pats[PropertyPattern.Action.NODE1_VALUES].values, "node1")

        if PropertyPattern.Action.NODE1_PATTERN in pats:
            result &= self.validate_pattern(rownum, node1_value.value, prop_or_datatype, pats[PropertyPattern.Action.NODE1_PATTERN].pattern, "node1")

        if prop_or_datatype in self.pps.occurs:
            groupby: str = orig_prop if prop_or_datatype in self.pps.groupbyprop else prop_or_datatype
            if groupby not in self.minoccurs_limits:
                if PropertyPattern.Action.MINOCCURS in pats and pats[PropertyPattern.Action.MINOCCURS].intval is not None:
                    self.minoccurs_limits[groupby] = pats[PropertyPattern.Action.MAXOCCURS].intval
                else:
                    self.minoccurs_limits[groupby] = None
                    
            if groupby not in self.maxoccurs_limits:
                if PropertyPattern.Action.MAXOCCURS in pats and pats[PropertyPattern.Action.MAXOCCURS].intval is not None:
                    self.maxoccurs_limits[groupby] = pats[PropertyPattern.Action.MAXOCCURS].intval
                else:
                    self.maxoccurs_limits[groupby] = None
                    
            if node1_value.value not in self.occurs_scoreboard:
                self.occurs_scoreboard[node1_value.value] = { }
            if prop_or_datatype in self.occurs_scoreboard[node1_value.value]:
                self.occurs_scoreboard[node1_value.value][groupby] += 1
            else:
                self.occurs_scoreboard[node1_value.value][groupby] = 1

        return result

    def validate_node2(self,
                       rownum: int,
                       node2: str,
                       prop_or_datatype: str,
                       orig_prop: str,
                       pats: typing.Mapping[PropertyPattern.Action, PropertyPattern])->bool:
        node2_value = KgtkValue(node2, options=self.value_options, parse_fields=True)
        if node2_value.validate():
            return self.validate_node2_value(rownum, node2_value, prop_or_datatype, orig_prop, pats)
        else:
            print("Row %d: the node2 value '%s' is not valid KGTK." % (rownum, node2_value.value), file=self.error_file, flush=True)
            return False

    def validate_node2_value(self,
                             rownum: int,
                             node2_value: KgtkValue,
                             prop_or_datatype: str,
                             orig_prop: str,
                             pats: typing.Mapping[PropertyPattern.Action, PropertyPattern])->bool:
        result: bool = True

        if node2_value.is_list():
            if PropertyPattern.Action.NODE2_ALLOW_LIST in pats and pats[PropertyPattern.Action.NODE2_ALLOW_LIST].truth:
                # Validate each item on the list seperately.
                list_item: KgtkValue
                for list_item in node2_value.get_list_items():
                    result &= self.validate_node2_value(rownum, list_item, prop_or_datatype, orig_prop, pats)
                return result
            else:
                print("Row %d: The node2 value '%s' is not allowed to be a list." % (rownum, node2_value.value), file=self.error_file, flush=True)
                return False

        if PropertyPattern.Action.NODE2_TYPE in pats:
            result &= self.validate_type(rownum, node2_value, prop_or_datatype, pats[PropertyPattern.Action.NODE2_TYPE].values, "node2")

        if PropertyPattern.Action.NODE2_NOT_TYPE in pats:
            result &= self.validate_type(rownum, node2_value, prop_or_datatype, pats[PropertyPattern.Action.NODE2_NOT_TYPE].values, "node2", invert=True)

        if PropertyPattern.Action.NODE2_VALUES in pats:
            result &= self.validate_value(rownum, node2_value, prop_or_datatype, pats[PropertyPattern.Action.NODE2_VALUES].values, "node2")

        if PropertyPattern.Action.NODE2_NOT_VALUES in pats:
            result &= self.validate_value(rownum, node2_value, prop_or_datatype, pats[PropertyPattern.Action.NODE2_NOT_VALUES].values, "node2", invert=True)

        if PropertyPattern.Action.NODE2_PATTERN in pats:
            result &= self.validate_pattern(rownum, node2_value.value, prop_or_datatype, pats[PropertyPattern.Action.NODE2_PATTERN].pattern, "node2")

        if PropertyPattern.Action.NODE2_NOT_PATTERN in pats:
            result &= self.validate_pattern(rownum, node2_value.value, prop_or_datatype, pats[PropertyPattern.Action.NODE2_NOT_PATTERN].pattern, "node2", invert=True)

        if PropertyPattern.Action.MINVAL in pats:
            result &= self.validate_minval(rownum, prop_or_datatype, pats[PropertyPattern.Action.MINVAL].numbers[0], node2_value)

        if PropertyPattern.Action.MAXVAL in pats:
            result &= self.validate_maxval(rownum, prop_or_datatype, pats[PropertyPattern.Action.MAXVAL].numbers[0], node2_value)

        if PropertyPattern.Action.GREATER_THAN in pats:
            result &= self.validate_greater_than(rownum, prop_or_datatype, pats[PropertyPattern.Action.GREATER_THAN].numbers[0], node2_value)

        if PropertyPattern.Action.LESS_THAN in pats:
            result &= self.validate_less_than(rownum, prop_or_datatype, pats[PropertyPattern.Action.LESS_THAN].numbers[0], node2_value)

        if PropertyPattern.Action.EQUAL_TO in pats:
            result &= self.validate_equal_to(rownum, prop_or_datatype, pats[PropertyPattern.Action.EQUAL_TO].numbers, node2_value)

        if PropertyPattern.Action.NOT_EQUAL_TO in pats:
            result &= self.validate_not_equal_to(rownum, prop_or_datatype, pats[PropertyPattern.Action.NOT_EQUAL_TO].numbers, node2_value)

        if prop_or_datatype in self.pps.distinct:
            groupby: str = orig_prop if prop_or_datatype in self.pps.groupbyprop else prop_or_datatype
            if groupby not in self.mindistinct_limits:
                if PropertyPattern.Action.MINDISTINCT in pats and pats[PropertyPattern.Action.MINDISTINCT].intval is not None:
                    self.mindistinct_limits[groupby] = pats[PropertyPattern.Action.MAXDISTINCT].intval
                else:
                    self.mindistinct_limits[groupby] = None
                    
            if groupby not in self.maxdistinct_limits:
                if PropertyPattern.Action.MAXDISTINCT in pats and pats[PropertyPattern.Action.MAXDISTINCT].intval is not None:
                    self.maxdistinct_limits[groupby] = pats[PropertyPattern.Action.MAXDISTINCT].intval
                else:
                    self.maxdistinct_limits[groupby] = None
                    
            if groupby not in self.distinct_scoreboard:
                self.distinct_scoreboard[groupby] = set()
            self.distinct_scoreboard[groupby].add(node2_value.value)
        
        return result

    def validate_isa(self, rownum: int, row: typing.List[str], prop_or_datatype: str, orig_prop: str, new_datatypes: typing.List[str])->bool:
        result: bool = True # Everying's good until we discover otherwise.
        new_datatype: str
        for new_datatype in new_datatypes:
            if new_datatype in self.isa_scoreboard:
                print("Row %d: isa loop detected with %s." % (rownum, new_datatype), file=self.error_file, flush=True)
            else:
                valid: bool
                matched: bool
                valid, matched = self.validate_prop_or_datatype(rownum, row, new_datatype, orig_prop)
                result &= valid
        return result

    def validate_switch(self, rownum: int, row: typing.List[str], prop_or_datatype: str, orig_prop: str, new_datatypes: typing.List[str])->bool:
        new_datatype: str
        for new_datatype in new_datatypes:
            if new_datatype in self.isa_scoreboard:
                print("Row %d: isa loop detected with %s." % (rownum, new_datatype), file=self.error_file, flush=True)
            else:
                save_isa_scoreboard: typing.Set[str] = self.isa_scoreboard
                valid: bool
                matched: bool
                valid, matched = self.validate_prop_or_datatype(rownum, row, new_datatype, orig_prop)
                if valid:
                    return True

                # If self weren't frozen, we could do a simple assignment:
                self.isa_scoreboard.clear()
                self.isa_scoreboard.update(save_isa_scoreboard)
        return False

    def get_idx(self,
                rownum: int,
                prop_or_datatype: str,
                action: PropertyPattern.Action,
                pats: typing.Mapping[PropertyPattern.Action, PropertyPattern],
                default_idx: int,
                who: str,
    )->int:
        if action in pats:
            column_name: str = pats[action].column_names[0]
            if column_name in self.column_name_map:
                return self.column_name_map[column_name]
            else:
                print("Row %d: prop_or_datatypep '%s' %s column name '%s' not found in input file." % (rownum, prop_or_datatype, who, column_name),
                      file=self.error_file, flush=True)
                return -1
        else:
            return default_idx        

    def validate_prop_or_datatype(self, rownum: int, row: typing.List[str], prop_or_datatype: str, orig_prop: str)->typing.Tuple[bool, bool]:
        result: bool = True # Everying's good until we discover otherwise.
        matched: bool = False

        if prop_or_datatype in self.pps.patterns:
            self.isa_scoreboard.add(prop_or_datatype)
            matched = True
            pats: typing.Mapping[PropertyPattern.Action, PropertyPattern] = self.pps.patterns[prop_or_datatype]

            if PropertyPattern.Action.REJECT in pats and pats[PropertyPattern.Action.REJECT].truth:
                print("Row %d: rejecting property '%s' based on '%s'." % (rownum, row[self.label_idx], prop_or_datatype), file=self.error_file, flush=True)

            if PropertyPattern.Action.LABEL_PATTERN in pats:
                result &= self.validate_pattern(rownum, row[self.label_idx], prop_or_datatype, pats[PropertyPattern.Action.LABEL_PATTERN].pattern, "label")

            result &= self.validate_node1(rownum, row[self.node1_idx], prop_or_datatype, orig_prop, pats)

            node2_idx: int = self.get_idx(rownum, prop_or_datatype, PropertyPattern.Action.NODE2_COLUMN, pats, self.node2_idx, "node2")
            if node2_idx >= 0:
                result &= self.validate_node2(rownum, row[node2_idx], prop_or_datatype, orig_prop, pats)
            else:
                result = False
                
            if PropertyPattern.Action.ISA in pats:
                result &= self.validate_isa(rownum, row, prop_or_datatype, orig_prop, pats[PropertyPattern.Action.ISA].values)

            if PropertyPattern.Action.SWITCH in pats:
                result &= self.validate_switch(rownum, row, prop_or_datatype, orig_prop, pats[PropertyPattern.Action.ISA].values)

        return result, matched

    def validate_row(self, rownum: int, row: typing.List[str])->bool:
        result: bool = True # Everying's good until we discover otherwise.
        matched_any: bool = False

        self.isa_scoreboard.clear()
        if len(self.pps.mustoccur) > 0:
            self.setup_mustoccur(rownum, row)

        result &= self.validate_not_in(rownum, row)

        prop: str = row[self.label_idx]

        valid: bool
        matched: bool
        valid, matched = self.validate_prop_or_datatype(rownum, row, prop, prop)
        result &= valid
        matched_any |= matched

        datatype: str
        for datatype in sorted(self.pps.matches.keys()):
            if self.pps.matches[datatype].fullmatch(prop):
                valid, matched = self.validate_prop_or_datatype(rownum, row, datatype, prop)
                result &= valid
                matched_any |= matched

        if not matched_any:
            unknown_datatype: str
            for unknown_datatype in self.pps.unknown:
                valid, matched = self.validate_prop_or_datatype(rownum, row, unknown_datatype, prop)
                result &= valid

        if len(self.pps.interesting) > 0:
            node1: str = row[self.node1_idx]
            if node1 in self.interesting_scoreboard:
                self.interesting_scoreboard[row[self.node1_idx]].update(self.isa_scoreboard.intersection(self.pps.interesting))
            else:
                self.interesting_scoreboard[row[self.node1_idx]] = self.isa_scoreboard.intersection(self.pps.interesting)

        return result

    def setup_mustoccur(self, rownum: int, row: typing.List[str]):
        prop_or_datatype: str
        for prop_or_datatype in self.pps.mustoccur:
            node1 = row[self.node1_idx]
            if node1 not in self.occurs_scoreboard:
                self.occurs_scoreboard[node1] = { }
            if prop_or_datatype not in self.occurs_scoreboard[node1]:
                self.occurs_scoreboard[node1][prop_or_datatype] = 0

    def report_occurance_violations(self)->bool:
        """
        Print a line when a minoccurs or maxoccurs violation happened. The results are
        ordered by node1 value, then by property.
        """
        result: bool = True
        limit: typing.Optional[int]
        node1: str
        for node1 in sorted(self.occurs_scoreboard.keys()):
            propcounts: typing.Mapping[str, int] = self.occurs_scoreboard[node1]
            prop_or_datatype: str
            for prop_or_datatype in sorted(propcounts.keys()):
                count: int = propcounts[prop_or_datatype]
                pats: typing.Mapping[PropertyPattern.Action, PropertyPattern] = self.pps.patterns[prop_or_datatype]

                if prop_or_datatype in self.pps.mustoccur and count == 0:
                    print("Property or datatype '%s' did not occur for node1 '%s'." % (prop_or_datatype, node1),
                          file=self.error_file, flush=True)
                    result = False                    
                    
                elif prop_or_datatype in self.minoccurs_limits:
                    limit = self.minoccurs_limits[prop_or_datatype]
                    if limit is not None and count < limit:
                        print("Property or datatype '%s' occured %d times for node1 '%s', minimum is %d." % (prop_or_datatype, count, node1, limit),
                              file=self.error_file, flush=True)
                        result = False

                if prop_or_datatype in self.maxoccurs_limits:
                    limit = self.maxoccurs_limits[prop_or_datatype]
                    if limit is not None and count > limit:
                        print("Property or datatype '%s' occured %d times for node1 '%s', maximum is %d." % (prop_or_datatype, count, node1, limit),
                              file=self.error_file, flush=True)
                        result = False
        return result

    def report_interesting_violations(self)->bool:
        """
        Print a line when a requires or prohibits violation happened. The results are
        ordered by node1 value, then by property.
        """
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
                        print("Node '%s': Property or datatype '%s' requires %s." % (node1, prop_or_datatype, ", ".join(sorted(list(missing_set)))),
                              file=self.error_file, flush=True)
                        result = False                    
            for prop_or_datatype in sorted(self.pps.prohibits.keys()):
                if prop_or_datatype in interesting_set:
                    prohibited_set: typing.Set[str] = self.pps.prohibits[prop_or_datatype].intersection(interesting_set)
                    if len(prohibited_set) > 0:
                        print("Node '%s': Property or datatype '%s' prohibits %s." % (node1, prop_or_datatype, ", ".join(sorted(list(prohibited_set)))),
                              file=self.error_file, flush=True)
                        result = False                    
        return result

    def report_distinct_violations(self)->bool:
        """
        Print a line when a mindistinct or maxdistinct violation happened. The results are
        grouped by property, then by node2 value.
        """
        result: bool = True
        prop_or_datatype: str
        for prop_or_datatype in sorted(self.distinct_scoreboard.keys()):
            count: int = len(self.distinct_scoreboard[prop_or_datatype])

            if prop_or_datatype in self.mindistinct_limits:
                limit = self.mindistinct_limits[prop_or_datatype]
                if limit is not None and count < limit:
                    print("Property or datatype '%s' has %d distinct node2 values, minimum is %d." % (prop_or_datatype, count, limit),
                          file=self.error_file, flush=True)
                    result = False

            if prop_or_datatype in self.maxdistinct_limits:
                limit = self.maxdistinct_limits[prop_or_datatype]
                if limit is not None and count < limit:
                    print("Property or datatype '%s' has %d distinct node2 values, maximum is %d." % (prop_or_datatype, count, limit),
                          file=self.error_file, flush=True)
                    result = False

        return result

    @classmethod
    def new(cls,
            pps: PropertyPatterns,
            kr: KgtkReader,
            value_options: KgtkValueOptions,
            error_file: typing.TextIO,
            verbose: bool,
            very_verbose: bool)->'PropertyPatternValidator':
        return PropertyPatternValidator(pps,
                                        kr.column_names.copy(),
                                        copy.copy(kr.column_name_map),
                                        kr.node1_column_idx,
                                        kr.label_column_idx,
                                        kr.node2_column_idx,
                                        value_options=value_options,
                                        error_file=error_file,
                                        verbose=verbose,
                                        very_verbose=very_verbose)

    def process_ungrouped(self,
                          ikr: KgtkReader,
                          okw: typing.Optional[KgtkWriter] = None,
                          rkw: typing.Optional[KgtkWriter] = None,
    )->typing.Tuple[int, int, int, int]:
        input_row_count: int = 0
        valid_row_count: int = 0
        output_row_count: int = 0
        reject_row_count: int = 0

        row: typing.List[str]
        for row in ikr:
            input_row_count += 1
            result: bool = self.validate_row(input_row_count, row)
            if result:
                valid_row_count += 1
                if okw is not None:
                    okw.write(row)
                    output_row_count += 1
            else:
                if rkw is not None:
                    rkw.write(row)
                    reject_row_count += 1

        self.report_occurance_violations()
        self.report_distinct_violations()
        self.report_interesting_violations()

        return (input_row_count, valid_row_count, output_row_count, reject_row_count)

    def process(self,
                ikr: KgtkReader,
                okw: typing.Optional[KgtkWriter] = None,
                rkw: typing.Optional[KgtkWriter] = None,
    )-> typing.Tuple[int, int, int, int]:
        return self.process_ungrouped(ikr, okw, rkw)
                

def main():
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument("-i", "--input-file", dest="input_file", help="The input file to validate. (default stdin)", type=Path, default="-")
    parser.add_argument(      "--pattern-file", dest="pattern_file", help="The property pattern file to load.", type=Path, required=True)
    parser.add_argument("-o", "--output-file", dest="output_file", help="The output file for good records. (optional)", type=Path)
    parser.add_argument(      "--reject-file", dest="reject_file", help="The output file for bad records. (optional)", type=Path)

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

    ppv: PropertyPatternValidator = PropertyPatternValidator.new(pps,
                                                                 ikr,
                                                                 value_options=value_options,
                                                                 error_file=error_file,
                                                                 verbose=args.verbose,
                                                                 very_verbose=args.very_verbose)

    okw: KgtkWriter = None
    if args.output_file is not None:
        okw = KgtkWriter.open(ikr.column_names, args.output_file)
        

    rkw: KgtkWriter = None
    if args.reject_file is not None:
        rkw = KgtkWriter.open(ikr.column_names, args.reject_file)
        

    input_row_count: int = 0
    valid_row_count: int = 0
    output_row_count: int = 0
    reject_row_count: int = 0
    input_row_count, valid_row_count, output_row_count, reject_row_count = ppv.process(ikr, okw, rkw)

    print("Read %d input rows, %d valid." % (input_row_count, valid_row_count), file=error_file, flush=True)
    if okw is not None:
        print("Wrote %d output rows." % (output_row_count), file=error_file, flush=True)
    if rkw is not None:
        print("Wrote %d reject rows." % (reject_row_count), file=error_file, flush=True)

    ikr.close()
    pkr.close()
    if okw is not None:
        okw.close()
    if rkw is not None:
        rkw.close()

if __name__ == "__main__":
    main()
