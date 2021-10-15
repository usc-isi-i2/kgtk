## Overview

The lift command copies its input file to its output file,
adding label columns for values in the node1, label, and node2 fields.
Options are available to control the columns being lifted, the source of the label values,
and the destination column for the label values.

### Memory Usage

By default, the input rows are saved in memory, as well as the value-to-label
mapping.  This will impose a limit on the size of the input files that can be
processed.

Seperating the labels from the  edges being lifted, and presorting each
of the files, enables operation with reduced memory requirements.

## Usage

```
usage: kgtk lift [-h] [-i INPUT_FILE] [-o OUTPUT_FILE]
                 [--label-file INPUT_FILE]
                 [--unmodified-row-output-file UNMODIFIED_ROW_OUTPUT_FILE]
                 [--matched-label-output-file MATCHED_LABEL_OUTPUT_FILE]
                 [--unmatched-label-output-file UNMATCHED_LABEL_OUTPUT_FILE]
                 [--columns-to-write [OUTPUT_LIFTED_COLUMN_NAMES [OUTPUT_LIFTED_COLUMN_NAMES ...]]]
                 [--default-value DEFAULT_VALUE]
                 [--suppress-empty-columns [True/False]]
                 [--ok-if-no-labels [True/False]]
                 [--prefilter-labels [True/False]]
                 [--input-file-is-presorted [True/False]]
                 [--label-file-is-presorted [True/False]]
                 [--clear-before-lift [CLEAR_BEFORE_LIFT]]
                 [--overwrite [OVERWRITE]]
                 [--output-only-modified-rows [OUTPUT_ONLY_MODIFIED_ROWS]]
                 [--use-label-envar [True/False]] [-v [optional True|False]]

Lift labels for a KGTK file. If called as "kgtk lift", for each of the items in the (node1, label, node2) columns, look for matching label records. If called as "kgtk add-labels", look for matching label records for all input columns. If found, lift the label values into additional columns in the current record. Label records are removed from the output unless --remove-label-records=False. 

Additional options are shown in expert help.
kgtk --expert lift --help

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK input file. (May be omitted or '-' for
                        stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for
                        stdout.)
  --label-file INPUT_FILE
                        A KGTK file with label records (Optional, use '-' for
                        stdin.)
  --unmodified-row-output-file UNMODIFIED_ROW_OUTPUT_FILE
                        A KGTK output file that will contain only unmodified
                        rows. This file will have the same columns as the
                        input file. (Optional, use '-' for stdout.)
  --matched-label-output-file MATCHED_LABEL_OUTPUT_FILE
                        A KGTK output file that will contain matched label
                        edges. This file will have the same columns as the
                        source of the labels, either the input file or the
                        label file. (Optional, use '-' for stdout.)
  --unmatched-label-output-file UNMATCHED_LABEL_OUTPUT_FILE
                        A KGTK output file that will contain unmatched label
                        edges. This file will have the same columns as the
                        source of the labels, either the input file or the
                        label file. (Optional, use '-' for stdout.)
  --columns-to-write [OUTPUT_LIFTED_COLUMN_NAMES [OUTPUT_LIFTED_COLUMN_NAMES ...]]
                        The columns into which to store the lifted values. The
                        default is [node1;label, label;label, node2;label] or
                        their aliases.
  --default-value DEFAULT_VALUE
                        The value to use if a lifted label is not found.
                        (default=)
  --suppress-empty-columns [True/False]
                        If true, do not create new columns that would be
                        empty. (default=False).
  --ok-if-no-labels [True/False]
                        If true, do not abort if no labels were found.
                        (default=False).
  --prefilter-labels [True/False]
                        If true, read the input file before reading the label
                        file. (default=False).
  --input-file-is-presorted [True/False]
                        If true, the input file is presorted on the column for
                        which values are to be lifted. (default=False).
  --label-file-is-presorted [True/False]
                        If true, the label file is presorted on the node1
                        column. (default=False).
  --clear-before-lift [CLEAR_BEFORE_LIFT]
                        If true, set columns to write to the default value
                        before lifting. (default=False).
  --overwrite [OVERWRITE]
                        If true, overwrite non-default values in the columns
                        to write. If false, do not overwrite non-default
                        values in the columns to write. (default=True).
  --output-only-modified-rows [OUTPUT_ONLY_MODIFIED_ROWS]
                        If true, output only modified edges to the primary
                        output stream. (default=False).
  --use-label-envar [True/False]
                        If true, use the KGTK_LABEL_FILE envar for the label
                        file if no --label-file. (default=False).

  -v [optional True|False], --verbose [optional True|False]
                        Print additional progress messages (default=False).
```

## Examples

### Sample Data

Suppose that `lift-file1.tsv` contains the following table in KGTK format:

```bash
kgtk cat --input-file examples/docs/lift-file1.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| Q1 | P1 | Q5 |
| Q1 | P2 | Q6 |
| Q1 | label | "Elmo" |
| Q2 | label | "Alice" |
| P1 | label | "instance of" |
| P2 | label | "friend" |
| Q5 | label | "human" |
| Q6 | P1 | Q5 |
| Q6 | label | "Fred" |


### Default Lift

```bash
kgtk lift --input-file examples/docs/lift-file1.tsv
```

The output will be the following table in KGTK format:

| node1 | label | node2 | node1;label | label;label | node2;label |
| -- | -- | -- | -- | -- | -- |
| Q1 | P1 | Q5 | "Elmo" | "instance of" | "human" |
| Q1 | P2 | Q6 | "Elmo" | "friend" | "Fred" |
| Q6 | P1 | Q5 | "Fred" | "instance of" | "human" |

`kgtk lift` has moved the labels into additional columns and removed
the label edges from the output file.

### Multiple Labels

By default, `kgtk lift` will build a list of labels if multiple label records
are found for a property. The labels in the list will be sorted and
deduplicated.

Suppose that `lift-file4.tsv` contains the following table in KGTK format:

```bash
kgtk cat --input-file examples/docs/lift-file4.tsv
```

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

Lift this file with no additional arguments:

```bash
kgtk lift --input-file examples/docs/lift-file4.tsv
```

| node1 | label | node2 | node1;label | label;label | node2;label |
| -- | -- | -- | -- | -- | -- |
| Q1 | P1 | Q5 | "Elmo" | "instance of" | "homo sapiens"\|"human" |
| Q1 | P2 | Q6 | "Elmo" | "amigo"\|"friend" | "Fred" |
| Q6 | P1 | Q5 | "Fred" | "instance of" | "homo sapiens"\|"human" |

### Lifting Specific Columns

Lift this file, lifting just the `node1` column:

```bash
kgtk lift --input-file examples/docs/lift-file4.tsv \
          --columns-to-lift node1
```
The output will be the following table in KGTK format:

| node1 | label | node2 | node1;label |
| -- | -- | -- | -- |
| Q1 | P1 | Q5 | "Elmo" |
| Q1 | P2 | Q6 | "Elmo" |
| Q6 | P1 | Q5 | "Fred" |

### Seperate Input Files

The labels may be in a seperate file from the input.  If
`--suppress-empty-columns` is `False` (its default), then the input file may be
processed in a single pass without keeping a copy in memory.  The labels will
still be loaded into an in-memory dictionary.

Suppose that `lift-file5.tsv` contains the following table in KGTK format:

```bash
kgtk cat --input-file examples/docs/lift-file5.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| Q1 | P1 | Q5 |
| Q1 | P2 | Q6 |
| Q6 | P1 | Q5 |

And `lift-file6.tsv` contains the following table in KGTK format:

```bash
kgtk cat --input-file examples/docs/lift-file6.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| Q1 | label | "Elmo" |
| Q2 | label | "Alice" |
| Q5 | label | "human" |
| Q6 | label | "Fred" |
| P1 | label | "instance of" |
| P2 | label | "friend" |

```bash
kgtk lift --input-file examples/docs/lift-file5.tsv \
          --label-file examples/docs/lift-file6.tsv \
          --columns-to-lift node1
```
The output will be the following table in KGTK format:

| node1 | label | node2 | node1;label |
| -- | -- | -- | -- |
| Q1 | P1 | Q5 | "Elmo" |
| Q1 | P2 | Q6 | "Elmo" |
| Q6 | P1 | Q5 | "Fred" |

### Presorted Input Files

If the labels are in a seperate file from the input rows, and the labels are sorted
on the node1 column, and the only a single column will be lifted from the input rows,
and the input file is sorted on that column, and if `--suppress-empty-columns` is `False`
(its default), then the data may be processed using a merge algorithm that does not
use in-memory buffering.  This is useful if the input and label files are both very
large.

```bash
kgtk lift --input-file examples/docs/lift-file5.tsv \
          --input-file-is-presorted \
          --label-file examples/docs/lift-file6.tsv \
          --label-file-is-presorted \
          --columns-to-lift node1
```
The output will be the following table in KGTK format:

| node1 | label | node2 | node1;label |
| -- | -- | -- | -- |
| Q1 | P1 | Q5 | "Elmo" |
| Q1 | P2 | Q6 | "Elmo" |
| Q6 | P1 | Q5 | "Fred" |


### Small Input, Many Labels

If the label file is very large but not sorted, and the input file is small
enough to fit in memory, then one alternate approach is to use
`--prefilter-labels`.  This causes the input file to be read into memory
first, then the values that need labels are extracted from it.  Next,
the label file is read, filtering out unneeded labels and keeping only needed
labels in memory.  Finally, the output file is generated from the in-memory
copy of the input file and the labels.  Multiple columns may be lifted in a
single pass with this approach.

```bash
kgtk lift --input-file examples/docs/lift-file5.tsv \
          --label-file examples/docs/lift-file6.tsv \
          --prefilter-labels
```
| node1 | label | node2 | node1;label | label;label | node2;label |
| -- | -- | -- | -- | -- | -- |
| Q1 | P1 | Q5 | "Elmo" | "instance of" | "human" |
| Q1 | P2 | Q6 | "Elmo" | "friend" | "Fred" |
| Q6 | P1 | Q5 | "Fred" | "instance of" | "human" |

### Duplicate Labels

Suppose that `lift-file7.tsv` contains the following table in KGTK format,
which is sorted on the `node1` column:

```bash
kgtk cat --input-file examples/docs/lift-file7.tsv
```

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

Lift the duplicate labels, using the presorted options:

```bash
kgtk lift --input-file examples/docs/lift-file5.tsv \
          --input-file-is-presorted \
          --label-file examples/docs/lift-file7.tsv \
          --label-file-is-presorted \
          --columns-to-lift node1
```

The output will be the following table in KGTK format:

| node1 | label | node2 | node1;label |
| -- | -- | -- | -- |
| Q1 | P1 | Q5 | "Elmo" |
| Q1 | P2 | Q6 | "Elmo" |
| Q6 | P1 | Q5 | "Fred"\|"Wilma" |

### More Sample Data

Suppose that `lift-file8.tsv` contains the following table in KGTK format:

```bash
kgtk cat --input-file examples/docs/lift-file8.tsv
```

| node1 | label | node2 | confident |
| -- | -- | -- | -- |
| Q1 | P1 | Q5 | True |
| Q1 | P2 | Q6 | True |
| Q2 | P1 | Q5 | False |
| Q2 | P2 | Q6 | False |

and suppose that `lift-file9.tsv` contains the following file in KGTK format:

```bash
kgtk cat --input-file examples/docs/lift-file9.tsv
```
| node1 | label | node2 | full-name |
| -- | -- | -- | -- |
| P1 | label | "instance of" |  |
| P2 | label | "friend" |  |
| P3 | label | "enemy" |  |
| Q1 | name | "Elmo" | "Elmo Fudd" |
| Q2 | name | "Alice" | "Alice Cooper" |
| Q5 | species | "human" |  |
| Q6 | name | "Fred" | "Fred Rogers" |

### Default Lift, Seperate Label File

Let's start with a default lift with the seperate label file:

```bash
kgtk lift --input-file examples/docs/lift-file8.tsv \
          --label-file examples/docs/lift-file9.tsv
```
| node1 | label | node2 | confident | node1;label | label;label | node2;label |
| -- | -- | -- | -- | -- | -- | -- |
| Q1 | P1 | Q5 | True |  | "instance of" |  |
| Q1 | P2 | Q6 | True |  | "friend" |  |
| Q2 | P1 | Q5 | False |  | "instance of" |  |
| Q2 | P2 | Q6 | False |  | "friend" |  |

### Lift a Single Property

Now, let's lift the `name` property (`label` column value):

```bash
kgtk lift --input-file examples/docs/lift-file8.tsv \
          --label-file examples/docs/lift-file9.tsv \
	  --property name
```

| node1 | label | node2 | confident | node1;label | label;label | node2;label |
| -- | -- | -- | -- | -- | -- | -- |
| Q1 | P1 | Q5 | True | "Elmo" |  |  |
| Q1 | P2 | Q6 | True | "Elmo" |  | "Fred" |
| Q2 | P1 | Q5 | False | "Alice" |  |  |
| Q2 | P2 | Q6 | False | "Alice" |  | "Fred" |

### Lift with a Column Name Suffix

Now, let's lift the `name` property, using ";name" as the column name suffix:

```bash
kgtk lift --input-file examples/docs/lift-file8.tsv \
          --label-file examples/docs/lift-file9.tsv \
          --property name \
          --lift-suffix ";name"
```

| node1 | label | node2 | confident | node1;name | label;name | node2;name |
| -- | -- | -- | -- | -- | -- | -- |
| Q1 | P1 | Q5 | True | "Elmo" |  |  |
| Q1 | P2 | Q6 | True | "Elmo" |  | "Fred" |
| Q2 | P1 | Q5 | False | "Alice" |  |  |
| Q2 | P2 | Q6 | False | "Alice" |  | "Fred" |

!!! note
    The `;node` argument needs to be quoted on the command line, since `;` is
    a shell metacharacter.

### Lift from a Specific Column

Let's lift the full names column.  The `--lift-from` option
(also known as the `label-value-column` option) allows us
to lift from a column other than the default, `node2`:

```bash
kgtk lift --input-file examples/docs/lift-file8.tsv \
          --label-file examples/docs/lift-file9.tsv \
          --property name \
          --lift-from full-name
```

| node1 | label | node2 | confident | node1;label | label;label | node2;label |
| -- | -- | -- | -- | -- | -- | -- |
| Q1 | P1 | Q5 | True | "Elmo Fudd" |  |  |
| Q1 | P2 | Q6 | True | "Elmo Fudd" |  | "Fred Rogers" |
| Q2 | P1 | Q5 | False | "Alice Cooper" |  |  |
| Q2 | P2 | Q6 | False | "Alice Cooper" |  | "Fred Rogers" |

### Lift from a Specific Column with a Column Name Suffix

Let's lift the full names again, this time using ";full-name" as the column
name suffix instead of "label".

```bash
kgtk lift --input-file examples/docs/lift-file8.tsv \
          --label-file examples/docs/lift-file9.tsv \
          --property name \
          --lift-from full-name \
          --lift-suffix ";full-name"
```

| node1 | label | node2 | confident | node1;full-name | label;full-name | node2;full-name |
| -- | -- | -- | -- | -- | -- | -- |
| Q1 | P1 | Q5 | True | "Elmo Fudd" |  |  |
| Q1 | P2 | Q6 | True | "Elmo Fudd" |  | "Fred Rogers" |
| Q2 | P1 | Q5 | False | "Alice Cooper" |  |  |
| Q2 | P2 | Q6 | False | "Alice Cooper" |  | "Fred Rogers" |

!!! note
    The `;full-name` needs to be quoted on the command line, since `;` is
    a shell metacharacter.

### Outputting Only Modified Rows

Let's output only modified rows.  We will start by outputting
all rows:

```bash
kgtk lift --input-file examples/docs/lift-file8.tsv \
          --label-file examples/docs/lift-file9.tsv \
          --property name \
          --lift-from full-name \
          --lift-suffix ";full-name" \
	  --columns-to-lift node2
```

| node1 | label | node2 | confident | node2;full-name |
| -- | -- | -- | -- | -- |
| Q1 | P1 | Q5 | True |  |
| Q1 | P2 | Q6 | True | "Fred Rogers" |
| Q2 | P1 | Q5 | False |  |
| Q2 | P2 | Q6 | False | "Fred Rogers" |

Next, we will output only the modified rows:

```bash
kgtk lift --input-file examples/docs/lift-file8.tsv \
          --label-file examples/docs/lift-file9.tsv \
          --property name \
          --lift-from full-name \
          --lift-suffix ";full-name" \
	  --columns-to-lift node2 \
	  --output-only-modified-rows
```

| node1 | label | node2 | confident | node2;full-name |
| -- | -- | -- | -- | -- |
| Q1 | P2 | Q6 | True | "Fred Rogers" |
| Q2 | P2 | Q6 | False | "Fred Rogers" |

### Unmodified Row Output File

Suppose we want to isolate the unmodified rows for
further processing.  We can send them to the unmodified row
output file.

We will send only the modified rows to the primary output
stream by using `--output-only-modified-rows`.

```bash
kgtk lift --input-file examples/docs/lift-file8.tsv \
          --label-file examples/docs/lift-file9.tsv \
          --property name \
          --lift-from full-name \
          --lift-suffix ";full-name" \
	  --columns-to-lift node2 \
	  --output-only-modified-rows \
	  --unmodified-row-output-file lift-unmodified-rows.tsv
```

| node1 | label | node2 | confident | node2;full-name |
| -- | -- | -- | -- | -- |
| Q1 | P2 | Q6 | True | "Fred Rogers" |
| Q2 | P2 | Q6 | False | "Fred Rogers" |

Here are the unmodified rows:

```bash
kgtk cat -i lift-unmodified-rows.tsv
```

| node1 | label | node2 | confident |
| -- | -- | -- | -- |
| Q1 | P1 | Q5 | True |
| Q2 | P1 | Q5 | False |

!!! note
    The unmodified row output file has the same columns as the
    primary input file.  In this example, it does not have the
    `node2;full-name` column that was added to the primary
    output file.

### Matched Label Output File

Suppose we are interested in finding which label file edges were matched with
input file edges during the lift.  The `--matched-label-output-file
OUTPUT_FILE` option provides a simple way to get this list.


```bash
kgtk lift --input-file examples/docs/lift-file8.tsv \
          --label-file examples/docs/lift-file9.tsv \
          --property name \
          --lift-from full-name \
          --lift-suffix ";full-name" \
	  --columns-to-lift node2 \
	  --output-only-modified-rows \
	  --matched-label-output-file lift-matched-labels.tsv
```

| node1 | label | node2 | confident | node2;full-name |
| -- | -- | -- | -- | -- |
| Q1 | P2 | Q6 | True | "Fred Rogers" |
| Q2 | P2 | Q6 | False | "Fred Rogers" |

Here are the matched labels:

```bash
kgtk cat -i lift-matched-labels.tsv
```

| node1 | label | node2 | full-name |
| -- | -- | -- | -- |
| Q6 | name | "Fred" | "Fred Rogers" |

!!! note
    The matched label output file has the same columns as the
    label file when a label file has been specified.  Otherwise,
    the matched label file has the same columns as the primary
    input file.

!!! note
    Logically, there should be an `--unmatched-labels-output-file OUTPUT_FILE`
    option.  This option may be added in the future.

!!! note
    It may be useful if the matched label output file had an additional
    column with a count of the number of matches.  This option may be
    added in the future.

### Unmatched Label Output File

Suppose we are interested in finding which label file edges were not matched with
input file edges during the lift.  The `--unmatched-label-output-file
OUTPUT_FILE` option provides a simple way to get this list.


```bash
kgtk lift --input-file examples/docs/lift-file8.tsv \
          --label-file examples/docs/lift-file9.tsv \
          --property name \
          --lift-from full-name \
          --lift-suffix ";full-name" \
	  --columns-to-lift node2 \
	  --output-only-modified-rows \
	  --unmatched-label-output-file lift-unmatched-labels.tsv
```

| node1 | label | node2 | confident | node2;full-name |
| -- | -- | -- | -- | -- |
| Q1 | P2 | Q6 | True | "Fred Rogers" |
| Q2 | P2 | Q6 | False | "Fred Rogers" |

Here are the unmatched labels:

```bash
kgtk cat -i lift-unmatched-labels.tsv
```

| node1 | label | node2 | full-name |
| -- | -- | -- | -- |
| Q1 | name | "Elmo" | "Elmo Fudd" |
| Q2 | name | "Alice" | "Alice Cooper" |

!!! note
    The unmatched label output file has the same columns as the
    label file when a label file has been specified.  Otherwise,
    the unmatched label file has the same columns as the primary
    input file.

### Expert Example: Input Filtering

Let's list the full names only when we are confident in the relationship.
The expert options `--input-select-column INPUT_SELECT_COLUMN_NAME` and `--input-select-value INPUT_SELECT_COLUMN_VALUE`
provide a built-in filter operation.

```bash
kgtk lift --input-file examples/docs/lift-file8.tsv \
          --label-file examples/docs/lift-file9.tsv \
          -p name \
          --label-value-column full-name \
          --input-select-column confident \
          --input-select-value True

```

| node1 | label | node2 | confident | node1;label | label;label | node2;label |
| -- | -- | -- | -- | -- | -- | -- |
| Q1 | P1 | Q5 | True | "Elmo Fudd" |  |  |
| Q1 | P2 | Q6 | True | "Elmo Fudd" |  | "Fred Rogers" |
| Q2 | P1 | Q5 | False |  |  |  |
| Q2 | P2 | Q6 | False |  |  |  |

### Expert Example: Lifting into `node2`

Let's lift full names into the node2 column, replacing the
existing values there.  We can do this by specifying
`--columns-to-lift node2` and giving an empty `--lift-suffix`.

```bash
kgtk lift --input-file examples/docs/lift-file8.tsv \
          --label-file examples/docs/lift-file9.tsv \
          --property name \
          --lift-from full-name \
          --columns-to-lift node2 \
          --lift-suffix ""
```

| node1 | label | node2 | confident |
| -- | -- | -- | -- |
| Q1 | P1 | Q5 | True |
| Q1 | P2 | "Fred Rogers" | True |
| Q2 | P1 | Q5 | False |
| Q2 | P2 | "Fred Rogers" | False |

!!! note
    `--lift-suffix ""' uses shell quotes to specify an empty value.
    `--lift-suffix=` is another way to specify the empty lift suffix,
    and does not require shell quoting.

!!! note
    This procedure, repeated for the `node1`, `label`, and `node2`
    columns, can be used to transform relationships from one
    knowledge base system to another.

### Expert Example: Lifting into `node2`, Outputting Only Modified Rows

Let's lift full names into the node2 column, replacing the
existing values there.  We can do this by specifying
`--columns-to-lift node2` and giving an empty `--lift-suffix`.
We will output only modified rows.

```bash
kgtk lift --input-file examples/docs/lift-file8.tsv \
          --label-file examples/docs/lift-file9.tsv \
          --property name \
          --lift-from full-name \
          --columns-to-lift node2 \
          --lift-suffix= \
	  --output-only-modified-rows
```

| node1 | label | node2 | confident |
| -- | -- | -- | -- |
| Q1 | P2 | "Fred Rogers" | True |
| Q2 | P2 | "Fred Rogers" | False |

### Expert Example: Update Lifted Relationships

Let's lift full names into the node2 column, changing the label of the relationahip when we do so.

```bash
kgtk lift --input-file examples/docs/lift-file8.tsv \
          --label-file examples/docs/lift-file9.tsv \
          --property name \
          --lift-from full-name \
          --columns-to-lift node2 \
          --lift-suffix "" \
          --update-select-value FullName
```

| node1 | label | node2 | confident |
| -- | -- | -- | -- |
| Q1 | P1 | Q5 | True |
| Q1 | FullName | "Fred Rogers" | True |
| Q2 | P1 | Q5 | False |
| Q2 | FullName | "Fred Rogers" | False |

### Expert Example: Overriding the Label Match and Value Columns

Consider the following file, `lift-file10.tsv`, which is like `lift-file9.tsv`,
but with the `node1` and `node2` columns swapped and with an additional column, `action`:

```bash
kgtk cat --input-file examples/docs/lift-file10.tsv
```

| node1 | label | node2 | full-name | action |
| -- | -- | -- | -- | -- |
| "instance of" | label | P1 |  | go |
| "friend" | label | P2 |  | go |
| "enemy" | label | P3 |  | go |
| "Elmo" | name | Q1 | "Elmo Fudd" | go |
| "Alice" | name | Q2 | "Alice Cooper" | go |
| "human" | species | Q5 |  | go |
| "Fred" | name | Q6 | "Fred Rogers" | go |

Let's lift full names from this file.  We'll swap the function of the node1 and node2 columns in the label file:

```bash
kgtk lift --input-file examples/docs/lift-file8.tsv \
          --label-file examples/docs/lift-file10.tsv \
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

### Expert Example: Selecting the Labels to Lift

Let's pick up all labels using the `action` column's `go` value
to select the labels that we pick:

```bash
kgtk lift --input-file examples/docs/lift-file8.tsv \
          --label-file examples/docs/lift-file10.tsv \
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

If we hadn't filtered the labels, the output would have looked like this:

```bash
kgtk lift --input-file examples/docs/lift-file8.tsv \
          --label-file examples/docs/lift-file10.tsv \
          --label-match-column node2 \
          --label-value-column node1
```

| node1 | label | node2 | confident | node1;label | label;label | node2;label |
| -- | -- | -- | -- | -- | -- | -- |
| Q1 | P1 | Q5 | True |  | "instance of" |  |
| Q1 | P2 | Q6 | True |  | "friend" |  |
| Q2 | P1 | Q5 | False |  | "instance of" |  |
| Q2 | P2 | Q6 | False |  | "friend" |  |
