"""Convert edge file and optional node file to html visualization
"""
import pandas as pd
import json
from argparse import Namespace, SUPPRESS
import sys

from kgtk.augment.augment_main import augment_np
from kgtk.augment.loader import get_data_np
from kgtk.augment.augment_main import augment_lp
from kgtk.augment.loader import get_data_lp

import argparse
from kgtk.augment.constant import *
import os

import math

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles


def parser():
    return {
        'help': 'Augment Graph File',
        'description': 'Augment Graph File'
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

    parser.add_input_file(positional=True)
    parser.add_output_file()

    parser.add_argument('--dataset', dest='dataset', type=str,
                        default=None,
                        help="Specify the location of dataset.")

    parser.add_argument('--train-file-name', dest='train_file_name', type=str,
                        default='train.tsv',
                        help="Specify name for training file")

    parser.add_argument('--numerical-literal-name', dest='num_literal_name', type=str,
                        default='numerical_literals.tsv',
                        help="Specify name for numerical literal file")

    parser.add_argument('--valid-file-name', dest='valid_file_name', type=str,
                        default='valid.tsv',
                        help="Specify name for valid file")

    parser.add_argument('--test-file-name', dest='test_file_name', type=str,
                        default='test.tsv',
                        help="Specify name for test file")

    parser.add_argument('--bins', dest='bins', type=int,
                        default=8,
                        help="Specify number of bins to use")

    parser.add_argument('--aug_mode', dest='aug_mode', type=str,
                        default='All',
                        help="Specify name for test file, seperated by comma, or All for using all modes")

    parser.add_argument('--prediction-type', dest='prediction_type', type=str,
                        default='lp',
                        help="Specify prediction type to use (lp, np)")

    parser.add_argument('--reverse', dest='reverse', type=bool,
                        default=False,
                        help="Specify whether to include reverse links")

    parser.add_argument('--output-path', dest='output_path', type=str,
                        default='numeric',
                        help="Specify path to store output files")

    parser.add_argument('--train-literal-name', dest='train_literal_name', type=str,
                        default='train_100.tsv',
                        help="Specify name for training file")

    parser.add_argument('--entity-triple-name', dest='entity_triple_name', type=str,
                        default='train_100.tsv',
                        help="Specify name for entity triple file")

    parser.add_argument('--valid-literal-name', dest='valid_literal_name', type=str,
                        default='dev.tsv',
                        help="Specify name for valid file")

    parser.add_argument('--test-literal-name', dest='test_literal_name', type=str,
                        default='test.tsv',
                        help="Specify name for test file")

    KgtkIdBuilderOptions.add_arguments(parser,
                                       expert=True)  # Show all the options.
    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, expert=_expert)
    KgtkValueOptions.add_arguments(parser, expert=_expert)


def run(input_file: KGTKFiles,
        output_file: KGTKFiles,
        dataset: str = None,
        train_file_name: str = 'train.tsv',
        num_literal_name: str = 'numerical_literals.tsv',
        valid_file_name: str = 'valid.tsv',
        test_file_name: str = 'test.tsv',
        bins: int = 8,
        aug_mode: str = 'All',
        prediction_type: str = 'lp',
        reverse: bool = False,
        output_path: str = 'output',
        entity_triple_name: str = 'train_kge.tsv',
        train_literal_name: str = 'train_100.tsv',
        valid_literal_name: str = 'dev.tsv',
        test_literal_name: str = 'test.tsv',

        **kwargs  # Whatever KgtkFileOptions and KgtkValueOptions want.
        ) -> int:
    modes = aug_mode.split(',')

    if modes[0] == "All":
        modes = SUPPORTED_MODE

    if prediction_type == 'lp':
       entities, values = get_data_lp(dataset, train_file_name, num_literal_name)

       for mode in modes:
           if mode in SUPPORTED_MODE:
               augment_lp(entities, values, dataset, train_file_name,
                          valid_file_name, test_file_name, mode, output_path, bins, reverse)

    elif prediction_type == 'np':
        entities, train, valid, test = get_data_np(dataset, entity_triple_name, train_literal_name,
                                                   valid_literal_name, test_literal_name)
        for mode in modes:
            if mode in SUPPORTED_MODE:
                augment_np(entities, train, valid, test, entity_triple_name, train_literal_name,
                           valid_literal_name, test_literal_name,
                           dataset, mode, output_path, bins, reverse)



