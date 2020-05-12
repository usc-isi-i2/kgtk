"""
Write a KGTK edge or node file in TSV format.

"""

from argparse import ArgumentParser
import attr
import bz2
from enum import Enum
import gzip
import lz4 # type: ignore
import lzma
from pathlib import Path
from multiprocessing import Queue
import sys
import typing

from kgtk.kgtkformat import KgtkFormat
from kgtk.io.kgtkbase import KgtkBase
from kgtk.io.kgtkreader import KgtkReader
from kgtk.utils.enumnameaction import EnumNameAction
from kgtk.utils.gzipprocess import GzipProcess
from kgtk.utils.validationaction import ValidationAction

@attr.s(slots=True, frozen=False)
class KgtkWriter(KgtkBase):
    GZIP_QUEUE_SIZE_DEFAULT: int = GzipProcess.GZIP_QUEUE_SIZE_DEFAULT

    file_path: typing.Optional[Path] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Path)))
    file_out: typing.TextIO = attr.ib() # Todo: validate TextIO
    column_separator: str = attr.ib(validator=attr.validators.instance_of(str))
    column_names: typing.List[str] = attr.ib(validator=attr.validators.deep_iterable(member_validator=attr.validators.instance_of(str),
                                                                                     iterable_validator=attr.validators.instance_of(list)))
    column_name_map: typing.Mapping[str, int] = attr.ib(validator=attr.validators.deep_mapping(key_validator=attr.validators.instance_of(str),
                                                                                               value_validator=attr.validators.instance_of(int)))

    # For convenience, the count of columns. This is the same as len(column_names).
    column_count: int = attr.ib(validator=attr.validators.instance_of(int))

    # Require or fill trailing fields?
    require_all_columns: bool = attr.ib(validator=attr.validators.instance_of(bool))
    prohibit_extra_columns: bool = attr.ib(validator=attr.validators.instance_of(bool))
    fill_missing_columns: bool = attr.ib(validator=attr.validators.instance_of(bool))

    # How should header errors be processed?
    error_file: typing.TextIO = attr.ib(default=sys.stderr)
    header_error_action: ValidationAction = attr.ib(validator=attr.validators.instance_of(ValidationAction), default=ValidationAction.EXIT)

    # Other implementation options?
    gzip_in_parallel: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    gzip_thread: typing.Optional[GzipProcess] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(GzipProcess)), default=None)
    gzip_queue_size: int = attr.ib(validator=attr.validators.instance_of(int), default=GZIP_QUEUE_SIZE_DEFAULT)

    line_count: int = attr.ib(validator=attr.validators.instance_of(int), default=0)

    verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    very_verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    class Mode(Enum):
        """
        There are four file writing modes:
        """
        NONE = 0 # Enforce neither edge nor node file required columns
        EDGE = 1 # Enforce edge file required columns
        NODE = 2 # Enforce node file required columns
        AUTO = 3 # Automatically decide whether to enforce edge or node file required columns

    @classmethod
    def open(cls,
             column_names: typing.List[str],
             file_path: typing.Optional[Path],
             require_all_columns: bool = True,
             prohibit_extra_columns: bool = True,
             fill_missing_columns: bool = False,
             error_file: typing.TextIO = sys.stderr,
             header_error_action: ValidationAction = ValidationAction.EXIT,
             gzip_in_parallel: bool = False,
             gzip_queue_size: int = GZIP_QUEUE_SIZE_DEFAULT,
             column_separator: str = KgtkFormat.COLUMN_SEPARATOR,
             mode: Mode = Mode.AUTO,
             verbose: bool = False,
             very_verbose: bool = False)->"KgtkWriter":
        if file_path is None or str(file_path) == "-":
            if verbose:
                print("KgtkWriter: writing stdout", file=sys.stderr)
            return cls._setup(column_names=column_names,
                              file_path=None,
                              file_out=sys.stdout,
                              require_all_columns=require_all_columns,
                              prohibit_extra_columns=prohibit_extra_columns,
                              fill_missing_columns=fill_missing_columns,
                              error_file=error_file,
                              header_error_action=header_error_action,
                              gzip_in_parallel=gzip_in_parallel,
                              gzip_queue_size=gzip_queue_size,
                              column_separator=column_separator,
                              mode=mode,
                              verbose=verbose,
                              very_verbose=very_verbose,
            )
        
        if verbose:
            print("File_path.suffix: %s" % file_path.suffix, file=sys.stderr)

        if file_path.suffix in [".gz", ".bz2", ".xz"]:
            # TODO: find a better way to coerce typing.IO[Any] to typing.TextIO
            gzip_file: typing.TextIO
            if file_path.suffix == ".gz":
                if verbose:
                    print("KgtkWriter: writing gzip %s" % str(file_path), file=sys.stderr)
                gzip_file = gzip.open(file_path, mode="wt") # type: ignore
            elif file_path.suffix == ".bz2":
                if verbose:
                    print("KgtkWriter: writing bz2 %s" % str(file_path), file=sys.stderr)
                gzip_file = bz2.open(file_path, mode="wt") # type: ignore
            elif file_path.suffix == ".xz":
                if verbose:
                    print("KgtkWriter: writing lzma %s" % str(file_path), file=sys.stderr)
                gzip_file = lzma.open(file_path, mode="wt") # type: ignore
            else:
                # TODO: throw a better exception.
                raise ValueError("Unexpected file_patn.suffiz = '%s'" % file_path.suffix)

            return cls._setup(column_names=column_names,
                              file_path=file_path,
                              file_out=gzip_file,
                              require_all_columns=require_all_columns,
                              prohibit_extra_columns=prohibit_extra_columns,
                              fill_missing_columns=fill_missing_columns,
                              error_file=error_file,
                              header_error_action=header_error_action,
                              gzip_in_parallel=gzip_in_parallel,
                              gzip_queue_size=gzip_queue_size,
                              column_separator=column_separator,
                              mode=mode,
                              verbose=verbose,
                              very_verbose=very_verbose,
            )
            
        else:
            if verbose:
                print("KgtkWriter: writing file %s" % str(file_path), file=sys.stderr)
            return cls._setup(column_names=column_names,
                              file_path=file_path,
                              file_out=open(file_path, "w"),
                              require_all_columns=require_all_columns,
                              prohibit_extra_columns=prohibit_extra_columns,
                              fill_missing_columns=fill_missing_columns,
                              error_file=error_file,
                              header_error_action=header_error_action,
                              gzip_in_parallel=gzip_in_parallel,
                              gzip_queue_size=gzip_queue_size,
                              column_separator=column_separator,
                              mode=mode,
                              verbose=verbose,
                              very_verbose=very_verbose,
)
    
    @classmethod
    def _setup(cls,
               column_names: typing.List[str],
               file_path: typing.Optional[Path],
               file_out: typing.TextIO,
               require_all_columns: bool,
               prohibit_extra_columns: bool,
               fill_missing_columns: bool,
               error_file: typing.TextIO,
               header_error_action: ValidationAction,
               gzip_in_parallel: bool,
               gzip_queue_size: int,
               column_separator: str,
               mode: Mode = Mode.AUTO,
               verbose: bool = False,
               very_verbose: bool = False,
    )->"KgtkWriter":

        # Build a header line for error feedback:
        header: str = column_separator.join(column_names)

        # Build a map from column name to column index.
        column_name_map: typing.Mapping[str, int] = cls.build_column_name_map(column_names,
                                                                              header_line=header,
                                                                              error_action=header_error_action,
                                                                              error_file=error_file)

        # Should we automatically determine if this is an edge file or a node file?
        is_edge_file: bool = False
        is_node_file: bool = False
        if mode is KgtkWriter.Mode.AUTO:
            # If we have a node1 (or alias) column, then this must be an edge file. Otherwise, assume it is a node file.
            node1_idx: int = cls.get_column_idx(cls.NODE1_COLUMN_NAMES, column_name_map,
                                                header_line=header,
                                                error_action=header_error_action,
                                                error_file=error_file,
                                                is_optional=True)
            is_edge_file = node1_idx >= 0
            is_node_file = not is_edge_file
        elif mode is KgtkWriter.Mode.EDGE:
            is_edge_file = True
        elif mode is KgtkWriter.Mode.NODE:
            is_node_file = True
        elif mode is KgtkWriter.Mode.NONE:
            pass
        
        # Validate that we have the proper columns for an edge or node file,
        # ignoring the result.
        cls.get_special_columns(column_name_map,
                                header_line=header,
                                error_action=header_error_action,
                                error_file=error_file,
                                is_edge_file=is_edge_file,
                                is_node_file=is_node_file)

        # Write the column names to the first line.
        if verbose:
            print("header: %s" % header, file=sys.stderr)
        file_out.write(header + "\n") # Todo: use system end-of-line sequence?

        gzip_thread: typing.Optional[GzipProcess] = None
        if gzip_in_parallel:
            gzip_thread = GzipProcess(file_out, Queue(gzip_queue_size))
            gzip_thread.start()

        return cls(file_path=file_path,
                   file_out=file_out,
                   column_separator=column_separator,
                   column_names=column_names,
                   column_name_map=column_name_map,
                   column_count=len(column_names),
                   require_all_columns=require_all_columns,
                   prohibit_extra_columns=prohibit_extra_columns,
                   fill_missing_columns=fill_missing_columns,
                   error_file=error_file,
                   header_error_action=header_error_action,
                   gzip_in_parallel=gzip_in_parallel,
                   gzip_thread=gzip_thread,
                   gzip_queue_size=gzip_queue_size,
                   line_count=1,
                   verbose=verbose,
                   very_verbose=very_verbose,
        )


    # Write the next list of edge values as a list of strings.
    # TODO: Convert integers, coordinates, etc. from Python types
    def write(self, values: typing.List[str],
              shuffle_list: typing.Optional[typing.List[int]]= None):

        if shuffle_list is not None:
            if len(shuffle_list) != len(values):
                # TODO: throw a better exception
                raise ValueError("The shuffle list is %d long but the values are %d long" % (len(shuffle_list), len(values)))

            shuffled_values: typing.List[str] = [""] * self.column_count
            idx: int
            for idx in range(len(shuffle_list)):
                shuffle_idx: int = shuffle_list[idx]
                if shuffle_idx >= 0:
                    shuffled_values[shuffle_idx] = values[idx]
            values = shuffled_values

        # Optionally fill missing trailing columns with empty values:
        if self.fill_missing_columns and len(values) < self.column_count:
            while len(values) < self.column_count:
                values.append("")

        line: str = self.column_separator.join(values)

        # Optionally validate that the line contained the right number of columns:
        #
        # When we report line numbers in error messages, line 1 is the first line after the header line.
        if self.require_all_columns and len(values) < self.column_count:
            raise ValueError("Required %d columns in input line %d, saw %d: '%s'" % (self.column_count, self.line_count, len(values), line))
        if self.prohibit_extra_columns and len(values) > self.column_count:
            raise ValueError("Required %d columns in input line %d, saw %d (%d extra): '%s'" % (self.column_count, self.line_count, len(values),
                                                                                                len(values) - self.column_count, line))

        if self.gzip_thread is not None:
            self.gzip_thread.write(line + "\n")
        else:
            self.file_out.write(line + "\n")

        self.line_count += 1
        if self.very_verbose:
            sys.stdout.write(".")
            sys.stdout.flush()

    def flush(self):
        if self.gzip_thread is None:
            self.file_out.flush()

    def close(self):
        if self.gzip_thread is not None:
            self.gzip_thread.close()
        else:
            self.file_out.close()


    def writemap(self, value_map: typing.Mapping[str, str]):
        """
        Write a map of values to the output file.
        """
        column_name: str

        # Optionally check for unexpected column names:
        if self.prohibit_extra_columns:
            for column_name in value_map.keys():
                if column_name not in self.column_name_map:
                    raise ValueError("Unexpected column name %s at data record %d" % (column_name, self.line_count))

        values: typing.List[str] = [ ]
        for column_name in self.column_names:
            if column_name in value_map:
                values.append(value_map[column_name])
            elif self.require_all_columns:
                # TODO: throw a better exception.
                raise ValueError("Missing column %s at data record %d" % (column_name, self.line_count))
            else:
                values.append("")
                
        self.write(values)

    def build_shuffle_list(self,
                           other_column_names: typing.List[str],
                           fail_on_unknown_column: bool = False)->typing.List[int]:
        results: typing.List[int] = [ ]
        column_name: str
        for column_name in other_column_names:
            if column_name in self.column_name_map:
                results.append(self.column_name_map[column_name])
            elif fail_on_unknown_column:
                # TODO: throw a better exception
                raise ValueError("Unknown column name %s when building shuffle list" % column_name)
            else:
                results.append(-1) # Means skip this column.
        return results
    
def main():
    """
    Test the KGTK edge file writer.
    """
    parser = ArgumentParser()
    parser.add_argument(dest="input_kgtk_file", help="The KGTK file to read", type=Path, nargs="?")
    parser.add_argument(dest="output_kgtk_file", help="The KGTK file to write", type=Path, nargs="?")
    parser.add_argument(      "--header-error-action", dest="header_error_action",
                              help="The action to take when a header error is detected  Only ERROR or EXIT are supported.",
                              type=ValidationAction, action=EnumNameAction, default=ValidationAction.EXIT)
    parser.add_argument(      "--gzip-in-parallel", dest="gzip_in_parallel", help="Execute gzip in a subthread.", action='store_true')
    parser.add_argument(      "--input-mode", dest="input_mode",
                              help="Determine the input KGTK file mode.", type=KgtkReader.Mode, action=EnumNameAction, default=KgtkReader.Mode.AUTO)
    parser.add_argument(      "--output-mode", dest="output_mode",
                              help="Determine the output KGTK file mode.", type=KgtkWriter.Mode, action=EnumNameAction, default=KgtkWriter.Mode.AUTO)
    parser.add_argument("-v", "--verbose", dest="verbose", help="Print additional progress messages.", action='store_true')
    parser.add_argument(      "--very-verbose", dest="very_verbose", help="Print additional progress messages.", action='store_true')
    args = parser.parse_args()

    error_file: typing.TextIO = sys.stdout if args.errors_to_stdout else sys.stderr

    kr: KgtkReader = KgtkReader.open(args.input_kgtk_file,
                                     error_file=error_file,
                                     header_error_action=args.header_error_action,
                                     gzip_in_parallel=args.gzip_in_parallel,
                                     mode=args.input_mode,
                                     verbose=args.verbose, very_verbose=args.very_verbose)

    kw: KgtkWriter = KgtkWriter.open(kr.column_names,
                                     args.output_kgtk_file,
                                     error_file=error_file,
                                     gzip_in_parallel=args.gzip_in_parallel,
                                     header_error_action=args.header_error_action,
                                     mode=args.output_mode,
                                     verbose=args.verbose, very_verbose=args.very_verbose)

    line_count: int = 0
    row: typing.List[str]
    for row in kr:
        kw.write(row)
        line_count += 1
    kw.close()
    if args.verbose:
        print("Copied %d lines" % line_count, file=sys.stderr)


if __name__ == "__main__":
    main()
