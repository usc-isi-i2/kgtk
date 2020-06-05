"""
Write a KGTK edge or node file in TSV format.

"""

from argparse import ArgumentParser
import attr
import bz2
from enum import Enum
import gzip
import json
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

    # TODO: use an enum
    OUTPUT_FORMAT_CSV: str = "csv"
    OUTPUT_FORMAT_JSON: str = "json"
    OUTPUT_FORMAT_JSON_MAP: str = "json-map"
    OUTPUT_FORMAT_JSON_MAP_COMPACT: str = "json-map-compact"
    OUTPUT_FORMAT_JSONL: str = "jsonl"
    OUTPUT_FORMAT_JSONL_MAP: str = "jsonl-map"
    OUTPUT_FORMAT_JSONL_MAP_COMPACT: str = "jsonl-map-compact"
    OUTPUT_FORMAT_KGTK: str = "kgtk"
    OUTPUT_FORMAT_MD: str = "md"

    OUTPUT_FORMAT_CHOICES: typing.List[str] = [
        OUTPUT_FORMAT_CSV,
        OUTPUT_FORMAT_JSON,
        OUTPUT_FORMAT_JSON_MAP,
        OUTPUT_FORMAT_JSON_MAP_COMPACT,
        OUTPUT_FORMAT_JSONL,
        OUTPUT_FORMAT_JSONL_MAP,
        OUTPUT_FORMAT_JSONL_MAP_COMPACT,
        OUTPUT_FORMAT_KGTK,
        OUTPUT_FORMAT_MD,
    ]
    OUTPUT_FORMAT_DEFAULT: str = OUTPUT_FORMAT_KGTK

    file_path: typing.Optional[Path] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Path)))
    file_out: typing.TextIO = attr.ib() # Todo: validate TextIO
    column_separator: str = attr.ib(validator=attr.validators.instance_of(str))
    column_names: typing.List[str] = attr.ib(validator=attr.validators.deep_iterable(member_validator=attr.validators.instance_of(str),
                                                                                     iterable_validator=attr.validators.instance_of(list)))
    column_name_map: typing.Mapping[str, int] = attr.ib(validator=attr.validators.deep_mapping(key_validator=attr.validators.instance_of(str),
                                                                                               value_validator=attr.validators.instance_of(int)))

    # Use these names in the output file, but continue to use
    # column_names for shuffle lists.
    output_column_names: typing.List[str] = \
        attr.ib(validator=attr.validators.deep_iterable(member_validator=attr.validators.instance_of(str),
                                                        iterable_validator=attr.validators.instance_of(list)))

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

    output_format: str = attr.ib(validator=attr.validators.instance_of(str), default=OUTPUT_FORMAT_DEFAULT) # TODO: use an enum

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
             who: str = "output",
             require_all_columns: bool = True,
             prohibit_extra_columns: bool = True,
             fill_missing_columns: bool = False,
             error_file: typing.TextIO = sys.stderr,
             header_error_action: ValidationAction = ValidationAction.EXIT,
             gzip_in_parallel: bool = False,
             gzip_queue_size: int = GZIP_QUEUE_SIZE_DEFAULT,
             column_separator: str = KgtkFormat.COLUMN_SEPARATOR,
             mode: Mode = Mode.AUTO,
             output_format: typing.Optional[str] = None,
             output_column_names: typing.Optional[typing.List[str]] = None,
             old_column_names: typing.Optional[typing.List[str]] = None,
             new_column_names: typing.Optional[typing.List[str]] = None,
             verbose: bool = False,
             very_verbose: bool = False)->"KgtkWriter":
        if file_path is None or str(file_path) == "-":
            if verbose:
                print("KgtkWriter: writing stdout", file=error_file, flush=True)

            return cls._setup(column_names=column_names,
                              file_path=None,
                              who=who,
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
                              output_format=output_format,
                              output_column_names=output_column_names,
                              old_column_names=old_column_names,
                              new_column_names=new_column_names,
                              verbose=verbose,
                              very_verbose=very_verbose,
            )
        
        if verbose:
            print("File_path.suffix: %s" % file_path.suffix, file=error_file, flush=True)

        if file_path.suffix in [".gz", ".bz2", ".xz", ".lz4"]:
            # TODO: find a better way to coerce typing.IO[Any] to typing.TextIO
            gzip_file: typing.TextIO
            if file_path.suffix == ".gz":
                if verbose:
                    print("KgtkWriter: writing gzip %s" % str(file_path), file=error_file, flush=True)
                gzip_file = gzip.open(file_path, mode="wt") # type: ignore
            elif file_path.suffix == ".bz2":
                if verbose:
                    print("KgtkWriter: writing bz2 %s" % str(file_path), file=error_file, flush=True)
                gzip_file = bz2.open(file_path, mode="wt") # type: ignore
            elif file_path.suffix == ".xz":
                if verbose:
                    print("KgtkWriter: writing lzma %s" % str(file_path), file=error_file, flush=True)
                gzip_file = lzma.open(file_path, mode="wt") # type: ignore
            elif file_path.suffix ==".lz4":
                if verbose:
                    print("KgtkWriter: writing lz4 %s" % str(file_path), file=error_file, flush=True)
                gzip_file = lz4.frame.open(file_or_path, mode="wt") # type: ignore
            else:
                # TODO: throw a better exception.
                raise ValueError("Unexpected file_path.suffiz = '%s'" % file_path.suffix)

            return cls._setup(column_names=column_names,
                              file_path=file_path,
                              who=who,
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
                              output_format=output_format,
                              output_column_names=output_column_names,
                              old_column_names=old_column_names,
                              new_column_names=new_column_names,
                              verbose=verbose,
                              very_verbose=very_verbose,
            )
            
        else:
            if output_format is None:
                # TODO: optionally stack these on top of compression
                if file_path.suffix == ".md":
                    output_format = "md"
                elif file_path.suffix == ".csv":
                    output_format = "csv"
                elif file_path.suffix == ".json":
                    output_format = "json"
                elif file_path.suffix == ".jsonl":
                    output_format = "jsonl"
                else:
                    output_format = "kgtk"

            if verbose:
                print("KgtkWriter: writing file %s" % str(file_path), file=error_file, flush=True)
            return cls._setup(column_names=column_names,
                              file_path=file_path,
                              who=who,
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
                              output_format=output_format,
                              output_column_names=output_column_names,
                              old_column_names=old_column_names,
                              new_column_names=new_column_names,
                              verbose=verbose,
                              very_verbose=very_verbose,
)
    
    @classmethod
    def _setup(cls,
               column_names: typing.List[str],
               file_path: typing.Optional[Path],
               who: str,
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
               output_format: typing.Optional[str] = None,
               output_column_names: typing.Optional[typing.List[str]] = None,
               old_column_names: typing.Optional[typing.List[str]] = None,
               new_column_names: typing.Optional[typing.List[str]] = None,
               verbose: bool = False,
               very_verbose: bool = False,
    )->"KgtkWriter":

        if output_format is None:
            output_format = cls.OUTPUT_FORMAT_DEFAULT
            if verbose:
                print("Defaulting the output format to %s" % output_format, file=error_file, flush=True)

        if output_format == cls.OUTPUT_FORMAT_CSV:
            column_separator = "," # What a cheat!
                
        if output_column_names is None:
            output_column_names = column_names
        else:
            # Rename all output columns.
            if len(output_column_names) != len(column_names):
                raise ValueError("%s: %d column names but %d output column names" % (who, len(column_names), len(output_column_names)))

        if old_column_names is not None or new_column_names is not None:
            # Rename selected output columns:
            if old_column_names is None or new_column_names is None:
                raise ValueError("%s: old/new column name mismatch" % who)
            if len(old_column_names) != len(new_column_names):
                raise ValueError("%s: old/new column name length mismatch: %d != %d" % (who, len(old_column_names), len(new_column_names)))

            # Rename columns in place.  Start by copyin the output column name
            # list so the changes don't inadvertantly propogate.
            output_column_names = output_column_names.copy()
            column_name: str
            idx: int
            for idx, column_name in enumerate(old_column_names):
                if column_name not in output_column_names:
                    raise ValueError("%s: old column names %s not in the output column names." % (who, column_name))
                output_column_names[output_column_names.index(column_name)] = new_column_names[idx]
                

        # Build a map from column name to column index.  This is used for
        # self.writemap(...)  and self.build_shuffle_list(...)
        column_name_map: typing.Mapping[str, int] = cls.build_column_name_map(column_names,
                                                                              header_line=column_separator.join(column_names),
                                                                              who=who,
                                                                              error_action=header_error_action,
                                                                              error_file=error_file)

        # Build a header line for error feedback:
        header: str = column_separator.join(output_column_names)

        # Build a map from output column name to column index.
        output_column_name_map: typing.Mapping[str, int] = cls.build_column_name_map(output_column_names,
                                                                                     header_line=header,
                                                                                     who=who,
                                                                                     error_action=header_error_action,
                                                                                     error_file=error_file)

        # Should we automatically determine if this is an edge file or a node file?
        is_edge_file: bool = False
        is_node_file: bool = False
        if mode is KgtkWriter.Mode.AUTO:
            # If we have a node1 (or alias) column, then this must be an edge file. Otherwise, assume it is a node file.
            node1_idx: int = cls.get_column_idx(cls.NODE1_COLUMN_NAMES, output_column_name_map,
                                                header_line=header,
                                                who=who,
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
        cls.get_special_columns(output_column_name_map,
                                header_line=header,
                                who=who,
                                error_action=header_error_action,
                                error_file=error_file,
                                is_edge_file=is_edge_file,
                                is_node_file=is_node_file)

        gzip_thread: typing.Optional[GzipProcess] = None
        if gzip_in_parallel:
            if verbose:
                print("Starting the gzip process.", file=error_file, flush=True)
            gzip_thread = GzipProcess(file_out, Queue(gzip_queue_size))
            gzip_thread.start()

        kw: KgtkWriter = cls(file_path=file_path,
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
                             output_format=output_format,
                             output_column_names=output_column_names,
                             line_count=1,
                             verbose=verbose,
                             very_verbose=very_verbose,
        )
        kw.write_header()
        return kw


    def join_csv(self, values: typing.List[str])->str:
        line: str = ""
        value: str
        for value in values:
            if '"' in value or ',' in value:
                value = '"' + '""'.join(value.split('"')) + '"'
            if len(line) > 0:
                line += ","
            line += value
        return line

    def join_md(self, values: typing.List[str])->str:
        line: str = "|"
        value: str
        for value in values:
            value = "\\|".join(value.split("|"))
            line += " " + value + " |"
        return line

    def json_map(self, values: typing.List[str], compact: bool = False)->typing.Mapping[str, str]:
        result: typing.MutableMapping[str, str] = { }
        idx: int
        value: str
        for idx, value in enumerate(values):
            if len(value) > 0 or not compact:
                result[self.output_column_names[idx]] = value
        return result

    def write_header(self):
        header: str
        header2: typing.Optional[str] = None

        # Contemplate a last-second rename of the columns
        column_names: typing.List[str]
        if self.output_column_names is not None:
            column_names = self.output_column_names
        else:
            column_names = self.column_names

        if self.output_format == self.OUTPUT_FORMAT_JSON:
            self.writeline("[")
            header = json.dumps(column_names, indent=None, separators=(',', ':')) + ","
        elif self.output_format == self.OUTPUT_FORMAT_JSON_MAP:
            self.writeline("[")
            return
        elif self.output_format == self.OUTPUT_FORMAT_JSON_MAP_COMPACT:
            self.writeline("[")
            return
        elif self.output_format == self.OUTPUT_FORMAT_JSONL:
            header = json.dumps(column_names, indent=None, separators=(',', ':'))
        elif self.output_format == self.OUTPUT_FORMAT_JSONL_MAP:
            return
        elif self.output_format == self.OUTPUT_FORMAT_JSONL_MAP_COMPACT:
            return
        elif self.output_format == self.OUTPUT_FORMAT_MD:
            header = "|"
            header2 = "|"
            col: str
            for col in column_names:
                col = "\\|".join(col.split("|"))
                header += " " + col + " |"
                header2 += " -- |"
            
        elif self.output_format in [self.OUTPUT_FORMAT_KGTK, self.OUTPUT_FORMAT_CSV]:
            header = self.column_separator.join(column_names)
        else:
            raise ValueError("KgtkWriter: header: Unrecognized output format '%s'." % self.output_format)

        # Write the column names to the first line.
        if self.verbose:
            print("header: %s" % header, file=self.error_file, flush=True)
        self.writeline(header)
        if header2 is not None:
            self.writeline(header2)

    def writeline(self, line: str):
        if self.gzip_thread is not None:
            self.gzip_thread.write(line + "\n") # Todo: use system end-of-line sequence?
        else:
            self.file_out.write(line + "\n") # Todo: use system end-of-line sequence?

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

        # Optionally validate that the line contained the right number of columns:
        #
        # When we report line numbers in error messages, line 1 is the first line after the header line.
        line: str
        if self.require_all_columns and len(values) < self.column_count:
            line = self.column_separator.join(values)
            raise ValueError("Required %d columns in input line %d, saw %d: '%s'" % (self.column_count, self.line_count, len(values), line))
        if self.prohibit_extra_columns and len(values) > self.column_count:
            line = self.column_separator.join(values)
            raise ValueError("Required %d columns in input line %d, saw %d (%d extra): '%s'" % (self.column_count, self.line_count, len(values),
                                                                                                len(values) - self.column_count, line))
        if self.output_format == self.OUTPUT_FORMAT_KGTK:
            self.writeline(self.column_separator.join(values))
        elif self.output_format == self.OUTPUT_FORMAT_CSV:
            self.writeline(self.join_csv(values))
        elif self.output_format == self.OUTPUT_FORMAT_MD:
            self.writeline(self.join_md(values))
        elif self.output_format == self.OUTPUT_FORMAT_JSON:
            self.writeline(json.dumps(values, indent=None, separators=(',', ':')) + ",")
        elif self.output_format == self.OUTPUT_FORMAT_JSON_MAP:
            self.writeline(json.dumps(self.json_map(values), indent=None, separators=(',', ':')) + ",")
        elif self.output_format == self.OUTPUT_FORMAT_JSON_MAP_COMPACT:
            self.writeline(json.dumps(self.json_map(values, compact=True), indent=None, separators=(',', ':')) + ",")
        elif self.output_format == self.OUTPUT_FORMAT_JSONL:
            self.writeline(json.dumps(values, indent=None, separators=(',', ':')))
        elif self.output_format == self.OUTPUT_FORMAT_JSONL_MAP:
            self.writeline(json.dumps(self.json_map(values), indent=None, separators=(',', ':')))
        elif self.output_format == self.OUTPUT_FORMAT_JSONL_MAP_COMPACT:
            self.writeline(json.dumps(self.json_map(values, compact=True), indent=None, separators=(',', ':')))
        else:
            raise ValueError("Unrecognized output format '%s'." % self.output_format)

        self.line_count += 1
        if self.very_verbose:
            sys.stdout.write(".")
            sys.stdout.flush()

    def flush(self):
        if self.gzip_thread is None:
            self.file_out.flush()

    def close(self):
        if self.output_format == "json":
            if self.verbose:
                print("Closing the JSON list.", file=self.error_file, flush=True)
            self.writeline("]")

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

    TODO: full reader options.

    TODO:  --show-options
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
    parser.add_argument(      "--output-format", dest="output_format", help="The file format (default=kgtk)", type=str)
    parser.add_argument(      "--output-columns", dest="output_column_names", help="Rename all output columns. (default=%(default)s)", type=str, nargs='+')
    parser.add_argument(      "--old-columns", dest="old_column_names", help="Rename seleted output columns: old names. (default=%(default)s)", type=str, nargs='+')
    parser.add_argument(      "--new-columns", dest="new_column_names", help="Rename seleted output columns: new names. (default=%(default)s)", type=str, nargs='+')
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
                                     output_format=args.output_format,
                                     output_column_names=args.output_column_names,
                                     old_column_names=args.old_column_names,
                                     new_column_names=args.new_column_names,
                                     verbose=args.verbose, very_verbose=args.very_verbose)

    line_count: int = 0
    row: typing.List[str]
    for row in kr:
        kw.write(row)
        line_count += 1
    kw.close()
    if args.verbose:
        print("Copied %d lines" % line_count, file=error_file, flush=True)


if __name__ == "__main__":
    main()
