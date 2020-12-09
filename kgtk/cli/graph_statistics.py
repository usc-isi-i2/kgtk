"""
Import CSV file in Graph-tool.

Note:  the log file wasn't coverted to the new filename parsing API.

Note:  The input file is read twice: once for the header, and once for the
data.  Thus, stdin cannot be used as the input file.

TODO: Convert to KgtkReader and read the file only once.
"""
from argparse import Namespace
import typing

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles

def parser():
    return {
        'help': 'Import a CSV file in Graph-tool.'
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

    parser.add_input_file(positional=True, optional=False)
    parser.add_output_file()

    parser.add_argument('--undirected', dest="undirected",
                        help="Is the graph undirected? (default=%(default)s)",
                        type=optional_bool, nargs='?', const=True, default=False, metavar="True|False")

    parser.add_argument('--degrees', dest='compute_degrees',
                        help="Whether or not to compute degree distribution. (default=%(default)s)",
                        type=optional_bool, nargs='?', const=True, default=False, metavar="True|False")

    parser.add_argument('--pagerank', dest='compute_pagerank',
                        help="Whether or not to compute PageRank centraility. (default=%(default)s)",
                        type=optional_bool, nargs='?', const=True, default=False, metavar="True|False")
                        
    parser.add_argument('--hits', dest='compute_hits',
                        help="Whether or not to compute HITS centraility. (default=%(default)s)",
                        type=optional_bool, nargs='?', const=True, default=False, metavar="True|False")

    parser.add_argument('--log', action='store', type=str, dest='log_file',
                        help='Summary file for the global statistics of the graph.', default="./summary.txt")

    parser.add_argument('--statistics-only', dest='statistics_only',
                        help='If this flag is set, output only the statistics edges. Else, append the statistics to the original graph. (default=%(default)s',
                        type=optional_bool, nargs='?', const=True, default=False, metavar="True|False")

    parser.add_argument('--vertex-in-degree-property', action='store', dest='vertex_in_degree',
                        default='vertex_in_degree',
                        help='Label for edge: vertex in degree property. (default=%(default)s')

    parser.add_argument('--vertex-out-degree-property', action='store', dest='vertex_out_degree',
                        default='vertex_out_degree',
                        help='Label for edge: vertex out degree property. (default=%(default)s)')

    parser.add_argument('--page-rank-property', action='store', dest='vertex_pagerank',
                        default='vertex_pagerank',
                        help='Label for pank rank property. (default=%(default)s)')

    parser.add_argument('--vertex-hits-authority-property', action='store', dest='vertex_auth',
                        default='vertex_auth',
                        help='Label for edge: vertext hits authority. (default=%(default)s)')
    
    parser.add_argument('--vertex-hits-hubs-property', action='store', dest='vertex_hubs',
                        default='vertex_hubs',
                        help='Label for edge: vertex hits hubs. (default=%(default)s)')

    parser.add_argument('--print-top-n', action='store', dest='top_n',
                        default=5, type=int,
                        help='Number of top centrality nodes to print. (default=%(default)d)')

    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, expert=_expert)
    KgtkValueOptions.add_arguments(parser, expert=_expert)

def run(input_file: KGTKFiles,
        output_file: KGTKFiles,
        
        undirected: bool,
        compute_degrees: bool,
        compute_pagerank: bool,
        compute_hits: bool,
        log_file: str,
        statistics_only: bool,
        vertex_in_degree: str,
        vertex_out_degree: str,
        vertex_pagerank: str,
        vertex_auth: str,
        vertex_hubs: str,
        top_n: int,

        errors_to_stdout: bool,
        errors_to_stderr: bool,
        show_options: bool,
        verbose: bool,
        very_verbose: bool,

        **kwargs, # Whatever KgtkFileOptions and KgtkValueOptions want.
        ):
    # import modules locally
    from pathlib import Path
    import sys

    from graph_tool import centrality
    from kgtk.exceptions import KGTKException
    import kgtk.gt.analysis_utils as gtanalysis
    from kgtk.gt.gt_load import load_graph_from_kgtk
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
    from kgtk.io.kgtkwriter import KgtkWriter
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    v_prop_dict = {
        'vertex_pagerank': vertex_pagerank,
        'vertex_hubs': vertex_hubs,
        'vertex_auth': vertex_auth
    }
    try:

        # Select where to send error messages, defaulting to stderr.
        error_file: typing.TextIO = sys.stdout if errors_to_stdout else sys.stderr

        # Build the option structures.
        reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs)
        value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)

        input_kgtk_file: Path = KGTKArgumentParser.get_input_file(input_file)
        output_kgtk_file: Path = KGTKArgumentParser.get_output_file(output_file)

        # hardcoded values useful for the script. Perhaps some of them should be exposed as arguments later
        directions = ['in', 'out', 'total']
        id_col = 'name'
        output_columns = ["node1", "label", "node2", "id"]

        if verbose:
            print('loading the KGTK input file...\n', file=error_file, flush=True)
        kr: KgtkReader = KgtkReader.open(input_kgtk_file,
                                         error_file=error_file,
                                         options=reader_options,
                                         value_options=value_options,
                                         verbose=verbose,
                                         very_verbose=very_verbose,
                                         )
        sub: int = kr.get_node1_column_index()
        if sub < 0:
            print("Missing node1 (subject) column.", file=error_file, flush=True)
        pred: int = kr.get_label_column_index()
        if pred < 0:
            print("Missing label (predicate) column.", file=error_file, flush=True)
        obj: int = kr.get_node2_column_index()
        if obj < 0:
            print("Missing node2 (object) column", file=error_file, flush=True)
        if sub < 0 or pred < 0 or obj < 0:
            kr.close()
            raise KGTKException("Exiting due to missing columns.")

        predicate: str = kr.column_names[pred]

        G2 = load_graph_from_kgtk(kr, directed=not undirected, ecols=(sub, obj), verbose=verbose, out=error_file)
        if verbose:
            print('graph loaded! It has %d nodes and %d edges.' % (G2.num_vertices(), G2.num_edges()), file=error_file, flush=True)

        kw: KgtkWriter = KgtkWriter.open(output_columns,
                                     output_kgtk_file,
                                     mode=KgtkWriter.Mode.EDGE,
                                     require_all_columns=True,
                                     prohibit_extra_columns=True,
                                     fill_missing_columns=False,
                                     verbose=verbose,
                                     very_verbose=very_verbose)

        with open(log_file, 'w') as writer:
            writer.write('graph loaded! It has %d nodes and %d edges\n' % (G2.num_vertices(), G2.num_edges()))
            writer.write('\n###Top relations:\n')
            for rel, freq in gtanalysis.get_topN_relations(G2, pred_property=predicate):
                writer.write('%s\t%d\n' % (rel, freq))

            if compute_degrees:
                writer.write('\n###Degrees:\n')
                for direction in directions:
                    degree_data = gtanalysis.compute_node_degree_hist(G2, direction)
                    max_degree = len(degree_data) - 1
                    mean_degree, std_degree = gtanalysis.compute_avg_node_degree(G2, direction)
                    writer.write(
                        '%s degree stats: mean=%f, std=%f, max=%d\n' % (direction, mean_degree, std_degree, max_degree))

            if compute_pagerank:
                writer.write('\n###PageRank\n')
                v_pr = G2.new_vertex_property('float')
                centrality.pagerank(G2, prop=v_pr)
                G2.properties[('v', 'vertex_pagerank')] = v_pr
                writer.write('Max pageranks\n')
                result = gtanalysis.get_topn_indices(G2, 'vertex_pagerank', top_n, id_col)
                for n_id, n_label, pr in result:
                    writer.write('%s\t%s\t%f\n' % (n_id, n_label, pr))

            if compute_hits:
                writer.write('\n###HITS\n')
                hits_eig, G2.vp['vertex_hubs'], G2.vp['vertex_auth'] = gtanalysis.compute_hits(G2)
                writer.write('HITS hubs\n')
                main_hubs = gtanalysis.get_topn_indices(G2, 'vertex_hubs', top_n, id_col)
                for n_id, n_label, hubness in main_hubs:
                    writer.write('%s\t%s\t%f\n' % (n_id, n_label, hubness))
                writer.write('HITS auth\n')
                main_auth = gtanalysis.get_topn_indices(G2, 'vertex_auth', top_n, id_col)
                for n_id, n_label, authority in main_auth:
                    writer.write('%s\t%s\t%f\n' % (n_id, n_label, authority))

        id_count = 0
        if not statistics_only:
            for e in G2.edges():
                sid, oid = e
                lbl = G2.ep[predicate][e]
                kw.write([G2.vp[id_col][sid], lbl, G2.vp[id_col][oid], '{}-{}-{}'.format(G2.vp[id_col][sid], lbl, id_count)])
                id_count += 1

        id_count = 0
        for v in G2.vertices():
            v_id = G2.vp[id_col][v]
            kw.write([v_id, vertex_in_degree, str(v.in_degree()), '{}-{}-{}'.format(v_id, vertex_in_degree, id_count)])
            id_count += 1
            kw.write([v_id, vertex_out_degree, str(v.out_degree()), '{}-{}-{}'.format(v_id, vertex_out_degree, id_count)])
            id_count += 1

            for vprop in G2.vertex_properties.keys():
                if vprop == id_col:
                    continue
                kw.write([v_id, v_prop_dict[vprop], str(G2.vp[vprop][v]), '{}-{}-{}'.format(v_id, v_prop_dict[vprop], id_count)])
                id_count += 1

        kw.close()
        kr.close()

    except Exception as e:
        raise KGTKException('Error: ' + str(e))
