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
kgtk lift file5.tsv --label-file file6.tsv --columns-to-lift node1  --input-file-is-presorted --label-file-is-presorted --suppress-empty-columns
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
kgtk lift lift-file5.tsv --label-file lift-file7.tsv --columns-to-lift node1  --input-file-is-presorted --label-file-is-presorted

```

The output will be the following table in KGTK format:

| node1 | label | node2 | node1;label |
| -- | -- | -- | -- |
| Q1 | P1 | Q5 | "Elmo" |
| Q1 | P2 | Q6 | "Elmo" |
| Q6 | P1 | Q5 | "Fred"\|"Wilma" |

Suppose that `file8.tsv` contains the following table in KGTK format:

| node1 | label | node2 | confident |
| -- | -- | -- | -- |
| Q1 | P1 | Q5 | True |
| Q1 | P2 | Q6 | True |
| Q2 | P1 | Q5 | False |
| Q2 | P2 | Q6 | False |

and suppose that `file9.tsv` contains the following file in KGTK format:

| node1 | label | node2 | full-name |
| -- | -- | -- | -- |
| P1 | label | "instance of" |  |
| P2 | label | "friend" |  |
| P3 | label | "enemy" |  |
| Q1 | name | "Elmo" | "Elmo Fudd" |
| Q2 | name | "Alice" | "Alice Cooper" |
| Q5 | species | "human" |  |
| Q6 | name | "Fred" | "Fred Rogers" |

Let's start with a default lift:

```bash
kgtk lift lift-file8.tsv --label-file lift-file9.tsv

```
| node1 | label | node2 | confident | node1;label | label;label | node2;label |
| -- | -- | -- | -- | -- | -- | -- |
| Q1 | P1 | Q5 | True |  | "instance of" |  |
| Q1 | P2 | Q6 | True |  | "friend" |  |
| Q2 | P1 | Q5 | False |  | "instance of" |  |
| Q2 | P2 | Q6 | False |  | "friend" |  |

Now, let's lift the `name` property:

```bash
kgtk lift lift-file8.tsv --label-file lift-file9.tsv --property name

```
| node1 | label | node2 | confident | node1;label | label;label | node2;label |
| -- | -- | -- | -- | -- | -- | -- |
| Q1 | P1 | Q5 | True | "Elmo" |  |  |
| Q1 | P2 | Q6 | True | "Elmo" |  | "Fred" |
| Q2 | P1 | Q5 | False | "Alice" |  |  |
| Q2 | P2 | Q6 | False | "Alice" |  | "Fred" |

Let's list the full names.

```bash
kgtk lift lift-file8.tsv --label-file lift-file9.tsv -p name --lift-from full-name

```

| node1 | label | node2 | confident | node1;label | label;label | node2;label |
| -- | -- | -- | -- | -- | -- | -- |
| Q1 | P1 | Q5 | True | "Elmo Fudd" |  |  |
| Q1 | P2 | Q6 | True | "Elmo Fudd" |  | "Fred Rogers" |
| Q2 | P1 | Q5 | False | "Alice Cooper" |  |  |
| Q2 | P2 | Q6 | False | "Alice Cooper" |  | "Fred Rogers" |

Let's list the full names only when we are confident in the relationship.


```bash
kgtk lift lift-file8.tsv \
          --label-file lift-file9.tsv \
          -p name \
	  -label-value-column full-name \
	  --input-select-column confident --input-select-value True

```
| node1 | label | node2 | confident | node1;label | label;label | node2;label |
| -- | -- | -- | -- | -- | -- | -- |
| Q1 | P1 | Q5 | True | "Elmo Fudd" |  |  |
| Q1 | P2 | Q6 | True | "Elmo Fudd" |  | "Fred Rogers" |
| Q2 | P1 | Q5 | False |  |  |  |
| Q2 | P2 | Q6 | False |  |  |  |

Let's lift full names into the node2 column.

```bash
kgtk lift lift-file8.tsv --label-file lift-file9.tsv --proerty name --lift-from full-name --columns-to-lift node2 --lift-suffix ""

```
| node1 | label | node2 | confident |
| -- | -- | -- | -- |
| Q1 | P1 | Q5 | True |
| Q1 | P2 | "Fred Rogers" | True |
| Q2 | P1 | Q5 | False |
| Q2 | P2 | "Fred Rogers" | False |


Let's lift full names into the node2 column, changing the label of the relationahip when we do so.

```bash
kgtk lift lift-file8.tsv \
          --label-file lift-file9.tsv \
	  --property name \
	  --lift-from full-name \
	  --columns-to-lift node2 \
	  --lift-suffix "" \
	  --update-select-value "FullName"

```
| node1 | label | node2 | confident |
| -- | -- | -- | -- |
| Q1 | P1 | Q5 | True |
| Q1 | FullName | "Fred Rogers" | True |
| Q2 | P1 | Q5 | False |
| Q2 | FullName | "Fred Rogers" | False |

Consider the following file, which is like `lift-file9.tsv`, but with the `node1` and `node2` columns swapped and with an additional column, `action`:

| node2 | label | node1 | full-name | action |
| -- | -- | -- | -- | -- |
| P1 | label | "instance of" |  | go |
| P2 | label | "friend" |  | go |
| P3 | label | "enemy" |  | go |
| Q1 | name | "Elmo" | "Elmo Fudd" | go |
| Q2 | name | "Alice" | "Alice Cooper" | go |
| Q5 | species | "human" |  | go |
| Q6 | name | "Fred" | "Fred Rogers" | go |

Let's lift full names from this file.  We'll swap the function of the node1 and node2 columns in the label file:

```bash
kgtk lift lift-file8.tsv \
          --label-file lift-file10.tsv \
	  --property name \
	  --lift-from full-name \
	  --columns-to-lift node2 \
	  --label-match-column node2 \
	  --label-value-column node1
```
| node1 | label | node2 | confident | node2;label |
| -- | -- | -- | -- | -- |
| Q1 | P1 | Q5 | True |  |
| Q1 | P2 | Q6 | True | "Fred" |
| Q2 | P1 | Q5 | False |  |
| Q2 | P2 | Q6 | False | "Fred" |

Let's pick up all labels using the `action` column's `go` value:
```bash
kgtk lift lift-file8.tsv \
          --label-file lift-file10.tsv \
	  --label-select-column action \
	  --label-select-value go \
	  --label-match-column node2 \
	  --label-value-column node1
```
| node1 | label | node2 | confident | node1;label | label;label | node2;label |
| -- | -- | -- | -- | -- | -- | -- |
| Q1 | P1 | Q5 | True | "Elmo" | "instance of" | "human" |
| Q1 | P2 | Q6 | True | "Elmo" | "friend" | "Fred" |
| Q2 | P1 | Q5 | False | "Alice" | "instance of" | "human" |
| Q2 | P2 | Q6 | False | "Alice" | "friend" | "Fred" |
