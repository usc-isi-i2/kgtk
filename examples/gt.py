import kgtk.gt.io_utils as gtio
import kgtk.gt.analysis_utils as gtanalysis

#datadir='data/'
mowgli_nodes=f'{datadir}nodes_v002.csv'
mowgli_edges=f'{datadir}edges_v002.csv'
output_gml=f'{datadir}graph.graphml'

gtio.transform_to_graphtool_format(mowgli_nodes, mowgli_edges, output_gml, True)
g=gtio.load_gt_graph(output_gml.replace(".graphml", '.gt'))

print(g.num_edges())
