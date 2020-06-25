"""
Unreify RDF values in KGTK files
"""
from argparse import ArgumentParser, Namespace
import attr
from pathlib import Path
import sys
import typing

from kgtk.kgtkformat import KgtkFormat
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderMode, KgtkReaderOptions
from kgtk.io.kgtkwriter import KgtkWriter
from kgtk.unreify.kgtksortbuffer import KgtkSortBuffer
from kgtk.utils.argparsehelpers import optional_bool
from kgtk.value.kgtkvalueoptions import KgtkValueOptions

@attr.s(slots=True, frozen=False)
class KgtkUnreifyValues(KgtkFormat):
    # Note: If you change any of these default values, be sure to change the
    # explanation in the corresponding parser.add_argument(...) call.
    DEFAULT_TRIGGER_LABEL_VALUE: typing.Optional[str] = None
    DEFAULT_TRIGGER_NODE2_VALUE: typing.Optional[str] = None
    DEFAULT_VALUE_LABEL_VALUE: typing.Optional[str] = None
    DEFAULT_OLD_LABEL_VALUE: typing.Optional[str] = None
    DEFAULT_NEW_LABEL_VALUE: typing.Optional[str] = None
    DEFAULT_ALLOW_MULTIPLE_VALUES: bool = False
    DEFAULT_ALLOW_EXTRA_COLUMNS: bool = False

    input_file_path: Path = attr.ib(validator=attr.validators.instance_of(Path))
    output_file_path: Path = attr.ib(validator=attr.validators.instance_of(Path))

    reified_file_path: typing.Optional[Path] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Path)))
    unreified_file_path: typing.Optional[Path] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Path)))
    uninvolved_file_path: typing.Optional[Path] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Path)))

    trigger_label_value: str = attr.ib(validator=attr.validators.instance_of(str), default=DEFAULT_TRIGGER_LABEL_VALUE)
    trigger_node2_value: str = attr.ib(validator=attr.validators.instance_of(str), default=DEFAULT_TRIGGER_NODE2_VALUE)
    value_label_value: str = attr.ib(validator=attr.validators.instance_of(str), default=DEFAULT_VALUE_LABEL_VALUE)
    old_label_value: str = attr.ib(validator=attr.validators.instance_of(str), default=DEFAULT_OLD_LABEL_VALUE)
    new_label_value: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)),
                                                    default=DEFAULT_NEW_LABEL_VALUE)

    allow_multiple_values: bool = attr.ib(validator=attr.validators.instance_of(bool), default=DEFAULT_ALLOW_MULTIPLE_VALUES)
    allow_extra_columns: bool = attr.ib(validator=attr.validators.instance_of(bool), default=DEFAULT_ALLOW_EXTRA_COLUMNS)

    # TODO: find working validators
    # value_options: typing.Optional[KgtkValueOptions] = attr.ib(attr.validators.optional(attr.validators.instance_of(KgtkValueOptions)), default=None)
    reader_options: typing.Optional[KgtkReaderOptions]= attr.ib(default=None)
    value_options: typing.Optional[KgtkValueOptions] = attr.ib(default=None)

    output_format: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None) # TODO: use an enum

    error_file: typing.TextIO = attr.ib(default=sys.stderr)
    verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    very_verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    # Working variables:
    output_line_count: int = attr.ib(default=0)

    def make_keygen(self, old_label_value: str)->KgtkSortBuffer.KEYGEN_TYPE:
        # Create a key generator function passing old_label_value as a
        # closure value.
        def keygen(buf: 'KgtkSortBuffer', row: typing.List[str])->str:
            label_column_idx: int = buf.label_column_idx
            if label_column_idx < 0:
                raise ValueError("Unknown label column.")
            
            if row[label_column_idx] == old_label_value:
                node2_column_idx: int = buf.node2_column_idx
                if node2_column_idx < 0:
                    raise ValueError("Unknown node2 column.")
                return row[node2_column_idx]

            else:
                node1_column_idx: int = buf.node1_column_idx
                if node1_column_idx < 0:
                    raise ValueError("Unknown node1 column.")
                return row[node1_column_idx]
        return keygen

    def process(self):
        # Open the input file.
        if self.verbose:
            print("Opening the input file: %s" % str(self.input_file_path), file=self.error_file, flush=True)

        kr: KgtkReader =  KgtkReader.open(self.input_file_path,
                                          mode=KgtkReaderMode.EDGE, # Must be an edge file.
                                          error_file=self.error_file,
                                          options=self.reader_options,
                                          value_options = self.value_options,
                                          verbose=self.verbose,
                                          very_verbose=self.very_verbose,
        )

        output_column_names: typing.List[str] = kr.column_names.copy()

        node1_column_idx: int = kr.node1_column_idx
        node1_column_name: str = output_column_names[node1_column_idx]

        label_column_idx: int = kr.label_column_idx
        label_column_name: str = output_column_names[label_column_idx]

        node2_column_idx: int = kr.node2_column_idx
        node2_column_name: str = output_column_names[node2_column_idx]

        # Adding an ID column?
        new_id_column: bool = False
        id_column_idx: int = kr.id_column_idx
        if id_column_idx < 0:
            new_id_column = True
            id_column_idx = len(output_column_names)
            output_column_names.append(KgtkFormat.ID)
        id_column_name: str = output_column_names[id_column_idx]

        # There should be exactly 4 output columns, iincluding an ID column.
        # If there are additional columns, some content may be lost when
        # unreifying records.
        num_columns: int = len(output_column_names)
        if num_columns < 4 or (num_columns > 4 and not self.allow_extra_columns):
            raise ValueError("Expecting 4 output columns, found %d." % num_columns)

        if self.verbose:
            print("Opening the output file: %s" % str(self.output_file_path), file=self.error_file, flush=True)
        # Open the output file.
        kw: KgtkWriter = KgtkWriter.open(output_column_names,
                                         self.output_file_path,
                                         mode=KgtkWriter.Mode[kr.mode.name],
                                         output_format=self.output_format,
                                         require_all_columns=not self.allow_extra_columns,
                                         prohibit_extra_columns=True,
                                         fill_missing_columns=self.allow_extra_columns,
                                         gzip_in_parallel=False,
                                         verbose=self.verbose,
                                         very_verbose=self.very_verbose)

        reifiedw: typing.Optional[KgtkWriter] = None
        if self.reified_file_path is not None:
            if self.verbose:
                print("Opening the reified value output file: %s" % str(self.reified_file_path), file=self.error_file, flush=True)
            reifiedw: KgtkWriter = KgtkWriter.open(kr.column_names,
                                                   self.reified_file_path,
                                                   mode=KgtkWriter.Mode[kr.mode.name],
                                                   output_format=self.output_format,
                                                   require_all_columns=not self.allow_extra_columns,
                                                   prohibit_extra_columns=True,
                                                   fill_missing_columns=self.allow_extra_columns,
                                                   gzip_in_parallel=False,
                                                   verbose=self.verbose,
                                                   very_verbose=self.very_verbose)

        unreifiedw: typing.Optional[KgtkWriter] = None
        if self.unreified_file_path is not None:
            if self.verbose:
                print("Opening the unreified value output file: %s" % str(self.unreified_file_path), file=self.error_file, flush=True)
            unreifiedw: KgtkWriter = KgtkWriter.open(output_column_names,
                                                   self.unreified_file_path,
                                                   mode=KgtkWriter.Mode[kr.mode.name],
                                                   output_format=self.output_format,
                                                   require_all_columns=True,
                                                   prohibit_extra_columns=True,
                                                   fill_missing_columns=False,
                                                   gzip_in_parallel=False,
                                                   verbose=self.verbose,
                                                   very_verbose=self.very_verbose)

        uninvolvedw: typing.Optional[KgtkWriter] = None
        if self.uninvolved_file_path is not None:
            if self.verbose:
                print("Opening the uninvolved records output file: %s" % str(self.uninvolved_file_path), file=self.error_file, flush=True)
            uninvolvedw: KgtkWriter = KgtkWriter.open(kr.column_names,
                                                   self.uninvolved_file_path,
                                                   mode=KgtkWriter.Mode[kr.mode.name],
                                                   output_format=self.output_format,
                                                   require_all_columns=True,
                                                   prohibit_extra_columns=True,
                                                   fill_missing_columns=False,
                                                   gzip_in_parallel=False,
                                                   verbose=self.verbose,
                                                   very_verbose=self.very_verbose)

        if self.verbose:
            print("Reading and grouping the input records.", file=self.error_file, flush=True)
        ksb: KgtkSortBuffer = KgtkSortBuffer.readall(kr, grouped=True, keygen=self.make_keygen(self.old_label_value))

        input_group_count: int = 0
        input_line_count: int = 0
        self.output_line_count = 0
        unreification_count: int = 0

        if self.verbose:
            print("Processing the input records.", file=self.error_file, flush=True)

        node1_group: typing.List[typing.List[str]]
        for node1_group in ksb.groupiterate():
            input_group_count += 1

            saw_error: bool = False
            saw_trigger: bool = False
            node1_value: typing.Optional[str] = None
            node2_values: typing.Set[str] = set()

            old_label_node2_value: typing.Optional[str] = None
            trigger_node1_value: typing.Optional[str] = None
           
            potential_edge_attributes: typing.List[typing.List[str]] = [ ]

            row: typing.List[str]
            for row in node1_group:
                input_line_count += 1
                node1: str = row[node1_column_idx]
                label: str = row[label_column_idx]
                node2: str = row[node2_column_idx]

                if label == self.trigger_label_value and node2 == self.trigger_node2_value:
                    if saw_trigger:
                        # TODO: Shout louder.
                        if self.verbose:
                            print("Warning: Duplicate trigger in input group %d (%s)" % (input_group_count, node1_value), file=self.error_file, flush=True)
                    saw_trigger = True
                    trigger_node1_value = node1

                elif label == self.value_label_value:
                    if len(node2_values) > 0 and node2 not in node2_values and not self.allow_multiple_values:
                        # TODO: Shout louder.
                        if self.verbose:
                            print("Warning: Multiple values in input group %d" % (input_group_count), file=self.error_file, flush=True)
                        saw_error = True
                    node2_values.add(node2)
                    
                elif label == self.old_label_value:
                    node1_value = node1
                    old_label_node2_value = node2

                else:
                    potential_edge_attributes.append(row)
                    
            if saw_trigger and \
               node1_value is not None and \
               len(node2_values) > 0 and \
               old_label_node2_value == trigger_node1_value and \
               not saw_error:
                # Unreification was triggered.
                unreification_count += 1

                node2_value: str = KgtkFormat.LIST_SEPARATOR.join(list(node2_values))

                if reifiedw is not None:
                    for row in node1_group:
                        reifiedw.write(row)

                self.write_new_edge(kw,
                                    reifiedw,
                                    potential_edge_attributes,
                                    node1_value,
                                    node2_value,
                                    trigger_node1_value,
                                    label_column_idx,
                                    node2_column_idx,
                                    node1_column_name,
                                    label_column_name,
                                    node2_column_name,
                                    id_column_name,
                )
                
            else:
                # Unreification was not triggered.  Pass this group of rows
                # through unchanged, except for possibly appending an ID
                # column.
                self.pass_group_through(kw, uninvolvedw, node1_group, new_id_column)

        if self.verbose:
            print("Processed %d records in %d groups." % (input_line_count, input_group_count), file=self.error_file, flush=True)
            print("Unreified %d groups." % unreification_count, file=self.error_file, flush=True)
            print("Wrote %d output records" % self.output_line_count, file=self.error_file, flush=True)

        
        kw.close()
        if reifiedw is not None:
            reifiedw.close()
        if unreifiedw is not None:
            unreifiedw.close()
        if uninvolvedw is not None:
            uninvolvedw.close()


    def make_new_id(self, edge_id: str, count: int, width: int)->str:
        # Generate a new ID that will sort after the new edge.
        # What if the existing ID is not a symbol or a string?
        #
        # TODO: Handle cases where the existing ID is not a symbol or string.
        new_id: str
        if edge_id.startswith(KgtkFormat.STRING_SIGIL) and edge_id.endswith(KgtkFormat.STRING_SIGIL):
            new_id = edge_id[:-1] + "-" + str(count).zfill(width) + KgtkFormat.STRING_SIGIL
        else:
            new_id = edge_id + "-" + str(count).zfill(width)
        return new_id

    def get_width(self, max_count: int)->int:
        return len(str(max_count).strip())
        
    def write_new_edge(self,
                       kw: KgtkWriter,
                       unreifiedw: typing.Optional[KgtkWriter],
                       potential_edge_attributes: typing.List[typing.List[str]],
                       node1_value: str,
                       node2_value: str,
                       edge_id: str,
                       label_column_idx: int,
                       node2_column_idx: int,
                       node1_column_name: str,
                       label_column_name: str,
                       node2_column_name: str,
                       id_column_name: str,
    ):
        new_label_value: str = self.new_label_value if self.new_label_value is not None else self.value_label_value
        kw.writemap({
            node1_column_name: node1_value,
            label_column_name: new_label_value,
            node2_column_name: node2_value,
            id_column_name: edge_id,
        })
        self.output_line_count += 1
        
        if unreifiedw is not None:
            unreifiedw.writemap({
                node1_column_name: node1_value,
                label_column_name: new_label_value,
                node2_column_name: node2_value,
                id_column_name: edge_id,
            })

        self.write_edge_attributes(kw,
                                   unreifiedw,
                                   potential_edge_attributes,
                                   edge_id,
                                   label_column_idx,
                                   node2_column_idx,
                                   node1_column_name,
                                   label_column_name,
                                   node2_column_name,
                                   id_column_name,
        )

    def write_edge_attributes(self,
                              kw: KgtkWriter,
                              unreifiedw: typing.Optional[KgtkWriter],
                              potential_edge_attributes: typing.List[typing.List[str]],
                              edge_id: str,
                              label_column_idx: int,
                              node2_column_idx: int,
                              node1_column_name: str,
                              label_column_name: str,
                              node2_column_name: str,
                              id_column_name: str,
    ):
        width: int = self.get_width(len(potential_edge_attributes))
        attribute_number: int = 0
        edge_row: typing.List[str]
        for edge_row in potential_edge_attributes:
            attribute_number += 1
            attr_edge_id: str = self.make_new_id(edge_id, attribute_number, width)

            kw.writemap({
                node1_column_name: edge_id,
                label_column_name: edge_row[label_column_idx],
                node2_column_name: edge_row[node2_column_idx],
                id_column_name: attr_edge_id
            })
            self.output_line_count += 1
                
            if unreifiedw is not None:
                unreifiedw.writemap({
                    node1_column_name: edge_id,
                    label_column_name: edge_row[label_column_idx],
                    node2_column_name: edge_row[node2_column_idx],
                    id_column_name: attr_edge_id
                })
                

    def pass_group_through(self,
                           kw: KgtkWriter,
                           uninvolvedw: typing.Optional[KgtkWriter],
                           node1_group: typing.List[typing.List[str]],
                           new_id_column: bool):
        # Unreification was not triggered.  Pass this group of rows
        # through unchanged, except for possibly appending an ID
        # column.
        #
        # TODO: Perhaps we'd like to build an ID value at the same time?
        row: typing.List[str]
        for row in node1_group:
            if uninvolvedw is not None:
                uninvolvedw.write(row)
                
            if new_id_column:
                row = row.copy()
                row.append("")

            kw.write(row)
            self.output_line_count += 1
        

    @classmethod
    def add_arguments(cls, parser: ArgumentParser):
        parser.add_argument(      "--trigger-label", dest="trigger_label_value", required=True,
                                  help="A value in the label (or its alias) column that identifies the trigger record. (default=%(default)s).",
                                  type=str, default=cls.DEFAULT_TRIGGER_LABEL_VALUE)

        parser.add_argument(      "--trigger-node2", dest="trigger_node2_value", required=True,
                                  help="A value in the node2 (or its alias) column that identifies the trigger record. " +
                                  "This is a required parameter for which there is no default value. (default=%(default)s).",
                                  type=str, default=cls.DEFAULT_TRIGGER_NODE2_VALUE)
    
        parser.add_argument(      "--value-label", dest="value_label_value", required=True,
                                  help="A value in the label (or its alias) column that identifies the record with the node2 value for the new, unreified edge. " +
                                  "This is a required parameter for which there is no default value. (default=%(default)s).",
                                  type=str, default=cls.DEFAULT_VALUE_LABEL_VALUE)
    
        parser.add_argument(      "--old-label", dest="old_label_value", required=True,
                                  help="A value in the label (or its alias) column  that identifies the edge with the node1 value being unreified. " +
                                  "The value in the node1 (or its alias) column of this record will be used in the node1 (or its alias) column for the " +
                                  "new, unreified edge. " +
                                  "This is a required parameter for which there is no default value. (default=%(default)s).",
                                  type=str, default=cls.DEFAULT_OLD_LABEL_VALUE)
    
        parser.add_argument(      "--new-label", dest="new_label_value",
                                  help="The value to be entered in the label (or its alias) column of the new, unreified edge. " +
                                  "If not specified (None), the value from --value-label is used. (default=%(default)s).",
                                  type=str, default=cls.DEFAULT_NEW_LABEL_VALUE)

        parser.add_argument(      "--allow-multiple-values", dest="allow_multiple_values",
                                  help="When true, allow multiple values (a '|' list) in the node2 (or its alias) column of the new, unreified edge. " +
                                  "(default=%(default)s).",
                                  type=optional_bool, nargs='?', const=True, default=cls.DEFAULT_ALLOW_MULTIPLE_VALUES)

        parser.add_argument(      "--allow-extra-columns", dest="allow_extra_columns",
                                  help="When true, allow extra columns (beyond node1, label, node2, and id, or their aliases. " +
                                  "Warning: the contents of these columns may be lost silently in unreified statements. " +
                                  "(default=%(default)s).",
                                  type=optional_bool, nargs='?', const=True, default=cls.DEFAULT_ALLOW_MULTIPLE_VALUES)

def main():
    """
    Test the KGTK copy template.
    """
    parser: ArgumentParser = ArgumentParser()

    parser.add_argument("-i", "--input-file", dest="input_file_path",
                        help="The KGTK input file. (default=%(default)s)", type=Path, default="-")

    parser.add_argument("-o", "--output-file", dest="output_file_path",
                        help="The KGTK output file. (default=%(default)s).", type=Path, default="-")
    
    parser.add_argument(      "--reified-file", dest="reified_file_path",
                              help="A KGTK output file that will contain only the reified values. (default=%(default)s).", type=Path, default=None)
    
    parser.add_argument(      "--unreified-file", dest="unreified_file_path",
                              help="A KGTK output file that will contain only the unreified values. (default=%(default)s).", type=Path, default=None)
    
    parser.add_argument(      "--uninvolved-file", dest="uninvolved_file_path",
                              help="A KGTK output file that will contain only the uninvolved input records. (default=%(default)s).", type=Path, default=None)
    
    parser.add_argument(      "--output-format", dest="output_format", help="The file format (default=kgtk)", type=str,
                              choices=KgtkWriter.OUTPUT_FORMAT_CHOICES)

    KgtkUnreifyValues.add_arguments(parser)
    KgtkReader.add_debug_arguments(parser)
    KgtkReaderOptions.add_arguments(parser, mode_options=False, expert=True)
    KgtkValueOptions.add_arguments(parser)

    args: Namespace = parser.parse_args()

    error_file: typing.TextIO = sys.stdout if args.errors_to_stdout else sys.stderr

    # Build the option structures.                                                                                                                          
    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_args(args)
    value_options: KgtkValueOptions = KgtkValueOptions.from_args(args)

   # Show the final option structures for debugging and documentation.                                                                                             
    if args.show_options:
        print("--input-files %s" % " ".join([str(path) for  path in input_file_paths]), file=error_file, flush=True)
        print("--output-file=%s" % str(args.output_file_path), file=error_file, flush=True)
        if args.reified_file_path is not None:
            print("--reified-file=%s" % str(args.reified_file_path), file=error_file, flush=True)
        if args.unreified_file_path is not None:
            print("--unreified-file=%s" % str(args.unreified_file_path), file=error_file, flush=True)
        if args.uninvolved_file_path is not None:
            print("--uninvolved-file=%s" % str(args.uninvolved_file_path), file=error_file, flush=True)

        if args.output_format is not None:
            print("--output-format=%s" % args.output_format, file=error_file, flush=True)

        if args.trigger_label_value is not None:
            print("--trigger-label=%s" % args.trigger_label_value, file=error_file, flush=True)
        if args.trigger_node2_value is not None:
            print("--trigger-node2=%s" % args.trigger_node2_value, file=error_file, flush=True)
        if args.value_label_value is not None:
            print("--value-label=%s" % args.value_label_value, file=error_file, flush=True)
        if args.old_label_value is not None:
            print("--old-label=%s" % args.old_label_value, file=error_file, flush=True)
        if args.new_label_value is not None:
            print("--new-label=%s" % args.new_label_value, file=error_file, flush=True)

        print("--allow-multiple-values=%s" % str(args.allow_multiple_values), file=error_file, flush=True)
        print("--allow-extra-columns=%s" % str(args.allow_extra_columns), file=error_file, flush=True)

        reader_options.show(out=error_file)
        value_options.show(out=error_file)

    kuv: KgtkUnreifyValues = KgtkUnreifyValues(
        input_file_path=args.input_file_path,
        output_file_path=args.output_file_path,
        reified_file_path=args.reified_file_path,
        unreified_file_path=args.unreified_file_path,
        uninvolved_file_path=args.uninvolved_file_path,

        trigger_label_value=args.trigger_label_value,
        trigger_node2_value=args.trigger_node2_value,
        value_label_value=args.value_label_value,
        old_label_value=args.old_label_value,
        new_label_value=args.new_label_value,

        allow_multiple_values=args.allow_multiple_values,
        allow_extra_columns=args.allow_extra_columns,

        reader_options=reader_options,
        value_options=value_options,
        output_format=args.output_format,
        error_file=error_file,
        verbose=args.verbose,
        very_verbose=args.very_verbose,
    )

    kuv.process()
    
if __name__ == "__main__":
    main()
