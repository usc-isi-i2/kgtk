"""Convert edge file to html visualization
"""
import json
from argparse import Namespace, SUPPRESS

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles

from pathlib import Path
import importlib

vfg = importlib.import_module('kgtk.cli.visualize-force-graph', None)


def parser():
    return {
        'help': 'Visualize API',
        'description': 'Use API to convert edge file to html visualization'
    }


class KGTKvisualize:
    def __init__(
                self,
                input_file: str = None,
                output_file: str = None,
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
                edge_color_default: str = None,
                edge_width_column: str = None,
                edge_width_mapping: str = None,
                edge_width_default: float = 1.0,
                edge_width_minimum: float = 1.0,
                edge_width_maximum: float = 5.0,
                edge_width_scale: str = None,
                node_color_column: str = None,
                node_color_style: str = None,
                node_color_mapping: str = None,
                node_color_default: str = None,
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
                edge_gradient_scale: str = 'd3.interpolateRdBu'):
        self.input_file = Path(input_file)
        self.output_file = Path(output_file)
        self.errors_to_stdout = errors_to_stdout
        self.errors_to_stderr = errors_to_stderr
        self.show_options = show_options
        self.verbose = verbose
        self.very_verbose = very_verbose
        self.node_file = node_file
        self.direction = direction
        self.edge_label = edge_label
        self.edge_color_column = edge_color_column
        self.edge_color_style = edge_color_style
        self.edge_color_mapping = edge_color_mapping
        self.edge_color_default = edge_color_default
        self.edge_width_column = edge_width_column
        self.edge_width_mapping = edge_width_mapping
        self.edge_width_default = edge_width_default
        self.edge_width_minimum = edge_width_minimum
        self.edge_width_maximum = edge_width_maximum
        self.edge_width_scale = edge_width_scale
        self.node_color_column = node_color_column
        self.node_color_style = node_color_style
        self.node_color_mapping = node_color_mapping
        self.node_color_default = node_color_default
        self.node_color_scale = node_color_scale
        self.node_size_column = node_size_column
        self.node_size_mapping = node_size_mapping
        self.node_size_default = node_size_default
        self.node_size_minimum = node_size_minimum
        self.node_size_maximum = node_size_maximum
        self.node_size_scale = node_size_scale
        self.node_file_id = node_file_id
        self.show_text_limit = show_text_limit
        self.node_border_color = node_border_color
        self.tooltip_column = tooltip_column
        self.text_node = text_node
        self.node_categorical_scale = node_categorical_scale
        self.edge_categorical_scale = edge_categorical_scale
        self.node_gradient_scale = node_gradient_scale
        self.edge_gradient_scale = edge_gradient_scale

    def execute(self):
        vfg.run(
            input_file=self.input_file,
            output_file=self.output_file,
            errors_to_stdout=self.errors_to_stdout,
            errors_to_stderr=self.errors_to_stderr,
            show_options=self.show_options,
            verbose=self.verbose,
            very_verbose=self.very_verbose,
            node_file=self.node_file,
            direction=self.direction,
            edge_label=self.edge_label,
            edge_color_column=self.edge_color_column,
            edge_color_style=self.edge_color_style,
            edge_color_mapping=self.edge_color_mapping,
            edge_color_default=self.edge_color_default,
            edge_width_column=self.edge_width_column,
            edge_width_mapping=self.edge_width_mapping,
            edge_width_default=self.edge_width_default,
            edge_width_minimum=self.edge_width_minimum,
            edge_width_maximum=self.edge_width_maximum,
            edge_width_scale=self.edge_width_scale,
            node_color_column=self.node_color_column,
            node_color_style=self.node_color_style,
            node_color_mapping=self.node_color_mapping,
            node_color_default=self.node_color_default,
            node_color_scale=self.node_color_scale,
            node_size_column=self.node_size_column,
            node_size_mapping=self.node_size_mapping,
            node_size_default=self.node_size_default,
            node_size_minimum=self.node_size_minimum,
            node_size_maximum=self.node_size_maximum,
            node_size_scale=self.node_size_scale,
            node_file_id=self.node_file_id,
            show_text_limit=self.show_text_limit,
            node_border_color=self.node_border_color,
            tooltip_column=self.tooltip_column,
            text_node=self.text_node,
            node_categorical_scale=self.node_categorical_scale,
            edge_categorical_scale=self.edge_categorical_scale,
            node_gradient_scale=self.node_gradient_scale,
            edge_gradient_scale=self.edge_gradient_scale
            )
