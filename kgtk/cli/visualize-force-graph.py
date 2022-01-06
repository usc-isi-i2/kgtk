"""Convert edge file and optional node file to html visualization
"""
import pandas as pd
import json
from argparse import Namespace, SUPPRESS
import sys

import math

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles


def parser():
    return {
        'help': 'Convert edge file to html visualization',
        'description': 'Convert edge file (optional node file) to html graph visualization file' 
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
    def h(msg: str) -> str:
        if _expert:
            return msg
        else:
            return SUPPRESS

    parser.add_input_file(positional=True)
    parser.add_output_file()

    parser.add_argument('--node-file', dest='node_file', type=str,
                        default=None,
                        help="Specify the location of node file.")

    parser.add_argument('--direction', dest='direction', type=str,
                        default=None,
                        help="Specify direction (arrow, particle and None), default none")

    parser.add_argument('--show-edge-label', dest='edge_label', type=bool,
                        default=False,
                        help="Specify direction (arrow, particle and None), default none")

    parser.add_argument('--edge-color-column', dest='edge_color_column', type=str,
                        default=None,
                        help="Specify column used for edge color")

    parser.add_argument('--edge-color-style', dest='edge_color_style', type=str,
                        default=None,
                        help="Specify style (categorical, gradient) used for edge color")

    parser.add_argument('--edge-color-mapping', dest='edge_color_mapping', type=str,
                        default=None,
                        help="Specify mapping (auto, fixed) used for edge color")

    parser.add_argument('--edge-color-default', dest='edge_color_default', type=str,
                        default=None,
                        help="Specify default color for edge")

    parser.add_argument('--edge-width-column', dest='edge_width_column', type=str,
                        default=None,
                        help="Specify column used for edge width")

    parser.add_argument('--edge-width-minimum', dest='edge_width_minimum', type=float,
                        default=1.0,
                        help="Specify edge width minimum")

    parser.add_argument('--edge-width-maximum', dest='edge_width_maximum', type=float,
                        default=5.0,
                        help="Specify edge width maximum")


    parser.add_argument('--edge-width-mapping', dest='edge_width_mapping', type=str,
                        default=None,
                        help="Specify mapping (auto, fixed) used for edge width")

    parser.add_argument('--edge-width-default', dest='edge_width_default', type=float,
                        default=1.0,
                        help="Specify default width for edge")

    parser.add_argument('--edge-width-scale', dest='edge_width_scale', type=str,
                        default=None,
                        help="Specify scale for width for edge (linear, log)")


    parser.add_argument('--node-color-column', dest='node_color_column', type=str,
                        default=None,
                        help="Specify column used for node color")

    parser.add_argument('--node-color-style', dest='node_color_style', type=str,
                        default=None,
                        help="Specify style (categorical, gradient) used for node color")

    parser.add_argument('--node-color-mapping', dest='node_color_mapping', type=str,
                        default=None,
                        help="Specify mapping (auto, fixed) used for node color")

    parser.add_argument('--node-color-default', dest='node_color_default', type=str,
                        default=None,
                        help="Specify default color for node")

    parser.add_argument('--node-color-scale', dest='node_color_scale', type=str,
                        default=None,
                        help="Specify node color scale (linear/log)")


    parser.add_argument('--node-size-column', dest='node_size_column', type=str,
                        default=None,
                        help="Specify column used for node size")

    parser.add_argument('--node-size-minimum', dest='node_size_minimum', type=float,
                        default=1.0,
                        help="Specify node size minimum")

    parser.add_argument('--node-size-maximum', dest='node_size_maximum', type=float,
                        default=5.0,
                        help="Specify node size maximum")


    parser.add_argument('--node-size-mapping', dest='node_size_mapping', type=str,
                        default=None,
                        help="Specify mapping (auto, fixed) used for node size")

    parser.add_argument('--node-size-default', dest='node_size_default', type=float,
                        default=2.0,
                        help="Specify default size for node")

    parser.add_argument('--node-size-scale', dest='node_size_scale', type=str,
                        default=None,
                        help="Specify scale for node size (linear, log)")


    parser.add_argument('--node-file-id', dest='node_file_id', type=str,
                        default='id',
                        help="Specify id column name in node file, default is id")

    parser.add_argument('--show-text', dest='show_text', type=int,
                        default=500,
                        help="When node number is greater than this number, will not show text as label, default is 500")

    parser.add_argument('--node-border-color', dest='node_border_color', type=str,
                        default=None,
                        help="Specify node border color ")

    parser.add_argument('--tooltip-column', dest='tooltip_column', type=str,
                        default=None,
                        help="Specify option to show tooltip ")

    parser.add_argument('--text-node', dest='text_node', type=str,
                        default='false',
                        help="Specify option to show text (false, center, above) ")


    parser.add_argument('--node-categorical-scale', dest='node_categorical_scale', type=str,
                        default='d3.schemeCategory10',
                        help="Specify color categorical scale for node from d3-scale-chromatic")

    parser.add_argument('--edge-categorical-scale', dest='edge_categorical_scale', type=str,
                        default='d3.schemeCategory10',
                        help="Specify color categorical scale for edge d3-scale-chromatic")

    parser.add_argument('--node-gradient-scale', dest='node_gradient_scale', type=str,
                        default='d3.interpolateRdBu',
                        help="Specify color gradient scale for node from d3-scale-chromatic")

    parser.add_argument('--edge-gradient-scale', dest='edge_gradient_scale', type=str,
                        default='d3.interpolateRdBu',
                        help="Specify color gradient scale for edge d3-scale-chromatic")



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
        show_text: int = 250,
        node_border_color: str = None,
        tooltip_column: str = None,
        text_node: str = None,
        node_categorical_scale: str = 'd3.schemeCategory10',
        edge_categorical_scale: str = 'd3.schemeCategory10',
        node_gradient_scale: str = 'd3.interpolateRdBu',
        edge_gradient_scale: str = 'd3.interpolateRdBu',

        **kwargs  # Whatever KgtkFileOptions and KgtkValueOptions want. 
        ) -> int:
    # import modules locally
    from pathlib import Path
    import sys
    import typing

    from kgtk.exceptions import KGTKException
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions, KgtkReaderMode
    from kgtk.io.kgtkwriter import KgtkWriter
    from kgtk.reshape.kgtkidbuilder import KgtkIdBuilder, KgtkIdBuilderOptions
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    input_kgtk_file: Path = KGTKArgumentParser.get_input_file(input_file)
    output_kgtk_file: Path = KGTKArgumentParser.get_output_file(output_file)

    # Select where to send error messages, defaulting to stderr.
    error_file: typing.TextIO = sys.stdout if errors_to_stdout else sys.stderr

    # Build the option structures.
    idbuilder_options: KgtkIdBuilderOptions =\
    KgtkIdBuilderOptions.from_dict(kwargs)
    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs)
    value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)

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
                                          verbose=verbose,
                                          very_verbose=very_verbose,
        )


        d = {}
        nodes = set()
        edges = []
        base = math.e


        if node_size_minimum == 0.0:
            node_size_minimum = 0.01

        if edge_width_minimum == 0:
            edge_width_minimum = 0.01

        if 'node1' not in kr.column_name_map:
          print('No node1 col in edge file', file=sys.stderr, flush=True)
        if 'node2' not in kr.column_name_map:
          print('No node2 col in edge file', file=sys.stderr, flush=True)


        if 'node1;label' in kr.column_name_map and node_file != None:
          print('node1;label in edge file will not be read due to the existence of node file', file=sys.stderr, flush=True)

        if 'node2;label' in kr.column_name_map and node_file != None:
          print('node2;label in edge file will not be read due to the existence of node file', file=sys.stderr, flush=True)

        n1 = kr.column_name_map['node1']
        n2 = kr.column_name_map['node2']

        if node_file == None and 'node1;label' in kr.column_name_map:
          l1 = kr.column_name_map['node1;label']


        if node_file == None and 'node1;label' in kr.column_name_map:
          l3 = kr.column_name_map['node2;label']

        if node_file == None and 'node1;label' in kr.column_name_map:
          l2 = kr.column_name_map['label;label']

        if 'node1;label' not in kr.column_name_map and node_file == None:
          print('node1;label not in edge file', file=sys.stderr, flush=True)
          l1 = kr.column_name_map['node1']

        if 'node2;label' not in kr.column_name_map and node_file == None:
          print('node2;label not in edge file', file=sys.stderr, flush=True)
          l3 = kr.column_name_map['node2']

        if 'label;label' not in kr.column_name_map:
          print('No label;label col in edge file', file=sys.stderr, flush=True)
          l2 = kr.column_name_map['label']
        else:
          l2 = kr.column_name_map['label;label']

        color_d = {}
        count = 0
        color_set = {}

        for row in kr:
          if node_file == None:
            if '@' in row[l1]:
              nodes.add((row[n1], row[l1][1:row[l1].find('@')-1])) 
            else:
              nodes.add((row[n1], row[l1]))

            if '@' in row[l3]:
              nodes.add((row[n2], row[l3][1:row[l3].find('@')-1])) 
            else:
              nodes.add((row[n2], row[l3]))  


          if edge_width_column != None:
              if (not pd.isna(row[kr.column_name_map[edge_width_column]])) and str(row[kr.column_name_map[edge_width_column]]) != '':
                width_orig = float(row[kr.column_name_map[edge_width_column]]) 
              else:
                width_orig =-1.0
          else:
              width_orig = 1
          


          if edge_color_column != None and '@' in row[l2]:
              if edge_color_mapping == 'fixed':
                  edges.append({'source': row[n1], 'target': row[n2], 'label': row[l2][1:row[l2].find('@')-1], 'color': row[kr.column_name_map[edge_color_column]] if not pd.isna(row[kr.column_name_map[edge_color_column]]) or str(row[kr.column_name_map[edge_color_column]]) != '' else edge_color_default, 'width_orig': width_orig})
              elif edge_color_style == 'gradient':
                  edges.append({'source': row[n1], 'target': row[n2], 'label': row[l2][1:row[l2].find('@')-1], 'color': row[kr.column_name_map[edge_color_column]] if not pd.isna(row[kr.column_name_map[edge_color_column]]) or str(row[kr.column_name_map[edge_color_column]]) else edge_color_default, 'width_orig': width_orig})
              else:
                  if row[kr.column_name_map[edge_color_column]] not in color_set:
                       color_set[row[kr.column_name_map[edge_color_column]]] = count
                       count += 1
                  edges.append({'source': row[n1], 'target': row[n2], 'label': row[l2][1:row[l2].find('@')-1], 'color': min(color_set[row[kr.column_name_map[edge_color_column]]], 9) if not pd.isna(row[kr.column_name_map[edge_color_column]]) or str(row[kr.column_name_map[edge_color_column]]) else edge_color_default,  'width_orig': width_orig})
          elif edge_color_column != None and '@' not in row[l2]:
              if edge_color_style == 'fixed':
                  edges.append({'source': row[n1], 'target': row[n2], 'label': row[l2], 'color': row[kr.column_name_map[edge_color_column]] if not pd.isna(row[kr.column_name_map[edge_color_column]]) or str(row[kr.column_name_map[edge_color_column]]) != '' else edge_color_default, 'width_orig': width_orig})
              elif edge_color_style == 'gradient':
                  edges.append({'source': row[n1], 'target': row[n2], 'label': row[l2], 'color': row[kr.column_name_map[edge_color_column]] if not pd.isna(row[kr.column_name_map[edge_color_column]]) or str(row[kr.column_name_map[edge_color_column]]) != '' else edge_color_default, 'width_orig': width_orig})
              else:
                  if row[kr.column_name_map[edge_color_column]] not in color_set:
                       color_set[row[kr.column_name_map[edge_color_column]]] = count
                       count += 1
                  edges.append({'source': row[n1], 'target': row[n2], 'label': row[l2], 'color': min(color_set[row[kr.column_name_map[edge_color_column]]], 9) if not pd.isna(row[kr.column_name_map[edge_color_column]]) else edge_color_default, 'width_orig': width_orig})
          elif edge_color_column == None and '@' in row[l2]:
              edges.append({'source': row[n1], 'target': row[n2], 'label': row[l2][1:row[l2].find('@')-1], 'width_orig': width_orig})
          else:
              edges.append({'source': row[n1], 'target': row[n2], 'label': row[l2], 'width_orig': width_orig})


        if edge_width_mapping == 'fixed':
          for edge in edges:
            if pd.isna(edge['width_orig']) or str(edge['width_orig']) == '':
              edge['width'] = edge_width_default
              continue
            if edge['width_orig'] >= 0:
              edge['width'] = edge['width_orig']
            else:
              edge['width'] = edge_width_default
        elif edge_width_scale == 'linear':          
          arr = []
          for edge in edges:
            if pd.isna(edge['width_orig']) or str(edge['width_orig']) == '':
              edge['width'] = edge_width_default
              continue
            if edge['width_orig'] >= 0:
              arr.append(edge['width_orig'])
          for edge in edges:
            if pd.isna(edge['width_orig']) or str(edge['width_orig']) == '':
              edge['width'] = edge_width_default
              continue
            if edge['width_orig'] >= 0:
              edge['width'] = edge_width_minimum + (edge['width_orig'] - min(arr)) * (edge_width_maximum - edge_width_minimum) / (max(arr) - min(arr))
            else:
              edge['width'] = edge_width_default
        elif edge_width_scale == 'log':
          arr = []
          for edge in edges:
            if pd.isna(edge['width_orig']) or str(edge['width_orig']) == '':
              edge['width'] = edge_width_default
              continue
            if edge['width_orig'] >= 0:
              arr.append(edge['width_orig'])
          for edge in edges:
            if pd.isna(edge['width_orig']) or str(edge['width_orig']) == '':
              edge['width'] = edge_width_default
              continue
            if edge['width_orig'] >= 0:
              if min(arr) == 0:
                log_min = 0
              else:
                log_min = math.log(min(arr), base)

              if max(arr) == 0:
                log_max = 0
              else:
                log_max = math.log(max(arr), base)

              if edge['width_orig'] == 0:
                log_cur = 0
              else:
                log_cur = math.log(edge['width_orig'], base)

              edge['width'] = edge_width_minimum + (log_cur - log_min) * (edge_width_maximum - edge_width_minimum) / (log_max - log_min)
            else:
              edge['width'] = edge_width_default


        if node_file == None:
            d['nodes'] = []
            for ele in nodes:
                d['nodes'].append({'id': ele[0], 'label': ele[1], 'tooltip': ele[1]})
        else:
            d['nodes'] = []

        d['links'] = edges
        color_set = {}
        count = 0

        node_color = 0


        if node_file != None:
            kr_node: KgtkReader = KgtkReader.open(node_file,
                                              error_file=error_file,
                                              options=reader_options,
                                              value_options=value_options,
                                              verbose=verbose,
                                              very_verbose=very_verbose,
                                              mode = KgtkReaderMode.NONE,
            )

            
            node_color_list = []
            node_size_list = []

            for row in kr_node:
                if node_color_scale == 'linear' or node_color_scale == 'log':
                    if not pd.isna(row[kr_node.column_name_map[node_color_column]]) and str(row[kr_node.column_name_map[node_color_column]]) != '':
                        node_color_list.append(float(row[kr_node.column_name_map[node_color_column]]))
                if node_size_scale == 'linear' or node_size_scale == 'log':
                    if not pd.isna(row[kr_node.column_name_map[node_size_column]]) and str(row[kr_node.column_name_map[node_size_column]]) != '':
                        node_size_list.append(float(row[kr_node.column_name_map[node_size_column]]))

            kr_node.close()

            kr_node: KgtkReader = KgtkReader.open(node_file,
                                              error_file=error_file,
                                              options=reader_options,
                                              value_options=value_options,
                                              verbose=verbose,
                                              very_verbose=very_verbose,
                                              mode = KgtkReaderMode.NONE,
            )

            if 'id' not in kr_node.column_name_map:
                print('Missing id column in node file', file=sys.stderr, flush=True)
            if 'label' not in kr_node.column_name_map:
                print('Missing label column in node file', file=sys.stderr, flush=True)


            for row in kr_node:      
                  temp = {'id': row[kr_node.column_name_map[node_file_id]]}

                  if 'label' not in kr_node.column_name_map:
                    temp['label'] = row[kr_node.column_name_map[node_file_id]]
                  elif '@' in str(row[kr_node.column_name_map['label']]):
                    temp['label'] = row[kr_node.column_name_map['label']][1:row[kr_node.column_name_map['label']].find('@')-1]
                  elif pd.isna(row[kr_node.column_name_map['label']]) or str(row[kr_node.column_name_map['label']]).lower() == 'nan' or str(row[kr_node.column_name_map['label']]).lower() == '':
                    temp['label'] = row[kr_node.column_name_map[node_file_id]]
                  else:
                    temp['label'] = row[kr_node.column_name_map['label']]

                  if tooltip_column != None:
                    if (not pd.isna(row[kr_node.column_name_map[tooltip_column]])) and str(row[kr_node.column_name_map[tooltip_column]]) != '':
                      temp['tooltip'] = str(row[kr_node.column_name_map[tooltip_column]]) 
                    else:
                      temp['tooltip'] = str(row[kr_node.column_name_map[node_file_id]]) 
                  else:
                    temp['tooltip'] = temp['label']

                  if node_color_column != None:
                    if pd.isna(row[kr_node.column_name_map[node_color_column]]) or str(row[kr_node.column_name_map[node_color_column]]) == '':
                       temp['color'] = node_color_default
                    else: 
                        if node_color_style == 'gradient':
                          if node_color_scale == 'linear':
                              node_color = 1
                              color_value = (row[kr_node.column_name_map[node_color_column]] - min(node_color_list)) / (max(node_color_list) - min(node_color_list))
                              temp['color'] = float(color_value) if not pd.isna(row[kr_node.column_name_map[node_color_column]]) else node_color_default
                          elif node_color_scale == 'log':
                              node_color = 1
                              if min(node_color_list) == 0:
                                log_min = 0
                              else:
                                log_min = math.log(min(node_color_list), base)

                              if max(node_color_list)  == 0:
                                log_max = 0
                              else:
                                log_max = math.log(max(node_color_list), base)

                              if float(row[kr_node.column_name_map[node_color_column]]) == 0:
                                log_cur = 0
                              else:
                                log_cur = math.log(float(row[kr_node.column_name_map[node_color_column]]), base)

                              color_value = 0 + (log_cur - log_min) * (1 - 0) / (log_max - log_min)
                              temp['color'] = float(color_value) if not pd.isna(row[kr_node.column_name_map[node_color_column]]) else node_color_default
                          else:
                              temp['color'] = row[kr_node.column_name_map[node_color_column]] if not pd.isna(row[kr_node.column_name_map[node_color_column]]) else node_color_default
                        else:
                          node_color = 2
                          if row[kr_node.column_name_map[node_color_column]] not in color_set:
                            color_set[row[kr_node.column_name_map[node_color_column]]] = count
                            count += 1
                          temp['color'] = min(color_set[row[kr_node.column_name_map[node_color_column]]], 9) if not pd.isna(row[kr_node.column_name_map[node_color_column]]) else node_color_default

                  if node_size_column != None:
                      if node_size_mapping == 'fixed':
                          temp['size'] = row[kr_node.column_name_map[node_size_column]] if not pd.isna(row[kr_node.column_name_map[node_size_column]]) else node_size_default

                      if pd.isna(row[kr_node.column_name_map[node_size_column]]) or str(row[kr_node.column_name_map[node_size_column]]) == '':
                        temp['size'] = node_size_default
                      else:
                          if node_size_scale == 'linear':
                              node_size = 1
                              size_value = node_size_minimum + (row[kr_node.column_name_map[node_size_column]]-min(node_size_list)) * (node_size_maximum - node_size_minimum) / (max(node_size_list) - min(node_size_list))
                              temp['size'] = float(size_value) if not pd.isna(row[kr_node.column_name_map[node_size_column]]) else node_size_default
                          elif node_size_scale == 'log':
                              node_size = 1

                              if min(node_size_list) == 0:
                                log_min = 0
                              else:
                                log_min = math.log(min(node_size_list), base)

                              if max(node_size_list) == 0:
                                log_max = 0
                              else:
                                log_max = math.log(max(node_size_list), base) 

                              if float(row[kr_node.column_name_map[node_size_column]]) == 0:
                                log_cur = 0
                              else:
                                log_cur = math.log(float(row[kr_node.column_name_map[node_size_column]]), base)


                              size_value = node_size_minimum + (log_cur - log_min) * (node_size_maximum - node_size_minimum) / (log_max - log_min)
                              temp['size'] = (size_value) if not pd.isna(row[kr_node.column_name_map[node_size_column]]) else node_size_default

                  else:
                      temp['size'] = node_size_default

                  if 'x' in kr_node.column_name_map:
                     temp['fx'] = float(row[kr_node.column_name_map['x']])
                     temp['fy'] = float(row[kr_node.column_name_map['y']])
                  d['nodes'].append(temp)


                  
            kr_node.close()


        f = open(output_kgtk_file, 'w')
        

        f.write('''  </script>
</body>''')
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
        f.write(json.dumps(d, indent = 4))
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
    .nodeColor((node) => node.color[0] == "#" ? node.color : {node_gradient_scale}(node.color))
    .linkWidth((link) => link.width)''')
          node_text_format = node_gradient_scale + '(node.color)'
        else:
          f.write(f'''
    .nodeColor((node) => node.color[0] == "#" ? node.color : {node_categorical_scale}[node.color])
    .linkWidth((link) => link.width)''')
          node_text_format = node_categorical_scale + '[node.color]'


        if node_border_color != None:
            node_text_format = "'" + node_border_color + "'"

        if direction == 'arrow':
            f.write('''
      .linkDirectionalArrowLength(6)
      .linkDirectionalArrowRelPos(1)''')
        elif direction == 'particle':
            f.write('''      .linkDirectionalParticles(2)
    ''')


        if edge_color_style == 'categorical':
            f.write(f'''        .linkColor((link) => link.color[0] == "#" ? link.color : {edge_categorical_scale}[link.color])''')
        elif edge_color_style == 'gradient':
            f.write(f'''        .linkColor((link) => link.color[0] == "#" ? link.color : {edge_gradient_scale}(node.color))''')
        else:
            f.write('''        .linkColor((link) => link.color)''')

        if edge_label:
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


        if text_node != 'false' and show_text > len(d['nodes']):

            if text_node == 'center':
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
          ctx.fillRect(node.x - bckgDimensions[0] / 2, node.y - {y_move} - bckgDimensions[1] / 2, ...bckgDimensions);

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
        kr.close()


        return 0

    except SystemExit as e:
        raise KGTKException("Exit requested")
    except Exception as e:
        raise KGTKException(str(e))
