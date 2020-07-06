
Join two KGTK edge files or two KGTK node files.

## Usage
```
usage: kgtk join [-h] [--left-file LEFT_FILE] [--right-file RIGHT_FILE] [-o OUTPUT_FILE]
                 [--join-on-label [JOIN_ON_LABEL]] [--join-on-node2 [JOIN_ON_NODE2]]
                 [--left-file-join-columns LEFT_JOIN_COLUMNS [LEFT_JOIN_COLUMNS ...]]
                 [--left-join [LEFT_JOIN]] [--prefix PREFIX]
                 [--right-file-join-columns RIGHT_JOIN_COLUMNS [RIGHT_JOIN_COLUMNS ...]]
                 [--right-join [RIGHT_JOIN]] [-v]
                 [LEFT_FILE] [RIGHT_FILE]

Join two KGTK edge files or two KGTK node files.

Join keys are extracted from one or both input files and stored in memory,
then the data files are processed in a second pass.  stdin will not work as an
input file if join keys are needed from it.

The output file contains the union of the columns in the two
input files, adjusted for predefined name aliasing.

Specify --left-join to get a left outer join.
Specify --right-join to get a right outer join.
Specify both to get a full outer join (equivalent to cat).
Specify neither to get an inner join.

By default, node files are joined on the id column, while edge files are joined
on the node1 column. The label and node2 columns may be added to the edge file
join criteria.  Alternatively, the left and right file join columns may be
listed explicitly.

To join an edge file to a node file, or to join quasi-KGTK files, use the
following option (enable expert mode for more information):

--mode=NONE

Expert mode provides additional command arguments.

positional arguments:
  LEFT_FILE             The left-side KGTK file to join (required). (May be omitted or '-'
                        for stdin.) (Deprecated, use --left-file LEFT_FILE)
  RIGHT_FILE            The right-side KGTK file to join (required). (May be omitted or '-'
                        for stdin.) (Deprecated, use --right-file RIGHT_FILE)

optional arguments:
  -h, --help            show this help message and exit
  --left-file LEFT_FILE
                        The left-side KGTK file to join (required). (May be omitted or '-'
                        for stdin.)
  --right-file RIGHT_FILE
                        The right-side KGTK file to join (required). (May be omitted or '-'
                        for stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for stdout.)
  --join-on-label [JOIN_ON_LABEL]
                        If both input files are edge files, include the label column in the
                        join (default=False).
  --join-on-node2 [JOIN_ON_NODE2]
                        If both input files are edge files, include the node2 column in the
                        join (default=False).
  --left-file-join-columns LEFT_JOIN_COLUMNS [LEFT_JOIN_COLUMNS ...]
                        Left file join columns (default=None).
  --left-join [LEFT_JOIN]
                        Perform a left outer join (default=False).
  --prefix PREFIX       An optional prefix applied to right file column names in the output
                        file (default=None).
  --right-file-join-columns RIGHT_JOIN_COLUMNS [RIGHT_JOIN_COLUMNS ...]
                        Right file join columns (default=None).
  --right-join [RIGHT_JOIN]
                        Perform a right outer join (default=False).

  -v, --verbose         Print additional progress messages (default=False).
```
## Usage considerations

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

To join an edge file to a node file, or to join quasi-KGTK files, use the
following option (enable expert mode for more information):

```
--mode=NONE
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

and `file2.tsv` contains the following table in KGTK format:

| node1  | label    | node2      | years |
| ------ | -------- | ---------- | ----- |
| john   | position | programmer | 3     |
| peter  | position | engineer   | 2     |
| edward | position | supervisor | 10    |
| john   | laptop   | dell       | 4     |
| peter  | laptop   | apple      | 7     |

Do an inner join on two KGTK files on node1, sending the output to standard output.

```bash
kgtk join file1.tsv file2.tsv
```

The result will be the following table in KGTK format:

| node1 | label    | node2      | location | years |
| ----- | -------- | ---------- | -------- | ----- |
| john  | zipcode  | 12345      | home     |       |
| john  | zipcode  | 12346      | work     |       |
| peter | zipcode  | 12040      | home     |       |
| peter | zipcode  | 12040      | work     |       |
| john  | position | programmer |          | 3     |
| peter | position | engineer   |          | 2     |
| john  | laptop   | dell       |          | 4     |
| peter | laptop   | apple      |          | 7     |


Do a left outer join on two KGTK files on node1, sending the output to standard output.

```bash
kgtk join file1.tsv file2.tsv --left-join
```

The result will be the following table in KGTK format:

| node1 | label    | node2      | location | years |
| ----- | -------- | ---------- | -------- | ----- |
| john  | zipcode  | 12345      | home     |       |
| john  | zipcode  | 12346      | work     |       |
| peter | zipcode  | 12040      | home     |       |
| peter | zipcode  | 12040      | work     |       |
| steve | zipcode  | 45601      | home     |       |
| steve | zipcode  | 45601      | work     |       |
| john  | position | programmer |          | 3     |
| peter | position | engineer   |          | 2     |
| john  | laptop   | dell       |          | 4     |
| peter | laptop   | apple      |          | 7     |


Do a right outer join on two KGTK files on node1, sending the output to standard output.

```bash
kgtk join file1.tsv file2.tsv --right-join
```

The result will be the following table in KGTK format:

| node1  | label    | node2      | location | years |
| ------ | -------- | ---------- | -------- | ----- |
| john   | zipcode  | 12345      | home     |       |
| john   | zipcode  | 12346      | work     |       |
| peter  | zipcode  | 12040      | home     |       |
| peter  | zipcode  | 12040      | work     |       |
| john   | position | programmer |          | 3     |
| peter  | position | engineer   |          | 2     |
| edward | position | supervisor |          | 10    |
| john   | laptop   | dell       |          | 4     |
| peter  | laptop   | apple      |          | 7     |

Do a full outer join on two KGTK files on node1, sending the output to standard output.
This produces the same output as the `kgtk cat` command.

```bash
kgtk join file1.tsv file2.tsv --left-join --right-join
```

The result will be the following table in KGTK format:

| node1  | label    | node2      | location | years |
| ------ | -------- | ---------- | -------- | ----- |
| john   | zipcode  | 12345      | home     |       |
| john   | zipcode  | 12346      | work     |       |
| peter  | zipcode  | 12040      | home     |       |
| peter  | zipcode  | 12040      | work     |       |
| steve  | zipcode  | 45601      | home     |       |
| steve  | zipcode  | 45601      | work     |       |
| john   | position | programmer |          | 3     |
| peter  | position | engineer   |          | 2     |
| edward | position | supervisor |          | 10    |
| john   | laptop   | dell       |          | 4     |
| peter  | laptop   | apple      |          | 7     |

