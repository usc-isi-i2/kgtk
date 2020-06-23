The reorder_columns command reorders file columns while copying a KGTK file from input to output.
## Usage

```
usage: kgtk rename_columns [-h] [-o OUTPUT_FILE_PATH]
                           [--output-columns NEW_COLUMN_NAME [NEW_COLUMN_NAME ...]]
                           [--old-columns OLD_COLUMN_NAME [OLD_COLUMN_NAME ...]]
                           [--new-columns NEW_COLUMN_NAME [NEW_COLUMN_NAME ...]] [-v]
                           input_file_path

This command renames one or more columns in a KGTK file. 

Rename all columns using --output-columns newname1 newname2 ... 
Rename selected columns using --old-columns and --new-columns 

The column names are listed seperately for each option, do not quote them as a group, e.g. 
kgtk rename_columns --old-columns oldname1 oldname2 --new-columns newname1 nsewname2

The input filename must come before --output-columns, --old-columns, or --new-columns. 
If no input filename is provided, the default is to read standard input. 

Additional options are shown in expert help.
kgtk --expert rename_columns --help

positional arguments:
  input_file_path       The KGTK input file. (default=-).

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_FILE_PATH, --output-file OUTPUT_FILE_PATH
                        The KGTK file to write (default=-).
  --output-columns NEW_COLUMN_NAME [NEW_COLUMN_NAME ...]
                        The list of new column names when renaming all columns.
  --old-columns OLD_COLUMN_NAME [OLD_COLUMN_NAME ...]
                        The list of old column names for selective renaming.
  --new-columns NEW_COLUMN_NAME [NEW_COLUMN_NAME ...]
                        The list of new column names for selective renaming.

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
kgtk -i reorder_columns file1.tsv --columns ... years location
```

The result will be the following table in KGTK format:
880% kgtk reorder_columns -i kgtk/join/test/compact-file2.tsv --columns ... years location --output-format md
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
kgtk -i reorder_columns file1.tsv --columns location ...
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
kgtk -i reorder_columns file1.tsv --columns label node1 node2 years location
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
