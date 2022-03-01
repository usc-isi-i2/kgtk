"""
Export a KGTK file to Graph-tool format.

Note:  the log file wasn't coverted to the new filename parsingAPI.

Note:  The input file is read twice: once for the header, and once for the
data.  Thus, stdin cannot be used as the input file.

TODO: Convert to KgtkReader and read the file only once.
"""
from argparse import Namespace
import typing
import pandas as pd

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles

def parser():
    return {
        'help': 'Export a KGTK file to Graph-tool format.'
    }


def add_arguments_extended(parser: KGTKArgumentParser, parsed_shared_args: Namespace):
    """
    Parse arguments
    Args:
            parser (argparse.ArgumentParser)
    """
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions, KgtkReaderMode
    from kgtk.utils.argparsehelpers import optional_bool
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    _expert: bool = parsed_shared_args._expert

    parser.add_input_file(positional=True, optional=False)
    parser.add_output_file(who="Graph tool file to dump the graph too - if empty, it will not be saved.", optional=True)

    parser.add_argument('--undirected', dest="undirected",
                        help="When True, the graph is undirected. (default=%(default)s)",
                        type=optional_bool, nargs='?', const=True, default=False, metavar="True|False")

    parser.add_argument('--node-file', dest='node_file', type=str,
                        default=None,
                        help="Specify the location of node file.")
    
    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser,
                                    mode_options=True,
                                    default_mode=KgtkReaderMode[parsed_shared_args._mode],
                                    expert=_expert)
    KgtkValueOptions.add_arguments(parser, expert=_expert)


def run(input_file: KGTKFiles,
        output_file: KGTKFiles,
        undirected: bool,
        node_file: None,

        errors_to_stdout: bool,
        errors_to_stderr: bool,
        show_options: bool,
        verbose: bool,
        very_verbose: bool,


        **kwargs, # Whatever KgtkFileOptions and KgtkValueOptions want.
        ):
    # import modules locally
    from pathlib import Path
    import sys

    from kgtk.exceptions import KGTKException
    import kgtk.gt.analysis_utils as gtanalysis
    from kgtk.gt.gt_load import load_graph_from_kgtk
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    try:
        # Select where to send error messages, defaulting to stderr.
        error_file: typing.TextIO = sys.stdout if errors_to_stdout else sys.stderr

        # Build the option structures.
        reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs)
        value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)

        input_kgtk_file: Path = KGTKArgumentParser.get_input_file(input_file)
        output_gt_file: typing.Optional[Path] = KGTKArgumentParser.get_optional_output_file(output_file)

        if verbose:
            print('loading the KGTK input file...\n', file=error_file, flush=True)
        kr: KgtkReader = KgtkReader.open(input_kgtk_file,
                                         error_file=error_file,
                                         options=reader_options,
                                         value_options=value_options,
                                         verbose=verbose,
                                         very_verbose=very_verbose,
                                         )
        sub: int = kr.get_node1_column_index()
        if sub < 0:
            print("Missing node1 (subject) column.", file=error_file, flush=True)
        pred: int = kr.get_label_column_index()
        if pred < 0:
            print("Missing label (predicate) column.", file=error_file, flush=True)
        obj: int = kr.get_node2_column_index()
        if obj < 0:
            print("Missing node2 (object) column", file=error_file, flush=True)
        if sub < 0 or pred < 0 or obj < 0:
            kr.close()
            raise KGTKException("Exiting due to missing columns.")

        G2 = load_graph_from_kgtk(kr, directed=not undirected, ecols=(sub, obj), verbose=verbose, out=error_file)

        if node_file is not None:
            kr_node: KgtkReader = KgtkReader.open(node_file,
                                                  error_file=error_file,
                                                  options=reader_options,
                                                  value_options=value_options,
                                                  verbose=verbose,
                                                  very_verbose=very_verbose,
                                                  )
            d = {}
            for i in range(0, len(list(G2.vp['name']))):
                d[G2.vp['name'][i]] = i

            vprop_dict = {}
            for col in kr_node.column_name_map:
                if col != 'id':
                    vprop_dict[col] = G2.new_vertex_property("string")
            for row in kr_node:
                for col in kr_node.column_name_map:
                    if col != 'id':
                        v = G2.vertex(d[row[kr_node.column_name_map['id']]])
                        vprop_dict[col][v] = row[kr_node.column_name_map[col]]
            for col in kr_node.column_name_map:
                if col != 'id':
                    G2.vertex_properties[col] = vprop_dict[col]


        if verbose:
            print('graph loaded! It has %d nodes and %d edges.' % (G2.num_vertices(), G2.num_edges()), file=error_file, flush=True)
            print('\n###Top relations:', file=error_file, flush=True)
            for rel, freq in gtanalysis.get_topN_relations(G2, pred_property=kr.column_names[pred]):
                print('%s\t%d' % (rel, freq), file=error_file, flush=True)

        if output_gt_file is not None:
            if verbose:
                print('\nNow saving the graph to %s' % str(output_gt_file), file=error_file, flush=True)
            G2.save(str(output_gt_file))
            if verbose:
                print('Done saving the graph.', file=error_file, flush=True)
    except Exception as e:
        raise KGTKException('Error: ' + str(e))
