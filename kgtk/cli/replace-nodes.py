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

    parser.add_argument(      "--confidence-column", dest="confidence_column_name",
                              help=h("The name of the confidence column.  (default=%(default)s)"),
                              default="confidence")

    parser.add_argument(      "--require-confidence", dest="require_confidence",
                              help=h("If true, require a confidence column with non-empty values. (default=%(default)s)."),
                              metavar="True/False",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--default-confidence-value", dest="default_confidence_str",
                              help=h("The default confidence value when the confidence column is missing " +
                                     "or a mapping edge does not have a confidence value. (default=None)"))
    
    parser.add_argument(      "--threshold", dest="confidence_threshold",
                              help="The minimum acceptable confidence value. Mapping records with a lower" +
                              " confidence value are excluded. (default=%(default)f)",
                              type=float, default=1.0)
    
    parser.add_argument(      "--same-as-item-label", dest="same_as_item_label",
                              help=h("The name of the mapping property for mapping the node1 and node2 columns.  (default=%(default)s)"),
                              default="same_as_item")

    parser.add_argument(      "--same-as-property-label", dest="same_as_property_label",
                              help=h("The name of the mapping property for mapping the label column.  (default=%(default)s)"),
                              default="same_as_property")

    parser.add_argument(      "--allow-exact-duplicates", dest="allow_exact_duplicates",
                              help=h("When True, allow duplicate mapping entries with the same node2 values.  (default=%(default)s)"),
                              metavar="True/False",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--allow-idempotent-mapping", dest="allow_idempotent_mapping",
                              help=h("When True, allow mapping entries having node1 == node2. Otherwise, filter them out.  (default=%(default)s)"),
                              metavar="True/False",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--split-output-mode", dest="split_output_mode",
                              help="If true, send only modified edges to the output file. (default=%(default)s).",
                              metavar="True/False",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--modified-pattern", dest="modified_pattern",
                              help=h("A pattern that defines a significant edge modifications.  (default=%(default)s)"),
                              default="node1|label|node2")

    parser.add_argument(      "--node1-column", dest="node1_column_name",
                              help=h("The name of the node1 column in the input file.  (default=node1 or its alias)"))

    parser.add_argument(      "--label-column", dest="label_column_name",
                              help=h("The name of the label column in the input file.  (default=label or its alias)"))

    parser.add_argument(      "--node2-column", dest="node2_column_name",
                              help=h("The name of the node2 column in the input file.  (default=node2 or its alias)"))

    parser.add_argument(      "--mapping-rule-mode", dest="mapping_rule_mode",
                              choices=["normal", "same-as-item", "same-as-property"],
                              help=h("Force a mapping rule mode.  (default=%(default)s"),
                              default="normal")

    parser.add_argument(      "--mapping-node1-column", dest="mapping_node1_column_name",
                              help=h("The name of the node1 column in the mapping file.  (default=node1 or its alias)"))

    parser.add_argument(      "--mapping-label-column", dest="mapping_label_column_name",
                              help=h("The name of the label column in the mapping file.  (default=label or its alias)"))

    parser.add_argument(      "--mapping-node2-column", dest="mapping_node2_column_name",
                              help=h("The name of the node2 column in the mapping file.  (default=node2 or its alias)"))

    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, expert=_expert)
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
    mapping_kgtk_file: Path = KGTKArgumentParser.get_input_file(mapping_file, who="KGTK mappping file")
    unmodified_edges_kgtk_file: typing.Optional[Path] = KGTKArgumentParser.get_optional_output_file(unmodified_edges_file, who="KGTK unmodified edges output file")
    activated_mapping_kgtk_file: typing.Optional[Path] = KGTKArgumentParser.get_optional_output_file(activated_mapping_file, who="KGTK activated mapping output file")
    rejected_mapping_kgtk_file: typing.Optional[Path] = KGTKArgumentParser.get_optional_output_file(rejected_mapping_file, who="KGTK rejected mapping output file")

    # Select where to send error messages, defaulting to stderr.
    error_file: typing.TextIO = sys.stdout if errors_to_stdout else sys.stderr

    # Build the option structures.
    input_reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs, who="input", fallback=True)
    mapping_reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs, who="mapping", fallback=True)
    value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)

    # Show the final option structures for debugging and documentation.
    if show_options:
        print("--input-file=%s" % repr(str(input_kgtk_file)), file=error_file, flush=True)
        print("--output-file=%s" % repr(str(output_kgtk_file)), file=error_file, flush=True)
        print("--mapping-file=%s" % repr(str(mapping_kgtk_file)), file=error_file, flush=True)
        if unmodified_edges_kgtk_file is not None:
            print("--unmodified-edges-file=%s" % repr(str(unmodified_edges_kgtk_file)), file=error_file, flush=True)
        if activated_mapping_kgtk_file is not None:
            print("--activated-mapping-edges-file=%s" % repr(str(activated_mapping_kgtk_file)), file=error_file, flush=True)
        if rejected_mapping_kgtk_file is not None:
            print("--rejected-mapping-edges-file=%s" % repr(str(rejected_mapping_kgtk_file)), file=error_file, flush=True)

        print("--confidence-column=%s" % repr(confidence_column_name), file=error_file, flush=True)
        print("--require-confidence=%s" % repr(require_confidence), file=error_file, flush=True)
        if default_confidence_str is not None:
            print("--default-confidence-value=%s" % default_confidence_str, file=error_file, flush=True)
        print("--threshold=%f" % confidence_threshold, file=error_file, flush=True)

        print("--same-as-item-label=%s" % repr(same_as_item_label), file=error_file, flush=True)
        print("--same-as-property-label=%s" % repr(same_as_property_label), file=error_file, flush=True)
        print("--allow-exact-duplicates=%s" % repr(allow_exact_duplicates), file=error_file, flush=True)
        print("--allow-idempotent-actions=%s" % repr(allow_idempotent_mapping), file=error_file, flush=True)

        print("--split-output-mode=%s" % repr(split_output_mode), file=error_file, flush=True)
        print("--modified-pattern=%s" % repr(modified_pattern), file=error_file, flush=True)

        if node1_column_name is not None:
            print("--node1-column-=%s" % repr(node1_column_name), file=error_file, flush=True)
        if label_column_name is not None:
            print("--label-column-=%s" % repr(label_column_name), file=error_file, flush=True)
        if node2_column_name is not None:
            print("--node2-column-=%s" % repr(node2_column_name), file=error_file, flush=True)
        print("--mapping-rule-mode=%s" % repr(mapping_rule_mode), file=error_file, flush=True)
        if mapping_node1_column_name is not None:
            print("--mapping-node1-column-=%s" % repr(mapping_node1_column_name), file=error_file, flush=True)
        if mapping_label_column_name is not None:
            print("--mapping-label-column-=%s" % repr(mapping_label_column_name), file=error_file, flush=True)
        if mapping_node2_column_name is not None:
            print("--mapping-node2-column-=%s" % repr(mapping_node2_column_name), file=error_file, flush=True)

        input_reader_options.show(out=error_file, who="input")
        mapping_reader_options.show(out=error_file, who="mapping")
        value_options.show(out=error_file)
        print("=======", file=error_file, flush=True)

    default_confidence_value: typing.Optional[float] = None
    if default_confidence_str is not None:
        try:
            default_confidence_value = float(default_confidence_str)
        except:
            raise KGTKException("--default-confidence-value=%s is invalid" % repr(default_confidence_str))

    try:

        if verbose:
            print("Opening the mapping file %s." % repr(str(mapping_kgtk_file)), file=error_file, flush=True)
        mkr:  KgtkReader = KgtkReader.open(mapping_kgtk_file,
                                           options=mapping_reader_options,
                                           value_options = value_options,
                                           error_file=error_file,
                                           verbose=verbose,
                                           very_verbose=very_verbose,
        )
        trouble = False
        mapping_node1_idx: int = mkr.get_node1_column_index(mapping_node1_column_name)
        mapping_label_idx: int = mkr.get_label_column_index(mapping_label_column_name)
        mapping_node2_idx: int = mkr.get_node2_column_index(mapping_node2_column_name)
        if mapping_node1_idx < 0:
            trouble = True
            print("Error: Cannot find the mapping file node1 column.", file=error_file, flush=True)
        if mapping_label_idx < 0 and mapping_rule_mode == "normal":
            trouble = True
            print("Error: Cannot find the mapping file label column.", file=error_file, flush=True)
        if mapping_node2_idx < 0:
            trouble = True
            print("Error: Cannot find the mapping file node2 column.", file=error_file, flush=True)
        if trouble:
            # Clean up:                                                                                                                                               
            mkr.close()
            raise KGTKException("Missing columns in the mapping file.")
        confidence_column_idx: int = mkr.column_name_map.get(confidence_column_name, -1)
        if require_confidence and confidence_column_idx < 0:
            mkr.close()
            raise KGTKException("The mapping file does not have a confidence column, and confidence is required.")
        
        rmkw: typing.Optional[KgtkWriter] = None
        if rejected_mapping_kgtk_file is not None:
            if verbose:
                print("Opening the rejected mapping edges file %s." % repr(str(rejected_mapping_kgtk_file)), file=error_file, flush=True)
            rmkw = KgtkWriter.open(mkr.column_names,
                                   rejected_mapping_kgtk_file,
                                   mode=KgtkWriter.Mode[mkr.mode.name],
                                   use_mgzip=input_reader_options.use_mgzip, # Hack!
                                   mgzip_threads=input_reader_options.mgzip_threads, # Hack!
                                   error_file=error_file,
                                   verbose=verbose,
                                   very_verbose=very_verbose)

        # Mapping structures:
        item_map: typing.MutableMapping[str, str] = dict()
        item_line_map: typing.MutableMapping[str, int] = dict()
        property_map: typing.MutableMapping[str, str] = dict()
        property_line_map: typing.MutableMapping[str, int] = dict()

        mapping_rows: typing.MutableMapping[int, typing.List[str]] = dict()
        activated_mapping_rows: typing.MutableMapping[int, typing.List[str]] = dict()

        # Read the mapping file.
        if verbose:
            print("Processing the mapping file.", file=error_file, flush=True)
        mapping_confidence_exclusions: int = 0
        mapping_idempotent_exclusions: int = 0
        mapping_errors: int = 0
        mapping_line_number: int = 0
        mrow: typing.List[str]
        for mrow in mkr:
            mapping_line_number += 1
            mapping_node1: str = mrow[mapping_node1_idx]
            mapping_label: str = mrow[mapping_label_idx] if mapping_rule_mode == "normal" else ""
            mapping_node2: str = mrow[mapping_node2_idx]
            mapping_confidence: typing.Optional[float] = default_confidence_value
            if confidence_column_idx >= 0:
                confidence_value_str: str = mrow[confidence_column_idx]
                if len(confidence_value_str) == 0:
                    if require_confidence:
                        print("In line %d of the mapping file: the required confidence value is missing" % (mapping_line_number),
                              file=error_file, flush=True)
                        mapping_errors += 1
                        continue
                else:
                    try:
                        mapping_confidence = float(confidence_value_str)
                    except ValueError:
                        print("In line %d of the mapping file: cannot parse confidence value %s" % (mapping_line_number, repr(mrow[confidence_column_idx])),
                              file=error_file, flush=True)
                        mapping_errors += 1
                        continue
            if mapping_confidence is not None and mapping_confidence < confidence_threshold:
                mapping_confidence_exclusions += 1
                if rmkw is not None:
                    rmkw.write(mrow)
                continue

            if mapping_node1 == mapping_node2 and not allow_idempotent_mapping:
                mapping_idempotent_exclusions += 1
                continue
        
            if mapping_rule_mode == "same-as-item" or mapping_label == same_as_item_label:
                if mapping_node1 in item_map:
                    if mapping_node2 != item_map[mapping_node1] or not allow_exact_duplicates:
                        print("Duplicate %s for %s at mapping file line %d, originally in line %d" % (mapping_label,
                                                                                                      repr(mapping_node1),
                                                                                                      mapping_line_number,
                                                                                                      item_line_map[mapping_node1]),
                              file=error_file, flush=True)
                        mapping_errors += 1
                    continue

                item_map[mapping_node1] = mapping_node2
                item_line_map[mapping_node1] = mapping_line_number
                mapping_rows[mapping_line_number] = mrow.copy()

            elif mapping_rule_mode == "same-as-property" or mapping_label == same_as_property_label:
                if mapping_node1 in property_map:
                    if mapping_node2 != property_map[mapping_node1] or not allow_exact_duplicates:
                        print("Duplicate %s for %s at mapping file line %d, originally in line %d" % (mapping_label,
                                                                                                      repr(mapping_node1),
                                                                                                      mapping_line_number,
                                                                                                      property_line_map[mapping_node1]),
                              file=error_file, flush=True)
                        mapping_errors += 1
                    continue
                property_map[mapping_node1] = mapping_node2
                property_line_map[mapping_node1] = mapping_line_number
                mapping_rows[mapping_line_number] = mrow.copy()

            else:
                print("Unknown mapping action %s at line %d of mapping file %s" % (mapping_label,
                                                                                   mapping_line_number,
                                                                                   repr(str(mapping_kgtk_file))),
                      file=error_file, flush=True)
                mapping_errors += 1
                continue
                

        # Close the mapping file.
        mkr.close()
        if rmkw is not None:
            rmkw.close()

        if mapping_errors > 0:
            raise KGTKException("%d errors detected in the mapping file %s" % (mapping_errors, repr(str(mapping_kgtk_file))))

        if len(item_map) == 0 and len(property_map) == 0:
            raise KGTKException("Nothing read from the mapping file %s" % repr(str(mapping_kgtk_file)))

        if verbose:
            print("%d mapping lines, %d excluded for confidence, %d excluded for idempotency." % (mapping_line_number,
                                                                                                  mapping_confidence_exclusions,
                                                                                                  mapping_idempotent_exclusions),
                  file=error_file, flush=True)
            print("%d item mapping rules." % len(item_map), file=error_file, flush=True)
            print("%d property mapping rules." % len(property_map), file=error_file, flush=True)

        if verbose:
            print("Opening the input file %s." % repr(str(input_kgtk_file)), file=error_file, flush=True)
        ikr:  KgtkReader = KgtkReader.open(input_kgtk_file,
                                           options=input_reader_options,
                                           value_options = value_options,
                                           error_file=error_file,
                                           verbose=verbose,
                                           very_verbose=very_verbose,
        )
        trouble = False
        input_node1_idx: int = ikr.get_node1_column_index(node1_column_name)
        input_label_idx: int = ikr.get_label_column_index(label_column_name)
        input_node2_idx: int = ikr.get_node2_column_index(node2_column_name)
        if input_node1_idx < 0 and mapping_rule_mode in ["normal", "same-as-item"]:
            trouble = True
            print("Error: Cannot find the input file node1 column.", file=error_file, flush=True)
        if input_label_idx < 0 and mapping_rule_mode in ["normal", "same-as-property"]:
            trouble = True
            print("Error: Cannot find the input file label column.", file=error_file, flush=True)
        if input_node2_idx < 0 and mapping_rule_mode in ["normal", "same-as-item"]:
            trouble = True
            print("Error: Cannot find the input file node2 column.", file=error_file, flush=True)
        if trouble:
            # Clean up:                                                                                                                                               
            ikr.close()
            raise KGTKException("Missing columns in the input file.")

        okw: KgtkWriter = KgtkWriter.open(ikr.column_names,
                                          output_kgtk_file,
                                          mode=KgtkWriter.Mode[ikr.mode.name],
                                          use_mgzip=input_reader_options.use_mgzip, # Hack!
                                          mgzip_threads=input_reader_options.mgzip_threads, # Hack!
                                          error_file=error_file,
                                          verbose=verbose,
                                          very_verbose=very_verbose)

        uekw: typing.Optional[KgtkWriter] = None
        if unmodified_edges_kgtk_file is not None:
            if verbose:
                print("Opening the unmodified edges file %s." % repr(str(unmodified_edges_kgtk_file)), file=error_file, flush=True)
            uekw = KgtkWriter.open(ikr.column_names,
                                   unmodified_edges_kgtk_file,
                                   mode=KgtkWriter.Mode[ikr.mode.name],
                                   use_mgzip=input_reader_options.use_mgzip, # Hack!
                                   mgzip_threads=input_reader_options.mgzip_threads, # Hack!
                                   error_file=error_file,
                                   verbose=verbose,
                                   very_verbose=very_verbose)

        amkw: typing.Optional[KgtkWriter] = None
        if activated_mapping_kgtk_file is not None:
            if verbose:
                print("Opening the activated mapping edges file %s." % repr(str(activated_mapping_kgtk_file)), file=error_file, flush=True)
            amkw = KgtkWriter.open(mkr.column_names,
                                   activated_mapping_kgtk_file,
                                   mode=KgtkWriter.Mode[mkr.mode.name],
                                   use_mgzip=input_reader_options.use_mgzip, # Hack!
                                   mgzip_threads=input_reader_options.mgzip_threads, # Hack!
                                   error_file=error_file,
                                   verbose=verbose,
                                   very_verbose=very_verbose)

        # Process each row of the input file.
        if verbose:
            print("Processing the input file.", file=error_file, flush=True)
        input_count: int = 0
        modified_edge_count: int = 0
        unmodified_edge_count: int = 0
        row: typing.List[str]
        for row in ikr:
            input_count +=1
            newrow: typing.List[str] = row.copy()

            modified_node1: bool = False
            modified_node2: bool = False
            modified_label: bool = False

            if mapping_rule_mode in ["normal", "same-as-item"]:
                input_node1: str = row[input_node1_idx]
                if input_node1 in item_map:
                    newrow[input_node1_idx] = item_map[input_node1]
                    modified_node1 = True
                    if amkw is not None:
                        mapping_line_number = item_line_map[input_node1]
                        if mapping_line_number not in activated_mapping_rows:
                            activated_mapping_rows[mapping_line_number] = mapping_rows[mapping_line_number]
                        
                input_node2: str = row[input_node2_idx]
                if input_node2 in item_map:
                    newrow[input_node2_idx] = item_map[input_node2]
                    modified_node2 = True
                    if amkw is not None:
                        mapping_line_number = item_line_map[input_node2]
                        if mapping_line_number not in activated_mapping_rows:
                            activated_mapping_rows[mapping_line_number] = mapping_rows[mapping_line_number]

            if mapping_rule_mode in ["normal", "same-as-property"]:
                input_label: str = row[input_label_idx]
                if input_label in property_map:
                    newrow[input_label_idx] = property_map[input_label]
                    modified_label = True
                    if amkw is not None:
                        mapping_line_number = property_line_map[input_label]
                        if mapping_line_number not in activated_mapping_rows:
                            activated_mapping_rows[mapping_line_number] = mapping_rows[mapping_line_number]

            modified: bool
            if modified_pattern == "node1|label|node2":
                modified = modified_node1 or modified_label or modified_node2
            elif modified_pattern == "node1|label":
                modified = modified_node1 or modified_label
            elif modified_pattern == "node1|node2":
                modified = modified_node1 or modified_node2
            elif modified_pattern == "label|node2":
                modified = modified_label or modified_node2
            elif modified_pattern == "node1":
                modified = modified_node1
            elif modified_pattern == "label":
                modified = modified_label
            elif modified_pattern == "node2":
                modified = modified_node2
            elif modified_pattern == "node1&label&node2":
                modified = modified_node1 and modified_label and modified_node2
            elif modified_pattern == "node1&label":
                modified = modified_node1 and modified_label
            elif modified_pattern == "node1&node2":
                modified = modified_node1 and modified_node2
            elif modified_pattern == "label&node2":
                modified = modified_label and modified_node2
            else:
                raise KGTKException("Unrecognized modification test pattern %s" % repr(modified_pattern))                

            if modified:
                modified_edge_count += 1
                okw.write(newrow)
            else:
                unmodified_edge_count += 1
                if uekw is not None:
                    uekw.write(row)
                if not split_output_mode:
                    okw.write(row)
                        
        # Done!
        ikr.close()
        okw.close()

        if verbose:
            print("%d edges read. %d modified, %d unmodified." % (input_count, modified_edge_count, unmodified_edge_count), file=error_file, flush=True)

        if uekw is not None:
            uekw.close()

        if amkw is not None:
            activated_count: int = 0
            for mapping_line_number in sorted(activated_mapping_rows.keys()):
                amkw.write(activated_mapping_rows[mapping_line_number])
                activated_count += 1
            amkw.close()

            if verbose:
                print("%d activated mapping edges" % activated_count, file=error_file, flush=True)

        return 0

    except SystemExit as e:
        raise KGTKException("Exit requested")
    except Exception as e:
        raise KGTKException(str(e))

