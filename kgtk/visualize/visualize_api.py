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


def parser():
    return {
        'help': 'Visualize API',
        'description': 'Use API to convert edge file to html visualization'
    }


node_color_map = {
    'few_subclasses': 0,
    'many_subclasses': 1
}

kgtk_format = KgtkFormat()


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
        self.kwargs = kwargs

    def execute(self) -> int:
        d, node_color, node_color_map_len = self.compute_visualization_graph()
        self.to_html(d, node_color, node_color_map_len - 1)
        return 0

    def compute_visualization_graph(self):
        input_kgtk_file: Path = KGTKArgumentParser.get_input_file(self.input_file)

        # Select where to send error messages, defaulting to stderr.
        error_file: typing.TextIO = sys.stdout if self.errors_to_stdout else sys.stderr
        # Build the option structures.
        reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(self.kwargs)
        value_options: KgtkValueOptions = KgtkValueOptions.from_dict(self.kwargs)
        # Show the final option structures for debugging and documentation.
        try:

            # First create the KgtkReader.  It provides parameters used by the ID
            # column builder. Next, create the ID column builder, which provides a
            # possibly revised list of column names for the KgtkWriter.  Create
            # the KgtkWriter.  Last, process the data stream.

            # Open the input file.
            kr: KgtkReader = KgtkReader.open(input_kgtk_file,
                                             error_file=error_file,
                                             options=reader_options,
                                             value_options=value_options,
                                             verbose=self.verbose,
                                             very_verbose=self.very_verbose,
                                             )

            d = {}
            nodes = set()
            edges = []
            base = math.e

            if self.node_size_minimum == 0.0 and self.node_size_scale == 'log':
                raise ValueError("node size cannot be 0 when using log scale")

            if self.edge_width_minimum == 0 and self.edge_width_scale == 'log':
                raise ValueError("edge width cannot be 0 when using log scale")

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

            count = 0
            color_set = {}

            for row in kr:
                if self.node_file is None:
                    clean_node1_label, _, _ = kgtk_format.destringify(row[node1_label_idx])
                    nodes.add((row[node1_idx], clean_node1_label))

                    clean_node2_label, _, _ = kgtk_format.destringify(row[node2_label_idx])
                    nodes.add((row[node2_idx], clean_node2_label))

                width_orig = 1.0
                if self.edge_width_column is not None:
                    _width_orig = row[kr.column_name_map[self.edge_width_column]]
                    try:
                        width_orig = float(_width_orig)
                    except Exception as e:
                        print(f"Can't convert edge width column value: {_width_orig} to float", file=error_file)

                if '@' in row[label_label_idx]:
                    _label_label, _, _ = kgtk_format.destringify(row[label_label_idx])
                else:
                    _label_label = row[label_label_idx]

                _edge_obj = {
                    'source': row[node1_idx],
                    'target': row[node2_idx],
                    'label': _label_label,
                    'width_orig': width_orig
                }

                if self.edge_color_column is not None:
                    _edge_color = row[kr.column_name_map[self.edge_color_column]].strip()
                    if self.edge_color_mapping == 'fixed':
                        _edge_obj['color'] = _edge_color if _edge_color != '' else self.edge_color_default
                    elif self.edge_color_style == 'gradient':
                        _edge_obj['color'] = _edge_color if _edge_color != '' else -1
                    else:
                        if _edge_color not in color_set:
                            color_set[_edge_color] = count
                            count += 1
                        _edge_obj['color'] = min(color_set[_edge_color], 9) \
                            if _edge_color != "" \
                            else self.edge_color_default
                else:
                    _edge_obj['color'] = self.edge_color_default

                edges.append(_edge_obj)

            arr = []
            if self.edge_width_mapping == 'fixed':
                for edge in edges:
                    if edge['width_orig'] >= 0:
                        edge['width'] = edge['width_orig']
                    else:
                        edge['width'] = self.edge_width_default
            elif self.edge_width_scale == 'linear':
                for edge in edges:
                    if edge['width_orig'] >= 0:
                        arr.append(edge['width_orig'])
                for edge in edges:
                    if edge['width_orig'] >= 0:
                        edge['width'] = self.edge_width_minimum + (edge['width_orig'] - min(arr)) * (
                                self.edge_width_maximum - self.edge_width_minimum) / (max(arr) - min(arr))
                    else:
                        edge['width'] = self.edge_width_default
            elif self.edge_width_scale == 'log':
                for edge in edges:
                    if edge['width_orig'] >= 0:
                        arr.append(edge['width_orig'])
                for edge in edges:
                    if edge['width_orig'] >= 0:
                        if min(arr) == 0:
                            log_min = -1
                        else:
                            log_min = math.log(min(arr), base)

                        if max(arr) == 0:
                            log_max = -1
                        else:
                            log_max = math.log(max(arr), base)

                        if edge['width_orig'] == 0:
                            log_cur = -1
                        else:
                            log_cur = math.log(edge['width_orig'], base)

                        if log_max == log_min:
                            edge['width'] = self.edge_width_default
                        else:
                            edge['width'] = self.edge_width_minimum + (log_cur - log_min) * (
                                    self.edge_width_maximum - self.edge_width_minimum) / (log_max - log_min)
                    else:
                        edge['width'] = self.edge_width_default
            else:
                for edge in edges:
                    edge['width'] = self.edge_width_default

            if self.edge_color_column is not None and self.edge_color_style == 'gradient':
                edge_color_list = []
                for edge in edges:
                    if float(edge['color']) > 0:
                        edge_color_list.append(float(edge['color']))
                for edge in edges:
                    if float(edge['color']) < 0:
                        edge['color'] = self.edge_color_default
                    else:
                        edge['color'] = (float(edge['color']) - min(edge_color_list)) / \
                                        (max(edge_color_list) - min(edge_color_list))

            if self.node_file is None:
                d['nodes'] = []
                for ele in nodes:
                    d['nodes'].append(
                        {'id': ele[0], 'label': ele[1], 'tooltip': ele[1]})
            else:
                d['nodes'] = []

            d['links'] = edges

            node_color = 0

            if self.node_file is not None:
                kr_node: KgtkReader = KgtkReader.open(self.node_file,
                                                      error_file=error_file,
                                                      options=reader_options,
                                                      value_options=value_options,
                                                      verbose=self.verbose,
                                                      very_verbose=self.very_verbose,
                                                      mode=KgtkReaderMode.NONE,
                                                      )

                node_color_list = []
                node_size_list = []

                for row in kr_node:
                    if self.node_color_scale == 'linear' or self.node_color_scale == 'log':
                        _node_color = None
                        try:
                            _node_color = float(row[kr_node.column_name_map[self.node_color_column]])
                        except:
                            pass
                        if _node_color is not None:
                            node_color_list.append(_node_color)
                    if self.node_size_scale == 'linear' or self.node_size_scale == 'log':
                        _node_size = None
                        try:
                            _node_size = float(row[kr_node.column_name_map[self.node_size_column]])
                        except:
                            pass
                        if _node_size is not None:
                            node_size_list.append(_node_size)

                kr_node.close()

                max_node_color = max(node_color_list) if node_color_list else None
                min_node_color = min(node_color_list) if node_color_list else None

                max_node_size = max(node_size_list) if node_size_list else None
                min_node_size = min(node_size_list) if node_size_list else None

                kr_node: KgtkReader = KgtkReader.open(self.node_file,
                                                      error_file=error_file,
                                                      options=reader_options,
                                                      value_options=value_options,
                                                      verbose=self.verbose,
                                                      very_verbose=self.very_verbose,
                                                      mode=KgtkReaderMode.NONE,
                                                      )

                if self.node_file_id not in kr_node.column_name_map:
                    raise ValueError("no id column in node file")

                for row in kr_node:
                    _id = row[kr_node.column_name_map[self.node_file_id]]
                    temp = {'id': _id}

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
                        if self.node_color_mapping == 'fixed':
                            if str(_node_color).strip() != '':
                                temp['color'] = _node_color
                            else:
                                temp['color'] = self.node_color_default
                        else:
                            if self.node_color_style == 'gradient':
                                if self.node_color_scale == 'linear':

                                    node_color = 1
                                    try:
                                        temp['color'] = (float(_node_color) - min_node_color) / (max_node_color
                                                                                                 - min_node_color)
                                    except:
                                        temp['color'] = self.node_color_default
                                elif self.node_color_scale == 'log':
                                    node_color = 1

                                    if min_node_color == 0:
                                        log_min = -1
                                    else:
                                        log_min = math.log(min_node_color, base)

                                    if max_node_color == 0:
                                        log_max = -1
                                    else:
                                        log_max = math.log(max_node_color, base)

                                    if float(_node_color) == 0:
                                        log_cur = -1
                                    else:
                                        log_cur = math.log(float(_node_color), base)

                                    if log_max == log_min:
                                        temp['color'] = self.node_color_default
                                    else:
                                        color_value \
                                            = 0 + (log_cur - log_min) * (1 - 0) / (log_max - log_min)
                                        try:
                                            temp['color'] = float(color_value)
                                        except:
                                            temp['color'] = self.node_color_default

                                else:
                                    if self.node_color_mapping == 'fixed':
                                        if str(_node_color).strip() != '':
                                            temp['color'] = _node_color
                                        else:
                                            temp['color'] = self.node_color_default
                            else:
                                node_color = 2
                                if _node_color not in node_color_map:
                                    node_color_map[_node_color] = len(node_color_map)

                                temp['color'] = node_color_map[_node_color]

                    if self.node_size_column is not None:
                        _node_size = row[kr_node.column_name_map[self.node_size_column]]
                        if self.node_size_mapping == 'fixed':
                            temp['size'] = _node_size if _node_size.strip() != "" else self.node_size_default
                        else:
                            if self.node_size_scale == 'linear':
                                try:
                                    size_value = self.node_size_minimum + (float(_node_size) - min_node_size) * \
                                                 (self.node_size_maximum - self.node_size_minimum) / \
                                                 (max_node_size - min_node_size)
                                    temp['size'] = float(size_value)
                                except:
                                    temp['size'] = self.node_size_default
                            elif self.node_size_scale == 'log':
                                if min_node_size == 0:
                                    log_min = -1
                                else:
                                    log_min = math.log(min_node_size, base)

                                if max_node_size == 0:
                                    log_max = -1
                                else:
                                    log_max = math.log(max_node_size, base)

                                if float(_node_size) == 0:
                                    log_cur = -1
                                else:
                                    log_cur = math.log(float(_node_size), base)

                                if log_max == log_min:
                                    temp['size'] = self.node_size_default
                                else:
                                    try:
                                        size_value = self.node_size_minimum + (log_cur - log_min) * (
                                                self.node_size_maximum - self.node_size_minimum) / (log_max - log_min)
                                        temp['size'] = size_value
                                    except:
                                        temp['size'] = self.node_size_default

                    else:
                        temp['size'] = self.node_size_default

                    if 'x' in kr_node.column_name_map:
                        temp['fx'] = float(row[kr_node.column_name_map['x']])
                        temp['fy'] = float(row[kr_node.column_name_map['y']])
                    d['nodes'].append(temp)

                kr_node.close()

            kr.close()

        except SystemExit as e:
            raise KGTKException("Exit requested")
        except Exception as e:
            raise KGTKException(str(e))
        return d, node_color, len(node_color_map)

    def to_html(self, d, node_color, num_colors):
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
        rainbow = d3.scaleSequential().domain([0, {num_colors}]).interpolator(d3.interpolateRainbow);
        <!--rainbow = d3.scaleSequential().domain([1,71]).interpolator(d3.interpolateSinebow);-->
        <!--rainbow = d3.scaleSequential().domain([1,71]).interpolator(d3.interpolateCool);-->
                
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

        if node_color == 0:
            f.write('''
        .nodeAutoColorBy('group')
        .linkWidth((link) => link.width)''')
        elif node_color == 1:
            f.write(f'''
        .nodeColor((node) => node.color[0] == "#" ? node.color : {self.node_gradient_scale}(node.color))
        .linkWidth((link) => link.width)''')
            node_text_format = self.node_gradient_scale + '(node.color)'
        else:
            f.write(f'''
                .nodeColor((node) => node.color[0] == "#" ? node.color : rainbow(node.color))
                .linkWidth((link) => link.width)''')

            node_text_format = 'rainbow(node.color)'
        if self.node_border_color is not None:
            node_text_format = "'" + self.node_border_color + "'"
        if self.direction == 'arrow':
            f.write('''
          .linkDirectionalArrowLength(6)
          .linkDirectionalArrowRelPos(1)''')
        elif self.direction == 'particle':
            f.write('''      .linkDirectionalParticles(2)
        ''')
        if self.edge_color_style == 'categorical':
            f.write(
                f'''        .linkColor((link) => link.color[0] == "#" ? link.color :
                    {self.edge_categorical_scale}[link.color])''')
        elif self.edge_color_style == 'gradient':
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
        if self.text_node is not None and self.show_text_limit > len(d['nodes']):

            if self.text_node == 'center':
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
        f.write('''  </script>
    </body>''')
