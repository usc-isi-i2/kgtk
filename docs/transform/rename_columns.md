The rename_columns command renames file columns while copying a KGTK file from input to output.
## Usage

```
usage: kgtk rename-columns [-h] [-o OUTPUT_FILE_PATH]
                           [--output-columns NEW_COLUMN_NAME [NEW_COLUMN_NAME ...]]
                           [--old-columns OLD_COLUMNS_NAME [OLD_COLUMNS_NAME ...]]
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
kgtk --expert rename-columns --help

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

| node1 | label   | node2 | location |
| ----- | ------- | ----- | -------- |
| john  | zipcode | 12345 | home     |
| john  | zipcode | 12346 | work     |
| peter | zipcode | 12040 | home     |
| peter | zipcode | 12040 | work     |
| steve | zipcode | 45601 | home     |
| steve | zipcode | 45601 | work     |

Copy `file1.tsv`, sending the output to standard output, renaming
the `location` column to `where`

```
kgtk rename_columns file1.tsv --old-columns location --new-columns where
```

The result will be the following table in KGTK format:
| node1 | label   | node2 | where |
| ----- | ------- | ----- | ----- |
| john  | zipcode | 12345 | home  |
| john  | zipcode | 12346 | work  |
| peter | zipcode | 12040 | home  |
| peter | zipcode | 12040 | work  |
| steve | zipcode | 45601 | home  |
| steve | zipcode | 45601 | work  |

Copy `file1.tsv`, sending the output to standard output, naming
all columns in the output file:

```
kgtk rename_columns file1.tsv --output-columns node1 label node2 where
```

The result will be the following table in KGTK format:
| node1 | label   | node2 | where |
| ----- | ------- | ----- | ----- |
| john  | zipcode | 12345 | home  |
| john  | zipcode | 12346 | work  |
| peter | zipcode | 12040 | home  |
| peter | zipcode | 12040 | work  |
| steve | zipcode | 45601 | home  |
| steve | zipcode | 45601 | work  |
