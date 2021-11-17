from argparse import Namespace, SUPPRESS
import typing

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles


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
    from kgtk.gt.connected_components import ConnectedComponents
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions, KgtkReaderMode
    from kgtk.utils.enumnameaction import EnumLowerNameAction

    _expert: bool = parsed_shared_args._expert

    parser.add_input_file(positional=True, who="The KGTK file to find connected components in.")
    parser.add_output_file()

    parser.add_argument("--properties", action="store", type=str, dest="properties",
                        help=' A comma separated list of properties to traverse while finding connected components, '
                             'by default all properties will be considered',
                        default='')
    parser.add_argument('--undirected', action='store_true', dest="undirected",
                        help="Specify if the input graph is undirected, default FALSE")
    parser.add_argument('--strong', action='store_true', dest="strong",
                        help="Treat graph as directed or not, independent of its actual directionality.")


    parser.add_argument("--cluster-name-method", dest="cluster_name_method",
                        help="Determine the naming method for clusters. (default=%(default)s)",
                        type=ConnectedComponents.Method, action=EnumLowerNameAction,
                        default=ConnectedComponents.DEFAULT_CLUSTER_NAME_METHOD)
    
    parser.add_argument("--cluster-name-separator", dest="cluster_name_separator",
                        help="Specify the separator to be used in cat and hash cluster name methods. (default=%(default)s)",
                        default=ConnectedComponents.DEFAULT_CLUSTER_NAME_SEPARATOR)

    parser.add_argument("--cluster-name-prefix", dest="cluster_name_prefix",
                        help="Specify the prefix to be used in the prefixed and hash cluster name methods. (default=%(default)s)",
                        default=ConnectedComponents.DEFAULT_CLUSTER_NAME_PREFIX)

    parser.add_argument("--cluster-name-zfill", dest="cluster_name_zfill", type=int,
                        help="Specify the zfill to be used in the numbered and prefixed cluster name methods. (default=%(default)s)",
                        default=ConnectedComponents.DEFAULT_CLUSTER_NAME_ZFILL)

    parser.add_argument("--minimum-cluster-size", dest="minimum_cluster_size", type=int,
                        help="Specify the minimum cluster size. (default=%(default)s)",
                        default=ConnectedComponents.DEFAULT_MINIMUM_CLUSTER_SIZE)


    # CMR: The folowing options aren't used.  Is the intent to support them?
    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser,
                                    mode_options=True,
                                    default_mode=KgtkReaderMode[parsed_shared_args._mode],
                                    expert=_expert)
    KgtkReaderOptions.add_arguments(parser,
                                    mode_options=True,
                                    default_mode=KgtkReaderMode[parsed_shared_args._mode],
                                    who="input",
                                    expert=_expert,
                                    defaults=False)
    # KgtkValueOptions.add_arguments(parser, expert=_expert)


def run(input_file: KGTKFiles,
        output_file: KGTKFiles,

        properties: str = '',
        undirected: bool = False,
        strong: bool = False,

        # The following have been modified to postpone importing gtaph_tools.
        # ClusterComponents cann't be referenced here.
        cluster_name_method: typing.Optional[typing.Any] = None,
        cluster_name_separator: typing.Optional[str] = None,
        cluster_name_prefix: typing.Optional[str] = None,
        cluster_name_zfill: typing.Optional[int] = None,
        minimum_cluster_size: typing.Optional[int] = None,

        **kwargs  # Whatever KgtkFileOptions and KgtkValueOptions want.
        ) -> int:
    from pathlib import Path
    
    from kgtk.exceptions import KGTKException
    from kgtk.gt.connected_components import ConnectedComponents
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions

    input_kgtk_file: Path = KGTKArgumentParser.get_input_file(input_file)
    output_kgtk_file: Path = KGTKArgumentParser.get_output_file(output_file)

    # It's OK to mention ClusterComponents here.
    cluster_name_method_x: ConnectedComponents.Method = \
        cluster_name_method if cluster_name_method is not None else ConnectedComponents.DEFAULT_CLUSTER_NAME_METHOD
    cluster_name_separator = ConnectedComponents.DEFAULT_CLUSTER_NAME_SEPARATOR if cluster_name_separator is None else cluster_name_separator
    cluster_name_prefix = ConnectedComponents.DEFAULT_CLUSTER_NAME_PREFIX if cluster_name_prefix is None else cluster_name_prefix
    cluster_name_zfill = ConnectedComponents.DEFAULT_CLUSTER_NAME_ZFILL if cluster_name_zfill is None else cluster_name_zfill
    minimum_cluster_size = ConnectedComponents.DEFAULT_MINIMUM_CLUSTER_SIZE if minimum_cluster_size is None else minimum_cluster_size

    cc: ConnectedComponents = ConnectedComponents(input_file_path=input_kgtk_file,
                                                  output_file_path=output_kgtk_file,
                                                  properties=properties,
                                                  undirected=undirected,
                                                  strong=strong,
                                                  cluster_name_method=cluster_name_method_x,
                                                  cluster_name_separator=cluster_name_separator,
                                                  cluster_name_prefix=cluster_name_prefix,
                                                  cluster_name_zfill=cluster_name_zfill,
                                                  minimum_cluster_size=minimum_cluster_size,
    )

    try:
        cc.process()
        return 0
    except Exception as e:
        raise KGTKException(str(e))
