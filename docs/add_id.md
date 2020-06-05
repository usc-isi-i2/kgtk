The add_id command copies its input file to its output file,
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
usage: kgtk add_id [-h] [-o OUTPUT_KGTK_FILE] [--id-column-name ID_COLUMN_NAME]
                   [--overwrite-id [OVERWRITE_ID]]
                   [--verify-id-unique [VERIFY_ID_UNIQUE]]
                   [--id-style {concat,concat-nlnum,concat-with-id,prefixed}]
                   [--id-prefix ID_PREFIX] [--initial-id INITIAL_ID] [-v]
                   [input_kgtk_file]

Copy a KGTK file, adding ID values.

The --overwrite-id option can be used to replace existing ID values in the ID column. It does not update instances of the same ID in other columns, such as node1, elsewhere in the file.

Several ID styles are supported. 

Additional options are shown in expert help.
kgtk --expert compact --help

positional arguments:
  input_kgtk_file       The KGTK file to filter. May be omitted or '-' for stdin
                        (default=-).

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_KGTK_FILE, --output-file OUTPUT_KGTK_FILE
                        The KGTK file to write (default=-).
  --id-column-name ID_COLUMN_NAME
                        The name of the id column. (default=id).
  --overwrite-id [OVERWRITE_ID]
                        Replace existing id values. (default=False).
  --verify-id-unique [VERIFY_ID_UNIQUE]
                        Verify ID uniqueness. Uses an in-memory set of IDs.
                        (default=True).
  --id-style {concat,concat-nlnum,concat-with-id,prefixed}
                        The id style. (default=prefixed).
  --id-prefix ID_PREFIX
                        The prefix for a prefix/number id. (default=E).
  --initial-id INITIAL_ID
                        The initial value for a prefix/number id. (default=1).

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

Add an ID column using the default ID style (prefixed)

```bash
kgtk add_id file1.tsv
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
