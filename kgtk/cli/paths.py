"""
Compute paths between nodes in a KGTK graph.
"""

def parser():
    return {
        'help': 'Compute paths between nodes in a KGTK graph.'
    }


def add_arguments(parser):
    """
    Parse arguments
    Args:
            parser (argparse.ArgumentParser)
    """
    parser.add_argument('--i', action="store", type=str, dest="filename", help='Input filename')
    parser.add_argument('--directed', action='store_true', dest="directed", help="Is the graph directed or not?")
    parser.add_argument('--max_hops', action="store", type=int, dest="max_hops", help="Maximum number of hops allowed.")
    parser.add_argument('--source_nodes', action="store", nargs="*", dest="source_nodes", help="List of source nodes")
    parser.add_argument('--target_nodes', action="store", nargs="*", dest="target_nodes", help="List of target nodes")
    parser.add_argument('--graph_edge', action="store", type=str, dest="graph_edge", default="graph", help="Name of the secondary edge type that stores the path id, default is 'graph'.")

def run(filename, directed, max_hops, source_nodes, target_nodes, graph_edge):
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

    try:
        # import modules locally
        import socket
        from graph_tool import load_graph_from_csv
        from graph_tool import centrality
        from graph_tool.all import find_vertex
        from graph_tool.topology import all_paths
        import sys
        from collections import defaultdict

        id_col = 'name'

        with open(filename, 'r') as f:
            header = next(f).split('\t')
            subj_index = infer_index(header, options=['node1', 'subject'])
            obj_index = infer_index(header, options=['node2', 'object', 'value'])
            predicate = infer_predicate(header, options=['property', 'predicate', 'label'])

            p = []
            for i, header_col in enumerate(header):
                if i in [subj_index, obj_index]: continue
                p.append(header_col)

        if 'id' not in p:
            raise KGTKException('Error: no id column found')

        G = load_graph_from_csv(filename,
                                 skip_first=True,
                                 directed=directed,
                                 hashed=True,
                                 ecols=[subj_index, obj_index],
                                 eprop_names=p,
                                 csv_options={'delimiter': '\t'})

        graph_id=1
        paths=defaultdict(set)
        for source_node in source_nodes:
            source_ids=find_vertex(G, prop=G.properties[('v', id_col)], match=source_node)
            if len(source_ids)==1:
                source_id=source_ids[0]
                for target_node in target_nodes:
                    target_ids=find_vertex(G, prop=G.properties[('v', id_col)], match=target_node)
                    if len(target_ids)==1:
                        target_id=target_ids[0]
                        for path in all_paths(G, source_id, target_id, cutoff=max_hops, edges=True):
                            for an_edge in path:
                                edge_id=G.properties[('e', 'id')][an_edge]
                                paths[edge_id].add(str(graph_id))
                            graph_id+=1

        sys.stdout.write('node1\tlabel\tnode2\tid\t%s\n' % graph_edge)
        for e in G.edges():
            sid, oid = e
            edge_id=G.properties[('e', 'id')][e]
            lbl = G.ep[predicate][e]
            graph_id='|'.join(list(paths[edge_id]))
            sys.stdout.write(
                '%s\t%s\t%s\t%s\t%s\n' % (G.vp[id_col][sid], lbl, G.vp[id_col][oid],
                                      edge_id,  
                                      graph_id))

    except Exception as e:
        raise KGTKException('Error: ' + str(e))
