"""Join two KTKG edge files.

Note: This implementation builds im-memory sets of all the node1 values in
each input file.

"""

import attr
import gzip
from pathlib import Path
from multiprocessing import Queue
import sys
import typing

from kgtk.join.edgereader import EdgeReader
from kgtk.join.edgewriter import EdgeWriter
from kgtk.join.kgtkformat import KgtkFormat

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

    # TODO: This is complicated by the alias list.
    # left_join_column_names: str = attr.ib(validator=attr.validators.instance_of(str), default=KgtkFormat.NODE1_COLUMN_NAMES)
    # right_join_column_names: str = attr.ib(validator=attr.validators.instance_of(str), default=KgtkFormat.NODE1_COLUMN_NAMES)

    # Require or fill trailing fields?
    require_all_columns: bool = attr.ib(validator=attr.validators.instance_of(bool), default=True)
    prohibit_extra_columns: bool = attr.ib(validator=attr.validators.instance_of(bool), default=True)
    fill_missing_columns: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    gzip_in_parallel: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    very_verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    # TODO: pass in join_column_names and find the index of the first matching column name.
    def node1_set(self, er: EdgeReader)->typing.Set[str]:
        result: typing.Set[str] = set()
        node1_idx: int = er.node1_column_idx
        for line in er:
            result.add(line[node1_idx])
        return result
        
    # TODO: pass through join_column_names
    def extract_node1_values(self, edge_path: Path)->typing.Set[str]:
        er: EdgeReader = EdgeReader.open(edge_path,
                                         require_all_columns=self.require_all_columns,
                                         prohibit_extra_columns=self.prohibit_extra_columns,
                                         fill_missing_columns=self.fill_missing_columns,
                                         gzip_in_parallel=self.gzip_in_parallel,
                                         verbose=self.verbose,
                                         very_verbose=self.very_verbose)
        return self.node1_set(er) # closes er file
        

    def join_node1_values(self)->typing.Set[str]:
        """
        Read the input edge files the first time, building the sets of left and right nodes.
        """
        # TODO: pass in self.left_join_column_names
        left_node1_values: typing.Set[str] = self.extract_node1_values(self.left_file_path)
        # TODO: pass in self.right_join_column_names
        right_node1_values: typing.Set[str] = self.extract_node1_values(self.right_file_path)

        joined_node1_values: typing.Set[str]
        if self.left_join and self.right_join:
            # TODO: This joins everything! We can shortut computing these sets.
            joined_node1_values = left_node1_values.union(right_node1_values)
        elif self.left_join and not self.right_join:
            joined_node1_values = left_node1_values.copy()
        elif self.right_join and not self.left_join:
            joined_node1_values = right_node1_values.copy()
        else:
            joined_node1_values = left_node1_values.intersection(right_node1_values)
        return joined_node1_values
    
        
    def process(self):
        joined_node1_values: typing.Set[str] = self.join_node1_values()

        # Open the input files for the second time. This won't work with stdin.
        left_er: EdgeReader =  EdgeReader.open(self.left_file_path,
                                               require_all_columns=self.require_all_columns,
                                               prohibit_extra_columns=self.prohibit_extra_columns,
                                               fill_missing_columns=self.fill_missing_columns)
        right_er: EdgeReader = EdgeReader.open(self.right_file_path,
                                               require_all_columns=self.require_all_columns,
                                               prohibit_extra_columns=self.prohibit_extra_columns,
                                               fill_missing_columns=self.fill_missing_columns)
        joined_column_names: typing.list[str] = left_er.merge_columns(right_er.column_names)
        
        ew: EdgeWriter = EdgeWriter.open(joined_column_names,
                                         self.output_path,
                                         require_all_columns=False,
                                         prohibit_extra_columns=True,
                                         fill_missing_columns=True,
                                         gzip_in_parallel=self.gzip_in_parallel,
                                         verbose=self.verbose,
                                         very_verbose=self.very_verbose)

        line: typing.list[str]
        left_node1_idx: int = left_er.node1_column_idx
        for line in left_er:
            node1_value: str = line[left_node1_idx]
            if node1_value in joined_node1_values:
                ew.write(line)

        right_shuffle_list: typing.List[int] = ew.build_shuffle_list(right_er.column_names)
        right_node1_idx: int = right_er.node1_column_idx
        for line in right_er:
            node1_value: str = line[right_node1_idx]
            if node1_value in joined_node1_values:
                ew.write(line, shuffle_list=right_shuffle_list)
            
        ew.close()
        
def main():
    """
    Test the KGTK file reader.
    """
    parser = ArgumentParser()
    parser.add_argument(dest="left_file_path", help="The KGTK file to read", type=Path, required=True)
    parser.add_argument(dest="right_file_path", help="The KGTK file to read", type=Path, required=True)
    parser.add_argument("-o", "output-file", dest="output_path", help="The KGTK file to read", type=Path, default=None)
    parser.add_argument(      "--gzip-in-parallel", dest="gzip_in_parallel", help="Execute gzip in parallel.", action='store_true')
    parser.add_argument(      "--left-join", dest="left_join", help="Perform a left outer join.", action='store_true')
    parser.add_argument(      "--right-join", dest="right_join", help="Perform a right outer join.", action='store_true')
    parser.add_argument("-v", "--verbose", dest="verbose", help="Print additional progress messages.", action='store_true')
    parser.add_argument(      "--very-verbose", dest="very_verbose", help="Print additional progress messages.", action='store_true')
    args = parser.parse_args()

    ej: EdgeJoiner = EdgeJoiner(left_file_path=args.left_file_path,
                                right_file_path=args.right_file_patn,
                                left_join=args.left_join,
                                right_join=args.right_join,
                                gzip_in_parallel=args.gzip_in_parallel,
                                verbose=args.verbose,
                                very_verbose=args.very_verbose)

    ej.process()

if __name__ == "__main__":
    main()

