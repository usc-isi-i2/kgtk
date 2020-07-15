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
from kgtk.utils.argparsehelpers import optional_bool
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
        NEXTCASE = "nextcase"
        MATCHES = "matches"
        LABEL_PATTERN = "label_pattern"
        UNKNOWN = "unknown"
        REJECT = "reject"

        DATATYPE = "datatype"
        PROPERTY = "property"

        MINDISTINCT = "mindistinct"
        MAXDISTINCT = "maxdistinct"

        REQUIRES = "requires"
        PROHIBITS = "prohibits"

        CHAIN = "chain"

        MINDATE = "mindate"
        MAXDATE = "maxdate"
        
    # TODO: create validators where missing:
    prop_or_datatype: str = attr.ib(validator=attr.validators.instance_of(str))
    action: Action = attr.ib()
    intval: typing.Optional[int] = attr.ib()
    patterns: typing.List[typing.Pattern] = attr.ib()
    numbers: typing.List[float] = attr.ib()
    column_names: typing.List[str] = attr.ib()
    values: typing.List[str] = attr.ib()
    truth: bool = attr.ib()

    # Even though the object is frozen, we can still alter lists.
    column_idxs: typing.List[int] = attr.ib(factory=list)

    @classmethod
    def new(cls,
            node1_value: KgtkValue,
            label_value: KgtkValue,
            node2_value: KgtkValue,
            old_ppat: typing.Optional['PropertyPattern'])->'PropertyPattern':
        prop_or_datatype = node1_value.value
        action: PropertyPattern.Action = cls.Action(label_value.value)

        kv: KgtkValue
        
        intval: typing.Optional[int] = None
        patterns: typing.List[typing.Pattern] = [ ]
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
                
            patterns.append(re.compile(node2_value.fields.text))

            # Merge any existing patterns, then removed duplicates:
            if old_ppat is not None and len(old_ppat.patterns) > 0:
                patterns.extend(old_ppat.patterns)
            patterns == list(set(patterns))

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

            # Merge any existing numbers, then removed duplicates and sort:
            if old_ppat is not None and len(old_ppat.numbers) > 0:
                numbers.extend(old_ppat.numbers)
            numbers == sorted(list(set(numbers)))

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

            # Merge any existing numbers, then removed duplicates and sort:
            if old_ppat is not None and  len(old_ppat.numbers) > 0:
                numbers.extend(old_ppat.numbers)
            numbers == sorted(list(set(numbers)))

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

            # Merge any existing column names, then removed duplicates and sort:
            if old_ppat is not None and len(old_ppat.column_names) > 0:
                column_names.extend(old_ppat.column_names)
            column_names == sorted(list(set(column_names)))

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
                        cls.Action.NEXTCASE,
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

            # Merge any existing values, then removed duplicates and sort:
            if old_ppat is not None and len(old_ppat.values) > 0:
                values.extend(old_ppat.values)
            values == sorted(list(set(values)))

        elif action in (cls.Action.NODE1_VALUES,
                        cls.Action.NODE2_VALUES,
                        cls.Action.NODE2_NOT_VALUES,
                        cls.Action.CHAIN,
        ):
            if node2_value.is_list():
                for kv in node2_value.get_list_items():
                    values.append(kv.value)
            else:
                values.append(node2_value.value)

            # Merge any existing values, then removed duplicates and sort:
            if old_ppat is not None and len(old_ppat.values) > 0:
                values.extend(old_ppat.values)
            values == sorted(list(set(values)))

        elif action in (cls.Action.NODE1_ALLOW_LIST,
                      cls.Action.NODE2_ALLOW_LIST,
                      cls.Action.MUSTOCCUR,
                      cls.Action.UNKNOWN,
                      cls.Action.REJECT,
                      cls.Action.PROPERTY,
                      cls.Action.DATATYPE,
                      cls.Action.GROUPBYPROP,
        ):
            if node2_value.is_boolean() and node2_value.fields is not None and node2_value.fields.truth is not None:
                truth = node2_value.fields.truth
            else:
                raise ValueError("%s: Value '%s' is not a boolean" % (action.value, node2_value.value)) # TODO: better complaint

            # Merge any existing values, then removed duplicates and sort:
            if old_ppat is not None and len(old_ppat.values) > 0:
                values.extend(old_ppat.values)
            values == sorted(list(set(values)))

        return cls(prop_or_datatype, action, intval, patterns, numbers, column_names, values, truth)

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
                 row: typing.List[str],
                 old_ppat: typing.Optional[PropertyPattern]=None,
    )->PropertyPattern:
        node1_value: KgtkValue = KgtkValue(row[self.node1_idx], options=self.value_options, parse_fields=True)
        label_value: KgtkValue = KgtkValue(row[self.label_idx], options=self.value_options, parse_fields=True)
        node2_value: KgtkValue = KgtkValue(row[self.node2_idx], options=self.value_options, parse_fields=True)

        node1_value.validate()
        label_value.validate()
        node2_value.validate()

        return PropertyPattern.new(node1_value, label_value, node2_value, old_ppat)

@attr.s(slots=True, frozen=True)
class PropertyPatterns:
    PATTERN_MAP_TYPE = typing.Mapping[PropertyPattern.Action, PropertyPattern]

    patterns: typing.Mapping[str, PATTERN_MAP_TYPE] = attr.ib()
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
                # Rebuild the property pattern, merging lists from the prior property pattern.
                # Non-list fields will be silently overwritten.
                pp = ppf.from_row(row, old_ppat=patmap[prop_or_datatype][action])
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
            elif action == PropertyPattern.Action.CHAIN and len(pp.values) > 0:
                chain_target_set: typing.Set[str] = set(pp.values)
                chain_targets.update(chain_target_set)
                interesting.update(chain_target_set)

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
                   chain_targets=chain_targets,
        )

    def lookup(self, prop: str, action: PropertyPattern.Action)->typing.Optional[PropertyPattern]:
        if prop in self.patterns:
            if action in self.patterns[prop]:
                return self.patterns[prop][action]
        return None
        

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

    value_options: KgtkValueOptions = attr.ib()

    grouped_input: bool = attr.ib(default=False)
    reject_node1_groups: bool = attr.ib(default=False)
    complain_immediately: bool = attr.ib(default=False) # True is good for debugging.
    isa_column_idx: int = attr.ib(default=-1)

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

    @classmethod
    def new(cls,
            pps: PropertyPatterns,
            kr: KgtkReader,
            grouped_input: bool,
            reject_node1_groups: bool,
            complain_immediately: bool,
            isa_column_idx: int,
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
                                        grouped_input=grouped_input,
                                        reject_node1_groups=reject_node1_groups,
                                        complain_immediately=complain_immediately,
                                        isa_column_idx=isa_column_idx,
                                        value_options=value_options,
                                        error_file=error_file,
                                        verbose=verbose,
                                        very_verbose=very_verbose)

    def grouse(self, complaint: str, immediately: bool = False):
        if self.complain_immediately or immediately:
            # For better debugging, complain immediately:
            print("%s" % complaint, file=self.error_file, flush=True)
        else:
            self.complaints.append(complaint)

    def show_complaints(self):
        complaint: str
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
                thing_patterns: PropertyPatterns.PATTERN_MAP_TYPE = self.pps.patterns[thing]
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
            self.grouse("Row %d: the %s value '%s' KGTK type is missing." % (rownum, who, value.value))
            return False # regardless of invert flag

        type_name: str = value.data_type.lower()
        if not invert:
            if type_name not in type_list:
                self.grouse("Row %d: the %s KGTK datatype '%s' is not in the list of allowed %s types for %s: %s" % (rownum, who, type_name, who, prop_or_datatype,
                                                                                                                     KgtkFormat.LIST_SEPARATOR.join(type_list)))
                return False
        else:
            if type_name in type_list:
                self.grouse("Row %d: the %s KGTK datatype '%s' is in the list of disallowed %s types for %s: %s" % (rownum, who, type_name, who, prop_or_datatype,
                                                                                                                    KgtkFormat.LIST_SEPARATOR.join(type_list)))
                return False
        return True

    def validate_value(self, rownum: int, value: KgtkValue, prop_or_datatype: str, value_list: typing.List[str], who: str, invert: bool=False)->bool:
        if not invert:
            if value.value not in value_list:
                self.grouse("Row %d: the %s value '%s' is not in the list of allowed %s values for %s: %s" % (rownum, who, value.value, who, prop_or_datatype,
                                                                                                              KgtkFormat.LIST_SEPARATOR.join(value_list)))
                return False
        else:
            if value.value in value_list:
                self.grouse("Row %d: the %s value '%s' is in the list of disallowed %s values for %s: %s" % (rownum, who, value.value, who, prop_or_datatype,
                                                                                                KgtkFormat.LIST_SEPARATOR.join(value_list)))
                return False
        return True        

    def validate_pattern(self, rownum: int, item: str, prop_or_datatype: str, patterns: typing.List[typing.Pattern], who: str, invert: bool=False)->bool:
        if len(patterns) == 0:
            raise ValueError("Missing %s pattern for %s" % (who, prop_or_datatype))

        success: bool = False
        pattern: typing.Pattern
        for pattern in patterns:
            match: typing.Optional[typing.Match] = pattern.fullmatch(item)
            if match:
                success = True
                break

        if not invert:
            if not success:
                self.grouse("Row %d: the %s value '%s' does not match the inclusion %s pattern(s) for %s" % (rownum, who, item, who, prop_or_datatype))
                return False
        else:
            if success:
                self.grouse("Row %d: the %s value '%s' matches the exclusion %s pattern(s) for %s" % (rownum, who, item, who, prop_or_datatype))
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
            self.grouse("Row: %d: prop_or_datatype %s value %f is less than minval %f." % (rownum, prop_or_datatype, number, minval))
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
            self.grouse("Row: %d: prop_or_datatype %s value %f is greater than maxval %f." % (rownum, prop_or_datatype, number, maxval))
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
            self.grouse("Row: %d: prop_or_datatype %s value %f is not greater than %f." % (rownum, prop_or_datatype, number, minval))
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
            self.grouse("Row: %d: prop_or_datatype %s value %f is not less than %f." % (rownum, prop_or_datatype, number, maxval))
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

        self.grouse("Row: %d: prop_or_datatype %s value %f is not equal to %s." % (rownum, prop_or_datatype, number, ", ".join(["%f" % a for a in value_list])))
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
              self.grouse("Row: %d: prop_or_datatype %s value %f is equal to %s." % (rownum, prop_or_datatype, number, ", ".join(["%f" % a for a in value_list])))
              return False
        return True

    def validate_chain(self, rownum: int, remote_node1: str, prop_or_datatype: str, value_list: typing.List[str])->bool:
        if remote_node1 not in self.chain_target_scoreboard:
            if self.suspended_row_groups is not None:
                if remote_node1 not in self.suspended_row_groups:
                    self.grouse("Row %d: remote node1 '%s' not found" % (rownum, remote_node1))
                    return False
            raise PropertyPatternValidator.ChainSuspensionException("Row %d: remote node1 '%s' is not ready." % (rownum, remote_node1));

        remote_datatypes: typing.Optional[typing.Set[str]] = self.chain_target_scoreboard[remote_node1]
        if remote_datatypes is None:
            self.grouse("Row %d: datatype '%s': remote node1 '%s' has not relevant datatypes'" % (rownum,
                                                                                                  KgtkFormat.LIST_SEPARATOR.join(value_list),
                                                                                                  remote_node1))
            return False

        test_value: str
        for test_value in value_list:
            if test_value in remote_datatypes:
                return True

        self.grouse("Row %d: datatype '%s' not in remote node1 '%s' datatypes '%s'" % (rownum,
                                                                                       KgtkFormat.LIST_SEPARATOR.join(value_list),
                                                                                       remote_node1,
                                                                                       KgtkFormat.LIST_SEPARATOR.join(remote_datatypes)))
        return False

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
            self.grouse("Row %d: the node1 value '%s' is not valid KGTK." % (rownum, node1_value.value))
            return False

    def validate_node1_value(self,
                             rownum: int,
                             node1_value: KgtkValue,
                             prop_or_datatype: str,
                             orig_prop: str,
                             pats: PropertyPatterns.PATTERN_MAP_TYPE)->bool:
        result: bool = True

        if node1_value.is_list():
            if PropertyPattern.Action.NODE1_ALLOW_LIST in pats and pats[PropertyPattern.Action.NODE1_ALLOW_LIST].truth:
                # Validate each item on the list seperately.
                list_item: KgtkValue
                for list_item in node1_value.get_list_items():
                    result &= self.validate_node1_value(rownum, list_item, prop_or_datatype, orig_prop, pats)
                return result
            else:
                self.grouse("Row %d: The node1 value '%s' is not allowed to be a list." % (rownum, node1_value.value))
                return False

        if PropertyPattern.Action.NODE1_TYPE in pats:
            result &= self.validate_type(rownum, node1_value, prop_or_datatype, pats[PropertyPattern.Action.NODE1_TYPE].values, "node1")

        if PropertyPattern.Action.NODE1_VALUES in pats:
            result &= self.validate_value(rownum, node1_value, prop_or_datatype, pats[PropertyPattern.Action.NODE1_VALUES].values, "node1")

        if PropertyPattern.Action.NODE1_PATTERN in pats:
            result &= self.validate_pattern(rownum, node1_value.value, prop_or_datatype, pats[PropertyPattern.Action.NODE1_PATTERN].patterns, "node1")

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
                    
            if self.occurs_scoreboard is None:
                self.occurs_scoreboard = dict()
            item: str = node1_value.value
            if item not in self.occurs_scoreboard:
                self.occurs_scoreboard[item] = { }
            if groupby in self.occurs_scoreboard[item]:
                self.occurs_scoreboard[item][groupby] += 1
            else:
                self.occurs_scoreboard[item][groupby] = 1

        return result

    def validate_node2(self,
                       rownum: int,
                       node2: str,
                       prop_or_datatype: str,
                       orig_prop: str,
                       pats: PropertyPatterns.PATTERN_MAP_TYPE)->bool:
        node2_value = KgtkValue(node2, options=self.value_options, parse_fields=True)
        if node2_value.validate():
            return self.validate_node2_value(rownum, node2_value, prop_or_datatype, orig_prop, pats)
        else:
            self.grouse("Row %d: the node2 value '%s' is not valid KGTK." % (rownum, node2_value.value))
            return False

    def validate_node2_value(self,
                             rownum: int,
                             node2_value: KgtkValue,
                             prop_or_datatype: str,
                             orig_prop: str,
                             pats: PropertyPatterns.PATTERN_MAP_TYPE)->bool:
        result: bool = True

        if node2_value.is_list():
            if PropertyPattern.Action.NODE2_ALLOW_LIST in pats and pats[PropertyPattern.Action.NODE2_ALLOW_LIST].truth:
                # Validate each item on the list seperately.
                list_item: KgtkValue
                for list_item in node2_value.get_list_items():
                    result &= self.validate_node2_value(rownum, list_item, prop_or_datatype, orig_prop, pats)
                return result
            else:
                self.grouse("Row %d: The node2 value '%s' is not allowed to be a list." % (rownum, node2_value.value))
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
            result &= self.validate_pattern(rownum, node2_value.value, prop_or_datatype, pats[PropertyPattern.Action.NODE2_PATTERN].patterns, "node2")

        if PropertyPattern.Action.NODE2_NOT_PATTERN in pats:
            result &= self.validate_pattern(rownum, node2_value.value, prop_or_datatype, pats[PropertyPattern.Action.NODE2_NOT_PATTERN].patterns, "node2", invert=True)

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

        if PropertyPattern.Action.CHAIN in pats:
            result &= self.validate_chain(rownum, node2_value.value, prop_or_datatype, pats[PropertyPattern.Action.CHAIN].values)

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
                    
            if self.distinct_scoreboard is None:
                self.distinct_scoreboard = dict()
            if groupby not in self.distinct_scoreboard:
                self.distinct_scoreboard[groupby] = set()
            self.distinct_scoreboard[groupby].add(node2_value.value)
        
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

                pats: typing.Mapping[PropertyPattern.Action, PropertyPattern] = self.pps.patterns[new_datatype]
                if PropertyPattern.Action.NEXTCASE not in pats:
                    break # no NEXTCASE

                new_datatype = pats[PropertyPattern.Action.NEXTCASE].values[0]
                
        save_complaints.extend(self.complaints) # Retain all complaints from failed cases.
        self.complaints = save_complaints
        self.grouse("Row %d: no switch case succeeded for %s." % (rownum, prop_or_datatype))
        return False

    def get_idx(self,
                rownum: int,
                prop_or_datatype: str,
                action: PropertyPattern.Action,
                pats: PropertyPatterns.PATTERN_MAP_TYPE,
                default_idx: int,
                who: str,
    )->int:
        if action in pats:
            column_name: str = pats[action].column_names[0]
            if column_name in self.column_name_map:
                return self.column_name_map[column_name]
            else:
                self.grouse("Row %d: prop_or_datatypep '%s' %s column name '%s' not found in input file." % (rownum, prop_or_datatype, who, column_name))
                return -1
        else:
            return default_idx        

    def validate_prop_or_datatype(self, rownum: int, row: typing.List[str], prop_or_datatype: str, orig_prop: str)->typing.Tuple[bool, bool]:
        result: bool = True # Everying's good until we discover otherwise.
        matched: bool = False

        if prop_or_datatype in self.pps.patterns:
            self.isa_current_scoreboard.append(prop_or_datatype)
            self.isa_full_scoreboard.append(prop_or_datatype)

            if self.isa_column_idx >= 0:
                if len(self.isa_tree_scoreboard) > 0 and self.isa_tree_scoreboard[-1] not in ("->(", ", "):
                    self.isa_tree_scoreboard.append("->")
                self.isa_tree_scoreboard.append(prop_or_datatype)

            matched = True
            pats: PropertyPatterns.PATTERN_MAP_TYPE = self.pps.patterns[prop_or_datatype]

            if PropertyPattern.Action.REJECT in pats and pats[PropertyPattern.Action.REJECT].truth:
                result = False
                self.grouse("Row %d: rejecting property '%s' based on '%s'." % (rownum, row[self.label_idx], prop_or_datatype))

            if PropertyPattern.Action.LABEL_PATTERN in pats:
                result &= self.validate_pattern(rownum, row[self.label_idx], prop_or_datatype, pats[PropertyPattern.Action.LABEL_PATTERN].patterns, "label")

            result &= self.validate_node1(rownum, row[self.node1_idx], prop_or_datatype, orig_prop, pats)

            node2_idx: int = self.get_idx(rownum, prop_or_datatype, PropertyPattern.Action.NODE2_COLUMN, pats, self.node2_idx, "node2")
            if node2_idx >= 0:
                result &= self.validate_node2(rownum, row[node2_idx], prop_or_datatype, orig_prop, pats)
            else:
                result = False
                
            if PropertyPattern.Action.ISA in pats:
                result &= self.validate_isa(rownum, row, prop_or_datatype, orig_prop, pats[PropertyPattern.Action.ISA].values)

            if PropertyPattern.Action.SWITCH in pats:
                result &= self.validate_switch(rownum, row, prop_or_datatype, orig_prop, pats[PropertyPattern.Action.SWITCH].values)

        return result, matched

    def validate_row(self, rownum: int, row: 'PropertyPatternValidator.ROW_TYPE')->bool:
        result: bool = True # Everying's good until we discover otherwise.
        matched_any: bool = False

        self.isa_current_scoreboard.clear()
        self.isa_full_scoreboard.clear()
        self.isa_tree_scoreboard.clear()
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
        if self.isa_column_idx < len(row):
            row[self.isa_column_idx] = self.build_isa_tree(isa_tree_scoreboard)
        else:
            row.append(self.build_isa_tree(isa_tree_scoreboard))
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
            save_isa_tree_scoreboards[row_number] = self.isa_tree_scoreboard

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
                    row = self.maybe_add_isa_column(row, save_isa_tree_scoreboards[row_num])
                    okw.write(row)
                    self.output_row_count += 1
        else:
            if rkw is not None:
                for row_num, row in row_group:
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

    parser.add_argument(      "--complain-immediately", dest="complain_immediately",
                              help="When true, print complaints immediately (for debugging). (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False, metavar="True|False")

    parser.add_argument(      "--add-isa-column", dest="add_isa_column",
                              help="When true, add an ISA column to the output and reject files. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False, metavar="True|False")

    parser.add_argument(      "--isa-column-name", dest="isa_column_name", default="isa;node2",
                              help="The name for the ISA column. (default %(default)s)")

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
                                                                 complain_immediately=args.complain_immediately,
                                                                 isa_column_idx=isa_column_idx,
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
