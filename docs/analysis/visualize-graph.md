This command creates a html visualization of a KGTK edge file
## Usage
```
usage: kgtk visualize-graph [-h] [-i INPUT_FILE] [-o OUTPUT_FILE] [--node-file NODE_FILE] [--direction DIRECTION]
                            [--show-edge-label] [--edge-color-column EDGE_COLOR_COLUMN]
                            [--edge-color-numbers EDGE_COLOR_NUMBERS] [--edge-color-hex]
                            [--edge-color-style EDGE_COLOR_STYLE] [--edge-color-default EDGE_COLOR_DEFAULT]
                            [--edge-width-column EDGE_WIDTH_COLUMN] [--edge-width-minimum EDGE_WIDTH_MINIMUM]
                            [--edge-width-maximum EDGE_WIDTH_MAXIMUM] [--edge-width-default EDGE_WIDTH_DEFAULT]
                            [--edge-width-scale EDGE_WIDTH_SCALE] [--node-color-column NODE_COLOR_COLUMN]
                            [--node-color-style NODE_COLOR_STYLE] [--node-color-default NODE_COLOR_DEFAULT]
                            [--node-color-numbers NODE_COLOR_NUMBERS] [--node-color-hex]
                            [--node-size-column NODE_SIZE_COLUMN] [--node-size-minimum NODE_SIZE_MINIMUM]
                            [--node-size-maximum NODE_SIZE_MAXIMUM] [--node-size-default NODE_SIZE_DEFAULT]
                            [--node-size-scale NODE_SIZE_SCALE] [--node-file-id NODE_FILE_ID]
                            [--show-text-limit SHOW_TEXT_LIMIT] [--node-border-color NODE_BORDER_COLOR]
                            [--tooltip-column TOOLTIP_COLUMN] [--show-text SHOW_TEXT] [--show-blank-labels]
                            [-v [optional True|False]]

Convert edge file (optional node file) to html graph visualization file

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK input file. (May be omitted or '-' for stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for stdout.)
  --node-file NODE_FILE
                        Path of the node file.
  --direction DIRECTION
                        The edge direction: arrow|particle|None. Default: None
  --show-edge-label     Add this option to show labels on edges. Default: False
  --edge-color-column EDGE_COLOR_COLUMN
                        Column for edge colors in the edge file. The values can be numbers, hex codes or any strings
  --edge-color-numbers EDGE_COLOR_NUMBERS
                        Indicate if the values in the --edge-color-column are numbers and specify how to scale the numbers.
                        The valid choices are:linear|log|as-is. Default: None. The numbers will be scaled linearly,
                        logarithmically, left as is respectively.
  --edge-color-hex      Add this option if the values in the --edge-color-column are valid hexadecimal colors.Valid
                        hexadecimal colors start with # and are of 3 or 6 length (without the #)
  --edge-color-style EDGE_COLOR_STYLE
                        Pick one of the following CATEGORICAL styles: d3.schemeCategory10, d3.schemeAccent, d3.schemeDark2,
                        d3.schemePaired, d3.schemePastel1, d3.schemePastel2, d3.schemeSet1, d3.schemeSet2, d3.schemeSet3,
                        d3.schemeTableau10 OR one of the following GRADIENT styles: d3.interpolateBrBG, d3.interpolatePRGn,
                        d3.interpolatePiYG, d3.interpolatePuOr, d3.interpolateRdBu, d3.interpolateRdGy,
                        d3.interpolateRdYlBu, d3.interpolateRdYlGn, d3.interpolateSpectral, d3.interpolateBlues,
                        d3.interpolateGreens, d3.interpolateOranges, d3.interpolatePurples, d3.interpolateReds,
                        d3.interpolateGreys, d3.interpolateTurbo, d3.interpolateViridis, d3.interpolateInferno,
                        d3.interpolateMagma, d3.interpolatePlasma, d3.interpolateCividis, d3.interpolateWarm,
                        d3.interpolateCool, d3.interpolateCubehelixDefault, d3.interpolateBuGn, d3.interpolateBuPu,
                        d3.interpolateGnBu, d3.interpolateOrRd, d3.interpolatePuBuGn, d3.interpolatePuBu,
                        d3.interpolatePuRd, d3.interpolateRdPu, d3.interpolateYlGnBu, d3.interpolateYlGn,
                        d3.interpolateYlOrBr, d3.interpolateYlOrRd, d3.interpolateRainbow Default:
                        d3.interpolateRainbow.See https://github.com/d3/d3-scale-chromatic for more details.
  --edge-color-default EDGE_COLOR_DEFAULT
                        Default color for edges. Default: '#000000'
  --edge-width-column EDGE_WIDTH_COLUMN
                        Column for edge widths in the edge file. The values should be numbers.
  --edge-width-minimum EDGE_WIDTH_MINIMUM
                        Minimum edge width. Default: 1.0
  --edge-width-maximum EDGE_WIDTH_MAXIMUM
                        Maximum edge width. Default: 5.0
  --edge-width-default EDGE_WIDTH_DEFAULT
                        Default edge width. Default: 1.0
  --edge-width-scale EDGE_WIDTH_SCALE
                        Edge width scale: linear|log. Default: None
  --node-color-column NODE_COLOR_COLUMN
                        Column for node colors in the --node-file. The values can be numbers, valid hex codes or any
                        strings.
  --node-color-style NODE_COLOR_STYLE
                        Pick one of the following CATEGORICAL styles: d3.schemeCategory10, d3.schemeAccent, d3.schemeDark2,
                        d3.schemePaired, d3.schemePastel1, d3.schemePastel2, d3.schemeSet1, d3.schemeSet2, d3.schemeSet3,
                        d3.schemeTableau10 OR one of the following GRADIENT styles: d3.interpolateBrBG, d3.interpolatePRGn,
                        d3.interpolatePiYG, d3.interpolatePuOr, d3.interpolateRdBu, d3.interpolateRdGy,
                        d3.interpolateRdYlBu, d3.interpolateRdYlGn, d3.interpolateSpectral, d3.interpolateBlues,
                        d3.interpolateGreens, d3.interpolateOranges, d3.interpolatePurples, d3.interpolateReds,
                        d3.interpolateGreys, d3.interpolateTurbo, d3.interpolateViridis, d3.interpolateInferno,
                        d3.interpolateMagma, d3.interpolatePlasma, d3.interpolateCividis, d3.interpolateWarm,
                        d3.interpolateCool, d3.interpolateCubehelixDefault, d3.interpolateBuGn, d3.interpolateBuPu,
                        d3.interpolateGnBu, d3.interpolateOrRd, d3.interpolatePuBuGn, d3.interpolatePuBu,
                        d3.interpolatePuRd, d3.interpolateRdPu, d3.interpolateYlGnBu, d3.interpolateYlGn,
                        d3.interpolateYlOrBr, d3.interpolateYlOrRd, d3.interpolateRainbow Default:
                        d3.interpolateRainbow.See https://github.com/d3/d3-scale-chromatic for more details.
  --node-color-default NODE_COLOR_DEFAULT
                        Default node color. Default: '#000000'
  --node-color-numbers NODE_COLOR_NUMBERS
                        Indicate if the values in the --node-color-column are numbers and specify how to scale the numbers.
                        The valid choices are:linear|log|as-is. Default: None. The numbers will be scaled linearly,
                        logarithmically, left as is respectively.
  --node-color-hex      Add this option if the values in the --node-color-column are valid hexadecimal colors.Valid
                        hexadecimal colors start with # and are of 3 or 6 length (without the #)
  --node-size-column NODE_SIZE_COLUMN
                        Column for node sizes in the --node-file. Default: None
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
                        When number of nodes is greater than --show-text-limit, node labels will not be visible.Default:
                        500
  --node-border-color NODE_BORDER_COLOR
                        Node border color. Default: None
  --tooltip-column TOOLTIP_COLUMN
                        Column for node tooltips in the --node-file. Default: None
  --show-text SHOW_TEXT
                        Show node labels at the position relative to node: center|above. Default: None. If the number of
                        nodes in the graph is greater than specified by --show-text-limit option, which is 500 by default,
                        then the text will not be shown in the visualization.
  --show-blank-labels   if --show-text is specified, show the label of a Qnode as emptry string, and not the Qnode, if the
                        label is an empty string.

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

|node1|label |node2|weight|hex_color|ordinal|
|-----|------|-----|------|---------|-------|
|Q1   |friend|Q2   |0.9   |#FF69B4  |0      |
|Q2   |friend|Q3   |0.3   |#FF69B4  |1      |
|Q3   |friend|Q4   |      |#FF69B4  |2      |
|Q5   |friend|Q3   |      |#FF69B4  |3      |
|Q6   |friend|Q5   |      |#FF69B4  |4      |
|Q6   |friend|Q1   |      |#FF69B4  |5      |
|Q1   |born  |Q7   |      |#FFF68F  |6      |
|Q2   |born  |Q7   |      |#FFF68F  |7      |
|Q3   |born  |Q7   |      |#FFF68F  |8      |
|Q4   |born  |Q8   |      |#FFF68F  |9      |
|Q5   |born  |Q8   |      |#FFF68F  |10     |
|Q6   |born  |Q8   |      |#FFF68F  |11     |
|Q1   |lives |Q8   |      |#32CD32  |12     |
|Q2   |lives |Q7   |      |#32CD32  |13     |
|Q3   |lives |Q9   |      |#32CD32  |14     |
|Q4   |lives |Q8   |      |#32CD32  |15     |
|Q5   |lives |Q9   |      |#32CD32  |16     |
|Q6   |lives |Q8   |      |#32CD32  |17     |


```bash
kgtk cat -i examples/docs/visualize_force_graph_example2_node.tsv
```

Node File

|id |label |is_country|type|degree |type_missing|population|hex_color|ordinal|
|---|------|----------|----|-------|------------|----------|---------|-------|
|Q1 |'Alice'@en|0         |human|40     |            |          |#00FFFF  |0      |
|Q2 |'Susan'@en|0         |human|14     |            |          |#8A2BE2  |1      |
|Q3 |'John'@en|0         |human|4      |            |          |#FF4040  |2      |
|Q4 |'Claudia'@en|0         |human|32     |            |          |#7FFF00  |3      |
|Q5 |'Ulrich'@en|0         |human|422    |            |          |#FFB90F  |4      |
|Q6 |'Fritz'@en|0         |human|4      |            |          |#C1FFC1  |5      |
|Q7 |'USA'@en|1         |country|50     |country     |300       |#FF1493  |6      |
|Q8 |'Germany'@en|1         |country|500    |country     |50        |#FFD700  |7      |
|Q9 |'Brazil'@en|1         |country|222    |country     |200       |#FF69B4  |8      |


## Node and Edge Color Style Options

|Color Style|URL                                                                    |Image                                                                           |
|-----------|-----------------------------------------------------------------------|--------------------------------------------------------------------------------|
|d3.schemeCategory10|https://github.com/d3/d3-scale-chromatic#d3.schemeCategory10           |![Image](https://raw.githubusercontent.com/d3/d3-scale-chromatic/master/img/category10.png)|
|d3.schemeAccent|https://github.com/d3/d3-scale-chromatic#d3.schemeAccent               |![Image](https://raw.githubusercontent.com/d3/d3-scale-chromatic/master/img/Accent.png)|
|d3.schemeDark2|https://github.com/d3/d3-scale-chromatic#d3.schemeDark2                |![Image](https://raw.githubusercontent.com/d3/d3-scale-chromatic/master/img/Dark2.png)|
|d3.schemePaired|https://github.com/d3/d3-scale-chromatic#d3.schemePaired               |![Image](https://raw.githubusercontent.com/d3/d3-scale-chromatic/master/img/Paired.png)|
|d3.schemePastel1|https://github.com/d3/d3-scale-chromatic#d3.schemePastel1              |![Image](https://raw.githubusercontent.com/d3/d3-scale-chromatic/master/img/Pastel1.png)|
|d3.schemePastel2|https://github.com/d3/d3-scale-chromatic#d3.schemePastel2              |![Image](https://raw.githubusercontent.com/d3/d3-scale-chromatic/master/img/Pastel2.png)|
|d3.schemeSet1|https://github.com/d3/d3-scale-chromatic#d3.schemeSet1                 |![Image](https://raw.githubusercontent.com/d3/d3-scale-chromatic/master/img/Set1.png)|
|d3.schemeSet2|https://github.com/d3/d3-scale-chromatic#d3.schemeSet2                 |![Image](https://raw.githubusercontent.com/d3/d3-scale-chromatic/master/img/Set2.png)|
|d3.schemeSet3|https://github.com/d3/d3-scale-chromatic#d3.schemeSet3                 |![Image](https://raw.githubusercontent.com/d3/d3-scale-chromatic/master/img/Set3.png)|
|d3.schemeTableau10|https://github.com/d3/d3-scale-chromatic#d3.schemeTableau10            |![Image](https://raw.githubusercontent.com/d3/d3-scale-chromatic/master/img/Tableau10.png)|
|d3.interpolateBrBG|https://github.com/d3/d3-scale-chromatic#d3.interpolateBrBG            |![Image](https://raw.githubusercontent.com/d3/d3-scale-chromatic/master/img/BrBG.png)|
|d3.interpolatePRGn|https://github.com/d3/d3-scale-chromatic#d3.interpolatePRGn            |![Image](https://raw.githubusercontent.com/d3/d3-scale-chromatic/master/img/PRGn.png)|
|d3.interpolatePiYG|https://github.com/d3/d3-scale-chromatic#d3.interpolatePiYG            |![Image](https://raw.githubusercontent.com/d3/d3-scale-chromatic/master/img/PiYG.png)|
|d3.interpolatePuOr|https://github.com/d3/d3-scale-chromatic#d3.interpolatePuOr            |![Image](https://raw.githubusercontent.com/d3/d3-scale-chromatic/master/img/PuOr.png)|
|d3.interpolateRdBu|https://github.com/d3/d3-scale-chromatic#d3.interpolateRdBu            |![Image](https://raw.githubusercontent.com/d3/d3-scale-chromatic/master/img/RdBu.png)|
|d3.interpolateRdGy|https://github.com/d3/d3-scale-chromatic#d3.interpolateRdGy            |![Image](https://raw.githubusercontent.com/d3/d3-scale-chromatic/master/img/RdGy.png)|
|d3.interpolateRdYlBu|https://github.com/d3/d3-scale-chromatic#d3.interpolateRdYlBu          |![Image](https://raw.githubusercontent.com/d3/d3-scale-chromatic/master/img/RdYlBu.png)|
|d3.interpolateRdYlGn|https://github.com/d3/d3-scale-chromatic#d3.interpolateRdYlGn          |![Image](https://raw.githubusercontent.com/d3/d3-scale-chromatic/master/img/RdYlGn.png)|
|d3.interpolateSpectral|https://github.com/d3/d3-scale-chromatic#d3.interpolateSpectral        |![Image](https://raw.githubusercontent.com/d3/d3-scale-chromatic/master/img/Spectral.png)|
|d3.interpolateBlues|https://github.com/d3/d3-scale-chromatic#d3.interpolateBlues           |![Image](https://raw.githubusercontent.com/d3/d3-scale-chromatic/master/img/Blues.png)|
|d3.interpolateGreens|https://github.com/d3/d3-scale-chromatic#d3.interpolateGreens          |![Image](https://raw.githubusercontent.com/d3/d3-scale-chromatic/master/img/Greens.png)|
|d3.interpolateOranges|https://github.com/d3/d3-scale-chromatic#d3.interpolateOranges         |![Image](https://raw.githubusercontent.com/d3/d3-scale-chromatic/master/img/Oranges.png)|
|d3.interpolatePurples|https://github.com/d3/d3-scale-chromatic#d3.interpolatePurples         |![Image](https://raw.githubusercontent.com/d3/d3-scale-chromatic/master/img/Purples.png)|
|d3.interpolateReds|https://github.com/d3/d3-scale-chromatic#d3.interpolateReds            |![Image](https://raw.githubusercontent.com/d3/d3-scale-chromatic/master/img/Reds.png)|
|d3.interpolateGreys|https://github.com/d3/d3-scale-chromatic#d3.interpolateGreys           |![Image](https://raw.githubusercontent.com/d3/d3-scale-chromatic/master/img/Greys.png)|
|d3.interpolateTurbo|https://github.com/d3/d3-scale-chromatic#d3.interpolateTurbo           |![Image](https://raw.githubusercontent.com/d3/d3-scale-chromatic/master/img/turbo.png)|
|d3.interpolateViridis|https://github.com/d3/d3-scale-chromatic#d3.interpolateViridis         |![Image](https://raw.githubusercontent.com/d3/d3-scale-chromatic/master/img/viridis.png)|
|d3.interpolateInferno|https://github.com/d3/d3-scale-chromatic#d3.interpolateInferno         |![Image](https://raw.githubusercontent.com/d3/d3-scale-chromatic/master/img/inferno.png)|
|d3.interpolateMagma|https://github.com/d3/d3-scale-chromatic#d3.interpolateMagma           |![Image](https://raw.githubusercontent.com/d3/d3-scale-chromatic/master/img/magma.png)|
|d3.interpolatePlasma|https://github.com/d3/d3-scale-chromatic#d3.interpolatePlasma          |![Image](https://raw.githubusercontent.com/d3/d3-scale-chromatic/master/img/plasma.png)|
|d3.interpolateCividis|https://github.com/d3/d3-scale-chromatic#d3.interpolateCividis         |![Image](https://raw.githubusercontent.com/d3/d3-scale-chromatic/master/img/cividis.png)|
|d3.interpolateWarm|https://github.com/d3/d3-scale-chromatic#d3.interpolateWarm            |![Image](https://raw.githubusercontent.com/d3/d3-scale-chromatic/master/img/warm.png)|
|d3.interpolateCool|https://github.com/d3/d3-scale-chromatic#d3.interpolateCool            |![Image](https://raw.githubusercontent.com/d3/d3-scale-chromatic/master/img/cool.png)|
|d3.interpolateCubehelixDefault|https://github.com/d3/d3-scale-chromatic#d3.interpolateCubehelixDefault|![Image](https://raw.githubusercontent.com/d3/d3-scale-chromatic/master/img/cubehelix.png)|
|d3.interpolateBuGn|https://github.com/d3/d3-scale-chromatic#d3.interpolateBuGn            |![Image](https://raw.githubusercontent.com/d3/d3-scale-chromatic/master/img/BuGn.png)|
|d3.interpolateBuPu|https://github.com/d3/d3-scale-chromatic#d3.interpolateBuPu            |![Image](https://raw.githubusercontent.com/d3/d3-scale-chromatic/master/img/BuPu.png)|
|d3.interpolateGnBu|https://github.com/d3/d3-scale-chromatic#d3.interpolateGnBu            |![Image](https://raw.githubusercontent.com/d3/d3-scale-chromatic/master/img/GnBu.png)|
|d3.interpolateOrRd|https://github.com/d3/d3-scale-chromatic#d3.interpolateOrRd            |![Image](https://raw.githubusercontent.com/d3/d3-scale-chromatic/master/img/OrRd.png)|
|d3.interpolatePuBuGn|https://github.com/d3/d3-scale-chromatic#d3.interpolatePuBuGn          |![Image](https://raw.githubusercontent.com/d3/d3-scale-chromatic/master/img/PuBuGn.png)|
|d3.interpolatePuBu|https://github.com/d3/d3-scale-chromatic#d3.interpolatePuBu            |![Image](https://raw.githubusercontent.com/d3/d3-scale-chromatic/master/img/PuBu.png)|
|d3.interpolatePuRd|https://github.com/d3/d3-scale-chromatic#d3.interpolatePuRd            |![Image](https://raw.githubusercontent.com/d3/d3-scale-chromatic/master/img/PuRd.png)|
|d3.interpolateRdPu|https://github.com/d3/d3-scale-chromatic#d3.interpolateRdPu            |![Image](https://raw.githubusercontent.com/d3/d3-scale-chromatic/master/img/RdPu.png)|
|d3.interpolateYlGnBu|https://github.com/d3/d3-scale-chromatic#d3.interpolateYlGnBu          |![Image](https://raw.githubusercontent.com/d3/d3-scale-chromatic/master/img/YlGnBu.png)|
|d3.interpolateYlGn|https://github.com/d3/d3-scale-chromatic#d3.interpolateYlGn            |![Image](https://raw.githubusercontent.com/d3/d3-scale-chromatic/master/img/YlGn.png)|
|d3.interpolateYlOrBr|https://github.com/d3/d3-scale-chromatic#d3.interpolateYlOrBr          |![Image](https://raw.githubusercontent.com/d3/d3-scale-chromatic/master/img/YlOrBr.png)|
|d3.interpolateYlOrRd|https://github.com/d3/d3-scale-chromatic#d3.interpolateYlOrRd          |![Image](https://raw.githubusercontent.com/d3/d3-scale-chromatic/master/img/YlOrRd.png)|
|d3.interpolateRainbow|https://github.com/d3/d3-scale-chromatic#d3.interpolateRainbow         |![Image](https://raw.githubusercontent.com/d3/d3-scale-chromatic/master/img/rainbow.png)|




## 1. Default
```
kgtk visualize-graph -i examples/docs/visualize_force_graph_example2.tsv -o default.html
```
This is the default version of this command, only producing a graph with default color, width and size

<img src="https://github.com/usc-isi-i2/kgtk/raw/dev/docs/images/visualize-force-graph-examples/1.jpg" width="300"/>


## 2. Color by `is_country` column in the node file, use `d3.schemeCategory10` to color nodes
```
kgtk visualize-graph -i examples/docs/visualize_force_graph_example2.tsv \
                     --node-file examples/docs/visualize_force_graph_example2_node.tsv \
                     --node-color-column is_country \
                     --node-color-style d3.schemeCategory10 \
                     --node-color-numbers as-is \
                     -o show_countries.html
```
This command specifies `is_country` as column for assigning colors. 

This command specifies that the values in the color column are numbers and should be left as is with the help of following option `--node-color-numbers as-
is`.

Finally, we specify that nodes should be colored using the `d3.schemeCategory10` style.

<img src="https://github.com/usc-isi-i2/kgtk/raw/dev/docs/images/visualize-force-graph-examples/2.png" width="300"/>

## 3. Color by column `degree`, values as numbers, color scale: log, `d3.schemePastel1` as color style
```
kgtk visualize-graph -i examples/docs/visualize_force_graph_example2.tsv \
                     --node-file examples/docs/visualize_force_graph_example2_node.tsv \
                     --node-color-column degree \
                     --node-color-numbers log \
                     --node-color-style d3.schemePastel1 \
                     -o show_degrees.html
```

This command specifies `degree` as column for assigning colors. 

This command specifies that the values in the color column are numbers and should be scaled logarithmically with the help of following option `--node-color-numbers log`.

Finally, we specify that nodes should be colored using the `d3.schemePastel1` style.


<img src="https://github.com/usc-isi-i2/kgtk/raw/dev/docs/images/visualize-force-graph-examples/3.png" width="300"/>

## 4. Handle missing values
```
kgtk visualize-graph -i examples/docs/visualize_force_graph_example2.tsv \
                     --node-file examples/docs/visualize_force_graph_example2_node.tsv \
                     --node-color-column type_missing \
                     --node-color-style d3.schemeSet3 \
                     -o show_types_missing.html
```

This command uses the column `type_missing` as assigning colors. 

Notice here there are missing values. 

All missing values will be assigned the default node color, using the style `d3.schemeSet3` to color nodes.

<img src="https://github.com/usc-isi-i2/kgtk/raw/dev/docs/images/visualize-force-graph-examples/4.png" width="300"/>

## 5. Color by column `hex_color`, values as hexadecimal color codes
```
kgtk visualize-graph -i examples/docs/visualize_force_graph_example2.tsv \
                     --node-file examples/docs/visualize_force_graph_example2_node.tsv \
                     --node-color-column hex_color \
                     --node-color-hex \
                     -o show_color_hex.html
```
This command uses the column `hex_color`, which contains valid hex colors, for coloring nodes.

<img src="https://github.com/usc-isi-i2/kgtk/raw/dev/docs/images/visualize-force-graph-examples/5.png" width="300"/>

## 6. Show Edge Color
```
kgtk visualize-graph -i examples/docs/visualize_force_graph_example2.tsv \
                     --edge-color-column hex_color \
                     --edge-color-hex \
                     -o show_edge_color.html
```
This command uses the column `hex_color`, which contains valid hex colors, for assigning edge colors.

<img src="https://github.com/usc-isi-i2/kgtk/raw/dev/docs/images/visualize-force-graph-examples/6.png" width="300"/>


## 7. Show Node Size and Color
```
kgtk visualize-graph -i examples/docs/visualize_force_graph_example2.tsv \
                     --node-file examples/docs/visualize_force_graph_example2_node.tsv \
                     --node-size-column population \
                     --node-size-minimum 2.0 \
                     --node-size-maximum 6.0 \
                     --node-size-default 4.0 \
                     --node-color-column hex_color \
                     --node-color-hex \
                     --node-size-scale log \
                     -o show_edge_node_color.html
```
Colors nodes according to the column `hex_color`, which contains valid hex colors.
Size of the nodes is proportional to the values in the column `population`, we scale the node size logarithmically

<img src="https://github.com/usc-isi-i2/kgtk/raw/dev/docs/images/visualize-force-graph-examples/7.png" width="300"/>


## 8. Edge Width
```
kgtk visualize-graph -i examples/docs/visualize_force_graph_example2.tsv \
                     --edge-width-column weight \
                     --edge-width-minimum 2.0 \
                     --edge-width-maximum 5.0 \
                     --edge-width-default 2.0 \
                     --edge-width-scale log \
                     --node-color-column degree \
                     --node-color-style d3.schemeDark2 \
                     --node-color-numbers linear \
                     -o node_size_log1.html
```
This command uses the column `weight` in edge file to interpolate edge width using the log scale. 

Resulting edge width will be between 2.0 and 5.0 as specified by the options `--edge-width-minimum` and `--edge-width-maximum`. 
Any edge with no value in weight columns will be assigned the default size: 2.0

Moreover, color the nodes using the numerical values in the column `degree`, scaling the values linearly, using the style `d3.schemeDark2`.

<img src="https://github.com/usc-isi-i2/kgtk/raw/dev/docs/images/visualize-force-graph-examples/8.png" width="300"/>

## 9. Show text above nodes
```
kgtk visualize-graph -i examples/docs/visualize_force_graph_example2.tsv \
                     --node-file examples/docs/visualize_force_graph_example2_node.tsv \
                     --node-color-column hex_color \
                     --node-color-hex \
                     --show-text above \
                     -o show_node_label.html
```
Colors nodes by the column `hex_color` and shows labels above the nodes

<img src="https://github.com/usc-isi-i2/kgtk/raw/dev/docs/images/visualize-force-graph-examples/9.png" width="300"/>


## 10. Show labels on edges, color edges using hex colors
```
kgtk visualize-graph -i examples/docs/visualize_force_graph_example2.tsv \
                     --edge-color-column hex_color \
                     --edge-color-hex \
                     --show-edge-label \
                     -o show_edge_label.html
```
Colors edges by the hexadecimal codes in the column `hex_color` and shows labels on the edges as well.

<img src="https://github.com/usc-isi-i2/kgtk/raw/dev/docs/images/visualize-force-graph-examples/10.png" width="300"/>

## 11. Show labels and color nodes and edges
```
kgtk visualize-graph -i examples/docs/visualize_force_graph_example2.tsv \
                     --node-file examples/docs/visualize_force_graph_example2_node.tsv \
                     --node-color-column hex_color \
                     --node-color-hex \
                     --show-text above \
                     --show-edge-label \
                     --edge-color-hex \
                     --edge-color-column hex_color \
                     -o show_node_edge_label.html
```

Colors nodes by hexadecimal color codes in the column `hex_color` for both edges and nodes and  show labels above nodes and on edges.

<img src="https://github.com/usc-isi-i2/kgtk/raw/dev/docs/images/visualize-force-graph-examples/11.png" width="300"/>

## 12. Show labels above nodes, blank labels for nodes with missing labels (instead of showing ids)
```
kgtk visualize-graph -i examples/docs/visualize_force_graph_example2.tsv \
                     --node-file examples/docs/visualize_force_graph_example2_node.tsv \
                     --node-color-column hex_color \
                     --node-color-hex \
                     --show-text above \
                     --show-blank-labels \
                     -o show_blank_labels.html
```
This command shows blank labels for nodes with no labels, coloring the nodes using the hex colors in the column `hex_color`

<img src="https://github.com/usc-isi-i2/kgtk/raw/dev/docs/images/visualize-force-graph-examples/12.png" width="300"/>


## 13. Color by column `ordinal`, values as numbers, use `d3.interpolateGreens` interpolator
```
kgtk visualize-graph -i examples/docs/visualize_force_graph_example2.tsv \
                     --node-file examples/docs/visualize_force_graph_example2_node.tsv \
                     --node-color-column ordinal \
                     --node-color-numbers as-is \
                     --node-color-style d3.interpolateGreens \
                     -o scolor_nodes_interpolator_green.html
```
This command colors the nodes using numerical values in the column `ordinal`. We will map the colors to the scale `d3.interpolateGreens`. 

The values in the column are sequential values, small values will be mapped to lighter shades of green while higher values will be mapped to darker shades.

<img src="https://github.com/usc-isi-i2/kgtk/raw/dev/docs/images/visualize-force-graph-examples/13.png" width="300"/>

## 14. Color by column `ordinal`, values as numbers, use `d3.interpolateGreens` interpolator, show labels on nodes
```
kgtk visualize-graph -i examples/docs/visualize_force_graph_example2.tsv \
                     --node-file examples/docs/visualize_force_graph_example2_node.tsv \
                     --node-color-column ordinal \
                     --node-color-numbers as-is \
                     --node-color-style d3.interpolateGreens \
                     --show-text above \
                     -o color_nodes_interpolator_green.html
```
This command colors the nodes using numerical values in the column `ordinal`. We will map the colors to the scale `d3.interpolateGreens`. 

The values in the column are sequential values, small values will be mapped to lighter shades of green while higher values will be mapped to darker shades. Labels on the nodes match the shade of green for that node.

<img src="https://github.com/usc-isi-i2/kgtk/raw/dev/docs/images/visualize-force-graph-examples/14.png" width="300"/>



## 15. Color edges by column `ordinal`, values as numbers, use `d3.interpolateReds` interpolator
```
kgtk visualize-graph -i examples/docs/visualize_force_graph_example2.tsv \
                     --edge-color-column ordinal \
                     --edge-color-numbers as-is \
                     --edge-color-style d3.interpolateReds \
                     -o color_edges_interpolator_reds.html
```
This command colors the edges using numerical values in the column `ordinal`. We will map the colors to the scale `d3.interpolateReds`. 

The values in the column are sequential values, small values will be mapped to lighter shades of red while higher values will be mapped to darker shades.

<img src="https://github.com/usc-isi-i2/kgtk/raw/dev/docs/images/visualize-force-graph-examples/15.png" width="300"/>

## 16. Color edges by column `label`, values as strings, use `d3.d3.schemeDark2` style
```
kgtk visualize-graph -i examples/docs/visualize_force_graph_example2.tsv \
                     --edge-color-column label \
                     --edge-color-style d3.schemeDark2 \
                     -o color_edges_categorical_dark.html
```

This command maps strings in the column `label` to a categorical scale `d3.schemeDark2`

<img src="https://github.com/usc-isi-i2/kgtk/raw/dev/docs/images/visualize-force-graph-examples/16.png" width="300"/>
