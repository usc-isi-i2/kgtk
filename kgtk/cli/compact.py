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
from kgtk.reshape.kgtkcompact import KgtkCompact
from kgtk.reshape.kgtkidbuilder import KgtkIdBuilder, KgtkIdBuilderOptions
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

    # This helper function makes it easy to suppress options from
    # The help message.  The options are still there, and initialize
    # what they need to initialize.
    def h(msg: str)->str:
        if _expert:
            return msg
        else:
            return SUPPRESS

    parser.add_argument(      "input_kgtk_file", nargs="?", type=Path, default="-",
                              help="The KGTK file to filter. May be omitted or '-' for stdin (default=%(default)s).")

    parser.add_argument(      "--columns", dest="key_column_names",
                              help="The key columns to identify records for compaction. " +
                              "(default=id for node files, (node1, label, node2, id) for edge files).", nargs='+', default=[ ])

    parser.add_argument(      "--compact-id", dest="compact_id",
                              help="Indicate that the ID column in KGTK edge files should be compacted. " +
                              "Normally, if the ID column exists, it is not compacted, " +
                              "as there are use cases that need to maintain distinct lists of secondary edges for each ID value. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--presorted", dest="sorted_input",
                              help="Indicate that the input has been presorted (or at least pregrouped) (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--verify-sort", dest="verify_sort",
                              help="If the input has been presorted, verify its consistency (disable if only pregrouped). (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=True)

    parser.add_argument("-o", "--output-file", dest="output_kgtk_file", help="The KGTK file to write (default=%(default)s).", type=Path, default="-")

    parser.add_argument(      "--build-id", dest="build_id",
                              help="Build id values in an id column. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)
    
    KgtkIdBuilderOptions.add_arguments(parser, expert=_expert)
    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, expert=_expert)
    KgtkValueOptions.add_arguments(parser, expert=_expert)

def run(input_kgtk_file: typing.Optional[Path],
        output_kgtk_file: typing.Optional[Path],
        key_column_names: typing.List[str],
        compact_id: bool,
        sorted_input: bool,
        verify_sort: bool,
        build_id: bool,

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
    idbuilder_options: KgtkIdBuilderOptions = KgtkIdBuilderOptions.from_dict(kwargs)
    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs)
    value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)

    # Show the final option structures for debugging and documentation.
    if show_options:
        print("input: %s" % (str(input_kgtk_file) if input_kgtk_file is not None else "-"), file=error_file)
        print("--columns=%s" % " ".join(key_column_names), file=error_file)
        print("--compact-id=%s" % str(compact_id), file=error_file, flush=True)
        print("--presorted=%s" % str(sorted_input))
        print("--verify-sort=%s" % str(verify_sort), file=error_file, flush=True)
        print("--output-file=%s" % (str(output_kgtk_file) if output_kgtk_file is not None else "-"), file=error_file)
        print("--build-id=%s" % str(build_id), file=error_file, flush=True)
        idbuilder_options.show(out=error_file)
        reader_options.show(out=error_file)
        value_options.show(out=error_file)
        print("=======", file=error_file, flush=True)

    try:
        ex: KgtkCompact = KgtkCompact(
            input_file_path=input_kgtk_file,
            key_column_names=key_column_names,
            compact_id=compact_id,
            sorted_input=sorted_input,
            verify_sort=verify_sort,
            output_file_path=output_kgtk_file,
            build_id=build_id,
            idbuilder_options=idbuilder_options,
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

