"""
Normalize a KGTK node file by creating an edge file with a row for each column value.
"""
from argparse import Namespace, SUPPRESS
from pathlib import Path
import sys
import typing

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles
from kgtk.kgtkformat import KgtkFormat
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions, KgtkReaderMode
from kgtk.io.kgtkwriter import KgtkWriter
from kgtk.utils.argparsehelpers import optional_bool
from kgtk.value.kgtkvalueoptions import KgtkValueOptions

def parser():
    return {
        'help': 'Normalize a KGTK node file into a KGTK edge file.',
        'description': 'Normalize a KGTK node file into a KGTK edge file with a row for each column value in the input file.'
    }


def add_arguments_extended(parser: KGTKArgumentParser, parsed_shared_args: Namespace):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """

    _expert: bool = parsed_shared_args._expert

    parser.add_input_file(positional=True)
    parser.add_output_file()

    parser.add_argument('-c', "--columns", action="store", type=str, dest="columns", nargs='+',
                        help="Columns to remove as a space-separated list. (default=all columns except id)")

    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, default_mode=KgtkReaderMode.NODE, expert=_expert)
    KgtkValueOptions.add_arguments(parser, expert=_expert)

def run(input_file: KGTKFiles,
        output_file: KGTKFiles,

        columns: typing.Optional[typing.List[str]] = None,

        errors_to_stdout: bool = False,
        errors_to_stderr: bool = True,
        show_options: bool = False,
        verbose: bool = False,
        very_verbose: bool = False,

        **kwargs # Whatever KgtkFileOptions and KgtkValueOptions want.
)->int:
    # import modules locally
    from kgtk.exceptions import kgtk_exception_auto_handler, KGTKException

    input_kgtk_file: Path = KGTKArgumentParser.get_input_file(input_file)
    output_kgtk_file: Path = KGTKArgumentParser.get_output_file(output_file)

    # Select where to send error messages, defaulting to stderr.
    error_file: typing.TextIO = sys.stdout if errors_to_stdout else sys.stderr

    # Build the option structures.
    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs)
    value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)

    # Show the final option structures for debugging and documentation.
    if show_options:
        print("--input-file=%s" % str(input_kgtk_file), file=error_file)
        print("--output-file=%s" % str(output_kgtk_file), file=error_file)

        if columns is not None:
            print("--columns=%s" % " ".join(columns), file=error_file)

        reader_options.show(out=error_file)
        value_options.show(out=error_file)
        print("=======", file=error_file, flush=True)

    try:
        if verbose:
            print("Opening the input file: %s" % str(input_kgtk_file), file=error_file, flush=True)
        kr: KgtkReader = KgtkReader.open(input_kgtk_file,
                                         options=reader_options,
                                         value_options = value_options,
                                         error_file=error_file,
                                         verbose=verbose,
                                         very_verbose=very_verbose,
        )

        output_column_names: typing.List[str] = [ KgtkFormat.NODE1, KgtkFormat.LABEL, KgtkFormat.NODE2 ]

        if verbose:
            print("Opening the output file: %s" % str(output_kgtk_file), file=error_file, flush=True)
        kw: KgtkWriter = KgtkWriter.open(output_column_names,
                                         output_kgtk_file,
                                         mode=KgtkWriter.Mode.EDGE,
                                         verbose=verbose,
                                         very_verbose=very_verbose)

        shuffle_list: typing.List[int] = kw.build_shuffle_list(kr.column_names)

        input_line_count: int = 0
        output_line_count: int = 0
        row: typing.List[str]
        for row in kr:
            input_line_count += 1

            node1_value: str = row[kr.id_column_idx]

            column_idx: int
            column_name: str
            for column_idx, column_name in enumerate(kr.column_names):
                if column_idx == kr.id_column_idx:
                    continue
                if columns is not None and column_name not in columns:
                    continue

                node2_value: str = row[column_idx]
                if len(node2_value) == 0:
                    continue

                output_row: typing.List[str] = [ node1_value , column_name, node2_value ]
            
                kw.write(output_row)
                output_line_count += 1

        if verbose:
            print("Read %d node rows, wrote %d edge rows." % (input_line_count, output_line_count), file=error_file, flush=True)

        kw.close()

        return 0

    except Exception as e:
        kgtk_exception_auto_handler(e)
        return 1
