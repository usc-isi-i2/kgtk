"""Copy records from the first KGTK file to the output file,
compacting lists.

The list compacting algorithm requires that input records with the same keyset
be grouped (not necessarily sorted).  kgtkcompact will sort its input
in-memory by default, but that can be disabled for large input files using an
external presorter.

"""

from argparse import ArgumentParser, Namespace
import attr
from pathlib import Path
import sys
import typing

from kgtk.kgtkformat import KgtkFormat
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
from kgtk.io.kgtkwriter import KgtkWriter
from kgtk.reshape.kgtkidbuilder import KgtkIdBuilder, KgtkIdBuilderOptions
from kgtk.utils.argparsehelpers import optional_bool
from kgtk.value.kgtkvalue import KgtkValue
from kgtk.value.kgtkvalueoptions import KgtkValueOptions

@attr.s(slots=True, frozen=False)
class KgtkCompact(KgtkFormat):
    input_file_path: typing.Optional[Path] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Path)))

    output_file_path: typing.Optional[Path] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Path)))

    key_column_names: typing.List[str] = attr.ib(validator=attr.validators.deep_iterable(member_validator=attr.validators.instance_of(str),
                                                                                         iterable_validator=attr.validators.instance_of(list)))
    compact_id: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    # The field separator used in multifield joins.  The KGHT list character should be safe.
    field_separator: str = attr.ib(validator=attr.validators.instance_of(str), default=KgtkFormat.LIST_SEPARATOR)

    sorted_input: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    verify_sort: bool = attr.ib(validator=attr.validators.instance_of(bool), default=True)

    build_id: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    idbuilder_options: typing.Optional[KgtkIdBuilderOptions] = attr.ib(default=None)

    # TODO: find working validators
    # value_options: typing.Optional[KgtkValueOptions] = attr.ib(attr.validators.optional(attr.validators.instance_of(KgtkValueOptions)), default=None)
    reader_options: typing.Optional[KgtkReaderOptions]= attr.ib(default=None)
    value_options: typing.Optional[KgtkValueOptions] = attr.ib(default=None)

    error_file: typing.TextIO = attr.ib(default=sys.stderr)
    verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    very_verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    # We unfroze this object to keep these rwitable fields around across
    # invocations of process_row.
    #
    # TODO: Introduce a row processing object?
    output_line_count: int = 0
    current_key: typing.Optional[str] = None
    current_row: typing.Optional[typing.List[str]] = None
    current_row_lists: typing.Optional[typing.List[typing.List[str]]] = None

    FIELD_SEPARATOR_DEFAULT: str = KgtkFormat.LIST_SEPARATOR

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

    def compact_row(self):
        if self.current_row_lists is None:
            return

        # Preallocate the list, this might be more efficient than appending to it..
        self.current_row = [None] * len(self.current_row_lists)
        idx: int
        item_list: typing.list[str]
        for idx, item_list in enumerate(self.current_row_lists):
            self.current_row[idx] = KgtkValue.join_sorted_list(item_list)
        self.current_row_lists = None

    def expand_row(self):
        # Expand the current row to row_lists.
        if self.current_row is None:
            return
        
        self.current_row_lists = [None] * len(self.current_row)
        idx: int
        item: str
        for idx, item in enumerate(self.current_row):
            self.current_row_lists[idx] = [item]

    def merge_row(self,  row: typing.List[str]):
        if self.current_row_lists is None:
            return
        idx: int
        item: str
        for idx, item in enumerate(row):
            if len(item) == 0:
                continue # Ignore empty items
            current_item_list: typing.List[str] = self.current_row_lists[idx]
            if len(current_item_list[0]) == 0:
                current_item_list[0] = item
                continue # Replace empty items in the row list.
            if item in current_item_list:
                continue # Ignore duplicate items
            self.current_row_lists[idx].append(item)

    def process_row(self,
                    input_key: str,
                    row: typing.List[str],
                    line_number: int,
                    idb: typing.Optional[KgtkIdBuilder],
                    ew: KgtkWriter,
                    flush: bool = False):
        # Note:  This code makes the assumption that row lengths do not vary!
        if self.current_key is not None:
            # We have a record being built.  Write it?
            if flush or self.current_key != input_key:
                # self.current_key != input_key means that the key is changing.
                self.compact_row()
                if self.current_row is not None:
                    if idb is None:
                        ew.write(self.current_row)
                    else:
                        ew.write(idb.build(self.current_row, line_number))
                self.current_key = None
                self.current_row = None

        if flush:
            # This was a flush request.  We're done.
            return

        # Are we starting a new key?
        if self.current_key is None:
            # Save the new row as the current row.  If the next row
            # doesn't have the same input key, we'll write this
            # row out with a minimum of handling.
            self.current_key = input_key
            self.current_row = row
            return

        if self.current_row_lists is None:
            self.expand_row()
        self.merge_row(row)

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

        # If requested, creat the ID column builder.
        # Assemble the list of output column names.
        output_column_names: typing.List[str]
        idb: typing.Optional[KgtkIdBuilder] = None
        if self.build_id:
            if self.idbuilder_options is None:
                raise ValueError("ID build requested but ID builder options are missing")
            idb = KgtkIdBuilder.new(kr, self.idbuilder_options)
            output_column_names = idb.column_names
        else:
            output_column_names = kr.column_names

        # Build the list of key column edges:
        key_idx_list: typing.List[int] = [ ]
        if kr.is_edge_file:
            # Add the KGTK edge file required columns.
            key_idx_list.append(kr.node1_column_idx)
            key_idx_list.append(kr.label_column_idx)
            key_idx_list.append(kr.node2_column_idx)
            if not self.compact_id and kr.id_column_idx >= 0:
                key_idx_list.append(kr.id_column_idx)

        elif kr.is_node_file:
            # Add the KGTK node file required column:
            key_idx_list.append(kr.id_column_idx)

        # Append additinal columns to the list of key column indixes,
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

        if self.verbose:
            key_idx_list_str: typing.List[str] = [ ]
            for key_idx in key_idx_list:
                key_idx_list_str.append(str(key_idx))
            print("key indexes: %s" % " ".join(key_idx_list_str))
            
        # Open the output file.
        ew: KgtkWriter = KgtkWriter.open(output_column_names,
                                         self.output_file_path,
                                         mode=kr.mode,
                                         require_all_columns=False,
                                         prohibit_extra_columns=True,
                                         fill_missing_columns=True,
                                         gzip_in_parallel=False,
                                         verbose=self.verbose,
                                         very_verbose=self.very_verbose)        
        input_line_count: int = 0
        row: typing.List[str] = [ ]
        input_key: str
        prev_input_key: typing.Optional[str] = None
        going_up: typing.Optional[bool] = None
        if self.sorted_input:
            if self.verbose:
                print("Reading the input data from %s" % self.input_file_path, file=self.error_file, flush=True)
            for row in kr:
                input_line_count += 1
                input_key = self.build_key(row, key_idx_list)
                if self.verify_sort:
                    if prev_input_key is None:
                        prev_input_key = input_key
                    else:
                        if going_up is None:
                            if prev_input_key < input_key:
                                going_up = True
                                prev_input_key = input_key
                            elif prev_input_key > input_key:
                                going_up = False
                                prev_input_key = input_key
                            else:
                                pass # No change in input key
                        elif going_up:
                            if prev_input_key < input_key:
                                prev_input_key = input_key
                            elif prev_input_key > input_key:
                                raise ValueError("Line %d sort violation going up: prev='%s' curr='%s'" % (input_line_count, prev_input_key, input_key))
                            else:
                                pass # No change in input_key
                        else:
                            if prev_input_key > input_key:
                                prev_input_key = input_key
                            elif prev_input_key < input_key:
                                raise ValueError("Line %d sort violation going down: prev='%s' curr='%s'" % (input_line_count, prev_input_key, input_key))
                            else:
                                pass # No change in input_key
                            
                self.process_row(input_key, row, input_line_count, idb, ew)
            
        else:
            if self.verbose:
                print("Sorting the input data from %s" % self.input_file_path, file=self.error_file, flush=True)
            # Map key values to lists of input and output data.
            input_map: typing.MutableMapping[str, typing.List[typing.List[str]]] = { }

            for row in kr:
                input_line_count += 1
                input_key = self.build_key(row, key_idx_list)
                if input_key in input_map:
                    # Append the row to an existing list for that key.
                    input_map[input_key].append(row)
                else:
                    # Create a new list of rows for this key.
                    input_map[input_key] = [ row ]

            if self.verbose:
                print("Processing the sorted input data", file=self.error_file, flush=True)
            
            for input_key in sorted(input_map.keys()):
                for row in input_map[input_key]:
                    self.process_row(input_key, row, input_line_count, idb, ew)

        # Flush the final row, if any.  We pass the last row read for
        # feedback, such as an ID uniqueness violation.
        self.process_row("", row, input_line_count, idb, ew, flush=True)
        
        if self.verbose:
            print("Read %d records, wrote %d records." % (input_line_count, self.output_line_count), file=self.error_file, flush=True)
        
        ew.close()

def main():
    """
    Test the KGTK compact processor.
    """
    parser: ArgumentParser = ArgumentParser()

    parser.add_argument(dest="input_file_path", help="The KGTK file with the input data (default=%(default)s)", type=Path, nargs="?", default="-")

    parser.add_argument(      "--columns", dest="key_column_names",
                              help="The key columns to identify records for compaction. " +
                              "(default=id for node files, (node1, label, node2, id) for edge files).", nargs='+', default=[ ])

    parser.add_argument(      "--compact-id", dest="compact_id",
                              help="Indicate that the ID column in KGTK edge files should be compacted. " +
                              "Normally, if the ID column exists, it is not compacted, " +
                              "as there are use cases that need to maintain distinct lists of secondary edges for each ID value. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--presorted", dest="sorted_input",
                              help="Indicate that the input has been presorted (or at least pregrouped). (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--verify-sort", dest="verify_sort",
                              help="If the input has been presorted, verify its consistency (disable if only pregrouped). (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=True)

    parser.add_argument("-o", "--output-file", dest="output_file_path", help="The KGTK file to write (default=%(default)s).", type=Path, default="-")
    
    parser.add_argument(      "--build-id", dest="build_id",
                              help="Build id values in an id column. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    KgtkIdBuilderOptions.add_arguments(parser)
    KgtkReader.add_debug_arguments(parser)
    KgtkReaderOptions.add_arguments(parser, mode_options=True)
    KgtkValueOptions.add_arguments(parser)

    args: Namespace = parser.parse_args()

    error_file: typing.TextIO = sys.stdout if args.errors_to_stdout else sys.stderr

    # Build the option structures.                                                                                                                          
    idbuilder_options: KgtkIdBuilderOptions = KgtkIdBuilderOptions.from_args(args)    
    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_args(args)
    value_options: KgtkValueOptions = KgtkValueOptions.from_args(args)

   # Show the final option structures for debugging and documentation.                                                                                             
    if args.show_options:
        print("input: %s" % str(args.input_file_path), file=error_file, flush=True)
        print("--columns %s" % " ".join(args.key_column_names), file=error_file, flush=True)
        print("--compact-id=%s" % str(args.compact_id), file=error_file, flush=True)
        print("--presorted=%s" % str(args.sorted_input), file=error_file, flush=True)
        print("--verify-sort=%s" % str(args.verify_sort), file=error_file, flush=True)
        print("--output-file=%s" % str(args.output_file_path), file=error_file, flush=True)
        print("--build-id=%s" % str(args.build_id), file=error_file, flush=True)
        idbuilder_options.show(out=error_file)
        reader_options.show(out=error_file)
        value_options.show(out=error_file)

    kc: KgtkCompact = KgtkCompact(
        input_file_path=args.input_file_path,
        key_column_names=args.key_column_names,
        compact_id=args.compact_id,
        sorted_input=args.sorted_input,
        verify_sort=args.verify_sort,
        output_file_path=args.output_file_path,
        build_id=args.build_id,
        idbuilder_options=idbuilder_options,
        reader_options=reader_options,
        value_options=value_options,
        error_file=error_file,
        verbose=args.verbose,
        very_verbose=args.very_verbose)

    kc.process()

if __name__ == "__main__":
    main()
