import graph_tool as gtmain
import graph_tool.all as gtall
import graph_tool.topology as gttop


def get_nodes_with_degree(g, deg_from, deg_to):
    u = gtmain.GraphView(g, vfilt=lambda v: v.in_degree()+v.out_degree() in range(deg_from,deg_to))
    return u

def get_nodes_by_node_prop(g, p, v):
    return gtall.find_vertex(g, prop=g.properties[('v', p)], match=v)

def get_edges_by_edge_prop(g, p, v):
    return gtall.find_edge(g, prop=g.properties[('e', p)], match=v)

def get_neighbors(g, node_id, direction):
    the_node=get_nodes_by_node_prop(g, '_graphml_vertex_id', node_id)[0]
    if direction=='out':
        return set(the_node.out_neighbors())
    elif direction=='in':
        return set(the_node.in_neighbors())
    else: # total
        return set(the_node.out_neighbors()) | set(the_node.in_neighbors())

def compute_transitive_closure(g):
    return gttop.transitive_closure(g)
