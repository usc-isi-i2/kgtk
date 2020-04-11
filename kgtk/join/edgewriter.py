"""
Read a KGTK edge file in TXV format.

TODO: Add support for decompression and alternative envelope formats,
such as JSON.
"""

import attr
import gzip
from pathlib import Path
from multiprocessing import Queue
import sys
from multiprocessing import Process
import typing

# This helper class supports running gzip in parallel.
#
# TODO: can we use attrs here?
class GzipProcess(Process):
    gzip_file: typing.TextIO = attr.ib() # Todo: validate TextIO

    # The line queue contains str with None as a plug.
    #
    # TODO: can we do a better job of type declaration here?
    line_queue: Queue = attr.ib(validator=attr.validators.instance_of(Queue))

    def __init__(self,  gzip_file: typing.TextIO, line_queue: Queue):
        super().__init__()
        self.gzip_file = gzip_file
        self.line_queue = line_queue

    def run(self):
        while True:
            line: typing.Optional[str] =  self.line_queue.get()
            if line is None: # This is the plug.
                self.gzip_file.close()
                return # Exit the process.
            gzip_file.write(line)

    # Called from the parent process.
    def write(self, line: str):
        self.line_queue.put(line)

    # Called from the parent process.
    def close(self):
        self.line_queue.put(None) # Send the plug.
        self.join() # Wait for the plug to exit the process.

@attr.s(slots=True, frozen=True)
class EdgeWriter:
    file_path: typing.Optional[Path] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Path)))
    file_out: typing.TextIO = attr.ib() # Todo: validate TextIO
    column_separator: str = attr.ib(validator=attr.validators.instance_of(str))
    column_names: typing.List[str] = attr.ib(validator=attr.validators.deep_iterable(member_validator=attr.validators.instance_of(str),
                                                                                     iterable_validator=attr.validators.instance_of(list)))

    # For convenience, the count of columns. This is the same as len(column_names).
    column_count: int = attr.ib(validator=attr.validators.instance_of(int))

    # Require or fill trailing fields?
    require_all_columns: bool = attr.ib(validator=attr.validators.instance_of(bool))
    prohibit_extra_columns: bool = attr.ib(validator=attr.validators.instance_of(bool))
    fill_missing_columns: bool = attr.ib(validator=attr.validators.instance_of(bool))

    # Other implementation options?
    gzip_in_parallel: bool = attr.ib(validator=attr.validators.instance_of(bool))
    gzip_thread: typing.Optional[GzipProcess] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(GzipProcess)))
    gzip_queue_size: int = attr.ib(validator=attr.validators.instance_of(int))

    # When we report line numbers in error messages, line 1 is the first line after the header line.
    #
    # The use of a list is a sneaky way to get around the frozen class.
    # TODO: Find the right way to do this.  Don't freeze the class?
    line_count: typing.List[int] = attr.ib(validator=attr.validators.deep_iterable(member_validator=attr.validators.instance_of(int),
                                                                                   iterable_validator=attr.validators.instance_of(list)))

    verbose: bool = attr.ib(validator=attr.validators.instance_of(bool))
    very_verbose: bool = attr.ib(validator=attr.validators.instance_of(bool))

    # TODO: There must be some place to import these constants
    NODE1_COLUMN_NAME: str = "node1"
    NODE2_COLUMN_NAME: str = "node2"
    LABEL_COLUMN_NAME: str = "label"

    GZIP_QUEUE_SIZE_DEFAULT: int = 1000

    @classmethod
    def open(cls,
             column_names: typing.List[str],
             file_path: typing.Optional[Path],
             require_all_columns: bool = True,
             prohibit_extra_columns: bool = True,
             fill_missing_columns: bool = False,
             gzip_in_parallel: bool = False,
             gzip_queue_size: int = GZIP_QUEUE_SIZE_DEFAULT,
             column_separator: str = "\t",
             verbose: bool = False,
             very_verbose: bool = False)->"EdgeWriter":
        if file_path is None or str(file_path) == "-":
            if verbose:
                print("EdgeWriter: writing stdout")
            return cls._setup(column_names=column_names,
                              file_path=None,
                              file_out=sys.stdout,
                              require_all_columns=require_all_columns,
                              prohibit_extra_columns=prohibit_extra_columns,
                              fill_missing_columns=fill_missing_columns,
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
                print("EdgeWriter: writing gzip %s" % str(file_path))

            # TODO: find a better way to coerce typing.IO[Any] to typing.TextIO
            gzip_file: typing.TextIO = gzip.open(file_path, mode="wt") # type: ignore
            return cls._setup(column_names=column_names,
                              file_path=file_path,
                              file_out=gzip_file,
                              require_all_columns=require_all_columns,
                              prohibit_extra_columns=prohibit_extra_columns,
                              fill_missing_columns=fill_missing_columns,
                              gzip_in_parallel=gzip_in_parallel,
                              gzip_queue_size=gzip_queue_size,
                              column_separator=column_separator,
                              verbose=verbose,
                              very_verbose=very_verbose,
            )
            
        else:
            if verbose:
                print("EdgeWriter: writing file %s" % str(file_path))
            return cls._setup(column_names=column_names,
                              file_path=file_path,
                              file_out=open(file_path, "w"),
                              require_all_columns=require_all_columns,
                              prohibit_extra_columns=prohibit_extra_columns,
                              fill_missing_columns=fill_missing_columns,
                              gzip_in_parallel=gzip_in_parallel,
                              gzip_queue_size=gzip_queue_size,
                              column_separator=column_separator,
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
               gzip_in_parallel: bool,
               gzip_queue_size: int,
               column_separator: str,
               verbose: bool = False,
               very_verbose: bool = False,
    )->"EdgeWriter":

        # Validate the column names.
        if EdgeWriter.NODE1_COLUMN_NAME not in column_names:
            # TODO: throw a better exception
            raise ValueError("Missing node1 column in the edge file header")

        if EdgeWriter.NODE2_COLUMN_NAME not in column_names:
            # TODO: throw a better exception
            raise ValueError("Missing node2 column in the edge file header")

        if EdgeWriter.LABEL_COLUMN_NAME not in column_names:
            # TODO: throw a better exception
            raise ValueError("Missing label column in the edge file header")

        # Write the column names to the first line.
        header: str = column_separator.join(column_names)
        if verbose:
            print("header: %s" % header)
        file_out.write(header + "\n") # Todo: use system end-of-line sequence?


        gzip_thread: typing.Optional[GzipProcess] = None
        if gzip_in_parallel:
            gzip_thread = GzipProcess(file_out, Queue(gzip_queue_size))
            gzip_thread.start()

        return cls(file_path=file_path,
                   file_out=file_out,
                   column_separator=column_separator,
                   column_names=column_names,
                   column_count=len(column_names),
                   require_all_columns=require_all_columns,
                   prohibit_extra_columns=prohibit_extra_columns,
                   fill_missing_columns=fill_missing_columns,
                   gzip_in_parallel=gzip_in_parallel,
                   gzip_thread=gzip_thread,
                   gzip_queue_size=gzip_queue_size,
                   line_count=[1], # TODO: find a better way to do this.
                   verbose=verbose,
                   very_verbose=very_verbose,
        )


    # Write the next list of edge values as a list of strings.
    # TODO: Convert integers, coordinates, etc. from Python types
    def write(self, values: typing.List[str]):
        # Optionally fill missing trailing columns with empty values:
        if self.fill_missing_columns and len(values) < self.column_count:
            while len(values) < self.column_count:
                values.append("")

        line: str = self.column_separator.join(values)

        # Optionally validate that the line contained the right number of columns:
        #
        # When we report line numbers in error messages, line 1 is the first line after the header line.
        if self.require_all_columns and len(values) < self.column_count:
            raise ValueError("Required %d columns in input line %d, saw %d: '%s'" % (self.column_count, self.line_count[0], len(values), line))
        if self.prohibit_extra_columns and len(values) > self.column_count:
            raise ValueError("Required %d columns in input line %d, saw %d (%d extra): '%s'" % (self.column_count, self.line_count[0], len(values),
                                                                                                len(values) - self.column_count, line))

        if self.gzip_thread is not None:
            self.gzip_thread.write(line + "\n")
        else:
            self.file_out.write(line + "\n")

        self.line_count[0] += 1
        if self.very_verbose:
            sys.stdout.write(".")
            sys.stdout.flush()

    def close(self):
        if self.gzip_thread is not None:
            self.gzip_thread.close()
        else:
            self.file_out.close()


