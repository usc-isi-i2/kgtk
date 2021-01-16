from argparse import ArgumentParser, Namespace
import attr
from pathlib import Path
import sys
import typing

from kgtk.io.kgtkreader import KgtkReader
from kgtk.utils.argparsehelpers import optional_bool

@attr.s(slots=True, frozen=True)
class DocUpdater():
    update_usage: bool = attr.ib(validator=attr.validators.instance_of(bool), default=True)

    error_file: typing.TextIO = attr.ib(default=sys.stderr)
    verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    very_verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
        
    def process(self, md_file: Path):
        if self.verbose:
            print("Processing %s" % repr(str(md_file)), file=self.error_file, flush=True)

def main():
    """
    Update the documentation files.
    """
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument("--md-files", dest="md_files", help="The .md files to be updated.", type=Path, nargs='+')

    parser.add_argument("--update-usage", dest="update_usage", metavar="optional True|False",
                        help="Update the ## Usage section (default=%(default)s).",
                        type=optional_bool, nargs='?', const=True, default=True)
    
    KgtkReader.add_debug_arguments(parser)

    args: Namespace = parser.parse_args()
    error_file: typing.TextIO = sys.stdout if args.errors_to_stdout else sys.stderr

    if args.show_options:
        print("--md-files %s" % " ".join([repr(str(x)) for x in args.md_files]), file=error_file, flush=True)
        print("--update-usage=%s" % repr(args.update_usage), file=error_file, flush=True)
        print("--verbose=%s" % repr(args.verbose), file=error_file, flush=True)
        print("--very-verbose=%s" % repr(args.very_verbose), file=error_file, flush=True)

    du: DocUpdater = DocUpdater(update_usage=args.update_usage,
                                error_file=error_file,
                                verbose=args.verbose,
                                very_verbose=args.very_verbose)

    md_file: Path
    for md_file in args.md_files:
        du.process(md_file)


if __name__ == "__main__":
    main()

