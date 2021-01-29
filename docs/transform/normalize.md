## Overview

`kgtk normalize` removes additional columns from a KGTK edge file.
It implements two column removal patterns:

  * It reverses `kgtk lift`, then
  * it converts the remaining additional columns to secondary edges.

### `kgtk lower`

This alias for `kgtk normalize` removes additional columns from a KGTK edge file,
reversing `kgtk lift`.  It does not convert other additional columns to secondary edges.

### `kgtk normalize-edges`

This alias for `kgtk normalize` converts all (or selected) additional columns
in a KGTK edge file to secondary edges.

### [`kgtk normalize-nodes`](https:../normalize_nodes)

[`kgtk normalize-nodes`](https:../normalize_nodes) converts KGTK node files to normalized
KGTK edge files.

!!! note
    [`kgtk normalize-nodes`](https:../normalize_nodes) is currently implemented as a seperate
    command.  In the future, `kgtk normalize` may provide the same functionality when the
    input file is a KGTK node file.

## Usage

```
usage: kgtk normalize [-h] [-i INPUT_FILE] [-o OUTPUT_FILE]
                      [--new-edges-file NEW_EDGES_FILE]
                      [--columns COLUMNS_TO_LOWER [COLUMNS_TO_LOWER ...]]
                      [--lower [True|False]] [--normalize [True|False]]
                      [--deduplicate-new-edges [True|False]]
                      [-v [optional True|False]]

Normalize a KGTK edge file by removing columns that match a "lift" pattern and converting remaining additional columns to new edges.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK input file. (May be omitted or '-' for
                        stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for
                        stdout.)
  --new-edges-file NEW_EDGES_FILE
                        An optional output file for new edges (normalized
                        and/or lowered). If omitted, new edges will go in the
                        main output file. (Optional, use '-' for stdout.)
  --columns COLUMNS_TO_LOWER [COLUMNS_TO_LOWER ...], --columns-to-lower COLUMNS_TO_LOWER [COLUMNS_TO_LOWER ...], --columns-to-remove COLUMNS_TO_LOWER [COLUMNS_TO_LOWER ...]
                        Columns to lower and remove as a space-separated list.
                        (default=all columns other than key columns)
  --lower [True|False]  When True, lower columns that match a lift pattern.
                        (default=True)
  --normalize [True|False]
                        When True, normalize columns that do not match a lift
                        pattern. (default=True)
  --deduplicate-new-edges [True|False]
                        When True, deduplicate new edges. Not suitable for
                        large files. (default=True).

  -v [optional True|False], --verbose [optional True|False]
                        Print additional progress messages (default=False).
```

## Examples


kgtk lift --input-file examples/docs/lift-file4.tsv -o examples/docs/normalize-file1.tsv

 kgtk normalize -i examples/docs/normalize-file1.tsv
--normalize was requested but the ID column was not found.
944% kgtk normalize -i examples/docs/normalize-file1.tsv --normalize False
node1   label   node2
Q1      P1      Q5
Q1      label   "Elmo"
P1      label   "instance of"
Q5      label   "homo sapiens"
Q5      label   "human"
Q1      P2      Q6
P2      label   "amigo"
P2      label   "friend"
Q6      label   "Fred"
Q6      P1      Q5
945% kgtk normalize -i examples/docs/normalize-file1.tsv --normalize False --new-edges new.tsv
node1   label   node2
Q1      P1      Q5
Q1      P2      Q6
Q6      P1      Q5
946% cat new.tsv
node1   label   node2
Q1      label   "Elmo"
P1      label   "instance of"
Q5      label   "homo sapiens"
Q5      label   "human"
P2      label   "amigo"
P2      label   "friend"
Q6      label   "Fred"
