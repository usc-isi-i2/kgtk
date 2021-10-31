## Overview

`kgtk count`  (aka `kgtk wc`) counts the number of data records or non-empty values per column in a KGTK file.

There are two uses for this command:

 * `kgtk count` produces a KGTK output file with non-empty value counts.
   Each column in the input file
   produces an edge in the output file with the name of the column in node1` and the
   number of non-empty data values in the column in `node2`.

 * `kgtk wc` (aka `kgtk count --lines`) counts the number of data lines (edges, records)
   in the input file.  The header line is not included in the count.  The output count
   is written to standard output as a single number, not as a KGTK file.

`kgtk count` or `kgtk wc` might be used as a filter at the end of a KGTK
pipeline, such as:

```bash
kgtk cat -i file1.tsv file2.tsv / count
```

```bash
kgtk cat -i file1.tsv file2.tsv / wc
```

## Usage

```
usage: kgtk count [-h] [-i INPUT_FILE] [-o OUTPUT_FILE] [-l [True/False]]
                  [-v [optional True|False]]

Count the number of records in a KGTK file, excluding the header record, or count the number of non-empty values per column.  Note:  not non-empty unique values, that is what `kgtk unique` does.

Additional options are shown in expert help.
kgtk --expert lift --help

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK input file. (May be omitted or '-' for
                        stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for
                        stdout.)
  -l [True/False], --lines [True/False]
                        If true, count records and print a single number to
                        stdout. If false, count non-empty values per column
                        and produce a simple KGTK output file.
                        (default=False).

  -v [optional True|False], --verbose [optional True|False]
                        Print additional progress messages (default=False).
```

## Examples

### Sample Input File

Here is a sample input file:

```bash
kgtk cat -i examples/docs/count-file1.tsv
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

### Count the Non-empty Values Per Column

```bash
kgtk count -i examples/docs/count-file1.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| node1 | count | 12 |
| label | count | 12 |
| node2 | count | 12 |
| location | count | 7 |
| years | count | 8 |

### Count the Non-empty Values Per Column in a Pipeline

```bash
kgtk cat -i examples/docs/count-file1.tsv / count
```

| node1 | label | node2 |
| -- | -- | -- |
| node1 | count | 12 |
| label | count | 12 |
| node2 | count | 12 |
| location | count | 7 |
| years | count | 8 |

### Count the Number of Records


```bash
kgtk wc -i examples/docs/count-file1.tsv
```

| 12 |
| -- |

### Count the Number of Records in a Pipeline

```bash
kgtk cat -i examples/docs/count-file1.tsv / wc
```

| 12 |
| -- |
