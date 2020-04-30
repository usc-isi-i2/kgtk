"""
Read a KGTK edge file in TSV format.

TODO: Add support for alternative envelope formats, such as JSON.
"""

from argparse import ArgumentParser
import attr
import bz2
from enum import Enum
import gzip
import lz4 # type: ignore
import lzma
from multiprocessing import Process, Queue
from pathlib import Path
import sys
import typing

from kgtk.join.closableiter import ClosableIter, ClosableIterTextIOWrapper
from kgtk.join.enumnameaction import EnumNameAction
from kgtk.join.gzipprocess import GunzipProcess
from kgtk.join.kgtkbase import KgtkBase
from kgtk.join.kgtkformat import KgtkFormat
from kgtk.join.kgtkvalue import KgtkValue
from kgtk.join.validationaction import ValidationAction

@attr.s(slots=True, frozen=False)
class KgtkReader(KgtkBase, ClosableIter[typing.List[str]]):
    ERROR_LIMIT_DEFAULT: int = 1000
    GZIP_QUEUE_SIZE_DEFAULT: int = GunzipProcess.GZIP_QUEUE_SIZE_DEFAULT

    file_path: typing.Optional[Path] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Path)))
    source: ClosableIter[str] = attr.ib() # Todo: validate
    column_names: typing.List[str] = attr.ib(validator=attr.validators.deep_iterable(member_validator=attr.validators.instance_of(str),
                                                                                     iterable_validator=attr.validators.instance_of(list)))
    column_name_map: typing.Mapping[str, int] = attr.ib(validator=attr.validators.deep_mapping(key_validator=attr.validators.instance_of(str),
                                                                                               value_validator=attr.validators.instance_of(int)))

    # For convenience, the count of columns. This is the same as len(column_names).
    column_count: int = attr.ib(validator=attr.validators.instance_of(int))

    data_lines_read: int = attr.ib(validator=attr.validators.instance_of(int), default=0)
    data_lines_passed: int = attr.ib(validator=attr.validators.instance_of(int), default=0)
    data_lines_ignored: int = attr.ib(validator=attr.validators.instance_of(int), default=0)
    data_errors_reported: int = attr.ib(validator=attr.validators.instance_of(int), default=0)

    # The column separator is normally tab.
    column_separator: str = attr.ib(validator=attr.validators.instance_of(str), default=KgtkFormat.COLUMN_SEPARATOR)

    # supply a missing header record or override an existing header record.
    force_column_names: typing.Optional[typing.List[str]] = attr.ib(validator=attr.validators.optional(attr.validators.deep_iterable(member_validator=attr.validators.instance_of(str),
                                                                                                                                     iterable_validator=attr.validators.instance_of(list))),
                                                                    default=None)
    skip_first_record: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    # The index of the mandatory columns.  -1 means missing:
    node1_column_idx: int = attr.ib(validator=attr.validators.instance_of(int), default=-1) # edge file
    node2_column_idx: int = attr.ib(validator=attr.validators.instance_of(int), default=-1) # edge file
    label_column_idx: int = attr.ib(validator=attr.validators.instance_of(int), default=-1) # edge file
    id_column_idx: int = attr.ib(validator=attr.validators.instance_of(int), default=-1) # node file

    # How do we handle errors?
    error_file: typing.TextIO = attr.ib(default=sys.stderr)
    error_limit: int = attr.ib(validator=attr.validators.instance_of(int), default=ERROR_LIMIT_DEFAULT) # >0 ==> limit error reports

    # Ignore empty lines, comments, and all whitespace lines, etc.?
    empty_line_action: ValidationAction = attr.ib(validator=attr.validators.instance_of(ValidationAction), default=ValidationAction.EXCLUDE)
    comment_line_action: ValidationAction = attr.ib(validator=attr.validators.instance_of(ValidationAction), default=ValidationAction.EXCLUDE)
    whitespace_line_action: ValidationAction = attr.ib(validator=attr.validators.instance_of(ValidationAction), default=ValidationAction.EXCLUDE)

    # Ignore records with values in certain fields:
    blank_node1_line_action: ValidationAction = attr.ib(validator=attr.validators.instance_of(ValidationAction), default=ValidationAction.PASS) # EXCLUDE on edge file
    blank_node2_line_action: ValidationAction = attr.ib(validator=attr.validators.instance_of(ValidationAction), default=ValidationAction.PASS) # EXCLUDE on edge file
    blank_id_line_action: ValidationAction = attr.ib(validator=attr.validators.instance_of(ValidationAction), default=ValidationAction.PASS) # EXCLUDE on node file
    
    # Ignore records with too many or too few fields?
    short_line_action: ValidationAction = attr.ib(validator=attr.validators.instance_of(ValidationAction), default=ValidationAction.EXCLUDE)
    long_line_action: ValidationAction = attr.ib(validator=attr.validators.instance_of(ValidationAction), default=ValidationAction.EXCLUDE)

    # How should header errors be processed?
    header_error_action: ValidationAction = attr.ib(validator=attr.validators.instance_of(ValidationAction), default=ValidationAction.EXIT)
    unsafe_column_name_action: ValidationAction = attr.ib(validator=attr.validators.instance_of(ValidationAction), default=ValidationAction.REPORT)

    # Validate data cell values?
    invalid_value_action: ValidationAction = attr.ib(validator=attr.validators.instance_of(ValidationAction), default=ValidationAction.REPORT)

    # Repair records with too many or too few fields?
    fill_short_lines: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    truncate_long_lines: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    # Other implementation options?
    compression_type: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None) # TODO: use an Enum
    gzip_in_parallel: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    gzip_queue_size: int = attr.ib(validator=attr.validators.instance_of(int), default=GZIP_QUEUE_SIZE_DEFAULT)

    # Is this an edge file or a node file?
    is_edge_file: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    is_node_file: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    very_verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    class Mode(Enum):
        """
        There are four file reading modes:
        """
        NONE = 0 # Enforce neither edge nore node file required columns
        EDGE = 1 # Enforce edge file required columns
        NODE = 2 # Enforce node file require columns
        AUTO = 3 # Automatically decide whether to enforce edge or node file required columns

    @classmethod
    def open(cls,
             file_path: typing.Optional[Path],
             force_column_names: typing.Optional[typing.List[str]] = None,
             skip_first_record: bool = False,
             fill_short_lines: bool = False,
             truncate_long_lines: bool = False,
             error_file: typing.TextIO = sys.stderr,
             error_limit: int = ERROR_LIMIT_DEFAULT,
             empty_line_action: ValidationAction = ValidationAction.EXCLUDE,
             comment_line_action: ValidationAction = ValidationAction.EXCLUDE,
             whitespace_line_action: ValidationAction = ValidationAction.EXCLUDE,
             blank_line_action: ValidationAction = ValidationAction.EXCLUDE,
             blank_node1_line_action: typing.Optional[ValidationAction] = None,
             blank_node2_line_action: typing.Optional[ValidationAction] = None,
             blank_id_line_action: typing.Optional[ValidationAction] = None,
             short_line_action: ValidationAction = ValidationAction.EXCLUDE,
             long_line_action: ValidationAction = ValidationAction.EXCLUDE,
             invalid_value_action: ValidationAction = ValidationAction.REPORT,
             header_error_action: ValidationAction = ValidationAction.EXIT,
             unsafe_column_name_action: ValidationAction = ValidationAction.REPORT,
             compression_type: typing.Optional[str] = None,
             gzip_in_parallel: bool = False,
             gzip_queue_size: int = GZIP_QUEUE_SIZE_DEFAULT,
             column_separator: str = KgtkFormat.COLUMN_SEPARATOR,
             mode: Mode = Mode.AUTO,
             verbose: bool = False,
             very_verbose: bool = False)->"KgtkReader":
        """
        Opens a KGTK file, which may be an edge file or a node file.  The appropriate reader is returned.
        """
        source: ClosableIter[str] = cls._openfile(file_path,
                                                  compression_type=compression_type,
                                                  gzip_in_parallel=gzip_in_parallel,
                                                  gzip_queue_size=gzip_queue_size,
                                                  error_file=error_file,
                                                  verbose=verbose)

        # Read the kgtk file header and split it into column names.  We get the
        # header back, too, for use in debugging and error messages.
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

        # Should we automatically determine if this is an edge file or a node file?
        is_edge_file: bool = False
        is_node_file: bool = False
        if mode is KgtkReader.Mode.AUTO:
            # If we have a node1 (or alias) column, then this must be an edge file. Otherwise, assume it is a node file.
            node1_idx: int = cls.get_column_idx(cls.NODE1_COLUMN_NAMES,
                                                column_name_map,
                                                header_line=header,
                                                error_action=header_error_action,
                                                error_file=error_file,
                                                is_optional=True)
            if node1_idx >= 0:
                is_edge_file = True
                is_node_file = False
                if verbose:
                    print("%s column found, this is a KGTK edge file" % column_names[node1_idx], file=error_file, flush=True)
            else:
                is_edge_file = False
                is_node_file = True
                if verbose:
                    print("node1 column not found, assuming this is a KGTK node file", file=error_file, flush=True)

        elif mode is KgtkReader.Mode.EDGE:
            is_edge_file = True
        elif mode is KgtkReader.Mode.NODE:
            is_node_file = True
        elif mode is KgtkReader.Mode.NONE:
            pass

        if is_edge_file:
            # We'll instantiate an EdgeReader, which is a subclass of KgtkReader.
            # The EdgeReader import is deferred to avoid circular imports.
            from kgtk.join.edgereader import EdgeReader
            
            # Get the indices of the required columns.
            node1_column_idx: int
            node2_column_idx: int
            label_column_idx: int
            (node1_column_idx, node2_column_idx, label_column_idx) = cls.required_edge_columns(column_name_map,
                                                                                               header_line=header,
                                                                                               error_action=header_error_action,
                                                                                               error_file=error_file)

            if verbose:
                print("KgtkReader: Reading an edge file. node1=%d label=%d node2=%d" % (node1_column_idx, label_column_idx, node2_column_idx), file=error_file, flush=True)

            # Apply the proper defaults to the blank node1, node2, and id actions:
            if blank_node1_line_action is None:
                blank_node1_line_action = blank_line_action
            if blank_node2_line_action is None:
                blank_node2_line_action = blank_line_action
            if blank_id_line_action is None:
                blank_id_line_action = ValidationAction.PASS

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
                              fill_short_lines=fill_short_lines,
                              truncate_long_lines=truncate_long_lines,
                              error_file=error_file,
                              error_limit=error_limit,
                              empty_line_action=empty_line_action,
                              comment_line_action=comment_line_action,
                              whitespace_line_action=whitespace_line_action,
                              blank_node1_line_action=blank_node1_line_action,
                              blank_node2_line_action=blank_node2_line_action,
                              blank_id_line_action=blank_id_line_action,
                              short_line_action=short_line_action,
                              long_line_action=long_line_action,
                              invalid_value_action=invalid_value_action,
                              header_error_action=header_error_action,
                              unsafe_column_name_action=unsafe_column_name_action,
                              compression_type=compression_type,
                              gzip_in_parallel=gzip_in_parallel,
                              gzip_queue_size=gzip_queue_size,
                              is_edge_file=is_edge_file,
                              is_node_file=is_node_file,
                              verbose=verbose,
                              very_verbose=very_verbose)
        
        elif is_node_file:
            # We'll instantiate an NodeReader, which is a subclass of KgtkReader.
            # The NodeReader import is deferred to avoid circular imports.
            from kgtk.join.nodereader import NodeReader
            
            # Get the index of the required column:
            id_column_idx: int = cls.required_node_column(column_name_map,
                                                          header_line=header,
                                                          error_action=header_error_action,
                                                          error_file=error_file)

            if verbose:
                print("KgtkReader: Reading an node file. id=%d" % (id_column_idx), file=error_file, flush=True)

            # Apply the proper defaults to the blank node1, node2, and id actions:
            if blank_node1_line_action is None:
                blank_node1_line_action = ValidationAction.PASS
            if blank_node2_line_action is None:
                blank_node2_line_action = ValidationAction.PASS
            if blank_id_line_action is None:
                blank_id_line_action = blank_line_action

            return NodeReader(file_path=file_path,
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
                              blank_node1_line_action=blank_node1_line_action,
                              blank_node2_line_action=blank_node2_line_action,
                              blank_id_line_action=blank_id_line_action,
                              short_line_action=short_line_action,
                              long_line_action=long_line_action,
                              invalid_value_action=invalid_value_action,
                              header_error_action=header_error_action,
                              unsafe_column_name_action=unsafe_column_name_action,
                              compression_type=compression_type,
                              gzip_in_parallel=gzip_in_parallel,
                              gzip_queue_size=gzip_queue_size,
                              is_edge_file=is_edge_file,
                              is_node_file=is_node_file,
                              verbose=verbose,
                              very_verbose=very_verbose,
            )
        else:
            # Apply the proper defaults to the blank node1, node2, and id actions:
            if blank_node1_line_action is None:
                blank_node1_line_action = ValidationAction.PASS
            if blank_node2_line_action is None:
                blank_node2_line_action = ValidationAction.PASS
            if blank_id_line_action is None:
                blank_id_line_action = ValidationAction.PASS

            return cls(file_path=file_path,
                       source=source,
                       column_separator=column_separator,
                       column_names=column_names,
                       column_name_map=column_name_map,
                       column_count=len(column_names),
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
                       blank_id_line_action=blank_id_line_action,
                       short_line_action=short_line_action,
                       long_line_action=long_line_action,
                       invalid_value_action=invalid_value_action,
                       header_error_action=header_error_action,
                       unsafe_column_name_action=unsafe_column_name_action,
                       compression_type=compression_type,
                       gzip_in_parallel=gzip_in_parallel,
                       gzip_queue_size=gzip_queue_size,
                       is_edge_file=is_edge_file,
                       is_node_file=is_node_file,
                       verbose=verbose,
                       very_verbose=very_verbose,
            )

    @classmethod
    def _open_compressed_file(cls,
                              compression_type: str,
                              file_name: str,
                              file_or_path: typing.Union[Path, typing.TextIO],
                              who: str,
                              error_file: typing.TextIO,
                              verbose: bool)->typing.TextIO:
        
        # TODO: find a better way to coerce typing.IO[Any] to typing.TextIO
        if compression_type in [".gz", "gz"]:
            if verbose:
                print("%s: reading gzip %s" % (who, file_name), file=error_file, flush=True)
            return gzip.open(file_or_path, mode="rt") # type: ignore
        
        elif compression_type in [".bz2", "bz2"]:
            if verbose:
                print("%s: reading bz2 %s" % (who, file_name), file=error_file, flush=True)
            return bz2.open(file_or_path, mode="rt") # type: ignore
        
        elif compression_type in [".xz", "xz"]:
            if verbose:
                print("%s: reading lzma %s" % (who, file_name), file=error_file, flush=True)
            return lzma.open(file_or_path, mode="rt") # type: ignore
        
        elif compression_type in [".lz4", "lz4"]:
            if verbose:
                print("%s: reading lz4 %s" % (who, file_name), file=error_file, flush=True)
            return lz4.frame.open(file_or_path, mode="rt") # type: ignore
        else:
            # TODO: throw a better exception.
                raise ValueError("%s: Unexpected compression_type '%s'" % (who, compression_type))

    @classmethod
    def _openfile(cls, file_path: typing.Optional[Path],
                  compression_type: typing.Optional[str],
                  gzip_in_parallel: bool,
                  gzip_queue_size: int,
                  error_file: typing.TextIO,
                  verbose: bool)->ClosableIter[str]:
        who: str = cls.__name__
        if file_path is None or str(file_path) == "-":
            if compression_type is not None and len(compression_type) > 0:
                return ClosableIterTextIOWrapper(cls._open_compressed_file(compression_type, "-", sys.stdin, who, error_file, verbose))
            else:
                if verbose:
                    print("%s: reading stdin" % who, file=error_file, flush=True)
                return ClosableIterTextIOWrapper(sys.stdin)

        if verbose:
            print("%s: File_path.suffix: %s" % (who, file_path.suffix), file=error_file, flush=True)

        gzip_file: typing.TextIO
        if compression_type is not None and len(compression_type) > 0:
            gzip_file = cls._open_compressed_file(compression_type, str(file_path), file_path, who, error_file, verbose)
        elif file_path.suffix in [".bz2", ".gz", ".lz4", ".xz"]:
            gzip_file = cls._open_compressed_file(file_path.suffix, str(file_path), file_path, who, error_file, verbose)
        else:
            if verbose:
                print("%s: reading file %s" % (who, str(file_path)))
            return ClosableIterTextIOWrapper(open(file_path, "r"))

        if gzip_in_parallel:
            gzip_thread: GunzipProcess = GunzipProcess(gzip_file, Queue(gzip_queue_size))
            gzip_thread.start()
            return gzip_thread
        else:
            return ClosableIterTextIOWrapper(gzip_file)
            

    @classmethod
    def _build_column_names(cls,
                            source: ClosableIter[str],
                            force_column_names: typing.Optional[typing.List[str]],
                            skip_first_record: bool,
                            column_separator: str,
                            error_file: typing.TextIO,
                            verbose: bool = False,
    )->typing.Tuple[str, typing.List[str]]:
        """
        Read the kgtk file header and split it into column names.
        """
        column_names: typing.List[str]
        if force_column_names is None:
            # Read the column names from the first line, stripping end-of-line characters.
            #
            # TODO: if the read fails, throw a more useful exception with the line number.
            header: str = next(source).rstrip("\r\n")
            if verbose:
                print("header: %s" % header, file=error_file, flush=True)

            # Split the first line into column names.
            return header, header.split(column_separator)
        else:
            # Skip the first record to override the column names in the file.
            # Do not skip the first record if the file does not hae a header record.
            if skip_first_record:
                next(source)
            # Use the forced column names.
            return column_separator.join(force_column_names), force_column_names

    def close(self):
        self.source.close()

    def exclude_line(self, action: ValidationAction, msg: str, line: str)->bool:
        """
        Take a validation action.  Returns True if the line should be excluded.
        """
        result: bool
        if action == ValidationAction.PASS:
            return False # Silently pass the line through
        elif action == ValidationAction.REPORT:
            result= False # Report the issue then pass the line.
        elif action == ValidationAction.EXCLUDE:
            return True # Silently exclude the line
        elif action == ValidationAction.COMPLAIN:
            result = True # Report the issue then exclude the line.
        elif action == ValidationAction.ERROR:
            # Immediately raise an exception.
            raise ValueError("In input data line %d, %s: %s" % (self.data_lines_read, msg, line))
        elif action == ValidationAction.EXIT:
            print("In input data line %d, %s: %s" % (self.data_lines_read, msg, line), file=self.error_file, flush=True)
            sys.exit(1)
            
        print("In input data line %d, %s: %s" % (self.data_lines_read, msg, line), file=self.error_file, flush=True)
        self.data_errors_reported += 1
        if self.error_limit > 0 and self.data_errors_reported >= self.error_limit:
            raise ValueError("Too many data errors.")
        return result

    # This is both and iterable and an iterator object.
    def __iter__(self)->typing.Iterator[typing.List[str]]:
        return self

    # Get the next edge values as a list of strings.
    # TODO: Convert integers, coordinates, etc. to Python types
    def __next__(self)-> typing.List[str]:
        values: typing.List[str]

        # This loop accomodates lines that are ignored.
        while (True):
            line: str
            try:
                
                line = next(self.source) # Will throw StopIteration
            except StopIteration as e:
                # Close the input file!
                #
                # TODO: implement a close() routine and/or whatever it takes to support "with".
                self.source.close() # Do we need to guard against repeating this call?
                raise e

            # Count the data line read.
            self.data_lines_read += 1

            # Strip the end-of-line characters:
            line = line.rstrip("\r\n")

            if self.very_verbose:
                print("'%s'" % line, file=self.error_file, flush=True)

            # Ignore empty lines.
            if self.empty_line_action != ValidationAction.PASS and len(line) == 0:
                if self.exclude_line(self.empty_line_action, "saw an empty line", line):
                    continue

            # Ignore comment lines:
            if self.comment_line_action != ValidationAction.PASS  and line[0] == self.COMMENT_INDICATOR:
                if self.exclude_line(self.comment_line_action, "saw a comment line", line):
                    continue

            # Ignore whitespace lines
            if self.whitespace_line_action != ValidationAction.PASS and line.isspace():
                if self.exclude_line(self.whitespace_line_action, "saw a whitespace line", line):
                    continue

            values = line.split(self.column_separator)

            # Optionally fill missing trailing columns with empty values:
            if self.fill_short_lines and len(values) < self.column_count:
                while len(values) < self.column_count:
                    values.append("")
                    
            # Optionally remove extra trailing columns:
            if self.truncate_long_lines and len(values) > self.column_count:
                values = values[:self.column_count]

            # Optionally validate that the line contained the right number of columns:
            #
            # When we report line numbers in error messages, line 1 is the first line after the header line.
            if self.short_line_action != ValidationAction.PASS and len(values) < self.column_count:
                if self.exclude_line(self.short_line_action,
                                     "Required %d columns, saw %d: '%s'" % (self.column_count,
                                                                            len(values),
                                                                            line),
                                     line):
                    continue
                             
            if self.long_line_action != ValidationAction.PASS and len(values) > self.column_count:
                if self.exclude_line(self.long_line_action,
                                     "Required %d columns, saw %d (%d extra): '%s'" % (self.column_count,
                                                                                       len(values),
                                                                                       len(values) - self.column_count,
                                                                                       line),
                                     line):
                    continue

            if self._ignore_if_blank_fields(values, line):
                continue

            if self.invalid_value_action != ValidationAction.PASS:
                if self._ignore_invalid_values(values, line):
                    continue

            self.data_lines_passed += 1
            if self.very_verbose:
                sys.stdout.write(".")
                sys.stdout.flush()
            
            return values

    def _ignore_invalid_values(self, values: typing.List[str], line: str)->bool:
        """Give a row of values, validate each value.  If we find one or more
        validation problems, we might want to emit erro messages and we might
        want to ignore the entire row.

        Returns True to indicate that the row should be ignored (skipped).

        """
        problems: typing.List[str] = [ ] # Build a list of problems.
        idx: int
        value: str
        for idx, value in enumerate(values):
            if len(value) > 0: # Optimize the common case of empty columns.
                kv: KgtkValue = KgtkValue(value)
                if not kv.is_valid():
                    problems.append("%s: %s" % (self.column_names[idx], kv.describe()))

        if len(problems) == 0:
            return False

        return self.exclude_line(self.invalid_value_action,
                                 "; ".join(problems),
                                 line)

    # May be overridden
    def _ignore_if_blank_fields(self, values: typing.List[str], line: str)->bool:
        return False

    # May be overridden
    def _skip_reserved_fields(self, column_name)->bool:
        return False

    def additional_column_names(self)->typing.List[str]:
        if self.is_edge_file:
            return KgtkBase.additional_edge_columns(self.column_names)
        elif self.is_node_file:
            return KgtkBase.additional_node_columns(self.column_names)
        else:
            # TODO: throw a better exception.
            raise ValueError("KgtkReader: Unknown Kgtk file type.")

    def merge_columns(self, additional_columns: typing.List[str])->typing.List[str]:
        """
        Return a list that merges the current column names with an additional set
        of column names.

        """
        merged_columns: typing.List[str] = self.column_names.copy()

        column_name: str
        for column_name in additional_columns:
            if column_name in self.column_name_map:
                continue
            merged_columns.append(column_name)

        return merged_columns

    def to_map(self, row: typing.List[str])->typing.Mapping[str, str]:
        """
        Convert an input line into a named map of fields.
        """
        result: typing.MutableMapping[str, str] = { }
        value: str
        idx: int = 0
        for value in row:
            result[self.column_names[idx]] = value
            idx += 1
        return result

    @classmethod
    def add_shared_arguments(cls, parser: ArgumentParser):
        parser.add_argument(dest="kgtk_file", help="The KGTK file to read", type=Path, nargs="?")

        parser.add_argument(      "--blank-required-field-line-action", dest="blank_line_action",
                                  help="The action to take when a line with a blank node1, node2, or id field (per mode) is detected.",
                                  type=ValidationAction, action=EnumNameAction, default=ValidationAction.EXCLUDE)
                                  
        parser.add_argument(      "--comment-line-action", dest="comment_line_action",
                                  help="The action to take when a comment line is detected.",
                                  type=ValidationAction, action=EnumNameAction, default=ValidationAction.EXCLUDE)

        parser.add_argument(      "--column-separator", dest="column_separator",
                                  help="Column separator.", type=str, default=cls.COLUMN_SEPARATOR)

        parser.add_argument(      "--compression-type", dest="compression_type", help="Specify the compression type.")

        parser.add_argument(      "--empty-line-action", dest="empty_line_action",
                                  help="The action to take when an empty line is detected.",
                                  type=ValidationAction, action=EnumNameAction, default=ValidationAction.EXCLUDE)

        parser.add_argument(      "--errors-to-stdout", dest="errors_to_stdout",
                                  help="Send errors to stdout instead of stderr", action="store_true")

        parser.add_argument(      "--error-limit", dest="error_limit",
                                  help="The maximum number of errors to report before failing", type=int, default=cls.ERROR_LIMIT_DEFAULT)

        parser.add_argument(      "--fill-short-lines", dest="fill_short_lines",
                                  help="Fill missing trailing columns in short lines with empty values.", action='store_true')

        parser.add_argument(      "--force-column-names", dest="force_column_names", help="Force the column names.", nargs='+')

        parser.add_argument(      "--gzip-in-parallel", dest="gzip_in_parallel", help="Execute gzip in parallel.", action='store_true')

        parser.add_argument(      "--gzip-queue-size", dest="gzip_queue_size",
                                  help="Queue size for parallel gzip.", type=int, default=cls.GZIP_QUEUE_SIZE_DEFAULT)

        parser.add_argument(      "--header-error-action", dest="header_error_action",
                                  help="The action to take when a header error is detected  Only ERROR or EXIT are supported.",
                                  type=ValidationAction, action=EnumNameAction, default=ValidationAction.EXIT)

        parser.add_argument(      "--invalid-value-action", dest="invalid_value_action",
                                  help="The action to take when a data cell value is invalid.",
                                  type=ValidationAction, action=EnumNameAction, default=ValidationAction.REPORT)

        parser.add_argument(      "--long-line-action", dest="long_line_action",
                                  help="The action to take when a long line is detected.",
                                  type=ValidationAction, action=EnumNameAction, default=ValidationAction.EXCLUDE)

        parser.add_argument(      "--short-line-action", dest="short_line_action",
                                  help="The action to take when a short line is detected.",
                                  type=ValidationAction, action=EnumNameAction, default=ValidationAction.EXCLUDE)

        parser.add_argument(      "--skip-first-record", dest="skip_first_record", help="Skip the first record when forcing column names.", action='store_true')

        parser.add_argument(      "--truncate-long-lines", dest="truncate_long_lines",
                                  help="Remove excess trailing columns in long lines.", action='store_true')

        parser.add_argument(      "--unsafe-column-name-action", dest="unsafe_column_name_action",
                                  help="The action to take when a column name is unsafe.",
                                  type=ValidationAction, action=EnumNameAction, default=ValidationAction.REPORT)

        parser.add_argument("-v", "--verbose", dest="verbose", help="Print additional progress messages.", action='store_true')

        parser.add_argument(      "--very-verbose", dest="very_verbose", help="Print additional progress messages.", action='store_true')

        parser.add_argument(      "--whitespace-line-action", dest="whitespace_line_action",
                                  help="The action to take when a whitespace line is detected.",
                                  type=ValidationAction, action=EnumNameAction, default=ValidationAction.EXCLUDE)
                                  
    # May be overridden
    @classmethod
    def add_arguments(cls, parser: ArgumentParser):
        parser.add_argument(      "--mode", dest="mode",
                                  help="Determine the KGTK file mode.", type=KgtkReader.Mode, action=EnumNameAction, default=KgtkReader.Mode.AUTO)


    
def main():
    """
    Test the KGTK file reader.
    """
    # The EdgeReader import is deferred to avoid circular imports.
    from kgtk.join.edgereader import EdgeReader
    # The NodeReader import is deferred to avoid circular imports.
    from kgtk.join.nodereader import NodeReader

    parser = ArgumentParser()
    KgtkReader.add_shared_arguments(parser)
    KgtkReader.add_arguments(parser)
    EdgeReader.add_arguments(parser)
    NodeReader.add_arguments(parser)
    args = parser.parse_args()

    error_file: typing.TextIO = sys.stdout if args.errors_to_stdout else sys.stderr

    kr: KgtkReader = KgtkReader.open(args.kgtk_file,
                                     force_column_names=args.force_column_names,
                                     skip_first_record=args.skip_first_record,
                                     fill_short_lines=args.fill_short_lines,
                                     truncate_long_lines=args.truncate_long_lines,
                                     error_file = error_file,
                                     error_limit=args.error_limit,
                                     empty_line_action=args.empty_line_action,
                                     comment_line_action=args.comment_line_action,
                                     whitespace_line_action=args.whitespace_line_action,
                                     blank_line_action=args.blank_line_action,
                                     blank_node1_line_action=args.blank_node1_line_action,
                                     blank_node2_line_action=args.blank_node2_line_action,
                                     blank_id_line_action=args.blank_id_line_action,
                                     short_line_action=args.short_line_action,
                                     long_line_action=args.long_line_action,
                                     invalid_value_action=args.invalid_value_action,
                                     header_error_action=args.header_error_action,
                                     unsafe_column_name_action=args.unsafe_column_name_action,
                                     compression_type=args.compression_type,
                                     gzip_in_parallel=args.gzip_in_parallel,
                                     gzip_queue_size=args.gzip_queue_size,
                                     column_separator=args.column_separator,
                                     mode=args.mode,
                                     verbose=args.verbose, very_verbose=args.very_verbose)

    line_count: int = 0
    row: typing.List[str]
    for row in kr:
        line_count += 1
    print("Read %d lines" % line_count, file=error_file, flush=True)

if __name__ == "__main__":
    main()
