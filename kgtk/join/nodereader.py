"""
Read a KGTK node file in TSV format.

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
from kgtk.join.kgtkvalueoptions import KgtkValueOptions
from kgtk.join.validationaction import ValidationAction

@attr.s(slots=True, frozen=False)
class NodeReader(KgtkReader):

    @classmethod
    def open_node_file(cls,
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
                       blank_id_line_action: ValidationAction = ValidationAction.EXCLUDE,
                       short_line_action: ValidationAction = ValidationAction.EXCLUDE,
                       long_line_action: ValidationAction = ValidationAction.EXCLUDE,
                       invalid_value_action: ValidationAction = ValidationAction.REPORT,
                       header_error_action: ValidationAction = ValidationAction.EXIT,
                       unsafe_column_name_action: ValidationAction = ValidationAction.REPORT,
                       value_options: typing.Optional[KgtkValueOptions] = None,
                       compression_type: typing.Optional[str] = None,
                       gzip_in_parallel: bool = False,
                       gzip_queue_size: int = KgtkReader.GZIP_QUEUE_SIZE_DEFAULT,
                       column_separator: str = KgtkReader.COLUMN_SEPARATOR,
                       verbose: bool = False,
                       very_verbose: bool = False)->"NodeReader":

        source: ClosableIter[str] = cls._openfile(file_path,
                                                  compression_type=compression_type,
                                                  gzip_in_parallel=gzip_in_parallel,
                                                  gzip_queue_size=gzip_queue_size,
                                                  error_file=error_file,
                                                  verbose=verbose)

        # Read the node file header and split it into column names.
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
        # Get the index of the required column.
        id_column_idx: int = cls.required_node_column(column_name_map,
                                                      header_line=header,
                                                      error_action=header_error_action,
                                                      error_file=error_file)

        if verbose:
            print("NodeReader: Reading an node file. id=%d" % (id_column_idx))

        return cls(file_path=file_path,
                   source=source,
                   column_separator=column_separator,
                   column_names=column_names,
                   column_name_map=column_name_map,
                   column_count=len(column_names),
                   id_column_idx=id_column_idx,
                   force_column_names=force_column_names,
                   skip_first_record=skip_first_record,
                   fill_short_lines=fill_short_lines,
                   truncate_long_lines=truncate_long_lines,
                   error_file=error_file,
                   error_limit=error_limit,
                   empty_line_action=empty_line_action,
                   comment_line_action=comment_line_action,
                   whitespace_line_action=whitespace_line_action,
                   blank_id_line_action=blank_id_line_action,
                   short_line_action=short_line_action,
                   long_line_action=long_line_action,
                   invalid_value_action=invalid_value_action,
                   header_error_action=header_error_action,
                   unsafe_column_name_action=unsafe_column_name_action,
                   value_options=value_options,
                   compression_type=compression_type,
                   gzip_in_parallel=gzip_in_parallel,
                   gzip_queue_size=gzip_queue_size,
                   is_edge_file=False,
                   is_node_file=True,
                   verbose=verbose,
                   very_verbose=very_verbose,
        )

    def _ignore_if_blank_fields(self, values: typing.List[str], line: str)->bool:
        # Ignore line_action with blank id fields.  This code comes after
        # filling missing trailing columns, although it could be reworked
        # to come first.
        if self.blank_id_line_action != ValidationAction.PASS and self.id_column_idx >= 0 and len(values) > self.id_column_idx:
            id_value: str = values[self.id_column_idx]
            if len(id_value) == 0 or id_value.isspace():
                return self.exclude_line(self.blank_id_line_action, "id is blank", line)
        return False # Do not ignore this line

    def _skip_reserved_fields(self, column_name)->bool:
        if self.id_column_idx >= 0 and column_name in self.ID_COLUMN_NAMES:
            return True
        return False

    @classmethod
    def add_arguments(cls, parser: ArgumentParser):
        # super().add_arguments(parser)
        parser.add_argument(      "--blank-id-line-action", dest="blank_id_line_action",
                                  help="The action to take when a blank id field is detected.",
                                  type=ValidationAction, action=EnumNameAction, default=ValidationAction.EXCLUDE)

    
def main():
    """
    Test the KGTK node file reader.
    """
    parser = ArgumentParser()
    KgtkReader.add_shared_arguments(parser)
    NodeReader.add_arguments(parser)
    KgtkValueOptions.add_arguments(parser)
    args = parser.parse_args()

    error_file: typing.TextIO = sys.stdout if args.errors_to_stdout else sys.stderr

    # Build the value parsing option structure.
    value_options: KgtkValueOptions = KgtkValueOptions.from_args(args)

    er: NodeReader = NodeReader.open(args.kgtk_file,
                                     force_column_names=args.force_column_names,
                                     skip_first_record=args.skip_first_record,
                                     fill_short_lines=args.fill_short_lines,
                                     truncate_long_lines=args.truncate_long_lines,
                                     error_file=error_file,
                                     error_limit=args.error_limit,
                                     empty_line_action=args.empty_line_action,
                                     comment_line=args.comment_line_action,
                                     whitespace_line_action=args.whitespace_line_action,
                                     blank_id_line_action=args.blank_id_line_action,
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
                                     mode=KgtkReader.Mode.NODE,
                                     verbose=args.verbose, very_verbose=args.very_verbose)

    line_count: int = 0
    row: typing.List[str]
    for row in er:
        line_count += 1
    print("Read %d lines" % line_count)

if __name__ == "__main__":
    main()

