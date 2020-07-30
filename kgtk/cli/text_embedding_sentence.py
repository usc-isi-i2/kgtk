import typing
from kgtk.exceptions import KGTKException
from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles
from kgtk.cli.text_embedding import \
    add_arguments as add_arguments_text_embedding, \
    main as main_text_embedding
import sys


def parser():
    return {
        'help': """Produce embedding sentence "only" on given file's nodes. 
                This function has exact same args support as "text_embedding" function."""
    }


def add_arguments(parser: KGTKArgumentParser):
    # please refer to text embedding.py
    add_arguments_text_embedding(parser)


def run(**kwargs):
    kwargs["save_embedding_sentence"] = True
    kwargs["need_produce_vector"] = False
    main_text_embedding(**kwargs)
