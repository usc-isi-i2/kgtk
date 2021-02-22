## Overview

### `kgtk normalize`

`kgtk normalize` removes additional columns from a KGTK edge file.
It implements two column removal patterns:

  * It reverses `kgtk lift`, then
  * it converts the remaining additional columns to normalized secondary edges.

### `kgtk lower`

This alias for `kgtk normalize` removes additional columns from a KGTK edge file,
reversing `kgtk lift`.  It does not convert other additional columns to secondary edges.

### `kgtk normalize-edges`

This alias for `kgtk normalize` converts all (or selected) additional columns
in a KGTK edge file to secondary edges.

### [`kgtk normalize-nodes`](../normalize_nodes)

[`kgtk normalize-nodes`](../normalize_nodes) converts KGTK node files to normalized
KGTK edge files.

!!! note
    [`kgtk normalize-nodes`](../normalize_nodes) is currently implemented as a seperate
    command.  In the future, `kgtk normalize` may provide the same functionality when the
    input file is a KGTK node file, with `kgtk normalize-nodes` as an alias.

### Reversing Default `kgtk lift`

By default, `kgtk lift` creates the following lifted columns:

 * `node1;label`
 * `label;label`
 * `node2;label`

The following input file:

| node1 | label | node2 | node1;label | label;label | node2;label |
| --- | --- | --- | --- | --- | --- |
| Q1  | P1 | Q2 | item1 | isa | group1 |

Would be transformed by `kgtk lower` into:

| node1 | label | node2 |
| --- | --- | --- |
| Q1 | P1 | Q2 |
| Q1 | label | item1 |
| Q2 | label | group1 |
| P1 | label | isa |

### Conversion to Secondary Edges Requires `id`

If converting additional columns to secondary edges is requested via `kgtk normalize-edges`
or `kgtk normalize --normalize` (the default), the input KGTK edge file
must contain an `id` column.

!!! note
    In the future, there may be an option to generate `id` values on input edges as needed.
    Until then, use the [`kgtk add-id`](../add_id) command to generate
    `id` field values prior to `kgtk normalize-edges`.

###  Converting Additional Columns to Normalized Secondary Edges

Additional columns that aren't lowered may ba converted to
normalized secondary edges.

The following input file:	   

| id | node1 | label | node2 | confidence | reference |
| --- | --- | --- | --- | --- | --- |
| E1 | Q1  | P1 | Q2 | 0.9 | Wikidata |

Would be transformed by `kgtk normalize-edges` to:

| id | node1 | label | node2 |
| -- | ----- | ----- | ----- |
| E1 | Q1 | P1         | Q2 |
|    | E1 | confidence | 0.9 |
|    | E1 | reference  | Wikidata |

!!! note
    The newly generated secondary edges do not themselves have `id` fields.
    In the future, there may be an option to generate `id` values on output edges as needed.
    Until then, use the [`kgtk add-id`](../add_id) command to generate
    `id` field values after `kgtk normalize-edges`.

### Selecting the Additional Columns to Normalize

The `--columns` option may be used to select the columns to normalize.
This option has the aliases `--columns-to-lower` and `--columns-to-remove`,
which may be used to increase the legibility of scripts that use the
`kgtk normalize` command or its aliases.

Additional columns that are not selected for normalization are passed through
to the output file.

### Sending New Edges to a Seperate File

By default, newly created edges are sent to the primary output file,
along with edges from the input file.

`--new-edges-file NEW_EDGES_FILE` may be used to route newly created edges
to a seperate file.

### Deduplicating New Edges

By default, newly created edges are deduplicated.  The first instance
generated is written to the appropriate output file (either the standard output
file or the new edges output file).

`--deduplicate False` disables new edge deduplication.

### Deduplication Memory Usage

Deduplication uses an in-memory dictionary.  It is not suitable for use
with processing large files with large numbers of unique newly-generated edges.
In this case, use [`kgtk sort`](../sort) and [`kgtk compact`](../compact) to deduplicate the new
edges as additional processing steps.

`kgtk normalize --deduplicate-new-edges ... / sort / compact`

### Expanding Lists

List of values in additional columns being lowered/normalized are expanded into seperate output
edges for each nonempty element of the list.

!!! note
    This is required by the [KGTK File Format v2.0](../../specification),
    which prohibits lists in the `node2` column.


## Usage

```
usage: kgtk normalize [-h] [-i INPUT_FILE] [-o OUTPUT_FILE]
                      [--new-edges-file NEW_EDGES_FILE]
                      [--columns COLUMNS_TO_LOWER [COLUMNS_TO_LOWER ...]]
                      [--lower [True|False]] [--normalize [True|False]]
                      [--deduplicate-new-edges [True|False]]
                      [-v [optional True|False]]

Normalize a KGTK edge file by removing columns that match a "lift" pattern and converting remaining additional columns to new edges.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK input file. (May be omitted or '-' for
                        stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for
                        stdout.)
  --new-edges-file NEW_EDGES_FILE
                        An optional output file for new edges (normalized
                        and/or lowered). If omitted, new edges will go in the
                        main output file. (Optional, use '-' for stdout.)
  --columns COLUMNS_TO_LOWER [COLUMNS_TO_LOWER ...], --columns-to-lower COLUMNS_TO_LOWER [COLUMNS_TO_LOWER ...], --columns-to-remove COLUMNS_TO_LOWER [COLUMNS_TO_LOWER ...]
                        Columns to lower and remove as a space-separated list.
                        (default=all columns other than key columns)
  --lower [True|False]  When True, lower columns that match a lift pattern.
                        (default=True)
  --normalize [True|False]
                        When True, normalize columns that do not match a lift
                        pattern. (default=True)
  --deduplicate-new-edges [True|False]
                        When True, deduplicate new edges. Not suitable for
                        large files. (default=True).

  -v [optional True|False], --verbose [optional True|False]
                        Print additional progress messages (default=False).
```

## Examples

### Sample Data

Suppose `file1`.tsv` contains the following table in KGTK format:

```bash
kgtk cat -i examples/docs/normalize-file1.tsv
```

| node1 | label | node2 | node1;label | label;label | node2;label |
| -- | -- | -- | -- | -- | -- |
| Q1 | P1 | Q5 | "Elmo" | "instance of" | "homo sapiens"\|"human" |
| Q1 | P2 | Q6 | "Elmo" | "amigo"\|"friend" | "Fred" |
| Q6 | P1 | Q5 | "Fred" | "instance of" | "homo sapiens"\|"human" |

!!! note
    This file was generated using [`kgtk lift`](../lift):
    
    kgtk lift --input-file examples/docs/lift-file4.tsv -o examples/docs/normalize-file1.tsv

### Reversing `kgtk lift` with `kgtk lower`

```bash
kgtk lower -i examples/docs/normalize-file1.tsv
```
| node1 | label | node2 |
| -- | -- | -- |
| Q1 | P1 | Q5 |
| Q1 | label | "Elmo" |
| P1 | label | "instance of" |
| Q5 | label | "homo sapiens" |
| Q5 | label | "human" |
| Q1 | P2 | Q6 |
| P2 | label | "amigo" |
| P2 | label | "friend" |
| Q6 | label | "Fred" |
| Q6 | P1 | Q5 |

!!! note
    The `node1;label`, `label;label`, and `node2;label` columns were
    recognized as lift-pattern additional columns.  They were removed
    from the output file and their contents generated as label records.

!!! note
    The list `"amigo"|"friend"` in the input file generated two output records.

### Reversing `kgtk lift` with `kgtk lower` and Without Deduplication

```bash
kgtk lower -i examples/docs/normalize-file1.tsv \
           --deduplicate-new-edges False
```
| node1 | label | node2 |
| -- | -- | -- |
| Q1 | P1 | Q5 |
| Q1 | label | "Elmo" |
| P1 | label | "instance of" |
| Q5 | label | "homo sapiens" |
| Q5 | label | "human" |
| Q1 | P2 | Q6 |
| Q1 | label | "Elmo" |
| P2 | label | "amigo" |
| P2 | label | "friend" |
| Q6 | label | "Fred" |
| Q6 | P1 | Q5 |
| Q6 | label | "Fred" |
| P1 | label | "instance of" |
| Q5 | label | "homo sapiens" |
| Q5 | label | "human" |

### Reversing `kgtk lift` with `kgtk lower / sort /compact`

```bash
kgtk lower -i examples/docs/normalize-file1.tsv \
           --deduplicate-new-edges False \
   / sort \
   / compact
```
| node1 | label | node2 |
| -- | -- | -- |
| P1 | label | "instance of" |
| P2 | label | "amigo" |
| P2 | label | "friend" |
| Q1 | P1 | Q5 |
| Q1 | P2 | Q6 |
| Q1 | label | "Elmo" |
| Q5 | label | "homo sapiens" |
| Q5 | label | "human" |
| Q6 | P1 | Q5 |
| Q6 | label | "Fred" |

!!! note
    This processing pipeline is suitable for use with larger files.
    Typically, additional parameters will be passed to `kgtk sort`
    to control the number of threads use, the amount of main memory
    used, and the filesystem location for temporary files.  These
    details have been omitted for clarity.

### Reversing Just `kgtk lift` with `kgtk normalize`

```bash
kgtk normalize -i examples/docs/normalize-file1.tsv \
               --normalize False
```

| node1 | label | node2 |
| -- | -- | -- |
| Q1 | P1 | Q5 |
| Q1 | label | "Elmo" |
| P1 | label | "instance of" |
| Q5 | label | "homo sapiens" |
| Q5 | label | "human" |
| Q1 | P2 | Q6 |
| P2 | label | "amigo" |
| P2 | label | "friend" |
| Q6 | label | "Fred" |
| Q6 | P1 | Q5 |

!!! note
    `--normalize False` is required because the input file does not have an `id` column.

### Directing New Edges to a Seperate File

```bash
kgtk lower -i examples/docs/normalize-file1.tsv \
           --new-edges new.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| Q1 | P1 | Q5 |
| Q1 | P2 | Q6 |
| Q6 | P1 | Q5 |

```bash
kgtk cat -i new.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| Q1 | label | "Elmo" |
| P1 | label | "instance of" |
| Q5 | label | "homo sapiens" |
| Q5 | label | "human" |
| P2 | label | "amigo" |
| P2 | label | "friend" |
| Q6 | label | "Fred" |

### Sample Data with `id` and a Non-lift Additional Column

Suppose `file2`.tsv` contains the following table in KGTK format:

```bash
kgtk cat -i examples/docs/normalize-file2.tsv
```

| node1 | label | node2 | node1;label | label;label | node2;label | id | confidence |
| -- | -- | -- | -- | -- | -- | -- | -- |
| Q1 | P1 | Q5 | "Elmo" | "instance of" | "homo sapiens"\|"human" | E1 | 0.3 |
| Q1 | P2 | Q6 | "Elmo" | "amigo"\|"friend" | "Fred" | E2 | 0.9 |
| Q6 | P1 | Q5 | "Fred" | "instance of" | "homo sapiens"\|"human" | E3 | 0.8 |

### Normalizing Both Lift and Non-lift Additional Columns

```bash
kgtk normalize -i examples/docs/normalize-file2.tsv
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| Q1 | P1 | Q5 | E1 |
| Q1 | label | "Elmo" |  |
| P1 | label | "instance of" |  |
| Q5 | label | "homo sapiens" |  |
| Q5 | label | "human" |  |
| E1 | confidence | 0.3 |  |
| Q1 | P2 | Q6 | E2 |
| P2 | label | "amigo" |  |
| P2 | label | "friend" |  |
| Q6 | label | "Fred" |  |
| E2 | confidence | 0.9 |  |
| Q6 | P1 | Q5 | E3 |
| E3 | confidence | 0.8 |  |

!!! note
    The additional columns have been removed from the output
    file.  Their contents appear as a mixture of label edges
    and secondary edges.

### Normalizing Just a Non-lift Additional Column

Let's normalize just the non-lift additional column:

```bash
kgtk normalize-edges -i examples/docs/normalize-file2.tsv \
                     --columns-to-remove confidence
```

| node1 | label | node2 | node1;label | label;label | node2;label | id |
| -- | -- | -- | -- | -- | -- | -- |
| Q1 | P1 | Q5 | "Elmo" | "instance of" | "homo sapiens"\|"human" | E1 |
| E1 | confidence | 0.3 |  |  |  |  |
| Q1 | P2 | Q6 | "Elmo" | "amigo"\|"friend" | "Fred" | E2 |
| E2 | confidence | 0.9 |  |  |  |  |
| Q6 | P1 | Q5 | "Fred" | "instance of" | "homo sapiens"\|"human" | E3 |
| E3 | confidence | 0.8 |  |  |  |  |

!!! note
    The `confidence` column has been removed from the output file.
    Its contents appear as new secondary edges.


### Normalizing a Non-lift Additional Column and Adding IDs

Let's normalize just the non-lift additional column:
To avoid generating the same ID values as existing IDs,
the newly generated edge IDs are generated with the prefix `N`

```bash
kgtk normalize-edges -i examples/docs/normalize-file2.tsv \
                     --columns-to-remove confidence \
  / add-id --id-prefix N
```

| node1 | label | node2 | node1;label | label;label | node2;label | id |
| -- | -- | -- | -- | -- | -- | -- |
| Q1 | P1 | Q5 | "Elmo" | "instance of" | "homo sapiens"\|"human" | E1 |
| E1 | confidence | 0.3 |  |  |  | N1 |
| Q1 | P2 | Q6 | "Elmo" | "amigo"\|"friend" | "Fred" | E2 |
| E2 | confidence | 0.9 |  |  |  | N2 |
| Q6 | P1 | Q5 | "Fred" | "instance of" | "homo sapiens"\|"human" | E3 |
| E3 | confidence | 0.8 |  |  |  | N3 |


### Normalizing a Non-lift Additional Column and Adding IDs with an Initial ID

Let's normalize just the non-lift additional column.
To avoid generating the same ID values as existing IDs,
the newly generated edge IDs are generated with the initial value `E100`.

```bash
kgtk normalize-edges -i examples/docs/normalize-file2.tsv \
                     --columns-to-remove confidence \
  / add-id --initial-id 100
```

| node1 | label | node2 | node1;label | label;label | node2;label | id |
| -- | -- | -- | -- | -- | -- | -- |
| Q1 | P1 | Q5 | "Elmo" | "instance of" | "homo sapiens"\|"human" | E1 |
| E1 | confidence | 0.3 |  |  |  | E100 |
| Q1 | P2 | Q6 | "Elmo" | "amigo"\|"friend" | "Fred" | E2 |
| E2 | confidence | 0.9 |  |  |  | E101 |
| Q6 | P1 | Q5 | "Fred" | "instance of" | "homo sapiens"\|"human" | E3 |
| E3 | confidence | 0.8 |  |  |  | E102 |

### Reversing `kgtk lift` with Other Labels

Suppose `file3`.tsv` contains the following table in KGTK format:

```bash
kgtk cat -i examples/docs/normalize-file3.tsv
```

| node1 | label | node2 | node1;name | label;relationship | node2;name |
| -- | -- | -- | -- | -- | -- |
| Q1 | P1 | Q5 | "Elmo" | "instance of" | "homo sapiens"\|"human" |
| Q1 | P2 | Q6 | "Elmo" | "amigo"\|"friend" | "Fred" |
| Q6 | P1 | Q5 | "Fred" | "instance of" | "homo sapiens"\|"human" |

Lowering the additional columns with default settings:

```bash
kgtk lower -i examples/docs/normalize-file3.tsv

```

| node1 | label | node2 |
| -- | -- | -- |
| Q1 | P1 | Q5 |
| Q1 | name | "Elmo" |
| P1 | relationship | "instance of" |
| Q5 | name | "homo sapiens" |
| Q5 | name | "human" |
| Q1 | P2 | Q6 |
| P2 | relationship | "amigo" |
| P2 | relationship | "friend" |
| Q6 | name | "Fred" |
| Q6 | P1 | Q5 |

### Expert Example: Lowering with Base Columns

Suppose `file4`.tsv` contains the following table in KGTK format:

```bash
kgtk cat -i examples/docs/normalize-file4.tsv
```

| node1 | label | node2 | color | material | size |
| -- | -- | -- | -- | -- | -- |
| block1 | isa | cube | red | wood | large |
| block2 | isa | pyramid | blue | steel | small |

In this case, the additional columns `color`, `material`, and `size` are
all attributes of the entity in `node`, but without the `node1;` prefix.

These columns can be lowered by supplying a base column for each
column to be lowered using the expert option `--base-columns BASE_COLUMNS ...`.
The columns to be lowered must be specified with `--columns COLUMNS_TO_LOWER`
(or an alias to this option), and there must be one base column specified for each
column to lower.

```bash
kgtk lower -i examples/docs/normalize-file4.tsv \
           --columns      color material size \
	   --base-columns node1  node1   node1
```
| node1 | label | node2 |
| -- | -- | -- |
| block1 | isa | cube |
| block1 | color | red |
| block1 | material | wood |
| block1 | size | large |
| block2 | isa | pyramid |
| block2 | color | blue |
| block2 | material | steel |
| block2 | size | small |

!!! note
    Another approach would be to rename the columns on input to names
    such as `node1;color`.
    
    See [`kgtk cat`](../cat) for am example of renaming columns
    on input.

### Expert Example: Lowering with Base Columns and Label Values

Suppose `file4`.tsv` contains the following table in KGTK format:

```bash
kgtk cat -i examples/docs/normalize-file4.tsv
```

| node1 | label | node2 | color | material | size |
| -- | -- | -- | -- | -- | -- |
| block1 | isa | cube | red | wood | large |
| block2 | isa | pyramid | blue | steel | small |

In this case, the additional columns `color`, `material`, and `size` are
all attributes of the entity in `node`, but without the `node1;` prefix.

These columns can be lowered by supplying a base column for each
column to be lowered using the expert option `--base-columns BASE_COLUMNS ...`.
The columns to be lowered must be specified with `--columns COLUMNS_TO_LOWER`
(or an alias to this option), and there must be one base column specified for each
column to lower.

Furthermore, suppose that the relationships in the label edges must be all capital
letters.  The expert option `--label-values LABEL_VALUES ...]` can be
used to supply the label values to use.  There must be one label value specified
for each column to lower.

```bash
kgtk lower -i examples/docs/normalize-file4.tsv \
           --columns      color material size \
	   --base-columns node1  node1   node1 \
	   --label-values COLOR MATERIAL SIZE
```
| node1 | label | node2 |
| -- | -- | -- |
| block1 | isa | cube |
| block1 | COLOR | red |
| block1 | MATERIAL | wood |
| block1 | SIZE | large |
| block2 | isa | pyramid |
| block2 | COLOR | blue |
| block2 | MATERIAL | steel |
| block2 | SIZE | small |

!!! note
    Another approach would be to rename the columns on input to names
    such as `node1;COLOR`.
    
    See [`kgtk cat`](../cat) for am example of renaming columns
    on input.
