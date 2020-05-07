"""
Join two KTKG edge files.  The output file is an edge file.

Note: This implementation builds im-memory sets of all the key values in
each input file.

"""

from argparse import ArgumentParser
import attr
import gzip
from pathlib import Path
from multiprocessing import Queue
import sys
import typing

from kgtk.join.enumnameaction import EnumNameAction
from kgtk.join.edgereader import EdgeReader
from kgtk.join.kgtkformat import KgtkFormat
from kgtk.join.kgtkwriter import KgtkWriter
from kgtk.join.kgtkvalueoptions import KgtkValueOptions, DEFAULT_KGTK_VALUE_OPTIONS
from kgtk.join.validationaction import ValidationAction

@attr.s(slots=True, frozen=True)
class EdgeJoiner(KgtkFormat):
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

    # The prefix applied to right file column names in the output file:
    prefix: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)

    # The field separator used in multifield joins.  The KGHT list character should be safe.
    field_separator: str = attr.ib(validator=attr.validators.instance_of(str), default=KgtkFormat.LIST_SEPARATOR)

    # Ignore records with too many or too few fields?
    short_line_action: ValidationAction = attr.ib(validator=attr.validators.instance_of(ValidationAction), default=ValidationAction.EXCLUDE)
    long_line_action: ValidationAction = attr.ib(validator=attr.validators.instance_of(ValidationAction), default=ValidationAction.EXCLUDE)

    # Require or fill trailing fields?
    fill_short_lines: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    truncate_long_lines: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    # TODO: find a working validator
    # value_options: typing.Optional[KgtkValueOptions] = attr.ib(attr.validators.optional(attr.validators.instance_of(KgtkValueOptions)), default=None)
    value_options: typing.Optional[KgtkValueOptions] = attr.ib(default=None)

    gzip_in_parallel: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    error_limit: int = attr.ib(validator=attr.validators.instance_of(int), default=EdgeReader.ERROR_LIMIT_DEFAULT)

    verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    very_verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    FIELD_SEPARATOR_DEFAULT: str = KgtkFormat.LIST_SEPARATOR

    def node1_column_idx(self, kr: EdgeReader, who: str)->int:
        idx: int = kr.node1_column_idx
        if idx < 0:
            # TODO: throw a better exception
            raise ValueError("EdgeJoiner: unknown node1 column index in KGTK %s edge type." % who)
        return idx

    def build_join_key(self, kr: EdgeReader, join_idx: int, row: typing.List[str])->str:
        key: str = row[join_idx]
        if self.join_on_label:
            key += self.field_separator+ row[kr.label_column_idx]
        if self.join_on_node2:
            key += self.field_separator+ row[kr.node2_column_idx]
        return key

    def multi_column_key_set(self, kr: EdgeReader, join_idx: int)->typing.Set[str]:
        result: typing.Set[str] = set()
        row: typing.List[str]
        for row in kr:
            result.add(self.build_join_key(kr, join_idx, row))
        return result
        
    # Optimized for a single join column:
    def single_column_key_set(self, kr: EdgeReader, join_idx: int)->typing.Set[str]:
        result: typing.Set[str] = set()
        row: typing.List[str]
        for row in kr:
            result.add(row[join_idx])
        return result
        
    def extract_join_key_set(self, file_path: Path, who: str)->typing.Set[str]:
        if self.verbose:
            print("Extracting the join key set from the %s input file: %s" % (who, str(file_path)), flush=True)
        kr: EdgeReader = EdgeReader.open_edge_file(file_path,
                                                   short_line_action=self.short_line_action,
                                                   long_line_action=self.long_line_action,
                                                   fill_short_lines=self.fill_short_lines,
                                                   truncate_long_lines=self.truncate_long_lines,
                                                   value_options = self.value_options,
                                                   gzip_in_parallel=self.gzip_in_parallel,
                                                   error_limit=self.error_limit,
                                                   verbose=self.verbose,
                                                   very_verbose=self.very_verbose)

        if not kr.is_edge_file:
            raise ValueError("The %s file is not an edge file" % who)
        
        join_idx: int = self.node1_column_idx(kr, who)
        if self.verbose:
            print("Joining on node1 (index %s in the %s input file)" % (join_idx, who))

        # join_on_label and join_on_node2 may be specified
        if self.join_on_label or self.join_on_node2:
            if self.join_on_label:
                if kr.label_column_idx < 0:
                    raise ValueError("join_on_label may not be used because the %s input file does not have a label column." % who)
                if self.verbose:
                    print("Joining on label (index %s in the %s input file)" % (kr.label_column_idx, who))
            if self.join_on_node2:
                if kr.node2_column_idx < 0:
                    raise ValueError("join_on_node2 may not be used because the %s input file does not have a node2 column." % who)
                if self.verbose:
                    print("Joining on node2 (index %s in the %s input file)" % (kr.node2_column_idx, who))
            return self.multi_column_key_set(kr, join_idx) # closes er file
        else:
            # This uses optimized code:
            return self.single_column_key_set(kr, join_idx) # closes er file
        

    def join_key_sets(self)->typing.Optional[typing.Set[str]]:
        """
        Read the input edge files the first time, building the sets of left and right join values.
        """
        join_key_set: typing.Set[str]
        if self.left_join and self.right_join:
            if self.verbose:
                print("Outer join, no need to compute join keys.", flush=True)
            return None
        elif self.left_join and not self.right_join:
            if self.verbose:
                print("Computing the left join key set", flush=True)
            join_key_set = self.extract_join_key_set(self.left_file_path, "left").copy()
            if self.verbose:
                print("There are %d keys in the left join key set." % len(join_key_set))
            return join_key_set

        elif self.right_join and not self.left_join:
            if self.verbose:
                print("Computing the right join key set", flush=True)
            join_key_set = self.extract_join_key_set(self.right_file_path, "right").copy()
            if self.verbose:
                print("There are %d keys in the right join key set." % len(join_key_set))
            return join_key_set

        else:
            if self.verbose:
                print("Computing the inner join key set", flush=True)
            left_join_key_set: typing.Set[str] = self.extract_join_key_set(self.left_file_path, "left")
            if self.verbose:
                print("There are %d keys in the left file key set." % len(left_join_key_set))
            right_join_key_set: typing.Set[str] = self.extract_join_key_set(self.right_file_path, "right")
            if self.verbose:
                print("There are %d keys in the right file key set." % len(right_join_key_set))
            join_key_set = left_join_key_set.intersection(right_join_key_set)
            if self.verbose:
                print("There are %d keys in the inner join key set." % len(join_key_set))
            return joiin_key_set
    
    def merge_columns(self, left_kr: EdgeReader, right_kr: EdgeReader)->typing.Tuple[typing.List[str], typing.List[str]]:
        joined_column_names: typing.List[str] = [ ]
        right_column_names: typing.List[str] = [ ]

        # First step: copy the left column names.
        column_name: str
        for column_name in left_kr.column_names:
            joined_column_names.append(column_name)

        idx: int = 0
        for column_name in right_kr.column_names:
            if idx == right_kr.node1_column_idx:
                # The right file is an edge file and this is its node1 column index.
                if left_kr.node1_column_idx >= 0:
                    # The left file has a node1 column.  Map to that.
                    column_name = left_kr.column_names[left_kr.node1_column_idx]
                else:
                    # Apparently we don't have a destination in the left file.  Punt.
                    raise ValueError("Can't map right join column name to the left file #2.")
            elif idx == right_kr.label_column_idx and left_kr.label_column_idx >= 0:
                # Map the right file's label column to the left file's label column.
                column_name = left_kr.column_names[left_kr.label_column_idx]
            elif idx == right_kr.node2_column_idx and left_kr.node2_column_idx >= 0:
                # Map the right file's node2 column to the left file's node2 column.
                column_name = left_kr.column_names[left_kr.node2_column_idx]
            else:
                # Apply the prefix.
                if self.prefix is not None and len(self.prefix) > 0:
                    column_name = self.prefix + column_name

            right_column_names.append(column_name)
            if column_name not in joined_column_names:
                joined_column_names.append(column_name)
            idx += 1        

        return (joined_column_names, right_column_names)

    def process(self):
        joined_key_set: typing.Optional[typing.Set[str]] = self.join_key_sets()

        if self.verbose:
            print("Opening the left edge file: %s" % str(self.left_file_path), flush=True)
        # Open the input files for the second time. This won't work with stdin.
        left_kr: EdgeReader =  EdgeReader.open_edge_file(self.left_file_path,
                                                         short_line_action=self.short_line_action,
                                                         long_line_action=self.long_line_action,
                                                         fill_short_lines=self.fill_short_lines,
                                                         truncate_long_lines=self.truncate_long_lines,
                                                         value_options = self.value_options,
                                                         error_limit=self.error_limit)


        if self.verbose:
            print("Opening the right edge file: %s" % str(self.right_file_path), flush=True)
        right_kr: EdgeReader = EdgeReader.open_edge_file(self.right_file_path,
                                                         short_line_action=self.short_line_action,
                                                         long_line_action=self.long_line_action,
                                                         fill_short_lines=self.fill_short_lines,
                                                         truncate_long_lines=self.truncate_long_lines,
                                                         value_options = self.value_options,
                                                         error_limit=self.error_limit)


        if self.verbose:
            print("Mapping the column names for the join.", flush=True)
        joined_column_names: typing.List[str]
        right_column_names: typing.List[str]
        (joined_column_names, right_column_names)  = self.merge_columns(left_kr, right_kr)

        if self.verbose:
            print("       left   columns: %s" % " ".join(left_kr.column_names), flush=True)
            print("       right  columns: %s" % " ".join(right_kr.column_names), flush=True)
            print("mapped right  columns: %s" % " ".join(right_column_names), flush=True)
            print("       joined columns: %s" % " ".join(joined_column_names), flush=True)
        
        if self.verbose:
            print("Opening the output edge file: %s" % str(self.output_path), flush=True)
        ew: KgtkWriter = KgtkWriter.open(joined_column_names,
                                         self.output_path,
                                         require_all_columns=False,
                                         prohibit_extra_columns=True,
                                         fill_missing_columns=True,
                                         gzip_in_parallel=self.gzip_in_parallel,
                                         verbose=self.verbose,
                                         very_verbose=self.very_verbose)

        output_data_lines: int = 0
        left_data_lines_read: int = 0
        left_data_lines_kept: int = 0
        right_data_lines_read: int = 0
        right_data_lines_kept: int = 0
        
        if self.verbose:
            print("Processing the left input file: %s" % str(self.left_file_path), flush=True)
        row: typing.list[str]
        left_node1_idx: int = self.node1_column_idx(left_kr, who="left")
        for row in left_kr:
            left_data_lines_read += 1
            if joined_key_set is None:
                ew.write(row)
                output_data_lines += 1
                left_data_lines_kept += 1
            else:
                left_key: str = self.build_join_key(left_kr, left_node1_idx, row)
                if left_key in joined_key_set:
                    ew.write(row)
                    output_data_lines += 1
                    left_data_lines_kept += 1
        # Flush the output file so far:
        ew.flush()

        if self.verbose:
            print("Processing the right input file: %s" % str(self.right_file_path), flush=True)
        right_shuffle_list: typing.List[int] = ew.build_shuffle_list(right_column_names)
        right_node1_idx: int = self.node1_column_idx(right_kr, who="right")
        for row in right_kr:
            right_data_lines_read += 1
            if joined_key_set is None:
                ew.write(row, shuffle_list=right_shuffle_list)
                output_data_lines += 1
                right_data_lines_kept += 1
            else:
                right_key: str = self.build_join_key(right_kr, right_node1_idx, row)
                if right_key in joined_key_set:
                    ew.write(row, shuffle_list=right_shuffle_list)
                    output_data_lines += 1
                    right_data_lines_kept += 1
            
        ew.close()
        if self.verbose:
            print("The join is complete", flush=True)
            print("%d left input data lines read, %d kept" % (left_data_lines_read, left_data_lines_kept), flush=True)
            print("%d right input data lines read, %d kept" % (right_data_lines_read, right_data_lines_kept), flush=True)
            print("%d data lines written." % output_data_lines, flush=True)
        
def main():
    """
    Test the KGTK file joiner.
    """
    parser = ArgumentParser()
    parser.add_argument(dest="left_file_path", help="The left KGTK file to join", type=Path)
    parser.add_argument(dest="right_file_path", help="The right KGTK file to join", type=Path)
    parser.add_argument(      "--error-limit", dest="error_limit",
                              help="The maximum number of errors to report before failing", type=int, default=EdgeReader.ERROR_LIMIT_DEFAULT)

    parser.add_argument(      "--field-separator", dest="field_separator", help="Separator for multifield keys", default=EdgeJoiner.FIELD_SEPARATOR_DEFAULT)
    parser.add_argument(      "--fill-short-lines", dest="fill_short_lines",
                              help="Fill missing trailing columns in short lines with empty values.", action='store_true')
    parser.add_argument(      "--join-on-label", dest="join_on_label", help="If both input files are edge files, include the label column in the join.", action='store_true')
    parser.add_argument(      "--join-on-node2", dest="join_on_node2", help="If both input files are edge files, include the node2 column in the join.", action='store_true')
    parser.add_argument(      "--gzip-in-parallel", dest="gzip_in_parallel", help="Execute gzip in parallel.", action='store_true')
    parser.add_argument(      "--left-join", dest="left_join", help="Perform a left outer join.", action='store_true')

    parser.add_argument(      "--long-line-action", dest="long_line_action",
                              help="The action to take when a long line is detected.",
                              type=ValidationAction, action=EnumNameAction, default=ValidationAction.EXCLUDE)

    parser.add_argument("-o", "--output-file", dest="output_file_path", help="The KGTK file to read", type=Path, default=None)
    parser.add_argument(      "--prefix", dest="prefix", help="The prefix applied to right file column names in the output file.")
    parser.add_argument(      "--right-join", dest="right_join", help="Perform a right outer join.", action='store_true')

    parser.add_argument(      "--short-line-action", dest="short_line_action",
                              help="The action to take whe a short line is detected.",
                              type=ValidationAction, action=EnumNameAction, default=ValidationAction.EXCLUDE)

    parser.add_argument(      "--truncate-long-lines", dest="truncate_long_lines",
                              help="Remove excess trailing columns in long lines.", action='store_true')
    parser.add_argument("-v", "--verbose", dest="verbose", help="Print additional progress messages.", action='store_true')
    parser.add_argument(      "--very-verbose", dest="very_verbose", help="Print additional progress messages.", action='store_true')

    KgtkValueOptions.add_arguments(parser)

    args = parser.parse_args()

    # Build the value parsing option structure.
    value_options: KgtkValueOptions = KgtkValueOptions.from_args(args)

    ej: EdgeJoiner = EdgeJoiner(left_file_path=args.left_file_path,
                                right_file_path=args.right_file_path,
                                output_path=args.output_file_path,
                                left_join=args.left_join,
                                right_join=args.right_join,
                                join_on_label=args.join_on_label,
                                join_on_node2=args.join_on_node2,
                                prefix=args.prefix,
                                field_separator=args.field_separator,
                                short_line_action=args.short_line_action,
                                long_line_action=args.long_line_action,
                                fill_short_lines=args.fill_short_lines,
                                truncate_long_lines=args.truncate_long_lines,
                                value_options=value_options,
                                gzip_in_parallel=args.gzip_in_parallel,
                                error_limit=args.error_limit,
                                verbose=args.verbose,
                                very_verbose=args.very_verbose)

    ej.process()

if __name__ == "__main__":
    main()

