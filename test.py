import topology_utils as tu
import graph_tool.all as gt

g=gt.random_graph(1000000, lambda: (3, 3))
g2=tu.compute_transitive_closure(g)

print(g2.num_edges(), g2.num_vertices(), g.num_edges())
