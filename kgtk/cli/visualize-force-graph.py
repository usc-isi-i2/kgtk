"""Convert edge file to html visualization
"""
import pandas as pd
import json
from argparse import Namespace, SUPPRESS

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
                        default="None",
                        help="Specify the location of node file.")

    parser.add_argument('--direction', dest='direction', type=str,
                        default="None",
                        help="Specify direction (arrow, particle and None), default none")

    parser.add_argument('--show-edge-label', dest='edge_label', type=bool,
                        default=False,
                        help="Specify direction (arrow, particle and None), default none")



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
        node_file: str = "None",
        direction: str = "None",
        edge_label: bool = False,

        **kwargs  # Whatever KgtkFileOptions and KgtkValueOptions want.
        ) -> int:
    # import modules locally
    from pathlib import Path
    import sys
    import typing

    from kgtk.exceptions import KGTKException
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
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

        number = False
        l1 = kr.column_name_map['node1;label']
        l2 = kr.column_name_map['label;label']
        l3 = kr.column_name_map['node2;label']

        color_d = {}
        color_count = 0
        flag = 0
        for row in kr:
            if 'thickness' in kr.column_name_map:
                width = float(row[kr.column_name_map['node2;label'][thickness]])
            else:
                width = 1
            if 'color' in kr.column_name_map and '@' in row[l1]:
                nodes.add(row[l1][1:row[l1].find('@')-1])
                nodes.add(row[l3][1:row[l3].find('@')-1])
                if '#' in row[kr.column_name_map['color']]:
                    h = row[kr.column_name_map['color']].lstrip('#')
                    s = str(tuple(int(h[i:i+2], 16) for i in (0, 2, 4)))
                    s1 = 'rgba(' + s[1:-1]  + ', '+ str(thickness) +')'
                    edges.append({'source': row[l1][1:row[l1].find('@')-1], 'target': row[l3][1:row[l3].find('@')-1], 'label': row[l2][1:row[l2].find('@')-1], 'color': tuple(int(h[i:i+2], 16) for i in (0, 2, 4)), 'color_s' : s1, 'width': width})
                elif row[kr.column_name_map['color']].replace('.', '').isdigit():
                    flag = 1
                    number = True
                    edges.append({'source': row[l1][1:row[l1].find('@')-1], 'target': row[l3][1:row[l3].find('@')-1], 'label': row[l2][1:row[l2].find('@')-1], 'color': row[kr.column_name_map['color']], 'width': width})
                else:
                    flag = 2
                    number = True
                    if row[kr.column_name_map['color']] not in color_set:
                         color_set[row[kr.column_name_map['color']]] = count
                         count += 1
                    edges.append({'source': row[l1][1:row[l1].find('@')-1], 'target': row[l3][1:row[l3].find('@')-1], 'label': row[l2][1:row[l2].find('@')-1], 'color': min(color_set[row[kr.column_name_map['color']]], 9), 'width': width})
            else:
                nodes.add(row[l1])
                nodes.add(row[l3])
                edges.append({'source': row[l1], 'target': row[l3], 'label': row[l2], 'width': width})
     

        d['nodes'] = []
        d['links'] = edges

        print(node_file)



        if 'None' in node_file:
            for ele in nodes:
                d['nodes'].append({'id': ele})
        elif '.tsv' in node_file:
            df = pd.read_csv(node_file, sep = '\t')
            for i in range(0, len(df)):
                if 'x' in df.columns:
                    h = df['color'][i].lstrip('#')
                    s = 'rgba' + str(tuple(int(h[i:i+2], 16) for i in (0, 2, 4)))
                    d['nodes'].append({'id': df['node;label'][i][1:df['node;label'][i].find('@')-1], 'color': s, 'fx': float(df['x'][i]) *50, 'fy': float(df['y'][i]) *50})
                else:
                    h = df['color'][i].lstrip('#')
                    s = 'rgba' + str(tuple(int(h[i:i+2], 16) for i in (0, 2, 4)))
                    d['nodes'].append({'id': df['node;label'][i], 'color': s})
        else:
            df = pd.read_csv(node_file)
            for i in range(0, len(df)):
                if 'x' in df.columns:
                    h = df['color'][i].lstrip('#')
                    s = 'rgba' + str(tuple(int(h[i:i+2], 16) for i in (0, 2, 4)))
                    d['nodes'].append({'id': df['node;label'][i][1:df['node;label'][i].find('@')-1], 'color': s, 'fx': float(df['x'][i]) *50, 'fy': float(df['y'][i]) *50})
                else:
                    h = df['color'][i].lstrip('#')
                    s = 'rgba' + str(tuple(int(h[i:i+2], 16) for i in (0, 2, 4)))
                    d['nodes'].append({'id': df['node;label'][i], 'color': s})
        

        f = open(output_kgtk_file, 'w')
        if not number:
            f.write('''<head>
  <style> body { margin: 0; } </style>

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
        .nodeLabel('id')
        .nodeAutoColorBy('group')
        .linkWidth((link) => link.width)''')

            if direction == 'arrow':
                f.write('''
	        .linkDirectionalArrowLength(6)
	        .linkDirectionalArrowRelPos(1)''')
            elif direction == 'particle':
                f.write('''      .linkDirectionalParticles(2)
	      ''')

            if edge_label:
                f.write('''        .linkColor((link) => link.color_s)
                        .linkCanvasObjectMode(() => 'after')
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
  </script>
</body>''')
            else:
                f.write('''  </script>
</body>''')
        else:
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
        .nodeLabel('id')
        .nodeAutoColorBy('group')
        .linkWidth((link) => link.width)''')

            if direction == 'arrow':
                f.write('''
	        .linkDirectionalArrowLength(6)
	        .linkDirectionalArrowRelPos(1)''')
            elif direction == 'particle':
                f.write('''      .linkDirectionalParticles(2)
	      ''')

            if flag == 1:
                f.write('''        .linkColor((link) => d3.interpolateYlGn(link.color))''')
            else:
                f.write('''        .linkColor((link) =>  d3.schemeCategory10[link.color])''')


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
  </script>
</body>''')
            
            else:
                f.write('''  </script>
</body>''')
        kr.close()
        return 0

    except SystemExit as e:
        raise KGTKException("Exit requested")
    except Exception as e:
        raise KGTKException(str(e))
