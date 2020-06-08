The explode command copies its input file to its output file, exploding one
column (normally node2) into separate columns for each structured subfield. If
a cell in the column being exploded contains a list, that record is optionally
expanded into multiple records before explosion, with all other columns
copied-as is.

By default, all KGTK data types are exploded.  The --types option allows the
user to specify the set of data types to explode.  Each data type is exploded
into one or more columns.  Some columns, such as text, are shared between
data types (e.g., string and language qualified string).

In expert help mode, the --fields option is presented.  It may be used to
specify a list of fields to extract, including finer grained fields, such
as individual fields for the year, month, and day of dates.  Either --types
or --fields may be used, but not both.

## Usage

```
usage: kgtk explode [-h] [-o OUTPUT_KGTK_FILE] [--column COLUMN_NAME]
                    [--types [{empty,list,number,quantity,string,language_qualified_string,location_coordinates,date_and_times,extension,boolean,symbol} [{empty,list,number,quantity,string,language_qualified_string,location_coordinates,date_and_times,extension,boolean,symbol} ...]]]
                    [--prefix PREFIX] [--overwrite [OVERWRITE_COLUMNS]] [--expand [EXPAND_LIST]] [-v]
                    [input_kgtk_file]

Copy a KGTK file, exploding one column (usually node2) into seperate columns for each subfield. If a cell in the column being exploded contains a list, that record is optionally expanded into multiple records before explosion, with all other columns copied-as is.

Additional options are shown in expert help.
kgtk --expert expand --help

positional arguments:
  input_kgtk_file       The KGTK file to filter. May be omitted or '-' for stdin (default=-).

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_KGTK_FILE, --output-file OUTPUT_KGTK_FILE
                        The KGTK file to write (default=-).
  --column COLUMN_NAME  The name of the column to explode. (default=node2).
  --types [{empty,list,number,quantity,string,language_qualified_string,location_coordinates,date_and_times,extension,boolean,symbol} [{empty,list,number,quantity,string,language_qualified_string,location_coordinates,date_and_times,extension,boolean,symbol} ...]]
                        The KGTK data types for which fields should be exploded. (default=['empty', 'list', 'number', 'quantity', 'string',
                        'language_qualified_string', 'location_coordinates', 'date_and_times', 'extension', 'boolean', 'symbol']).
  --prefix PREFIX       The prefix for exploded column names. (default=node2;kgtk:).
  --overwrite [OVERWRITE_COLUMNS]
                        Indicate that it is OK to overwrite existing columns. (default=False).
  --expand [EXPAND_LIST]
                        Expand the source column if it contains a list, else fail. (default=False).

  -v, --verbose         Print additional progress messages (default=False).
```

## KGTK Data Types and Fields

This table shows the fields (without the prefix value, normally `node2;`) that are created for each KGTK data type.

| Data Type                 | Fields                      |
| ------------------------- | --------------------------- |
| boolean                   | valid truth                 |
| date_and_times            | valid year date_and_time precision |
| empty                     | valid                       |
| extension                 |                             |
| language_qualified_string | valid text language suffix  |
| list                      | valid list_len              |
| location_coordinates      | valid latitude longitude    |
| number                    | valid number                |
| quantity                  | valid number low_tolerance high_tolerance si_units wikidata_node |
| string                    | valid text                  |
| symbol                    | valid symbol                |

## Examples

Suppose that `file1.tsv` contains the following table in KGTK format:

| node1 | label         | node2         |
| ----- | ------------- | ------------- |
| john  | string        | "John"        |
| john  | lqstring      | "John"@en     |
| john  | integer       | 12345         |
| john  | number        | 186.2         |
| john  | number        | 186.2e04      |
| john  | number        | -186.2        |
| john  | number        | +186.2e-6     |
| john  | quantity      | 84.3[84,85]kg |
| john  | date_and_time | ^1960-11-05T00:00 |
| john  | date_and_time | ^1960-11-05T00:00Z/6 |
| john  | location      | @60.2/134.3   |
| john  | boolean       | True          |
| john  | symbol        | quadrature    |
| john  | list          | home\|work    |


```bash
kgtk explode file1.tsv
```

The output will be the following table in KGTK format:

| node1 | label | node2 | node2;kgtk:data_type | node2;kgtk:valid | node2;kgtk:list_len | node2;kgtk:number | node2;kgtk:low_tolerance | node2;kgtk:high_tolerance | node2;kgtk:si_units | node2;kgtk:units_node | node2;kgtk:text | node2;kgtk:language | node2;kgtk:language_suffix | node2;kgtk:latitude | node2;kgtk:longitude | node2;kgtk:date_and_time | node2;kgtk:precision | node2;kgtk:truth | node2;kgtk:symbol |
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
| john | list | home\|work | list | True | 2 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
