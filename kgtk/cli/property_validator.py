"""
Copy a KGTK file, validating it and producing a clean KGTK file (no
comments, whitespace lines, etc.), then running the property validator.

TODO: Need KgtkWriterOptions.

TODO: Need to plumn the infrastructure so we can report at least
a count of how many repair actions took place (per action type).
Ideally, we'ld like the optino to log individual repair actions.

TODO: Add a reject file.

"""

from argparse import Namespace, SUPPRESS
from pathlib import Path
import sys
import typing

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderMode, KgtkReaderOptions
from kgtk.io.kgtkwriter import KgtkWriter
from kgtk.utils.argparsehelpers import optional_bool
from kgtk.value.propertypatternvalidator import PropertyPatterns, PropertyPatternValidator
from kgtk.value.kgtkvalueoptions import KgtkValueOptions

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
    _expert: bool = parsed_shared_args._expert

    parser.add_input_file()
    parser.add_input_file(who="The property pattern definitions.", default_stdin=False,
                          options=["--pattern-file"], dest="pattern_file", metavar="PATTERN_FILE")
    parser.add_output_file(optional=True)
    parser.add_output_file(who="The property pattern reject output.", optional=True,
                          options=["--reject-file"], dest="reject_file", metavar="REJECT_FILE")

    parser.add_argument(      "--presorted", dest="grouped_input",
                              help="Indicate that the input has been presorted (or at least pregrouped) on the node1 column. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False, metavar="True|False")

    parser.add_argument(      "--reject-node1-groups", dest="reject_node1_groups",
                              help="Indicate that when a record is rejected, all records for the same node1 value " +
                              "should be rejected. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=True, metavar="True|False")

    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, validate_by_default=True, expert=_expert)
    KgtkValueOptions.add_arguments(parser, expert=_expert)


def run(input_file: KGTKFiles,
        pattern_file: KGTKFiles,
        output_file: KGTKFiles,
        reject_file: KGTKFiles,
        grouped_input: bool = False,
        reject_node1_groups: bool = False,
        errors_to_stdout: bool = False,
        errors_to_stderr: bool = False,
        show_options: bool = False,
        verbose: bool = False,
        very_verbose: bool = False,
        **kwargs # Whatever KgtkReaderOptions and KgtkValueOptions want.
)->int:
    # import modules locally
    from kgtk.exceptions import KGTKException

    input_kgtk_file: Path = KGTKArgumentParser.get_input_file(input_file)
    pattern_kgtk_file: Path = KGTKArgumentParser.get_input_file(pattern_file, default_stdin=False)
    output_kgtk_file: typing.Optional[Path] = KGTKArgumentParser.get_optional_output_file(output_file)
    reject_kgtk_file: typing.Optional[Path] = KGTKArgumentParser.get_optional_output_file(reject_file)

    # Select where to send error messages, defaulting to stderr.
    error_file: typing.TextIO = sys.stdout if errors_to_stdout else sys.stderr

    # Build the option structures.
    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs)
    value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)

    # Show the final option structures for debugging and documentation.
    if show_options:
        print("--input-file=%s" % str(input_kgtk_file), file=error_file)
        print("--pattern-file=%s" % str(pattern_kgtk_file), file=error_file)
        if output_kgtk_file is not None:
            print("--output-file=%s" % str(output_kgtk_file), file=error_file)
        if reject_kgtk_file is not None:
            print("--reject-file=%s" % str(reject_kgtk_file), file=error_file)
        print("--presorted=%s" % str(grouped_input))
        print("--reject-node1-groups=%s" % str(reject_node1_groups))
        reader_options.show(out=error_file)
        value_options.show(out=error_file)
        print("=======", file=error_file, flush=True)

    if verbose:
        print("Reading data from '%s'" % str(input_kgtk_file), file=error_file, flush=True)
        print("Reading patterns from '%s'" % str(pattern_kgtk_file), file=error_file, flush=True)
        if output_kgtk_file is not None:
            print("Writing good data to '%s'" % str(output_kgtk_file), file=error_file, flush=True)
        if reject_kgtk_file is not None:
            print("Writing rejected data to '%s'" % str(reject_kgtk_file), file=error_file, flush=True)
                
    try:
        pkr: KgtkReader = KgtkReader.open(pattern_kgtk_file,
                                          error_file=error_file,
                                          mode=KgtkReaderMode.EDGE,
                                          options=reader_options,
                                          value_options=value_options,
                                          verbose=verbose,
                                          very_verbose=very_verbose)
        
        pps: PropertyPatterns = PropertyPatterns.load(pkr,
                                                      value_options,
                                                      error_file=error_file,
                                                      verbose=verbose,
                                                      very_verbose=very_verbose)
        
        kr: KgtkReader = KgtkReader.open(input_kgtk_file,
                                         error_file=error_file,
                                         options=reader_options,
                                         value_options=value_options,
                                         verbose=verbose,
                                         very_verbose=very_verbose)

        ppv: PropertyPatternValidator = PropertyPatternValidator.new(pps,
                                                                     kr,
                                                                     grouped_input=grouped_input,
                                                                     reject_node1_groups=reject_node1_groups,
                                                                     value_options=value_options,
                                                                     error_file=error_file,
                                                                     verbose=verbose,
                                                                     very_verbose=very_verbose)

        kw: typing.Optional[KgtkWriter] = None
        if output_kgtk_file is not None:
            kw = KgtkWriter.open(kr.column_names,
                                 output_kgtk_file,
                                 verbose=verbose, very_verbose=very_verbose)
        
        rkw: typing.Optional[KgtkWriter] = None
        if reject_kgtk_file is not None:
            rkw = KgtkWriter.open(kr.column_names,
                                  reject_kgtk_file,
                                  verbose=verbose, very_verbose=very_verbose)
        
        input_row_count: int = 0
        valid_row_count: int = 0
        output_row_count: int = 0
        reject_row_count: int = 0
        input_row_count, valid_row_count, output_row_count, reject_row_count = ppv.process(kr, kw, rkw)

        if verbose:
            print("Read %d rows, %d valid" % (input_row_count, valid_row_count), file=error_file, flush=True)
            if kw is not None:
                print("Wrote %d good rows" % output_row_count, file=error_file, flush=True)
            if rkw is not None:
                print("Wrote %d rejected rows" % reject_row_count, file=error_file, flush=True)

        if kw is not None:
            kw.close()
        if rkw is not None:
            rkw.close()

        return 0

    except Exception as e:
        raise KGTKException(e)

