import graph_tool as gtmain
import graph_tool.all as gtall
import numpy as np  # type: ignore
from collections import defaultdict

import matplotlib.pyplot as plt  # type: ignore

plt.rcParams.update({'font.size': 12})

import seaborn as sns  # type: ignore

sns.set_style("whitegrid")


#### BASIC STATS ####

def get_num_nodes(g):
    return g.num_vertices()


def get_num_edges(g):
    return g.num_edges()


#### DEGREES ####

def compute_avg_node_degree(g, direction):
    return gtmain.stats.vertex_average(g, direction)


def compute_node_degree_hist(g, direction):
    return gtall.vertex_hist(g, direction, float_count=False)


def get_degree_maxn_counts(g, direction):
    return list(compute_node_degree_hist(g, direction)[0])[:10]


def plot_degrees(degrees, plottype='loglog', base=10, xlabel='', ylabel='', title=''):
    plt.loglog(degrees, basex=base, basey=base)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.title(title)
    plt.show()


#### CENTRALITY ####

def compute_betweenness(g):
    bn, be = gtmain.centrality.betweenness(g)
    return bn, be


def compute_pagerank(g):
    v_pr = g.new_vertex_property('float')
    gtmain.centrality.pagerank(g, prop=v_pr)
    return v_pr


def compute_hits(g):
    hits_eig, v_hubs, v_auth = gtmain.centrality.hits(g)
    return hits_eig, v_hubs, v_auth


def get_max_node(g, prop):
    max_pr = 0.0
    max_pr_vertex = None
    for v in g.vertices():
        vertex_pr = g.vp[prop][v]
        if vertex_pr > max_pr:
            max_pr = vertex_pr
            max_pr_vertex = g.vp['_graphml_vertex_id'][v]

    return max_pr, max_pr_vertex


def get_topn_indices(g, prop, n, print_prop):
    a = g.vp[prop].a
    ind = np.argpartition(a, -n)[-n:]
    result = []
    for i in ind:
        result.append([i, g.vp[print_prop][i], g.vp[prop][i]])
    return sorted(result, key=lambda x: x[-1], reverse=True)


#### RUN ALL STATS ####

def compute_stats(g, direction):
    avg_degree, stdev_degree = compute_avg_node_degree(g, direction)
    return {
        'num_nodes': get_num_nodes(g),
        'num_edges': get_num_edges(g),
        'avg_degree': avg_degree,
        'degree_maxn_counts': get_degree_maxn_counts(g, direction),
        'stdev_degree': stdev_degree
    }


def get_topN_relations(g, N=10, pred_property='predicate'):
    rel_freq = defaultdict(int)
    for i, e in enumerate(g.edges()):
        r = g.edge_properties[pred_property][e]
        rel_freq[r] += 1
    return sorted(rel_freq.items(), key=lambda x: x[1], reverse=True)[:N]
