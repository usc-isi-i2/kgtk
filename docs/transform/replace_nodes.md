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
`--confidence-column COLUMN_NAME`).

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
   `node1` and `node2` columns of edges from the input file.

   * `same_as_property`: This controls the mapping of values
   (properties) in the `label` column of edges from the input file.

These two actions may have different `label` values assigned to them
through the expert options `--same-as-item-label LABEL_VALUE` and
`--same-as-property-label LABEL_VALUE`.

Here is an example using the default `label` values:

| node1 | label | node2 |
| ----- | ----- | ----- |
| Q001  | same_as_item | X001 |
| isa   | same_as_property | P123 |


Only these two actions are allowed in the `label` column of the
mapping file.  Error messages will be issued if other `label`
values ae found, and processing will abort before reading the
input file.

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

A confidence value must be an empty value or a valid integer or floating point number.
By convention, confidence values, when present, are in the range 0.0 to 1.0, but other ranges
(e.g., 0 to 100) may be used.

A default confidence value may be specified using the expert option
`--default-confidence-value CONFIDENCE_VALUE`. If this expert option has not been
specified (or has been specified with an empty argument, e.g. `--default-confidence-value=`),
the the default confidence value is the empty value.

When a confidence column is not present, or when a mapping edge has an empty value
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

!!! note
    When the expert option `--require-confidence` is specified, the `confidence` column
    is required and must contain non-empty values. 

#### Idempotent Mapping Rules

A mapping rule that maps a `node1` value in an input edge to itself is called an
`idempotent mapping rule`.  Idempotent mapping rules are discarded when the
mapping file is read unless the expert option `--allow-idempotent-mapping` has
been specified.

When idempotent mapping rules are allowed, input edges that satisfy an idempotent
mapping rule will be considered `modified` (see below), even though the values in the edge
are unchanged, and the mapping edge will be considered `activated` (see below).
There may be some circumstances in which this is the desired behavior, and
other circumstances in which the default behavior is preferred.  See the expert example,
below.

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

### Significant Modifications

By default, a "modified edge" means an edge with a change in any
of the fields that are subject to replacement.  By default, this means
a change to any of the `node`, `label`, `node2` fields.

However, there are circumstances in which you are interested in other
modification patterns. The expert option `--modified-pattern MODIFIED_PATTERN` provides control over
which fields must be modified for an edge to be considered to have been modified.

| MODIFIED_PATTERN | Description |
| ---------------- | ----------- |
| `node1`          | Only the `node1` field matters. |
| `label`          | Only the `label` field matters. |
| `node2 `         | Only the `node2` field matters. |
| `node1\|label`    | A modification to the `node1` or `label` fields. |
| `node1\|node2`    | A modification to the `node1` or `node2` fields. |
| `label\|node2`    | A modification to the `label` or `node2` fields. |
| `node1\|label\|node2` | A modification to the `node1`, `label`, or `node2` fields. This is the default. |
| `node1&label`    | The `node1` and `label` fields are both modified. |
| `node1&node2`    | The `node1` and `node2` fields are both modified. |
| `label&node2`    | The `label` and `node2` fields are both modified. |
| `node1&label&node2` | The `node1`, `label`, and `node2` fields are all modified. |

For example, you may be performing a `same_as_item`
modification, and expect both `node1` and `node2` to be modified in every
record.  You can achieve this with `--modified-pattern node1&node2`

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

!!! note
    When `--allow-idempotent-actions` has been specified, an input edge that
    satisfies an idenpotent mapping rule will be treated as a modified edge,
    even when the output edge has the same values as it did on input.

### The Activated Mapping Edges Output File

When `--activated-mapping-edges-file ACTIVATED_MAPPING_EDGES_FILE` is specified,
then the activated mapping edges output file will contain a copy of the mapping
edges that were applied to at least one input edge.

The activated mapping edges output file will have the same columns and record
order as the mapping file.

### The Rejected Mapping Edges Output File

When `--rejected-mapping-edges-file REJECTED_MAPPING_EDGES_FILE` is specified,
then the rejected mapping edges output file will contain a copy of the mapping
edges that were rejected due to a confidence value that did not meet the threshold value.

The rejected mapping edges output file will have the same columns and record
order as the mapping file.

## Usage

```
usage: kgtk replace-nodes [-h] [-i INPUT_FILE] [-o OUTPUT_FILE]
                          [--mapping-file INPUT_FILE]
                          [--unmodified-edges-file UNMODIFIED_EDGES_FILE]
                          [--activated-mapping-edges-file ACTIVATED_MAPPING_EDGES_FILE]
                          [--rejected-mapping-edges-file REJECTED_MAPPING_EDGES_FILE]
                          [--threshold CONFIDENCE_THRESHOLD]
                          [--split-output-mode [True/False]]
                          [-v [optional True|False]]

Replace item and relationship values to move a network from one symbol set to another. 

Additional options are shown in expert help.
kgtk --expert replace-nodes --help

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
  --rejected-mapping-edges-file REJECTED_MAPPING_EDGES_FILE
                        A KGTK output file that will contain rejected mapping
                        edges. (Optional, use '-' for stdout.)
  --threshold CONFIDENCE_THRESHOLD
                        The minimum acceptable confidence value. Mapping
                        records with a lower confidence value are excluded.
                        (default=1.000000)
  --split-output-mode [True/False]
                        If true, send only modified edges to the output file.
                        (default=False).

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

### Apply the Mapping with Full Output

```bash
kgtk replace-nodes \
     --input-file examples/docs/replace-nodes-input.tsv \
     --mapping-file examples/docs/replace-nodes-mapping1.tsv
     
```

| node1 | label | node2 |
| -- | -- | -- |
| Q001 | P1 | box |
| Q002 | P1 | box |
| box3 | hasa | box |
| Q001 | color | red |
| Q002 | color | blue |

### Apply the Mapping with Split Output

The output stream will not contain any unmodified edges.

```bash
kgtk replace-nodes \
     --input-file examples/docs/replace-nodes-input.tsv \
     --mapping-file examples/docs/replace-nodes-mapping1.tsv \
     --split-output-mode
     
```

| node1 | label | node2 |
| -- | -- | -- |
| Q001 | P1 | box |
| Q002 | P1 | box |
| Q001 | color | red |
| Q002 | color | blue |

### Apply the Mapping with an Unmodified Edges Output File

The unmodified edges output file will receive a copy of the unmodified edges
from the input file.  The unmodified edges will also be sent to the primary
output file, unliess `--split-output-mode` is specifed.

```bash
kgtk replace-nodes \
     --input-file examples/docs/replace-nodes-input.tsv \
     --mapping-file examples/docs/replace-nodes-mapping1.tsv \
     --unmodified-edges-file replace-nodes-unmodified.tsv
     
```

| node1 | label | node2 |
| -- | -- | -- |
| Q001 | P1 | box |
| Q002 | P1 | box |
| box3 | hasa | box |
| Q001 | color | red |
| Q002 | color | blue |


Here is the unmodified edges output file:

```bask
kgtk cat -i replace-nodes-unmodified.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| box3 | hasa | box |

### Apply the Mapping with an Unmodified Edges Output File and Split Output

The unmodified edges output file will receive a copy of the unmodified edges
from the input file.  The unmodified edges will not be sent to the primary
output file because `--split-output-mode` is specifed.

```bash
kgtk replace-nodes \
     --input-file examples/docs/replace-nodes-input.tsv \
     --mapping-file examples/docs/replace-nodes-mapping1.tsv \
     --unmodified-edges-file replace-nodes-unmodified.tsv \
     --split-output-mode
     
```

| node1 | label | node2 |
| -- | -- | -- |
| Q001 | P1 | box |
| Q002 | P1 | box |
| Q001 | color | red |
| Q002 | color | blue |


Here is the unmodified edges output file:

```bask
kgtk cat -i replace-nodes-unmodified.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| box3 | hasa | box |

### Apply the Mapping with an Activated Mapping Edges Output File

```bash
kgtk replace-nodes \
     --input-file examples/docs/replace-nodes-input.tsv \
     --mapping-file examples/docs/replace-nodes-mapping1.tsv \
     --activated-mapping-edges-file replace-nodes-activated.tsv
     
```

| node1 | label | node2 |
| -- | -- | -- |
| Q001 | P1 | box |
| Q002 | P1 | box |
| box3 | hasa | box |
| Q001 | color | red |
| Q002 | color | blue |


Here is the activated mapping edges output file:

```bash
kgtk cat -i replace-nodes-activated.tsv
```

| node1 | label | node2 | confidence |
| -- | -- | -- | -- |
| box1 | same_as_item | Q001 | 1.0 |
| box2 | same_as_item | Q002 |  |
| isa | same_as_property | P1 | 1.0 |

### Apply the Mapping with a Rejected Mapping Edges Output File

Here is a mapping file with confidence values:

```bash
kgtk cat -i examples/docs/replace-nodes-mapping8.tsv
```

| node1 | label | node2 | confidence |
| -- | -- | -- | -- |
| box1 | same_as_item | Q001 | 1.0 |
| box2 | same_as_item | Q002 | .9 |
| box4 | same_as_item | Q004 | .8 |
| isa | same_as_property | P1 | 1.0 |

```bash
kgtk replace-nodes \
     --input-file examples/docs/replace-nodes-input.tsv \
     --mapping-file examples/docs/replace-nodes-mapping8.tsv \
     --threshold .95 \
     --rejected-mapping-edges-file replace-nodes-rejected.tsv
     
```

| node1 | label | node2 |
| -- | -- | -- |
| Q001 | P1 | box |
| box2 | P1 | box |
| box3 | hasa | box |
| Q001 | color | red |
| box2 | color | blue |


Here is the rejected mapping edges output file:

```bash
kgtk cat -i replace-nodes-rejected.tsv
```

| node1 | label | node2 | confidence |
| -- | -- | -- | -- |
| box2 | same_as_item | Q002 | .9 |
| box4 | same_as_item | Q004 | .8 |

### Multiple Input Files

`kgtk replace-nodes` takes a single primary input file.
If you want to process the concatenation of several input files,
use `kgtk cat` to combine them first.

Here is a second input file:

```bash
kgtk cat -i examples/docs/replace-nodes-input2.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| box11 | isa | box |
| box12 | isa | box |
| box13 | isa | box |
| box11 | color | green |
| box12 | color | yellow |
| box13 | color | cyan |

Combining our two input files and processing them
together:

```bash
kgtk cat -i examples/docs/replace-nodes-input.tsv \
            examples/docs/replace-nodes-input2.tsv \
   / replace-nodes \
     --mapping-file examples/docs/replace-nodes-mapping1.tsv
     
```

| node1 | label | node2 |
| -- | -- | -- |
| Q001 | P1 | box |
| Q002 | P1 | box |
| box3 | hasa | box |
| Q001 | color | red |
| Q002 | color | blue |
| box11 | P1 | box |
| box12 | P1 | box |
| box13 | P1 | box |
| box11 | color | green |
| box12 | color | yellow |
| box13 | color | cyan |


### Expert Example: The Case for Idempotent Mapping

Suppose that you want to map property `isa` in the input file
to property `P1` in the output file.  Here's a mapping file:

```bash
kgtk cat -i examples/docs/replace-nodes-mapping2.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| isa | same_as_property | P1 |

Applying this to our input file, and splitting the results, we get:

```bash
kgtk replace-nodes \
     --input-file examples/docs/replace-nodes-input.tsv \
     --mapping-file examples/docs/replace-nodes-mapping2.tsv \
     --unmodified-edges-file replace-nodes-unmodified.tsv \
     --split-output-mode
```

| node1 | label | node2 |
| -- | -- | -- |
| box1 | P1 | box |
| box2 | P1 | box |

Here are the unmodified edges:

```bash
kgtk cat -i replace-nodes-unmodified.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| box3 | hasa | box |
| box1 | color | red |
| box2 | color | blue |

There are two unmapped properties: `hasa` and `color`.  Suppose
that it is OK to leave `hasa` as-is, but we want to identify any
records with a property other than `isa` or `hasa` (represented in the
input file by the `color` property).

Clearly, you could do this with a `kgtk filter` command, if the
number of properties is small and known ahead of tile.  Consider:

```bash
kgtk filter -i examples/docs/replace-nodes-input.tsv \
     --pattern ";isa,hasa;" --invert
```

| node1 | label | node2 |
| -- | -- | -- |
| box1 | color | red |
| box2 | color | blue |

On the other hand, using `kgtk filter` may be less attractive if the
number of properties being handled is large, and/or is determined
as a result of prior processing steps.

Here is a mapping file that adds an itempotent mapping rule for `hasa`:

```bash
kgtk cat -i examples/docs/replace-nodes-mapping3.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| isa | same_as_property | P1 |
| hasa | same_as_property | hasa |

Apply this mapping to the input file, allowing idempotent mapping rules:

```bash
kgtk replace-nodes \
     --input-file examples/docs/replace-nodes-input.tsv \
     --mapping-file examples/docs/replace-nodes-mapping3.tsv \
     --unmodified-edges-file replace-nodes-unmodified.tsv \
     --split-output-mode \
     --allow-idempotent-mapping
```

| node1 | label | node2 |
| -- | -- | -- |
| box1 | P1 | box |
| box2 | P1 | box |
| box3 | hasa | box |

Here are the unmodified edges:

```bash
kgtk cat -i replace-nodes-unmodified.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| box1 | color | red |
| box2 | color | blue |

We've isolated the edges with the "unknown" `color` property.

### Expert Example: Expecting Modifications to Both `node1` and `node2`

Let's assume that we are mapping only items, and we expect every item to be mapped.

Here is the mapping file:

```bash
kgtk cat -i examples/docs/replace-nodes-mapping4.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| box | same_as_item | Q000 |
| box1 | same_as_item | Q001 |
| box2 | same_as_item | Q002 |
| box4 | same_as_item | Q004 |
| red | same_as_item | Q006 |
| blue | same_as_item | Q007 |

Applying this mapping file:

```bash
kgtk replace-nodes \
     --input-file examples/docs/replace-nodes-input.tsv \
     --mapping-file examples/docs/replace-nodes-mapping4.tsv \
     --unmodified-edges-file replace-nodes-unmodified.tsv \
     --split-output-mode \
     --modified-pattern 'node1&node2'
```

| node1 | label | node2 |
| -- | -- | -- |
| Q001 | isa | Q000 |
| Q002 | isa | Q000 |
| Q001 | color | Q006 |
| Q002 | color | Q007 |

Here are the unmodified edges:

```bash
kgtk cat -i replace-nodes-unmodified.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| box3 | hasa | box |

The `box3` item was not defined in the mapping file.

### Expert Example: Requiring Confidence Values

Using the `--require-confidence` option, we can require
non-empty confidence values.

Consider the following mapping file, which does not contain
a `confidence` column:

```bash
kgtk cat -i examples/docs/replace-nodes-mapping2.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| isa | same_as_property | P1 |

Applying this to our input file, and requiring confidence:

```bash
kgtk replace-nodes \
     --input-file examples/docs/replace-nodes-input.tsv \
     --mapping-file examples/docs/replace-nodes-mapping2.tsv \
     --unmodified-edges-file replace-nodes-unmodified.tsv \
     --require-confidence
```

We get the following error message:

    The mapping file does not have a confidence column, and confidence is required.

Conside the following mappping file, which contains a `confidence`
column, but for which some confidence values ae missing:

```bash
kgtk cat --input-file examples/docs/replace-nodes-mapping1.tsv
```

| node1 | label | node2 | confidence |
| -- | -- | -- | -- |
| box1 | same_as_item | Q001 | 1.0 |
| box2 | same_as_item | Q002 |  |
| box4 | same_as_item | Q004 |  |
| isa | same_as_property | P1 | 1.0 |

Applying this to our input file, and requiring confidence:

```bash
kgtk replace-nodes \
     --input-file examples/docs/replace-nodes-input.tsv \
     --mapping-file examples/docs/replace-nodes-mapping1.tsv \
     --require-confidence
     
```
We get the following error messages:

    In line 2 of the mapping file: the required confidence value is missing
    In line 3 of the mapping file: the required confidence value is missing
    2 errors detected in the mapping file 'examples/docs/replace-nodes-mapping1.tsv'

### Expert Example: Replacing Other Columns

`kgtk replace-nodes` can be used to replace values in columns other than
`node1`, `label`, and `node2` (or their aliases), using the following options:

`--node1-column COLUMN_NAME`
`--label-column COLUMN_NAME`
`--node2-column COLUMN_NAME`

Using a `same_as_item` mapping rule, you can update values in two columns at once.  Using a
`same_as_property` mapping rule, you can update values in a single column.

Consider the following input file, which is not a KGTK edge or node file:

```bash
kgtk cat --mode=NONE -i examples/docs/replace-nodes-input3.tsv
```
| item | rel | shape |
| -- | -- | -- |
| box1 | isa | box |
| box2 | isa | box |
| box3 | isa | box |

Apply mapping rules to that file as follows:

```bash
kgtk replace-nodes \
     --input-file examples/docs/replace-nodes-input3.tsv \
     --input-mode NONE \
     --node1-column item \
     --label-column rel \
     --node2-column shape \
     --mapping-file examples/docs/replace-nodes-mapping1.tsv
     
```

| item | rel | shape |
| -- | -- | -- |
| Q001 | P1 | box |
| Q002 | P1 | box |
| box3 | P1 | box |

### Expert Example: Mapping Rules in Other Columns

`kgtk replace-nodes` can extract mapping rules from columns other than
`node1`, `label`, and `node2` (or their aliases), using the following options:

`--mapping-node1-column COLUMN_NAME`
`--mapping-label-column COLUMN_NAME`
`--mapping-node2-column COLUMN_NAME`

Consider the following mapping file, which is not a KGTK edge or node file:

```bash
kgtk cat --mode=NONE -i examples/docs/replace-nodes-mapping5.tsv
```
| item | transform | replacement |
| -- | -- | -- |
| box1 | same_as_item | Q001 |
| box2 | same_as_item | Q002 |
| box4 | same_as_item | Q004 |
| isa | same_as_property | P1 |

Apply this mapping rule file as follows:

```bash
kgtk replace-nodes \
     --input-file examples/docs/replace-nodes-input.tsv \
     --mapping-file examples/docs/replace-nodes-mapping5.tsv \
     --mapping-mode NONE \
     --mapping-node1-column item \
     --mapping-label-column transform \
     --mapping-node2-column replacement     
```

| node1 | label | node2 |
| -- | -- | -- |
| Q001 | P1 | box |
| Q002 | P1 | box |
| box3 | hasa | box |
| Q001 | color | red |
| Q002 | color | blue |

### Expert Example: Simplified same-as-item Mapping Rules

Suppose you have a file with two columns for item replacement:
the original item symbol and the replacement item symbol.

The expert option `--mapping-rule-mode same-as-item`
causes `kgt-replace-nodes` to ignore the `label` column
in the mapping file and assume that all `node1`->`node2`
maps are item maps.  Property maps will not be performed.

```bash
kgtk cat --mode=NONE -i examples/docs/replace-nodes-mapping6.tsv
```

| item | replacement |
| -- | -- |
| box | Q000 |
| box1 | Q001 |
| box2 | Q002 |
| box4 | Q004 |

Apply this mapping rule file as follows:

```bash
kgtk replace-nodes \
     --input-file examples/docs/replace-nodes-input.tsv \
     --mapping-file examples/docs/replace-nodes-mapping6.tsv \
     --mapping-mode NONE \
     --mapping-rule-mode same-as-item \
     --mapping-node1-column item \
     --mapping-node2-column replacement     
```

| node1 | label | node2 |
| -- | -- | -- |
| Q001 | isa | Q000 |
| Q002 | isa | Q000 |
| box3 | hasa | Q000 |
| Q001 | color | red |
| Q002 | color | blue |

### Expert Example: Simplified same-as-property Mapping Rules

Suppose you have a file with two columns for property replacement:
the original property symbol and the replacement property symbol.

The expert option `--mapping-rule-mode same-as-property`
causes `kgt-replace-nodes` to ignore the `label` column
in the mapping file and assume that all `node1`->`node2`
maps are property maps.  Item maps will not be performed.

```bash
kgtk cat --mode=NONE -i examples/docs/replace-nodes-mapping7.tsv
```

| property | replacement |
| -- | -- |
| isa | P1 |

Apply this mapping rule file as follows:

```bash
kgtk replace-nodes \
     --input-file examples/docs/replace-nodes-input.tsv \
     --mapping-file examples/docs/replace-nodes-mapping7.tsv \
     --mapping-mode NONE \
     --mapping-rule-mode same-as-property \
     --mapping-node1-column property \
     --mapping-node2-column replacement     
```

| node1 | label | node2 |
| -- | -- | -- |
| box1 | P1 | box |
| box2 | P1 | box |
| box3 | hasa | box |
| box1 | color | red |
| box2 | color | blue |
