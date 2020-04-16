"""
Read a KGTK edge file in TSV format.

TODO: Add support for alternative envelope formats, such as JSON.
"""

from argparse import ArgumentParser
import attr
from pathlib import Path
import sys
import typing

from kgtk.join.basereader import BaseReader
from kgtk.join.closableiter import ClosableIter
from kgtk.join.edgereader import EdgeReader
from kgtk.join.nodereader import NodeReader

class KgtkReader(BaseReader):
    @classmethod
    def open(cls,
             file_path: typing.Optional[Path],
             force_column_names: typing.Optional[typing.List[str]] = None,
             skip_first_record: bool = False,
             require_all_columns: bool = True,
             prohibit_extra_columns: bool = True,
             fill_missing_columns: bool = False,
             ignore_empty_lines: bool = True,
             ignore_comment_lines: bool = True,
             ignore_whitespace_lines: bool = True,
             ignore_blank_node1_lines: bool = True,
             ignore_blank_node2_lines: bool = True,
             ignore_blank_id_lines: bool = True,
             gzip_in_parallel: bool = False,
             gzip_queue_size: int = BaseReader.GZIP_QUEUE_SIZE_DEFAULT,
             column_separator: str = BaseReader.COLUMN_SEPARATOR,
             verbose: bool = False,
             very_verbose: bool = False)->"BaseReader":
        """
        Opens a KGTK file, which may be an edge file or a node file.  The appropriate reader is returned.
        """
        source: ClosableIter[str] = cls._openfile(file_path,
                                                  gzip_in_parallel=gzip_in_parallel,
                                                  gzip_queue_size=gzip_queue_size,
                                                  verbose=verbose)

        # Read the kgtk file header and split it into column names.
        column_names: typing.List[str] = cls._build_column_names(source,
                                                                 force_column_names=force_column_names,
                                                                 skip_first_record=skip_first_record,
                                                                 column_separator=column_separator,
                                                                 verbose=verbose)
        # Build a map from column name to column index.
        column_name_map: typing.Mapping[str, int] = cls.build_column_name_map(column_names)

        # If we have a node1 column, then this must be an edge file. Otherwise, assume it is a node file.
        node1_idx: int = cls.get_column_idx(cls.NODE1_COLUMN_NAMES, column_name_map, is_optional=True)
        is_edge_file: bool = node1_idx >= 0

        if is_edge_file:
            # Get the indices of the required columns.
            node1_column_idx: int
            node2_column_idx: int
            label_column_idx: int
            (node1_column_idx, node2_column_idx, label_column_idx) = cls.required_edge_columns(column_name_map)

            if verbose:
                print("Reading an edge file. node1=%d label=%d node2=%d" % (node1_column_idx, label_column_idx, node2_column_idx))

            return EdgeReader(file_path=file_path,
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
                              require_all_columns=require_all_columns,
                              prohibit_extra_columns=prohibit_extra_columns,
                              fill_missing_columns=fill_missing_columns,
                              ignore_empty_lines=ignore_empty_lines,
                              ignore_comment_lines=ignore_comment_lines,
                              ignore_whitespace_lines=ignore_whitespace_lines,
                              ignore_blank_node1_lines=ignore_blank_node1_lines,
                              ignore_blank_node2_lines=ignore_blank_node2_lines,
                              gzip_in_parallel=gzip_in_parallel,
                              gzip_queue_size=gzip_queue_size,
                              line_count=[1, 0], # TODO: find a better way to do this.
                              is_edge_file=True,
                              is_node_file=False,
                              verbose=verbose,
                              very_verbose=very_verbose,
            )
        else:
            # Get the index of the required column:
            id_column_idx: int = cls.required_node_column(column_name_map)

            if verbose:
                print("Reading an node file. id=%d" % (id_column_idx))

            return NodeReader(file_path=file_path,
                              source=source,
                              column_separator=column_separator,
                              column_names=column_names,
                              column_name_map=column_name_map,
                              column_count=len(column_names),
                              id_column_idx=id_column_idx,
                              force_column_names=force_column_names,
                              skip_first_record=skip_first_record,
                              require_all_columns=require_all_columns,
                              prohibit_extra_columns=prohibit_extra_columns,
                              fill_missing_columns=fill_missing_columns,
                              ignore_empty_lines=ignore_empty_lines,
                              ignore_comment_lines=ignore_comment_lines,
                              ignore_whitespace_lines=ignore_whitespace_lines,
                              ignore_blank_id_lines=ignore_blank_id_lines,
                              gzip_in_parallel=gzip_in_parallel,
                              gzip_queue_size=gzip_queue_size,
                              line_count=[1, 0], # TODO: find a better way to do this.
                              is_edge_file=False,
                              is_node_file=True,
                              verbose=verbose,
                              very_verbose=very_verbose,
            )

    @classmethod
    def add_arguments(cls, parser: ArgumentParser):
        BaseReader.add_arguments(parser)
        parser.add_argument(      "--no-ignore-blank-id-lines", dest="ignore_blank_id_lines",
                                  help="When specified, do not ignore blank id lines.", action='store_false')

        parser.add_argument(      "--no-ignore-blank-node1-lines", dest="ignore_blank_node1_lines",
                                  help="When specified, do not ignore blank node1 lines.", action='store_false')

        parser.add_argument(      "--no-ignore-blank-node2-lines", dest="ignore_blank_node2_lines",
                                  help="When specified, do not ignore blank node2 lines.", action='store_false')

    
def main():
    """
    Test the KGTK file reader.
    """
    parser = ArgumentParser()
    KgtkReader.add_arguments(parser)
    args = parser.parse_args()

    er: BaseReader = KgtkReader.open(args.kgtk_file,
                                     force_column_names=args.force_column_names,
                                     skip_first_record=args.skip_first_record,
                                     require_all_columns=args.require_all_columns,
                                     prohibit_extra_columns=args.prohibit_extra_columns,
                                     fill_missing_columns=args.fill_missing_columns,
                                     ignore_empty_lines=args.ignore_empty_lines,
                                     ignore_comment_lines=args.ignore_comment_lines,
                                     ignore_whitespace_lines=args.ignore_whitespace_lines,
                                     ignore_blank_node1_lines=args.ignore_blank_node1_lines,
                                     ignore_blank_node2_lines=args.ignore_blank_node2_lines,
                                     ignore_blank_id_lines=args.ignore_blank_id_lines,
                                     gzip_in_parallel=args.gzip_in_parallel,
                                     gzip_queue_size=args.gzip_queue_size,
                                     column_separator=args.column_separator,
                                     verbose=args.verbose, very_verbose=args.very_verbose)

    line_count: int = 0
    line: typing.List[str]
    for line in er:
        line_count += 1
    print("Read %d lines" % line_count)

if __name__ == "__main__":
    main()

