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
usage: kgtk implode [-h] [-o OUTPUT_KGTK_FILE] [--reject-file REJECT_KGTK_FILE]
                    [--column COLUMN_NAME] [--prefix PREFIX]
                    [--types [{empty,list,number,quantity,string,language_qualified_string,location_coordinates,date_and_times,extension,boolean,symbol} [{empty,list,number,quantity,string,language_qualified_string,location_coordinates,date_and_times,extension,boolean,symbol} ...]]]
                    [--without [{valid,list_len,language_suffix,low_tolerance,high_tolerance,si_units,units_node,precision} [{valid,list_len,language_suffix,low_tolerance,high_tolerance,si_units,units_node,precision} ...]]]
                    [--overwrite [OVERWRITE_COLUMN]] [--validate [VALIDATE]]
                    [--escape-pipes [ESCAPE_PIPES]]
                    [--quantities-include-numbers [QUANTITIES_INCLUDE_NUMBERS]]
                    [--general-strings [GENERAL_STRINGS]]
                    [--show-data-types [SHOW_DATA_TYPES]] [-v]
                    [input_kgtk_file]

Copy a KGTK file, building one column (usually node2) from seperate columns for each subfield. 

Strings may include language qualified strings, and quantities may include numbers. 

Date and times subfields and symbol subfields may be optionally quoted. Triple quotes may be used where quotes are accepted. 

Additional options are shown in expert help.
kgtk --expert expand --help

positional arguments:
  input_kgtk_file       The KGTK file to filter. May be omitted or '-' for stdin
                        (default=-).

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_KGTK_FILE, --output-file OUTPUT_KGTK_FILE
                        The KGTK file to write (default=-).
  --reject-file REJECT_KGTK_FILE
                        The KGTK file into which to write rejected records
                        (default=None).
  --column COLUMN_NAME  The name of the column to explode. (default=node2).
  --prefix PREFIX       The prefix for exploded column names. (default=node2;kgtk:).
  --types [{empty,list,number,quantity,string,language_qualified_string,location_coordinates,date_and_times,extension,boolean,symbol} [{empty,list,number,quantity,string,language_qualified_string,location_coordinates,date_and_times,extension,boolean,symbol} ...]]
                        The KGTK data types for which fields should be imploded.
                        (default=['empty', 'list', 'number', 'quantity', 'string',
                        'language_qualified_string', 'location_coordinates',
                        'date_and_times', 'extension', 'boolean', 'symbol']).
  --without [{language_suffix,low_tolerance,high_tolerance,si_units,units_node,precision} [{valid,list_len,language_suffix,low_tolerance,high_tolerance,si_units,units_node,precision} ...]]
                        The KGTK fields to do without. (default=None).
  --overwrite [OVERWRITE_COLUMN]
                        Indicate that it is OK to overwrite an existing imploded
                        column. (default=True).
  --validate [VALIDATE]
                        Validate imploded values. (default=True).
  --escape-pipes [ESCAPE_PIPES]
                        When true, pipe characters (|) need to be escaped (\|) per KGTK
                        file format. (default=False).
  --quantities-include-numbers [QUANTITIES_INCLUDE_NUMBERS]
                        When true, numbers are acceptable quantities. (default=True).
  --general-strings [GENERAL_STRINGS]
                        When true, strings may include language qualified strings.
                        (default=True).
  --show-data-types [SHOW_DATA_TYPES]
                        Print the list of data types and exit. (default=False).

  -v, --verbose         Print additional progress messages (default=False).
```

## KGTK Data Types and Fields

This table shows the fields (without the prefix value, normally `node2;`) that are used for each KGTK data type.

| Data Type                 | Fields                      |
| ------------------------- | --------------------------- |
| boolean                   | truth                 |
| date_and_times            | date_and_time precision* |
| empty                     |                       |
| extension**              |                             |
| language_qualified_string | text language* language_suffix*  |
| list**                   |              |
| location_coordinates      | latitude longitude    |
| number                    | number                |
| quantity                  | number low_tolerance* high_tolerance* si_units* units_node* |
| string                    | text                  |
| symbol                    | symbol                |

Data types may have required fields and optional fields (marked `*` in the
table above).  If an optional field is listed in the `--without` list, then it
will not be used to to build KGTk values and need not be present as a column.

The `extension` and `list` data types (marked `**` in the table above) cannot
be build by `kgtk implode`.


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
kgtk explode file2.tsv --mode=NONE
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
kgtk implode file1.tsv -v --without si_units language_suffix
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
kgtk implode file1.tsv -v --without si_units language_suffix --remove-prefixed-columns
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
