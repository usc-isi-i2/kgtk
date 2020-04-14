"""
Read a KGTK edge file in TSV format.

TODO: Add support for alternative envelope formats, such as JSON.
"""

import attr
import gzip
from pathlib import Path
from multiprocessing import Queue
import sys
import typing

from kgtk.join.gzipprocess import GunzipProcess
from kgtk.join.kgtk_format import KgtkFormat

@attr.s(slots=True, frozen=True)
class EdgeReader:
    file_path: typing.Optional[Path] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Path)))
    file_in: typing.TextIO = attr.ib() # Todo: validate TextIO
    column_separator: str = attr.ib(validator=attr.validators.instance_of(str))
    column_names: typing.List[str] = attr.ib(validator=attr.validators.deep_iterable(member_validator=attr.validators.instance_of(str),
                                                                                     iterable_validator=attr.validators.instance_of(list)))
    column_name_map: typing.Mapping[str, int] = attr.ib(validator=attr.validators.deep_mapping(key_validator=attr.validators.instance_of(str),
                                                                                               value_validator=attr.validators.instance_of(int)))

    # For convenience, the count of columns. This is the same as len(column_names).
    column_count: int = attr.ib(validator=attr.validators.instance_of(int))

    # The indices of the three mandatory columns:
    node1_column_idx: int = attr.ib(validator=attr.validators.instance_of(int))
    node2_column_idx: int = attr.ib(validator=attr.validators.instance_of(int)) # -1 means missing
    label_column_idx: int = attr.ib(validator=attr.validators.instance_of(int))

    # Require or fill trailing fields?
    require_all_columns: bool = attr.ib(validator=attr.validators.instance_of(bool))
    prohibit_extra_columns: bool = attr.ib(validator=attr.validators.instance_of(bool))
    fill_missing_columns: bool = attr.ib(validator=attr.validators.instance_of(bool))

    # Ignore empty lines, comments, and all whitespace lines, etc.?
    ignore_empty_lines: bool = attr.ib(validator=attr.validators.instance_of(bool))
    ignore_comment_lines: bool = attr.ib(validator=attr.validators.instance_of(bool))
    ignore_whitespace_lines: bool = attr.ib(validator=attr.validators.instance_of(bool))
    ignore_blank_node1_lines: bool = attr.ib(validator=attr.validators.instance_of(bool))
    ignore_blank_node2_lines: bool = attr.ib(validator=attr.validators.instance_of(bool))

    # Other implementation options?
    gzip_in_parallel: bool = attr.ib(validator=attr.validators.instance_of(bool))
    gzip_thread: typing.Optional[GunzipProcess] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(GunzipProcess)))
    gzip_queue_size: int = attr.ib(validator=attr.validators.instance_of(int))

    # When we report line numbers in error messages, line 1 is the first line after the header line.
    #
    # The use of a list is a sneaky way to get around the frozen class.
    # TODO: Find the right way to do this.  Don't freeze the class?
    #
    # line_count[0] Count of accepted lines
    # line_count[1] Count of ignored lines (comments, etc.)
    line_count: typing.List[int] = attr.ib(validator=attr.validators.deep_iterable(member_validator=attr.validators.instance_of(int),
                                                                                   iterable_validator=attr.validators.instance_of(list)))

    verbose: bool = attr.ib(validator=attr.validators.instance_of(bool))
    very_verbose: bool = attr.ib(validator=attr.validators.instance_of(bool))


    GZIP_QUEUE_SIZE_DEFAULT: int = 1000

    @classmethod
    def open(cls,
             file_path: typing.Optional[Path],
             require_all_columns: bool = True,
             prohibit_extra_columns: bool = True,
             fill_missing_columns: bool = False,
             ignore_empty_lines: bool = True,
             ignore_comment_lines: bool = True,
             ignore_whitespace_lines: bool = True,
             ignore_blank_node1_lines: bool = True,
             ignore_blank_node2_lines: bool = True,
             gzip_in_parallel: bool = False,
             gzip_queue_size: int = GZIP_QUEUE_SIZE_DEFAULT,
             column_separator: str = KgtkFormat.COLUMN_SEPARATOR,
             verbose: bool = False,
             very_verbose: bool = False)->"EdgeReader":
        if file_path is None or str(file_path) == "-":
            if verbose:
                print("EdgeReader: reading stdin")
            return cls._setup(file_path=None,
                              file_in=sys.stdin,
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
        
        if verbose:
            print("File_path.suffix: %s" % file_path.suffix)
        if file_path.suffix == ".gz":
            if verbose:
                print("EdgeReader: reading gzip %s" % str(file_path))

            # TODO: find a better way to coerce typing.IO[Any] to typing.TextIO
            gzip_file: typing.TextIO = gzip.open(file_path, mode="rt") # type: ignore
            return cls._setup(file_path=file_path,
                              file_in=gzip_file,
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
    
    @classmethod
    def _setup(cls,
               file_path: typing.Optional[Path],
               file_in: typing.TextIO,
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
        # Read the column names from the first line.
        #
        # TODO: if the read fails, throw a more useful exception with the line number.
        header: str = file_in.readline()
        if verbose:
            print("header: %s" % header)

        # Split the first line into column names.
        column_names: typing.List[str] = header.split(column_separator)

        # Validate the column names and build a map from column name to column index.
        column_name_map: typing.Mapping[str, int] = KgtkFormat.validate_kgtk_edge_columns(column_names)

        # Get the indices of the required columns.
        node1_column_idx: int = KgtkFormat.get_column_idx(KgtkFormat.NODE1_COLUMN_NAMES, column_name_map)
        node2_column_idx: int = KgtkFormat.get_column_idx(KgtkFormat.NODE2_COLUMN_NAMES, column_name_map)
        label_column_idx: int = KgtkFormat.get_column_idx(KgtkFormat.LABEL_COLUMN_NAMES, column_name_map)

        gzip_thread: typing.Optional[GunzipProcess] = None
        if gzip_in_parallel:
            gzip_thread = GunzipProcess(file_in, Queue(gzip_queue_size))
            gzip_thread.start()

        return cls(file_path=file_path,
                   file_in=file_in,
                   column_separator=column_separator,
                   column_names=column_names,
                   column_name_map=column_name_map,
                   column_count=len(column_names),
                   node1_column_idx=node1_column_idx,
                   node2_column_idx=node2_column_idx,
                   label_column_idx=label_column_idx,
                   require_all_columns=require_all_columns,
                   prohibit_extra_columns=prohibit_extra_columns,
                   fill_missing_columns=fill_missing_columns,
                   ignore_empty_lines=ignore_empty_lines,
                   ignore_comment_lines=ignore_comment_lines,
                   ignore_whitespace_lines=ignore_whitespace_lines,
                   ignore_blank_node1_lines=ignore_blank_node1_lines,
                   ignore_blank_node2_lines=ignore_blank_node2_lines,
                   gzip_in_parallel=gzip_in_parallel,
                   gzip_thread=gzip_thread,
                   gzip_queue_size=gzip_queue_size,
                   line_count=[1, 0], # TODO: find a better way to do this.
                   verbose=verbose,
                   very_verbose=very_verbose,
        )

    # This is an iterator object.
    def __iter__(self)-> typing.Iterator:
        return self

    # Get the next edge values as a list of strings.
    # TODO: Convert integers, coordinates, etc. to Python types
    def __next__(self)-> typing.List[str]:
        values: typing.List[str]

        # This loop accomodates lines that are ignored.
        while (True):
            line: str
            try:
                if self.gzip_thread is not None:
                    line = next(self.gzip_thread) # TODO: unify this
                else:
                    line = next(self.file_in) # Will throw StopIteration
            except StopIteration as e:
                # Close the input file!
                #
                # TODO: implement a close() routine and/or whatever it takes to support "with".
                self.file_in.close() # Do we need to guard against repeating this call?
                raise e

            # Ignore empty lines.
            if len(line) == 0 and self.ignore_empty_lines:
                self.line_count[1] += 1
                continue
            # Ignore comment lines:
            if line[0] == KgtkFormat.COMMENT_INDICATOR and self.ignore_comment_lines:
                self.line_count[1] += 1
                continue
            # Ignore whitespace lines
            if self.ignore_whitespace_lines and line.isspace():
                self.line_count[1] += 1
                continue

            values = line.split(self.column_separator)

            # Optionally validate that the line contained the right number of columns:
            #
            # When we report line numbers in error messages, line 1 is the first line after the header line.
            if self.require_all_columns and len(values) < self.column_count:
                raise ValueError("Required %d columns in input line %d, saw %d: '%s'" % (self.column_count, self.line_count[0], len(values), line))
            if self.prohibit_extra_columns and len(values) > self.column_count:
                raise ValueError("Required %d columns in input line %d, saw %d (%d extra): '%s'" % (self.column_count, self.line_count[0], len(values),
                                                                                                    len(values) - self.column_count, line))

            # Optionally fill missing trailing columns with empty values:
            if self.fill_missing_columns and len(values) < self.column_count:
                while len(values) < self.column_count:
                    values.append("")

            # Ignore lines with blank node1 fields.  This code comes after
            # filling missing trailing columns, although it could be reworked
            # to come first.
            if self.ignore_blank_node1_lines and self.node1_column_idx >= 0 and len(values) > self.node1_column_idx:
                node1_value: str = values[self.node1_column_idx]
                if len(node1_value) == 0 or node1_value.isspace():
                    self.line_count[1] += 1
                    continue

            # Ignore lines with blank node2 fields:
            if self.ignore_blank_node2_lines and self.node2_column_idx >= 0 and len(values) > self.node2_column_idx:
                node2_value: str = values[self.node2_column_idx]
                if len(node2_value) == 0 or node2_value.isspace():
                    self.line_count[1] += 1
                    continue

            self.line_count[0] += 1
            if self.very_verbose:
                sys.stdout.write(".")
                sys.stdout.flush()
            
            return values

    def merge_columns(self, additional_columns: typing.List[str])->typing.List[str]:
        """
        Return a list that merges the current column names with an additional set
        of column names, taking care to respect the use of column names
        aliases.

        """
        merged_columns: typing.List[str] = self.column_names.copy()

        column_name: str
        for column_name in additional_columns:
            if self.node1_column_idx >= 0 and column_name in KgtkFormat.NODE1_COLUMN_NAMES:
                continue
            if self.node2_column_idx >= 0 and column_name in KgtkFormat.NODE2_COLUMN_NAMES:
                continue
            if self.label_column_idx >= 0 and column_name in KgtkFormat.LABEL_COLUMN_NAMES:
                continue
            if column_name in self.column_name_map:
                continue
            merged_columns.append(column_name)

        return merged_columns

    def to_map(self, line: typing.List[str])->typing.Mapping[str, str]:
        """
        Convert an input line into a named map of fields.
        """
        result: typing.MutableMapping[str, str] = { }
        value: str
        idx: int = 0
        for value in line:
            result[self.column_names[idx]] = value
            idx += 1
        return result
