"""Count records or non-empty values per column.

This is a simple command that illustrates several aspects of building
a KGTK command.  The following features are illustrated:

* Reading a KGTK input file.
* Writing a KGTK output file.
* Writing non-KGTK output to stdout.
* Writing progress feedback to etderr.
* A command alias with a different default than the base command.
* An expert option.
"""

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
    from kgtk.exceptions import KGTKException
    from kgtk.lift.kgtklift import KgtkLift
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
    from kgtk.utils.argparsehelpers import optional_bool
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    _expert: bool = parsed_shared_args._expert
    _command: str = parsed_shared_args._command

    # This helper function makes it easy to suppress options from
    # The help message.  The options are still there, and initialize
    # what they need to initialize.
    def h(msg: str)->str:
        if _expert:
            return msg
        else:
            return SUPPRESS

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

    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, expert=_expert)
    KgtkValueOptions.add_arguments(parser, expert=_expert)


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

    import sys

    from kgtk.exceptions import KGTKException
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
    from kgtk.io.kgtkwriter import KgtkWriter
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    input_kgtk_file: Path = KGTKArgumentParser.get_input_file(input_file)
    output_kgtk_file: Path = KGTKArgumentParser.get_output_file(output_file)

    # Select where to send error messages, defaulting to stderr.
    error_file: typing.TextIO = sys.stdout if errors_to_stdout else sys.stderr

    # Build the option structures.
    input_reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs, who="input", fallback=True)
    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs)
    value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)

    # Show the final option structures for debugging and documentation.
    if show_options:
        print("--input-file=%s" % str(input_kgtk_file), file=error_file, flush=True)
        print("--output-file=%s" % str(output_kgtk_file), file=error_file, flush=True)
        print("--lines=%s" % repr(count_records),  file=error_file, flush=True)
        print("--count-property=%s" % repr(count_property),  file=error_file, flush=True)

        input_reader_options.show(out=error_file, who="input")
        label_reader_options.show(out=error_file, who="label")
        value_options.show(out=error_file)
        print("=======", file=error_file, flush=True)

    try:
        
        if verbose:
            print("Opening the input file %s" % str(input_kgtk_file), file=error_file, flush=True)
        kr: KgtkReader = KgtkReader.open(input_kgtk_file,
                                         options=reader_options,
                                         value_options = value_options,
                                         error_file=error_file,
                                         verbose=verbose,
                                         very_verbose=very_verbose,
        )

        row: typing.List[str]
        if count_records:
            record_count: int = 0
            for row in kr:
                record_count += 1

            print("%d" % record_count, file=sys.stdout, flush=True)


        else:
            if verbose:
                print("Opening the output file %s" % str(output_kgtk_file), file=error_file, flush=True)
            kw: KgtkWriter = KgtkWriter.open(["node1", "label", "node2" ],
                                             output_kgtk_file,
                                             verbose=verbose,
                                             very_verbose=very_verbose,
                                 )
            record_counts: typing.List[int] = [ 0 for idx in range(kr.column_count) ]
            idx: int
            for row in kr:
                item: str
                for idx, item in enumerate(row):
                    if len(item) > 0:
                        record_counts[idx] += 1

            count: int
            for idx, count in enumerate(record_counts):
                kw.write([ kr.column_names[idx], count_property, str(record_counts[idx]) ])

            kw.close()            

        kr.close()
        return 0

    except SystemExit as e:
        raise KGTKException("Exit requested")
    except Exception as e:
        raise KGTKException(str(e))
