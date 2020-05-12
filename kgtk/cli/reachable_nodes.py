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
    parser.add_argument('--root',action='store',dest='root',help='Set of root nodes to use, comma-separated string',default=None)
    parser.add_argument('--rootfile',action='store',dest='rootfile',help='Option to specify a file containing the set of root nodes',default=None)
    parser.add_argument('--rootfilecolumn',action='store',type=int,dest='rootfilecolumn',help='Option to specify column of roots file to use, default 0',default=0)
    parser.add_argument('--norootheader',action='store_true',dest='root_header_bool',help='Option to specify that root file has no header')
    parser.add_argument('-o', '--out', action='store', type=str, dest='output', help='File to output the reachable nodes,if empty will be written out to standard output',default=None)
    parser.add_argument("--noheader", action="store_true", dest="header_bool", help="Option to specify that file does not have a header")
    parser.add_argument("--subj", action="store", type=int, dest="sub", help='Column in which the subject is given, default 0', default=0)
    parser.add_argument("--obj", action="store", type=int, dest="obj", help='Column in which the subject is given, default 2', default=2)
    parser.add_argument("--pred",action="store" ,type=int, dest="pred",help='Column in which predicate is given, default 1',default=1)
    parser.add_argument("--props", action="store", type=str, dest="props",help='Properties to consider while finding reachable nodes - comma-separated string,default all properties',default=None)
    parser.add_argument('--undirected', action='store_true', dest="undirected", help="Option to specify graph as undirected?")


def run(filename,root,rootfile,rootfilecolumn,root_header_bool,output,header_bool,sub,obj,pred,props,undirected):
    import sys
    import csv
    import time
    from graph_tool.search import dfs_iterator
    from graph_tool import load_graph_from_csv
    from graph_tool.util import find_edge
    from kgtk.exceptions import KGTKException
    from kgtk.cli_argparse import KGTKArgumentParser


    #Graph-tool names columns that are not subject or object c0, c1... This function finds the number that graph tool assigned to the predicate column
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
    root_set=set()
    property_list=[]

    if (rootfile):
        tsv_file = open(rootfile)
        read_tsv = csv.reader(tsv_file, delimiter="\t")
        first_row=True
        for row in read_tsv:
            if first_row and not root_header_bool:
                    first_row=False
                    continue
            root_set.add(row[rootfilecolumn])
        tsv_file.close()
    if (root):
        for r in root.split(','):
            root_set.add(r)

    G = load_graph_from_csv(filename,not(undirected),skip_first=not(header_bool),hashed=True,csv_options={'delimiter': '\t'},ecols=(sub,obj))

    name = G.vp["name"]

    index_list = []
    for v in G.vertices():
        if name[v] in root_set:
            index_list.append(v)

    edge_filter_set = set()
    if props:
        property_list = [item for item in props.split(',')]
        for prop in property_list:
            edge_filter_set.update(get_edges_by_edge_prop(G, label,prop));        
        G.clear_edges()
        G.add_edge_list(list(edge_filter_set))

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
