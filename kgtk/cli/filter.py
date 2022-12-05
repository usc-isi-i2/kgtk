"""
Filter rows by subject, predicate, object values.
"""
from argparse import Namespace
import typing

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles


def parser():
    return {
        'help': 'Filter rows by subject, predicate, object values.',
        'description': 'Filter KGTK file based on values in the node1 (subject), ' +
                       'label (predicate), and node2 (object) fields.  Optionally filter based on ' +
                       'regular expressions.'
    }


REGEX_MATCH_TYPES: typing.List[str] = ["fullmatch", "match", "search"]
NUMERIC_MATCH_TYPES: typing.List[str] = ["eq", "ne", "gt", "ge", "lt", "le"]
MATCH_TYPES: typing.List[str] = REGEX_MATCH_TYPES + NUMERIC_MATCH_TYPES


def add_arguments_extended(parser: KGTKArgumentParser, parsed_shared_args: Namespace):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions, KgtkReaderMode
    from kgtk.utils.argparsehelpers import optional_bool
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    _expert: bool = parsed_shared_args._expert

    # '$label == "/r/DefinedAs" && $node2=="/c/en/number_zero"'
    parser.add_input_file(positional=True)
    parser.add_output_file(
        who="The KGTK output file for records that pass the filter. Multiple output file may be specified, each with their own pattern.",
        allow_list=True, dest="output_files")
    parser.add_output_file(who="The KGTK reject file for records that fail the filter.",
                           dest="reject_file",
                           options=["--reject-file"],
                           metavar="REJECT_FILE",
                           optional=True)

    # parser.add_argument('-dt', "--datatype", action="store", type=str, dest="datatype", help="Datatype of the input file, e.g., tsv or csv.", default="tsv")
    parser.add_argument('-p', '--pattern', action="append", nargs="+", type=str, dest="patterns", required=True,
                        help="Pattern to filter on, for instance, \" ; P154 ; \". Multiple patterns may be specified when there are mutiple output files.")
    parser.add_argument('--node1', '--subj', action="store", type=str, dest='subj_col',
                        help="The subject column, default is node1 or its alias.")
    parser.add_argument('--label', '--pred', action="store", type=str, dest='pred_col',
                        help="The predicate column, default is label or its alias.")
    parser.add_argument('--node2', '--obj', action="store", type=str, dest='obj_col',
                        help="The object column, default is node2 or its alias.")

    parser.add_argument("--or", dest="or_pattern", metavar="True|False",
                        help="'Or' the clauses of the pattern. (default=%(default)s).",
                        type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument("--invert", dest="invert", metavar="True|False",
                        help="Invert the result of applying the pattern. (default=%(default)s).",
                        type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument("--regex", dest="regex", metavar="True|False",
                        help="When True, treat the filter clauses as regular expressions. (default=%(default)s).",
                        type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument("--numeric", dest="numeric", metavar="True|False",
                        help="When True, treat the filter clauses as numeric values for comparison. (default=%(default)s).",
                        type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument("--fancy", dest="fancy", metavar="True|False",
                        help="When True, treat the filter clauses as strings, numbers, or regular expressions. (default=%(default)s).",
                        type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument("--match-type", dest="match_type",
                        help="Which type of regular expression match: %(choices)s. (default=%(default)s).",
                        type=str, default="match", choices=MATCH_TYPES)

    parser.add_argument("--first-match-only", dest="first_match_only", metavar="True|False",
                        help="If true, write only to the file with the first matching pattern.  If false, write to all files with matching patterns. (default=%(default)s).",
                        type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument("--pass-empty-value", dest="pass_empty_value", metavar="True|False",
                        help="If true, empty data values will pass a numeric pattern.  If false, write to all files with matching patterns. (default=%(default)s).",
                        type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument('--pattern-separator', action="store", type=str, dest='pattern_separator', default=";",
                        help="The separator between the pattern components. (default=%(default)s.")

    parser.add_argument('--word-separator', action="store", type=str, dest='word_separator', default=",",
                        help="The separator between the words in a pattern component. (default=%(default)s.")

    parser.add_argument("--show-version", dest="show_version", type=optional_bool, nargs='?', const=True, default=False,
                        help="Print the version of this program. (default=%(default)s).", metavar="True/False")

    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser,
                                    mode_options=True,
                                    default_mode=KgtkReaderMode[parsed_shared_args._mode],
                                    expert=_expert)
    KgtkValueOptions.add_arguments(parser, expert=_expert)


def run(input_file: KGTKFiles,
        output_files: KGTKFiles,
        reject_file: KGTKFiles,

        patterns: typing.List[typing.List[str]],
        subj_col: typing.Optional[str],
        pred_col: typing.Optional[str],
        obj_col: typing.Optional[str],

        or_pattern: bool,
        invert: bool,
        regex: bool,
        numeric: bool,
        fancy: bool,
        match_type: str,
        first_match_only: bool,
        pass_empty_value: bool,

        pattern_separator: str = ";",
        word_separator: str = ",",

        show_version: bool = False,

        errors_to_stdout: bool = False,
        errors_to_stderr: bool = True,
        show_options: bool = False,
        verbose: bool = False,
        very_verbose: bool = False,

        **kwargs  # Whatever KgtkFileOptions and KgtkValueOptions want.
        ) -> int:
    # import modules locally
    from pathlib import Path
    import sys

    from kgtk.exceptions import kgtk_exception_auto_handler
    from kgtk.io.kgtkreader import KgtkReaderOptions
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions
    from kgtk.utils.filter import Filter
    try:
        input_kgtk_file: Path = KGTKArgumentParser.get_input_file(input_file)
        output_kgtk_files: typing.List[Path] = KGTKArgumentParser.get_output_file_list(output_files,
                                                                                       default_stdout=True)
        reject_kgtk_file: typing.Optional[Path] = KGTKArgumentParser.get_optional_output_file(reject_file,
                                                                                              who="KGTK reject file")

        # Select where to send error messages, defaulting to stderr.
        error_file: typing.TextIO = sys.stdout if errors_to_stdout else sys.stderr

        # Build the option structures.
        reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs)
        value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)

        UPDATE_VERSION: str = "2022-08-31T20:44:35.211458+00:00#u+yUIrg4l2PTfg7u5ta1F9DHS32Qw5fIK6T2ZNJeI1C6kONkQGC7Vt+IsnxLD5qyyfkHq/yW99VcJ08Nhs8wjQ=="
        if show_version or verbose:
            print("kgtk filter version: %s" % UPDATE_VERSION, file=error_file, flush=True)

        f = Filter(input_kgtk_file=input_kgtk_file,
                   output_kgtk_files=output_kgtk_files,
                   patterns=patterns,
                   reject_kgtk_file=reject_kgtk_file,
                   reader_options=reader_options,
                   value_options=value_options,
                   subj_col=subj_col,
                   pred_col=pred_col,
                   obj_col=obj_col,
                   or_pattern=or_pattern,
                   invert=invert,
                   regex=regex,
                   numeric=numeric,
                   fancy=fancy,
                   match_type=match_type,
                   first_match_only=first_match_only,
                   pass_empty_value=pass_empty_value,
                   pattern_separator=pattern_separator,
                   word_separator=word_separator,
                   show_version=show_version,
                   error_file=error_file,
                   show_options=show_options,
                   verbose=verbose,
                   very_verbose=very_verbose)
        f.process()

    except Exception as e:
        kgtk_exception_auto_handler(e)
        return 1
