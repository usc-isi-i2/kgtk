## Overview

This tool validates that KGTK files meet the rules in the [KGTK File Format v2](../../specification).
Error messages will be generated when rule violations are detected.
By default, most error messages are written to standard output so they may be
easily captured in a log file.

One or more KGTK files may be processed at a time.  Input files will be decompressed
automatically in certain conditions.

!!! note
    All of the validations shown here are done by KgtkReader and mey be
    enabled in any KGTK tool that uses KgtkReader to read its input files.
    `kgtk validate` enables line and data value validation by default, while
    other KGTK tools disable these processing steps by default.

### Input File Decompression

Input files may be (de)compressed using a algorithm selected
by the file extension: .bz2 .gz .lz4 .xy

The expert option --compression-type may be used to override the
decompression selection algorithm;  this is useful when reading from piped input.

### Default Rules
By default, the following rules apply:

 - errors that occur while processing a KGTK file's column header line cause an immediate exit:
    - An empty column name
    - A duplicate column name
    - A missing required column name for an edge or node file
    - An ambiguous required column name (e.g., `id` and `ID` are both present)
 - empty data lines are silently ignored and not passed through.
 - data lines containing only whitespace are silently ignored and not passed through.
 - data lines with empty required fields (node1 and node2 for KGTK edge files, id for KGTK node files) are silently ignored.
 - data lines that have too few fields cause a complaint to be issued.
 - data lines that have too many fields cause a complaint to be issued.
 - lines with data value validation errors cause a complaint to be issued.

These defaults may be changed through expert options.

### Action Codes

| Action keyword | Action when condition detected |
| -------------- | ------------------------------ |
| PASS           | Silently allow the data line to pass through |
| REPORT         | Report the data line and let it pass through |
| EXCLUDE        | Silently exclude (ignore) the data line |
| COMPLAIN       | Report the data line and exclude (ignore) it |
| ERROR          | Raise a ValueError |
| EXIT           | sys.exit(1) |

### `--header-error-action`
The action to take if a header error is detected, such as:

- An empty column name
- A duplicate column name
- A missing required column name for an edge or node file
- An ambiguous required column name (e.g., `id` and `ID` are both present)

Only ERROR and EXIT actions are implemented for header errors.

### `--unsafe-column-name`
The action to take if a header column name contains one of the following:

- Leading white space
- Trailing white space
- Internal white space except in strings or language-qualified strings
- Commas
- Vertical bars

### `--error-limit`
Execution will stop if the error limit is exceeded.  The default value is 1000 errors.
To avoid stopping at 1000 errors, either
raise the error limit or set it to zero:

  --error-limit=0

### KGTK File Mode

|Mode|Meaning|
|----|-------|
|NONE|Do not require node1, node1, or id columns|
|EDGE|Treat the input file as a KGTK edge file and require the presence of node1 and node2 columns or their allowable aliases.|
|NODE|Treat the input file as a KGTK node file and require the presence of an id column or its allowable alias (ID).|
|AUTO|Automatically determine if an input file is an edge file or a node file. If a node1 (or allowable alias) column is present, assume that the file is a KGTK edge file. Otherwise, assume that it is a KGTK node file|

### Special Column Names and Aliases

| Canonical Name | Allowed Aliases | Comments |
| -------------- | --------------- | -------- |
| `id`           | `ID`            | This is a required column in Node files, an optional one in Edge files (but may cause behavior changes if present). |
| `node1`        | `from`, `subject` | This is a required column in Edge files. It may not contain empty values. |
| `label`        | `predicate`, `relation`, `relationship` | This is a required columns in Edge files. It may contain empty values. |
| `node2`        | `to`, `object` | This is a required column in Edge files. It may not contain empty values. |

## Usage
```
usage: kgtk validate [-h] [-i INPUT_FILE [INPUT_FILE ...]]
                     [--header-only [HEADER_ONLY]]
                     [--summary [REPORT_SUMMARY]] [-v [optional True|False]]

Validate one or more KGTK files. Empty lines, whitespace lines, comment lines, and lines with empty required fields are silently skipped. Header errors cause an immediate exception. Data value errors are reported. 

To validate data and pass clean data to an output file or pipe, use the kgtk clean_data command.

Additional options are shown in expert help.
kgtk --expert validate --help

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE [INPUT_FILE ...], --input-files INPUT_FILE [INPUT_FILE ...]
                        The KGTK file(s) to validate. (May be omitted or '-'
                        for stdin.)
  --header-only [HEADER_ONLY]
                        Process the only the header of the input file
                        (default=False).
  --summary [REPORT_SUMMARY]
                        Report a summary on the lines processed.
                        (default=True).

  -v [optional True|False], --verbose [optional True|False]
                        Print additional progress messages (default=False).
```

## Expert Usage

```
usage: kgtk validate [-h] [-i INPUT_FILE [INPUT_FILE ...]]
                     [--header-only [HEADER_ONLY]]
                     [--summary [REPORT_SUMMARY]]
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

Validate one or more KGTK files. Empty lines, whitespace lines, comment lines, and lines with empty required fields are silently skipped. Header errors cause an immediate exception. Data value errors are reported. 

To validate data and pass clean data to an output file or pipe, use the kgtk clean_data command.

Additional options are shown in expert help.
kgtk --expert validate --help

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE [INPUT_FILE ...], --input-files INPUT_FILE [INPUT_FILE ...]
                        The KGTK file(s) to validate. (May be omitted or '-'
                        for stdin.)
  --header-only [HEADER_ONLY]
                        Process the only the header of the input file
                        (default=False).
  --summary [REPORT_SUMMARY]
                        Report a summary on the lines processed.
                        (default=True).

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
                        Repair and validate lines (default=True).
  --repair-and-validate-values [optional True|False]
                        Repair and validate values (default=True).
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
                        Additional language codes. (default=None).
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

### Sample Data: a Date Containing Day `00`

Suppose that `examples/docs/validate-bad-date.tsv` contains the following table in KGTK format:

```bash
kgtk cat -i examples/docs/validate-bad-date.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| john | woke | ^2020-05-00T00:00 |
| john | woke | ^2020-05-02T00:00 |

### Validate using Default Options

```bash
kgtk validate -i examples/docs/validate-bad-date.tsv
```

The following complaint and summary will be issued:

~~~
Data line 1:
john	woke	^2020-05-00T00:00
col 2 (node2) value '^2020-05-00T00:00' is an Invalid Date and Times

====================================================
Data lines read: 2
Data lines passed: 1
Data lines excluded due to invalid values: 1
Data errors reported: 1
~~~

The first data line was flagged because it contained "00" in the day
field, which violates the ISO 8601 specification.

### Validate Allowing Month or Day Zero

Instruct the validator to accept month or day 00, even though
this is not allowed in ISO 6801.

```bash
kgtk validate -i examples/docs/validate-bad-date.tsv \
              --allow-month-or-day-zero
```

This results in no error messages, and the following summary:

~~~

====================================================
Data lines read: 2
Data lines passed: 2
~~~

### Validate with Verbose Feedback

Sometimes you may wish to get more feedback about what `kgtk validate` is
doing.

```bash
kgtk validate -i examples/docs/validate-bad-date.tsv \
              --allow-month-or-day-zero \
              --verbose
```

This results in the following output:

~~~

====================================================
Validating 'examples/docs/validate-bad-date.tsv'
KgtkReader: File_path.suffix: .tsv
KgtkReader: reading file examples/docs/validate-bad-date.tsv
header: node1	label	node2
input format: kgtk
node1 column found, this is a KGTK edge file
KgtkReader: Special columns: node1=0 label=1 node2=2 id=-1
KgtkReader: Reading an edge file.
Validated 2 data lines

====================================================
Data lines read: 2
Data lines passed: 2
~~~

### Validate Only the Header

Validate only the header record, ignoring data records:

```bash
kgtk validate -i examples/docs/validate-bad-date.tsv \
              --header-only
```

~~~

====================================================
Data lines read: 0
Data lines passed: 0
~~~

### Header Error: No Header Line in File (Empty File)

Validate an empty input file:

```bash
kgtk validate -i examples/docs/validate-empty-file.tsv
```

This generates the following message on standard output:

~~~
Error: No header line in file
~~~

This also generates the following message on standard error:

    Exiting due to error

!!! note
    At the present time, the latter error message is not routable
    to standard output.

### Supply a Missing Header Line

Validate an empty input file, supplying a header line:

```bash
kgtk validate -i examples/docs/validate-empty-file.tsv \
              --force-column-names node1 label node2
```

This generates the following message on standard output:

~~~

====================================================
Data lines read: 0
Data lines passed: 0
~~~

### Header Error: No Header Line to Skip

Validate an empty input file, skipping a nonexistant header line.


```bash
kgtk validate -i examples/docs/validate-empty-file.tsv \
              --force-column-names node1 label node2 \
	      --skip-header-record 
```

This generates the following message on standard output:

~~~
Error: No header line to skip
~~~

This also generates the following message on standard error:

    Exiting due to error

!!! note
    At the present time, this latter error message is not routable
    to standard output.

### Header Error: Column Name Is Empty

Validate an input file with an empty column name:

```bash
cat examples/docs/validate-empty-column-name.tsv
```
~~~
	label	node2
~~~

```bash
kgtk validate -i examples/docs/validate-empty-column-name.tsv
```

The following error is reported on standard output:

~~~
In input header '	label	node2': Column 0 has an empty name in the file header
~~~

The following message appears on standard error:

    Exit requested

!!! note
    The `Exit requested` message cannot be routed to standard output at the present time.
    
### Header Error: See All Header Errors

Validate an input file with an empty column name.  This will generate an error
message, and normally an immediate exit.  If you want to see all header error
messages, use `--header-error-action COMPLAIN` to continue processing.

```bash
cat examples/docs/validate-empty-column-name.tsv
```
~~~
	label	node2
~~~

```bash
kgtk validate -i examples/docs/validate-empty-column-name.tsv \
              --header-error-action COMPLAIN
```

The following error is reported on standard output:

~~~
In input header '	label	node2': Column 0 has an empty name in the file header
In input header '	label	node2': Missing required column: id | ID

====================================================
Data lines read: 0
Data lines passed: 0
~~~

Processing continues without exiting.


### Header Error: Column Name Starts with White Space

Validate an input file where the intended `node1`, `label`, and `node2`
column names have initial whitespace.

```bash
cat examples/docs/validate-column-names-initial-whitespace.tsv
```
~~~
id	 node1	 label	 node2
~~~

```bash
kgtk validate -i examples/docs/validate-column-names-initial-whitespace.tsv
```

The following error is reported on standard output:

~~~
In input header 'id	 node1	 label	 node2': 
Column name ' node1' starts with leading white space
Column name ' label' starts with leading white space
Column name ' node2' starts with leading white space

====================================================
Data lines read: 0
Data lines passed: 0
~~~

### Header Error: Column Name Ends with White Space

Validate an input file where the intended `node1`, `label`, and `node2`
column names have trailing whitespace.

```bash
cat examples/docs/validate-column-names-trailing-whitespace.tsv
```
~~~
id	node1 	label 	node2 
~~~

```bash
kgtk validate -i examples/docs/validate-column-names-trailing-whitespace.tsv
```

The following error is reported on standard output:

~~~
In input header 'id	node1 	label 	node2 ': 
Column name 'node1 ' ends with trailing white space
Column name 'label ' ends with trailing white space
Column name 'node2 ' ends with trailing white space

====================================================
Data lines read: 0
Data lines passed: 0
~~~

### Header Error: Column Name Contains Internal White Space

Validate an input file where the intended `node1` and `node2`
column names have internal whitespace.

```bash
cat examples/docs/validate-column-names-internal-whitespace.tsv
```
~~~
id	node 1	label	node 2
~~~

```bash
kgtk validate -i examples/docs/validate-column-names-internal-whitespace.tsv
```

The following error is reported on standard output:

~~~

====================================================
Data lines read: 0
Data lines passed: 0
~~~

### Header Error: Column Name Contains a Comma (`,`)

Validate an input file where the intended `node1`, `label`, and `node2`
column names have a comma (`,`) at the end.

```bash
cat examples/docs/validate-column-names-with-comma.tsv
```
~~~
node1,	label,	node2,	id
~~~

```bash
kgtk validate -i examples/docs/validate-column-names-with-comma.tsv
```

The following error is reported on standard output:

~~~
In input header 'node1,	label,	node2,	id': 
Warning: Column name 'node1,' contains a comma (,)
Warning: Column name 'label,' contains a comma (,)
Warning: Column name 'node2,' contains a comma (,)

====================================================
Data lines read: 0
Data lines passed: 0
~~~

### Header Error: Column Name Contains a Vertical Bar (`|`)

Validate an input file where the intended `node1`, `label`, and `node2`
column names have a vertical bar (`|) at the end.

```bash
kgtk validate -i examples/docs/validate-column-names-with-vertical-bar.tsv
```

The following warnings is reported on standard output:

~~~
In input header 'node1|	label|	node2|	id': 
Warning: Column name 'node1|' contains a vertical bar (|)
Warning: Column name 'label|' contains a vertical bar (|)
Warning: Column name 'node2|' contains a vertical bar (|)

====================================================
Data lines read: 0
Data lines passed: 0
~~~

### Header Error: Column Name Is a Duplicate

Validate an input file with two `node1` columns instead of
`node1` and `node2` columns.

```bash
cat examples/docs/validate-column-names-with-duplicates.tsv
```
~~~
node1	label	node1	id
~~~

```bash
kgtk validate -i examples/docs/validate-column-names-with-duplicates.tsv
```

The following error is reported on standard output:

~~~
In input header 'node1	label	node1	id': Column 2 (node1) is a duplicate of column 0
~~~

The following is reported on standard error:

    Exit requested

### Header Error: Missing Required Column in a Node File

Validate an input file as a KGTK Node file when the input
file does not have the required column (`id`) for a Node file.  We force
the file to be treated as a Node file by specifying `--mode=NODE`.

```bash
cat examples/docs/validate-column-names-without-required-columns.tsv
```
~~~
col1	col2	col3
~~~

```bash
kgtk validate -i examples/docs/validate-column-names-without-required-columns.tsv \
              --mode=NODE
```

The following error is reported on standard output:

~~~
In input header 'col1	col2	col3': Missing required column: id | ID
~~~

The following is reported on standard error:

    Exit requested

### Header Error: Missing Required Columns in an Edge File

Validate an input file as a KGTK Edge file when the input
file does not have the required columns (`node1`, `label`, `node2`) for a Edge file.  We force
the file to be treated as a Edge file by specifying `--mode=EDGE`.

```bash
cat examples/docs/validate-column-names-without-required-columns.tsv
```
~~~
col1	col2	col3
~~~

```bash
kgtk validate -i examples/docs/validate-column-names-without-required-columns.tsv \
              --mode=EDGE
```

The following error is reported on standard output:

~~~
In input header 'col1	col2	col3': Missing required column: node1 | from | subject
~~~

The following is reported on standard error:

    Exit requested

### Header Error: Missing Required Column with `--mode=AUTO`

Validate an input file when the input
file does not have the required columns for as Edge or Node file,
and we force auto-mode sensing with `--mode=AUTO`.

```bash
cat examples/docs/validate-column-names-without-required-columns.tsv
```
~~~
col1	col2	col3
~~~

```bash
kgtk validate -i examples/docs/validate-column-names-without-required-columns.tsv \
              --mode=AUTO
```

The following error is reported on standard output:

~~~
In input header 'col1	col2	col3': Missing required column: id | ID
~~~

The following is reported on standard error:

    Exit requested

### Note: No Columns are Required with `--mode=NONE`

Validate an input file with required column validtion
disabled with `--mode=NONE`

```bash
cat examples/docs/validate-column-names-without-required-columns.tsv
```
~~~
col1	col2	col3
~~~

```bash
kgtk validate -i examples/docs/validate-column-names-without-required-columns.tsv \
              --mode=NONE
```

The following is reported on standard output:

~~~

====================================================
Data lines read: 0
Data lines passed: 0
~~~

### Header Error: Ambiguous Required Columns

Validate an input file with a `node1` column abd its alias `from`.

```bash
cat examples/docs/validate-column-names-with-ambiguities.tsv
```
~~~
node1	label	node2	id	from
~~~

```bash
kgtk validate -i examples/docs/validate-column-names-with-ambiguities.tsv
```

The following error is reported on standard output:

~~~
In input header 'node1	label	node2	id	from': Ambiguous required column names node1 and from
~~~

The following is reported on standard error:

    Exit requested

!!! note
    When there are multiple ambiguous column names, only the first pair of
    ambiguous names is reported.  This behavior may change in the future to
    report all ambiguous column names sets.

### Line Check: Empty Lines

Empty lines are stripped from input files during validation.

```bash
cat examples/docs/validate-empty-lines.tsv
```
~~~
node1	label	node2
line1	isa	line

line3	isa	line
~~~

```bash
kgtk validate -i examples/docs/validate-empty-lines.tsv
```

~~~

====================================================
Data lines read: 3
Data lines passed: 2
Data lines ignored: 1
~~~

### Line Check: Comment Lines

Comment lines (lines that begin with hash (`#`))
are stripped from input files during validation.



```bash
kgtk validate -i examples/docs/validate-comment-lines.tsv
```

~~~

====================================================
Data lines read: 3
Data lines passed: 2
Data lines ignored: 1
~~~

!!! note
    At the present time the input file cannot be shown for this example.

### Line Check: Whitespace Lines

Whitespace lines are stripped from input files during validation.

```bash
cat examples/docs/validate-whitespace-lines.tsv
```
~~~
node1	label	node2
line1	isa	line
		
line3	isa	line
~~~

```bash
kgtk validate -i examples/docs/validate-whitespace-lines.tsv
```

~~~

====================================================
Data lines read: 3
Data lines passed: 2
Data lines ignored: 1
~~~

### Line Check: Short Lines

Short lines, lines with too few columns, are stripped from input files
during validation if `fill-short-lines=False` (the default) and
`--short-line-action=COMPLAIN` (the default) 

```bash
cat examples/docs/validate-short-lines.tsv
```
~~~
node1	label	node2
line1	isa	line
line2	isashortline
line3	isa	line
~~~

```bash
kgtk validate -i examples/docs/validate-short-lines.tsv
```

~~~
Data line 2:
line2	isashortline
Required 3 columns, saw 2: 'line2	isashortline'

====================================================
Data lines read: 3
Data lines passed: 2
Data lines excluded due to too few columns: 1
Data errors reported: 1
~~~

!!! note
    See the table of Action Codes for a discussion of other
    `--short-line-action` settings.

### Line Check: Fill Missing Trailing Columns

Short lines, lines with too few columns, are padded on input
if `--fill-short-lines=True` is specified.  `--short-line-action`
will not be triggered.

```bash
cat examples/docs/validate-short-lines.tsv
```
~~~
node1	label	node2
line1	isa	line
line2	isashortline
line3	isa	line
~~~

```bash
kgtk validate -i examples/docs/validate-short-lines.tsv \
              --fill-short-lines
```

~~~

====================================================
Data lines read: 3
Data lines passed: 3
Data lines filled: 1
~~~

### Line Check: Long Lines

Long lines, lines with extra columns, are stripped from input files
during validation if `truncate-long-lines=True` (the default) and
`--long-line-action=COMPLAIN` (the default).

```bash
cat examples/docs/validate-long-lines.tsv
```
~~~
node1	label	node2
line1	isa	line
line2	isa	long	line
line3	isa	line
~~~

```bash
kgtk validate -i examples/docs/validate-long-lines.tsv
```

~~~
Data line 2:
line2	isa	long	line
Required 3 columns, saw 4 (1 extra): 'line2	isa	long	line'

====================================================
Data lines read: 3
Data lines passed: 2
Data lines excluded due to too many columns: 1
Data errors reported: 1
~~~

!!! note
    See the table of Action Codes for a discussion of other
    `--long-liine-action` values.

### Line Check: Remove Extra Trailing Columns

Long lines, lines with extra columns, are truncated on input
if `--truncate-longt-lines=True` is specified.  `--long-line-action`
will not be triggered.

```bash
cat examples/docs/validate-long-lines.tsv
```
~~~
node1	label	node2
line1	isa	line
line2	isa	long	line
line3	isa	line
~~~

```bash
kgtk validate -i examples/docs/validate-long-lines.tsv \
              --truncate-long-lines
```

~~~

====================================================
Data lines read: 3
Data lines passed: 3
Data lines truncated: 1
~~~

### Line Check: Prohibited Lists in `node1`

Does this apply to node files?

### Line Check: Prohibited Lists in `label`

Does this apply to node files?

### Line Check: Prohibited Lists in `node2`

Does this apply to node files?

### Line Check: Ignore Prohibited Lists

### Line Check: `node1` Is Blank (Edge Files)

### Note: `label` May Be Blank (Edge Files)

### Line Check: `node2` Is Blank (Edge Files)

### Line Check: `id` Is Blank (Node Files)

### Value Check: Number or Quantity: Match Failed

### Value Check: Number or Quantity: Lax Match Failed

### Value Check: Number or Quantity: Low Tolerance is Not Float

### Value Check: Number or Quantity: High Tolerance is Not Float

### Value Check: Number or Quantity: Missing Numeric part
(Shouldn't hapen)

### Value Check: Number: Match Failed

### Value Check: Number: Missing Numeric part
(Shouldn't hapen)

### Value Check: Quantity: Match Failed

### Value Check: Quantity: Lax Match Failed

### Value Check: Quantity: Low Tolerance is Not Float

### Value Check: Quantity: High Tolerance is Not Float

### Value Check: Quantity: Missing Numeric part
(Shouldn't hapen)

### Value Check: String: Lax Match Failed

### Value Check: String: Strict Match Failed

### Value Check: Language Qualified String: Lax Match Failed

### Value Check: Language Qualified String: Strict Match Failed

### Value Check: Language Qualified String: Wikidata Match Failed

### Value Check: Language Qualified String: Language Validation Failed

### Value Check: Language Qualified String: Allow Language Suffixes

### Value Check: Language Qualified String: Additional Language Codes

### Value Check: Location Coordinates: Match Failed

### Value Check: Location Coordinates: Lax Match Failed

### Value Check: Location Coordinates: Lat Is Not Float

### Value Check: Location Coordinates: Lat Less than Minimum

### Value Check: Location Coordinates: Lat Greater Than Maximum

### Value Check: Location Coordinates: Lon Is Not Float

### Value Check: Location Coordinates: Lon Less than Minimum

### Value Check: Location Coordinates: Lon Greater Than Maximum

### Values Check: Date and Times: Lax Match Failed

### Values Check: Date and Times: Missing Hyphen

### Values Check: Date and Times: No Year

### Values Check: Date and Times: Year Not Int
(Shouldn't happen)

### Values Check: Date and Times: Year Less than Minimum

### Values Check: Date and Times: Year Greater then Maximum

### Values Check: Date and Times: Month Not Int
(Shouldn't happen)

### Values Check: Date and Times: Month 0 Disallowed

### Values Check: Date and Times: Day Not Int
(Shouldn't happen)

### Values Check: Date and Times: Day 0 Disallowed

### Values Check: Date and Times: Hour Not Int
(Shouldn't happen)

### Values Check: Date and Times: Minutes Not Int
(Shouldn't happen)

### Values Check: Date and Times: Seconds Not Int
(Shouldn't happen)

### Values Check: Date and Times: Hour 24 and Minutes or Seconds Not Zero

### Values Check: Date and Times: End-of-day Value Disallowed

