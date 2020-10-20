This command will find all nodes reachable from given root nodes in a KGTK edge file. That is, given a set of nodes N and a set of properties P, this command computes the set of nodes R that can be reached from N via paths containing any of the properties in P.

The output file is an edge file that contains the following columns:

- `node1`: this column contains a root node
- `label`: this column contains only 'reachable'
- `node2`: this column contains node that is reachable from a root node

## Usage
```
usage: kgtk reachable-nodes [-h] [-i INPUT_FILE] [-o OUTPUT_FILE] [--root [ROOT [ROOT ...]]] [--root-file ROOTFILE] [--rootfilecolumn ROOTFILECOLUMN]
                            [--subj SUBJECT_COLUMN_NAME] [--obj OBJECT_COLUMN_NAME] [--pred PREDICATE_COLUMN_NAME] [--props [PROPS [PROPS ...]]]
                            [--undirected [True|False]] [--label LABEL] [--selflink [True|False]] [--show-properties [True|False]] [--breadth-first [True|False]]
                            [-v]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK file to find connected components in. (May be omitted or '-' for stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for stdout.)
  --root [ROOT [ROOT ...]]
                        Set of root nodes to use, space- or comma-separated strings. (default=None)
  --root-file ROOTFILE, --rootfile ROOTFILE
                        Option to specify a file containing the set of root nodes
  --rootfilecolumn ROOTFILECOLUMN
                        Specify the name or number of the root file column with the root nodes. (default=node1 or its alias if edge file, id if node file)
  --subj SUBJECT_COLUMN_NAME
                        Name of the subject column. (default: node1 or its alias)
  --obj OBJECT_COLUMN_NAME
                        Name of the object column. (default: label or its alias)
  --pred PREDICATE_COLUMN_NAME
                        Name of the predicate column. (default: node2 or its alias)
  --props [PROPS [PROPS ...]]
                        Properties to consider while finding reachable nodes, space- or comma-separated string. (default: all properties)
  --undirected [True|False]
                        When True, specify graph as undirected. (default=False)
  --label LABEL         The label for the reachable relationship. (default: reachable)
  --selflink [True|False]
                        When True, include a link from each output node to itself. (default=False)
  --show-properties [True|False]
                        When True, show the graph properties. (default=False)
  --breadth-first [True|False]
                        When True, search the graph breadth first. When false, search depth first. (default=False)

  -v, --verbose         Print additional progress messages (default=False).

```

### Examples

Find all the classes that given root nodes are a subclass of (transitive closure). Root nodes are obtained from node2 of P31.tsv (instance of) file. Command is run on P279.tsv (subclass of) file. Generates P279*.tsv. 

```
kgtk -i reachable-nodes P279.tsv --rootfile P31.tsv --rootfilecolumn node2 -o P279*.tsv
```
