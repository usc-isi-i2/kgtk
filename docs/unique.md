The ifexists command reads a KGTK file, constructing a second KGTK file
containing the unique values and counts for a column in the first file.

This implementation, in Python, builds an im-memory dictionary of the unique
values and counts.  Performance will be poor, and execution may fail, if there
are a very large number of unique values.

In the default output format, the output file is a KGTK edge file.
The node1 column contains the unique values, thelabel column is `count`,
and the node2 column contains the unique count.

Since KGTK edge files cannot have an empty node1 column, the `--empty value`
option provides a substitute value (e.g. NONE) that will be used in the ouput
KGTK file to represent empty values in the input KGTK file.

The value used in the `label` column, normally `count`, may be changed
with the `--label VALUE` option.

There are two expert options specifically for this command:

The `--prefix VALUE` option supplies a prefix to the value in the output file.

The `--format node` option creates a KGTK node file as its output.  The value
(prefixed if requested) appears in the `id` column of the output file, and new
columns (prefixed) are created for each unique value found in the specified
column in the input file.

## Usage

```bash
usage: kgtk unique [-h] --column COLUMN_NAME [--empty EMPTY_VALUE] [-o OUTPUT_KGTK_FILE]
                   [--label LABEL_VALUE] [-v]
                   [input_kgtk_file]

Count the unique values in a column in a KGTK file. Write the unique values and counts as a new KGTK file.

Additional options are shown in expert help.
kgtk --expert ifnotempty --help

positional arguments:
  input_kgtk_file       The KGTK file to filter. May be omitted or '-' for stdin.

optional arguments:
  -h, --help            show this help message and exit
  --column COLUMN_NAME  The column to count unique values (required).
  --empty EMPTY_VALUE   A value to substitute for empty values (default=).
  -o OUTPUT_KGTK_FILE, --output-file OUTPUT_KGTK_FILE
                        The KGTK file to write (required).
  --label LABEL_VALUE   The output file label column value (default=count).

  -v, --verbose         Print additional progress messages (default=False).

```

Expert help:
```
usage: kgtk unique [-h] --column COLUMN_NAME [--empty EMPTY_VALUE] [-o OUTPUT_KGTK_FILE]
                   [--label LABEL_VALUE] [--format {edge,node}] [--prefix PREFIX]
                   [--errors-to-stdout | --errors-to-stderr] [--show-options] [-v]
                   [--very-verbose] [--column-separator COLUMN_SEPARATOR]
                   [--compression-type COMPRESSION_TYPE] [--error-limit ERROR_LIMIT]
                   [--gzip-in-parallel [GZIP_IN_PARALLEL]] [--gzip-queue-size GZIP_QUEUE_SIZE]
                   [--mode {NONE,EDGE,NODE,AUTO}]
                   [--force-column-names FORCE_COLUMN_NAMES [FORCE_COLUMN_NAMES ...]]
                   [--header-error-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}]
                   [--skip-first-record [SKIP_FIRST_RECORD]]
                   [--unsafe-column-name-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}]
                   [--repair-and-validate-lines [REPAIR_AND_VALIDATE_LINES]]
                   [--repair-and-validate-values [REPAIR_AND_VALIDATE_VALUES]]
                   [--blank-required-field-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}]
                   [--comment-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}]
                   [--empty-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}]
                   [--fill-short-lines [FILL_SHORT_LINES]]
                   [--invalid-value-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}]
                   [--long-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}]
                   [--short-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}]
                   [--truncate-long-lines [TRUNCATE_LONG_LINES]]
                   [--whitespace-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}]
                   [--additional-language-codes [ADDITIONAL_LANGUAGE_CODES [ADDITIONAL_LANGUAGE_CODES ...]]]
                   [--allow-language-suffixes [ALLOW_LANGUAGE_SUFFIXES]]
                   [--allow-lax-strings [ALLOW_LAX_STRINGS]]
                   [--allow-lax-lq-strings [ALLOW_LAX_LQ_STRINGS]]
                   [--allow-month-or-day-zero [ALLOW_MONTH_OR_DAY_ZERO]]
                   [--repair-month-or-day-zero [REPAIR_MONTH_OR_DAY_ZERO]]
                   [--minimum-valid-year MINIMUM_VALID_YEAR]
                   [--maximum-valid-year MAXIMUM_VALID_YEAR]
                   [--minimum-valid-lat MINIMUM_VALID_LAT]
                   [--maximum-valid-lat MAXIMUM_VALID_LAT]
                   [--minimum-valid-lon MINIMUM_VALID_LON]
                   [--maximum-valid-lon MAXIMUM_VALID_LON]
                   [--escape-list-separators [ESCAPE_LIST_SEPARATORS]]
                   [input_kgtk_file]

Count the unique values in a column in a KGTK file. Write the unique values and counts as a new KGTK file.

Additional options are shown in expert help.
kgtk --expert unique --help

positional arguments:
  input_kgtk_file       The KGTK file to filter. May be omitted or '-' for stdin.

optional arguments:
  -h, --help            show this help message and exit
  --column COLUMN_NAME  The column to count unique values (required).
  --empty EMPTY_VALUE   A value to substitute for empty values (default=).
  -o OUTPUT_KGTK_FILE, --output-file OUTPUT_KGTK_FILE
                        The KGTK file to write (required).
  --label LABEL_VALUE   The output file label column value (default=count).
  --format {edge,node}  The output file format and mode (default=edge).
  --prefix PREFIX       The value prefix (default=).

...
```
(See `kgtk validate` for a description of additional options)

## Examples

Suppose that `file1.tsv` contains the following table in KGTK format:

| node1 | label   | node2 | location | years |
| ----- | ------- | ----- | -------- | ----- |
| eric  | zipcode | 12040 | work     | 5     |
| john  | zipcode | 12345 | home     | 10    |
| john  | zipcode | 12346 |          |       |
| john  | zipcode | 12347 |          |       |
| peter | zipcode | 12040 | home     |       |
| peter | zipcode | 12040 | work     | 6     |
| steve | zipcode | 45600 |          | 3     |
| steve | zipcode | 45601 | work     |       |


```bash
kgtk unique file1.tsv --column location

```

| node1 | label | node2 |
| ----- | ----- | ----- |
| home  | count | 2     |
| work  | count | 3     |

```bash
kgtk unique file1.tsv --column location --empty NONE

```

| node1 | label | node2 |
| ----- | ----- | ----- |
| NONE  | count | 3     |
| home  | count | 2     |
| work  | count | 3     |

```bash
kgtk unique file1.tsv --column location --empty NONE --format node

```

| id       | NONE | home | work |
| -------- | ---- | ---- | ---- |
| location | 3    | 2    | 3    |

```bash
kgtk unique file1.tsv --column location --empty NONE --format node --prefix 'location;'

```

| id       | location;NONE | location;home | location;work |
| -------- | ---- | ---- | ---- |
| location | 3    | 2    | 3    |

