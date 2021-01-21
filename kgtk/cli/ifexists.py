"""Filter a KGTK file based on whether one or more records exist in a second
KGTK file with matching values for one or more fields.

Note: By default, this implementation builds im-memory sets of all the key
values in the second file (the filter file). Optionally, it will cache the
first file (the input file) instead.

Note: By default, input records are passed in order to the output file.  When
the input file is cached, the output records are order by key value (alpha
sort), then by input order.

TODO: Need KgtkWriterOptions
"""

from argparse import Namespace, SUPPRESS
import typing

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles

def parser():
    return {
        'help': 'Filter a KGTK file by matching records in a second KGTK file.',
        'description': 'Filter a KGTK file based on whether one or more records exist in a second KGTK file with matching values for one or more fields.' +
        '\n\nAdditional options are shown in expert help.\nkgtk --expert ifexists --help'
    }


def add_arguments_extended(parser: KGTKArgumentParser, parsed_shared_args: Namespace):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """
    from kgtk.iff.kgtkifexists import KgtkIfExists
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
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
    parser.add_input_file(who="The KGTK file to filter against.",
                          options=["--filter-on", "--filter-file"], dest="filter_file", metavar="FILTER_FILE")
    parser.add_output_file()
    parser.add_output_file(who="The KGTK file for input records that fail the filter.",
                           dest="reject_file",
                           options=["--reject-file"],
                           metavar="REJECT_FILE",
                           optional=True)

    parser.add_output_file(who="The KGTK file for filter records that matched at least one input record.",
                           dest="matched_filter_file",
                           options=["--matched-filter-file"],
                           metavar="MATCHED_FILTER_FILE",
                           optional=True)

    parser.add_output_file(who="The KGTK file for filter records that did not match any input records.",
                           dest="unmatched_filter_file",
                           options=["--unmatched-filter-file"],
                           metavar="UNMATCHED_FILTER_FILE",
                           optional=True)

    parser.add_output_file(who=h("The KGTK file for joined output records (EXPERIMENTAL)."),
                           dest="join_file",
                           options=["--join-file"],
                           metavar="JOIN_FILE",
                           optional=True)

    parser.add_argument(      "--input-keys", "--left-keys", dest="input_keys",
                              help="The key columns in the file being filtered (default=None).", nargs='*')

    parser.add_argument(      "--filter-keys", "--right-keys", dest="filter_keys",
                              help="The key columns in the filter-on file (default=None).", nargs='*')

    parser.add_argument(      "--cache-input", dest="cache_input", metavar="True|False",
                              help="Cache the input file instead of the filter keys (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--preserve-order", dest="preserve_order", metavar="True|False",
                              help="Preserve record order when cacheing the input file. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--presorted", dest="presorted",  metavar="True|False",
                              help="When True, assume that the input and filter files are both presorted.  Use a merge-style algorithm that does not require caching either file. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--field-separator", dest="field_separator",
                              help=h("Separator for multifield keys (default=%(default)s)"),
                              default=KgtkIfExists.FIELD_SEPARATOR_DEFAULT)

    parser.add_argument(      "--left-join", dest="left_join",  metavar="True|False",
                              help=h("When True, Include all input records in the join (EXPERIMENTAL). (default=%(default)s)."),
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--right-join", dest="right_join",  metavar="True|False",
                              help=h("When True, Include all filter records in the join (EXPERIMENTAL). (default=%(default)s)."),
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--input-prefix", dest="input_prefix",
                              help=h("Input file column name prefix for joins (EXPERIMENTAL). (default=%(default)s)"))

    parser.add_argument(      "--filter-prefix", dest="filter_prefix",
                              help=h("Filter file column name prefix for joins (EXPERIMENTAL). (default=%(default)s)"))

    parser.add_argument(      "--join-output", dest="join_output",  metavar="True|False",
                              help=h("When True, send the join records to the main output (EXPERIMENTAL). (default=%(default)s)."),
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--right-first-join", dest="right_first",  metavar="True|False",
                              help=h("When True, send the filter record to join output before the first matching input record. " +
                              " Otherwise, send the first matching input record, then the filter record, then othe rmatching input records. " +
                              "(EXPERIMENTAL). (default=%(default)s)."),
                              type=optional_bool, nargs='?', const=True, default=False)

    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, expert=_expert)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, who="input", expert=_expert, defaults=False)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, who="filter", expert=_expert, defaults=False)
    KgtkValueOptions.add_arguments(parser, expert=_expert)

def run(input_file: KGTKFiles,
        filter_file: KGTKFiles,
        output_file: KGTKFiles,
        reject_file: KGTKFiles,
        matched_filter_file: KGTKFiles,
        unmatched_filter_file: KGTKFiles,
        join_file: KGTKFiles,

        input_keys: typing.Optional[typing.List[str]],
        filter_keys: typing.Optional[typing.List[str]],
        
        cache_input: bool = False,
        preserve_order: bool = False,
        presorted: bool = False,

        field_separator: typing.Optional[str] = None,

        left_join: bool = False,
        right_join: bool = False,
        input_prefix: typing.Optional[str] = None,
        filter_prefix: typing.Optional[str] = None,
        join_output: bool = False,
        right_first: bool = False,

        errors_to_stdout: bool = False,
        errors_to_stderr: bool = True,
        show_options: bool = False,
        verbose: bool = False,
        very_verbose: bool = False,

        **kwargs # Whatever KgtkFileOptions and KgtkValueOptions want.
)->int:
    # import modules locally
    from pathlib import Path
    import sys
    
    from kgtk.exceptions import KGTKException
    from kgtk.iff.kgtkifexists import KgtkIfExists
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
    from kgtk.io.kgtkwriter import KgtkWriter
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    input_kgtk_file: Path = KGTKArgumentParser.get_input_file(input_file)
    filter_kgtk_file: Path = KGTKArgumentParser.get_input_file(filter_file, who="KGTK filter file")
    output_kgtk_file: Path = KGTKArgumentParser.get_output_file(output_file)
    reject_kgtk_file: typing.Optional[Path] = KGTKArgumentParser.get_optional_output_file(reject_file, who="KGTK reject file")
    matched_filter_kgtk_file: typing.Optional[Path] = KGTKArgumentParser.get_optional_output_file(matched_filter_file, who="KGTK matched filter file")
    unmatched_filter_kgtk_file: typing.Optional[Path] = KGTKArgumentParser.get_optional_output_file(unmatched_filter_file, who="KGTK unmatched filter file")
    join_kgtk_file: typing.Optional[Path] = KGTKArgumentParser.get_optional_output_file(join_file, who="KGTK join file")

    if (str(input_kgtk_file) == "-" and str(filter_kgtk_file) == "-"):
        raise KGTKException("My not use stdin for both --input-file and --filter-on files.")

    field_separator = KgtkIfExists.FIELD_SEPARATOR_DEFAULT if field_separator is None else field_separator

    # Select where to send error messages, defaulting to stderr.
    error_file: typing.TextIO = sys.stdout if errors_to_stdout else sys.stderr

    # Build the option structures.
    input_reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs, who="input", fallback=True)
    filter_reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs, who="filter", fallback=True)
    value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)

    # Show the final option structures for debugging and documentation.
    if show_options:
        print("--input-file=%s" % str(input_kgtk_file), file=error_file)
        print("--filter-file=%s" % str(filter_kgtk_file), file=error_file)
        print("--output-file=%s" % str(output_kgtk_file), file=error_file)
        if reject_kgtk_file is not None:
            print("--reject-file=%s" % str(reject_kgtk_file), file=error_file)
        if matched_filter_kgtk_file is not None:
            print("--matched-filter-file=%s" % str(matched_filter_kgtk_file), file=error_file)
        if unmatched_filter_kgtk_file is not None:
            print("--unmatched-filter-file=%s" % str(unmatched_filter_kgtk_file), file=error_file)
        if join_kgtk_file is not None:
            print("--join-file=%s" % str(join_kgtk_file), file=error_file)
        if input_keys is not None:
            print("--input-keys=%s" % " ".join(input_keys), file=error_file)
        if filter_keys is not None:
            print("--filter-keys=%s" % " ".join(filter_keys), file=error_file)
        print("--cache-input=%s" % str(cache_input), file=error_file)
        print("--preserve-order=%s" % str(preserve_order), file=error_file)
        print("--presortedr=%s" % str(presorted), file=error_file)
        print("--field-separator=%s" % repr(field_separator), file=error_file)
        print("--left-join=%s" % str(left_join), file=error_file)
        print("--right-join=%s" % str(right_join), file=error_file)
        if input_prefix is not None:
            print("--input-prefix=%s" % repr(input_prefix), file=error_file)
        if filter_prefix is not None:
            print("--filter-prefix=%s" % repr(filter_prefix), file=error_file)
        print("--join-output=%s" % str(join_output), file=error_file)
        print("--right-join-first=%s" % str(right_first), file=error_file)
        input_reader_options.show(out=error_file, who="input")
        filter_reader_options.show(out=error_file, who="filter")
        value_options.show(out=error_file)
        print("=======", file=error_file, flush=True)

    try:
        ie: KgtkIfExists = KgtkIfExists(
            input_file_path=input_kgtk_file,
            input_keys=input_keys,
            filter_file_path=filter_kgtk_file,
            filter_keys=filter_keys,
            output_file_path=output_kgtk_file,
            reject_file_path=reject_kgtk_file,
            matched_filter_file_path=matched_filter_kgtk_file,
            unmatched_filter_file_path=unmatched_filter_kgtk_file,
            join_file_path=join_kgtk_file,
            left_join=left_join,
            right_join=right_join,
            input_prefix=input_prefix,
            filter_prefix=filter_prefix,
            join_output=join_output,
            right_first=right_first,
            invert=False,
            cache_input=cache_input,
            preserve_order=preserve_order,
            presorted=presorted,
            field_separator=field_separator,
            input_reader_options=input_reader_options,
            filter_reader_options=filter_reader_options,
            value_options=value_options,
            error_file=error_file,
            verbose=verbose,
            very_verbose=very_verbose,
        )
        
        ie.process()

        return 0

    except SystemExit as e:
        raise KGTKException("Exit requested")
    except Exception as e:
        raise KGTKException(str(e))

