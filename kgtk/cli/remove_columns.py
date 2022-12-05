"""
Remove columns from a KGTK file.
"""
from argparse import Namespace, SUPPRESS
import typing

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles


def parser():
    return {
        'help': 'Remove columns from a KGTK file.',
        'description': 'Remove specific columns from a KGTK file.'
    }


def add_arguments_extended(parser: KGTKArgumentParser, parsed_shared_args: Namespace):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions, KgtkReaderMode
    from kgtk.utils.argparsehelpers import optional_bool
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    _expert: bool = parsed_shared_args._expert

    parser.add_input_file(positional=True)
    parser.add_output_file()

    parser.add_argument('-c', "--columns", action="store", type=str, dest="columns", nargs='+', required=True,
                        help="Columns to remove as a comma- or space-separated strings, e.g., id,docid or id docid")

    parser.add_argument("--split-on-commas", dest="split_on_commas",
                        help="When True, parse the list of columns, splitting on commas. (default=%(default)s).",
                        type=optional_bool, nargs='?', const=True, default=True)

    parser.add_argument("--split-on-spaces", dest="split_on_spaces",
                        help="When True, parse the list of columns, splitting on spaces. (default=%(default)s).",
                        type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument("--strip-spaces", dest="strip_spaces",
                        help="When True, parse the list of columns, stripping whitespace. (default=%(default)s).",
                        type=optional_bool, nargs='?', const=True, default=True)

    parser.add_argument("--all-except", dest="all_except",
                        help="When True, remove all columns except the listed ones. (default=%(default)s).",
                        type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument("--ignore-missing-columns", dest="ignore_missing_columns",
                        help="When True, ignore missing columns. (default=%(default)s).",
                        type=optional_bool, nargs='?', const=True, default=False)

    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser,
                                    mode_options=True,
                                    default_mode=KgtkReaderMode.NONE,
                                    expert=_expert)
    KgtkValueOptions.add_arguments(parser, expert=_expert)


def run(input_file: KGTKFiles,
        output_file: KGTKFiles,

        columns: typing.Optional[typing.List[str]],

        split_on_commas: bool,
        split_on_spaces: bool,
        strip_spaces: bool,

        all_except: bool,
        ignore_missing_columns: bool,

        errors_to_stdout: bool = False,
        errors_to_stderr: bool = True,
        show_options: bool = False,
        verbose: bool = False,
        very_verbose: bool = False,

        **kwargs  # Whatever KgtkFileOptions and KgtkValueOptions want.
        ) -> int:
    # import modules locally
    from pathlib import Path
    import sys

    from kgtk.exceptions import kgtk_exception_auto_handler, KGTKException
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions, KgtkReaderMode
    from kgtk.io.kgtkwriter import KgtkWriter
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions
    from kgtk.utils.remove_columns import RemoveColumns

    input_kgtk_file: Path = KGTKArgumentParser.get_input_file(input_file)
    output_kgtk_file: Path = KGTKArgumentParser.get_output_file(output_file)

    # Select where to send error messages, defaulting to stderr.
    error_file: typing.TextIO = sys.stdout if errors_to_stdout else sys.stderr

    # Build the option structures.
    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs)
    value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)

    try:
        rc = RemoveColumns(input_kgtk_file=input_kgtk_file,
                           output_kgtk_file=output_kgtk_file,
                           columns=columns,
                           split_on_commas=split_on_commas,
                           split_on_spaces=split_on_spaces,
                           strip_spaces=strip_spaces,
                           all_except=all_except,
                           ignore_missing_columns=ignore_missing_columns,
                           reader_options=reader_options,
                           value_options=value_options,
                           error_file=error_file,
                           show_options=show_options,
                           verbose=verbose,
                           very_verbose=very_verbose
                           )
        rc.process()
        return 0

    except Exception as e:
        kgtk_exception_auto_handler(e)
        return 1
