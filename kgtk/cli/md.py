"""
Convert a KGTK file to a GitHub markdown table.

TODO: Need KgtkWriterOptions
"""

from argparse import Namespace, SUPPRESS
from pathlib import Path
import sys
import typing

from kgtk.cli_argparse import KGTKArgumentParser
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
from kgtk.io.kgtkwriter import KgtkWriter
from kgtk.join.kgtkcat import KgtkCat
from kgtk.value.kgtkvalueoptions import KgtkValueOptions

def parser():
    return {
        'help': 'Convert a KGTK file to a GitHub Markdown Table.',
        'description': 'Convert a KGTK input file to a GitHub markdown table on output. ' +
        '\n\nUse this command to filter the output of any KGTK command: ' +
        '\n\nkgtk md ' +
        '\n\nUse it to convert a KGTK file to a GitHub Markdown table in a file: ' +
        '\n\nkgtk md file.tsv ' +
        '\n\nAdditional options are shown in expert help.\nkgtk --expert cat --help'
    }


def add_arguments_extended(parser: KGTKArgumentParser, parsed_shared_args: Namespace):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """

    _expert: bool = parsed_shared_args._expert

    # This helper function makes it easy to suppress options from
    # The help message.  The options are still there, and initialize
    # what they need to initialize.
    def h(msg: str)->str:
        if _expert:
            return msg
        else:
            return SUPPRESS

    parser.add_argument(      "input_file_path", help="The KGTK file to convert to a GitHub markdown table.", type=Path, nargs='?', default=Path("-"))

    parser.add_argument("-o", "--output-file", dest="output_file_path", help="The KGTK file to write (default=%(default)s).", type=Path, default="-")

    parser.add_argument(      "--output-format", dest="output_format", help=h("The file format (default=%(default)s)"), type=str, default="md")

    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, expert=_expert)
    KgtkValueOptions.add_arguments(parser, expert=_expert)

def run(input_file_path: Path,
        output_file_path: Path,
        output_format: str,

        errors_to_stdout: bool = False,
        errors_to_stderr: bool = True,
        show_options: bool = False,
        verbose: bool = False,
        very_verbose: bool = False,

        **kwargs # Whatever KgtkFileOptions and KgtkValueOptions want.
)->int:
    # import modules locally
    from kgtk.exceptions import KGTKException


    # Select where to send error messages, defaulting to stderr.
    error_file: typing.TextIO = sys.stdout if errors_to_stdout else sys.stderr

    # TODO: check that at most one input file is stdin?

    # Build the option structures.
    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs)
    value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)

    # Show the final option structures for debugging and documentation.
    if show_options:
        print("input: %s" % str(input_file_path), file=error_file, flush=True)
        print("--output-file=%s" % str(output_file_path), file=error_file, flush=True)
        reader_options.show(out=error_file)
        value_options.show(out=error_file)
        print("=======", file=error_file, flush=True)

    try:
        kc: KgtkCat = KgtkCat(input_file_paths=[input_file_path],
                              output_path=output_file_path,
                              output_format=output_format,
                              reader_options=reader_options,
                              value_options=value_options,
                              error_file=error_file,
                              verbose=verbose,
                              very_verbose=very_verbose
        )
        
        kc.process()

        return 0

    except SystemExit as e:
        raise KGTKException("Exit requested")
    except Exception as e:
        raise KGTKException(str(e))

