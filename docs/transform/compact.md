## Overview

### `kgtk compact`

The compact command copies its input file to its output file, compacting
repeated items into [multi-valued edges (`|` lists)](../../specification#multi-valued-edges).
Compact is intended to operate on KGTK node
files or on the additional columns of KGTK denormalized edge files.
It should not be used to compact the `node2` column of a KGTK edge file.

### `kgtk deduplicate`

`kgtk deduplicate` is an alias for `kgtk compact --deduplicate`.  In this mode,
duplicate edges are removed without compacting any columns into
[multi-valued edges (`|` lists)](../../specification#multi-valued-edges).

!!! note
    If you wish to use deduplicate mode with a presorted input file, the
    sort key needs to be the entire set of columns in the input file in
    the order in which they appear in the file.

    If it is difficult to ascertain the order in which columns appear in
    the input file, an alternative approach is to list all the column names
    in some order to the sort command, then list them in that order to
    `kgtk compact --columns`.

### Creating Multi-value Edges

Suppose you have a KGTK edge file such as:

| node1 | label | node2 | genre|
| --- | --- | --- | --- |
| terminator2_jd | isa | movie | science_fiction |
| terminator2_jd | isa | movie | action |

The compacted result would be:

| node1 | label | node2 | genre |
| --- | --- | --- | --- |
| terminator2_jd | isa | movie | action\|science_fiction |

!!! note
    The key columns (see below) in this example are (`node1`, `label`, `node2`).

### Key Columns

Compaction occurs by grouping records on a set of key columns,
then compacting the records into a single output record.

When `--deduplicate=TRUE`, all columns will be used as key columns, in the order in which they appear
in the input file's header record.  This overrides `--columns` and `--compact-id`.

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
    The key column order with an `id` column is not the same as is used in most
    other KGTK commands.  It may change in the future.

### `id` Generation

`kgtk compact` may be used to generate `id` column values.
The expert option `--id-style` may be used to select the style of the id.
See the [`kgtk add-id`](../add_id) command for adidtional
details on `--id-style` and related options.

### Processing Large Files

By default, the input file is sorted in memory to achieve the
grouping necessary for the compaction algorithm. This may cause
memory usage issues for large input files. This may be solved by
sorting the input file using [`kgtk sort`](../sort),
then using  `kgtk compact --presorted`.

### Compacting `node2` Is Discouraged

If you have a KGTK edge file with normalized edges (no additional columns),
you might want to compact the `node2` column using (`node1`, `label`) as the
key.

For example, using movies as the topic:

| node1 | label | node2 |
| --- | --- | --- |
| terminator2_jd | genre | science_fiction |
| terminator2_jd | genre | action |

You intend to create:

| node1 | label | node2 |
| --- | --- | --- |
| terminator2_jd | genre | action\|science_fiction |

This would result in an invalid KGTK file, as the `node2` column is
not allowed to contain multi-value edges (`|` lists) according to the
[KGTK File Specification](../../specification#multi-valued-edges).

!!! note
    If you insist on compacting the `node2` column, you can do so using:

    `kgtk compact --mode=NONE --columns node1 label`

## Usage

```
usage: kgtk compact [-h] [-i INPUT_FILE] [-o OUTPUT_FILE]
                    [--columns KEY_COLUMN_NAMES [KEY_COLUMN_NAMES ...]]
                    [--compact-id [True|False]] [--deduplicate [True|False]]
                    [--lists-in-input [LISTS_IN_INPUT]]
                    [--presorted [True|False]] [--verify-sort [True|False]]
                    [--build-id [True|False]]
                    [--overwrite-id [optional true|false]]
                    [--verify-id-unique [optional true|false]]
                    [--value-hash-width VALUE_HASH_WIDTH]
                    [--claim-id-hash-width CLAIM_ID_HASH_WIDTH]
                    [--claim-id-column-name CLAIM_ID_COLUMN_NAME]
                    [--id-separator ID_SEPARATOR] [-v [optional True|False]]

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
  --deduplicate [True|False]
                        Treat all columns as key columns, overriding --columns
                        and --compact-id. This will remove completely
                        duplicate records without compacting any new lists.
                        (default=False).
  --lists-in-input [LISTS_IN_INPUT]
                        Assume that the input file may contain lists (disable
                        when certain it does not). (default=True).
  --presorted [True|False]
                        Indicate that the input has been presorted (or at
                        least pregrouped) (default=False).
  --verify-sort [True|False]
                        If the input has been presorted, verify its
                        consistency (disable if only pregrouped).
                        (default=True).
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
  --id-separator ID_SEPARATOR
                        The separator user between ID subfields. (default=-)

  -v [optional True|False], --verbose [optional True|False]
                        Print additional progress messages (default=False).
```

## Examples

### Compact with Builtin Sorting

Suppose that `file2.tsv`, which is not presorted,
contains the following table in KGTK format:

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

### Compact with Improperly Sorted Input

This example demonstrates that feeding a non-presorted
file to `kgtk compact --presorted` generates an error.

```bash
kgtk compact -i examples/docs/compact-file2.tsv --presorted
```

The output will begin with the following on stdout:

| node1 | label | node2 | location | years |
| -- | -- | -- | -- | -- |
| steve | zipcode | 45601 | cabin |  |

The output will end with the following error message on stderr:

    Line 3 sort violation going down: prev='john|zipcode|12345' curr='steve|zipcode|45601'

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

### Compact with External Sorting, No `id`

This example demonstrates a pipeline that sorts edges without an `id` field,
using [`kgtk sort`](../sort), before `kgtk compact`:

```base
kgtk sort -i examples/docs/compact-file2.tsv \
   / compact --presorted
```

The output will be the following table in KGTK format:

| node1 | label | node2 | location | years |
| -- | -- | -- | -- | -- |
| john | zipcode | 12345 | home | 10 |
| john | zipcode | 12346 |  |  |
| peter | zipcode | 12040 | cabin\|home\|work | 5\|6 |
| steve | zipcode | 45601 | cabin\|home\|work | 1\|2\|3\|4\|5 |

!!! note
    Normally, additional options would be passed to `kgtk sort` to
    control the amount of memory used, the maximum number of threads,
    and the location of the temporary files.

### Compact with External Sorting, with `id`

Suppose that `file5.tsv` contains the following table in KGTK format:

```bash
kgtk cat -i examples/docs/compact-file5.tsv
```

| id | node1 | label | node2 | location | years |
| -- | -- | -- | -- | -- | -- |
| E01 | steve | zipcode | 45601 | cabin |  |
| E02 | john | zipcode | 12345 | home | 10 |
| E03 | steve | zipcode | 45601 |  | 4 |
| E04 | john | zipcode | 12346 |  |  |
| E05 | peter | zipcode | 12040 | home |  |
| E06 | steve | zipcode | 45601 | home | 1 |
| E07 | peter | zipcode | 12040 | work | 5 |
| E08 | peter | zipcode | 12040 |  | 6 |
| E09 | steve | zipcode | 45601 |  | 3 |
| E10 | peter | zipcode | 12040 | cabin |  |
| E11 | steve | zipcode | 45601 |  | 5 |
| E12 | steve | zipcode | 45601 | work | 2 |

This example demonstrates a pipeline that sorts edges with an `id` field,
using [`kgtk sort`](../sort), before `kgtk compact`:

```base
kgtk sort -i examples/docs/compact-file5.tsv \
   / compact --presorted \
             --columns id node1 label node2
```

The output will be the following table in KGTK format:

| id | node1 | label | node2 | location | years |
| -- | -- | -- | -- | -- | -- |
| E01 | steve | zipcode | 45601 | cabin |  |
| E02 | john | zipcode | 12345 | home | 10 |
| E03 | steve | zipcode | 45601 |  | 4 |
| E04 | john | zipcode | 12346 |  |  |
| E05 | peter | zipcode | 12040 | home |  |
| E06 | steve | zipcode | 45601 | home | 1 |
| E07 | peter | zipcode | 12040 | work | 5 |
| E08 | peter | zipcode | 12040 |  | 6 |
| E09 | steve | zipcode | 45601 |  | 3 |
| E10 | peter | zipcode | 12040 | cabin |  |
| E11 | steve | zipcode | 45601 |  | 5 |
| E12 | steve | zipcode | 45601 | work | 2 |

!!! note
    `kgtk compact` and `kgtk sort` use different default key
    column orders for KGTK edge files with an `id` column, so it
    is necessary to specify `--columns` for one or both of the
    commands. This behavior may change in the future.

!!! note
    Normally, additional options would be passed to `kgtk sort` to
    control the amount of memory used, the maximum number of threads,
    and the location of the temporary files.

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
kgtk compact -i examples/docs/compact-file3.tsv --columns id
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


### Deduplication with Builtin Sorting

Suppose that `file4.tsv` contains the following table in KGTK format,
which is not presorted and which contains some duplicate lines:

```bash
kgtk cat -i examples/docs/compact-file4.tsv
```

| node1 | label | node2 | location | years |
| -- | -- | -- | -- | -- |
| john | zipcode | 12345 | home | 10 |
| steve | zipcode | 45601 | work | 2 |
| john | zipcode | 12346 |  |  |
| peter | zipcode | 12040 | home |  |
| peter | zipcode | 12040 | cabin |  |
| john | zipcode | 12345 | home | 10 |
| peter | zipcode | 12040 | work | 5 |
| peter | zipcode | 12040 |  | 6 |
| steve | zipcode | 45601 |  | 3 |
| steve | zipcode | 45601 |  | 3 |
| peter | zipcode | 12040 | cabin |  |
| steve | zipcode | 45601 |  | 4 |
| steve | zipcode | 45601 |  | 5 |
| steve | zipcode | 45601 | home | 1 |
| steve | zipcode | 45601 | work | 2 |
| steve | zipcode | 45601 | cabin |  |

Deduplicating with built-in sorting:
```bash
kgtk deduplicate -i examples/docs/compact-file4.tsv
```

The output will be the following table in KGTK format:

| node1 | label | node2 | location | years |
| -- | -- | -- | -- | -- |
| john | zipcode | 12345 | home | 10 |
| john | zipcode | 12346 |  |  |
| peter | zipcode | 12040 |  | 6 |
| peter | zipcode | 12040 | cabin |  |
| peter | zipcode | 12040 | home |  |
| peter | zipcode | 12040 | work | 5 |
| steve | zipcode | 45601 |  | 3 |
| steve | zipcode | 45601 |  | 4 |
| steve | zipcode | 45601 |  | 5 |
| steve | zipcode | 45601 | cabin |  |
| steve | zipcode | 45601 | home | 1 |
| steve | zipcode | 45601 | work | 2 |

The output is sorted and duplicate lines have been removed, without creating any new
[multi-valued edges (`|` lists)](../../specification#multi-valued-edges).

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

### Expert Example: Compacting on (`node1`, `label`)

Compacting with the tuple (`node1`, `label`) as the key (removing
the `id` and `node2` columns from the default for a KGTK edge file)
may produce an invalid KGTK file.  Nonetheless, there may be occasions
when this is what you want to do:

```bash
kgtk compact -i examples/docs/compact-file3.tsv \
             --mode=NONE --columns node1 label
```

The output will be the following table in quasi-KGTK format:

| node1 | label | node2 | id | location | years |
| -- | -- | -- | -- | -- | -- |
| john | zipcode | 12345\|12346 | 1\|2 | home | 10 |
| peter | zipcode | 12040 | 3\|4 | cabin\|home\|work | 5\|6 |
| steve | zipcode | 45601 | 5\|6 | cabin\|home\|work | 1\|2\|3\|4\|5 |

