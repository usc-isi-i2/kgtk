"""
Train and populate a faiss index that can compute nearest neighbors of given embeddings.
"""

# from argparse import Namespace, SUPPRESS
# import typing

# from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles
from kgtk.cli_argparse import KGTKArgumentParser


def parser():
    return {
        'help': 'Train and populate a faiss index that can compute nearest neighbors of given embeddings.',
        'description': 'Train and populate a faiss index that can compute nearest neighbors of given embeddings.'
    }

def add_arguments(parser: KGTKArgumentParser):
    """
    Parse arguments
    Args:
        parser (kgtk.cli_argparse.KGTKArgumentParser)
    """
    
    # REQUIRED #
    # Related to input file
    parser.add_argument('--embeddings_file', action='store', dest='embeddings_file', required=True,
                        help='Input file containing the embeddings for which a Faiss index will be created.')
    
    # Related to output
    parser.add_argument('--index_file_out', action='store', dest='index_file_out', required=True,
                        help="Output .idx file where the index fill be saved.")

    parser.add_argument('--index_to_qnode_file_out', action='store', dest='index_to_qnode_file_out', required=True,
                        help="Output Kgtk-format file containing index --> qnode.")
    
    # OPTIONAL #
    # Related to input file
    parser.add_argument('--embeddings_format', action='store', type=str, dest='embeddings_format', required=False,
                        help='Format of the input embeddings [Default: w2v] Choice: kgtk | w2v | glove',
                        default="w2v", metavar="kgtk|w2v|glove")

    # Related to index building
    parser.add_argument('--max_train_examples', action='store', type=int, dest='max_train_examples', required=False,
                        help="The maximum number of embeddings that will be used to train the index.",
                        default=10000000)

    parser.add_argument('--workers', action='store', type=int, dest='workers', required=False,
                        help="The number of worker processes for training. If not given, set to CPU count.",
                        default=None, metavar='')

    parser.add_argument('--index_string', action='store', type=str, dest='index_string', required=False,
                        help="A string denoting the type of index to be used. This will be passed to" +
                        "faiss.index_factory()",
                        default="IVF8192_HNSW32,Flat")

    parser.add_argument('--metric_type', action='store', type=str, dest='metric_type', required=False,
                        help="A string denoting the Faiss metric to be used. This will be passed to" +
                        "faiss.index_factory(). Currently, the only option is metric_l2.",
                        default="metric_l2", metavar="metric_l2")

    parser.add_argument('--metric_arg', action='store', type=float, dest='metric_arg', required=False,
                        help="If you choose Lp as your metric_type, this parameter should be used to " +
                        "specify the value of p to use.",
                        default=None)

    

    # Misc
#     parser.accept_shared_argument('_verbose') Not sure how to get this to work
#     parser.accept_shared_argument('_debug') Doesn't seem like I need this?

def run(**kwargs):
    import traceback
    from kgtk.exceptions import KGTKException
    from kgtk.graph_embeddings.build_faiss import build_faiss
    try:
        build_faiss(kwargs['embeddings_file'],
                    kwargs['embeddings_format'],
                    kwargs['index_file_out'],
                    kwargs['index_to_qnode_file_out'],
                    kwargs['max_train_examples'],
                    kwargs['workers'],
                    kwargs['index_string'],
                    kwargs['metric_type'],
                    kwargs['metric_arg'])
        
    except:
        message = 'Command: build_faiss_for_embeddings\n'
        message += 'Error Message:  {}\n'.format(traceback.format_exc())
        raise KGTKException(message)




