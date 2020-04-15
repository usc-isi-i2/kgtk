"""
Read a KGTK edge file in TSV format.

TODO: Add support for alternative envelope formats, such as JSON.
"""

from argparse import ArgumentParser
import attr
import bz2
import gzip
import lzma
from pathlib import Path
from multiprocessing import Queue
import sys
import typing

from kgtk.join.basereader import BaseReader
from kgtk.join.closableiter import ClosableIter, ClosableIterTextIOWrapper
from kgtk.join.gzipprocess import GunzipProcess
from kgtk.join.kgtk_format import KgtkFormat

@attr.s(slots=True, frozen=True)
class EdgeReader(BaseReader):
    # The indices of the three mandatory columns:
    node1_column_idx: int = attr.ib(validator=attr.validators.instance_of(int))
    node2_column_idx: int = attr.ib(validator=attr.validators.instance_of(int)) # -1 means missing
    label_column_idx: int = attr.ib(validator=attr.validators.instance_of(int))

    # Ignore records with blank node1 or node2 values
    ignore_blank_node1_lines: bool = attr.ib(validator=attr.validators.instance_of(bool))
    ignore_blank_node2_lines: bool = attr.ib(validator=attr.validators.instance_of(bool))

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
             ignore_blank_node1_lines: bool = True,
             ignore_blank_node2_lines: bool = True,
             gzip_in_parallel: bool = False,
             gzip_queue_size: int = BaseReader.GZIP_QUEUE_SIZE_DEFAULT,
             column_separator: str = KgtkFormat.COLUMN_SEPARATOR,
             verbose: bool = False,
             very_verbose: bool = False)->"EdgeReader":
        if file_path is None or str(file_path) == "-":
            if verbose:
                print("EdgeReader: reading stdin")
            return cls._setup(file_path=None,
                              file_in=sys.stdin,
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
                              gzip_in_parallel=False,
                              gzip_queue_size=gzip_queue_size,
                              column_separator=column_separator,
                              verbose=verbose,
                              very_verbose=very_verbose,
            )
        
        if verbose:
            print("File_path.suffix: %s" % file_path.suffix)

        if file_path.suffix in [".gz", ".bz2", ".xz"]:
            # TODO: find a better way to coerce typing.IO[Any] to typing.TextIO
            gzip_file: typing.TextIO
            if file_path.suffix == ".gz":
                if verbose:
                    print("EdgeReader: reading gzip %s" % str(file_path))
                gzip_file = gzip.open(file_path, mode="rt") # type: ignore
            elif file_path.suffix == ".bz2":
                if verbose:
                    print("EdgeReader: reading bz2 %s" % str(file_path))
                gzip_file = bz2.open(file_path, mode="rt") # type: ignore
            elif file_path.suffix == ".xz":
                if verbose:
                    print("EdgeReader: reading lzma %s" % str(file_path))
                gzip_file = lzma.open(file_path, mode="rt") # type: ignore
            else:
                # TODO: throw a better exception.
                raise ValueError("Unexpected file_patn.suffiz = '%s'" % file_path.suffix)
            return cls._setup(file_path=file_path,
                              file_in=gzip_file,
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
                              column_separator=column_separator,
                              verbose=verbose,
                              very_verbose=very_verbose,
            )

        else:
            if verbose:
                print("EdgeReader: reading file %s" % str(file_path))
            return cls._setup(file_path=file_path,
                              file_in=open(file_path, "r"),
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
                              gzip_in_parallel=False,
                              gzip_queue_size=gzip_queue_size,
                              column_separator=column_separator,
                              verbose=verbose,
                              very_verbose=very_verbose,
)
    
    @classmethod
    def _setup(cls,
               file_path: typing.Optional[Path],
               file_in: typing.TextIO,
               force_column_names: typing.Optional[typing.List[str]],
               skip_first_record: bool,
               require_all_columns: bool,
               prohibit_extra_columns: bool,
               fill_missing_columns: bool,
               ignore_empty_lines: bool,
               ignore_comment_lines: bool,
               ignore_whitespace_lines: bool,
               ignore_blank_node1_lines: bool,
               ignore_blank_node2_lines: bool,
               gzip_in_parallel: bool,
               gzip_queue_size: int,
               column_separator: str,
               verbose: bool = False,
               very_verbose: bool = False,
    )->"EdgeReader":
        """
        Read the edge file header and split it into column names. Locate the three essential comumns.
        """
        column_names: typing.List[str] = cls._build_column_names(file_in,
                                                                 force_column_names=force_column_names,
                                                                 skip_first_record=skip_first_record,
                                                                 column_separator=column_separator,
                                                                 verbose=verbose)

        # Validate the column names and build a map from column name to column index.
        column_name_map: typing.Mapping[str, int] = KgtkFormat.validate_kgtk_edge_columns(column_names)

        # Get the indices of the required columns.
        node1_column_idx: int = KgtkFormat.get_column_idx(KgtkFormat.NODE1_COLUMN_NAMES, column_name_map)
        node2_column_idx: int = KgtkFormat.get_column_idx(KgtkFormat.NODE2_COLUMN_NAMES, column_name_map)
        label_column_idx: int = KgtkFormat.get_column_idx(KgtkFormat.LABEL_COLUMN_NAMES, column_name_map)

        source: ClosableIter[str]
        if gzip_in_parallel:
            gzip_thread: GunzipProcess = GunzipProcess(file_in, Queue(gzip_queue_size))
            gzip_thread.start()
            source = gzip_thread
        else:
            source = ClosableIterTextIOWrapper(file_in)

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
                self.line_count[1] += 1
                return True # ignore this line

        # Ignore lines with blank node2 fields:
        if self.ignore_blank_node2_lines and self.node2_column_idx >= 0 and len(values) > self.node2_column_idx:
            node2_value: str = values[self.node2_column_idx]
            if len(node2_value) == 0 or node2_value.isspace():
                self.line_count[1] += 1
                return True # ignore this line
        return False # Do not ignore this line

    def _skip_reserved_fields(self, column_name):
        if self.node1_column_idx >= 0 and column_name in KgtkFormat.NODE1_COLUMN_NAMES:
            return True
        if self.node2_column_idx >= 0 and column_name in KgtkFormat.NODE2_COLUMN_NAMES:
            return True
        if self.label_column_idx >= 0 and column_name in KgtkFormat.LABEL_COLUMN_NAMES:
            return True
        return False

    @classmethod
    def add_arguments(cls, parser: ArgumentParser):
        super().add_arguments(parser)
        parser.add_argument(      "--no-ignore-blank-node1-lines", dest="ignore_blank_node1_lines",
                                  help="When specified, do not ignore blank node1 lines.", action='store_false')

        parser.add_argument(      "--no-ignore-blank-node2-lines", dest="ignore_blank_node2_lines",
                                  help="When specified, do not ignore blank node2 lines.", action='store_false')

    
def main():
    """
    Test the KGTK edge file reader.
    """
    parser = ArgumentParser()
    EdgeReader.add_arguments(parser)
    args = parser.parse_args()

    er: EdgeReader = EdgeReader.open(args.edge_file,
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

