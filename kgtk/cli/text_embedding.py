import typing
from kgtk.exceptions import KGTKException

ALL_EMBEDDING_MODELS_NAMES = [
    "bert-base-nli-cls-token",
    "bert-base-nli-max-tokens",
    "bert-base-nli-mean-tokens",
    "bert-base-nli-stsb-mean-tokens",
    "bert-base-wikipedia-sections-mean-tokens",
    "bert-large-nli-cls-token",
    "bert-large-nli-max-tokens",
    "bert-large-nli-mean-tokens",
    "bert-large-nli-stsb-mean-tokens",
    "distilbert-base-nli-mean-tokens",
    "distilbert-base-nli-stsb-mean-tokens",
    "distiluse-base-multilingual-cased",
    "roberta-base-nli-mean-tokens",
    "roberta-base-nli-stsb-mean-tokens",
    "roberta-large-nli-mean-tokens",
    "roberta-large-nli-stsb-mean-tokens"
]


def load_property_labels_file(input_files: typing.List[str]):
    labels_dict = {}
    headers = None
    for each_file in input_files:
        with open(each_file, "r") as f:
            for each_line in f.readlines():
                each_line = each_line.replace("\n", "").split("\t")
                if headers is None:
                    headers = each_line
                    if len(headers) < 2:
                        raise KGTKException(
                            "No enough columns found on given input file. Only {} columns given but at least 2 needed.".format(
                                len(headers)))
                    elif "predicate" in headers and "label" in headers:
                        column_references = {"predicate": headers.index("predicate"),
                                             "label": headers.index("label")}
                    elif "label" in headers:
                        column_references = {"predicate": 0,
                                             "label": headers.index("label"),
                                             }
                    else:
                        raise KGTKException("Can't determine which column is label column for label file!")

                else:
                    node_id = each_line[column_references["predicate"]]
                    node_label = each_line[column_references["label"]]
                    if "@en" in node_label:
                        node_label = node_label.replace("'", "").split("@")[0]
                        labels_dict[node_id] = node_label
                    if node_id not in labels_dict:
                        labels_dict[node_id] = node_label
    return labels_dict


def load_black_list_files(file_path):
    import tarfile
    import zipfile
    import gzip
    import logging
    import re
    import numpy as np
    token_pattern = re.compile(r"(?u)\b\w\w+\b")
    qnodes_set = set()
    _logger = logging.getLogger(__name__)
    for each_file in file_path:
        try:
            # tar.gz file
            if each_file.endswith("tar.gz"):
                tar = tarfile.open("filename.tar.gz", "r:gz")
                for member in tar.getmembers():
                    f = tar.extractfile(member)
                    if f:
                        content = f.read()
                        input_data = np.loadtxt(content)
            # gz file
            elif each_file.endswith(".gz"):
                with gzip.open('big_file.txt.gz', 'rb') as f:
                    input_data = f.readlines()
            # zip file
            elif each_file.endswith(".zip"):
                archive = zipfile.ZipFile(each_file, 'r')
                input_data = archive.read(each_file.replace(".zip", "")).decode().split("\n")
            # other file, just read directly
            else:
                with open(each_file, "r") as f:
                    input_data = f.readlines()

            for each in input_data:
                each = each.replace("\n", "")
                for each_part in token_pattern.findall(each):
                    if each_part[0] == "Q" and each_part[1:].isnumeric():
                        qnodes_set.add(each_part)
        except Exception as e:
            _logger.error("Load black list file {} failed!".format(each_file))
            _logger.debug(e, exc_info=True)

    _logger.info("Totally {} black list nodes loadded.".format(len(qnodes_set)))
    return qnodes_set


def main(**kwargs):
    from kgtk.exceptions import KGTKException
    import logging
    import os
    from time import strftime
    do_logging = kwargs.get("_debug", False)
    if do_logging:
        logging_level_class = logging.DEBUG
        logger_path = os.path.join(os.environ.get("HOME"),
                                   "kgtk_text_embedding_log_{}.log".format(strftime("%Y-%m-%d-%H-%M")))
        logging.basicConfig(level=logging_level_class,
                            format="%(asctime)s [%(levelname)s] %(name)s %(lineno)d -- %(message)s",
                            datefmt='%m-%d %H:%M:%S',
                            filename=logger_path,
                            filemode='w')

    _logger = logging.getLogger(__name__)
    _logger.warning("Running with logging level {}".format(_logger.getEffectiveLevel()))

    try:
        import time
        import torch
        import typing
        import pandas as pd
        import string
        import math
        import re
        import argparse
        import pickle
        from collections import defaultdict
        from kgtk.gt.embedding_utils import EmbeddingVector

        # get input parameters from kwargs
        output_uri = kwargs.get("output_uri", "")
        parallel_count = kwargs.get("parallel_count", "1")
        black_list_files = kwargs.get("black_list_files", [])
        all_models_names = kwargs.get("all_models_names", ['bert-base-wikipedia-sections-mean-tokens'])
        input_format = kwargs.get("input_format", "kgtk_format")
        input_file = kwargs.get("input_file", None)
        output_format = kwargs.get("output_format", "kgtk_format")
        property_labels_files = kwargs.get("property_labels_file_uri", [])
        query_server = kwargs.get("query_server")
        save_embedding_sentence = kwargs.get("save_embedding_sentence", False)

        cache_config = {
            "use_cache": kwargs.get("use_cache", False),
            "host": kwargs.get("cache_host", "dsbox01.isi.edu"),
            "port": kwargs.get("cache_port", 6379)
        }

        sentence_properties = {
            "label_properties": kwargs.get("label_properties", ["label"]),
            "description_properties": kwargs.get("description_properties", ["description"]),
            "isa_properties": kwargs.get("isa_properties", ["P31"]),
            "has_properties": kwargs.get("has_properties", ["all"]),
            "property_values": kwargs.get("property_values", [])
        }

        output_properties = {
            "metadata_properties": kwargs.get("metadata_properties", []),
            "output_properties": kwargs.get("output_properties", "text_embedding")
        }

        if isinstance(all_models_names, str):
            all_models_names = [all_models_names]
        # if isinstance(input_uris, str):
        #     input_uris = [input_uris]
        if len(all_models_names) == 0:
            raise KGTKException("No embedding vector model name given!")
        if not input_file:
            raise KGTKException("No input file path given!")

        if output_uri == "":
            output_uri = os.getenv("HOME")
        if black_list_files:
            black_list_set = load_black_list_files(black_list_files)
        else:
            black_list_set = set()
        if property_labels_files:
            property_labels_dict = load_property_labels_file(property_labels_files)
            _logger.info("Totally {} property labels loaded.".format(len(property_labels_dict)))
        else:
            property_labels_dict = {}

        dimensional_reduction = kwargs.get("dimensional_reduction", "none")
        dimension_val = kwargs.get("dimension_val", 2)

        try:
            input_file_name = input_file.name
        except AttributeError:
            input_file_name = "input from memory"

        for each_model_name in all_models_names:
            _logger.info("Running {} model on {}".format(each_model_name, input_file_name))
            process = EmbeddingVector(each_model_name, query_server=query_server, cache_config=cache_config,
                                      parallel_count=parallel_count)
            process.read_input(input_file=input_file, skip_nodes_set=black_list_set,
                               input_format=input_format, target_properties=sentence_properties,
                               property_labels_dict=property_labels_dict)
            process.get_vectors()
            process.plot_result(output_properties=output_properties,
                                input_format=input_format, output_uri=output_uri,
                                dimensional_reduction=dimensional_reduction, dimension_val=dimension_val,
                                output_format=output_format, save_embedding_sentence=save_embedding_sentence)
            # process.evaluate_result()
            _logger.info("*" * 20 + "finished" + "*" * 20)
    except Exception as e:
        _logger.debug(e, exc_info=True)
        raise KGTKException(str(e))


def parser():
    return {
        'help': """Produce embedding vectors on given file's nodes."""
    }


def add_arguments(parser):
    from kgtk.utils.argparsehelpers import optional_bool
    import sys
    import argparse
    parser.accept_shared_argument('_debug')

    # model name
    all_models_names = ALL_EMBEDDING_MODELS_NAMES
    parser.add_argument('-m', '--model', action='store', nargs='+', dest='all_models_names',
                        default="bert-base-wikipedia-sections-mean-tokens", choices=all_models_names,
                        help="the model to used for embedding")
    # input file
    parser.add_argument('input_file', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    # parser.add_argument('-i', '--input', action='store', nargs='+', dest='input_uris',
    #                     help="input path", )
    parser.add_argument('-f', '--input-format', action='store', dest='input_format',
                        choices=("test_format", "kgtk_format"), default="kgtk_format",
                        help="the input file format, could either be `test_format` or `kgtk_format`, default is `kgtk_format`", )
    parser.add_argument('-p', '--property-labels-file', action='store', nargs='+',
                        dest='property_labels_file_uri', help="the path to the property labels file.", )

    # properties (only valid for kgtk format input/output data)
    parser.add_argument('--label-properties', action='store', nargs='+',
                        dest='label_properties', default=["label"],
                        help="""The names of the edges for label properties, Default is ["label"]. \n 
                        This argument is only valid for input in kgtk format.""")
    parser.add_argument('--description-properties', action='store', nargs='+',
                        dest='description_properties', default=["description"],
                        help="""The names of the edges for description properties, Default is ["description"].\n 
                        This argument is only valid for input in kgtk format.""")
    parser.add_argument('--isa-properties', action='store', nargs='+',
                        dest='isa_properties', default=["P31"],
                        help="""The names of the edges for `isa` properties, Default is ["P31"] (the `instance of` node in 
                        wikidata).""")
    parser.add_argument('--has-properties', action='store', nargs='+',
                        dest='has_properties', default=["all"],
                        help="""The names of the edges for `has` properties, Default is ["all"] (will automatically append all 
                        properties found for each node).""")
    parser.add_argument('--property-value', action='store', nargs='+',
                        dest='property_values', default=[],
                        help="""For those edges found in `has` properties, the nodes specified here will display with 
                        corresponding edge(property) values. instead of edge name. """)
    parser.add_argument('--output-property', action='store',
                        dest='output_properties', default="text_embedding",
                        help="""The output property name used to record the embedding. Default is `output_properties`. \n
                        This argument is only valid for output in kgtk format.""")
    # output
    parser.add_argument('--save-embedding-sentence', action='store_true', dest='save_embedding_sentence',
                        help="if set, will also save the embedding sentences to output.")
    parser.add_argument('-o', '--embedding-projector-metadata-path', action='store', dest='output_uri', default="",
                        help="output path for the metadata file, default will be current user's home directory")
    parser.add_argument('--output-format', action='store', dest='output_format',
                        default="kgtk", choices=("tsv_format", "kgtk_format"),
                        help="output format, can either be `tsv_format` or `kgtk_format`. \nIf choose `tsv_format`, the output "
                             "will be a tsv file, with each row contains only the vector representation of a node. Each "
                             "dimension is separated by a tab")
    parser.add_argument('--embedding-projector-metadata', action='store', nargs='+',
                        dest='metadata_properties', default=[],
                        help="""list of properties used to construct a metadata file for use in the Google Embedding Projector: 
                        http://projector.tensorflow.org. \n Default: the label and description of each node.""")

    # black list file
    parser.add_argument('-b', '--black-list', nargs='+', action='store', dest='black_list_files',
                        default=[],
                        help="the black list file, contains the Q nodes which should not consider as candidates.")

    # dimensional reduction relate
    parser.add_argument("--dimensional-reduction", nargs='?', action='store',
                        default="none", dest="dimensional_reduction", choices=("pca", "tsne", "none"),
                        help='whether to run dimensional reduction algorithm or not after the embedding, default is None (not '
                             'run). '
                        )
    parser.add_argument("--dimension", type=int, nargs='?', action='store',
                        default=2, dest="dimension_val",
                        help='How many dimension should remained after reductions, only valid when set to run dimensional '
                             'reduction, default value is 2 '
                        )

    parser.add_argument("--parallel", nargs='?', action='store',
                        default="1", dest="parallel_count",
                        help="How many processes to be run in same time, default is 1.")
    # cache config
    parser.add_argument("--use-cache", type=optional_bool, nargs='?', action='store',
                        default=False, dest="use_cache",
                        help="whether to use cache to get some embedding vectors quicker, default is False")
    parser.add_argument("--cache-host", nargs='?', action='store',
                        default="dsbox01.isi.edu", dest="cache_host",
                        help="cache host address, default is `dsbox01.isi.edu`"
                        )
    parser.add_argument("--cache-port", nargs='?', action='store',
                        default="6379", dest="cache_port",
                        help="cache server port, default is `6379`"
                        )
    # query server
    parser.add_argument("--query-server", nargs='?', action='store',
                        default="", dest="query_server",
                        help="sparql query endpoint used for test_format input files, default is "
                             "https://query.wikidata.org/sparql "
                        )


def run(**kwargs):
    main(**kwargs)
