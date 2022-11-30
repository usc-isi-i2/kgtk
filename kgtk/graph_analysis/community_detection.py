from pathlib import Path
import sys
from graph_tool import Graph
from graph_tool.inference.minimize import minimize_blockmodel_dl, minimize_nested_blockmodel_dl  # type: ignore
import graph_tool
from kgtk.exceptions import KGTKException
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
from kgtk.io.kgtkwriter import KgtkWriter
from kgtk.value.kgtkvalueoptions import KgtkValueOptions
from typing import TextIO


class CommunityDetection(object):
    def __init__(self,
                 input_kgtk_file: Path,
                 output_kgtk_file: Path,
                 method: str = "blockmodel",
                 error_file: TextIO = sys.stderr,
                 reader_options: KgtkReaderOptions = None,
                 value_options: KgtkValueOptions = None,
                 verbose: bool = False,
                 very_verbose: bool = False
                 ):
        self.input_kgtk_file = input_kgtk_file
        self.output_kgtk_file = output_kgtk_file
        self.method = method
        self.error_file = error_file
        self.reader_options = reader_options
        self.value_options = value_options
        self.verbose = verbose
        self.very_verbose = very_verbose

    def process(self):
        try:

            # First create the KgtkReader.  It provides parameters used by the ID
            # column builder. Next, create the ID column builder, which provides a
            # possibly revised list of column names for the KgtkWriter.  Create
            # the KgtkWriter.  Last, process the data stream.

            # Open the input file.
            kr: KgtkReader = KgtkReader.open(self.input_kgtk_file,
                                             error_file=self.error_file,
                                             options=self.reader_options,
                                             value_options=self.value_options,
                                             verbose=self.verbose,
                                             very_verbose=self.very_verbose,
                                             )

            g = Graph(directed=False)

            d = {}
            count = 0
            nodes = []
            edges = []
            for row in kr:
                if row[kr.node1_column_idx] not in d:
                    d[row[kr.node1_column_idx]] = count
                    count = count + 1
                    nodes.append(row[kr.node1_column_idx])
                if row[kr.node2_column_idx] not in d:
                    d[row[kr.node2_column_idx]] = count
                    count = count + 1
                    nodes.append(row[kr.node2_column_idx])
                edges.append((row[kr.node1_column_idx], row[kr.node2_column_idx]))

            vlist = g.add_vertex(len(d))

            for ele in edges:
                g.add_edge(g.vertex(d[ele[0]]), g.vertex(d[ele[1]]))

            if self.method == 'blockmodel':
                state = minimize_blockmodel_dl(g)
                arr = []

                for i in range(0, len(nodes)):
                    arr.append('cluster_' + str(state.get_blocks()[i]))

                kw: KgtkWriter = KgtkWriter.open(["node1", "label", "node2"],
                                                 self.output_kgtk_file,
                                                 verbose=self.verbose,
                                                 very_verbose=self.very_verbose,
                                                 )

                for i in range(0, len(nodes)):
                    kw.write([nodes[i], 'in', arr[i]])

                kw.close()

            elif self.method == 'nested':
                state = minimize_nested_blockmodel_dl(g)

                arr = []

                for i in range(0, len(nodes)):
                    arr.append([str(i)])

                for i in range(0, len(state.levels)):
                    if state.levels[i].get_B() == 1:
                        break
                    for j in range(0, len(arr)):
                        arr[j].insert(0, str(state.levels[i].get_blocks()
                                             [arr[j][len(arr[j]) - 1]]))
                for i in range(0, len(nodes)):
                    if len(arr[i]) > 0:
                        arr[i].pop()
                    arr[i] = 'cluster_' + '_'.join(arr[i])

                kw: KgtkWriter = KgtkWriter.open(["node1", "label", "node2"],
                                                 self.output_kgtk_file,
                                                 verbose=self.verbose,
                                                 very_verbose=self.very_verbose,
                                                 )
                for i in range(0, len(nodes)):
                    kw.write([nodes[i], 'in', arr[i]])

                kw.close()
            elif self.method == 'mcmc':
                state = minimize_blockmodel_dl(g)
                graph_tool.inference.mcmc. \
                    mcmc_equilibrate(state, wait=1000, mcmc_args=dict(niter=10))

                dS, nattempts, nmoves = state.multiflip_mcmc_sweep(niter=1000)
                graph_tool.inference.mcmc. \
                    mcmc_equilibrate(state, wait=10,
                                     nbreaks=2, mcmc_args=dict(niter=10))

                bs = []  # collect some partitions

                def collect_partitions(s):
                    bs.append(s.b.a.copy())

                # Now we collect partitions for exactly 100,000 sweeps
                # of 10 sweeps:
                graph_tool.inference.mcmc.mcmc_equilibrate(
                    state,
                    force_niter=10000,
                    mcmc_args=dict(niter=10),
                    callback=collect_partitions)

                # Disambiguate partitions and obtain marginals
                pmode = graph_tool.inference.partition_modes.PartitionModeState(bs, converge=True)
                pv = list(pmode.get_marginal(g))
                m = list(pmode.get_max(g))

                kw: KgtkWriter = \
                    KgtkWriter.open(["node1", "label", "node2", 'node2;prob'],
                                    self.output_kgtk_file,
                                    verbose=self.verbose,
                                    very_verbose=self.very_verbose,
                                    )

                for i in range(0, len(nodes)):
                    kw.write([nodes[i], 'in',
                              'cluster_' + str(m[i]), str(pv[i][m[i]] / sum(pv[i]))])
                kw.close()

            kr.close()
        except SystemExit as e:
            raise KGTKException("Exit requested")
        except Exception as e:
            raise KGTKException(str(e))
