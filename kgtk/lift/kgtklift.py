"""lift

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
class KgtkLift(KgtkFormat):
    input_file_path: Path = attr.ib(validator=attr.validators.instance_of(Path))

    lift_column_names: typing.Optional[typing.List[str]] = \
        attr.ib(validator=attr.validators.optional(attr.validators.deep_iterable(member_validator=attr.validators.instance_of(str),
                                                                                 iterable_validator=attr.validators.instance_of(list))))
    output_file_path: Path = attr.ib(validator=attr.validators.instance_of(Path))
 
    node1_column_name: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    label_column_name: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    node2_column_name: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)

    label_column_value: typing.Optional[str] = attr.ib(validator=attr.validators.instance_of(str), default="label")
    lifted_column_suffix: str = attr.ib(validator=attr.validators.instance_of(str), default=";label")
    suppress_empty_columns: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

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

        node1_column_idx: int
        if self.node1_column_name is None:
            if kr.node1_column_idx < 0:
                raise ValueError("No node1 column index.")
            node1_column_idx = kr.node1_column_idx
        else:
            if self.node1_column_name not in kr.column_name_map:
                raise ValueError("Node1 column `%s` not found." % self.node1_column_name)
            node1_column_idx = kr.column_name_map[self.node1_column_name]

        label_column_idx: int
        if self.label_column_name is None:
            if kr.label_column_idx < 0:
                raise ValueError("No label column index.")
            label_column_idx = kr.label_column_idx
        else:
            if self.label_column_name not in kr.column_name_map:
                raise ValueError("Label column `%s` not found." % self.label_column_name)
            label_column_idx = kr.column_name_map[self.label_column_name]

        node2_column_idx: int
        if self.node2_column_name is None:
            if kr.node2_column_idx < 0:
                raise ValueError("No node2 column index.")
            node2_column_idx = kr.node2_column_idx
        else:
            if self.node2_column_name not in kr.column_name_map:
                raise ValueError("Node2 column `%s` not found." % self.node2_column_name)
            node2_column_idx = kr.column_name_map[self.node2_column_name]

        lift_column_idxs: typing.List[int] = [ ]
        if self.lift_column_names is not None and len(self.lift_column_names) > 0:
            # Process a custom list of columns to be lifted.
            lift_column_name: str
            for lift_column_name in self.lift_column_names:
                if lift_column_name not in kr.column_name_map:
                    raise ValueError("Unknown lift column %s." % lift_column_name)
                lift_column_idxs.append(kr.column_name_map[lift_column_name])
        else:
            # Use the edge file key columns with any overrides.
            lift_column_idxs.append(node1_column_idx)
            lift_column_idxs.append(label_column_idx)
            lift_column_idxs.append(node2_column_idx)

        input_line_count: int = 0
        label_line_count: int = 0
        output_line_count: int = 0

        input_rows: typing.List[typing.List[str]] = [ ]
        labels: typing.MutableMapping[str, str] = { }

        if self.verbose:
            print("Reading records from %s" % self.input_file_path, file=self.error_file, flush=True)
        row: typing.list[str]
        for row in kr:
            if row[label_column_idx] == self.label_column_value:
                # This is a label definition row.
                label_line_count += 1
                key: str = row[node1_column_idx]
                if key in labels:
                    # This label already exists in the table, build a list.
                    labels[key] += "|" + row[node2_column_idx]
                else:
                    # This is the first instance of this label definition.
                    labels[key] = row[node2_column_idx]
            else:
                input_rows.append(row)
                           
        lifted_column_idxs: typing.List[int] = [ ]
        if self.suppress_empty_columns:
            if self.verbose:
                print("Checking for empty columns", file=self.error_file, flush=True)
            lift_column_idxs_empties: typing.List[int] = lift_column_idxs.copy()
            lift_column_idx: int
            # Scan the input file, checking for empty output columns.
            for row in input_rows:
                idx: int
                restart: bool = True
                while restart:
                    # The restart mechanism compensates for modifying
                    # lift_column_idxs_empties inside the for loop, at the
                    # expense of potentially double testing some items.
                    restart = False
                    for idx, lift_column_idx in enumerate(lift_column_idxs_empties):
                        item: str = row[lift_column_idx]
                        if item in labels:
                            lift_column_idxs_empties.pop(idx)
                            restart = True
                            break
                if len(lift_column_idxs_empties) == 0:
                    break
            if self.verbose:
                if len(lift_column_idxs_empties) == 0:
                    print("No lifted columns are empty", file=self.error_file, flush=True)
                else:
                    lift_column_names_empties: typing.List[str] = [ ]
                    for idx in lift_column_idxs_empties:
                        lift_column_names_empties.append(kr.column_names[idx])
                    print("Unlifted columns: %s" % " ".join(lift_column_names_empties), file=self.error_file, flush=True)
            for lift_column_idx in lift_column_idxs:
                if lift_column_idx not in lift_column_idxs_empties:
                    lifted_column_idxs.append(lift_column_idx)            
        else:
            # Lift all the candidate columns.
            lifted_column_idxs = lift_column_idxs.copy()

        # Build the output column names.
        lifted_output_column_idxs: typing.List[int] = [ ]
        output_column_names: typing.list[str] = kr.column_names.copy()
        for idx in lifted_column_idxs:
            lifted_column_name: str = kr.column_names[idx] + self.lifted_column_suffix
            if lifted_column_name in kr.column_name_map:
                # Overwrite an existing lifted output column.
                #
                # TODO: DO we want to control whether or not we overwrite existing columns?
                lifted_output_column_idxs.append(kr.column_name_map[lifted_column_name])
            else:
                # Append a new lifted output column.
                lifted_output_column_idxs.append(len(output_column_names))
                output_column_names.append(lifted_column_name)
        new_columns: int = len(output_column_names) - len(kr.column_names)

        if self.verbose:
            print("Opening the output file: %s" % self.output_file_path, file=self.error_file, flush=True)
        ew: KgtkWriter = KgtkWriter.open(output_column_names,
                                         self.output_file_path,
                                         mode=kr.mode,
                                         require_all_columns=False,
                                         prohibit_extra_columns=True,
                                         fill_missing_columns=True,
                                         gzip_in_parallel=False,
                                         verbose=self.verbose,
                                         very_verbose=self.very_verbose)        

        if self.verbose:
            print("Writing output records", file=self.error_file, flush=True)

        for row in input_rows:
            output_row: typing.List[int] = row.copy()
            if new_columns > 0:
                output_row.extend([""] * new_columns)
                
            lifted_column_idx: int
            for idx, lifted_column_idx in enumerate(lifted_column_idxs):
                lifted_value: str = row[lifted_column_idx]
                if lifted_value in labels:
                    output_row[lifted_output_column_idxs[idx]] = labels[row[lifted_column_idx]]

            ew.write(output_row)
            output_line_count += 1


        if self.verbose:
            print("Read %d records." % (input_line_count), file=self.error_file, flush=True)
            print("%d records were labels." % (label_line_count), file=self.error_file, flush=True)
            print("%d symbols were labeled." % (len(labels)), file=self.error_file, flush=True)
            print("Wrote %d records." % (output_line_count), file=self.error_file, flush=True)
        
        ew.close()

def main():
    """
    Test the KGTK ifempty processor.
    """
    parser: ArgumentParser = ArgumentParser()

    parser.add_argument(dest="input_file_path", help="The KGTK file with the input data", type=Path, default="-")

    parser.add_argument(      "--node1-name", dest="node1_column_name",
                              help="The name of the node1 column. (default=node1 or alias).", default=None)

    parser.add_argument(      "--label-name", dest="label_column_name",
                              help="The name of the label column. (default=label).", default=None)

    parser.add_argument(      "--node2-name", dest="node2_column_name",
                              help="The name of the node2 column. (default=node1 or alias).", default=None)

    parser.add_argument(      "--label-value", dest="label_column_value", help="The value in the label column. (default=%(default)s).", default="label")
    parser.add_argument(      "--lift-suffix", dest="lifted_column_suffix", help="The value in the label column. (default=%(default)s).", default=";label")

    parser.add_argument(      "--columns-to-lift", dest="lift_column_names", help="The columns to lift. (default=[node1, label, node2]).", nargs='*')

    parser.add_argument("-o", "--output-file", dest="output_file_path", help="The KGTK file to write (default=%(default)s).", type=Path, default="-")
    
    parser.add_argument(      "--suppress-empty-columns", dest="suppress_empty_columns", help="If trye, suppress empty columns (default=%(default)s).",
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
        print("input: %s" % str(args.input_file_path), file=error_file, flush=True)
        if args.node1_column_name is not None:
            print("--node1-name=%s" % args.node1_column_name, file=error_file, flush=True)
        if args.label_column_name is not None:
            print("--label-name=%s" % args.label_column_name, file=error_file, flush=True)
        if args.node2_column_name is not None:
            print("--node2-name=%s" % args.node2_column_name, file=error_file, flush=True)
        print("--label-value=%s" % args.label_column_value, file=error_file, flush=True)
        print("--lift-suffix=%s" % args.lifted_column_suffix, file=error_file, flush=True)
        if args.lift_column_names is not None and len(args.lift_column_names) > 0:
            print("--columns-to-lift %s" % " ".join(args.lift_column_names), file=error_file, flush=True)
        print("--output-file=%s" % str(args.output_file_path), file=error_file, flush=True)
        print("--suppress-empty-columns=%s" % str(args.suppress_empty_columns))
        reader_options.show(out=error_file)
        value_options.show(out=error_file)

    kl: KgtkLift = KgtkLift(
        input_file_path=args.input_file_path,
        node1_column_name=args.node1_column_name,
        label_column_name=args.label_column_name,
        node2_column_name=args.node2_column_name,
        label_column_value=args.label_column_value,
        lifted_column_suffix=args.lifted_column_suffix,
        lift_column_names=args.lift_column_names,
        output_file_path=args.output_file_path,
        suppress_empty_columns=args.suppress_empty_columns,
        reader_options=reader_options,
        value_options=value_options,
        error_file=error_file,
        verbose=args.verbose,
        very_verbose=args.very_verbose)

    kl.process()

if __name__ == "__main__":
    main()
