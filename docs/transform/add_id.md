## Overview

The add-id command copies its input file to its output file,
adding an ID column and ID values when needed.

### ID Styles

New IDs may be generated using one of the following ID generation styles.

| ID Style | Description |
| -------- | ----------- |
| empty | Sets the ID column to the empty value (clears it). |
| node1-label-node2 | Concatenates the node1, label, and node2 column values. |
| node1-label-node2-id | Concatenates the node1, label, and node2 column values, then concatenate any existing non-blank ID value. |
| node1-label-node2-num | Concatenates the node1, label, and node2 column values with a sequence number per (node1, label, node2) tuple. |
| node1-label-num | Concatenates the node1 and label column values with a sequence number per-(node1, label) pair. |
| prefix### | Concatenate a prefix value (from `--id-prefix`) with an incrementing counter with leading zeros per `--id-prefix-num-width`). |
| wikidata | Concatenate the node1 and label column values with either the node2 column value (if it starts with P or Q) or the SHA256 hash of the node2 column value (truncated to the width giver by ``--value-hash-width`). |
| wikidata-with-claim-id | If the claim-id column is empty, produce an ID value as per `--id-style wikidata`, above. Otherwise, if `--claim-id-hash-width` is 0, then concatenate the value from the column named by `--claim-id-column-name` (default `claim_id`) to the `--id-style wikidata` ID value. Otherwise, concatenate a SHA256 hash of the `claim_id` column value, truncated per `--claim-id-hash-width`. | 

### Uniqueness and Memory Use

By default, the ID values in the file are validated for uniqueness using an in-memory set.  This may cause
memory usage issues for large input files, and may be inappropriate
for some files that legitimately contain duplicate records.
The `--verify-id-unique=false` option may be used to disable this check.

## Usage

```
usage: kgtk add-id [-h] [-i INPUT_FILE] [-o OUTPUT_FILE]
                   [--old-id-column-name COLUMN_NAME]
                   [--new-id-column-name COLUMN_NAME]
                   [--overwrite-id [optional true|false]]
                   [--verify-id-unique [optional true|false]]
                   [--id-style {node1-label-node2,node1-label-num,node1-label-node2-num,node1-label-node2-id,empty,prefix###,wikidata,wikidata-with-claim-id}]
                   [--id-prefix PREFIX] [--initial-id INTEGER]
                   [--id-prefix-num-width INTEGER]
                   [--id-concat-num-width INTEGER]
                   [--value-hash-width VALUE_HASH_WIDTH]
                   [--claim-id-hash-width CLAIM_ID_HASH_WIDTH]
                   [--claim-id-column-name CLAIM_ID_COLUMN_NAME]
                   [-v [optional True|False]]

Copy a KGTK file, adding ID values.

The `--overwrite-id` option can be used to replace existing ID values in the ID column.
It does not update instances of the same ID in other columns, such as node1, elsewhere in the file.

Several ID styles are supported.

Additional options are shown in expert help.
kgtk --expert add-id --help

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK input file. (May be omitted or '-' for
                        stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for
                        stdout.)
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

  -v [optional True|False], --verbose [optional True|False]
                        Print additional progress messages (default=False).
```

## Examples

Suppose that `examples/docs/add-id-file1.tsv` contains the following table in KGTK format:

```bash
kgtk cat -i examples/docs/add-id-file1.tsv
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

!!! note
    The `years` column means years employed, not age.

### Add an ID column using the default ID style (prefix###)

```bash
kgtk add-id -i examples/docs/add-id-file1.tsv
```

The output will be the following table in KGTK format:

| node1 | label | node2 | location | years | id |
| -- | -- | -- | -- | -- | -- |
| john | zipcode | 12345 | home | 10 | E1 |
| john | zipcode | 12346 |  |  | E2 |
| peter | zipcode | 12040 | home |  | E3 |
| peter | zipcode | 12040 | cabin |  | E4 |
| peter | zipcode | 12040 | work | 5 | E5 |
| peter | zipcode | 12040 |  | 6 | E6 |
| steve | zipcode | 45601 |  | 3 | E7 |
| steve | zipcode | 45601 |  | 4 | E8 |
| steve | zipcode | 45601 |  | 5 | E9 |
| steve | zipcode | 45601 | home | 1 | E10 |
| steve | zipcode | 45601 | work | 2 | E11 |
| steve | zipcode | 45601 | cabin |  | E12 |

### Add an ID column using the node1-label-node2 ID style

```bash
kgtk add-id -i examples/docs/add-id-file1.tsv --id-style node1-label-node2
```

The output will be the following table in KGTK format:

| node1 | label | node2 | location | years | id |
| -- | -- | -- | -- | -- | -- |
| john | zipcode | 12345 | home | 10 | john-zipcode-12345 |
| john | zipcode | 12346 |  |  | john-zipcode-12346 |
| peter | zipcode | 12040 | home |  | peter-zipcode-12040 |
| peter | zipcode | 12040 | cabin |  | peter-zipcode-12040 |
| peter | zipcode | 12040 | work | 5 | peter-zipcode-12040 |
| peter | zipcode | 12040 |  | 6 | peter-zipcode-12040 |
| steve | zipcode | 45601 |  | 3 | steve-zipcode-45601 |
| steve | zipcode | 45601 |  | 4 | steve-zipcode-45601 |
| steve | zipcode | 45601 |  | 5 | steve-zipcode-45601 |
| steve | zipcode | 45601 | home | 1 | steve-zipcode-45601 |
| steve | zipcode | 45601 | work | 2 | steve-zipcode-45601 |
| steve | zipcode | 45601 | cabin |  | steve-zipcode-45601 |

### Add an ID column using the node1-label-num ID style

```bash
kgtk add-id -i examples/docs/add-id-file1.tsv --id-style node1-label-num
```

The output will be the following table in KGTK format:

| node1 | label | node2 | location | years | id |
| -- | -- | -- | -- | -- | -- |
| john | zipcode | 12345 | home | 10 | john-zipcode-0000 |
| john | zipcode | 12346 |  |  | john-zipcode-0001 |
| peter | zipcode | 12040 | home |  | peter-zipcode-0000 |
| peter | zipcode | 12040 | cabin |  | peter-zipcode-0001 |
| peter | zipcode | 12040 | work | 5 | peter-zipcode-0002 |
| peter | zipcode | 12040 |  | 6 | peter-zipcode-0003 |
| steve | zipcode | 45601 |  | 3 | steve-zipcode-0000 |
| steve | zipcode | 45601 |  | 4 | steve-zipcode-0001 |
| steve | zipcode | 45601 |  | 5 | steve-zipcode-0002 |
| steve | zipcode | 45601 | home | 1 | steve-zipcode-0003 |
| steve | zipcode | 45601 | work | 2 | steve-zipcode-0004 |
| steve | zipcode | 45601 | cabin |  | steve-zipcode-0005 |

### Add an ID column building on an existing ID value using the node1-label-node2-id format

```bash
kgtk add-id -i examples/docs/add-id-file1.tsv / add-id --id-style node1-label-node2-id --overwrite-id
```

| node1 | label | node2 | location | years | id |
| -- | -- | -- | -- | -- | -- |
| john | zipcode | 12345 | home | 10 | john-zipcode-12345-E1 |
| john | zipcode | 12346 |  |  | john-zipcode-12346-E2 |
| peter | zipcode | 12040 | home |  | peter-zipcode-12040-E3 |
| peter | zipcode | 12040 | cabin |  | peter-zipcode-12040-E4 |
| peter | zipcode | 12040 | work | 5 | peter-zipcode-12040-E5 |
| peter | zipcode | 12040 |  | 6 | peter-zipcode-12040-E6 |
| steve | zipcode | 45601 |  | 3 | steve-zipcode-45601-E7 |
| steve | zipcode | 45601 |  | 4 | steve-zipcode-45601-E8 |
| steve | zipcode | 45601 |  | 5 | steve-zipcode-45601-E9 |
| steve | zipcode | 45601 | home | 1 | steve-zipcode-45601-E10 |
| steve | zipcode | 45601 | work | 2 | steve-zipcode-45601-E11 |
| steve | zipcode | 45601 | cabin |  | steve-zipcode-45601-E12 |

### Create a new ID column for the result instead of overwriting the existing ID column value

```bash
kgtk add-id -i examples/docs/add-id-file1.tsv / add-id --id-style node1-label-node2-id --new-id-column-name new-id
```

| node1 | label | node2 | location | years | id | new-id |
| -- | -- | -- | -- | -- | -- | -- |
| john | zipcode | 12345 | home | 10 | E1 | john-zipcode-12345-E1 |
| john | zipcode | 12346 |  |  | E2 | john-zipcode-12346-E2 |
| peter | zipcode | 12040 | home |  | E3 | peter-zipcode-12040-E3 |
| peter | zipcode | 12040 | cabin |  | E4 | peter-zipcode-12040-E4 |
| peter | zipcode | 12040 | work | 5 | E5 | peter-zipcode-12040-E5 |
| peter | zipcode | 12040 |  | 6 | E6 | peter-zipcode-12040-E6 |
| steve | zipcode | 45601 |  | 3 | E7 | steve-zipcode-45601-E7 |
| steve | zipcode | 45601 |  | 4 | E8 | steve-zipcode-45601-E8 |
| steve | zipcode | 45601 |  | 5 | E9 | steve-zipcode-45601-E9 |
| steve | zipcode | 45601 | home | 1 | E10 | steve-zipcode-45601-E10 |
| steve | zipcode | 45601 | work | 2 | E11 | steve-zipcode-45601-E11 |
| steve | zipcode | 45601 | cabin |  | E12 | steve-zipcode-45601-E12 |

### Add an ID column using the node1-label-node2-num ID style

```bash
kgtk add-id -i examples/docs/add-id-file1.tsv --id-style node1-label-node2-num
```

The output will be the following table in KGTK format:

| node1 | label | node2 | location | years | id |
| -- | -- | -- | -- | -- | -- |
| john | zipcode | 12345 | home | 10 | john-zipcode-12345-0000 |
| john | zipcode | 12346 |  |  | john-zipcode-12346-0000 |
| peter | zipcode | 12040 | home |  | peter-zipcode-12040-0000 |
| peter | zipcode | 12040 | cabin |  | peter-zipcode-12040-0001 |
| peter | zipcode | 12040 | work | 5 | peter-zipcode-12040-0002 |
| peter | zipcode | 12040 |  | 6 | peter-zipcode-12040-0003 |
| steve | zipcode | 45601 |  | 3 | steve-zipcode-45601-0000 |
| steve | zipcode | 45601 |  | 4 | steve-zipcode-45601-0001 |
| steve | zipcode | 45601 |  | 5 | steve-zipcode-45601-0002 |
| steve | zipcode | 45601 | home | 1 | steve-zipcode-45601-0003 |
| steve | zipcode | 45601 | work | 2 | steve-zipcode-45601-0004 |
| steve | zipcode | 45601 | cabin |  | steve-zipcode-45601-0005 |

### Add an ID column using the node1-label-num ID style

```bash
kgtk add-id -i examples/docs/add-id-file1.tsv --id-style node1-label-num
```

The output will be the following table in KGTK format:

| node1 | label | node2 | location | years | id |
| -- | -- | -- | -- | -- | -- |
| john | zipcode | 12345 | home | 10 | john-zipcode-0000 |
| john | zipcode | 12346 |  |  | john-zipcode-0001 |
| peter | zipcode | 12040 | home |  | peter-zipcode-0000 |
| peter | zipcode | 12040 | cabin |  | peter-zipcode-0001 |
| peter | zipcode | 12040 | work | 5 | peter-zipcode-0002 |
| peter | zipcode | 12040 |  | 6 | peter-zipcode-0003 |
| steve | zipcode | 45601 |  | 3 | steve-zipcode-0000 |
| steve | zipcode | 45601 |  | 4 | steve-zipcode-0001 |
| steve | zipcode | 45601 |  | 5 | steve-zipcode-0002 |
| steve | zipcode | 45601 | home | 1 | steve-zipcode-0003 |
| steve | zipcode | 45601 | work | 2 | steve-zipcode-0004 |
| steve | zipcode | 45601 | cabin |  | steve-zipcode-0005 |

### Add an ID column using the wikidata ID style

```bash
kgtk add-id -i examples/docs/add-id-file1.tsv --id-style wikidata
```

The output will be the following table in KGTK format:

| node1 | label | node2 | location | years | id |
| -- | -- | -- | -- | -- | -- |
| john | zipcode | 12345 | home | 10 | john-zipcode-599447 |
| john | zipcode | 12346 |  |  | john-zipcode-34d128 |
| peter | zipcode | 12040 | home |  | peter-zipcode-a5ceb2 |
| peter | zipcode | 12040 | cabin |  | peter-zipcode-a5ceb2 |
| peter | zipcode | 12040 | work | 5 | peter-zipcode-a5ceb2 |
| peter | zipcode | 12040 |  | 6 | peter-zipcode-a5ceb2 |
| steve | zipcode | 45601 |  | 3 | steve-zipcode-3f5bb8 |
| steve | zipcode | 45601 |  | 4 | steve-zipcode-3f5bb8 |
| steve | zipcode | 45601 |  | 5 | steve-zipcode-3f5bb8 |
| steve | zipcode | 45601 | home | 1 | steve-zipcode-3f5bb8 |
| steve | zipcode | 45601 | work | 2 | steve-zipcode-3f5bb8 |
| steve | zipcode | 45601 | cabin |  | steve-zipcode-3f5bb8 |

!!! note
   The existing test dataset doesn't have any entries with node2 values starting with P or Q,
   so this example doesn't  doesn't illustrate the full range of IDs generated inthis style.

### Add an ID column using the wikidata-with-claim-id ID style, using the location column as a placeholder for the claim-id column

```bash
kgtk add-id -i examples/docs/add-id-file1.tsv --id-style wikidata-with-claim-id --claim-id-column-name location
```

The output will be the following table in KGTK format:

| node1 | label | node2 | location | years | id |
| -- | -- | -- | -- | -- | -- |
| john | zipcode | 12345 | home | 10 | john-zipcode-599447-4ea14058 |
| john | zipcode | 12346 |  |  | john-zipcode-34d128 |
| peter | zipcode | 12040 | home |  | peter-zipcode-a5ceb2-4ea14058 |
| peter | zipcode | 12040 | cabin |  | peter-zipcode-a5ceb2-2764182d |
| peter | zipcode | 12040 | work | 5 | peter-zipcode-a5ceb2-00e13ed7 |
| peter | zipcode | 12040 |  | 6 | peter-zipcode-a5ceb2 |
| steve | zipcode | 45601 |  | 3 | steve-zipcode-3f5bb8 |
| steve | zipcode | 45601 |  | 4 | steve-zipcode-3f5bb8 |
| steve | zipcode | 45601 |  | 5 | steve-zipcode-3f5bb8 |
| steve | zipcode | 45601 | home | 1 | steve-zipcode-3f5bb8-4ea14058 |
| steve | zipcode | 45601 | work | 2 | steve-zipcode-3f5bb8-00e13ed7 |
| steve | zipcode | 45601 | cabin |  | steve-zipcode-3f5bb8-2764182d |
