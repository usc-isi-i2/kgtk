"""Filter a KGTK file based on whether one or more records exist in a second
KGTK file with matching values for one or more fields.

TODO: Need KgtkWriterOptions
"""

from argparse import Namespace, SUPPRESS
import sys
import typing

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles

def parser():
    return {
        'help': 'Count unique values in a column.',
        'description': 'Count the unique values in a column in a KGTK file. Write the unique values and counts as a new KGTK file.' +
        '\n\nAdditional options are shown in expert help.\nkgtk --expert unique --help'
    }


def add_arguments_extended(parser: KGTKArgumentParser, parsed_shared_args: Namespace):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """
    from kgtk.kgtkformat import KgtkFormat
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
    from kgtk.join.unique import Unique
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

    parser.add_input_file(positional=True)
    parser.add_output_file()

    parser.add_argument('-c', "--column", "--columns", dest="column_names", nargs='*',
                        metavar="COLUMN_NAME",
                              help="The column(s) to count unique values (default=node2 or its alias).")

    parser.add_argument(      "--empty", dest="empty_value", help="A value to substitute for empty values (default=%(default)s).", default="")

    parser.add_argument(      "--label", dest="label_value", help="The output file label column value (default=%(default)s).", default="count")

    # TODO: use an emum
    parser.add_argument(      "--format", dest="output_format", help="The output file format and mode (default=%(default)s).",
                              default=Unique.DEFAULT_FORMAT, choices=Unique.OUTPUT_FORMATS)

    parser.add_argument(      "--prefix", dest="prefix", help="The value prefix (default=%(default)s).", default="")

    parser.add_argument(      "--where", dest="where_column_name",
                              help="The name of a column for a record selection test. (default=%(default)s).", default=None)

    parser.add_argument(      "--in", dest="where_values", nargs="+",
                              help="The list of values for a record selection test. (default=%(default)s).", default=None)

    parser.add_argument(      "--value-filter", dest="value_filter", metavar="VALUE_FILTER_RE",
                              help="A regular expression filter on the extracted values. (default=%(default)s).", default="")

    parser.add_argument(      "--value-match-type", dest="value_match_type", 
                              help="Which type of regular expression value match: %(choices)s. (default=%(default)s).",
                              type=str, default="match", choices=["fullmatch", "match", "search"])

    parser.add_argument(      "--presorted", dest="presorted", metavar="True|False",
                              help="When True, the input file is presorted. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--min-count", dest="min_count", type=int, default=0,
                              help=f"The minimum count output filter (does not apply to {repr(Unique.NODE_FORMAT)} format). The minimum and maximum count filters are conjunctive. (default=%(default)s).")

    parser.add_argument(      "--max-count", dest="max_count", type=int, default=999999999999999,
                              help=f"The minimum count output filter (does not apply to {repr(Unique.NODE_FORMAT)} format). The minimum and maximum count filters are conjunctive. (default=%(default)s).")

    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, expert=_expert)
    KgtkValueOptions.add_arguments(parser, expert=_expert)

def run(input_file: KGTKFiles,
        output_file: KGTKFiles,

        column_names: typing.Optional[typing.List[str]] = None,
        empty_value: str = "",
        label_value: str = "count",

        output_format: str = "edge",
        prefix: str = "",

        where_column_name: typing.Optional[str] = None,
        where_values: typing.Optional[typing.List[str]] = None,

        value_filter: str = "",
        value_match_type: str = "match",

        presorted: bool = False,

        min_count: int = 0,
        max_count: int = sys.maxsize,

        errors_to_stdout: bool = False,
        errors_to_stderr: bool = True,
        show_options: bool = False,
        verbose: bool = False,
        very_verbose: bool = False,

        **kwargs # Whatever KgtkFileOptions and KgtkValueOptions want.
)->int:
    # import modules locally
    from pathlib import Path

    from kgtk.exceptions import KGTKException
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
    from kgtk.io.kgtkwriter import KgtkWriter
    from kgtk.join.unique import Unique
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    input_kgtk_file: Path = KGTKArgumentParser.get_input_file(input_file)
    output_kgtk_file: Path = KGTKArgumentParser.get_output_file(output_file)

    # Select where to send error messages, defaulting to stderr.
    error_file: typing.TextIO = sys.stdout if errors_to_stdout else sys.stderr

    # Build the option structures.
    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs)
    value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)

    # Show the final option structures for debugging and documentation.
    if show_options:
        print("--input-file=%s" % str(input_kgtk_file), file=error_file)
        print("--output-file=%s" % str(output_kgtk_file), file=error_file)
        if column_names is not None:
            print("--columns %s" % " ".join(column_names), file=error_file, flush=True)
        print("--empty=%s" % str(empty_value), file=error_file)
        print("--label=%s" % str(label_value), file=error_file)
        print("--format=%s" % output_format, file=error_file)
        print("--prefix=%s" % prefix, file=error_file)
        if where_column_name is not None:
            print("--where=%s" % where_column_name, file=error_file)
        if where_values is not None and len(where_values) > 0:
            print("--in=%s" % " ".join(where_values), file=error_file)
        print("--value-filter=%s" % repr(value_filter), file=error_file)
        print("--value-match-type=%s" % repr(value_match_type), file=error_file)
        print("--prefix=%s" % repr(presorted), file=error_file)
        print("--min-count=%d" % min_count, file=error_file)
        print("--max-count=%d" % max_count, file=error_file)
        reader_options.show(out=error_file)
        value_options.show(out=error_file)
        print("=======", file=error_file, flush=True)

    if min_count > max_count:
        raise KGTKException("Error: --min-count %d is greater than --max-count %d" % (min_count, max_count))

    try:
        uniq: Unique = Unique(
            input_file_path=input_kgtk_file,
            output_file_path=output_kgtk_file,
            column_names=column_names,
            label_value=label_value,
            empty_value=empty_value,
            output_format=output_format,
            prefix=prefix,
            where_column_name=where_column_name,
            where_values=where_values,
            value_filter=value_filter,
            value_match_type=value_match_type,
            presorted=presorted,
            min_count=min_count,
            max_count=max_count,
            reader_options=reader_options,
            value_options=value_options,
            error_file=error_file,
            verbose=verbose,
            very_verbose=very_verbose,
        )
        
        uniq.process()

        return 0

    except SystemExit as e:
        raise KGTKException("Exit requested")
    except Exception as e:
        raise KGTKException(str(e))

