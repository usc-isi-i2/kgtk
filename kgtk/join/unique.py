"""Count the unique values in a column in an KGTK file.  Generate an output
KGTK node or edge file with the counts.  Empty values are omitted from the
output KGTK file unless a non-empty substitute value is provided.

TODO: Consider other output formats. Perhaps seperate counts for each node1
(node2, etc.) value in the input file?

"""

from argparse import ArgumentParser, Namespace
import attr
from pathlib import Path
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

    column_name: str = attr.ib(validator=attr.validators.instance_of(str))

    output_file_path: typing.Optional[Path] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Path)))

    empty_value: str = attr.ib(validator=attr.validators.instance_of(str), default="")

    label_value: str = attr.ib(validator=attr.validators.instance_of(str), default="count")

    # TODO: make this an enum
    output_format: str = attr.ib(validator=attr.validators.instance_of(str), default="edge")
    prefix: str = attr.ib(validator=attr.validators.instance_of(str), default="")

    # TODO: find working validators
    # value_options: typing.Optional[KgtkValueOptions] = attr.ib(attr.validators.optional(attr.validators.instance_of(KgtkValueOptions)), default=None)
    reader_options: typing.Optional[KgtkReaderOptions]= attr.ib(default=None)
    value_options: typing.Optional[KgtkValueOptions] = attr.ib(default=None)

    error_file: typing.TextIO = attr.ib(default=sys.stderr)
    verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    very_verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    def process(self):
        # Open the input file.
        if self.verbose:
            if self.input_file_path is not None:
                print("Opening the input file: %s" % self.input_file_path, file=self.error_file, flush=True)
            else:
                print("Reading the input data from stdin", file=self.error_file, flush=True)

        kr: KgtkReader =  KgtkReader.open(self.input_file_path,
                                          error_file=self.error_file,
                                          options=self.reader_options,
                                          value_options = self.value_options,
                                          verbose=self.verbose,
                                          very_verbose=self.very_verbose,
        )

        if self.column_name not in kr.column_name_map:
            raise ValueError("Column %s is not in the input file" % (self.column_name))
        column_idx: int = kr.column_name_map[self.column_name]

        if self.verbose:
            print("Counting unique values from the %s column in %s" % (self.column_name, self.input_file_path), file=self.error_file, flush=True)
        input_line_count: int = 0

        value_counts: typing.MutableMapping[str, int] = { }
        
        row: typing.list[str]
        for row in kr:
            input_line_count += 1
            value: str = row[column_idx]
            if len(value) == 0:
                value = self.empty_value
            if len(value) > 0:
                value = self.prefix + value
                value_counts[value] = value_counts.get(value, 0) + 1
                
        if self.verbose:
            print("Read %d records, found %d unique non-empty values, %d empty values." % (input_line_count,
                                                                                           len(value_counts),
                                                                                           input_line_count - len(value_counts)),
                  file=self.error_file, flush=True)

        # No node mode we can't open the output file until we are done reading
        # the input file, because we need the list of uniqueue values to
        # build the column list.
        output_columns: typing.List[str]
        if self.output_format == "edge":
            output_columns = ["node1", "label", "node2"]
        elif self.output_format == "node":
            output_columns = [ "id" ]
            for value in sorted(value_counts.keys()):
                # TODO: provide a way to override this check.
                if value in KgtkFormat.NODE1_COLUMN_NAMES:
                    raise ValueError("Cannot write a KGTK node file with a column named '%s'." % value)
                output_columns.append(value)
        else:
            raise ValueError("Unknown output format %s" % str(self.output_format))
        
        if self.verbose:
            print("Opening the output file: %s" % self.output_file_path, file=self.error_file, flush=True)

        ew: KgtkWriter = KgtkWriter.open(output_columns,
                                         self.output_file_path,
                                         require_all_columns=False,
                                         prohibit_extra_columns=True,
                                         fill_missing_columns=True,
                                         gzip_in_parallel=False,
                                         verbose=self.verbose,
                                         very_verbose=self.very_verbose)        

        if self.output_format == "edge":
            for value in sorted(value_counts.keys()):
                ew.write([value, self.label_value, str(value_counts[value])])
        elif self.output_format == "node":
            row = [ self.column_name ]
            for value in sorted(value_counts.keys()):
                row.append(str(value_counts[value]))
            ew.write(row)
        else:
            raise ValueError("Unknown output format %s" % str(self.output_format))

        ew.close()
       
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
                              default="edge", choices=["edge", "node"])

    parser.add_argument(      "--prefix", dest="prefix", help="The value prefix (default=%(default)s).", default="")

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
        reader_options=reader_options,
        value_options=value_options,
        error_file=error_file,
        verbose=args.verbose,
        very_verbose=args.very_verbose)

    uniq.process()

if __name__ == "__main__":
    main()
