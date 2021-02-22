## Overview

The add-id command copies its input file to its output file,
adding an ID column and ID values when needed.

### ID Styles

New IDs may be generated using one of the following ID generation styles.

| ID Style | Description |
| -------- | ----------- |
| empty | Sets the ID column to the empty value (clears it). |
| node1-label-node2 | Concatenates the node1, label, and node2 column values. |
| node1-label-node2-id | Concatenates the node1, label, and node2 column values, then concatenate any existing non-blank ID value. |
| node1-label-node2-num | Concatenates the node1, label, and node2 column values with a sequence number per (node1, label, node2) tuple. |
| node1-label-num | Concatenates the node1 and label column values with a sequence number per-(node1, label) pair. |
| prefix### | Concatenate a prefix value (from `--id-prefix`) with an incrementing counter with leading zeros per `--id-prefix-num-width`). |
| wikidata | Concatenate the node1 and label column values with either the node2 column value (if it starts with P or Q) or the SHA256 hash of the node2 column value (truncated to the width giver by ``--value-hash-width`). |
| wikidata-with-claim-id | If the claim-id column is empty, produce an ID value as per `--id-style wikidata`, above. Otherwise, if `--claim-id-hash-width` is 0, then concatenate the value from the column named by `--claim-id-column-name` (default `claim_id`) to the `--id-style wikidata` ID value. Otherwise, concatenate a SHA256 hash of the `claim_id` column value, truncated per `--claim-id-hash-width`. | 

### Uniqueness and Memory Use

By default, the ID values in the file are validated for uniqueness using an in-memory set.  This may cause
memory usage issues for large input files, and may be inappropriate
for some files that legitimately contain duplicate records.
The `--verify-id-unique=false` option may be used to disable this check.

## Usage

```
usage: kgtk add-id [-h] [-i INPUT_FILE] [-o OUTPUT_FILE]
                   [--old-id-column-name COLUMN_NAME]
                   [--new-id-column-name COLUMN_NAME]
                   [--overwrite-id [optional true|false]]
                   [--verify-id-unique [optional true|false]]
                   [--id-style {node1-label-node2,node1-label-num,node1-label-node2-num,node1-label-node2-id,empty,prefix###,wikidata,wikidata-with-claim-id}]
                   [--id-prefix PREFIX] [--initial-id INTEGER]
                   [--id-prefix-num-width INTEGER]
                   [--id-concat-num-width INTEGER]
                   [--value-hash-width VALUE_HASH_WIDTH]
                   [--claim-id-hash-width CLAIM_ID_HASH_WIDTH]
                   [--claim-id-column-name CLAIM_ID_COLUMN_NAME]
                   [--id-separator ID_SEPARATOR] [-v [optional True|False]]

Copy a KGTK file, adding ID values.

The `--overwrite-id` option can be used to replace existing ID values in the ID column.
It does not update instances of the same ID in other columns, such as node1, elsewhere in the file.

Several ID styles are supported.

Additional options are shown in expert help.
kgtk --expert add-id --help

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK input file. (May be omitted or '-' for
                        stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for
                        stdout.)
  --old-id-column-name COLUMN_NAME
                        The name of the old ID column. (default=id).
  --new-id-column-name COLUMN_NAME
                        The name of the new ID column. (default=id).
  --overwrite-id [optional true|false]
                        When true, replace existing ID values. When false,
                        copy existing ID values. When --overwrite-id is
                        omitted, it defaults to False. When --overwrite-id is
                        supplied without an argument, it is True.
  --verify-id-unique [optional true|false]
                        When true, verify ID uniqueness using an in-memory set
                        of IDs. When --verify-id-unique is omitted, it
                        defaults to False. When --verify-id-unique is supplied
                        without an argument, it is True.
  --id-style {node1-label-node2,node1-label-num,node1-label-node2-num,node1-label-node2-id,empty,prefix###,wikidata,wikidata-with-claim-id}
                        The ID generation style. (default=prefix###).
  --id-prefix PREFIX    The prefix for a prefix### ID. (default=E).
  --initial-id INTEGER  The initial numeric value for a prefix### ID.
                        (default=1).
  --id-prefix-num-width INTEGER
                        The width of the numeric value for a prefix### ID.
                        (default=1).
  --id-concat-num-width INTEGER
                        The width of the numeric value for a concatenated ID.
                        (default=4).
  --value-hash-width VALUE_HASH_WIDTH
                        How many characters should be used in a value hash?
                        (default=6)
  --claim-id-hash-width CLAIM_ID_HASH_WIDTH
                        How many characters should be used to hash the claim
                        ID? 0 means do not hash the claim ID. (default=8)
  --claim-id-column-name CLAIM_ID_COLUMN_NAME
                        The name of the claim_id column. (default=claim_id)
  --id-separator ID_SEPARATOR
                        The separator user between ID subfields. (default=-)

  -v [optional True|False], --verbose [optional True|False]
                        Print additional progress messages (default=False).
```

## Examples

Suppose that `examples/docs/add-id-file1.tsv` contains the following table in KGTK format:

```bash
kgtk cat -i examples/docs/add-id-file1.tsv
```

| node1 | label | node2 | location | years |
| -- | -- | -- | -- | -- |
| john | zipcode | 12345 | home | 10 |
| john | zipcode | 12346 |  |  |
| peter | zipcode | 12040 | home |  |
| peter | zipcode | 12040 | cabin |  |
| peter | zipcode | 12040 | work | 5 |
| peter | zipcode | 12040 |  | 6 |
| steve | zipcode | 45601 |  | 3 |
| steve | zipcode | 45601 |  | 4 |
| steve | zipcode | 45601 |  | 5 |
| steve | zipcode | 45601 | home | 1 |
| steve | zipcode | 45601 | work | 2 |
| steve | zipcode | 45601 | cabin |  |

!!! note
    The `years` column means years employed, not age.

### Add an ID column using the default ID style (prefix###)

```bash
kgtk add-id -i examples/docs/add-id-file1.tsv
```

The output will be the following table in KGTK format:

| node1 | label | node2 | location | years | id |
| -- | -- | -- | -- | -- | -- |
| john | zipcode | 12345 | home | 10 | E1 |
| john | zipcode | 12346 |  |  | E2 |
| peter | zipcode | 12040 | home |  | E3 |
| peter | zipcode | 12040 | cabin |  | E4 |
| peter | zipcode | 12040 | work | 5 | E5 |
| peter | zipcode | 12040 |  | 6 | E6 |
| steve | zipcode | 45601 |  | 3 | E7 |
| steve | zipcode | 45601 |  | 4 | E8 |
| steve | zipcode | 45601 |  | 5 | E9 |
| steve | zipcode | 45601 | home | 1 | E10 |
| steve | zipcode | 45601 | work | 2 | E11 |
| steve | zipcode | 45601 | cabin |  | E12 |

### Add an ID column using the node1-label-node2 ID style

```bash
kgtk add-id -i examples/docs/add-id-file1.tsv --id-style node1-label-node2
```

The output will be the following table in KGTK format:

| node1 | label | node2 | location | years | id |
| -- | -- | -- | -- | -- | -- |
| john | zipcode | 12345 | home | 10 | john-zipcode-12345 |
| john | zipcode | 12346 |  |  | john-zipcode-12346 |
| peter | zipcode | 12040 | home |  | peter-zipcode-12040 |
| peter | zipcode | 12040 | cabin |  | peter-zipcode-12040 |
| peter | zipcode | 12040 | work | 5 | peter-zipcode-12040 |
| peter | zipcode | 12040 |  | 6 | peter-zipcode-12040 |
| steve | zipcode | 45601 |  | 3 | steve-zipcode-45601 |
| steve | zipcode | 45601 |  | 4 | steve-zipcode-45601 |
| steve | zipcode | 45601 |  | 5 | steve-zipcode-45601 |
| steve | zipcode | 45601 | home | 1 | steve-zipcode-45601 |
| steve | zipcode | 45601 | work | 2 | steve-zipcode-45601 |
| steve | zipcode | 45601 | cabin |  | steve-zipcode-45601 |

### Add an ID column using the node1-label-num ID style

```bash
kgtk add-id -i examples/docs/add-id-file1.tsv --id-style node1-label-num
```

The output will be the following table in KGTK format:

| node1 | label | node2 | location | years | id |
| -- | -- | -- | -- | -- | -- |
| john | zipcode | 12345 | home | 10 | john-zipcode-0000 |
| john | zipcode | 12346 |  |  | john-zipcode-0001 |
| peter | zipcode | 12040 | home |  | peter-zipcode-0000 |
| peter | zipcode | 12040 | cabin |  | peter-zipcode-0001 |
| peter | zipcode | 12040 | work | 5 | peter-zipcode-0002 |
| peter | zipcode | 12040 |  | 6 | peter-zipcode-0003 |
| steve | zipcode | 45601 |  | 3 | steve-zipcode-0000 |
| steve | zipcode | 45601 |  | 4 | steve-zipcode-0001 |
| steve | zipcode | 45601 |  | 5 | steve-zipcode-0002 |
| steve | zipcode | 45601 | home | 1 | steve-zipcode-0003 |
| steve | zipcode | 45601 | work | 2 | steve-zipcode-0004 |
| steve | zipcode | 45601 | cabin |  | steve-zipcode-0005 |

### Add an ID column building on an existing ID value using the node1-label-node2-id format

```bash
kgtk add-id -i examples/docs/add-id-file1.tsv / add-id --id-style node1-label-node2-id --overwrite-id
```

| node1 | label | node2 | location | years | id |
| -- | -- | -- | -- | -- | -- |
| john | zipcode | 12345 | home | 10 | john-zipcode-12345-E1 |
| john | zipcode | 12346 |  |  | john-zipcode-12346-E2 |
| peter | zipcode | 12040 | home |  | peter-zipcode-12040-E3 |
| peter | zipcode | 12040 | cabin |  | peter-zipcode-12040-E4 |
| peter | zipcode | 12040 | work | 5 | peter-zipcode-12040-E5 |
| peter | zipcode | 12040 |  | 6 | peter-zipcode-12040-E6 |
| steve | zipcode | 45601 |  | 3 | steve-zipcode-45601-E7 |
| steve | zipcode | 45601 |  | 4 | steve-zipcode-45601-E8 |
| steve | zipcode | 45601 |  | 5 | steve-zipcode-45601-E9 |
| steve | zipcode | 45601 | home | 1 | steve-zipcode-45601-E10 |
| steve | zipcode | 45601 | work | 2 | steve-zipcode-45601-E11 |
| steve | zipcode | 45601 | cabin |  | steve-zipcode-45601-E12 |

### Create a new ID column for the result instead of overwriting the existing ID column value

```bash
kgtk add-id -i examples/docs/add-id-file1.tsv / add-id --id-style node1-label-node2-id --new-id-column-name new-id
```

| node1 | label | node2 | location | years | id | new-id |
| -- | -- | -- | -- | -- | -- | -- |
| john | zipcode | 12345 | home | 10 | E1 | john-zipcode-12345-E1 |
| john | zipcode | 12346 |  |  | E2 | john-zipcode-12346-E2 |
| peter | zipcode | 12040 | home |  | E3 | peter-zipcode-12040-E3 |
| peter | zipcode | 12040 | cabin |  | E4 | peter-zipcode-12040-E4 |
| peter | zipcode | 12040 | work | 5 | E5 | peter-zipcode-12040-E5 |
| peter | zipcode | 12040 |  | 6 | E6 | peter-zipcode-12040-E6 |
| steve | zipcode | 45601 |  | 3 | E7 | steve-zipcode-45601-E7 |
| steve | zipcode | 45601 |  | 4 | E8 | steve-zipcode-45601-E8 |
| steve | zipcode | 45601 |  | 5 | E9 | steve-zipcode-45601-E9 |
| steve | zipcode | 45601 | home | 1 | E10 | steve-zipcode-45601-E10 |
| steve | zipcode | 45601 | work | 2 | E11 | steve-zipcode-45601-E11 |
| steve | zipcode | 45601 | cabin |  | E12 | steve-zipcode-45601-E12 |

### Add an ID column using the node1-label-node2-num ID style

```bash
kgtk add-id -i examples/docs/add-id-file1.tsv --id-style node1-label-node2-num
```

The output will be the following table in KGTK format:

| node1 | label | node2 | location | years | id |
| -- | -- | -- | -- | -- | -- |
| john | zipcode | 12345 | home | 10 | john-zipcode-12345-0000 |
| john | zipcode | 12346 |  |  | john-zipcode-12346-0000 |
| peter | zipcode | 12040 | home |  | peter-zipcode-12040-0000 |
| peter | zipcode | 12040 | cabin |  | peter-zipcode-12040-0001 |
| peter | zipcode | 12040 | work | 5 | peter-zipcode-12040-0002 |
| peter | zipcode | 12040 |  | 6 | peter-zipcode-12040-0003 |
| steve | zipcode | 45601 |  | 3 | steve-zipcode-45601-0000 |
| steve | zipcode | 45601 |  | 4 | steve-zipcode-45601-0001 |
| steve | zipcode | 45601 |  | 5 | steve-zipcode-45601-0002 |
| steve | zipcode | 45601 | home | 1 | steve-zipcode-45601-0003 |
| steve | zipcode | 45601 | work | 2 | steve-zipcode-45601-0004 |
| steve | zipcode | 45601 | cabin |  | steve-zipcode-45601-0005 |

### Add an ID column using the node1-label-num ID style

```bash
kgtk add-id -i examples/docs/add-id-file1.tsv --id-style node1-label-num
```

The output will be the following table in KGTK format:

| node1 | label | node2 | location | years | id |
| -- | -- | -- | -- | -- | -- |
| john | zipcode | 12345 | home | 10 | john-zipcode-0000 |
| john | zipcode | 12346 |  |  | john-zipcode-0001 |
| peter | zipcode | 12040 | home |  | peter-zipcode-0000 |
| peter | zipcode | 12040 | cabin |  | peter-zipcode-0001 |
| peter | zipcode | 12040 | work | 5 | peter-zipcode-0002 |
| peter | zipcode | 12040 |  | 6 | peter-zipcode-0003 |
| steve | zipcode | 45601 |  | 3 | steve-zipcode-0000 |
| steve | zipcode | 45601 |  | 4 | steve-zipcode-0001 |
| steve | zipcode | 45601 |  | 5 | steve-zipcode-0002 |
| steve | zipcode | 45601 | home | 1 | steve-zipcode-0003 |
| steve | zipcode | 45601 | work | 2 | steve-zipcode-0004 |
| steve | zipcode | 45601 | cabin |  | steve-zipcode-0005 |

### Add an ID column using the wikidata ID style

```bash
kgtk add-id -i examples/docs/add-id-file1.tsv --id-style wikidata
```

The output will be the following table in KGTK format:

| node1 | label | node2 | location | years | id |
| -- | -- | -- | -- | -- | -- |
| john | zipcode | 12345 | home | 10 | john-zipcode-599447 |
| john | zipcode | 12346 |  |  | john-zipcode-34d128 |
| peter | zipcode | 12040 | home |  | peter-zipcode-a5ceb2 |
| peter | zipcode | 12040 | cabin |  | peter-zipcode-a5ceb2 |
| peter | zipcode | 12040 | work | 5 | peter-zipcode-a5ceb2 |
| peter | zipcode | 12040 |  | 6 | peter-zipcode-a5ceb2 |
| steve | zipcode | 45601 |  | 3 | steve-zipcode-3f5bb8 |
| steve | zipcode | 45601 |  | 4 | steve-zipcode-3f5bb8 |
| steve | zipcode | 45601 |  | 5 | steve-zipcode-3f5bb8 |
| steve | zipcode | 45601 | home | 1 | steve-zipcode-3f5bb8 |
| steve | zipcode | 45601 | work | 2 | steve-zipcode-3f5bb8 |
| steve | zipcode | 45601 | cabin |  | steve-zipcode-3f5bb8 |

!!! note
   The existing test dataset doesn't have any entries with node2 values starting with P or Q,
   so this example doesn't  doesn't illustrate the full range of IDs generated inthis style.

### Add an ID column using the wikidata-with-claim-id ID style, using the location column as a placeholder for the claim-id column

```bash
kgtk add-id -i examples/docs/add-id-file1.tsv --id-style wikidata-with-claim-id --claim-id-column-name location
```

The output will be the following table in KGTK format:

| node1 | label | node2 | location | years | id |
| -- | -- | -- | -- | -- | -- |
| john | zipcode | 12345 | home | 10 | john-zipcode-599447-4ea14058 |
| john | zipcode | 12346 |  |  | john-zipcode-34d128 |
| peter | zipcode | 12040 | home |  | peter-zipcode-a5ceb2-4ea14058 |
| peter | zipcode | 12040 | cabin |  | peter-zipcode-a5ceb2-2764182d |
| peter | zipcode | 12040 | work | 5 | peter-zipcode-a5ceb2-00e13ed7 |
| peter | zipcode | 12040 |  | 6 | peter-zipcode-a5ceb2 |
| steve | zipcode | 45601 |  | 3 | steve-zipcode-3f5bb8 |
| steve | zipcode | 45601 |  | 4 | steve-zipcode-3f5bb8 |
| steve | zipcode | 45601 |  | 5 | steve-zipcode-3f5bb8 |
| steve | zipcode | 45601 | home | 1 | steve-zipcode-3f5bb8-4ea14058 |
| steve | zipcode | 45601 | work | 2 | steve-zipcode-3f5bb8-00e13ed7 |
| steve | zipcode | 45601 | cabin |  | steve-zipcode-3f5bb8-2764182d |


### Add an ID column using Colon (`:`) as an ID Separator

We will add an ID column using the node1-label-node2-num ID
stype, but with colon (`:`) as the ID separator.

```bash
kgtk add-id -i examples/docs/add-id-file1.tsv \
            --id-style node1-label-node2-num \
            --id-separator ":"
```

The output will be the following table in KGTK format:

| node1 | label | node2 | location | years | id |
| -- | -- | -- | -- | -- | -- |
| john | zipcode | 12345 | home | 10 | john:zipcode:12345:0000 |
| john | zipcode | 12346 |  |  | john:zipcode:12346:0000 |
| peter | zipcode | 12040 | home |  | peter:zipcode:12040:0000 |
| peter | zipcode | 12040 | cabin |  | peter:zipcode:12040:0001 |
| peter | zipcode | 12040 | work | 5 | peter:zipcode:12040:0002 |
| peter | zipcode | 12040 |  | 6 | peter:zipcode:12040:0003 |
| steve | zipcode | 45601 |  | 3 | steve:zipcode:45601:0000 |
| steve | zipcode | 45601 |  | 4 | steve:zipcode:45601:0001 |
| steve | zipcode | 45601 |  | 5 | steve:zipcode:45601:0002 |
| steve | zipcode | 45601 | home | 1 | steve:zipcode:45601:0003 |
| steve | zipcode | 45601 | work | 2 | steve:zipcode:45601:0004 |
| steve | zipcode | 45601 | cabin |  | steve:zipcode:45601:0005 |

### Expert Topic: Converting a CSV File to a KGTK TSV File

The expert option `--input-format csv` may be used to read an
input file in CSV (comma-separated values) format.  The expert
option `--mode=NONE` will also be needed if the input file
does not have the required columns of a KGTK edge or node file.

In this example, we will read a CSV input file, adding an `id` column and
writing the result to standard output as a KGTK node file.

```bash
kgtk add-id -i examples/docs/periodic_table_of_elements_1-18.csv \
         --input-format csv --mode=NONE
```

The result will be the following table in KGTK format:

| AtomicNumber | Element | Symbol | AtomicMass | NumberofNeutrons | NumberofProtons | NumberofElectrons | Period | Group | Phase | Radioactive | Natural | Metal | Nonmetal | Metalloid | Type | AtomicRadius | Electronegativity | FirstIonization | Density | MeltingPoint | BoilingPoint | NumberOfIsotopes | Discoverer | Year | SpecificHeat | NumberofShells | NumberofValence | id |
| -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- |
| 1 | Hydrogen | H | 1.007 | 0 | 1 | 1 | 1 | 1 | gas |  | yes |  | yes |  | Nonmetal | 0.79 | 2.2 | 13.5984 | 8.99E-05 | 14.175 | 20.28 | 3 | Cavendish | 1766 | 14.304 | 1 | 1 | E1 |
| 2 | Helium | He | 4.002 | 2 | 2 | 2 | 1 | 18 | gas |  | yes |  | yes |  | NobleGas | 0.49 |  | 24.5874 | 1.79E-04 |  | 4.22 | 5 | Janssen | 1868 | 5.193 | 1 |  | E2 |
| 3 | Lithium | Li | 6.941 | 4 | 3 | 3 | 2 | 1 | solid |  | yes | yes |  |  | AlkaliMetal | 2.1 | 0.98 | 5.3917 | 5.34E-01 | 453.85 | 1615 | 5 | Arfvedson | 1817 | 3.582 | 2 | 1 | E3 |
| 4 | Beryllium | Be | 9.012 | 5 | 4 | 4 | 2 | 2 | solid |  | yes | yes |  |  | AlkalineEarthMetal | 1.4 | 1.57 | 9.3227 | 1.85E+00 | 1560.15 | 2742 | 6 | Vaulquelin | 1798 | 1.825 | 2 | 2 | E4 |
| 5 | Boron | B | 10.811 | 6 | 5 | 5 | 2 | 13 | solid |  | yes |  |  | yes | Metalloid | 1.2 | 2.04 | 8.298 | 2.34E+00 | 2573.15 | 4200 | 6 | Gay-Lussac | 1808 | 1.026 | 2 | 3 | E5 |
| 6 | Carbon | C | 12.011 | 6 | 6 | 6 | 2 | 14 | solid |  | yes |  | yes |  | Nonmetal | 0.91 | 2.55 | 11.2603 | 2.27E+00 | 3948.15 | 4300 | 7 | Prehistoric |  | 0.709 | 2 | 4 | E6 |
| 7 | Nitrogen | N | 14.007 | 7 | 7 | 7 | 2 | 15 | gas |  | yes |  | yes |  | Nonmetal | 0.75 | 3.04 | 14.5341 | 1.25E-03 | 63.29 | 77.36 | 8 | Rutherford | 1772 | 1.04 | 2 | 5 | E7 |
| 8 | Oxygen | O | 15.999 | 8 | 8 | 8 | 2 | 16 | gas |  | yes |  | yes |  | Nonmetal | 0.65 | 3.44 | 13.6181 | 1.43E-03 | 50.5 | 90.2 | 8 | Priestley\|Scheele | 1774 | 0.918 | 2 | 6 | E8 |
| 9 | Fluorine | F | 18.998 | 10 | 9 | 9 | 2 | 17 | gas |  | yes |  | yes |  | Halogen | 0.57 | 3.98 | 17.4228 | 1.70E-03 | 53.63 | 85.03 | 6 | Moissan | 1886 | 0.824 | 2 | 7 | E9 |
| 10 | Neon | Ne | 20.18 | 10 | 10 | 10 | 2 | 18 | gas |  | yes |  | yes |  | Noble Gas | 0.51 |  | 21.5645 | 9.00E-04 | 24.703 | 27.07 | 8 | Ramsay_and_Travers | 1898 | 1.03 | 2 | 8 | E10 |
| 11 | Sodium | Na | 22.99 | 12 | 11 | 11 | 3 | 1 | solid |  | yes | yes |  |  | AlkaliMetal | 2.2 | 0.93 | 5.1391 | 9.71E-01 | 371.15 | 1156 | 7 | Davy | 1807 | 1.228 | 3 | 1 | E11 |
| 12 | Magnesium | Mg | 24.305 | 12 | 12 | 12 | 3 | 2 | solid |  | yes | yes |  |  | AlkalineEarthMetal | 1.7 | 1.31 | 7.6462 | 1.74E+00 | 923.15 | 1363 | 8 | Black | 1755 | 1.023 | 3 | 2 | E12 |
| 13 | Aluminum | Al | 26.982 | 14 | 13 | 13 | 3 | 13 | solid |  | yes | yes |  |  | Metal | 1.8 | 1.61 | 5.9858 | 2.70E+00 | 933.4 | 2792 | 8 | Wshler | 1827 | 0.897 | 3 | 3 | E13 |
| 14 | Silicon | Si | 28.086 | 14 | 14 | 14 | 3 | 14 | solid |  | yes |  |  | yes | Metalloid | 1.5 | 1.9 | 8.1517 | 2.33E+00 | 1683.15 | 3538 | 8 | Berzelius | 1824 | 0.705 | 3 | 4 | E14 |
| 15 | Phosphorus | P | 30.974 | 16 | 15 | 15 | 3 | 15 | solid |  | yes |  | yes |  | Nonmetal | 1.2 | 2.19 | 10.4867 | 1.82E+00 | 317.25 | 553 | 7 | BranBrand | 1669 | 0.769 | 3 | 5 | E15 |
| 16 | Sulfur | S | 32.065 | 16 | 16 | 16 | 3 | 16 | solid |  | yes |  | yes |  | Nonmetal | 1.1 | 2.58 | 10.36 | 2.07E+00 | 388.51 | 717.8 | 10 | Prehistoric |  | 0.71 | 3 | 6 | E16 |
| 17 | Chlorine | Cl | 35.453 | 18 | 17 | 17 | 3 | 17 | gas |  | yes |  | yes |  | Halogen | 0.97 | 3.16 | 12.9676 | 3.21E-03 | 172.31 | 239.11 | 11 | Scheele | 1774 | 0.479 | 3 | 7 | E17 |
| 18 | Argon | Ar | 39.948 | 22 | 18 | 18 | 3 | 18 | gas |  | yes |  | yes |  | NobleGas | 0.88 |  | 15.7596 | 1.78E-03 | 83.96 | 87.3 | 8 | Rayleigh_and_Ramsay | 1894 | 0.52 | 3 | 8 | E18 |
