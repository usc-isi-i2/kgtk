"""
Cat multuple KGTK file together.

TODO: Need output file mode.

"""

from argparse import ArgumentParser
import attr
import os
from pathlib import Path
import sh  # type: ignore
import sys
import typing

from kgtk.cli_entry import progress_startup
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
from kgtk.io.kgtkwriter import KgtkWriter
from kgtk.join.kgtkmergecolumns import KgtkMergeColumns
from kgtk.value.kgtkvalueoptions import KgtkValueOptions

@attr.s(slots=True, frozen=True)
class KgtkCat():
    DEFAULT_PURE_PYTHON: bool = False
    DEFAULT_FAST_COPY_MIN_SIZE: int = 10000
    DEFAULT_BASH_COMMAND: str = "bash"
    DEFAULT_BZIP2_COMMAND: str = "bzip2"
    DEFAULT_CAT_COMMAND: str = "cat"
    DEFAULT_GZIP_COMMAND: str = "gzip"
    DEFAULT_TAIL_COMMAND: str = "tail"
    DEFAULT_XZ_COMMAND: str = "xz"

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

    no_output_header: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    pure_python: bool = attr.ib(validator=attr.validators.instance_of(bool), default=DEFAULT_PURE_PYTHON)
    fast_copy_min_size: int = attr.ib(validator=attr.validators.instance_of(int), default=DEFAULT_FAST_COPY_MIN_SIZE)

    bash_command: str = attr.ib(validator=attr.validators.instance_of(str), default=DEFAULT_BASH_COMMAND)
    bzip2_command: str = attr.ib(validator=attr.validators.instance_of(str), default=DEFAULT_BZIP2_COMMAND)
    cat_command: str = attr.ib(validator=attr.validators.instance_of(str), default=DEFAULT_CAT_COMMAND)
    gzip_command: str = attr.ib(validator=attr.validators.instance_of(str), default=DEFAULT_GZIP_COMMAND)
    tail_command: str = attr.ib(validator=attr.validators.instance_of(str), default=DEFAULT_TAIL_COMMAND)
    xz_command: str = attr.ib(validator=attr.validators.instance_of(str), default=DEFAULT_XZ_COMMAND)

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
            print("Starting kgtkcat pid=%d" % (os.getpid()), file=self.error_file, flush=True)

        if self.verbose:
            print("Opening the %d input files." % len(self.input_file_paths), file=self.error_file, flush=True)

        use_system_copy: bool = not self.pure_python
        if self.output_format is not None and self.output_format != KgtkWriter.OUTPUT_FORMAT_KGTK:
            # TODO: OK if the input and output formats are both CSV with headers.
            use_system_copy = False
        initial_column_names: typing.Optional[typing.List[str]] = None

        saw_stdin: bool = False
        input_file_path: Path
        for idx, input_file_path in enumerate(self.input_file_paths):
            if str(input_file_path) == "-":
                if saw_stdin:
                    raise ValueError("Duplicate standard input file %d" % (idx + 1))
                else:
                    saw_stdin = False
                if self.verbose:
                    print("Opening file %d: standard input" % (idx + 1), file=self.error_file, flush=True)
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
                    # Close the open files before raising the exception.
                    #
                    # TODO: Use a try..finally block to ensure these files are closed.
                    for kr2 in krs:
                        kr2.close()
                    raise ValueError("Cannot merge an edge file to a node file: %s" % input_file_path)
                if is_edge_file == False and self.verbose:
                    print("The output file will be an edge file.", file=self.error_file, flush=True)
                is_edge_file = True
            elif kr.is_node_file:
                if is_edge_file:
                    # Close the open files before raising the exception.
                    #
                    # TODO: Use a try..finally block to ensure these files are closed.
                    for kr2 in krs:
                        kr2.close()
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

            # Can we still use the system copy?
            if not kr.use_fast_path:
                use_system_copy = False
            if kr.options.force_column_names is not None:
                use_system_copy = False
            if kr.options.supply_missing_column_names:
                use_system_copy = False
            if kr.options.no_input_header:
                use_system_copy = False
            if kr.options.number_of_columns is not None:
                use_system_copy = False
            if kr.options.require_column_names is not None:
                # This constraint could be removed.
                use_system_copy = False
            if kr.options.no_additional_columns:
                # This constraint could be removed.
                use_system_copy = False
            if not kr.rewindable:
                use_system_copy = False
            if initial_column_names is None:
                initial_column_names = kr.column_names.copy()
            else:
                # TODO: Account for coumn name aliases.
                if initial_column_names != kr.column_names:
                    use_system_copy = False

        if self.verbose or self.very_verbose:
            print("There are %d merged columns." % len(kmc.column_names), file=self.error_file, flush=True)
        if self.very_verbose:
            print(" ".join(kmc.column_names), file=self.error_file, flush=True)
            
        if self.output_column_names is not None:
            if self.verbose:
                print("There are %d new output column names." % len(self.output_column_names), file=self.error_file, flush=True)
            if len(self.output_column_names) != len(kmc.column_names):
                # Close the open files before raising the exception.
                #
                # TODO: Use a try..finally block to ensure these files are closed.
                for kr2 in krs:
                    kr2.close()
                raise ValueError("There are %d merged columns, but %d output column names." % (len(kmc.column_names), len(self.output_column_names)))

        if use_system_copy:
            # TODO: restructure this code for better readability.
            if self.verbose:
                print("Using the system commands for fast copies.", file=self.error_file, flush=True)
            copied_column_names: typing.List[str] = initial_column_names
            if self.output_column_names is not None:
                copied_column_names = self.output_column_names
            if self.do_system_copy(krs, copied_column_names):
                return
        progress_startup()

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
                                         use_mgzip=self.reader_options.use_mgzip, # Hack!
                                         mgzip_threads=self.reader_options.mgzip_threads, # Hack!
                                         gzip_in_parallel=False,
                                         mode=output_mode,
                                         output_format=self.output_format,
                                         output_column_names=self.output_column_names,
                                         old_column_names=self.old_column_names,
                                         new_column_names=self.new_column_names,
                                         no_header=self.no_output_header,
                                         error_file=self.error_file,
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
                #
                # Close the open files before raising the exception.
                #
                # TODO: Use a try..finally block to ensure these files are closed.
                for kr2 in krs:
                    kr2.close()
                raise ValueError("Missing file path.")
            input_file_path = kr.file_path
            if self.verbose:
                print("Copying data from file %d: %s" % (idx + 1, input_file_path), file=self.error_file, flush=True)

            input_data_lines: int = ew.copyfile(kr, new_column_names=kmc.new_column_name_lists[idx])
            output_data_lines += input_data_lines

            if self.verbose:
                print("Read %d data lines from file %d: %s" % (input_data_lines, idx + 1, input_file_path), file=self.error_file, flush=True)
        
        if self.verbose:
            print("Wrote %d lines total from %d files" % (output_data_lines, len(krs)), file=self.error_file, flush=True)

        # Close the open files.
        ew.close()
        for kr2 in krs:
            kr2.close()

    def safe_filename(self, file_path: Path) -> str:
        """Convert a path into a quoted and escaped filename that is safe for bash."""
        filename: str = str(file_path)
        if filename.startswith('-') and filename != '-':
            # Prevent filenames that begin with dash from being treated as
            # command options.  Strictly speaking, this is not a bash problem
            # per se.
            filename = './' + filename
        return "'" + filename.replace("'", "'\\''") + "'"

    def do_system_copy(self,
                       krs: typing.List[KgtkReader],
                       column_names: typing.List[str]) -> bool:

        # TODO: Support numbered FDs as input files.
        input_file_path: str
        for input_file_path in self.input_file_paths:
            filename: str = str(input_file_path)
            if filename.startswith("<"):
                if verbose:
                    print(("Cannot use numbered FDs with system tools yet (%s)."
                           % repr(filename)),
                          file=self.error_file, flush=True)
                return False

        # Sum the the sizes of the input files.  Skip the fast copy if
        # the total size is too small.
        total_input_file_size: int = 0
        for input_file_path in self.input_file_paths:
            total_input_file_size += input_file_path.stat().st_size
        if total_input_file_size < self.fast_copy_min_size:
            if self.verbose:
                print(("The total file size (%d) is less than the minimum "
                       + "for fast copies (%d).") % (total_input_file_size,
                                                     self.fast_copy_min_size),
                      file=self.error_file, flush=True)
            return False  # Take the slow path.
        if self.verbose:
            print(("The total file size (%d) meets the minimum "
                   + "for fast copies (%d).") % (total_input_file_size,
                                                 self.fast_copy_min_size),
                  file=self.error_file, flush=True)

        # Close the open files.
        for kr2 in krs:
            kr2.close()

        cmd: str = "("

        idx: int
        for idx, input_file_path in enumerate(self.input_file_paths):
            input_suffix: str = input_file_path.suffix.lower()
            if idx == 0:
                if input_suffix in [".gz", ".z"]:
                    cmd += " " + self.gzip_command + " --decompress --stdout "
                elif input_suffix in [".bz2", ".bz"]:
                    cmd += " " + self.bzip2_command + " --decompress --stdout "
                elif input_suffix in [".xz", ".lzma"]:
                    cmd += " " + self.xz_command + " --decompress --stdout "
                else:
                    cmd += " " + self.cat_command + " "

                cmd += self.safe_filename(input_file_path)

            else:
                cmd += " && "
                if input_suffix in [".gz", ".z"]:
                    cmd += (self.gzip_command + " --decompress --stdout "
                            + self.safe_filename(input_file_path)
                            + " | " + self.tail_command + " -n +2")
                elif input_suffix in [".bz2", ".bz"]:
                    cmd += (self.bzip2_command + " --decompress --stdout "
                            + self.safe_filename(input_file_path)
                            + " | " + self.tail_command + " -n +2")
                elif input_suffix in [".xz", ".lzma"]:
                    cmd += (self.xz_command + " --decompress --stdout "
                            + self.safe_filename(input_file_path)
                            + " | " + self.tail_command + " -n +2")
                else:
                    cmd += self.tail_command + " -n +2 " + self.safe_filename(input_file_path)

        cmd += " )"
        if self.output_path is not None and str(self.output_path) != "-":
            output_suffix: str = self.output_path.suffix.lower()
            if input_suffix in [".gz", ".z"]:
                cmd += " | " + self.gzip_command
            elif input_suffix in [".bz2", ".bz"]:
                cmd += " | " + self.bzip2_command
            elif input_suffix in [".xz", ".lzma"]:
                cmd += " | " + self.xz_command

            cmd += " "
            if str(self.output_path).startswith(">"):
                cmd += str(self.output_path)
            else:
                cmd += '>' + self.safe_filename(self.output_path)

        if self.verbose:
            print("system command: %s" % repr(cmd), file=self.error_file, flush=True)

        sh_bash = sh.Command(self.bash_command)
        cmd_proc = sh_bash("-c", cmd, _out=sys.stdout, _err=sys.stderr,
                           bg=True, _bg_exc=False, _internal_bufsize=1)

        if self.verbose:
            print("\nRunning the cat script (pid=%d)." % cmd_proc.pid, file=self.error_file, flush=True)
        progress_startup(pid=cmd_proc.pid)

        if self.verbose:
            print("\nWaiting for the cat command to complete.\n", file=self.error_file, flush=True)
        cmd_proc.wait()

        return True

        
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

