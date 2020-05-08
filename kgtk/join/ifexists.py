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

from argparse import ArgumentParser, Namespace
import attr
import gzip
from pathlib import Path
from multiprocessing import Queue
import sys
import typing

from kgtk.join.enumnameaction import EnumNameAction
from kgtk.join.kgtkformat import KgtkFormat
from kgtk.join.kgtkreader import KgtkReader
from kgtk.join.kgtkwriter import KgtkWriter
from kgtk.join.kgtkvalueoptions import KgtkValueOptions
from kgtk.join.validationaction import ValidationAction

@attr.s(slots=True, frozen=True)
class IfExists(KgtkFormat):
    input_reader_args: typing.Mapping[str, typing.Any] = attr.ib()
    input_keys: typing.Optional[typing.List[str]] = attr.ib(validator=attr.validators.optional(attr.validators.deep_iterable(member_validator=attr.validators.instance_of(str),
                                                                                                                            iterable_validator=attr.validators.instance_of(list))))

    filter_reader_args: typing.Mapping[str, typing.Any] = attr.ib()
    filter_keys: typing.Optional[typing.List[str]] = attr.ib(validator=attr.validators.optional(attr.validators.deep_iterable(member_validator=attr.validators.instance_of(str),
                                                                                                                             iterable_validator=attr.validators.instance_of(list))))

    output_file_path: typing.Optional[Path] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Path)))

    # The field separator used in multifield joins.  The KGHT list character should be safe.
    field_separator: str = attr.ib(validator=attr.validators.instance_of(str), default=KgtkFormat.LIST_SEPARATOR)

    invert: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    # TODO: find a working validator
    # value_options: typing.Optional[KgtkValueOptions] = attr.ib(attr.validators.optional(attr.validators.instance_of(KgtkValueOptions)), default=None)
    value_options: typing.Optional[KgtkValueOptions] = attr.ib(default=None)

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
        result: typing.Set[str] = set()
        row: typing.List[str]
        for row in kr:
            result.add(self.build_key(row, key_columns))
        return result

    def process(self):
        # Open the input files once.
        if self.verbose:
            print("Opening the input file: %s" % self.left_file_path, flush=True)
            left_kr: KgtkReader =  KgtkReader.open(self.left_file_path,
                                               short_line_action=self.short_line_action,
                                               long_line_action=self.long_line_action,
                                               fill_short_lines=self.fill_short_lines,
                                               truncate_long_lines=self.truncate_long_lines,
                                               invalid_value_action=self.invalid_value_action,
                                               value_options = self.value_options,
                                               error_limit=self.error_limit,
                                               verbose=self.verbose,
                                               very_verbose=self.very_verbose,
        )

        if self.verbose:
            print("Opening the right input file: %s" % self.right_file_path, flush=True)
        right_kr: KgtkReader = KgtkReader.open(self.right_file_path,
                                               short_line_action=self.short_line_action,
                                               long_line_action=self.long_line_action,
                                               fill_short_lines=self.fill_short_lines,
                                               truncate_long_lines=self.truncate_long_lines,
                                               invalid_value_action=self.invalid_value_action,
                                               value_options = self.value_options,
                                               error_limit=self.error_limit,
                                               verbose=self.verbose,
                                               very_verbose=self.very_verbose,
        )

        left_key_columns: typing.List[int] = self.get_key_columns(self.left_keys, left_kr, right_kr, "left")
        right_key_columns: typing.List[int] = self.get_key_columns(self.right_keys, right_kr, left_kr, "right")

        if len(left_key_columns) != len(right_key_columns):
            print("There are %d left key columns but %d right key columns.  Exiting." % (len(left_key_columns), len(right_key_columns)), flush=True)
            return

        if self.verbose:
            print("Building the input key set from %s" % self.right_file_path, flush=True)
        key_set: typint.Set[str] = self.extract_key_set(right_kr, "right", right_key_columns)
        if self.verbose or self.very_verbose:
            print("There are %d entries in the key set." % len(key_set))
            if self.very_verbose:
                print("Keys: %s" % " ".join(key_set))

        if self.verbose:
            print("Opening the output file: %s" % self.output_path, flush=True)
        ew: KgtkWriter = KgtkWriter.open(left_kr.column_names,
                                         self.output_path,
                                         require_all_columns=False,
                                         prohibit_extra_columns=True,
                                         fill_missing_columns=True,
                                         gzip_in_parallel=self.gzip_in_parallel,
                                         verbose=self.verbose,
                                         very_verbose=self.very_verbose)

        if self.verbose:
            print("Filtering records from %s" % self.left_file_path, flush=True)
        input_line_count: int = 0
        output_line_count: int = 0;

        row: typing.list[str]
        for row in left_kr:
            input_line_count += 1
            left_key: str = self.build_key(row, left_key_columns)
            if self.invert:
                if left_key not in key_set:
                    ew.write(row)
                    output_line_count += 1
            else:
                if left_key in key_set:
                    ew.write(row)
                    output_line_count += 1

        if self.verbose:
            print("Read %d records, wrote %d records." % (input_line_count, output_line_count), flush=True)
        
        ew.close()

def main():
    """
    Test the KGTK file joiner.
    """
    parser: ArgumentParser = ArgumentParser()
    KgtkReader.add_operation_arguments(parser)

    parser.add_argument("-o", "--output-file", dest="output_file_path", help="The KGTK file to read", type=Path, default=None)
    
    parser.add_argument(      "--field-separator", dest="field_separator", help="Separator for multifield keys", default=IfExists.FIELD_SEPARATOR_DEFAULT)
   
    parser.add_argument(      "--invert", dest="invert", help="Invert the test (if not exists).", action='store_true')

    parser.add_argument(      "--input-keys", dest="_input_keys", help="The key columns in the input file.", nargs='*')
    parser.add_argument(      "--filter-keys", dest="_filter_keys", help="The key columns in the filter file.", nargs='*')

    KgtkReader.add_file_arguments(parser, mode_options=True, who="input")

    # TODO: Find a way to use "--filter-on"
    KgtkReader.add_file_arguments(parser, mode_options=True, who="filter", optional_file=True)

    KgtkValueOptions.add_arguments(parser)

    args: Namespace = parser.parse_args()

    input_args: typing.Mapping[str, typing.Any] = dict(((item[0][len("input_"):], item[1]) for item in vars(args) if item[0].startswith("input_")))
    filter_args: typing.Mapping[str, typing.Any] = dict(((item[0][len("filter_"):], item[1]) for item in vars(args) if item[0].startswith("filter_")))

    # Build the value parsing option structure.
    value_options: KgtkValueOptions = KgtkValueOptions.from_args(args)

    ie: IfExists = IfExists(input_reader_args=input_args,
                            input_keys=args._input_keys,
                            filter_reader_args=filter_args,
                            filter_keys=args._filter_keys,
                            output_file_path=args.output_file_path,
                            field_separator=args.field_separator,
                            invert=args.invert,
                            value_options=value_options,
                            verbose=args.verbose,
                            very_verbose=args.very_verbose)

    ie.process()

if __name__ == "__main__":
    main()
