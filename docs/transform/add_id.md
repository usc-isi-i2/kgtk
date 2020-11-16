The add-id command copies its input file to its output file,
adding ID values where needed.

New IDs may be generated using one of several available ID generation
styles.

| ID Style | Description |
| -------- | ----------- |
| concat   | node1-label-node2 |
| concat-nlnum | Concatenates (node1, label) with a sequence number per-(node1, label) pair: node1-label-num |
| concat-with-id | node1-label-node2-id |
| prefixed | PREFIX### where PREFIX is supplied from --id-prefix and ### increments. |

By default, the ID values in the file are validated for uniqueness,
using an in-memory set.  This may cause
memory usage issues for large input files, and may be inappropriate
for some files that legitimately contain duplicate records.
The --verify-id-unique=false optin may be used to disable this check.

## Usage

```
usage: kgtk add-id [-h] [-i INPUT_FILE] [-o OUTPUT_FILE] [--old-id-column-name COLUMN_NAME]
                   [--new-id-column-name COLUMN_NAME] [--overwrite-id [optional true|false]]
                   [--verify-id-unique [optional true|false]]
                   [--id-style {node1-label-node2,node1-label-num,node1-label-node2-num,node1-label-node2-id,empty,prefix###}]
                   [--id-prefix PREFIX] [--initial-id INTEGER]
                   [--id-prefix-num-width INTEGER] [--id-concat-num-width INTEGER] [-v]

Copy a KGTK file, adding ID values.

The --overwrite-id option can be used to replace existing ID values in the ID column. It does not update instances of the same ID in other columns, such as node1, elsewhere in the file.

Several ID styles are supported. 

Additional options are shown in expert help.
kgtk --expert add-id --help

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK input file. (May be omitted or '-' for stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for stdout.)
  --old-id-column-name COLUMN_NAME
                        The name of the old ID column. (default=id).
  --new-id-column-name COLUMN_NAME
                        The name of the new ID column. (default=id).
  --overwrite-id [optional true|false]
                        When true, replace existing ID values. When false, copy existing ID
                        values. When --overwrite-id is omitted, it defaults to False. When
                        --overwrite-id is supplied without an argument, it is True.
  --verify-id-unique [optional true|false]
                        When true, verify ID uniqueness using an in-memory set of IDs. When
                        --verify-id-unique is omitted, it defaults to False. When --verify-
                        id-unique is supplied without an argument, it is True.
  --id-style {node1-label-node2,node1-label-num,node1-label-node2-num,node1-label-node2-id,empty,prefix###}
                        The ID generation style. (default=prefix###).
  --id-prefix PREFIX    The prefix for a prefix### ID. (default=E).
  --initial-id INTEGER  The initial numeric value for a prefix### ID. (default=1).
  --id-prefix-num-width INTEGER
                        The width of the numeric value for a prefix### ID. (default=1).
  --id-concat-num-width INTEGER
                        The width of the numeric value for a concatenated ID. (default=4).

  -v, --verbose         Print additional progress messages (default=False).
```

## Examples

Suppose that `file1.tsv` contains the following table in KGTK format:
(Note:  The `years` column means years employed, not age.)

| node1 | label   | node2 | location  | years |
| ----- | ------- | ----- | --------- | ----- |
| john  | zipcode | 12345 | home      | 10    |
| john  | zipcode | 12346 |           |       |
| peter | zipcode | 12040 | home      |       |
| peter | zipcode | 12040 | cabin     |       |
| peter | zipcode | 12040 | work      | 5     |
| peter | zipcode | 12040 |           | 6     |
| steve | zipcode | 45601 |           | 3     |
| steve | zipcode | 45601 |           | 4     |
| steve | zipcode | 45601 |           | 5     |
| steve | zipcode | 45601 | home      | 1     |
| steve | zipcode | 45601 | work      | 2     |
| steve | zipcode | 45601 | cabin     |       |

Add an ID column using the default ID style (prefixed):

```bash
kgtk add-id -i file1.tsv
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

Add an ID column using the node1-label-num ID style:

```bash
kgtk add-id -i file1.tsv --id-style node1-label-num
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
