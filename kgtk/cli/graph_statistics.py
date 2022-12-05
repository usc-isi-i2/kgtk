"""
Import CSV file in Graph-tool.

Note:  the log file wasn't converted to the new filename parsing API.

Note: ID generation is fixed.  The standard ID generator should be used instead.
"""
from argparse import Namespace
import typing

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles


def parser():
    return {
        'help': 'Import a TSV or CSV file in Graph-tool, optionally generating various statistics ' +
                '(pagerank, in-degrees, out-degrees, degree distribution, and hits).  Two different output ' +
                'files are generated: a log file, containing a combination of TSV data nd plain text records, ' +
                'and a KGTK file. Summary statistics are directed to ' +
                'the text log file, while detailed statistics (in-degrees, out-degrees, pagerank) are directed ' +
                'to the KGTK output file.' +
                '\nBy default, in-degrees, out-degrees, and pageranks will be computed and output. ' +
                'HITS properties will be computed an doutput for directed graphs, but not for undirected ones.'
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

    parser.add_input_file(positional=True, optional=False)
    parser.add_output_file()

    parser.add_argument('--undirected', dest="undirected",
                        help='Is the graph undirected? If false, then the graph is ' +
                             ' treated as (node1)->(node2).  If true, then the graph is ' +
                             ' treated as (node1)<->(node2). ' +
                             '\nAlso, HITS will not be computed on undirected graphs. ' +
                             '\n(default=%(default)s)',
                        type=optional_bool, nargs='?', const=True, default=False, metavar='True|False')

    parser.add_argument('--compute-pagerank', dest='compute_pagerank',
                        help='Whether or not to compute the PageRank property. ' +
                             '\nNote: --undirected improves the pagerank calculation. ' +
                             'If you want both pagerank and in/out-degrees, you should make two runs. ' +
                             '\n(default=%(default)s)',
                        type=optional_bool, nargs='?', const=True, default=True, metavar='True|False')

    parser.add_argument('--compute-hits', dest='compute_hits',
                        help='Whether or not to compute the HITS properties. ' +
                             '\nNote: --undirected disables HITS calculation. (default=%(default)s)',
                        type=optional_bool, nargs='?', const=True, default=True, metavar='True|False')

    parser.add_argument('--compute-betweenness', dest='compute_betweenness',
                        help='Whether or not to compute the betweenness property. ' +
                             '\nNote: betweenness is not suitable for large graphs. ' +
                             '\n(default=%(default)s)',
                        type=optional_bool, nargs='?', const=True, default=False, metavar='True|False')

    parser.add_argument('--compute-local-clustering', dest='compute_local_clustering',
                        help='Whether or not to compute the local clustering property. ' +
                             '\nUse --edge-weight-property to specify optional edge weights.\n(default=%(default)s)',
                        type=optional_bool, nargs='?', const=True, default=False, metavar='True|False')

    parser.add_argument('--compute-extended-clustering', dest='compute_extended_clustering',
                        help='Whether or not to compute the extended clustering property. ' +
                             '\nUse --max-depth to specify maximum clustering ordering.\n(default=%(default)s)',
                        type=optional_bool, nargs='?', const=True, default=False, metavar='True|False')

    parser.add_argument('--edge-weight-property', action='store', dest='edge_weight_property', default=None,
                        help='Input edge weight property name for compute-local-clustering option.')

    parser.add_argument('--max-depth', action='store', dest='max_depth', type=int, default=1,
                        help='Maximum clustering ordering for compute-extended-clustering option.(default=%(default)s)')

    parser.add_argument('--output-statistics-only', dest='output_statistics_only',
                        help='If this option is set, write only the statistics edges to the primary output file. ' +
                             'Else, write both the statistics and the original graph. (default=%(default)s',
                        type=optional_bool, nargs='?', const=True, default=False, metavar='True|False')

    parser.add_argument('--output-degrees', dest='output_degrees',
                        help='Whether or not to write degree edges to the primary output file. (default=%(default)s)',
                        type=optional_bool, nargs='?', const=True, default=True, metavar='True|False')

    parser.add_argument('--output-pagerank', dest='output_pagerank',
                        help='Whether or not to write pagerank edges to the primary output file. (default=%(default)s)',
                        type=optional_bool, nargs='?', const=True, default=True, metavar='True|False')

    parser.add_argument('--output-hits', dest='output_hits',
                        help='Whether or not to write HITS edges to the primary output file. (default=%(default)s)',
                        type=optional_bool, nargs='?', const=True, default=True, metavar='True|False')

    parser.add_argument('--output-betweenness', dest='output_betweenness',
                        help='Whether or not to write betweenness to the primary output file. (default=%(default)s)',
                        type=optional_bool, nargs='?', const=True, default=True, metavar='True|False')

    parser.add_argument('--output-local-clustering', dest='output_local_clustering',
                        help='Whether or not to write local clustering to the primary output file.'
                             '(default=%(default)s)',
                        type=optional_bool, nargs='?', const=True, default=True, metavar='True|False')

    parser.add_argument('--output-extended-clustering', dest='output_extended_clustering',
                        help='Whether or not to write extended clustering to the primary output file. (default=%(default)s)',
                        type=optional_bool, nargs='?', const=True, default=True, metavar='True|False')

    parser.add_argument('--log-file', action='store', type=str, dest='log_file',
                        help='Summary file for the global statistics of the graph.', default='./summary.txt')

    parser.add_argument('--log-top-relations', dest='log_top_relations',
                        help='Whether or not to compute top relations and output them to the log file. (default=%(default)s)',
                        type=optional_bool, nargs='?', const=True, default=True, metavar='True|False')

    parser.add_argument('--log-degrees-histogram', dest='log_degrees_histogram',
                        help='Whether or not to compute degree distribution and output it to the log file. (default=%(default)s)',
                        type=optional_bool, nargs='?', const=True, default=True, metavar='True|False')

    parser.add_argument('--log-top-pageranks', dest='log_top_pageranks',
                        help='Whether or not to output PageRank centrality top-n to the log file. ' +
                             '\n(default=%(default)s)',
                        type=optional_bool, nargs='?', const=True, default=True, metavar='True|False')

    parser.add_argument('--log-top-hits', dest='log_top_hits',
                        help='Whether or not to output the top-n HITS to the log file. (default=%(default)s)',
                        type=optional_bool, nargs='?', const=True, default=True, metavar='True|False')

    parser.add_argument('--log-top-n', action='store', dest='top_n',
                        default=5, type=int,
                        help='Number of top centrality nodes to write to the log file. (default=%(default)d)')

    parser.add_argument('--vertex-in-degree-property', action='store', dest='vertex_in_degree',
                        default='vertex_in_degree',
                        help='Label for edge: vertex in degree property. ' +
                             '\nNote: If --undirected is True, then the in-degree will be 0. ' +
                             '\n(default=%(default)s')

    parser.add_argument('--vertex-out-degree-property', action='store', dest='vertex_out_degree',
                        default='vertex_out_degree',
                        help='Label for edge: vertex out degree property. ' +
                             '\nNote: if --undirected is True, the the out-degree will be the sum of ' +
                             'the values that would have been calculated for in-degree and -out-degree ' +
                             ' if --undirected were False. ' +
                             '\n(default=%(default)s)')

    parser.add_argument('--page-rank-property', action='store', dest='vertex_pagerank',
                        default='vertex_pagerank',
                        help='Label for page rank property. (default=%(default)s)')

    parser.add_argument('--vertex-hits-authority-property', action='store', dest='vertex_auth',
                        default='vertex_auth',
                        help='Label for edge: vertext hits authority. (default=%(default)s)')

    parser.add_argument('--vertex-hits-hubs-property', action='store', dest='vertex_hubs',
                        default='vertex_hubs',
                        help='Label for edge: vertex hits hubs. (default=%(default)s)')

    parser.add_argument('--betweenness-property', action='store', dest='vertex_betweenness',
                        default='vertex_betweenness',
                        help='Label for betweenness property. (default=%(default)s)')

    parser.add_argument('--local-clustering-property', action='store', dest='vertex_local_clustering',
                        default='vertex_local_clustering',
                        help='Label for vertex_local_clustering property. (default=%(default)s)')

    parser.add_argument('--extended-clustering-property', action='store', dest='vertex_extended_clustering_prefix',
                        default='vertex_extended_clustering_',
                        help='Label for vertex_local_clustering property. (default=%(default)s)')

    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser,
                                    mode_options=True,
                                    default_mode=KgtkReaderMode[parsed_shared_args._mode],
                                    expert=_expert)
    KgtkValueOptions.add_arguments(parser, expert=_expert)


def run(input_file: KGTKFiles,
        output_file: KGTKFiles,

        undirected: bool,
        compute_pagerank: bool,
        compute_hits: bool,
        compute_betweenness: bool,
        compute_local_clustering: bool,
        compute_extended_clustering: bool,
        edge_weight_property: str,
        max_depth: int,
        output_statistics_only: bool,
        output_degrees: bool,
        output_pagerank: bool,
        output_hits: bool,
        output_betweenness: bool,
        output_local_clustering: bool,
        output_extended_clustering: bool,
        log_file: str,
        log_degrees_histogram: bool,
        log_top_relations: bool,
        log_top_pageranks: bool,
        log_top_hits: bool,
        top_n: int,

        vertex_in_degree: str,
        vertex_out_degree: str,
        vertex_pagerank: str,
        vertex_betweenness: str,
        vertex_auth: str,
        vertex_hubs: str,
        vertex_extended_clustering_prefix: str,
        vertex_local_clustering: str,

        errors_to_stdout: bool,
        verbose: bool,
        very_verbose: bool,

        **kwargs,  # Whatever KgtkFileOptions and KgtkValueOptions want.
        ):
    # import modules locally
    from pathlib import Path
    import sys

    from kgtk.exceptions import KGTKException
    from kgtk.io.kgtkreader import KgtkReaderOptions
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions
    from kgtk.graph_analysis.statistics import GraphStatistics

    try:

        # Select where to send error messages, defaulting to stderr.
        error_file: typing.TextIO = sys.stdout if errors_to_stdout else sys.stderr

        # Build the option structures.
        reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs)
        value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)

        input_kgtk_file: Path = KGTKArgumentParser.get_input_file(input_file)
        output_kgtk_file: Path = KGTKArgumentParser.get_output_file(output_file)

        gs = GraphStatistics(input_kgtk_file=input_kgtk_file,
                             output_kgtk_file=output_kgtk_file,
                             undirected=undirected,
                             compute_pagerank=compute_pagerank,
                             compute_hits=compute_hits,
                             compute_betweenness=compute_betweenness,
                             compute_local_clustering=compute_local_clustering,
                             compute_extended_clustering=compute_extended_clustering,
                             edge_weight_property=edge_weight_property,
                             max_depth=max_depth,
                             output_statistics_only=output_statistics_only,
                             output_degrees=output_degrees,
                             output_pagerank=output_pagerank,
                             output_hits=output_hits,
                             output_betweenness=output_betweenness,
                             output_local_clustering=output_local_clustering,
                             output_extended_clustering=output_extended_clustering,
                             log_file=log_file,
                             log_degrees_histogram=log_degrees_histogram,
                             log_top_relations=log_top_relations,
                             log_top_pageranks=log_top_pageranks,
                             log_top_hits=log_top_hits,
                             top_n=top_n,
                             vertex_in_degree=vertex_in_degree,
                             vertex_out_degree=vertex_out_degree,
                             vertex_pagerank=vertex_pagerank,
                             vertex_betweenness=vertex_betweenness,
                             vertex_auth=vertex_auth,
                             vertex_hubs=vertex_hubs,
                             vertex_extended_clustering_prefix=vertex_extended_clustering_prefix,
                             vertex_local_clustering=vertex_local_clustering,
                             reader_options=reader_options,
                             value_options=value_options,
                             error_file=error_file,
                             verbose=verbose,
                             very_verbose=very_verbose)
        gs.process()
    except Exception as e:
        raise KGTKException('Error: ' + str(e))
