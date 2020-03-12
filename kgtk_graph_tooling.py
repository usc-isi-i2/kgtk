import graph_tool
from kgtk.gt import analysis_utils, topology_utils

#input_file="P279_sorted_by_node.csv"
input_file="first100k_P279.csv"
direction='total'

G=graph_tool.load_graph_from_csv(input_file,
                                 directed=True,
                                 skip_first=True,
                                 ecols=(0,2),
                                 csv_options={'delimiter': ',', 'quotechar': '"'})

print(analysis_utils.get_num_nodes(G))

print(analysis_utils.get_num_edges(G))

print(analysis_utils.compute_stats(G, direction))
print('now computing transitive closure')
G2=topology_utils.compute_transitive_closure(G)
print('transitive closure computed')

print(analysis_utils.get_num_nodes(G2))

print(analysis_utils.get_num_edges(G2))

print(analysis_utils.compute_stats(G2, direction))
