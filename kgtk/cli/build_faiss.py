"""
Train and populate a faiss index that can compute nearest neighbors of given embeddings.
"""

from argparse import Namespace
from kgtk.cli_argparse import KGTKArgumentParser


def parser():
    return {
        'help': 'Train and populate a faiss index that can compute nearest neighbors of given embeddings.',
        'description': 'Train and populate a faiss index that can compute nearest neighbors of given embeddings.'
    }


def add_arguments_extended(parser: KGTKArgumentParser, parsed_shared_args: Namespace):
    """
    Parse arguments
    Args:
        parser (kgtk.cli_argparse.KGTKArgumentParser)
    """

    # import modules locally
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions, KgtkReaderMode
    from kgtk.utils.argparsehelpers import optional_bool    # not used yet
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    _expert: bool = parsed_shared_args._expert

    # REQUIRED #
    # Related to input file
    parser.add_argument('-i', '--input_file', '--embeddings_file', action='store', dest='embeddings_file',
                        required=True, metavar="EMBEDDINGS_FILE",
                        help='Input file containing the embeddings for which a Faiss index will be created.')

    # Related to output
    parser.add_argument('-o', '--output_file', '--index_file_out', action='store', dest='index_file_out',
                        required=True, help="Output .idx file where the index fill be saved.",
                        metavar="INDEX_FILE_OUT")

    parser.add_argument('-id2n', '--index_to_node_file_out', action='store', dest='index_to_node_file_out',
                        required=False, help="Output Kgtk-format file containing index --> node.",
                        default=None, metavar="INDEX_TO_NODE_FILE_OUT")

    # OPTIONAL #
    # Related to input file
    parser.add_argument('-ef', '--embeddings_format', action='store', type=str,
                        dest='embeddings_format', required=False,
                        help='Format of the input embeddings [Default: w2v] Choice: kgtk | w2v | glove',
                        default="w2v", choices=["kgtk", "w2v", "glove"], metavar="kgtk|w2v|glove")

    parser.add_argument('--no_input_header', action='store', type=optional_bool, dest="no_input_header",
                        required=False, help='If your input embeddings file is in KGTK format, this ' +
                        'allows you to specify if it has a header line or not.',
                        const=True, nargs='?', default=False, metavar='True|False')

    # Related to index building
    parser.add_argument('-te', '--max_train_examples', action='store', type=int,
                        dest='max_train_examples', required=False, default=10000000,
                        help="The maximum number of embeddings that will be used to train the index.")

    parser.add_argument('-w', '--workers', action='store', type=int, dest='workers', required=False,
                        help="The number of worker processes for training. If not given, set to CPU count.",
                        default=None)

    parser.add_argument('-is', '--index_string', action='store', type=str, dest='index_string', required=False,
                        help="A string denoting the type of index to be used. This will be passed to " +
                        "faiss.index_factory()",
                        default="IVF8192_HNSW32,Flat")

    parser.add_argument('-m', '--metric_type', action='store', type=str, dest='metric_type', required=False,
                        help="A string denoting the Faiss metric to be used. This will be passed to " +
                        "faiss.index_factory().", default="L2", 
                        choices=["Inner_product", "L2", "L1", "Linf", "Lp", "Canberra", "BrayCurtis", "JensenShannon"],
                        metavar="Inner_product|L2|L1|Linf|Lp|Canberra|BrayCurtis|JensenShannon")

    parser.add_argument('-ma', '--metric_arg', action='store', type=float, dest='metric_arg', required=False,
                        help="If you choose Lp as your metric_type, this parameter should be used to " +
                        "specify the value of p to use.",
                        default=None)

    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser,
                                    mode_options=True,
                                    default_mode=KgtkReaderMode[parsed_shared_args._mode],
                                    expert=_expert)
    KgtkValueOptions.add_arguments(parser)


def run(**kwargs):
    from kgtk.exceptions import KGTKException
    from kgtk.graph_embeddings.build_faiss import build_faiss
    try:
        build_faiss(kwargs['embeddings_file'],
                    kwargs['embeddings_format'],
                    kwargs['no_input_header'],
                    kwargs['index_file_out'],
                    kwargs['index_to_node_file_out'],
                    kwargs['max_train_examples'],
                    kwargs['workers'],
                    kwargs['index_string'],
                    kwargs['metric_type'],
                    kwargs['metric_arg'],
                    kwargs['verbose'])

    except SystemExit as e:
        raise KGTKException("Exit requested")
    except KGTKException as e:
        raise
    except Exception as e:
        raise KGTKException(str(e))
