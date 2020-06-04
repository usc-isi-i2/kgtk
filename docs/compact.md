The expand command copies its input file to its output file,
compacting repeated items into | lists.

By default, the input file is sorted in memory to achieve the
grouping necessary for the compaction algorithm. This may cause
memory usage issues for large input files. If the input file has
already been sorted (or at least grouped), the `--presorted`
option may be used.

## Usage

```
usage: kgtk compact [-h] [--columns KEY_COLUMN_NAMES [KEY_COLUMN_NAMES ...]] [--presorted [SORTED_INPUT]] [--verify-sort [VERIFY_SORT]] [-o OUTPUT_KGTK_FILE]
                    [--build-id [BUILD_ID]] [--overwrite-id [OVERWRITE_ID]] [--verify-id-unique [VERIFY_ID_UNIQUE]] [-v]
                    [input_kgtk_file]

Copy a KGTK file, compacting multiple records into | lists. 

By default, the input file is sorted in memory to achieve the grouping necessary for the compaction algorithm. This may cause  memory usage issues for large input files. If the input file has already been sorted (or at least grouped), the `--presorted` option may be used.

Additional options are shown in expert help.
kgtk --expert compact --help

positional arguments:
  input_kgtk_file       The KGTK file to filter. May be omitted or '-' for stdin (default=-).

optional arguments:
  -h, --help            show this help message and exit
  --columns KEY_COLUMN_NAMES [KEY_COLUMN_NAMES ...]
                        The key columns to identify records for compaction. (default=id for node files, (node1, label, node2) for edge files).
  --presorted [SORTED_INPUT]
                        Indicate that the input has been presorted (or at least pregrouped) (default=False).
  --verify-sort [VERIFY_SORT]
                        If the input has been presorted, verify its consistency (disable if only pregrouped). (default=True).
  -o OUTPUT_KGTK_FILE, --output-file OUTPUT_KGTK_FILE
                        The KGTK file to write (default=-).
  --build-id [BUILD_ID]
                        Build id values in an id column. (default=False).
  --overwrite-id [OVERWRITE_ID]
                        Replace existing id values. (default=False).
  --verify-id-unique [VERIFY_ID_UNIQUE]
                        Verify ID uniqueness. Uses an in-memory set of IDs. (default=True).

  -v, --verbose         Print additional progress messages (default=False).
```

## Examples

Suppose that `file1.tsv` contains the following table in KGTK format:

| node1 | label   | node2 | location  | years |
| ----- | ------- | ----- | --------- | ----- |
| john  | zipcode | 12345 | home      | 10    |
| john  | zipcode | 12346 |           |       |
| peter | zipcode | 12040 | home      |       |
| peter | zipcode | 12040 | cabin     |       |
| peter | zipcode | 12040 | work      | 5     |
| peter | zipcode | 12040 |           | 6     |
| steve | zipcode | 45601 |           | 3     |
| steve | zipcode | 45601 |           | 4     |
| steve | zipcode | 45601 |           | 5     |
| steve | zipcode | 45601 | home      | 1     |
| steve | zipcode | 45601 | work      | 2     |
| steve | zipcode | 45601 | cabin     |       |

```bash
kgtk compact file1.tsv
```

The output will be the following table in KGTK format:

| node1 | label   | node2 | location          | years         |
| ----- | ------- | ----- | ----------------- | ------------- |
| john  | zipcode | 12345 | home              | 10            |
| john  | zipcode | 12346 |                   |               |
| peter | zipcode | 12040 | cabin\|home\|work | 5\|6          |
| steve | zipcode | 45601 | cabin\|home\|work | 1\|2\|3\|4\|5 |

Suppose that `file2.tsv` contains the following table in KGTK format
(this is the same as `file1.tsv`, with the rows in a jumbled order):

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
kgtk compact file2.tsv
```

The output will be the following table in KGTK format:

| node1 | label   | node2 | location          | years         |
| ----- | ------- | ----- | ----------------- | ------------- |
| john  | zipcode | 12345 | home              | 10            |
| john  | zipcode | 12346 |                   |               |
| peter | zipcode | 12040 | cabin\|home\|work | 5\|6          |
| steve | zipcode | 45601 | cabin\|home\|work | 1\|2\|3\|4\|5 |

Compacting with built-in sorting disabled:
```bash
kgtk compact file2.tsv --presorted
```
The output will be the following table in KGTK format (which is not
a complate compaction):

| node1 | label   | node2 | location          | years         |
| ----- | ------- | ----- | ----------------- | ------------- |
| steve | zipcode | 45601 | cabin             |               |
| john  | zipcode | 12345 | home              | 10            |
| steve | zipcode | 45601 |                   | 4             |
| john  | zipcode | 12346 |                   |               |
| peter | zipcode | 12040 | home              |               |
| steve | zipcode | 45601 | home              | 1             |
| peter | zipcode | 12040 | work              | 5\|6          |
| steve | zipcode | 45601 |                   | 3             |
| peter | zipcode | 12040 | cabin             |               |
| steve | zipcode | 45601 | work              | 2\|5          |

Suppose that `file3.tsv` contains the following table in KGTK format:

| node1 | label   | node2 | id	| location  | years |
| ----- | ------- | ----- | --	| --------- | ----- |
| john  | zipcode | 12345 | 1	| home      | 10    |
| john  | zipcode | 12346 | 2	|           |       |
| peter | zipcode | 12040 | 3	| home      |       |
| peter | zipcode | 12040 | 4	| cabin     |       |
| peter | zipcode | 12040 | 4	| work      | 5     |
| peter | zipcode | 12040 | 4	|           | 6     |
| steve | zipcode | 45601 | 5	|           | 3     |
| steve | zipcode | 45601 | 5	|           | 4     |
| steve | zipcode | 45601 | 5	|           | 5     |
| steve | zipcode | 45601 | 6	| home      | 1     |
| steve | zipcode | 45601 | 6	| work      | 2     |
| steve | zipcode | 45601 | 6	| cabin     |       |

Compacting with the tuple (`node1`, `label`, `node2`) (the default
for a KGTK edge file) as the key:
```bash
kgtk compact file3.tsv
```

The output will be the following table in KGTK format:

| node1 | label   | node2 | id   | location          | years         |
| ----- | ------- | ----- | ---- | ----------------- | ------------- |
| john  | zipcode | 12345 | 1    | home              | 10            |
| john  | zipcode | 12346 | 2    |                   |               |
| peter | zipcode | 12040 | 3\|4 | cabin\|home\|work | 5\|6          |
| steve | zipcode | 45601 | 5\|6 | cabin\|home\|work | 1\|2\|3\|4\|5 |


Compacting with the tuple (`node1`, `label`, `node2`, `id`) as the key (adding
the `id` column to the default for a KGTK edge file):

```bash
kgtk compact file3.tsv --columns id
```

The output will be the following table in KGTK format:

| node1 | label   | node2 | id   | location          | years         |
| ----- | ------- | ----- | ---- | ----------------- | ------------- |
| john  | zipcode | 12345 | 1    | home              | 10            |
| john  | zipcode | 12346 | 2    |                   |               |
| peter | zipcode | 12040 | 3    | home              |               |
| peter | zipcode | 12040 | 4    | cabin\|work       | 5\|6          |
| steve | zipcode | 45601 | 5    |                   | 3\|4\|5       |
| steve | zipcode | 45601 | 6    | cabin\|home\|work | 1\|2          |

Since the `id` values are not duplicated between (`node1`, `label`, `node2`)
tuples, compacting on just the `id` column yields the same results:

```bash
kgtk compact file3.tsv --mode=NONE --columns id
```

The output will be the following table in KGTK format:

| node1 | label   | node2 | id   | location          | years         |
| ----- | ------- | ----- | ---- | ----------------- | ------------- |
| john  | zipcode | 12345 | 1    | home              | 10            |
| john  | zipcode | 12346 | 2    |                   |               |
| peter | zipcode | 12040 | 3    | home              |               |
| peter | zipcode | 12040 | 4    | cabin\|work       | 5\|6          |
| steve | zipcode | 45601 | 5    |                   | 3\|4\|5       |
| steve | zipcode | 45601 | 6    | cabin\|home\|work | 1\|2          |

Suppose you want to build new, unique IDs for your compacted edges:
```bash
kgtk compact file3.tsv --build-id --overwrite-id
```

The output will be the following table in KGTK format:

| node1 | label   | node2 | id  | location          | years         |
| ----- | ------- | ----- | --- | ----------------- | ------------- |
| john  | zipcode | 12345 | E1  | home              | 10            |
| john  | zipcode | 12346 | E2  |                   |               |
| peter | zipcode | 12040 | E3  | cabin\|home\|work | 5\|6          |
| steve | zipcode | 45601 | E4  | cabin\|home\|work | 1\|2\|3\|4\|5 |

