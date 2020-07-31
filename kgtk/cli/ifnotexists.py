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
        'help': 'Filter a KGTK file by not matching records in a second KGTK file.',
        'description': 'Filter a KGTK file based on whether one or more records do not exist in a second KGTK file with matching values for one or more fields.' +
        '\n\nAdditional options are shown in expert help.\nkgtk --expert ifnotexists --help'
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
                          options=["--filter-on"], dest="filter_file", metavar="FILTER_FILE")
    parser.add_output_file()
    parser.add_output_file(who="The KGTK reject file for records that fail the filter.",
                           dest="reject_file",
                           options=["--reject-file"],
                           metavar="REJECT_FILE",
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

    parser.add_argument(      "--field-separator", dest="field_separator",
                              help=h("Separator for multifield keys (default=%(default)s)"),
                              default=KgtkIfExists.FIELD_SEPARATOR_DEFAULT)

    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, expert=_expert)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, who="input", expert=_expert, defaults=False)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, who="filter", expert=_expert, defaults=False)
    KgtkValueOptions.add_arguments(parser, expert=_expert)

def run(input_file: KGTKFiles,
        filter_file: KGTKFiles,
        output_file: KGTKFiles,
        reject_file: KGTKFiles,

        input_keys: typing.Optional[typing.List[str]],
        filter_keys: typing.Optional[typing.List[str]],
        
        cache_input: bool = False,
        preserve_order: bool = False,

        field_separator: typing.Optional[str] = None,

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
        print("input: %s" % (str(input_kgtk_file) if input_kgtk_file is not None else "-"), file=error_file)
        print("--output-file=%s" % (str(output_kgtk_file) if output_kgtk_file is not None else "-"), file=error_file)
        if reject_kgtk_file is not None:
            print("--reject-file=%s" % str(reject_kgtk_file), file=error_file)
        print("--filter-on=%s" % (str(filter_kgtk_file) if filter_kgtk_file is not None else "-"), file=error_file)
        if input_keys is not None:
            print("--input-keys=%s" % " ".join(input_keys), file=error_file)
        if filter_keys is not None:
            print("--filter-keys=%s" % " ".join(filter_keys), file=error_file)
        print("--cache-input=%s" % str(cache_input), file=error_file)
        print("--preserve-order=%s" % str(preserve_order), file=error_file)
        print("--field-separator='%s'" % repr(field_separator), file=error_file)
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
            invert=True,
            cache_input=cache_input,
            preserve_order=preserve_order,
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

