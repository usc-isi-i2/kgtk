# text embedding.
#
# TODO: Use KgtkReader to read the property values file.
#
# TODO: Provide seperate KgtkReader options (with fallback) for
# property labels, property values, and the main input files
# read by EmbeddingVector in "gt/embeddng_utils.py".
#
# TODO: Convert EmbeddingVector to use KgtkFormat and KgtkWriter.
#
from argparse import Namespace, SUPPRESS
import typing

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles

DEFAULT_LABEL_PROPERTIES: typing.List[str] = [ "label" ]
DEFAULT_DESCRIPTION_PROPERTIES: typing.List[str] = [ "description" ]
DEFAULT_ISA_PROPERTIES: typing.List[str] = [ "P21", "P31", "P39", "P106", "P279" ]
DEFAULT_HAS_PROPERTIES: typing.List[str] = [ ]
DEFAULT_PROPERTY_VALUES: typing.List[str] = [ "P17" ]
DEFAULT_METADATA_PROPERTIES: typing.List[str] = [ "label", "P31"]

OUTPUT_COLUMNS: typing.List[str] = [ "node1", "label", "node2" ]

def parser():
    return {
        'help': """Produce sentences from a KGTK file."""
    }


def add_arguments_extended(parser: KGTKArgumentParser, parsed_shared_args: Namespace ):

    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
    from kgtk.utils.argparsehelpers import optional_bool
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    _expert: bool = parsed_shared_args._expert

    parser.add_input_file()
    parser.add_output_file()

    parser.add_argument("--label-properties", dest="label_properties", nargs="*",
                        help="The label properties. (default=%s)" % repr(DEFAULT_LABEL_PROPERTIES))

    parser.add_argument("--description-properties", dest="description_properties", nargs="*",
                        help="The description properties. (default=%s)" % repr(DEFAULT_DESCRIPTION_PROPERTIES))

    parser.add_argument("--isa-properties", dest="isa_properties", nargs="*",
                        help="The isa properties. (default=%s)" % repr(DEFAULT_ISA_PROPERTIES))

    parser.add_argument("--has-properties", dest="has_properties", nargs="*",
                        help="The has properties. (default=%s)" % repr(DEFAULT_HAS_PROPERTIES))

    parser.add_argument("--property-values", dest="property_values", nargs="*",
                        help="The property values. (default=%s)" % repr(DEFAULT_PROPERTY_VALUES))

    parser.add_argument("--metadata-properties", dest="metadata_properties", nargs="*",
                        help="The metadata properties. (default=%s)" % repr(DEFAULT_METADATA_PROPERTIES))

    KgtkReader.add_debug_arguments(parser, expert=False)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, expert=False)
    KgtkValueOptions.add_arguments(parser, expert=False)


def run(input_file: KGTKFiles,
        output_file: KGTKFiles,

        label_properties: typing.Optional[typing.List[str]],
        description_properties: typing.Optional[typing.List[str]],
        isa_properties: typing.Optional[typing.List[str]],
        has_properties: typing.Optional[typing.List[str]],
        property_values: typing.Optional[typing.List[str]],
        metadata_properties: typing.Optional[typing.List[str]],

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

    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
    from kgtk.io.kgtkwriter import KgtkWriter
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    input_kgtk_file: Path = KGTKArgumentParser.get_input_file(input_file)
    output_kgtk_file: Path = KGTKArgumentParser.get_output_file(output_file)

    # Select where to send error messages, defaulting to stderr.
    error_file: typing.TextIO = sys.stdout if errors_to_stdout else sys.stderr

    # Build the option structures.
    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs)
    value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)

    if label_properties is None:
        label_properties = DEFAULT_LABEL_PROPERTIES

    if description_properties is None:
        description_properties = DEFAULT_DESCRIPTION_PROPERTIES

    if isa_properties is None:
        isa_properties = DEFAULT_ISA_PROPERTIES

    if has_properties is None:
        has_properties = DEFAULT_HAS_PROPERTIES

    if property_values is None:
        property_values = DEFAULT_PROPERTY_VALUES

    if metadata_properties is None:
        metadata_properties = DEFAULT_METADATA_PROPERTIES

    # Show the final option structures for debugging and documentation.
    if show_options:
        print("--input-file=%s" % str(input_kgtk_file), file=error_file, flush=True)
        print("--output-file=%s" % str(output_kgtk_file), file=error_file, flush=True)

        if len(label_properties) > 0:
            print("--label-properties %s" % " ".join(label_properties), file=error_file, flush=True)

        if len(description_properties) > 0:
            print("--description-properties %s" % " ".join(description_properties), file=error_file, flush=True)

        if len(isa_properties) > 0:
            print("--isa-properties %s" % " ".join(isa_properties), file=error_file, flush=True)

        if len(has_properties) > 0:
            print("--has-properties %s" % " ".join(has_properties), file=error_file, flush=True)

        if len(property_values) > 0:
            print("--property-values %s" % " ".join(property_values), file=error_file, flush=True)

        if len(metadata_properties) > 0:
            print("--metadata-properties %s" % " ".join(metadata_properties), file=error_file, flush=True)

        reader_options.show(out=error_file)
        value_options.show(out=error_file)
        print("=======", file=error_file, flush=True)

    kr: typing.Optional[KgtkReader] = None
    kw: typing.Optional[KgtkWriter] = None

    try:
        if verbose:
            print("Opening the input file %s" % str(input_kgtk_file), file=error_file, flush=True)
        kr = KgtkReader.open(input_kgtk_file,
                             options=reader_options,
                             value_options = value_options,
                             error_file=error_file,
                             verbose=verbose,
                             very_verbose=very_verbose,
                             )

        if verbose:
            print("Opening the output file %s" % str(output_kgtk_file), file=error_file, flush=True)
            kw: KgtkWriter = KgtkWriter.open(OUTPUT_COLUMNS,
                                             output_kgtk_file,
                                             require_all_columns=True,
                                             prohibit_extra_columns=True,
                                             fill_missing_columns=False,
                                             gzip_in_parallel=False,
                                             verbose=verbose,
                                             very_verbose=very_verbose,
                                             )


        return 0

    except Exception as e:
        raise KGTKException(str(e))

    finally:
        if kw is not None:
            kw.close()
            
        if kr is not None:
            kr.close()
