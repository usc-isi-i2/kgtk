The expand command copies its input file to its output file,
expanding | lists into multiple records.

## Usage

```bash
usage: kgtk expand [-h] [--columns KEY_COLUMN_NAMES [KEY_COLUMN_NAMES ...]]
                   [-o OUTPUT_KGTK_FILE] [-v]
                   [input_kgtk_file]

Copy a KGTK file, expanding | lists into multiple records. 

Additional options are shown in expert help.
kgtk --expert expand --help

positional arguments:
  input_kgtk_file       The KGTK file to filter. May be omitted or '-' for stdin (default=-).

optional arguments:
  -h, --help            show this help message and exit
  --columns KEY_COLUMN_NAMES [KEY_COLUMN_NAMES ...]
                        The key columns will not be expanded. They will be repeated on each
                        output record. (default=id for node files, (node1, label, node2) for
                        edge files).
  -o OUTPUT_KGTK_FILE, --output-file OUTPUT_KGTK_FILE
                        The KGTK file to write (default=-).

  -v, --verbose         Print additional progress messages (default=False).
```

## Examples

Suppose that `file1.tsv` contains the following table in KGTK format:

| node1 | label   | node2 | location          | years   |
| ----- | ------- | ----- | ----------------- | ------- |
| john  | zipcode | 12345 | home              | 10      |
| john  | zipcode | 12346 |                   |         |
| peter | zipcode | 12040 | home\|cabin       |         |
| peter | zipcode | 12040 | work              | 5\|6    |
| steve | zipcode | 45600 |                   | 3\|4\|5 |
| steve | zipcode | 45601 | home\|work\|cabin | 1\|2    |

```bash
kgtk expand file1.tsv
```

The output will be the following table in KGTK format:

| node1 | label   | node2 | location  | years |
| ----- | ------- | ----- | --------- | ----- |
| john  | zipcode | 12345 | home      | 10    |
| john  | zipcode | 12346 |           |       |
| peter | zipcode | 12040 | home      |       |
| peter | zipcode | 12040 | cabin     |       |
| peter | zipcode | 12040 | work      | 5     |
| peter | zipcode | 12040 |           | 6     |
| steve | zipcode | 45600 |           | 3     |
| steve | zipcode | 45600 |           | 4     |
| steve | zipcode | 45600 |           | 5     |
| steve | zipcode | 45601 | home      | 1     |
| steve | zipcode | 45601 | work      | 2     |
| steve | zipcode | 45601 | cabin     |       |
