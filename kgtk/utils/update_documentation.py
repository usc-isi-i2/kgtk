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

    process_usage: bool = attr.ib(validator=attr.validators.instance_of(bool), default=True)
    update_usage: bool = attr.ib(validator=attr.validators.instance_of(bool), default=True)

    process_examples: bool = attr.ib(validator=attr.validators.instance_of(bool), default=True)
    update_examples: bool = attr.ib(validator=attr.validators.instance_of(bool), default=True)

    error_file: typing.TextIO = attr.ib(default=sys.stderr)
    verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    very_verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
        
    def readlines(self, md_file: Path)->typing.List[str]:
        with open(md_file, "r") as fd:
            return list(fd) # Read all lines.  Each line (except maybe the last) will end with newline.

    def writelines(self, md_file: Path, lines: typing.List[str])->typing.List[str]:
        with open(md_file, "w") as fd:
            fd.writelines(lines)

    def find_section(self, section: str, lines: typing.List[str])->int:
        start_of_section: str = "## " + section
        line_number: int
        line: str
        for line_number, line in enumerate(lines):
            if line.startswith(start_of_section):
                return line_number
        return -1

    def find_block(self,
                   lines: typing.List[str],
                   start_idx: int,
                   stop_at_next_section: bool = True,
                   skip_text: bool = True,
                   )->typing.Tuple[int, int]:
        current_idx: int = start_idx
        begin_idx: int = -1
        while current_idx < len(lines):
            line: str = lines[current_idx]
            if stop_at_next_section and line.startswith("#"):
                if self.very_verbose:
                    print("find_block begin search left the section at index %d" % current_idx, file=self.error_file, flush=True)
                return -1, -1
            if line.startswith("```"):
                current_idx += 1
                begin_idx = current_idx
                break
            if len(line.strip()) < 0 and not skip_text:
                if self.very_verbose:
                    print("find_block begin search found unexpected text at index %d" % current_idx, file=self.error_file, flush=True)
                return -1, -1
            current_idx += 1

        if begin_idx < 0:
            if self.very_verbose:
                print("find_block did not find the beginning of a block.", file=self.error_file, flush=True)
            return -1, -1

        while current_idx < len(lines):
            line: str = lines[current_idx]
            if stop_at_next_section and line.startswith("#"):
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

    def find_table(self,
                   lines: typing.List[str],
                   start_idx: int,
                   stop_at_next_section: bool = False,
                   stop_at_next_block: bool = True,
                   skip_text: bool = False,
                   )->typing.Tuple[int, int]:
        current_idx: int = start_idx
        begin_idx: int = -1
        while current_idx < len(lines):
            line: str = lines[current_idx]
            if stop_at_next_section and line.startswith("#"):
                if self.very_verbose:
                    print("find_table begin search left the section at index %d" % current_idx, file=self.error_file, flush=True)
                return -1, -1
            if stop_at_next_block and line.startswith("```"):
                if self.very_verbose:
                    print("find_table begin search found a block at index %d" % current_idx, file=self.error_file, flush=True)
                return -1, -1
            if line.startswith("|"):
                begin_idx = current_idx
                break
            if len(line.strip()) < 0 and not skip_text:
                if self.very_verbose:
                    print("find_table begin search found unexpected text at index %d" % current_idx, file=self.error_file, flush=True)
                return -1, -1
            current_idx += 1

        if begin_idx < 0:
            if self.very_verbose:
                print("find_table did not find the beginning of a table.", file=self.error_file, flush=True)
            return -1, -1

        while current_idx < len(lines):
            line: str = lines[current_idx]
            if stop_at_next_section and line.startswith("#"):
                if self.very_verbose:
                    print("find_table end search left the section at index %d" % current_idx, file=self.error_file, flush=True)
                return -1, -1
            if not line.startswith("|"):
                if self.very_verbose:
                    print("Table found with contents in slice %d:%d" % (begin_idx, current_idx), file=self.error_file, flush=True)
                return begin_idx, current_idx # Return the slice of the contents of the block.
            current_idx += 1

        if self.very_verbose:
            print("Table found ending the file with contents in slice %d:%d" % (begin_idx, current_idx), file=self.error_file, flush=True)
        return begin_idx, current_idx # Return the slice of the contents of the block.

    def do_usage(self, subcommand: str, lines: typing.List[str]):
        usage_section_idx: int = self.find_section("Usage", lines)
        if usage_section_idx < 0:
            if self.verbose:
                print("No Usage section found." , file=self.error_file, flush=True)
            return
        if self.verbose:
            print("Usage section found at index %d" % usage_section_idx, file=self.error_file, flush=True)

        usage_block_begin: int
        usage_block_end: int
        usage_block_begin, usage_block_end = self.find_block(lines, usage_section_idx + 1)
        if usage_block_begin < 0:
            if self.verbose:
                print("No usage block found.", file=self.error_file, flush=True)
            return
        if self.very_verbose:
            print("Existing usage:\n****************\n%s****************" % "".join(lines[usage_block_begin:usage_block_end]), file=self.error_file, flush=True)

            
        command: str = "%s %s --help" % (self.kgtk_command, subcommand)
        if self.verbose:
            print("Getting new usage for %s" % repr(command), file=self.error_file, flush=True)
        new_usage: typing.List[str] = subprocess.getoutput(command).splitlines(keepends=True)
        nlines: int = len(new_usage)
        if nlines > 0:
                new_usage[nlines-1] = new_usage[nlines-1].rstrip('\n') + '\n'
        if self.very_verbose:
            print("new usage:\n****************\n%s****************" % "".join(new_usage), file=self.error_file, flush=True)

        if self.update_usage:
            # Replace the old usage with the new usage:
            lines[usage_block_begin:usage_block_end] = new_usage

    def do_examples(self, subcommand: str, lines: typing.List[str]):
        examples_section_idx: int = self.find_section("Examples", lines)
        if examples_section_idx < 0:
            if self.verbose:
                print("No Examples section found." , file=self.error_file, flush=True)
            return
        if self.verbose:
            print("Examples section found at index %d" % examples_section_idx, file=self.error_file, flush=True)

        current_idx = examples_section_idx + 1

        table_count: int = 0
        while (True):
            command_block_begin: int
            command_block_end: int
            command_block_begin, command_block_end = self.find_block(lines, current_idx, stop_at_next_section=False)
            if command_block_begin < 0:
                if self.verbose:
                    print ("%d example tables processed" % table_count, file=self.error_file, flush=True)
                return
            if self.very_verbose:
                print("Example command:\n----------\n%s----------" % "".join(lines[command_block_begin:command_block_end]), file=self.error_file, flush=True)
            current_idx = command_block_end + 1

            command: str = "".join(lines[command_block_begin:command_block_end]).strip() + " / md"
            if self.verbose:
                print("Getting new table lines for:\n%s" % command, file=self.error_file, flush=True)
                                   
            new_table_lines: typing.List[str] = subprocess.getoutput(command).splitlines(keepends=True)
            nlines: int = len(new_table_lines)
            if nlines > 0:
                new_table_lines[nlines-1] = new_table_lines[nlines-1].rstrip('\n') + '\n'
            if self.very_verbose:
                print("New table:\n****************\n%s****************" % "".join(new_table_lines), file=self.error_file, flush=True)

            table_begin: int
            table_end: int
            table_begin, table_end = self.find_table(lines, current_idx)
            if table_begin < 0:
                if self.verbose:
                    print ("No table found for example:\n----------\n%s----------" % "".join(lines[command_block_begin:command_block_end]),
                           file=self.error_file, flush=True)
                continue
            table_count += 1

            if self.very_verbose:
                print("Existing table:\n****************\n%s****************" % "".join(lines[table_begin:table_end]), file=self.error_file, flush=True)
            
            if nlines == 0:
                if self.verbose:
                    print("Error fetching new table (no output)", file=self.error_file, flush=True)
                current_idx = table_end
            elif not new_table_lines[0].startswith("|"):
                if self.verbose:
                    print("Error fetching new table:\n%s" % "".join(new_table_lines), file=self.error_file, flush=True)
                current_idx = table_end
            elif self.update_examples:
                # Replace the old example table with the new example table:
                lines[table_begin:table_end] = new_table_lines
                current_idx = table_end + (nlines - (table_end - table_begin))
            else:
                current_idx = table_end

    def process(self, md_file: Path):
        subcommand: str = md_file.stem
        if self.verbose:
            print("Processing %s for %s %s" % (repr(str(md_file)), self.kgtk_command, subcommand), file=self.error_file, flush=True)
        lines: typing.List[str] = self.readlines(md_file)
        if self.verbose:
            print("Read %d lines." % len(lines), file=self.error_file, flush=True)
        if self.very_verbose:
            line_idx: int
            line: str
            print("============================", file=self.error_file, flush=True)
            for line_idx, line in enumerate(lines):
                print("%d: %s" % (line_idx, line.rstrip()), file=self.error_file, flush=True)
            print("============================", file=self.error_file, flush=True)

        if self.process_usage:
            self.do_usage(subcommand, lines)

        if self.process_examples:
            self.do_examples(subcommand, lines)

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

    parser.add_argument("--process-usage", dest="process_usage", metavar="optional True|False",
                        help="Process the ## Usage section (default=%(default)s).",
                        type=optional_bool, nargs='?', const=True, default=True)
    
    parser.add_argument("--update-usage", dest="update_usage", metavar="optional True|False",
                        help="Update the ## Usage section (default=%(default)s).",
                        type=optional_bool, nargs='?', const=True, default=True)
    
    parser.add_argument("--process-examples", dest="process_examples", metavar="optional True|False",
                        help="Process the ## Examples section (default=%(default)s).",
                        type=optional_bool, nargs='?', const=True, default=True)
    
    parser.add_argument("--update-examples", dest="update_examples", metavar="optional True|False",
                        help="Update the ## Examples section (default=%(default)s).",
                        type=optional_bool, nargs='?', const=True, default=True)
    
    KgtkReader.add_debug_arguments(parser)

    args: Namespace = parser.parse_args()
    error_file: typing.TextIO = sys.stdout if args.errors_to_stdout else sys.stderr

    if args.show_options:
        print("--md-files %s" % " ".join([repr(str(x)) for x in args.md_files]), file=error_file, flush=True)
        print("--kgtk-command=%s" % repr(args.kgtk_command), file=error_file, flush=True)
        print("--process-usage=%s" % repr(args.process_usage), file=error_file, flush=True)
        print("--update-usage=%s" % repr(args.update_usage), file=error_file, flush=True)
        print("--process-examples=%s" % repr(args.process_examples), file=error_file, flush=True)
        print("--update-examples=%s" % repr(args.update_examples), file=error_file, flush=True)
        print("--verbose=%s" % repr(args.verbose), file=error_file, flush=True)
        print("--very-verbose=%s" % repr(args.very_verbose), file=error_file, flush=True)

    du: DocUpdater = DocUpdater(kgtk_command=args.kgtk_command,
                                process_usage=args.process_usage,
                                update_usage=args.update_usage,
                                process_examples=args.process_examples,
                                update_examples=args.update_examples,
                                error_file=error_file,
                                verbose=args.verbose,
                                very_verbose=args.very_verbose)

    md_file: Path
    for md_file in args.md_files:
        du.process(md_file)


if __name__ == "__main__":
    main()

