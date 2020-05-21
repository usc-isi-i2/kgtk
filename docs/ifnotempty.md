The ifnotempty command filters KGTK files, passing through only those rows for
which one (or more) specified columns contain nonempty values.  When multiple
columns are specified, there is the choice of requiring any of the columns to
be not empty or all of the columns to be not empty.

Optionally, report the count of rows that passed the filter instead of
copying the rows to the output file.

## Usage

```
usage: kgtk ifnotempty [-h] --columns FILTER_COLUMN_NAMES [FILTER_COLUMN_NAMES ...]
                       [--count [ONLY_COUNT]] [-o OUTPUT_KGTK_FILE] [--all [ALL_ARE]] [-v]
                       [input_kgtk_file]

Filter a KGTK file based on whether one or more fields are not empty. When multiple fields are specified, either any field or all fields must be not empty.

Additional options are shown in expert help.
kgtk --expert ifnotempty --help

positional arguments:
  input_kgtk_file       The KGTK file to filter. May be omitted or '-' for stdin.

optional arguments:
  -h, --help            show this help message and exit
  --columns FILTER_COLUMN_NAMES [FILTER_COLUMN_NAMES ...]
                        The columns in the file being filtered (Required).
  --count [ONLY_COUNT]  Only count the records, do not copy them. (default=False).
  -o OUTPUT_KGTK_FILE, --output-file OUTPUT_KGTK_FILE
                        The KGTK file to write (default=-).
  --all [ALL_ARE]       False: Test if any are, True: test if all are (default=False).

  -v, --verbose         Print additional progress messages (default=False).
```

## Examples

Suppose that `file1.tsv` contains the following table in KGTK format:

| node1 | label   | node2 | location | years |
| ----- | ------- | ----- | -------- | ----- |
| john  | zipcode | 12345 | home     | 10    |
| john  | zipcode | 12346 |          |       |
| peter | zipcode | 12040 | home     |       |
| peter | zipcode | 12040 | work     | 6     |
| steve | zipcode | 45600 |          | 3     |
| steve | zipcode | 45601 |          |       |

```bash
kgtk ifnotempty file1.tsv --columns location
```
| node1 | label   | node2 | location | years |
| ----- | ------- | ----- | -------- | ----- |
| john  | zipcode | 12345 | home     | 10    |
| peter | zipcode | 12040 | home     |       |
| peter | zipcode | 12040 | work     | 6     |

```bash
kgtk ifnotempty file1.tsv --columns years
```
| node1 | label   | node2 | location | years |
| ----- | ------- | ----- | -------- | ----- |
| john  | zipcode | 12345 | home     | 10    |
| peter | zipcode | 12040 | work     | 6     |
| steve | zipcode | 45600 |          | 3     |

```bash
kgtk ifnotempty file1.tsv --columns location years
```
| node1 | label   | node2 | location | years |
| ----- | ------- | ----- | -------- | ----- |
| john  | zipcode | 12345 | home     | 10    |
| john  | zipcode | 12346 |          |       |
| peter | zipcode | 12040 | home     |       |
| peter | zipcode | 12040 | work     | 6     |
| steve | zipcode | 45600 |          | 3     |

```bash
kgtk ifnotempty file1.tsv --all --columns location years
```
| node1 | label   | node2 | location | years |
| ----- | ------- | ----- | -------- | ----- |
| john  | zipcode | 12345 | home     | 10    |
| peter | zipcode | 12040 | work     | 6     |
