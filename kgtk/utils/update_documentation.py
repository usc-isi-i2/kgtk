from argparse import ArgumentParser, Namespace
import attr
from pathlib import Path
import subprocess
import sys
import typing

from kgtk.io.kgtkreader import KgtkReader
from kgtk.utils.argparsehelpers import optional_bool

@attr.s(slots=True, frozen=True)
class DocUpdater():
    kgtk_command: bool = attr.ib(validator=attr.validators.instance_of(str), default="kgtk")
    update_usage: bool = attr.ib(validator=attr.validators.instance_of(bool), default=True)

    error_file: typing.TextIO = attr.ib(default=sys.stderr)
    verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    very_verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
        
    def readlines(self, md_file: Path)->typing.List[str]:
        with open(md_file, "r") as fd:
            return list(fd) # Read all lines.  Each line (except maybe the last) will end with newline.

    def writelines(self, md_file: Path, lines: typing.List[str])->typing.List[str]:
        with open(md_file, "w") as fd:
            fd.writelines(lines)

    def find_usage(self, lines: typing.List[str])->int:
        line_number: int
        line: str
        for line_number, line in enumerate(lines):
            if line.startswith("## Usage"):
                return line_number
        return -1

    def find_block(self, lines: typing.List[str], start_idx: int)->typing.Tuple[int, int]:
        current_idx: int = start_idx + 1
        begin_idx: int = -1
        while current_idx < len(lines):
            line: str = lines[current_idx]
            if line.startswith("#"):
                if self.very_verbose:
                    print("find_block begin search left the section at index %d" % current_idx, file=self.error_file, flush=True)
                return -1, -1
            current_idx += 1
            if line.startswith("```"):
                begin_idx = current_idx
                break

        if begin_idx < 0:
            if self.very_verbose:
                print("find_block did not find the beginning of a block.", file=self.error_file, flush=True)
            return -1, -1

        while current_idx < len(lines):
            line: str = lines[current_idx]
            if line.startswith("#"):
                if self.very_verbose:
                    print("find_block end search left the section at index %d" % current_idx, file=self.error_file, flush=True)
                return -1, -1
            if line.startswith("```"):
                if self.very_verbose:
                    print("Block found with contents in slice %d:%d" % (begin_idx, current_idx), file=self.error_file, flush=True)
                return begin_idx, current_idx # Return the slice of the contents of the block.
            current_idx += 1
        if self.very_verbose:
            print("find_block did not find the end of a block that began at index %d." % begin_idx, file=self.error_file, flush=True)
        return -1, -1


    def process_usage(self, subcommand: str, lines: typing.List[str]):
        if not self.update_usage:
            return

        usage_idx: int = self.find_usage(lines)
        if usage_idx < 0:
            if self.verbose:
                print("No Usage section found." , file=self.error_file, flush=True)
            return
        if self.verbose:
            print("Usage section found at index %d" % usage_idx, file=self.error_file, flush=True)

        usage_begin: int
        usage_end: int
        usage_begin, usage_end = self.find_block(lines, usage_idx)
        if usage_begin < 0:
            if self.verbose:
                print("No usage block found.", file=self.error_file, flush=True)
            return

        if self.very_verbose:
            print("Existing usage:\n%s\n" % "".join(lines[usage_begin:usage_end]), file=self.error_file, flush=True)

            
        command: str = "%s %s --help" % (self.kgtk_command, subcommand)
        if self.verbose:
            print("Getting new usage for %s" % repr(command), file=self.error_file, flush=True)
        new_usage: typing.List[str] = subprocess.getoutput(command).splitlines(keepends=True)
        if self.very_verbose:
            print("new usage:\n%s" % "".join(new_usage), file=self.error_file, flush=True)

        # Replace the old usage with the new usage:
        lines[usage_begin:usage_end] = new_usage

    def process(self, md_file: Path):
        subcommand: str = md_file.stem
        if self.verbose:
            print("Processing %s for %s %s" % (repr(str(md_file)), self.kgtk_command, subcommand), file=self.error_file, flush=True)
        lines: typing.List[str] = self.readlines(md_file)
        if self.verbose:
            print("Read %d lines." % len(lines), file=self.error_file, flush=True)

        if self.update_usage:
            self.process_usage(subcommand, lines)

        if self.verbose:
            print("Writing %d lines" % len(lines), file=self.error_file, flush=True)
        self.writelines(md_file, lines)

def main():
    """
    Update the documentation files.
    """
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument("--md-files", dest="md_files", help="The .md files to be updated.", type=Path, nargs='+')

    parser.add_argument("--kgtk-command", dest="kgtk_command", help="The kgtk command (default %(default)s.", type=str, default="kgtk")

    parser.add_argument("--update-usage", dest="update_usage", metavar="optional True|False",
                        help="Update the ## Usage section (default=%(default)s).",
                        type=optional_bool, nargs='?', const=True, default=True)
    
    KgtkReader.add_debug_arguments(parser)

    args: Namespace = parser.parse_args()
    error_file: typing.TextIO = sys.stdout if args.errors_to_stdout else sys.stderr

    if args.show_options:
        print("--md-files %s" % " ".join([repr(str(x)) for x in args.md_files]), file=error_file, flush=True)
        print("--kgtk-command=%s" % repr(args.kgtk_command), file=error_file, flush=True)
        print("--update-usage=%s" % repr(args.update_usage), file=error_file, flush=True)
        print("--verbose=%s" % repr(args.verbose), file=error_file, flush=True)
        print("--very-verbose=%s" % repr(args.very_verbose), file=error_file, flush=True)

    du: DocUpdater = DocUpdater(kgtk_command=args.kgtk_command,
                                update_usage=args.update_usage,
                                error_file=error_file,
                                verbose=args.verbose,
                                very_verbose=args.very_verbose)

    md_file: Path
    for md_file in args.md_files:
        du.process(md_file)


if __name__ == "__main__":
    main()

