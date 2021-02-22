## Overview

This command performs calculations on one or more columns in a KGTK file. 
If no input filename is provided, the default is to read standard input.

The output of a calculation can be written into an existing column or into
a new column, which will be added after all existing columns.

!!! note
    [`kgtk query`](../query) can perform the same calculations as
    `kgtk calc` in a more elegant and more general manner. 

## Usage

```
usage: kgtk calc [-h] [-i INPUT_FILE] [-o OUTPUT_FILE]
                 [-c [COLUMN_NAME [COLUMN_NAME ...]]] --into INTO_COLUMN_NAMES
                 [INTO_COLUMN_NAMES ...] --do
                 {average,capitalize,casefold,copy,join,lower,max,min,percentage,replace,set,substitute,sum,swapcase,title,upper}
                 [--values [VALUES [VALUES ...]]]
                 [--with-values [WITH_VALUES [WITH_VALUES ...]]]
                 [--limit LIMIT] [--format FORMAT_STRING]
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
  --do {average,capitalize,casefold,copy,join,lower,max,min,percentage,replace,set,substitute,sum,swapcase,title,upper}
                        The name of the operation.
  --values [VALUES [VALUES ...]]
                        An optional list of values
  --with-values [WITH_VALUES [WITH_VALUES ...]]
                        An optional list of additional values
  --limit LIMIT         A limit count.
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


### Convert the `node1` column value with capitalization.

!!! info
    Multiple columns may be converted if ther is a matching number of `--into` columns.

```bash
kgtk calc -i examples/docs/calc-file1.tsv \
          --do capitalize \
          --columns  node1 \
          --into     node1
```

The output will be the following table in KGTK format:

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

### Convert the `node1` column value with case folding.

!!! info
    Multiple columns may be converted if ther is a matching number of `--into` columns.

```bash
kgtk calc -i examples/docs/calc-file1.tsv \
          --do casefold \
          --columns  node1 \
          --into     node1
```

The output will be the following table in KGTK format:

| node1 | label | node2 | node1;total |
| -- | -- | -- | -- |
| p10 | p585-count | 73 | 3879 |
| p1000 | p585-count | 16 | 266 |
| p101 | p585-count | 5 | 157519 |
| p1018 | p585-count | 2 | 177 |
| p102 | p585-count | 295 | 414726 |
| p1025 | p585-count | 26 | 693 |
| p1026 | p585-count | 40 | 6930 |
| p1027 | p585-count | 14 | 10008 |
| p1028 | p585-count | 1131 | 4035 |
| p1029 | p585-count | 4 | 2643 |
| p1035 | p585-count | 4 | 366 |
| p1037 | p585-count | 60 | 9317 |
| p1040 | p585-count | 1 | 45073 |
| p1050 | p585-count | 246 | 226380 |

### Calculate the average of `node2` and `node1;total`.

!!! info
    `--do average` requires at least one source column (`--columns`) and one destination column (`--into`).

!!! info
    The format option (`--format`), which takes a Python %-style format string as argument,
    may be used to format the result of this calculation.

```bash
kgtk calc -i examples/docs/calc-file1.tsv \
          --do average --columns node2 "node1;total" --into result
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
kgtk calc -i examples/docs/calc-file1.tsv \
          --do copy --columns node2 --into node2-copy
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
kgtk calc -i examples/docs/calc-file1.tsv \
          --do copy \
          --columns  node2        "node1;total" \
          --into    "node1;total"  node2
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
kgtk calc -i examples/docs/calc-file1.tsv \
          --do join --columns node1 label --value : --into result
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

```bashk
kgtk calc -i examples/docs/calc-file1.tsv \
          --do join --columns node1 label --value "" --into result
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

### Convert the `node1` column value into lower case.

!!! info
    Multiple columns may be converted if ther is a matching number of `--into` columns.

```bash
kgtk calc -i examples/docs/calc-file1.tsv \
          --do lower \
          --columns  node1 \
          --into     node1
```

The output will be the following table in KGTK format:

| node1 | label | node2 | node1;total |
| -- | -- | -- | -- |
| p10 | p585-count | 73 | 3879 |
| p1000 | p585-count | 16 | 266 |
| p101 | p585-count | 5 | 157519 |
| p1018 | p585-count | 2 | 177 |
| p102 | p585-count | 295 | 414726 |
| p1025 | p585-count | 26 | 693 |
| p1026 | p585-count | 40 | 6930 |
| p1027 | p585-count | 14 | 10008 |
| p1028 | p585-count | 1131 | 4035 |
| p1029 | p585-count | 4 | 2643 |
| p1035 | p585-count | 4 | 366 |
| p1037 | p585-count | 60 | 9317 |
| p1040 | p585-count | 1 | 45073 |
| p1050 | p585-count | 246 | 226380 |

### Calculate the maximum of `node2` and `node1;total`.

!!! info
    `--do max` requires at least one source column (`--columns`) and one destination column (`--into`).

!!! info
    The format option (`--format`), which takes a Python %-style format string as argument,
    may be used to format the result of this calculation.

```bash
kgtk calc -i examples/docs/calc-file1.tsv \
          --do max --columns node2 "node1;total" --into result
```

The output will be the following table in KGTK format:

| node1 | label | node2 | node1;total | result |
| -- | -- | -- | -- | -- |
| P10 | p585-count | 73 | 3879 | 3879.00 |
| P1000 | p585-count | 16 | 266 | 266.00 |
| P101 | p585-count | 5 | 157519 | 157519.00 |
| P1018 | p585-count | 2 | 177 | 177.00 |
| P102 | p585-count | 295 | 414726 | 414726.00 |
| P1025 | p585-count | 26 | 693 | 693.00 |
| P1026 | p585-count | 40 | 6930 | 6930.00 |
| P1027 | p585-count | 14 | 10008 | 10008.00 |
| P1028 | p585-count | 1131 | 4035 | 4035.00 |
| P1029 | p585-count | 4 | 2643 | 2643.00 |
| P1035 | p585-count | 4 | 366 | 366.00 |
| P1037 | p585-count | 60 | 9317 | 9317.00 |
| P1040 | p585-count | 1 | 45073 | 45073.00 |
| P1050 | p585-count | 246 | 226380 | 226380.00 |

### Calculate the minimum of `node2` and `node1;total`.

!!! info
    `--do min` requires at least one source column (`--columns`) and one destination column (`--into`).

!!! info
    The format option (`--format`), which takes a Python %-style format string as argument,
    may be used to format the result of this calculation.

```bash
kgtk calc -i examples/docs/calc-file1.tsv \
          --do min --columns node2 "node1;total" --into result
```

The output will be the following table in KGTK format:

| node1 | label | node2 | node1;total | result |
| -- | -- | -- | -- | -- |
| P10 | p585-count | 73 | 3879 | 73.00 |
| P1000 | p585-count | 16 | 266 | 16.00 |
| P101 | p585-count | 5 | 157519 |  5.00 |
| P1018 | p585-count | 2 | 177 |  2.00 |
| P102 | p585-count | 295 | 414726 | 295.00 |
| P1025 | p585-count | 26 | 693 | 26.00 |
| P1026 | p585-count | 40 | 6930 | 40.00 |
| P1027 | p585-count | 14 | 10008 | 14.00 |
| P1028 | p585-count | 1131 | 4035 | 1131.00 |
| P1029 | p585-count | 4 | 2643 |  4.00 |
| P1035 | p585-count | 4 | 366 |  4.00 |
| P1037 | p585-count | 60 | 9317 | 60.00 |
| P1040 | p585-count | 1 | 45073 |  1.00 |
| P1050 | p585-count | 246 | 226380 | 246.00 |

### Calculate the percentage of `node2` and `node1;total`.

!!! info
    `--do percent` requires two source columns (`--columns`) and one destination column (`--into`).

!!! info
    The format option (`--format`), which takes a Python %-style format string as argument,
    may be used to format the result of this calculation.

```bash
kgtk calc -i examples/docs/calc-file1.tsv \
          --do percentage --columns node2 "node1;total" --into result
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

### Replace a String into a New Column

We want to do a string replacement, replacing a lower-case
"p" with an upper-cas "P" in the `label` column, storing the result
in the `result` column.

!!! info
    `--do replace` requires one source column (`--column`), one destination column (`--into`,
    one search value (`--value`), and one replacement value (--with-value`).  Optionally,
    it takes a limit (`--limit`) on th enumber of replacements per edge.

```bash
kgtk calc -i examples/docs/calc-file1.tsv \
          --do replace --columns label --into result \
          --value p --with P
```

The output will be the following table in KGTK format:

| node1 | label | node2 | node1;total | result |
| -- | -- | -- | -- | -- |
| P10 | p585-count | 73 | 3879 | P585-count |
| P1000 | p585-count | 16 | 266 | P585-count |
| P101 | p585-count | 5 | 157519 | P585-count |
| P1018 | p585-count | 2 | 177 | P585-count |
| P102 | p585-count | 295 | 414726 | P585-count |
| P1025 | p585-count | 26 | 693 | P585-count |
| P1026 | p585-count | 40 | 6930 | P585-count |
| P1027 | p585-count | 14 | 10008 | P585-count |
| P1028 | p585-count | 1131 | 4035 | P585-count |
| P1029 | p585-count | 4 | 2643 | P585-count |
| P1035 | p585-count | 4 | 366 | P585-count |
| P1037 | p585-count | 60 | 9317 | P585-count |
| P1040 | p585-count | 1 | 45073 | P585-count |
| P1050 | p585-count | 246 | 226380 | P585-count |

!!! note
    If you want to perform a more complex replacement operation,
    use the regular expression-based substitute command (`kgtk calc --do substitute`).

### Replace a String in Place

We want to do a string replacement, replacing a lower-case
"p" with an upper-case "P" in the label column, overwriting
the original value in the `label` column.

!!! info
    `--do replace` requires one source column (`--column`), one destination column (`--into`,
    one search value (`--value`), and one replacement value (--with-value`).  Optionally,
    it takes a limit (`--limit`) on the number of replacements per edge.

```bash
kgtk calc -i examples/docs/calc-file1.tsv \
          --do replace --columns label --into label \
          --value p --with P
```

The output will be the following table in KGTK format:

| node1 | label | node2 | node1;total |
| -- | -- | -- | -- |
| P10 | P585-count | 73 | 3879 |
| P1000 | P585-count | 16 | 266 |
| P101 | P585-count | 5 | 157519 |
| P1018 | P585-count | 2 | 177 |
| P102 | P585-count | 295 | 414726 |
| P1025 | P585-count | 26 | 693 |
| P1026 | P585-count | 40 | 6930 |
| P1027 | P585-count | 14 | 10008 |
| P1028 | P585-count | 1131 | 4035 |
| P1029 | P585-count | 4 | 2643 |
| P1035 | P585-count | 4 | 366 |
| P1037 | P585-count | 60 | 9317 |
| P1040 | P585-count | 1 | 45073 |
| P1050 | P585-count | 246 | 226380 |

!!! note
    If you want to perform a more complex replacement operation,
    use the regular expression-based substitute command (`kgtk calc --do substitute`).

### Set a value into an existing column.

!!! info
    `--do set` requires at least one `--values` argument and a matching number of destination columns (`--into`).
    It does not allow any source column (`--columns`).

```bash
kgtk calc -i examples/docs/calc-file1.tsv \
          --do set --value count --into label
```

The output will be the following table in KGTK format:

| node1 | label | node2 | node1;total |
| -- | -- | -- | -- |
| P10 | count | 73 | 3879 |
| P1000 | count | 16 | 266 |
| P101 | count | 5 | 157519 |
| P1018 | count | 2 | 177 |
| P102 | count | 295 | 414726 |
| P1025 | count | 26 | 693 |
| P1026 | count | 40 | 6930 |
| P1027 | count | 14 | 10008 |
| P1028 | count | 1131 | 4035 |
| P1029 | count | 4 | 2643 |
| P1035 | count | 4 | 366 |
| P1037 | count | 60 | 9317 |
| P1040 | count | 1 | 45073 |
| P1050 | count | 246 | 226380 |

### Set a value into a new column.

!!! info
    `--do set` requires at least one `--values` argument and a matching number of destination columns (`--into`).
    It does not allow any source column (`--columns`).

```bash
kgtk calc -i examples/docs/calc-file1.tsv \
          --do set --value xxx --into result
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

### Substitute a String in Place

We want to do a regular expression substitution, replacing a lower-case
"p" with an upper-case "P" and a dash in the label column, appending a "-x", and overwriting
the original value in the `label` column.

!!! info
    `--do substitute` requires one source column (`--column`), one destination column (`--into`,
    one search value (`--value`), and one replacement value (--with-value`).  Optionally,
    it takes a limit (`--limit`) on the number of replacements per edge.

```bash
kgtk calc -i examples/docs/calc-file1.tsv \
          --do substitute --columns label --into label \
          --value '^p(.*)$' --with 'P-\g<1>-x'
```

The output will be the following table in KGTK format:

| node1 | label | node2 | node1;total |
| -- | -- | -- | -- |
| P10 | P-585-count-x | 73 | 3879 |
| P1000 | P-585-count-x | 16 | 266 |
| P101 | P-585-count-x | 5 | 157519 |
| P1018 | P-585-count-x | 2 | 177 |
| P102 | P-585-count-x | 295 | 414726 |
| P1025 | P-585-count-x | 26 | 693 |
| P1026 | P-585-count-x | 40 | 6930 |
| P1027 | P-585-count-x | 14 | 10008 |
| P1028 | P-585-count-x | 1131 | 4035 |
| P1029 | P-585-count-x | 4 | 2643 |
| P1035 | P-585-count-x | 4 | 366 |
| P1037 | P-585-count-x | 60 | 9317 |
| P1040 | P-585-count-x | 1 | 45073 |
| P1050 | P-585-count-x | 246 | 226380 |

!!! note
    If you want to perform a simpler replacement operation,
    use the string-based replace command (`kgtk calc --do replace`).

!!! note
    Be certain to include shell escapes when needed.

!!! note
    See Python 3 documentation on regular expressions for more details
    on pattern matching and substitution.

### Calculate the sum of `node2` and `node1;total`.

!!! info
    `--do sum` requires at least one source column (`--columns`) and one destination column (`--into`).

!!! info
    The format option (`--format`), which takes a Python %-style format string as argument,
    may be used to format the result of the calculation.

```bash
kgtk calc -i examples/docs/calc-file1.tsv \
          --do sum --columns node2 "node1;total" --into result
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
kgtk calc -i examples/docs/calc-file1.tsv \
          --do sum --columns node2 "node1;total" --into result --format '%d'
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

### Convert the `node1` column value by swapping case.

!!! info
    Multiple columns may be converted if there is a matching number of `--into` columns.

```bash
kgtk calc -i examples/docs/calc-file1.tsv \
          --do swapcase \
          --columns  label \
          --into     label
```

The output will be the following table in KGTK format:

| node1 | label | node2 | node1;total |
| -- | -- | -- | -- |
| P10 | P585-COUNT | 73 | 3879 |
| P1000 | P585-COUNT | 16 | 266 |
| P101 | P585-COUNT | 5 | 157519 |
| P1018 | P585-COUNT | 2 | 177 |
| P102 | P585-COUNT | 295 | 414726 |
| P1025 | P585-COUNT | 26 | 693 |
| P1026 | P585-COUNT | 40 | 6930 |
| P1027 | P585-COUNT | 14 | 10008 |
| P1028 | P585-COUNT | 1131 | 4035 |
| P1029 | P585-COUNT | 4 | 2643 |
| P1035 | P585-COUNT | 4 | 366 |
| P1037 | P585-COUNT | 60 | 9317 |
| P1040 | P585-COUNT | 1 | 45073 |
| P1050 | P585-COUNT | 246 | 226380 |

### Convert the `node1` column value into title case.

!!! info
    Multiple columns may be converted if there is a matching number of `--into` columns.

```bash
kgtk calc -i examples/docs/calc-file1.tsv \
          --do title \
          --columns  label \
          --into     label
```

The output will be the following table in KGTK format:

| node1 | label | node2 | node1;total |
| -- | -- | -- | -- |
| P10 | P585-Count | 73 | 3879 |
| P1000 | P585-Count | 16 | 266 |
| P101 | P585-Count | 5 | 157519 |
| P1018 | P585-Count | 2 | 177 |
| P102 | P585-Count | 295 | 414726 |
| P1025 | P585-Count | 26 | 693 |
| P1026 | P585-Count | 40 | 6930 |
| P1027 | P585-Count | 14 | 10008 |
| P1028 | P585-Count | 1131 | 4035 |
| P1029 | P585-Count | 4 | 2643 |
| P1035 | P585-Count | 4 | 366 |
| P1037 | P585-Count | 60 | 9317 |
| P1040 | P585-Count | 1 | 45073 |
| P1050 | P585-Count | 246 | 226380 |

### Convert the `node1` column value into upper case.

!!! info
    Multiple columns may be converted if there is a matching number of `--into` columns.

```bash
kgtk calc -i examples/docs/calc-file1.tsv \
          --do upper \
          --columns  label \
          --into     label
```

The output will be the following table in KGTK format:

| node1 | label | node2 | node1;total |
| -- | -- | -- | -- |
| P10 | P585-COUNT | 73 | 3879 |
| P1000 | P585-COUNT | 16 | 266 |
| P101 | P585-COUNT | 5 | 157519 |
| P1018 | P585-COUNT | 2 | 177 |
| P102 | P585-COUNT | 295 | 414726 |
| P1025 | P585-COUNT | 26 | 693 |
| P1026 | P585-COUNT | 40 | 6930 |
| P1027 | P585-COUNT | 14 | 10008 |
| P1028 | P585-COUNT | 1131 | 4035 |
| P1029 | P585-COUNT | 4 | 2643 |
| P1035 | P585-COUNT | 4 | 366 |
| P1037 | P585-COUNT | 60 | 9317 |
| P1040 | P585-COUNT | 1 | 45073 |
| P1050 | P585-COUNT | 246 | 226380 |

