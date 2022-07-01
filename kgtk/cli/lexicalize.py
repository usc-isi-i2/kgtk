# text embedding lexicalization.
#
# TODO: Provide seperate KgtkReader options (with fallback) for
# the entity label files, and the main input files.
#
# Approach:
# The input file is assumed to be sorted by node1 value (lowest to highest).
# Read each group of records with the same node1 value and construct
# an English sentence that describes the entity and its properties.
#
# Processing an entity may need English labels for the relationships (label column)
# and other entities (node2 column) to which it is related. The lable values must
# be loaded into memory first.  This can be accomplished by splitting the English labels
# into a separate file and passing it to  --entity-label-file, or by reading
# the input file twice (once as --input-file and once as --entity-label-file, both
# of which must be specified on the command line).
#
from argparse import Namespace
import typing

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles

DEFAULT_LABEL_PROPERTIES: typing.List[str] = ["label"]
DEFAULT_DESCRIPTION_PROPERTIES: typing.List[str] = ["description"]
DEFAULT_ISA_PROPERTIES: typing.List[str] = ["P21", "P31", "P39", "P106", "P279"]
DEFAULT_HAS_PROPERTIES: typing.List[str] = []
DEFAULT_PROPERTY_VALUES: typing.List[str] = ["P17"]
DEFAULT_SENTENCE_LABEL: str = "sentence"
DEFAULT_LANGUAGE: str = "en"

OUTPUT_COLUMNS: typing.List[str] = ["node1", "label", "node2"]


def parser():
    return {
        'help': """Produce sentences from a KGTK file."""
    }


def add_arguments_extended(parser: KGTKArgumentParser, parsed_shared_args: Namespace):
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions, KgtkReaderMode
    from kgtk.utils.argparsehelpers import optional_bool
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    _expert: bool = parsed_shared_args._expert

    parser.add_input_file()
    parser.add_input_file(who="The entity label file(s)",
                          dest="entity_label_files",
                          options=['--entity-label-file'],
                          metavar="ENTITY_LABEL_FILE",
                          optional=True,
                          allow_list=True,
                          default_stdin=False)
    parser.add_output_file()

    parser.add_argument("--label-properties", dest="label_properties", nargs="*",
                        help="The label properties. (default=%s)" % repr(DEFAULT_LABEL_PROPERTIES))

    parser.add_argument("--description-properties", dest="description_properties", nargs="*",
                        help="The description properties. (default=%s)" % repr(DEFAULT_DESCRIPTION_PROPERTIES))

    parser.add_argument("--language", dest="language", nargs="*",
                        help="The label and description language. (default=%s)" % repr(DEFAULT_LANGUAGE))

    parser.add_argument("--isa-properties", dest="isa_properties", nargs="*",
                        help="The isa properties. (default=%s)" % repr(DEFAULT_ISA_PROPERTIES))

    parser.add_argument("--has-properties", dest="has_properties", nargs="*",
                        help="The has properties. (default=%s)" % repr(DEFAULT_HAS_PROPERTIES))

    parser.add_argument("--property-values", dest="property_values", nargs="*",
                        help="The property values. (default=%s)" % repr(DEFAULT_PROPERTY_VALUES))

    parser.add_argument('--sentence-label', action='store', type=str, dest='sentence_label',
                        default=DEFAULT_SENTENCE_LABEL,
                        help="The relationship to write in the output file. (default=%(default)s)")

    parser.add_argument("--explain", dest="explain", metavar="True|False",
                        help="When true, include an explanation column that tells how the sentence was constructed. "
                             "(default=%(default)s).",
                        type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument("--presorted", dest="presorted", metavar="True|False",
                        help="When true, the input file is presorted on node1. (default=%(default)s).",
                        type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument("--add-entity-labels-from-input", dest="add_entity_labels_from_input", metavar="True|False",
                        help="When true, extract entity labels from the unsorted input file. (default=%(default)s).",
                        type=optional_bool, nargs='?', const=True, default=False)

    KgtkReader.add_debug_arguments(parser, expert=False)
    KgtkReaderOptions.add_arguments(parser,
                                    mode_options=True,
                                    default_mode=KgtkReaderMode[parsed_shared_args._mode],
                                    expert=_expert)
    KgtkValueOptions.add_arguments(parser, expert=False)


def run(input_file: KGTKFiles,
        entity_label_files: KGTKFiles,
        output_file: KGTKFiles,

        label_properties: typing.Optional[typing.List[str]],
        description_properties: typing.Optional[typing.List[str]],
        isa_properties: typing.Optional[typing.List[str]],
        has_properties: typing.Optional[typing.List[str]],
        property_values: typing.Optional[typing.List[str]],
        sentence_label: str,
        language: str,
        explain: bool,
        presorted: bool,
        add_entity_labels_from_input: bool,

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

    from kgtk.exceptions import KGTKException

    from kgtk.gt.lexicalize_utils import Lexicalize

    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
    from kgtk.io.kgtkwriter import KgtkWriter
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    input_kgtk_file: Path = KGTKArgumentParser.get_input_file(input_file)
    entity_label_kgtk_files: typing.List[Path] = KGTKArgumentParser.get_input_file_list(entity_label_files,
                                                                                        who="The entity label file(s)",
                                                                                        default_stdin=False)
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

    if language is None:
        language = DEFAULT_LANGUAGE

    # Show the final option structures for debugging and documentation.
    if show_options:
        print("--input-file=%s" % str(input_kgtk_file), file=error_file, flush=True)
        if len(entity_label_kgtk_files) > 0:
            print("--entity-label-files %s" % " ".join([str(f) for f in entity_label_kgtk_files]), file=error_file,
                  flush=True)
        print("--output-file=%s" % str(output_kgtk_file), file=error_file, flush=True)
        print("--language=%s" % str(language), file=error_file, flush=True)

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

        print("--sentence-label=%s" % str(sentence_label), file=error_file, flush=True)
        print("--explain=%s" % str(explain), file=error_file, flush=True)
        print("--presorted=%s" % str(presorted), file=error_file, flush=True)

        reader_options.show(out=error_file)
        value_options.show(out=error_file)
        print("=======", file=error_file, flush=True)

    lexer: Lexicalize = Lexicalize(label_properties,
                                   description_properties,
                                   isa_properties,
                                   has_properties,
                                   property_values,
                                   sentence_label,
                                   language=language,
                                   explain=explain,
                                   error_file=error_file,
                                   verbose=verbose,
                                   very_verbose=very_verbose)
    if len(entity_label_kgtk_files) > 0:
        lexer.load_entity_label_files(entity_label_kgtk_files,
                                      error_file,
                                      reader_options,
                                      value_options,
                                      label_properties=label_properties,
                                      verbose=verbose)

    kr: typing.Optional[KgtkReader] = None
    kw: typing.Optional[KgtkWriter] = None

    try:
        if verbose:
            print("Opening the input file %s" % str(input_kgtk_file), file=error_file, flush=True)
        kr = KgtkReader.open(input_kgtk_file,
                             options=reader_options,
                             value_options=value_options,
                             error_file=error_file,
                             verbose=verbose,
                             very_verbose=very_verbose,
                             )

        if kr.node1_column_idx < 0:
            raise KGTKException("Missing column: node1 or alias")
        if kr.label_column_idx < 0:
            raise KGTKException("Missing column: label or alias")
        if kr.node2_column_idx < 0:
            raise KGTKException("Missing column: node2 or alias")

        if verbose:
            print("node1 column index = {}".format(kr.node1_column_idx), file=error_file, flush=True)
            print("label column index = {}".format(kr.label_column_idx), file=error_file, flush=True)
            print("node2 column index = {}".format(kr.node2_column_idx), file=error_file, flush=True)

        output_columns: typing.List[str] = OUTPUT_COLUMNS.copy()
        if explain:
            output_columns.append("explanation")
            if verbose:
                print("Including an explanation column in the output.", file=error_file, flush=True)

        if verbose:
            print("Opening the output file %s" % str(output_kgtk_file), file=error_file, flush=True)
        kw = KgtkWriter.open(output_columns,
                             output_kgtk_file,
                             require_all_columns=True,
                             prohibit_extra_columns=True,
                             fill_missing_columns=False,
                             gzip_in_parallel=False,
                             verbose=verbose,
                             very_verbose=very_verbose,
                             )

        if presorted:
            lexer.process_presorted_input(kr, kw)
        else:
            lexer.process_unsorted_input(kr, kw, add_entity_labels=add_entity_labels_from_input)

        return 0

    except Exception as e:
        raise KGTKException(str(e))

    finally:
        if kw is not None:
            kw.close()

        if kr is not None:
            kr.close()
