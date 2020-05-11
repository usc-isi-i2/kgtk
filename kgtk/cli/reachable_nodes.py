"""
Find reachable nodes given a set of root nodes and properties
"""


def parser():
    return {
        'help': 'Find reachable nodes in a graph.'
    }


def add_arguments(parser):
    """
    Parse arguments
    Args:
            parser (argparse.ArgumentParser)
    """
    parser.add_argument(action="store", type=str, dest="filename", metavar='filename', help='input filename here')
    parser.add_argument('--root',action='store',dest='root',help='File containing the set of root nodes')
    parser.add_argument('-o', '--out', action='store', type=str, dest='output', help='File to output the reachable nodes,if empty will be written out to standard output',default=None)
    parser.add_argument("--noheader", action="store_true", dest="header_bool", help="Option to specify that file does not have a header")
    parser.add_argument("--subj", action="store", type=int, dest="sub", help='Column in which the subject is given, default 0', default=0)
    parser.add_argument("--obj", action="store", type=int, dest="obj", help='Column in which the subject is given, default 2', default=2)
    parser.add_argument("--pred",action="store" ,type=int, dest="pred",help='Column in which predicate is given, default 1',default=1)
    parser.add_argument("--props", action="store", type=str, dest="props",help='Properties to consider while finding reachable nodes - comma-separated string, default all properties considered',default=None)
    parser.add_argument('--undirected', action='store_true', dest="undirected", help="Option to specify graph as undirected?")


def run(filename,root,output,header_bool,sub,obj,pred,props,undirected):
    import sys
    import csv
    from graph_tool.search import dfs_iterator
    from graph_tool import load_graph_from_csv
    from graph_tool.util import find_edge
    from kgtk.exceptions import KGTKException
    from kgtk.cli_argparse import KGTKArgumentParser

    def find_pred_position(sub,pred,obj):
        if pred < sub and pred < obj:
            return pred
        elif (pred > sub and pred < obj) or (pred<sub and pred>obj):
            return pred-1
        else:
            return pred-2

    def get_edges_by_edge_prop(g, p, v):
        return find_edge(g, prop=g.properties[('e', p)], match=v)

    label='c'+str(find_pred_position(sub,pred,obj))
    header=['node1','label','node2']
    root_list=[]
    property_list=[]

    tsv_file = open(root)
    read_tsv = csv.reader(tsv_file, delimiter="\t")

    for row in read_tsv:
        root_list.append(row[0])
    tsv_file.close()
    property_list = [item for item in props.split(',')]
    G = load_graph_from_csv(filename,not(undirected),skip_first=not(header_bool),hashed=True,csv_options={'delimiter': '\t'},ecols=(sub,obj))

    name = G.vp["name"]

    index_list = []
    for v in G.vertices():
        if name[v] in root_list:
            index_list.append(v)

    edge_filter_set = set()
    for prop in property_list:
        edge_filter_set.update(get_edges_by_edge_prop(G, label,prop));
    e_prop= G.new_edge_property("bool")

    v_prop= G.new_vertex_property("bool")
    for e in G.edges():
        if e in edge_filter_set:
            e_prop[e] = True
            v_prop[e.source()] = True
            v_prop[e.target()] = True
        else:
            e_prop[e] = False
            if(v_prop[e.source()] is None):
                v_prop[e.source()] = False
            if(v_prop[e.target()] is None):
                v_prop[e.target()] = False
    G.set_edge_filter(e_prop)
    G.set_vertex_filter(v_prop)


    if output:
        f=open(output,'w')
        tsv_writer = csv.writer(f, quoting=csv.QUOTE_NONE,delimiter="\t",escapechar="\n",quotechar='')
        if index_list == []:
            print("No root nodes found in the graph")
        else:
            tsv_writer.writerow(header)
            for index in index_list:
                for e in dfs_iterator(G, G.vertex(index)):
                    tsv_writer.writerow([name[index], 'reachable', name[e.target()]])
        f.close()
    else:
        if index_list == []:
            print("No root nodes found in the graph")
        else:
            sys.stdout.write('%s\t%s\t%s\n' % ('node1', 'label', 'node2'))
            for index in index_list:
                for e in dfs_iterator(G, G.vertex(index)):
                    sys.stdout.write('%s\t%s\t%s\n' % (name[index], 'reachable', name[e.target()]))