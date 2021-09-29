"""
Read a KGTK file in TSV format using the fast path.
"""

import attr
import typing

from kgtk.io.kgtkreader import KgtkReader

@attr.s(slots=True, frozen=False)
class FastReader(KgtkReader):
# This is the fast read path.

    # Get the next edge values as a list of strings.
    def nextrow(self)-> typing.List[str]:
        line: str
        row: typing.List[str]

        # Read a line from the source
        try:
            line = next(self.source) # Will throw StopIteration when done.

        except StopIteration as e:
            # Close the input file!
            #
            # TODO: implement a close() routine and/or whatever it takes to support "with".
            self.source.close() # Do we need to guard against repeating this call?
            raise e

        # Count the data line read and passed on:
        self.data_lines_read += 1
        self.data_lines_passed += 1

        # Strip the end-of-line characters and split the fields:
        return line.rstrip("\r\n").split(self.options.column_separator)

@attr.s(slots=True, frozen=False)
class FilteredFastReader(KgtkReader):
# This is the fast read path with a filter.

    # Get the next edge values as a list of strings.
    def nextrow(self)-> typing.List[str]:
        line: str
        row: typing.List[str]

        while True:
            # Read a line from the source
            try:
                line = next(self.source) # Will throw StopIteration when done.

            except StopIteration as e:
                # Close the input file!
                #
                # TODO: implement a close() routine and/or whatever it takes to support "with".
                self.source.close() # Do we need to guard against repeating this call?
                raise e

            # Count the data line read and passed on:
            self.data_lines_read += 1

            if self.input_filter is not None:
                input_filter_idx: int
                input_filter_set: typing.Set[str]
                fail: bool = False
                for input_filter_idx, input_filter_set in self.input_filter.items():
                    value: str = row[input_filter_idx]
                    if value not in input_filter_set:
                        fail = True
                        break
                if fail:
                    self.data_lines_excluded_by_filter += 1
                    continue

            self.data_lines_passed += 1

            # Strip the end-of-line characters and split the fields:
            return line.rstrip("\r\n").split(self.options.column_separator)
