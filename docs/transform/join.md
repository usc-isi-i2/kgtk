## Overview

Join two KGTK edge files or two KGTK node files.

### Summary

* The output file contains the union of the columns in the two
input files, adjusted for predefined name aliasing.
* Specify `--left-join` to get a left outer join.
* Specify `--right-join` to get a right outer join.
* Specify both to get a full outer join (equivalent to [`kgtk cat`](../cat)).
* Specify neither to get an inner join.
* By default, node files are joined on the id column, while edge files are joined on the node1 column. The label and node2 columns may be added to the edge file join  criteria.  Alternatively, the left and right file join columns may be
  listed explicitly.
* Join keys are extracted from one or both input files and stored in memory, then the data files are processed in a second pass.  Performance will be poor, and execution may fail, if the files are very large.
* stdin will not work as an input file if join keys are needed from it.

### Uses for Join

 * to assemble edges from different files, building an
   enriched set of relationships for selected subjects (`node1` values).

 * to assemble additional columns from different files,
   building an enriched set of additional columns for selected edges or nodes.

 * to select a smaller set of edges (or nodes) from a larger set, to
   improve the performance of future processing steps by eliminating
   unwanted edges (or nodes).

 * to perform a logical (set) operation on two sets of edges or nodes.

     * intersection (inner join, defined below)
     * union (outer join, defined below; also, [`kgtk cat`](../cat))

### Left and Right Input Files

`kgtk join` takes two KGTK edge or node files (called `left` and `right`, in a nod to relational
database terminology) and produces a new KGTK edge or node file that contains
a selection of the edges or nodes from the two input files.

The following combinations are accepted:

 * both input files are KGTK edge files, or
 * both input files are KGTK node files, or,
 * at least one input file is a quasi-KGTK file (indicated by the expert options `--mode=NONE`,
   `--left-mode=NONE`, and `--right-mode=NONE`).

### Join Types

Following the terminology used for relational databases:

| Join Type | Indicated by | Description |
| ----      | --- | ----- |
| inner join | | The output file contains only left and right edges or nodes that satisfy the matching criteria discussed below.  This is equivalend to a logical intersection. |
| left join | `--left-join` | The output file contains all of the left edges or nodes, and only the right edges or nodes that satisfy the matching criteria. |
| right join | `--right-join` | The output file contains all of the right edges or nodes, and only the left edges or nodes that satisfy the matching criteria. |
| outer join | `--left-join --right-join` | The output file contains all edges or nodes from both input files.  This is equivalend to a logical union, or [`kgtk cat`](../cat) |

### Duplicate Edges or Nodes

If either input file contains duplicate edges or nodes, or the two input files contain
copies of the edge or node, and these edges or nodes are selected for inclusion in the output file,
then the output file will contain duplicate edges or nodes.

The command [`kgtk compact`](../compact) can be used to remove duplicate
edges or nodes from the output file.

### Joining Normalized Edges

A normalized KGTK edge file contains only the following columns:

 * `node1` (or its alias)
 * `label` (or its alias)
 * `node2` (or its alias)
 *  optionally `id` (or its alias)

The `label` column typically expresses a relationship between the values
(symbols, strings, numbers, etc.) in the `node1` and `node2` columns.

If the two input files to `kgtk join` contain only normalized edges then the output file will contain only normalized edges.

### The Optional `id` Column

The `id` columns is optional in KGTK edge files.  It is required in KGTK node files.

 * If either input file contains an `id` column, then the output file will
contain an `id` column.

 * If an `id` column is missing from an input file, the corresponding edges
in the output file will have empty `id` values.

 * Existing `id` column values will not be checked for duplication.

!!! note
    See [`kgtk add-id`](../add_id) if you wish to generate new `id` column values or
    manipulate existing `id` column values.
    [`kgtk calc`](../calc) may also be useful for modifying `id` column values.

### Joining Edge Files on `node1` Alone

By default, `kgtk join` matches the `node1` column (or its alias) in the `left` input edge
file to the `node1` column (or its alias) in the `right` input edge file.  The goal is to
gather relationships, expressed by the `label` and `node2` columns, pertaining to
specific `node1` objects.

Left input files:

| node1 | label | node2 |
| ----- | ----- | ----- |
| block1 | isa | block|
| block1 | color | red |

Right input file:

| node1 | label | node2 |
| ----- | ----- | ----- |
| block1 | isa | block|
| block1 | size | large |

Output file after joining on `node1`:

| node1 | label | node2 |
| -- | -- | -- |
| block1 | isa | block|
| block1 | color | red |
| block1 | isa | block|
| block1 | size | large |

The left and right edges will remain distinct in the output file,
leading to duplicate edges (`block1 isa block`).

[`kgtk compact`](../compact) may be used to remove duplicate
edges after the join.  The output would be:

| node1 | label | node2 |
| -- | -- | -- |
| block1 | color | red |
| block1 | isa | block|
| block1 | size | large |

After `kgtk join`, [`kgtk lift`](https../lift) may be used to
build additional columns with the assembled information, such
as `node1;color` and `node1;size`.  The result might an edge
file with denormalzed edges (see below).

After `kgtk lift`:

| node1 | label | node2 | node1;color | node1;size |
| ----- | ----- | ----- | ----- | ---- |
| block1 | isa | block | red | large


### Joining with Additional Columns (Denormalized Edges)

A denormalized KGTK edge file contains additional columns beyond (`node1`, `label`, `node2`, and `id`).

When one or both of the input edge file are denormalized, the output file will also be denormalized.
The output file will contain the union of the additional columns from the input files, with empty values
in the additional columns when an input file does not contain a corresponding nonempty value.

Left input file:

| node1 | label | node2 | color |
| ----- | ----- | ----- | ----- |
| block1 | isa | block|
| block1 | type | cube | red |

Right input file:

| node1 | label | node2 | size |
| ----- | ----- | ----- | ----- |
| block1 | isa | block|
| block1 | type | cube | large |

Output file after joining on `node1`:

| node1 | label | node2 | color | size |
| ----- | ----- | ----- | ----- | --- |
| block1 | isa | block| | |
| block1 | type | cube | red |       |
| block1 | isa | block| | |
| block1 | type | cube |     | large |

[`kgtk compact`](../compact) may be used to remove duplicate edges
edges and compact the additional columns after the join:

| node1 | label | node2 | color | size |
| ----- | ----- | ----- | ----- | --- |
| block1 | isa | block| | |
| block1 | type | cube | red | large |

### Prefixing Additional Columns

`--left-prefix LEFT_PREFIX` and `--right-prefix RIGHT_PREFIX` provide optional
prefixes for the additional columns in the output field.
Without prefixing, additional columns with the same name in the left and right input
files become a single column in the output file:

Left input file:

| node1 | label | node2 | color |
| ----- | ----- | ----- | ----- |
| block1 | isa | block | |
| block1 | type | cube | red |

Right input file:

| node1 | label | node2 | color |
| ----- | ----- | ----- | ----- |
| block1 | isa | block | |
| block1 | type | cube | green |

Output file after joining without prefixing:

| node1 | label | node2 | color |
| ----- | ----- | ----- | ----- |
| block1 | isa | block | |
| block1 | type | cube | red |
| block1 | isa | block | |
| block1 | type | cube | green |

Output file after joining on `node1` with `--left-prefix=l- --right-prefix=r-`:

| node1 | label | node2 | l-color | r-color |
| ----- | ----- | ----- | ----- | --- |
| block1 | isa | block | | |
| block1 | type | cube | red |       |
| block1 | isa | block | | |
| block1 | type | cube |     | green |

### Joining Edges on `node1`, `label`, `node2`, and optionally `id`

Another use for `kgtk join` is to assemble a set of additional columns for
edges with entries in two different files.  Joining on edge identity can be
requested by specifying `--join-on-label --join-on-node2`.  If the `id`
column is significant for edge identity, `--join-on-id` can also be specified.

Left input file:

| node1 | label | node2 | color |
| ----- | ----- | ----- | ----- |
| block1 | material | wood | |
| block1 | type | cube | red |
| block2 | material | steel | |
| block2 | type | cube | blue |

Right input file:

| node1 | label | node2 | size |
| ----- | ----- | ----- | ----- |
| block1 | type | cube | large |
| block3 | type | cube | small |

Output file after an inner join on (`node1`, `label`, `node2`):

| node1 | label | node2 | color | size |
| ----- | ----- | ----- | ----- | --- |
| block1 | type | cube | red |       |
| block1 | type | cube |     | large |

[`kgtk compact`](../compact) can then be used to
compact the additional columns after the join:

| node1 | label | node2 | color | size |
| ----- | ----- | ----- | ----- | --- |
| block1 | type | cube | red | large |

### Joining Node Files: Set Intersection

Node files may be joined to perform a set intersection using the default
join type (omit `--left-join` and `--right-join`).

Left input file:

| id |
| --- |
| block1 |
| block2 |

Right input file:

| id |
| --- |
| block1 |
| block3 |

Output file after the inner join:

| id |
| --- |
| block1 |

### Joining Node Files: Set Union

Node files may be joined to perform a set union.  Use `--left-join --right-join` to
perform an outer join.

Left input file:

| id |
| --- |
| block1 |
| block2 |

Right input file:

| id |
| --- |
| block1 |
| block3 |

Output file after the outer join:

| id |
| --- |
| block1 |
| block2 |
| block1 |
| block3 |

After using [`kgtk compact`](../compact) to remove duplicates:

| id |
| --- |
| block1 |
| block2 |
| block3 |

### Joining Node Files: Merging Additional Columns

Node files may be joined to merge the additional columns found in the two input files.

Left input file:

| id | shape |
| --- | --- |
| block1 | cube |

Right input file:

| id | color |
| --- | --- |
| block1 | red |

Output file:

| id | shape | color |
| --- | --- | --- |
| block1 | cube | |
| block1 | | red |

After using [`kgtk compact`](../compact) to compact the entries:

| id | shape | color |
| --- | --- | --- |
| block1 | cube | red |

### Joining on Arbitrary Columns

`--left-file-join-columns LEFT_JOIN_COLUMNS ...` and `--right-file-join-columns RIGHT_JOIN_COLUMNS ...`
may be used to join on arbitrary sets of left and right file columns.  It is necessary to use these
options when processing quasi-KGTK files (`--mode=NONE`, `--left-mode=NONE`, `--right-mode=NONE`).

### Memory Usage and stdin Limitation

`kgtk join` builds in-memory key sets from one or both input files.  This may cause performance
problems if the join requires more memory than is available.

| Join Type | Input File Key Sets |
| --- | --- |
| Inner join | Key sets are built in memory  for both the left and right input files. |
| Left join | A key set is built in memory for the left input file. |
| Right join | A key set is built in memory for the right input file. |
| Outer join | No key sets are built in memory. |

!!! note 
    `kgtk join` builds in-memory key sets from one or both input files. Standard input (stdin)
    from a pipe may not be used for an input file for which a key set is built in memory.

!!! note
    [`kgtk ifexists`](../ifexists) provides an experimental join mode that works with
    presorted input files and uses much less memory.  In the future, `kgtk join` may offer support for
    presorted input files.


### Bending the Rules

To join an edge file to a node file, or to join quasi-KGTK files, use the
following options (enable expert mode for usage information):

| Option | Description |
| --- | --- |
| `--left-mode=NONE` | Treat the left input file as a quasi-KGTK file.  `--left-file-join-columns` must be supplied. |
| `--mode=NONE` | Treat both input files as quasi-KGTK files.  Both `--left-file-join-columns` and `--right-file-join-columns` must be supplied. |
| `--right-mode=NONE` | Treat the right input file as a quasi-KGTK file.  `--right-file-join-columns` must be supplied. |

### `kgtk join / compact`

The pipeline `kgtk join / compact` is a frequent idiom to remove duplicates and
compact additional columns in the output from a join operation.

!!! info
    In the future, `kgtk join --compact` will run `kgtk compact` automatically
    on the output of `kgtk join`.  This will reduce the
    number of command options that may need to be specified.  It may increase
    performance as well. [Issue #116](https://github.com/usc-isi-i2/kgtk/issues/116).


## Usage

```
usage: kgtk join [-h] [--left-file LEFT_FILE] [--right-file RIGHT_FILE]
                 [-o OUTPUT_FILE] [--join-on-id [JOIN_ON_ID]]
                 [--join-on-label [JOIN_ON_LABEL]]
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
  --join-on-id [JOIN_ON_ID]
                        If both input files are edge files, include the id
                        column in the join (default=False).
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

### Denormalized Sample Data

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

