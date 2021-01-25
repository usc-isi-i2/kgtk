## Overview

Join two KGTK edge files or two KGTK node files.

### Summary

* Join keys are extracted from one or both input files and stored in memory, then the data files are processed in a second pass.  Performance will be poor, and execution may fail, if the files are very large.
* stdin will not work as an input file if join keys are needed from it.
* The output file contains the union of the columns in the two
input files, adjusted for predefined name aliasing.
* Specify --left-join to get a left outer join.
* Specify --right-join to get a right outer join.
* Specify both to get a full outer join (equivalent to cat).
* Specify neither to get an inner join.
* By default, node files are joined on the id column, while edge files are joined on the node1 column. The label and node2 columns may be added to the edge file join  criteria.  Alternatively, the left and right file join columns may be
  listed explicitly.

### Joining Normalized Edges

A normalized KGTK edge file contains the following columns:

 * `node1` (or an alias)
 * `label` (or an alias)
 * `node2` (or an alias)
 *  optionally `id` (or an alias)

The `label` column typically expresses a relationship between the values
(symbols, strings, numbers, etc.) in the `node1` and `node2` columns.

`kgtk join` takes two edge files and produces a new edge file that contains
a selection of the edges from the two input files.  If the two input files
contain normalized edges then the output file will contain normalized edges.

### `id` Column

 * If either input file contains an `id` column, then the output file will
contain an `id` column.

 * If an `id` column is missing from an input file, the corresponding edges
in the output file will have empty `id` values.

 * Existing `id` column values will not be checked for duplication.

!!! note
    See [`kgtk add-id`](https:../add_id) if you wish to generate new `id` column values or
    manipulate existing `id` column values.
    [`kgtk calc`](https://../calc) may also be useful for modifying `id` column values.

### Duplicate Edges

If either edge file contains duplicate edges, or the two edge files contain
copies of the same edge, and these edges are selected for inclusion in the output file,
then the output file will contain duplicate edges.

The command [`kgtk compact`](https:../compact) can be used to remove duplicate
edges from the output file.

### Joining Denormalized Edges

A denormalized KGTK edge file contains additional columns beyond (`node1`, `label`, `node2`, and `id`).

When one or both of the input edge file are denormalized, the output file will also be denormalized.
The output file will contain the union of the additional columns from the input files, with empty values
when an input file does not contain a nonempty value.

### Joining on `node1`, `label`, and `node2`


### Compacting Joined Edges

The left and right edges will remain distinct in the output file,
even if the (`node1`, `label`, `node2, and `id`) fields match.
If you want to create a single edge with additional columns from
both input files, process the output of `kgtk join` with [`kgtk compact`](https:../compact),
or use [`kgtk lift`](https:../lift) to merge the data records.

### Bending the Rules

To join an edge file to a node file, or to join quasi-KGTK files, use the
following option (enable expert mode for usage information):

```
--mode=NONE
```

## Usage

```
usage: kgtk join [-h] [--left-file LEFT_FILE] [--right-file RIGHT_FILE]
                 [-o OUTPUT_FILE] [--join-on-label [JOIN_ON_LABEL]]
                 [--join-on-node2 [JOIN_ON_NODE2]] [--left-prefix LEFT_PREFIX]
                 [--left-file-join-columns LEFT_JOIN_COLUMNS [LEFT_JOIN_COLUMNS ...]]
                 [--left-join [LEFT_JOIN]] [--right-prefix RIGHT_PREFIX]
                 [--right-file-join-columns RIGHT_JOIN_COLUMNS [RIGHT_JOIN_COLUMNS ...]]
                 [--right-join [RIGHT_JOIN]] [-v [optional True|False]]

Join two KGTK edge files or two KGTK node files.

Join keys are extracted from one or both input files and stored in memory,
then the data files are processed in a second pass.  stdin will not work as an
input file if join keys are needed from it.

The output file contains the union of the columns in the two
input files, adjusted for predefined name aliasing.

Specify --left-join to get a left outer join.
        The output file will contain all records from the
        left input file, along with records from the right
        input file with matching join column values.

Specify --right-join to get a right outer join.
        The output file will contain all records from the
        right input file, along with records from the left
        input file with matching join column values.

Specify both --left-join and --right-join to get a full outer
join (equivalent to cat or set union).
        The output file will contain all records from both
        the left input file and the right input file.

Specify neither --left-join nor --right-join to get an inner
join.  If there are no columns beyond the join columns, then
this is equivalent to set intersection.
        The output file will contain records from the left
        input file and from the right input file for which
        the join column value match.

By default, node files are joined on the id column, while edge files are joined
on the node1 column. The label and node2 columns may be added to the edge file
join criteria.  Alternatively, the left and right file join columns may be
listed explicitly.

To join an edge file to a node file, or to join quasi-KGTK files, use the
following option (enable expert mode for more information):

--mode=NONE

Expert mode provides additional command arguments.

optional arguments:
  -h, --help            show this help message and exit
  --left-file LEFT_FILE
                        The left-side KGTK file to join (required). (May be
                        omitted or '-' for stdin.)
  --right-file RIGHT_FILE
                        The right-side KGTK file to join (required). (May be
                        omitted or '-' for stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for
                        stdout.)
  --join-on-label [JOIN_ON_LABEL]
                        If both input files are edge files, include the label
                        column in the join (default=False).
  --join-on-node2 [JOIN_ON_NODE2]
                        If both input files are edge files, include the node2
                        column in the join (default=False).
  --left-prefix LEFT_PREFIX
                        An optional prefix applied to left file column names
                        in the output file (default=None).
  --left-file-join-columns LEFT_JOIN_COLUMNS [LEFT_JOIN_COLUMNS ...]
                        Left file join columns (default=None).
  --left-join [LEFT_JOIN]
                        Perform a left outer join (default=False).
  --right-prefix RIGHT_PREFIX, --prefix RIGHT_PREFIX
                        An optional prefix applied to right file column names
                        in the output file (default=None).
  --right-file-join-columns RIGHT_JOIN_COLUMNS [RIGHT_JOIN_COLUMNS ...]
                        Right file join columns (default=None).
  --right-join [RIGHT_JOIN]
                        Perform a right outer join (default=False).

  -v [optional True|False], --verbose [optional True|False]
                        Print additional progress messages (default=False).
```
## Examples

### Normalized Sample Data

Suppose that `file1.tsv` contains the following table in KGTK format:

```bash
kgtk cat -i examples/docs/join-file1.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| john | zipcode | 12345 |
| peter | zipcode | 12040 |
| steve | zipcode | 45601 |

and `file2.tsv` contains the following table in KGTK format:

```bash
kgtk cat -i examples/docs/join-file2.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| john | position | programmer |
| peter | position | engineer |
| edward | position | supervisor |

### Do an inner join on two KGTK normalized edge files on `node1`.

The output will contain edges from the left and right files
got only those `node1` values that appear in both files.


```bash
kgtk join --left-file examples/docs/join-file1.tsv \
          --right-file examples/docs/join-file2.tsv
```

The result will be the following table in KGTK format:

| node1 | label | node2 |
| -- | -- | -- |
| john | zipcode | 12345 |
| peter | zipcode | 12040 |
| john | position | programmer |
| peter | position | engineer |


### Do a left outer join on two KGTK normalized edge files on `node1`.

The output will contain all edges from the left file,
and any edges from the right file with a `node1` value that
matches at least one edge in the left file.

```bash
kgtk join --left-join \
          --left-file examples/docs/join-file1.tsv \
	  --right-file examples/docs/join-file2.tsv
```

The result will be the following table in KGTK format:

| node1 | label | node2 |
| -- | -- | -- |
| john | zipcode | 12345 |
| peter | zipcode | 12040 |
| steve | zipcode | 45601 |
| john | position | programmer |
| peter | position | engineer |


### Do a right outer join on two KGTK normalized edge files on `node1`.

The output will contain all edges from the right file,
and any edges from the left file with a `node1` value that
matches at least one edge in the right file.

```bash
kgtk join --right-join \
          --left-file examples/docs/join-file1.tsv \
	  --right-file examples/docs/join-file2.tsv
```

The result will be the following table in KGTK format:

| node1 | label | node2 |
| -- | -- | -- |
| john | zipcode | 12345 |
| peter | zipcode | 12040 |
| john | position | programmer |
| peter | position | engineer |
| edward | position | supervisor |

### Do a full outer join on two KGTK normalized edge files on `node1`.

This produces the same output as the `kgtk cat` command,
and is included here for completeness.

```bash
kgtk join --left-join --right-join \
          --left-file examples/docs/join-file1.tsv \
	  --right-file examples/docs/join-file2.tsv
```

The result will be the following table in KGTK format:

| node1 | label | node2 |
| -- | -- | -- |
| john | zipcode | 12345 |
| peter | zipcode | 12040 |
| steve | zipcode | 45601 |
| john | position | programmer |
| peter | position | engineer |
| edward | position | supervisor |

### Deormalized Sample Data

Suppose that `file3.tsv` contains the following table in KGTK format:

```bash
kgtk cat -i examples/docs/join-file3.tsv
```

| node1 | label | node2 | location |
| -- | -- | -- | -- |
| john | zipcode | 12345 | home |
| john | zipcode | 12346 | work |
| peter | zipcode | 12040 | home |
| peter | zipcode | 12040 | work |
| steve | zipcode | 45601 | home |
| steve | zipcode | 45601 | work |

and `file4.tsv` contains the following table in KGTK format:

```bash
kgtk cat -i examples/docs/join-file4.tsv
```

| node1 | label | node2 | years |
| -- | -- | -- | -- |
| john | position | programmer | 3 |
| peter | position | engineer | 2 |
| edward | position | supervisor | 10 |
| john | laptop | dell | 4 |
| peter | laptop | apple | 7 |

### Do an inner join on two KGTK denormalized edge files on `node1`.

The output will contain edges from the left and right files
got only those `node1` values that appear in both files.


```bash
kgtk join --left-file examples/docs/join-file3.tsv \
          --right-file examples/docs/join-file4.tsv
```

The result will be the following table in KGTK format:

| node1 | label | node2 | location | years |
| -- | -- | -- | -- | -- |
| john | zipcode | 12345 | home |  |
| john | zipcode | 12346 | work |  |
| peter | zipcode | 12040 | home |  |
| peter | zipcode | 12040 | work |  |
| john | position | programmer |  | 3 |
| peter | position | engineer |  | 2 |
| john | laptop | dell |  | 4 |
| peter | laptop | apple |  | 7 |


### Do a left outer join on two KGTK denormalized edge files on `node1`.

The output will contain all edges from the left file,
and any edges from the right file with a `node1` value that
matches at least one edge in the left file.

```bash
kgtk join --left-join \
          --left-file examples/docs/join-file3.tsv \
	  --right-file examples/docs/join-file4.tsv
```

The result will be the following table in KGTK format:

| node1 | label | node2 | location | years |
| -- | -- | -- | -- | -- |
| john | zipcode | 12345 | home |  |
| john | zipcode | 12346 | work |  |
| peter | zipcode | 12040 | home |  |
| peter | zipcode | 12040 | work |  |
| steve | zipcode | 45601 | home |  |
| steve | zipcode | 45601 | work |  |
| john | position | programmer |  | 3 |
| peter | position | engineer |  | 2 |
| john | laptop | dell |  | 4 |
| peter | laptop | apple |  | 7 |


### Do a right outer join on two KGTK denormalized edge files on `node1`.

The output will contain all edges from the right file,
and any edges from the left file with a `node1` value that
matches at least one edge in the right file.

```bash
kgtk join --right-join \
          --left-file examples/docs/join-file3.tsv \
	  --right-file examples/docs/join-file4.tsv
```

The result will be the following table in KGTK format:

| node1 | label | node2 | location | years |
| -- | -- | -- | -- | -- |
| john | zipcode | 12345 | home |  |
| john | zipcode | 12346 | work |  |
| peter | zipcode | 12040 | home |  |
| peter | zipcode | 12040 | work |  |
| john | position | programmer |  | 3 |
| peter | position | engineer |  | 2 |
| edward | position | supervisor |  | 10 |
| john | laptop | dell |  | 4 |
| peter | laptop | apple |  | 7 |

### Do a full outer join on two KGTK denormalized edge files on `node1`.

This produces the same output as the `kgtk cat` command,
and is included here for completeness.

```bash
kgtk join --left-join --right-join \
          --left-file examples/docs/join-file3.tsv \
	  --right-file examples/docs/join-file4.tsv
```

The result will be the following table in KGTK format:

| node1 | label | node2 | location | years |
| -- | -- | -- | -- | -- |
| john | zipcode | 12345 | home |  |
| john | zipcode | 12346 | work |  |
| peter | zipcode | 12040 | home |  |
| peter | zipcode | 12040 | work |  |
| steve | zipcode | 45601 | home |  |
| steve | zipcode | 45601 | work |  |
| john | position | programmer |  | 3 |
| peter | position | engineer |  | 2 |
| edward | position | supervisor |  | 10 |
| john | laptop | dell |  | 4 |
| peter | laptop | apple |  | 7 |

