>This command will find all nodes reachable from given root nodes in a input file. That is, given a set of nodes N and a set of properties P, this command computes the set of nodes R that can be reached from N via paths containing any of the properties in P.

The input file should be a KGTK Edge file with the following columns or their aliases:

- `node1`: the subject column
- `label`: the predicate column
- `node2`: the object column

Optionally, other columns may be used as the subject/predicate/object columns using the following
command line options:

- `--subj SUBJECT_COLUMN_NAME`: the name of the subject column (default: `node1`).
- `--pred PREDICATE_COLUMN_NAME`: the name of the predicate column (default: `label`).
- `--obj OBJECT_COLUMN_NAME`: the name of the object column (default: `node2`).

Note: If your input file doesn't have `node1`, `label`, or `node2` columns (or their aliases) at all, then it is
not a valid KGTK Edge file.  In this case, you also have to pass the following command line option:

- `--input-mode=NONE`


The root file, if specified with `--root-file ROOTFILE`, is used to get the list of starting nodes for the reachability analysis.
It, too, should be a valid KGTK file.

- If the root file is a KGTK Edge file (containing at least `node1`, `label`, and `node2` columns, or their aliases),
  then the unique values in the `node1` column (by default) will be used to build the set of root node names.
- If the root file is a KGTK Node file (containing at least an `id` column or its alias,
  and not containing a `node1` column or its alias), then the unique values in the `id` column (by default) will be
  used to build the set of root node names.

If the root file is a valid KGTK Edge or Node file, but you want to use a different column name than the defaults
shown above, then the `--rootfilecolumn COLUMN_NAME` option may be used to specify the root file column
name.

If the root file is not a valid KGTK Edge or Node file, but can be parsed by KgtkReader (it is a
valid tab-separated file), the it is necessary to speficy the following options:

- `--input-mode=NONE`
- `--rootfilecolumn COLUMN_NAME`

Here is another option:  if the argument to `--rootfilecolumn` is an integer, then it is treated
as a 0's-origin index into the root file's columns (e.g., the first column is nomber 0, the second column is number 1m
etc.)

The set of root nodes can also be specified on the command line, using the following command option:
- `--root ROOT [ROOT ...]`

Each `ROOT` group can be a comma-separated list of root node names.

Note: a comma-separated list should not have spaces before or after the comma(s).

Note: this implies that commas are not allowed in node names.  At the present time, there is
no option to override this constraint.

Both `--root` and `--rootfile` may be specified, in which case the root node set is the union of
the nodes from the root file and the nodes from the command line.

The output file is an edge file that contains the following columns:

- `node1`: this column contains a root node
- `label`: this column contains only 'reachable'
- `node2`: this column contains node that is reachable from a root node

## Usage
```
usage: kgtk reachable-nodes [-h] [-i INPUT_FILE] [-o OUTPUT_FILE]
                            [--root [ROOT [ROOT ...]]] [--root-file ROOTFILE]
                            [--rootfilecolumn ROOTFILECOLUMN]
                            [--subj SUBJECT_COLUMN_NAME]
                            [--obj OBJECT_COLUMN_NAME]
                            [--pred PREDICATE_COLUMN_NAME]
                            [--props [PROPS [PROPS ...]]]
                            [--undirected [True|False]] [--label LABEL]
                            [--selflink [True|False]]
                            [--show-properties [True|False]]
                            [--breadth-first [True|False]]
                            [-v [optional True|False]]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK file to find connected components in. (May be
                        omitted or '-' for stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for
                        stdout.)
  --root [ROOT [ROOT ...]]
                        Set of root nodes to use, space- or comma-separated
                        strings. (default=None)
  --root-file ROOTFILE, --rootfile ROOTFILE
                        Option to specify a file containing the set of root
                        nodes
  --rootfilecolumn ROOTFILECOLUMN
                        Specify the name or number of the root file column
                        with the root nodes. (default=node1 or its alias if
                        edge file, id if node file)
  --subj SUBJECT_COLUMN_NAME
                        Name of the subject column. (default: node1 or its
                        alias)
  --obj OBJECT_COLUMN_NAME
                        Name of the object column. (default: label or its
                        alias)
  --pred PREDICATE_COLUMN_NAME
                        Name of the predicate column. (default: node2 or its
                        alias)
  --props [PROPS [PROPS ...]]
                        Properties to consider while finding reachable nodes,
                        space- or comma-separated string. (default: all
                        properties)
  --undirected [True|False]
                        When True, specify graph as undirected.
                        (default=False)
  --label LABEL         The label for the reachable relationship. (default:
                        reachable)
  --selflink [True|False]
                        When True, include a link from each output node to
                        itself. (default=False)
  --show-properties [True|False]
                        When True, show the graph properties. (default=False)
  --breadth-first [True|False]
                        When True, search the graph breadth first. When false,
                        search depth first. (default=False)

  -v [optional True|False], --verbose [optional True|False]
                        Print additional progress messages (default=False).
```

## Examples

### P279 Example

Find all the classes that given root nodes are a subclass of (transitive closure).
Root nodes are obtained from node2 of P31.tsv (instance of) file, which is a KGTK Edge file.
Command is run on P279.tsv (subclass of) file, a KGTK Edge file.
The output is  P279-star.tsv. 

```
kgtk -i reachable-nodes P279.tsv --rootfile P31.tsv --rootfilecolumn node2 -o P279-star.tsv
```

### Nonstandard Root File

Suppose that the root file has only a `node1` column, making it neither a KGTK Edge file nor a KGTK Node file.
The following command may be used to process it:

```
kgtk -i reachable-nodes P279.tsv --rootfile P31.tsv --rootfilecolumn node2 -o P279-star.tsv \
     --root-mode=NONE --rootfilecolumn node1
```

### Basic Blocks

The following file will be used to illustrate some of the capabilities of `kgtk reachable-nodes`.

```bash
kgtk cat -i examples/docs/reachable-nodes-blocks.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| block | isa | thing |
| wood-block | isa | block |
| wood-block | madeof | wood |
| metal-block | isa | block |
| metal-block | madeof | metal |
| oak | isa | wood |
| pine | isa | wood |
| oak-block | isa | wood-block |
| oak-block | madeof | oak |
| pine-block | isa | wood-block |
| pine-block | madeof | pine |
| gold | isa | metal |
| gold-block | isa | metal-block |
| gold-block | madeof | gold |
| silver-block | isa | metal-block |
| silver-block | madeof | silver |

### Find All Nodes Reachable from gold-block

Find the nodes reachable from gold-block.

```bash
kgtk reachable-nodes -i examples/docs/reachable-nodes-blocks.tsv \
     --root gold-block
```

| node1 | label | node2 |
| -- | -- | -- |
| gold-block | reachable | metal-block |
| gold-block | reachable | block |
| gold-block | reachable | thing |
| gold-block | reachable | metal |
| gold-block | reachable | gold |

### Find All Nodes Reachable from gold-block or silver-block Using Spaces

Find the nodes reachable from gold-block or silver-block, using spaces
to separate the root nodes on the command line.

```bash
kgtk reachable-nodes -i examples/docs/reachable-nodes-blocks.tsv \
     --root gold-block silver-block
```

| node1 | label | node2 |
| -- | -- | -- |
| gold-block | reachable | metal-block |
| gold-block | reachable | block |
| gold-block | reachable | thing |
| gold-block | reachable | metal |
| gold-block | reachable | gold |
| silver-block | reachable | metal-block |
| silver-block | reachable | block |
| silver-block | reachable | thing |
| silver-block | reachable | metal |
| silver-block | reachable | silver |

### Find All Nodes Reachable from gold-block or silver-block Using Commas

Find the nodes reachable from gold-block or silver-block, using commas
to separate the root nodes on the command line.

```bash
kgtk reachable-nodes -i examples/docs/reachable-nodes-blocks.tsv \
     --root gold-block,silver-block
```

| node1 | label | node2 |
| -- | -- | -- |
| gold-block | reachable | metal-block |
| gold-block | reachable | block |
| gold-block | reachable | thing |
| gold-block | reachable | metal |
| gold-block | reachable | gold |
| silver-block | reachable | metal-block |
| silver-block | reachable | block |
| silver-block | reachable | thing |
| silver-block | reachable | metal |
| silver-block | reachable | silver |

### Find All Nodes Reachable from gold-block or silver-block Using a Root File

Find the nodes reachable from gold-block or silver-block, using a
root file instead of listing the root nodes on the command line.

In this example, the root file is a KGTK Node file.

```bash
kgtk cat -i examples/docs/reachable-nodes-metal-blocks.tsv
```
| id |
| -- |
| gold-block |
| silver-block |

```bash
kgtk reachable-nodes -i examples/docs/reachable-nodes-blocks.tsv \
    --rootfile examples/docs/reachable-nodes-metal-blocks.tsv

```

| node1 | label | node2 |
| -- | -- | -- |
| gold-block | reachable | metal-block |
| gold-block | reachable | block |
| gold-block | reachable | thing |
| gold-block | reachable | metal |
| gold-block | reachable | gold |
| silver-block | reachable | metal-block |
| silver-block | reachable | block |
| silver-block | reachable | thing |
| silver-block | reachable | metal |
| silver-block | reachable | silver |

### Find All Nodes Reachable from gold-block by the `isa` Property

Find the nodes reachable from gold-block, restricting the analysis to
the `isa` property.

```bash
kgtk reachable-nodes -i examples/docs/reachable-nodes-blocks.tsv \
     --root gold-block --prop isa
```

| node1 | label | node2 |
| -- | -- | -- |
| gold-block | reachable | metal-block |
| gold-block | reachable | block |
| gold-block | reachable | thing |

### Find All Nodes Reachable from gold-block by the `madeof` Property

Find the nodes reachable from gold-block, restricting the analysis to
the `madeof` property.

```bash
kgtk reachable-nodes -i examples/docs/reachable-nodes-blocks.tsv \
     --root gold-block --prop madeof
```

| node1 | label | node2 |
| -- | -- | -- |
| gold-block | reachable | gold |

### Find All Nodes Reachable from gold-block by the `isa` Property as `isa-reachable`

The label in the output file can be controlled with the `--label LABEL` option.

```bash
kgtk reachable-nodes -i examples/docs/reachable-nodes-blocks.tsv \
     --root gold-block --prop isa --label isa-reachable
```

| node1 | label | node2 |
| -- | -- | -- |
| gold-block | isa-reachable | metal-block |
| gold-block | isa-reachable | block |
| gold-block | isa-reachable | thing |

### Adding Selflinks to the Output

Selflinks are links from the root nodes to themselves.  We will repeat the
example "Find All Nodes Reachable from gold-block or silver-block Using Spaces",
but adding selflinks.

```bash
kgtk reachable-nodes -i examples/docs/reachable-nodes-blocks.tsv \
     --root gold-block silver-block --prop isa --selflink
```

| node1 | label | node2 |
| -- | -- | -- |
| gold-block | reachable | gold-block |
| gold-block | reachable | metal-block |
| gold-block | reachable | block |
| gold-block | reachable | thing |
| silver-block | reachable | silver-block |
| silver-block | reachable | metal-block |
| silver-block | reachable | block |
| silver-block | reachable | thing |

Each root node now has a link to itself in the output.  Only
the root nodes have selflinks.

### Starting Partway Up the `isa` Tree

This example shows the output when the root node is partway up
the `isa` property tree.

```bash
kgtk reachable-nodes -i examples/docs/reachable-nodes-blocks.tsv \
     --root metal-block --prop isa
```

| node1 | label | node2 |
| -- | -- | -- |
| metal-block | reachable | block |
| metal-block | reachable | thing |

### Starting Partway Up the `isa` Tree with Undirected Links

This example shows the output when the root node is partway up
the `isa` property tree, but links are considered undirected.

```bash
kgtk reachable-nodes -i examples/docs/reachable-nodes-blocks.tsv \
     --root metal-block --prop isa --undirected
```

| node1 | label | node2 |
| -- | -- | -- |
| metal-block | reachable | block |
| metal-block | reachable | thing |
| metal-block | reachable | wood-block |
| metal-block | reachable | oak-block |
| metal-block | reachable | pine-block |
| metal-block | reachable | gold-block |
| metal-block | reachable | silver-block |


### Starting Partway Up the `isa` or `madeof` Trees

This example shows the output when the root node is partway up
the `isa` property tree, allowing `madeof` links to be considered in
the analysis.

```bash
kgtk reachable-nodes -i examples/docs/reachable-nodes-blocks.tsv \
     --root metal-block --prop isa madeof
```

| node1 | label | node2 |
| -- | -- | -- |
| metal-block | reachable | block |
| metal-block | reachable | thing |
| metal-block | reachable | metal |

Although `modeof` links were considered, they did not contribute to the output.

### Starting Partway Up the `isa` or `madeof` Trees with Undirected Links

This example shows the output when the root node is partway up
the `isa` property tree, allowing `madeof` links to be considered in
the analysis, but when links are considered undirected

```bash
kgtk reachable-nodes -i examples/docs/reachable-nodes-blocks.tsv \
     --root metal-block --prop isa madeof --undirected
```

| node1 | label | node2 |
| -- | -- | -- |
| metal-block | reachable | block |
| metal-block | reachable | thing |
| metal-block | reachable | wood-block |
| metal-block | reachable | wood |
| metal-block | reachable | oak |
| metal-block | reachable | oak-block |
| metal-block | reachable | pine |
| metal-block | reachable | pine-block |
| metal-block | reachable | metal |
| metal-block | reachable | gold |
| metal-block | reachable | gold-block |
| metal-block | reachable | silver-block |
| metal-block | reachable | silver |

With the links considered undirected, the endire graph became reachable
from `metal-block`.

### Expert Example: Showing Graph Properties

The `--show-properties` option is intended for debugging `kgtk reachable-nodes`.
It dicplays some of the properties of the internal graph object that is
constructed to solve the reachability analysis.

```bash
kgtk reachable-nodes -i examples/docs/reachable-nodes-blocks.tsv \
     --root gold-block silver-block --prop isa --show-properties
```

| node1 | label | node2 |
| -- | -- | -- |
| gold-block | reachable | metal-block |
| gold-block | reachable | block |
| gold-block | reachable | thing |
| silver-block | reachable | metal-block |
| silver-block | reachable | block |
| silver-block | reachable | thing |

Here is the additional graph properties output:

    Graph name=<VertexPropertyMap object with value type 'string', for Graph 0x7f09eb8a5c70, at 0x7f09ea2f5280>
    Graph properties:
        ('v', 'name'): <VertexPropertyMap object with value type 'string', for Graph 0x7f09eb8a5c70, at 0x7f09ea2f5280>
        ('e', 'label'): <EdgePropertyMap object with value type 'string', for Graph 0x7f09eb8a5c70, at 0x7f09ea2f51f0>

### Expert Example: Breadth-first Search

By default, the graph is traversed depth first.  `kgtk reachable-nodes --breadth-first`
instructs the command to traverse the graph breadth first. The output should be the same,
but the performace of the two approaches may differ in some cases.

```bash
kgtk reachable-nodes -i examples/docs/reachable-nodes-blocks.tsv \
     --root gold-block silver-block --prop isa --breadth-first
```

| node1 | label | node2 |
| -- | -- | -- |
| gold-block | reachable | metal-block |
| gold-block | reachable | block |
| gold-block | reachable | thing |
| silver-block | reachable | metal-block |
| silver-block | reachable | block |
| silver-block | reachable | thing |

