This command loads a TSV edges file into html visualization of graph
## Usage
```
usage: kgtk visualize-graph [-h] [-i INPUT_FILE] [-o OUTPUT_FILE]
                            [--node-file NODE_FILE] [--direction DIRECTION]
                            [--show-edge-label]
                            [--edge-color-column EDGE_COLOR_COLUMN]
                            [--edge-color-numbers] [--edge-color-hex]
                            [--edge-color-style EDGE_COLOR_STYLE]
                            [--edge-color-default EDGE_COLOR_DEFAULT]
                            [--edge-width-column EDGE_WIDTH_COLUMN]
                            [--edge-width-minimum EDGE_WIDTH_MINIMUM]
                            [--edge-width-maximum EDGE_WIDTH_MAXIMUM]
                            [--edge-width-default EDGE_WIDTH_DEFAULT]
                            [--edge-width-scale EDGE_WIDTH_SCALE]
                            [--node-color-column NODE_COLOR_COLUMN]
                            [--node-color-style NODE_COLOR_STYLE]
                            [--node-color-default NODE_COLOR_DEFAULT]
                            [--node-color-scale NODE_COLOR_SCALE]
                            [--node-color-numbers] [--node-color-hex]
                            [--node-size-column NODE_SIZE_COLUMN]
                            [--node-size-minimum NODE_SIZE_MINIMUM]
                            [--node-size-maximum NODE_SIZE_MAXIMUM]
                            [--node-size-default NODE_SIZE_DEFAULT]
                            [--node-size-scale NODE_SIZE_SCALE]
                            [--node-file-id NODE_FILE_ID]
                            [--show-text-limit SHOW_TEXT_LIMIT]
                            [--node-border-color NODE_BORDER_COLOR]
                            [--tooltip-column TOOLTIP_COLUMN]
                            [--show-text SHOW_TEXT]
                            [--node-categorical-scale NODE_CATEGORICAL_SCALE]
                            [--edge-categorical-scale EDGE_CATEGORICAL_SCALE]
                            [--node-gradient-scale NODE_GRADIENT_SCALE]
                            [--edge-gradient-scale EDGE_GRADIENT_SCALE]
                            [-v [optional True|False]]

Convert edge file (optional node file) to html graph visualization file

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK input file. (May be omitted or '-' for
                        stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for
                        stdout.)
  --node-file NODE_FILE
                        Path of the node file.
  --direction DIRECTION
                        The edge direction: arrow|particle|None. Default: None
  --show-edge-label     Add this option to show labels on edges. Default:
                        False
  --edge-color-column EDGE_COLOR_COLUMN
                        Column for edge colors in the edge file. The values
                        can be numbers, hex codes or any strings
  --edge-color-numbers  Add this option if the values in the --edge-color-
                        column are numbers
  --edge-color-hex      Add this option if the values in the --edge-color-
                        column are valid hexadecimal colors.Valid hexadecimal
                        colors start with # and are of 3 or 6 length (without
                        the #)
  --edge-color-style EDGE_COLOR_STYLE
                        Edge color style for edge color: categorical|gradient.
                        Default: None
  --edge-color-default EDGE_COLOR_DEFAULT
                        Default color for edges. Default: '#000000'
  --edge-width-column EDGE_WIDTH_COLUMN
                        Column for edge widths in the edge file. The values
                        should be numbers.
  --edge-width-minimum EDGE_WIDTH_MINIMUM
                        Minimum edge width. Default: 1.0
  --edge-width-maximum EDGE_WIDTH_MAXIMUM
                        Maximum edge width. Default: 5.0
  --edge-width-default EDGE_WIDTH_DEFAULT
                        Default edge width. Default: 1.0
  --edge-width-scale EDGE_WIDTH_SCALE
                        Edge width scale: linear|log. Default: None
  --node-color-column NODE_COLOR_COLUMN
                        Column for node colors in the --node-file. The values
                        can be numbers, valid hex codes or any strings.
  --node-color-style NODE_COLOR_STYLE
                        Node color style: categorical|gradient. Default: None
  --node-color-default NODE_COLOR_DEFAULT
                        Default node color. Default: '#000000'
  --node-color-scale NODE_COLOR_SCALE
                        Node color scale: linear|log. Default: None
  --node-color-numbers  Add this option if the values in the --node-color-
                        column are numbers
  --node-color-hex      Add this option if the values in the --node-color-
                        column are valid hexadecimal colors.Valid hexadecimal
                        colors start with # and are of 3 or 6 length (without
                        the #)
  --node-size-column NODE_SIZE_COLUMN
                        Column for node sizes in the --node-file. Default:
                        None
  --node-size-minimum NODE_SIZE_MINIMUM
                        Minimum node size. Default: 1.0
  --node-size-maximum NODE_SIZE_MAXIMUM
                        Maximum node size. Default: 5.0
  --node-size-default NODE_SIZE_DEFAULT
                        Default node size. Default: 2.0
  --node-size-scale NODE_SIZE_SCALE
                        Node size scale: linear|log. Default: None
  --node-file-id NODE_FILE_ID
                        ID column name in the --node-file. Default: 'id'
  --show-text-limit SHOW_TEXT_LIMIT
                        When number of nodes is greater than --show-text-
                        limit, node labels will not be visible.Default: 500
  --node-border-color NODE_BORDER_COLOR
                        Node border color. Default: None
  --tooltip-column TOOLTIP_COLUMN
                        Column for node tooltips in the --node-file. Default:
                        None
  --show-text SHOW_TEXT
                        Show node labels at the position relative to node:
                        center|above. Default: None. If the number of nodes in
                        the graph is greater than specified by --show-text-
                        limit option, which is 500 by default, then the text
                        will not be shown in the visualization.
  --node-categorical-scale NODE_CATEGORICAL_SCALE
                        Node color categorical scale node from d3-scale-
                        chromatic.https://observablehq.com/@d3/sequential-
                        scales. Default: rainbow
  --edge-categorical-scale EDGE_CATEGORICAL_SCALE
                        Edge color categorical scale for edge d3-scale-
                        chromatic.https://observablehq.com/@d3/sequential-
                        scales. Default: rainbow
  --node-gradient-scale NODE_GRADIENT_SCALE
                        Node color gradient scale from d3-scale-chromatic.
                        Default: d3.interpolateRdBu
  --edge-gradient-scale EDGE_GRADIENT_SCALE
                        Edge color gradient scale from d3-scale-chromatic.
                        Default: d3.interpolateRdBu

  -v [optional True|False], --verbose [optional True|False]
                        Print additional progress messages (default=False).

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

Both node file and edge file can contain additional columns. These columns can be used to provide more information as needed (see examples below)

## Examples

```bash
kgtk cat -i examples/docs/visualize_force_graph_example2.tsv
```

Edge File

|id     |node;label|is_country|type|degree|type_missing|population|
|-------|----------|----------|----|------|------------|----------|
|Alice  |‘Alice’@en|0         |human|4     |            |          |
|Susan  |‘Susan’@en|0         |human|4     |            |          |
|John   |‘John’@en |0         |human|4     |            |          |
|Claudia|‘Claudia’@en|0         |human|3     |            |          |
|Ulrich |‘Ulrich’@en|0         |human|4     |            |          |
|Fritz  |‘Fritz’@en|0         |human|4     |            |          |
|USA    |‘USA’@en  |1         |country|5     |country     |300       |
|Germany|‘Germany’@en|1         |country|5     |country     |50        |
|Brazil |‘Brazil’@en|1         |country|2     |country     |200       |

```bash
kgtk cat -i examples/docs/visualize_force_graph_example2_node.tsv
```

Node File

|node1  |label |node2  |weight|
|-------|------|-------|------|
|Alice  |friend|Susan  |0.9   |
|Susan  |friend|John   |0.3   |
|John   |friend|Claudia|      |
|Ulrich |friend|John   |      |
|Fritz  |friend|Ulrich |      |
|Fritz  |friend|Alice  |      |
|Alice  |born  |USA    |      |
|Susan  |born  |USA    |      |
|John   |born  |USA    |      |
|Claudia|born  |Germany|      |
|Ulrich |born  |Germany|      |
|Fritz  |born  |Germany|      |
|Alice  |lives |Germany|      |
|Susan  |lives |USA    |      |
|John   |lives |Brazil |      |
|Claudia|lives |Germany|      |
|Ulrich |lives |Brazil |      |
|Fritz  |lives |Germany|      |


## 1. Default
```
kgtk visualize-force-graph -i examples/docs/visualize_force_graph_example2.tsv -o default.html
```
This is the default version of this command, only producing a graph with default color, width and size

<img src="https://github.com/usc-isi-i2/kgtk/raw/dev/docs/images/visualize-force-graph-examples/1_default.jpg" width="300"/>


## 2. Show countries
```
kgtk visualize-force-graph -i examples/docs/visualize_force_graph_example2.tsv \
--node-file examples/docs/visualize_force_graph_example2_node.tsv \
--node-color-column is_country \
--node-color-style categorical \
-o show_countries.html
```
This customization uses is_country as columns for assigning colors. --node-color-style categorical indicates that we assign a unique color to each different string. The default d3.schemeCategory10 supports a max of 10 different colors.

<img src="https://github.com/usc-isi-i2/kgtk/raw/dev/docs/images/visualize-force-graph-examples/2_show_country.jpg" width="300"/>

## 3. Show types
```
kgtk visualize-force-graph -i examples/docs/visualize_force_graph_example2.tsv \
--node-file examples/docs/visualize_force_graph_example2_node.tsv \
--node-color-column type \
--node-color-style categorical \
-o show_types.html
```
This customization uses type as columns for assigning colors. --node-color-style categorical indicates that we assign a unique color to each different string. The default d3.schemeCategory10 supports a max of 10 different colors 

<img src="https://github.com/usc-isi-i2/kgtk/raw/dev/docs/images/visualize-force-graph-examples/3_show_type.jpg" width="300"/>

## 4. Handle missing values
```
kgtk visualize-force-graph -i examples/docs/visualize_force_graph_example2.tsv \
--node-file examples/docs/visualize_force_graph_example2_node.tsv \
--node-color-column type_missing \
--node-color-style categorical \
-o show_types_missing.html
```

This customization uses type_missing as columns for assigning colors. --node-color-style categorical indicates that we assign a unique color to each different string. The default d3.schemeCategory10 supports a max of 10 different colors. Notice here there are missing values. All missing values will be assigned a color. 

<img src="https://github.com/usc-isi-i2/kgtk/raw/dev/docs/images/visualize-force-graph-examples/4_missing_value.jpg" width="300"/>

## 5. Node color gradient
```
kgtk visualize-force-graph -i examples/docs/visualize_force_graph_example2.tsv \
--node-file examples/docs/visualize_force_graph_example2_node.tsv \
--node-color-column degree \
--node-color-style gradient \
--node-color-scale log \
-o show_color_gradient.html
```
This customization uses degree as columns for assigning colors. --node-color-style gradient indicates that we assign color based on interpolation of number in node-color-column to 0-1. The default scale is d3.interpolateRdBu.

<img src="https://github.com/usc-isi-i2/kgtk/raw/dev/docs/images/visualize-force-graph-examples/5_node_color_gradient.jpg" width="300"/>

## 6. Show Edge Color
```
kgtk visualize-force-graph -i examples/docs/visualize_force_graph_example2.tsv \
--edge-color-column label \
--edge-color-style categorical \
-o show_edge_color.html
```
This customization uses label as categorical coloring. Each different label will be assigned a different color. The default d3.schemeCategory10 supports a max of 10 different colors.

<img src="https://github.com/usc-isi-i2/kgtk/raw/dev/docs/images/visualize-force-graph-examples/6_edge_color_categorical.jpg" width="300"/>


## 7. Show Edge and Node Color
```
kgtk visualize-force-graph -i examples/docs/visualize_force_graph_example2.tsv \
--edge-color-column label \
--edge-color-style categorical \
--node-file examples/docs/visualize_force_graph_example2_node.tsv \
--node-color-column degree \
--node-color-style gradient \
--node-color-scale linear \
-o show_edge_node_color.html
```
This customization uses label as categorical edge coloring and degree for gradient node coloring.

<img src="https://github.com/usc-isi-i2/kgtk/raw/dev/docs/images/visualize-force-graph-examples/7_edge_node_color.jpg" width="300"/>


## 8. Node Size
```
kgtk visualize-force-graph -i examples/docs/visualize_force_graph_example2.tsv \
--node-file examples/docs/visualize_force_graph_example2_node.tsv \
--node-size-column population \
--node-size-minimum 2.0 \
--node-size-maximum 6.0 \
--node-size-default 4.0 \
--node-size-scale log \
-o node_size_log1.html
```
This customization uses population to interpolate node size based on log scale. Resulting range would be from 2 to 6. Any node with no value in population columns will be assigned the default size (6)

<img src="https://github.com/usc-isi-i2/kgtk/raw/dev/docs/images/visualize-force-graph-examples/8_node_size.jpg" width="300"/>

## 9. Edge width
```
kgtk visualize-force-graph -i examples/docs/visualize_force_graph_example2.tsv \
--edge-width-column weight \
--edge-width-minimum 2.0 \
--edge-width-maximum 5.0 \
--edge-width-default 2.0 \
--edge-width-scale log \
-o show_edge_thickness.html
```
This customization use weight column in edge file to interpolate edge width from log scale. Resulting range will be from 2 to 5.  Any edge with no value in weight columns will be assigned the default size (2)

<img src="https://github.com/usc-isi-i2/kgtk/raw/dev/docs/images/visualize-force-graph-examples/9_edge_width.jpg" width="300"/>


## 10. Text node
```
kgtk visualize-force-graph -i examples/docs/visualize_force_graph_example2.tsv \
--node-file examples/docs/visualize_force_graph_example2_node.tsv \
--node-color-column degree \
--node-color-style gradient \
--node-color-scale linear \
--text-node above \
-o show_node_label.html
```
This customization uses degree column in node file to interpolate color based on linear scale. Also the label of each nodes will be showing as text above nodes.

<img src="https://github.com/usc-isi-i2/kgtk/raw/dev/docs/images/visualize-force-graph-examples/10_text_node.jpg" width="300"/>
