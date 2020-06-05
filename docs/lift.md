The lift command copies its input file to its output file,
adding label columns for values in the node1, label, and node2 fields.

The input rows are saved in memory, as well as the value-to-label mapping.
This will impose a limit on the size of the input files that can be processed.   

## Usage

```
usage: kgtk lift [-h] [-o OUTPUT_KGTK_FILE] [--suppress-empty-columns [SUPPRESS_EMPTY_COLUMNS]] [-v] [input_kgtk_file]

Lift labels for a KGTK file. For each of the items in the (node1, label, node2) columns, look for matching label records. If found, lift the label values into additional columns in the current record. Label records are reoved from the output. 

Additional options are shown in expert help.
kgtk --expert lift --help

positional arguments:
  input_kgtk_file       The KGTK file to lift. May be omitted or '-' for stdin.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_KGTK_FILE, --output-file OUTPUT_KGTK_FILE
                        The KGTK file to write (default=-).
  --suppress-empty-columns [SUPPRESS_EMPTY_COLUMNS]
                        If true, do not create new columns that would be empty. (default=False).
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

(Although one wonders whether Muppets should be labeled "human".  Perhaps "muppet"?)

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

The output will be the following table in KGTK format:

| node1 | label | node2 | node1;label | label;label | node2;label |
| -- | -- | -- | -- | -- | -- |
| Q1 | P1 | Q5 | "Elmo" | "instance of" | "homo sapiens"\|"human" |
| Q1 | P2 | Q6 | "Elmo" | "amigo"\|"friend" | "Fred" |
| Q6 | P1 | Q5 | "Fred" | "instance of" | "homo sapiens"\|"human" |
