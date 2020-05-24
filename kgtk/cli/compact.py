"""Copy records from the first KGTK file to the output file,
compacting repeated items into | lists.

TODO: Need KgtkWriterOptions
"""

from argparse import Namespace, SUPPRESS
from pathlib import Path
import sys
import typing

from kgtk.cli_argparse import KGTKArgumentParser
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
from kgtk.io.kgtkwriter import KgtkWriter
from kgtk.join.kgtkcompact import KgtkCompact
from kgtk.utils.argparsehelpers import optional_bool
from kgtk.value.kgtkvalueoptions import KgtkValueOptions

def parser():
    return {
        'help': 'Copy a KGTK file compacting | lists.',
        'description': 'Copy a KGTK file, compacting multiple records into | lists. ' +
        '\n\nBy default, the input file is sorted in memory to achieve the ' +
        'grouping necessary for the compaction algorithm. This may cause ' +
        ' memory usage issues for large input files. If the input file has ' +
        'already been sorted (or at least grouped), the `--presorted` ' +
        'option may be used.' +
        '\n\nAdditional options are shown in expert help.\nkgtk --expert compact --help'
    }


def add_arguments_extended(parser: KGTKArgumentParser, parsed_shared_args: Namespace):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """

    _expert: bool = parsed_shared_args._expert

    parser.add_argument(      "input_kgtk_file", nargs="?", type=Path, default="-",
                              help="The KGTK file to filter. May be omitted or '-' for stdin (default=%(default)s).")

    parser.add_argument(      "--columns", dest="key_column_names",
                              help="The key columns to identify records for compaction. " +
                              "(default=id for node files, (node1, label, node2) for edge files).", nargs='+', default=[ ])

    parser.add_argument(      "--presorted", dest="sorted_input",
                              help="Indicate that the input has been presorted (or at least pregrouped) (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument("-o", "--output-file", dest="output_kgtk_file", help="The KGTK file to write (default=%(default)s).", type=Path, default="-")

    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, expert=_expert)
    KgtkValueOptions.add_arguments(parser, expert=_expert)

def run(input_kgtk_file: typing.Optional[Path],
        output_kgtk_file: typing.Optional[Path],
        key_column_names: typing.List[str],
        sorted_input: bool,

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
        print("input: %s" % (str(input_kgtk_file) if input_kgtk_file is not None else "-"), file=error_file)
        print("--columns=%s" % " ".join(key_column_names), file=error_file)
        print("--presorted=%s" % str(args.sorted_input))
        print("--output-file=%s" % (str(output_kgtk_file) if output_kgtk_file is not None else "-"), file=error_file)
        reader_options.show(out=error_file)
        value_options.show(out=error_file)
        print("=======", file=error_file, flush=True)

    try:
        ex: KgtkCompact = KgtkCompact(
            input_file_path=input_kgtk_file,
            key_column_names=key_column_names,
            sorted_input = sorted_input,
            output_file_path=output_kgtk_file,
            reader_options=reader_options,
            value_options=value_options,
            error_file=error_file,
            verbose=verbose,
            very_verbose=very_verbose,
        )
        
        ex.process()

        return 0

    except SystemExit as e:
        raise KGTKException("Exit requested")
    except Exception as e:
        raise KGTKException(str(e))

