## Summary

This command will find all nodes reachable from given root nodes in a input file.
Given a set of nodes N and a set of properties P, this command computes the set of nodes R
that can be reached from N via paths containing any of the properties in P.

### Input File

The input file should be a KGTK Edge file with the following columns or their aliases:

- `node1`: the subject column (source node)
- `label`: the predicate column (property name)
- `node2`: the object column (target node)

### Column Substitutions

Optionally, other columns may be used as the subject/predicate/object columns using the following
command line options:

- `--subj SUBJECT_COLUMN_NAME`: the name of the subject column (default: `node1`).
- `--pred PREDICATE_COLUMN_NAME`: the name of the predicate column (default: `label`).
- `--obj OBJECT_COLUMN_NAME`: the name of the object column (default: `node2`).

### Processing an Input File that is Not a KGTK Edge File

If your input file doesn't have `node1`, `label`, or `node2` columns (or their aliases) at all, then it is
not a valid KGTK Edge file.  In this case, you also have to pass the following command line option:

- `--input-mode=NONE`

### Root Node File

The root node file, if specified with `--root-file ROOTFILE`, is used to get the list of starting nodes for the reachability analysis.
It should be a valid KGTK file.

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

- `--root-mode=NONE`
- `--rootfilecolumn COLUMN_NAME`

If the argument to `--rootfilecolumn` is an integer, then it is treated
as a 0's-origin index into the root file's columns (e.g., the first column is nomber 0, the second column is number 1,
etc.)

### Root Nodes on the Command Line

The set of root nodes can also be specified on the command line, using the following command option:
- `--root ROOT [ROOT ...]`

Each `ROOT` group can be a comma-separated list of root node names.

Note: a comma-separated list should not have spaces before or after the comma(s).

Note: this implies that commas are not allowed in node names on the command line.  At the present time, there is
no option to override this constraint.

Both `--root` and `--rootfile` may be specified, in which case the root node set is the union of
the nodes from the root file and the nodes from the command line.

### The Output File

The output file is an edge file that contains the following columns:

- `node1`: this column contains a root node
- `label`: this column contains only 'reachable'
- `node2`: this column contains node that is reachable from a root node

### Limiting the Properties Traversed

By default, "kgtk reachable-nodes` will perform its analysis using all properties (values in
the `label` column or its alias or substitution) found in the input file.

It is possible to limit the properties traversed using a file or on the command line.

### Limiting the Properties Traversed from a File

The property file, if specified with `--props-file ROOTFILE`, is used to get the list of property names to traverse for the reachability analysis.
It should be a valid KGTK file.

- If the property file is a KGTK Edge file (containing at least `node1`, `label`, and `node2` columns, or their aliases),
  then the unique values in the `node1` column (by default) will be used to build the set of property names.
- If the property file is a KGTK Node file (containing at least an `id` column or its alias,
  and not containing a `node1` column or its alias), then the unique values in the `id` column (by default) will be
  used to build the set of property names.

If the property file is a valid KGTK Edge or Node file, but you want to use a different column name than the defaults
shown above, then the `--propsfilecolumn COLUMN_NAME` option may be used to specify the name of the column property file
that contains the property names.

If the property file is not a valid KGTK Edge or Node file, but can be parsed by KgtkReader (it is a
valid tab-separated file), the it is necessary to speficy the following options:

- `--props-mode=NONE`
- `--propsfilecolumn COLUMN_NAME`

If the argument to `--propsfilecolumn` is an integer, then it is treated
as a 0's-origin index into the root file's columns (e.g., the first column is nomber 0, the second column is number 1,
etc.)

### Limiting the Properties Traversed on the Command Line

To limit the set of properties on the command line, use the fillowing command option:
- `--props PROPS [ PROPS ...]`

Each `PROPS` group can be a comma-separated list of root node names.

Note: a comma-separated list should not have spaces before or after the comma(s).

Note: this implies that commas are not allowed in property names on the command line.  At the present time, there is
no option to override this constraint.

Both `--props` and `--props-file` may be specified, in which case the property name set is the union of
the names from the property file and the names from the command line.

### Directionality

`kgtk reachable-nodes` normally traces reachability from node1 to node2 (`node1->node2`).

### Inverted Directionality

When `--inverted` is True, all relationships are reversed, and reachability is
traced from node2 to node1 (`node1<-node2`).

`--inverted-props INVERTED_PROPS [INVERTED_PROPS ...]` may be used to specify certain properties (values in the
`label` column or its alias or substitution) that are to be reversed.  Each INVERTED_PROPS group
can be a comma-separated list of property names.

Note: a comma-separated list should not have spaces before or after the comma(s).

Note: Commas are not allowed in property names in INVERTED_PROPS.  At the present time, there is
no option to override this constraint.

Note: `--inverted` and `--inverted-props` may not be used together.

Note: If you want only certain props to be considered, and you want them inverted, then you need
to specify *both* `--props` (and/or `--props-file`) and `--inverted-props` (and/or `--inverted-props-file`).  

- `--props P249 --inverted-props P249` # Consider only P249, an inverted prop.
- `--props P249 P731 --inverted-props P249` # Consider both P249 and P731, with P249 inverted.
- `--inverted-props P249` # Since `--props` was not specified, *all* properties are used, with P249 inverted.

`--inverted-props-file INVERTED_PROPS_FILE` can be used to read a file containing a list of
properties to invert.   It should be a valid KGTK file.

- If the inverted properties file is a KGTK Edge file (containing at least `node1`, `label`, and `node2` columns, or their aliases),
  then the unique values in the `node1` column (by default) will be used to build the set of inverted property names.
- If the inverted properties file is a KGTK Node file (containing at least an `id` column or its alias,
  and not containing a `node1` column or its alias), then the unique values in the `id` column (by default) will be
  used to build the set of inverrted property names.

If the inverted properties file is a valid KGTK Edge or Node file, but you want to use a different column name than the defaults
shown above, then the `--invertedpropsfilecolumn COLUMN_NAME` option may be used to specify the name of the inverted properties file column
containing the inverted properties.

If the inverted properties file is not a valid KGTK Edge or Node file, but can be parsed by KgtkReader (it is a
valid tab-separated file), the it is necessary to speficy the following options:

- `--inverted-props-mode=NONE`
- `--invertedpropsfilecolumn COLUMN_NAME`

If the argument to `--invertedpropsfilecolumn` is an integer, then it is treated
as a 0's-origin index into the inverted property file's columns (e.g., the first column is nomber 0, the second column is number 1,
etc.)

Note: `--inverted` and `--inverted-props-file` may not be used together.

### Undirected Directionality

When `--undirected` is True, all relationships are treated as undirected (bidirectional).
Reachablity is traced from node1 to node2 and from node2 to node1 (`node`<->node2`).

`--undirected-props UNDIRECTED_PROPS [UNDIRECTED_PROPS ...]` may be used to specify certain properties (values in the
`label` column or its alias or substitution) that are to be treated as undirected (bidirectional).  Each UNDIRECTED_PROPS group
can be a comma-separated list of property names.

Note: a comma-separated list should not have spaces before or after the comma(s).

Note: Commas are not allowed in property names in UNDIRECTED_PROPS.  At the present time, there is
no option to override this constraint.

Note: `--undirected` and `--undirected-props` may not be used together.

`--undirected-props-file UNDIRECTED_PROPS_FILE` can be used to read a file containing a list of
properties to invert.   It should be a valid KGTK file.

- If the undirected properties file is a KGTK Edge file (containing at least `node1`, `label`, and `node2` columns, or their aliases),
  then the unique values in the `node1` column (by default) will be used to build the set of undirected property names.
- If the undirected properties file is a KGTK Node file (containing at least an `id` column or its alias,
  and not containing a `node1` column or its alias), then the unique values in the `id` column (by default) will be
  used to build the set of inverrted property names.

If the undirected properties file is a valid KGTK Edge or Node file, but you want to use a different column name than the defaults
shown above, then the `--undirectedpropsfilecolumn COLUMN_NAME` option may be used to specify the name of the undirected properties file column
containing the undirected properties.

If the undirected properties file is not a valid KGTK Edge or Node file, but can be parsed by KgtkReader (it is a
valid tab-separated file), the it is necessary to speficy the following options:

- `--undirected-props-mode=NONE`
- `--undirectedpropsfilecolumn COLUMN_NAME`

If the argument to `--undirectedpropsfilecolumn` is an integer, then it is treated
as a 0's-origin index into the undirected property file's columns (e.g., the first column is nomber 0, the second column is number 1,
etc.)

Note: `--undirected` and `--undirected-props-file` may not be used together.

## Usage
```
usage: kgtk reachable-nodes [-h] [-i INPUT_FILE] [-o OUTPUT_FILE]
                            [--root [ROOT [ROOT ...]]] [--root-file ROOTFILE]
                            [--rootfilecolumn ROOTFILECOLUMN]
                            [--subj SUBJECT_COLUMN_NAME]
                            [--obj OBJECT_COLUMN_NAME]
                            [--pred PREDICATE_COLUMN_NAME]
                            [--prop [PROPS [PROPS ...]]]
                            [--props-file PROPS_FILE]
                            [--propsfilecolumn PROPSFILECOLUMN]
                            [--inverted [True|False]]
                            [--inverted-prop [INVERTED_PROPS [INVERTED_PROPS ...]]]
                            [--inverted-props-file INVERTED_PROPS_FILE]
                            [--invertedpropsfilecolumn INVERTEDPROPSFILECOLUMN]
                            [--undirected [True|False]]
                            [--undirected-prop [UNDIRECTED_PROPS [UNDIRECTED_PROPS ...]]]
                            [--undirected-props-file UNDIRECTED_PROPS_FILE]
                            [--undirectedpropsfilecolumn UNDIRECTEDPROPSFILECOLUMN]
                            [--label LABEL] [--selflink [True|False]]
                            [--show-properties [True|False]]
                            [--breadth-first [True|False]]
                            [--depth-limit DEPTH_LIMIT]
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
  --prop [PROPS [PROPS ...]], --props [PROPS [PROPS ...]]
                        Properties to consider while finding reachable nodes,
                        space- or comma-separated string. (default: all
                        properties)
  --props-file PROPS_FILE
                        Option to specify a file containing the set of
                        properties
  --propsfilecolumn PROPSFILECOLUMN
                        Specify the name or number of the props file column
                        with the property names. (default=node1 or its alias
                        if edge file, id if node file)
  --inverted [True|False]
                        When True, and when --undirected is False, invert the
                        source and target nodes in the graph. (default=False)
  --inverted-prop [INVERTED_PROPS [INVERTED_PROPS ...]], --inverted-props [INVERTED_PROPS [INVERTED_PROPS ...]]
                        Properties to invert, space- or comma-separated
                        string. (default: no properties)
  --inverted-props-file INVERTED_PROPS_FILE
                        Option to specify a file containing the set of
                        inverted properties
  --invertedpropsfilecolumn INVERTEDPROPSFILECOLUMN
                        Specify the name or number of the inverted props file
                        column with the property names. (default=node1 or its
                        alias if edge file, id if node file)
  --undirected [True|False]
                        When True, specify graph as undirected.
                        (default=False)
  --undirected-prop [UNDIRECTED_PROPS [UNDIRECTED_PROPS ...]], --undirected-props [UNDIRECTED_PROPS [UNDIRECTED_PROPS ...]]
                        Properties to treat as undirected, space- or comma-
                        separated string. (default: no properties)
  --undirected-props-file UNDIRECTED_PROPS_FILE
                        Option to specify a file containing the set of
                        undirected properties
  --undirectedpropsfilecolumn UNDIRECTEDPROPSFILECOLUMN
                        Specify the name or number of the undirected props
                        file column with the property names. (default=node1 or
                        its alias if edge file, id if node file)
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
  --depth-limit DEPTH_LIMIT
                        An optional depth limit for breadth-first searches.
                        (default=None)

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
kgtk reachable-nodes -i P279.tsv --rootfile P31.tsv --rootfilecolumn node2 -o P279-star.tsv
```

### Nonstandard Root File

Suppose that the root file has only a `node1` column, making it neither a KGTK Edge file nor a KGTK Node file.
The following command may be used to process it:

```
kgtk reachable-nodes -i P279.tsv --rootfile P31.tsv --rootfilecolumn node2 -o P279-star.tsv \
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

### Find All Nodes Reachable from gold-block by the `isa` Property from a File

Find the nodes reachable from gold-block, restricting the analysis to
the `isa` property.  Get the name of the property from a file.

```bash
kgtk reachable-nodes -i examples/docs/reachable-nodes-blocks.tsv \
     --root gold-block \
     --props-file examples/docs/reachable-nodes-isa-prop.tsv
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

### Starting Partway Up the `isa` Tree with Inverted Links

Invert the direction of the reachability analysis.  All properties
(`label` column values) are treated as inverted.

```bash
kgtk reachable-nodes -i examples/docs/reachable-nodes-blocks.tsv \
     --root metal-block --prop isa --inverted
```

| node1 | label | node2 |
| -- | -- | -- |
| metal-block | reachable | gold-block |
| metal-block | reachable | silver-block |

### Starting Partway Up the `isa` Tree with Specific Inverted Links

Invert the direction of the reachability analysis for a specific property
(`label` column value).

```bash
kgtk reachable-nodes -i examples/docs/reachable-nodes-blocks.tsv \
     --root metal-block --prop isa --inverted-prop isa
```

| node1 | label | node2 |
| -- | -- | -- |
| metal-block | reachable | gold-block |
| metal-block | reachable | silver-block |

Note: `--inverted` and `--inverted-props` may not be requested at the same time.

### Starting Partway Up the `isa` Tree with Specific Inverted Links from a File

Invert the direction of the reachability analysis for a specific property
(`label` column value).

```bash
kgtk reachable-nodes -i examples/docs/reachable-nodes-blocks.tsv \
     --root metal-block --prop isa \
     --inverted-props-file examples/docs/reachable-nodes-isa-prop.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| metal-block | reachable | gold-block |
| metal-block | reachable | silver-block |

Note: `--inverted` and `--inverted-props-file` may not be requested at the same time.

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


### Starting Partway Up the `isa` Tree with Specific Undirected Links

Invert the direction of the reachability analysis for a specific property
(`label` column value).

```bash
kgtk reachable-nodes -i examples/docs/reachable-nodes-blocks.tsv \
     --root metal-block --prop isa --undirected-prop isa
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

Note: `--undirected` and `--undirected-props` may not be requested at the same time.

### Starting Partway Up the `isa` Tree with Specific Undirected Links from a File

Invert the direction of the reachability analysis for a specific property
(`label` column value).

```bash
kgtk reachable-nodes -i examples/docs/reachable-nodes-blocks.tsv \
     --root metal-block --prop isa \
     --undirected-props-file examples/docs/reachable-nodes-isa-prop.tsv
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

Note: `--undirected` and `--undirected-props-file` may not be requested at the same time.

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

Although `modeof` links were considered, they did not contribute to the output
because they were not reachable.

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

### Starting Partway Up the `isa` Tree Again

```bash
kgtk reachable-nodes -i examples/docs/reachable-nodes-blocks.tsv \
     --root gold
```

| node1 | label | node2 |
| -- | -- | -- |
| gold | reachable | metal |

### Starting Partway Up the `isa` Tree Again with `madeof` Inverted

```bash
kgtk reachable-nodes -i examples/docs/reachable-nodes-blocks.tsv \
     --root gold --inverted-prop madeof
```

| node1 | label | node2 |
| -- | -- | -- |
| gold | reachable | metal |
| gold | reachable | metal-block |
| gold | reachable | block |
| gold | reachable | thing |
| gold | reachable | gold-block |

### Starting Partway Up the `isa` Tree Again with `madeof` Undirected

```bash
kgtk reachable-nodes -i examples/docs/reachable-nodes-blocks.tsv \
     --root gold --undirected-prop madeof
```

| node1 | label | node2 |
| -- | -- | -- |
| gold | reachable | metal |
| gold | reachable | metal-block |
| gold | reachable | block |
| gold | reachable | thing |
| gold | reachable | gold-block |

Note: `--undirected` and `--undirected-props` may not be requested at the same time.

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

    Graph name=<VertexPropertyMap object with value type 'string', for Graph 0x7f6b6c8ec760, at 0x7f6b6c8ecac0>
    Graph properties:
        ('v', 'name'): <VertexPropertyMap object with value type 'string', for Graph 0x7f6b6c8ec760, at 0x7f6b6c8ecac0>
        ('e', 'label'): <EdgePropertyMap object with value type 'string', for Graph 0x7f6b6c8ec760, at 0x7f6b6c8eca30>

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

### Expert Example: Depth Limited Breadth-first Search

Consider the following graph:

```bash
kgtk cat -i examples/docs/reachable-nodes-depth-limit.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| red_top | is-connected-to | red_one |
| red_one | is-connected-to | red_two |
| red_two | is-connected-to | red_three |
| red_three | is-connected-to | red_four |
| red_four | is-connected-to | red_five |

Let's look at connections breadth-first:

```bash
kgtk reachable-nodes -i examples/docs/reachable-nodes-depth-limit.tsv \
     --root red_top --prop is-connected-to \
     --breadth-first --depth-limit 10
```

| node1 | label | node2 |
| -- | -- | -- |
| red_top | reachable | red_one |
| red_top | reachable | red_two |
| red_top | reachable | red_three |
| red_top | reachable | red_four |
| red_top | reachable | red_five |

```bash
kgtk reachable-nodes -i examples/docs/reachable-nodes-depth-limit.tsv \
     --root red_top --prop is-connected-to \
     --breadth-first --depth-limit 3
```

| node1 | label | node2 |
| -- | -- | -- |
| red_top | reachable | red_one |
| red_top | reachable | red_two |
| red_top | reachable | red_three |

```bash
kgtk reachable-nodes -i examples/docs/reachable-nodes-depth-limit.tsv \
     --root red_top --prop is-connected-to \
     --breadth-first --depth-limit 1
```

| node1 | label | node2 |
| -- | -- | -- |
| red_top | reachable | red_one |
