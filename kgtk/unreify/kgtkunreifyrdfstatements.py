"""
Unreify RDF statements in KGTK files.

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
class KgtkUnreifyRdfStatements(KgtkFormat):
    DEFAULT_TRIGGER_LABEL_VALUE: str = "rdf:type"
    DEFAULT_TRIGGER_NODE2_VALUE: str = "rdf:Statement"
    DEFAULT_RDF_OBJECT_LABEL_VALUE: str = "rdf:object"
    DEFAULT_RDF_PREDICATE_LABEL_VALUE: str = "rdf:predicate"
    DEFAULT_RDF_SUBJECT_LABEL_VALUE: str = "rdf:subject"
    DEFAULT_ALLOW_MULTIPLE_SUBJECTS: bool = True
    DEFAULT_ALLOW_MULTIPLE_PREDICATES: bool = True
    DEFAULT_ALLOW_MULTIPLE_OBJECTS: bool = True

    input_file_path: Path = attr.ib(validator=attr.validators.instance_of(Path))
    output_file_path: Path = attr.ib(validator=attr.validators.instance_of(Path))

    reified_file_path: typing.Optional[Path] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Path)))
    unreified_file_path: typing.Optional[Path] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Path)))
    uninvolved_file_path: typing.Optional[Path] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Path)))

    trigger_label_value: str = attr.ib(validator=attr.validators.instance_of(str), default=DEFAULT_TRIGGER_LABEL_VALUE)
    trigger_node2_value: str = attr.ib(validator=attr.validators.instance_of(str), default=DEFAULT_TRIGGER_NODE2_VALUE)
    rdf_object_label_value: str = attr.ib(validator=attr.validators.instance_of(str), default=DEFAULT_RDF_OBJECT_LABEL_VALUE)
    rdf_predicate_label_value: str = attr.ib(validator=attr.validators.instance_of(str), default=DEFAULT_RDF_PREDICATE_LABEL_VALUE)
    rdf_subject_label_value: str = attr.ib(validator=attr.validators.instance_of(str), default=DEFAULT_RDF_SUBJECT_LABEL_VALUE)

    allow_multiple_subjects: bool = attr.ib(validator=attr.validators.instance_of(bool), default=DEFAULT_ALLOW_MULTIPLE_SUBJECTS)
    allow_multiple_predicates: bool = attr.ib(validator=attr.validators.instance_of(bool), default=DEFAULT_ALLOW_MULTIPLE_PREDICATES)
    allow_multiple_objects: bool = attr.ib(validator=attr.validators.instance_of(bool), default=DEFAULT_ALLOW_MULTIPLE_OBJECTS)

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

        if self.verbose:
            print("Opening the output file: %s" % str(self.output_file_path), file=self.error_file, flush=True)
        # Open the output file.
        kw: KgtkWriter = KgtkWriter.open(output_column_names,
                                         self.output_file_path,
                                         mode=KgtkWriter.Mode[kr.mode.name],
                                         output_format=self.output_format,
                                         require_all_columns=True,
                                         prohibit_extra_columns=True,
                                         fill_missing_columns=False,
                                         gzip_in_parallel=False,
                                         verbose=self.verbose,
                                         very_verbose=self.very_verbose)

        reifiedw: typing.Optional[KgtkWriter] = None
        if self.reified_file_path is not None:
            if self.verbose:
                print("Opening the reified RDF statements output file: %s" % str(self.reified_file_path), file=self.error_file, flush=True)
            reifiedw: KgtkWriter = KgtkWriter.open(kr.column_names,
                                                   self.reified_file_path,
                                                   mode=KgtkWriter.Mode[kr.mode.name],
                                                   output_format=self.output_format,
                                                   require_all_columns=True,
                                                   prohibit_extra_columns=True,
                                                   fill_missing_columns=False,
                                                   gzip_in_parallel=False,
                                                   verbose=self.verbose,
                                                   very_verbose=self.very_verbose)

        unreifiedw: typing.Optional[KgtkWriter] = None
        if self.unreified_file_path is not None:
            if self.verbose:
                print("Opening the unreified RDF statements output file: %s" % str(self.unreified_file_path), file=self.error_file, flush=True)
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
        ksb: KgtkSortBuffer = KgtkSortBuffer.readall(kr, grouped=True, keygen=KgtkSortBuffer.node1_keygen)

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
            rdf_object_values: typing.Set[str] = set()
            rdf_predicate_values: typing.Set[str] = set()
            rdf_subject_values: typing.Set[str] = set()
            
            potential_edge_attributes: typing.List[typing.List[str]] = [ ]

            row: typing.List[str]
            for row in node1_group:
                input_line_count += 1
                if node1_value is None:
                    node1_value = row[node1_column_idx]
                label: str = row[label_column_idx]
                node2: str = row[node2_column_idx]

                if label == self.trigger_label_value and node2 == self.trigger_node2_value:
                    if saw_trigger:
                        # TODO: Shout louder.
                        if self.verbose:
                            print("Warning: Duplicate trigger in input group %d (%s)" % (input_group_count, node1_value), file=self.error_file, flush=True)
                    saw_trigger = True
                elif label == self.rdf_object_label_value:
                    if len(rdf_object_values) > 0 and node2 not in rdf_object_values and not self.allow_multple_objects:
                        # TODO: Shout louder.
                        if self.verbose:
                            print("Warning: Multiple rdf objects in input group %d (%s)" % (input_group_count, node1_value), file=self.error_file, flush=True)
                        saw_error = True # until we implement the cartesan product
                    rdf_object_values.add(node2)
                elif label == self.rdf_predicate_label_value:
                    if len(rdf_predicate_values) > 0  and node2 not in rdf_predicate_values and not self.allow_multiple_predicates:
                        # TODO: Shout louder.
                        if self.verbose:
                            print("Warning: Multiple rdf predicates in input group %d (%s)" % (input_group_count, node1_value), file=self.error_file, flush=True)
                        saw_error = True # until we implement the cartesan product
                    rdf_predicate_values.add(node2)
                elif label == self.rdf_subject_label_value:
                    if len(rdf_subject_values) > 0 and node2 not in rdf_subject_values and not self.allow_multple_subjects:
                        # TODO: Shout louder.
                        if self.verbose:
                            print("Warning: Multiple rdf subjects in input group %d (%s)" % (input_group_count, node1_value), file=self.error_file, flush=True)
                        saw_error = True # until we implement the cartesan product
                    rdf_subject_values.add(node2)
                else:
                    potential_edge_attributes.append(row)
                    
            rdf_product: int = len(rdf_object_values) * len(rdf_predicate_values) * len(rdf_subject_values)

            if saw_trigger and \
               node1_value is not None and \
               rdf_product > 0 and \
               not saw_error:
                # Unreification was triggered.
                unreification_count += 1

                self.write_new_edge_or_edges(kw,
                                             reifiedw,
                                             unreifiedw,
                                             potential_edge_attributes,
                                             node1_group,
                                             rdf_product,
                                             list(rdf_subject_values),
                                             list(rdf_predicate_values),
                                             list(rdf_object_values),
                                             node1_value,
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

    def write_new_edge_or_edges(self,
                                kw: KgtkWriter,
                                reifiedw: typing.Optional[KgtkWriter],
                                unreifiedw: typing.Optional[KgtkWriter],
                                potential_edge_attributes: typing.List[typing.List[str]],
                                node1_group: typing.List[typing.List[str]],
                                rdf_product: int,
                                rdf_subject_values: typing.List[str],
                                rdf_predicate_values: typing.List[str],
                                rdf_object_values: typing.List[str],
                                edge_id: str,
                                label_column_idx: int,
                                node2_column_idx: int,
                                node1_column_name: str,
                                label_column_name: str,
                                node2_column_name: str,
                                id_column_name: str,
    ):
        if reifiedw is not None:
            for row in node1_group:
                reifiedw.write(row)
        if rdf_product == 1:
            # Generate the new edge:
            self.write_new_edge(kw,
                                unreifiedw,
                                potential_edge_attributes,
                                edge_id,
                                rdf_subject_values[0],
                                rdf_predicate_values[0],
                                rdf_object_values[0],
                                label_column_idx,
                                node2_column_idx,
                                node1_column_name,
                                label_column_name,
                                node2_column_name,
                                id_column_name,
            )
        else:
            width: int = self.get_width(rdf_product)
            edge_number: int = 0
            rdf_subject_value: str
            for rdf_subject_value in sorted(rdf_subject_values):
                rdf_predicate_value: str
                for rdf_predicate_value in sorted(rdf_predicate_values):
                    rdf_object_value: str
                    for rdf_object_value in sorted(rdf_object_values):
                        edge_number += 1
                        new_edge_id: str = self.make_new_id(edge_id, edge_number, width)
                        self.write_new_edge(kw,
                                            unreifiedw,
                                            potential_edge_attributes,
                                            new_edge_id,
                                            rdf_subject_value,
                                            rdf_predicate_value,
                                            rdf_object_value,
                                            label_column_idx,
                                            node2_column_idx,
                                            node1_column_name,
                                            label_column_name,
                                            node2_column_name,
                                            id_column_name,
            )


    def make_new_id(self, edge_id: str, count: int, width: int)->str:
        # Generate a new ID that will sort after the new edge.
        # What if the existing ID is not a symbol or a string?
        #
        # TODO: Handle these cases.
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
                       edge_id: str,
                       rdf_subject_value: str,
                       rdf_predicate_value: str,
                       rdf_object_value: str,
                       label_column_idx: int,
                       node2_column_idx: int,
                       node1_column_name: str,
                       label_column_name: str,
                       node2_column_name: str,
                       id_column_name: str,
    ):
        kw.writemap({
            node1_column_name: rdf_subject_value,
            label_column_name: rdf_predicate_value,
            node2_column_name: rdf_object_value,
            id_column_name: edge_id,
        })
        self.output_line_count += 1
        
        if unreifiedw is not None:
            unreifiedw.writemap({
                node1_column_name: rdf_subject_value,
                label_column_name: rdf_predicate_value,
                node2_column_name: rdf_object_value,
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
        parser.add_argument(      "--trigger-label", dest="trigger_label_value",
                                  help="A value that identifies the trigger label. (default=%(default)s).",
                                  type=str, default=cls.DEFAULT_TRIGGER_LABEL_VALUE)

        parser.add_argument(      "--trigger-node2", dest="trigger_node2_value",
                                  help="A value that identifies the trigger node2. (default=%(default)s).",
                                  type=str, default=cls.DEFAULT_TRIGGER_NODE2_VALUE)
    
        parser.add_argument(      "--node1-role", dest="rdf_subject_label_value",
                                  help="The label that identifies the edge with the node2 value that will serve in the node1 role. (default=%(default)s).",
                                  type=str, default=cls.DEFAULT_RDF_SUBJECT_LABEL_VALUE)
    
        parser.add_argument(      "--label-role", dest="rdf_predicate_label_value",
                                  help="The label that identifies the edge with the node2 value that will serve in the label role. (default=%(default)s).",
                                  type=str, default=cls.DEFAULT_RDF_PREDICATE_LABEL_VALUE)
    
        parser.add_argument(      "--node2-role", dest="rdf_object_label_value",
                                  help="The label that identifies the edge with the node2 value that will serve in the node2 role. (default=%(default)s).",
                                  type=str, default=cls.DEFAULT_RDF_OBJECT_LABEL_VALUE)

        parser.add_argument(      "--allow-multiple-subjects", dest="allow_multiple_subjects",
                                  help="When true, allow multiple subjects, resulting in a cartesian product. (default=%(default)s).",
                                  type=optional_bool, nargs='?', const=True, default=cls.DEFAULT_ALLOW_MULTIPLE_SUBJECTS)

        parser.add_argument(      "--allow-multiple-predicates", dest="allow_multiple_predicates",
                                  help="When true, allow multiple predicates, resulting in a cartesian product. (default=%(default)s).",
                                  type=optional_bool, nargs='?', const=True, default=cls.DEFAULT_ALLOW_MULTIPLE_PREDICATES)

        parser.add_argument(      "--allow-multiple-objects", dest="allow_multiple_objects",
                                  help="When true, allow multiple objects, resulting in a cartesian product. (default=%(default)s).",
                                  type=optional_bool, nargs='?', const=True, default=cls.DEFAULT_ALLOW_MULTIPLE_OBJECTS)
            
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
                              help="A KGTK output file that will contain only the reified RDF statements. (default=%(default)s).", type=Path, default=None)
    
    parser.add_argument(      "--unreified-file", dest="unreified_file_path",
                              help="A KGTK output file that will contain only the unreified RDF statements. (default=%(default)s).", type=Path, default=None)
    
    parser.add_argument(      "--uninvolved-file", dest="uninvolved_file_path",
                              help="A KGTK output file that will contain only the uninvolved input records. (default=%(default)s).", type=Path, default=None)
    
    parser.add_argument(      "--output-format", dest="output_format", help="The file format (default=kgtk)", type=str,
                              choices=KgtkWriter.OUTPUT_FORMAT_CHOICES)

    KgtkUnreifyRdfStatements.add_arguments(parser)
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

        print("--trigger-label=%s" % args.trigger_label_value, file=error_file, flush=True)
        print("--trigger-node2=%s" % args.trigger_node2_value, file=error_file, flush=True)
        print("--node1-role=%s" % args.rdf_subject_label_value, file=error_file, flush=True)
        print("--label-role=%s" % args.rdf_predicate_label_value, file=error_file, flush=True)
        print("--node2-role=%s" % args.rdf_object_label_value, file=error_file, flush=True)

        print("--allow-multiple-subjects=%s" % str(args.allow_multiple_subjects), file=error_file, flush=True)
        print("--allow-multiple-predicates=%s" % str(args.allow_multiple_predicates), file=error_file, flush=True)
        print("--allow-multiple-objects=%s" % str(args.allow_multiple_objects), file=error_file, flush=True)

        reader_options.show(out=error_file)
        value_options.show(out=error_file)

    kurs: KgtkUnreifyRdfStatements = KgtkUnreifyRdfStatements(
        input_file_path=args.input_file_path,
        output_file_path=args.output_file_path,
        reified_file_path=args.reified_file_path,
        unreified_file_path=args.unreified_file_path,
        uninvolved_file_path=args.uninvolved_file_path,

        trigger_label_value=args.trigger_label_value,
        trigger_node2_value=args.trigger_node2_value,
        rdf_object_label_value=args.rdf_object_label_value,
        rdf_predicate_label_value=args.rdf_predicate_label_value,
        rdf_subject_label_value=args.rdf_subject_label_value,

        allow_multiple_subjects=args.allow_multiple_subjects,
        allow_multiple_predicates=args.allow_multiple_predicates,
        allow_multiple_objects=args.allow_multiple_objects,

        reader_options=reader_options,
        value_options=value_options,
        output_format=args.output_format,
        error_file=error_file,
        verbose=args.verbose,
        very_verbose=args.very_verbose,
    )

    kurs.process()
    
if __name__ == "__main__":
    main()
