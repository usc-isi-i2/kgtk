"""
Copy a KGTK file, validating it and producing a clean KGTK file (no
comments, whitespace lines, etc.) as output.

TODO: Need KgtkWriterOptions.

TODO: Need to plumn the infrastructure so we can report at least
a count of how many repair actions took place (per action type).
Ideally, we'ld like the optino to log individual repair actions.

TODO: Add a reject file.

"""

from argparse import Namespace, SUPPRESS

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles

def parser():
    return {
        'help': 'Validate a KGTK file and output a clean copy: no comments, whitespace lines, invalid lines, etc. ',
        'description': 'Validate a KGTK file and output a clean copy. ' +
        'Empty lines, whitespace lines, comment lines, and lines with empty required fields are silently skipped. ' +
        'Header errors cause an immediate exception. Data value errors are reported and the line containing them skipped. ' +
        '\n\nAdditional options are shown in expert help.\nkgtk --expert clean-data --help'
    }


def add_arguments_extended(parser: KGTKArgumentParser, parsed_shared_args: Namespace):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """
    # import modules locally
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions
    
    _expert: bool = parsed_shared_args._expert

    parser.add_input_file(positional=True)
    parser.add_output_file(positional=True)
    parser.add_output_file(who="Reject file",
                           dest="reject_file",
                           options=["--reject-file"],
                           metavar="REJECT_FILE",
                           optional=True)

    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, validate_by_default=True, expert=_expert)
    KgtkValueOptions.add_arguments(parser, expert=_expert)


def run(input_file: KGTKFiles,
        output_file: KGTKFiles,
        reject_file: KGTKFiles,
        errors_to_stdout: bool = False,
        errors_to_stderr: bool = False,
        show_options: bool = False,
        verbose: bool = False,
        very_verbose: bool = False,
        **kwargs # Whatever KgtkReaderOptions and KgtkValueOptions want.
)->int:
    # import modules locally
    from pathlib import Path
    import sys
    import typing
    
    from kgtk.exceptions import KGTKException
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
    from kgtk.io.kgtkwriter import KgtkWriter
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    input_kgtk_file_path: Path = KGTKArgumentParser.get_input_file(input_file)
    output_kgtk_file_path: Path = KGTKArgumentParser.get_output_file(output_file)
    reject_kgtk_file_path: typing.Optional[Path] = KGTKArgumentParser.get_optional_output_file(reject_file, who="Reject file")

    # Select where to send error messages, defaulting to stderr.
    error_file: typing.TextIO = sys.stdout if errors_to_stdout else sys.stderr

    # Build the option structures.
    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs)
    value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)

    # Show the final option structures for debugging and documentation.
    if show_options:
        print("--input-file=%s" % str(input_kgtk_file_path), file=error_file)
        print("--output-file=%s" % str(output_kgtk_file_path), file=error_file)
        if reject_kgtk_file_path is not None:
            print("--reject-file=%s" % str(reject_kgtk_file_path), file=error_file)
            
        reader_options.show(out=error_file)
        value_options.show(out=error_file)
        print("=======", file=error_file, flush=True)

    if verbose:
        if str(input_kgtk_file_path) == "-":
            print ("Cleaning data from stdin", file=error_file, flush=True)
        else:
            print("Cleaning data from '%s'" % str(input_kgtk_file_path), file=error_file, flush=True)
        if str(output_kgtk_file_path) == "-":
            print ("Writing data to stdout", file=error_file, flush=True)
        else:
            print("Writing data to '%s'" % str(output_kgtk_file_path), file=error_file, flush=True)
        if str(reject_kgtk_file_path) == "-":
            print ("Writing reject data to stdout", file=error_file, flush=True)
        else:
            print("Writing reject data to '%s'" % str(reject_kgtk_file_path), file=error_file, flush=True)

    reject_kgtk_file: typing.Optional[typing.TextIO] = None
    if reject_kgtk_file_path is not None:
        reject_kgtk_file = open(reject_kgtk_file_path, mode="wt")

    try:
        kr: KgtkReader = KgtkReader.open(input_kgtk_file_path,
                                         error_file=error_file,
                                         reject_file=reject_kgtk_file,
                                         options=reader_options,
                                         value_options=value_options,
                                         verbose=verbose,
                                         very_verbose=very_verbose)

        kw: KgtkWriter = KgtkWriter.open(kr.column_names,
                                         output_kgtk_file_path,
                                         verbose=verbose, very_verbose=very_verbose)
        
        line_count: int = 0
        row: typing.List[str]
        for row in kr:
            kw.write(row)
            line_count += 1

        kw.close()
        if reject_kgtk_file is not None:
            reject_kgtk_file.close()

        if verbose:
            print("Copied %d clean data lines" % line_count, file=error_file, flush=True)
        return 0

    except Exception as e:
        raise KGTKException(e)

