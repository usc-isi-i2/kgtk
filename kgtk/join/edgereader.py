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
from kgtk.join.kgtkreader import KgtkReader, KgtkReaderErrorAction

@attr.s(slots=True, frozen=False)
class EdgeReader(KgtkReader):

    @classmethod
    def open_edge_file(cls,
                       file_path: typing.Optional[Path],
                       force_column_names: typing.Optional[typing.List[str]] = None, #
                       skip_first_record: bool = False,
                       fill_short_lines: bool = False,
                       truncate_long_lines: bool = False,
                       error_action: KgtkReaderErrorAction = KgtkReaderErrorAction.STDOUT,
                       error_limit: int = KgtkReader.ERROR_LIMIT_DEFAULT,
                       ignore_empty_lines: bool = True,
                       ignore_comment_lines: bool = True,
                       ignore_whitespace_lines: bool = True,
                       ignore_blank_node1_lines: bool = True,
                       ignore_blank_node2_lines: bool = True,
                       ignore_short_lines: bool = True,
                       ignore_long_lines: bool = True,
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
                                                  verbose=verbose)

        # Read the node file header and split it into column names.
        column_names: typing.List[str] = cls._build_column_names(source,
                                                                 force_column_names=force_column_names,
                                                                 skip_first_record=skip_first_record,
                                                                 column_separator=column_separator,
                                                                 verbose=verbose)

        # Build a map from column name to column index.
        column_name_map: typing.Mapping[str, int] = cls.build_column_name_map(column_names)
        
        # Get the indices of the required columns.
        node1_column_idx: int
        node2_column_idx: int
        label_column_idx: int
        (node1_column_idx, node2_column_idx, label_column_idx) = cls.required_edge_columns(column_name_map)

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
                   error_action=error_action,
                   ignore_empty_lines=ignore_empty_lines,
                   ignore_comment_lines=ignore_comment_lines,
                   ignore_whitespace_lines=ignore_whitespace_lines,
                   ignore_blank_node1_lines=ignore_blank_node1_lines,
                   ignore_blank_node2_lines=ignore_blank_node2_lines,
                   ignore_short_lines=ignore_short_lines,
                   ignore_long_lines=ignore_long_lines,
                   compression_type=compression_type,
                   gzip_in_parallel=gzip_in_parallel,
                   gzip_queue_size=gzip_queue_size,
                   is_edge_file=True,
                   is_node_file=False,
                   verbose=verbose,
                   very_verbose=very_verbose,
        )

    def _ignore_if_blank_fields(self, values: typing.List[str]):
        # Ignore lines with blank node1 fields.  This code comes after
        # filling missing trailing columns, although it could be reworked
        # to come first.
        if self.ignore_blank_node1_lines and self.node1_column_idx >= 0 and len(values) > self.node1_column_idx:
            node1_value: str = values[self.node1_column_idx]
            if len(node1_value) == 0 or node1_value.isspace():
                return True # ignore this line

        # Ignore lines with blank node2 fields:
        if self.ignore_blank_node2_lines and self.node2_column_idx >= 0 and len(values) > self.node2_column_idx:
            node2_value: str = values[self.node2_column_idx]
            if len(node2_value) == 0 or node2_value.isspace():
                return True # ignore this line
        return False # Do not ignore this line

    def _skip_reserved_fields(self, column_name):
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
        parser.add_argument(      "--allow-blank-node1-lines", dest="ignore_blank_node1_lines",
                                  help="When specified, do not ignore blank node1 lines.", action='store_false')

        parser.add_argument(      "--allow-blank-node2-lines", dest="ignore_blank_node2_lines",
                                  help="When specified, do not ignore blank node2 lines.", action='store_false')

    
def main():
    """
    Test the KGTK edge file reader.
    """
    parser = ArgumentParser()
    KgtkReader.add_shared_arguments(parser)
    EdgeReader.add_arguments(parser)
    args = parser.parse_args()

    er: EdgeReader = EdgeReader.open(args.kgtk_file,
                                     force_column_names=args.force_column_names,
                                     skip_first_record=args.skip_first_record,
                                     fill_short_lines=args.fill_short_lines,
                                     truncate_long_lines=args.truncate_long_lines,
                                     error_action=args.error_action,
                                     error_limit=args.error_limit,
                                     ignore_empty_lines=args.ignore_empty_lines,
                                     ignore_comment_lines=args.ignore_comment_lines,
                                     ignore_whitespace_lines=args.ignore_whitespace_lines,
                                     ignore_blank_node1_lines=args.ignore_blank_node1_lines,
                                     ignore_blank_node2_lines=args.ignore_blank_node2_lines,
                                     ignore_short_lines=args.ignore_short_lines,
                                     ignore_long_lines=args.ignore_long_lines,
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

