"""
Read a KGTK node file in TSV format.

TODO: Add support for alternative envelope formats, such as JSON.
"""

from argparse import ArgumentParser
import attr
from pathlib import Path
import sys
import typing

from kgtk.join.basereader import BaseReader
from kgtk.join.closableiter import ClosableIter

@attr.s(slots=True, frozen=True)
class NodeReader(BaseReader):
    # The index of the one mandatory column:
    id_column_idx: int = attr.ib(validator=attr.validators.instance_of(int))

    # Ignore records with blank id values
    ignore_blank_id_lines: bool = attr.ib(validator=attr.validators.instance_of(bool))

    @classmethod
    def open(cls,
             file_path: typing.Optional[Path],
             force_column_names: typing.Optional[typing.List[str]] = None, #
             skip_first_record: bool = False,
             require_all_columns: bool = True,
             prohibit_extra_columns: bool = True,
             fill_missing_columns: bool = False,
             ignore_empty_lines: bool = True,
             ignore_comment_lines: bool = True,
             ignore_whitespace_lines: bool = True,
             ignore_blank_id_lines: bool = True,
             gzip_in_parallel: bool = False,
             gzip_queue_size: int = BaseReader.GZIP_QUEUE_SIZE_DEFAULT,
             column_separator: str = BaseReader.COLUMN_SEPARATOR,
             verbose: bool = False,
             very_verbose: bool = False)->"NodeReader":

        source: ClosableIter[str] = cls._openfile(file_path,
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
        
        # Get the index of the required column.
        id_column_idx: int = cls.required_node_column(column_name_map)

        return cls(file_path=file_path,
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

    def _ignore_if_blank_fields(self, values: typing.List[str]):
        # Ignore lines with blank id fields.  This code comes after
        # filling missing trailing columns, although it could be reworked
        # to come first.
        if self.ignore_blank_id_lines and self.id_column_idx >= 0 and len(values) > self.id_column_idx:
            id_value: str = values[self.id_column_idx]
            if len(id_value) == 0 or id_value.isspace():
                self.line_count[1] += 1
                return True # ignore this line
        return False # Do not ignore this line

    def _skip_reserved_fields(self, column_name):
        if self.id_column_idx >= 0 and column_name in self.ID_COLUMN_NAMES:
            return True
        return False

    @classmethod
    def add_arguments(cls, parser: ArgumentParser):
        super().add_arguments(parser)
        parser.add_argument(      "--no-ignore-blank-id-lines", dest="ignore_blank_id_lines",
                                  help="When specified, do not ignore blank id lines.", action='store_false')

    
def main():
    """
    Test the KGTK node file reader.
    """
    parser = ArgumentParser()
    NodeReader.add_arguments(parser)
    args = parser.parse_args()

    er: NodeReader = NodeReader.open(args.kgtk_file,
                                     force_column_names=args.force_column_names,
                                     skip_first_record=args.skip_first_record,
                                     require_all_columns=args.require_all_columns,
                                     prohibit_extra_columns=args.prohibit_extra_columns,
                                     fill_missing_columns=args.fill_missing_columns,
                                     ignore_empty_lines=args.ignore_empty_lines,
                                     ignore_comment_lines=args.ignore_comment_lines,
                                     ignore_whitespace_lines=args.ignore_whitespace_lines,
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

