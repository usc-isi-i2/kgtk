"""
Reorder KGTK file columns (while copying)

TODO: Need KgtkWriterOptions

TODO: Make --as-columns modify the preceeding --columns such that
--as-columns can be applied selectively.
"""

from argparse import Namespace, SUPPRESS
import typing

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles

REORDER_COLUMNS_COMMAND: str = 'reorder-columns'
SELECT_COLUMNS_COMMAND: str = 'select-columns'


def parser():
    return {
        'aliases': [SELECT_COLUMNS_COMMAND],
        'help': 'Reorder KGTK file columns.',
        'description': 'This command reorders one or more columns in a KGTK file. ' +
                       '\n\nReorder all columns using --columns col1 col2' +
                       '\nReorder selected columns using --columns col1 col2 ... coln-1 coln' +
                       '\nMove a column to the front: --columns col ...' +
                       '\nMove a column to the end: --columns ... col' +
                       '\nExtract named columns, omitting the rest: --columns col1 col2 --trim' +
                       '\nMove a range of columns: --columns coln .. colm ...' +
                       '\nIf no input filename is provided, the default is to read standard input. ' +
                       '\n\nAdditional options are shown in expert help.\nkgtk --expert reorder-columns --help'
    }


def add_arguments_extended(parser: KGTKArgumentParser, parsed_shared_args: Namespace):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """
    # import modules locally
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions, KgtkReaderMode
    from kgtk.utils.argparsehelpers import optional_bool
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    _expert: bool = parsed_shared_args._expert
    _command: str = parsed_shared_args._command

    # This helper function makes it easy to suppress options from
    # The help message.  The options are still there, and initialize
    # what they need to initialize.
    def h(msg: str) -> str:
        if _expert:
            return msg
        else:
            return SUPPRESS

    parser.add_input_file()
    parser.add_output_file()

    parser.add_argument("--output-format", dest="output_format", help=h("The file format (default=kgtk)"), type=str)

    parser.add_argument('-c', "--columns", "--column", dest="column_names_list", required=True, nargs='+',
                        action="append", default=list(),
                        metavar="COLUMN_NAME",
                        help="The list of reordered column names, optionally containing '...' for column names not explicitly mentioned.")

    parser.add_argument("--as", "--as-columns", "--as-column", dest="as_column_names_list", nargs='+', action="append",
                        default=list(),
                        metavar="COLUMN_NAME",
                        help="Replacement column names.")

    parser.add_argument("--trim", dest="omit_remaining_columns",
                        help="If true, omit unmentioned columns. (default=%(default)s).",
                        metavar="True|False",
                        type=optional_bool, nargs='?', const=True, default=(_command == SELECT_COLUMNS_COMMAND))

    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser,
                                    mode_options=True,
                                    default_mode=KgtkReaderMode.NONE,
                                    expert=_expert)
    KgtkValueOptions.add_arguments(parser, expert=_expert)


def run(input_file: KGTKFiles,
        output_file: KGTKFiles,
        output_format: typing.Optional[str],

        column_names_list: typing.List[typing.List[str]],
        as_column_names_list: typing.List[typing.List[str]],

        omit_remaining_columns: bool,

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

    from kgtk.exceptions import KGTKException
    from kgtk.io.kgtkreader import KgtkReaderOptions
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions
    from kgtk.utils.reorder_columns import ReorderColumns

    try:
        # Select where to send error messages, defaulting to stderr.
        error_file: typing.TextIO = sys.stdout if errors_to_stdout else sys.stderr

        input_kgtk_file: Path = KGTKArgumentParser.get_input_file(input_file)
        output_kgtk_file: Path = KGTKArgumentParser.get_output_file(output_file)

        # Build the option structures.
        reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs)
        value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)
        rc = ReorderColumns(input_kgtk_file=input_kgtk_file,
                            output_kgtk_file=output_kgtk_file,
                            output_format=output_format,
                            column_names_list=column_names_list,
                            as_column_names_list=as_column_names_list,
                            omit_remaining_columns=omit_remaining_columns,
                            reader_options=reader_options,
                            value_options=value_options,
                            error_file=error_file,
                            show_options=show_options,
                            verbose=verbose,
                            very_verbose=very_verbose
                            )
        rc.process()
        return 0

    except SystemExit as e:
        raise KGTKException("Exit requested")

    except Exception as e:
        raise KGTKException(str(e))
