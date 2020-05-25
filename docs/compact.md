The expand command copies its input file to its output file,
compacting repeated items into | lists.

By default, the input file is sorted in memory to achieve the
grouping necessary for the compaction algorithm. This may cause
memory usage issues for large input files. If the input file has
already been sorted (or at least grouped), the `--presorted`
option may be used.

## Usage

```bash
usage: kgtk compact [-h] [--columns KEY_COLUMN_NAMES [KEY_COLUMN_NAMES ...]]
                    [--presorted [SORTED_INPUT]] [-o OUTPUT_KGTK_FILE] [-v]
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
                        The key columns to identify records for compaction. (default=id for
                        node files, (node1, label, node2) for edge files).
  --presorted [SORTED_INPUT]
                        Indicate that the input has been presorted (or at least pregrouped)
                        (default=False).
  -o OUTPUT_KGTK_FILE, --output-file OUTPUT_KGTK_FILE
                        The KGTK file to write (default=-).

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
| peter | zipcode | 12040 | cabin\|home\|work | | 5\|6        |
| steve | zipcode | 45601 |                   | 1\|2\|3\|4\|5 |
