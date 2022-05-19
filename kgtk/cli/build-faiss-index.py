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
    parser.add_input_file(who="Input file containing the embeddings for which a Faiss index will be created.",
                          options=["-i", "--input-file", "--embeddings-file"],
                          metavar="EMBEDDINGS_FILE", dest='embeddings_file')
    # parser.add_argument('-i', '--input_file', '--embeddings_file', action='store', dest='embeddings_file',
    #                     required=True, metavar="EMBEDDINGS_FILE",
    #                     help='Input file containing the embeddings for which a Faiss index will be created.')

    # Related to output
    parser.add_output_file(who="Output .idx file where the index fill be saved.",
                           options=['-o', '--output-file', '--index-file-out'],
                           metavar="INDEX_FILE_OUT", dest='index_file_out')
    # parser.add_argument('-o', '--output_file', '--index_file_out', action='store', dest='index_file_out',
    #                     required=True, help="Output .idx file where the index fill be saved.",
    #                     metavar="INDEX_FILE_OUT")

    parser.add_argument('-id2n', '--faiss-id-to-node-mapping-file', action='store', dest='index_to_node_file_out',
                        required=False, help="Output Kgtk-format file containing index --> node.",
                        default=None, metavar="FAISS_ID_TO_NODE_MAPPING_FILE")

    # OPTIONAL #
    # Related to input file
    parser.add_argument('-ef', '--embeddings-format', action='store', type=str,
                        dest='embeddings_format', required=False,
                        help='Format of the input embeddings [Default: w2v] Choice: kgtk | w2v | glove',
                        default="w2v", choices=["kgtk", "w2v", "glove"], metavar="kgtk|w2v|glove")

    parser.add_argument('--no-kgtk-input-header', action='store', type=optional_bool, dest="no_input_header",
                        required=False, help='If your input embeddings file is in KGTK format, this ' +
                        'allows you to specify if it has a header line or not.',
                        const=True, nargs='?', default=False, metavar='True|False')

    # Related to index building
    parser.add_argument('-te', '--max-train-examples', action='store', type=int,
                        dest='max_train_examples', required=False, default=10000000,
                        help="The maximum number of embeddings that will be used to train the index.")

    parser.add_argument('-w', '--workers', action='store', type=int, dest='workers', required=False,
                        help="The number of worker processes for training. If not given, set to CPU count.",
                        default=None)

    parser.add_argument('-is', '--index-string', action='store', type=str, dest='index_string', required=False,
                        help="A string denoting the type of index to be used. This will be passed to " +
                        "faiss.index_factory()",
                        default="IVF8192_HNSW32,Flat")

    parser.add_argument('-m', '--metric-type', action='store', type=str, dest='metric_type', required=False,
                        help="A string denoting the Faiss metric to be used. This will be passed to " +
                        "faiss.index_factory(). 'Cosine' may also be specified, in which case " +
                        "we will use inner product and L2-normalize your vectors before training " +
                        "and adding them to the index. When searching in the resulting index, you " +
                        "will need to L2-normalize vectors before searching with them by calling " +
                        "faiss.normalize_L2(vecs).", default="L2",
                        choices=["Inner_product", "L2", "L1", "Linf", "Lp", "Canberra", "BrayCurtis",
                                 "JensenShannon", "Cosine"],
                        metavar="Inner_product|L2|L1|Linf|Lp|Canberra|BrayCurtis|JensenShannon|Cosine")

    parser.add_argument('-ma', '--metric-arg', action='store', type=float, dest='metric_arg', required=False,
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
    from kgtk.graph_embeddings.build_faiss_index import build_faiss_index
    from kgtk.io.kgtkreader import KgtkReaderOptions
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    # error_file: typing.TextIO = sys.stdout if args.errors_to_stdout else sys.stderr

    # Build the option structures for kgtk reader
    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs)
    value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)
    try:
        build_faiss_index(kwargs['embeddings_file'],
                          kwargs['embeddings_format'],
                          kwargs['no_input_header'],
                          kwargs['index_file_out'],
                          kwargs['index_to_node_file_out'],
                          kwargs['max_train_examples'],
                          kwargs['workers'],
                          kwargs['index_string'],
                          kwargs['metric_type'],
                          kwargs['metric_arg'],
                          kwargs['verbose'],
                          reader_options,
                          value_options)

    except SystemExit as e:
        raise KGTKException("Exit requested")
    except KGTKException as e:
        raise e
    except Exception as e:
        raise KGTKException(str(e))
