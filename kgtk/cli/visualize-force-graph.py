"""Convert edge file and optional node file to html visualization
"""
import pandas as pd
import json
from argparse import Namespace, SUPPRESS
import sys

import math
from kgtk.visualize.visualize_api import KgtkVisualize

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles


def parser():
    return {
        'help': 'Convert edge file to html visualization',
        'description': 'Convert edge file (optional node file)' +
        'to html graph visualization file'
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

    parser.add_argument('--node-file', dest='node_file', type=str,
                        default=None,
                        help="Specify the location of node file.")

    parser.add_argument('--direction', dest='direction', type=str,
                        default=None,
                        help="Specify direction (arrow, " +
                        "particle and None), default none")

    parser.add_argument('--show-edge-label', dest='edge_label', type=bool,
                        default=False,
                        help="Specify direction (arrow, particle and None)" +
                        ", default none")

    parser.add_argument('--edge-color-column',
                        dest='edge_color_column', type=str,
                        default=None,
                        help="Specify column used for edge color")

    parser.add_argument('--edge-color-style',
                        dest='edge_color_style', type=str,
                        default=None,
                        help="Specify style (categorical, gradient)" +
                        "used for edge color")

    parser.add_argument('--edge-color-mapping',
                        dest='edge_color_mapping', type=str,
                        default=None,
                        help="Specify mapping (auto, fixed) for edge color")

    parser.add_argument('--edge-color-default',
                        dest='edge_color_default', type=str,
                        default='#000000',
                        help="Specify default color for edge")

    parser.add_argument('--edge-width-column',
                        dest='edge_width_column', type=str,
                        default=None,
                        help="Specify column used for edge width")

    parser.add_argument('--edge-width-minimum', dest='edge_width_minimum',
                        type=float, default=1.0,
                        help="Specify edge width minimum")

    parser.add_argument('--edge-width-maximum', dest='edge_width_maximum',
                        type=float, default=5.0,
                        help="Specify edge width maximum")

    parser.add_argument('--edge-width-mapping', dest='edge_width_mapping',
                        type=str, default=None,
                        help="Specify mapping (auto, fixed) for edge width")

    parser.add_argument('--edge-width-default', dest='edge_width_default',
                        type=float, default=1.0,
                        help="Specify default width for edge")

    parser.add_argument('--edge-width-scale', dest='edge_width_scale',
                        type=str, default=None,
                        help="Specify scale for width for edge (linear, log)")

    parser.add_argument('--node-color-column', dest='node_color_column',
                        type=str, default=None,
                        help="Specify column used for node color")

    parser.add_argument('--node-color-style', dest='node_color_style',
                        type=str, default=None,
                        help="Specify style (categorical, gradient)" +
                        " used for node color")

    parser.add_argument('--node-color-mapping', dest='node_color_mapping',
                        type=str, default=None,
                        help="Specify mapping (auto, fixed)" +
                        " for node color")

    parser.add_argument('--node-color-default', dest='node_color_default',
                        type=str, default='#000000',
                        help="Specify default color for node")

    parser.add_argument('--node-color-scale', dest='node_color_scale',
                        type=str, default=None,
                        help="Specify node color scale (linear/log)")

    parser.add_argument('--node-size-column', dest='node_size_column',
                        type=str, default=None,
                        help="Specify column used for node size")

    parser.add_argument('--node-size-minimum', dest='node_size_minimum',
                        type=float, default=1.0,
                        help="Specify node size minimum")

    parser.add_argument('--node-size-maximum', dest='node_size_maximum',
                        type=float, default=5.0,
                        help="Specify node size maximum")

    parser.add_argument('--node-size-mapping', dest='node_size_mapping',
                        type=str, default=None,
                        help="Specify mapping (auto, fixed) for node size")

    parser.add_argument('--node-size-default', dest='node_size_default',
                        type=float, default=2.0,
                        help="Specify default size for node")

    parser.add_argument('--node-size-scale', dest='node_size_scale', type=str,
                        default=None,
                        help="Specify scale for node size (linear, log)")

    parser.add_argument('--node-file-id', dest='node_file_id', type=str,
                        default='id',
                        help="Specify id column name in node file," +
                        " default is id")

    parser.add_argument('--show-text-limit', dest='show_text_limit', type=int,
                        default=500,
                        help="When node number is greater than this number, " +
                        "will not show text as label, default is 500")

    parser.add_argument('--node-border-color', dest='node_border_color',
                        type=str, default=None,
                        help="Specify node border color ")

    parser.add_argument('--tooltip-column', dest='tooltip_column', type=str,
                        default=None,
                        help="Specify option to show tooltip ")

    parser.add_argument('--text-node', dest='text_node', type=str,
                        default=None,
                        help="Specify option to show text" +
                        " (None, center, above), default is None")

    parser.add_argument('--node-categorical-scale',
                        dest='node_categorical_scale',
                        type=str, default='d3.schemeCategory10',
                        help="Specify color categorical scale " +
                        "for node from d3-scale-chromatic")

    parser.add_argument('--edge-categorical-scale',
                        dest='edge_categorical_scale',
                        type=str, default='d3.schemeCategory10',
                        help="Specify color categorical scale " +
                        "for edge d3-scale-chromatic")

    parser.add_argument('--node-gradient-scale', dest='node_gradient_scale',
                        type=str, default='d3.interpolateRdBu',
                        help="Specify color gradient scale" +
                        " for node from d3-scale-chromatic")

    parser.add_argument('--edge-gradient-scale', dest='edge_gradient_scale',
                        type=str, default='d3.interpolateRdBu',
                        help="Specify color gradient scale" +
                        " for edge d3-scale-chromatic")

    KgtkIdBuilderOptions.add_arguments(parser,
                                       expert=True)  # Show all the options.
    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, expert=_expert)
    KgtkValueOptions.add_arguments(parser, expert=_expert)


def run(input_file: KGTKFiles,
        output_file: KGTKFiles,
        errors_to_stdout: bool = False,
        errors_to_stderr: bool = True,
        show_options: bool = False,
        verbose: bool = False,
        very_verbose: bool = False,
        node_file: str = None,
        direction: str = None,
        edge_label: bool = False,
        edge_color_column: str = None,
        edge_color_style: str = None,
        edge_color_mapping: str = None,
        edge_color_default: str = '#000000',
        edge_width_column: str = None,
        edge_width_mapping: str = None,
        edge_width_default: float = 1.0,
        edge_width_minimum: float = 1.0,
        edge_width_maximum: float = 5.0,
        edge_width_scale: str = None,
        node_color_column: str = None,
        node_color_style: str = None,
        node_color_mapping: str = None,
        node_color_default: str = '#000000',
        node_color_scale: str = None,
        node_size_column: str = None,
        node_size_mapping: str = None,
        node_size_default: float = 2.0,
        node_size_minimum: float = 1.0,
        node_size_maximum: float = 5.0,
        node_size_scale: str = None,
        node_file_id: str = 'id',
        show_text_limit: int = 500,
        node_border_color: str = None,
        tooltip_column: str = None,
        text_node: str = None,
        node_categorical_scale: str = 'd3.schemeCategory10',
        edge_categorical_scale: str = 'd3.schemeCategory10',
        node_gradient_scale: str = 'd3.interpolateRdBu',
        edge_gradient_scale: str = 'd3.interpolateRdBu',

        **kwargs  # Whatever KgtkFileOptions and KgtkValueOptions want.
        ) -> int:

    kv: KgtkVisualize = KgtkVisualize(
                        input_file=input_file,
                        output_file=output_file,
                        errors_to_stdout=errors_to_stdout,
                        errors_to_stderr=errors_to_stderr,
                        show_options=show_options,
                        verbose=verbose,
                        very_verbose=very_verbose,
                        node_file=node_file,
                        direction=direction,
                        edge_label=edge_label,
                        edge_color_column=edge_color_column,
                        edge_color_style=edge_color_style,
                        edge_color_mapping=edge_color_mapping,
                        edge_color_default=edge_color_default,
                        edge_width_column=edge_width_column,
                        edge_width_mapping=edge_width_mapping,
                        edge_width_default=edge_width_default,
                        edge_width_minimum=edge_width_minimum,
                        edge_width_maximum=edge_width_maximum,
                        edge_width_scale=edge_width_scale,
                        node_color_column=node_color_column,
                        node_color_style=node_color_style,
                        node_color_mapping=node_color_mapping,
                        node_color_default=node_color_default,
                        node_color_scale=node_color_scale,
                        node_size_column=node_size_column,
                        node_size_mapping=node_size_mapping,
                        node_size_default=node_size_default,
                        node_size_minimum=node_size_minimum,
                        node_size_maximum=node_size_maximum,
                        node_size_scale=node_size_scale,
                        node_file_id=node_file_id,
                        show_text_limit=show_text_limit,
                        node_border_color=node_border_color,
                        tooltip_column=tooltip_column,
                        text_node=text_node,
                        node_categorical_scale=node_categorical_scale,
                        edge_categorical_scale=edge_categorical_scale,
                        node_gradient_scale=node_gradient_scale,
                        edge_gradient_scale=edge_gradient_scale,
                        kwargs=kwargs
                )
    kv.execute()
