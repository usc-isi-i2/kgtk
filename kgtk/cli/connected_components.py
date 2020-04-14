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
    parser.add_argument('-i','--inp',action="store", type=str, dest="filename", metavar='filename', help='filename here')
    parser.add_argument('-o', '--out', action='store', type=str, dest='output', help='File to output the nodes file with respective components')
    parser.add_argument("--header", action="store",type=bool, dest="header_bool", help="Does the file contain a header in its first row",default=True)
    parser.add_argument("--subj", action="store", type=int, dest="sub", help='Column in which the subject is given, default 0', default=0)
    parser.add_argument("--obj", action="store", type=int, dest="obj", help='Column in which the subject is given, default 2', default=2)
    parser.add_argument("--props", action="store", type=str, dest="props",help='Properties to consider while finding connected components - comma-separated string, default all properties considered',default=None)
    parser.add_argument('--directed', action='store',type=bool, dest="directed", help="Is the graph directed or not?",default=True)
    parser.add_argument('--strong', action='store',type=bool, dest="strong", help="If graph is directed, strongly connected components or treat graph as undirected",default=False)


    
def run(filename,output,directed,header,sub,obj,props,strong):
    # import modules locally
    import csv 
    from graph_tool import load_graph_from_csv
    from graph_tool.util import find_edge
    from graph_tool.topology import label_components
    from kgtk.exceptions import KGTKException
    
    try:
        g=load_graph_from_csv(filename,directed,skip_first=header,hashed=True,csv_options={'delimiter': '\t'},ecols=(sub,obj))
        es=[]
        if props:
            properties=props.split(',')
            for e in properties:
                es+=(find_edge(g,g.edge_properties['c0'],e))        
            g.clear_edges()
            g.add_edge_list(list(set(es)))
        comp, hist= label_components(g,directed=strong)
        f=open(output,'w')
        wr = csv.writer(f, quoting=csv.QUOTE_NONE,delimiter="\t",escapechar="\n",quotechar='')
        wr.writerow(['node','component'])
        for v,c in enumerate(comp):
            wr.writerow([g.vertex_properties['name'][v],c])
        f.close()
    except:
        raise KGTKException