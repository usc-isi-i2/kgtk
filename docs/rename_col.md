The rename_col command renames file columns while copying one
(or more) KGTK files from input to output. See the `kgtk cat`
command for more details on how KGTK files are concatenated and merged.
## Usage

```
usage: kgtk rename_col [-h] [-o OUTPUT_FILE_PATH] [--output-columns OUTPUT_COLUMN_NAMES [OUTPUT_COLUMN_NAMES ...]]
                       [--old-columns OLD_COLUMN_NAMES [OLD_COLUMN_NAMES ...]] [--new-columns NEW_COLUMN_NAMES [NEW_COLUMN_NAMES ...]] [-v]
                       input_file_paths [input_file_paths ...]

Rename KGT file columns while concatenating KGTK files. All files must be KGTK edge files or all files must be KGTK node files (unless overridden with --mode=NONE). Rename all columns or selected columns. 

Additional options are shown in expert help.
kgtk --expert rename_col --help

positional arguments:
  input_file_paths      The KGTK files to concatenate while renaming columns.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_FILE_PATH, --output-file OUTPUT_FILE_PATH
                        The KGTK file to write (default=-).
  --output-columns OUTPUT_COLUMN_NAMES [OUTPUT_COLUMN_NAMES ...]
                        Rename all output columns. (default=None)
  --old-columns OLD_COLUMN_NAMES [OLD_COLUMN_NAMES ...]
                        Rename seleted output columns: old names. (default=None)
  --new-columns NEW_COLUMN_NAMES [NEW_COLUMN_NAMES ...]
                        Rename seleted output columns: new names. (default=None)

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

```bash
kgtk rename_col file1.tsv --old-columns location --new-columns where

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

```bash
kgtk rename_col file1.tsv --output-columns node1 label node2 where

The result will be the following table in KGTK format:
| node1 | label   | node2 | where |
| ----- | ------- | ----- | ----- |
| john  | zipcode | 12345 | home  |
| john  | zipcode | 12346 | work  |
| peter | zipcode | 12040 | home  |
| peter | zipcode | 12040 | work  |
| steve | zipcode | 45601 | home  |
| steve | zipcode | 45601 | work  |
