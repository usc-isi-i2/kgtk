"""
Cat multuple KGTK file together.

TODO: Need output file mode.

"""

from argparse import ArgumentParser
import attr
from pathlib import Path
import sys
import typing

from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
from kgtk.io.kgtkwriter import KgtkWriter
from kgtk.join.kgtkmergecolumns import KgtkMergeColumns
from kgtk.value.kgtkvalueoptions import KgtkValueOptions

@attr.s(slots=True, frozen=True)
class KgtkCat():
    input_file_paths: typing.List[Path] = attr.ib()
    output_path: typing.Optional[Path] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Path)))

    # When supplied, rename all output columns.
    output_column_names: typing.Optional[typing.List[str]] = \
        attr.ib(validator=attr.validators.optional(attr.validators.deep_iterable(member_validator=attr.validators.instance_of(str),
                                                                                 iterable_validator=attr.validators.instance_of(list))),
                default=None)

    # When supplied, renames selected colums: old names.
    old_column_names: typing.Optional[typing.List[str]] = \
        attr.ib(validator=attr.validators.optional(attr.validators.deep_iterable(member_validator=attr.validators.instance_of(str),
                                                                                 iterable_validator=attr.validators.instance_of(list))),
                default=None)

    # When supplied, renames selected colums: new names.
    new_column_names: typing.Optional[typing.List[str]] = \
        attr.ib(validator=attr.validators.optional(attr.validators.deep_iterable(member_validator=attr.validators.instance_of(str),
                                                                                 iterable_validator=attr.validators.instance_of(list))),
                default=None)

    # TODO: find working validators:
    reader_options: typing.Optional[KgtkReaderOptions] = attr.ib(default=None)
    # value_options: typing.Optional[KgtkValueOptions] = attr.ib(attr.validators.optional(attr.validators.instance_of(KgtkValueOptions)), default=None)
    value_options: typing.Optional[KgtkValueOptions] = attr.ib(default=None)

    output_format: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None) # TODO: use an enum

    error_file: typing.TextIO = attr.ib(default=sys.stderr)
    verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    very_verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    def process(self):
        kmc: KgtkMergeColumns = KgtkMergeColumns()

        # Is the output file an edge file, a node file, or unknown?
        is_edge_file: bool = False
        is_node_file: bool = False

        krs: typing.List[KgtkReader] = [ ]
        kr: KgtkReader
        idx: int

        if self.verbose:
            print("Opening the %d input files." % len(self.input_file_paths), file=self.error_file, flush=True)

        saw_stdin: bool = False
        input_file_path: Path
        for idx, input_file_path in enumerate(self.input_file_paths):
            if str(input_file_path) == "-":
                if saw_stdin:
                    raise ValueError("Duplicate standard input file %d" % idx + 1)
                else:
                    saw_stdin = False
                if self.verbose:
                    print("Opening file %d: standard input" % idx + 1, file=self.error_file, flush=True)
            else:
                if self.verbose:
                    print("Opening file %d: %s" % (idx + 1, str(input_file_path)), file=self.error_file, flush=True)

            kr = KgtkReader.open(input_file_path,
                                 who="input " + str(idx + 1),
                                 options=self.reader_options,
                                 value_options = self.value_options,
                                 error_file=self.error_file,
                                 verbose=self.verbose,
                                 very_verbose=self.very_verbose,
            )
            krs.append(kr)

            # Unless directed otherwise, do not merge edge files with node
            # files.  If options.mode == KgtkReaderMode.NONE, then neither
            # kr.is_edge_file nor kr.is_node_file will be set and the
            # consistency check will be skipped.
            if kr.is_edge_file:
                if is_node_file:
                    raise ValueError("Cannot merge an edge file to a node file: %s" % input_file_path)
                if is_edge_file == False and self.verbose:
                    print("The output file will be an edge file.", file=self.error_file, flush=True)
                is_edge_file = True
            elif kr.is_node_file:
                if is_edge_file:
                    raise ValueError("Cannot merge a node file to an edge file: %s" % input_file_path)
                if is_node_file == False and self.verbose:
                    print("The output file will be an node file.", file=self.error_file, flush=True)
                is_node_file = True

            if self.verbose or self.very_verbose:
                print("Mapping the %d column names in %s." % (len(kr.column_names), input_file_path), file=self.error_file, flush=True)
            if self.very_verbose:
                print(" ".join(kr.column_names), file=self.error_file, flush=True)
            new_column_names: typing.List[str] =  kmc.merge(kr.column_names)
            if self.very_verbose:
                print(" ".join(new_column_names), file=self.error_file, flush=True)

        if self.verbose or self.very_verbose:
            print("There are %d merged columns." % len(kmc.column_names), file=self.error_file, flush=True)
        if self.very_verbose:
            print(" ".join(self.column_names), file=self.error_file, flush=True)
            
        if self.output_column_names is not None:
            if self.verbose:
                print("There are %d new output column names." % len(self.output_column_names), file=self.error_file, flush=True)
            if len(self.output_column_names) != len(kmc.column_names):
                raise ValueError("There are %d merged columns, but %d output column names." % (len(kmc.column_names), len(self.output_column_names)))

        output_mode: KgtkWriter.Mode = KgtkWriter.Mode.NONE
        if is_edge_file:
            output_mode = KgtkWriter.Mode.EDGE
            if self.verbose:
                print("Opening the output edge file: %s" % str(self.output_path), file=self.error_file, flush=True)
        elif is_node_file:
            output_mode = KgtkWriter.Mode.NODE
            if self.verbose:
                print("Opening the output node file: %s" % str(self.output_path), file=self.error_file, flush=True)
        else:
            if self.verbose:
                print("Opening the output file: %s" % str(self.output_path), file=self.error_file, flush=True)

        ew: KgtkWriter = KgtkWriter.open(kmc.column_names,
                                         self.output_path,
                                         require_all_columns=False,
                                         prohibit_extra_columns=True,
                                         fill_missing_columns=True,
                                         gzip_in_parallel=False,
                                         mode=output_mode,
                                         output_format=self.output_format,
                                         output_column_names=self.output_column_names,
                                         old_column_names=self.old_column_names,
                                         new_column_names=self.new_column_names,
                                         verbose=self.verbose,
                                         very_verbose=self.very_verbose)

        output_data_lines: int = 0
        for idx, kr in enumerate(krs):
            if kr.file_path is None:
                # This shouldn't happen because we constrined all
                # input_file_path elements to be not None.  However,
                # checking here keeps mypy happy.
                #
                # TODO: throw a better exception.
                raise ValueError("Missing file path.")
            input_file_path = kr.file_path
            if self.verbose:
                print("Copying data from file %d: %s" % (idx + 1, input_file_path), file=self.error_file, flush=True)

            shuffle_list: typing.List[int] = ew.build_shuffle_list(kmc.new_column_name_lists[idx])

            input_data_lines: int = 0
            row: typing.List[str]
            for row in kr:
                input_data_lines += 1
                output_data_lines += 1
                ew.write(row, shuffle_list=shuffle_list)

            # Flush the output file so far:
            ew.flush()

            if self.verbose:
                print("Read %d data lines from file %d: %s" % (input_data_lines, idx + 1, input_file_path))
        
        if self.verbose:
            print("Wrote %d lines total from %d files" % (output_data_lines, len(krs)), file=self.error_file, flush=True)

        ew.close()
        
def main():
    """
    Test the KGTK file concatenator.
    """
    parser = ArgumentParser()
    parser.add_argument(dest="input_file_paths", help="The KGTK files to concatenate", type=Path, nargs='+')
    parser.add_argument("-o", "--output-file", dest="output_file_path", help="The KGTK file to write (default=%(default)s)", type=Path, default="-")

    parser.add_argument(      "--output-format", dest="output_format", help="The file format (default=kgtk)", type=str,
                              choices=KgtkWriter.OUTPUT_FORMAT_CHOICES)

    parser.add_argument(      "--output-columns", dest="output_column_names", help="Rename all output columns. (default=%(default)s)", type=str, nargs='+')
    parser.add_argument(      "--old-columns", dest="old_column_names", help="Rename seleted output columns: old names. (default=%(default)s)", type=str, nargs='+')
    parser.add_argument(      "--new-columns", dest="new_column_names", help="Rename seleted output columns: new names. (default=%(default)s)", type=str, nargs='+')

    KgtkReader.add_debug_arguments(parser, expert=True)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, expert=True)
    KgtkValueOptions.add_arguments(parser, expert=True)

    args = parser.parse_args()

    error_file: typing.TextIO = sys.stdout if args.errors_to_stdout else sys.stderr

    # Build the option structures.
    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_args(args)
    value_options: KgtkValueOptions = KgtkValueOptions.from_args(args)

   # Show the final option structures for debugging and documentation.                                                                                             
    if args.show_options:
        input_files: typing.List[str] = [ ]
        input_file: Path
        for input_file in args.input_file_paths:
            input_files.append(str(input_file))
        print("input: %s" % " ".join(input_files), file=error_file, flush=True)
        print("--output-file=%s" % args.output_file_path, file=error_file, flush=True)
        if args.output_format is not None:
            print("--output-format=%s" % args.output_format, file=error_file, flush=True)
        if args.output_column_names is not None:
            print("--output-columns=%s" %" ".join(args.output_column_names), file=error_file, flush=True)
        if args.old_column_names is not None:
            print("--old-columns=%s" %" ".join(args.old_column_names), file=error_file, flush=True)
        if args.new_column_names is not None:
            print("--new-columns=%s" %" ".join(args.new_column_names), file=error_file, flush=True)
        reader_options.show(out=error_file)
        value_options.show(out=error_file)

    kc: KgtkCat = KgtkCat(input_file_paths=args.input_file_paths,
                          output_path=args.output_file_path,
                          output_format=args.output_format,
                          output_column_names=args.output_column_names,
                          old_column_names=args.old_column_names,
                          new_column_names=args.new_column_names,
                          reader_options=reader_options,
                          value_options=value_options,
                          error_file=error_file,
                          verbose=args.verbose,
                          very_verbose=args.very_verbose)

    kc.process()

if __name__ == "__main__":
    main()

