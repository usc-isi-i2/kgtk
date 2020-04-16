"""
Read a KGTK edge or node file in TSV format (common parts)

TODO: Add support for alternative envelope formats, such as JSON.
"""

import abc
from argparse import ArgumentParser
import attr
import bz2
import gzip
import lz4.frame # type: ignore
import lzma
from pathlib import Path
from multiprocessing import Queue
import sys
import typing

from kgtk.join.closableiter import ClosableIter, ClosableIterTextIOWrapper
from kgtk.join.gzipprocess import GunzipProcess
from kgtk.join.kgtk_format import KgtkFormat

@attr.s(slots=True, frozen=True)
class BaseReader(KgtkFormat, ClosableIter[typing.List[str]], metaclass=abc.ABCMeta):
    file_path: typing.Optional[Path] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Path)))
    source: ClosableIter[str] = attr.ib() # Todo: validate
    column_separator: str = attr.ib(validator=attr.validators.instance_of(str))
    column_names: typing.List[str] = attr.ib(validator=attr.validators.deep_iterable(member_validator=attr.validators.instance_of(str),
                                                                                     iterable_validator=attr.validators.instance_of(list)))
    column_name_map: typing.Mapping[str, int] = attr.ib(validator=attr.validators.deep_mapping(key_validator=attr.validators.instance_of(str),
                                                                                               value_validator=attr.validators.instance_of(int)))

    # For convenience, the count of columns. This is the same as len(column_names).
    column_count: int = attr.ib(validator=attr.validators.instance_of(int))

    # supply a missing header record or override an existing header record.
    force_column_names: typing.Optional[typing.List[str]] = attr.ib(validator=attr.validators.optional(attr.validators.deep_iterable(member_validator=attr.validators.instance_of(str),
                                                                                                       iterable_validator=attr.validators.instance_of(list))))
    skip_first_record: bool = attr.ib(validator=attr.validators.instance_of(bool))

    # Require or fill trailing fields?
    require_all_columns: bool = attr.ib(validator=attr.validators.instance_of(bool))
    prohibit_extra_columns: bool = attr.ib(validator=attr.validators.instance_of(bool))
    fill_missing_columns: bool = attr.ib(validator=attr.validators.instance_of(bool))

    # Ignore empty lines, comments, and all whitespace lines, etc.?
    ignore_empty_lines: bool = attr.ib(validator=attr.validators.instance_of(bool))
    ignore_comment_lines: bool = attr.ib(validator=attr.validators.instance_of(bool))
    ignore_whitespace_lines: bool = attr.ib(validator=attr.validators.instance_of(bool))

    # Other implementation options?
    gzip_in_parallel: bool = attr.ib(validator=attr.validators.instance_of(bool))
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

    # Is this an edge file or a node file?
    is_edge_file: bool = attr.ib(validator=attr.validators.instance_of(bool))
    is_node_file: bool = attr.ib(validator=attr.validators.instance_of(bool))

    verbose: bool = attr.ib(validator=attr.validators.instance_of(bool))
    very_verbose: bool = attr.ib(validator=attr.validators.instance_of(bool))


    GZIP_QUEUE_SIZE_DEFAULT: int = 1000

    @classmethod
    def _openfile(cls, file_path: typing.Optional[Path],
                  gzip_in_parallel: bool,
                  gzip_queue_size: int,
                  verbose: bool)->ClosableIter[str]:
        who: str = cls.__name__
        if file_path is None or str(file_path) == "-":
            if verbose:
                print("%s: reading stdin" % who)
            return ClosableIterTextIOWrapper(sys.stdin)

        if verbose:
            print("%s: File_path.suffix: %s" % (who, file_path.suffix))

        if file_path.suffix in [".bz2", ".gz", ".lz4", ".xz"]:
            # TODO: find a better way to coerce typing.IO[Any] to typing.TextIO
            gzip_file: typing.TextIO
            if file_path.suffix == ".gz":
                if verbose:
                    print("%s: reading gzip %s" % (who, str(file_path)))
                gzip_file = gzip.open(file_path, mode="rt") # type: ignore
            elif file_path.suffix == ".bz2":
                if verbose:
                    print("%s: reading bz2 %s" % (who, str(file_path)))
                gzip_file = bz2.open(file_path, mode="rt") # type: ignore
            elif file_path.suffix == ".xz":
                if verbose:
                    print("%s: reading lzma %s" % (who, str(file_path)))
                gzip_file = lzma.open(file_path, mode="rt") # type: ignore
            elif file_path.suffix == ".lz4":
                if verbose:
                    print("%s: reading lz4 %s" % (who, str(file_path)))
                gzip_file = lz4.frame.open(file_path, mode="rt") # type: ignore
            else:
                # TODO: throw a better exception.
                raise ValueError("%s: Unexpected file_path.suffix = '%s'" % (who, file_path.suffix))

            if gzip_in_parallel:
                gzip_thread: GunzipProcess = GunzipProcess(gzip_file, Queue(gzip_queue_size))
                gzip_thread.start()
                return gzip_thread
            else:
                return ClosableIterTextIOWrapper(gzip_file)
            
        else:
            if verbose:
                print("%s: reading file %s" % (who, str(file_path)))
            return ClosableIterTextIOWrapper(open(file_path, "r"))

    @classmethod
    def _build_column_names(cls,
                            source: ClosableIter[str],
                            force_column_names: typing.Optional[typing.List[str]],
                            skip_first_record: bool,
                            column_separator: str,
                            verbose: bool = False,
    )->typing.List[str]:
        """
        Read the kgtk file header and split it into column names.
        """
        column_names: typing.List[str]
        if force_column_names is None:
            # Read the column names from the first line.
            #
            # TODO: if the read fails, throw a more useful exception with the line number.
            header: str = next(source)
            if verbose:
                print("header: %s" % header)

            # Split the first line into column names.
            column_names = header.split(column_separator)
        else:
            # Skip the first record to override the column names in the file.
            # Do not skip the first record if the file does not hae a header record.
            if skip_first_record:
                next(source)
            # Use the forced column names.
            column_names = force_column_names
        return column_names

    def close(self):
        self.source.close()

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

            # Ignore empty lines.
            if len(line) == 0 and self.ignore_empty_lines:
                self.line_count[1] += 1
                continue
            # Ignore comment lines:
            if line[0] == self.COMMENT_INDICATOR and self.ignore_comment_lines:
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

            if self._ignore_if_blank_fields(values):
                continue

            self.line_count[0] += 1
            if self.very_verbose:
                sys.stdout.write(".")
                sys.stdout.flush()
            
            return values

    @abc.abstractmethod
    def _ignore_if_blank_fields(self, values: typing.List[str]):
        raise NotImplementedError

    @abc.abstractmethod
    def _skip_reserved_fields(self, column_name):
        raise NotImplementedError

    def merge_columns(self, additional_columns: typing.List[str])->typing.List[str]:
        """
        Return a list that merges the current column names with an additional set
        of column names, taking care to respect the use of column names
        aliases.

        """
        merged_columns: typing.List[str] = self.column_names.copy()

        column_name: str
        for column_name in additional_columns:
            if self._skip_reserved_fields(column_name):
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

    @classmethod
    def add_arguments(cls, parser: ArgumentParser):
        parser.add_argument(dest="kgtk_file", help="The KGTK file to read", type=Path, default=None)

        parser.add_argument(      "--column-separator", dest="column_separator",
                                  help="Column separator.", type=str, default=cls.COLUMN_SEPARATOR)

        parser.add_argument(      "--fill-missing-columns", dest="fill_missing_columns",
                                  help="Fill missing trailing columns in each line.", action='store_true')

        parser.add_argument(      "--force-column-names", dest="force_column_names", help="Force the column names.", nargs='*')

        parser.add_argument(      "--gzip-in-parallel", dest="gzip_in_parallel", help="Execute gzip in parallel.", action='store_true')

        parser.add_argument(      "--gzip-queue-size", dest="gzip_queue_size",
                                  help="Queue size for parallel gzip.", type=int, default=cls.GZIP_QUEUE_SIZE_DEFAULT)

        parser.add_argument(      "--no-ignore-comment-lines", dest="ignore_comment_lines",
                                  help="When specified, do not ignore comment lines.", action='store_false')

        parser.add_argument(      "--no-ignore-empty-lines", dest="ignore_empty_lines",
                                  help="When specified, do not ignore empty lines.", action='store_false')

        parser.add_argument(      "--no-ignore-whitespace-lines", dest="ignore_whitespace_lines",
                                  help="When specified, do not ignore whitespace lines.", action='store_false')

        parser.add_argument(      "--no-prohibit-extra-columns", dest="prohibit_extra_columns",
                                  help="When specified, do not prohibit extra columns in each line.", action='store_false')

        parser.add_argument(      "--no-require-all-columns", dest="require_all_columns",
                                  help="When specified, do not require all columns in each line.", action='store_false')

        parser.add_argument(      "--skip-first-record", dest="skip_first_record", help="Skip the first record when forcing column names.", action='store_true')

        parser.add_argument("-v", "--verbose", dest="verbose", help="Print additional progress messages.", action='store_true')

        parser.add_argument(      "--very-verbose", dest="very_verbose", help="Print additional progress messages.", action='store_true')
