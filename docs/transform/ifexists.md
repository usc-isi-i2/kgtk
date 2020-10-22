The ifexists command filters a KGTK file, passing through only those rows for
which one or more specified columns match records in a second KGTK file.

This implementation, in Python, builds an in-memory dictionary of the key
values in the --filter-on file.  Performance will be poor, and execution may
fail, if the --filter-on file is very large.  Alternatively, the --cache-input
option causes the code to cache the input file and not the --on-filter-file.
Optionally, presort the input and filter files and use --presorted to avoid
caching.

By default, input records are passed in order to the output file.  When                                                                                        
the input file is cached, the output records are order by key value (alpha                                                                                           
sort), then by input order.

The fields to match may be supplied by the user.  If not supplied, the
following defaults will be used.  "left" refers to the KFTK file being
filtered, and "right" refers to the file supplying the matching records.

| Left    | Right   | Key fields |
| ------- | ------- | ---------- |
| edge    | edge    | left.node1 == right.node1 and |
|         |         | left.label == right.label and |
|         |         | left.node2 == right.node2 |
| node    | node    | left.id    == right.id |
| edge    | node    | left.node1 == right.id |
| node    | edge    | right.id   == left.node1 |

## Usage

```
usage: kgtk ifexists [-h] [-i INPUT_FILE] [--filter-on FILTER_FILE] [-o OUTPUT_FILE]
                     [--input-keys [INPUT_KEYS [INPUT_KEYS ...]]]
                     [--filter-keys [FILTER_KEYS [FILTER_KEYS ...]]]
                     [--cache-input [True|False]] [--preserve-order [True|False]] [-v]

Filter a KGTK file based on whether one or more records exist in a second KGTK file with matching values for one or more fields.

Additional options are shown in expert help.
kgtk --expert ifexists --help

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK input file. (May be omitted or '-' for stdin.)
  --filter-on FILTER_FILE, --filter-file FILTER_FILE
                        The KGTK file to filter against (required). (May be omitted or '-'
                        for stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for stdout.)
  --reject-file REJECT_FILE
                        The KGTK reject file for records that fail the filter. (Optional, use '-' for stdout.)
  --matched-filter-file MATCHED_FILTER_FILE
                        The KGTK file for filter records that matched at least one input record. (Optional, use '-' for stdout.)
  --unmatched-filter-file UNMATCHED_FILTER_FILE
                        The KGTK file for filter records that did not match any input records. (Optional, use '-' for stdout.)
  --input-keys [INPUT_KEYS [INPUT_KEYS ...]], --left-keys [INPUT_KEYS [INPUT_KEYS ...]]
                        The key columns in the file being filtered (default=None).
  --filter-keys [FILTER_KEYS [FILTER_KEYS ...]], --right-keys [FILTER_KEYS [FILTER_KEYS ...]]
                        The key columns in the filter-on file (default=None).
  --cache-input [True|False]
                        Cache the input file instead of the filter keys (default=False).
  --preserve-order [True|False]
                        Preserve record order when cacheing the input file. (default=False).

  --presorted [True|False]
                        When True, assume that the input and filter files are both presorted. Use a merge-style algorithm that does not require caching either
                        file. (default=False).

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
| steve | zipcode | 45601 | work     |       |

Suppose that `file2.tsv` contains the following table in KGTK format:

| node1 | label   | node2 |
| ----- | ------- | ----- |
| peter | zipcode | 12040 |

Suppose that `file3.tsv` contains the following table in KGTK format:

| id    |
| ----- |
| steve |
| john  |

Suppose that `file4.tsv` contains the following table in KGTK format:

| id    |
| ----- |
| peter |
| john  |

Suppose that `file5.tsv` contains the following table in KGTK format:

| id   |
| ---- |
| home |

```bash
kgtk ifexists -i file1.tsv --filter-on file2.tsv

```

| node1 | label   | node2 | location | years |
| ----- | ------- | ----- | -------- | ----- |
| peter | zipcode | 12040 | home     |       |
| peter | zipcode | 12040 | work     | 6     |

```bash
kgtk ifexists -i file1.tsv --filter-on file3.tsv

```
| node1 | label   | node2 | location | years |
| ----- | ------- | ----- | -------- | ----- |
| john  | zipcode | 12345 | home     | 10    |
| john  | zipcode | 12346 |          |       |
| steve | zipcode | 45600 |          | 3     |
| steve | zipcode | 45601 | work     |       |

```bash
kgtk ifexists -i file4.tsv --filter-on file3.tsv

```
| id    |
| ----- |
| john  |

```bash
kgtk ifexists -i file1.tsv --filter-on file5.tsv --input-keys location

```
| node1 | label   | node2 | location | years |
| ----- | ------- | ----- | -------- | ----- |
| john  | zipcode | 12345 | home     | 10    |
| peter | zipcode | 12040 | home     |       |
