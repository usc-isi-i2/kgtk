"""
Join two KTKG edge files or two KGTK node files.  The output file is an edge file or a node file.

Note: This implementation builds im-memory sets of all the key values in
each input file.

"""

from argparse import ArgumentParser
import attr
from pathlib import Path
import sys
import typing

from kgtk.kgtkformat import KgtkFormat
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
from kgtk.io.kgtkwriter import KgtkWriter
from kgtk.join.kgtkmergecolumns import KgtkMergeColumns
from kgtk.utils.argparsehelpers import optional_bool
from kgtk.value.kgtkvalueoptions import KgtkValueOptions

@attr.s(slots=True, frozen=True)
class KgtkJoiner(KgtkFormat):
    FIELD_SEPARATOR_DEFAULT: str = KgtkFormat.LIST_SEPARATOR

    LEFT: str = "left"
    RIGHT: str = "right"

    left_file_path: Path = attr.ib(validator=attr.validators.instance_of(Path))
    right_file_path: Path = attr.ib(validator=attr.validators.instance_of(Path))
    output_path: typing.Optional[Path] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Path)))

    # left_join == False and right_join == False: inner join
    # left_join == True and right_join == False: left join
    # left_join == False and right_join == True: right join
    # left_join = True and right_join == True: outer join
    left_join: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    right_join: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    # The fllowing may be specified only when both input files are edge files:
    join_on_label: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    join_on_node2: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    # TODO: Write fuill validators
    left_join_columns: typing.Optional[typing.List[str]] = attr.ib(default=None)
    right_join_columns: typing.Optional[typing.List[str]] = attr.ib(default=None)

    # The prefix applied to right file column names in the output file:
    prefix: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)

    # The field separator used in multifield joins.  The KGTK list character should be safe.
    # TODO: USE THE COLUMN SEPARATOR !!!!!
    field_separator: str = attr.ib(validator=attr.validators.instance_of(str), default=FIELD_SEPARATOR_DEFAULT)

    # TODO: find working validators:
    left_reader_options: typing.Optional[KgtkReaderOptions] = attr.ib(default=None)
    right_reader_options: typing.Optional[KgtkReaderOptions] = attr.ib(default=None)
    # value_options: typing.Optional[KgtkValueOptions] = attr.ib(attr.validators.optional(attr.validators.instance_of(KgtkValueOptions)), default=None)
    value_options: typing.Optional[KgtkValueOptions] = attr.ib(default=None)

    error_file: typing.TextIO = attr.ib(default=sys.stderr)
    verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    very_verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    def node1_column_idx(self, kr: KgtkReader, who: str)->int:
        idx: int = kr.node1_column_idx
        if idx < 0:
            # TODO: throw a better exception
            raise ValueError("KgtkJoiner: unknown node1 column index in KGTK %s edge file." % who)
        return idx

    def id_column_idx(self, kr: KgtkReader, who: str)->int:
        idx: int = kr.id_column_idx
        if idx < 0:
            # TODO: throw a better exception
            raise ValueError("KgtkJoiner: unknown id column index in KGTK %s node file." % who)
        return idx

    def build_join_key(self, kr: KgtkReader, join_idx_list: typing.List[int], row: typing.List[str])->str:
        key: str = ""
        join_idx: int
        first: bool = True
        for join_idx in join_idx_list:
            if first:
                first = False
            else:
                key += self.field_separator
                
            key += row[join_idx]
        return key

    def multi_column_key_set(self, kr: KgtkReader, join_idx_list: typing.List[int])->typing.Set[str]:
        result: typing.Set[str] = set()
        row: typing.List[str]
        for row in kr:
            result.add(self.build_join_key(kr, join_idx_list, row))
        return result
        
    # Optimized for a single join column:
    def single_column_key_set(self, kr: KgtkReader, join_idx: int)->typing.Set[str]:
        result: typing.Set[str] = set()
        row: typing.List[str]
        for row in kr:
            result.add(row[join_idx])
        return result
        
    def build_join_idx_list(self, kr: KgtkReader, who: str, join_columns: typing.Optional[typing.List[str]])->typing.List[int]:
        join_idx: int
        join_idx_list: typing.List[int] = [ ]
        col_num: int = 1
        if join_columns is not None and len(join_columns) > 0:
            if self.verbose:
                print("Using %s file join columns: %s" % (who, " ".join(join_columns)), file=self.error_file, flush=True)
            join_column:str
            for join_column in join_columns:
                if join_column not in kr.column_name_map:
                    raise ValueError("Join column %s not found in in the %s input file" % (join_column, who))
                join_idx = kr.column_name_map[join_column]
                if self.verbose:
                    print("Join column %d: %s (index %d in the %s input file)" % (col_num, join_column, join_idx, who), file=self.error_file, flush=True)
                join_idx_list.append(join_idx)
            return join_idx_list

        if kr.is_edge_file:
            join_idx = self.node1_column_idx(kr, who)
            if self.verbose:
                print("Joining on node1 (index %s in the %s input file)" % (join_idx, who), file=self.error_file, flush=True)
            join_idx_list.append(join_idx)
        elif kr.is_node_file:
            join_idx = self.id_column_idx(kr, who)
            if self.verbose:
                print("Joining on id (index %s in the %s input file)" % (join_idx, who), file=self.error_file, flush=True)
            join_idx_list.append(join_idx)
        else:
            raise ValueError("Quasi-KGTK files require an explicit list of join columns")

        # join_on_label and join_on_node2 may be specified
        if self.join_on_label or self.join_on_node2:
            if self.join_on_label:
                if kr.label_column_idx < 0:
                    raise ValueError("join_on_label may not be used because the %s input file does not have a label column." % who)
                if self.verbose:
                    print("Joining on label (index %s in the %s input file)" % (kr.label_column_idx, who), file=self.error_file, flush=True)
                join_idx_list.append(kr.label_column_idx)
                
            if self.join_on_node2:
                if kr.node2_column_idx < 0:
                    raise ValueError("join_on_node2 may not be used because the %s input file does not have a node2 column." % who)
                if self.verbose:
                    print("Joining on node2 (index %s in the %s input file)" % (kr.node2_column_idx, who), file=self.error_file, flush=True)
                join_idx_list.append(kr.node2_column_idx)
        return join_idx_list
        

    def extract_join_key_set(self, file_path: Path, who: str, join_idx_list: typing.List[int])->typing.Set[str]:
        if self.verbose:
            print("Extracting the join key set from the %s input file: %s" % (who, str(file_path)), file=self.error_file, flush=True)
        reader_options: typing.Optional[KgtkReaderOptions]
        if who == self.LEFT:
            reader_options = self.left_reader_options
        else:
            reader_options = self.right_reader_options
            
        kr: KgtkReader = KgtkReader.open(file_path,
                                         who=who + " input",
                                         options=reader_options,
                                         value_options = self.value_options,
                                         error_file=self.error_file,
                                         verbose=self.verbose,
                                         very_verbose=self.very_verbose)

        if len(join_idx_list) == 1:
            # This uses optimized code:
            return self.single_column_key_set(kr, join_idx_list[0]) # closes er file
        else:
            return self.multi_column_key_set(kr, join_idx_list) # closes er file
        

    def join_key_sets(self, left_join_idx_list: typing.List[int], right_join_idx_list: typing.List[int])->typing.Optional[typing.Set[str]]:
        """
        Read the input edge files the first time, building the sets of left and right join values.
        """
        join_key_set: typing.Set[str]
        if self.left_join and self.right_join:
            if self.verbose:
                print("Outer join, no need to compute join keys.", file=self.error_file, flush=True)
            return None
        elif self.left_join and not self.right_join:
            if self.verbose:
                print("Computing the left join key set", file=self.error_file, flush=True)
            join_key_set = self.extract_join_key_set(self.left_file_path, self.LEFT, left_join_idx_list).copy()
            if self.verbose:
                print("There are %d keys in the left join key set." % len(join_key_set), file=self.error_file, flush=True)
            return join_key_set

        elif self.right_join and not self.left_join:
            if self.verbose:
                print("Computing the right join key set", file=self.error_file, flush=True)
            join_key_set = self.extract_join_key_set(self.right_file_path, self.RIGHT, right_join_idx_list).copy()
            if self.verbose:
                print("There are %d keys in the right join key set." % len(join_key_set), file=self.error_file, flush=True)
            return join_key_set

        else:
            if self.verbose:
                print("Computing the inner join key set", file=self.error_file, flush=True)
            left_join_key_set: typing.Set[str] = self.extract_join_key_set(self.left_file_path, self.LEFT, left_join_idx_list)
            if self.verbose:
                print("There are %d keys in the left file key set." % len(left_join_key_set), file=self.error_file, flush=True)
            right_join_key_set: typing.Set[str] = self.extract_join_key_set(self.right_file_path, self.RIGHT, right_join_idx_list)
            if self.verbose:
                print("There are %d keys in the right file key set." % len(right_join_key_set), file=self.error_file, flush=True)
            join_key_set = left_join_key_set.intersection(right_join_key_set)
            if self.verbose:
                print("There are %d keys in the inner join key set." % len(join_key_set), file=self.error_file, flush=True)
            return join_key_set
    
    def ok_to_join(self, left_kr: KgtkReader, right_kr: KgtkReader)->bool:
        if left_kr.is_edge_file and right_kr.is_edge_file:
            if self.verbose:
                print("Both input files are edge files.", file=self.error_file, flush=True)
            return True

        elif left_kr.is_node_file and right_kr.is_node_file:
            if self.verbose:
                print("Both input files are node files.", file=self.error_file, flush=True)
            return True

        elif (not (left_kr.is_node_file or left_kr.is_edge_file)) or (not(right_kr.is_edge_file or right_kr.is_node_file)):
            if self.verbose:
               print("One or both input files are quasi-KGTK files.", file=self.error_file, flush=True)
            return True

        else:
            print("Cannot join edge and node files.", file=self.error_file, flush=True)
            return False

    def process(self):
        if self.verbose:
            print("Opening the left edge file: %s" % str(self.left_file_path), file=self.error_file, flush=True)
        left_kr: KgtkReader = KgtkReader.open(self.left_file_path,
                                              who="left input",
                                              options=self.left_reader_options,
                                              value_options = self.value_options,
                                              error_file=self.error_file,
                                              verbose=self.verbose,
                                              very_verbose=self.very_verbose
        )


        if self.verbose:
            print("Opening the right edge file: %s" % str(self.right_file_path), file=self.error_file, flush=True)
        right_kr: KgtkReader = KgtkReader.open(self.right_file_path,
                                               who="right input",
                                               options=self.right_reader_options,
                                               value_options = self.value_options,
                                               error_file=self.error_file,
                                               verbose=self.verbose,
                                               very_verbose=self.very_verbose
        )

        if not self.ok_to_join(left_kr, right_kr):
            left_kr.close()
            right_kr.close()
            return 1

        left_join_idx_list: typing.List[int] = self.build_join_idx_list(left_kr, self.LEFT, self.left_join_columns)
        right_join_idx_list: typing.List[int] = self.build_join_idx_list(right_kr, self.RIGHT, self.right_join_columns)
        if len(left_join_idx_list) != len(right_join_idx_list):
            print("the left join key has %d components, the right join key has %d columns. Exiting." % (len(left_join_idx_list), len(right_join_idx_list)), file=self.error_file, flush=True)
            left_kr.close()
            right_kr.close()
            return 1

        # This might open the input files for a second time. This won't work with stdin.
        joined_key_set: typing.Optional[typing.Set[str]] = self.join_key_sets(left_join_idx_list, right_join_idx_list)

        if self.verbose:
            print("Mapping the column names for the join.", file=self.error_file, flush=True)
        kmc: KgtkMergeColumns = KgtkMergeColumns()
        kmc.merge(left_kr.column_names)
        right_column_names: typing.List[str] = kmc.merge(right_kr.column_names, prefix=self.prefix)
        joined_column_names: typing.List[str] = kmc.column_names

        if self.verbose:
            print("       left   columns: %s" % " ".join(left_kr.column_names), file=self.error_file, flush=True)
            print("       right  columns: %s" % " ".join(right_kr.column_names), file=self.error_file, flush=True)
            print("mapped right  columns: %s" % " ".join(right_column_names), file=self.error_file, flush=True)
            print("       joined columns: %s" % " ".join(joined_column_names), file=self.error_file, flush=True)
        
        if self.verbose:
            print("Opening the output edge file: %s" % str(self.output_path), file=self.error_file, flush=True)
        ew: KgtkWriter = KgtkWriter.open(joined_column_names,
                                         self.output_path,
                                         mode=left_kr.mode,
                                         require_all_columns=False,
                                         prohibit_extra_columns=True,
                                         fill_missing_columns=True,
                                         gzip_in_parallel=False,
                                         verbose=self.verbose,
                                         very_verbose=self.very_verbose)

        output_data_lines: int = 0
        left_data_lines_read: int = 0
        left_data_lines_kept: int = 0
        right_data_lines_read: int = 0
        right_data_lines_kept: int = 0
        
        if self.verbose:
            print("Processing the left input file: %s" % str(self.left_file_path), file=self.error_file, flush=True)
        row: typing.List[str]
        for row in left_kr:
            left_data_lines_read += 1
            if joined_key_set is None:
                ew.write(row)
                output_data_lines += 1
                left_data_lines_kept += 1
            else:
                left_key: str = self.build_join_key(left_kr, left_join_idx_list, row)
                if left_key in joined_key_set:
                    ew.write(row)
                    output_data_lines += 1
                    left_data_lines_kept += 1
        # Flush the output file so far:
        ew.flush()

        if self.verbose:
            print("Processing the right input file: %s" % str(self.right_file_path), file=self.error_file, flush=True)
        right_shuffle_list: typing.List[int] = ew.build_shuffle_list(right_column_names)
        for row in right_kr:
            right_data_lines_read += 1
            if joined_key_set is None:
                ew.write(row, shuffle_list=right_shuffle_list)
                output_data_lines += 1
                right_data_lines_kept += 1
            else:
                right_key: str = self.build_join_key(right_kr, right_join_idx_list, row)
                if right_key in joined_key_set:
                    ew.write(row, shuffle_list=right_shuffle_list)
                    output_data_lines += 1
                    right_data_lines_kept += 1
            
        ew.close()
        if self.verbose:
            print("The join is complete", file=self.error_file, flush=True)
            print("%d left input data lines read, %d kept" % (left_data_lines_read, left_data_lines_kept), file=self.error_file, flush=True)
            print("%d right input data lines read, %d kept" % (right_data_lines_read, right_data_lines_kept), file=self.error_file, flush=True)
            print("%d data lines written." % output_data_lines, file=self.error_file, flush=True)
        
def main():
    """
    Test the KGTK file joiner.

    Edge files can be joined to edge files.
    Node files can also be joined to node files.

    TODO: Add more KgtkReader parameters, especially mode.
    """
    parser = ArgumentParser()
    parser.add_argument(dest="left_file_path", help="The left KGTK file to join", type=Path)
    parser.add_argument(dest="right_file_path", help="The right KGTK file to join", type=Path)
    parser.add_argument(      "--field-separator", dest="field_separator", help="Separator for multifield keys", default=KgtkJoiner.FIELD_SEPARATOR_DEFAULT)

    parser.add_argument(      "--join-on-label", dest="join_on_label",
                              help="If both input files are edge files, include the label column in the join (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)
    
    parser.add_argument(      "--join-on-node2", dest="join_on_node2",
                              help="If both input files are edge files, include the node2 column in the join (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)
    
    parser.add_argument(      "--left-file-join-columns", dest="left_join_columns", help="Left file join columns.", nargs='+')

    parser.add_argument(      "--left-join", dest="left_join", help="Perform a left outer join (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument("-o", "--output-file", dest="output_file_path", help="The KGTK file to write", type=Path, default=None)
    parser.add_argument(      "--prefix", dest="prefix", help="An optional prefix applied to right file column names in the output file (default=None).")
    parser.add_argument(      "--right-file-join-columns", dest="right_join_columns", help="Right file join columns.", nargs='+')

    parser.add_argument(      "--right-join", dest="right_join", help="Perform a right outer join (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    KgtkReader.add_debug_arguments(parser, expert=True)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, who=KgtkJoiner.LEFT, expert=True)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, who=KgtkJoiner.RIGHT, expert=True)
    KgtkValueOptions.add_arguments(parser, expert=True)

    args = parser.parse_args()

    error_file: typing.TextIO = sys.stdout if args.errors_to_stdout else sys.stderr

    # Build the option structures.
    left_reader_options: KgtkReaderOptions = KgtkReaderOptions.from_args(args, who=KgtkJoiner.LEFT)
    right_reader_options: KgtkReaderOptions = KgtkReaderOptions.from_args(args, who=KgtkJoiner.RIGHT)
    value_options: KgtkValueOptions = KgtkValueOptions.from_args(args)

   # Show the final option structures for debugging and documentation.                                                                                             
    if args.show_options:
        left_reader_options.show(out=error_file, who=KgtkJoiner.LEFT)
        right_reader_options.show(out=error_file, who=KgtkJoiner.RIGHT)
        value_options.show(out=error_file)

    ej: KgtkJoiner = KgtkJoiner(left_file_path=args.left_file_path,
                                right_file_path=args.right_file_path,
                                output_path=args.output_file_path,
                                left_join=args.left_join,
                                right_join=args.right_join,
                                join_on_label=args.join_on_label,
                                join_on_node2=args.join_on_node2,
                                left_join_columns=args.left_join_columns,
                                right_join_columns=args.right_join_columns,
                                prefix=args.prefix,
                                field_separator=args.field_separator,
                                left_reader_options=left_reader_options,
                                right_reader_options=right_reader_options,
                                value_options=value_options,
                                error_file=error_file,
                                verbose=args.verbose,
                                very_verbose=args.very_verbose)

    ej.process()

if __name__ == "__main__":
    main()

