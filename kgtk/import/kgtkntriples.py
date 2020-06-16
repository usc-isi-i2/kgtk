"""Import ntriples into KGTK format.
"""
from argparse import ArgumentParser, Namespace
import attr
import csv
from pathlib import Path
import sys
import typing
import uuid

from kgtk.kgtkformat import KgtkFormat
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderMode
from kgtk.io.kgtkwriter import KgtkWriter
from kgtk.reshape.kgtkidbuilder import KgtkIdBuilder, KgtkIdBuilderOptions
from kgtk.utils.argparsehelpers import optional_bool


@attr.s(slots=True, frozen=True)
class KgtkNtriples(KgtkFormat):
    input_file_path: Path = attr.ib(validator=attr.validators.instance_of(Path))

    output_file_path: Path = attr.ib(validator=attr.validators.instance_of(Path))

    reject_file_path: typing.Optional[Path] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Path)))

    namespace_file_path: typing.Optional[Path] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Path)))

    # attr.converters.default_if_none(...) does not seem to work.                                                                                                   
    local_namespace_prefix: str = attr.ib(validator=attr.validators.instance_of(str))
    local_namespace_use_uuid: bool = attr.ib(validator=attr.validators.instance_of(bool))

    prefix_expansion_label: str = attr.ib(validator=attr.validators.instance_of(str), default="prefix_expansion")

    build_id: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    idbuilder_options: typing.Optional[KgtkIdBuilderOptions] = attr.ib(default=None)

    error_file: typing.TextIO = attr.ib(default=sys.stderr)
    verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    very_verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    local_namespace_uuid: str = str(uuid.uuid4())

    COLUMN_NAMES: typing.List[str] = [KgtkFormat.NODE1, KgtkFormat.LABEL, KgtkFormat.NODE2, KgtkFormat.ID]
    
    namespace_prefixes: typing.MutableMapping[str, str] = { }
    namespace_ids: typing.MutableMapping[str, str] = { }

    def convert_blank_node(self, item: str)->str:
        body: str = item[1:] # Stip the leading underscore, keep the colon.
        if self.local_namespace_use_uuid:
            return self.local_namespace_prefix + self.local_namespace_uuid + body
        else:
            return self.local_namespace_prefix + body

    def convert(self, item: str, ew: KgtkWriter)->str:
        """
        Convert an ntriples item to KGTK format.

        TODO: update output_line_count for row written here.
        """
        if item.startswith("_:"):
            return self.convert_blank_node(item)

        return item            
    
    def read_initial_namespaces(self)->int:
        # Read the namespaces:
        if self.namespace_file_path is None:
            return 0

        if self.verbose:
            print("Processing namespace file file %s" % str(self.reject_file_path), file=self.error_file, flush=True)

        kr: KgtkReader =  KgtkReader.open(self.namespace_file_path,
                                          mode=KgtkReaderMode.EDGE,
                                          error_file=self.error_file,
                                          verbose=self.verbose,
                                          very_verbose=self.very_verbose,
        )
        namespace_line_count: int = 0
        namespace_row: typing.List[str]
        for namespace_row in kr:
            namespace_line_count += 1
            if namespace_row[kr.label_column_idx] == self.prefix_expansion_label:
                namespace_id: str = namespace_row[kr.node1_column_idx]
                namespace_prefix: str = namespace_row[kr.node2_column_idx]
                if namespace_prefix in self.namespace_prefixes:
                    if self.verbose:
                        print("Duplicate initial namespace prefix '%s'" % namespace_prefix)
                else:
                    self.namespace_prefixes[namespace_prefix] = namespace_id
                if namespace_id in self.namespace_ids:
                    if self.verbose:
                        print("Duplicate initial namespace id '%s'" % namespace_id)
                else:
                    self.namespace_ids[namespace_id] = namespace_prefix
            else:
                if self.verbose:
                    print("Ignoring initial namespace label '%s'" % namespace_row[kr.label_column_idx])

        return namespace_line_count
        
    def write_namespaces(self, ew: KgtkWriter)->int:
        # Append the namespaces to the output file.
        output_line_count: int = 0
        n_id: str
        for n_id in sorted(self.namespace_ids.keys()):
            o_row: typing.List[str] = ["", "", "", "" ]
            o_row[0] = n_id
            o_row[1] = self.prefix_expansion_label
            o_row[3] = self.namespace_ids[n_id]
            # TODO: assign an ID.
            ew.write(o_row)
            output_line_count += 1
        return output_line_count

    def process(self):

        if self.verbose:
            print("Opening output file %s" % str(self.output_file_path), file=self.error_file, flush=True)
        # Open the output file.
        ew: KgtkWriter = KgtkWriter.open(self.COLUMN_NAMES,
                                         self.output_file_path,
                                         mode=KgtkWriter.Mode.EDGE,
                                         require_all_columns=False,
                                         prohibit_extra_columns=True,
                                         fill_missing_columns=False,
                                         gzip_in_parallel=False,
                                         verbose=self.verbose,
                                         very_verbose=self.very_verbose)

        rw: typing.Optional[KgtkWriter] = None
        if self.reject_file_path is not None:
            if self.verbose:
                print("Opening reject file %s" % str(self.reject_file_path), file=self.error_file, flush=True)
            # Open the reject file.
            rw: KgtkWriter = KgtkWriter.open(self.COLUMN_NAMES,
                                             self.reject_file_path,
                                             mode=KgtkWriter.Mode.NONE,
                                             require_all_columns=False,
                                             prohibit_extra_columns=True,
                                             fill_missing_columns=False,
                                             gzip_in_parallel=False,
                                             verbose=self.verbose,
                                             very_verbose=self.very_verbose)

        input_line_count: int = 0
        reject_line_count: int = 0
        output_line_count: int = 0
        
        # Read the namespaces:
        namespace_line_count: int =  self.read_initial_namespaces()
            
        # Open the input file.
        if self.verbose:
            print("Opening the input file: %s" % self.input_file_path, file=self.error_file, flush=True)
        with open(self.input_file_path, newline='') as infile:
            # Use the CSV reader with suitable delimiters.
            reader = csv.reader(infile, delimiter=" ", doublequote=False, escapechar="\\")
            row: typing.List[str]
            for row in reader:
                input_line_count += 1

                if len(row) != 4:
                    if self.verbose:
                        print("Line %d: expected 4 fields, got %d." % len(row))
                    if rw is not None:
                        rw.write(row)
                    reject_line_count += 1
                    continue

                if row[3] != ".":
                    if self.verbose:
                        print("Line %d: missing trailing dot." % input_line_count)
                    if rw is not None:
                        rw.write(row)
                    reject_line_count += 1
                    continue

                output_row: typing.List[str] = ["", "", "", "" ]
                output_row[0] = self.convert(row[0], ew)
                output_row[1] = self.convert(row[1], ew)
                output_row[2] = self.convert(row[2], ew)

                # TODO: build an ID

                ew.write(output_row)
                output_line_count += 1

        # Append the namespaces to the output file:
        output_line_count += self.write_namespaces(ew)

        if self.verbose:
            print("Processed %d known namespaces." % (namespace_line_count), file=self.error_file, flush=True)
            print("Processed %d records." % (input_line_count), file=self.error_file, flush=True)
            print("Rejected %d records." % (reject_line_count), file=self.error_file, flush=True)
            print("Wrote %d records." % (output_line_count), file=self.error_file, flush=True)
        
        if ew is not None:
            ew.close()
            
        if rw is not None:
            rw.close()
            
def main():
    """
    Test the KGTK implode processor.
    """
    parser: ArgumentParser = ArgumentParser()

    parser.add_argument(dest="input_file_path", help="The KGTK file with the input data. (default=%(default)s)", type=Path, nargs="?", default="-")

    parser.add_argument("-o", "--output-file", dest="output_file_path", help="The KGTK file to write (default=%(default)s).", type=Path, default="-")
    
    parser.add_argument(      "--reject-file", dest="reject_file_path", help="The KGTK file into which to write rejected records. (default=%(default)s).",
                              type=Path, default=None)
    
    parser.add_argument(      "--namespace-file", dest="namespace_file_path", help="The KGTK file with known namespaces. (default=%(default)s).",
                              type=Path, default=None)
    
    parser.add_argument(      "--local-namespace-prefix", dest="local_namespace_prefix",
                              help="The namespace prefix for blank nodes. (default=%(default)s).",
                              default="X")

    parser.add_argument(      "--local-namespace-use-uuid", dest="local_namespace_use_uuid",
                              help="Generate a UUID for the local namespace. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=True)

    parser.add_argument(      "--build-id", dest="build_id",
                              help="Build id values in an id column. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    KgtkIdBuilderOptions.add_arguments(parser)
    KgtkReader.add_debug_arguments(parser)

    args: Namespace = parser.parse_args()

    error_file: typing.TextIO = sys.stdout if args.errors_to_stdout else sys.stderr

    # Build the option structures.                                                                                                                          
    idbuilder_options: KgtkIdBuilderOptions = KgtkIdBuilderOptions.from_args(args)

   # Show the final option structures for debugging and documentation.                                                                                             
    if args.show_options:
        print("input: %s" % str(args.input_file_path), file=error_file, flush=True)
        print("--output-file=%s" % str(args.output_file_path), file=error_file, flush=True)
        # TODO: show ifempty-specific options.
        if args.reject_file_path is not None:
            print("--reject-file=%s" % str(args.reject_file_path), file=error_file, flush=True)
        if args.namespace_file_path is not None:
            print("--namespace-file=%s" % str(args.namespace_file_path), file=error_file, flush=True)
        print("--local-namespace-prefix %s" % args.local_namespace_prefix, file=error_file, flush=True)
        print("--local-namespace-use-uuid %s" % args.local_namespace_use_uuid, file=error_file, flush=True)
        print("--build-id=%s" % str(args.build_id), file=error_file, flush=True)

        idbuilder_options.show(out=error_file)

    kn: KgtkNtriples = KgtkNtriples(
        input_file_path=args.input_file_path,
        output_file_path=args.output_file_path,
        reject_file_path=args.reject_file_path,
        namespace_file_path=args.namespace_file_path,
        local_namespace_prefix=args.local_namespace_prefix,
        local_namespace_use_uuid=args.local_namespace_use_uuid,
        build_id=args.build_id,
        idbuilder_options=idbuilder_options,
        error_file=error_file,
        verbose=args.verbose,
        very_verbose=args.very_verbose)

    kn.process()
    
if __name__ == "__main__":
    main()
