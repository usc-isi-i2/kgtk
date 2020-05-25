"""Copy records from the first ("left") KGTK file to the output file, if
a match is made with records in the second ("right") KGTK input file.

The fields to match may be supplied by the user.  If not supplied,
the following defaults will be used:

Left    Right   Key fields
edge    edge    left.node1 = right.node1 and left.label=right.label and left.node2=right.node2
node    node    left.id = right.id
edge    node    left.node1 = right.id
node    edge    right.id = left.node1

Note: By default, this implementation builds im-memory sets of all the key
values in the second file (the filter file). Optionally, it will cache the
first file (the input file) instead.

Note: By default, input records are passed in order to the output file.  When
the input file is cached, the output records are order by key value (alpha
sort), then by input order.  However, --preserve-order can be used to retain
the input file's order in the output file.

TODO: Study the time and space tradeoff between process_cacheing_input(...)
and process_cacheing_input_preserving_order(...).  Perhaps there's no reason
for both algorithms?
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
class KgtkIfExists(KgtkFormat):
    input_file_path: typing.Optional[Path] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Path)))
    input_keys: typing.Optional[typing.List[str]] = attr.ib(validator=attr.validators.optional(attr.validators.deep_iterable(member_validator=attr.validators.instance_of(str),
                                                                                                                            iterable_validator=attr.validators.instance_of(list))))

    filter_file_path: Path = attr.ib(validator=attr.validators.instance_of(Path))
    filter_keys: typing.Optional[typing.List[str]] = attr.ib(validator=attr.validators.optional(attr.validators.deep_iterable(member_validator=attr.validators.instance_of(str),
                                                                                                                             iterable_validator=attr.validators.instance_of(list))))

    output_file_path: typing.Optional[Path] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Path)))

    # The field separator used in multifield joins.  The KGHT list character should be safe.
    field_separator: str = attr.ib(validator=attr.validators.instance_of(str), default=KgtkFormat.LIST_SEPARATOR)

    invert: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    cache_input: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    preserve_order: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    # TODO: find working validators
    # value_options: typing.Optional[KgtkValueOptions] = attr.ib(attr.validators.optional(attr.validators.instance_of(KgtkValueOptions)), default=None)
    input_reader_options: typing.Optional[KgtkReaderOptions]= attr.ib(default=None)
    filter_reader_options: typing.Optional[KgtkReaderOptions]= attr.ib(default=None)
    value_options: typing.Optional[KgtkValueOptions] = attr.ib(default=None)

    error_file: typing.TextIO = attr.ib(default=sys.stderr)
    verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    very_verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    FIELD_SEPARATOR_DEFAULT: str = KgtkFormat.LIST_SEPARATOR
    
    def get_primary_key_column(self, kr: KgtkReader, who: str)->typing.List[int]:
        if kr.is_node_file:
            if kr.id_column_idx < 0:
                raise ValueError("The id column is missing from the %s node file." % who)
            return [ kr.id_column_idx ]
        elif kr.is_edge_file:
            if kr.node1_column_idx < 0:
                raise ValueError("The node1 column is missing from the %s node file." % who)
            return [ kr.node1_column_idx ]
        else:
            raise ValueError("The %s file is neither edge nor node." % who)

    def get_edge_key_columns(self, kr: KgtkReader, who: str)-> typing.List[int]:
        if not kr.is_edge_file:
            raise ValueError("get_edge_keys called on %s at wrong time." % who)
        if kr.node1_column_idx < 0:
            raise ValueError("The node1 column is missing from the %s edge file." % who)
        if kr.label_column_idx < 0:
            raise ValueError("The label column is missing from the %s edge file." % who)
        if kr.node2_column_idx < 0:
            raise ValueError("The node2 column is missing from the %s edge file." % who)
        return [ kr.node1_column_idx, kr.label_column_idx, kr.node2_column_idx ]

    def get_supplied_key_columns(self, supplied_keys: typing.List[str], kr: KgtkReader, who: str)->typing.List[int]:
        result: typing.List[int] = [ ]
        key: str
        for key in supplied_keys:
            if key not in kr.column_name_map:
                raise ValueError("Column %s is not in the %s file" % (key, who))
            result.append(kr.column_name_map[key])
        return result
    
    def get_key_columns(self, supplied_keys: typing.Optional[typing.List[str]], kr: KgtkReader, other_kr: KgtkReader, who: str)->typing.List[int]:
        if supplied_keys is not None and len(supplied_keys) > 0:
            return self.get_supplied_key_columns(supplied_keys, kr, who)

        if not (kr.is_node_file or kr.is_edge_file):
            raise ValueError("The %s file is a quasi-KGTK file.  Please supply its keys." % who)

        if kr.is_node_file or other_kr.is_node_file:
            return self.get_primary_key_column(kr, who)

        return self.get_edge_key_columns(kr, who)

    def build_key(self, row: typing.List[str], key_columns: typing.List[int])->str:
        key: str = ""
        idx: int
        first: bool = True
        for idx in key_columns:
            if first:
                first = False
            else:
                key += self.field_separator
            key += row[idx]
        return key

    def extract_key_set(self, kr: KgtkReader, who: str, key_columns: typing.List[int])->typing.Set[str]:
        key_set: typing.Set[str] = set()
        row: typing.List[str]
        for row in kr:
            key_set.add(self.build_key(row, key_columns))
        return key_set

    def extract_key_set_and_cache(self, kr: KgtkReader, who: str, key_columns: typing.List[int])->typing.Tuple[typing.Set[str], typing.List[typing.List[str]]]:
        key_set: typing.Set[str] = set()
        cache: typing.List[typing.List[str]] = [ ]
        row: typing.List[str]
        for row in kr:
            key_set.add(self.build_key(row, key_columns))
            cache.append(row)
        return key_set, cache

    def process_cacheing_filter(self,
                                input_kr: KgtkReader,
                                filter_kr: KgtkReader,
                                input_key_columns: typing.List[int],
                                filter_key_columns: typing.List[int],
                                ew: KgtkWriter):
        if self.verbose:
            print("Processing by cacheing the filter file's key set..")

        if self.verbose:
            print("Building the filter key set from %s" % self.filter_file_path, file=self.error_file, flush=True)
        key_set: typing.Set[str] = self.extract_key_set(filter_kr, "filter", filter_key_columns)
        if self.verbose or self.very_verbose:
            print("There are %d entries in the filter key set." % len(key_set), file=self.error_file, flush=True)
            if self.very_verbose:
                print("Keys: %s" % " ".join(key_set), file=self.error_file, flush=True)

        if self.verbose:
            print("Filtering records from %s" % self.input_file_path, file=self.error_file, flush=True)
        input_line_count: int = 0
        output_line_count: int = 0;

        # TODO: join these two code paths using xor?
        row: typing.List[str]
        input_key: str
        if self.invert:
            for row in input_kr:
                input_line_count += 1
                input_key = self.build_key(row, input_key_columns)
                if input_key not in key_set:
                    ew.write(row)
                    output_line_count += 1
        else:
            for row in input_kr:
                input_line_count += 1
                input_key = self.build_key(row, input_key_columns)
                if input_key in key_set:
                    ew.write(row)
                    output_line_count += 1

        if self.verbose:
            print("Read %d records, wrote %d records." % (input_line_count, output_line_count), file=self.error_file, flush=True)
        

    def process_cacheing_input(self,
                               input_kr: KgtkReader,
                               filter_kr: KgtkReader,
                               input_key_columns: typing.List[int],
                               filter_key_columns: typing.List[int],
                               ew: KgtkWriter):
        if self.verbose:
            print("Processing by cacheing the input file.")
        input_line_count: int = 0
        filter_line_count: int = 0
        output_line_count: int = 0
        
        # Map key values to lists of input and output data.
        inputmap: typing.MutableMapping[str, typing.List[typing.List[str]]] = { }
        outputmap: typing.MutableMapping[str, typing.List[typing.List[str]]] = { }

        if self.verbose:
            print("Reading the input data from %s" % self.input_file_path, file=self.error_file, flush=True)
        row: typing.List[str]
        for row in input_kr:
            input_line_count += 1
            input_key: str = self.build_key(row, input_key_columns)
            if input_key in inputmap:
                # Append the row to an existing list for that key.
                inputmap[input_key].append(row)
            else:
                # Create a new list of rows for this key.
                inputmap[input_key] = [ row ]

        if self.verbose:
            print("Applying the filter from %s" % self.filter_file_path, file=self.error_file, flush=True)
        filter_key: str
        if self.invert:
            outputmap = inputmap
            for row in filter_kr:
                filter_line_count += 1
                filter_key = self.build_key(row, filter_key_columns)
                if filter_key in outputmap:
                    del outputmap[filter_key]
        else:
            for row in filter_kr:
                filter_line_count += 1
                filter_key = self.build_key(row, filter_key_columns)
                if filter_key in inputmap:
                    outputmap[filter_key] = inputmap[filter_key]

        if self.verbose:
            print("Writing the output data to %s" % self.output_file_path, file=self.error_file, flush=True)

        # To simplify debugging, write the output data in sorted order (keys,
        # then input order).
        key: str
        for key in sorted(outputmap.keys()):
            for row in outputmap[key]:
                ew.write(row)
                output_line_count += 1

        if self.verbose:
            print("Read %d input records, read %d filter records, wrote %d records." % (input_line_count,
                                                                                        filter_line_count,
                                                                                        output_line_count),
                  file=self.error_file, flush=True)

    def process_cacheing_input_preserving_order(self,
                                                input_kr: KgtkReader,
                                                filter_kr: KgtkReader,
                                                input_key_columns: typing.List[int],
                                                filter_key_columns: typing.List[int],
                                                ew: KgtkWriter):
        # This algorithm preserves the input file's record order in the output file,
        # at the cost of extra work building keys.

        if self.verbose:
            print("Processing by cacheing the input file while preserving record order.")

        # Step one:  read the input file, cache it, and build the input key set
        if self.verbose:
            print("Building the input key set from %s" % self.input_file_path, file=self.error_file, flush=True)
        input_key_set: typing.Set[str]
        input_cache: typing.List[typing.List[str]]
        input_key_set, input_cache = self.extract_key_set_and_cache(input_kr, "input", input_key_columns)
        input_line_count: int = len(input_cache)
        if self.verbose or self.very_verbose:
            print("There are %d rows in the input cache." % input_line_count, file=self.error_file, flush=True)
            print("There are %d entries in the input key set." % len(input_key_set), file=self.error_file, flush=True)
            if self.very_verbose:
                print("Keys: %s" % " ".join(input_key_set), file=self.error_file, flush=True)

        # Step two: read the filter file and act on the key_set.
        output_key_set: typing.Set[str] = set()
        if self.verbose:
            print("Applying the filter from %s" % self.filter_file_path, file=self.error_file, flush=True)
        filter_key: str
        filter_line_count: int = 0
        row: typing.List[str]
        if self.invert:
            output_key_set = input_key_set
            for row in filter_kr:
                filter_line_count += 1
                filter_key = self.build_key(row, filter_key_columns)
                if filter_key in output_key_set:
                    output_key_set.remove(filter_key)
        else:
            for row in filter_kr:
                filter_line_count += 1
                filter_key = self.build_key(row, filter_key_columns)
                if filter_key in input_key_set:
                    output_key_set.add(filter_key)
        if self.verbose:
            print("Read %d rows from the filter file." % filter_line_count, file=self.error_file, flush=True)
            print("There are %d entries in the output key set." % len(output_key_set), file=self.error_file, flush=True)

        # Step three: read the input rows from the cache and write only the
        # ones with keys in the output key set.
        output_line_count: int = 0
        for row in input_cache:
            input_key: str = self.build_key(row, input_key_columns)
            if input_key in output_key_set:
                ew.write(row)
                output_line_count += 1
        if self.verbose:
            print("Wrote %d rows to the output file." % output_line_count, file=self.error_file, flush=True)
        
    def process(self):
        # Open the input files once.
        if self.verbose:
            if self.input_file_path is not None:
                print("Opening the input file: %s" % self.input_file_path, file=self.error_file, flush=True)
            else:
                print("Reading the input data from stdin", file=self.error_file, flush=True)

        input_kr: KgtkReader =  KgtkReader.open(self.input_file_path,
                                                error_file=self.error_file,
                                                who="input",
                                                options=self.input_reader_options,
                                                value_options = self.value_options,
                                                verbose=self.verbose,
                                                very_verbose=self.very_verbose,
        )

        if self.verbose:
            print("Opening the filter input file: %s" % self.filter_file_path, flush=True)
        filter_kr: KgtkReader = KgtkReader.open(self.filter_file_path,
                                                who="filter",
                                                error_file=self.error_file,
                                                options=self.filter_reader_options,
                                                value_options=self.value_options,
                                                verbose=self.verbose,
                                                very_verbose=self.very_verbose,
        )

        input_key_columns: typing.List[int] = self.get_key_columns(self.input_keys, input_kr, filter_kr, "input")
        filter_key_columns: typing.List[int] = self.get_key_columns(self.filter_keys, filter_kr, input_kr, "filter")

        if len(input_key_columns) != len(filter_key_columns):
            print("There are %d input key columns but %d filter key columns.  Exiting." % (len(input_key_columns), len(filter_key_columns)),
                  file=self.error_file, flush=True)
            return

        if self.verbose:
            print("Opening the output file: %s" % self.output_file_path, file=self.error_file, flush=True)
        ew: KgtkWriter = KgtkWriter.open(input_kr.column_names,
                                         self.output_file_path,
                                         mode=input_kr.mode,
                                         require_all_columns=False,
                                         prohibit_extra_columns=True,
                                         fill_missing_columns=True,
                                         gzip_in_parallel=False,
                                         verbose=self.verbose,
                                         very_verbose=self.very_verbose)

        if self.cache_input:
            if self.preserve_order:
                pass
                self.process_cacheing_input_preserving_order(input_kr=input_kr,
                                                             filter_kr=filter_kr,
                                                             input_key_columns=input_key_columns,
                                                             filter_key_columns=filter_key_columns,
                                                             ew=ew)
            else:
                self.process_cacheing_input(input_kr=input_kr,
                                            filter_kr=filter_kr,
                                            input_key_columns=input_key_columns,
                                            filter_key_columns=filter_key_columns,
                                            ew=ew)
        else:
            self.process_cacheing_filter(input_kr=input_kr,
                                         filter_kr=filter_kr,
                                         input_key_columns=input_key_columns,
                                         filter_key_columns=filter_key_columns,
                                         ew=ew)

        ew.close()

def main():
    """
    Test the KGTK file joiner.
    """
    parser: ArgumentParser = ArgumentParser()

    parser.add_argument(dest="input_file_path", help="The KGTK file with the input data", type=Path, nargs="?")

    parser.add_argument(      "--filter-on", dest="filter_file_path", help="The KGTK file with the filter data (required).", type=Path, required=True)

    parser.add_argument("-o", "--output-file", dest="output_file_path", help="The KGTK file to write (default=%(default)s).", type=Path, default="-")
    
    parser.add_argument(      "--field-separator", dest="field_separator", help="Separator for multifield keys (default=%(default)s)",
                              default=KgtkIfExists.FIELD_SEPARATOR_DEFAULT)
   
    parser.add_argument(      "--invert", dest="invert", help="Invert the test (if not exists) (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--cache-input", dest="cache_input", help="Cache the input file instead of the filter keys. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--preserve-order", dest="preserve_order", help="Preserve record order when cacheing the input file. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--input-keys", dest="input_keys", help="The key columns in the input file (default=None).", nargs='*')
    parser.add_argument(      "--filter-keys", dest="filter_keys", help="The key columns in the filter file (default=None).", nargs='*')

    KgtkReader.add_debug_arguments(parser)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, who="input")
    KgtkReaderOptions.add_arguments(parser, mode_options=True, who="filter")
    KgtkValueOptions.add_arguments(parser)

    args: Namespace = parser.parse_args()

    error_file: typing.TextIO = sys.stdout if args.errors_to_stdout else sys.stderr

    # Build the option structures.                                                                                                                          
    input_reader_options: KgtkReaderOptions = KgtkReaderOptions.from_args(args, who="input")
    filter_reader_options: KgtkReaderOptions = KgtkReaderOptions.from_args(args, who="filter")
    value_options: KgtkValueOptions = KgtkValueOptions.from_args(args)

   # Show the final option structures for debugging and documentation.                                                                                             
    if args.show_options:
        print("input: %s" % (str(args.input_file_path) if args.input_file_path is not None else "-"), file=error_file)
        print("--filter-on=%s" % str(args.filter_file_path), file=error_file)
        print("--output-file=%s" % str(args.output_file_path), file=error_file)
        print("--field-separator=%s" % repr(args.field_separator), file=error_file)
        print("--invert=%s" % str(args.invert), file=error_file)
        print("--cache-input=%s" % str(args.cache_input), file=error_file)
        print("--preserve-order=%s" % str(args.preserve_order), file=error_file)
        if args.input_keys is not None:
            print("--input-keys %s" % " ".join(args.input_keys), file=error_file)
        if args.filter_keys is not None:
            print("--filter-keys %s" % " ".join(args.filter_keys), file=error_file)
        input_reader_options.show(out=error_file, who="input")
        filter_reader_options.show(out=error_file, who="filter")
        value_options.show(out=error_file)

    ie: KgtkIfExists = KgtkIfExists(
        input_file_path=args.input_file_path,
        input_keys=args.input_keys,
        filter_file_path=args.filter_file_path,
        filter_keys=args.filter_keys,
        output_file_path=args.output_file_path,
        field_separator=args.field_separator,
        invert=args.invert,
        cache_input=args.cache_input,
        preserve_order=args.preserve_order,
        input_reader_options=input_reader_options,
        filter_reader_options=filter_reader_options,
        value_options=value_options,
        error_file=error_file,
        verbose=args.verbose,
        very_verbose=args.very_verbose)

    ie.process()

if __name__ == "__main__":
    main()
