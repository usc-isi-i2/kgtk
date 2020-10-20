The expand command copies its input file to its output file,
compacting repeated items into | lists.

By default, the input file is sorted in memory to achieve the
grouping necessary for the compaction algorithm. This may cause
memory usage issues for large input files. If the input file has
already been sorted (or at least grouped), the `--presorted`
option may be used.

## Usage

```
usage: kgtk compact [-h] [-i INPUT_FILE] [-o OUTPUT_FILE]
                    [--columns KEY_COLUMN_NAMES [KEY_COLUMN_NAMES ...]]
                    [--compact-id [True|False]] [--presorted [True|False]]
                    [--verify-sort [True|False]] [--build-id [True|False]]
                    [--overwrite-id [optional true|false]]
                    [--verify-id-unique [optional true|false]] [-v]

Copy a KGTK file, compacting multiple records into | lists. 

By default, the input file is sorted in memory to achieve the grouping necessary for the compaction algorithm. This may cause  memory usage issues for large input files. If the input file has already been sorted (or at least grouped), the `--presorted` option may be used.

Additional options are shown in expert help.
kgtk --expert compact --help

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK input file. (May be omitted or '-' for stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for stdout.)
  --columns KEY_COLUMN_NAMES [KEY_COLUMN_NAMES ...]
                        The key columns to identify records for compaction. (default=id for
                        node files, (node1, label, node2, id) for edge files).
  --compact-id [True|False]
                        Indicate that the ID column in KGTK edge files should be compacted.
                        Normally, if the ID column exists, it is not compacted, as there are
                        use cases that need to maintain distinct lists of secondary edges
                        for each ID value. (default=False).
  --presorted [True|False]
                        Indicate that the input has been presorted (or at least pregrouped)
                        (default=False).
  --verify-sort [True|False]
                        If the input has been presorted, verify its consistency (disable if
                        only pregrouped). (default=True).
  --lists-in-input [LISTS_IN_INPUT]
                        Assume that the input file may contain lists (disable when certain it does not). (default=True).
  --build-id [True|False]
                        Build id values in an id column. (default=False).
  --overwrite-id [optional true|false]
                        When true, replace existing ID values. When false, copy existing ID
                        values. When --overwrite-id is omitted, it defaults to False. When
                        --overwrite-id is supplied without an argument, it is True.
  --verify-id-unique [optional true|false]
                        When true, verify ID uniqueness using an in-memory set of IDs. When
                        --verify-id-unique is omitted, it defaults to False. When --verify-
                        id-unique is supplied without an argument, it is True.

  -v, --verbose         Print additional progress messages (default=False).
```

## Examples

Suppose that `file1.tsv` contains the following table in KGTK format:
(Note:  The `years` column means years employed, not age.)

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
kgtk compact -i file1.tsv
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
kgtk compact -i file2.tsv
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
kgtk compact -i file2.tsv --presorted
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

Compacting with the tuple (`node1`, `label`, `node2`, `id`) (the default
for a KGTK edge file) as the key:
```bash
kgtk compact -i file3.tsv
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
tuples in this examplee, compacting on just the `id` column yields the same results:

```bash
kgtk compact -i file3.tsv --mode=NONE --columns id
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

Compacting with the tuple (`node1`, `label`, `node2`) as the key (removing
the `id` column from the default for a KGTK edge file):

```bash
kgtk compact -i file3.tsv --compact-id
```

The output will be the following table in KGTK format:

| node1 | label   | node2 | id   | location          | years         |
| ----- | ------- | ----- | ---- | ----------------- | ------------- |
| john  | zipcode | 12345 | 1    | home              | 10            |
| john  | zipcode | 12346 | 2    |                   |               |
| peter | zipcode | 12040 | 3\|4 | cabin\|home\|work | 5\|6          |
| steve | zipcode | 45601 | 5\|6 | cabin\|home\|work | 1\|2\|3\|4\|5 |


Suppose you want to build new, unique IDs for your compacted edges:
```bash
kgtk compact -i file3.tsv --build-id --overwrite-id
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

Compacting the ID column, too:
```bash
kgtk compact -i file3.tsv --build-id --overwrite-id --compact-id
```

The output will be the following table in KGTK format:

| node1 | label | node2 | id | location | years |
| -- | -- | -- | -- | -- | -- |
| john | zipcode | 12345 | E1 | home | 10 |
| john | zipcode | 12346 | E2 |  |  |
| peter | zipcode | 12040 | E3 | cabin\|home\|work | 5\|6 |
| steve | zipcode | 45601 | E4 | cabin\|home\|work | 1\|2\|3\|4\|5 |


Using the expert option --id-style=concat, you can generate IDs
that concatenate (node1, label, node2).

```bash
kgtk compact -i file3.tsv --build-id --overwrite-id --compact-id --id-style=concat
```

The output will be the following table in KGTK format:

| node1 | label | node2 | id | location | years |
| -- | -- | -- | -- | -- | -- |
| john | zipcode | 12345 | john-zipcode-12345 | home | 10 |
| john | zipcode | 12346 | john-zipcode-12346 |  |  |
| peter | zipcode | 12040 | peter-zipcode-12040 | cabin\|home\|work | 5\|6 |
| steve | zipcode | 45601 | steve-zipcode-45601 | cabin\|home\|work | 1\|2\|3\|4\|5 |

If you want to generate new ID value without compacting existing IDs,
use the expert option --id-wtyle=concat-with-id.

The output will be the following table in KGTK format:

| node1 | label | node2 | id | location | years |
| -- | -- | -- | -- | -- | -- |
| john | zipcode | 12345 | john-zipcode-12345-1 | home | 10 |
| john | zipcode | 12346 | john-zipcode-12346-2 |  |  |
| peter | zipcode | 12040 | peter-zipcode-12040-3 | home |  |
| peter | zipcode | 12040 | peter-zipcode-12040-4 | cabin\|work | 5\|6 |
| steve | zipcode | 45601 | steve-zipcode-45601-5 |  | 3\|4\|5 |
| steve | zipcode | 45601 | steve-zipcode-45601-6 | cabin\|home\|work | 1\|2 |
