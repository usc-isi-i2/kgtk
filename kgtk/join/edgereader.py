"""
Read a KGTK edge file in TSV format.

TODO: Add support for alternative envelope formats, such as JSON.
"""

from argparse import ArgumentParser
import attr
from pathlib import Path
import sys
import typing

from kgtk.join.closableiter import ClosableIter
from kgtk.join.enumnameaction import EnumNameAction
from kgtk.join.kgtkreader import KgtkReader
from kgtk.join.kgtkvalue import KgtkValueOptions, DEFAULT_KGTK_VALUE_OPTIONS
from kgtk.join.validationaction import ValidationAction

@attr.s(slots=True, frozen=False)
class EdgeReader(KgtkReader):

    @classmethod
    def open_edge_file(cls,
                       file_path: typing.Optional[Path],
                       force_column_names: typing.Optional[typing.List[str]] = None, #
                       skip_first_record: bool = False,
                       fill_short_lines: bool = False,
                       truncate_long_lines: bool = False,
                       error_file: typing.TextIO = sys.stderr,
                       error_limit: int = KgtkReader.ERROR_LIMIT_DEFAULT,
                       empty_line_action: ValidationAction = ValidationAction.EXCLUDE,
                       comment_line_action: ValidationAction = ValidationAction.EXCLUDE,
                       whitespace_line_action: ValidationAction = ValidationAction.EXCLUDE,
                       blank_node1_line_action: ValidationAction = ValidationAction.EXCLUDE,
                       blank_node2_line_action: ValidationAction = ValidationAction.EXCLUDE,
                       short_line_action: ValidationAction = ValidationAction.EXCLUDE,
                       long_line_action: ValidationAction = ValidationAction.EXCLUDE,
                       invalid_value_action: ValidationAction = ValidationAction.REPORT,
                       header_error_action: ValidationAction = ValidationAction.EXIT,
                       unsafe_column_name_action: ValidationAction = ValidationAction.REPORT,
                       value_options: KgtkValueOptions = DEFAULT_KGTK_VALUE_OPTIONS,
                       compression_type: typing.Optional[str] = None,
                       gzip_in_parallel: bool = False,
                       gzip_queue_size: int = KgtkReader.GZIP_QUEUE_SIZE_DEFAULT,
                       column_separator: str = KgtkReader.COLUMN_SEPARATOR,
                       verbose: bool = False,
                       very_verbose: bool = False)->"EdgeReader":

        source: ClosableIter[str] = cls._openfile(file_path,
                                                  compression_type=compression_type,
                                                  gzip_in_parallel=gzip_in_parallel,
                                                  gzip_queue_size=gzip_queue_size,
                                                  error_file=error_file,
                                                  verbose=verbose)

        # Read the edge file header and split it into column names.
        header: str
        column_names: typing.List[str]
        (header, column_names) = cls._build_column_names(source,
                                                         force_column_names=force_column_names,
                                                         skip_first_record=skip_first_record,
                                                         column_separator=column_separator,
                                                         error_file=error_file,
                                                         verbose=verbose)

        # Check for unsafe column names.
        cls.check_column_names(column_names,
                               header_line=header,
                               error_action=unsafe_column_name_action,
                               error_file=error_file)

        # Build a map from column name to column index.
        column_name_map: typing.Mapping[str, int] = cls.build_column_name_map(column_names,
                                                                              header_line=header,
                                                                              error_action=header_error_action,
                                                                              error_file=error_file)
        # Get the indices of the required columns.
        node1_column_idx: int
        node2_column_idx: int
        label_column_idx: int
        (node1_column_idx, node2_column_idx, label_column_idx) = cls.required_edge_columns(column_name_map,
                                                                                           header_line=header,
                                                                                           error_action=header_error_action,
                                                                                           error_file=error_file)

        if verbose:
            print("EdgeReader: Reading an edge file. node1=%d label=%d node2=%d" % (node1_column_idx, label_column_idx, node2_column_idx))


        return cls(file_path=file_path,
                   source=source,
                   column_separator=column_separator,
                   column_names=column_names,
                   column_name_map=column_name_map,
                   column_count=len(column_names),
                   node1_column_idx=node1_column_idx,
                   node2_column_idx=node2_column_idx,
                   label_column_idx=label_column_idx,
                   force_column_names=force_column_names,
                   skip_first_record=skip_first_record,
                   fill_short_lines=fill_short_lines,
                   truncate_long_lines=truncate_long_lines,
                   error_file=error_file,
                   error_limit=error_limit,
                   empty_line_action=empty_line_action,
                   comment_line_action=comment_line_action,
                   whitespace_line_action=whitespace_line_action,
                   blank_node1_line_action=blank_node1_line_action,
                   blank_node2_line_action=blank_node2_line_action,
                   short_line_action=short_line_action,
                   long_line_action=long_line_action,
                   invalid_value_action=invalid_value_action,
                   header_error_action=header_error_action,
                   unsafe_column_name_action=unsafe_column_name_action,
                   value_options=value_options,
                   compression_type=compression_type,
                   gzip_in_parallel=gzip_in_parallel,
                   gzip_queue_size=gzip_queue_size,
                   is_edge_file=True,
                   is_node_file=False,
                   verbose=verbose,
                   very_verbose=very_verbose,
        )

    def _ignore_if_blank_fields(self, values: typing.List[str], line: str)->bool:
        # Ignore line_action with blank node1 fields.  This code comes after
        # filling missing trailing columns, although it could be reworked
        # to come first.
        if self.blank_node1_line_action != ValidationAction.PASS and self.node1_column_idx >= 0 and len(values) > self.node1_column_idx:
            node1_value: str = values[self.node1_column_idx]
            if len(node1_value) == 0 or node1_value.isspace():
                return self.exclude_line(self.blank_node1_line_action, "node1 is blank", line)

        # Ignore lines with blank node2 fields:
        if self.blank_node2_line_action != ValidationAction.PASS and self.node2_column_idx >= 0 and len(values) > self.node2_column_idx:
            node2_value: str = values[self.node2_column_idx]
            if len(node2_value) == 0 or node2_value.isspace():
                return self.exclude_line(self.blank_node2_line_action, "node2 is blank", line)
        return False # Do not ignore this line

    def _skip_reserved_fields(self, column_name)->bool:
        if self.node1_column_idx >= 0 and column_name in self.NODE1_COLUMN_NAMES:
            return True
        if self.node2_column_idx >= 0 and column_name in self.NODE2_COLUMN_NAMES:
            return True
        if self.label_column_idx >= 0 and column_name in self.LABEL_COLUMN_NAMES:
            return True
        return False

    @classmethod
    def add_arguments(cls, parser: ArgumentParser):
        # super().add_arguments(parser)
        parser.add_argument(      "--blank-node1-line-action", dest="blank_node1_line_action",
                                  help="The action to take when a blank node1 field is detected.",
                                  type=ValidationAction, action=EnumNameAction, default=ValidationAction.EXCLUDE)

        parser.add_argument(      "--blank-node2-line-action", dest="blank_node2_line_action",
                                  help="The action to take when a blank node2 field is detected.",
                                  type=ValidationAction, action=EnumNameAction, default=ValidationAction.EXCLUDE)
    
def main():
    """
    Test the KGTK edge file reader.
    """
    parser = ArgumentParser()
    KgtkReader.add_shared_arguments(parser)
    EdgeReader.add_arguments(parser)
    KgtkValueOptions.add_arguments(parser)
    args = parser.parse_args()

    error_file: typing.TextIO = sys.stdout if args.errors_to_stdout else sys.stderr

    # Build the value parsing option structure.
    value_options: KgtkValueOptions = KgtkValueOptions.from_args(args)

    er: EdgeReader = EdgeReader.open(args.kgtk_file,
                                     force_column_names=args.force_column_names,
                                     skip_first_record=args.skip_first_record,
                                     fill_short_lines=args.fill_short_lines,
                                     truncate_long_lines=args.truncate_long_lines,
                                     error_file=error_file,
                                     error_limit=args.error_limit,
                                     empty_line_action=args.empty_line_action,
                                     comment_line_action=args.comment_line_action,
                                     whitespace_line_action=args.whitespace_line_action,
                                     blank_node1_line_action=args.blank_node1_line_action,
                                     blank_node2_line_action=args.blank_node2_line_action,
                                     short_line_action=args.short_line_action,
                                     long_line_action=args.long_line_action,
                                     invalid_value_action=args.invalid_value_action,
                                     header_error_action=args.header_error_action,
                                     unsafe_column_name_action=args.unsafe_column_name_action,
                                     value_options=value_options,
                                     compression_type=args.compression_type,
                                     gzip_in_parallel=args.gzip_in_parallel,
                                     gzip_queue_size=args.gzip_queue_size,
                                     column_separator=args.column_separator,
                                     mode=KgtkReader.Mode.EDGE,
                                     verbose=args.verbose, very_verbose=args.very_verbose)

    line_count: int = 0
    row: typing.List[str]
    for row in er:
        line_count += 1
    print("Read %d lines" % line_count)

if __name__ == "__main__":
    main()

