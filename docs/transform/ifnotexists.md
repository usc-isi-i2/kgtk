## Overview

The ifnotexists command filters a KGTK file (the input file specified by `--input-file`, which defaults to standard input),
passing through only those rows forwhich one or more specified columns do not
match records in a second KGTK file (the filter file, specified by `--filter-on`).

!!! note
    This command computes the inverse of the output of the [`kgtk ifexists`](../ifexists) command.
    It is provided as a seperate command for convenience and clarity in KGTK processing scripts.

### Memory Usage Options

This implementation of `ifnotexists` is written in Python.  By default, it builds
an in-memory dictionary of the key values it finds in the `--filter-on` file
before processing the `--input-file` in a single pass.  Performance will be poor, and execution may
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

### Key Fields

The names of the fields used match records may be supplied by the user using
the `--input-keys` and `--filter-keys` option.
Each option may take a variable number of space-separated field names.  If keys are not supplied,
the following defaults will be used, which depend on the KGTK file type
(edge or node) of the input and filter files.

| Input File Type | Filter File Type   | Key fields |
| ------- | ------- | ---------- |
| edge    | edge    | input.node1 == filter.node1 and |
|         |         | input.label == filter.label and |
|         |         | input.node2 == filter.node2 |
| node    | node    | input.id    == filter.id |
| edge    | node    | input.node1 == filter.id |
| node    | edge    | input.id   == filter.node1 |

!!! note
    The number of input file keys must match the number of output file keys, after
    taking into consideration the default keys.  So, if you want to match an edge file's
    node1 value to a nonstandard column in a node file, only the `--filter-keys`
    option needs to be specified.

### Optional Output Files

The `--reject-file`, when specified, will receive any input records
that failed the filter test and were not written to the output file.

The `--matched-filter-file`, when specified, will receive a copy of
any filter records that found a match in the input file.


The `--unmatched-filter-file`, when specified, will receive a copy of
any filter records that did not find a match in the input file.

### Experimental Join Facility

The `kgtk ifnotexists` command contains experimental support for performing
a join.  The join output file (which may be the primary output file)
will contain the union of the columns found in the `--input-file` and the `--filter-on` file, and may contain
records from both file.  At the present time, please refer to
`kgtk --expert ifnotexists --help` and the KGTK source code files for more
details on this facility.


## Usage

```
usage: kgtk ifnotexists [-h] [-i INPUT_FILE] [--filter-on FILTER_FILE]
                        [-o OUTPUT_FILE] [--reject-file REJECT_FILE]
                        [--matched-filter-file MATCHED_FILTER_FILE]
                        [--unmatched-filter-file UNMATCHED_FILTER_FILE]
                        [--input-keys [INPUT_KEYS [INPUT_KEYS ...]]]
                        [--filter-keys [FILTER_KEYS [FILTER_KEYS ...]]]
                        [--cache-input [True|False]]
                        [--preserve-order [True|False]]
                        [--presorted [True|False]] [-v [optional True|False]]

Filter a KGTK file based on whether one or more records do not exist in a second KGTK file with matching values for one or more fields.

Additional options are shown in expert help.
kgtk --expert ifnotexists --help

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
                        The KGTK reject file for records that fail the filter.
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

| id | node1 | label | node2 | location | years |
| -- | -- | -- | -- | -- | -- |
| p1 | peter | title | manager |  |  |
| p2 | peter | zipcode | 12040 | home |  |
| p3 | peter | zipcode | 12040 | work | 6 |
| s1 | steve | title | supervisor |  |  |
| s2 | steve | zipcode | 45601 |  | 3 |
| s3 | steve | zipcode | 45601 | work |  |
| j1 | john | title | programmer |  |  |
| j2 | john | zipcode | 12345 | home | 10 |
| j2 | john | zipcode | 12346 |  |  |
| k1 | kathy | title | owner |  |  |
| k2 | kathy | zipcode | 12040 | home |  |
| k3 | kathy | zipcode | 12040 | work | 6 |

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

Suppose that `ifexists-file6.tsv` contains the following table in KGTK format:

```bash
kgtk cat -i examples/docs/ifexists-file6.tsv --mode NONE
```

| label | node2 |
| -- | -- |
| zipcode | 12040 |
| zipcode | 45601 |
| zipcode | 45601 |
| zipcode | 52040 |
| zipcode | 62040 |
| zipcode | 72040 |

!!! note
    This is not a valid KGTK file, as it does not meet the mandatory column requirements
    for an edge file nor a node file.

Suppose that `ifexists-file7.tsv` contains the following table in KGTK format:

```bash
kgtk cat -i examples/docs/ifexists-file7.tsv
```

| id |
| -- |
| j1 |
| s1 |

!!! note
    This is a KGTK node file.

### Filter an Edge File on Another Edge File.

```bash
kgtk ifnotexists --input-file examples/docs/ifexists-file1.tsv \
              --filter-on examples/docs/ifexists-file2.tsv

```

| id | node1 | label | node2 | location | years |
| -- | -- | -- | -- | -- | -- |
| p1 | peter | title | manager |  |  |
| s1 | steve | title | supervisor |  |  |
| s2 | steve | zipcode | 45601 |  | 3 |
| s3 | steve | zipcode | 45601 | work |  |
| j1 | john | title | programmer |  |  |
| j2 | john | zipcode | 12345 | home | 10 |
| j2 | john | zipcode | 12346 |  |  |
| k1 | kathy | title | owner |  |  |
| k2 | kathy | zipcode | 12040 | home |  |
| k3 | kathy | zipcode | 12040 | work | 6 |

!!! note
    Since both the input file and the filter file are KGTK edge files, the
    default key field comparisons are:
    
    > input.node1 == filter.node1 and
    > input.label == filter.label and
    > input.node2 == filter.node2

    The `id` fields are not part of this comparison (and the
    `id` field isn't present in `examples/docs/ifexists-file2.tsv`).

### Filter an Edge File on a Node File

```bash
kgtk ifnotexists --input-file examples/docs/ifexists-file1.tsv \
                 --filter-on examples/docs/ifexists-file3.tsv

```
| id | node1 | label | node2 | location | years |
| -- | -- | -- | -- | -- | -- |
| p1 | peter | title | manager |  |  |
| p2 | peter | zipcode | 12040 | home |  |
| p3 | peter | zipcode | 12040 | work | 6 |
| k1 | kathy | title | owner |  |  |
| k2 | kathy | zipcode | 12040 | home |  |
| k3 | kathy | zipcode | 12040 | work | 6 |

!!! note
    Since the input file is a KGTK edge file and the filter file is
    a KGTK node file, the default key field comparison is:

    > input.node1 == filter.id

### Filter a Node File on a Node File

```bash
kgtk ifnotexists --input-file examples/docs/ifexists-file4.tsv \
                 --filter-on examples/docs/ifexists-file3.tsv

```
| id |
| -- |
| peter |

!!! note
    Since the input file and the filter files are both KGTK
    node files, the default key field comparison is:

    > input.id == filter.id

### Filter an Edge File on a Node File Using an Alternate Input Column

```bash
kgtk ifnotexists --input-file examples/docs/ifexists-file1.tsv \
                 --filter-on examples/docs/ifexists-file5.tsv \
                 --input-keys location

```
| id | node1 | label | node2 | location | years |
| -- | -- | -- | -- | -- | -- |
| p1 | peter | title | manager |  |  |
| p3 | peter | zipcode | 12040 | work | 6 |
| s1 | steve | title | supervisor |  |  |
| s2 | steve | zipcode | 45601 |  | 3 |
| s3 | steve | zipcode | 45601 | work |  |
| j1 | john | title | programmer |  |  |
| j2 | john | zipcode | 12346 |  |  |
| k1 | kathy | title | owner |  |  |
| k3 | kathy | zipcode | 12040 | work | 6 |

!!! note
    This used the key field comparison:

    > input.location == filter.id

### Filter an Edge File on a Nonstandard File

We want to filter a KGTK edge file agains a file that not
a valid KGTK file (it is almost a KGTK edge file, but it is
missing the `node1` column). We can use the expert option
`--filter-mode NONE` to disable the mandatory column check
on the filter file, then use `--input-keys` and `--filter-keys`
to specify the columns that we want to compare.

```bash
kgtk ifnotexists --input-file examples/docs/ifexists-file1.tsv \
                 --filter-on examples/docs/ifexists-file6.tsv \
                 --filter-mode NONE \
                 --input-keys label node2 \
                 --filter-keys label node2

```
| id | node1 | label | node2 | location | years |
| -- | -- | -- | -- | -- | -- |
| p1 | peter | title | manager |  |  |
| s1 | steve | title | supervisor |  |  |
| j1 | john | title | programmer |  |  |
| j2 | john | zipcode | 12345 | home | 10 |
| j2 | john | zipcode | 12346 |  |  |
| k1 | kathy | title | owner |  |  |

!!! note
    This used the key field comparison:

    > input.label == filter.label and input.node2 == filter.node2

### Filter an Edge File: Filter Matches

We want to filter a KGTK edge file agains a file that not
a valid KGTK file (it is almost a KGTK edge file, but it is
missing the `node1` column). We can use the expert option
`--filter-mode NONE` to disable the mandatory column check
on the filter file, then use `--input-keys` and `--filter-keys`
to specify the columns that we want to compare.

Furthermore, we want to see which filter records found
at least one matching input record, and which filter records
did not find a match.

```bash
kgtk ifnotexists --input-file examples/docs/ifexists-file1.tsv \
                 --filter-on examples/docs/ifexists-file6.tsv \
                 --filter-mode NONE \
                 --input-keys label node2 \
                 --filter-keys label node2 \
                 --matched-filter-file ifexists-matched-filter.tsv \
                 --unmatched-filter-file ifexists-unmatched-filter.tsv

```
| id | node1 | label | node2 | location | years |
| -- | -- | -- | -- | -- | -- |
| p1 | peter | title | manager |  |  |
| s1 | steve | title | supervisor |  |  |
| j1 | john | title | programmer |  |  |
| j2 | john | zipcode | 12345 | home | 10 |
| j2 | john | zipcode | 12346 |  |  |
| k1 | kathy | title | owner |  |  |

```bash
kgtk cat -i ifexists-matched-filter.tsv --mode NONE
```
| label | node2 |
| -- | -- |
| zipcode | 12040 |
| zipcode | 45601 |
| zipcode | 45601 |

```bash
kgtk cat -i ifexists-unmatched-filter.tsv --mode NONE
```
| label | node2 |
| -- | -- |
| zipcode | 52040 |
| zipcode | 62040 |
| zipcode | 72040 |

!!! note
    Since the filter file was missing a mandatory KGTK column (`node1`), the
    matched and unmatched filter output files are also missing that
    column.  Thus, the `kgtk cat` commands that disply them also need
    `--mode NONE`.


### Filter an Edge File By id

This is another example of filtering an input file using an
alternate input file key column.  `examples/docs/ifexists-file7.tsv`
contains a list of edge ids that we want to retain in the output file.

```bash
kgtk ifnotexists --input-file examples/docs/ifexists-file1.tsv \
                 --filter-on examples/docs/ifexists-file7.tsv \
                 --input-keys id

```
| id | node1 | label | node2 | location | years |
| -- | -- | -- | -- | -- | -- |
| p1 | peter | title | manager |  |  |
| p2 | peter | zipcode | 12040 | home |  |
| p3 | peter | zipcode | 12040 | work | 6 |
| s2 | steve | zipcode | 45601 |  | 3 |
| s3 | steve | zipcode | 45601 | work |  |
| j2 | john | zipcode | 12345 | home | 10 |
| j2 | john | zipcode | 12346 |  |  |
| k1 | kathy | title | owner |  |  |
| k2 | kathy | zipcode | 12040 | home |  |
| k3 | kathy | zipcode | 12040 | work | 6 |

! note
    This used the key field comparison:

    > input.id == filter.id

### Filter an Edge File By id: Reject File

This is another example of filtering an input file using an
alternate input file key column.  `examples/docs/ifexists-file7.tsv`
contains a list of edge ids that we want to retain in the output file.
However, we also want to obtain the records that were rejected to
check that the records that were rejected match our expectations, or
perhaps to apply different processing to them.

```bash
kgtk ifnotexists --input-file examples/docs/ifexists-file1.tsv \
                 --filter-on examples/docs/ifexists-file7.tsv \
                 --reject-file ifexists-rejects.tsv \
                 --input-keys id

```
| id | node1 | label | node2 | location | years |
| -- | -- | -- | -- | -- | -- |
| p1 | peter | title | manager |  |  |
| p2 | peter | zipcode | 12040 | home |  |
| p3 | peter | zipcode | 12040 | work | 6 |
| s2 | steve | zipcode | 45601 |  | 3 |
| s3 | steve | zipcode | 45601 | work |  |
| j2 | john | zipcode | 12345 | home | 10 |
| j2 | john | zipcode | 12346 |  |  |
| k1 | kathy | title | owner |  |  |
| k2 | kathy | zipcode | 12040 | home |  |
| k3 | kathy | zipcode | 12040 | work | 6 |

```bash
kgtk cat -i ifexists-rejects.tsv
```
| id | node1 | label | node2 | location | years |
| -- | -- | -- | -- | -- | -- |
| s1 | steve | title | supervisor |  |  |
| j1 | john | title | programmer |  |  |

!!! note
    If the intent of the filter was to separate all title records by edge
    ID, then the output and reject files show that id `p1` was omitted from the filter file.

### Filter a Small Input File on a Large Filter File

Although the example data files are very small, this example
command shows how to filter a small input file against a
large filter file:

```bash
kgtk ifnotexists --input-file examples/docs/ifexists-file1.tsv \
                 --filter-on examples/docs/ifexists-file3.tsv \
                 --cache-input

```
| id | node1 | label | node2 | location | years |
| -- | -- | -- | -- | -- | -- |
| k1 | kathy | title | owner |  |  |
| k2 | kathy | zipcode | 12040 | home |  |
| k3 | kathy | zipcode | 12040 | work | 6 |
| p1 | peter | title | manager |  |  |
| p2 | peter | zipcode | 12040 | home |  |
| p3 | peter | zipcode | 12040 | work | 6 |

!!! note
    Since the input file is a KGTK edge file and the filter file is
    a KGTK node file, the default key field comparison is:

    > input.node1 == filter.id

    Because we are cacheing the input file, the output edges have
    been reordered by the input key, then by order.


### Filter a Small Input File on a Large Filter File, Preserving Order

Although the example data files are very small, this example
command shows how to filter a small input file against a
large filter file, preserving the input file's order:

```bash
kgtk ifnotexists --input-file examples/docs/ifexists-file1.tsv \
                 --filter-on examples/docs/ifexists-file3.tsv \
                 --cache-input --preserve-order

```
| id | node1 | label | node2 | location | years |
| -- | -- | -- | -- | -- | -- |
| p1 | peter | title | manager |  |  |
| p2 | peter | zipcode | 12040 | home |  |
| p3 | peter | zipcode | 12040 | work | 6 |
| k1 | kathy | title | owner |  |  |
| k2 | kathy | zipcode | 12040 | home |  |
| k3 | kathy | zipcode | 12040 | work | 6 |

!!! note
    Since the input file is a KGTK edge file and the filter file is
    a KGTK node file, the default key field comparison is:

    > input.node1 == filter.id

    The output edges appear in the same order as the input edges.

### Filter a Large Input File on a Large Filter File

Although the example data files are very small, this example
command shows how to filter a large input file against a
large filter file by sorting the two files.

We will explicitly tell the `kgtk sort` command which
columns to sort on.

```bash
kgtk sort --input-file examples/docs/ifexists-file1.tsv \
          --output-file ifexists-file1-sorted-by-node1.tsv \
          --column node1
```

```bash
kgtk sort --input-file examples/docs/ifexists-file3.tsv \
          --output-file ifexists-file3-sorted-by-id.tsv \
          --column id
```

```bash
kgtk ifnotexists --input-file ifexists-file1-sorted-by-node1.tsv \
                 --filter-on ifexists-file3-sorted-by-id.tsv \
                 --presorted
```

| id | node1 | label | node2 | location | years |
| -- | -- | -- | -- | -- | -- |
| k1 | kathy | title | owner |  |  |
| k2 | kathy | zipcode | 12040 | home |  |
| k3 | kathy | zipcode | 12040 | work | 6 |
| p1 | peter | title | manager |  |  |
| p2 | peter | zipcode | 12040 | home |  |
| p3 | peter | zipcode | 12040 | work | 6 |

!!! note
    Since the input file is a KGTK edge file and the filter file is
    a KGTK node file, the default key field comparison is:

    > input.node1 == filter.id
