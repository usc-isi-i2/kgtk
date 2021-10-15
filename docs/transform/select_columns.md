41;368;0c>## Overview

`kgtk select-columns` selects a subsetfile columns while copying a KGTK file from input to output.
You provide a list of column names in the order in which they should appear in the output file.
This command is equivalent to [`kgtk reorder-columns --trim`](../reorder_columns).

For more details, see [`kgtk reorder-columns --trim`](../reorder_columns).

## Usage
```
usage: kgtk reorder-columns [-h] [-i INPUT_FILE] [-o OUTPUT_FILE] -c
                            COLUMN_NAME [COLUMN_NAME ...]
                            [--trim [True|False]] [-v [optional True|False]]

This command reorders one or more columns in a KGTK file. 

Reorder all columns using --columns col1 col2
Reorder selected columns using --columns col1 col2 ... coln-1 coln
Move a column to the front: --columns col ...
Move a column to the end: --columns ... col
Extract named columns, omitting the rest: --columns col1 col2 --trim
Move a range of columns: --columns coln .. colm ...
If no input filename is provided, the default is to read standard input. 

Additional options are shown in expert help.
kgtk --expert reorder-columns --help

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK input file. (May be omitted or '-' for
                        stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for
                        stdout.)
  -c COLUMN_NAME [COLUMN_NAME ...], --columns COLUMN_NAME [COLUMN_NAME ...]
                        The list of reordered column names, optionally
                        containing '...' for column names not explicitly
                        mentioned.
  --trim [True|False]   If true, omit unmentioned columns. (default=True).

  -v [optional True|False], --verbose [optional True|False]
                        Print additional progress messages (default=False).
```

## Examples

### Sample Data

Suppose that `file1.tsv` contains the following table in KGTK format:

```bash
kgtk cat -i examples/docs/reorder-columns-file1.tsv
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


### Select a List of Column Names

Copy `file1.tsv`, sending the output to standard output, specifying
the list of desired columnsL

```
kgtk select-columns -i examples/docs/reorder-columns-file1.tsv \
                    --columns label node1 node2
```
The result will be the following table in KGTK format:

| label | node1 | node2 |
| -- | -- | -- |
| zipcode | john | 12345 |
| zipcode | john | 12346 |
| zipcode | peter | 12040 |
| zipcode | peter | 12040 |
| zipcode | peter | 12040 |
| zipcode | peter | 12040 |
| zipcode | steve | 45601 |
| zipcode | steve | 45601 |
| zipcode | steve | 45601 |
| zipcode | steve | 45601 |
| zipcode | steve | 45601 |
| zipcode | steve | 45601 |
