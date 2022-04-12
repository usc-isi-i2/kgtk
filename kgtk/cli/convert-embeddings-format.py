from argparse import Namespace, SUPPRESS
from pathlib import Path
import sys
import typing
from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles


def parser():
    return {
        'help': 'Convert embeddings format from KGTK edge file to word2vec or Google Projector format, or vice versa',
        'description': 'Converts KGTK edge embeddings file to word2vec or Google Projector format.'
                       'Takes an optional node file for Google Project format to create a metadata file. '
                       'Processes only top 10,000 rows from the edge file for Google Projector as it only'
                       ' accepts 10,000 rows.\n'
                       'Additional options are shown in expert help.\n'
                       'kgtk --expert convert-embeddings-format --help'
    }


def add_arguments_extended(parser: KGTKArgumentParser, parsed_shared_args: Namespace):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderMode, KgtkReaderOptions
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

    parser.add_input_file(who="The KGTK node file for creating Google Projector Metadata. All the columns in the node "
                              "file will be added to the metadata file by default. You can customise this with the "
                              "--metadata-columns option.",
                          options=["--node-file"],
                          dest="node_file",
                          metavar="NODE_FILE",
                          optional=True,
                          allow_stdin=False)

    parser.add_output_file()

    parser.add_output_file(who="The output metadata file for Google Projector. If --output-format == gprojector and"
                               "--metadata-file is not specified, a file named "
                               "`kgtk_embeddings_gprojector_metadata.tsv` will be created in USER_HOME",
                           options=["--metadata-file"],
                           dest="metadata_file",
                           metavar="METADATA_FILE",
                           optional=True,
                           allow_stdout=False,
                           default_stdout=False)

    parser.add_argument("--input-property",
                        dest="input_property",
                        help="The property name for embeddings in the input KGTK edge file. (default=embeddings).",
                        default='embeddings',
                        type=str)

    parser.add_argument("--output-format",
                        dest="output_format",
                        help="The desired output file format: word2vec|gprojector (default=word2vec)",
                        default="word2vec",
                        type=str)

    parser.add_argument("--metadata-columns",
                        dest="metadata_columns",
                        help="A comma separated string of columns names in the input file or the --node-file to be "
                             "used for creating the metadata file for Google projector. "
                             "Only to be used when --output-format == 'gprojector'. If --node-file is specified, "
                             "the command will look for --metadata-columns in the --node-file, otherwise input file."
                             "The command will throw an error if the columns specified are not in either of the files.",
                        default=None,
                        type=str)

    KgtkReaderOptions.add_arguments(parser,
                                    mode_options=True,
                                    default_mode=KgtkReaderMode[parsed_shared_args._mode],
                                    expert=_expert)


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
                                                               metadata_columns=metadata_columns,
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
