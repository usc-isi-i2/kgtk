The implode command copies its input file to its output file, building one
column (normally node2) from separate columns for each structured subfield.

By default, all KGTK data types are candidates to be build.  The --types option allows the
user to specify the set of data types to build.  Each data type is built from
one or more columns.  Some columns, such as text, are shared between
data types (e.g., string and language qualified string).  Some columns are optional,
and need not be present in the data.

By default, KGKT quantities man include KGTK numbers, and KGTK strings may include
KGTK language qualified strings.

## Usage
```
usage: kgtk implode [-h] [-i INPUT_FILE] [-o OUTPUT_FILE]
                    [--reject-file REJECT_FILE] [--column COLUMN_NAME]
                    [--prefix PREFIX]
                    [--types [{empty,list,number,quantity,string,language_qualified_string,location_coordinates,date_and_times,extension,boolean,symbol} [{empty,list,number,quantity,string,language_qualified_string,location_coordinates,date_and_times,extension,boolean,symbol} ...]]]
                    [--without [{language_suffix,low_tolerance,high_tolerance,si_units,units_node,precision} [{language_suffix,low_tolerance,high_tolerance,si_units,units_node,precision} ...]]]
                    [--overwrite [OVERWRITE_COLUMN]] [--validate [VALIDATE]]
                    [--escape-pipes [ESCAPE_PIPES]]
                    [--quantities-include-numbers [QUANTITIES_INCLUDE_NUMBERS]]
                    [--general-strings [GENERAL_STRINGS]]
                    [--remove-prefixed-columns [REMOVE_PREFIXED_COLUMNS]]
                    [--ignore-unselected-types [IGNORE_UNSELECTED_TYPES]]
                    [--retain-unselected-types [RETAIN_UNSELECTED_TYPES]]
                    [--build-id [BUILD_ID]]
                    [--show-data-types [SHOW_DATA_TYPES]] [--quiet [QUIET]]
                    [--overwrite-id [optional true|false]]
                    [--verify-id-unique [optional true|false]]
                    [--value-hash-width VALUE_HASH_WIDTH]
                    [--claim-id-hash-width CLAIM_ID_HASH_WIDTH]
                    [--claim-id-column-name CLAIM_ID_COLUMN_NAME]
                    [--id-separator ID_SEPARATOR] [-v [optional True|False]]

Copy a KGTK file, building one column (usually node2) from seperate columns for each subfield. 

Strings may include language qualified strings, and quantities may include numbers. 

Date and times subfields and symbol subfields may be optionally quoted. Triple quotes may be used where quotes are accepted. 

Additional options are shown in expert help.
kgtk --expert implode --help

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK input file. (May be omitted or '-' for
                        stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for
                        stdout.)
  --reject-file REJECT_FILE
                        The KGTK file for records that are rejected.
                        (Optional, use '-' for stdout.)
  --column COLUMN_NAME  The name of the column to explode. (default=node2).
  --prefix PREFIX       The prefix for exploded column names.
                        (default=node2;kgtk:).
  --types [{empty,list,number,quantity,string,language_qualified_string,location_coordinates,date_and_times,extension,boolean,symbol} [{empty,list,number,quantity,string,language_qualified_string,location_coordinates,date_and_times,extension,boolean,symbol} ...]]
                        The KGTK data types for which fields should be
                        imploded. (default=['empty', 'list', 'number',
                        'quantity', 'string', 'language_qualified_string',
                        'location_coordinates', 'date_and_times', 'extension',
                        'boolean', 'symbol']).
  --without [{language_suffix,low_tolerance,high_tolerance,si_units,units_node,precision} [{language_suffix,low_tolerance,high_tolerance,si_units,units_node,precision} ...]]
                        The KGTK fields to do without. (default=None).
  --overwrite [OVERWRITE_COLUMN]
                        Indicate that it is OK to overwrite an existing
                        imploded column. (default=True).
  --validate [VALIDATE]
                        Validate imploded values. (default=True).
  --escape-pipes [ESCAPE_PIPES]
                        When true, pipe characters (|) need to be escaped (\|)
                        per KGTK file format. (default=False).
  --quantities-include-numbers [QUANTITIES_INCLUDE_NUMBERS]
                        When true, numbers are acceptable quantities.
                        (default=True).
  --general-strings [GENERAL_STRINGS]
                        When true, strings may include language qualified
                        strings. (default=True).
  --remove-prefixed-columns [REMOVE_PREFIXED_COLUMNS]
                        When true, remove all columns beginning with the
                        prefix from the output file. (default=False).
  --ignore-unselected-types [IGNORE_UNSELECTED_TYPES]
                        When true, input records with valid but unselected
                        data types will be passed through to output.
                        (default=True).
  --retain-unselected-types [RETAIN_UNSELECTED_TYPES]
                        When true, input records with valid but unselected
                        data types will be retain existing data on output.
                        (default=True).
  --build-id [BUILD_ID]
                        Build id values in an id column. (default=False).
  --show-data-types [SHOW_DATA_TYPES]
                        Print the list of data types and exit.
                        (default=False).
  --quiet [QUIET]       When true, suppress certain complaints unless verbose.
                        (default=False).
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

## Additional usage notes

### `--reject-file REJECT_KGTK_FILE`

When a reject file is provided, input records with invalid data will be
copied to the reject file instead of the output file.

Records can be rejected for the following general reasons:

 * missing or unrecognized value in the `data_type` column
 * missing data in a column that is required for the data type
 * missing data in a column that is optional for the data type, when at least one optional value must be supplied
 * poorly formatted data in a column that is used to build the data type

### `--types [TYPE_LIST]`

Normally, `kgtk implode` will process all KGTK data types, and will expect all
of the required exploded columns to be present in the KGTK file.

By specifying `--types TYPE_LIST`, which TYPE_LIST is a space-separated list
of KGTK type names, the user can tell `kgtk implode` to expect only the listed
data types when processing the input file.  Only the required columns for the
selected data types must appear in the input KGTK file; optional columns may
be excluded with the `--without COLUMN_LIST` option.

See the table of KGTK Data Types and Columns for more details.

### `--without [COLUMN_LIST]`

The KGTK data types proessed by `kgtk implode` may have optional columns of
exploded data.  These columns may be excluded by wpecifying them in the
`--without [COLUMN_LIST]` option, e.g. if the input file does not contain
the `precision` column used to build quantities:

```
kgtk implode --without precision
```
See the table of KGTK Data Types and Columns for more details.

### `--escape-pipes`

KGTK File Format allows lists of values in all columns except `node1`, `label`, and
`node2` in a KGTK edge file.  Lists are valid KGTK values separated by thevertical
bar (pipe) character(|).  Any vertical bar (pipe) characters inside a KGTK value
myse be escaped by backslash (\), i.e. "\|".  These may appear in the following
KGTK data types:

 * strings
 * language qualified strings
 * symbols

Note: in C/C++, "\|" in a string literal is equivalent to "|".  In Python,
it is process unchanged ("\|").

`kgtk implode` is intended to assist with importing data to KGTK format.  It
does not import list values from exploded columns.  If you specify
`--escape-pipes` (`--escape-pipes True, not the default value), then it `kgtk
implode` will escape any vertical bar (pipe) characters it finds inside
strings, language qualified strings, or symbols.

### `--ignore-unselected-types` and `--retain-unselected-types`

Unrecognized data type names will generate an error.  The input record will be
rejected if a reject file is available.

When a data type that is recognized but unselected appears in the input record,
the following will happen:

 * When `--retain-unselected-types` (`--retain-unselected-types True, the default
   value) is specified and the destination column exists in
   the input file, then the record will be passed through to the output
   file with its exisiting value in the destination column.

 * Else, when `--ignore-unselected-types` (`--ignore-unselected-types True`, the
   default value) is specified, then the record will be passed through to
   the output file with an empty value in the destination column.

 * Else, an error has taken place. The input record will be sent to the reject
   file if a reject file is available, otherwise the input record will be passed
   through to the output file with an empty value in the destination column.

### `--quantities-include-numbers`

When `--quantities-include-numbers` (`--quantities-include-numbers True`, the
default setting) is specified, if `quantity` is specified in the `data_type`
column (normally `node2;kgtk:data_type`) but none of the optional fields for
quantity are present, a KGTK number will be built in the destination column
(normally `node2`).  When `--quantities-include-numbers False` is specified, a
`quantity` will be built and at least one of the optional fields must be
present for the quantity to be considered valid.

### `--general-strings`

When `--general-strings` (`--general-strings True`, the default setting) is
specified, if `string` is specified in the `data_type` column and a `language`
value appears, then a language_qualified-string will be built in the
destination column.  When `--general-strings False` is specified and `string`
is specified in the `data_type` column, then the `language` column will be
ignored and only a `string` value will be built.

### `--validate`

When `--validate` (`--validate True`, the default setting) is specified,
then values built for the destination column (normally `node2`) will be validated.
When `--validate False` is specified, then values will not be validated after
they are built.  Skipping the validation step will lead to faster execution,
but will allow potentially invalid values to appear in the output KGTK file.


## KGTK Data Types and Exploded Columns

This table shows the exploded columns (without the prefix value, normally `node2;kgtk:`) that are used for each KGTK data type.

| Data Type                 | Required Columns | Optional Columns |
| ------------------------- | --------------- | --------------- |
| boolean                   | truth           |                 |
| date_and_times            | date_and_time   | precision       |
| empty                     |                 |                 |
| extension                 |                 |                 |
| language_qualified_string | text language   | language_suffix |
| list                      |                 |                 |
| location_coordinates      | latitude longitude |              |
| number                    | number          |                 |
| quantity                  | number          | low_tolerance* high_tolerance* si_units* units_node* |
| string                    | text            |                 |
| symbol                    | symbol          |                 |

Data types may have required columns and optional columns.  If an optional
column is listed in the `--without` list (which by default is empty), then it
will not be used to to build KGTK values and need not be present in the KGTK
file.

The `extension` and `list` KGTK data types cannot be built by `kgtk implode`.

## String Wrappers in Exploded Columns

Except for the `text` column, all of values in the the exploded columns may be
optionally wrapped as quoted strings in one of the following formats:

 * triple double quotes
 * triple single quotes
 * double quotes
 * single quotes

We do *not* attempt to remove backslash escape characters (\) from the body of
the value when unwrapping the string: backslash escape characters should not
appear in numbers or date-and-times, and are discouraged in symbols.

We do *not* attempt to undouble internal quotes from the body of the value
whtn unwrapping the string: internal single or double quotes should not appear
in numbers or date-and-times, and are discouraged in symbols.

## Examples

Suppose that `file2.tsv` contains the following table in KGTK format:

| node1 | label | old_node2 | node2;kgtk:data_type | node2;kgtk:valid | node2;kgtk:list_len | node2;kgtk:number | node2;kgtk:low_tolerance | node2;kgtk:high_tolerance | node2;kgtk:si_units | node2;kgtk:units_node | node2;kgtk:text | node2;kgtk:language | node2;kgtk:language_suffix | node2;kgtk:latitude | node2;kgtk:longitude | node2;kgtk:date_and_time | node2;kgtk:precision | node2;kgtk:truth | node2;kgtk:symbol |
| -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- |
| john | string | "John" | string | True | 0 |  |  |  |  |  | "John" |  |  |  |  |  |  |  |  |
| john | lqstring | 'John'@en | language_qualified_string | True | 0 |  |  |  |  |  | "John" | en |  |  |  |  |  |  |  |
| john | integer | 12345 | number | True | 0 | 12345 |  |  |  |  |  |  |  |  |  |  |  |  |  |
| john | number | 186.2 | number | True | 0 | 186.2 |  |  |  |  |  |  |  |  |  |  |  |  |  |
| john | number | 186.2e04 | number | True | 0 | 1862000.0 |  |  |  |  |  |  |  |  |  |  |  |  |  |
| john | number | -186.2 | number | True | 0 | -186.2 |  |  |  |  |  |  |  |  |  |  |  |  |  |
| john | number | +186.2e-6 | number | True | 0 | 0.0001862 |  |  |  |  |  |  |  |  |  |  |  |  |  |
| john | quantity | 84.3[84,85]kg | quantity | True | 0 | 84.3 | 84.0 | 85.0 | kg |  |  |  |  |  |  |  |  |  |  |
| john | date_and_time | ^1960-11-05T00:00 | date_and_times | True | 0 |  |  |  |  |  |  |  |  |  |  | "1960-11-05T00:00" |  |  |  |
| john | date_and_time | ^1980-11-05T00:00Z/6 | date_and_times | True | 0 |  |  |  |  |  |  |  |  |  |  | "1980-11-05T00:00Z" | 6 |  |  |
| john | location | @60.2/134.3 | location_coordinates | True | 0 |  |  |  |  |  |  |  |  | 60.2 | 134.3 |  |  |  |  |
| john | boolean | True | boolean | True | 0 |  |  |  |  |  |  |  |  |  |  |  |  | True |  |
| john | symbol | quadrature | symbol | True | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  | quadrature |
| john | symbol-string | quadrature | symbol | True | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  | "quadrature" |
| john | symbol-with-raw-pipe | quadr\\|ature | symbol | True | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  | quadr\|ature |
| john | symbol-with-escaped-pipe | quadr\\|ature | symbol | True | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  | quadr\\|ature |
| john | list | home\|work | list | True | 2 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| john | string-with-tab | "Jo\thn" | string | True | 0 |  |  |  |  |  | "Jo\thn" |  |  |  |  |  |  |  |  |
| john | string-with-raw-pipe | "Jo\\|hn" | string | True | 0 |  |  |  |  |  | "Jo\|hn" |  |  |  |  |  |  |  |  |
| john | string-with-escaped-pipe | "Jo\\|hn" | string | True | 0 |  |  |  |  |  | "Jo\\|hn" |  |  |  |  |  |  |  |  |
| john | string-with-escaped-quote | "Jo\"hn" | string | True | 0 |  |  |  |  |  | "Jo\"hn" |  |  |  |  |  |  |  |  |
| john | string-with-escaped-prime | "Jo\'hn" | string | True | 0 |  |  |  |  |  | "Jo\'hn" |  |  |  |  |  |  |  |  |
| john | lqstring-with-tab | 'Joh\tn'@en | language_qualified_string | True | 0 |  |  |  |  |  | "Joh\tn" | en |  |  |  |  |  |  |  |
| john | lqstring-with-raw-pipe | 'Joh\\|n'@en | language_qualified_string | True | 0 |  |  |  |  |  | "Joh\|n" | en |  |  |  |  |  |  |  |
| john | lqstring-with-escaped-pipe | 'Joh\\|n'@en | language_qualified_string | True | 0 |  |  |  |  |  | "Joh\\|n" | en |  |  |  |  |  |  |  |
| john | lqstring-with-escaped-quote | 'Joh\"n'@en | language_qualified_string | True | 0 |  |  |  |  |  | "Joh\"n" | en |  |  |  |  |  |  |  |
| john | lqstring-with-escaped-prime | 'Joh\'n'@en | language_qualified_string | True | 0 |  |  |  |  |  | "Joh\'n" | en |  |  |  |  |  |  |  |
| john | lqstring-with-escaped-prime-and-quote | 'Joh\'\"n'@en | language_qualified_string | True | 0 |  |  |  |  |  | "Joh\'\"n" | en |  |  |  |  |  |  |  |
| john | lqstring-with-triple-double-quotes | 'John'@en | language_qualified_string | True | 0 |  |  |  |  |  | """John""" | en |  |  |  |  |  |  |  |

```bash
kgtk explode -i file2.tsv --mode=NONE
```
The output will be the following table in KGTK format:

| node1 | label | old_node2 | node2;kgtk:data_type | node2;kgtk:valid | node2;kgtk:list_len | node2;kgtk:number | node2;kgtk:low_tolerance | node2;kgtk:high_tolerance | node2;kgtk:si_units | node2;kgtk:units_node | node2;kgtk:text | node2;kgtk:language | node2;kgtk:language_suffix | node2;kgtk:latitude | node2;kgtk:longitude | node2;kgtk:date_and_time | node2;kgtk:precision | node2;kgtk:truth | node2;kgtk:symbol | node2 |
| -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- |
| john | string | "John" | string | True | 0 |  |  |  |  |  | "John" |  |  |  |  |  |  |  |  | "John" |
| john | lqstring | 'John'@en | language_qualified_string | True | 0 |  |  |  |  |  | "John" | en |  |  |  |  |  |  |  | 'John'@en |
| john | integer | 12345 | number | True | 0 | 12345 |  |  |  |  |  |  |  |  |  |  |  |  |  | 12345 |
| john | number | 186.2 | number | True | 0 | 186.2 |  |  |  |  |  |  |  |  |  |  |  |  |  | 186.2 |
| john | number | 186.2e04 | number | True | 0 | 1862000.0 |  |  |  |  |  |  |  |  |  |  |  |  |  | 1862000.0 |
| john | number | -186.2 | number | True | 0 | -186.2 |  |  |  |  |  |  |  |  |  |  |  |  |  | -186.2 |
| john | number | +186.2e-6 | number | True | 0 | 0.0001862 |  |  |  |  |  |  |  |  |  |  |  |  |  | 0.0001862 |
| john | quantity | 84.3[84,85]kg | quantity | True | 0 | 84.3 | 84.0 | 85.0 | kg |  |  |  |  |  |  |  |  |  |  | 84.3[84.0,85.0]kg |
| john | date_and_time | ^1960-11-05T00:00 | date_and_times | True | 0 |  |  |  |  |  |  |  |  |  |  | "1960-11-05T00:00" |  |  |  | ^1960-11-05T00:00 |
| john | date_and_time | ^1980-11-05T00:00Z/6 | date_and_times | True | 0 |  |  |  |  |  |  |  |  |  |  | "1980-11-05T00:00Z" | 6 |  |  | ^1980-11-05T00:00Z/6 |
| john | location | @60.2/134.3 | location_coordinates | True | 0 |  |  |  |  |  |  |  |  | 60.2 | 134.3 |  |  |  |  | @60.2/134.3 |
| john | boolean | True | boolean | True | 0 |  |  |  |  |  |  |  |  |  |  |  |  | True |  | True |
| john | symbol | quadrature | symbol | True | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  | quadrature | quadrature |
| john | symbol-string | quadrature | symbol | True | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  | "quadrature" | quadrature |
| john | symbol-with-raw-pipe | quadr\\|ature | symbol | True | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  | quadr\|ature | quadr\|ature |
| john | symbol-with-escaped-pipe | quadr\\|ature | symbol | True | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  | quadr\\|ature | quadr\\|ature |
| john | list | home\|work | list | True | 2 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| john | string-with-tab | "Jo\thn" | string | True | 0 |  |  |  |  |  | "Jo\thn" |  |  |  |  |  |  |  |  | "Jo\thn" |
| john | string-with-raw-pipe | "Jo\\|hn" | string | True | 0 |  |  |  |  |  | "Jo\|hn" |  |  |  |  |  |  |  |  | "Jo\\|hn" |
| john | string-with-escaped-pipe | "Jo\\|hn" | string | True | 0 |  |  |  |  |  | "Jo\\|hn" |  |  |  |  |  |  |  |  | "Jo\\|hn" |
| john | string-with-escaped-quote | "Jo\"hn" | string | True | 0 |  |  |  |  |  | "Jo\"hn" |  |  |  |  |  |  |  |  | "Jo\"hn" |
| john | string-with-escaped-prime | "Jo\'hn" | string | True | 0 |  |  |  |  |  | "Jo\'hn" |  |  |  |  |  |  |  |  | "Jo\'hn" |
| john | lqstring-with-tab | 'Joh\tn'@en | language_qualified_string | True | 0 |  |  |  |  |  | "Joh\tn" | en |  |  |  |  |  |  |  | 'Joh\tn'@en |
| john | lqstring-with-raw-pipe | 'Joh\\|n'@en | language_qualified_string | True | 0 |  |  |  |  |  | "Joh\|n" | en |  |  |  |  |  |  |  | 'Joh\\|n'@en |
| john | lqstring-with-escaped-pipe | 'Joh\\|n'@en | language_qualified_string | True | 0 |  |  |  |  |  | "Joh\\|n" | en |  |  |  |  |  |  |  | 'Joh\\|n'@en |
| john | lqstring-with-escaped-quote | 'Joh\"n'@en | language_qualified_string | True | 0 |  |  |  |  |  | "Joh\"n" | en |  |  |  |  |  |  |  | 'Joh\"n'@en |
| john | lqstring-with-escaped-prime | 'Joh\'n'@en | language_qualified_string | True | 0 |  |  |  |  |  | "Joh\'n" | en |  |  |  |  |  |  |  | 'Joh\'n'@en |
| john | lqstring-with-escaped-prime-and-quote | 'Joh\'\"n'@en | language_qualified_string | True | 0 |  |  |  |  |  | "Joh\'\"n" | en |  |  |  |  |  |  |  | 'Joh\'\"n'@en |
| john | lqstring-with-triple-double-quotes | 'John'@en | language_qualified_string | True | 0 |  |  |  |  |  | """John""" | en |  |  |  |  |  |  |  | 'John'@en |

A new `node2` column has been created with the imploded data.  The
`--mode=NONE` option was required because the input file did not have a
`node2` column, and thus was not a valid KGTK edge file.

Suppose that `file1.tsv` contains the following table in KGTK format.

| id | node1 | label | node2 | node2;kgtk:data_type | node2;kgtk:number | node2;kgtk:low_tolerance | node2;kgtk:high_tolerance | node2;kgtk:units_node | node2;kgtk:date_and_time | node2;kgtk:precision | node2;kgtk:calendar | node2;kgtk:truth | node2;kgtk:symbol | node2;kgtk:latitude | node2;kgtk:longitude | node2;kgtk:text | node2;kgtk:language |
| -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- |
| oecd;OECD-Latvia g2g9e7f8-en..csv;D6 | Q211 | P1082 |  | quantity | 19782 |  |  | Q10000000040001 |  |  |  |  |  |  |  |  |  |
| oecd;OECD-Latvia g2g9e7f8-en...csv;D6;D4 | oecd;OECD-Latvia g2g9e7f8-en..csv;D6 | P585 |  | date_and_times |  |  |  |  | 2011-01-01T00:00:00 | 9 | Q1985727 |  |  |  |  |  |  |
| oecd;OECD-Latvia g2g9e7f8-en...csv;D6; | oecd;OECD-Latvia g2g9e7f8-en..csv;D6 | P248 |  | symbol |  |  |  |  |  |  |  |  | Q41550 |  |  |  |  |
| oecd;OECD-Latvia g2g9e7f8-en..csv;D7 | Q211 | P1082 |  | quantity | 19776 |  |  | Q10000000040001 |  |  |  |  |  |  |  |  |  |
| oecd;OECD-Latvia g2g9e7f8-en...csv;D7;D4 | oecd;OECD-Latvia g2g9e7f8-en..csv;D7 | P585 |  | date_and_times |  |  |  |  | 2011-01-01T00:00:00 | 9 | Q1985727 |  |  |  |  |  |  |
| oecd;OECD-Latvia g2g9e7f8-en...csv;D7; | oecd;OECD-Latvia g2g9e7f8-en..csv;D7 | P248 |  | symbol |  |  |  |  |  |  |  |  | Q41550 |  |  |  |  |
| oecd;OECD-Latvia g2g9e7f8-en..csv;D8 | Q211 | P1082 |  | quantity | -7.5 |  |  | Q10000000040002 |  |  |  |  |  |  |  |  |  |
| oecd;OECD-Latvia g2g9e7f8-en...csv;D8;D4 | oecd;OECD-Latvia g2g9e7f8-en..csv;D8 | P585 |  | date_and_times |  |  |  |  | 2011-01-01T00:00:00 | 9 | Q1985727 |  |  |  |  |  |  |
| oecd;OECD-Latvia g2g9e7f8-en...csv;D8; | oecd;OECD-Latvia g2g9e7f8-en..csv;D8 | P248 |  | symbol |  |  |  |  |  |  |  |  | Q41550 |  |  |  |  |
| oecd;OECD-Latvia g2g9e7f8-en..csv;D10 | Q211 | P1082 |  | quantity | 6.4 |  |  | Q10000000040002 |  |  |  |  |  |  |  |  |  |


The file does not include the `si_units` or `language_suffix` optional columns.
It does include a `node2` column, so the `--mode=NONE` option is not required.
The existing `node2` column, which is empty, will be overwritten with the
imploded data.

```bash
kgtk implode -i file1.tsv -v --without si_units language_suffix
```

The output will be the following table in KGTK format:

| id | node1 | label | node2 | node2;kgtk:data_type | node2;kgtk:number | node2;kgtk:low_tolerance | node2;kgtk:high_tolerance | node2;kgtk:units_node | node2;kgtk:date_and_time | node2;kgtk:precision | node2;kgtk:calendar | node2;kgtk:truth | node2;kgtk:symbol | node2;kgtk:latitude | node2;kgtk:longitude | node2;kgtk:text | node2;kgtk:language |
| -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- |
| oecd;OECD-Latvia g2g9e7f8-en..csv;D6 | Q211 | P1082 | 19782Q10000000040001 | quantity | 19782 |  |  | Q10000000040001 |  |  |  |  |  |  |  |  |  |
| oecd;OECD-Latvia g2g9e7f8-en...csv;D6;D4 | oecd;OECD-Latvia g2g9e7f8-en..csv;D6 | P585 | ^2011-01-01T00:00:00/9 | date_and_times |  |  |  |  | 2011-01-01T00:00:00 | 9 | Q1985727 |  |  |  |  |  |  |
| oecd;OECD-Latvia g2g9e7f8-en...csv;D6; | oecd;OECD-Latvia g2g9e7f8-en..csv;D6 | P248 | Q41550 | symbol |  |  |  |  |  |  |  |  | Q41550 |  |  |  |  |
| oecd;OECD-Latvia g2g9e7f8-en..csv;D7 | Q211 | P1082 | 19776Q10000000040001 | quantity | 19776 |  |  | Q10000000040001 |  |  |  |  |  |  |  |  |  |
| oecd;OECD-Latvia g2g9e7f8-en...csv;D7;D4 | oecd;OECD-Latvia g2g9e7f8-en..csv;D7 | P585 | ^2011-01-01T00:00:00/9 | date_and_times |  |  |  |  | 2011-01-01T00:00:00 | 9 | Q1985727 |  |  |  |  |  |  |
| oecd;OECD-Latvia g2g9e7f8-en...csv;D7; | oecd;OECD-Latvia g2g9e7f8-en..csv;D7 | P248 | Q41550 | symbol |  |  |  |  |  |  |  |  | Q41550 |  |  |  |  |
| oecd;OECD-Latvia g2g9e7f8-en..csv;D8 | Q211 | P1082 | -7.5Q10000000040002 | quantity | -7.5 |  |  | Q10000000040002 |  |  |  |  |  |  |  |  |  |
| oecd;OECD-Latvia g2g9e7f8-en...csv;D8;D4 | oecd;OECD-Latvia g2g9e7f8-en..csv;D8 | P585 | ^2011-01-01T00:00:00/9 | date_and_times |  |  |  |  | 2011-01-01T00:00:00 | 9 | Q1985727 |  |  |  |  |  |  |
| oecd;OECD-Latvia g2g9e7f8-en...csv;D8; | oecd;OECD-Latvia g2g9e7f8-en..csv;D8 | P248 | Q41550 | symbol |  |  |  |  |  |  |  |  | Q41550 |  |  |  |  |
| oecd;OECD-Latvia g2g9e7f8-en..csv;D10 | Q211 | P1082 | 6.4Q10000000040002 | quantity | 6.4 |  |  | Q10000000040002 |  |  |  |  |  |  |  |  |  |


Suppose you now wish to remove the exploded columns from the final output file.

```bash
kgtk implode -i file1.tsv -v --without si_units language_suffix --remove-prefixed-columns
```

The output will be the following table in KGTK format:

| id | node1 | label | node2 |
| -- | -- | -- | -- |
| oecd;OECD-Latvia g2g9e7f8-en..csv;D6 | Q211 | P1082 | 19782Q10000000040001 |
| oecd;OECD-Latvia g2g9e7f8-en...csv;D6;D4 | oecd;OECD-Latvia g2g9e7f8-en..csv;D6 | P585 | ^2011-01-01T00:00:00/9 |
| oecd;OECD-Latvia g2g9e7f8-en...csv;D6; | oecd;OECD-Latvia g2g9e7f8-en..csv;D6 | P248 | Q41550 |
| oecd;OECD-Latvia g2g9e7f8-en..csv;D7 | Q211 | P1082 | 19776Q10000000040001 |
| oecd;OECD-Latvia g2g9e7f8-en...csv;D7;D4 | oecd;OECD-Latvia g2g9e7f8-en..csv;D7 | P585 | ^2011-01-01T00:00:00/9 |
| oecd;OECD-Latvia g2g9e7f8-en...csv;D7; | oecd;OECD-Latvia g2g9e7f8-en..csv;D7 | P248 | Q41550 |
| oecd;OECD-Latvia g2g9e7f8-en..csv;D8 | Q211 | P1082 | -7.5Q10000000040002 |
| oecd;OECD-Latvia g2g9e7f8-en...csv;D8;D4 | oecd;OECD-Latvia g2g9e7f8-en..csv;D8 | P585 | ^2011-01-01T00:00:00/9 |
| oecd;OECD-Latvia g2g9e7f8-en...csv;D8; | oecd;OECD-Latvia g2g9e7f8-en..csv;D8 | P248 | Q41550 |
| oecd;OECD-Latvia g2g9e7f8-en..csv;D10 | Q211 | P1082 | 6.4Q10000000040002 |
