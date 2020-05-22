"""Copy records from the first KGTK file to the output file,
expanding lists.

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
from kgtk.value.kgtkvalue import KgtkValue
from kgtk.value.kgtkvalueoptions import KgtkValueOptions

@attr.s(slots=True, frozen=True)
class KgtkExpand(KgtkFormat):
    input_file_path: typing.Optional[Path] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Path)))

    output_file_path: typing.Optional[Path] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Path)))

    key_column_names: typing.List[str] = attr.ib(validator=attr.validators.deep_iterable(member_validator=attr.validators.instance_of(str),
                                                                                         iterable_validator=attr.validators.instance_of(list)))

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

        # Build the list of key column edges:
        key_idx_list: typing.List[int] = [ ]
        if kr.is_edge_file:
            # Add the KGTK edge file required columns.
            key_idx_list.append(kr.node1_column_idx)
            key_idx_list.append(kr.label_column_idx)
            key_idx_list.append(kr.node2_column_idx)

        elif kr.is_node_file:
            # Add the KGTK node file required column:
            key_idx_list.append(kr.id_column_idx)

        # Append the key columns to the list of key column indixes,
        # silently removing duplicates, but complaining about unknown names.
        #
        # TODO: warn about duplicates?
        column_name: str
        for column_name in self.key_column_names:
            if column_name not in kr.column_name_map:
                raise ValueError("Column %s is not in the input file" % (column_name))
            key_idx: int = kr.column_name_map[column_name]
            if key_idx not in key_idx_list:
                key_idx_list.append(key_idx)
            
        # Open the output file.
        ew: KgtkWriter = KgtkWriter.open(kr.column_names,
                                         self.output_file_path,
                                         mode=kr.mode,
                                         require_all_columns=False,
                                         prohibit_extra_columns=True,
                                         fill_missing_columns=True,
                                         gzip_in_parallel=False,
                                         verbose=self.verbose,
                                         very_verbose=self.very_verbose)        
        
        if self.verbose:
            print("Expanding records from %s" % self.input_file_path, file=self.error_file, flush=True)
        input_line_count: int = 0
        output_line_count: int = 0;

        # Process the data records as list of KgtkValues.  Perhaps some day
        # this will lead to an optimization when validation is enabled.
        values: typing.list[KgtkValues]
        for values in kr.kgtk_values():
            input_line_count += 1

            # Convert the list of values to a list of list of strings.
            # Perhaps this should be an interface provided by KgtkReader,
            # although we do take special action for key columns.
            ll: typing.List[typing.List[str]] = [ ]
            idx: int
            value: KgtkValue
            for idx, value in enumerate(values):
                if idx in key_idx_list:
                    # Copy the key column values as-is, without looking for lists.
                    ll.append([ value.value ])
                else:
                    list_values: typing.List[KgtkValue] = value.get_list_items()
                    if len(list_values) == 0:
                        ll.append([ value.value ])
                    else:
                        l2: typing.List[str] = [ ]
                        v2: KgtkValue
                        for v2 in list_values:
                            l2.append(v2.value)
                        ll.append(l2)

            # Expand any lists into multiple rows.  The key columns are
            # repeated in each row, while lists are are expandd with one entry
            # from each remaining list on each row.
            more: bool = True
            while more:
                newrow: typing.List[str] = [ ]
                more = False
                l3: typing.List[str]
                for idx, l3 in enumerate(ll):
                    if idx in key_idx_list:
                        newrow.append(l3[0])
                    else:
                        if len(l3) == 0:
                            newrow.append("")
                        else:
                            newrow.append(l3.pop(0))
                            if len(l3) > 0:
                                more = True
                ew.write(newrow)
                output_line_count += 1

        if self.verbose:
            print("Read %d records, wrote %d records." % (input_line_count, output_line_count), file=self.error_file, flush=True)
        
        ew.close()

def main():
    """
    Test the KGTK ifempty processor.
    """
    parser: ArgumentParser = ArgumentParser()

    parser.add_argument(dest="input_file_path", help="The KGTK file with the input data (default=%(default)s)", type=Path, nargs="?", default="-")

    parser.add_argument(      "--columns", dest="key_column_names", help="The key columns will not be expanded (default=None).", nargs='+', default = [ ])

    parser.add_argument("-o", "--output-file", dest="output_file_path", help="The KGTK file to write (default=%(default)s).", type=Path, default="-")
    
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
        # TODO: show ifempty-specific options.
        print("input: %s" % str(args.input_file_path), file=error_file, flush=True)
        print("--columns %s" % " ".join(args.key_column_names), file=error_file, flush=True)
        print("--output-file=%s" % str(args.output_file_path))
        reader_options.show(out=error_file)
        value_options.show(out=error_file)

    ex: KgtkExpand = KgtkExpand(
        input_file_path=args.input_file_path,
        key_column_names=args.key_column_names,
        output_file_path=args.output_file_path,
        reader_options=reader_options,
        value_options=value_options,
        error_file=error_file,
        verbose=args.verbose,
        very_verbose=args.very_verbose)

    ex.process()

if __name__ == "__main__":
    main()
