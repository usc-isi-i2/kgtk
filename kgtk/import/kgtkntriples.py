"""Import ntriples into KGTK format.
"""
from argparse import ArgumentParser, Namespace
import attr
import csv
from pathlib import Path
import sys
import typing
from kgtk.kgtkformat import KgtkFormat
from kgtk.io.kgtkreader import KgtkReader
from kgtk.io.kgtkwriter import KgtkWriter
from kgtk.reshape.kgtkidbuilder import KgtkIdBuilder, KgtkIdBuilderOptions
from kgtk.utils.argparsehelpers import optional_bool


@attr.s(slots=True, frozen=True)
class KgtkNtriples(KgtkFormat):
    input_file_path: Path = attr.ib(validator=attr.validators.instance_of(Path))

    output_file_path: Path = attr.ib(validator=attr.validators.instance_of(Path))

    reject_file_path: typing.Optional[Path] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Path)))

    # attr.converters.default_if_none(...) does not seem to work.                                                                                                   
    local_namespace_prefix: str = attr.ib(validator=attr.validators.instance_of(str))
    local_namespace_uuid: bool = attr.ib(validator=attr.validators.instance_of(bool))

    build_id: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    idbuilder_options: typing.Optional[KgtkIdBuilderOptions] = attr.ib(default=None)

    error_file: typing.TextIO = attr.ib(default=sys.stderr)
    verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    very_verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    COLUMN_NAMES: typing.List[str] = ["node1", "label", "node2", "dot"]
    
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

        # Open the input file.
        if self.verbose:
            print("Opening the input file: %s" % self.input_file_path, file=self.error_file, flush=True)
        with open(self.input_file_path, newline='') as infile:
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

                ew.write(row)
                output_line_count += 1

        if self.verbose:
            print("Processed %d records." % (input_line_count), file=self.error_file, flush=True)
            print("Rejected %d records." % (reject_line_count), file=self.error_file, flush=True)
            print("Wrote %d records." % (output_line_count), file=self.error_file, flush=True)
        
        infile.close()

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
    
    parser.add_argument(      "--local-namespace-prefix", dest="local_namespace_prefix",
                              help="The namespace prefix for blank nodes. (default=%(default)s).",
                              default="X")

    parser.add_argument(      "--local-namespace-uuid", dest="local_namespace_uuid",
                              help="Generate a UUID for the local namespace. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=True)

    parser.add_argument(      "--reject-file", dest="reject_file_path", help="The KGTK file into which to write rejected records (default=%(default)s).",
                              type=Path, default=None)
    
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
        print("--local-namespace-prefix %s" % args.local_namespace_prefix, file=error_file, flush=True)
        print("--local-namespace-uui %s" % args.local_namespace_uui, file=error_file, flush=True)
        print("--build-id=%s" % str(args.build_id), file=error_file, flush=True)

        idbuilder_options.show(out=error_file)

    kn: KgtkNtriples = KgtkNtriples(
        input_file_path=args.input_file_path,
        output_file_path=args.output_file_path,
        reject_file_path=args.reject_file_path,
        local_namespace_prefix=args.local_namespace_prefix,
        local_namespace_uuid=args.local_namespace_uuid,
        build_id=args.build_id,
        idbuilder_options=idbuilder_options,
        error_file=error_file,
        verbose=args.verbose,
        very_verbose=args.very_verbose)

    kn.process()
    
if __name__ == "__main__":
    main()
