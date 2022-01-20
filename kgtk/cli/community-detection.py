"""Copy records from the first KGTK file to the output file,
adding ID values.
TODO: Need KgtkWriterOptions
"""
from argparse import Namespace, SUPPRESS

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles


def parser():
    return {
        'help': 'Creating community detection from graph-tool using KGTK file',
        'description': 'Creating community detection from graph-tool ' +
        'using KGTK file, available options are blockmodel, nested and mcmc'
    }


def add_arguments_extended(parser: KGTKArgumentParser,
                           parsed_shared_args: Namespace):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """
    # import modules locally
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
    from kgtk.reshape.kgtkidbuilder import KgtkIdBuilder, KgtkIdBuilderOptions
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    _expert: bool = parsed_shared_args._expert

    # This helper function makes it easy to suppress options from
    # The help message.  The options are still there, and initialize
    # what they need to initialize.
    def h(msg: str) -> str:
        if _expert:
            return msg
        else:
            return SUPPRESS

    parser.add_input_file(positional=True)
    parser.add_output_file()

    parser.add_argument('--method', dest='method', type=str,
                        default="blockmodel",
                        help="Specify the clustering method to use.")

    KgtkIdBuilderOptions.add_arguments(parser,
                                       expert=True)  # Show all the options.
    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, expert=_expert)
    KgtkValueOptions.add_arguments(parser, expert=_expert)


def run(input_file: KGTKFiles,
        output_file: KGTKFiles,
        errors_to_stdout: bool = False,
        errors_to_stderr: bool = True,
        show_options: bool = False,
        verbose: bool = False,
        very_verbose: bool = False,
        method: str = "blockmodel",

        **kwargs  # Whatever KgtkFileOptions and KgtkValueOptions want.
        ) -> int:
    # import modules locally
    from pathlib import Path
    import sys
    import typing

    from graph_tool import Graph
    from graph_tool.inference.minimize import minimize_blockmodel_dl, \
        minimize_nested_blockmodel_dl
    import graph_tool

    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
    from kgtk.io.kgtkwriter import KgtkWriter
    from kgtk.reshape.kgtkidbuilder import KgtkIdBuilder, KgtkIdBuilderOptions
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    input_kgtk_file: Path = KGTKArgumentParser.get_input_file(input_file)
    output_kgtk_file: Path = KGTKArgumentParser.get_output_file(output_file)

    # Select where to send error messages, defaulting to stderr.
    error_file: typing.TextIO = sys.stdout if errors_to_stdout else sys.stderr

    # Build the option structures.
    idbuilder_options: KgtkIdBuilderOptions =\
    KgtkIdBuilderOptions.from_dict(kwargs)
    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs)
    value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)

    # Show the final option structures for debugging and documentation.
    try:

        # First create the KgtkReader.  It provides parameters used by the ID
        # column builder. Next, create the ID column builder, which provides a
        # possibly revised list of column names for the KgtkWriter.  Create
        # the KgtkWriter.  Last, process the data stream.

        # Open the input file.
        kr: KgtkReader = KgtkReader.open(input_kgtk_file,
                                          error_file=error_file,
                                          options=reader_options,
                                          value_options=value_options,
                                          verbose=verbose,
                                          very_verbose=very_verbose,
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

        if method == 'blockmodel':
            state = minimize_blockmodel_dl(g)
            arr = []

            for i in range(0, len(nodes)):
                arr.append('cluster_' + str(state.get_blocks()[i]))

            kw: KgtkWriter = KgtkWriter.open(["node1", "label", "node2"],
                                                 output_kgtk_file,
                                                 verbose=verbose,
                                                 very_verbose=very_verbose,
                                     )

            for i in range(0, len(nodes)):
                kw.write([nodes[i], 'in', arr[i]])

        elif method == 'nested':
            state = minimize_nested_blockmodel_dl(g)

            arr = []

            for i in range(0, len(nodes)):
                arr.append([str(i)])

            for i in range(0, len(state.levels)):
                if state.levels[i].get_B() == 1:
                    break
                for j in range(0, len(arr)):
                    arr[j].insert(0, str(state.levels[i].get_blocks()
                                         [arr[j][len(arr[j])-1]]))
            for i in range(0, len(nodes)):
                if len(arr[i]) > 0:
                    arr[i].pop()
                arr[i] = 'cluster_' + '_'.join(arr[i])

            kw: KgtkWriter = KgtkWriter.open(["node1", "label", "node2"],
                                                 output_kgtk_file,
                                                 verbose=verbose,
                                                 very_verbose=very_verbose,
                                     )
            for i in range(0, len(nodes)):
                kw.write([nodes[i], 'in', arr[i]])
        elif method == 'mcmc':
            state = minimize_blockmodel_dl(g)
            graph_tool.inference.mcmc.\
                mcmc_equilibrate(state, wait=1000, mcmc_args=dict(niter=10))

            dS, nattempts, nmoves = state.multiflip_mcmc_sweep(niter=1000)
            graph_tool.inference.mcmc.\
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

            kw: KgtkWriter =\
            KgtkWriter.open(["node1", "label", "node2", 'node2;prob'],
                                                 output_kgtk_file,
                                                 verbose=verbose,
                                                 very_verbose=very_verbose,
                                     )

            for i in range(0, len(nodes)):
                kw.write([nodes[i], 'in',
                         'cluster_' + str(m[i]), str(pv[i][m[i]]/sum(pv[i]))])

        kr.close()
        kw.close()
        return 0

    except SystemExit as e:
        raise KGTKException("Exit requested")
    except Exception as e:
        raise KGTKException(str(e))
