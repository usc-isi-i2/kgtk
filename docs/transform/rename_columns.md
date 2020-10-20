The rename-columns command renames file columns while copying a KGTK file from input to output.
## Usage

```
usage: kgtk rename-columns [-h] [-i INPUT_FILE] [-o OUTPUT_FILE]
                           [--output-columns NEW_COLUMN_NAME [NEW_COLUMN_NAME ...]]
                           [--old-columns OLD_COLUMN_NAME [OLD_COLUMN_NAME ...]]
                           [--new-columns NEW_COLUMN_NAME [NEW_COLUMN_NAME ...]] [-v]

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
                        The KGTK input file. (May be omitted or '-' for stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for stdout.)
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
kgtk rename-columns -i file1.tsv --old-columns location --new-columns where
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
kgtk rename-columns -i file1.tsv --output-columns node1 label node2 where
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
