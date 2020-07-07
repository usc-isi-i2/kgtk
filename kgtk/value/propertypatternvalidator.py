"""
Validate property patterns..
"""

from argparse import ArgumentParser, Namespace
import attr
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
        LABEL_COLUM = "label_column"
        NODE1_COLUMN = "node1_column"
        NODE2_COLUMN = "node2_column"
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
            if label_value.is_symbol:
                column_names.append(label_value.value)
            elif label_value.is_list:
                kv: KgtkValue
                for kv in label_value.get_list_items:
                    if kv.is_symbol:
                        column_names.append(kv.value)
                    else:
                        raise ValueError("%s: List value is not a symbol" % (action.value)) # TODO: better complaint
            else:
                raise ValueError("%s:Value is not a symbol or list of symbols" % (action.value)) # TODO: better complaint
            # TODO: validate that the column names are valid and get their indexes.

        if action in (cls.Action.LABEL_COLUM,
                      cls.Action.NODE1_COLUMN,
                      cls.Action.NODE2_COLUMN,
                      cls.Action.REQUIRED_IN):
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

    error_file: typing.TextIO = attr.ib(default=sys.stderr)
    verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    very_verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

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

        return cls(patmap, error_file=error_file, verbose=verbose, very_verbose=very_verbose)

def main():
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument(      "--pattern-file", dest="pattern_file", help="The property pattern file to load.", required=True, type=Path)

    KgtkReader.add_debug_arguments(parser, expert=True)
    KgtkReaderOptions.add_arguments(parser, validate_by_default=True, expert=True)
    KgtkValueOptions.add_arguments(parser)
    args: Namespace = parser.parse_args()

    error_file: typing.TextIO = sys.stdout if args.errors_to_stdout else sys.stderr

    # Build the option structures.
    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_args(args)
    value_options: KgtkValueOptions = KgtkValueOptions.from_args(args)

    kr: KgtkReader = KgtkReader.open(args.pattern_file,
                                     error_file=error_file,
                                     mode=KgtkReaderMode.EDGE,
                                     options=reader_options,
                                     value_options=value_options,
                                     verbose=args.verbose,
                                     very_verbose=args.very_verbose)

    ppv: PropertyPatternValidator = PropertyPatternValidator.load(kr,
                                                                  value_options,
                                                                  error_file=error_file,
                                                                  verbose=args.verbose,
                                                                  very_verbose=args.very_verbose,
    )

if __name__ == "__main__":
    main()
