"""
Compute paths between nodes in a KGTK graph.

TODO: Add --output-file
"""

import sys
from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles

def parser():
    return {
        'help': 'Compute paths between nodes in a KGTK graph.'
    }


def add_arguments(parser: KGTKArgumentParser):
    """
    Parse arguments
    Args:
            parser (argparse.ArgumentParser)
    """
    parser.add_input_file(positional=True)
    parser.add_input_file(who="KGTK file with path start and end nodes.",
                          options=["--path_file"], dest="path_file", metavar="PATH_FILE")
    parser.add_argument('--statistics-only', action='store_true', dest='output_stats',
                        help='If this flag is set, output only the statistics edges. Else, append the statistics to the original graph.')

    parser.add_argument('--directed', action='store_true', dest="directed", help="Is the graph directed or not?")
    parser.add_argument('--max_hops', action="store", type=int, dest="max_hops", help="Maximum number of hops allowed.")

def run(input_file: KGTKFiles, path_file, output_stats, directed, max_hops):
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

    try:
        # import modules locally
        from kgtk.exceptions import KGTKException
        import socket
        from graph_tool import load_graph_from_csv
        from graph_tool import centrality
        from graph_tool.all import find_vertex
        from graph_tool.topology import all_paths
        import sys
        import csv
        from collections import defaultdict
        csv.field_size_limit(sys.maxsize)
        id_col = 'name'
    
        pairs=[]
        with open(path_file, 'r') as f:
            header=next(f)
            for line in f:
                src, tgt=line.strip().split('\t')
                pairs.append((src, tgt))
        filename: Path = KGTKArgumentParser.get_input_file(input_file)
        with open(filename, 'r') as f:
            header = next(f).strip().split('\t')
            subj_index = infer_index(header, options=['node1', 'subject'])
            obj_index = infer_index(header, options=['node2', 'object', 'value'])
            predicate = infer_predicate(header, options=['property', 'predicate', 'label'])

            p = []
            for i, header_col in enumerate(header):
                if i in [subj_index, obj_index]: continue
                p.append(header_col)

        if 'id' not in p:
            raise KGTKException('Error: no id column found')
        G = load_graph_from_csv(str(filename),
                                 skip_first=True,
                                 directed=directed,
                                 hashed=True,
                                 ecols=[subj_index, obj_index],
                                 eprop_names=p,
                                 csv_options={'delimiter': '\t'})

        sys.stdout.write('node1\tlabel\tnode2\tid\n')
        id_count = 0
        if not output_stats:
            for e in G.edges():
                sid, oid = e
                lbl = G.ep[predicate][e]
                sys.stdout.write(
                    '%s\t%s\t%s\t%s\n' % (G.vp[id_col][sid], lbl, G.vp[id_col][oid],
                                          '{}-{}-{}'.format(G.vp[id_col][sid], lbl, id_count)))
                id_count += 1

        id_count=0
        path_id=0
        paths=defaultdict(set)
        for pair in pairs:
            source_node, target_node=pair
            source_ids=find_vertex(G, prop=G.properties[('v', id_col)], match=source_node)
            target_ids=find_vertex(G, prop=G.properties[('v', id_col)], match=target_node)
            if len(source_ids)==1 and len(target_ids)==1:
                source_id=source_ids[0]
                target_id=target_ids[0]
                for path in all_paths(G, source_id, target_id, cutoff=max_hops, edges=True):
                    for edge_num, an_edge in enumerate(path):
                        edge_id=G.properties[('e', 'id')][an_edge]
                        node1='p%d' % path_id
                        sys.stdout.write(
                                '%s\t%d\t%s\t%s\n' % (node1, edge_num, edge_id, '{}-{}-{}'.format(node1, edge_num, id_count)))
                        id_count+=1
                    path_id+=1

    except Exception as e:
        raise KGTKException('Error: ' + str(e))
