"""Count the unique values in a column in an KGTK file.  Generate an output
KGTK node or edge file with the counts.  Empty values are omitted from the
output KGTK file unless a non-empty substitute value is provided.

TODO: Consider other output formats. Perhaps seperate counts for each node1
(node2, etc.) value in the input file?

"""

from argparse import ArgumentParser, Namespace
import attr
from pathlib import Path
import re
import sys
import typing

from kgtk.kgtkformat import KgtkFormat
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
from kgtk.io.kgtkwriter import KgtkWriter
from kgtk.utils.argparsehelpers import optional_bool
from kgtk.value.kgtkvalueoptions import KgtkValueOptions

@attr.s(slots=True, frozen=True)
class Unique(KgtkFormat):
    input_file_path: typing.Optional[Path] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Path)))

    column_names: typing.Optional[typing.List[str]] = attr.ib() # TODO: complete this validator!

    output_file_path: typing.Optional[Path] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Path)))

    empty_value: str = attr.ib(validator=attr.validators.instance_of(str), default="")

    label_value: str = attr.ib(validator=attr.validators.instance_of(str), default="count")

    where_column_name: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    where_values: typing.Optional[typing.List[str]] = attr.ib(default=None) # TODO: Complete this validator!

    value_filter: str = attr.ib(validator=attr.validators.instance_of(str), default="")
    value_match_type: str = attr.ib(validator=attr.validators.instance_of(str), default="match")

    # TODO: make this an enum
    output_format: str = attr.ib(validator=attr.validators.instance_of(str), default="edge")
    prefix: str = attr.ib(validator=attr.validators.instance_of(str), default="")

    presorted: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    # TODO: find working validators
    # value_options: typing.Optional[KgtkValueOptions] = attr.ib(attr.validators.optional(attr.validators.instance_of(KgtkValueOptions)), default=None)
    reader_options: typing.Optional[KgtkReaderOptions]= attr.ib(default=None)
    value_options: typing.Optional[KgtkValueOptions] = attr.ib(default=None)

    error_file: typing.TextIO = attr.ib(default=sys.stderr)
    verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    very_verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    EDGE_FORMAT: str = "edge"
    NODE_FORMAT: str = "node"
    NODE_COUNTS_FORMAT: str = "node-counts"
    NODE_ONLY_FORMAT: str = "node-only"
    OUTPUT_FORMATS: typing.List[str] = [EDGE_FORMAT, NODE_FORMAT, NODE_COUNTS_FORMAT, NODE_ONLY_FORMAT]
    DEFAULT_FORMAT: str = EDGE_FORMAT

    def process_presorted(self,
                          output_columns: typing.List[str],
                          kr: KgtkReader,
                          column_idx: int,
                          where_column_idx: int,
                          where_value_set: typing.Set[str]):

        if self.verbose:
            print("Counting unique values from the %s column in presorted %s" % (kr.column_names[column_idx], self.input_file_path), file=self.error_file, flush=True)
        input_line_count: int = 0
        skip_line_count: int = 0
        skip_value_count: int = 0
        empty_value_count: int = 0
        unique_value_count: int = 0

        previous_value: typing.Optional[str] = None
        value_count: int

        if self.verbose:
            print("Opening the output file: %s" % self.output_file_path, file=self.error_file, flush=True)

        ew: KgtkWriter = KgtkWriter.open(output_columns,
                                         self.output_file_path,
                                         require_all_columns=False,
                                         prohibit_extra_columns=True,
                                         fill_missing_columns=True,
                                         use_mgzip=self.reader_options.use_mgzip if self.reader_options is not None else False, # Hack!
                                         mgzip_threads=self.reader_options.mgzip_threads if self.reader_options is not None else 3, # Hack!
                                         gzip_in_parallel=False,
                                         verbose=self.verbose,
                                         very_verbose=self.very_verbose)        

        value_filter_re: typing.Optional[typing.Pattern] = None if len(self.value_filter) == 0 else re.compile(self.value_filter)

        row: typing.List[str]
        for row in kr:
            input_line_count += 1
            if where_column_idx >= 0:
                if row[where_column_idx] not in where_value_set:
                    skip_line_count += 1
                    continue
            if len(row) <= column_idx:
                raise ValueError("Line %d: Short row (len(row)=%d, column_idx=%d): %s" % (input_line_count, len(row), column_idx, repr(row)))
            value: str = row[column_idx]

            if value_filter_re is not None:
                match: typing.Optional[typing.Match]
                if self.value_match_type == "fullmatch":
                    match = value_filter_re.fullmatch(value)
                elif self.value_match_type == "match":
                    match = value_filter_re.match(value)
                elif self.value_match_type == "search":
                    match = value_filter_re.search(value)
                if match is None:
                    skip_value_count += 1
                    continue

            if len(value) == 0:
                value = self.empty_value
            if len(value) > 0:
                value = self.prefix + value

            if previous_value is None:
                previous_value = value
                value_count = 1
                unique_value_count += 1

            else:
                if value < previous_value:
                    raise ValueError("Line %d: input is not presorted: value %s < previous value %s" % (input_line_count, repr(previous_value), repr(value)))

                if value == previous_value:
                    value_count += 1

                else:
                    if len(previous_value) == 0:
                        empty_value_count = value_count

                    elif self.output_format == self.EDGE_FORMAT:
                        ew.write([previous_value, self.label_value, str(value_count)])

                    elif self.output_format == self.NODE_ONLY_FORMAT:
                        ew.write([previous_value])

                    elif self.output_format == self.NODE_COUNTS_FORMAT:
                        ew.write([previous_value, str(value_count)])

                    else:
                        raise ValueError("Unknown output format %s" % str(self.output_format))

                    previous_value = value
                    value_count = 1
                    unique_value_count += 1

        if previous_value is not None:
            if len(previous_value) == 0:
                empty_value_count = value_count

            elif self.output_format == self.EDGE_FORMAT:
                ew.write([previous_value, self.label_value, str(value_count)])

            elif self.output_format == self.NODE_ONLY_FORMAT:
                ew.write([previous_value])

            elif self.output_format == self.NODE_COUNTS_FORMAT:
                ew.write([previous_value, str(value_count)])

            else:
                raise ValueError("Unknown output format %s" % str(self.output_format))
            

        if self.verbose:
            print("Read %d records, skipped %d, skipped %d values, found %d unique non-empty values, %d empty values." % (input_line_count,
                                                                                                                          skip_line_count,
                                                                                                                          skip_value_count,
                                                                                                                          unique_value_count,
                                                                                                                          empty_value_count),
                  file=self.error_file, flush=True)

        ew.close()

    def process_unsorted(self,
                         output_columns: typing.List[str],
                         kr: KgtkReader,
                         column_idxs: typing.List[int],
                         where_column_idx: int,
                         where_value_set: typing.Set[str]):

        if self.verbose:
            print("Counting unique values from the %s columns in %s" % (" ".join([repr(kr.column_names[column_idx]) for column_idx in column_idxs]),
                                                                        repr(str(self.input_file_path))), file=self.error_file, flush=True)
        input_line_count: int = 0
        skip_line_count: int = 0
        skip_value_count: int = 0
        empty_value_count: int = 0

        value_counts: typing.MutableMapping[str, int] = { }
        
        value_filter_re: typing.Optional[typing.Pattern] = None if len(self.value_filter) == 0 else re.compile(self.value_filter)

        row: typing.List[str]
        for row in kr:
            input_line_count += 1
            if where_column_idx >= 0:
                if row[where_column_idx] not in where_value_set:
                    skip_line_count += 1
                    continue
            column_idx: int
            for column_idx in column_idxs:
                if len(row) <= column_idx:
                    raise ValueError("Line %d: Short row (len(row)=%d, column_idx=%d): %s" % (input_line_count, len(row), column_idx, repr(row)))
                value: str = row[column_idx]

                if value_filter_re is not None:
                    match: typing.Optional[typing.Match]
                    if self.value_match_type == "fullmatch":
                        match = value_filter_re.fullmatch(value)
                    elif self.value_match_type == "match":
                        match = value_filter_re.match(value)
                    elif self.value_match_type == "search":
                        match = value_filter_re.search(value)
                    if match is None:
                        skip_value_count += 1
                        continue

                if len(value) == 0:
                    value = self.empty_value
                if len(value) > 0:
                    value = self.prefix + value
                    value_counts[value] = value_counts.get(value, 0) + 1
                else:
                    empty_value_count += 1
                
        if self.verbose:
            print("Read %d records, skipped %d, skipped %d values, found %d unique non-empty values, %d empty values." % (input_line_count,
                                                                                                                          skip_line_count,
                                                                                                                          skip_value_count,
                                                                                                                          len(value_counts),
                                                                                                                          empty_value_count),
                  file=self.error_file, flush=True)

        # In node format we can't open the output file until we are done
        # reading the input file, because we need the list of unique values to
        # build the column list.
        if self.output_format == self.NODE_FORMAT:
            for value in sorted(value_counts.keys()):
                # TODO: provide a way to override this check.
                if value in KgtkFormat.NODE1_COLUMN_NAMES:
                    raise ValueError("Cannot write a KGTK node file with a column named '%s'." % value)
                output_columns.append(value)
        
        if self.verbose:
            print("Opening the output file: %s" % self.output_file_path, file=self.error_file, flush=True)

        ew: KgtkWriter = KgtkWriter.open(output_columns,
                                         self.output_file_path,
                                         require_all_columns=False,
                                         prohibit_extra_columns=True,
                                         fill_missing_columns=True,
                                         use_mgzip=self.reader_options.use_mgzip if self.reader_options is not None else False, # Hack!
                                         mgzip_threads=self.reader_options.mgzip_threads if self.reader_options is not None else 3, # Hack!
                                         gzip_in_parallel=False,
                                         verbose=self.verbose,
                                         very_verbose=self.very_verbose)        

        if self.output_format == self.EDGE_FORMAT:
            for value in sorted(value_counts.keys()):
                ew.write([value, self.label_value, str(value_counts[value])])

        elif self.output_format == self.NODE_ONLY_FORMAT:
            for value in sorted(value_counts.keys()):
                ew.write([value])

        elif self.output_format == self.NODE_COUNTS_FORMAT:
            for value in sorted(value_counts.keys()):
                ew.write([value, str(value_counts[value])])

        elif self.output_format == self.NODE_FORMAT:
            row = [ kr.column_names[column_idx] ]
            for value in sorted(value_counts.keys()):
                row.append(str(value_counts[value]))
            ew.write(row)

        else:
            raise ValueError("Unknown output format %s" % str(self.output_format))

        if self.verbose:
            print("There were %d unique values." % len(value_counts), file=self.error_file, flush=True)

        ew.close()
       
    def process(self):
        # Open the input file.
        if self.verbose:
            if self.input_file_path is not None:
                print("Opening the input file: %s" % self.input_file_path, file=self.error_file, flush=True)
            else:
                print("Reading the input data from stdin", file=self.error_file, flush=True)

        output_columns: typing.List[str]
        if self.output_format == self.EDGE_FORMAT:
            output_columns = ["node1", "label", "node2"]

        elif self.output_format == self.NODE_ONLY_FORMAT:
            output_columns = [ "id" ]

        elif self.output_format == self.NODE_COUNTS_FORMAT:
            output_columns = [ "id", self.label_value ]

        elif self.output_format == self.NODE_FORMAT:
            output_columns = [ "id" ] # Add more later

        else:
            raise ValueError("Unknown output format %s" % str(self.output_format))
        
        kr: KgtkReader =  KgtkReader.open(self.input_file_path,
                                          error_file=self.error_file,
                                          options=self.reader_options,
                                          value_options = self.value_options,
                                          verbose=self.verbose,
                                          very_verbose=self.very_verbose,
        )

        column_idxs: typing.List[int]
        if self.column_names is None:
            if kr.node2_column_idx < 0:
                raise ValueError("No node2 default column name in the input file.")
            column_idxs = [ kr.node2_column_idx ]
        else:
            column_idxs = [ ]
            column_name: str
            for column_name in self.column_names:
                if column_name not in kr.column_name_map:
                    raise ValueError("Column %s is not in the input file" % (column_name))
                column_idxs.append(kr.column_name_map[column_name])

        where_column_idx: int = -1
        where_value_set: typing.Set[str] = { }
        if self.where_column_name is not None:
            if self.where_column_name not in kr.column_name_map:
                raise ValueError("Where column '%s' is not in the input file." % (self.where_column_name))
            where_column_idx = kr.column_name_map[self.where_column_name]
            if self.where_values is None or len(self.where_values) == 0:
                raise ValueError("Where column '%s' but no values to test." % (self.where_column_name))
            else:
                where_value_set = set(self.where_values)

        if self.presorted and self.output_format != self.NODE_FORMAT and len(column_idxs) == 1:
            self.process_presorted(output_columns, kr, column_idxs[0], where_column_idx, where_value_set)
        else:
            self.process_unsorted(output_columns, kr, column_idxs, where_column_idx, where_value_set)
       
def main():
    """
    Test the KGTK unique processor.
    """
    parser: ArgumentParser = ArgumentParser()

    parser.add_argument(dest="input_file_path", help="The KGTK file with the input data", type=Path, nargs="?")

    parser.add_argument(      "--column", dest="column_name", help="The column to count unique values (required).", required=True)

    parser.add_argument(      "--empty", dest="empty_value", help="A value to substitute for empty values (default=%(default)s).", default="")

    parser.add_argument("-o", "--output-file", dest="output_file_path", help="The KGTK file to write (default=%(default)s).", type=Path, default="-")

    parser.add_argument(      "--label", dest="label_value", help="The output file label column value (default=%(default)s).", default="count")

    # TODO: use an enum
    parser.add_argument(      "--format", dest="output_format", help="The output file format and mode (default=%(default)s).",
                              default=Unique.DEFAULT_FORMAT, choices=Unique.OUTPUT_FORMATS)

    parser.add_argument(      "--prefix", dest="prefix", help="The value prefix (default=%(default)s).", default="")

    parser.add_argument(      "--where", dest="where_column_name",
                              help="The name of a column for a record selection test. (default=%(default)s).", default=None)

    parser.add_argument(      "--in", dest="where_values", nargs="+",
                              help="The list of values for a record selection test. (default=%(default)s).", default=None)

    parser.add_argument(      "--presorted", dest="presorted", metavar="True|False",
                              help="When True, the input file is presorted. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    KgtkReader.add_debug_arguments(parser)
    KgtkReaderOptions.add_arguments(parser, mode_options=True)
    KgtkValueOptions.add_arguments(parser)

    args: Namespace = parser.parse_args()

    error_file: typing.TextIO = sys.stdout if args.errors_to_stdout else sys.stderr

    # Build the option structures.                                                                                                                          
    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_args(args)
    value_options: KgtkValueOptions = KgtkValueOptions.from_args(args)

   # Show the final option structures for debugging and documentation.                                                                                             
    if args.show_options:
        print("input: %s" % (str(args.input_file_path) if args.input_file_path is not None else "-"), file=error_file)
        print("--column=%s" % args.column_name, file=error_file)
        print("--empty=%s" % args.empty_value, file=error_file)
        print("--output-file=%s" % str(args.output_file_path), file=error_file)
        print("--label=%s" % args.label_value, file=error_file)
        print("--format=%s" % args.output_format, file=error_file)
        print("--prefix=%s" % args.prefix, file=error_file)
        if args.where_column_name is not None:
            print("--where=%s" % args.where_column_name, file=error_file)
        if args.where_values is not None and len(args.where_values) > 0:
            print("--in=%s" % " ".join(args.where_values), file=error_file)
        print("--prefix=%s" % repr(args.presorted), file=error_file)

        reader_options.show(out=error_file)
        value_options.show(out=error_file)

    uniq: Unique = Unique(
        input_file_path=args.input_file_path,
        column_name=args.column_name,
        output_file_path=args.output_file_path,
        empty_value=args.empty_value,
        label_value=args.label_value,
        output_format=args.output_format,
        prefix=args.prefix,
        where_column_name=args.where_column_name,
        where_values=args.where_values,
        presorted=args.presorted,
        reader_options=reader_options,
        value_options=value_options,
        error_file=error_file,
        verbose=args.verbose,
        very_verbose=args.very_verbose)

    uniq.process()

if __name__ == "__main__":
    main()
