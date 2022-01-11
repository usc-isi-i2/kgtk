"""Convert edge file to html visualization
"""
import json
import math
import pandas as pd
from argparse import Namespace, SUPPRESS

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles

from pathlib import Path

def parser():
    return {
        'help': 'Visualize API',
        'description': 'Use API to convert edge file to html visualization'
    }

def to_html(input_file: KGTKFiles,
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


        if node_size_minimum == 0.0 and node_size_scale == 'log':
            raise ValueError("node size cannot be 0 when using log scale")

        if edge_width_minimum == 0 and edge_width_scale == 'log':
            raise ValueError("edge width cannot be 0 when using log scale")

        n1 = kr.column_name_map['node1']
        n2 = kr.column_name_map['node2']

        if node_file == None and 'node1;label' in kr.column_name_map:
          l1 = kr.column_name_map['node1;label']


        if node_file == None and 'node1;label' in kr.column_name_map:
          l3 = kr.column_name_map['node2;label']

        if node_file == None and 'node1;label' in kr.column_name_map:
          l2 = kr.column_name_map['label;label']

        if 'node1;label' not in kr.column_name_map and node_file == None:
          l1 = kr.column_name_map['node1']

        if 'node2;label' not in kr.column_name_map and node_file == None:
          l3 = kr.column_name_map['node2']

        if 'label;label' not in kr.column_name_map:
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
                  edges.append({'source': row[n1], 'target': row[n2], 'label': row[l2][1:row[l2].find('@')-1], 'color': row[kr.column_name_map[edge_color_column]] if not pd.isna(row[kr.column_name_map[edge_color_column]]) and str(row[kr.column_name_map[edge_color_column]]) != '' else edge_color_default, 'width_orig': width_orig})
              elif edge_color_style == 'gradient':
                  edges.append({'source': row[n1], 'target': row[n2], 'label': row[l2][1:row[l2].find('@')-1], 'color': row[kr.column_name_map[edge_color_column]] if not pd.isna(row[kr.column_name_map[edge_color_column]]) and str(row[kr.column_name_map[edge_color_column]]) != '' else -1, 'width_orig': width_orig})
              else:
                  if row[kr.column_name_map[edge_color_column]] not in color_set:
                       color_set[row[kr.column_name_map[edge_color_column]]] = count
                       count += 1
                  edges.append({'source': row[n1], 'target': row[n2], 'label': row[l2][1:row[l2].find('@')-1], 'color': min(color_set[row[kr.column_name_map[edge_color_column]]], 9) if not pd.isna(row[kr.column_name_map[edge_color_column]]) or str(row[kr.column_name_map[edge_color_column]]) else edge_color_default,  'width_orig': width_orig})
          elif edge_color_column != None and '@' not in row[l2]:
              if edge_color_style == 'fixed':
                  edges.append({'source': row[n1], 'target': row[n2], 'label': row[l2], 'color': row[kr.column_name_map[edge_color_column]] if not pd.isna(row[kr.column_name_map[edge_color_column]]) and str(row[kr.column_name_map[edge_color_column]]) != '' else edge_color_default, 'width_orig': width_orig})
              elif edge_color_style == 'gradient':
                  edges.append({'source': row[n1], 'target': row[n2], 'label': row[l2], 'color': row[kr.column_name_map[edge_color_column]] if not pd.isna(row[kr.column_name_map[edge_color_column]]) and str(row[kr.column_name_map[edge_color_column]]) != '' else -1, 'width_orig': width_orig})
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


        if edge_color_column != None and edge_color_style == 'gradient':
          edge_color_list = []
          for edge in edges:
            if float(edge['color']) > 0:
              edge_color_list.append(float(edge['color']))  
          for edge in edges:
            if float(edge['color']) < 0:
              edge['color'] = edge_color_default
            else:
              edge['color'] = (float(edge['color']) - min(edge_color_list)) / (max(edge_color_list) - min(edge_color_list))


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

            if node_file_id not in kr_node.column_name_map:
                raise ValueError("no id column in node file")

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
                              temp['color'] = (float(row[kr_node.column_name_map[node_color_column]]) - min(node_color_list)) / (max(node_color_list) - min(node_color_list)) if not pd.isna(row[kr_node.column_name_map[node_color_column]]) else node_color_default
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
            f.write(f'''        .linkColor((link) => link.color[0] == "#" ? link.color : {edge_gradient_scale}(link.color))''')
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


        if text_node != 'false' and show_text_limit > len(d['nodes']):

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
        to_html(input_file = self.input_file,
                output_file = self.output_file,
                errors_to_stdout = self.errors_to_stdout,
                errors_to_stderr = self.errors_to_stderr,
                show_options = self.show_options,
                verbose = self.verbose,
                very_verbose = self.very_verbose,
                node_file = self.node_file,
                direction = self.direction,
                edge_label = self.edge_label,
                edge_color_column = self.edge_color_column,
                edge_color_style = self.edge_color_style,
                edge_color_mapping = self.edge_color_mapping,
                edge_color_default = self.edge_color_default,
                edge_width_column = self.edge_width_column,
                edge_width_mapping = self.edge_width_mapping,
                edge_width_default = self.edge_width_default,
                edge_width_minimum = self.edge_width_minimum,
                edge_width_maximum = self.edge_width_maximum,
                edge_width_scale = self.edge_width_scale,
                node_color_column = self.node_color_column,
                node_color_style = self.node_color_style,
                node_color_mapping = self.node_color_mapping,
                node_color_default = self.node_color_default,
                node_color_scale = self.node_color_scale,
                node_size_column = self.node_size_column,
                node_size_mapping = self.node_size_mapping,
                node_size_default = self.node_size_default,
                node_size_minimum = self.node_size_minimum,
                node_size_maximum = self.node_size_maximum,
                node_size_scale = self.node_size_scale,
                node_file_id = self.node_file_id,
                show_text_limit = self.show_text_limit,
                node_border_color = self.node_border_color,
                tooltip_column = self.tooltip_column,
                text_node = self.text_node,
                node_categorical_scale = self.node_categorical_scale,
                edge_categorical_scale = self.edge_categorical_scale,
                node_gradient_scale = self.node_gradient_scale,
                edge_gradient_scale = self.edge_gradient_scale)
