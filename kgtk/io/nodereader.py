"""
Read a KGTK node file in TSV format.

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
class NodeReader(KgtkReader):

    @classmethod
    def open_node_file(cls,
                       file_path: typing.Optional[Path],
                       error_file: typing.TextIO = sys.stderr,
                       options: typing.Optional[KgtkReaderOptions] = None,
                       value_options: typing.Optional[KgtkValueOptions] = None,
                       verbose: bool = False,
                       very_verbose: bool = False)->"NodeReader":

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
        # Get the index of the required column.
        id_column_idx: int = cls.required_node_column(column_name_map,
                                                      header_line=header,
                                                      error_action=options.header_error_action,
                                                      error_file=error_file)

        if verbose:
            print("NodeReader: Reading an node file. id=%d" % (id_column_idx))

        return cls(file_path=file_path,
                   source=source,
                   column_names=column_names,
                   column_name_map=column_name_map,
                   column_count=len(column_names),
                   id_column_idx=id_column_idx,
                   error_file=error_file,
                   options=options,
                   value_options=value_options,
                   is_edge_file=False,
                   is_node_file=True,
                   verbose=verbose,
                   very_verbose=very_verbose,
        )

    def _ignore_if_blank_required_fields(self, values: typing.List[str], line: str)->bool:
        # Ignore line_action with blank id fields.  This code comes after
        # filling missing trailing columns, although it could be reworked
        # to come first.
        if self.options.blank_required_field_line_action != ValidationAction.PASS and self.id_column_idx >= 0 and len(values) > self.id_column_idx:
            id_value: str = values[self.id_column_idx]
            if len(id_value) == 0 or id_value.isspace():
                return self.exclude_line(self.options.blank_required_field_line_action, "id is blank", line)
        return False # Do not ignore this line

    def _skip_reserved_fields(self, column_name)->bool:
        if self.id_column_idx >= 0 and column_name in self.ID_COLUMN_NAMES:
            return True
        return False

def main():
    """
    Test the KGTK node file reader.
    """
    parser = ArgumentParser()
    parser.add_argument(dest="kgtk_file", help="The KGTK edge file to read", type=Path, nargs="?")
    KgtkReader.add_debug_arguments(parser, validate=True)
    KgtkReaderOptions.add_arguments(parser)
    KgtkValueOptions.add_arguments(parser)
    args = parser.parse_args()

    error_file: typing.TextIO = sys.stdout if args.errors_to_stdout else sys.stderr

    # Build the option structures.
    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_args(args, mode=KgtkReaderMode.NODE)
    value_options: KgtkValueOptions = KgtkValueOptions.from_args(args)

    nr: NodeReader = NodeReader.open_edge_file(args.kgtk_file,
                                               error_file=error_file,
                                               options=reader_options,
                                               value_options=value_options,
                                               column_separator=args.column_separator,
                                               verbose=args.verbose, very_verbose=args.very_verbose)

    line_count: int = 0
    row: typing.List[str]
    for row in nr:
        line_count += 1
    print("Read %d lines" % line_count)

if __name__ == "__main__":
    main()

