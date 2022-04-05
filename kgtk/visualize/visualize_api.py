"""Convert edge file to html visualization
"""
import json
import math

from kgtk.cli_argparse import KGTKArgumentParser

from pathlib import Path
import sys
import typing

from kgtk.exceptions import KGTKException
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions, KgtkReaderMode
from kgtk.value.kgtkvalueoptions import KgtkValueOptions
from kgtk.kgtkformat import KgtkFormat
import re
from typing import List


def parser():
    return {
        'help': 'Visualize API',
        'description': 'Use API to convert edge file to html visualization'
    }


kgtk_format = KgtkFormat()

compiled_hex_color_regex = re.compile(r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$")

GRADIENT = 'gradient'
CATEGORICAL = 'categorical'


class KgtkVisualize:
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
            edge_color_default: str = '#000000',
            edge_width_column: str = None,
            edge_width_default: float = 1.0,
            edge_width_minimum: float = 1.0,
            edge_width_maximum: float = 5.0,
            edge_width_scale: str = None,
            edge_color_numbers: bool = False,
            edge_color_hex: bool = False,
            edge_color_scale: str = None,
            node_color_column: str = None,
            node_color_style: str = None,
            node_color_default: str = '#000000',
            node_color_scale: str = None,
            node_color_numbers: bool = False,
            node_color_hex: bool = False,
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
            kwargs=None):
        if kwargs is None:
            kwargs = {'errors_to_stderr': True, 'show_options': False}
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
        self.edge_color_default = edge_color_default
        self.edge_color_numbers = edge_color_numbers
        self.edge_color_hex = edge_color_hex
        self.edge_color_scale = edge_color_scale
        self.edge_width_column = edge_width_column
        self.edge_width_default = edge_width_default
        self.edge_width_minimum = edge_width_minimum
        self.edge_width_maximum = edge_width_maximum
        self.edge_width_scale = edge_width_scale
        self.node_color_column = node_color_column
        self.node_color_style = node_color_style
        self.node_color_default = node_color_default
        self.node_color_scale = node_color_scale
        self.node_size_column = node_size_column
        self.node_size_default = node_size_default
        self.node_size_minimum = node_size_minimum
        self.node_size_maximum = node_size_maximum
        self.node_size_scale = node_size_scale
        self.node_file_id = node_file_id
        self.show_text_limit = show_text_limit
        self.node_border_color = node_border_color
        self.tooltip_column = tooltip_column
        self.show_text = show_text
        self.node_categorical_scale = node_categorical_scale
        self.edge_categorical_scale = edge_categorical_scale
        self.node_gradient_scale = node_gradient_scale
        self.edge_gradient_scale = edge_gradient_scale
        self.node_color_numbers = node_color_numbers
        self.node_color_hex = node_color_hex
        self.kwargs = kwargs

        self.input_kgtk_file: Path = KGTKArgumentParser.get_input_file(self.input_file)

        # Select where to send error messages, defaulting to stderr.
        self.error_file: typing.TextIO = sys.stdout if self.errors_to_stdout else sys.stderr
        # Build the option structures.
        self.reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(self.kwargs)
        self.value_options: KgtkValueOptions = KgtkValueOptions.from_dict(self.kwargs)

        # define the base for log
        self.base = 2.0

        self.edge_color_map = {}

        self.node_color_map = {
            'few_subclasses': 0,
            'many_subclasses': 1
        }

        self.node_color_choice = 0

        if self.node_size_minimum == 0.0 and self.node_size_scale == 'log':
            raise ValueError("node size cannot be 0 when using log scale")
        if self.edge_width_minimum == 0 and self.edge_width_scale == 'log':
            raise ValueError("edge width cannot be 0 when using log scale")

    def execute(self) -> int:

        d = self.compute_visualization_graph()
        self.to_html(d)
        return 0

    def compute_visualization_graph(self):
        d = {}
        # Show the final option structures for debugging and documentation.
        try:
            edges, nodes = self.process_edge_file()
            if self.node_file is not None:
                nodes = self.process_node_file()
            d['links'] = edges
            d['nodes'] = nodes
        except SystemExit as e:
            raise KGTKException("Exit requested")
        except Exception as e:
            raise KGTKException(str(e))
        return d

    def process_edge_file(self):
        # First create the KgtkReader.  It provides parameters used by the ID
        # column builder. Next, create the ID column builder, which provides a
        # possibly revised list of column names for the KgtkWriter.  Create
        # the KgtkWriter.  Last, process the data stream.
        # Open the input file.
        kr: KgtkReader = KgtkReader.open(self.input_kgtk_file,
                                         error_file=self.error_file,
                                         options=self.reader_options,
                                         value_options=self.value_options,
                                         verbose=self.verbose,
                                         very_verbose=self.very_verbose,
                                         )

        nodes = set()
        nodes_from_edge_file = []
        edges = []

        node1_idx = kr.column_name_map['node1']
        node2_idx = kr.column_name_map['node2']

        if self.node_file is None and 'node1;label' in kr.column_name_map:
            node1_label_idx = kr.column_name_map['node1;label']
        else:
            node1_label_idx = kr.column_name_map['node1']

        if self.node_file is None and 'node2;label' in kr.column_name_map:
            node2_label_idx = kr.column_name_map['node2;label']
        else:
            node2_label_idx = kr.column_name_map['node2']

        if 'label;label' not in kr.column_name_map:
            label_label_idx = kr.column_name_map['label']
        else:
            label_label_idx = kr.column_name_map['label;label']

        for row in kr:
            if self.node_file is None:
                node1_label = row[node1_label_idx]
                node2_label = row[node2_label_idx]
                if '@' in node1_label:
                    clean_node1_label, _, _ = kgtk_format.destringify(node1_label)
                else:
                    clean_node1_label = node1_label
                nodes.add((row[node1_idx], clean_node1_label))

                if '@' in node2_label:
                    clean_node2_label, _, _ = kgtk_format.destringify(node2_label)
                else:
                    clean_node2_label = node2_label
                nodes.add((row[node2_idx], clean_node2_label))

            if '@' in row[label_label_idx]:
                _label_label, _, _ = kgtk_format.destringify(row[label_label_idx])
            else:
                _label_label = row[label_label_idx]

            _edge_obj = {
                'source': row[node1_idx],
                'target': row[node2_idx],
                'label': _label_label
            }

            if self.edge_width_column is not None:
                _width_orig = KgtkVisualize.convert_string_float(row[kr.column_name_map[self.edge_width_column]])
                if _width_orig is not None:
                    _edge_obj['width_orig'] = _width_orig
                else:
                    _edge_obj['width_orig'] = 0.0
            else:
                _edge_obj['width'] = self.edge_width_default

            if self.edge_color_column is not None:
                _edge_color = row[kr.column_name_map[self.edge_color_column]].strip()

                if self.edge_color_numbers:
                    _edge_color = KgtkVisualize.convert_string_float(_edge_color)
                    if _edge_color is not None:
                        _edge_obj['orig_color'] = _edge_color
                    else:
                        _edge_obj['orig_color'] = 0.0
                elif self.edge_color_hex:
                    if KgtkVisualize.is_valid_hex_color(_edge_color):
                        _edge_obj['color'] = _edge_color
                    else:
                        _edge_obj['color'] = self.edge_color_default
                else:
                    _edge_obj['orig_color'] = _edge_color
            else:
                _edge_obj['color'] = self.edge_color_default

            edges.append(_edge_obj)

        kr.close()

        if self.edge_width_column is not None:
            edges = self.calculate_size(edges,
                                        self.edge_width_scale,
                                        self.edge_width_default,
                                        self.edge_width_minimum,
                                        self.edge_width_maximum,
                                        'width_orig',
                                        'width')

        if self.edge_color_column is not None:
            edges = self.calculate_color(edges,
                                         self.edge_color_hex,
                                         self.edge_color_numbers,
                                         self.edge_color_style,
                                         self.edge_color_scale,
                                         self.edge_color_default,
                                         False)
        if self.node_file is None:
            for ele in nodes:
                nodes_from_edge_file.append(
                    {'id': ele[0], 'label': ele[1], 'tooltip': ele[1]})

        return edges, nodes_from_edge_file

    @staticmethod
    def is_valid_hex_color(color_string: str) -> bool:

        if color_string is None or color_string.strip() == "":
            return False

        if re.search(compiled_hex_color_regex, color_string.strip()):
            return True
        else:
            return False

    @staticmethod
    def convert_string_float(a_string: str) -> float:
        if a_string is None or a_string.strip() == '':
            return None
        try:
            return float(a_string.strip())
        except ValueError:
            return None

    def process_node_file(self):
        nodes = []
        if self.node_file is not None:

            kr_node: KgtkReader = KgtkReader.open(self.node_file,
                                                  error_file=self.error_file,
                                                  options=self.reader_options,
                                                  value_options=self.value_options,
                                                  verbose=self.verbose,
                                                  very_verbose=self.very_verbose,
                                                  mode=KgtkReaderMode.NONE,
                                                  )

            if self.node_file_id not in kr_node.column_name_map:
                raise ValueError("no id column in node file")

            for row in kr_node:
                _id = row[kr_node.column_name_map[self.node_file_id]]
                temp = {'id': _id}

                if 'x' in kr_node.column_name_map:
                    temp['fx'] = float(row[kr_node.column_name_map['x']])
                    temp['fy'] = float(row[kr_node.column_name_map['y']])

                if 'label' in kr_node.column_name_map:
                    _node_label, _, _ = kgtk_format.destringify(row[kr_node.column_name_map['label']])
                    if _node_label != "":
                        temp['label'] = _node_label
                    else:
                        temp['label'] = _id
                else:
                    temp['label'] = _id

                if self.tooltip_column is not None:
                    if str(row[kr_node.column_name_map[self.tooltip_column]]).strip() != '':
                        temp['tooltip'] = str(row[kr_node.column_name_map[self.tooltip_column]])
                    else:
                        temp['tooltip'] = temp['label']
                else:
                    temp['tooltip'] = temp['label']

                if self.node_color_column is not None:
                    _node_color = row[kr_node.column_name_map[self.node_color_column]]
                    if self.node_color_numbers:
                        _node_color = KgtkVisualize.convert_string_float(_node_color)
                        if _node_color is not None:
                            temp['orig_color'] = _node_color
                        else:
                            temp['orig_color'] = 0.0
                    elif self.node_color_hex:
                        if KgtkVisualize.is_valid_hex_color(_node_color):
                            temp['color'] = _node_color
                        else:
                            temp['color'] = self.node_color_default
                    else:
                        temp['orig_color'] = _node_color
                else:
                    temp['color'] = self.node_color_default

                if self.node_size_column is not None:
                    _node_size = KgtkVisualize.convert_string_float(row[kr_node.column_name_map[self.node_size_column]])
                    if _node_size is not None:
                        temp['orig_size'] = _node_size
                    else:
                        temp['orig_size'] = 0.0
                else:
                    temp['size'] = self.node_size_default

                nodes.append(temp)
            kr_node.close()

            if self.node_color_column is not None:
                nodes = self.calculate_color(nodes,
                                             self.node_color_hex,
                                             self.node_color_numbers,
                                             self.node_color_style,
                                             self.node_color_scale,
                                             self.node_color_default,
                                             True)

            if self.node_size_column is not None:
                self.calculate_size(nodes,
                                    self.node_size_scale,
                                    self.node_size_default,
                                    self.node_size_minimum,
                                    self.node_size_maximum,
                                    'orig_size',
                                    'size')

        return nodes

    def calculate_color(self,
                        nodes: List[dict],
                        node_color_hex: bool,
                        node_color_numbers: bool,
                        node_color_style: str,
                        node_color_scale: str,
                        node_color_default: str,
                        process_nodes: bool) -> List[dict]:

        if node_color_hex:
            # all good, nothing to do here
            pass
        else:
            node_color_list = []
            max_color = -1
            min_color = -1
            if self.node_color_numbers:
                node_color_list = [x['orig_color'] for x in nodes]
                max_color = max(node_color_list)
                min_color = min(node_color_list)
            for node in nodes:
                orig_color = node['orig_color']
                if node_color_numbers:

                    log_max_color = math.log(max_color, self.base) if max_color > 0.0 else -1.0
                    log_min_color = math.log(min_color, self.base) if min_color > 0.0 else -1.0

                    if node_color_style == GRADIENT:
                        if process_nodes:
                            self.node_color_choice = 1
                        if node_color_scale == 'linear':
                            node['color'] = (orig_color - min_color) / (max_color - min_color)
                        elif node_color_scale == 'log':
                            if orig_color == 0.0 or log_max_color == log_min_color:
                                node['color'] = node_color_default
                            else:
                                node['color'] = (math.log(orig_color, self.base) - log_min_color) / (
                                        log_max_color - log_min_color)
                        else:
                            node['color'] = orig_color if orig_color != 0.0 else node_color_default

                if 'color' not in node:
                    if process_nodes:
                        self.node_color_choice = 2
                        if orig_color not in self.node_color_map:
                            self.node_color_map[orig_color] = len(self.node_color_map)

                        node['color'] = self.node_color_map[orig_color]
                    else:
                        if orig_color not in self.edge_color_map:
                            self.edge_color_map[orig_color] = len(self.edge_color_map)
                        node['color'] = self.edge_color_map[orig_color]
                del node['orig_color']
        return nodes

    def calculate_size(self,
                       nodes: List[dict],
                       node_size_scale: str,
                       node_size_default: str,
                       node_size_minimum: float,
                       node_size_maximum: float,
                       size_field: str,
                       output_field: str
                       ) -> List[dict]:
        node_size_list = [x[size_field] for x in nodes]
        max_size = max(node_size_list)
        min_size = min(node_size_list)
        log_max_size = math.log(max_size, self.base) if max_size > 0.0 else -1.0
        log_min_size = math.log(min_size, self.base) if min_size > 0.0 else -1.0
        for node in nodes:
            node_size = node[size_field]
            if node_size_scale == 'linear':
                node[output_field] = node_size_minimum + (node_size - min_size) * \
                                     (node_size_maximum - node_size_minimum) / \
                                     (max_size - min_size)
            elif node_size_scale == 'log':
                if node_size == 0.0 or log_min_size == log_max_size:
                    node[output_field] = node_size_default
                else:
                    node[output_field] = node_size_minimum + (math.log(node_size, self.base) - log_min_size) * (
                            node_size_maximum - node_size_minimum) / (log_max_size - log_min_size)
            else:
                node[output_field] = node_size if node_size > 0 else node_size_default
        return nodes

    def to_html(self, d):
        output_kgtk_file: Path = KGTKArgumentParser.get_output_file(self.output_file)
        f = open(output_kgtk_file, 'w')
        f.write(f'''<head>
            <style> body {{ margin: 0; }} </style>
            <script src="https://cdn.jsdelivr.net/npm/d3-color@3"></script>
            <script src="https://cdn.jsdelivr.net/npm/d3-interpolate@3"></script>
            <script src="https://cdn.jsdelivr.net/npm/d3-scale-chromatic@3"></script>
            <script src="https://cdn.jsdelivr.net/npm/d3-scale@4"></script>
            <script src="https://unpkg.com/force-graph"></script>
            <!--<script src="../../dist/force-graph.js"></script>-->
            </head>
            <body>
            <div id="graph"></div>
            <script>
                rainbow = d3.scaleSequential().domain([0, {len(self.node_color_map) - 1}]).interpolator(d3.interpolateRainbow);        
               const j = ''')
        f.write(json.dumps(d, indent=4))
        f.write('''
              const Graph = ForceGraph()
              (document.getElementById('graph'))
                .graphData(j)
                .nodeId('id')
                .nodeLabel('tooltip')
                .nodeVal('size')''')

        node_text_format = ''
        if self.node_color_choice == 0:
            f.write('''
                .nodeAutoColorBy('group')
                .linkWidth((link) => link.width)''')
            node_text_format = '(node.color)'
        elif self.node_color_choice == 1:
            f.write(f'''
                .nodeColor((node) => node.color[0] == "#" ? node.color : {self.node_gradient_scale}(node.color))
                .linkWidth((link) => link.width)''')
            node_text_format = self.node_gradient_scale + '(node.color)'
        else:
            f.write(f'''
                        .nodeColor((node) => node.color[0] == "#" ? node.color : {self.node_categorical_scale}(node.color))
                        .linkWidth((link) => link.width)''')

            node_text_format = f'{self.node_categorical_scale}(node.color)'
        if self.node_border_color is not None:
            node_text_format = "'" + self.node_border_color + "'"
        if self.direction == 'arrow':
            f.write('''
                  .linkDirectionalArrowLength(6)
                  .linkDirectionalArrowRelPos(1)''')
        elif self.direction == 'particle':
            f.write('''      .linkDirectionalParticles(2)
                ''')
        if self.show_text is not None and self.show_text_limit > len(d['nodes']):

            if self.show_text == 'center':
                y_move = 0
            else:
                y_move = 10

            f.write('''
                            .nodeCanvasObject((node, ctx, globalScale) => {
                      const label = node.label;
                      const fontSize = 12/globalScale;
                      ctx.font = `${fontSize}px Sans-Serif`;
                      const textWidth = ctx.measureText(label).width;
                      const bckgDimensions = [textWidth, fontSize].map(n => n + fontSize * 0.2); // some padding
                      ''')

            f.write(f'''
                      ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
                      ctx.fillRect(node.x - bckgDimensions[0] / 2, node.y - {y_move} - 
                      bckgDimensions[1] / 2, ...bckgDimensions);
                      ctx.textAlign = 'center';
                      ctx.textBaseline = 'middle';
                      ''')

            if node_text_format != '':
                f.write(f'''
                        ctx.fillStyle = {node_text_format};
                        ''')
            f.write(f'''
                      ctx.fillText(label, node.x, node.y - {y_move});
                      ''')

            f.write('''
                      ctx.beginPath(); ctx.arc(node.x, node.y, node.size, 0, 2 * Math.PI, false);  ctx.fill();
                      node.__bckgDimensions = bckgDimensions; // to re-use in nodePointerAreaPaint
                      })''')
        if self.edge_color_style == CATEGORICAL:
            f.write(
                f'''        .linkColor((link) => link.color[0] == "#" ? link.color :
                            {self.edge_categorical_scale}[link.color])''')
        elif self.edge_color_style == GRADIENT:
            f.write(
                f'''        .linkColor((link) => link.color[0] == "#" ? link.color :
                            {self.edge_gradient_scale}(link.color))''')
        else:
            f.write('''        .linkColor((link) => link.color)''')
        if self.edge_label:
            f.write('''                        .linkCanvasObjectMode(() => 'after')
                .linkCanvasObject((link, ctx) => {
                  const MAX_FONT_SIZE = 4;
                  const LABEL_NODE_MARGIN = Graph.nodeRelSize() * 1.5;
                  const start = link.source;
                  const end = link.target;
                  // ignore unbound links
                  if (typeof start !== 'object' || typeof end !== 'object') return;
                  // calculate label positioning
                  const textPos = Object.assign(...['x', 'y'].map(c => ({
                    [c]: start[c] + (end[c] - start[c]) / 2 // calc middle point
                  })));
                  const relLink = { x: end.x - start.x, y: end.y - start.y };
                  const maxTextLength = Math.sqrt(Math.pow(relLink.x, 2) + Math.pow(relLink.y, 2)) - LABEL_NODE_MARGIN * 2;
                  let textAngle = Math.atan2(relLink.y, relLink.x);
                  // maintain label vertical orientation for legibility
                  if (textAngle > Math.PI / 2) textAngle = -(Math.PI - textAngle);
                  if (textAngle < -Math.PI / 2) textAngle = -(-Math.PI - textAngle);
                  const label = `${link.label}`;
                  // estimate fontSize to fit in link length
                  const color = `rgba(${link.color}, 0.8)`;
                  ctx.font = '1px Sans-Serif';
                  const fontSize = Math.min(MAX_FONT_SIZE, maxTextLength / ctx.measureText(label).width);
                  ctx.font = `${fontSize}px Sans-Serif`;
                  const textWidth = ctx.measureText(label).width;
                  const bckgDimensions = [textWidth, fontSize].map(n => n + fontSize * 0.2); // some padding
                  // draw text label (with background rect)
                  ctx.save();
                  ctx.translate(textPos.x, textPos.y);
                  ctx.rotate(textAngle);
                  ctx.fillStyle = 'rgba(255, 255, 255)';
                  ctx.fillRect(- bckgDimensions[0] / 2, - bckgDimensions[1] / 2, ...bckgDimensions);
                  ctx.textAlign = 'center';
                  ctx.textBaseline = 'middle';
                  ctx.fillStyle = 'darkgrey';
                  ctx.fillText(label, 0, 0);
                  ctx.restore();
                });
                ''')
        f.write('''  </script>
            </body>''')
