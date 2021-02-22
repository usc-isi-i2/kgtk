## Overview

`kgtk reorder-columns` reorders file columns while copying a KGTK file from input to output.
You provide a list of column names in the order in which they should appear in the output file.

!!! note
    You may not omit any column names from the list of column names unless
    you use "..", `...`, or `--trim`, described below.

!!! note
    This comand can be used to reorder the columns of non-KGTK input TSV files (quasi-KGTK files)
    by using the expert option `--mode=NONE`.

!!! note
    The output file should still have required columns (`id` for a KGTK node file, (`node1`, `label`, `node2`)
    for a KGTK edge file).  This requirement may be disabled with the expert option `--mode=NONE`, but the
    output file will not be a valid KGTK node or edge file.

!!! info
    See [`kgtk remove-columns`](../remove_columns) if you wish to remove columns.

    See [`kgtk rename-columns`](../rename_columns) if you wish to rename columns.

### List of Column Names

When you use this command, you supply the `--columns` option with
a list of column names in the
order you wish them to appear in the output file.

### Column Ranges

When listing the output column names, you may use `..` to indicate a range of column names (e.g., `first .. last`)
in the order of the columns in the input file.

### Elipses

When listing the output column names, you may use `...` to indicate all columns not explicitly mentioned.

### Trimming Columns

You may remove ("trim") columns with this command using the `--trim` option.
When this option is specified, all unmentioned columns will be removed
from the output file.

!!! note
    An elipses (`...`) will consume all remaining column names, leaving none left
    for `--trim` to remove.

!!! note
    `kgtk remove-columns --trim` will not complain if there are no column names to
    remove.

!!! note
    If you use this option to remove a required column name (`id` for KGTK
    node files, (`node1`, `label`, `node2`) for a KGTK edge file), then
    you will create an invalid KGTK file (a quasi-KGTK file).  You must
    include the expert option `--mode=NONE` on the command line to
    accomplish this.

!!! note
    `kgtk reorder-columns --trim` may be used as an alternative to [`kgtk remove-columns`](../remove_columns).


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
  --trim [True|False]   If true, omit unmentioned columns. (default=False).

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


### Giving a Complete List of Column Names

Copy `file1.tsv`, sending the output to standard output, giving
the complete list of columns, while swapping the order of
some columns:

```
kgtk reorder-columns -i examples/docs/reorder-columns-file1.tsv \
                     --columns label node1 node2 years location
```
The result will be the following table in KGTK format:

| label | node1 | node2 | years | location |
| -- | -- | -- | -- | -- |
| zipcode | john | 12345 | 10 | home |
| zipcode | john | 12346 |  |  |
| zipcode | peter | 12040 |  | home |
| zipcode | peter | 12040 |  | cabin |
| zipcode | peter | 12040 | 5 | work |
| zipcode | peter | 12040 | 6 |  |
| zipcode | steve | 45601 | 3 |  |
| zipcode | steve | 45601 | 4 |  |
| zipcode | steve | 45601 | 5 |  |
| zipcode | steve | 45601 | 1 | home |
| zipcode | steve | 45601 | 2 | work |
| zipcode | steve | 45601 |  | cabin |

### Giving a Range of Column Names

Copy `file1.tsv`, sending the output to standard output, giving
a range of columns, while swapping the order of
the lsat two columns:

```
kgtk reorder-columns -i examples/docs/reorder-columns-file1.tsv \
                     --columns node1 .. node2 years location
```
The result will be the following table in KGTK format:

| node1 | label | node2 | years | location |
| -- | -- | -- | -- | -- |
| john | zipcode | 12345 | 10 | home |
| john | zipcode | 12346 |  |  |
| peter | zipcode | 12040 |  | home |
| peter | zipcode | 12040 |  | cabin |
| peter | zipcode | 12040 | 5 | work |
| peter | zipcode | 12040 | 6 |  |
| steve | zipcode | 45601 | 3 |  |
| steve | zipcode | 45601 | 4 |  |
| steve | zipcode | 45601 | 5 |  |
| steve | zipcode | 45601 | 1 | home |
| steve | zipcode | 45601 | 2 | work |
| steve | zipcode | 45601 |  | cabin |

### Move a Column to the Beginning

Copy `file1.tsv`, sending the output to standard output, with
the `location` column first.  Use the elipses (`...`) to name
all other columns.

```
kgtk reorder-columns -i examples/docs/reorder-columns-file1.tsv \
                     --columns location ...
```

The result will be the following table in KGTK format:

| location | node1 | label | node2 | years |
| -- | -- | -- | -- | -- |
| home | john | zipcode | 12345 | 10 |
|  | john | zipcode | 12346 |  |
| home | peter | zipcode | 12040 |  |
| cabin | peter | zipcode | 12040 |  |
| work | peter | zipcode | 12040 | 5 |
|  | peter | zipcode | 12040 | 6 |
|  | steve | zipcode | 45601 | 3 |
|  | steve | zipcode | 45601 | 4 |
|  | steve | zipcode | 45601 | 5 |
| home | steve | zipcode | 45601 | 1 |
| work | steve | zipcode | 45601 | 2 |
| cabin | steve | zipcode | 45601 |  |

### Swap Two Columns, Naming Only Those Columns

Copy `file1.tsv`, sending the output to standard output, swapping
the positions of the `location` and `years` columns at the end
of the list of column names.

```
kgtk reorder-columns -i examples/docs/reorder-columns-file1.tsv \
                     --columns ... years location
```

The result will be the following table in KGTK format:

| node1 | label | node2 | years | location |
| -- | -- | -- | -- | -- |
| john | zipcode | 12345 | 10 | home |
| john | zipcode | 12346 |  |  |
| peter | zipcode | 12040 |  | home |
| peter | zipcode | 12040 |  | cabin |
| peter | zipcode | 12040 | 5 | work |
| peter | zipcode | 12040 | 6 |  |
| steve | zipcode | 45601 | 3 |  |
| steve | zipcode | 45601 | 4 |  |
| steve | zipcode | 45601 | 5 |  |
| steve | zipcode | 45601 | 1 | home |
| steve | zipcode | 45601 | 2 | work |
| steve | zipcode | 45601 |  | cabin |

### Trimming Omitted Columns

Copy `file1.tsv`, sending the output to standard output, giving
a partial list of columns and trimming the remainder:

```
kgtk reorder-columns -i examples/docs/reorder-columns-file1.tsv \
                     --columns label node1 node2 \
                     --trim
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

### Trimming a Required Column

Copy `file1.tsv`, sending the output to standard output, giving
a partial list of columns and trimming the remainder, which includes
required columns:

```
kgtk reorder-columns -i examples/docs/reorder-columns-file1.tsv \
                     --columns node1 location \
                     --trim --mode=NONE
```
The result will be the following table in KGTK format:

| node1 | location |
| -- | -- |
| john | home |
| john |  |
| peter | home |
| peter | cabin |
| peter | work |
| peter |  |
| steve |  |
| steve |  |
| steve |  |
| steve | home |
| steve | work |
| steve | cabin |

!!! note
    Quasi-KGTK input files may also be processed by specifying `--mode=NONE`.
