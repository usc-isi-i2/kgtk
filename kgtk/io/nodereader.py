"""
Read a KGTK node file in TSV format.

TODO: Add support for alternative envelope formats, such as JSON.
"""

from argparse import ArgumentParser
import attr
from pathlib import Path
import sys
import typing

from kgtk.io.kgtkreader import KgtkReader, KgtkReaderMode, KgtkReaderOptions
from kgtk.utils.closableiter import ClosableIter
from kgtk.utils.enumnameaction import EnumNameAction
from kgtk.utils.validationaction import ValidationAction
from kgtk.value.kgtkvalueoptions import KgtkValueOptions

@attr.s(slots=True, frozen=False)
class NodeReader(KgtkReader):

    @classmethod
    def open_node_file(cls,
                       file_path: typing.Optional[Path],
                       who: str = "node input",
                       error_file: typing.TextIO = sys.stderr,
                       reject_file: typing.Optional[typing.TextIO] = None,
                       options: typing.Optional[KgtkReaderOptions] = None,
                       value_options: typing.Optional[KgtkValueOptions] = None,
                       verbose: bool = False,
                       very_verbose: bool = False)->"NodeReader":

        result: KgtkReader = cls.open(file_path=file_path,
                                      who=who,
                                      error_file=error_file,
                                      reject_file=reject_file,
                                      mode=KgtkReaderMode.NODE,
                                      options=options,
                                      value_options=value_options,
                                      verbose=verbose,
                                      very_verbose=very_verbose)
        # This doesn't work because the EdgeReader imported inside KgtkReader
        # is a different class than this one!
        #
        # TODO: Fix this.
        #
        #if isinstance(result, cls):
        #    return result
        #else:
        #    # TODO: throw a better exception
        #    raise ValueError("open_node_file expected to produce a NodeReader")
        return typing.cast(NodeReader, result)

    def _ignore_prohibited_lists(self, row: typing.List[str], line: str)->bool:
        # TODO: Should we apply this to the `id` column of a node file for simplicity?
        return False

    def _ignore_if_blank_required_fields(self, values: typing.List[str], line: str)->bool:
        # Ignore line_action with blank id fields.  This code comes after
        # filling missing trailing columns, although it could be reworked
        # to come first.
        if self.options.blank_required_field_line_action != ValidationAction.PASS and self.id_column_idx >= 0 and len(values) > self.id_column_idx:
            id_value: str = values[self.id_column_idx]
            if len(id_value) == 0 or id_value.isspace():
                return self.exclude_line(self.options.blank_required_field_line_action, "id is blank", line)
        return False # Do not ignore this line

    def _skip_reserved_fields(self, column_name)->bool:
        if self.id_column_idx >= 0 and column_name in self.ID_COLUMN_NAMES:
            return True
        return False

def main():
    """
    Test the KGTK node file reader.
    """
    parser = ArgumentParser()
    parser.add_argument(dest="kgtk_file", help="The KGTK edge file to read", type=Path, nargs="?")
    KgtkReader.add_debug_arguments(parser, expert=True)
    KgtkReaderOptions.add_arguments(parser, validate_by_default=True, expert=True)
    KgtkValueOptions.add_arguments(parser, expert=True)
    args = parser.parse_args()

    error_file: typing.TextIO = sys.stdout if args.errors_to_stdout else sys.stderr

    # Build the option structures.
    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_args(args, mode=KgtkReaderMode.NODE)
    value_options: KgtkValueOptions = KgtkValueOptions.from_args(args)

    if args.show_options:
        reader_options.show(out=error_file)
        value_options.show(out=error_file)
        print("=======", file=error_file, flush=True)

    nr: NodeReader = NodeReader.open_node_file(args.kgtk_file,
                                               error_file=error_file,
                                               options=reader_options,
                                               value_options=value_options,
                                               verbose=args.verbose, very_verbose=args.very_verbose)

    line_count: int = 0
    row: typing.List[str]
    for row in nr:
        line_count += 1
    print("Read %d lines" % line_count, file=error_file, flush=True)

if __name__ == "__main__":
    main()

