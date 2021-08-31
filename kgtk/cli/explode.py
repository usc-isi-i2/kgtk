"""Copy records from the first KGTK file to the output file,
expanding one column (usualy node2) into seperate columns for each subfield.

TODO: Need KgtkWriterOptions
"""

from argparse import _MutuallyExclusiveGroup, Namespace, SUPPRESS
import typing

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles

def parser():
    return {
        'aliases': ['denormalize_node2'],
        'help': 'Copy a KGTK file, exploding one column (usualy node2) into seperate columns for each subfield.',
        'description': 'Copy a KGTK file, exploding one column (usually node2) into seperate columns for each subfield. ' +
        'If a cell in the column being exploded contains a list, that record is optionally expanded into multiple records ' +
        'before explosion, with all other columns copied-as is.' +
        '\n\nAdditional options are shown in expert help.\nkgtk --expert explode --help'
    }


def add_arguments_extended(parser: KGTKArgumentParser, parsed_shared_args: Namespace):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """
    from kgtk.kgtkformat import KgtkFormat
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
    from kgtk.io.kgtkwriter import KgtkWriter
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

    parser.add_argument(      "--column", dest="column_name", help="The name of the column to explode. (default=%(default)s).", default=KgtkFormat.NODE2)

    fgroup: _MutuallyExclusiveGroup = parser.add_mutually_exclusive_group()
    fgroup.add_argument(      "--types", dest="type_names", nargs='*',
                              help="The KGTK data types for which fields should be exploded. (default=%(default)s).",
                              choices=KgtkFormat.DataType.choices(),
                              default=KgtkFormat.DataType.choices())

    fgroup.add_argument(      "--fields", dest="field_names", nargs='*', 
                              help=h("The names of the fields to extract (overrides --types). (default=%(default)s)."),
                              choices=KgtkValueFields.FIELD_NAMES)

    parser.add_argument(      "--prefix", dest="prefix", help="The prefix for exploded column names. (default=%(default)s).",
                              default=KgtkFormat.NODE2 + ";" + KgtkFormat.KGTK_NAMESPACE)

    parser.add_argument(      "--overwrite", dest="overwrite_columns", metavar="True|False",
                              help="Indicate that it is OK to overwrite existing columns. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--expand", dest="expand_list", metavar="True|False",
                              help="When True, expand source cells that contain a lists, else fail if a source cell contains a list. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--show-data-types", dest="show_data_types", metavar="True|False",
                              help="Print the list of data types and exit. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--show-field-names", dest="show_field_names", metavar="True|False",
                              help="Print the list of field names and exit. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--show-field-formats", dest="show_field_formats", metavar="True|False",
                              help="Print the list of field names and formats, then exit. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--output-format", dest="output_format", help="The file format (default=kgtk)", type=str,
                              choices=KgtkWriter.OUTPUT_FORMAT_CHOICES)

    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, expert=_expert)
    KgtkValueOptions.add_arguments(parser, expert=_expert)

def run(input_file: KGTKFiles,
        output_file:KGTKFiles,
        column_name: str,
        type_names: typing.List[str],
        field_names: typing.List[str],
        prefix: str,
        overwrite_columns: bool,
        expand_list: bool,
        show_data_types: bool,
        show_field_names: bool,
        show_field_formats: bool,
        output_format: typing.Optional[str],
        
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
    from kgtk.reshape.kgtkexplode import KgtkExplode
    from kgtk.value.kgtkvalue import KgtkValueFields
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
        print("--column %s" % column_name, file=error_file, flush=True)
        print("--prefix %s" % prefix, file=error_file, flush=True)
        print("--overwrite %s" % str(overwrite_columns), file=error_file, flush=True)
        print("--expand %s" % str(expand_list), file=error_file, flush=True)
        if type_names is not None:
            print("--types %s" % " ".join(type_names), file=error_file, flush=True)
        if field_names is not None:
            print("--fields %s" % " ".join(field_names), file=error_file, flush=True)
        print("--show-data-types %s" % str(show_data_types), file=error_file, flush=True)
        print("--show-field-names %s" % str(show_field_names), file=error_file, flush=True)
        print("--show-field-formats %s" % str(show_field_formats), file=error_file, flush=True)
        if output_format is not None:
            print("--output-format=%s" % output_format, file=error_file, flush=True)
        reader_options.show(out=error_file)
        value_options.show(out=error_file)
        print("=======", file=error_file, flush=True)

    if show_data_types:
        data_type: str
        for data_type in KgtkFormat.DataType.choices():
            print("%s" % data_type, file=error_file, flush=True)
        return 0

    field_name: str
    if show_field_names:
        for field_name in sorted(KgtkValueFields.FIELD_NAMES):
            print("%s" % field_name, file=error_file, flush=True)
        return 0

    if show_field_formats:
        for field_name in sorted(KgtkValueFields.FIELD_NAME_FORMATS.keys()):
            field_format: str = KgtkValueFields.FIELD_NAME_FORMATS[field_name]
            print("| %20s | %-5s |" % (field_name, field_format), file=error_file, flush=True)
        return 0

    try:
        ex: KgtkExplode = KgtkExplode(
            input_file_path=input_kgtk_file,
            output_file_path=output_kgtk_file,
            output_format=output_format,
            column_name=column_name,
            type_names=type_names,
            field_names=field_names,
            prefix=prefix,
            overwrite_columns=overwrite_columns,
            expand_list=expand_list,
            reader_options=reader_options,
            value_options=value_options,
            error_file=error_file,
            verbose=verbose,
            very_verbose=very_verbose,
        )
        
        ex.process()

        return 0

    except SystemExit as e:
        raise KGTKException("Exit requested")
    except Exception as e:
        raise KGTKException(str(e))

