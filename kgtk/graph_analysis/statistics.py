from pathlib import Path
import sys

from graph_tool import centrality, clustering
from kgtk.exceptions import KGTKException
import kgtk.gt.analysis_utils as gtanalysis
from kgtk.gt.gt_load import load_graph_from_kgtk
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
from kgtk.io.kgtkwriter import KgtkWriter
from kgtk.value.kgtkvalueoptions import KgtkValueOptions
from typing import TextIO


class GraphStatistics(object):
    def __init__(self,
                 input_kgtk_file: Path,
                 output_kgtk_file: Path,
                 undirected: bool = False,
                 compute_pagerank: bool = True,
                 compute_hits: bool = True,
                 compute_betweenness: bool = False,
                 compute_local_clustering: bool = False,
                 compute_extended_clustering: bool = False,
                 edge_weight_property: str = None,
                 max_depth: int = None,
                 output_statistics_only: bool = False,
                 output_degrees: bool = True,
                 output_pagerank: bool = True,
                 output_hits: bool = True,
                 output_betweenness: bool = True,
                 output_local_clustering: bool = False,
                 output_extended_clustering: bool = False,
                 log_file: str = './summary.txt',
                 log_degrees_histogram: bool = True,
                 log_top_relations: bool = True,
                 log_top_pageranks: bool = True,
                 log_top_hits: bool = True,
                 top_n: int = 5,
                 vertex_in_degree: str = 'vertex_in_degree',
                 vertex_out_degree: str = 'vertex_out_degree',
                 vertex_pagerank: str = 'vertex_pagerank',
                 vertex_betweenness: str = 'vertex_betweenness',
                 vertex_auth: str = 'vertex_auth',
                 vertex_hubs: str = 'vertex_hubs',
                 vertex_extended_clustering_prefix: str = 'vertex_local_clustering',
                 vertex_local_clustering: str = 'vertex_extended_clustering_',
                 reader_options: KgtkReaderOptions = None,
                 value_options: KgtkValueOptions = None,
                 error_file: TextIO = sys.stderr,
                 verbose: bool = False,
                 very_verbose: bool = False
                 ):
        self.input_kgtk_file = input_kgtk_file
        self.output_kgtk_file = output_kgtk_file
        self.reader_options = reader_options
        self.value_options = value_options
        self.error_file = error_file
        self.verbose = verbose
        self.very_verbose = very_verbose
        self.undirected = undirected
        self.compute_pagerank = compute_pagerank
        self.compute_hits = compute_hits
        self.compute_betweenness = compute_betweenness
        self.compute_local_clustering = compute_local_clustering
        self.compute_extended_clustering = compute_extended_clustering
        self.edge_weight_property = edge_weight_property
        self.max_depth = max_depth
        self.output_statistics_only = output_statistics_only
        self.output_degrees = output_degrees
        self.output_pagerank = output_pagerank
        self.output_hits = output_hits
        self.output_betweenness = output_betweenness
        self.output_local_clustering = output_local_clustering
        self.output_extended_clustering = output_extended_clustering
        self.log_file = log_file
        self.log_degrees_histogram = log_degrees_histogram
        self.log_top_relations = log_top_relations
        self.log_top_pageranks = log_top_pageranks
        self.log_top_hits = log_top_hits
        self.top_n = top_n
        self.vertex_in_degree = vertex_in_degree
        self.vertex_out_degree = vertex_out_degree
        self.vertex_pagerank = vertex_pagerank
        self.vertex_betweenness = vertex_betweenness
        self.vertex_extended_clustering_prefix = vertex_extended_clustering_prefix
        self.vertex_local_clustering = vertex_local_clustering
        self.vertex_auth = vertex_auth
        self.vertex_hubs = vertex_hubs

    def process(self):
        try:

            # hardcoded values useful for the script. Perhaps some of them should be exposed as arguments later
            directions = ['in', 'out', 'total']
            id_col = 'name'
            output_columns = ["node1", "label", "node2", "id"]

            if self.verbose:
                print('loading the KGTK input file...\n', file=self.error_file, flush=True)
            kr: KgtkReader = KgtkReader.open(self.input_kgtk_file,
                                             error_file=self.error_file,
                                             options=self.reader_options,
                                             value_options=self.value_options,
                                             verbose=self.verbose,
                                             very_verbose=self.very_verbose,
                                             )
            sub: int = kr.get_node1_column_index()
            if sub < 0:
                print("Missing node1 (subject) column.", file=self.error_file, flush=True)
            pred: int = kr.get_label_column_index()
            if pred < 0:
                print("Missing label (predicate) column.", file=self.error_file, flush=True)
            obj: int = kr.get_node2_column_index()
            if obj < 0:
                print("Missing node2 (object) column", file=self.error_file, flush=True)
            if sub < 0 or pred < 0 or obj < 0:
                kr.close()
                raise KGTKException("Exiting due to missing columns.")

            predicate: str = kr.column_names[pred]

            G2 = load_graph_from_kgtk(kr,
                                      directed=not self.undirected,
                                      ecols=(sub, obj),
                                      verbose=self.verbose,
                                      out=self.error_file)
            if self.verbose:
                print('graph loaded! It has %d nodes and %d edges.' % (G2.num_vertices(), G2.num_edges()),
                      file=self.error_file, flush=True)
            kr.close()

            if self.compute_pagerank:
                if self.verbose:
                    print('Computing pagerank.', file=self.error_file, flush=True)
                v_pr = G2.new_vertex_property('float')
                centrality.pagerank(G2, prop=v_pr)
                G2.properties[('v', self.vertex_pagerank)] = v_pr

            if self.compute_betweenness:
                if self.verbose:
                    print('Computing betweenness.', file=self.error_file, flush=True)
                v_betweenness = G2.new_vertex_property('float')
                centrality.betweenness(G2, vprop=v_betweenness)
                G2.properties[('v', self.vertex_betweenness)] = v_betweenness

            if self.compute_local_clustering:
                if self.verbose:
                    print(f'Computing local clustering using edge weight={self.edge_weight_property}.',
                          file=self.error_file, flush=True)
                v_local_clustering = G2.new_vertex_property('float')
                weight = None
                if self.edge_weight_property:
                    weight = G2.copy_property(G2.edge_properties[self.edge_weight_property], value_type='float')
                clustering.local_clustering(G2, weight=weight, prop=v_local_clustering)
                G2.properties[('v', self.vertex_local_clustering)] = v_local_clustering

            if self.compute_extended_clustering:
                if self.verbose:
                    print(f'Computing extended clustering with max depth={self.max_depth}.',
                          file=self.error_file, flush=True)
                if self.max_depth:
                    clusters = clustering.extended_clustering(G2, max_depth=self.max_depth)
                else:
                    clusters = clustering.extended_clustering(G2)
                max_depth = len(clusters)
                for i in range(len(clusters)):
                    G2.properties[('v', f'{self.vertex_extended_clustering_prefix}{i + 1}')] = clusters[i]

            if self.compute_hits and not self.undirected:
                if self.verbose:
                    print('Computing HITS.', file=self.error_file, flush=True)
                hits_eig, G2.vp[self.vertex_hubs], G2.vp[self.vertex_auth] = gtanalysis.compute_hits(G2)

            if self.verbose:
                print('Opening the output file: %s' % repr(str(self.output_kgtk_file)), file=self.error_file,
                      flush=True)
            kw: KgtkWriter = KgtkWriter.open(output_columns,
                                             self.output_kgtk_file,
                                             mode=KgtkWriter.Mode.EDGE,
                                             require_all_columns=True,
                                             prohibit_extra_columns=True,
                                             fill_missing_columns=False,
                                             verbose=self.verbose,
                                             very_verbose=self.very_verbose)

            if not self.output_statistics_only:
                if self.verbose:
                    print('Copying the input edges to the output.', file=self.error_file, flush=True)
                id_count = 0
                for e in G2.edges():
                    sid, oid = e
                    lbl = G2.ep[predicate][e]
                    kw.write([G2.vp[id_col][sid], lbl, G2.vp[id_col][oid],
                              '{}-{}-{}'.format(G2.vp[id_col][sid], lbl, id_count)])
                    id_count += 1

            if self.output_degrees \
                    or self.output_pagerank \
                    or self.output_hits \
                    or self.output_betweenness \
                    or self.output_local_clustering \
                    or self.output_extended_clustering:
                if self.verbose:
                    print('Outputting vertex degrees and/or properties.', file=self.error_file, flush=True)
                id_count = 0
                for v in G2.vertices():
                    v_id = G2.vp[id_col][v]
                    if self.output_degrees:
                        kw.write([v_id, self.vertex_in_degree, str(v.in_degree()),
                                  '{}-{}-{}'.format(v_id, self.vertex_in_degree, id_count)])
                        id_count += 1
                        kw.write([v_id, self.vertex_out_degree, str(v.out_degree()),
                                  '{}-{}-{}'.format(v_id, self.vertex_out_degree, id_count)])
                        id_count += 1

                    if self.output_pagerank:
                        if self.vertex_pagerank in G2.vp:
                            kw.write([v_id, self.vertex_pagerank, str(G2.vp[self.vertex_pagerank][v]),
                                      '{}-{}-{}'.format(v_id, self.vertex_pagerank, id_count)])
                            id_count += 1

                    if self.output_hits:
                        if self.vertex_auth in G2.vp:
                            kw.write([v_id, self.vertex_auth, str(G2.vp[self.vertex_auth][v]),
                                      '{}-{}-{}'.format(v_id, self.vertex_auth, id_count)])
                            id_count += 1
                        if self.vertex_hubs in G2.vp:
                            kw.write([v_id, self.vertex_hubs, str(G2.vp[self.vertex_hubs][v]),
                                      '{}-{}-{}'.format(v_id, self.vertex_hubs, id_count)])
                            id_count += 1

                    if self.output_betweenness:
                        if self.vertex_betweenness in G2.vp:
                            kw.write([v_id, self.vertex_betweenness, str(G2.vp[self.vertex_betweenness][v]),
                                      '{}-{}-{}'.format(v_id, self.vertex_betweenness, id_count)])
                            id_count += 1

                    if self.output_local_clustering:
                        if self.vertex_local_clustering in G2.vp:
                            kw.write([v_id, self.vertex_local_clustering, str(G2.vp[self.vertex_local_clustering][v]),
                                      '{}-{}-{}'.format(v_id, self.vertex_local_clustering, id_count)])
                            id_count += 1

                    if self.output_extended_clustering and self.max_depth:
                        for i in range(self.max_depth):
                            vertex_name = f'{self.vertex_extended_clustering_prefix}{i + 1}'
                            if vertex_name in G2.vp:
                                kw.write([v_id, vertex_name, str(G2.vp[vertex_name][v]),
                                          '{}-{}-{}'.format(v_id, vertex_name, id_count)])
                                id_count += 1

            kw.close()

            if self.verbose:
                print('Writing the summary file.', file=self.error_file, flush=True)
            with open(self.log_file, 'w') as writer:
                writer.write('graph loaded! It has %d nodes and %d edges\n' % (G2.num_vertices(), G2.num_edges()))
                if self.log_top_relations:
                    writer.write('\n*** Top relations:\n')
                    for rel, freq in gtanalysis.get_topN_relations(G2, pred_property=predicate):
                        writer.write('%s\t%d\n' % (rel, freq))

                if self.log_degrees_histogram:
                    writer.write('\n*** Degrees:\n')
                    for direction in directions:
                        degree_data = gtanalysis.compute_node_degree_hist(G2, direction)
                        max_degree = len(degree_data) - 1
                        mean_degree, std_degree = gtanalysis.compute_avg_node_degree(G2, direction)
                        writer.write(
                            '%s degree stats: mean=%f, std=%f, max=%d\n' % (
                                direction, mean_degree, std_degree, max_degree))

                if self.log_top_pageranks and self.compute_pagerank:
                    writer.write('\n*** PageRank\n')
                    writer.write('Max pageranks\n')
                    result = gtanalysis.get_topn_indices(G2, self.vertex_pagerank, self.top_n, id_col)
                    for n_id, n_label, pr in result:
                        writer.write('%s\t%s\t%f\n' % (n_id, n_label, pr))

                if self.log_top_hits and self.compute_hits and not self.undirected:
                    writer.write('\n*** HITS\n')
                    writer.write('HITS hubs\n')
                    main_hubs = gtanalysis.get_topn_indices(G2, self.vertex_hubs, self.top_n, id_col)
                    for n_id, n_label, hubness in main_hubs:
                        writer.write('%s\t%s\t%f\n' % (n_id, n_label, hubness))
                    writer.write('HITS auth\n')
                    main_auth = gtanalysis.get_topn_indices(G2, self.vertex_auth, self.top_n, id_col)
                    for n_id, n_label, authority in main_auth:
                        writer.write('%s\t%s\t%f\n' % (n_id, n_label, authority))

        except Exception as e:
            raise KGTKException('Error: ' + str(e))
