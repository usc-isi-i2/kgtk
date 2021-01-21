## Overview

This command performs calculations on one or more columns in a KGTK file. 
If no input filename is provided, the default is to read standard input. 

## Usage

```
usage: kgtk calc [-h] [-i INPUT_FILE] [-o OUTPUT_FILE]
                 [-c [COLUMN_NAME [COLUMN_NAME ...]]] --into INTO_COLUMN_NAMES
                 [INTO_COLUMN_NAMES ...] --do
                 {average,copy,join,percentage,set,sum}
                 [--values [VALUES [VALUES ...]]] [--format FORMAT_STRING]
                 [-v [optional True|False]]

This command performs calculations on one or more columns in a KGTK file. 
If no input filename is provided, the default is to read standard input. 

Additional options are shown in expert help.
kgtk --expert rename_columns --help

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK input file. (May be omitted or '-' for
                        stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for
                        stdout.)
  -c [COLUMN_NAME [COLUMN_NAME ...]], --columns [COLUMN_NAME [COLUMN_NAME ...]]
                        The list of source column names, optionally containing
                        '..' for column ranges and '...' for column names not
                        explicitly mentioned.
  --into INTO_COLUMN_NAMES [INTO_COLUMN_NAMES ...]
                        The name of the column to receive the result of the
                        calculation.
  --do {average,copy,join,percentage,set,sum}
                        The name of the operation.
  --values [VALUES [VALUES ...]]
                        An optional list of values
  --format FORMAT_STRING
                        The format string for the calculation.

  -v [optional True|False], --verbose [optional True|False]
                        Print additional progress messages (default=False).
```

## Examples

### Sample Data

Suppose that `file1.tsv` contains the following table in KGTK format:

```bash
kgtk cat -i examples/docs/calc-file1.tsv
```

| node1 | label | node2 | node1;total |
| -- | -- | -- | -- |
| P10 | p585-count | 73 | 3879 |
| P1000 | p585-count | 16 | 266 |
| P101 | p585-count | 5 | 157519 |
| P1018 | p585-count | 2 | 177 |
| P102 | p585-count | 295 | 414726 |
| P1025 | p585-count | 26 | 693 |
| P1026 | p585-count | 40 | 6930 |
| P1027 | p585-count | 14 | 10008 |
| P1028 | p585-count | 1131 | 4035 |
| P1029 | p585-count | 4 | 2643 |
| P1035 | p585-count | 4 | 366 |
| P1037 | p585-count | 60 | 9317 |
| P1040 | p585-count | 1 | 45073 |
| P1050 | p585-count | 246 | 226380 |


### Calculate the average of `node2` and `node1;total`.

!!! info
    `--do average` requires at least one source column (`--columns`) and one destination column (`--into`).

!!! info
    The format option (`--format`), which takes a Python %-style format string as argument,
    may be used to format the result of this calculation.

```bash
kgtk calc -i examples/docs/calc-file1.tsv -c node2 "node1;total" --into result --do average
```

The output will be the following table in KGTK format:

| node1 | label | node2 | node1;total | result |
| -- | -- | -- | -- | -- |
| P10 | p585-count | 73 | 3879 | 1976.00 |
| P1000 | p585-count | 16 | 266 | 141.00 |
| P101 | p585-count | 5 | 157519 | 78762.00 |
| P1018 | p585-count | 2 | 177 | 89.50 |
| P102 | p585-count | 295 | 414726 | 207510.50 |
| P1025 | p585-count | 26 | 693 | 359.50 |
| P1026 | p585-count | 40 | 6930 | 3485.00 |
| P1027 | p585-count | 14 | 10008 | 5011.00 |
| P1028 | p585-count | 1131 | 4035 | 2583.00 |
| P1029 | p585-count | 4 | 2643 | 1323.50 |
| P1035 | p585-count | 4 | 366 | 185.00 |
| P1037 | p585-count | 60 | 9317 | 4688.50 |
| P1040 | p585-count | 1 | 45073 | 22537.00 |
| P1050 | p585-count | 246 | 226380 | 113313.00 |

### Copy `node2` into the `node2-copy` column.

!!! info
    `--do copy` requires at least one source column (`--columns`) and at least one destination column (`--into`).
    The number of source and destination columns must match.

```bash
kgtk calc -i examples/docs/calc-file1.tsv -c node2 --into node2-copy --do copy
```

The output will be the following table in KGTK format:

| node1 | label | node2 | node1;total | node2-copy |
| -- | -- | -- | -- | -- |
| P10 | p585-count | 73 | 3879 | 73 |
| P1000 | p585-count | 16 | 266 | 16 |
| P101 | p585-count | 5 | 157519 | 5 |
| P1018 | p585-count | 2 | 177 | 2 |
| P102 | p585-count | 295 | 414726 | 295 |
| P1025 | p585-count | 26 | 693 | 26 |
| P1026 | p585-count | 40 | 6930 | 40 |
| P1027 | p585-count | 14 | 10008 | 14 |
| P1028 | p585-count | 1131 | 4035 | 1131 |
| P1029 | p585-count | 4 | 2643 | 4 |
| P1035 | p585-count | 4 | 366 | 4 |
| P1037 | p585-count | 60 | 9317 | 60 |
| P1040 | p585-count | 1 | 45073 | 1 |
| P1050 | p585-count | 246 | 226380 | 246 |


### Copy and swap the `node2` and 'node1;total' column values.

!!! info
    When multiple columns are copied in the same command, the copies take place
    simultaneously.  This allows column values to be swapped, shifted, permuted, etc.

```bash
kgtk calc -i examples/docs/calc-file1.tsv -c node2 "node1;total" --into "node1;total" node2 --do copy
```

The output will be the following table in KGTK format:

| node1 | label | node2 | node1;total |
| -- | -- | -- | -- |
| P10 | p585-count | 3879 | 73 |
| P1000 | p585-count | 266 | 16 |
| P101 | p585-count | 157519 | 5 |
| P1018 | p585-count | 177 | 2 |
| P102 | p585-count | 414726 | 295 |
| P1025 | p585-count | 693 | 26 |
| P1026 | p585-count | 6930 | 40 |
| P1027 | p585-count | 10008 | 14 |
| P1028 | p585-count | 4035 | 1131 |
| P1029 | p585-count | 2643 | 4 |
| P1035 | p585-count | 366 | 4 |
| P1037 | p585-count | 9317 | 60 |
| P1040 | p585-count | 45073 | 1 |
| P1050 | p585-count | 226380 | 246 |

### Join the 'node1' and 'label' column values using ':' as a separator.

!!! info
    `---do join` requires at least one source column (`--columns`) and one destination column (`--into`).
    It also needs one `--values` argument, which may be an explicit empty value (`--values ""`),
    to provide the separator between the joined fields.

```bash
kgtk calc -i examples/docs/calc-file1.tsv -c node1 label --value : --into result --do join
```

The output will be the following table in KGTK format:

| node1 | label | node2 | node1;total | result |
| -- | -- | -- | -- | -- |
| P10 | p585-count | 73 | 3879 | P10:p585-count |
| P1000 | p585-count | 16 | 266 | P1000:p585-count |
| P101 | p585-count | 5 | 157519 | P101:p585-count |
| P1018 | p585-count | 2 | 177 | P1018:p585-count |
| P102 | p585-count | 295 | 414726 | P102:p585-count |
| P1025 | p585-count | 26 | 693 | P1025:p585-count |
| P1026 | p585-count | 40 | 6930 | P1026:p585-count |
| P1027 | p585-count | 14 | 10008 | P1027:p585-count |
| P1028 | p585-count | 1131 | 4035 | P1028:p585-count |
| P1029 | p585-count | 4 | 2643 | P1029:p585-count |
| P1035 | p585-count | 4 | 366 | P1035:p585-count |
| P1037 | p585-count | 60 | 9317 | P1037:p585-count |
| P1040 | p585-count | 1 | 45073 | P1040:p585-count |
| P1050 | p585-count | 246 | 226380 | P1050:p585-count |

### Join the 'node1' and 'label' column values without a separator.

!!! info
    `---do join` requires at least one source column (`--columns`) and one destination column (`--into`).
    It also needs one `--values` argument, which may be an explicit empty value (`--values ""`),
    to provide the separator between the joined fields.

```bash
kgtk calc -i examples/docs/calc-file1.tsv -c node1 label --value "" --into result --do join
```

The output will be the following table in KGTK format:

| node1 | label | node2 | node1;total | result |
| -- | -- | -- | -- | -- |
| P10 | p585-count | 73 | 3879 | P10p585-count |
| P1000 | p585-count | 16 | 266 | P1000p585-count |
| P101 | p585-count | 5 | 157519 | P101p585-count |
| P1018 | p585-count | 2 | 177 | P1018p585-count |
| P102 | p585-count | 295 | 414726 | P102p585-count |
| P1025 | p585-count | 26 | 693 | P1025p585-count |
| P1026 | p585-count | 40 | 6930 | P1026p585-count |
| P1027 | p585-count | 14 | 10008 | P1027p585-count |
| P1028 | p585-count | 1131 | 4035 | P1028p585-count |
| P1029 | p585-count | 4 | 2643 | P1029p585-count |
| P1035 | p585-count | 4 | 366 | P1035p585-count |
| P1037 | p585-count | 60 | 9317 | P1037p585-count |
| P1040 | p585-count | 1 | 45073 | P1040p585-count |
| P1050 | p585-count | 246 | 226380 | P1050p585-count |

### Calculate the percentage of `node2` and `node1;total`.

!!! info
    `--do percent` requires two source columns (`--columns`) and one destination column (`--into`).

!!! info
    The format option (`--format`), which takes a Python %-style format string as argument,
    may be used to format the result of this calculation.

```bash
kgtk calc -i examples/docs/calc-file1.tsv -c node2 "node1;total" --into result --do percentage
```

The output will be the following table in KGTK format:

| node1 | label | node2 | node1;total | result |
| -- | -- | -- | -- | -- |
| P10 | p585-count | 73 | 3879 |  1.88 |
| P1000 | p585-count | 16 | 266 |  6.02 |
| P101 | p585-count | 5 | 157519 |  0.00 |
| P1018 | p585-count | 2 | 177 |  1.13 |
| P102 | p585-count | 295 | 414726 |  0.07 |
| P1025 | p585-count | 26 | 693 |  3.75 |
| P1026 | p585-count | 40 | 6930 |  0.58 |
| P1027 | p585-count | 14 | 10008 |  0.14 |
| P1028 | p585-count | 1131 | 4035 | 28.03 |
| P1029 | p585-count | 4 | 2643 |  0.15 |
| P1035 | p585-count | 4 | 366 |  1.09 |
| P1037 | p585-count | 60 | 9317 |  0.64 |
| P1040 | p585-count | 1 | 45073 |  0.00 |
| P1050 | p585-count | 246 | 226380 |  0.11 |

### Set a value into a column.

!!! info
    `--do set` requires at least one `--values` argument and a matching number of destination columnes (`--into`).
    It does not allow any source columne (`--columns`).

```bash
kgtk calc -i examples/docs/calc-file1.tsv --value xxx --into result --do set
```

The output will be the following table in KGTK format:

| node1 | label | node2 | node1;total | result |
| -- | -- | -- | -- | -- |
| P10 | p585-count | 73 | 3879 | xxx |
| P1000 | p585-count | 16 | 266 | xxx |
| P101 | p585-count | 5 | 157519 | xxx |
| P1018 | p585-count | 2 | 177 | xxx |
| P102 | p585-count | 295 | 414726 | xxx |
| P1025 | p585-count | 26 | 693 | xxx |
| P1026 | p585-count | 40 | 6930 | xxx |
| P1027 | p585-count | 14 | 10008 | xxx |
| P1028 | p585-count | 1131 | 4035 | xxx |
| P1029 | p585-count | 4 | 2643 | xxx |
| P1035 | p585-count | 4 | 366 | xxx |
| P1037 | p585-count | 60 | 9317 | xxx |
| P1040 | p585-count | 1 | 45073 | xxx |
| P1050 | p585-count | 246 | 226380 | xxx |

### Calculate the sum of `node2` and `node1;total`.

!!! info
    `--do sum` requires at least one source column (`--columns`) and one destination column (`--into`).

!!! info
    The format option (`--format`), which takes a Python %-style format string as argument,
    may be used to format the result of the calculation.

```bash
kgtk calc -i examples/docs/calc-file1.tsv -c node2 "node1;total" --into result --do sum
```

The output will be the following table in KGTK format:

| node1 | label | node2 | node1;total | result |
| -- | -- | -- | -- | -- |
| P10 | p585-count | 73 | 3879 | 3952.00 |
| P1000 | p585-count | 16 | 266 | 282.00 |
| P101 | p585-count | 5 | 157519 | 157524.00 |
| P1018 | p585-count | 2 | 177 | 179.00 |
| P102 | p585-count | 295 | 414726 | 415021.00 |
| P1025 | p585-count | 26 | 693 | 719.00 |
| P1026 | p585-count | 40 | 6930 | 6970.00 |
| P1027 | p585-count | 14 | 10008 | 10022.00 |
| P1028 | p585-count | 1131 | 4035 | 5166.00 |
| P1029 | p585-count | 4 | 2643 | 2647.00 |
| P1035 | p585-count | 4 | 366 | 370.00 |
| P1037 | p585-count | 60 | 9317 | 9377.00 |
| P1040 | p585-count | 1 | 45073 | 45074.00 |
| P1050 | p585-count | 246 | 226380 | 226626.00 |

### Calculate the sum of `node2` and `node1;total`, with the result formatted as an integer.

```bash
kgtk calc -i examples/docs/calc-file1.tsv -c node2 "node1;total" --into result --do sum --format '%d'
```

The output will be the following table in KGTK format:

| node1 | label | node2 | node1;total | result |
| -- | -- | -- | -- | -- |
| P10 | p585-count | 73 | 3879 | 3952 |
| P1000 | p585-count | 16 | 266 | 282 |
| P101 | p585-count | 5 | 157519 | 157524 |
| P1018 | p585-count | 2 | 177 | 179 |
| P102 | p585-count | 295 | 414726 | 415021 |
| P1025 | p585-count | 26 | 693 | 719 |
| P1026 | p585-count | 40 | 6930 | 6970 |
| P1027 | p585-count | 14 | 10008 | 10022 |
| P1028 | p585-count | 1131 | 4035 | 5166 |
| P1029 | p585-count | 4 | 2643 | 2647 |
| P1035 | p585-count | 4 | 366 | 370 |
| P1037 | p585-count | 60 | 9317 | 9377 |
| P1040 | p585-count | 1 | 45073 | 45074 |
| P1050 | p585-count | 246 | 226380 | 226626 |
