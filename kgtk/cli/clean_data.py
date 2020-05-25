"""
Copy a KGTK file, validating it and producing a clean KGTK file (no
comments, whitespace lines, etc.) as output.

TODO: Need KgtkWriterOptions.

TODO: Need to plumn the infrastructure so we can report at least
a count of how many repair actions took place (per action type).
Ideally, we'ld like the optino to log individual repair actions.

"""

from argparse import Namespace, SUPPRESS
from pathlib import Path
import sys
import typing

from kgtk.cli_argparse import KGTKArgumentParser
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
from kgtk.io.kgtkwriter import KgtkWriter
from kgtk.value.kgtkvalueoptions import KgtkValueOptions

def parser():
    return {
        'help': 'Validate a KGTK file and output a clean copy: no comments, whitespace lines, invalid lines, etc. ',
        'description': 'Validate a KGTK file and output a clean copy. ' +
        'Empty lines, whitespace lines, comment lines, and lines with empty required fields are silently skipped. ' +
        'Header errors cause an immediate exception. Data value errors are reported and the line containing them skipped. ' +
        '\n\nAdditional options are shown in expert help.\nkgtk --expert clean_data --help'
    }


def add_arguments_extended(parser: KGTKArgumentParser, parsed_shared_args: Namespace):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """
    _expert: bool = parsed_shared_args._expert

    parser.add_argument(      "input_file", nargs="?", help="The KGTK file to read.  May be omitted or '-' for stdin.", type=Path)
    parser.add_argument(      "output_file", nargs="?", help="The KGTK file to write.  May be omitted or '-' for stdout.", type=Path)
    
    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, validate_by_default=True, expert=_expert)
    KgtkValueOptions.add_arguments(parser, expert=_expert)


def run(input_file: typing.Optional[Path],
        output_file: typing.Optional[Path],
        errors_to_stdout: bool = False,
        errors_to_stderr: bool = False,
        show_options: bool = False,
        verbose: bool = False,
        very_verbose: bool = False,
        **kwargs # Whatever KgtkReaderOptions and KgtkValueOptions want.
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
        print("input: %s" % (str(input_file) if input_file is not None else "-"), file=error_file)
        print("output: %s" % (str(output_file) if output_file is not None else "-"), file=error_file)
        reader_options.show(out=error_file)
        value_options.show(out=error_file)
        print("=======", file=error_file, flush=True)

    if verbose:
        if input_file is not None:
            print("Cleaning data from '%s'" % str(input_file), file=error_file, flush=True)
        else:
            print ("Cleaning data from stdin", file=error_file, flush=True)
        if output_file is not None:
            print("Writing data to '%s'" % str(output_file), file=error_file, flush=True)
        else:
            print ("Writing data to stdin", file=error_file, flush=True)
                
    try:
        kr: KgtkReader = KgtkReader.open(input_file,
                                         error_file=error_file,
                                         options=reader_options,
                                         value_options=value_options,
                                         verbose=verbose,
                                         very_verbose=very_verbose)

        kw: KgtkWriter = KgtkWriter.open(kr.column_names,
                                         output_file,
                                         verbose=verbose, very_verbose=very_verbose)
        
        line_count: int = 0
        row: typing.List[str]
        for row in kr:
            kw.write(row)
            line_count += 1

        kw.close()
        if verbose:
            print("Copied %d clean data lines" % line_count, file=error_file, flush=True)
        return 0

    except Exception as e:
        raise KGTKException(e)

