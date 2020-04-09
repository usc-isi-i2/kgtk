"""
Import CSV file in Graph-tool.
"""


def parser():
    return {
        'help': 'Import a CSV file in Graph-tool.'
    }


def add_arguments(parser):
    """
    Parse arguments
    Args:
            parser (argparse.ArgumentParser)
    """
    parser.add_argument(action="store", type=str, dest="filename", metavar='filename', help='filename here')
    parser.add_argument("--header", action="store_true", dest="header_bool", help="Does the file contain a header in its first row")
    parser.add_argument("--subj", action="store", type=int, dest="sub", help='Column in which the subject is given, default 0', default=0)
    parser.add_argument("--obj", action="store", type=int, dest="obj", help='Column in which the subject is given, default 2', default=2)
    parser.add_argument('--pred', action='store', type=str, dest="props", help="Edge properties to store in their order of appearance - comma-separated string.")
    parser.add_argument('--directed', action='store_true', dest="directed", help="Is the graph directed or not?")
    parser.add_argument('-o', '--out', action='store', type=str, dest='output', help='Graph tool file to dump the graph too - if empty, it will not be saved.')

def run(filename, header_bool, sub, obj, props, directed, output):
    # import modules locally
    import socket
    from graph_tool import load_graph_from_csv
    from kgtk.exceptions import KGTKException

    try:
            
        p=props.split(',')
        print('loading the TSV graph now ...')
        #filename='/nas/home/ilievski/kgtk/data/conceptnet_first10.tsv'
        #G2=load_graph_from_csv(filename)
        #print('yo')
        G2 = load_graph_from_csv(filename, 
                                                        skip_first=header_bool, 
                                                        directed=directed, 
                                                        hashed=True, 
                                                        ecols=[sub,obj],
                                                        eprop_names=props.split(','), 
                                                        csv_options={'delimiter': '\t'})

        print('graph loaded! It has %d nodes and %d edges' % (G2.num_vertices(), G2.num_edges()))

        if output:
                print('now saving the graph to %s' % output)
                G2.save(output)
    except:
        raise KGTKException
