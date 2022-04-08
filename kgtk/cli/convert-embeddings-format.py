from argparse import Namespace, SUPPRESS
from pathlib import Path
import sys
import typing
from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles


def parser():
    return {
        'help': 'Convert embeddings format from KGTK edge file to word2vec or Google Projector format, or vice versa',
        'description': 'Convert KGTK edge embeddings file to word2vec or Google Projector format or vice versa\n. '
                       'Takes an optional node file for Google Project format and processes only the top 10,000 '
                       'rows from the edge file as Google Projector only accepts 10,000 rows\n.'
                       'Also creates a metadata file for Google Projector if a node file is present.\n'
    }


def add_arguments_extended(parser: KGTKArgumentParser, parsed_shared_args: Namespace):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderMode, KgtkReaderOptions
    from kgtk.io.kgtkwriter import KgtkWriter
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

    parser.add_input_file(who="KGTK input files",
                          dest="input_file",
                          options=["-i", "--input-file"],
                          positional=True,
                          allow_list=False)

    parser.add_input_file(who="The KGTK node file for Google Projector Metadata",
                          options=["--node-file"],
                          dest="node_file",
                          metavar="NODE_FILE",
                          optional=True,
                          allow_stdin=False)

    parser.add_output_file()

    parser.add_output_file(who="The metadata file for Google Projector",
                           options=["--metadata-file"],
                           dest="metadata_file",
                           metavar="METADATA_FILE",
                           optional=True,
                           allow_stdout=False,
                           default_stdout=False)

    parser.add_argument("--input-property",
                        dest="input_property",
                        help="The property name for embeddings in the input KGTK edge file. (default=embeddings)."
                             "Only relevant if --input-format == kgtk",
                        default='embeddings',
                        type=str)

    parser.add_argument("--output-format",
                        dest="output_format",
                        help="The desired output file format: word2vec|gprojector (default=word2vec)",
                        default="word2vec",
                        type=str)

    parser.add_argument("--metadata-columns",
                        dest="metadata_columns",
                        help="A comma separated string of columns names in the input file to be used for creating the"
                             "metadata file for Google projector. Only to be used when --output-format == 'gprojector',"
                             "and --node-file is not specified.",
                        default=None,
                        type=str)

    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser,
                                    mode_options=True,
                                    default_mode=KgtkReaderMode[parsed_shared_args._mode],
                                    expert=_expert)
    KgtkValueOptions.add_arguments(parser, expert=_expert)


def run(input_file: KGTKFiles,
        output_file: KGTKFiles,
        node_file: KGTKFiles,
        output_format: typing.Optional[str] = 'word2vec',
        input_property: typing.Optional[str] = 'embeddings',
        metadata_file: KGTKFiles = None,
        metadata_columns: str = None,
        errors_to_stderr: bool = True,
        **kwargs  # Whatever KgtkFileOptions and KgtkValueOptions want.
        ) -> int:
    # import modules locally
    from kgtk.exceptions import KGTKException
    from kgtk.utils.convert_embeddings_format import ConvertEmbeddingsFormat

    input_file_path: Path = KGTKArgumentParser.get_input_file(input_file)
    output_file_path: Path = KGTKArgumentParser.get_output_file(output_file)
    node_file_path: Path = KGTKArgumentParser.get_input_file(node_file) if node_file is not None else None
    metadata_file_path: Path = KGTKArgumentParser.get_input_file(metadata_file)

    # Select where to send error messages, defaulting to stderr.
    error_file: typing.TextIO = sys.stderr if errors_to_stderr else sys.stdout

    # Build the option structures.
    kwargs['use_graph_cache_envar'] = False

    try:
        cef: ConvertEmbeddingsFormat = ConvertEmbeddingsFormat(input_file=input_file_path,
                                                               output_file=output_file_path,
                                                               node_file=node_file_path,
                                                               output_format=output_format,
                                                               input_property=input_property,
                                                               error_file=error_file,
                                                               output_metadata_file=metadata_file_path,
                                                               edge_columns_metadata=metadata_columns,
                                                               **kwargs
                                                               )

        cef.process()
        return 0

    except SystemExit as e:
        raise KGTKException("Exit requested")
    except KGTKException as e:
        raise KGTKException(e)
    except Exception as e:
        raise KGTKException(str(e))
