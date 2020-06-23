"""Unreify values in a KGTK file.

TODO: Need KgtkWriterOptions
"""

from argparse import _MutuallyExclusiveGroup, Namespace, SUPPRESS
from pathlib import Path
import sys
import typing

from kgtk.kgtkformat import KgtkFormat
from kgtk.cli_argparse import KGTKArgumentParser
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
from kgtk.unreify.kgtkunreifyvalues import KgtkUnreifyValues
from kgtk.utils.argparsehelpers import optional_bool
from kgtk.value.kgtkvalueoptions import KgtkValueOptions

def parser():
    return {
        'help': 'Unreify values in a KGTK file.',
        'description': 'Read a KGTK file, such as might have been created by importing an ntriples file.  ' +
        'Search for reified values and transform them into an unreified form.' +
        '\n\nAn ID column will be added to the output file if not present in the input file.  ' +
        '\n\n--reified-file PATH, if specified, will get a copy of the input records that were ' +
        'identified as reified values. ' +
        '\n\n--uninvolved-file PATH, if specified, will get a copy of the input records that were ' +
        ' identified as not being reified values. ' +
        '\n\n--unreified-file PATH, if specified, will get a copy of the unreified output records, which ' +
        ' will still be written to the main output file.' +
        '\n\nAdditional options are shown in expert help.\nkgtk --expert expand --help'
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

    parser.add_argument("-i", "--input-file", dest="input_kgtk_file",
                        help="The KGTK input file with the reified data. " +
                        "It must have node1, label, and node2 columns, or their aliases. " +
                        "It may have an ID column;  if it does not, one will be appended to the output file. " +
                        "It may not have any additional columns. " +
                        "(default=%(default)s)", type=Path, default="-")

    parser.add_argument("-o", "--output-file", dest="output_kgtk_file",
                        help="The KGTK file to write output records with unreified data. " +
                        "This file may differ in shape from the input file by the addition of an ID column. " +
                        "The records in the output file will not, generally, be in the same order as they appeared in the input file. " +
                        "(default=%(default)s).", type=Path, default="-")
    
    parser.add_argument(      "--reified-file", dest="reified_kgtk_file",
                              help="An optional KGTK output file that will contain only the reified RDF statement output records. (default=%(default)s).",
                              type=Path, default=None)
    
    parser.add_argument(      "--unreified-file", dest="unreified_kgtk_file",
                              help="An optional KGTK output file that will contain only the unreified RDF statement input records. (default=%(default)s).",
                              type=Path, default=None)
    
    parser.add_argument(      "--uninvolved-file", dest="uninvolved_kgtk_file",
                              help="An optional KGTK output file that will contain only the uninvolved input records. (default=%(default)s).",
                              type=Path, default=None)
    
    KgtkUnreifyValues.add_arguments(parser)
    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, expert=_expert)
    KgtkValueOptions.add_arguments(parser)

def run(input_kgtk_file: Path,
        output_kgtk_file: Path,
        reified_kgtk_file: typing.Optional[Path],
        unreified_kgtk_file: typing.Optional[Path],
        uninvolved_kgtk_file: typing.Optional[Path],

        trigger_label_value: str,
        trigger_node2_value: str,
        value_label_value: str,
        old_label_value: str,
        new_label_value: typing.Optional[str],

        allow_multiple_values: bool,
        allow_extra_columns: bool,

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
        print("--input-files %s" % str(input_kgtk_file), file=error_file, flush=True)
        print("--output-file=%s" % str(output_kgtk_file), file=error_file, flush=True)
        if reified_kgtk_file is not None:
            print("--reified-file=%s" % str(reified_kgtk_file), file=error_file, flush=True)
        if unreified_kgtk_file is not None:
            print("--unreified-file=%s" % str(unreified_kgtk_file), file=error_file, flush=True)
        if uninvolved_kgtk_file is not None:
            print("--uninvolved-file=%s" % str(uninvolved_kgtk_file), file=error_file, flush=True)
        
        print("--trigger-label=%s" % trigger_label_value, file=error_file, flush=True)
        print("--trigger-node2=%s" % trigger_node2_value, file=error_file, flush=True)
        print("--value-label=%s" % value_label_value, file=error_file, flush=True)
        print("--old-label=%s" % old_label_value, file=error_file, flush=True)
        if new_label_value is not None:
            print("--new-label=%s" % new_label_value, file=error_file, flush=True)

        print("--allow-multiple-values=%s" % str(allow_multiple_values), file=error_file, flush=True)
        print("--allow-extra-columns=%s" % str(allow_extra_columns), file=error_file, flush=True)

        reader_options.show(out=error_file)
        value_options.show(out=error_file)
        print("=======", file=error_file, flush=True)

    try:
        kuv: KgtkUnreifyValues = KgtkUnreifyValues(
            input_file_path=input_kgtk_file,
            output_file_path=output_kgtk_file,
            reified_file_path=reified_kgtk_file,
            unreified_file_path=unreified_kgtk_file,
            uninvolved_file_path=uninvolved_kgtk_file,

            trigger_label_value=trigger_label_value,
            trigger_node2_value=trigger_node2_value,
            value_label_value=value_label_value,
            old_label_value=old_label_value,
            new_label_value=new_label_value,

            allow_multiple_values=allow_multiple_values,
            allow_extra_columns=allow_extra_columns,

            reader_options=reader_options,
            value_options=value_options,
            error_file=error_file,
            verbose=verbose,
            very_verbose=very_verbose)

        kuv.process()
    
        return 0

    except SystemExit as e:
        raise KGTKException("Exit requested")
    except Exception as e:
        raise KGTKException(str(e))

