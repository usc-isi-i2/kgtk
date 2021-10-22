"""
Validate a KGTK file, producing error messages.

At the present time, validation looks at such things as:
1)      Presence of require columns
2)      Consistent number of columns
3)      Comments, whitespace lines, line s with empty required columns

Certain constraints can be overlooked or repaired.

TODO: Add a reject file.
"""

from argparse import Namespace
import typing

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles

def parser():
    return {
        'help': 'Validate one or more KGTK files ',
        
        'description': 'Validate one or more KGTK files. ' +
        'Empty lines, whitespace lines, comment lines, and lines with empty required fields are silently skipped. ' +
        'Header errors cause an immediate exception. Data value errors are reported. ' +

        '\n\nTo validate data and pass clean data to an output file or pipe, use the kgtk clean_data command.' +

        '\n\nAdditional options are shown in expert help.\nkgtk --expert validate --help'
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

    parser.add_input_file(who="The KGTK file(s) to validate.",
                          dest="input_files",
                          options=["-i", "--input-files"],
                          allow_list=True,
                          positional=True)

    parser.add_argument(      "--header-only", dest="header_only",
                              help="Process the only the header of the input file (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--summary", dest="report_summary",
                              help="Report a summary on the lines processed. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=True)

    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, validate_by_default=True, expert=_expert)
    KgtkValueOptions.add_arguments(parser, expert=_expert)


def run(input_files: KGTKFiles,
        errors_to_stdout: bool = False,
        errors_to_stderr: bool = False,
        header_only: bool = False,
        report_summary: bool = False,
        show_options: bool = False,
        verbose: bool = False,
        very_verbose: bool = False,
        **kwargs # Whatever KgtkReaderOptions and KgtkValueOptions want.
)->int:
    # import modules locally
    from pathlib import Path
    import sys
    
    from kgtk.exceptions import KGTKException
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    kgtk_files: typing.List[Path] = KGTKArgumentParser.get_input_file_list(input_files)

    # Select where to send error messages, defaulting to stderr.
    error_file: typing.TextIO = sys.stderr if errors_to_stderr else sys.stdout

    # Build the option structures.
    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs)
    value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)

    # Show the final option structures for debugging and documentation.
    if show_options:
        print("--input-files: %s" % " ".join((str(kgtk_file) for kgtk_file in kgtk_files)), file=error_file)
        print("--header-only=%s" % str(header_only), file=error_file)
        print("--report-summary=%s" % str(report_summary), file=error_file)
        reader_options.show(out=error_file)
        value_options.show(out=error_file)
        print("=======", file=error_file, flush=True)

    kgtk_file: Path
    for kgtk_file in kgtk_files:
        if verbose:
            print("\n====================================================", file=error_file, flush=True)
            if str(kgtk_file) != "-":
                print("Validating '%s'" % str(kgtk_file), file=error_file, flush=True)
            else:
                print ("Validating from stdin", file=error_file, flush=True)

        kr: typing.Optional[KgtkReader] = None
        error_return: int = 1
        try:
            kr = KgtkReader.open(kgtk_file,
                                 error_file=error_file,
                                 options=reader_options,
                                 value_options=value_options,
                                 verbose=verbose,
                                 very_verbose=very_verbose)

            if header_only:
                if verbose:
                    print("Validated the header only.", file=error_file, flush=True)
            else:
                line_count: int = 0
                row: typing.List[str]
                for row in kr:
                    line_count += 1
                if verbose:
                    print("Validated %d data lines" % line_count, file=error_file, flush=True)

        except ValueError as e:
            print("Error: %s" % str(e), file=error_file, flush=True)
            raise KGTKException("Exiting due to error")

        except SystemExit as e:
            raise KGTKException("Exit requested")
        except Exception as e:
            raise KGTKException(str(e))

        finally:
            if kr is not None:
                if report_summary or verbose:
                    print("\n====================================================", file=error_file, flush=True)
                    kr.report_summary()

                if kr.data_errors_reported == 0:
                    error_return = 0
                kr.close()

    if error_return == 0:
        return 0
    else:
        raise KGTKException("Errors detected")
