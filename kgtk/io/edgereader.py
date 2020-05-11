"""
Read a KGTK edge file in TSV format.

TODO: Add support for alternative envelope formats, such as JSON.
"""

from argparse import ArgumentParser
import attr
from pathlib import Path
import sys
import typing

from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
from kgtk.utils.closableiter import ClosableIter
from kgtk.utils.enumnameaction import EnumNameAction
from kgtk.utils.validationaction import ValidationAction
from kgtk.value.kgtkvalueoptions import KgtkValueOptions

@attr.s(slots=True, frozen=False)
class EdgeReader(KgtkReader):

    @classmethod
    def open_edge_file(cls,
                       file_path: typing.Optional[Path],
                       error_file: typing.TextIO = sys.stderr,
                       options: typing.Optional[KgtkReaderOptions] = None,
                       value_options: typing.Optional[KgtkValueOptions] = None,
                       verbose: bool = False,
                       very_verbose: bool = False)->"EdgeReader":

        # Supply the default reader and value options:
        (options, value_options) = cls._default_options(options, value_options)

        source: ClosableIter[str] = cls._openfile(file_path, options=options, error_file=error_file, verbose=verbose)

        # Read the edge file header and split it into column names.
        header: str
        column_names: typing.List[str]
        (header, column_names) = cls._build_column_names(source, options=options, error_file=error_file, verbose=verbose)

        # Check for unsafe column names.
        cls.check_column_names(column_names,
                               header_line=header,
                               error_action=options.unsafe_column_name_action,
                               error_file=error_file)

        # Build a map from column name to column index.
        column_name_map: typing.Mapping[str, int] = cls.build_column_name_map(column_names,
                                                                              header_line=header,
                                                                              error_action=options.header_error_action,
                                                                              error_file=error_file)
        # Get the indices of the required columns.
        node1_column_idx: int
        node2_column_idx: int
        label_column_idx: int
        (node1_column_idx, node2_column_idx, label_column_idx) = cls.required_edge_columns(column_name_map,
                                                                                           header_line=header,
                                                                                           error_action=options.header_error_action,
                                                                                           error_file=error_file)

        if verbose:
            print("EdgeReader: Reading an edge file. node1=%d label=%d node2=%d" % (node1_column_idx, label_column_idx, node2_column_idx))


        return cls(file_path=file_path,
                   source=source,
                   column_names=column_names,
                   column_name_map=column_name_map,
                   column_count=len(column_names),
                   node1_column_idx=node1_column_idx,
                   node2_column_idx=node2_column_idx,
                   label_column_idx=label_column_idx,
                   error_file=error_file,
                   options=options,
                   value_options=value_options,
                   is_edge_file=True,
                   is_node_file=False,
                   verbose=verbose,
                   very_verbose=very_verbose,
        )

    def _ignore_if_blank_required_fields(self, values: typing.List[str], line: str)->bool:
        # Ignore line_action with blank node1 fields.  This code comes after
        # filling missing trailing columns, although it could be reworked
        # to come first.
        if self.options.blank_required_field_line_action != ValidationAction.PASS and self.node1_column_idx >= 0 and len(values) > self.node1_column_idx:
            node1_value: str = values[self.node1_column_idx]
            if len(node1_value) == 0 or node1_value.isspace():
                return self.exclude_line(self.options.blank_required_field_line_action, "node1 is blank", line)

        # Ignore lines with blank node2 fields:
        if self.options.blank_required_field_line_action != ValidationAction.PASS and self.node2_column_idx >= 0 and len(values) > self.node2_column_idx:
            node2_value: str = values[self.node2_column_idx]
            if len(node2_value) == 0 or node2_value.isspace():
                return self.exclude_line(self.options.blank_required_field_line_action, "node2 is blank", line)
        return False # Do not ignore this line

    def _skip_reserved_fields(self, column_name)->bool:
        if self.node1_column_idx >= 0 and column_name in self.NODE1_COLUMN_NAMES:
            return True
        if self.node2_column_idx >= 0 and column_name in self.NODE2_COLUMN_NAMES:
            return True
        if self.label_column_idx >= 0 and column_name in self.LABEL_COLUMN_NAMES:
            return True
        return False

def main():
    """
    Test the KGTK edge file reader.
    """
    parser = ArgumentParser()
    parser.add_argument(dest="kgtk_file", help="The KGTK edge file to read", type=Path, nargs="?")
    KgtkReader.add_debug_arguments(parser)
    KgtkReaderOptions.add_arguments(parser)
    KgtkValueOptions.add_arguments(parser)
    args = parser.parse_args()

    error_file: typing.TextIO = sys.stdout if args.errors_to_stdout else sys.stderr

    # Build the option structures.
    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_args(args, mode=KgtkReaderMode.EDGE)
    value_options: KgtkValueOptions = KgtkValueOptions.from_args(args)

    # Force the edge mode:
    er: EdgeReader = EdgeReader.open_edge_file(args.kgtk_file,
                                               error_file=error_file,
                                               options=reader_options,
                                               value_options=value_options,
                                               column_separator=args.column_separator,
                                               verbose=args.verbose, very_verbose=args.very_verbose)

    line_count: int = 0
    row: typing.List[str]
    for row in er:
        line_count += 1
    print("Read %d lines" % line_count)

if __name__ == "__main__":
    main()

