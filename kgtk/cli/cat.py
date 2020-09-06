"""
Concatenate KGTK files.

TODO: Need KgtkWriterOptions
"""

from argparse import Namespace, SUPPRESS
from pathlib import Path
import sys
import typing

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles

def parser():
    return {
        'help': 'Concatenate KGTK files.',
        'description': 'Concatenate two or more KGTK files, merging the columns appropriately. ' +
        'All files must be KGTK edge files or all files must be KGTK node files (unless overridden with --mode=NONE). ' +
        '\n\nAdditional options are shown in expert help.\nkgtk --expert cat --help'
    }


def add_arguments_extended(parser: KGTKArgumentParser, parsed_shared_args: Namespace):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
    from kgtk.io.kgtkwriter import KgtkWriter
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    _expert: bool = parsed_shared_args._expert

    # This helper function makes it easy to suppress options from
    # The help message.  The options are still there, and initialize
    # what they need to initialize.
    def h(msg: str)->str:
        if _expert:
            return msg
        else:
            return SUPPRESS

    parser.add_input_file(who="KGTK input files",
                          dest="input_files",
                          options=["-i", "--input-files"],
                          allow_list=True,
                          positional=True)
    parser.add_output_file()

    parser.add_argument(      "--output-format", dest="output_format", help="The file format (default=kgtk)", type=str,
                              choices=KgtkWriter.OUTPUT_FORMAT_CHOICES)

    parser.add_argument(      "--output-columns", dest="output_column_names",
                              metavar="NEW_COLUMN_NAME",
                              help=h("The list of new column names when renaming all columns."),
                              type=str, nargs='+')
    parser.add_argument(      "--old-columns", dest="old_column_names",
                              metavar="OLD_COLUMN_NAME",
                              help=h("The list of old column names for selective renaming."),
                              type=str, nargs='+')
    parser.add_argument(      "--new-columns", dest="new_column_names",
                              metavar="NEW_COLUMN_NAME",
                              help=h("The list of new column names for selective renaming."),
                              type=str, nargs='+')

    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, expert=_expert)
    KgtkValueOptions.add_arguments(parser, expert=_expert)

def run(input_files: KGTKFiles,
        output_file: KGTKFiles,
        output_format: typing.Optional[str],

        output_column_names: typing.Optional[typing.List[str]],
        old_column_names: typing.Optional[typing.List[str]],
        new_column_names: typing.Optional[typing.List[str]],

        errors_to_stdout: bool = False,
        errors_to_stderr: bool = True,
        show_options: bool = False,
        verbose: bool = False,
        very_verbose: bool = False,

        **kwargs # Whatever KgtkFileOptions and KgtkValueOptions want.
)->int:
    # import modules locally
    from kgtk.exceptions import KGTKException

    from kgtk.join.kgtkcat import KgtkCat
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
    from kgtk.io.kgtkwriter import KgtkWriter
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions
    
    input_file_paths: typing.List[Path] = KGTKArgumentParser.get_input_file_list(input_files)
    output_file_path: Path = KGTKArgumentParser.get_output_file(output_file)
    
    # Select where to send error messages, defaulting to stderr.
    error_file: typing.TextIO = sys.stdout if errors_to_stdout else sys.stderr

    # print("cat running", file=error_file, flush=True) # ***

    # TODO: check that at most one input file is stdin?

    # Build the option structures.
    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs)
    value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)

    # Show the final option structures for debugging and documentation.
    if show_options:
        print("--input-files %s" % " ".join((str(input_file_path) for input_file_path in input_file_paths)), file=error_file, flush=True)
        print("--output-file=%s" % str(output_file_path), file=error_file, flush=True)
        if output_format is not None:
            print("--output-format=%s" % output_format, file=error_file, flush=True)
        if output_column_names is not None:
            print("--output-coloumns %s" % " ".join(output_column_names), file=error_file, flush=True)
        if old_column_names is not None:
            print("--old-columns %s" % " ".join(old_column_names), file=error_file, flush=True)
        if new_column_names is not None:
            print("--new-columns %s" % " ".join(new_column_names), file=error_file, flush=True)
        reader_options.show(out=error_file)
        value_options.show(out=error_file)
        print("=======", file=error_file, flush=True)

    # Check for comsistent options.  argparse doesn't support this yet.
    if output_column_names is not None and len(output_column_names) > 0:
        if (old_column_names is not None and len(old_column_names) > 0) or \
           (new_column_names is not None and len(new_column_names) > 0):
            raise KGTKException("When --output-columns is used, --old-columns and --new-columns may not be used.")
    elif (old_column_names is not None and len(old_column_names) > 0) ^ \
         (new_column_names is not None and len(new_column_names) > 0):
        raise KGTKException("Both --old-columns and --new-columns must be used when either is used.")

    elif (old_column_names is not None and len(old_column_names) > 0) and \
         (new_column_names is not None and len(new_column_names) > 0):
        if len(old_column_names) != len(new_column_names):
            raise KGTKException("Both --old-columns and --new-columns must have the same number of columns.")
    try:
        kc: KgtkCat = KgtkCat(input_file_paths=input_file_paths,
                              output_path=output_file_path,
                              output_format=output_format,
                              output_column_names=output_column_names,
                              old_column_names=old_column_names,
                              new_column_names=new_column_names,
                              reader_options=reader_options,
                              value_options=value_options,
                              error_file=error_file,
                              verbose=verbose,
                              very_verbose=very_verbose
        )
        
        kc.process()

        # print("cat done", file=error_file, flush=True) # ***
        return 0

    except SystemExit as e:
        raise KGTKException("Exit requested")
    except Exception as e:
        raise KGTKException(str(e))

