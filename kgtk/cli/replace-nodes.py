"""Replace symbol names to move relationships form one KG to another..

"""

from argparse import Namespace, SUPPRESS
import typing

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles

def parser():
    return {
        'help': 'Lift labels from a KGTK file.',
        'description': 'Lift labels for a KGTK file. For each of the items in the (node1, label, node2) columns, look for matching label records. ' +
        'If found, lift the label values into additional columns in the current record. ' +
        'Label records are reoved from the output. ' +
        '\n\nAdditional options are shown in expert help.\nkgtk --expert lift --help'
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

    parser.add_argument(      "--confidence-column", dest="confidence_column_name",
                              help=h("The name of the confidence column.  (default=%(default)s)"),
                              default="confidence")

    parser.add_argument(      "--default-confidence-value", dest="default_confidence_value",
                              help=h("The default confidence value when the confidence column is missing " +
                                     "or a mapping edge does not have a confidence value. (default=%(default)f)"),
                              type=float, default=1.0)
    
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

    parser.add_argument(      "--split-output-mode", dest="split_output_mode",
                              help="If true, send only modified edges to the output file. (default=%(default)s).",
                              metavar="True/False",
                              type=optional_bool, nargs='?', const=True, default=True)

    KgtkReader.add_debug_arguments(parser, expert=_expert)
    # TODO: seperate reader_options for the label file.
    KgtkReaderOptions.add_arguments(parser, mode_options=True, expert=_expert)
    KgtkValueOptions.add_arguments(parser, expert=_expert)

def run(input_file: KGTKFiles,
        output_file: KGTKFiles,
        mapping_file: KGTKFiles,
        unmodified_edges_file: KGTKFiles,
        activated_mapping_file: KGTKFiles,

        confidence_column_name: str,
        default_confidence_value: float,
        confidence_threshold: float,

        same_as_item_label: str,
        same_as_property_label: str,

        split_output_mode: bool,

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

    # Select where to send error messages, defaulting to stderr.
    error_file: typing.TextIO = sys.stdout if errors_to_stdout else sys.stderr

    # Build the option structures.
    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs)
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

        print("--confidence-column=%s" % repr(confidence_column_name), file=error_file, flush=True)
        print("--default-confidence-value=%f" % default_confidence_value, file=error_file, flush=True)
        print("--threshold=%f" % confidence_threshold, file=error_file, flush=True)

        print("--same-as-item-label=%s" % repr(same_as_item_label), file=error_file, flush=True)
        print("--same-as-property-label=%s" % repr(same_as_property_label), file=error_file, flush=True)

        print("--split-output-mode=%s" % repr(split_output_mode), file=error_file, flush=True)

        reader_options.show(out=error_file)
        value_options.show(out=error_file)
        print("=======", file=error_file, flush=True)

    try:

        ikr:  KgtkReader = KgtkReader.open(input_kgtk_file,
                                           options=reader_options,
                                           value_options = value_options,
                                           error_file=error_file,
                                           verbose=verbose,
                                           very_verbose=very_verbose,
        )
        trouble: bool = False
        input_node1_idx: int = ikr.node1_column_idx
        input_label_idx: int = ikr.label_column_idx
        input_node2_idx: int = ikr.node2_column_idx
        if input_node1_idx < 0:
            trouble = True
            print("Error: Cannot find the input file node1 column.", file=error_file, flush=True)
        if input_label_idx < 0:
            trouble = True
            print("Error: Cannot find the input file label column.", file=error_file, flush=True)
        if input_node2_idx < 0:
            trouble = True
            print("Error: Cannot find the input file node2 column.", file=error_file, flush=True)
        if trouble:
            # Clean up:                                                                                                                                               
            ikr.close()
            raise KGTKException("Missing columns in the input file.")

        mkr:  KgtkReader = KgtkReader.open(mapping_kgtk_file,
                                           options=reader_options,
                                           value_options = value_options,
                                           error_file=error_file,
                                           verbose=verbose,
                                           very_verbose=very_verbose,
        )
        trouble = False
        mapping_node1_idx: int = mkr.node1_column_idx
        mapping_label_idx: int = mkr.label_column_idx
        mapping_node2_idx: int = mkr.node2_column_idx
        if mapping_node1_idx < 0:
            trouble = True
            print("Error: Cannot find the mapping file node1 column.", file=error_file, flush=True)
        if mapping_label_idx < 0:
            trouble = True
            print("Error: Cannot find the mapping file label column.", file=error_file, flush=True)
        if mapping_node2_idx < 0:
            trouble = True
            print("Error: Cannot find the mapping file node2 column.", file=error_file, flush=True)
        if trouble:
            # Clean up:                                                                                                                                               
            ikr.close()
            mkr.close()
            raise KGTKException("Missing columns in the mapping file.")
        confidence_column_idx: int = mkr.column_name_map.get(confidence_column_name, -1)
        
        okw: KgtkWriter = KgtkWriter.open(ikr.column_names,
                                          output_kgtk_file,
                                          mode=KgtkWriter.Mode[ikr.mode.name],
                                          use_mgzip=reader_options.use_mgzip, # Hack!
                                          mgzip_threads=reader_options.mgzip_threads, # Hack!
                                          error_file=error_file,
                                          verbose=verbose,
                                          very_verbose=very_verbose)

        uekw: typing.Optional[KgtkWriter] = None
        if unmodified_edges_kgtk_file is not None:
            uekw = KgtkWriter.open(ikr.column_names,
                                   unmodified_edges_kgtk_file,
                                   mode=KgtkWriter.Mode[ikr.mode.name],
                                   use_mgzip=reader_options.use_mgzip, # Hack!
                                   mgzip_threads=reader_options.mgzip_threads, # Hack!
                                   error_file=error_file,
                                   verbose=verbose,
                                   very_verbose=very_verbose)

        amkw: typing.Optional[KgtkWriter] = None
        if activated_mapping_kgtk_file is not None:
            amkw = KgtkWriter.open(mkr.column_names,
                                   activated_mapping_kgtk_file,
                                   mode=KgtkWriter.Mode[mkr.mode.name],
                                   use_mgzip=reader_options.use_mgzip, # Hack!
                                   mgzip_threads=reader_options.mgzip_threads, # Hack!
                                   error_file=error_file,
                                   verbose=verbose,
                                   very_verbose=very_verbose)

        # Done!
        ikr.close()
        mkr.close()
        okw.close()
        if uekw is not None:
            uekw.close()
        if amkw is not None:
            amkw.close()
        return 0

    except SystemExit as e:
        raise KGTKException("Exit requested")
    except Exception as e:
        raise KGTKException(str(e))

