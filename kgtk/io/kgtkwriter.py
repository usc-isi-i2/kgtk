"""
Write a KGTK edge or node file in TSV format.

"""

from argparse import ArgumentParser
import attr
from enum import Enum
import errno
import html
import json
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
    MGZIP_THREAD_COUNT_DEFAULT: int = 3

    # TODO: use an enum
    OUTPUT_FORMAT_CSV: str = "csv"
    OUTPUT_FORMAT_HTML: str = "html"
    OUTPUT_FORMAT_HTML_COMPACT: str = "html-compact"
    OUTPUT_FORMAT_JSON: str = "json"
    OUTPUT_FORMAT_JSON_MAP: str = "json-map"
    OUTPUT_FORMAT_JSON_MAP_COMPACT: str = "json-map-compact"
    OUTPUT_FORMAT_JSONL: str = "jsonl"
    OUTPUT_FORMAT_JSONL_MAP: str = "jsonl-map"
    OUTPUT_FORMAT_JSONL_MAP_COMPACT: str = "jsonl-map-compact"
    OUTPUT_FORMAT_KGTK: str = "kgtk"
    OUTPUT_FORMAT_MD: str = "md"
    OUTPUT_FORMAT_TABLE: str = "table"
    OUTPUT_FORMAT_TSV: str = "tsv"
    OUTPUT_FORMAT_TSV_CSVLIKE: str = "tsv-csvlike"
    OUTPUT_FORMAT_TSV_UNQUOTED: str = "tsv-unquoted"
    OUTPUT_FORMAT_TSV_UNQUOTED_EP: str = "tsv-unquoted-ep"

    OUTPUT_FORMAT_CHOICES: typing.List[str] = [
        OUTPUT_FORMAT_CSV,
        OUTPUT_FORMAT_HTML,
        OUTPUT_FORMAT_HTML_COMPACT,
        OUTPUT_FORMAT_JSON,
        OUTPUT_FORMAT_JSON_MAP,
        OUTPUT_FORMAT_JSON_MAP_COMPACT,
        OUTPUT_FORMAT_JSONL,
        OUTPUT_FORMAT_JSONL_MAP,
        OUTPUT_FORMAT_JSONL_MAP_COMPACT,
        OUTPUT_FORMAT_KGTK,
        OUTPUT_FORMAT_MD,
        OUTPUT_FORMAT_TABLE,
        OUTPUT_FORMAT_TSV,
        OUTPUT_FORMAT_TSV_CSVLIKE,
        OUTPUT_FORMAT_TSV_UNQUOTED,
        OUTPUT_FORMAT_TSV_UNQUOTED_EP,
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
    use_mgzip: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    used_mgzip: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    mgzip_threads: int = attr.ib(validator=attr.validators.instance_of(int), default=MGZIP_THREAD_COUNT_DEFAULT)
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

    def __attrs_post_init__(self):
        self.format_writers: typing.Mapping[str, typing.Callable[[typing.List[str]], None]] = {
            self.OUTPUT_FORMAT_KGTK: self.write_kgtk,
            self.OUTPUT_FORMAT_TABLE: self.write_table,
            self.OUTPUT_FORMAT_TSV: self.write_tsv,
            self.OUTPUT_FORMAT_TSV_UNQUOTED: self.write_tsv_unquoted,
            self.OUTPUT_FORMAT_TSV_UNQUOTED_EP: self.write_tsv_unquoted_ep,
            self.OUTPUT_FORMAT_TSV_CSVLIKE: self.write_tsv_csvlike,
            self.OUTPUT_FORMAT_CSV: self.write_csv,
            self.OUTPUT_FORMAT_MD: self.write_md,
            self.OUTPUT_FORMAT_HTML: self.write_html,
            self.OUTPUT_FORMAT_HTML_COMPACT: self.write_html_compact,
            self.OUTPUT_FORMAT_JSON: self.write_json,
            self.OUTPUT_FORMAT_JSON_MAP: self.write_json_map,
            self.OUTPUT_FORMAT_JSON_MAP_COMPACT: self.write_json_map_compact,
            self.OUTPUT_FORMAT_JSONL: self.write_jsonl,
            self.OUTPUT_FORMAT_JSONL_MAP: self.write_jsonl_map,
            self.OUTPUT_FORMAT_JSONL_MAP_COMPACT: self.write_jsonl_map_compact,
        }
        

    @classmethod
    def open(cls,
             column_names: typing.List[str],
             file_path: typing.Optional[typing.Union[Path, str]],
             who: str = "output",
             require_all_columns: bool = True,
             prohibit_extra_columns: bool = True,
             fill_missing_columns: bool = False,
             error_file: typing.TextIO = sys.stderr,
             header_error_action: ValidationAction = ValidationAction.EXIT,
             use_mgzip: bool = False,
             mgzip_threads: int = MGZIP_THREAD_COUNT_DEFAULT,
             gzip_in_parallel: bool = False,
             gzip_queue_size: int = GZIP_QUEUE_SIZE_DEFAULT,
             column_separator: str = KgtkFormat.COLUMN_SEPARATOR,
             mode: Mode = Mode.AUTO,
             output_format: typing.Optional[str] = None,
             output_column_names: typing.Optional[typing.List[str]] = None,
             old_column_names: typing.Optional[typing.List[str]] = None,
             new_column_names: typing.Optional[typing.List[str]] = None,
             no_header: bool = False,
             verbose: bool = False,
             very_verbose: bool = False)->"KgtkWriter":

        if file_path is not None and isinstance(file_path, str):
            file_path = Path(file_path)

        if file_path is None or str(file_path) == "-":
            if verbose:
                print("KgtkWriter: writing stdout", file=error_file, flush=True)

            if output_format is None:
                output_format = cls.OUTPUT_FORMAT_DEFAULT

            return cls._setup(column_names=column_names,
                              file_path=None,
                              who=who,
                              file_out=sys.stdout,
                              require_all_columns=require_all_columns,
                              prohibit_extra_columns=prohibit_extra_columns,
                              fill_missing_columns=fill_missing_columns,
                              error_file=error_file,
                              header_error_action=header_error_action,
                              use_mgzip=use_mgzip,
                              used_mgzip=False,
                              mgzip_threads=mgzip_threads,
                              gzip_in_parallel=gzip_in_parallel,
                              gzip_queue_size=gzip_queue_size,
                              column_separator=column_separator,
                              mode=mode,
                              output_format=output_format,
                              output_column_names=output_column_names,
                              old_column_names=old_column_names,
                              new_column_names=new_column_names,
                              no_header=no_header,
                              verbose=verbose,
                              very_verbose=very_verbose,
            )
        
        if str(file_path).startswith(">"):
            fd: int = int(str(file_path)[1:])
            if verbose:
                print("%s: writing file descriptor %d" % (who, fd), file=error_file, flush=True)

            if output_format is None:
                output_format = cls.OUTPUT_FORMAT_DEFAULT

            return cls._setup(column_names=column_names,
                              file_path=file_path,
                              who=who,
                              file_out=open(fd, "w"),
                              require_all_columns=require_all_columns,
                              prohibit_extra_columns=prohibit_extra_columns,
                              fill_missing_columns=fill_missing_columns,
                              error_file=error_file,
                              header_error_action=header_error_action,
                              use_mgzip=use_mgzip,
                              used_mgzip=False,
                              mgzip_threads=mgzip_threads,
                              gzip_in_parallel=gzip_in_parallel,
                              gzip_queue_size=gzip_queue_size,
                              column_separator=column_separator,
                              mode=mode,
                              output_format=output_format,
                              output_column_names=output_column_names,
                              old_column_names=old_column_names,
                              new_column_names=new_column_names,
                              no_header=no_header,
                              verbose=verbose,
                              very_verbose=very_verbose,
            )
                

        if verbose:
            print("File_path.suffix: %s" % file_path.suffix, file=error_file, flush=True)

        used_mgzip: bool = False
        if file_path.suffix in [".gz", ".bz2", ".xz", ".lz4"]:
            # TODO: find a better way to coerce typing.IO[Any] to typing.TextIO
            gzip_file: typing.TextIO
            if file_path.suffix == ".gz":
                if use_mgzip:
                    if verbose:
                        print("KgtkWriter: writing mgzip with %d threads: %s" % (mgzip_threads, str(file_path)), file=error_file, flush=True)
                    import mgzip
                    gzip_file = mgzip.open(str(file_path), mode="wt", thread=mgzip_threads) # type: ignore
                    used_mgzip = True
                else:
                    if verbose:
                        print("KgtkWriter: writing gzip %s" % str(file_path), file=error_file, flush=True)
                    import gzip
                    gzip_file = gzip.open(file_path, mode="wt") # type: ignore

            elif file_path.suffix == ".bz2":
                if verbose:
                    print("KgtkWriter: writing bz2 %s" % str(file_path), file=error_file, flush=True)
                import bz2
                gzip_file = bz2.open(file_path, mode="wt") # type: ignore

            elif file_path.suffix == ".xz":
                if verbose:
                    print("KgtkWriter: writing lzma %s" % str(file_path), file=error_file, flush=True)
                import lzma
                gzip_file = lzma.open(file_path, mode="wt") # type: ignore

            elif file_path.suffix ==".lz4":
                if verbose:
                    print("KgtkWriter: writing lz4 %s" % str(file_path), file=error_file, flush=True)
                import lz4 # type: ignore
                gzip_file = lz4.frame.open(file_or_path, mode="wt") # type: ignore
            else:
                # TODO: throw a better exception.
                raise ValueError("Unexpected file_path.suffiz = '%s'" % file_path.suffix)

            if output_format is None:
                if len(file_path.suffixes) < 2:
                    output_format = cls.OUTPUT_FORMAT_DEFAULT
                else:
                    format_suffix: str = file_path.suffixes[-2]
                    if format_suffix == ".md":
                        output_format = cls.OUTPUT_FORMAT_MD
                    elif format_suffix == ".csv":
                        output_format = cls.OUTPUT_FORMAT_CSV
                    elif format_suffix == ".html":
                        output_format = cls.OUTPUT_FORMAT_HTML
                    elif format_suffix == ".json":
                        output_format = cls.OUTPUT_FORMAT_JSON
                    elif format_suffix == ".jsonl":
                        output_format = cls.OUTPUT_FORMAT_JSONL
                    elif format_suffix == ".table":
                        output_format = cls.OUTPUT_FORMAT_TABLE
                    else:
                        output_format = cls.OUTPUT_FORMAT_DEFAULT

            return cls._setup(column_names=column_names,
                              file_path=file_path,
                              who=who,
                              file_out=gzip_file,
                              require_all_columns=require_all_columns,
                              prohibit_extra_columns=prohibit_extra_columns,
                              fill_missing_columns=fill_missing_columns,
                              error_file=error_file,
                              header_error_action=header_error_action,
                              use_mgzip=use_mgzip,
                              used_mgzip=used_mgzip,
                              mgzip_threads=mgzip_threads,
                              gzip_in_parallel=gzip_in_parallel,
                              gzip_queue_size=gzip_queue_size,
                              column_separator=column_separator,
                              mode=mode,
                              output_format=output_format,
                              output_column_names=output_column_names,
                              old_column_names=old_column_names,
                              new_column_names=new_column_names,
                              no_header=no_header,
                              verbose=verbose,
                              very_verbose=very_verbose,
            )
            
        else:
            if output_format is None:
                if file_path.suffix == ".md":
                    output_format = cls.OUTPUT_FORMAT_MD
                elif file_path.suffix == ".csv":
                    output_format = cls.OUTPUT_FORMAT_CSV
                elif file_path.suffix == ".html":
                    output_format = cls.OUTPUT_FORMAT_HTML
                elif file_path.suffix == ".json":
                    output_format = cls.OUTPUT_FORMAT_JSON
                elif file_path.suffix == ".jsonl":
                    output_format = cls.OUTPUT_FORMAT_JSONL
                elif file_path.suffix == ".table":
                    output_format = cls.OUTPUT_FORMAT_TABLE
                else:
                    output_format = cls.OUTPUT_FORMAT_DEFAULT

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
                              use_mgzip=use_mgzip,
                              used_mgzip = False,
                              mgzip_threads=mgzip_threads,
                              gzip_in_parallel=gzip_in_parallel,
                              gzip_queue_size=gzip_queue_size,
                              column_separator=column_separator,
                              mode=mode,
                              output_format=output_format,
                              output_column_names=output_column_names,
                              old_column_names=old_column_names,
                              new_column_names=new_column_names,
                              no_header=no_header,
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
               use_mgzip: bool,
               used_mgzip: bool,
               mgzip_threads: int,
               gzip_in_parallel: bool,
               gzip_queue_size: int,
               column_separator: str,
               mode: Mode = Mode.AUTO,
               output_format: typing.Optional[str] = None,
               output_column_names: typing.Optional[typing.List[str]] = None,
               old_column_names: typing.Optional[typing.List[str]] = None,
               new_column_names: typing.Optional[typing.List[str]] = None,
               no_header: bool = False,
               verbose: bool = False,
               very_verbose: bool = False,
    )->"KgtkWriter":

        if output_format is None:
            output_format = cls.OUTPUT_FORMAT_DEFAULT
            if verbose:
                print("Defaulting the output format to %s" % output_format, file=error_file, flush=True)

        if output_format == cls.OUTPUT_FORMAT_CSV:
            column_separator = "," # What a cheat!
                
        if output_column_names is None or len(output_column_names) == 0:
            output_column_names = column_names
        else:
            # Rename all output columns.
            if len(output_column_names) != len(column_names):
                raise ValueError("%s: %d column names but %d output column names" % (who, len(column_names), len(output_column_names)))

        if (old_column_names is not None and len(old_column_names) > 0) or (new_column_names is not None and len(new_column_names) > 0):
            # Rename selected output columns:
            if old_column_names is None or new_column_names is None:
                raise ValueError("%s: old/new column name mismatch" % who)
            if len(old_column_names) != len(new_column_names):
                raise ValueError("%s: old/new column name length mismatch: %d != %d" % (who, len(old_column_names), len(new_column_names)))

            # Rename columns in place.  Start by copying the output column name
            # list so the changes don't inadvertantly propogate.
            new_output_column_names: typing.List[str] = output_column_names.copy()
            column_name: str
            idx: int
            for idx, column_name in enumerate(old_column_names):
                if column_name not in output_column_names:
                    raise ValueError("%s: old column names %s not in the output column names." % (who, column_name))
                new_output_column_names[output_column_names.index(column_name)] = new_column_names[idx]
            output_column_names = new_output_column_names # Update the outptu column names.

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
                print("KgtkWriter: File %s: Starting the gzip process." % (repr(file_path)), file=error_file, flush=True)
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
                             use_mgzip=use_mgzip,
                             used_mgzip=used_mgzip,
                             mgzip_threads=mgzip_threads,
                             gzip_in_parallel=gzip_in_parallel,
                             gzip_thread=gzip_thread,
                             gzip_queue_size=gzip_queue_size,
                             output_format=output_format,
                             output_column_names=output_column_names,
                             line_count=1,
                             verbose=verbose,
                             very_verbose=very_verbose,
        )
        if not no_header:
            kw.write_header()
        return kw


    def reformat_datetime(self, value: str)->str:
        return value[1:] # Strip the datetime sigil, perhaps more reformatting later.

    def join_csv(self, values: typing.List[str],
                 unquoted: bool = False,
                 )->str:
        line: str = ""
        value: str
        for value in values:
            # TODO: Complain if the value is a KGTK List.
            if value.startswith(KgtkFormat.DATE_AND_TIMES_SIGIL):
                value = self.reformat_datetime(value)

            elif value.startswith((KgtkFormat.STRING_SIGIL, KgtkFormat.LANGUAGE_QUALIFIED_STRING_SIGIL)):
                # What if the value is a list? unstringify(...) will be
                # unhappy.  The following hack protects strings (but not
                # language-qualified strings) against errors, introducing
                # an ambiguity when exporting lists:
                value = value.replace('"|"', '|')
                value = KgtkFormat.unstringify(value) # Lose the language code.
                # TODO: Complain if internal newline or carriage return.

                if not unquoted:
                    value = '"' + value.replace('"', '""') + '"'
                
            else:
                value = value.replace("\\|", "|")
                if '"' in value or ',' in value:
                    # A symbol with an internal double quote or comma: turn it into a string.
                    value = '"' + value.replace('"', '""') + '"'
            if len(line) > 0:
                line += ","
            line += value
        return line

    def join_tsv(self,
                 values: typing.List[str],
                 unquoted: bool = False,
                 unescape_pipe: bool = True,
                 csvlike: bool = False,
                 )->str:
        line: str = ""
        value: str
        for value in values:
            # TODO: Complain if the value is a KGTK List.
            if value.startswith(KgtkFormat.DATE_AND_TIMES_SIGIL):
                value = self.reformat_datetime(value)

            elif value.startswith((KgtkFormat.STRING_SIGIL, KgtkFormat.LANGUAGE_QUALIFIED_STRING_SIGIL)):
                if unquoted:
                    # What if the value is a list? unstringify(...) will be
                    # unhappy.  The following hack protects strings (but not
                    # language-qualified strings) against errors, introducing
                    # an ambiguity when exporting lists:
                    value = value.replace('"|"', '|')
                    try:
                        value = KgtkFormat.unstringify(value, unescape_pipe=unescape_pipe) # Lose the language code.
                    except ValueError as e:
                        print("KgtkWriter: File %s: Error unstringifying %s" % (repr(self.file_path), repr(value)), file=self.error_file, flush=True)
                        raise e
                elif csvlike:
                    # What if the value is a list? unstringify(...) will be
                    # unhappy.  The following hack protects strings (but not
                    # language-qualified strings) against errors, introducing
                    # an ambiguity when exporting lists:
                    value = value.replace('"|"', '|')
                    try:
                        value = KgtkFormat.unstringify(value, unescape_pipe=unescape_pipe) # Lose the language code.
                    except ValueError as e:
                        print("KgtkWriter: File %s: Error unstringifying %s" % (repr(self.file_path), repr(value)), file=self.error_file, flush=True)
                        raise e
                    value = '"' + value.replace('"', '""') + '"'
                    
                else:
                    value = value.replace("\\|", "|")
            else:
                value = value.replace("\\|", "|")

            if len(line) > 0:
                line += "\t"
            line += value
        return line

    def join_md(self, values: typing.List[str])->str:
        linebuf: typing.List[str] = ["|"]
        value: str
        for value in values:
            linebuf.append(" ")
            linebuf.append(value.replace("\\", "\\\\").replace("|", "\\|"))
            linebuf.append(" |")
        return "".join(linebuf)

    def reformat_value_for_json(self, value: str)->typing.Union[str, int, float, bool]:
        # TODO: Complain if the value is a KGTK List.
        if value.startswith((KgtkFormat.STRING_SIGIL, KgtkFormat.LANGUAGE_QUALIFIED_STRING_SIGIL)):
            # What if the value is a list? unstringify(...) will be
            # unhappy.  The following hack protects strings (but not
            # language-qualified strings) against errors, introducing
            # an ambiguity when exporting lists:
            value = value.replace('"|"', '|')
            return KgtkFormat.unstringify(value) # Lose the language code.
        elif value == KgtkFormat.TRUE_SYMBOL:
            return True
        elif value == KgtkFormat.FALSE_SYMBOL:
            return False
        elif value.isdigit():
            return int(value)
        elif value.startswith(("+", "-")) and value[1:].isdigit():
            return int(value)
        else:
            # TODO: process floating point numbers.
            # TODO: process datetimes
            # TODO: process geolocations
            return value

    def reformat_values_for_json(self, values: typing.List[str])->typing.List[typing.Union[str, int, float, bool]]:
        results: typing.List[typing.Union[str, int, float, bool]] = [ ]
        value: str
        for value in values:
            results.append(self.reformat_value_for_json(value))
        return results

    def json_map(self, values: typing.List[str], compact: bool = False)->typing.Mapping[str, typing.Union[str, int, float, bool]]:
        result: typing.MutableMapping[str, typing.Union[str, int, float, bool]] = { }
        idx: int
        value: str
        for idx, value in enumerate(values):
            if len(value) > 0 or not compact:
                result[self.output_column_names[idx]] = self.reformat_value_for_json(value)
        return result

    def writehtml(self, line: str, indent: int, compact: bool = False):
        if compact:
            self.writeline_noeol(line)
        else:
            self.writeline("  " * indent + line)

    def write_html_header(self, compact: bool = False):
        self.writehtml('<!DOCTYPE html>', 0, compact=compact)
        self.writehtml('<html lang="en">', 0, compact=compact)
        self.writehtml('<head>', 1, compact=compact)
        self.writehtml('<meta charset="utf-8">', 2, compact=compact)
        self.writehtml('<style>', 2, compact=compact)
        self.writehtml('table, th, td {', 0, compact=compact)
        self.writehtml('border: 1px solid black;', 0, compact=compact)
        self.writehtml('border-collapse: collapse;', 0, compact=compact)
        self.writehtml('}', 0, compact=compact)
        self.writehtml('</style>', 2, compact=compact)
        self.writehtml('</head>', 1, compact=compact)
        self.writehtml('<body>', 1, compact=compact)
        self.writehtml('<table>', 2, compact=compact)

        self.writehtml('<tr>', 3, compact=compact)

        column_name: str
        for column_name in self.output_column_names:
            self.writehtml('<th>%s</th>' % html.escape(column_name), 4, compact=compact)

        self.writehtml('</tr>', 3, compact=compact)

    def write_html(self, values: typing.List[str], compact: bool = False):
        self.writehtml('<tr>', 3, compact=compact)

        value: str
        for value in values:
            self.writehtml('<td>%s</td>' % html.escape(value), 4, compact=compact)

        self.writehtml('</tr>', 3, compact=compact)

    def write_html_compact(self, values: typing.List[str]):
        self.write_html(values, compact=True)

    def write_html_trailer(self, compact: bool = False):
        self.writehtml('</table>', 2, compact=compact)
        self.writehtml('</body>', 1, compact=compact)
        self.writehtml('</html>', 0)

    def write_header(self):
        header: str
        header2: typing.Optional[str] = None

        noeol: bool = False

        # Contemplate a last-second rename of the columns
        column_names: typing.List[str]
        if self.output_column_names is not None:
            column_names = self.output_column_names
        else:
            column_names = self.column_names

        if self.output_format == self.OUTPUT_FORMAT_HTML:
            self.write_html_header()
            return;

        elif self.output_format == self.OUTPUT_FORMAT_HTML_COMPACT:
            self.write_html_header(compact=True)
            return;

        elif self.output_format == self.OUTPUT_FORMAT_JSON:
            self.writeline("[")
            header = json.dumps(column_names, indent=None, separators=(',', ':'))
            noeol = True
        elif self.output_format == self.OUTPUT_FORMAT_JSON_MAP:
            self.writeline_noeol("[")
            return
        elif self.output_format == self.OUTPUT_FORMAT_JSON_MAP_COMPACT:
            self.writeline_noeol("[")
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
            
        elif self.output_format == self.OUTPUT_FORMAT_TABLE:
            return # We'll write a header later.

        elif self.output_format in [self.OUTPUT_FORMAT_KGTK,
                                    self.OUTPUT_FORMAT_CSV,
                                    self.OUTPUT_FORMAT_TSV,
                                    self.OUTPUT_FORMAT_TSV_CSVLIKE,
                                    self.OUTPUT_FORMAT_TSV_UNQUOTED,
                                    self.OUTPUT_FORMAT_TSV_UNQUOTED_EP,
                                    ]:
            header = self.column_separator.join(column_names)
        else:
            raise ValueError("KgtkWriter: File %s: header: Unrecognized output format '%s'." % (repr(self.file_path), self.output_format))

        # Write the column names to the first line.
        if self.verbose:
            print("header: %s" % header, file=self.error_file, flush=True)
        if noeol:
            self.writeline_noeol(header)
        else:
            self.writeline(header)
        if header2 is not None:
            if self.verbose:
                print("header2: %s" % header2, file=self.error_file, flush=True)
            self.writeline(header2)

    def writeline(self, line: str):
        if self.gzip_thread is not None:
            # self.gzip_thread.write(line + "\n") # TODO: use alternative end-of-line sequences?
            self.gzip_thread.write(line)
            self.gzip_thread.write("\n") # TODO: use alternative end-of-line sequences?
        else:
            try:
                # self.file_out.write(line + "\n") # Todo: use system end-of-line sequence?
                self.file_out.write(line)
                self.file_out.write("\n") # Todo: use system end-of-line sequence?
            except IOError as e:
                if e.errno == errno.EPIPE:
                    pass # TODO: propogate a close backwards.
                else:
                    raise

    def writeline_noeol(self, line: str):
        if self.gzip_thread is not None:
            self.gzip_thread.write(line) # TODO: use alternative end-of-line sequences?
        else:
            try:
                self.file_out.write(line) # Todo: use system end-of-line sequence?
            except IOError as e:
                if e.errno == errno.EPIPE:
                    pass # TODO: propogate a close backwards.
                else:
                    raise

    def shuffle(self, values: typing.List[str], shuffle_list: typing.List[int])->typing.List[str]:
        if len(shuffle_list) != len(values):
            # TODO: throw a better exception
            raise ValueError("KgtkWriter: File %s: The shuffle list is %d long but the values are %d long" % (repr(self.file_path),
                                                                                                              len(shuffle_list),
                                                                                                              len(values)))

        shuffled_values: typing.List[str] = [""] * self.column_count
        idx: int
        for idx in range(len(shuffle_list)):
            shuffle_idx: int = shuffle_list[idx]
            if shuffle_idx >= 0:
                shuffled_values[shuffle_idx] = values[idx]
        return shuffled_values

    # Write the next list of edge values as a list of strings.
    def write(self, values: typing.List[str],
              shuffle_list: typing.Optional[typing.List[int]]= None):

        if shuffle_list is not None:
            values = self.shuffle(values, shuffle_list)

        if len(values) != self.column_count:
            # Optionally fill missing trailing columns with empty values:
            if self.fill_missing_columns and len(values) < self.column_count:
                while len(values) < self.column_count:
                    values.append("")

            if len(values) != self.column_count:
                # Optionally validate that the line contained the right number of columns:
                #
                # When we report line numbers in error messages, line 1 is the first line after the header line.
                line: str
                if self.require_all_columns and len(values) < self.column_count:
                    line = self.column_separator.join(values)
                    raise ValueError("KgtkWriter: File %s: Required %d columns (%s) in output line %d, saw %d: %s" % (repr(self.file_path),
                                                                                                                      self.column_count,
                                                                                                                      repr(self.column_separator.join(self.column_names)),
                                                                                                                      self.line_count,
                                                                                                                      len(values),
                                                                                                                      repr(line)))
                if self.prohibit_extra_columns and len(values) > self.column_count:
                    line = self.column_separator.join(values)
                    raise ValueError("KgtkWriter: File %s: Required %d columns (%s)in output line %d, saw %d (%d extra): %s" % (repr(self.file_path),
                                                                                                                                self.column_count,
                                                                                                                                repr(self.column_separator.join(self.column_names)),
                                                                                                                                self.line_count,
                                                                                                                                len(values),
                                                                                                                                len(values) - self.column_count,
                                                                                                                                repr(line)))
        format_writer: typing.Optional[typing.Callable[[typing.List[str]], None]] = self.format_writers.get(self.output_format)
        if format_writer is None:
            raise ValueError("KgtkWriter: File %s: Unrecognized output format %s." % (repr(self.file_path), repr(self.output_format)))
        format_writer(values)

        self.line_count += 1
        if self.very_verbose:
            sys.stdout.write(".")
            sys.stdout.flush()

    # Write the next list of edge values as a list of strings,
    # converting Python types into KGTK types.  Currently,
    # only strings, booleans, ints, floats, datetime, and None are supported.
    #
    # Sometimes we want to convert Python strings into KGTK strings, and
    # sometimes into KGTK symbols.  The format string is used to distinguish
    # between these cases:
    #
    # '.': Use the Python datatype:
    #      string   -> string
    #      bool     -> boolean
    #      int      -> number
    #      float    -> number
    #      datetime -> date_and_times
    # 'b': bool -> boolean
    # 'c': int/float, int/float -> location_coordinates
    # 'd': datetime -> date_and_times
    # 'D': datetime, string/int -> date_and_times with precision
    # '#': int or float -> number
    # ':': string -> symbol
    # 'S': string, string -> language_qualified_string
    # 's': string -> string
    #
    # TODO: Support lists.
    def writef(self,
               raw_values: typing.List[typing.Any],
               format: typing.Optional[str] = None,
               shuffle_list: typing.Optional[typing.List[int]] = None):

        values: typing.List[str] = list()
        idx: int
        raw_value: typing.Any

        if format is None:
            for idx, raw_value in enumerate(raw_values):
                if isinstance(raw_value, str):
                    values.append(KgtkFormat.stringify(raw_value))
                elif isinstance(raw_value, (int, float)):
                    values.append(str(raw_value))
                elif isinstance(raw_value, bool):
                    values.append(KgtkFormat.to_boolean(raw_value))
                elif isinstance(raw_value, datetime):
                    values.append(KgtkFormat.from_datetime(raw_value))
                else:
                    raise ValueError("KgtkWriter: unsupported datatype in item %d: %s" % (idx, repr(raw_values)))
                
        else:
            fidx: int
            f: str
            for fidx, f in enumerate(format):
                if idx > len(raw_values):
                    raise ValueError("KgtkWriter: not enough values for format %d: %s %s" % (fidx, repr(format), repr(raw_values)))
                raw_value = raw_values[idx]
                idx += 1

                if raw_value is None:
                    values.append("")

                elif f == ".":
                    if isinstance(raw_value, str):
                        values.append(KgtkFormat.stringify(raw_value))
                    elif isinstance(raw_value, (int, float)):
                        values.append(str(raw_value))
                    elif isinstance(raw_value, bool):
                        values.append(KgtkFormat.to_boolean(raw_value))
                    elif isinstance(raw_value, datetime):
                        values.append(KgtkFormat.from_datetime(raw_value))
                    else:
                        raise ValueError("KgtkWriter: unsupported datatype in item %d: %s" % (idx, repr(raw_values)))

                elif f == 'b':
                    if isinstance(raw_value, bool):
                        values.append(KgtkFormat.to_boolean(raw_value))
                    else:
                        raise ValueError("KgtkWriter:  item %d was boolean, format was %s: %s" % (idx, f, repr(raw_values)))

                elif f == 'c':
                    if idx > len(raw_values):
                        raise ValueError("KgtkWriter: not enough values for second value in format %s: %s" % (repr(format), repr(raw_values)))
                    raw_value_2 = raw_values[idx]
                    idx += 1
                    values.append(KgtkFormat.lat_lon(lat, lon))

                elif f == 'd':
                    values.append(KgtkFormat.from_datetime(raw_value))

                elif f == 'D':
                    if idx > len(raw_values):
                        raise ValueError("KgtkWriter: not enough values for second value in format %s: %s" % (repr(format), repr(raw_values)))
                    raw_value_2 = raw_values[idx]
                    idx += 1
                    values.append(KgtkFormat.from_datetime(raw_value, precision=raw_value_2))

                elif f == '#':
                    values.append(str(raw_value))

                elif f == ':':
                    values.append(raw_value)

                elif f == 's':
                    values.append(KgtkFormat.stringify(raw_value))

                elif f == 'S':
                    if idx > len(raw_values):
                        raise ValueError("KgtkWriter: not enough values for second value in format %s: %s" % (repr(format), repr(raw_values)))
                    raw_value_2 = raw_values[idx]
                    idx += 1

                    values.append(KgtkFormat.stringify(raw_value, language=raw_value_2))

                else:
                    raise ValueError("KgtkWriter: unknown format %s" % (f))

            if idx < len(raw_values):
                raise ValueError("KgtkWriter: too many values for format %s: %s" % (repr(format), repr(raw_values)))
        
        if shuffle_list is not None:
            values = self.shuffle(values, shuffle_list)

        if len(values) != self.column_count:
            # Optionally fill missing trailing columns with empty values:
            if self.fill_missing_columns and len(values) < self.column_count:
                while len(values) < self.column_count:
                    values.append("")

            if len(values) != self.column_count:
                # Optionally validate that the line contained the right number of columns:
                #
                # When we report line numbers in error messages, line 1 is the first line after the header line.
                line: str
                if self.require_all_columns and len(values) < self.column_count:
                    line = self.column_separator.join(values)
                    raise ValueError("KgtkWriter: File %s: Required %d columns (%s) in output line %d, saw %d: %s" % (repr(self.file_path),
                                                                                                                      self.column_count,
                                                                                                                      repr(self.column_separator.join(self.column_names)),
                                                                                                                      self.line_count,
                                                                                                                      len(values),
                                                                                                                      repr(line)))
                if self.prohibit_extra_columns and len(values) > self.column_count:
                    line = self.column_separator.join(values)
                    raise ValueError("KgtkWriter: File %s: Required %d columns (%s)in output line %d, saw %d (%d extra): %s" % (repr(self.file_path),
                                                                                                                                self.column_count,
                                                                                                                                repr(self.column_separator.join(self.column_names)),
                                                                                                                                self.line_count,
                                                                                                                                len(values),
                                                                                                                                len(values) - self.column_count,
                                                                                                                                repr(line)))

        format_writer: typing.Optional[typing.Callable[[typing.List[str]], None]] = self.format_writers.get(self.output_format)
        if format_writer is None:
            raise ValueError("KgtkWriter: File %s: Unrecognized output format %s." % (repr(self.file_path), repr(self.output_format)))
        format_writer(values)

        self.line_count += 1
        if self.very_verbose:
            sys.stdout.write(".")
            sys.stdout.flush()

    def shortcut_copy_is_possible(self, kr: KgtkReader, new_column_names: typing.Optional[typing.List[str]]=None)->bool:
        if len(kr.column_names) != len(self.column_names):
            if self.verbose:
                print("Shortcut not possible: len(kr.column_names)=%d != len(kw.column_names)=%d" % (len(kr.column_names),
                                                                                                     len(self.column_names)),
                      file=self.error_file, flush=True)
            return False

        idx: int
        name: str
        for idx, name in enumerate(self.column_names):
            if name != kr.column_names[idx]:
                if self.verbose:
                    print("Shortcut not possible: kr.colum_names[%d]=%s != kw.column_names[%d]=%s" % (idx,
                                                                                                      repr(name),
                                                                                                      idx,
                                                                                                      repr(kr.column_names[idx])),
                          file=self.error_file, flush=True)
                return False

        if new_column_names is not None:
            if len(new_column_names) != len(self.column_names):
                if self.verbose:
                    print("Shortcut not possible: len(new_column_names)=%d != len(kw.column_names)=%d" % (len(new_column_names),
                                                                                                          len(self.column_names)),
                          file=self.error_file, flush=True)
                return False
            for idx, name in enumerate(new_column_names):
                if name != self.column_names[idx]:
                    if self.verbose:
                        print("Shortcut not possible: new_column_names[%d]=%s != kw.column_names[%d]=%s" % (idx,
                                                                                                            name,
                                                                                                            idx,
                                                                                                            self.column_names[idx]),
                              file=self.error_file, flush=True)
                    return False
        if self.column_separator != kr.options.column_separator:
            if self.verbose:
                print("Shortcut not possible: kr.options.column_separator=%s != kw.column_separator=%s" % (kr.options.column_separator,
                                                                                                           self.column_separator),
                       file=self.error_file, flush=True)
            return False

        if self.output_format is not None and self.output_format != self.OUTPUT_FORMAT_KGTK:
            if self.verbose:
                print("Shortcut not possible: kw.output_format=%s" % repr(self.output_format),
                      file=self.error_file, flush=True)
            return False

        if not kr.use_fast_path:
            if self.verbose:
                print("Shortcut not possible: kr does not use fast path", file=self.error_file, flush=True)
            return False

        if self.gzip_thread is not None:
            if self.verbose:
                print("Shortcut not possible: kw.gzip_thread is not None", file=self.error_file, flush=True)
            return False
        
        return True
        

    def copyfile(self, kr: KgtkReader, new_column_names: typing.Optional[typing.List[str]]=None)->int:
        """Copy all remaining rows from `kr` to our output stream.
        """
        input_data_lines: int = 0

        row: typing.List[str]
        if self.shortcut_copy_is_possible(kr, new_column_names):
            if self.verbose:
                print("Line by line file copy", file=self.error_file, flush=True)
            line: str
            for line in kr.source:
                input_data_lines += 1
                try:
                    self.file_out.write(line)

                except IOError as e:
                    if e.errno == errno.EPIPE:
                        pass # TODO: propogate a close backwards.                                                                                                                        else:
                        raise
            kr.source.close()
                
        elif new_column_names is not None and self.is_shuffle_needed(new_column_names):
            shuffle_list: typing.List[int] = self.build_shuffle_list(new_column_names)
            if self.verbose:
                print("Row by row file copy with a shuffle list: %s" % " ".join([str(x) for x in shuffle_list]), file=self.error_file, flush=True)
                    
            for row in kr:
                input_data_lines += 1
                self.write(row, shuffle_list=shuffle_list)
        else:
            if self.verbose:
                print("Row by row file copy", file=self.error_file, flush=True)
            for row in kr:
                input_data_lines += 1
                self.write(row)

        # Flush the output file so far:
        self.flush()
        return input_data_lines

    def write_kgtk(self, values: typing.List[str]):
        self.writeline(self.column_separator.join(values))

    def write_tsv(self, values: typing.List[str]):
        self.writeline(self.join_tsv(values))            

    def write_tsv_unquoted(self, values: typing.List[str]):
        self.writeline(self.join_tsv(values, unquoted=True))

    def write_tsv_unquoted_ep(self, values: typing.List[str]):
        self.writeline(self.join_tsv(values, unquoted=True, unescape_pipe=False))

    def write_tsv_csvlike(self, values: typing.List[str]):
        self.writeline(self.join_tsv(values, unquoted=True, unescape_pipe=False, csvlike=True))

    def write_csv(self, values: typing.List[str]):
        self.writeline(self.join_csv(values))

    def write_md(self, values: typing.List[str]):
        self.writeline(self.join_md(values))

    def write_json(self, values: typing.List[str]):
        self.writeline(",")
        self.writeline_noeol(json.dumps(self.reformat_values_for_json(values), indent=None, separators=(',', ':')))

    def write_json_map(self, values: typing.List[str]):
        if self.line_count == 1:
            self.writeline("")
        else:
            self.writeline(",")
        self.writeline_noeol(json.dumps(self.json_map(values), indent=None, separators=(',', ':')))

    def write_json_map_compact(self, values: typing.List[str]):
        if self.line_count == 1:
            self.writeline("")
        else:
            self.writeline(",")
        self.writeline_noeol(json.dumps(self.json_map(values, compact=True), indent=None, separators=(',', ':')))

    def write_jsonl(self, values: typing.List[str]):
        self.writeline(json.dumps(values, indent=None, separators=(',', ':')))

    def write_jsonl_map(self, values: typing.List[str]):
        self.writeline(json.dumps(self.json_map(values), indent=None, separators=(',', ':')))

    def write_jsonl_map_compact(self, values: typing.List[str]):
        self.writeline(json.dumps(self.json_map(values, compact=True), indent=None, separators=(',', ':')))

    table_buffer: typing.List[typing.List[str]] = [ ]
    def write_table(self, values: typing.List[str]):
        self.table_buffer.append(values.copy())

    def join_table(self, values: typing.List[str], col_widths: typing.List[int], fillchar: str = " ")->str:
        linebuf: typing.List[str] = ["|"]
        idx: int
        value: str
        for idx, value in enumerate(values):
            linebuf.append(" ")
            linebuf.append(value.ljust(col_widths[idx], fillchar))
            linebuf.append(" |")
        return "".join(linebuf)

    def finish_table(self):
        # Compute the initial column widths:
        col_widths: typing.List[int] = [ len(x) for x in self.output_column_names ]

        # Consider the widths of the buffered data:
        row: typing.List[str]
        for row in self.table_buffer:
            idx: int
            val: str
            for idx, val in enumerate(row):
                vallen: int = len(val)
                if vallen > col_widths[idx]:
                    col_widths[idx] = vallen

        # Output the header:
        self.writeline(self.join_table(self.output_column_names, col_widths))

        # Output the line of dashes under the header:
        self.writeline(self.join_table(["" for x in self.output_column_names], col_widths, fillchar="-"))

        # Output the saved data:
        for row in self.table_buffer:
            self.writeline(self.join_table(row, col_widths))
                       

    def writerow(self, row: typing.List[typing.Union[str, int, float, bool]]):
        # Convenience method for interoperability with csv.writer.
        # Don't forget to call kw.close() when done, though.
        try:
            newrow: typing.List[str] = [ ]
            item: typing.Union[str, int, float, bool]
            for item in row:
                newrow.append(str(item))
            self.write(newrow)
        except TypeError:
            print("KgtkWriter: File %s: TypeError on %s" % (repr(self.file_path), "[" + ", ".join([repr(x) for x in row]) + "]"), file=self.error_file, flush=True)
            raise

    def writerows(self, rows: typing.List[typing.List[typing.Union[str, int, float, bool]]]):
        # Convenience method for interoperability with csv.writer.
        # Don't forget to call kw.close() when done, though.
        row: typing.List[typing.Union[str, int, float, bool]]
        for row in rows:
            self.writerow(row)

    def flush(self):
        if self.gzip_thread is None:
            try:
                self.file_out.flush()
            except IOError as e:
                if e.errno == errno.EPIPE:
                    pass # Ignore.
                else:
                    raise

    def close(self):
        if self.output_format in [self.OUTPUT_FORMAT_JSON, self.OUTPUT_FORMAT_JSON_MAP, self.OUTPUT_FORMAT_JSON_MAP_COMPACT]:
            if self.verbose:
                print("Closing the JSON list.", file=self.error_file, flush=True)
            self.writeline("")
            self.writeline("]")
        elif self.output_format == self.OUTPUT_FORMAT_TABLE:
            if self.verbose:
                print("Writing the table buffer: %d rows." % len(self.table_buffer), file=self.error_file, flush=True)
            self.finish_table()

        elif self.output_format == self.OUTPUT_FORMAT_HTML:
            if self.verbose:
                print("Writing the HTML trailer.", file=self.error_file, flush=True)
            self.write_html_trailer()

        elif self.output_format == self.OUTPUT_FORMAT_HTML_COMPACT:
            if self.verbose:
                print("Writing the compact HTML trailer.", file=self.error_file, flush=True)
            self.write_html_trailer(compact=True)

        if self.gzip_thread is not None:
            if self.verbose:
                print("Closing the GZIP thread.", file=self.error_file, flush=True)
            self.gzip_thread.close()
        else:
            if self.file_path is None:
                if self.verbose:
                    print("KgtkWriter: not closing standard output", file=self.error_file, flush=True)
            else:
                if self.verbose:
                    print("KgtkWriter: closing the output file", file=self.error_file, flush=True)
                try:
                    self.file_out.close()
                except IOError as e:
                    if e.errno == errno.EPIPE:
                        pass # Ignore.
                    else:
                        raise

    def mapvalues(self, value_map: typing.Mapping[str, str])->typing.List[str]:
        # Optionally check for unexpected column names:
        if self.prohibit_extra_columns:
            for column_name in value_map.keys():
                if column_name not in self.column_name_map:
                    raise ValueError("KgtkWriter: File %s: Unexpected column name %s at data record %d" % (repr(self.file_path), column_name, self.line_count))

        values: typing.List[str] = [ ]
        for column_name in self.column_names:
            if column_name in value_map:
                values.append(value_map[column_name])
            elif self.require_all_columns:
                # TODO: throw a better exception.
                raise ValueError("KgtkWriter: File %s: Missing column %s at data record %d" % (repr(self.file_path), column_name, self.line_count))
            else:
                values.append("")
        return values

    def writemap(self, value_map: typing.Mapping[str, str]):
        """
        Write a map of values to the output file.
        """
        self.write(self.mapvalues(value_map))

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

    def is_shuffle_needed(self,
                          other_column_names: typing.List[str],
                          fail_on_unknown_column: bool = False)->bool:
        idx: int
        column_name: str
        for idx, column_name in enumerate(other_column_names):
            if column_name in self.column_name_map:
                if idx != self.column_name_map[column_name]:
                    return True # A shuffle is needed.
            elif fail_on_unknown_column:
                # TODO: throw a better exception
                raise ValueError("Unknown column name %s when considering shuffle list" % column_name)
            else:
                return True # This column is skipped, so a shuffle is needed.

        if len(other_column_names) < len(self.column_names):
            if self.fill_missing_columns:
                return False # A shuffle is not needed.
            return True # A shuffle is needed.
        
        return False # A shuffle is not needed.
    
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
