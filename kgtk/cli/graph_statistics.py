"""
Import CSV file in Graph-tool.

Note:  the log file wasn't coverted to the new filename parsing API.

Note:  The input file is read twice: once for the header, and once for the
data.  Thus, stdin cannot be used as the input file.

TODO: Convert to KgtkReader and read the file only once.
"""
from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles

def parser():
    return {
        'help': 'Import a CSV file in Graph-tool.'
    }


def add_arguments(parser: KGTKArgumentParser):
    """
    Parse arguments
    Args:
            parser (argparse.ArgumentParser)
    """
    parser.add_input_file(positional=True, optional=False)

    parser.add_argument('--directed', action='store_true', dest="directed", help="Is the graph directed or not?")
    parser.add_argument('--degrees', action='store_true', dest='compute_degrees',
                        help="Whether or not to compute degree distribution.")
    parser.add_argument('--pagerank', action='store_true', dest='compute_pagerank',
                        help="Whether or not to compute PageRank centraility.")
    parser.add_argument('--hits', action='store_true', dest='compute_hits',
                        help="Whether or not to compute HITS centraility.")
    parser.add_argument('--log', action='store', type=str, dest='log_file',
                        help='Summary file for the global statistics of the graph.', default="./summary.txt")
    parser.add_argument('--statistics-only', action='store_true', dest='output_stats',
                        help='If this flag is set, output only the statistics edges. Else, append the statistics to the original graph.')
    parser.add_argument('--vertex-in-degree-property', action='store', dest='vertex_in_degree',
                        default='vertex_in_degree',
                        help='Label for edge: vertex in degree property')
    parser.add_argument('--vertex-out-degree-property', action='store', dest='vertex_out_degree',
                        default='vertex_out_degree',
                        help='Label for edge: vertex out degree property')
    parser.add_argument('--page-rank-property', action='store', dest='vertex_pagerank',
                        default='vertex_pagerank',
                        help='Label for pank rank property')
    parser.add_argument('--vertex-hits-authority-property', action='store', dest='vertex_auth',
                        default='vertex_auth',
                        help='Label for edge: vertext hits authority')
    parser.add_argument('--vertex-hits-hubs-property', action='store', dest='vertex_hubs',
                        default='vertex_hubs',
                        help='Label for edge: vertex hits hubs')


def run(input_file: KGTKFiles, directed, compute_degrees, compute_pagerank, compute_hits, log_file, output_stats,
        vertex_in_degree, vertex_out_degree, vertex_pagerank, vertex_auth, vertex_hubs):
    from kgtk.exceptions import KGTKException
    def infer_index(h, options=[]):
        for o in options:
            if o in h:
                return h.index(o)
        return -1

    def infer_predicate(h, options=[]):
        for o in options:
            if o in h:
                return o
        return ''

    v_prop_dict = {
        'vertex_pagerank': vertex_pagerank,
        'vertex_hubs': vertex_hubs,
        'vertex_auth': vertex_auth
    }
    try:
        # import modules locally
        import socket
        from graph_tool import load_graph_from_csv
        from graph_tool import centrality
        import kgtk.gt.analysis_utils as gtanalysis
        from pathlib import Path
        import sys
        import csv
        csv.field_size_limit(sys.maxsize)

        filename: Path = KGTKArgumentParser.get_input_file(input_file)

        # hardcoded values useful for the script. Perhaps some of them should be exposed as arguments later
        directions = ['in', 'out', 'total']
        id_col = 'name'

        with open(filename, 'r') as f:
            header = next(f).split('\t')
            header=[h.strip() for h in header]
            subj_index = infer_index(header, options=['node1', 'subject'])
            obj_index = infer_index(header, options=['node2', 'object', 'value'])
            predicate = infer_predicate(header, options=['label', 'predicate', 'relation', 'relationship'])
            p = []
            for i, header_col in enumerate(header):
                if i in [subj_index, obj_index]: continue
                p.append(header_col)
        with open(log_file, 'w') as writer:

            writer.write('loading the TSV graph now ...\n')
            G2 = load_graph_from_csv(str(filename),
                                     skip_first=True,
                                     directed=directed,
                                     hashed=True,
                                     ecols=[subj_index, obj_index],
                                     eprop_names=p,
                                     csv_options={'delimiter': '\t'})

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
                result = gtanalysis.get_topn_indices(G2, 'vertex_pagerank', 5, id_col)
                for n_id, n_label, pr in result:
                    writer.write('%s\t%s\t%f\n' % (n_id, n_label, pr))

            if compute_hits:
                writer.write('\n###HITS\n')
                hits_eig, G2.vp['vertex_hubs'], G2.vp['vertex_auth'] = gtanalysis.compute_hits(G2)
                writer.write('HITS hubs\n')
                main_hubs = gtanalysis.get_topn_indices(G2, 'vertex_hubs', 5, id_col)
                for n_id, n_label, hubness in main_hubs:
                    writer.write('%s\t%s\t%f\n' % (n_id, n_label, hubness))
                writer.write('HITS auth\n')
                main_auth = gtanalysis.get_topn_indices(G2, 'vertex_auth', 5, id_col)
                for n_id, n_label, authority in main_auth:
                    writer.write('%s\t%s\t%f\n' % (n_id, n_label, authority))

            sys.stdout.write('node1\tlabel\tnode2\tid\n')
            id_count = 0
            if not output_stats:
                for e in G2.edges():
                    sid, oid = e
                    lbl = G2.ep[predicate][e]
                    sys.stdout.write(
                        '%s\t%s\t%s\t%s\n' % (G2.vp[id_col][sid], lbl, G2.vp[id_col][oid],
                                              '{}-{}-{}'.format(G2.vp[id_col][sid], lbl, id_count)))
                    id_count += 1

            id_count = 0
            for v in G2.vertices():
                v_id = G2.vp[id_col][v]

                sys.stdout.write(
                    '{}\t{}\t{}\t{}\n'.format(v_id, vertex_in_degree, v.in_degree(),
                                              '{}-{}-{}'.format(v_id, vertex_in_degree, id_count)))
                id_count += 1
                sys.stdout.write(
                    '{}\t{}\t{}\t{}\n'.format(v_id, vertex_out_degree, v.out_degree(),
                                              '{}-{}-{}'.format(v_id, vertex_out_degree, id_count)))
                id_count += 1

                for vprop in G2.vertex_properties.keys():
                    if vprop == id_col: continue
                    sys.stdout.write(
                        '%s\t%s\t%s\t%s\n' % (v_id, v_prop_dict[vprop], G2.vp[vprop][v],
                                              '{}-{}-{}'.format(v_id, v_prop_dict[vprop], id_count)))
                    id_count += 1

    except Exception as e:
        raise KGTKException('Error: ' + str(e))
