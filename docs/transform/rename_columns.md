## Overview

The rename-columns command renames file columns while copying a KGTK file from input to output.

!!! note
    This comand can be used to remove the columns of non-KGTK TSV input files (quasi-KGTK files)
    by using the expert option `--mode=NONE`.

!!! note
    The output file should still have required columns (`id` for a KGTK node file, (`node1`, `label`, `node2`)
    for a KGTK edge file).  This requirement may be disabled with the expert option `--mode=NONE`, but the
    output file will not be a valid KGTK node or edge file.

!!! info
    See [`kgtk remove-columns`](../remove_columns) if you wish to remove columns.

    See [`kgtk reorder-columns`](../reorder_columns) if you wish to reorder columns.

## Usage

```
usage: kgtk rename-columns [-h] [-i INPUT_FILE] [-o OUTPUT_FILE]
                           [--output-columns NEW_COLUMN_NAME [NEW_COLUMN_NAME ...]]
                           [--old-columns OLD_COLUMN_NAME [OLD_COLUMN_NAME ...]]
                           [--new-columns NEW_COLUMN_NAME [NEW_COLUMN_NAME ...]]
                           [-v [optional True|False]]

This command renames one or more columns in a KGTK file. 

Rename all columns using --output-columns newname1 newname2 ... 
Rename selected columns using --old-columns and --new-columns 

The column names are listed seperately for each option, do not quote them as a group, e.g. 
kgtk rename_columns --old-columns oldname1 oldname2 --new-columns newname1 nsewname2

The input filename must come before --output-columns, --old-columns, or --new-columns. 
If no input filename is provided, the default is to read standard input. 

Additional options are shown in expert help.
kgtk --expert rename-columns --help

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK input file. (May be omitted or '-' for
                        stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for
                        stdout.)
  --output-columns NEW_COLUMN_NAME [NEW_COLUMN_NAME ...]
                        The list of new column names when renaming all
                        columns.
  --old-columns OLD_COLUMN_NAME [OLD_COLUMN_NAME ...]
                        The list of old column names for selective renaming.
  --new-columns NEW_COLUMN_NAME [NEW_COLUMN_NAME ...]
                        The list of new column names for selective renaming.

  -v [optional True|False], --verbose [optional True|False]
                        Print additional progress messages (default=False).
```

## Examples

Suppose that `file1.tsv` contains the following table in KGTK format:

```bash
kgtk cat -i examples/docs/rename-columns-file1.tsv
```

| node1 | label | node2 | location |
| -- | -- | -- | -- |
| john | zipcode | 12345 | home |
| john | zipcode | 12346 | work |
| peter | zipcode | 12040 | home |
| peter | zipcode | 12040 | work |
| steve | zipcode | 45601 | home |
| steve | zipcode | 45601 | work |

### Rename One Column

Copy `file1.tsv`, sending the output to standard output, renaming
the `location` column to `where`:

```
kgtk rename-columns -i examples/docs/rename-columns-file1.tsv \
                    --old-columns location \
                    --new-columns where
```

The result will be the following table in KGTK format:

| node1 | label | node2 | where |
| -- | -- | -- | -- |
| john | zipcode | 12345 | home |
| john | zipcode | 12346 | work |
| peter | zipcode | 12040 | home |
| peter | zipcode | 12040 | work |
| steve | zipcode | 45601 | home |
| steve | zipcode | 45601 | work |

### Swap `node1` and `node2` Without Reordering

Copy `file1.tsv`, sending the output to standard output,
swapping the `node1` and `node2` columns by renaming them:

```
kgtk rename-columns -i examples/docs/rename-columns-file1.tsv \
                    --old-columns node1 node2 \
                    --new-columns node2 node1
```

| node2 | label | node1 | location |
| -- | -- | -- | -- |
| john | zipcode | 12345 | home |
| john | zipcode | 12346 | work |
| peter | zipcode | 12040 | home |
| peter | zipcode | 12040 | work |
| steve | zipcode | 45601 | home |
| steve | zipcode | 45601 | work |

!!! note
    The `node1` and `node2` columns in this example are logically swapped,
    but not physically swapped.  If you need to reorder the columns as well
    as renaming them, use [`kgtk reorder-columns`](../reorder_columns),
    as shown in the next example.

### Swap `node1` and `node2` with Reordering

Copy `file1.tsv`, sending the output to standard output,
swapping the `node1` and `node2` columns by renaming the columns
with `kgtk rename-columns` and reordering the columns with
[`kgtk reorder-columns`](../reorder_columns):

```
kgtk rename-columns -i examples/docs/rename-columns-file1.tsv \
                    --old-columns node1 node2 \
                    --new-columns node2 node1 \
   / reorder-columns --columns node1 label node2 ...
```

| node1 | label | node2 | location |
| -- | -- | -- | -- |
| 12345 | zipcode | john | home |
| 12346 | zipcode | john | work |
| 12040 | zipcode | peter | home |
| 12040 | zipcode | peter | work |
| 45601 | zipcode | steve | home |
| 45601 | zipcode | steve | work |


### Rename All Columns

Copy `file1.tsv`, sending the output to standard output, renaming
all columns in the output file:

```
kgtk rename-columns -i examples/docs/rename-columns-file1.tsv \
                    --output-columns node1 label node2 where
```

The result will be the following table in KGTK format:

| node1 | label | node2 | where |
| -- | -- | -- | -- |
| john | zipcode | 12345 | home |
| john | zipcode | 12346 | work |
| peter | zipcode | 12040 | home |
| peter | zipcode | 12040 | work |
| steve | zipcode | 45601 | home |
| steve | zipcode | 45601 | work |

### Expert Example: Rename All Columns Creating a Quasi-KGTK File.

Occasionally you may wish to create a quasi-KGTK file (e.g., a KGTK
file that does not contain the required column names).  For example, you
may need certain names on the columns to clarify their meaning in a
report.  To accomplish this, you will need to include the expert option
`--mode=NONE` on the command line.

Copy `file1.tsv`, sending the output to standard output, renaming
all columns in the output file, including renaming some of the required
columns to nonstandard names:
```
kgtk rename-columns -i examples/docs/rename-columns-file1.tsv \
                    --old-columns node1 node2 location \
                    --new-columns Employee 'Zip Code' 'Home or Work' \
                    --mode=NONE
```

| Employee | label | Zip Code | Home or Work |
| -- | -- | -- | -- |
| john | zipcode | 12345 | home |
| john | zipcode | 12346 | work |
| peter | zipcode | 12040 | home |
| peter | zipcode | 12040 | work |
| steve | zipcode | 45601 | home |
| steve | zipcode | 45601 | work |

!!! note
    Quasi-KGTK input files may also be processed by specifying `--mode=NONE`.
