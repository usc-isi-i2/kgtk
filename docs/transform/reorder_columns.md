The reorder-columns command reorders file columns while copying a KGTK file from input to output.
## Usage

```
usage: kgtk reorder-columns [-h] [-i INPUT_FILE] [-o OUTPUT_FILE] -c COLUMN_NAME
                            [COLUMN_NAME ...] [--trim [True|False]] [-v]

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
                        The KGTK input file. (May be omitted or '-' for stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for stdout.)
  -c COLUMN_NAME [COLUMN_NAME ...], --columns COLUMN_NAME [COLUMN_NAME ...]
                        The list of reordered column names, optionally containing '...' for
                        column names not explicitly mentioned.
  --trim [True|False]   If true, omit unmentioned columns. (default=False).

  -v, --verbose         Print additional progress messages (default=False).
```

## Examples

Suppose that `file1.tsv` contains the following table in KGTK format:

| node1 | label | node2 | location | years |
| -- | -- | -- | -- | -- |
| steve | zipcode | 45601 | cabin |  |
| john | zipcode | 12345 | home | 10 |
| steve | zipcode | 45601 |  | 4 |
| john | zipcode | 12346 |  |  |
| peter | zipcode | 12040 | home |  |
| steve | zipcode | 45601 | home | 1 |
| peter | zipcode | 12040 | work | 5 |
| peter | zipcode | 12040 |  | 6 |
| steve | zipcode | 45601 |  | 3 |
| peter | zipcode | 12040 | cabin |  |
| steve | zipcode | 45601 |  | 5 |
| steve | zipcode | 45601 | work | 2 |


Copy `file1.tsv`, sending the output to standard output, swapping
the positions of the `location` and `years` columns.

```
kgtk reorder-columns -i file1.tsv --columns ... years location
```

The result will be the following table in KGTK format:

| node1 | label | node2 | years | location |
| -- | -- | -- | -- | -- |
| steve | zipcode | 45601 |  | cabin |
| john | zipcode | 12345 | 10 | home |
| steve | zipcode | 45601 | 4 |  |
| john | zipcode | 12346 |  |  |
| peter | zipcode | 12040 |  | home |
| steve | zipcode | 45601 | 1 | home |
| peter | zipcode | 12040 | 5 | work |
| peter | zipcode | 12040 | 6 |  |
| steve | zipcode | 45601 | 3 |  |
| peter | zipcode | 12040 |  | cabin |
| steve | zipcode | 45601 | 5 |  |
| steve | zipcode | 45601 | 2 | work |

Copy `file1.tsv`, sending the output to standard output, with
the `location` column first:

```
kgtk reorder-columns -i file1.tsv --columns location ...
```

The result will be the following table in KGTK format:

| location | node1 | label | node2 | years |
| -- | -- | -- | -- | -- |
| cabin | steve | zipcode | 45601 |  |
| home | john | zipcode | 12345 | 10 |
|  | steve | zipcode | 45601 | 4 |
|  | john | zipcode | 12346 |  |
| home | peter | zipcode | 12040 |  |
| home | steve | zipcode | 45601 | 1 |
| work | peter | zipcode | 12040 | 5 |
|  | peter | zipcode | 12040 | 6 |
|  | steve | zipcode | 45601 | 3 |
| cabin | peter | zipcode | 12040 |  |
|  | steve | zipcode | 45601 | 5 |
| work | steve | zipcode | 45601 | 2 |

Copy `file1.tsv`, sending the output to standard output, giving
the complete list of columns:

```
kgtk reorder-columns -i file1.tsv --columns label node1 node2 years location
```
The result will be the following table in KGTK format:

| label | node1 | node2 | years | location |
| -- | -- | -- | -- | -- |
| zipcode | steve | 45601 |  | cabin |
| zipcode | john | 12345 | 10 | home |
| zipcode | steve | 45601 | 4 |  |
| zipcode | john | 12346 |  |  |
| zipcode | peter | 12040 |  | home |
| zipcode | steve | 45601 | 1 | home |
| zipcode | peter | 12040 | 5 | work |
| zipcode | peter | 12040 | 6 |  |
| zipcode | steve | 45601 | 3 |  |
| zipcode | peter | 12040 |  | cabin |
| zipcode | steve | 45601 | 5 |  |
| zipcode | steve | 45601 | 2 | work |
