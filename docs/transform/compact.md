## Overview

The expand command copies its input file to its output file,
compacting repeated items into `|` lists.

### Key Columns

Compaction occurs by grouping records on a set of key columns,
then compacting the records into a single output record.

For KGTK node files, the default key is (`id`).
The `--columns KEY_COLUMN_NAMES ...` option may be used to add additional columns to this list.

For KGTK edge files without an `id` column, the default key is (`node1`, `label`, `node2`).
The `--columns KEY_COLUMN_NAMES ...` option may be used to add additional columns to this list.

For KGTK edge files with an `id` column, the default key is (`node1`, `label`, `node2`, `id`).
The `--columns KEY_COLUMN_NAMES ...` option may be used to add additional columns to this list.
The `--compact-id` option may be used to remove the `id` column from this list.

When `--mode=NONE` is specified, there is no default key.
The `--columns KEY_COLUMN_NAMES ...` option *MUST* be used to add additional columns to this list.

!!! note
    This key column selection behavior is not the same as is used in most
    other KGTK commands.  It may change in the future.

### `id` Generation

`kgtk compact` may be used to generate `id` column values.
The `--id-style` option may be used to select the style of the id.

### Processing Large Files

By default, the input file is sorted in memory to achieve the
grouping necessary for the compaction algorithm. This may cause
memory usage issues for large input files. This may be solved by
sorting the input file using [`kgtk sort`](https:../sort),
then using  `kgtk compact --presorted`.

## Usage

```
usage: kgtk compact [-h] [-i INPUT_FILE] [-o OUTPUT_FILE]
                    [--columns KEY_COLUMN_NAMES [KEY_COLUMN_NAMES ...]]
                    [--compact-id [True|False]] [--presorted [True|False]]
                    [--verify-sort [True|False]]
                    [--lists-in-input [LISTS_IN_INPUT]]
                    [--build-id [True|False]]
                    [--overwrite-id [optional true|false]]
                    [--verify-id-unique [optional true|false]]
                    [--value-hash-width VALUE_HASH_WIDTH]
                    [--claim-id-hash-width CLAIM_ID_HASH_WIDTH]
                    [--claim-id-column-name CLAIM_ID_COLUMN_NAME]
                    [-v [optional True|False]]

Copy a KGTK file, compacting multiple records into | lists. 

By default, the input file is sorted in memory to achieve the grouping necessary for the compaction algorithm. This may cause  memory usage issues for large input files. If the input file has already been sorted (or at least grouped), the `--presorted` option may be used.

Additional options are shown in expert help.
kgtk --expert compact --help

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK input file. (May be omitted or '-' for
                        stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for
                        stdout.)
  --columns KEY_COLUMN_NAMES [KEY_COLUMN_NAMES ...]
                        The key columns to identify records for compaction.
                        (default=id for node files, (node1, label, node2, id)
                        for edge files).
  --compact-id [True|False]
                        Indicate that the ID column in KGTK edge files should
                        be compacted. Normally, if the ID column exists, it is
                        not compacted, as there are use cases that need to
                        maintain distinct lists of secondary edges for each ID
                        value. (default=False).
  --presorted [True|False]
                        Indicate that the input has been presorted (or at
                        least pregrouped) (default=False).
  --verify-sort [True|False]
                        If the input has been presorted, verify its
                        consistency (disable if only pregrouped).
                        (default=True).
  --lists-in-input [LISTS_IN_INPUT]
                        Assume that the input file may contain lists (disable
                        when certain it does not). (default=True).
  --build-id [True|False]
                        Build id values in an id column. (default=False).
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
  --value-hash-width VALUE_HASH_WIDTH
                        How many characters should be used in a value hash?
                        (default=6)
  --claim-id-hash-width CLAIM_ID_HASH_WIDTH
                        How many characters should be used to hash the claim
                        ID? 0 means do not hash the claim ID. (default=8)
  --claim-id-column-name CLAIM_ID_COLUMN_NAME
                        The name of the claim_id column. (default=claim_id)

  -v [optional True|False], --verbose [optional True|False]
                        Print additional progress messages (default=False).
```

## Examples

### Compact with Builtin Sorting

Suppose that `file2.tsv`, which is not presorted,
contains the following table in KGTK format

| node1 | label   | node2 | location  | years |
| ----- | ------- | ----- | --------- | ----- |
| steve | zipcode | 45601 | cabin     |       |
| john  | zipcode | 12345 | home      | 10    |
| steve | zipcode | 45601 |           | 4     |
| john  | zipcode | 12346 |           |       |
| peter | zipcode | 12040 | home      |       |
| steve | zipcode | 45601 | home      | 1     |
| peter | zipcode | 12040 | work      | 5     |
| peter | zipcode | 12040 |           | 6     |
| steve | zipcode | 45601 |           | 3     |
| peter | zipcode | 12040 | cabin     |       |
| steve | zipcode | 45601 |           | 5     |
| steve | zipcode | 45601 | work      | 2     |

Compacting with built-in sorting:
```bash
kgtk compact -i examples/docs/compact-file2.tsv
```

The output will be the following table in KGTK format:

| node1 | label | node2 | location | years |
| -- | -- | -- | -- | -- |
| john | zipcode | 12345 | home | 10 |
| john | zipcode | 12346 |  |  |
| peter | zipcode | 12040 | cabin\|home\|work | 5\|6 |
| steve | zipcode | 45601 | cabin\|home\|work | 1\|2\|3\|4\|5 |

### Compact with Improperly Sorted Imput

This example demonstrates that feeding a non-presorted
file to `kgtk compact --presorted` generates an error.

    ```bash
    kgtk compact -i examples/docs/compact-file2.tsv --presorted
    ```
The output will be the following table  error message:

    Line 3 sort violation going down: prev='johnzipcode12345' curr='stevezipcode45601'

### Compact with Presorted Input

Suppose that `file1.tsv` contains the following table in KGTK format:
(Note:  The `years` column means years employed, not age.)

```bash
kgtk cat -i examples/docs/compact-file1.tsv
```

| node1 | label | node2 | location | years |
| -- | -- | -- | -- | -- |
| john | zipcode | 12345 | home | 10 |
| john | zipcode | 12346 |  |  |
| peter | zipcode | 12040 | home |  |
| peter | zipcode | 12040 | cabin |  |
| peter | zipcode | 12040 | work | 5 |
| peter | zipcode | 12040 |  | 6 |
| steve | zipcode | 45601 |  | 3 |
| steve | zipcode | 45601 |  | 4 |
| steve | zipcode | 45601 |  | 5 |
| steve | zipcode | 45601 | home | 1 |
| steve | zipcode | 45601 | work | 2 |
| steve | zipcode | 45601 | cabin |  |

```bash
kgtk compact -i examples/docs/compact-file1.tsv --presorted
```

The output will be the following table in KGTK format:

| node1 | label | node2 | location | years |
| -- | -- | -- | -- | -- |
| john | zipcode | 12345 | home | 10 |
| john | zipcode | 12346 |  |  |
| peter | zipcode | 12040 | cabin\|home\|work | 5\|6 |
| steve | zipcode | 45601 | cabin\|home\|work | 1\|2\|3\|4\|5 |

### Compact with Default Keys

Suppose that `file3.tsv` contains the following table in KGTK format:

```bash
kgtk cat -i examples/docs/compact-file3.tsv
```

| node1 | label | node2 | id | location | years |
| -- | -- | -- | -- | -- | -- |
| john | zipcode | 12345 | 1 | home | 10 |
| john | zipcode | 12346 | 2 |  |  |
| peter | zipcode | 12040 | 3 | home |  |
| peter | zipcode | 12040 | 4 | cabin |  |
| peter | zipcode | 12040 | 4 | work | 5 |
| peter | zipcode | 12040 | 4 |  | 6 |
| steve | zipcode | 45601 | 5 |  | 3 |
| steve | zipcode | 45601 | 5 |  | 4 |
| steve | zipcode | 45601 | 5 |  | 5 |
| steve | zipcode | 45601 | 6 | home | 1 |
| steve | zipcode | 45601 | 6 | work | 2 |
| steve | zipcode | 45601 | 6 | cabin |  |

Compacting with the tuple (`node1`, `label`, `node2`, `id`) (the default
for a KGTK edge file) as the key:
```bash
kgtk compact -i examples/docs/compact-file3.tsv
```

The output will be the following table in KGTK format:

| node1 | label | node2 | id | location | years |
| -- | -- | -- | -- | -- | -- |
| john | zipcode | 12345 | 1 | home | 10 |
| john | zipcode | 12346 | 2 |  |  |
| peter | zipcode | 12040 | 3 | home |  |
| peter | zipcode | 12040 | 4 | cabin\|work | 5\|6 |
| steve | zipcode | 45601 | 5 |  | 3\|4\|5 |
| steve | zipcode | 45601 | 6 | cabin\|home\|work | 1\|2 |

!!! note
    The default key is (`node1`, `label`, `node2`, `id`).

### Compacting on the ID Column
 
Since the `id` values are not duplicated between (`node1`, `label`, `node2`)
tuples in the previous example, compacting on just the `id` column yields the same results.

```bash
kgtk compact -i examples/docs/compact-file3.tsv --mode=NONE --columns id
```

The output will be the following table in KGTK format:

| node1 | label | node2 | id | location | years |
| -- | -- | -- | -- | -- | -- |
| john | zipcode | 12345 | 1 | home | 10 |
| john | zipcode | 12346 | 2 |  |  |
| peter | zipcode | 12040 | 3 | home |  |
| peter | zipcode | 12040 | 4 | cabin\|work | 5\|6 |
| steve | zipcode | 45601 | 5 |  | 3\|4\|5 |
| steve | zipcode | 45601 | 6 | cabin\|home\|work | 1\|2 |

!!! note
    In order to compact on just the `id` column, it was necessary to
    specify `--mode=NONE`.  This behavior may change in the future.

### Compacting on (`node1`, `label`, `node2`)

Compacting with the tuple (`node1`, `label`, `node2`) as the key (removing
the `id` column from the default for a KGTK edge file):

```bash
kgtk compact -i examples/docs/compact-file3.tsv --compact-id
```

The output will be the following table in KGTK format:

| node1 | label | node2 | id | location | years |
| -- | -- | -- | -- | -- | -- |
| john | zipcode | 12345 | 1 | home | 10 |
| john | zipcode | 12346 | 2 |  |  |
| peter | zipcode | 12040 | 3\|4 | cabin\|home\|work | 5\|6 |
| steve | zipcode | 45601 | 5\|6 | cabin\|home\|work | 1\|2\|3\|4\|5 |


### Building New, Unique IDs for the Compacted Edges.

```bash
kgtk compact -i examples/docs/compact-file3.tsv \
             --build-id --overwrite-id
```

The output will be the following table in KGTK format:

| node1 | label | node2 | id | location | years |
| -- | -- | -- | -- | -- | -- |
| john | zipcode | 12345 | E1 | home | 10 |
| john | zipcode | 12346 | E2 |  |  |
| peter | zipcode | 12040 | E3 | home |  |
| peter | zipcode | 12040 | E4 | cabin\|work | 5\|6 |
| steve | zipcode | 45601 | E5 |  | 3\|4\|5 |
| steve | zipcode | 45601 | E6 | cabin\|home\|work | 1\|2 |

### Building New, Unique IDs for the Compacted Edges, Compacting the ID column, Too.

```bash
kgtk compact -i examples/docs/compact-file3.tsv \
             --build-id --overwrite-id --compact-id
```

The output will be the following table in KGTK format:

| node1 | label | node2 | id | location | years |
| -- | -- | -- | -- | -- | -- |
| john | zipcode | 12345 | E1 | home | 10 |
| john | zipcode | 12346 | E2 |  |  |
| peter | zipcode | 12040 | E3 | cabin\|home\|work | 5\|6 |
| steve | zipcode | 45601 | E4 | cabin\|home\|work | 1\|2\|3\|4\|5 |


### Expert Example: Using `--id-style=node1-label-node2`

Using the expert option `--id-style=node1-label-node2`, you can generate IDs
that concatenate (node1, label, node2).

```bash
kgtk compact -i examples/docs/compact-file3.tsv \
             --build-id --overwrite-id --compact-id \
	     --id-style=node1-label-node2
```

The output will be the following table in KGTK format:

| node1 | label | node2 | id | location | years |
| -- | -- | -- | -- | -- | -- |
| john | zipcode | 12345 | john-zipcode-12345 | home | 10 |
| john | zipcode | 12346 | john-zipcode-12346 |  |  |
| peter | zipcode | 12040 | peter-zipcode-12040 | cabin\|home\|work | 5\|6 |
| steve | zipcode | 45601 | steve-zipcode-45601 | cabin\|home\|work | 1\|2\|3\|4\|5 |

### Expert Example: Using `--id-style=node1-label-node2-num`

```bash
kgtk compact -i examples/docs/compact-file3.tsv \
             --build-id --overwrite-id --compact-id \
	     --id-style=node1-label-node2-num
```
The output will be the following table in KGTK format:

| node1 | label | node2 | id | location | years |
| -- | -- | -- | -- | -- | -- |
| john | zipcode | 12345 | john-zipcode-12345-0000 | home | 10 |
| john | zipcode | 12346 | john-zipcode-12346-0000 |  |  |
| peter | zipcode | 12040 | peter-zipcode-12040-0000 | cabin\|home\|work | 5\|6 |
| steve | zipcode | 45601 | steve-zipcode-45601-0000 | cabin\|home\|work | 1\|2\|3\|4\|5 |

### Expert Example: Using `--id-style=node1-label-node2-id`

```bash
kgtk compact -i examples/docs/compact-file3.tsv \
             --build-id --overwrite-id --compact-id \
	     --id-style=node1-label-node2-id
```
The output will be the following table in KGTK format:

| node1 | label | node2 | id | location | years |
| -- | -- | -- | -- | -- | -- |
| john | zipcode | 12345 | john-zipcode-12345-1 | home | 10 |
| john | zipcode | 12346 | john-zipcode-12346-2 |  |  |
| peter | zipcode | 12040 | peter-zipcode-12040-3\|4 | cabin\|home\|work | 5\|6 |
| steve | zipcode | 45601 | steve-zipcode-45601-5\|6 | cabin\|home\|work | 1\|2\|3\|4\|5 |
