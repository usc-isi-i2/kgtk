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
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderMode, KgtkReaderOptions
    from kgtk.io.kgtkwriter import KgtkWriter
    from kgtk.join.kgtkcat import KgtkCat
    from kgtk.utils.argparsehelpers import optional_bool
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

    parser.add_argument("--output-format", dest="output_format", help="The file format (default=kgtk)", type=str,
                        choices=KgtkWriter.OUTPUT_FORMAT_CHOICES)

    parser.add_argument("--output-columns", dest="output_column_names",
                        metavar="NEW_COLUMN_NAME",
                        help=h("The list of new column names when renaming all columns."),
                        type=str, nargs='+')
    parser.add_argument("--old-columns", dest="old_column_names",
                        metavar="OLD_COLUMN_NAME",
                        help=h("The list of old column names for selective renaming."),
                        type=str, nargs='+')
    parser.add_argument("--new-columns", dest="new_column_names",
                        metavar="NEW_COLUMN_NAME",
                        help=h("The list of new column names for selective renaming."),
                        type=str, nargs='+')

    parser.add_argument("--no-output-header", dest="no_output_header", metavar="True|False",
                        help=h("When true, do not write a header to the output file (default=%(default)s)."),
                        type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument('--pure-python', dest='pure_python', metavar="True|False",
                        help="When True, use Python code. (default=%(default)s)",
                        type=optional_bool, nargs='?', const=True, default=KgtkCat.DEFAULT_PURE_PYTHON)

    parser.add_argument('--fast-copy-min-size', dest='fast_copy_min_size', type=int,
                        default=KgtkCat.DEFAULT_FAST_COPY_MIN_SIZE,
                        help='The minium number of bytes before using OS tools for fast copy (default=%(default)d).')

    parser.add_argument('--bash-command', dest='bash_command', type=str, default=KgtkCat.DEFAULT_BASH_COMMAND,
                        help=h("The bash command or its substitute. (default=%(default)s)"))

    parser.add_argument('--bzip2-command', dest='bzip2_command', type=str, default=KgtkCat.DEFAULT_BZIP2_COMMAND,
                        help=h("The bzip2 command or its substitute. (default=%(default)s)"))

    parser.add_argument('--cat-command', dest='cat_command', type=str, default=KgtkCat.DEFAULT_CAT_COMMAND,
                        help=h("The cat command or its substitute. (default=%(default)s)"))

    parser.add_argument('--gzip-command', dest='gzip_command', type=str, default=KgtkCat.DEFAULT_GZIP_COMMAND,
                        help=h("The gzip command or its substitute. (default=%(default)s)"))

    parser.add_argument('--tail-command', dest='tail_command', type=str, default=KgtkCat.DEFAULT_TAIL_COMMAND,
                        help=h("The tail command or its substitute. (default=%(default)s)"))

    parser.add_argument('--xz-command', dest='xz_command', type=str, default=KgtkCat.DEFAULT_XZ_COMMAND,
                        help=h("The xz command or its substitute. (default=%(default)s)"))

    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser,
                                    mode_options=True,
                                    default_mode=KgtkReaderMode[parsed_shared_args._mode],
                                    expert=_expert)
    KgtkValueOptions.add_arguments(parser, expert=_expert)


def custom_progress() -> bool:
    return True  # We want to start a custom progress monitor.


def run(input_files: KGTKFiles,
        output_file: KGTKFiles,
        output_format: typing.Optional[str],

        output_column_names: typing.Optional[typing.List[str]],
        old_column_names: typing.Optional[typing.List[str]],
        new_column_names: typing.Optional[typing.List[str]],

        no_output_header: bool,
        pure_python: bool,
        fast_copy_min_size: int,

        bash_command: str,
        bzip2_command: str,
        cat_command: str,
        gzip_command: str,
        tail_command: str,
        xz_command: str,

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
        print("--input-files %s" % " ".join((repr(str(input_file_path)) for input_file_path in input_file_paths)),
              file=error_file, flush=True)
        print("--output-file %s" % repr(str(output_file_path)), file=error_file, flush=True)
        if output_format is not None:
            print("--output-format %s" % repr(output_format), file=error_file, flush=True)
        if output_column_names is not None:
            print("--output-columns %s" % " ".join(output_column_names), file=error_file, flush=True)
        if old_column_names is not None:
            print("--old-columns %s" % " ".join(old_column_names), file=error_file, flush=True)
        if new_column_names is not None:
            print("--new-columns %s" % " ".join(new_column_names), file=error_file, flush=True)
        print("--no-output-header %s" % str(no_output_header), file=error_file, flush=True)
        print("--pure-python %s" % str(pure_python), file=error_file, flush=True)
        print("--fast-copy-min-size %d" % fast_copy_min_size, file=error_file, flush=True)
        print("--bash-commahd %s" % repr(bash_command), file=error_file, flush=True)
        print("--bzip2-commahd %s" % repr(bzip2_command), file=error_file, flush=True)
        print("--cat-commahd %s" % repr(cat_command), file=error_file, flush=True)
        print("--gzip-commahd %s" % repr(gzip_command), file=error_file, flush=True)
        print("--tail-commahd %s" % repr(tail_command), file=error_file, flush=True)
        print("--xz-commahd %s" % repr(xz_command), file=error_file, flush=True)
        reader_options.show(out=error_file)
        value_options.show(out=error_file)
        print("=======", file=error_file, flush=True)

    # Check for consistent options.  argparse doesn't support this yet.
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
                              no_output_header=no_output_header,
                              pure_python=pure_python,
                              fast_copy_min_size=fast_copy_min_size,
                              bash_command=bash_command,
                              bzip2_command=bzip2_command,
                              cat_command=cat_command,
                              gzip_command=gzip_command,
                              tail_command=tail_command,
                              xz_command=xz_command,
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
    except KGTKException as e:
        raise
    except Exception as e:
        raise KGTKException(str(e))

