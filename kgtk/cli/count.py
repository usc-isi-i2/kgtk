"""Count records or non-empty values per column.

This is a simple command that illustrates several aspects of building
a KGTK command.  The following features are illustrated:

* Using the KGTK command line parser's extended features.
  * Adding command alias.
  * Adding an option with a different default for the command alias.
  * Adding an expert option.
* Reading a KGTK input file.
* Writing a KGTK output file.
* Writing non-KGTK output to stdout.
* Writing progress feedback to etderr.
"""

# We minimize the imports here because every additional global import
# slows down `kgtk` command initialization.
from argparse import Namespace, SUPPRESS
import typing

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles

# Decine the name of the command and its alias.
COUNT_COMMAND: str = "count"
WC_COMMAND: str = "wc"

# Default option values:
DEFAULT_COUNT_RECORDS: bool = False
DEFAULT_COUNT_RECORDS_WC: bool = True
DEFAULT_COUNT_PROPERTY: str = "count"

def parser():
    return {
        'aliases': [ WC_COMMAND ],
        'help': 'Count records or non-empty values per column.',
        'description': 'Count the number of records in a KGTK file, excluding the header record, ' +
        'or count the number of non-empty values per column.  Note:  not non-empty unique values, ' +
        'that is what `kgtk unique` does.' +
        '\n\nAdditional options are shown in expert help.\nkgtk --expert lift --help'
    }

def add_arguments_extended(parser: KGTKArgumentParser, parsed_shared_args: Namespace):
    """                                                                                                                                                               
    Parse arguments                                                                                                                                                   
    Args:                                                                                                                                                             
        parser (argparse.ArgumentParser)                                                                                                                              
    """
    # Import modules thay we will use when declaring arguments.
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions, KgtkReaderMode
    from kgtk.utils.argparsehelpers import optional_bool
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    # These special shared aruments inticate whether the `--expert` option
    # was supplied and the command name that was used.
    _expert: bool = parsed_shared_args._expert
    _command: str = parsed_shared_args._command

    # This helper function makes it easy to suppress options from the help
    # message unless `--expert` has bee asserted.  The options are still
    # there, and initialize what they need to initialize.
    def h(msg: str)->str:
        if _expert:
            return msg
        else:
            return SUPPRESS

    # Add the primary input and output files without special features.
    parser.add_input_file()
    parser.add_output_file()

    # The default value for this option depends upon the command used.
    parser.add_argument('-l', '--lines', dest="count_records", metavar="True/False",
                        help="If true, count records and print a single number to stdout. " +
                        "If false, count non-empty values per column and produce a simple KGTK output file. (default=%(default)s).",
                        type=optional_bool, nargs='?', const=True,
                        default=DEFAULT_COUNT_RECORDS_WC if _command == WC_COMMAND else DEFAULT_COUNT_RECORDS)

    # This is an expert option.  It will not show up on `--help` without `--expert`:
    parser.add_argument(      "--count-property", dest="count_property",
                              help=h("The property used for column count output edges. (default=%(default)s)."),
                              default=DEFAULT_COUNT_PROPERTY)

    # Add the standard debugging arguments and the KgtkReader and KgtkValue
    # options.
    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser,
                                    mode_options=True,
                                    default_mode=KgtkReaderMode[parsed_shared_args._mode],
                                    expert=_expert)
    KgtkValueOptions.add_arguments(parser, expert=_expert)


# This is our irimary entry point after command parsing.  Note the special
# KGTKFiles type used for input and output files that were declared using the
# extended argument parser's `add_input_file()` and `add_output_file()`
# methods.
def run(input_file: KGTKFiles,
        output_file: KGTKFiles,

        count_records: bool = DEFAULT_COUNT_RECORDS,
        count_property: str = DEFAULT_COUNT_PROPERTY,

        errors_to_stdout: bool = False,
        errors_to_stderr: bool = True,
        show_options: bool = False,
        verbose: bool = False,
        very_verbose: bool = False,

        **kwargs # Whatever KgtkFileOptions and KgtkValueOptions want.
)->int:

    # Import the modules that we need for processing:
    import sys

    from kgtk.exceptions import KGTKException
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
    from kgtk.io.kgtkwriter import KgtkWriter

    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    # Perform the final parsing steps on the primary input and output files.
    # The naming convention is unfortunate;  these should have been called
    # `input_kgtk_path` and `output_kgtk_path`.
    input_kgtk_file: Path = KGTKArgumentParser.get_input_file(input_file)
    output_kgtk_file: Path = KGTKArgumentParser.get_output_file(output_file)

    # Select where to send error messages, defaulting to stderr.
    error_file: typing.TextIO = sys.stdout if errors_to_stdout else sys.stderr

    # Build the KGTKReader and KgtkValue option structures.
    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs)
    value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)

    # Show the final option values for debugging and documentation.
    if show_options:
        print("--input-file=%s" % str(input_kgtk_file), file=error_file, flush=True)
        print("--output-file=%s" % str(output_kgtk_file), file=error_file, flush=True)
        print("--lines=%s" % repr(count_records),  file=error_file, flush=True)
        print("--count-property=%s" % repr(count_property),  file=error_file, flush=True)

        input_reader_options.show(out=error_file, who="input")
        label_reader_options.show(out=error_file, who="label")
        value_options.show(out=error_file)
        print("=======", file=error_file, flush=True)

    # Prepare to catch SystemExit and Exception.
    try:
        
        # Open the primary input file:
        if verbose:
            print("Opening the input file %s" % str(input_kgtk_file), file=error_file, flush=True)
        kr: KgtkReader = KgtkReader.open(input_kgtk_file,
                                         options=reader_options,
                                         value_options = value_options,
                                         error_file=error_file,
                                         verbose=verbose,
                                         very_verbose=very_verbose,
        )

        # We have two execution paths, depending on count_records:
        row: typing.List[str]
        if count_records:
            # Count the number of data records in the input file.
            record_count: int = 0
            for row in kr:
                record_count += 1

            if str(output_kgtk_file) == "-":
                # Send the record count to standard output:
                print("%d" % record_count, file=sys.stdout, flush=True)

            else:
                with open(output_kgtk_file, "w") as outf:
                    # Send the record count to a file:
                    print("%d" % record_count, file=outf)

        else:
            # Open a KgtkWriter file for the primary output file:
            if verbose:
                print("Opening the output file %s" % str(output_kgtk_file), file=error_file, flush=True)
            kw: KgtkWriter = KgtkWriter.open(["node1", "label", "node2" ],
                                             output_kgtk_file,
                                             verbose=verbose,
                                             very_verbose=very_verbose,
                                 )
            # Count the number of non-empty cells for each column:
            record_counts: typing.List[int] = [ 0 for idx in range(kr.column_count) ]
            idx: int
            for row in kr:
                item: str
                for idx, item in enumerate(row):
                    if len(item) > 0:
                        record_counts[idx] += 1

            # Send the results to the primary output file as a series of edges.
            count: int
            for idx, count in enumerate(record_counts):
                kw.write([ kr.column_names[idx], count_property, str(record_counts[idx]) ])

            # Close the primary output file.
            kw.close()            

        # Close the primary input file.
        kr.close()
        return 0

    except SystemExit as e:
        raise KGTKException("Exit requested")
    except Exception as e:
        raise KGTKException(str(e))
