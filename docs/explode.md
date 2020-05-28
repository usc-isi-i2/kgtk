The explode command copies its input file to its output file, exploding one
column (normally node2) into seperate columns for esch structured subfield. If
a cell in the column being exploded contains a list, that record is optionally
expanded into multiple records before explosion, with all other columns
copied-as is.

## Usage

```bash
usage: kgtk explode [-h] [-o OUTPUT_KGTK_FILE] [--column COLUMN_NAME]
                    [--fields {list_len,data_type,valid,text,language,suffix,numberstr,number,low_tolerancestr,low_tolerance,high_tolerancestr,high_tolerance,si_units,wikidata_node,latitudestr,latitude,longitudestr,longitude,date,time,date_and_time,yearstr,year,monthstr,month,daystr,day,hourstr,hour,minutesstr,minutes,secondsstr,seconds,zonestr,precisionstr,precision,iso8601extended,truth,symbol} [{list_len,data_type,valid,text,language,suffix,numberstr,number,low_tolerancestr,low_tolerance,high_tolerancestr,high_tolerance,si_units,wikidata_node,latitudestr,latitude,longitudestr,longitude,date,time,date_and_time,yearstr,year,monthstr,month,daystr,day,hourstr,hour,minutesstr,minutes,secondsstr,seconds,zonestr,precisionstr,precision,iso8601extended,truth,symbol} ...]]
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
  --fields {list_len,data_type,valid,text,language,suffix,numberstr,number,low_tolerancestr,low_tolerance,high_tolerancestr,high_tolerance,si_units,wikidata_node,latitudestr,latitude,longitudestr,longitude,date,time,date_and_time,yearstr,year,monthstr,month,daystr,day,hourstr,hour,minutesstr,minutes,secondsstr,seconds,zonestr,precisionstr,precision,iso8601extended,truth,symbol} [{list_len,data_type,valid,text,language,suffix,numberstr,number,low_tolerancestr,low_tolerance,high_tolerancestr,high_tolerance,si_units,wikidata_node,latitudestr,latitude,longitudestr,longitude,date,time,date_and_time,yearstr,year,monthstr,month,daystr,day,hourstr,hour,minutesstr,minutes,secondsstr,seconds,zonestr,precisionstr,precision,iso8601extended,truth,symbol} ...]
                        The names of the fields to extract. (default=['data_type', 'valid', 'list_len', 'text', 'language', 'suffix', 'number', 'low_tolerance',
                        'high_tolerance', 'si_units', 'wikidata_node', 'latitude', 'longitude', 'date_and_time', 'precision', 'truth', 'symbol']).
  --prefix PREFIX       The prefix for exploded column names. (default=node2;).
  --overwrite [OVERWRITE_COLUMNS]
                        Indicate that it is OK to overwrite existing columns. (default=False).
  --expand [EXPAND_LIST]
                        Expand the source column if it contains a list, else fail. (default=False).

  -v, --verbose         Print additional progress messages (default=False).
```

## KGTK Data Types and Fields

| Data Type                 | Fields                      |
| ========================= | =========================== |
| boolean                   | valid truth                 |
| date_and_times            | valid yearstr year monthstr month daystr day hourstr hour minutesstr minutes secondsstr seconds zonestr precisionstr precision iso8601extended |
| empty                     | valid                       |
| extension                 |                             |
| language_qualified_string | valid text language suffix  |
| list                      | valid list_len              |
| location_coordinates      | valid latitudestr latitude longitudestr longitude |
| number                    | valid numberstr number      |
| quantity                  | valid numberstr number low_tolerancestr low_tolerance high_tolerancestr high_tolerance si_units wikidata_node |
| string                    | valid text                  |
| symbol                    | valid symbol                |

## Examples

Suppose that `file1.tsv` contains the following table in KGTK format:

| node1 | label         | node2         |
| ===== | ============= | ============= |
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
(This is obsolete, no that date_and_time is the default instead of individual subfields.)

| node1 | label | node2 | node2;data_type | node2;valid | node2;list_len | node2;text | node2;language | node2;suffix | node2;number | node2;low_tolerance | node2;high_tolerance | node2;si_units | node2;wikidata_node | node2;lat | node2;lon | node2;year | node2;month | node2;day | node2;hour | node2;minutes | node2;seconds | node2;zonestr | node2;precision | node2;iso8601extended | node2;truth | node2;symbol |
| ===== | ===== | ===== | =============== | =========== | ============== | ============== | =========== | =========== | ============ | =================== | ==================== | ============== | =================== | ========= | ========= | ========== | =========== | ========= | ========== | ============= | ============= | ============= | =============== | ===================== | =========== | ============ |
| john | string | "John" | string | True | 0 | "John" |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| john | lqstring | 'John'@en | language_qualified_string | True | 0 | "John" | en |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| john | integer | 12345 | number | True | 0 |  |  |  | 12345 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| john | number | 186.2 | number | True | 0 |  |  |  | 186.2 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| john | number | 186.2e04 | number | True | 0 |  |  |  | 1862000.0 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| john | number | -186.2 | number | True | 0 |  |  |  | -186.2 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| john | number | +186.2e-6 | number | True | 0 |  |  |  | 0.0001862 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| john | quantity | 84.3[84,85]kg | quantity | True | 0 |  |  |  | 84.3 | 84.0 | 85.0 | kg |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| john | date_and_time | ^1960-11-05T00:00 | date_and_times | True | 0 |  |  |  |  |  |  |  |  |  |  | 1960 | 11 | 5 | 0 | 0 |  |  |  | True |  |  |
| john | date_and_time | ^1980-11-05T00:00Z/6 | date_and_times | True | 0 |  |  |  |  |  |  |  |  |  |  | 1980 | 11 | 5 | 0 | 0 |  | "Z" | 6 | True |  |  |
| john | location | @60.2/134.3 | location_coordinates | True | 0 |  |  |  |  |  |  |  |  | 60.2 | 134.3 |  |  |  |  |  |  |  |  |  |  |  |
| john | boolean | True | boolean | True | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | True |  |
| john | symbol | quadrature | symbol | True | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | quadrature |
| john | list | home\|work | list | True | 2 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
