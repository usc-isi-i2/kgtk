"""Convert edge file to html visualization
"""
import json
import math
import pandas as pd

from kgtk.cli_argparse import KGTKArgumentParser

from pathlib import Path
import sys
import typing

from kgtk.exceptions import KGTKException
from kgtk.io.kgtkreader import KgtkReader, \
    KgtkReaderOptions, KgtkReaderMode
from kgtk.value.kgtkvalueoptions import KgtkValueOptions


def parser():
    return {
        'help': 'Visualize API',
        'description': 'Use API to convert edge file to html visualization'
    }


node_color_map = {
    'few_subclasses': 0,
    'many_subclasses': 1
}


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
        d, node_color = self.compute_visualization_graph()
        self.to_html(d, node_color)
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

            n1 = kr.column_name_map['node1']
            n2 = kr.column_name_map['node2']

            if self.node_file is None and 'node1;label' in kr.column_name_map:
                l1 = kr.column_name_map['node1;label']
            else:
                l1 = kr.column_name_map['node1']

            if self.node_file is None and 'node1;label' in kr.column_name_map:
                l3 = kr.column_name_map['node2;label']
            else:
                l3 = kr.column_name_map['node2']

            if 'label;label' not in kr.column_name_map:
                l2 = kr.column_name_map['label']
            else:
                l2 = kr.column_name_map['label;label']

            count = 0
            color_set = {}

            for row in kr:
                if self.node_file is None:
                    if '@' in row[l1]:
                        nodes.add((row[n1], row[l1][1:row[l1].find('@') - 1]))
                    else:
                        nodes.add((row[n1], row[l1]))

                    if '@' in row[l3]:
                        nodes.add((row[n2], row[l3][1:row[l3].find('@') - 1]))
                    else:
                        nodes.add((row[n2], row[l3]))

                if self.edge_width_column is not None:
                    if (not pd.isna(row[kr.column_name_map[self.edge_width_column]])) and str(
                            row[kr.column_name_map[self.edge_width_column]]) != '':
                        width_orig = float(
                            row[kr.column_name_map[self.edge_width_column]])
                    else:
                        width_orig = -1.0
                else:
                    width_orig = 1

                if self.edge_color_column is not None and '@' in row[l2]:
                    if self.edge_color_mapping == 'fixed':
                        edges.append({'source': row[n1], 'target': row[n2], 'label': row[l2][1:row[l2].find('@') - 1],
                                      'color': row[kr.column_name_map[self.edge_color_column]] if not pd.isna(
                                          row[kr.column_name_map[self.edge_color_column]]) and str(
                                          row[kr.column_name_map[
                                              self.edge_color_column]]) != '' else self.edge_color_default,
                                      'width_orig': width_orig})
                    elif self.edge_color_style == 'gradient':
                        edges.append({'source': row[n1], 'target': row[n2], 'label': row[l2][1:row[l2].find('@') - 1],
                                      'color': row[kr.column_name_map[self.edge_color_column]] if not pd.isna(
                                          row[kr.column_name_map[self.edge_color_column]]) and str(
                                          row[kr.column_name_map[self.edge_color_column]]) != '' else -1,
                                      'width_orig': width_orig})
                    else:
                        if row[kr.column_name_map[self.edge_color_column]] not in color_set:
                            color_set[row[kr.column_name_map[self.edge_color_column]]] = count
                            count += 1
                        edges.append({'source': row[n1], 'target': row[n2], 'label': row[l2][1:row[l2].find('@') - 1],
                                      'color': min(color_set[row[kr.column_name_map[self.edge_color_column]]],
                                                   9) if not pd.isna(
                                          row[kr.column_name_map[self.edge_color_column]]) or str(
                                          row[kr.column_name_map[self.edge_color_column]]) else self.edge_color_default,
                                      'width_orig': width_orig})
                elif self.edge_color_column is not None and '@' not in row[l2]:
                    if self.edge_color_style == 'fixed':
                        edges.append({'source': row[n1], 'target': row[n2], 'label': row[l2],
                                      'color': row[kr.column_name_map[self.edge_color_column]] if not pd.isna(
                                          row[kr.column_name_map[self.edge_color_column]]) and str(
                                          row[kr.column_name_map[
                                              self.edge_color_column]]) != '' else self.edge_color_default,
                                      'width_orig': width_orig})
                    elif self.edge_color_style == 'gradient':
                        edges.append({'source': row[n1], 'target': row[n2], 'label': row[l2],
                                      'color': row[kr.column_name_map[self.edge_color_column]] if not pd.isna(
                                          row[kr.column_name_map[self.edge_color_column]]) and str(
                                          row[kr.column_name_map[self.edge_color_column]]) != '' else -1,
                                      'width_orig': width_orig})
                    else:
                        if row[kr.column_name_map[self.edge_color_column]] not in color_set:
                            color_set[row[kr.column_name_map[self.edge_color_column]]] = count
                            count += 1
                        edges.append({'source': row[n1], 'target': row[n2], 'label': row[l2],
                                      'color': min(color_set[row[kr.column_name_map[self.edge_color_column]]],
                                                   9) if not pd.isna(
                                          row[kr.column_name_map[self.edge_color_column]]) else self.edge_color_default,
                                      'width_orig': width_orig})
                elif self.edge_color_column is None and '@' in row[l2]:
                    edges.append({'source': row[n1], 'target': row[n2], 'label': row[l2][1:row[l2].find(
                        '@') - 1], 'width_orig': width_orig})
                else:
                    edges.append(
                        {'source': row[n1], 'target': row[n2], 'label': row[l2], 'width_orig': width_orig})

            arr = []
            if self.edge_width_mapping == 'fixed':
                for edge in edges:
                    if pd.isna(edge['width_orig']) or str(edge['width_orig']) == '':
                        edge['width'] = self.edge_width_default
                        continue
                    if edge['width_orig'] >= 0:
                        edge['width'] = edge['width_orig']
                    else:
                        edge['width'] = self.edge_width_default
            elif self.edge_width_scale == 'linear':
                for edge in edges:
                    if pd.isna(edge['width_orig']) or str(edge['width_orig']) == '':
                        edge['width'] = self.edge_width_default
                        continue
                    if edge['width_orig'] >= 0:
                        arr.append(edge['width_orig'])
                for edge in edges:
                    if pd.isna(edge['width_orig']) or str(edge['width_orig']) == '':
                        edge['width'] = self.edge_width_default
                        continue
                    if edge['width_orig'] >= 0:
                        edge['width'] = self.edge_width_minimum + (edge['width_orig'] - min(arr)) * (
                                self.edge_width_maximum - self.edge_width_minimum) / (max(arr) - min(arr))
                    else:
                        edge['width'] = self.edge_width_default
            elif self.edge_width_scale == 'log':
                for edge in edges:
                    if pd.isna(edge['width_orig']) or str(edge['width_orig']) == '':
                        edge['width'] = self.edge_width_default
                        continue
                    if edge['width_orig'] >= 0:
                        arr.append(edge['width_orig'])
                for edge in edges:
                    if pd.isna(edge['width_orig']) or str(edge['width_orig']) == '':
                        edge['width'] = self.edge_width_default
                        continue
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
            color_set = {}
            count = 0

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
                        if not pd.isna(row[kr_node.column_name_map[self.node_color_column]]) and str(
                                row[kr_node.column_name_map[self.node_color_column]]) != '':
                            node_color_list.append(
                                float(row[kr_node.column_name_map[self.node_color_column]]))
                    if self.node_size_scale == 'linear' or self.node_size_scale == 'log':
                        if not pd.isna(row[kr_node.column_name_map[self.node_size_column]]) and str(
                                row[kr_node.column_name_map[self.node_size_column]]) != '':
                            node_size_list.append(
                                float(row[kr_node.column_name_map[self.node_size_column]]))

                kr_node.close()

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
                    temp = {'id': row[kr_node.column_name_map[self.node_file_id]]}

                    if 'label' not in kr_node.column_name_map:
                        temp['label'] = row[kr_node.column_name_map[self.node_file_id]]
                    elif '@' in str(row[kr_node.column_name_map['label']]):
                        temp['label'] = row[kr_node.column_name_map['label']][
                                        1:row[kr_node.column_name_map['label']].find('@') - 1]
                    elif pd.isna(row[kr_node.column_name_map['label']]) \
                            or str(row[kr_node.column_name_map['label']]).lower() == 'nan' \
                            or str(row[kr_node.column_name_map['label']]).lower() == '':
                        temp['label'] = row[kr_node.column_name_map[self.node_file_id]]
                    else:
                        temp['label'] = row[kr_node.column_name_map['label']]

                    if self.tooltip_column is not None:
                        if (not pd.isna(row[kr_node.column_name_map[self.tooltip_column]])) and str(
                                row[kr_node.column_name_map[self.tooltip_column]]) != '':
                            temp['tooltip'] = str(
                                row[kr_node.column_name_map[self.tooltip_column]])
                        else:
                            temp['tooltip'] = str(
                                row[kr_node.column_name_map[self.node_file_id]])
                    else:
                        temp['tooltip'] = temp['label']

                    if self.node_color_column is not None:
                        if self.node_color_mapping == 'fixed':
                            if pd.isna(row[kr_node.column_name_map[self.node_color_column]]) or str(
                                    row[kr_node.column_name_map[self.node_color_column]]) == '':
                                temp['color'] = self.node_color_default
                            else:
                                temp['color'] = row[kr_node.column_name_map[self.node_color_column]]
                        else:
                            if self.node_color_style == 'gradient':
                                if self.node_color_scale == 'linear':
                                    node_color = 1
                                    temp['color'] = (float(row[kr_node.column_name_map[self.node_color_column]]) -
                                                     min(node_color_list)) / (max(node_color_list)
                                                                              - min(node_color_list)) \
                                        if not pd.isna(row[kr_node.column_name_map[self.node_color_column]]) \
                                           or str(row[kr_node.column_name_map[self.node_color_column]]) == '' \
                                        else self.node_color_default
                                elif self.node_color_scale == 'log':
                                    node_color = 1
                                    node_color_min = min(node_color_list)
                                    node_color_max = max(node_color_list)
                                    if node_color_min == 0:
                                        log_min = -1
                                    else:
                                        log_min = math.log(
                                            node_color_min, base)

                                    if node_color_max == 0:
                                        log_max = -1
                                    else:
                                        log_max = math.log(
                                            node_color_max, base)

                                    if float(row[kr_node.column_name_map[self.node_color_column]]) == 0:
                                        log_cur = -1
                                    else:
                                        log_cur = math.log(float(row[kr_node.column_name_map[self.node_color_column]]),
                                                           base)

                                    if log_max == log_min:
                                        temp['color'] = self.node_color_default
                                    else:
                                        color_value\
                                            = 0 + (log_cur - log_min) * (1 - 0) / (log_max - log_min)
                                        temp['color'] = float(color_value) if not pd.isna(
                                            row[kr_node.column_name_map[
                                                self.node_color_column]]) else self.node_color_default
                                else:
                                    temp['color'] = row[kr_node.column_name_map[self.node_color_column]] if not pd.isna(
                                        row[kr_node.column_name_map[
                                            self.node_color_column]]) else self.node_color_default
                            else:
                                node_color = 2
                                if row[kr_node.column_name_map[self.node_color_column]] not in node_color_map \
                                        and len(node_color_map) < 10:
                                    node_color_map[row[kr_node.column_name_map[self.node_color_column]]] \
                                        = len(node_color_map)

                                # temp['color'] = min(color_set[row[kr_node.column_name_map[self.node_color_column]]],
                                #                     9) if not pd.isna(
                                #     row[kr_node.column_name_map[self.node_color_column]]) else self.node_color_default
                                # TODO this is a hack for now to get fix colors for few and many subclasses node,
                                # TODO these are the only 2 options in the node graph, we'll fix it properly
                                temp['color'] = node_color_map.get(row[kr_node.column_name_map[self.node_color_column]],
                                                                   self.node_color_default)
                    if self.node_size_column is not None:
                        if self.node_size_mapping == 'fixed':
                            temp['size'] = row[kr_node.column_name_map[self.node_size_column]] if not pd.isna(
                                row[kr_node.column_name_map[self.node_size_column]]) else self.node_size_default

                        if pd.isna(row[kr_node.column_name_map[self.node_size_column]]) or str(
                                row[kr_node.column_name_map[self.node_size_column]]) == '':
                            temp['size'] = self.node_size_default
                        else:
                            if self.node_size_scale == 'linear':
                                size_value = self.node_size_minimum + (
                                        float(row[kr_node.column_name_map[self.node_size_column]]) -
                                        min(node_size_list)) * (
                                        self.node_size_maximum - self.node_size_minimum) / (
                                        max(node_size_list) - min(node_size_list))
                                temp['size'] = float(size_value) if not pd.isna(
                                    row[kr_node.column_name_map[self.node_size_column]]) else self.node_size_default
                            elif self.node_size_scale == 'log':
                                if min(node_size_list) == 0:
                                    log_min = -1
                                else:
                                    log_min = math.log(min(node_size_list), base)

                                if max(node_size_list) == 0:
                                    log_max = -1
                                else:
                                    log_max = math.log(max(node_size_list), base)

                                if float(row[kr_node.column_name_map[self.node_size_column]]) == 0:
                                    log_cur = -1
                                else:
                                    log_cur = math.log(
                                        float(row[kr_node.column_name_map[self.node_size_column]]), base)

                                if log_max == log_min:
                                    temp['size'] = self.node_size_default
                                else:
                                    size_value = self.node_size_minimum + (log_cur - log_min) * (
                                            self.node_size_maximum - self.node_size_minimum) / (log_max - log_min)
                                    temp['size'] = size_value if not pd.isna(
                                        row[kr_node.column_name_map[self.node_size_column]]) else self.node_size_default

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
        return d, node_color

    def to_html(self, d, node_color):
        output_kgtk_file: Path = KGTKArgumentParser.get_output_file(self.output_file)
        f = open(output_kgtk_file, 'w')
        f.write('''<head>
    <style> body { margin: 0; } </style>
    <script src="https://cdn.jsdelivr.net/npm/d3-color@3"></script>
    <script src="https://cdn.jsdelivr.net/npm/d3-interpolate@3"></script>
    <script src="https://cdn.jsdelivr.net/npm/d3-scale-chromatic@3"></script>
    <script src="https://unpkg.com/force-graph"></script>
    <!--<script src="../../dist/force-graph.js"></script>-->
    </head>
    <body>
    <div id="graph"></div>
    <script>
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
        .nodeColor((node) => node.color[0] == "#" ? node.color : {self.node_categorical_scale}[node.color])
        .linkWidth((link) => link.width)''')
            node_text_format = self.node_categorical_scale + '[node.color]'
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
