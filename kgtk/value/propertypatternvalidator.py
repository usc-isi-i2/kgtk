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

from kgtk.io.kgtkreader import KgtkReader, KgtkReaderMode, KgtkReaderOptions
from kgtk.value.kgtkvalue import KgtkValue
from kgtk.value.kgtkvalueoptions import KgtkValueOptions

@attr.s(slots=True, frozen=True)
class PropertyPattern:
    class Action(Enum):
        NODE1_TYPE = "node1_type"
        NODE2_TYPE = "node2_type"
        NOT_IN = "not_in"
        # LABEL_COLUM = "label_column"
        # NODE1_COLUMN = "node1_column"
        # NODE2_COLUMN = "node2_column"
        NODE1_VALUES = "node1_values"
        NODE2_VALUES = "node2_values"
        MINVAL = "minval"
        MAXVAL = "maxval"
        MINOCCURS = "minoccurs"
        MAXOCCURS = "maxoccurs"
        ISA = "isa"
        MATCHES = "matches"
        NODE1_PATTERN = "node1_pattern"
        NODE2_PATTERN = "node2_pattern"
        LABEL_PATTERN = "label_pattern"
        MINDISTINCT = "mindistinct"
        MAXDISTINCT = "maxdistinct"
        REQUIRED_IN = "required_id"
        MINDATE = "mindate"
        MAXDATE = "maxdate"
        
    # TODO: create validators where missing:
    prop_datatype: str = attr.ib(validator=attr.validators.instance_of(str))
    action: Action = attr.ib()
    pattern: typing.Optional[typing.Pattern] = attr.ib()
    intval: typing.Optional[int] = attr.ib()
    number: typing.Optional[float] = attr.ib()
    column_names: typing.List[str] = attr.ib()
    value: str = attr.ib()

    # Even though the object is frozen, we can still alter lists.
    column_idxs: typing.List[int] = attr.ib(factory=list)

    @classmethod
    def new(cls, node1_value: KgtkValue, label_value: KgtkValue, node2_value: KgtkValue)->'PropertyPattern':
        prop_datatype = node1_value.value
        action: PropertyPattern.Action = cls.Action(label_value.value)

        pattern: typing.Optional[typing.Pattern] = None
        if action in (cls.Action.NODE1_PATTERN,
                      cls.Action.NODE2_PATTERN,
                      cls.Action.LABEL_PATTERN,
                      cls.Action.MATCHES):
            if node2_value.fields is None:
                raise ValueError("%s: Node2 has no fields" % (action.value)) # TODO: better complaint
            if node2_value.fields.text is None:
                raise ValueError("%s: Node2 has no text" % (action.value)) # TODO: better complaint
                
            pattern = re.compile(node2_value.fields.text)

        intval: typing.Optional[int] = None
        if action in (cls.Action.MINOCCURS,
                      cls.Action.MAXOCCURS,
                      cls.Action.MINDISTINCT,
                      cls.Action.MAXDISTINCT):
            if node2_value.fields is None:
                raise ValueError("%s: Node2 has no fields" % (action.value)) # TODO: better complaint
            if node2_value.fields.number is None:
                raise ValueError("%s: Node2 has no number" % (action.value)) # TODO: better complaint
            intval = int(node2_value.fields.number)

        number: typing.Optional[float] = None
        if action in(cls.Action.MINVAL,
                     cls.Action.MAXVAL):
            if node2_value.fields is None:
                raise ValueError("%s: Node2 has no fields" % (action.value)) # TODO: better complaint
            if node2_value.fields.number is None:
                raise ValueError("%s: Node2 has no number" % (action.value)) # TODO: better complaint
            number = float(node2_value.fields.number)

        column_names: typing.List[str] = [ ]
        if action in (cls.Action.NOT_IN,):
            if node2_value.is_symbol:
                column_names.append(node2_value.value)
            elif node2_value.is_list:
                kv: KgtkValue
                for kv in node2_value.get_list_items:
                    if kv.is_symbol:
                        column_names.append(kv.value)
                    else:
                        raise ValueError("%s: List value is not a symbol" % (action.value)) # TODO: better complaint
            else:
                raise ValueError("%s:Value is not a symbol or list of symbols" % (action.value)) # TODO: better complaint
            # TODO: validate that the column names are valid and get their indexes.

        if action in (
                # cls.Action.LABEL_COLUM,
                # cls.Action.NODE1_COLUMN,
                # cls.Action.NODE2_COLUMN,
                cls.Action.REQUIRED_IN,):
            if label_value.is_symbol:
                column_names.append(label_value.value)
            else:
                raise ValueError("%s:Value is not a symbol" % (action.value)) # TODO: better complaint
            # TODO: validate that the column names are valid and get their indexes.

        value: str = ""
        if action in (cls.Action.NODE1_TYPE,
                      cls.Action.NODE2_TYPE,
                      cls.Action.ISA):
            value = node2_value.value
                        

        return cls(prop_datatype, action, pattern, intval, number, column_names, value)

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

        return PropertyPattern.new(node1_value, label_value, node2_value)

@attr.s(slots=True, frozen=True)
class PropertyPatternValidator:
    patterns: typing.Mapping[str, typing.Mapping[PropertyPattern.Action, PropertyPattern]] = attr.ib()

    column_names: typing.List[str] = attr.ib()
    column_name_map: typing.Mapping[str, int] = attr.ib()

    error_file: typing.TextIO = attr.ib(default=sys.stderr)
    verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    very_verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

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
            if thing in self.patterns:
                thing_patterns: typing.Mapping[PropertyPattern.Action, PropertyPattern] = self.patterns[thing]
                # print("len(thing_patterns) = %d" % len(thing_patterns), file=self.error_file, flush=True)
                if PropertyPattern.Action.NOT_IN in thing_patterns:
                    column_names: typing.List[str] = thing_patterns[PropertyPattern.Action.NOT_IN].column_names
                    # print("NOT_IN columns: %s" % " ".join(column_names), file=self.error_file, flush=True)
                    if column_name in column_names:
                        print("Row %d: Found '%s' in column '%s', which is prohibited." % (rownum, thing, column_name), file=self.error_file, flush=True)
                        result = False
        return result

    def validate(self, rownum: int, row: typing.List[str])->bool:
        result: bool = True # Everying's good until we discover otherwise.

        result &= self.validate_not_in(rownum, row)

        return result

    @classmethod
    def load(cls, kr: KgtkReader,
             value_options: KgtkValueOptions,
             error_file: typing.TextIO = sys.stderr,
             verbose: bool = False,
             very_verbose: bool = False,
    )->'PropertyPatternValidator':
        patmap: typing.MutableMapping[str, typing.MutableMapping[PropertyPattern.Action, PropertyPattern]] = { }
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
            prop_datatype: str = pp.prop_datatype
            if prop_datatype not in patmap:
                patmap[prop_datatype] = { }
            action: PropertyPattern.Action = pp.action
            if action in patmap[prop_datatype]:
                raise ValueError("Duplicate action record in (%s)" % "|".join(row))
            patmap[prop_datatype][action] = pp
            if very_verbose:
                print("loaded %s->%s" % (prop_datatype, action.value), file=error_file, flush=True)

        return cls(patmap,
                   column_names=kr.column_names.copy(),
                   column_name_map=copy.copy(kr.column_name_map), # TODO: can't use xxx.copy() because typing.Mapping not typing.Dict.
                   error_file=error_file,
                   verbose=verbose,
                   very_verbose=very_verbose)

def main():
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument(      "--input-file", dest="input_file", help="The input file to validate.", type=Path)
    parser.add_argument(      "--pattern-file", dest="pattern_file", help="The property pattern file to load.", required=True, type=Path)

    KgtkReader.add_debug_arguments(parser, expert=True)
    KgtkReaderOptions.add_arguments(parser, validate_by_default=True, expert=True)
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

    ppv: PropertyPatternValidator = PropertyPatternValidator.load(pkr,
                                                                  value_options,
                                                                  error_file=error_file,
                                                                  verbose=args.verbose,
                                                                  very_verbose=args.very_verbose,
    )

    if args.input_file is not None:
        ikr: KgtkReader = KgtkReader.open(args.input_file,
                                          error_file=error_file,
                                          mode=KgtkReaderMode.EDGE,
                                          options=reader_options,
                                          value_options=value_options,
                                          verbose=args.verbose,
                                          very_verbose=args.very_verbose)

        input_row_count: int = 0
        valid_row_count: int = 0

        row: typing.List[str]
        for row in ikr:
            input_row_count += 1
            result: bool = ppv.validate(input_row_count, row)
            if result:
                valid_row_count += 1

        print("Read %d input rows, %d valid." % (input_row_count, valid_row_count), file=error_file, flush=True)

        ikr.close()

    pkr.close()

if __name__ == "__main__":
    main()
