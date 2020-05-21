"""
Find connected components in a graph
"""


def parser():
    return {
        'help': 'Find connected components in a graph.'
    }


def add_arguments(parser):
    """
    Parse arguments
    Args:
            parser (argparse.ArgumentParser)
    """
    parser.add_argument(action="store", type=str, dest="filename", metavar='filename', help='input filename here')
    parser.add_argument('-o', '--out', action='store', type=str, dest='output', help='File to output the edge file with respective components,if empty will be written out to standard output',default=None)
    parser.add_argument("--noheader", action="store_true", dest="header_bool", help="Option to specify that file does not have a header")
    parser.add_argument("--subj", action="store", type=int, dest="sub", help='Column in which the subject is given, default 0', default=0)
    parser.add_argument("--obj", action="store", type=int, dest="obj", help='Column in which the subject is given, default 2', default=2)
    parser.add_argument("--pred",action="store" ,type=int, dest="pred",help='Column in which predicate is given, default 1',default=1)
    parser.add_argument("--props", action="store", type=str, dest="props",help='Properties to consider while finding connected components - comma-separated string, default all properties considered',default=None)
    parser.add_argument('--undirected', action='store_true', dest="undirected", help="Option to specify graph as undirected?")
    parser.add_argument('--strong', action='store_true', dest="strong", help="If graph is directed, strongly connected components or treat graph as undirected")


    
def run(filename,output,header_bool,sub,obj,pred,props,undirected,strong):
    # import modules locally
    import csv 
    import sys
    from graph_tool import load_graph_from_csv
    from graph_tool.util import find_edge
    from graph_tool.topology import label_components
    from kgtk.exceptions import KGTKException
    from kgtk.cli_argparse import KGTKArgumentParser
    

    def find_pred_position(sub,pred,obj):
        if pred < sub and pred < obj:
            return pred
        elif (pred > sub and pred < obj) or (pred<sub and pred>obj):
            return pred-1
        else:
            return pred-2
    try:
        header=['node1','label','node2']
        label='c'+str(find_pred_position(sub,pred,obj))
        g=load_graph_from_csv(filename,not(undirected),skip_first=not(header_bool),hashed=True,csv_options={'delimiter': '\t'},ecols=(sub,obj))
        es=[]
        if props:
            properties=props.split(',')
            for e in properties:
                es+=(find_edge(g,g.edge_properties[label],e))        
            g.clear_edges()
            g.add_edge_list(list(set(es)))
        comp, hist= label_components(g,directed=strong)
        if output:
            f=open(output,'w')
            wr = csv.writer(f, quoting=csv.QUOTE_NONE,delimiter="\t",escapechar="\n",quotechar='')
            wr.writerow(header)
            for v,c in enumerate(comp):
                wr.writerow([g.vertex_properties['name'][v],'connected_component',c])
            f.close()
        else:
            sys.stdout.write('%s\t%s\t%s\n' % ('node1', 'label', 'node2'))
            for v,c in enumerate(comp):
                sys.stdout.write('%s\t%s\t%s\n' % (g.vertex_properties['name'][v], 'connected_component', str(c)))
    except:
        raise KGTKException