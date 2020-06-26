from argparse import Namespace, SUPPRESS
from pathlib import Path
import sys
import typing

from kgtk.cli_argparse import KGTKArgumentParser
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions


def parser():
    return {
        'help': 'Find connected components in a Graph.',
        'description': 'Find all the connected components in an undirected or directed Graph.' +
                       '\n\nAdditional options are shown in expert help.\nkgtk --expert connected-components --help'
    }


def add_arguments_extended(parser: KGTKArgumentParser, parsed_shared_args: Namespace):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """
    _expert: bool = parsed_shared_args._expert

    parser.add_argument("input_kgtk_file", nargs="?",
                        help="The KGTK file to find connected components in. May be omitted or '-' for stdin.",
                        type=Path)
    parser.add_argument("--no-header", action="store_true", dest="no_header",
                        help="Specify if the input file does not have a header, default FALSE")
    parser.add_argument("--properties", action="store", type=str, dest="properties",
                        help=' A comma separated list of properties to traverse while finding connected components, '
                             'by default all properties will be considered',
                        default='')
    parser.add_argument('--undirected', action='store_true', dest="undirected",
                        help="Specify if the input graph is undirected, default FALSE")
    parser.add_argument('--strong', action='store_true', dest="strong",
                        help="Treat graph as directed or not, independent of its actual directionality.")
    parser.add_argument("-o", "--output-file", dest="output_kgtk_file",
                        help="The KGTK file to write, by default the output will be written to standard output).",
                        type=Path, default=None)

    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, expert=_expert)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, who="input", expert=_expert, defaults=False)
    # KgtkValueOptions.add_arguments(parser, expert=_expert)


def run(input_kgtk_file: typing.Optional[Path],
        output_kgtk_file: typing.Optional[Path],
        no_header: bool = False,
        properties: str = None,
        undirected: bool = False,
        strong: bool = False,
        **kwargs  # Whatever KgtkFileOptions and KgtkValueOptions want.
        ) -> int:
    from kgtk.gt.connected_components import ConnectedComponents
    from kgtk.exceptions import KGTKException
    cc: ConnectedComponents = ConnectedComponents(input_file_path=input_kgtk_file,
                                                  output_file_path=output_kgtk_file,
                                                  no_header=no_header,
                                                  properties=properties,
                                                  undirected=undirected,
                                                  strong=strong)

    try:
        cc.process()
    except Exception as e:
        raise KGTKException(str(e))
