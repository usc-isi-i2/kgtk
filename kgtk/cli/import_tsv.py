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
    parser.add_argument('--degrees', action='store_true', dest='compute_degrees', help="Whether or not to compute degree distribution.")
    parser.add_argument('--pagerank', action='store_true', dest='compute_pagerank', help="Whether or not to compute PageRank centraility.")
    parser.add_argument('--hits', action='store_true', dest='compute_hits', help="Whether or not to compute HITS centraility.")
    parser.add_argument('-o', '--out', action='store', type=str, dest='output', help='Graph tool file to dump the graph too - if empty, it will not be saved.')

def run(filename, header_bool, sub, obj, props, directed, compute_degrees, compute_pagerank, compute_hits, output):

	try:
		# import modules locally
		import socket
		from graph_tool import load_graph_from_csv
		from graph_tool import centrality
		import kgtk.gt.analysis_utils as gtanalysis
		from kgtk.exceptions import KGTKException

		# hardcoded values useful for the script. Perhaps some of them should be exposed as arguments later
		directions=['in', 'out', 'total']
		id_col='name'

		p=props.split(',')
		print('loading the TSV graph now ...')
		G2 = load_graph_from_csv(filename, 
								skip_first=header_bool, 
								directed=directed, 
								hashed=True, 
								ecols=[sub,obj],
								eprop_names=props.split(','), 
								csv_options={'delimiter': '\t'})

		print('graph loaded! It has %d nodes and %d edges' % (G2.num_vertices(), G2.num_edges()))		
		print('\n###Top relations:')
		print(*gtanalysis.get_topN_relations(G2), sep='\n')

		if compute_degrees:
			print('\n###Degrees:')
			for direction in directions:
				degree_data=gtanalysis.compute_node_degree_hist(G2, direction)
				max_degree=len(degree_data)-1
				mean_degree, std_degree= gtanalysis.compute_avg_node_degree(G2, direction)
				print('%s degree stats: mean=%f, std=%f, max=%d' % (direction, mean_degree, std_degree, max_degree))


		if compute_pagerank:
			print('\n###PageRank')
			v_pr = G2.new_vertex_property('float')
			centrality.pagerank(G2, prop=v_pr)
			G2.properties[('v', 'vertex_pagerank')] = v_pr 
			print('Max pageranks')
			gtanalysis.get_topn_indices(G2, 'vertex_pagerank', 5, id_col)

		if compute_hits:
			print('\n###HITS')
			hits_eig, G2.vp['vertex_hubs'], G2.vp['vertex_auth']=gtanalysis.compute_hits(G2)
			print('HITS hubs')
			gtanalysis.get_topn_indices(G2, 'vertex_hubs', 5, id_col)
			print('HITS auth')
			gtanalysis.get_topn_indices(G2, 'vertex_auth', 5, id_col)

		if output:
				print('now saving the graph to %s' % output)
				G2.save(output)
	except Exception as e:
		raise KGTKException('Error: ' + str(e))
	
