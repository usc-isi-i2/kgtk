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
  --old-id-column-name COLUMN_NAME
                        The name of the old ID column. (default=id).
  --new-id-column-name COLUMN_NAME
                        The name of the new ID column. (default=id).
  --overwrite-id [optional true|false]
                        When true, replace existing ID values. When false,
                        copy existing ID values. When --overwrite-id is
                        omitted, it defaults to False. When --overwrite-id is
                        supplied without an argument, it is True.
  --verify-id-unique [optional true|false]
                        When true, verify ID uniqueness using an in-memory set
                        of IDs. When --verify-id-unique is omitted, it
                        defaults to False. When --verify-id-unique is supplied
                        without an argument, it is True.
  --id-style {node1-label-node2,node1-label-num,node1-label-node2-num,node1-label-node2-id,empty,prefix###,wikidata,wikidata-with-claim-id}
                        The ID generation style. (default=prefix###).
  --id-prefix PREFIX    The prefix for a prefix### ID. (default=E).
  --initial-id INTEGER  The initial numeric value for a prefix### ID.
                        (default=1).
  --id-prefix-num-width INTEGER
                        The width of the numeric value for a prefix### ID.
                        (default=1).
  --id-concat-num-width INTEGER
                        The width of the numeric value for a concatenated ID.
                        (default=4).
  --value-hash-width VALUE_HASH_WIDTH
                        How many characters should be used in a value hash?
                        (default=6)
  --claim-id-hash-width CLAIM_ID_HASH_WIDTH
                        How many characters should be used to hash the claim
                        ID? 0 means do not hash the claim ID. (default=8)
  --claim-id-column-name CLAIM_ID_COLUMN_NAME
                        The name of the claim_id column. (default=claim_id)
  --id-separator ID_SEPARATOR
                        The separator user between ID subfields. (default=-)

  -v [optional True|False], --verbose [optional True|False]
                        Print additional progress messages (default=False).
```

## Examples

Edge File contains:
- `node1`: the subject column (source node)
- `label`: the predicate column (property name)
- `node2`: the object column (target node)
- `node1;label`: the subject label (source node)
- `label;label`: the predicate label (property name)
- `node2;label`: the object label (target node)

    
Optional:
- `thickness`: thickness of edge (property name)
- `color`: color(string, float from 0-1, or hex color)
    
 
Node File contains:
- `id`: id of the node
- `color`: color(string, float from 0-1, or hex color)
- `node;label`: the node label
Optional:
- `x`: x_coordinate of node
- `y`: y_coordinate of node

Import a TSV file into Graph-tool, and store the result to disk. We store the statistics to log.txt. 

```
kgtk visualize-force-graph -i examples/docs/visualize_force_graph_example.tsv --direction arrow --show-edge-label True -o graph.html
```


The html file is the visualization of tsv edge file.

