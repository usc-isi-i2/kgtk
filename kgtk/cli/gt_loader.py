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
    parser.add_argument('--log', action='store', type=str, dest='log_file', help='Log file for summarized statistics of the graph.', default="./log.txt")
    parser.add_argument('-o', '--out', action='store', type=str, dest='output', help='Graph tool file to dump the graph too - if empty, it will not be saved.')

def run(filename, header_bool, sub, obj, props, directed, compute_degrees, compute_pagerank, compute_hits, log_file, output):

	try:
		# import modules locally
		import socket
		from graph_tool import load_graph_from_csv
		from graph_tool import centrality
		import kgtk.gt.analysis_utils as gtanalysis
		from kgtk.exceptions import KGTKException
		import sys

		# hardcoded values useful for the script. Perhaps some of them should be exposed as arguments later
		directions=['in', 'out', 'total']
		id_col='name'

		p=props.split(',')
		predicate=p[0]
		with open(log_file, 'w') as writer:

			writer.write('loading the TSV graph now ...\n')
			G2 = load_graph_from_csv(filename, 
									skip_first=header_bool, 
									directed=directed, 
									hashed=True, 
									ecols=[sub,obj],
									eprop_names=props.split(','), 
									csv_options={'delimiter': '\t'})

			writer.write('graph loaded! It has %d nodes and %d edges\n' % (G2.num_vertices(), G2.num_edges()))		
			writer.write('\n###Top relations:\n')
			for rel, freq in gtanalysis.get_topN_relations(G2):
				writer.write('%s\t%d\n' % (rel, freq))

			if compute_degrees:
				writer.write('\n###Degrees:\n')
				for direction in directions:
					degree_data=gtanalysis.compute_node_degree_hist(G2, direction)
					max_degree=len(degree_data)-1
					mean_degree, std_degree= gtanalysis.compute_avg_node_degree(G2, direction)
					writer.write('%s degree stats: mean=%f, std=%f, max=%d\n' % (direction, mean_degree, std_degree, max_degree))

			if compute_pagerank:
				writer.write('\n###PageRank\n')
				v_pr = G2.new_vertex_property('float')
				centrality.pagerank(G2, prop=v_pr)
				G2.properties[('v', 'vertex_pagerank')] = v_pr 
				writer.write('Max pageranks\n')
				result=gtanalysis.get_topn_indices(G2, 'vertex_pagerank', 5, id_col)
				for n_id, n_label, pr in result:
					writer.write('%s\t%s\t%f\n' % (n_id, n_label, pr))

			if compute_hits:
				writer.write('\n###HITS\n')
				hits_eig, G2.vp['vertex_hubs'], G2.vp['vertex_auth']=gtanalysis.compute_hits(G2)
				writer.write('HITS hubs\n')
				main_hubs=gtanalysis.get_topn_indices(G2, 'vertex_hubs', 5, id_col)
				for n_id, n_label, hubness in main_hubs:
					writer.write('%s\t%s\t%f\n' % (n_id, n_label, hubness))
				writer.write('HITS auth\n')
				main_auth=gtanalysis.get_topn_indices(G2, 'vertex_auth', 5, id_col)
				for n_id, n_label, authority in main_auth:
					writer.write('%s\t%s\t%f\n' % (n_id, n_label, authority))

			for e in G2.edges():
				sid, oid=e
				lbl=G2.ep[predicate][e]
				sys.stdout.write('%s\t%s\t%s\n' % (G2.vp[id_col][sid], lbl, G2.vp[id_col][oid]))

			for v in G2.vertices():
				v_id=G2.vp[id_col][v]
				for vprop in G2.vertex_properties.keys():
					if vprop==id_col: continue
					sys.stdout.write('%s\t%s\t%s\n' % (v_id, vprop, G2.vp[vprop][v]))

			if output:
					writer.write('now saving the graph to %s\n' % output)
					G2.save(output)
	except Exception as e:
		raise KGTKException('Error: ' + str(e))
	
