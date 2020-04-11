"""
Read a KGTK edge file in TXV format.

TODO: Add support for decompression and alternative envelope formats,
such as JSON.
"""

import attr
import gzip
from pathlib import Path
import sys
import typing

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
    node2_column_idx: int = attr.ib(validator=attr.validators.instance_of(int))
    label_column_idx: int = attr.ib(validator=attr.validators.instance_of(int))

    # Require or fill trailing fields?
    require_all_columns: bool = attr.ib(validator=attr.validators.instance_of(bool))
    prohibit_extra_columns: bool = attr.ib(validator=attr.validators.instance_of(bool))
    fill_missing_columns: bool = attr.ib(validator=attr.validators.instance_of(bool))


    # TODO: There must be some place to import these constants
    NODE1_COLUMN_NAME: str = "node1"
    NODE2_COLUMN_NAME: str = "node2"
    LABEL_COLUMN_NAME: str = "label"
    

    @classmethod
    def open(cls,
             file_path: typing.Optional[Path],
             require_all_columns: bool = True,
             prohibit_extra_columns: bool = True,
             fill_missing_columns: bool = False,
             column_separator: str = "\t",
             verbose: bool = False)->"EdgeReader":
        if file_path is None or str(file_path) == "-":
            if verbose:
                print("EdgeReader: reading stdin")
            return cls._setup(file_path=None,
                              file_in=sys.stdin,
                              require_all_columns=require_all_columns,
                              prohibit_extra_columns=prohibit_extra_columns,
                              fill_missing_columns=fill_missing_columns,
                              column_separator=column_separator,
                              verbose=verbose)
        
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
                              column_separator=column_separator,
                              verbose=verbose)
            
        else:
            if verbose:
                print("EdgeReader: reading file %s" % str(file_path))
            return cls._setup(file_path=file_path,
                              file_in=open(file_path, "r"),
                              require_all_columns=require_all_columns,
                              prohibit_extra_columns=prohibit_extra_columns,
                              fill_missing_columns=fill_missing_columns,
                              column_separator=column_separator,
                              verbose=verbose)
    
    @classmethod
    def _setup(cls,
               file_path: typing.Optional[Path],
               file_in: typing.TextIO,
               require_all_columns: bool,
               prohibit_extra_columns: bool,
               fill_missing_columns: bool,
               column_separator: str,
               verbose: bool = False)->"EdgeReader":
        """
        Read the edge file header and split it into column names. Locate the three essential comumns.
        """
        # Read the column names from the first line.
        header: str = file_in.readline()
        if verbose:
            print("header: %s" % header)
        #
        # TODO: if the read fails, throw a useful exception.

        # Split the first line into column names.
        column_names: typing.List[str] = header.split(column_separator)
        if len(column_names) < 3:
            # TODO: throw a better exception
            raise ValueError("The edge file header must have at least three columns.")

        # Validate the column names and build a map from column name
        # to column index.
        column_name_map: typing.MutableMapping[str, int] = { }
        column_idx: int = 0 # There may be a more pythonic way to do this
        column_name: str
        for column_name in column_names:
            if column_name is None or len(column_name) == 0:
                # TODO: throw a better exception
                raise ValueError("Invalid column name in the edge file header")
            column_name_map[column_name] = column_idx
            column_idx += 1

        if EdgeReader.NODE1_COLUMN_NAME not in column_name_map:
            # TODO: throw a better exception
            raise ValueError("Missing node1 column in the edge file header")
        else:
            node1_column_idx: int = column_name_map[EdgeReader.NODE1_COLUMN_NAME]

        if EdgeReader.NODE2_COLUMN_NAME not in column_name_map:
            # TODO: throw a better exception
            raise ValueError("Missing node2 column in the edge file header")
        else:
            node2_column_idx: int = column_name_map[EdgeReader.NODE2_COLUMN_NAME]

        if EdgeReader.LABEL_COLUMN_NAME not in column_name_map:
            # TODO: throw a better exception
            raise ValueError("Missing label column in the edge file header")
        else:
            label_column_idx: int = column_name_map[EdgeReader.LABEL_COLUMN_NAME]

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
        )

    # This is an iterator object.
    def __iter__(self)-> typing.Iterator:
        return self

    # Get the next edge values as a list of strings.
    # TODO: Convert integers, coordinates, etc. to Python types
    def __next__(self)-> typing.List[str]:
        try:
            line: str = next(self.file_in) # Will throw StopIteration
        except StopIteration as e:
            # Close the input file!
            self.file_in.close() # Do we need to guard against repeating this call?
            raise e

        values: typing.List[str] = line.split(self.column_separator)

        # Optionally validate that the line contained the right number of columns:
        if self.require_all_columns and len(values) < self.column_count:
            raise ValueError("Required %d columns in input line, saw %d: '%s'" % (self.column_count, len(values), line))
        if self.prohibit_extra_columns and len(values) > self.column_count:
            raise ValueError("Required %d columns in input line, saw %d (%d extra): '%s'" % (self.column_count, len(values), len(values) - self.column_count, line))

        # Optionally fill missing trailing columns with empty values:
        if self.fill_missing_columns and len(values) < self.column_count:
            while len(values) < self.column_count:
                values.append("")
            
        return values
