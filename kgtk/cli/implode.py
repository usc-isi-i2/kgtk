"""Copy records from the first KGTK file to the output file,
building one column (usually node2) from discrete subfields.

TODO: Need KgtkWriterOptions
"""

from argparse import _MutuallyExclusiveGroup, Namespace, SUPPRESS
import typing

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles

def parser():
    return {
        'help': 'Copy a KGTK file, building one column (usualy node2) from seperate columns for each subfield.',
        'description': 'Copy a KGTK file, building one column (usually node2) from seperate columns for each subfield. ' +
        '\n\nStrings may include language qualified strings, and quantities may include numbers. ' +
        '\n\nDate and times subfields and symbol subfields may be optionally quoted. Triple quotes may be used where quotes are accepted. ' +
        '\n\nAdditional options are shown in expert help.\nkgtk --expert implode --help'
    }


def add_arguments_extended(parser: KGTKArgumentParser, parsed_shared_args: Namespace):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """
    from kgtk.kgtkformat import KgtkFormat
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions, KgtkReaderMode
    from kgtk.reshape.kgtkidbuilder import KgtkIdBuilder, KgtkIdBuilderOptions
    from kgtk.utils.argparsehelpers import optional_bool
    from kgtk.value.kgtkvalue import KgtkValueFields
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
    parser.add_output_file(who="The KGTK file for records that are rejected.",
                           dest="reject_file",
                           options=["--reject-file"],
                           metavar="REJECT_FILE",
                           optional=True)

    parser.add_argument(      "--column", dest="column_name", help="The name of the column to explode. (default=%(default)s).", default=KgtkFormat.NODE2)

    parser.add_argument(      "--prefix", dest="prefix", help="The prefix for exploded column names. (default=%(default)s).",
                              default=KgtkFormat.NODE2 + ";" + KgtkFormat.KGTK_NAMESPACE)

    parser.add_argument(      "--types", dest="type_names", nargs='*',
                               help="The KGTK data types for which fields should be imploded. (default=%(default)s).",
                               choices=KgtkFormat.DataType.choices(),
                               default=KgtkFormat.DataType.choices())

    parser.add_argument(      "--without", dest="without_fields", nargs='*',
                               help="The KGTK fields to do without. (default=%(default)s).",
                               choices=KgtkValueFields.OPTIONAL_DEFAULT_FIELD_NAMES,
                               default=None)

    parser.add_argument(      "--overwrite", dest="overwrite_column", metavar='True/False',
                              help="Indicate that it is OK to overwrite an existing imploded column. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=True)

    parser.add_argument(      "--validate", dest="validate", metavar='True/False',
                              help="Validate imploded values. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=True)

    parser.add_argument(      "--escape-pipes", dest="escape_pipes", metavar='True/False',
                              help="When true, pipe characters (|) need to be escaped (\\|) per KGTK file format. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--quantities-include-numbers", dest="quantities_include_numbers", metavar='True/False',
                              help="When true, numbers are acceptable quantities. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=True)

    parser.add_argument(      "--general-strings", dest="general_strings", metavar='True/False',
                              help="When true, strings may include language qualified strings. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=True)

    parser.add_argument(      "--remove-prefixed-columns", dest="remove_prefixed_columns", metavar='True/False',
                              help="When true, remove all columns beginning with the prefix from the output file. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--ignore-unselected-types", dest="ignore_unselected_types", metavar='True/False',
                              help="When true, input records with valid but unselected data types will be passed through to output. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=True)

    parser.add_argument(      "--retain-unselected-types", dest="retain_unselected_types", metavar='True/False',
                              help="When true, input records with valid but unselected data types will be retain existing data on output. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=True)

    parser.add_argument(      "--build-id", dest="build_id", metavar='True/False',
                              help="Build id values in an id column. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--show-data-types", dest="show_data_types", metavar='True/False',
                              help="Print the list of data types and exit. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--quiet", dest="quiet", metavar='True/False',
                              help="When true, suppress certain complaints unless verbose. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    KgtkIdBuilderOptions.add_arguments(parser, expert=_expert)
    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser,
                                    mode_options=True,
                                    default_mode=KgtkReaderMode[parsed_shared_args._mode],
                                    expert=_expert)
    KgtkValueOptions.add_arguments(parser, expert=_expert)

def run(input_file: KGTKFiles,
        output_file: KGTKFiles,
        reject_file: KGTKFiles,

        column_name: str,
        prefix: str,
        type_names: typing.List[str],
        without_fields: typing.Optional[typing.List[str]],
        overwrite_column: bool,
        validate: bool,
        escape_pipes: bool,
        quantities_include_numbers: bool,
        general_strings: bool,
        remove_prefixed_columns: bool,
        ignore_unselected_types: bool,
        retain_unselected_types: bool,
        build_id: bool,
        show_data_types: bool,
        quiet: bool,
        
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
    from kgtk.kgtkformat import KgtkFormat
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
    from kgtk.io.kgtkwriter import KgtkWriter
    from kgtk.reshape.kgtkidbuilder import KgtkIdBuilder, KgtkIdBuilderOptions
    from kgtk.reshape.kgtkimplode import KgtkImplode
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    input_kgtk_file: Path = KGTKArgumentParser.get_input_file(input_file)
    output_kgtk_file: Path = KGTKArgumentParser.get_output_file(output_file)
    reject_kgtk_file: typing.Optional[Path] = KGTKArgumentParser.get_optional_output_file(reject_file, who="KGTK reject file")

    # Select where to send error messages, defaulting to stderr.
    error_file: typing.TextIO = sys.stdout if errors_to_stdout else sys.stderr

    # Build the option structures.
    idbuilder_options: KgtkIdBuilderOptions = KgtkIdBuilderOptions.from_dict(kwargs)    
    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs)
    value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)

    # Show the final option structures for debugging and documentation.
    if show_options:
        print("--input-file=%s" % str(input_kgtk_file), file=error_file)
        print("--output-file=%s" % str(output_kgtk_file), file=error_file, flush=True)
        if reject_kgtk_file is not None:
            print("--reject-file=%s" % str(reject_kgtk_file), file=error_file, flush=True)

        print("--column %s" % column_name, file=error_file, flush=True)
        print("--prefix %s" % prefix, file=error_file, flush=True)
        print("--overwrite %s" % str(overwrite_column), file=error_file, flush=True)
        print("--validate %s" % str(validate), file=error_file, flush=True)
        print("--escape-pipes %s" % str(escape_pipes), file=error_file, flush=True)
        print("--quantities-include-numbers %s" % str(quantities_include_numbers), file=error_file, flush=True)
        print("--general-strings %s" % str(general_strings), file=error_file, flush=True)
        print("--remove-prefixed-columns %s" % str(remove_prefixed_columns), file=error_file, flush=True)
        print("--ignore-unselected-types %s" % str(ignore_unselected_types), file=error_file, flush=True)
        print("--retain-unselected-types %s" % str(retain_unselected_types), file=error_file, flush=True)
        if type_names is not None:
            print("--types %s" % " ".join(type_names), file=error_file, flush=True)
        if without_fields is not None:
            print("--without %s" % " ".join(without_fields), file=error_file, flush=True)
        print("--show-data-types %s" % str(show_data_types), file=error_file, flush=True)
        print("--quiet %s" % str(quiet), file=error_file, flush=True)
        print("--build-id=%s" % str(build_id), file=error_file, flush=True)
        idbuilder_options.show(out=error_file)
        reader_options.show(out=error_file)
        value_options.show(out=error_file)
        print("=======", file=error_file, flush=True)
    if show_data_types:
        data_type: str
        for data_type in KgtkFormat.DataType.choices():
            print("%s" % data_type, file=error_file, flush=True)
        return 0

    wf: typing.List[str] = without_fields if without_fields is not None else list()

    try:
        ex: KgtkImplode = KgtkImplode(
            input_file_path=input_kgtk_file,
            output_file_path=output_kgtk_file,
            reject_file_path=reject_kgtk_file,
            column_name=column_name,
            prefix=prefix,
            type_names=type_names,
            without_fields=wf,
            overwrite_column=overwrite_column,
            validate=validate,
            escape_pipes=escape_pipes,
            quantities_include_numbers=quantities_include_numbers,
            general_strings=general_strings,
            remove_prefixed_columns=remove_prefixed_columns,
            ignore_unselected_types=ignore_unselected_types,
            retain_unselected_types=retain_unselected_types,
            quiet=quiet,
            build_id=build_id,
            idbuilder_options=idbuilder_options,
            reader_options=reader_options,
            value_options=value_options,
            error_file=error_file,
            verbose=verbose,
            very_verbose=very_verbose)

        ex.process()

        return 0

    except SystemExit as e:
        raise KGTKException("Exit requested")
    except Exception as e:
        raise KGTKException(str(e))

