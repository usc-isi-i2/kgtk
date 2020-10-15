The unique command reads a KGTK file, constructing a second KGTK file
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

Usint the `--where name` and `--in value(s)` options, you can restrict the
count to records where the value in a specified column matches a list of
specified values.

## Usage

```
usage: kgtk unique [-h] [-i INPUT_FILE] [-o OUTPUT_FILE] --column COLUMN_NAME
                   [--empty EMPTY_VALUE] [--label LABEL_VALUE] [--where WHERE_COLUMN_NAME]
                   [--in WHERE_VALUES [WHERE_VALUES ...]] [-v]

Count the unique values in a column in a KGTK file. Write the unique values and counts as a new KGTK file.

Additional options are shown in expert help.
kgtk --expert unique --help

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK input file. (May be omitted or '-' for stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for stdout.)
  --column COLUMN_NAME  The column to count unique values (required).
  --empty EMPTY_VALUE   A value to substitute for empty values (default=).
  --label LABEL_VALUE   The output file label column value (default=count).
  --where WHERE_COLUMN_NAME
                        The name of a column for a record selection test. (default=None).
  --in WHERE_VALUES [WHERE_VALUES ...]
                        The list of values for a record selection test. (default=None).

  -v, --verbose         Print additional progress messages (default=False).
```

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
kgtk unique -i file1.tsv --column location

```

| node1 | label | node2 |
| ----- | ----- | ----- |
| home  | count | 2     |
| work  | count | 3     |

```bash
kgtk unique -i file1.tsv --column location --empty NONE

```

| node1 | label | node2 |
| ----- | ----- | ----- |
| NONE  | count | 3     |
| home  | count | 2     |
| work  | count | 3     |

```bash
kgtk unique -i file1.tsv --column location --empty NONE --format node

```

| id       | NONE | home | work |
| -------- | ---- | ---- | ---- |
| location | 3    | 2    | 3    |

```bash
kgtk unique -i file1.tsv --column location --empty NONE --format node --prefix 'location;'

```

| id       | location;NONE | location;home | location;work |
| -------- | ---- | ---- | ---- |
| location | 3    | 2    | 3    |

```bash
kgtk unique -i file1.tsv --column location --where node1 --in peter
```

| node1 | label | node2 |
| -- | -- | -- |
| home | count | 1 |
| work | count | 1 |
