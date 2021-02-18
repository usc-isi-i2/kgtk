"""Filter a KGTK file based on whether one or more records exist in a second
KGTK file with matching values for one or more fields.

TODO: Need KgtkWriterOptions
"""

from argparse import Namespace, SUPPRESS
import typing

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles

def parser():
    return {
        'help': 'Filter a KGTK file for nonempty fields.',
        'description': 'Filter a KGTK file based on whether one or more fields are not empty. ' +
        'When multiple fields are specified, either any field or all fields must be not empty.' +
        '\n\nAdditional options are shown in expert help.\nkgtk --expert ifnotempty --help'
    }


def add_arguments_extended(parser: KGTKArgumentParser, parsed_shared_args: Namespace):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
    from kgtk.utils.argparsehelpers import optional_bool
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    _expert: bool = parsed_shared_args._expert

    parser.add_input_file(positional=True)
    parser.add_output_file()
    parser.add_output_file(who="The KGTK file for input records that fail the filter.",
                           dest="reject_file",
                           options=["--reject-file"],
                           metavar="REJECT_FILE",
                           optional=True)

    parser.add_argument(      "--columns", dest="filter_column_names",
                              help="The columns in the file being filtered (Required).", nargs='+', required=True)

    parser.add_argument(      "--count", dest="only_count", metavar="True|False",
                              help="Only count the records, do not copy them. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--all", dest="all_are", metavar="True|False",
                              help="False: Test if any are not empty, True: test if all are not empty (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, expert=_expert)
    KgtkValueOptions.add_arguments(parser, expert=_expert)

def run(input_file: KGTKFiles,
        output_file: KGTKFiles,
        reject_file: KGTKFiles,
        filter_column_names: typing.List[str],
        all_are: bool = False,

        only_count: bool = False,

        errors_to_stdout: bool = False,
        errors_to_stderr: bool = True,
        show_options: bool = False,
        verbose: bool = False,
        very_verbose: bool = False,

        **kwargs # Whatever KgtkFileOptions and KgtkValueOptions want.
)->int:
    # import modules locally
    from pathlib import Path
    import sys

    from kgtk.exceptions import KGTKException
    from kgtk.iff.kgtkifempty import KgtkIfEmpty
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
    from kgtk.io.kgtkwriter import KgtkWriter
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    input_kgtk_file: Path = KGTKArgumentParser.get_input_file(input_file)
    output_kgtk_file: Path = KGTKArgumentParser.get_output_file(output_file)
    reject_kgtk_file: typing.Optional[Path] = KGTKArgumentParser.get_optional_output_file(reject_file, who="KGTK reject file")

    # Select where to send error messages, defaulting to stderr.
    error_file: typing.TextIO = sys.stdout if errors_to_stdout else sys.stderr

    # Build the option structures.
    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs)
    value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)

    # Show the final option structures for debugging and documentation.
    if show_options:
        print("--input-file=%s" % str(input_kgtk_file), file=error_file)
        print("--output-file=%s" % str(output_kgtk_file), file=error_file)
        if reject_kgtk_file is not None:
            print("--reject-file=%s" % str(reject_kgtk_file), file=error_file)
        print("--columns=%s" % " ".join(filter_column_names), file=error_file)
        print("--count=%s" % str(only_count), file=error_file)
        print("--all=%s" % str(all_are), file=error_file)
        reader_options.show(out=error_file)
        value_options.show(out=error_file)
        print("=======", file=error_file, flush=True)

    try:
        ie: KgtkIfEmpty = KgtkIfEmpty(
            input_file_path=input_kgtk_file,
            filter_column_names=filter_column_names,
            output_file_path=output_kgtk_file,
            reject_file_path=reject_kgtk_file,
            all_are=all_are,
            notempty=True,
            only_count=only_count,
            reader_options=reader_options,
            value_options=value_options,
            error_file=error_file,
            verbose=verbose,
            very_verbose=very_verbose,
        )
        
        ie.process()

        return 0

    except SystemExit as e:
        raise KGTKException("Exit requested")
    except Exception as e:
        raise KGTKException(str(e))

