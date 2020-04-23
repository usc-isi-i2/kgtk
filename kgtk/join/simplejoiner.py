"""
Join two KTKG edge files.

Note: This implementation builds im-memory sets of all the node1 values in
each input file.

"""

from argparse import ArgumentParser
import attr
import gzip
from pathlib import Path
from multiprocessing import Queue
import sys
import typing

from kgtk.join.kgtkformat import KgtkFormat
from kgtk.join.kgtkreader import KgtkReader
from kgtk.join.kgtkwriter import KgtkWriter

@attr.s(slots=True, frozen=True)
class SimpleJoiner(KgtkFormat):
    left_file_path: Path = attr.ib(validator=attr.validators.instance_of(Path))
    right_file_path: Path = attr.ib(validator=attr.validators.instance_of(Path))
    output_path: typing.Optional[Path] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Path)))

    # left_join == False and right_join == False: inner join
    # left_join == True and right_join == False: left join
    # left_join == False and right_join == True: right join
    # left_join = True and right_join == True: outer join
    left_join: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    right_join: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    left_join_column_name: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    right_join_column_name: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)

    # The prefix applied to right file column names in the output file:
    prefix: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)

    # Require or fill trailing fields?
    ignore_short_lines: bool = attr.ib(validator=attr.validators.instance_of(bool), default=True)
    ignore_long_lines: bool = attr.ib(validator=attr.validators.instance_of(bool), default=True)
    fill_short_lines: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    truncate_long_lines: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    gzip_in_parallel: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    very_verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    def join_column_idx(self, kr: KgtkReader, join_column_name: typing.Optional[str], who: str)->int:
        if join_column_name is not None:
            if join_column_name in kr.column_name_map:
                return kr.column_name_map[join_column_name]
            else:
                # TODO: throw a better exception
                raise ValueError("SimpleJoiner: unknown %s join column %s" % (who, join_column_name))
        else:
            idx: int
            if kr.is_edge_file:
                idx = kr.node1_column_idx
                if idx < 0:
                    # TODO: throw a better exception
                    raise ValueError("SimpleJoiner: unknown node1 column index in KGTK %s edge type." % who)
                return idx
            elif kr.is_node_file:
                idx = kr.id_column_idx
                if idx < 0:
                    # TODO: throw a better exception
                    raise ValueError("SimpleJoiner: unknown node1 column index in KGTK %s node type." % who)
                return idx
            else:
                # TODO: throw a better exception
                raise ValueError("SimpleJoiner: unknown %s KGTK file type." % who)

    def join_column_set(self, kr: KgtkReader, join_column_idx: int)->typing.Set[str]:
        result: typing.Set[str] = set()
        for line in kr:
            result.add(line[join_column_idx])
        return result
        
    def extract_join_values(self, file_path: Path, join_column_name: typing.Optional[str], who: str)->typing.Set[str]:
        kr: KgtkReader = KgtkReader.open(file_path,
                                         ignore_short_lines=self.ignore_short_lines,
                                         ignore_long_lines=self.ignore_long_lines,
                                         fill_short_lines=self.fill_short_lines,
                                         truncate_long_lines=self.truncate_long_lines,
                                         gzip_in_parallel=self.gzip_in_parallel,
                                         verbose=self.verbose,
                                         very_verbose=self.very_verbose)
        
        return self.join_column_set(kr, self.join_column_idx(kr, join_column_name, who)) # closes er file
        

    def join_column_values(self)->typing.Set[str]:
        """
        Read the input edge files the first time, building the sets of left and right join values.
        """
        left_join_values: typing.Set[str] = self.extract_join_values(self.left_file_path, self.left_join_column_name, "left")
        right_join_values: typing.Set[str] = self.extract_join_values(self.right_file_path, self.right_join_column_name, "right")

        joined_column_values: typing.Set[str]
        if self.left_join and self.right_join:
            # TODO: This joins everything! We can shortut computing these sets.
            joined_column_values = left_join_values.union(right_join_values)
        elif self.left_join and not self.right_join:
            joined_column_values = left_join_values.copy()
        elif self.right_join and not self.left_join:
            joined_column_values = right_join_values.copy()
        else:
            joined_column_values = left_join_values.intersection(right_join_values)
        return joined_column_values
    
    def merge_columns(self, left_kr: KgtkReader, right_kr: KgtkReader)->typing.Tuple[typing.List[str], typing.List[str]]:
        joined_column_names: typing.List[str] = [ ]
        right_column_names: typing.List[str] = [ ]

        # First step: copy the left column names.
        column_name: str
        for column_name in left_kr.column_names:
            joined_column_names.append(column_name)

        # Second step: merge the right column names.
        # Rule 1: If the left file is an edge file and the right file is a node file,
        # then rename the right file's id column to whatever name the left file is using
        # for its node1 column, if it has one,
        # Rule 2: If the left file is an node file and the right file is a node file,
        # then rename the right file's id column to whatever name the left file is using
        # for its id column, if it has one.
        # Rule 3: If the right file is an edge file, its node1, label, and node2 columns
        # are mapped to the corresponding names in the left file.
        # Rule 4: Apply the optional prefix to the remaining column names
        # Rule 5: Append the new column name to the new right column names
        # Rule 6: Append the new column name to the joind column names if it isn't already in the list.
        idx: int = 0
        for column_name in right_kr.column_names:
            if self.right_join_column_name is not None and len(self.right_join_column_name) > 0 and self.right_join_column_name == column_name:
                # A right join column name was provided.  If a left join
                # column name was also provided, map the right join column
                # name to the left join column name.
                if self.left_join_column_name is not None and len(self.left_join_column_name) > 0:
                    column_name = self.left_join_column_name
                else:
                    # A right join column name was provided, but a left join column name was not.
                    # Map th e right join column name the left file's primary column name.
                    if left_kr.is_edge_file and left_kr.node1_column_idx >= 0:
                        # The left file is an edge file.  Use its node1 column name.
                        column_name = left_kr.column_names[left_kr.node1_column_idx]
                    elif left_kr.is_node_file and left_kr.id_column_idx >= 0:
                        # The left file is a node file.  Use its id column name.
                        column_name = left_kr.column_names[left_kr.id_column_idx]
                    else:
                        # The left file is neither an edge nor a node file, and/or respective
                        # primary column is missing.  Give up.
                        raise ValueError("Can't map right join column name to the left file #1.")
            elif right_kr.is_node_file:
                if idx == right_kr.id_column_idx:
                    # The right file is a node file, and this is the id column.
                    if self.left_join_column_name is not None and len(self.left_join_column_name) > 0:
                        # Map the right file's id column to an explicit left join column.
                        column_name = self.left_join_column_name
                    elif left_kr.is_edge_file and left_kr.node1_column_idx >= 0:
                        # The left file is an edge file.  Map the right file's id column to the left file's node1 column.
                        column_name = left_kr.column_names[left_kr.node1_column_idx]
                    elif left_kr.is_node_file and left_kr.id_column_idx >= 0:
                        # The left file is a node file.  Map the right file's id column to the left file's id column.
                        column_name = left_kr.column_names[left_kr.id_column_idx]
                    else:
                        # This is the right file's id column, and
                        # we weren't given an explicit left join column name and:
                        # 1) the left file isn't an edge or node file, and/or:
                        # 2) the left file's node1 or id column is missing
                        # Apply any prefix to the column name.
                        if self.prefix is not None and len(self.prefix) > 0:
                            column_name = self.prefix + column_name
                else:
                    # This is not the right file's id column.  Apply any prefix.
                    if self.prefix is not None and len(self.prefix) > 0:
                        column_name = self.prefix + column_name
            elif right_kr.is_edge_file:
                if idx == right_kr.node1_column_idx:
                    # The right file is an edge file and this is its node1 column index. Was there
                    # an explicit left join column name?
                    if self.left_join_column_name is not None and len(self.left_join_column_name) > 0:
                        # Yes, map this column to the left file's join column name.
                        column_name = self.left_join_column_name
                    elif left_kr.node1_column_idx >= 0:
                        # No, but the left file has a node1 column.  Map to that.
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
            else:
                # We don't have an explicit right join column name, and the right file is
                # neither a node file nor an edge file.  Punt.
                raise ValueError("Can't map right join column name to the left file #3.")

            right_column_names.append(column_name)
            if column_name not in joined_column_names:
                joined_column_names.append(column_name)
            idx += 1        

        return (joined_column_names, right_column_names)

    def process(self):
        joined_column_values: typing.Set[str] = self.join_column_values()

        # Open the input files for the second time. This won't work with stdin.
        left_kr: KgtkReader =  KgtkReader.open(self.left_file_path,
                                               ignore_short_lines=self.ignore_short_lines,
                                               ignore_long_lines=self.ignore_long_lines,
                                               fill_short_lines=self.fill_short_lines,
                                               truncate_long_lines=self.truncate_long_lines)

        right_kr: EdgeReader = KgtkReader.open(self.right_file_path,
                                               ignore_short_lines=self.ignore_short_lines,
                                               ignore_long_lines=self.ignore_long_lines,
                                               fill_short_lines=self.fill_short_lines,
                                               truncate_long_lines=self.truncate_long_lines)

        # If the left file is an edge file, the right file may be an edge file or a node file.
        # If the left file is a node file, the right file may be only a node file.  For now.
        if left_kr.is_node_file and right_kr.is_edge_file:
            raise ValueError("Unsupported join: the left file is a node file and the right file is an edge file")

        # Map the right column names for the join:
        joined_column_names: typing.List[str]
        right_column_names: typing.List[str]
        (joined_column_names, right_column_names)  = self.merge_columns(left_kr, right_kr)

        if self.verbose:
            print("       left   columns: %s" % " ".join(left_kr.column_names))
            print("       right  columns: %s" % " ".join(right_kr.column_names))
            print("mapped right  columns: %s" % " ".join(right_column_names))
            print("       joined columns: %s" % " ".join(joined_column_names))
        
        ew: KgtkWriter = KgtkWriter.open(joined_column_names,
                                         self.output_path,
                                         require_all_columns=False,
                                         prohibit_extra_columns=True,
                                         fill_missing_columns=True,
                                         gzip_in_parallel=self.gzip_in_parallel,
                                         verbose=self.verbose,
                                         very_verbose=self.very_verbose)

        line: typing.list[str]
        left_node1_idx: int = self.join_column_idx(left_kr, self.left_join_column_name, who="left")
        for line in left_kr:
            node1_value: str = line[left_node1_idx]
            if node1_value in joined_column_values:
                ew.write(line)

        right_shuffle_list: typing.List[int] = ew.build_shuffle_list(right_column_names)
        right_node1_idx: int = self.join_column_idx(right_kr, self.right_join_column_name, who="right")
        for line in right_kr:
            node1_value: str = line[right_node1_idx]
            if node1_value in joined_column_values:
                ew.write(line, shuffle_list=right_shuffle_list)
            
        ew.close()
        
def main():
    """
    Test the KGTK file joiner.
    """
    parser = ArgumentParser()
    parser.add_argument(dest="left_file_path", help="The KGTK file to read", type=Path)
    parser.add_argument(dest="right_file_path", help="The KGTK file to read", type=Path)
    parser.add_argument(      "--allow-long-lines", dest="ignore_long_lines",
                              help="When specified, do not ignore lines with extra columns.", action='store_false')
    parser.add_argument(      "--allow-short-lines", dest="ignore_short_lines",
                              help="When specified, do not ignore lines with missing columns.", action='store_false')
    parser.add_argument(      "--fill-short-lines", dest="fill_short_lines",
                              help="Fill missing trailing columns in short lines with empty values.", action='store_true')
    parser.add_argument(      "--gzip-in-parallel", dest="gzip_in_parallel", help="Execute gzip in parallel.", action='store_true')
    parser.add_argument(      "--left-join", dest="left_join", help="Perform a left outer join.", action='store_true')
    parser.add_argument(      "--left-join-column-name", dest="left_join_column_name", help="The name of the left join column.")
    parser.add_argument("-o", "--output-file", dest="output_file_path", help="The KGTK file to read", type=Path, default=None)
    parser.add_argument(      "--prefix", dest="prefix", help="The prefix applied to right file column names in the output file.")
    parser.add_argument(      "--right-join", dest="right_join", help="Perform a right outer join.", action='store_true')
    parser.add_argument(      "--right-join-column-name", dest="right_join_column_name", help="The name of the right join column.")
    parser.add_argument(      "--truncate-long-lines", dest="truncate_long_lines",
                              help="Remove excess trailing columns in long lines.", action='store_true')
    parser.add_argument("-v", "--verbose", dest="verbose", help="Print additional progress messages.", action='store_true')
    parser.add_argument(      "--very-verbose", dest="very_verbose", help="Print additional progress messages.", action='store_true')
    args = parser.parse_args()

    ej: SimpleJoiner = SimpleJoiner(left_file_path=args.left_file_path,
                                    right_file_path=args.right_file_path,
                                    output_path=args.output_file_path,
                                    left_join=args.left_join,
                                    right_join=args.right_join,
                                    left_join_column_name=args.left_join_column_name,
                                    right_join_column_name=args.right_join_column_name,
                                    prefix=args.prefix,
                                    ignore_short_lines=args.ignore_short_lines,
                                    ignore_long_lines=args.ignore_long_lines,
                                    fill_short_lines=args.fill_short_lines,
                                    truncate_long_lines=args.truncate_long_lines,
                                    gzip_in_parallel=args.gzip_in_parallel,
                                    verbose=args.verbose,
                                    very_verbose=args.very_verbose)

    ej.process()

if __name__ == "__main__":
    main()

