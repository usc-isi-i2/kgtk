"""
Export a KGTK file to Graph-tool format.

Note:  the log file wasn't coverted to the new filename parsing.
"""
from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles

def parser():
    return {
        'help': 'Export a KGTK file to Graph-tool format.'
    }


def add_arguments(parser: KGTKArgumentParser):
    """
    Parse arguments
    Args:
            parser (argparse.ArgumentParser)
    """
    parser.add_input_file(positional=True)
    parser.add_output_file(who="Graph tool file to dump the graph too - if empty, it will not be saved.", optional=True)

    parser.add_argument('--directed', action='store_true', dest="directed", help="Is the graph directed or not?")
    parser.add_argument('--log', action='store', type=str, dest='log_file',
                        help='Log file for summarized statistics of the graph.', default="./log.txt")

def run(input_file: KGTKFiles,
        output_file: KGTKFiles,
        directed, log_file):
    from kgtk.exceptions import KGTKException
    def infer_index(h, options=[]):
        for o in options:
            if o in h:
                return h.index(o)
        return -1

    def infer_predicate(h, options=[]):
        for o in options:
            if o in h:
                return o
        return ''

    try:
        # import modules locally
        from pathlib import Path
        import socket
        import sys
        import typing
        from graph_tool import load_graph_from_csv
        from graph_tool import centrality
        import kgtk.gt.analysis_utils as gtanalysis

        filename: Path = KGTKArgumentParser.get_input_file(input_file)
        output: typing.Optional[Path] = KGTKArgumentParser.get_output_file(output_file, optional=True)

        with open(filename, 'r') as f:
            header = next(f).split('\t')
            subj_index = infer_index(header, options=['node1', 'subject'])
            obj_index = infer_index(header, options=['node2', 'object', 'value'])
            predicate = infer_predicate(header, options=['property', 'predicate', 'label'])

            p = []
            for i, header_col in enumerate(header):
                if i in [subj_index, obj_index]: continue
                p.append(header_col)

        with open(log_file, 'w') as writer:
            writer.write('loading the TSV graph now ...\n')
            G2 = load_graph_from_csv(filename,
                                     skip_first=True,
                                     directed=directed,
                                     hashed=True,
                                     ecols=[subj_index, obj_index],
                                     eprop_names=p,
                                     csv_options={'delimiter': '\t'})

            writer.write('graph loaded! It has %d nodes and %d edges\n' % (G2.num_vertices(), G2.num_edges()))
            writer.write('\n###Top relations:\n')
            for rel, freq in gtanalysis.get_topN_relations(G2, pred_property=predicate):
                writer.write('%s\t%d\n' % (rel, freq))

            

            if output:
                writer.write('now saving the graph to %s\n' % str(output))
                G2.save(str(output))
    except Exception as e:
        raise KGTKException('Error: ' + str(e))
