"""Lift

TODO: Need KgtkWriterOptions
"""

from argparse import Namespace, SUPPRESS
from pathlib import Path
import sys
import typing

from kgtk.cli_argparse import KGTKArgumentParser
from kgtk.lift.kgtklift import KgtkLift
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
from kgtk.io.kgtkwriter import KgtkWriter
from kgtk.utils.argparsehelpers import optional_bool
from kgtk.value.kgtkvalueoptions import KgtkValueOptions

def parser():
    return {
        'help': 'Lift labels from a KGTK file.',
        'description': 'Lift labels for a KGTK file. ' +
        '\n\nAdditional options are shown in expert help.\nkgtk --expert ifempty --help'
    }


def add_arguments_extended(parser: KGTKArgumentParser, parsed_shared_args: Namespace):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """

    _expert: bool = parsed_shared_args._expert

    parser.add_argument(      "input_kgtk_file", nargs="?", help="The KGTK file to lift. May be omitted or '-' for stdin.", type=Path, default="-")

    parser.add_argument(      "--label-value", dest="label_column_value", help="The value in the label column. (default=%(default)s).", default="label")
    parser.add_argument(      "--lift-suffix", dest="lifted_column_suffix", help="The value in the label column. (default=%(default)s).", default=";label")

    parser.add_argument(      "--columns-to-lift", dest="lift_column_names", help="The columns to lift. (default=[node1, label, node2]).", nargs='*')

    parser.add_argument("-o", "--output-file", dest="output_kgtk_file", help="The KGTK file to write (default=%(default)s).", type=Path, default="-")

    parser.add_argument(      "--suppress-empty-columns", dest="suppress_empty_columns", help="If trye, suppress empty columns (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, expert=_expert)
    KgtkValueOptions.add_arguments(parser, expert=_expert)

def run(input_kgtk_file: Path,
        output_kgtk_file: Path,
        label_column_value: str,
        lifted_column_suffix: str,
        lift_column_names: typing.List[str],
        suppress_empty_columns: bool = False,

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

    # Build the option structures.
    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs)
    value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)

    # Show the final option structures for debugging and documentation.
    if show_options:
        print("input: %s" % str(input_kgtk_file), file=error_file, flush=True)
        print("--label-value=%s" % label_column_value, file=error_file, flush=True)
        print("--lift-suffix=%s" % lifted_column_suffix, file=error_file, flush=True)
        if lift_column_names is not None and len(lift_column_names) > 0:
            print("--columns-to-lift %s" % " ".join(lift_column_names), file=error_file, flush=True)
        print("--output-file=%s" % str(output_kgtk_file), file=error_file, flush=True)
        print("--suppress-empty-columns=%s" % str(suppress_empty_columns))
        reader_options.show(out=error_file)
        value_options.show(out=error_file)
        print("=======", file=error_file, flush=True)

    try:
        kl: KgtkLift = KgtkLift(
            input_file_path=input_kgtk_file,
            label_column_value=label_column_value,
            lifted_column_suffix=lifted_column_suffix,
            lift_column_names=lift_column_names,
            output_file_path=output_kgtk_file,
            suppress_empty_columns=suppress_empty_columns,
            reader_options=reader_options,
            value_options=value_options,
            error_file=error_file,
            verbose=verbose,
            very_verbose=very_verbose,
        )
        
        kl.process()

        return 0

    except SystemExit as e:
        raise KGTKException("Exit requested")
    except Exception as e:
        raise KGTKException(str(e))

