from argparse import Namespace
import typing
from kgtk.cli_argparse import KGTKArgumentParser
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions, KgtkReaderMode
from kgtk.value.kgtkvalueoptions import KgtkValueOptions
import sys

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
    "roberta-large-nli-stsb-mean-tokens",
    "sentence-transformers/all-distilroberta-v1"
]


def parser():
    return {
        'help': """Produce embedding vectors on given file's nodes."""
    }


def add_arguments_extended(parser: KGTKArgumentParser, parsed_shared_args: Namespace):
    _expert: bool = parsed_shared_args._expert

    parser.accept_shared_argument('_debug')

    parser.add_input_file(positional=True)

    # model name
    all_models_names = ALL_EMBEDDING_MODELS_NAMES
    parser.add_argument('-m', '--model', action='store', nargs='+', dest='all_models_names',
                        default="bert-base-nli-cls-token", choices=all_models_names,
                        help="the model to used for embedding")

    parser.add_argument('--sentence-property', action='store',
                        dest='sentence_property', default="sentence",
                        help="""The name of the property with sentence for each Qnode. Default is 'sentence'""")

    parser.add_argument('--output-property', action='store',
                        dest='output_properties', default="text_embedding",
                        help="""The output property name used to record the embedding. Default is `output_properties`.
                        This argument is only valid for output in kgtk format.""")

    parser.add_argument('--batch-size', action='store',
                        dest='batch_size', default=100000, type=int,
                        help="""The number of sentences to be processed at a time. Default is 100000.
                        Set this value to '-1' to process the whole file as one batch""")

    parser.add_argument('-o', '--out-file', action='store', dest='output_file', default="-",
                        help="output path for the text embedding file, by default it will be printed in console")

    parser.add_argument('--output-data-format', action='store', dest='output_data_format',
                        default="kgtk", choices=("w2v", "kgtk"),
                        help="output format, can either be `w2v` or `kgtk`. \n"
                             "If choose `w2v`, the output will be a text file, with each row contains the qnode and "
                             " the vector representation, separated by a space. The first line is the number of qnodes"
                             " and dimension of vectors, separated by space")

    KgtkReader.add_debug_arguments(parser, expert=False)
    KgtkReaderOptions.add_arguments(parser,
                                    mode_options=True,
                                    default_mode=KgtkReaderMode[parsed_shared_args._mode],
                                    expert=_expert)
    KgtkValueOptions.add_arguments(parser, expert=False)


def run(**kwargs):
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
        from pathlib import Path
        from kgtk.gt.embedding_utils import EmbeddingVector

        all_models_names = kwargs.get("all_models_names", ['bert-base-wikipedia-sections-mean-tokens'])
        output_format = kwargs.get("output_data_format")

        output_file = kwargs.get("output_file")
        batch_size = kwargs.get("batch_size")
        sentence_property = kwargs.get("sentence_property")
        output_properties = kwargs.get("output_properties")

        # Select where to send error messages, defaulting to stderr.
        error_file: typing.TextIO = sys.stdout if kwargs.get("errors_to_stdout") else sys.stderr

        # Build the option structures.
        reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs)
        value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)

        verbose: bool = kwargs.get("verbose")

        input_file_path: Path = KGTKArgumentParser.get_input_file(kwargs.get("input_file"))

        if isinstance(all_models_names, str):
            all_models_names = [all_models_names]

        if len(all_models_names) == 0:
            raise KGTKException("No embedding vector model name given!")

        for each_model_name in all_models_names:
            _logger.info("Running {} model on {}".format(each_model_name, str(input_file_path)))
            process = EmbeddingVector(each_model_name,
                                      output_property_name=output_properties,
                                      sentence_property_name=sentence_property,
                                      output_format=output_format)

            process.process_sentences_kgtk(input_file_path=input_file_path,
                                           output_file_path=output_file,
                                           error_file=error_file,
                                           reader_options=reader_options,
                                           value_options=value_options,
                                           verbose=verbose,
                                           batch_size=batch_size
                                           )

            _logger.info("*" * 20 + "finished" + "*" * 20)
    except Exception as e:
        _logger.debug(e, exc_info=True)
        raise KGTKException(str(e))
