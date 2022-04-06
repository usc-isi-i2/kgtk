"""Convert edge file and optional node file to html visualization
"""
from argparse import Namespace
from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
from kgtk.value.kgtkvalueoptions import KgtkValueOptions


def parser():
    return {
        'help': 'Convert edge file to html visualization',
        'description': 'Convert edge file (optional node file)' +
                       ' to html graph visualization file'
    }


def add_arguments_extended(parser: KGTKArgumentParser, parsed_shared_args: Namespace):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """

    _expert: bool = parsed_shared_args._expert

    # This helper function makes it easy to suppress options from
    # The help message.  The options are still there, and initialize
    # what they need to initialize.

    parser.add_input_file(positional=True)
    parser.add_output_file()

    parser.add_argument('--node-file',
                        dest='node_file',
                        type=str,
                        default=None,
                        help="Path of the node file.")

    parser.add_argument('--direction',
                        dest='direction',
                        type=str,
                        default=None,
                        help="The edge direction: arrow|particle|None. Default: None")

    parser.add_argument('--show-edge-label',
                        dest='edge_label',
                        action='store_true',
                        default=False,
                        help="Add this option to show labels on edges. Default: False")

    parser.add_argument('--edge-color-column',
                        dest='edge_color_column',
                        type=str,
                        default=None,
                        help="Column for edge colors in the edge file. "
                             "The values can be numbers, hex codes or any strings")

    parser.add_argument('--edge-color-numbers',
                        dest='edge_color_numbers',
                        action='store_true',
                        default=False,
                        help="Add this option if the values in the --edge-color-column are numbers")

    parser.add_argument('--edge-color-hex',
                        dest='edge_color_hex',
                        action='store_true',
                        default=False,
                        help="Add this option if the values in the --edge-color-column are valid hexadecimal colors."
                             "Valid hexadecimal colors start with # and are of 3 or 6 length (without the #) ")

    parser.add_argument('--edge-color-style',
                        dest='edge_color_style',
                        type=str,
                        default=None,
                        help="Edge color style for edge color: categorical|gradient. Default: None")

    parser.add_argument('--edge-color-default',
                        dest='edge_color_default',
                        type=str,
                        default='#000000',
                        help="Default color for edges. Default: '#000000'")

    parser.add_argument('--edge-width-column',
                        dest='edge_width_column',
                        type=str,
                        default=None,
                        help="Column for edge widths in the edge file. The values should be numbers.")

    parser.add_argument('--edge-width-minimum',
                        dest='edge_width_minimum',
                        type=float,
                        default=1.0,
                        help="Minimum edge width. Default: 1.0")

    parser.add_argument('--edge-width-maximum',
                        dest='edge_width_maximum',
                        type=float,
                        default=5.0,
                        help="Maximum edge width. Default: 5.0")

    parser.add_argument('--edge-width-default',
                        dest='edge_width_default',
                        type=float,
                        default=1.0,
                        help="Default edge width. Default: 1.0")

    parser.add_argument('--edge-width-scale',
                        dest='edge_width_scale',
                        type=str,
                        default=None,
                        help="Edge width scale: linear|log. Default: None")

    parser.add_argument('--node-color-column',
                        dest='node_color_column',
                        type=str,
                        default=None,
                        help="Column for node colors in the --node-file. The values can be numbers, valid hex codes"
                             " or any strings.")

    parser.add_argument('--node-color-style',
                        dest='node_color_style',
                        type=str,
                        default=None,
                        help="Node color style: categorical|gradient. Default: None")

    parser.add_argument('--node-color-default',
                        dest='node_color_default',
                        type=str,
                        default='#000000',
                        help="Default node color. Default: '#000000'")

    parser.add_argument('--node-color-scale',
                        dest='node_color_scale',
                        type=str,
                        default=None,
                        help="Node color scale: linear|log. Default: None")

    parser.add_argument('--node-color-numbers',
                        dest='node_color_numbers',
                        action='store_true',
                        default=False,
                        help="Add this option if the values in the --node-color-column are numbers")

    parser.add_argument('--node-color-hex',
                        dest='node_color_hex',
                        action='store_true',
                        default=False,
                        help="Add this option if the values in the --node-color-column are valid hexadecimal colors."
                             "Valid hexadecimal colors start with # and are of 3 or 6 length (without the #) ")

    parser.add_argument('--node-size-column',
                        dest='node_size_column',
                        type=str,
                        default=None,
                        help="Column for node sizes in the --node-file. Default: None")

    parser.add_argument('--node-size-minimum',
                        dest='node_size_minimum',
                        type=float,
                        default=1.0,
                        help="Minimum node size. Default: 1.0")

    parser.add_argument('--node-size-maximum',
                        dest='node_size_maximum',
                        type=float,
                        default=5.0,
                        help="Maximum node size. Default: 5.0")

    parser.add_argument('--node-size-default',
                        dest='node_size_default',
                        type=float,
                        default=2.0,
                        help="Default node size. Default: 2.0")

    parser.add_argument('--node-size-scale',
                        dest='node_size_scale',
                        type=str,
                        default=None,
                        help="Node size scale: linear|log. Default: None")

    parser.add_argument('--node-file-id',
                        dest='node_file_id',
                        type=str,
                        default='id',
                        help="ID column name in the --node-file. Default: 'id'")

    parser.add_argument('--show-text-limit',
                        dest='show_text_limit',
                        type=int,
                        default=500,
                        help="When number of nodes is greater than --show-text-limit, node labels will not be visible."
                             "Default: 500")

    parser.add_argument('--node-border-color',
                        dest='node_border_color',
                        type=str,
                        default=None,
                        help="Node border color. Default: None")

    parser.add_argument('--tooltip-column',
                        dest='tooltip_column',
                        type=str,
                        default=None,
                        help="Column for node tooltips in the --node-file. Default: None")

    parser.add_argument('--show-text',
                        dest='show_text',
                        type=str,
                        default=None,
                        help="Show node labels at the position relative to node: center|above. Default: None. "
                             "If the number of nodes in the graph is greater than specified by "
                             "--show-text-limit option, which is 500 by default, "
                             "then the text will not be shown in the visualization.")

    parser.add_argument('--node-categorical-scale',
                        dest='node_categorical_scale',
                        type=str,
                        default='rainbow',
                        help="Node color categorical scale node from d3-scale-chromatic."
                             "https://observablehq.com/@d3/sequential-scales. Default: rainbow")

    parser.add_argument('--edge-categorical-scale',
                        dest='edge_categorical_scale',
                        type=str,
                        default='rainbow',
                        help="Edge color categorical scale for edge d3-scale-chromatic."
                             "https://observablehq.com/@d3/sequential-scales. Default: rainbow")

    parser.add_argument('--node-gradient-scale',
                        dest='node_gradient_scale',
                        type=str,
                        default='d3.interpolateRdBu',
                        help="Node color gradient scale from d3-scale-chromatic. Default: d3.interpolateRdBu")

    parser.add_argument('--edge-gradient-scale',
                        dest='edge_gradient_scale',
                        type=str,
                        default='d3.interpolateRdBu',
                        help="Edge color gradient scale from d3-scale-chromatic. Default: d3.interpolateRdBu")

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
        edge_color_hex: bool = False,
        edge_color_numbers: bool = False,
        edge_color_style: str = None,
        edge_color_default: str = '#000000',
        edge_width_column: str = None,
        edge_width_default: float = 1.0,
        edge_width_minimum: float = 1.0,
        edge_width_maximum: float = 5.0,
        edge_width_scale: str = None,
        node_color_column: str = None,
        node_color_numbers: bool = False,
        node_color_hex: bool = False,
        node_color_style: str = None,
        node_color_default: str = '#000000',
        node_color_scale: str = None,
        node_size_column: str = None,
        node_size_default: float = 2.0,
        node_size_minimum: float = 1.0,
        node_size_maximum: float = 5.0,
        node_size_scale: str = None,
        node_file_id: str = 'id',
        show_text_limit: int = 500,
        node_border_color: str = None,
        tooltip_column: str = None,
        show_text: str = None,
        node_categorical_scale: str = 'rainbow',
        edge_categorical_scale: str = 'rainbow',
        node_gradient_scale: str = 'd3.interpolateRdBu',
        edge_gradient_scale: str = 'd3.interpolateRdBu',

        **kwargs  # Whatever KgtkFileOptions and KgtkValueOptions want.
        ) -> int:
    from kgtk.visualize.visualize_api import KgtkVisualize
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
        edge_color_hex=edge_color_hex,
        edge_color_numbers=edge_color_numbers,
        edge_color_style=edge_color_style,
        edge_color_default=edge_color_default,
        edge_width_column=edge_width_column,
        edge_width_default=edge_width_default,
        edge_width_minimum=edge_width_minimum,
        edge_width_maximum=edge_width_maximum,
        edge_width_scale=edge_width_scale,
        node_color_column=node_color_column,
        node_color_hex=node_color_hex,
        node_color_numbers=node_color_numbers,
        node_color_style=node_color_style,
        node_color_default=node_color_default,
        node_color_scale=node_color_scale,
        node_size_column=node_size_column,
        node_size_default=node_size_default,
        node_size_minimum=node_size_minimum,
        node_size_maximum=node_size_maximum,
        node_size_scale=node_size_scale,
        node_file_id=node_file_id,
        show_text_limit=show_text_limit,
        node_border_color=node_border_color,
        tooltip_column=tooltip_column,
        show_text=show_text,
        node_categorical_scale=node_categorical_scale,
        edge_categorical_scale=edge_categorical_scale,
        node_gradient_scale=node_gradient_scale,
        edge_gradient_scale=edge_gradient_scale,
        kwargs=kwargs
    )
    kv.execute()
