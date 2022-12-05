from pathlib import Path
import sys

from graph_tool.all import find_vertex  # type: ignore
from graph_tool.topology import all_paths  # type: ignore
from graph_tool.topology import all_shortest_paths  # type: ignore

from kgtk.gt.gt_load import load_graph_from_kgtk
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
from kgtk.io.kgtkwriter import KgtkWriter
from kgtk.value.kgtkvalueoptions import KgtkValueOptions
from typing import TextIO, List

from kgtk.exceptions import KGTKException


class Paths(object):
    def __init__(self,
                 input_kgtk_file: Path,
                 path_kgtk_file: Path,
                 output_kgtk_file: Path,
                 max_hops: int,
                 statistics_only: bool = False,
                 undirected: bool = False,
                 source_column_name: str = 'node1',
                 target_column_name: str = 'node2',
                 shortest_path: bool = False,
                 input_reader_options: KgtkReaderOptions = None,
                 path_reader_options: KgtkReaderOptions = None,
                 value_options: KgtkValueOptions = None,
                 error_file: TextIO = sys.stderr,
                 verbose: bool = False,
                 very_verbose: bool = False,

                 ):
        self.input_kgtk_file = input_kgtk_file
        self.path_kgtk_file = path_kgtk_file
        self.output_kgtk_file = output_kgtk_file
        self.statistics_only = statistics_only
        self.undirected = undirected
        self.max_hops = max_hops
        self.source_column_name = source_column_name
        self.target_column_name = target_column_name
        self.shortest_path = shortest_path
        self.input_reader_options = input_reader_options
        self.path_reader_options = path_reader_options
        self.value_options = value_options
        self.error_file = error_file
        self.verbose = verbose
        self.very_verbose = very_verbose

    def process(self):

        try:

            id_col = 'name'

            if self.verbose:
                print("Reading the path file: %s" % str(self.path_kgtk_file), file=self.error_file, flush=True)
            pairs = []
            pkr: KgtkReader = KgtkReader.open(self.path_kgtk_file,
                                              error_file=self.error_file,
                                              options=self.path_reader_options,
                                              value_options=self.value_options,
                                              verbose=self.verbose,
                                              very_verbose=self.very_verbose,
                                              )
            path_source_idx: int = pkr.get_node1_column_index(self.source_column_name)
            if path_source_idx < 0:
                print("Missing node1 (source) column name in the path file.", file=self.error_file, flush=True)

            path_target_idx: int = pkr.get_node2_column_index(self.target_column_name)
            if path_target_idx < 0:
                print("Missing node1 (target) column name in the path file.", file=self.error_file, flush=True)
            if path_source_idx < 0 or path_target_idx < 0:
                pkr.close()
                raise KGTKException("Exiting due to missing columns.")

            paths_read: int = 0
            path_row: List[str]
            for path_row in pkr:
                paths_read += 1
                if len(path_row) != pkr.column_count:
                    raise KGTKException(
                        "Exiting because line %d in the path file (%s) is the wrong length: "
                        "%d columns expected, %d were read." % (
                            paths_read,
                            str(self.path_kgtk_file),
                            pkr.column_count,
                            len(path_row)))
                src: str = path_row[path_source_idx]
                tgt: str = path_row[path_target_idx]
                pairs.append((src, tgt))
            pkr.close()
            if self.verbose:
                print("%d path rows read" % paths_read, file=self.error_file, flush=True)
            if len(pairs) == 0:
                print("No path pairs found, the output will be empty.", file=self.error_file, flush=True)
            elif self.verbose:
                print("%d path pairs found" % len(pairs), file=self.error_file, flush=True)

            if self.verbose:
                print("Reading the input file: %s" % str(self.input_kgtk_file), file=self.error_file, flush=True)
            kr: KgtkReader = KgtkReader.open(self.input_kgtk_file,
                                             error_file=self.error_file,
                                             options=self.input_reader_options,
                                             value_options=self.value_options,
                                             verbose=self.verbose,
                                             very_verbose=self.very_verbose,
                                             )

            sub_index: int = kr.get_node1_column_index()
            if sub_index < 0:
                print("Missing node1 (subject) column.", file=self.error_file, flush=True)
            pred_index: int = kr.get_label_column_index()
            if pred_index < 0:
                print("Missing label (predicate) column.", file=self.error_file, flush=True)
            obj_index: int = kr.get_node2_column_index()
            if obj_index < 0:
                print("Missing node2 (object) column", file=self.error_file, flush=True)
            id_index: int = kr.get_id_column_index()
            if id_index < 0:
                print("Missing id column", file=self.error_file, flush=True)
            if sub_index < 0 or pred_index < 0 or obj_index < 0 or id_index < 0:
                kr.close()
                raise KGTKException("Exiting due to missing columns.")

            predicate: str = kr.column_names[pred_index]

            G = load_graph_from_kgtk(kr,
                                     directed=not self.undirected,
                                     ecols=(sub_index, obj_index),
                                     verbose=self.verbose,
                                     out=self.error_file
                                     )

            output_columns: List[str] = ['node1', 'label', 'node2', 'id']
            kw: KgtkWriter = KgtkWriter.open(output_columns,
                                             self.output_kgtk_file,
                                             mode=KgtkWriter.Mode.EDGE,
                                             require_all_columns=True,
                                             prohibit_extra_columns=True,
                                             fill_missing_columns=False,
                                             verbose=self.verbose,
                                             very_verbose=self.very_verbose)

            id_count = 0
            if not self.statistics_only:
                for e in G.edges():
                    sid, oid = e
                    lbl = G.ep[predicate][e]
                    kw.write(
                        [G.vp[id_col][sid], lbl, G.vp[id_col][oid],
                         '{}-{}-{}'.format(G.vp[id_col][sid], lbl, id_count)])
                    id_count += 1
                if self.verbose:
                    print("%d edges found." % id_count, file=self.error_file, flush=True)

            id_count = 0
            path_id = 0
            for pair in pairs:
                source_node, target_node = pair
                source_ids = find_vertex(G, prop=G.properties[('v', id_col)], match=source_node)
                target_ids = find_vertex(G, prop=G.properties[('v', id_col)], match=target_node)
                if len(source_ids) == 1 and len(target_ids) == 1:
                    source_id = source_ids[0]
                    target_id = target_ids[0]
                    if self.shortest_path:
                        _all_paths = all_shortest_paths(G, source_id, target_id, edges=True)
                    else:
                        _all_paths = all_paths(G, source_id, target_id, cutoff=self.max_hops, edges=True)

                    for path in _all_paths:
                        for edge_num, an_edge in enumerate(path):
                            edge_id = G.properties[('e', 'id')][an_edge]
                            node1: str = 'p%d' % path_id
                            kw.write([node1, str(edge_num), edge_id, '{}-{}-{}'.format(node1, edge_num, id_count)])
                            id_count += 1
                        path_id += 1

            if self.verbose:
                print("%d paths containing %d edges found." % (path_id, id_count), file=self.error_file, flush=True)

            kw.close()
            kr.close()
        except Exception as e:
            raise KGTKException('Error: ' + str(e))
