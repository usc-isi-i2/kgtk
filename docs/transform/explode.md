## Summary

The explode command copies its input file to its output file, exploding one
column (normally node2) into separate columns for each structured subfield.

!!! note
    [`kgtk implode`](../implode) is the inverse of `kgtk explode`.

### Exploding a Multivalue (List) Cell

If a cell in the column being exploded contains a list, that record is optionally
expanded into multiple records before explosion, with all other columns
copied-as is.

### Data Type Selection

By default, all KGTK data types are exploded.  The `--types` option allows the
user to specify the set of data types to explode.  Each data type is exploded
into one or more columns.  Some columns, such as text, are shared between
data types (e.g., string and language qualified string).

### Field-level Control

In expert help mode, the `--fields` option is presented.  It may be used to
specify a list of fields to extract, including finer grained fields, such
as individual fields for the year, month, and day of dates.

!!! note
    Either `--types` or `--fields` may be used, but not both.

### KGTK Data Types and Fields

This table shows the fields (without the prefix value, normally `node2;kgtk:`) that are created for each KGTK data type.

| Data Type                 | Default Fields              | Additional Fields |
| ------------------------- | --------------------------- | ----------------- |
| boolean                   | valid truth                 |                   |
| date_and_times            | valid date_and_time precision | date time year yearstr monthstr month daystr day hourstr hour minutesstr minutes secondsstr seconds zonestr precisionstr iso8601extended |
| empty                     | valid                       | |
| extension                 |                             | |
| language_qualified_string | valid text language language_suffix  | |
| list                      | valid list_len              | |
| location_coordinates      | valid latitude longitude    | latitudestr longitudestr |
| number                    | valid number                | numberstr |
| quantity                  | valid number low_tolerance high_tolerance si_units units_node | numberstr los_tolerancestr high_tolerancestr |
| string                    | valid text                  | |
| symbol                    | valid symbol                | |

### KGTK Data Fields

| Field Name           | Format  | Data Type | Comments |
| -------------------- | ------  | --------- | -------- |
|            data_type | sym   | (all) | This field identifies the KGTK data type of the item being exploded. |
|                 date | str   | date_and_times | The date (year/month/day) section of an ISO 8601 date and time item. |
|        date_and_time | str   | date_and_times | The ISO 8601 date and time string, excluding the KGTK date-and-tmes sigil (`^`) and the optional precision suffix.  |
|                  day | int   | date_and_times | The day of the month of an ISO 8601 date and time item as an integer. 1-31 |
|               daystr | str   | date_and_times | The day of the month of an ISO 8610 date and time item as a sting with a leading zero if needed. |
|       high_tolerance | num   | quantity       | The upper end of the tolerance range of a KGTK quantity, as a floating point number. |
|    high_tolerancestr | str   | quantity       | The upper end of the tolerance range of a KGTK quantity, as a string. |
|                 hour | int   | date_and_times | The hour of the dat of an ISO 8601 date and time item as an integer. 0-24 |
|              hourstr | str   | date_and_times | The hour of the dat of an ISO 8601 date and time item as a string with a leading zero if needed. |
|      iso8601extended | bool  | date_and_times | A boolean indicating whether or not an ISO 8601 date and time item has internal field separators (`-` and `:`). |
|             language | sym   | date and times | A language code from a KGTK date and times item, without the `@` separator and without the optional language suffix. This is typically a 2- and 3-character ISO 639-3 or ISO 639-5 code, although other codes are possible. |
|      language_suffix | sym   | date_and_times | A language code suffix, including the suffix separator (typically `-`).
|             latitude | num   | location_coordinates | A latitude, validly limited to the interval [-90 .. 90], as a floating point number. |
|          latitudestr | str   | location_coordinates | A latitude, validly limited to the interval[-90 .. 90], as a string. |
|             list_len | int   | list | The number of items in a multivalued (list, `|`) cell. |
|            longitude | num   | location_coordinates |  A longitude, validly limited to the interval [-180 .. 1800], as a floating point number. |
|         longitudestr | str   | location_coordinates |  A longitude, validly limited to the interval [-180 .. 1800], as a string. |
|        low_tolerance | num   | quantity       | The lower end of the tolerance range of a KGTK quantity, as a floating point number. |
|     low_tolerancestr | str   | quantity       | The lower end of the tolerance range of a KGTK quantity, as a string. |
|              minutes | int   | date_and_times | The minutes of the hour of an ISO 8601 date and time item as an integer. 0-59|
|           minutesstr | str   | date_and_times | The minutes of the hour of an ISO 8601 date and time item as a string. |
|                month | int   | date_and_times | The month of the year of an ISO 8601 date and time item as an integer. 1-12 |
|             monthstr | str   | date_and_times | The month of the year of an ISO 8601 date and time item as an string. |
|               number | num   | number quantity | The numeric part of a KGTK number or quantity data type, as a floating point number. |
|            numberstr | str   | number quantity | The numeric part of a KGTK number or quantity data type, as a string. |
|            precision | int   | date_and_times  | A code indicating the precision of the value.  Currently 0 to 19, without the `/` separator, as an integer. |
|         precisionstr | str   | date_and_times  | A code indicating the precision of the value.  Currently 0 to 19, without the `/` separator, as a string. |
|              seconds | int   | date_and_times  | The seconds of the minute of an ISO 8601 date and time item as an integer. Fractional seconds are not supported. |
|           secondsstr | str   | date_and_times  | The seconds of the minute of an ISO 8601 date and time item as a string.  Fractional seconds are not supported. |
|             si_units | sym   | quantity        | A dimensional pattern using SI units. |
|               symbol | sym   | symbol          | A named symbol. |
|                 text | str   | language_qualified_string string | The text contents of a string or language qualified string. |
|                 time | str   | date_and_times  | The time (hour/minute/second) section of an ISO 8601 date and time item. |
|                truth | bool  | boolean         | The value of a boolean item. |
|           units_node | sym   | quantity        | A generalized Wikipedia node symbol, which may be used an alternative dimensional identifier. |
|                valid | bool  | (all)           | An indicator of whether the item is a valid KGTK value representation. |
|                 year | int   | date_and_times  | The year of an ISO 8601 date and time string as an integer.  May be negative. |
|              yearstr | str   | date_and_times  | The year of an ISO 8601 date and time string as a string.  May be negative. |
|              zonestr | str   | date_and_times  | The time zone portion of an ISO 8601 date and time string. May start with `+` or `-`.|

## Usage

```
usage: kgtk explode [-h] [-i INPUT_FILE] [-o OUTPUT_FILE]
                    [--column COLUMN_NAME]
                    [--types [{empty,list,number,quantity,string,language_qualified_string,location_coordinates,date_and_times,extension,boolean,symbol} [{empty,list,number,quantity,string,language_qualified_string,location_coordinates,date_and_times,extension,boolean,symbol} ...]]]
                    [--prefix PREFIX] [--overwrite [True|False]]
                    [--expand [True|False]] [--show-data-types [True|False]]
                    [--show-field-names [True|False]]
                    [--show-field-formats [True|False]]
                    [--output-format {csv,json,json-map,json-map-compact,jsonl,jsonl-map,jsonl-map-compact,kgtk,md,tsv,tsv-csvlike,tsv-unquoted,tsv-unquoted-ep}]
                    [-v [optional True|False]]

Copy a KGTK file, exploding one column (usually node2) into seperate columns for each subfield. If a cell in the column being exploded contains a list, that record is optionally expanded into multiple records before explosion, with all other columns copied-as is.

Additional options are shown in expert help.
kgtk --expert explode --help

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK input file. (May be omitted or '-' for
                        stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for
                        stdout.)
  --column COLUMN_NAME  The name of the column to explode. (default=node2).
  --types [{empty,list,number,quantity,string,language_qualified_string,location_coordinates,date_and_times,extension,boolean,symbol} [{empty,list,number,quantity,string,language_qualified_string,location_coordinates,date_and_times,extension,boolean,symbol} ...]]
                        The KGTK data types for which fields should be
                        exploded. (default=['empty', 'list', 'number',
                        'quantity', 'string', 'language_qualified_string',
                        'location_coordinates', 'date_and_times', 'extension',
                        'boolean', 'symbol']).
  --prefix PREFIX       The prefix for exploded column names.
                        (default=node2;kgtk:).
  --overwrite [True|False]
                        Indicate that it is OK to overwrite existing columns.
                        (default=False).
  --expand [True|False]
                        When True, expand source cells that contain a lists,
                        else fail if a source cell contains a list.
                        (default=False).
  --show-data-types [True|False]
                        Print the list of data types and exit.
                        (default=False).
  --show-field-names [True|False]
                        Print the list of field names and exit.
                        (default=False).
  --show-field-formats [True|False]
                        Print the list of field names and formats, then exit.
                        (default=False).
  --output-format {csv,json,json-map,json-map-compact,jsonl,jsonl-map,jsonl-map-compact,kgtk,md,tsv,tsv-csvlike,tsv-unquoted,tsv-unquoted-ep}
                        The file format (default=kgtk)

  -v [optional True|False], --verbose [optional True|False]
                        Print additional progress messages (default=False).
```

## Expert Usage

```
usage: kgtk explode [-h] [-i INPUT_FILE] [-o OUTPUT_FILE]
                    [--column COLUMN_NAME]
                    [--types [{empty,list,number,quantity,string,language_qualified_string,location_coordinates,date_and_times,extension,boolean,symbol} [{empty,list,number,quantity,string,language_qualified_string,location_coordinates,date_and_times,extension,boolean,symbol} ...]]
                    | --fields
                    [{list_len,data_type,valid,text,decoded_text,language,language_suffix,numberstr,number,low_tolerancestr,low_tolerance,high_tolerancestr,high_tolerance,si_units,units_node,latitudestr,latitude,longitudestr,longitude,date,time,date_and_time,yearstr,year,monthstr,month,daystr,day,hourstr,hour,minutesstr,minutes,secondsstr,seconds,zonestr,precisionstr,precision,iso8601extended,truth,symbol} [{list_len,data_type,valid,text,decoded_text,language,language_suffix,numberstr,number,low_tolerancestr,low_tolerance,high_tolerancestr,high_tolerance,si_units,units_node,latitudestr,latitude,longitudestr,longitude,date,time,date_and_time,yearstr,year,monthstr,month,daystr,day,hourstr,hour,minutesstr,minutes,secondsstr,seconds,zonestr,precisionstr,precision,iso8601extended,truth,symbol} ...]]]
                    [--prefix PREFIX] [--overwrite [True|False]]
                    [--expand [True|False]] [--show-data-types [True|False]]
                    [--show-field-names [True|False]]
                    [--show-field-formats [True|False]]
                    [--output-format {csv,json,json-map,json-map-compact,jsonl,jsonl-map,jsonl-map-compact,kgtk,md,tsv,tsv-csvlike,tsv-unquoted,tsv-unquoted-ep}]
                    [--errors-to-stdout [optional True|False] |
                    --errors-to-stderr [optional True|False]]
                    [--show-options [optional True|False]]
                    [-v [optional True|False]]
                    [--very-verbose [optional True|False]]
                    [--column-separator COLUMN_SEPARATOR]
                    [--input-format INPUT_FORMAT]
                    [--compression-type COMPRESSION_TYPE]
                    [--error-limit ERROR_LIMIT]
                    [--use-mgzip [optional True|False]]
                    [--mgzip-threads MGZIP_THREADS]
                    [--gzip-in-parallel [optional True|False]]
                    [--gzip-queue-size GZIP_QUEUE_SIZE]
                    [--mode {NONE,EDGE,NODE,AUTO}]
                    [--force-column-names FORCE_COLUMN_NAMES [FORCE_COLUMN_NAMES ...]]
                    [--header-error-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}]
                    [--skip-header-record [optional True|False]]
                    [--unsafe-column-name-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}]
                    [--prohibit-whitespace-in-column-names [optional True|False]]
                    [--initial-skip-count INITIAL_SKIP_COUNT]
                    [--every-nth-record EVERY_NTH_RECORD]
                    [--record-limit RECORD_LIMIT] [--tail-count TAIL_COUNT]
                    [--repair-and-validate-lines [optional True|False]]
                    [--repair-and-validate-values [optional True|False]]
                    [--blank-required-field-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}]
                    [--comment-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}]
                    [--empty-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}]
                    [--fill-short-lines [optional True|False]]
                    [--invalid-value-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}]
                    [--long-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}]
                    [--prohibited-list-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}]
                    [--short-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}]
                    [--truncate-long-lines [TRUNCATE_LONG_LINES]]
                    [--whitespace-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}]
                    [--additional-language-codes [ADDITIONAL_LANGUAGE_CODES [ADDITIONAL_LANGUAGE_CODES ...]]]
                    [--allow-lax-qnodes [ALLOW_LAX_QNODES]]
                    [--allow-language-suffixes [ALLOW_LANGUAGE_SUFFIXES]]
                    [--allow-lax-strings [ALLOW_LAX_STRINGS]]
                    [--allow-lax-lq-strings [ALLOW_LAX_LQ_STRINGS]]
                    [--allow-wikidata-lq-strings [ALLOW_WIKIDATA_LQ_STRINGS]]
                    [--require-iso8601-extended [REQUIRE_ISO8601_EXTENDED]]
                    [--force-iso8601-extended [FORCE_ISO8601_EXTENDED]]
                    [--allow-month-or-day-zero [ALLOW_MONTH_OR_DAY_ZERO]]
                    [--repair-month-or-day-zero [REPAIR_MONTH_OR_DAY_ZERO]]
                    [--allow-end-of-day [ALLOW_END_OF_DAY]]
                    [--minimum-valid-year MINIMUM_VALID_YEAR]
                    [--clamp-minimum-year [CLAMP_MINIMUM_YEAR]]
                    [--ignore-minimum-year [IGNORE_MINIMUM_YEAR]]
                    [--maximum-valid-year MAXIMUM_VALID_YEAR]
                    [--clamp-maximum-year [CLAMP_MAXIMUM_YEAR]]
                    [--ignore-maximum-year [IGNORE_MAXIMUM_YEAR]]
                    [--validate-fromisoformat [VALIDATE_FROMISOFORMAT]]
                    [--allow-lax-coordinates [ALLOW_LAX_COORDINATES]]
                    [--repair-lax-coordinates [REPAIR_LAX_COORDINATES]]
                    [--allow-out-of-range-coordinates [ALLOW_OUT_OF_RANGE_COORDINATES]]
                    [--minimum-valid-lat MINIMUM_VALID_LAT]
                    [--clamp-minimum-lat [CLAMP_MINIMUM_LAT]]
                    [--maximum-valid-lat MAXIMUM_VALID_LAT]
                    [--clamp-maximum-lat [CLAMP_MAXIMUM_LAT]]
                    [--minimum-valid-lon MINIMUM_VALID_LON]
                    [--clamp-minimum-lon [CLAMP_MINIMUM_LON]]
                    [--maximum-valid-lon MAXIMUM_VALID_LON]
                    [--clamp-maximum-lon [CLAMP_MAXIMUM_LON]]
                    [--modulo-repair-lon [MODULO_REPAIR_LON]]
                    [--escape-list-separators [ESCAPE_LIST_SEPARATORS]]

Copy a KGTK file, exploding one column (usually node2) into seperate columns for each subfield. If a cell in the column being exploded contains a list, that record is optionally expanded into multiple records before explosion, with all other columns copied-as is.

Additional options are shown in expert help.
kgtk --expert explode --help

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK input file. (May be omitted or '-' for
                        stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for
                        stdout.)
  --column COLUMN_NAME  The name of the column to explode. (default=node2).
  --types [{empty,list,number,quantity,string,language_qualified_string,location_coordinates,date_and_times,extension,boolean,symbol} [{empty,list,number,quantity,string,language_qualified_string,location_coordinates,date_and_times,extension,boolean,symbol} ...]]
                        The KGTK data types for which fields should be
                        exploded. (default=['empty', 'list', 'number',
                        'quantity', 'string', 'language_qualified_string',
                        'location_coordinates', 'date_and_times', 'extension',
                        'boolean', 'symbol']).
  --fields [{list_len,data_type,valid,text,decoded_text,language,language_suffix,numberstr,number,low_tolerancestr,low_tolerance,high_tolerancestr,high_tolerance,si_units,units_node,latitudestr,latitude,longitudestr,longitude,date,time,date_and_time,yearstr,year,monthstr,month,daystr,day,hourstr,hour,minutesstr,minutes,secondsstr,seconds,zonestr,precisionstr,precision,iso8601extended,truth,symbol} [{list_len,data_type,valid,text,decoded_text,language,language_suffix,numberstr,number,low_tolerancestr,low_tolerance,high_tolerancestr,high_tolerance,si_units,units_node,latitudestr,latitude,longitudestr,longitude,date,time,date_and_time,yearstr,year,monthstr,month,daystr,day,hourstr,hour,minutesstr,minutes,secondsstr,seconds,zonestr,precisionstr,precision,iso8601extended,truth,symbol} ...]]
                        The names of the fields to extract (overrides
                        --types). (default=None).
  --prefix PREFIX       The prefix for exploded column names.
                        (default=node2;kgtk:).
  --overwrite [True|False]
                        Indicate that it is OK to overwrite existing columns.
                        (default=False).
  --expand [True|False]
                        When True, expand source cells that contain a lists,
                        else fail if a source cell contains a list.
                        (default=False).
  --show-data-types [True|False]
                        Print the list of data types and exit.
                        (default=False).
  --show-field-names [True|False]
                        Print the list of field names and exit.
                        (default=False).
  --show-field-formats [True|False]
                        Print the list of field names and formats, then exit.
                        (default=False).
  --output-format {csv,json,json-map,json-map-compact,jsonl,jsonl-map,jsonl-map-compact,kgtk,md,tsv,tsv-csvlike,tsv-unquoted,tsv-unquoted-ep}
                        The file format (default=kgtk)

Error and feedback messages:
  Send error messages and feedback to stderr or stdout, control the amount of feedback and debugging messages.

  --errors-to-stdout [optional True|False]
                        Send errors to stdout instead of stderr.
                        (default=False).
  --errors-to-stderr [optional True|False]
                        Send errors to stderr instead of stdout.
                        (default=False).
  --show-options [optional True|False]
                        Print the options selected (default=False).
  -v [optional True|False], --verbose [optional True|False]
                        Print additional progress messages (default=False).
  --very-verbose [optional True|False]
                        Print additional progress messages (default=False).

File options:
  Options affecting processing.

  --column-separator COLUMN_SEPARATOR
                        Column separator (default=<TAB>).
  --input-format INPUT_FORMAT
                        Specify the input format (default=None).
  --compression-type COMPRESSION_TYPE
                        Specify the compression type (default=None).
  --error-limit ERROR_LIMIT
                        The maximum number of errors to report before failing
                        (default=1000)
  --use-mgzip [optional True|False]
                        Execute multithreaded gzip. (default=False).
  --mgzip-threads MGZIP_THREADS
                        Multithreaded gzip thread count. (default=3).
  --gzip-in-parallel [optional True|False]
                        Execute gzip in parallel. (default=False).
  --gzip-queue-size GZIP_QUEUE_SIZE
                        Queue size for parallel gzip. (default=1000).
  --mode {NONE,EDGE,NODE,AUTO}
                        Determine the KGTK file mode
                        (default=KgtkReaderMode.AUTO).
  --prohibit-whitespace-in-column-names [optional True|False]
                        Prohibit whitespace in column names. (default=False).

Header parsing:
  Options affecting header parsing.

  --force-column-names FORCE_COLUMN_NAMES [FORCE_COLUMN_NAMES ...]
                        Force the column names (default=None).
  --header-error-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}
                        The action to take when a header error is detected.
                        Only ERROR or EXIT are supported
                        (default=ValidationAction.EXIT).
  --skip-header-record [optional True|False]
                        Skip the first record when forcing column names
                        (default=False).
  --unsafe-column-name-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}
                        The action to take when a column name is unsafe
                        (default=ValidationAction.REPORT).

Pre-validation sampling:
  Options affecting pre-validation data line sampling.

  --initial-skip-count INITIAL_SKIP_COUNT
                        The number of data records to skip initially
                        (default=do not skip).
  --every-nth-record EVERY_NTH_RECORD
                        Pass every nth record (default=pass all records).
  --record-limit RECORD_LIMIT
                        Limit the number of records read (default=no limit).
  --tail-count TAIL_COUNT
                        Pass this number of records (default=no tail
                        processing).

Line parsing:
  Options affecting data line parsing.

  --repair-and-validate-lines [optional True|False]
                        Repair and validate lines (default=False).
  --repair-and-validate-values [optional True|False]
                        Repair and validate values (default=False).
  --blank-required-field-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}
                        The action to take when a line with a blank node1,
                        node2, or id field (per mode) is detected
                        (default=ValidationAction.EXCLUDE).
  --comment-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}
                        The action to take when a comment line is detected
                        (default=ValidationAction.EXCLUDE).
  --empty-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}
                        The action to take when an empty line is detected
                        (default=ValidationAction.EXCLUDE).
  --fill-short-lines [optional True|False]
                        Fill missing trailing columns in short lines with
                        empty values (default=False).
  --invalid-value-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}
                        The action to take when a data cell value is invalid
                        (default=ValidationAction.COMPLAIN).
  --long-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}
                        The action to take when a long line is detected
                        (default=ValidationAction.COMPLAIN).
  --prohibited-list-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}
                        The action to take when a data cell contains a
                        prohibited list (default=ValidationAction.COMPLAIN).
  --short-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}
                        The action to take when a short line is detected
                        (default=ValidationAction.COMPLAIN).
  --truncate-long-lines [TRUNCATE_LONG_LINES]
                        Remove excess trailing columns in long lines
                        (default=False).
  --whitespace-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}
                        The action to take when a whitespace line is detected
                        (default=ValidationAction.EXCLUDE).

Data value parsing:
  Options controlling the parsing and processing of KGTK data values.

  --additional-language-codes [ADDITIONAL_LANGUAGE_CODES [ADDITIONAL_LANGUAGE_CODES ...]]
                        Additional language codes. (default=use internal
                        list).
  --allow-lax-qnodes [ALLOW_LAX_QNODES]
                        Allow qnode suffixes in quantities to include alphas
                        and dash as well as digits. (default=False).
  --allow-language-suffixes [ALLOW_LANGUAGE_SUFFIXES]
                        Allow language identifier suffixes starting with a
                        dash. (default=False).
  --allow-lax-strings [ALLOW_LAX_STRINGS]
                        Do not check if double quotes are backslashed inside
                        strings. (default=False).
  --allow-lax-lq-strings [ALLOW_LAX_LQ_STRINGS]
                        Do not check if single quotes are backslashed inside
                        language qualified strings. (default=False).
  --allow-wikidata-lq-strings [ALLOW_WIKIDATA_LQ_STRINGS]
                        Allow Wikidata language qualifiers. (default=False).
  --require-iso8601-extended [REQUIRE_ISO8601_EXTENDED]
                        Require colon(:) and hyphen(-) in dates and times.
                        (default=False).
  --force-iso8601-extended [FORCE_ISO8601_EXTENDED]
                        Force colon (:) and hyphen(-) in dates and times.
                        (default=False).
  --allow-month-or-day-zero [ALLOW_MONTH_OR_DAY_ZERO]
                        Allow month or day zero in dates. (default=False).
  --repair-month-or-day-zero [REPAIR_MONTH_OR_DAY_ZERO]
                        Repair month or day zero in dates. (default=False).
  --allow-end-of-day [ALLOW_END_OF_DAY]
                        Allow 24:00:00 to represent the end of the day.
                        (default=True).
  --minimum-valid-year MINIMUM_VALID_YEAR
                        The minimum valid year in dates. (default=1583).
  --clamp-minimum-year [CLAMP_MINIMUM_YEAR]
                        Clamp years at the minimum value. (default=False).
  --ignore-minimum-year [IGNORE_MINIMUM_YEAR]
                        Ignore the minimum year constraint. (default=False).
  --maximum-valid-year MAXIMUM_VALID_YEAR
                        The maximum valid year in dates. (default=2100).
  --clamp-maximum-year [CLAMP_MAXIMUM_YEAR]
                        Clamp years at the maximum value. (default=False).
  --ignore-maximum-year [IGNORE_MAXIMUM_YEAR]
                        Ignore the maximum year constraint. (default=False).
  --validate-fromisoformat [VALIDATE_FROMISOFORMAT]
                        Validate that datetim.fromisoformat(...) can parse
                        this date and time. This checks that the
                        year/month/day combination is valid. The year must be
                        in the range 1..9999, inclusive. (default=False).
  --allow-lax-coordinates [ALLOW_LAX_COORDINATES]
                        Allow coordinates using scientific notation.
                        (default=False).
  --repair-lax-coordinates [REPAIR_LAX_COORDINATES]
                        Allow coordinates using scientific notation.
                        (default=False).
  --allow-out-of-range-coordinates [ALLOW_OUT_OF_RANGE_COORDINATES]
                        Allow coordinates that don't make sense.
                        (default=False).
  --minimum-valid-lat MINIMUM_VALID_LAT
                        The minimum valid latitude. (default=-90.000000).
  --clamp-minimum-lat [CLAMP_MINIMUM_LAT]
                        Clamp latitudes at the minimum value. (default=False).
  --maximum-valid-lat MAXIMUM_VALID_LAT
                        The maximum valid latitude. (default=90.000000).
  --clamp-maximum-lat [CLAMP_MAXIMUM_LAT]
                        Clamp latitudes at the maximum value. (default=False).
  --minimum-valid-lon MINIMUM_VALID_LON
                        The minimum valid longitude. (default=-180.000000).
  --clamp-minimum-lon [CLAMP_MINIMUM_LON]
                        Clamp longitudes at the minimum value.
                        (default=False).
  --maximum-valid-lon MAXIMUM_VALID_LON
                        The maximum valid longitude. (default=180.000000).
  --clamp-maximum-lon [CLAMP_MAXIMUM_LON]
                        Clamp longitudes at the maximum value.
                        (default=False).
  --modulo-repair-lon [MODULO_REPAIR_LON]
                        Wrap longitude to (-180.0,180.0]. (default=False).
  --escape-list-separators [ESCAPE_LIST_SEPARATORS]
                        Escape all list separators instead of splitting on
                        them. (default=False).
```

## Examples

### Sample Data

Suppose that `file1.tsv` contains the following table in KGTK format:

```bash
kgtk cat -i examples/docs/explode-file1.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| john | string | "John" |
| john | lqstring | 'John'@en |
| john | integer | 12345 |
| john | number | 186.2 |
| john | number | 186.2e04 |
| john | number | -186.2 |
| john | number | +186.2e-6 |
| john | quantity | 84.3[84,85]kg |
| john | date_and_time | ^1960-11-05T00:00 |
| john | date_and_time | ^1980-11-05T00:00Z/6 |
| john | date_and_time | ^1990-12-07T13:45Z/6 |
| john | date_and_time | ^2005-03-22T13:40:15Z/6 |
| john | location | @60.2/134.3 |
| john | boolean | True |
| john | symbol | quadrature |
| john | list | home\|work |


### Default Explode Operation

Explode the default column (`node2`) using the default settings.

```bash
kgtk explode -i examples/docs/explode-file1.tsv
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
| john | date_and_time | ^1990-12-07T13:45Z/6 | date_and_times | True | 0 |  |  |  |  |  |  |  |  |  |  | "1990-12-07T13:45Z" | 6 |  |  |
| john | date_and_time | ^2005-03-22T13:40:15Z/6 | date_and_times | True | 0 |  |  |  |  |  |  |  |  |  |  | "2005-03-22T13:40:15Z" | 6 |  |  |
| john | location | @60.2/134.3 | location_coordinates | True | 0 |  |  |  |  |  |  |  |  | 60.2 | 134.3 |  |  |  |  |
| john | boolean | True | boolean | True | 0 |  |  |  |  |  |  |  |  |  |  |  |  | True |  |
| john | symbol | quadrature | symbol | True | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  | quadrature |
| john | list | home\|work | list | True | 2 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

### Explode a Specific Column

Explode a specific column (`node1`, in this case) using the default settings.

```bash
kgtk explode -i examples/docs/explode-file1.tsv \
             --column node1
```

The output will be the following table in KGTK format:

| node1 | label | node2 | node2;kgtk:data_type | node2;kgtk:valid | node2;kgtk:list_len | node2;kgtk:number | node2;kgtk:low_tolerance | node2;kgtk:high_tolerance | node2;kgtk:si_units | node2;kgtk:units_node | node2;kgtk:text | node2;kgtk:language | node2;kgtk:language_suffix | node2;kgtk:latitude | node2;kgtk:longitude | node2;kgtk:date_and_time | node2;kgtk:precision | node2;kgtk:truth | node2;kgtk:symbol |
| -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- |
| john | string | "John" | symbol | True | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  | john |
| john | lqstring | 'John'@en | symbol | True | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  | john |
| john | integer | 12345 | symbol | True | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  | john |
| john | number | 186.2 | symbol | True | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  | john |
| john | number | 186.2e04 | symbol | True | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  | john |
| john | number | -186.2 | symbol | True | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  | john |
| john | number | +186.2e-6 | symbol | True | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  | john |
| john | quantity | 84.3[84,85]kg | symbol | True | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  | john |
| john | date_and_time | ^1960-11-05T00:00 | symbol | True | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  | john |
| john | date_and_time | ^1980-11-05T00:00Z/6 | symbol | True | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  | john |
| john | date_and_time | ^1990-12-07T13:45Z/6 | symbol | True | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  | john |
| john | date_and_time | ^2005-03-22T13:40:15Z/6 | symbol | True | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  | john |
| john | location | @60.2/134.3 | symbol | True | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  | john |
| john | boolean | True | symbol | True | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  | john |
| john | symbol | quadrature | symbol | True | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  | john |
| john | list | home\|work | symbol | True | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  | john |

### Explode Only Strings

Explode the default column (`node`) and only the `string` KGTK datatype.

```bash
kgtk explode -i examples/docs/explode-file1.tsv \
             --type string
```

The output will be the following table in KGTK format:

| node1 | label | node2 | node2;kgtk:data_type | node2;kgtk:valid | node2;kgtk:text |
| -- | -- | -- | -- | -- | -- |
| john | string | "John" | string | True | "John" |
| john | lqstring | 'John'@en | language_qualified_string | True | "John" |
| john | integer | 12345 | number | True |  |
| john | number | 186.2 | number | True |  |
| john | number | 186.2e04 | number | True |  |
| john | number | -186.2 | number | True |  |
| john | number | +186.2e-6 | number | True |  |
| john | quantity | 84.3[84,85]kg | quantity | True |  |
| john | date_and_time | ^1960-11-05T00:00 | date_and_times | True |  |
| john | date_and_time | ^1980-11-05T00:00Z/6 | date_and_times | True |  |
| john | date_and_time | ^1990-12-07T13:45Z/6 | date_and_times | True |  |
| john | date_and_time | ^2005-03-22T13:40:15Z/6 | date_and_times | True |  |
| john | location | @60.2/134.3 | location_coordinates | True |  |
| john | boolean | True | boolean | True |  |
| john | symbol | quadrature | symbol | True |  |
| john | list | home\|work | list | True |  |

### Explode Only Language-Qualified Strings

Explode the default column (`node`) and only the `language_qualified_string` KGTK datatype.

```bash
kgtk explode -i examples/docs/explode-file1.tsv \
             --type language_qualified_string
```

The output will be the following table in KGTK format:

| node1 | label | node2 | node2;kgtk:data_type | node2;kgtk:valid | node2;kgtk:text | node2;kgtk:language | node2;kgtk:language_suffix |
| -- | -- | -- | -- | -- | -- | -- | -- |
| john | string | "John" | string | True | "John" |  |  |
| john | lqstring | 'John'@en | language_qualified_string | True | "John" | en |  |
| john | integer | 12345 | number | True |  |  |  |
| john | number | 186.2 | number | True |  |  |  |
| john | number | 186.2e04 | number | True |  |  |  |
| john | number | -186.2 | number | True |  |  |  |
| john | number | +186.2e-6 | number | True |  |  |  |
| john | quantity | 84.3[84,85]kg | quantity | True |  |  |  |
| john | date_and_time | ^1960-11-05T00:00 | date_and_times | True |  |  |  |
| john | date_and_time | ^1980-11-05T00:00Z/6 | date_and_times | True |  |  |  |
| john | date_and_time | ^1990-12-07T13:45Z/6 | date_and_times | True |  |  |  |
| john | date_and_time | ^2005-03-22T13:40:15Z/6 | date_and_times | True |  |  |  |
| john | location | @60.2/134.3 | location_coordinates | True |  |  |  |
| john | boolean | True | boolean | True |  |  |  |
| john | symbol | quadrature | symbol | True |  |  |  |
| john | list | home\|work | list | True |  |  |  |

### Explode Both Strings and Language-Qualified Strings

Explode the default column (`node`) and both the `string` and `language_qualified_string` KGTK datatypes.

```bash
kgtk explode -i examples/docs/explode-file1.tsv \
             --type string language_qualified_string
```

The output will be the following table in KGTK format:

| node1 | label | node2 | node2;kgtk:data_type | node2;kgtk:valid | node2;kgtk:text | node2;kgtk:language | node2;kgtk:language_suffix |
| -- | -- | -- | -- | -- | -- | -- | -- |
| john | string | "John" | string | True | "John" |  |  |
| john | lqstring | 'John'@en | language_qualified_string | True | "John" | en |  |
| john | integer | 12345 | number | True |  |  |  |
| john | number | 186.2 | number | True |  |  |  |
| john | number | 186.2e04 | number | True |  |  |  |
| john | number | -186.2 | number | True |  |  |  |
| john | number | +186.2e-6 | number | True |  |  |  |
| john | quantity | 84.3[84,85]kg | quantity | True |  |  |  |
| john | date_and_time | ^1960-11-05T00:00 | date_and_times | True |  |  |  |
| john | date_and_time | ^1980-11-05T00:00Z/6 | date_and_times | True |  |  |  |
| john | date_and_time | ^1990-12-07T13:45Z/6 | date_and_times | True |  |  |  |
| john | date_and_time | ^2005-03-22T13:40:15Z/6 | date_and_times | True |  |  |  |
| john | location | @60.2/134.3 | location_coordinates | True |  |  |  |
| john | boolean | True | boolean | True |  |  |  |
| john | symbol | quadrature | symbol | True |  |  |  |
| john | list | home\|work | list | True |  |  |  |

### Explode Only Numbers

Explode the default column (`node`) and only the `number` KGTK datatype.

```bash
kgtk explode -i examples/docs/explode-file1.tsv \
             --type number
```

The output will be the following table in KGTK format:

| node1 | label | node2 | node2;kgtk:data_type | node2;kgtk:valid | node2;kgtk:number |
| -- | -- | -- | -- | -- | -- |
| john | string | "John" | string | True |  |
| john | lqstring | 'John'@en | language_qualified_string | True |  |
| john | integer | 12345 | number | True | 12345 |
| john | number | 186.2 | number | True | 186.2 |
| john | number | 186.2e04 | number | True | 1862000.0 |
| john | number | -186.2 | number | True | -186.2 |
| john | number | +186.2e-6 | number | True | 0.0001862 |
| john | quantity | 84.3[84,85]kg | quantity | True | 84.3 |
| john | date_and_time | ^1960-11-05T00:00 | date_and_times | True |  |
| john | date_and_time | ^1980-11-05T00:00Z/6 | date_and_times | True |  |
| john | date_and_time | ^1990-12-07T13:45Z/6 | date_and_times | True |  |
| john | date_and_time | ^2005-03-22T13:40:15Z/6 | date_and_times | True |  |
| john | location | @60.2/134.3 | location_coordinates | True |  |
| john | boolean | True | boolean | True |  |
| john | symbol | quadrature | symbol | True |  |
| john | list | home\|work | list | True |  |

### Explode Only Quantities

Explode the default column (`node`) and only the `quantity` KGTK datatype.

```bash
kgtk explode -i examples/docs/explode-file1.tsv \
             --type quantity
```

The output will be the following table in KGTK format:

| node1 | label | node2 | node2;kgtk:data_type | node2;kgtk:valid | node2;kgtk:number | node2;kgtk:low_tolerance | node2;kgtk:high_tolerance | node2;kgtk:si_units | node2;kgtk:units_node |
| -- | -- | -- | -- | -- | -- | -- | -- | -- | -- |
| john | string | "John" | string | True |  |  |  |  |  |
| john | lqstring | 'John'@en | language_qualified_string | True |  |  |  |  |  |
| john | integer | 12345 | number | True | 12345 |  |  |  |  |
| john | number | 186.2 | number | True | 186.2 |  |  |  |  |
| john | number | 186.2e04 | number | True | 1862000.0 |  |  |  |  |
| john | number | -186.2 | number | True | -186.2 |  |  |  |  |
| john | number | +186.2e-6 | number | True | 0.0001862 |  |  |  |  |
| john | quantity | 84.3[84,85]kg | quantity | True | 84.3 | 84.0 | 85.0 | kg |  |
| john | date_and_time | ^1960-11-05T00:00 | date_and_times | True |  |  |  |  |  |
| john | date_and_time | ^1980-11-05T00:00Z/6 | date_and_times | True |  |  |  |  |  |
| john | date_and_time | ^1990-12-07T13:45Z/6 | date_and_times | True |  |  |  |  |  |
| john | date_and_time | ^2005-03-22T13:40:15Z/6 | date_and_times | True |  |  |  |  |  |
| john | location | @60.2/134.3 | location_coordinates | True |  |  |  |  |  |
| john | boolean | True | boolean | True |  |  |  |  |  |
| john | symbol | quadrature | symbol | True |  |  |  |  |  |
| john | list | home\|work | list | True |  |  |  |  |  |

### Explode Both Numbers and Quantities

Explode the default column (`node`) and both the `number` and `quantity` KGTK datatypes.

```bash
kgtk explode -i examples/docs/explode-file1.tsv \
             --type number quantity
```

The output will be the following table in KGTK format:

| node1 | label | node2 | node2;kgtk:data_type | node2;kgtk:valid | node2;kgtk:number | node2;kgtk:low_tolerance | node2;kgtk:high_tolerance | node2;kgtk:si_units | node2;kgtk:units_node |
| -- | -- | -- | -- | -- | -- | -- | -- | -- | -- |
| john | string | "John" | string | True |  |  |  |  |  |
| john | lqstring | 'John'@en | language_qualified_string | True |  |  |  |  |  |
| john | integer | 12345 | number | True | 12345 |  |  |  |  |
| john | number | 186.2 | number | True | 186.2 |  |  |  |  |
| john | number | 186.2e04 | number | True | 1862000.0 |  |  |  |  |
| john | number | -186.2 | number | True | -186.2 |  |  |  |  |
| john | number | +186.2e-6 | number | True | 0.0001862 |  |  |  |  |
| john | quantity | 84.3[84,85]kg | quantity | True | 84.3 | 84.0 | 85.0 | kg |  |
| john | date_and_time | ^1960-11-05T00:00 | date_and_times | True |  |  |  |  |  |
| john | date_and_time | ^1980-11-05T00:00Z/6 | date_and_times | True |  |  |  |  |  |
| john | date_and_time | ^1990-12-07T13:45Z/6 | date_and_times | True |  |  |  |  |  |
| john | date_and_time | ^2005-03-22T13:40:15Z/6 | date_and_times | True |  |  |  |  |  |
| john | location | @60.2/134.3 | location_coordinates | True |  |  |  |  |  |
| john | boolean | True | boolean | True |  |  |  |  |  |
| john | symbol | quadrature | symbol | True |  |  |  |  |  |
| john | list | home\|work | list | True |  |  |  |  |  |

### Explode Only Dates and Times

Explode the default column (`node`) and only the `date_and_times` KGTK datatype.

```bash
kgtk explode -i examples/docs/explode-file1.tsv \
             --type date_and_times
```

The output will be the following table in KGTK format:

| node1 | label | node2 | node2;kgtk:data_type | node2;kgtk:valid | node2;kgtk:date_and_time | node2;kgtk:precision |
| -- | -- | -- | -- | -- | -- | -- |
| john | string | "John" | string | True |  |  |
| john | lqstring | 'John'@en | language_qualified_string | True |  |  |
| john | integer | 12345 | number | True |  |  |
| john | number | 186.2 | number | True |  |  |
| john | number | 186.2e04 | number | True |  |  |
| john | number | -186.2 | number | True |  |  |
| john | number | +186.2e-6 | number | True |  |  |
| john | quantity | 84.3[84,85]kg | quantity | True |  |  |
| john | date_and_time | ^1960-11-05T00:00 | date_and_times | True | "1960-11-05T00:00" |  |
| john | date_and_time | ^1980-11-05T00:00Z/6 | date_and_times | True | "1980-11-05T00:00Z" | 6 |
| john | date_and_time | ^1990-12-07T13:45Z/6 | date_and_times | True | "1990-12-07T13:45Z" | 6 |
| john | date_and_time | ^2005-03-22T13:40:15Z/6 | date_and_times | True | "2005-03-22T13:40:15Z" | 6 |
| john | location | @60.2/134.3 | location_coordinates | True |  |  |
| john | boolean | True | boolean | True |  |  |
| john | symbol | quadrature | symbol | True |  |  |
| john | list | home\|work | list | True |  |  |

### Explode Only Location Coordinates

Explode the default column (`node`) and only the `location_coordinates` KGTK datatype.

```bash
kgtk explode -i examples/docs/explode-file1.tsv \
             --type location_coordinates
```

The output will be the following table in KGTK format:

| node1 | label | node2 | node2;kgtk:data_type | node2;kgtk:valid | node2;kgtk:latitude | node2;kgtk:longitude |
| -- | -- | -- | -- | -- | -- | -- |
| john | string | "John" | string | True |  |  |
| john | lqstring | 'John'@en | language_qualified_string | True |  |  |
| john | integer | 12345 | number | True |  |  |
| john | number | 186.2 | number | True |  |  |
| john | number | 186.2e04 | number | True |  |  |
| john | number | -186.2 | number | True |  |  |
| john | number | +186.2e-6 | number | True |  |  |
| john | quantity | 84.3[84,85]kg | quantity | True |  |  |
| john | date_and_time | ^1960-11-05T00:00 | date_and_times | True |  |  |
| john | date_and_time | ^1980-11-05T00:00Z/6 | date_and_times | True |  |  |
| john | date_and_time | ^1990-12-07T13:45Z/6 | date_and_times | True |  |  |
| john | date_and_time | ^2005-03-22T13:40:15Z/6 | date_and_times | True |  |  |
| john | location | @60.2/134.3 | location_coordinates | True | 60.2 | 134.3 |
| john | boolean | True | boolean | True |  |  |
| john | symbol | quadrature | symbol | True |  |  |
| john | list | home\|work | list | True |  |  |

### Explode Only Booleans

Explode the default column (`node`) and only the `boolean` KGTK datatype.

```bash
kgtk explode -i examples/docs/explode-file1.tsv \
             --type boolean
```

The output will be the following table in KGTK format:

| node1 | label | node2 | node2;kgtk:data_type | node2;kgtk:valid | node2;kgtk:truth |
| -- | -- | -- | -- | -- | -- |
| john | string | "John" | string | True |  |
| john | lqstring | 'John'@en | language_qualified_string | True |  |
| john | integer | 12345 | number | True |  |
| john | number | 186.2 | number | True |  |
| john | number | 186.2e04 | number | True |  |
| john | number | -186.2 | number | True |  |
| john | number | +186.2e-6 | number | True |  |
| john | quantity | 84.3[84,85]kg | quantity | True |  |
| john | date_and_time | ^1960-11-05T00:00 | date_and_times | True |  |
| john | date_and_time | ^1980-11-05T00:00Z/6 | date_and_times | True |  |
| john | date_and_time | ^1990-12-07T13:45Z/6 | date_and_times | True |  |
| john | date_and_time | ^2005-03-22T13:40:15Z/6 | date_and_times | True |  |
| john | location | @60.2/134.3 | location_coordinates | True |  |
| john | boolean | True | boolean | True | True |
| john | symbol | quadrature | symbol | True |  |
| john | list | home\|work | list | True |  |

### Explode Only Symbols

Explode the default column (`node`) and only the `symbol` KGTK datatype.

```bash
kgtk explode -i examples/docs/explode-file1.tsv \
             --type symbol
```

The output will be the following table in KGTK format:

| node1 | label | node2 | node2;kgtk:data_type | node2;kgtk:valid | node2;kgtk:symbol |
| -- | -- | -- | -- | -- | -- |
| john | string | "John" | string | True |  |
| john | lqstring | 'John'@en | language_qualified_string | True |  |
| john | integer | 12345 | number | True |  |
| john | number | 186.2 | number | True |  |
| john | number | 186.2e04 | number | True |  |
| john | number | -186.2 | number | True |  |
| john | number | +186.2e-6 | number | True |  |
| john | quantity | 84.3[84,85]kg | quantity | True |  |
| john | date_and_time | ^1960-11-05T00:00 | date_and_times | True |  |
| john | date_and_time | ^1980-11-05T00:00Z/6 | date_and_times | True |  |
| john | date_and_time | ^1990-12-07T13:45Z/6 | date_and_times | True |  |
| john | date_and_time | ^2005-03-22T13:40:15Z/6 | date_and_times | True |  |
| john | location | @60.2/134.3 | location_coordinates | True |  |
| john | boolean | True | boolean | True |  |
| john | symbol | quadrature | symbol | True | quadrature |
| john | list | home\|work | list | True |  |

### Expand a List and Explode

Explode the default column (`node`) and only the `symbol` KGTK datatype.

```bash
kgtk explode -i examples/docs/explode-file1.tsv \
             --expand \
             --type symbol
```

The output will be the following table in KGTK format:

| node1 | label | node2 | node2;kgtk:data_type | node2;kgtk:valid | node2;kgtk:symbol |
| -- | -- | -- | -- | -- | -- |
| john | string | "John" | string | True |  |
| john | lqstring | 'John'@en | language_qualified_string | True |  |
| john | integer | 12345 | number | True |  |
| john | number | 186.2 | number | True |  |
| john | number | 186.2e04 | number | True |  |
| john | number | -186.2 | number | True |  |
| john | number | +186.2e-6 | number | True |  |
| john | quantity | 84.3[84,85]kg | quantity | True |  |
| john | date_and_time | ^1960-11-05T00:00 | date_and_times | True |  |
| john | date_and_time | ^1980-11-05T00:00Z/6 | date_and_times | True |  |
| john | date_and_time | ^1990-12-07T13:45Z/6 | date_and_times | True |  |
| john | date_and_time | ^2005-03-22T13:40:15Z/6 | date_and_times | True |  |
| john | location | @60.2/134.3 | location_coordinates | True |  |
| john | boolean | True | boolean | True |  |
| john | symbol | quadrature | symbol | True | quadrature |
| john | list | home\|work | symbol | True | home |
| john | list | home\|work | symbol | True | work |

### Explode Without a Prefix

Explode the default column (`node2`) using the default settings, except without a prefix in the new column names.

```bash
kgtk explode -i examples/docs/explode-file1.tsv \
             --prefix=
```

The output will be the following table in KGTK format:

| node1 | label | node2 | data_type | valid | list_len | number | low_tolerance | high_tolerance | si_units | units_node | text | language | language_suffix | latitude | longitude | date_and_time | precision | truth | symbol |
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
| john | date_and_time | ^1990-12-07T13:45Z/6 | date_and_times | True | 0 |  |  |  |  |  |  |  |  |  |  | "1990-12-07T13:45Z" | 6 |  |  |
| john | date_and_time | ^2005-03-22T13:40:15Z/6 | date_and_times | True | 0 |  |  |  |  |  |  |  |  |  |  | "2005-03-22T13:40:15Z" | 6 |  |  |
| john | location | @60.2/134.3 | location_coordinates | True | 0 |  |  |  |  |  |  |  |  | 60.2 | 134.3 |  |  |  |  |
| john | boolean | True | boolean | True | 0 |  |  |  |  |  |  |  |  |  |  |  |  | True |  |
| john | symbol | quadrature | symbol | True | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  | quadrature |
| john | list | home\|work | list | True | 2 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

### Explode to Get Just the KGTK Data Type

Explode the default column (`node2`), extracting just the `data_type` field.

```bash
kgtk explode -i examples/docs/explode-file1.tsv \
             --field=data_type
```

The output will be the following table in KGTK format:

| node1 | label | node2 | node2;kgtk:data_type |
| -- | -- | -- | -- |
| john | string | "John" | string |
| john | lqstring | 'John'@en | language_qualified_string |
| john | integer | 12345 | number |
| john | number | 186.2 | number |
| john | number | 186.2e04 | number |
| john | number | -186.2 | number |
| john | number | +186.2e-6 | number |
| john | quantity | 84.3[84,85]kg | quantity |
| john | date_and_time | ^1960-11-05T00:00 | date_and_times |
| john | date_and_time | ^1980-11-05T00:00Z/6 | date_and_times |
| john | date_and_time | ^1990-12-07T13:45Z/6 | date_and_times |
| john | date_and_time | ^2005-03-22T13:40:15Z/6 | date_and_times |
| john | location | @60.2/134.3 | location_coordinates |
| john | boolean | True | boolean |
| john | symbol | quadrature | symbol |
| john | list | home\|work | list |

### Error: Explode with Overwriting Not Enabled

Explode the default column (`node2`), extracting just the `data_type` field,
using an input file that already has a `node2;kgtk:data_type1 field`, without
enabling `--overwrite`.

```bash
kgtk cat -i examples/docs/explode-file2.tsv
```

| node1 | label | node2 | node2;kgtk:data_type |
| -- | -- | -- | -- |
| john | string | "John" |  |
| john | lqstring | 'John'@en |  |
| john | integer | 12345 |  |
| john | number | 186.2 |  |
| john | number | 186.2e04 |  |
| john | number | -186.2 |  |
| john | number | +186.2e-6 |  |
| john | quantity | 84.3[84,85]kg |  |
| john | date_and_time | ^1960-11-05T00:00 |  |
| john | date_and_time | ^1980-11-05T00:00Z/6 |  |
| john | location | @60.2/134.3 |  |
| john | boolean | True |  |
| john | symbol | quadrature |  |
| john | list | home\|work |  |

```bash
kgtk explode -i examples/docs/explode-file2.tsv \
             --field=data_type
```

The output will be the following error messages on standatd output

    Exploded column 'node2;kgtk:data_type' already exists and not allowed to overwrite

### Explode with Overwriting Enabled

Explode the default column (`node2`), extracting just the `data_type` field,
using an input file that already has a `node2;kgtk:data_type1 field`, with
`--overwrite` enabled.

```bash
kgtk explode -i examples/docs/explode-file2.tsv \
             --field=data_type \
             --overwrite
```

The output will be the following table in KGTK format:

| node1 | label | node2 | node2;kgtk:data_type |
| -- | -- | -- | -- |
| john | string | "John" | string |
| john | lqstring | 'John'@en | language_qualified_string |
| john | integer | 12345 | number |
| john | number | 186.2 | number |
| john | number | 186.2e04 | number |
| john | number | -186.2 | number |
| john | number | +186.2e-6 | number |
| john | quantity | 84.3[84,85]kg | quantity |
| john | date_and_time | ^1960-11-05T00:00 | date_and_times |
| john | date_and_time | ^1980-11-05T00:00Z/6 | date_and_times |
| john | location | @60.2/134.3 | location_coordinates |
| john | boolean | True | boolean |
| john | symbol | quadrature | symbol |
| john | list | home\|work | list |

### Exploding Dates into Year Month Day Hour Minutes Seconds

Explode the default column (`node2`), extracting certain `date_and_times` fields.
Don't prefix the extracted field names.

```bash
kgtk explode -i examples/docs/explode-file1.tsv \
             --fields year month day hour minutes seconds \
	     --prefix=
```

The output will be the following table in KGTK format:

| node1 | label | node2 | year | month | day | hour | minutes | seconds |
| -- | -- | -- | -- | -- | -- | -- | -- | -- |
| john | string | "John" |  |  |  |  |  |  |
| john | lqstring | 'John'@en |  |  |  |  |  |  |
| john | integer | 12345 |  |  |  |  |  |  |
| john | number | 186.2 |  |  |  |  |  |  |
| john | number | 186.2e04 |  |  |  |  |  |  |
| john | number | -186.2 |  |  |  |  |  |  |
| john | number | +186.2e-6 |  |  |  |  |  |  |
| john | quantity | 84.3[84,85]kg |  |  |  |  |  |  |
| john | date_and_time | ^1960-11-05T00:00 | 1960 | 11 | 5 | 0 | 0 |  |
| john | date_and_time | ^1980-11-05T00:00Z/6 | 1980 | 11 | 5 | 0 | 0 |  |
| john | date_and_time | ^1990-12-07T13:45Z/6 | 1990 | 12 | 7 | 13 | 45 |  |
| john | date_and_time | ^2005-03-22T13:40:15Z/6 | 2005 | 3 | 22 | 13 | 40 | 15 |
| john | location | @60.2/134.3 |  |  |  |  |  |  |
| john | boolean | True |  |  |  |  |  |  |
| john | symbol | quadrature |  |  |  |  |  |  |
| john | list | home\|work |  |  |  |  |  |  |

### Exploding Dates into Year and Yearstr, Month and Monthstr, Day and Daystr

Explode the default column (`node2`), extracting certain `date_and_times` fields.
Don't prefix the extracted field names.

The fields without `str` at the end of the name (`year`, `month`, `day`) appear as KGTK
numbers.  The fields with `str` at the end of the name (`yearstr`, `monthstr`, `daystr`)
appear as KGTK strings.

```bash
kgtk explode -i examples/docs/explode-file1.tsv \
             --fields year yearstr month monthstr day  daystr \
	     --prefix=
```

The output will be the following table in KGTK format:

| node1 | label | node2 | year | yearstr | month | monthstr | day | daystr |
| -- | -- | -- | -- | -- | -- | -- | -- | -- |
| john | string | "John" |  |  |  |  |  |  |
| john | lqstring | 'John'@en |  |  |  |  |  |  |
| john | integer | 12345 |  |  |  |  |  |  |
| john | number | 186.2 |  |  |  |  |  |  |
| john | number | 186.2e04 |  |  |  |  |  |  |
| john | number | -186.2 |  |  |  |  |  |  |
| john | number | +186.2e-6 |  |  |  |  |  |  |
| john | quantity | 84.3[84,85]kg |  |  |  |  |  |  |
| john | date_and_time | ^1960-11-05T00:00 | 1960 | "1960" | 11 | "11" | 5 | "05" |
| john | date_and_time | ^1980-11-05T00:00Z/6 | 1980 | "1980" | 11 | "11" | 5 | "05" |
| john | date_and_time | ^1990-12-07T13:45Z/6 | 1990 | "1990" | 12 | "12" | 7 | "07" |
| john | date_and_time | ^2005-03-22T13:40:15Z/6 | 2005 | "2005" | 3 | "03" | 22 | "22" |
| john | location | @60.2/134.3 |  |  |  |  |  |  |
| john | boolean | True |  |  |  |  |  |  |
| john | symbol | quadrature |  |  |  |  |  |  |
| john | list | home\|work |  |  |  |  |  |  |
