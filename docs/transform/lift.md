The lift command copies its input file to its output file,
adding label columns for values in the node1, label, and node2 fields.

The input rows are saved in memory, as well as the value-to-label mapping.
This will impose a limit on the size of the input files that can be processed.   

## Usage

```
usage: kgtk lift [-h] [--label-file LABEL_KGTK_FILE] [-o OUTPUT_KGTK_FILE]
                 [--suppress-empty-columns [SUPPRESS_EMPTY_COLUMNS]]
                 [--ok-if-no-labels [OK_IF_NO_LABELS]]
                 [--input-file-is-presorted [INPUT_IS_PRESORTED]]
                 [--label-file-is-presorted [LABELS_ARE_PRESORTED]] [-v]
                 [input_kgtk_file]

Lift labels for a KGTK file. For each of the items in the (node1, label, node2) columns, look for matching label records. If found, lift the label values into additional columns in the current record. Label records are reoved from the output. 

Additional options are shown in expert help.
kgtk --expert lift --help

positional arguments:
  input_kgtk_file       The KGTK file to lift. May be omitted or '-' for stdin.

optional arguments:
  -h, --help            show this help message and exit
  --label-file LABEL_KGTK_FILE
                        A KGTK file with label records (default=None).
  -o OUTPUT_KGTK_FILE, --output-file OUTPUT_KGTK_FILE
                        The KGTK file to write (default=-).
  --suppress-empty-columns [SUPPRESS_EMPTY_COLUMNS]
                        If true, do not create new columns that would be empty.
                        (default=False).
  --ok-if-no-labels [OK_IF_NO_LABELS]
                        If true, do not abort if no labels were found.
                        (default=False).
  --input-file-is-presorted [INPUT_IS_PRESORTED]
                        If true, the input file is presorted on the column for
                        which values are to be lifted. (default=False).
  --label-file-is-presorted [LABELS_ARE_PRESORTED]
                        If true, the label file is presorted on the node1 column.
                        (default=False).

  -v, --verbose         Print additional progress messages (default=False).
```

## Examples

Suppose that `file1.tsv` contains the following table in KGTK format:

| node1 | label | node2         |
| ----- | ----- | ------------- |
| Q1    | P1    | Q5            |
| Q1    | P2    | Q6            |
| Q1    | label | "Elmo"        |
| Q2    | label | "Alice"       |
| P1    | label | "instance of" |
| P2    | label | "friend"      |
| Q5    | label | "human"       |
| Q6    | P1    | Q5            |
| Q6    | label | "Fred"        |


```bash
kgtk lift file1.tsv
```

The output will be the following table in KGTK format:

| node1 | label | node2 | node1;label | label;label | node2;label |
| -- | -- | -- | -- | -- | -- |
| Q1 | P1 | Q5 | "Elmo" | "instance of" | "human" |
| Q1 | P2 | Q6 | "Elmo" | "friend" | "Fred" |
| Q6 | P1 | Q5 | "Fred" | "instance of" | "human" |

By default, `kgtk lift` will build a list of labels if multiple label records
are found for a property. The labels in the list will be sorted and
deduplicated.

Suppose that `file4.tsv` contains the following table in KGTK format:

| node1 | label | node2 |
| -- | -- | -- |
| Q1 | P1 | Q5 |
| Q1 | P2 | Q6 |
| Q1 | label | "Elmo" |
| Q2 | label | "Alice" |
| P1 | label | "instance of" |
| P2 | label | "friend" |
| P2 | label | "amigo" |
| Q5 | label | "human" |
| Q5 | label | "homo sapiens" |
| Q5 | label | "human" |
| Q6 | P1 | Q5 |
| Q6 | label | "Fred" |

```bash
kgtk lift file4.tsv
```


| node1 | label | node2 | node1;label | label;label | node2;label |
| -- | -- | -- | -- | -- | -- |
| Q1 | P1 | Q5 | "Elmo" | "instance of" | "homo sapiens"\|"human" |
| Q1 | P2 | Q6 | "Elmo" | "amigo"\|"friend" | "Fred" |
| Q6 | P1 | Q5 | "Fred" | "instance of" | "homo sapiens"\|"human" |

The labels may be in a seperate file from the input.  If
`--suppress-empty-columns` is `False` (its default), then the input file may be
processed in a single pass without keeping a copy in memory.  The labels will
still be loaded into an in-memory dictionary.

Suppose that `file5.tsv` contains the following table in KGTK format:

| node1 | label | node2 |
| -- | -- | -- |
| Q1 | P1 | Q5 |
| Q1 | P2 | Q6 |
| Q6 | P1 | Q5 |

And `file6.tsv` contains the following table in KGTK format:

| node1 | label | node2 |
| -- | -- | -- |
| Q1 | label | "Elmo" |
| Q2 | label | "Alice" |
| P1 | label | "instance of" |
| P2 | label | "friend" |
| Q5 | label | "human" |
| Q6 | label | "Fred" |


```bash
kgtk lift file5.tsv --label-file file6.tsv -v --columns-to-lift node1  --input-file-is-presorted --label-file-is-presorted --suppress-empty-columns
```
The output will be the following table in KGTK format:

| node1 | label | node2 | node1;label | label;label | node2;label |
| -- | -- | -- | -- | -- | -- |
| Q1 | P1 | Q5 | "Elmo" | "instance of" | "human" |
| Q1 | P2 | Q6 | "Elmo" | "friend" | "Fred" |
| Q6 | P1 | Q5 | "Fred" | "instance of" | "human" |

If the labels are in a seperate file from the input rows, and the labels are sorted
on the node1 column, and the only a single column will be lifted from the input rows,
and the input file is sorted on that column, and if `--suppress-empty-columns` is `False`
(its default), then the data may be process using a merge algorithm that does not
use in-memory buffering.


Suppose that `file7.tsv` contains the following table in KGTK format,
which is sorted on the `node1` column:

| node1 | label | node2 |
| -- | -- | -- |
| P1 | label | "instance of" |
| P2 | label | "friend" |
| Q1 | label | "Elmo" |
| Q2 | label | "Alice" |
| Q5 | label | "human" |
| Q6 | label | "Fred" |
| Q6 | label | "Wilma" |
| Q6 | label | "Wilma" |

```bash
kgtk lift lift-file5.tsv --label-file lift-file7.tsv -v --columns-to-lift node1  --input-file-is-presorted --label-file-is-presorted

```

The output will be the following table in KGTK format:

| node1 | label | node2 | node1;label |
| -- | -- | -- | -- |
| Q1 | P1 | Q5 | "Elmo" |
| Q1 | P2 | Q6 | "Elmo" |
| Q6 | P1 | Q5 | "Fred"\|"Wilma" |
