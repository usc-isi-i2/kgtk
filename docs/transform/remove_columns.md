## Overview

`kgtk remove-columns` removes a subset of the columns from a KGTK file.

!!! note
    This comand can be used to remove the columns of non-KGTK TSV input files (quasi-KGTK files)
    by using the expert option `--mode=NONE`.

!!! note
    The output file should still have required columns (`id` for a KGTK node file, (`node1`, `label`, `node2`)
    for a KGTK edge file).  This requirement may be disabled with the expert option `--mode=NONE`, but the
    output file will not be a valid KGTK node or edge file.

!!! note
    [`kgtk reorder-columns --trim`](../reorder_columns) may be used as an alternative to `kgtk remove-columns`.

!!! info
    See [`kgtk rename-columns`](../rename_columns) if you wish to rename columns.

    See [`kgtk reorder-columns`](../reorder_columns) if you wish to reorder columns.

### List of Column Names

When you use this command, you supply the `--columns` option with
a list of column names in the
order you wish them to appear in the output file.

Column names may be passed to the `--columns` option as an unquoted, space-separated
list, as with other KGTK commands.

By default, column names are split on commas (`,`), unless `--split-on-commas=FALSE` is specified.

By default, leading and trailing whitespace is removed from column names,
unless `--strip-spaces=FALSE` is specified.

Column names can be passed as a quoted list and split on spaces, if `--split-on-spaces=TRUE` is specified.

## Usage
```
usage: kgtk remove-columns [-h] [-i INPUT_FILE] [-o OUTPUT_FILE] -c COLUMNS
                           [COLUMNS ...] [--split-on-commas [SPLIT_ON_COMMAS]]
                           [--split-on-spaces [SPLIT_ON_SPACES]]
                           [--strip-spaces [STRIP_SPACES]]
                           [--all-except [ALL_EXCEPT]]
                           [--ignore-missing-columns [IGNORE_MISSING_COLUMNS]]
                           [-v [optional True|False]]

Remove specific columns from a KGTK file.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK input file. (May be omitted or '-' for
                        stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for
                        stdout.)
  -c COLUMNS [COLUMNS ...], --columns COLUMNS [COLUMNS ...]
                        Columns to remove as a comma- or space-separated
                        strings, e.g., id,docid or id docid
  --split-on-commas [SPLIT_ON_COMMAS]
                        When True, parse the list of columns, splitting on
                        commas. (default=True).
  --split-on-spaces [SPLIT_ON_SPACES]
                        When True, parse the list of columns, splitting on
                        spaces. (default=False).
  --strip-spaces [STRIP_SPACES]
                        When True, parse the list of columns, stripping
                        whitespace. (default=True).
  --all-except [ALL_EXCEPT]
                        When True, remove all columns except the listed ones.
                        (default=False).
  --ignore-missing-columns [IGNORE_MISSING_COLUMNS]
                        When True, ignore missing columns. (default=False).

  -v [optional True|False], --verbose [optional True|False]
                        Print additional progress messages (default=False).
```
## Examples

### Sample Data

Suppose that `file1.tsv` contains the following table in KGTK format:

```bash
kgtk cat -i examples/docs/remove-columns-file1.tsv
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


### Remove Specific Columns using an Unquoted List

Copy `file1.tsv`, sending the output to standard output,
removing the columns `location` and `years`, using an
unquoted list:

```
kgtk remove-columns -i examples/docs/remove-columns-file1.tsv \
                    --columns location years
```
| node1 | label | node2 |
| -- | -- | -- |
| john | zipcode | 12345 |
| john | zipcode | 12346 |
| peter | zipcode | 12040 |
| peter | zipcode | 12040 |
| peter | zipcode | 12040 |
| peter | zipcode | 12040 |
| steve | zipcode | 45601 |
| steve | zipcode | 45601 |
| steve | zipcode | 45601 |
| steve | zipcode | 45601 |
| steve | zipcode | 45601 |
| steve | zipcode | 45601 |

### Remove Specific Columns using an Unquoted List, Allowing Commas

Copy `file1.tsv`, sending the output to standard output,
removing the columns `location` and `years`, using an
unquoted list that allows commas inside column names

!!! note
    The sample data does not include a column name with commas
    in it, so this is not a very good example.  If it did, there would be a warning message whenever
    a KGTK command reads the file's header record.

```
kgtk remove-columns -i examples/docs/remove-columns-file1.tsv \
                    --split-on-commas False \
                    --columns location years
```
| node1 | label | node2 |
| -- | -- | -- |
| john | zipcode | 12345 |
| john | zipcode | 12346 |
| peter | zipcode | 12040 |
| peter | zipcode | 12040 |
| peter | zipcode | 12040 |
| peter | zipcode | 12040 |
| steve | zipcode | 45601 |
| steve | zipcode | 45601 |
| steve | zipcode | 45601 |
| steve | zipcode | 45601 |
| steve | zipcode | 45601 |
| steve | zipcode | 45601 |

### Remove Specific Columns using a Comma-Separated List

Copy `file1.tsv`, sending the output to standard output,
removing the columns `location` and `years`, using a
comma-separated list:

```
kgtk remove-columns -i examples/docs/remove-columns-file1.tsv \
                    --columns location,years
```
| node1 | label | node2 |
| -- | -- | -- |
| john | zipcode | 12345 |
| john | zipcode | 12346 |
| peter | zipcode | 12040 |
| peter | zipcode | 12040 |
| peter | zipcode | 12040 |
| peter | zipcode | 12040 |
| steve | zipcode | 45601 |
| steve | zipcode | 45601 |
| steve | zipcode | 45601 |
| steve | zipcode | 45601 |
| steve | zipcode | 45601 |
| steve | zipcode | 45601 |

### Remove Specific Columns using Quotes and Spaces

Copy `file1.tsv`, sending the output to standard output,
removing the columns `location` and `years`, using a
quoted, space-separated list:

```
kgtk remove-columns -i examples/docs/remove-columns-file1.tsv \
                    --split-on-spaces True \
                    --columns "location years"
```
| node1 | label | node2 |
| -- | -- | -- |
| john | zipcode | 12345 |
| john | zipcode | 12346 |
| peter | zipcode | 12040 |
| peter | zipcode | 12040 |
| peter | zipcode | 12040 |
| peter | zipcode | 12040 |
| steve | zipcode | 45601 |
| steve | zipcode | 45601 |
| steve | zipcode | 45601 |
| steve | zipcode | 45601 |
| steve | zipcode | 45601 |
| steve | zipcode | 45601 |

### Removing Required Columns

Copy `file1.tsv`, sending the output to standard output, removing the columns
`label` and `node2`, using a space-separated list.  The output file is an invalid
KGTK file (a quasi-KGTK file), which requires that "--mode=NONE" be specified:

```
kgtk remove-columns -i examples/docs/remove-columns-file1.tsv \
                    --split-on-spaces True --mode=NONE \
                    --columns "label node2"
```

| node1 | location | years |
| -- | -- | -- |
| john | home | 10 |
| john |  |  |
| peter | home |  |
| peter | cabin |  |
| peter | work | 5 |
| peter |  | 6 |
| steve |  | 3 |
| steve |  | 4 |
| steve |  | 5 |
| steve | home | 1 |
| steve | work | 2 |
| steve | cabin |  |

!!! note
    Quasi-KGTK input files may also be processed by specifying `--mode=NONE`.
