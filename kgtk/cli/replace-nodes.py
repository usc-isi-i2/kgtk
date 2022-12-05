"""Replace symbol names to move relationships form one KG to another..

"""

from argparse import Namespace, SUPPRESS
import typing

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles


def parser():
    return {
        'help': 'Replace item and relationship identifiers in a KGTK file.',
        'description': 'Replace item and relationship values to move a network from one symbol set to another. ' +
                       '\n\nAdditional options are shown in expert help.\nkgtk --expert replace-nodes --help'
    }


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

    # This helper function makes it easy to suppress options from
    # The help message.  The options are still there, and initialize
    # what they need to initialize.
    def h(msg: str) -> str:
        if _expert:
            return msg
        else:
            return SUPPRESS

    parser.add_input_file(positional=True)
    parser.add_output_file()

    parser.add_input_file(who="A KGTK file with mapping records",
                          dest="mapping_file",
                          options=["--mapping-file"],
                          optional=False)

    parser.add_output_file(who="A KGTK output file that will contain unmodified edges.",
                           dest="unmodified_edges_file",
                           options=["--unmodified-edges-file"],
                           metavar="UNMODIFIED_EDGES_FILE",
                           optional=True)

    parser.add_output_file(who="A KGTK output file that will contain activated mapping edges.",
                           dest="activated_mapping_file",
                           options=["--activated-mapping-edges-file"],
                           metavar="ACTIVATED_MAPPING_EDGES_FILE",
                           optional=True)

    parser.add_output_file(who="A KGTK output file that will contain rejected mapping edges.",
                           dest="rejected_mapping_file",
                           options=["--rejected-mapping-edges-file"],
                           metavar="REJECTED_MAPPING_EDGES_FILE",
                           optional=True)

    parser.add_argument("--confidence-column", dest="confidence_column_name",
                        help=h("The name of the confidence column.  (default=%(default)s)"),
                        default="confidence")

    parser.add_argument("--require-confidence", dest="require_confidence",
                        help=h("If true, require a confidence column with non-empty values. (default=%(default)s)."),
                        metavar="True/False",
                        type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument("--default-confidence-value", dest="default_confidence_str",
                        help=h("The default confidence value when the confidence column is missing " +
                               "or a mapping edge does not have a confidence value. (default=None)"))

    parser.add_argument("--threshold", dest="confidence_threshold",
                        help="The minimum acceptable confidence value. Mapping records with a lower" +
                             " confidence value are excluded. (default=%(default)f)",
                        type=float, default=1.0)

    parser.add_argument("--same-as-item-label", dest="same_as_item_label",
                        help=h(
                            "The name of the mapping property for mapping the node1 and node2 columns.  (default=%(default)s)"),
                        default="same_as_item")

    parser.add_argument("--same-as-property-label", dest="same_as_property_label",
                        help=h("The name of the mapping property for mapping the label column.  (default=%(default)s)"),
                        default="same_as_property")

    parser.add_argument("--allow-exact-duplicates", dest="allow_exact_duplicates",
                        help=h(
                            "When True, allow duplicate mapping entries with the same node2 values.  (default=%(default)s)"),
                        metavar="True/False",
                        type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument("--allow-idempotent-mapping", dest="allow_idempotent_mapping",
                        help=h(
                            "When True, allow mapping entries having node1 == node2. Otherwise, filter them out.  (default=%(default)s)"),
                        metavar="True/False",
                        type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument("--split-output-mode", dest="split_output_mode",
                        help="If true, send only modified edges to the output file. (default=%(default)s).",
                        metavar="True/False",
                        type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument("--modified-pattern", dest="modified_pattern",
                        help=h("A pattern that defines a significant edge modifications.  (default=%(default)s)"),
                        default="node1|label|node2")

    parser.add_argument("--node1-column", dest="node1_column_name",
                        help=h("The name of the node1 column in the input file.  (default=node1 or its alias)"))

    parser.add_argument("--label-column", dest="label_column_name",
                        help=h("The name of the label column in the input file.  (default=label or its alias)"))

    parser.add_argument("--node2-column", dest="node2_column_name",
                        help=h("The name of the node2 column in the input file.  (default=node2 or its alias)"))

    parser.add_argument("--mapping-rule-mode", dest="mapping_rule_mode",
                        choices=["normal", "same-as-item", "same-as-property"],
                        help=h("Force a mapping rule mode.  (default=%(default)s"),
                        default="normal")

    parser.add_argument("--mapping-node1-column", dest="mapping_node1_column_name",
                        help=h("The name of the node1 column in the mapping file.  (default=node1 or its alias)"))

    parser.add_argument("--mapping-label-column", dest="mapping_label_column_name",
                        help=h("The name of the label column in the mapping file.  (default=label or its alias)"))

    parser.add_argument("--mapping-node2-column", dest="mapping_node2_column_name",
                        help=h("The name of the node2 column in the mapping file.  (default=node2 or its alias)"))

    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser,
                                    mode_options=True,
                                    default_mode=KgtkReaderMode[parsed_shared_args._mode],
                                    expert=_expert)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, who="input", expert=_expert, defaults=False)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, who="mapping", expert=_expert, defaults=False)
    KgtkValueOptions.add_arguments(parser, expert=_expert)


def run(input_file: KGTKFiles,
        output_file: KGTKFiles,
        mapping_file: KGTKFiles,
        unmodified_edges_file: KGTKFiles,
        activated_mapping_file: KGTKFiles,
        rejected_mapping_file: KGTKFiles,

        confidence_column_name: str,
        require_confidence: bool,
        default_confidence_str: typing.Optional[str],
        confidence_threshold: float,

        same_as_item_label: str,
        same_as_property_label: str,
        allow_exact_duplicates: bool,
        allow_idempotent_mapping: bool,

        split_output_mode: bool,
        modified_pattern: str,

        node1_column_name: typing.Optional[str],
        label_column_name: typing.Optional[str],
        node2_column_name: typing.Optional[str],
        mapping_rule_mode: str,
        mapping_node1_column_name: typing.Optional[str],
        mapping_label_column_name: typing.Optional[str],
        mapping_node2_column_name: typing.Optional[str],

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
    from kgtk.io.kgtkreader import KgtkReaderOptions
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions
    from kgtk.utils.replace_nodes import ReplaceNodes

    input_kgtk_file: Path = KGTKArgumentParser.get_input_file(input_file)
    output_kgtk_file: Path = KGTKArgumentParser.get_output_file(output_file)
    mapping_kgtk_file: Path = KGTKArgumentParser.get_input_file(mapping_file, who="KGTK mappping file")
    unmodified_edges_kgtk_file: typing.Optional[Path] = KGTKArgumentParser.get_optional_output_file(
        unmodified_edges_file, who="KGTK unmodified edges output file")
    activated_mapping_kgtk_file: typing.Optional[Path] = KGTKArgumentParser.get_optional_output_file(
        activated_mapping_file, who="KGTK activated mapping output file")
    rejected_mapping_kgtk_file: typing.Optional[Path] = KGTKArgumentParser.get_optional_output_file(
        rejected_mapping_file, who="KGTK rejected mapping output file")

    # Select where to send error messages, defaulting to stderr.
    error_file: typing.TextIO = sys.stdout if errors_to_stdout else sys.stderr

    # Build the option structures.
    input_reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs, who="input", fallback=True)
    mapping_reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs, who="mapping", fallback=True)
    value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)

    try:
        rr = ReplaceNodes(input_kgtk_file=input_kgtk_file,
                          output_kgtk_file=output_kgtk_file,
                          mapping_kgtk_file=mapping_kgtk_file,
                          unmodified_edges_kgtk_file=unmodified_edges_kgtk_file,
                          activated_mapping_kgtk_file=activated_mapping_kgtk_file,
                          rejected_mapping_kgtk_file=rejected_mapping_kgtk_file,
                          input_reader_options=input_reader_options,
                          mapping_reader_options=mapping_reader_options,
                          value_options=value_options,
                          confidence_column_name=confidence_column_name,
                          require_confidence=require_confidence,
                          default_confidence_str=default_confidence_str,
                          confidence_threshold=confidence_threshold,
                          same_as_item_label=same_as_item_label,
                          same_as_property_label=same_as_property_label,
                          allow_exact_duplicates=allow_exact_duplicates,
                          allow_idempotent_mapping=allow_idempotent_mapping,
                          split_output_mode=split_output_mode,
                          modified_pattern=modified_pattern,
                          node1_column_name=node1_column_name,
                          label_column_name=label_column_name,
                          node2_column_name=node2_column_name,
                          mapping_rule_mode=mapping_rule_mode,
                          mapping_node1_column_name=mapping_node1_column_name,
                          mapping_label_column_name=mapping_label_column_name,
                          mapping_node2_column_name=mapping_node2_column_name,
                          error_file=error_file,
                          show_options=show_options,
                          verbose=verbose,
                          very_verbose=very_verbose)
        rr.process()

        return 0

    except SystemExit as e:
        raise KGTKException("Exit requested")
    except Exception as e:
        raise KGTKException(str(e))
