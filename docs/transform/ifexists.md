## Overview

The ifexists command filters a KGTK file (the input file), passing through only those rows for
which one or more specified columns match records in a second KGTK file (the filter file).

### Memory Useage Options

This implementation of `ifexists` is written in Python.  By default, it builds
an in-memory dictionary of the key values it finds in the `--filter-on` file
before processing the `--input-file` .  Performance will be poor, and execution may
fail, if the `--filter-on` file is too large for the key dictionary to fit into main memory.

If the input file is small, the `--cache-input`
option can be used to tell the code to cache the `--input-file` instead of the `--filter-on` file.
After cacheing the `--input-file`, the code will make a single pass through the `--filter-on` file.

If both the `--input-file` and the `--filter-on` file are too large to hold in
memory, then you should presort the input and filter files on their key
columns using `kgtk sort`, followed by using `kgtk filter --presorted` to avoid caching
either file.

### Output Record Order

Normally, input records are passed in order to the output file.  However, when
the input file is cached (`--cache-input`), the default is for the output
records to ordered by key value (alpha sort), then by input order.  If you
wish the output file to retain the input file's order when cacheing the
input file, use the ``--preserve-order` option.

### Matching Fields

The fields to match may be supplied by the user using `--input-keys` and `--filter-keys`.
If not supplied, the following defaults will be used, which depend on the KGTK file type
(edge or node) of the input and filter files.

| Input File Type | Filter File Type   | Key fields |
| ------- | ------- | ---------- |
| edge    | edge    | input.node1 == filter.node1 and |
|         |         | input.label == filter.label and |
|         |         | input.node2 == filter.node2 |
| node    | node    | input.id    == filter.id |
| edge    | node    | input.node1 == filter.id |
| node    | edge    | input.id   == filter.node1 |

### Optional Output Files

The `--reject-file`, when specified, will receive any input records
that failed the filter test and were not written to the output file.

The `--matched-filter-file`, when specified, will receive a copy of
any filter records that found a match in the input file.


The `--unmatched-filter-file`, when specified, will receive a copy of
any filter records that did not find a match in the input file.


## Usage

```
usage: kgtk ifexists [-h] [-i INPUT_FILE] [--filter-on FILTER_FILE]
                     [-o OUTPUT_FILE] [--reject-file REJECT_FILE]
                     [--matched-filter-file MATCHED_FILTER_FILE]
                     [--unmatched-filter-file UNMATCHED_FILTER_FILE]
                     [--input-keys [INPUT_KEYS [INPUT_KEYS ...]]]
                     [--filter-keys [FILTER_KEYS [FILTER_KEYS ...]]]
                     [--cache-input [True|False]]
                     [--preserve-order [True|False]]
                     [--presorted [True|False]] [-v [optional True|False]]

Filter a KGTK file based on whether one or more records exist in a second KGTK file with matching values for one or more fields.

Additional options are shown in expert help.
kgtk --expert ifexists --help

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK input file. (May be omitted or '-' for
                        stdin.)
  --filter-on FILTER_FILE, --filter-file FILTER_FILE
                        The KGTK file to filter against. (May be omitted or
                        '-' for stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for
                        stdout.)
  --reject-file REJECT_FILE
                        The KGTK file for input records that fail the filter.
                        (Optional, use '-' for stdout.)
  --matched-filter-file MATCHED_FILTER_FILE
                        The KGTK file for filter records that matched at least
                        one input record. (Optional, use '-' for stdout.)
  --unmatched-filter-file UNMATCHED_FILTER_FILE
                        The KGTK file for filter records that did not match
                        any input records. (Optional, use '-' for stdout.)
  --input-keys [INPUT_KEYS [INPUT_KEYS ...]], --left-keys [INPUT_KEYS [INPUT_KEYS ...]]
                        The key columns in the file being filtered
                        (default=None).
  --filter-keys [FILTER_KEYS [FILTER_KEYS ...]], --right-keys [FILTER_KEYS [FILTER_KEYS ...]]
                        The key columns in the filter-on file (default=None).
  --cache-input [True|False]
                        Cache the input file instead of the filter keys
                        (default=False).
  --preserve-order [True|False]
                        Preserve record order when cacheing the input file.
                        (default=False).
  --presorted [True|False]
                        When True, assume that the input and filter files are
                        both presorted. Use a merge-style algorithm that does
                        not require caching either file. (default=False).

  -v [optional True|False], --verbose [optional True|False]
                        Print additional progress messages (default=False).
```

## Examples

### Sample Data

Suppose that `ifexists-file1.tsv` contains the following table in KGTK format:

```bash
kgtk cat -i examples/docs/ifexists-file1.tsv
```

| node1 | label | node2 | location | years |
| -- | -- | -- | -- | -- |
| john | zipcode | 12345 | home | 10 |
| john | zipcode | 12346 |  |  |
| peter | zipcode | 12040 | home |  |
| peter | zipcode | 12040 | work | 6 |
| steve | zipcode | 45601 |  | 3 |
| steve | zipcode | 45601 | work |  |

!!! note
    This is a KGTK edge file.

Suppose that `ifexists-file2.tsv` contains the following table in KGTK format:

```bash
kgtk cat -i examples/docs/ifexists-file2.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| peter | zipcode | 12040 |

!!! note
    This is a KGTK edge file.

Suppose that `ifexists-file3.tsv` contains the following table in KGTK format:

```bash
kgtk cat -i examples/docs/ifexists-file3.tsv
```

| id |
| -- |
| steve |
| john |

!!! note
    This is a KGTK node file.

Suppose that `ifexists-file4.tsv` contains the following table in KGTK format:

```bash
kgtk cat -i examples/docs/ifexists-file4.tsv
```

| id |
| -- |
| peter |
| john |

!!! note
    This is a KGTK node file.

Suppose that `ifexists-file5.tsv` contains the following table in KGTK format:

```bash
kgtk cat -i examples/docs/ifexists-file5.tsv
```

| id |
| -- |
| home |

!!! note
    This is a KGTK node file.

### Filter an Edge File on Another Edge File.

```bash
kgtk ifexists --input-file examples/docs/ifexists-file1.tsv \
              --filter-on examples/docs/ifexists-file2.tsv

```

| node1 | label | node2 | location | years |
| -- | -- | -- | -- | -- |
| peter | zipcode | 12040 | home |  |
| peter | zipcode | 12040 | work | 6 |

### Filter an Edge File on a Node File

```bash
kgtk ifexists --input-file examples/docs/ifexists-file1.tsv \
              --filter-on examples/docs/ifexists-file3.tsv

```
| node1 | label | node2 | location | years |
| -- | -- | -- | -- | -- |
| john | zipcode | 12345 | home | 10 |
| john | zipcode | 12346 |  |  |
| steve | zipcode | 45601 |  | 3 |
| steve | zipcode | 45601 | work |  |

### Filter a Node File on a Node File

```bash
kgtk ifexists --input-file examples/docs/ifexists-file4.tsv \
              --filter-on examples/docs/ifexists-file3.tsv

```
| id |
| -- |
| john |

### Filter an Edge File on a Node File Using an Alternate Input Column

```bash
kgtk ifexists --input-file examples/docs/ifexists-file1.tsv \
              --filter-on examples/docs/ifexists-file5.tsv \
	      --input-keys location

```
| node1 | label | node2 | location | years |
| -- | -- | -- | -- | -- |
| john | zipcode | 12345 | home | 10 |
| peter | zipcode | 12040 | home |  |
