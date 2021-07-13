## Overview

The `kgtk replace-nodes` command copies its input file to its output file,
substituting item symbols and relationship symbols.  The intended use
for this command is to transform a knowlege graph (KG) from one system
(such as DBpedia) to another system (such as Wikidata).

Other uses are possible.  For example, this command could be used to
substitute strings in a KG, such as replacing strings in one language
with strings in another language.

### The Mapping File

The mapping file contains rules that control the replacements made by the `kgtk replace-nodes` command.
It must be a KGTK edge file with `node1`, `label`, and `node2`
columns, or their aliases.  The `id` column is optional.

The mapping file may optionally have a `confidence` column
(the name of which is controlled by the expert option
`--confidence-column COLUMN_NAME`.

Here are some mapping file examples:

| node1 | label | node2 |
| ----- | ----- | ----- |
| Q001  | same_as_item | X001 |
| isa   | same_as_property | P123 |

| node1 | label | node2 | id |
| ----- | ----- | ----- | -- |
| Q001  | same_as_item | X001 | Q001_item |
| isa   | same_as_property | P123 | isa_property |

| node1 | label | node2 | confidence |
| ----- | ----- | ----- | ---------- |
| Q001  | same_as_item | X001 | 0.9 |
| Q002  | same_as_item | X002 | 0.9 |
| isa   | same_as_property | P123 | |

#### Mapping Actions

There are two mapping actions that may appear in the `label` column
of edges in the mapping file.

   * `same_as_item`: This controls the mapping of values in the
   `node1` and `node2` columns of edges in the input file.

   * `same_as_property`: This controls the mapping of values
   (properties) in the `label` column of edges in the input file.

These two actions may have different label value assigned to them
through the expert options `--same-as-item-label LABEL_VALUE` and
`--same-as-property-label LABEL_VALUE`.

Here is an example:

| node1 | label | node2 |
| ----- | ----- | ----- |
| Q001  | same_as_item | X001 |
| isa   | same_as_property | P123 |


Only these two actions are allowed in the `label` column of the
mapping file.

#### Uniqueness Constraints

For each `node1` value in a `same_as_item` mapping action, there
must be a unique `node2` value.

For each `node1` value in a `same_as_property` mapping action, there
must be a unique `node2` value.

This is not allowed:

| node1 | label | node2 |
| ----- | ----- | ----- |
| Q001  | same_as_item | X001 |
| Q001  | same_as_item | X002 |

By default, duplicate mapping file edges are not allowed even if they do not violate
the uniqueness constraint.  For example, this is not allowed:

| node1 | label | node2 |
| ----- | ----- | ----- |
| Q001  | same_as_item | X001 |
| Q001  | same_as_item | X001 |

The expert option `--allow-exact-duplicates` will allow exact duplicate
maps.

!!! note
    At the present time, uniqueness constraints are applied after
    confidence filtering (see below). This ordering may change in the future.

#### Confidence Filtering

Mapping edges are filtered by confidence value and threshold value (`--threshold THRESHOLD_VALUE`).
The default threshold value is 1.0.

A mapping file may contain an optional `confidence` column.  When a `confidence`
column is present, the edges in the mapping file may contain an optional confidence value.

A confidence value must be an empty value, or a valid integer or floating point number.
By convention, confidence values, when present, are in the range 0 to 1, but other ranges
(e.g., 0 to 100) may be used.

A default confidence value may be specified using the expert option
`--default-confidence-value CONFIDENCE_VALUE`. If this expert option has not been
specified (or has been specified with an empty argument, e.g. `--default-confidence-value=`),
the the default confidence value is the empty value.

When a confidence column is not present, or when a mapping edge hav an empty value
in the confidence column, then the default confidence value is used.

  * If a mapping edge has a confidence value that is empty after applying the default
    confidence value, then this edge always passes the confidence filter and is included
    in the mapping procedure.

  * If a mapping edge has a confidence value that is not empty after applying the default
    confidence value, then the edge will pass the confidence filter if and only if the edge's
    confidence value is greater than or equal to the threshold value.

!!! note
    At the present time, uniqueness constraints (see above) are applied after
    confidence filtering. This ordering may change in the future.

### Memory Usage

The mapping file edges are saved in memory.
This will impose a limit on the size of the mapping files that can be processed.

### Split Output Mode

When the `--split-output-mode` option has been specified, only modified edges
will be sent to the primary output file.  Otherwise, the primary output file
contains all edges from the input file, including unmodified edges (this is called
`full` output mode).

!!! note
    If `--unmodified-edges-file UNMODIFIED_EDGES_FILE` is specified, then the
    unmodified edges will be sent to the unmodified edges output file.

### The Unmodified Edges Output File

When `--unmodified-edges-file UNMODIFIED_EDGES_FILE` is speficied, an
additional output file will be created.  It will have the same shape as
the input file.  It will receive a copy of any input file edges that were not modified by
one or more mapping rules.

When an unmodified edges output file has been specified and full output mode is in effect, unmodified edges will be sent to both the
primary output file and the unmodified edges output file.

When an unmodified edges output file has been specified and split output mode is in effect, unmodified edges will be sent to
only the unmodified edges output file.

When an unmodified edges output file has not been specified and full output mode is in effect, unmodified edges will be sent
to the primary output file.

When an unmodified edges output file has not been specified and split output mode is in effect, unmodified edges will
not be sent to an output file.

### The Activated mapping Edges Output File

When `--activated-mapping-edges-file ACTIVATED_MAPPING_EDGES_FILE` is specified,
then the activated mapping edges output file will contain a copy of the mapping
edges that were applied to at least one input edge.

The activated mapping edges output file will have the same columns and record
order as the mapping file.

## Usage

```
usage: kgtk replace-nodes [-h] [-i INPUT_FILE] [-o OUTPUT_FILE]
                          [--mapping-file INPUT_FILE]
                          [--unmodified-edges-file UNMODIFIED_EDGES_FILE]
                          [--activated-mapping-edges-file ACTIVATED_MAPPING_EDGES_FILE]
                          [--threshold CONFIDENCE_THRESHOLD]
                          [--split-output-mode [True/False]]
                          [-v [optional True|False]]

Lift labels for a KGTK file. For each of the items in the (node1, label, node2) columns, look for matching label records. If found, lift the label values into additional columns in the current record. Label records are reoved from the output. 

Additional options are shown in expert help.
kgtk --expert lift --help

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK input file. (May be omitted or '-' for
                        stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for
                        stdout.)
  --mapping-file INPUT_FILE
                        A KGTK file with mapping records (May be omitted or
                        '-' for stdin.)
  --unmodified-edges-file UNMODIFIED_EDGES_FILE
                        A KGTK output file that will contain unmodified edges.
                        (Optional, use '-' for stdout.)
  --activated-mapping-edges-file ACTIVATED_MAPPING_EDGES_FILE
                        A KGTK output file that will contain activated mapping
                        edges. (Optional, use '-' for stdout.)
  --threshold CONFIDENCE_THRESHOLD
                        The minimum acceptable confidence value. Mapping
                        records with a lower confidence value are excluded.
                        (default=1.000000)
  --split-output-mode [True/False]
                        If true, send only modified edges to the output file.
                        (default=True).

  -v [optional True|False], --verbose [optional True|False]
                        Print additional progress messages (default=False).
```

## Examples

### Sample Data

Suppose that `replace-nodes-input.tsv` contains the following table in KGTK format:

```bash
kgtk cat --input-file examples/docs/replace-nodes-input.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| box1 | isa | box |
| box2 | isa | box |
| box3 | hasa | box |
| box1 | color | red |
| box2 | color | blue |

Suppose that `replace-nodes-mapping1.tsv` contains the following table in KGTK format:

```bash
kgtk cat --input-file examples/docs/replace-nodes-mapping1.tsv
```

| node1 | label | node2 | confidence |
| -- | -- | -- | -- |
| box1 | same_as_item | Q001 | 1.0 |
| box2 | same_as_item | Q002 |  |
| box4 | same_as_item | Q004 |  |
| isa | same_as_property | P1 | 1.0 |

