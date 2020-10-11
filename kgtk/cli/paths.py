"""
Compute paths between nodes in a KGTK graph.

TODO: Add --output-file
"""
from argparse import Namespace
import typing

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles

def parser():
    return {
        'help': 'Compute paths between nodes in a KGTK graph.'
    }


def add_arguments_extended(parser: KGTKArgumentParser, parsed_shared_args: Namespace):
    """
    Parse arguments
    Args:
            parser (argparse.ArgumentParser)
    """
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
    from kgtk.utils.argparsehelpers import optional_bool
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    _expert: bool = parsed_shared_args._expert


    parser.add_input_file(positional=True)
    parser.add_output_file()
    parser.add_input_file(who="KGTK file with path start and end nodes.",
                          options=["--path-file", "--path_file"], dest="path_file", metavar="PATH_FILE", optional=False)

    parser.add_argument('--statistics-only', dest='statistics_only',
                        help='If this flag is set, output only the statistics edges. Else, append the statistics to the original graph. (default=%(default)s)',
                        type=optional_bool, nargs='?', const=True, default=False, metavar="True|False")

    parser.add_argument('--undirected', dest="undirected",
                        help="Is the graph undirected or not? (default=%(default)s)",
                        type=optional_bool, nargs='?', const=True, default=False, metavar="True|False")

    parser.add_argument('--max_hops', action="store", type=int, dest="max_hops", help="Maximum number of hops allowed.")

    parser.add_argument("--path-source", action="store", type=str, dest="source_column_name",
                        help='Name of the source column in the path file. (default: node1 or its alias)')
    parser.add_argument("--path-target", action="store", type=str, dest="target_column_name",
                        help='Name of the source column in the path file. (default: node2 or its alias)')

    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, expert=_expert)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, who="input", expert=_expert, defaults=False)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, who="path", expert=_expert, defaults=False)
    KgtkValueOptions.add_arguments(parser, expert=_expert)

def run(input_file: KGTKFiles,
        path_file: KGTKFiles,
        output_file: KGTKFiles,
        statistics_only: bool,
        undirected: bool,
        max_hops: int,

        source_column_name: typing.Optional[str],
        target_column_name: typing.Optional[str],

        errors_to_stdout: bool,
        errors_to_stderr: bool,
        show_options: bool,
        verbose: bool,
        very_verbose: bool,

        **kwargs, # Whatever KgtkFileOptions and KgtkValueOptions want.
        ):

    # import modules locally
    from collections import defaultdict
    from pathlib import Path
    import sys

    from graph_tool import centrality
    from graph_tool.all import find_vertex
    from graph_tool.topology import all_paths

    from kgtk.gt.gt_load import load_graph_from_kgtk
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
    from kgtk.io.kgtkwriter import KgtkWriter
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    from kgtk.exceptions import KGTKException
    try:

        # Select where to send error messages, defaulting to stderr.
        error_file: typing.TextIO = sys.stdout if errors_to_stdout else sys.stderr

        # Build the option structures.
        input_reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs, who="input", fallback=True)
        path_reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs, who="path", fallback=True)
        value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)

        input_kgtk_file: Path = KGTKArgumentParser.get_input_file(input_file)
        path_kgtk_file: Path = KGTKArgumentParser.get_input_file(path_file)
        output_kgtk_file: Path = KGTKArgumentParser.get_output_file(output_file)

        id_col = 'name'
    
        if verbose:
            print("Reading the path file: %s" % str(path_kgtk_file), file=error_file, flush=True)
        pairs=[]
        pkr: KgtkReader = KgtkReader.open(path_kgtk_file,
                                          error_file=error_file,
                                          options=path_reader_options,
                                          value_options=value_options,
                                          verbose=verbose,
                                          very_verbose=very_verbose,
                                          )
        path_source_idx: int = pkr.get_node1_column_index(source_column_name)
        if path_source_idx < 0:
            print("Missing node1 (source) column name in the path file.", file=error_file, flush=True)

        path_target_idx: int = pkr.get_node2_column_index(target_column_name)
        if path_target_idx < 0:
            print("Missing node1 (target) column name in the path file.", file=error_file, flush=True)
        if path_source_idx < 0 or path_target_idx < 0:
            pkr.close()
            raise KGTKException("Exiting due to missing columns.")

        path_row: typing.List[str]
        for path_row in pkr:
            src: str = path_row[path_source_idx]
            tgt: str = path_row[path_target_idx]
            pairs.append((src, tgt))
        pkr.close()
        if len(pairs) == 0:
            print("No path pairs found, the output will be empty.", file=error_file, flush=True)
        elif verbose:
            print("%d path pairs found" % len(pairs),  file=error_file, flush=True)

        if verbose:
            print("Reading the input file: %s" % str(input_kgtk_file), file=error_file, flush=True)
        kr: KgtkReader = KgtkReader.open(input_kgtk_file,
                                         error_file=error_file,
                                         options=input_reader_options,
                                         value_options=value_options,
                                         verbose=verbose,
                                         very_verbose=very_verbose,
                                         )

        sub_index: int = kr.get_node1_column_index()
        if sub_index < 0:
            print("Missing node1 (subject) column.", file=error_file, flush=True)
        pred_index: int = kr.get_label_column_index()
        if pred_index < 0:
            print("Missing label (predicate) column.", file=error_file, flush=True)
        obj_index: int = kr.get_node2_column_index()
        if obj_index < 0:
            print("Missing node2 (object) column", file=error_file, flush=True)
        id_index: int = kr.get_id_column_index()
        if id_index < 0:
            print("Missing id column", file=error_file, flush=True)
        if sub_index < 0 or pred_index < 0 or obj_index < 0 or id_index < 0:
            kr.close()
            raise KGTKException("Exiting due to missing columns.")

        predicate: str = kr.column_names[pred_index]
        id_col_name: str = kr.column_names[id_index]

        G = load_graph_from_kgtk(kr, directed=not undirected, ecols=(sub_index, obj_index), verbose=verbose, out=error_file)

        output_columns: typing.List[str] = ['node1', 'label', 'node2', 'id']
        kw: KgtkWriter = KgtkWriter.open(output_columns,
                                         output_kgtk_file,
                                         mode=KgtkWriter.Mode.EDGE,
                                         require_all_columns=True,
                                         prohibit_extra_columns=True,
                                         fill_missing_columns=False,
                                         verbose=verbose,
                                         very_verbose=very_verbose)

        id_count = 0
        if not statistics_only:
            for e in G.edges():
                sid, oid = e
                lbl = G.ep[predicate][e]
                kw.write([G.vp[id_col][sid], lbl, G.vp[id_col][oid], '{}-{}-{}'.format(G.vp[id_col][sid], lbl, id_count)])
                id_count += 1
            if verbose:
                print("%d edges found." % id_count, file=error_file, flush=True)

        id_count=0
        path_id=0
        for pair in pairs:
            source_node, target_node=pair
            source_ids=find_vertex(G, prop=G.properties[('v', id_col)], match=source_node)
            target_ids=find_vertex(G, prop=G.properties[('v', id_col)], match=target_node)
            if len(source_ids)==1 and len(target_ids)==1:
                source_id=source_ids[0]
                target_id=target_ids[0]
                for path in all_paths(G, source_id, target_id, cutoff=max_hops, edges=True):
                    for edge_num, an_edge in enumerate(path):
                        edge_id=G.properties[('e', 'id')][an_edge]
                        node1: str ='p%d' % path_id
                        kw.write([node1, str(edge_num), edge_id, '{}-{}-{}'.format(node1, edge_num, id_count)])
                        id_count+=1
                    path_id+=1

        if verbose:
            print("%d paths contining %d edges found." % (path_id, id_count), file=error_file, flush=True)

        kw.close()
        kr.close()

    except Exception as e:
        raise KGTKException('Error: ' + str(e))
