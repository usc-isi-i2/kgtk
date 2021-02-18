## Overview

The ifempty command filters a KGTK file, passing through only those rows for
which one (or more) specified columns contain *empty* values.

!!! note
    The [`kgtk ifnotempty`](../ifnotempty/) command computes the inverse output of this command.

### Any or All

When multiple
columns are specified, there is the choice of requiring any of the columns to
be empty or all of the columns to be empty.

### Count Only

`kgtk ifempty --count` reports the count of rows that passed the filter instead of
copying the rows to the output file.  The count will normally be reported to
standard error;  standard output will not receive any data.

## Usage

```
usage: kgtk ifempty [-h] [-i INPUT_FILE] [-o OUTPUT_FILE]
                    [--reject-file REJECT_FILE] --columns FILTER_COLUMN_NAMES
                    [FILTER_COLUMN_NAMES ...] [--count [True|False]]
                    [--all [True|False]] [-v [optional True|False]]

Filter a KGTK file based on whether one or more fields are empty. When multiple fields are specified, either any field or all fields must be empty.

Additional options are shown in expert help.
kgtk --expert ifempty --help

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK input file. (May be omitted or '-' for
                        stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for
                        stdout.)
  --reject-file REJECT_FILE
                        The KGTK file for input records that fail the filter.
                        (Optional, use '-' for stdout.)
  --columns FILTER_COLUMN_NAMES [FILTER_COLUMN_NAMES ...]
                        The columns in the file being filtered (Required).
  --count [True|False]  Only count the records, do not copy them.
                        (default=False).
  --all [True|False]    False: Test if any are empty, True: test if all are
                        empty (default=False).

  -v [optional True|False], --verbose [optional True|False]
                        Print additional progress messages (default=False).
```

## Examples

### Sample data

Suppose that `file1.tsv` contains the following table in KGTK format:

```bash
kgtk cat -i examples/docs/ifempty-file1.tsv
```

| node1 | label | node2 | location | years |
| -- | -- | -- | -- | -- |
| john | zipcode | 12345 | home | 10 |
| john | zipcode | 12346 |  |  |
| peter | zipcode | 12040 | home |  |
| peter | zipcode | 12040 | work | 6 |
| steve | zipcode | 45601 |  | 3 |
| steve | zipcode | 45601 | work |  |

### Pass Records with Empty Cells in a Single Column

```bash
kgtk ifempty -i examples/docs/ifempty-file1.tsv \
             --columns location
```

| node1 | label | node2 | location | years |
| -- | -- | -- | -- | -- |
| john | zipcode | 12346 |  |  |
| steve | zipcode | 45601 |  | 3 |


```bash
kgtk ifempty -i examples/docs/ifempty-file1.tsv \
             --columns years
```

| node1 | label | node2 | location | years |
| -- | -- | -- | -- | -- |
| john | zipcode | 12346 |  |  |
| peter | zipcode | 12040 | home |  |
| steve | zipcode | 45601 | work |  |

### Pass Records with Empty Cells in Either of Two Columns

```bash
kgtk ifempty -i examples/docs/ifempty-file1.tsv \
             --columns location years
```

| node1 | label | node2 | location | years |
| -- | -- | -- | -- | -- |
| john | zipcode | 12346 |  |  |
| peter | zipcode | 12040 | home |  |
| steve | zipcode | 45601 |  | 3 |
| steve | zipcode | 45601 | work |  |

### Pass Records with Empty Cells in Either of Two Columns with Rejects

```bash
kgtk ifempty -i examples/docs/ifempty-file1.tsv \
             --columns location years \
             --reject-file ifempty-file1-rejects.tsv
```

| node1 | label | node2 | location | years |
| -- | -- | -- | -- | -- |
| john | zipcode | 12346 |  |  |
| peter | zipcode | 12040 | home |  |
| steve | zipcode | 45601 |  | 3 |
| steve | zipcode | 45601 | work |  |

Here are the rejected edges:

```bash
kgtk cat -i ifempty-file1-rejects.tsv
```
| node1 | label | node2 | location | years |
| -- | -- | -- | -- | -- |
| john | zipcode | 12345 | home | 10 |
| peter | zipcode | 12040 | work | 6 |


### Pass Records with Empty Cells in Both of Two Columns

```bash
kgtk ifempty -i examples/docs/ifempty-file1.tsv \
             --all --columns location years
```

| node1 | label | node2 | location | years |
| -- | -- | -- | -- | -- |
| john | zipcode | 12346 |  |  |

### Count Records with Empty Cells in a Column

```bash
kgtk ifempty -i examples/docs/ifempty-file1.tsv \
             --count --columns years
```

The result on standard error will be:

    Read 6 records, 3 records passed the filter, 3 rejected.

!!! note
    The expert option `--errors-to-stdout` can be used to route this message to standard output.
