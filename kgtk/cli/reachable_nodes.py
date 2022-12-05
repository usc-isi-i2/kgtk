"""
Find reachable nodes given a set of root nodes and properties

TODO: the --subj, --pred, and --obj options should perhaps be renamed to
      --node1-column-name, --label-column-name, and --node2-column-name, with
      the old options kept as synonyms.

TODO: the root file name should be parsed with parser.add_input_file(...)
"""
from argparse import Namespace, _MutuallyExclusiveGroup
import typing

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles


def parser():
    return {
        'help': 'Find reachable nodes in a graph.'
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

    parser.add_input_file(positional=True, who="The KGTK file to find connected components in.")
    parser.add_output_file()

    parser.add_argument('--root', action='store', dest='root', type=str, nargs="*",
                        help='Set of root nodes to use, space- or comma-separated strings. (default=None)')
    parser.add_argument('--root-file', '--rootfile', action='store', dest='rootfile',
                        help='Option to specify a file containing the set of root nodes', default=None)
    parser.add_argument('--rootfilecolumn', action='store', type=str, dest='rootfilecolumn',
                        help='Specify the name or number of the root file column with the root nodes.  '
                             '(default=node1 or its alias if edge file, id if node file)')
    parser.add_argument("--subj", action="store", type=str, dest="subject_column_name",
                        help='Name of the subject column. (default: node1 or its alias)')
    parser.add_argument("--obj", action="store", type=str, dest="object_column_name",
                        help='Name of the object column. (default: label or its alias)')
    parser.add_argument("--pred", action="store", type=str, dest="predicate_column_name",
                        help='Name of the predicate column. (default: node2 or its alias)')

    parser.add_argument("--prop", "--props", action="store", type=str, dest="props", nargs="*",
                        help='Properties to consider while finding reachable nodes, space- or comma-separated string. '
                             '(default: all properties)',
                        default=None)
    parser.add_argument('--props-file', action='store', dest='props_file',
                        help='Option to specify a file containing the set of properties', default=None)
    parser.add_argument('--propsfilecolumn', action='store', type=str, dest='propsfilecolumn', default=None,
                        help='Specify the name or number of the props file column with the property names.  '
                             '(default=node1 or its alias if edge file, id if node file)')

    parser.add_argument('--inverted', dest="inverted",
                        help="When True, and when --undirected is False, invert the source and target nodes in the "
                             "graph. (default=%(default)s)",
                        type=optional_bool, nargs='?', const=True, default=False, metavar="True|False")

    parser.add_argument("--inverted-prop", "--inverted-props", action="store", type=str, dest="inverted_props",
                        nargs="*",
                        help='Properties to invert, space- or comma-separated string. (default: no properties)',
                        default=None)
    parser.add_argument('--inverted-props-file', action='store', dest='inverted_props_file',
                        help='Option to specify a file containing the set of inverted properties', default=None)
    parser.add_argument('--invertedpropsfilecolumn', action='store', type=str, dest='invertedpropsfilecolumn',
                        default=None,
                        help='Specify the name or number of the inverted props file column with the property names.  '
                             '(default=node1 or its alias if edge file, id if node file)')

    parser.add_argument('--undirected', dest="undirected",
                        help="When True, specify graph as undirected. (default=%(default)s)",
                        type=optional_bool, nargs='?', const=True, default=False, metavar="True|False")

    parser.add_argument("--undirected-prop", "--undirected-props", action="store", type=str, dest="undirected_props",
                        nargs="*",
                        help='Properties to treat as undirected, space- or comma-separated string. '
                             '(default: no properties)',
                        default=None)
    parser.add_argument('--undirected-props-file', action='store', dest='undirected_props_file',
                        help='Option to specify a file containing the set of undirected properties', default=None)
    parser.add_argument('--undirectedpropsfilecolumn', action='store', type=str, dest='undirectedpropsfilecolumn',
                        default=None,
                        help='Specify the name or number of the undirected props file column with the property names.  '
                             '(default=node1 or its alias if edge file, id if node file)')

    parser.add_argument('--label', action='store', type=str, dest='label',
                        help='The label for the reachable relationship. (default: %(default)s)', default="reachable")
    parser.add_argument('--selflink', dest='selflink_bool',
                        help='When True, include a link from each output node to itself. (default=%(default)s)',
                        type=optional_bool, nargs='?', const=True, default=False, metavar="True|False")

    parser.add_argument('--show-properties', dest='show_properties',
                        help='When True, show the graph properties. (default=%(default)s)',
                        type=optional_bool, nargs='?', const=True, default=False, metavar="True|False")

    parser.add_argument('--breadth-first', dest='breadth_first',
                        help='When True, search the graph breadth first.  When false, search depth first. '
                             '(default=%(default)s)',
                        type=optional_bool, nargs='?', const=True, default=False, metavar="True|False")

    parser.add_argument('--depth-limit', dest='depth_limit',
                        help='An optional depth limit for breadth-first searches. (default=%(default)s)',
                        type=int, default=None)

    parser.add_argument('--show-distance', dest='show_distance',
                        help='When True, also given breadth first true, append another column showing the '
                             'shortest distance, default col name is distance',
                        type=optional_bool, nargs='?', const=True, default=False, metavar="True|False")

    parser.add_argument('--dist-col-name', action='store', type=str, dest='dist_col_name',
                        help='The column name for distance, default is distance', default="distance")

    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser,
                                    mode_options=True,
                                    default_mode=KgtkReaderMode[parsed_shared_args._mode],
                                    expert=_expert)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, who="input", expert=_expert, defaults=False)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, who="root", expert=_expert, defaults=False)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, who="props", expert=_expert, defaults=False)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, who="undirected_props", expert=_expert, defaults=False)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, who="inverted_props", expert=_expert, defaults=False)
    KgtkValueOptions.add_arguments(parser, expert=_expert)


def run(input_file: KGTKFiles,
        output_file: KGTKFiles,

        root: typing.Optional[typing.List[str]],
        rootfile,
        rootfilecolumn,
        subject_column_name: typing.Optional[str],
        object_column_name: typing.Optional[str],
        predicate_column_name: typing.Optional[str],

        props: typing.Optional[typing.List[str]],
        props_file: typing.Optional[str],
        propsfilecolumn: typing.Optional[str],

        inverted: bool,
        inverted_props: typing.Optional[typing.List[str]],
        inverted_props_file: typing.Optional[str],
        invertedpropsfilecolumn: typing.Optional[str],

        undirected: bool,
        undirected_props: typing.Optional[typing.List[str]],
        undirected_props_file: typing.Optional[str],
        undirectedpropsfilecolumn: typing.Optional[str],

        label: str,
        selflink_bool: bool,
        show_properties: bool,
        breadth_first: bool,
        depth_limit: typing.Optional[int],

        errors_to_stdout: bool,
        errors_to_stderr: bool,
        show_options: bool,
        verbose: bool,
        very_verbose: bool,
        show_distance: bool,
        dist_col_name: str,

        **kwargs,  # Whatever KgtkFileOptions and KgtkValueOptions want.
        ):
    import sys
    from pathlib import Path
    from graph_tool.search import dfs_iterator, bfs_iterator, bfs_search, BFSVisitor  # type: ignore
    from graph_tool.util import find_edge  # type: ignore
    from kgtk.exceptions import KGTKException
    from kgtk.cli_argparse import KGTKArgumentParser
    from kgtk.io.kgtkreader import KgtkReaderOptions
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions
    from kgtk.graph_analysis.reachable_nodes import ReachableNodes

    # Graph-tool names columns that are not subject or object c0, c1...
    # This function finds the number that graph tool assigned to the predicate column

    try:
        input_kgtk_file: Path = KGTKArgumentParser.get_input_file(input_file)
        output_kgtk_file: Path = KGTKArgumentParser.get_output_file(output_file)

        # Select where to send error messages, defaulting to stderr.
        error_file: typing.TextIO = sys.stdout if errors_to_stdout else sys.stderr

        # Build the option structures.
        input_reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs, who="input", fallback=True)
        root_reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs, who="root", fallback=True)
        props_reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs, who="props", fallback=True)
        undirected_props_reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs, who="undirected_props",
                                                                                         fallback=True)
        inverted_props_reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs, who="inverted_props",
                                                                                       fallback=True)
        value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)
        rn = ReachableNodes(input_kgtk_file=input_kgtk_file,
                            output_kgtk_file=output_kgtk_file,
                            input_reader_options=input_reader_options,
                            root_reader_options=root_reader_options,
                            props_reader_options=props_reader_options,
                            undirected_props_reader_options=undirected_props_reader_options,
                            inverted_props_reader_options=inverted_props_reader_options,
                            value_options=value_options,
                            show_properties=show_properties,
                            show_distance=show_distance,
                            dist_col_name=dist_col_name,
                            label=label,
                            root=root,
                            rootfile=rootfile,
                            rootfilecolumn=rootfilecolumn,
                            subject_column_name=subject_column_name,
                            object_column_name=object_column_name,
                            predicate_column_name=predicate_column_name,
                            inverted=inverted,
                            inverted_props_file=inverted_props_file,
                            invertedpropsfilecolumn=invertedpropsfilecolumn,
                            props=props,
                            props_file=props_file,
                            propsfilecolumn=propsfilecolumn,
                            undirected_props=undirected_props,
                            inverted_props=inverted_props,
                            undirected=undirected,
                            undirected_props_file=undirected_props_file,
                            undirectedpropsfilecolumn=undirectedpropsfilecolumn,
                            selflink_bool=selflink_bool,
                            breadth_first=breadth_first,
                            depth_limit=depth_limit,
                            error_file=error_file,
                            verbose=verbose,
                            very_verbose=very_verbose,
                            show_options=show_options,
                            errors_to_stdout=errors_to_stdout,
                            errors_to_stderr=errors_to_stderr
                            )
        rn.process()
    except Exception as e:
        raise KGTKException(str(e))
