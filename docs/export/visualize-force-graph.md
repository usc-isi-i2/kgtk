This command loads a TSV edges file into html visualization of graph
## Usage
```
optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK input file. (May be omitted or '-' for
                        stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for
                        stdout.)
  --node-file NODE_FILE
                        Specify the location of node file.
  --direction DIRECTION
                        Specify direction (arrow, particle and None), default
                        none
  --show-edge-label EDGE_LABEL
                        Specify direction (arrow, particle and None), default
                        none
  --edge-color-column EDGE_COLOR_COLUMN
                        Specify column used for edge color
  --edge-color-style EDGE_COLOR_STYLE
                        Specify style (categorical, gradient) used for edge
                        color
  --edge-color-mapping EDGE_COLOR_MAPPING
                        Specify mapping (auto, fixed) used for edge color
  --edge-color-default EDGE_COLOR_DEFAULT
                        Specify default color for edge
  --edge-width-column EDGE_WIDTH_COLUMN
                        Specify column used for edge width
  --edge-width-minimum EDGE_WIDTH_MINIMUM
                        Specify edge width minimum
  --edge-width-maximum EDGE_WIDTH_MAXIMUM
                        Specify edge width maximum
  --edge-width-mapping EDGE_WIDTH_MAPPING
                        Specify mapping (auto, fixed) used for edge width
  --edge-width-default EDGE_WIDTH_DEFAULT
                        Specify default width for edge
  --edge-width-scale EDGE_WIDTH_SCALE
                        Specify scale for width for edge (linear, log)
  --node-color-column NODE_COLOR_COLUMN
                        Specify column used for node color
  --node-color-style NODE_COLOR_STYLE
                        Specify style (categorical, gradient) used for node
                        color
  --node-color-mapping NODE_COLOR_MAPPING
                        Specify mapping (auto, fixed) used for node color
  --node-color-default NODE_COLOR_DEFAULT
                        Specify default color for node
  --node-color-scale NODE_COLOR_SCALE
                        Specify node color scale (linear/log)
  --node-size-column NODE_SIZE_COLUMN
                        Specify column used for node size
  --node-size-minimum NODE_SIZE_MINIMUM
                        Specify node size minimum
  --node-size-maximum NODE_SIZE_MAXIMUM
                        Specify node size maximum
  --node-size-mapping NODE_SIZE_MAPPING
                        Specify mapping (auto, fixed) used for node size
  --node-size-default NODE_SIZE_DEFAULT
                        Specify default size for node
  --node-size-scale NODE_SIZE_SCALE
                        Specify scale for node size (linear, log)
  --node-file-id NODE_FILE_ID
                        Specify id column name in node file, default is id
  --show-text SHOW_TEXT
                        When node number is greater than this number, will not
                        show text as label, default is 500
  --node-border-color NODE_BORDER_COLOR
                        Specify node border color
  --tooltip-column TOOLTIP_COLUMN
                        Specify option to show tooltip
  --text-node TEXT_NODE
                        Specify option to show text (false, center, above)
  --node-categorical-scale NODE_CATEGORICAL_SCALE
                        Specify color categorical scale for node from
                        d3-scale-chromatic
  --edge-categorical-scale EDGE_CATEGORICAL_SCALE
                        Specify color categorical scale for edge d3-scale-
                        chromatic
  --node-gradient-scale NODE_GRADIENT_SCALE
                        Specify color gradient scale for node from d3-scale-
                        chromatic
  --edge-gradient-scale EDGE_GRADIENT_SCALE
                        Specify color gradient scale for edge d3-scale-
                        chromatic
```



Edge File contains:
- `node1`: the subject column (source node)
- `label`: the predicate column (property name)
- `node2`: the object column (target node)

    
Optional:
- `node1;label`: the subject label (source node)
- `label;label`: the predicate label (property name)
- `node2;label`: the object label (target node)
 
Node File contains:
- `id`: id of the node. Default is 'id' col, but can be configured through --node-file-id option.

Optional:
- `label`: the node label
- `x`: x_coordinate of node
- `y`: y_coordinate of node

## Examples

## 1. Default
```
kgtk visualize-force-graph -i example.tsv -o default.html
```
<img src="https://github.com/GrantXie/kgtk/tree/dev_1/docs/images/visualize-force-graph-examples/1_default.jpg" width="150"/>

