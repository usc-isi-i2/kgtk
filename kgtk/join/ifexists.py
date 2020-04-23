"""
Copy records from the first ("left") KGTK file to the output file, if
a match is made with records in the second ("right") KGTK input file.

The fields to match may be supplied by the user.  If not supplied,
the following defaults will be used:

Left    Right   Key fields
edge    edge    left.node1 = right.node1 and left.label=right.label and left.node2=right.node2
node    node    left.id = right.id
edge    node    left.node1 = right.id
node    edge    right.id = left.node1

Note: This implementation builds im-memory sets of all the key values in
the second file.

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
class IfExists(KgtkFormat):
    left_file_path: Path = attr.ib(validator=attr.validators.instance_of(Path))
    right_file_path: Path = attr.ib(validator=attr.validators.instance_of(Path))
    output_path: typing.Optional[Path] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Path)))

    left_keys: typing.Optional[typing.List[str]] = attr.ib(validator=attr.validators.optional(attr.validators.deep_iterable(member_validator=attr.validators.instance_of(str),
                                                                                                                            iterable_validator=attr.validators.instance_of(list))),
                                                           default=None)
    right_keys: typing.Optional[typing.List[str]] = attr.ib(validator=attr.validators.optional(attr.validators.deep_iterable(member_validator=attr.validators.instance_of(str),
                                                                                                                             iterable_validator=attr.validators.instance_of(list))),
                                                            default=None)

    # The field separator used in multifield joins.  The KGHT list character should be safe.
    field_separator: str = attr.ib(validator=attr.validators.instance_of(str), default=KgtkFormat.LIST_SEPARATOR)

    # Require or fill trailing fields?
    ignore_short_lines: bool = attr.ib(validator=attr.validators.instance_of(bool), default=True)
    ignore_long_lines: bool = attr.ib(validator=attr.validators.instance_of(bool), default=True)
    fill_short_lines: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    truncate_long_lines: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    gzip_in_parallel: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

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
            raise ValueError("The %s file is neither edge nore node." % who)

    def get_edge_key_columns(self, kr: KgtkReader, who: str)-> typing.List[int]:
        if not kr.is_edge_file:
            raise ValueError("get_edge_keys called on %s at wrong time." % who)
        if kr.node1_column_idx < 0:
            raise ValueError("The node1 column is missing from the %s node file." % who)
        if kr.label_column_idx < 0:
            raise ValueError("The label column is missing from the %s node file." % who)
        if kr.node2_column_idx < 0:
            raise ValueError("The node2 column is missing from the %s node file." % who)
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

        if kr.is_node_file or other_kr.is_node_file:
            return self.get_primary_key_column(kr, who)

        return self.get_edge_key_columns(kr, who)

    def build_key(self, line: typing.List[str], key_columns: typing.List[int])->str:
        key: str = ""
        idx: int
        for idx in key_columns:
            key += self.field_separator+ line[idx]
        return key

    def extract_key_set(self, kr: KgtkReader, who: str, key_columns: typing.List[int])->typing.Set[str]:
        result: typing.Set[str] = set()
        for line in kr:
            result.add(self.build_key(line, key_columns))
        return result

    def process(self):
        # Open the input files once.
        left_kr: KgtkReader =  KgtkReader.open(self.left_file_path,
                                               ignore_short_lines=self.ignore_short_lines,
                                               ignore_long_lines=self.ignore_long_lines,
                                               fill_short_lines=self.fill_short_lines,
                                               truncate_long_lines=self.truncate_long_lines)

        right_kr: KgtkReader = KgtkReader.open(self.right_file_path,
                                               ignore_short_lines=self.ignore_short_lines,
                                               ignore_long_lines=self.ignore_long_lines,
                                               fill_short_lines=self.fill_short_lines,
                                               truncate_long_lines=self.truncate_long_lines)

        left_key_columns: typing.List[int] = self.get_key_columns(self.left_keys, left_kr, right_kr, "left")
        right_key_columns: typing.List[int] = self.get_key_columns(self.right_keys, right_kr, left_kr, "right")

        key_set: typint.Set[str] = self.extract_key_set(right_kr, "right", right_key_columns)

        ew: KgtkWriter = KgtkWriter.open(left_kr.column_names,
                                         self.output_path,
                                         require_all_columns=False,
                                         prohibit_extra_columns=True,
                                         fill_missing_columns=True,
                                         gzip_in_parallel=self.gzip_in_parallel,
                                         verbose=self.verbose,
                                         very_verbose=self.very_verbose)

        line: typing.list[str]
        for line in left_kr:
            left_key: str = self.build_key(line, left_key_columns)
            if left_key in key_set:
                ew.write(line)
        ew.close()
        
def main():
    """
    Test the KGTK file joiner.
    """
    parser = ArgumentParser()
    parser.add_argument(dest="left_file_path", help="The left KGTK file to join", type=Path)
    parser.add_argument(dest="right_file_path", help="The right KGTK file to join", type=Path)
    parser.add_argument(      "--allow-long-lines", dest="ignore_long_lines",
                              help="When specified, do not ignore lines with extra columns.", action='store_false')
    parser.add_argument(      "--allow-short-lines", dest="ignore_short_lines",
                              help="When specified, do not ignore lines with missing columns.", action='store_false')
    parser.add_argument(      "--field-separator", dest="field_separator", help="Separator for multifield keys", default=IfExists.FIELD_SEPARATOR_DEFAULT)
    parser.add_argument(      "--fill-short-lines", dest="fill_short_lines",
                              help="Fill missing trailing columns in short lines with empty values.", action='store_true')
    parser.add_argument(      "--gzip-in-parallel", dest="gzip_in_parallel", help="Execute gzip in parallel.", action='store_true')
    parser.add_argument(      "--left-keys", dest="left_keys", help="The key columns in the left file.", nargs='*')
    parser.add_argument("-o", "--output-file", dest="output_file_path", help="The KGTK file to read", type=Path, default=None)
    parser.add_argument(      "--right-keys", dest="right_keys", help="The key columns in the right file.", nargs='*')
    parser.add_argument(      "--truncate-long-lines", dest="truncate_long_lines",
                              help="Remove excess trailing columns in long lines.", action='store_true')
    parser.add_argument("-v", "--verbose", dest="verbose", help="Print additional progress messages.", action='store_true')
    parser.add_argument(      "--very-verbose", dest="very_verbose", help="Print additional progress messages.", action='store_true')
    args = parser.parse_args()

    ie: IfExists = IfExists(left_file_path=args.left_file_path,
                            right_file_path=args.right_file_path,
                            output_path=args.output_file_path,
                            left_keys=args.left_keys,
                            right_keys=args.right_keys,
                            field_separator=args.field_separator,
                            ignore_short_lines=args.ignore_short_lines,
                            ignore_long_lines=args.ignore_long_lines,
                            fill_short_lines=args.fill_short_lines,
                            truncate_long_lines=args.truncate_long_lines,
                            gzip_in_parallel=args.gzip_in_parallel,
                            verbose=args.verbose,
                            very_verbose=args.very_verbose)

    ie.process()

if __name__ == "__main__":
    main()

