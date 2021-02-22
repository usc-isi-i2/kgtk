## Overview

This tool validates that KGTK files meet the rules in the [KGTK File Format v2](../../specification).
Error messages will be generated when rule violations are detected.
By default, most error messages are written to standard output so they may be
easily captured in a log file.

One or more KGTK files may be processed at a time.  Input files will be decompressed
automatically in certain conditions.

!!! note
    All of the validations shown here are done by KgtkReader.  They may be
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

The action codes are used to control what happens when `kgtk validate`
discovers a rule violation. 

| Action keyword | Action when condition detected |
| -------------- | ------------------------------ |
| PASS           | Silently allow the data line to pass through. |
| REPORT         | Report the data line and let it pass through. |
| EXCLUDE        | Silently exclude (ignore) the data line. |
| COMPLAIN       | Report the data line and exclude (ignore) it. |
| ERROR          | Raise a ValueError. This may be useful when you wish to interrupt processing of a large file. |
| EXIT           | sys.exit(1)  This may be useful when you wish to interrupt processing of a large file.|

These codes apply to the following `kgtk validate` comand line options:

| Option | Default |
| ------ | ------- |
|    `--blank-required-field-line-action` | EXCLUDE |
|    `--comment-line-action` | EXCLUDE |
|    `--empty-line-action` | EXCLUDE |
|    `--invalid-value-action` | EXCLUDE |
|    `--long-line-action` | COMPLAIN |
|    `--prohibited-list-action` | COMPLAIN |
|    `--short-line-action` | COMPLAIN | 
|    `--whitespace-line-action` | EXCLUDE |

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

### Escapes in Strings and Language Qualified Strings

KGTK strings (`"..."`) and language-qualified strings (`'...'@lan`) may contain
the following escape sequences.

| Sequence | Description | Comments |
| -------- | ----------- |  ------- |
| \a       | alarm (bell) - ASCII &lt;BEL&gt; | |
| \b       | backspace - ASCII &lt;BS&gt; | |
| \f       | formfeed - ASCII &lt;FF&gt; | |
| \n       | newline (linefeed) - ASCII &lt;LF&gt; | |
| \r       | carriage return - ASCII &lt;CR&gt; | |
| \t       | horizontal tab - ASCII &lt;TAB&gt; | |
| \v       | vertical tab - ASCII &lt;VT&gt; | |
| \\\\       | backslash - (\\) | |
| \'       | single quote - (') | The KGTK sigil for language qualified strings. |
| \"       | double quote - (") | The KGTK sigil for strings. |
| \\\|       | vertical bar - (\|) | The KGTK multi-valued list separator. |

!!! info
    A `sigil` is a symbol attached to (usually prefixing) a variable
    name, usually expressing the variable's datatype or scope (see [Wikipedia](https://en.wikipedia.org/wiki/Sigil_(computer_programming))). Here,
    it means the introductory character that determines the datatype
    of a KGTK value.

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

Suppose that `examples/docs/validate-date-with-day-zero.tsv` contains the following table in KGTK format:

```bash
kgtk cat -i examples/docs/validate-date-with-day-zero.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| john | woke | ^2020-05-00T00:00 |
| john | woke | ^2020-00-00T00:00 |

### Validate using Default Options

```bash
kgtk validate -i examples/docs/validate-date-with-day-zero.tsv
```

The following complaint and summary will be issued:

~~~
Data line 1:
john	woke	^2020-05-00T00:00
col 2 (node2) value '^2020-05-00T00:00' is an Invalid Date and Times
Data line 2:
john	woke	^2020-00-00T00:00
col 2 (node2) value '^2020-00-00T00:00' is an Invalid Date and Times

====================================================
Data lines read: 2
Data lines passed: 0
Data lines excluded due to invalid values: 2
Data errors reported: 2
~~~

The first data line was flagged because it contained "00" in the day
field, which violates the ISO 8601 specification.

### Validate with Verbose Feedback

Sometimes you may wish to get more feedback about what `kgtk validate` is
doing.

```bash
kgtk validate -i examples/docs/validate-date-with-day-zero.tsv \
              --verbose
```

This results in the following output:

~~~

====================================================
Validating 'examples/docs/validate-date-with-day-zero.tsv'
KgtkReader: File_path.suffix: .tsv
KgtkReader: reading file examples/docs/validate-date-with-day-zero.tsv
header: node1	label	node2
input format: kgtk
node1 column found, this is a KGTK edge file
KgtkReader: Special columns: node1=0 label=1 node2=2 id=-1
KgtkReader: Reading an edge file.
KgtkValue.is_date_and_times: day 0 disallowed in '^2020-05-00T00:00'.
Data line 1:
john	woke	^2020-05-00T00:00
col 2 (node2) value '^2020-05-00T00:00': 
col 2 (node2) value '^2020-05-00T00:00' is an Invalid Date and Times
KgtkValue.is_date_and_times: month 0 disallowed in '^2020-00-00T00:00'.
Data line 2:
john	woke	^2020-00-00T00:00
col 2 (node2) value '^2020-00-00T00:00': 
col 2 (node2) value '^2020-00-00T00:00' is an Invalid Date and Times
Validated 0 data lines

====================================================
Data lines read: 2
Data lines passed: 0
Data lines excluded due to invalid values: 2
Data errors reported: 2
~~~

### Validate Only the Header

Validate only the header record, ignoring data records:

```bash
kgtk validate -i examples/docs/validate-date-with-day-zero.tsv \
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

Empty lines are silently ignored from input files during validation
when `--empty-line-action=EXCLUDE` (the default).

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

!!! note
    See the table of Action Codes for a discussion of other
    `--empty-line-action` values.

### Line Check: Comment Lines

Comment lines (lines that begin with hash (`#`))
are silently ignored in input files during validation when
`--comment-line-action=EXCLUDE` (the default).

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
    At the present time the input file cannot be shown in this document for this example.

!!! note
    See the table of Action Codes for a discussion of other
    `--comment-line-action` values.

### Line Check: Whitespace Lines

Whitespace lines are silently ignored in input files during validation whe
`--whitespace-line-action=EXCLUDE` (the default).

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

!!! note
    See the table of Action Codes for a discussion of other
    `--whitespace-line-action` values.

### Line Check: Short Lines

Short lines, lines with too few columns, are silently ignored input files
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
Data lines passed: 2
Data lines filled: 1
Data lines excluded due to blank fields: 1
~~~

### Line Check: Long Lines

Long lines, lines with extra columns, are silently ignored input files
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
    `--long-line-action` values.

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

### Line Check: Prohibited Lists in the `node1` Column of Edge Files

[Multivalue lists (`|`) are prohibited by the KGTK File Specification v2](../../specification#multi-valued-edges)
in the `node1`, `label`, and `node2` columns of a KGTK edge file.
This constraint is applied when `--prohibited-list-action==COMPLAIN` (the default).

```bash
cat examples/docs/validate-node1-list.tsv
```
~~~
node1	label	node2	id
line1|line3	isa	line	id1
~~~

```bash
kgtk validate -i examples/docs/validate-node1-list.tsv
```

~~~
Data line 1:
line1|line3	isa	line	id1
col 0 (node1) value 'line1|line3'is a prohibited list

====================================================
Data lines read: 1
Data lines passed: 0
Data lines excluded due to prohibited lists: 1
Data errors reported: 1
~~~

!!! note
    This constraint does not apply to KGTK node files or to
    quasi-KGTK (`--mode=NONE`) files.

!!! note
    See the table of Action Codes for a discussion of other
    `--prohibited-list-action` values.

### Line Check: Prohibited Lists in the `label` Column of Edge Files

[Multivalue lists (`|`) are prohibited by the KGTK File Specification v2](../../specification#multi-valued-edges)
in the `node1`, `label`, and `node2` columns of a KGTK edge file.
This constraint is applied when `--prohibited-list-action==COMPLAIN` (the default).

```bash
cat examples/docs/validate-label-list.tsv
```
~~~
node1	label	node2	id
line1	isa|equals	line	id1
~~~

```bash
kgtk validate -i examples/docs/validate-label-list.tsv
```

~~~
Data line 1:
line1	isa|equals	line	id1
col 1 (label) value 'isa|equals'is a prohibited list

====================================================
Data lines read: 1
Data lines passed: 0
Data lines excluded due to prohibited lists: 1
Data errors reported: 1
~~~

!!! note
    This constraint does not apply to KGTK node files or to
    quasi-KGTK (`--mode=NONE`) files.

!!! note
    See the table of Action Codes for a discussion of other
    `--prohibited-list-action` values.

### Line Check: Prohibited Lists in the `node2` Column of Edge Files

[Multivalue lists (`|`) are prohibited by the KGTK File Specification v2](../../specification#multi-valued-edges)
in the `node1`, `label`, and `node2` columns of a KGTK edge file.
This constraint is applied when `--prohibited-list-action==COMPLAIN` (the default).

```bash
cat examples/docs/validate-node2-list.tsv
```
~~~
node1	label	node2	id
line1	isa	line|record	id1
~~~

```bash
kgtk validate -i examples/docs/validate-node2-list.tsv
```

~~~
Data line 1:
line1	isa	line|record	id1
col 2 (node2) value 'line|record'is a prohibited list

====================================================
Data lines read: 1
Data lines passed: 0
Data lines excluded due to prohibited lists: 1
Data errors reported: 1
~~~

!!! note
    This constraint does not apply to KGTK node files or to
    quasi-KGTK (`--mode=NONE`) files.

!!! note
    See the table of Action Codes for a discussion of other
    `--prohibited-list-action` values.

### Line Check: Allow Multivalue Lists in the `node1`, `label`, and `node2` Columns of Edge Files

[Multivalue lists (`|`) are prohibited by the KGTK File Specification v2](../../specification#multi-valued-edges)
in the `node1`, `label`, and `node2` columns of a KGTK edge file.  This constraint is applied when
`--prohibited-list-action==COMPLAIN` (the default).  The constraint can be
removed by specifying `--prohibited-list-action=PASS` or
`--prohibited-list-action=REPORT`.

```bash
cat examples/docs/validate-node2-list.tsv
```
~~~
node1	label	node2	id
line1	isa	line|record	id1
~~~

```bash
kgtk validate -i examples/docs/validate-node2-list.tsv \
              --prohibited-list-action=PASS
```

~~~

====================================================
Data lines read: 1
Data lines passed: 1
~~~

The REPORT option will allow lines with
prohibited multivalue lists to pass, but will report them to the output file
(normally standard output for `kgtk validate`).

```bash
kgtk validate -i examples/docs/validate-node2-list.tsv \
              --prohibited-list-action=REPORT
```

~~~
Data line 1:
line1	isa	line|record	id1
col 2 (node2) value 'line|record'is a prohibited list

====================================================
Data lines read: 1
Data lines passed: 1
Data errors reported: 1
~~~

!!! note
    This constraint does not apply to KGTK node files or to
    quasi-KGTK (`--mode=NONE`) files, so setting `--mode=NONE`
    is another way to remove this constraint, although it also
    removes many other constraints.

### Line Check: `node1` May Not Be Blank in an Edge File

The `node1` field may not be blank in a KGTK edge file.

```bash
cat examples/docs/validate-node1-blank-edge.tsv
```
~~~
node1	label	node2	id
	isa	line	id1
~~~

```bash
kgtk validate -i examples/docs/validate-node1-blank-edge.tsv
```

~~~

====================================================
Data lines read: 1
Data lines passed: 0
Data lines excluded due to blank fields: 1
~~~

### Line Check: `node1` May Be Blank in a Node File

The `node1` field may be blank in a KGTK node file.

```bash
cat examples/docs/validate-node1-blank-node.tsv
```
~~~
id	size	color	node1
id1	large	red	
~~~

```bash
kgtk validate -i examples/docs/validate-node1-blank-node.tsv \
              --mode=NODE
```

~~~

====================================================
Data lines read: 1
Data lines passed: 1
~~~

!!! note
    In this example it was necessary to specify `--mode=NODE` to
    prevent the input file from being treated as an edge file.

### Line Check: `label` May Be Blank in an Edge File

The `label` field may be blank in a KGTK edge file.

```bash
cat examples/docs/validate-label-blank-edge.tsv
```
~~~
node1	label	node2	id
line1		line	id1
~~~

```bash
kgtk validate -i examples/docs/validate-label-blank-edge.tsv
```

~~~

====================================================
Data lines read: 1
Data lines passed: 1
~~~

### Line Check: `label` May Be Blank in a Node File

The `label` field may be blank in a KGTK node file.

```bash
cat examples/docs/validate-label-blank-node.tsv
```
~~~
id	size	color	label
id1	large	red	
~~~

```bash
kgtk validate -i examples/docs/validate-label-blank-node.tsv
```

~~~

====================================================
Data lines read: 1
Data lines passed: 1
~~~

### Line Check: `node2` May Not Be Blank in an Edge File

The `node2` field may not be blank in a KGTK edge file.

```bash
cat examples/docs/validate-node2-blank-edge.tsv
```
~~~
node1	label	node2	id
line1	isa		id1
~~~

```bash
kgtk validate -i examples/docs/validate-node2-blank-edge.tsv
```

~~~

====================================================
Data lines read: 1
Data lines passed: 0
Data lines excluded due to blank fields: 1
~~~

### Line Check: `node2` May Be Blank in a Node File

The `node2` field may be blank in a KGTK node file.

```bash
cat examples/docs/validate-node2-blank-node.tsv
```
~~~
id	size	color	node2
id1	large	red	
~~~

```bash
kgtk validate -i examples/docs/validate-node2-blank-node.tsv
```

~~~

====================================================
Data lines read: 1
Data lines passed: 1
~~~

### Line Check: `id` May Be Blank in an Edge File

The `id` field may be blank in a KGTK edge file.

```bash
cat examples/docs/validate-id-blank-edge.tsv
```
~~~
node1	label	node2	id
line1	isa	line	
~~~

```bash
kgtk validate -i examples/docs/validate-id-blank-edge.tsv
```

~~~

====================================================
Data lines read: 1
Data lines passed: 1
~~~

### Line Check: `id` May Not Be Blank in a Node File

The `id` field may not be blank in a KGTK node file.

```bash
cat examples/docs/validate-id-blank-node.tsv
```
~~~
id	size	color
	large	red
~~~

```bash
kgtk validate -i examples/docs/validate-id-blank-node.tsv
```

~~~

====================================================
Data lines read: 1
Data lines passed: 0
Data lines excluded due to blank fields: 1
~~~

### Value Check: Numbers and Quantities

Numbers are dimensionless.  They may be integers (decimal, binary,
octal, or hexadecimal), 
floating point (with or without exponential), or imaginary.

Quanties are numbers with an attached tolerance and/or dimension.  The dimemsion
may be indicated by SI units or by a QNode (a Wikidata QID or Q identifier).

By default, standard Wikidata QNodes are allowed as dimension
qualifiers in quantities.  When `--allow-lax-qnodes=FALSE` (the
default), a QNode is an initial `Q` followed by an initial digit
other than `0`, followed by zero or more digits `0-9`.

Lines with invalid numbers quantities are excluded
by default.


```bash
kgtk cat -i examples/docs/validate-numbers-and-quantities.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| line1 | invalid | 9x |
| line2 | invalid | 9[8,10j] |
| line3 | invalid | --9 |
| line4 | valid | 9 |
| line5 | valid | 9m |
| line6 | valid | 9Q12345 |
| line7 | invalid | 9Q012345 |
| line8 | invalid | 9Q123_45 |
| line9 | invalid | 9Q123-45 |
| line10 | invalid | 9Q123az |
| line11 | invalid | 9Q123AZ |

```bash
kgtk validate -i examples/docs/validate-numbers-and-quantities.tsv
```

~~~
Data line 1:
line1	invalid	9x
col 2 (node2) value '9x' is an Invalid Quantity
Data line 2:
line2	invalid	9[8,10j]
col 2 (node2) value '9[8,10j]' is an Invalid Quantity
Data line 3:
line3	invalid	--9
col 2 (node2) value '--9' is an Invalid Quantity
Data line 7:
line7	invalid	9Q012345
col 2 (node2) value '9Q012345' is an Invalid Quantity
Data line 8:
line8	invalid	9Q123_45
col 2 (node2) value '9Q123_45' is an Invalid Quantity
Data line 9:
line9	invalid	9Q123-45
col 2 (node2) value '9Q123-45' is an Invalid Quantity
Data line 10:
line10	invalid	9Q123az
col 2 (node2) value '9Q123az' is an Invalid Quantity
Data line 11:
line11	invalid	9Q123AZ
col 2 (node2) value '9Q123AZ' is an Invalid Quantity

====================================================
Data lines read: 11
Data lines passed: 3
Data lines excluded due to invalid values: 8
Data errors reported: 8
~~~

### Value Check: Lax QNodes in Quantities

By default, standard QNodes (Wikidata QIDs or Q identifiers) are allowed as dimension
qualifiers in quantities.  When `--allow-lax-qnodes=FALSE` (the
default), a QNode is an initial `Q` followed by an initial digit
other than `0`, followed by zero or more digits `0-9`.

When `--allow-lax-qnodes=TRUE`, 
the QNode pattern is generalized with the addition of `-`,
`_`, and upper- and lower-case alphas (`a-zA-Z`) after the initial `Q`.

```bash
kgtk cat -i examples/docs/validate-lax-qnodes-in-quantities.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| line6 | valid | 9Q12345 |
| line7 | valid | 9Q012345 |
| line8 | valid | 9Q123_45 |
| line9 | valid | 9Q123-45 |
| line10 | valid | 9Q123az |
| line11 | valid | 9Q123AZ |

```bash
kgtk validate -i examples/docs/validate-lax-qnodes-in-quantities.tsv \
         --allow-lax-qnodes
```

~~~

====================================================
Data lines read: 6
Data lines passed: 6
~~~

### Value Check: Strings

Strings begin and end with double quotes (`"`).

Strings that start with a double quote but do not end with one are
invalid.

Internal double quotes in a string must be escaped with backslash (`\"`) when `--allow-lax-strings=FALSE` (the default),
otherwise the string is invalid.

Tab characters inside a string must be represented by `\t` whens the tab character is the column separator
(controlled by `--column-separator`).

List separators (`|`) must be escaped (`\|`) inside a string when `--escape-list-separators=True` (the default).

Invalid strings are excluded by default.

```bash
kgtk cat -i examples/docs/validate-strings.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| line1 | invalid | "xxx |
| line2 | valid | "xxx\"yyy" |
| line3 | invalid | "xxx"yyy" |
| line4 | valid | "xxx\\yyy" |
| line5 | valid | "xxx\tyyy" |

```bash
kgtk validate -i examples/docs/validate-strings.tsv
```

~~~
Data line 1:
line1	invalid	"xxx
col 2 (node2) value '"xxx' is an Invalid String
Data line 3:
line3	invalid	"xxx"yyy"
col 2 (node2) value '"xxx"yyy"' is an Invalid String

====================================================
Data lines read: 5
Data lines passed: 3
Data lines excluded due to invalid values: 2
Data errors reported: 2
~~~

### Value Check: Lax Strings

Strings with internal double quote characters(`"`) that are not escaped
(`\"`) are considered valid when `--allow-lax-strings=TRUE`.

[`kgtk clean`](../clean) can convert lax strings into strict KGTK strings.

```bash
kgtk cat -i examples/docs/validate-lax-strings.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| line1 | invalid | "xxx |
| line2 | valid | "xxx\"yyy" |
| line3 | valid | "xxx"yyy" |
| line4 | valid | "xxx\\yyy" |
| line5 | valid | "xxx\tyyy" |


```bash
kgtk validate -i examples/docs/validate-lax-strings.tsv \
              --allow-lax-strings
```

~~~
Data line 1:
line1	invalid	"xxx
col 2 (node2) value '"xxx' is an Invalid String

====================================================
Data lines read: 5
Data lines passed: 4
Data lines excluded due to invalid values: 1
Data errors reported: 1
~~~

### Value Check: Language-Qualified Strings

KGTK language-qualified strings begin with single quotes (`'`).
They end with single quotes (`'`) followed by an at sign (`@`) and
a language qualifier (e.g., `en`).  Example: `'abc'@en`.

Language-qualified strings that start with a single quote but do not end with one, followed by
at sign and the language qualifier, are invalid.

Internal single quotes in a language-qualified string must be escaped with backslash (`\'`) when `--allow-lax-lq-strings=FALSE` (the default),
otherwise the language-qualified string is invalid.

Tab characters inside a language-qualified string must be represented by `\t` whens the tab character is the column separator
(controlled by `--column-separator`).

List separators (`|`) must be escaped (`\|`) inside a language-qualified string when `--escape-list-separators=True` (the default).

The language qualifier is an ISO 639-3 (or ISO 639-5) two- or three-character language code
when `--allow-wikidata-lq-strings=FALSE` (the default).  The language
qualifiers are validated against internal tables of ISO 639-3 (or ISO 639-5) codes and additional
language codes.

When `--additional-language-codes` is specified it overrides the internal table
of additional language codes.

By default, `--allow-language-suffixes=FALSE`.  When `--allow-language-suffixes=TRUE`, the
language qualifier may be followed by a language suffix, which is a dash (`-`) followed by
 a string matching the pattern `[-a-zA-Z0-9]+`.

Invalid language-qualified strings are excluded by default.

```bash
kgtk cat -i examples/docs/validate-language-qualified-strings.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| line1 | valid | 'abc'@en |
| line2 | valid | 'a\'bc'@en |
| line3 | invalid | 'a'bc'@en |
| line4 | invalid | 'abc'@en-gb |
| line5 | invalid | 'abc'@xxx |

```bash
kgtk validate -i examples/docs/validate-language-qualified-strings.tsv
```

~~~
Data line 3:
line3	invalid	'a'bc'@en
col 2 (node2) value "'a'bc'@en" is an Invalid Language Qualified String
Data line 4:
line4	invalid	'abc'@en-gb
col 2 (node2) value "'abc'@en-gb" is an Invalid Language Qualified String
Data line 5:
line5	invalid	'abc'@xxx
col 2 (node2) value "'abc'@xxx" is an Invalid Language Qualified String

====================================================
Data lines read: 5
Data lines passed: 2
Data lines excluded due to invalid values: 3
Data errors reported: 3
~~~

### Value Check: Language-Qualified Strings with Suffixes

When `--allow-language-suffixes=TRUE`, the
language qualifier may be followed by a language suffix, which is a dash (`-`) followed by
 a string matching the pattern `[-a-zA-Z0-9]+`.

```bash
kgtk cat -i examples/docs/validate-language-qualified-strings-with-suffixes.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| line1 | valid | 'abc'@en-gb |

```bash
kgtk validate -i examples/docs/validate-language-qualified-strings-with-suffixes.tsv \
              --allow-language-suffixes
```

~~~

====================================================
Data lines read: 1
Data lines passed: 1
~~~

### Value Check: Lax Language-Qualified Strings

KGTK language-qualified strings with internal double quote characters(`"`) that are not escaped
(`\"`) are considered valid when `--allow-lax-lq-strings=TRUE`.

[`kgtk clean`](../clean) can convert lax language-qualified strings into strict KGTK strings.

```bash
kgtk cat -i examples/docs/validate-lax-language-qualified-strings.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| line1 | valid | 'abc'@en |
| line1 | valid | 'a'bc'@en |

```bash
kgtk validate -i examples/docs/validate-lax-language-qualified-strings.tsv \
              --allow-lax-lq-strings TRUE
```

~~~

====================================================
Data lines read: 2
Data lines passed: 2
~~~

### Value Check: Wikidata Language-Qualified Strings

When `--allow-wikidata-lq-strings=TRUE`, the language qualifier
may be two or more alpha characters, optionally followed by a
language suffix (a dash (`-`) followed by a string matching the pattern `[-a-zA-Z0-9]+`).
The language qualifier is not validated against known values.

```bash
kgtk cat -i examples/docs/validate-wikidata-language-qualified-strings.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| line1 | valid | 'abc'@english |
| line2 | valid | 'abc'@english-gb |

```bash
kgtk validate -i examples/docs/validate-wikidata-language-qualified-strings.tsv \
              --allow-wikidata-lq-strings
```

~~~

====================================================
Data lines read: 2
Data lines passed: 2
~~~

### Value Check: Language Qualified Strings with Additional Language Codes

```bash
kgtk cat -i examples/docs/validate-language-qualified-strings-with-addl-codes.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| line1 | valid | 'abc'@xxx |
| line2 | valid | 'abc'@yyy |

```bash
kgtk validate -i examples/docs/validate-language-qualified-strings-with-addl-codes.tsv \
              --additional-language-codes xxx yyy
```

~~~

====================================================
Data lines read: 2
Data lines passed: 2
~~~

### Value Check: Location Coordinates

KGTk location coodinates values start with the at sign (`@`), followed
by the latitude and longitude separated by a slash (`/`).

Latitude and longitude are indegrees.  They may be integers or
floating point numbers.

When `--allow-lax-coordinates=FALSE` (the dafault), latitude and
longitude may not include exponents.  When `--allow-lax-coordinates=TRUE`,
latitude and longitude may be floating point numbers with exponents.

When `--allow-out-of-range-coordinates=FALSE` (the default),
the latitude and longitude must fit within specified ranges.
When `--allow-out-of-range-coordinates=TRUE), the following checks are not applied.

`--minimum-valid-lat` (default -90.00) is the minimum valid
latitide.  When `--clamp-minimum-lat=FALSE` (the default), a latitude
value less than the minimum value will result in an error.  When `--clamp-minimum-lat=TRUE`,
a latitude value less than the minimum value will be set to the minimum value.


`--maximum-valid-lat` (default 90.00) is the maximum valid
latitide.  When `--clamp-maximum-lat=FALSE` (the default), a latitude
value less than the maximum value will result in an error.  When `--clamp-maximum-lat=TRUE`,
a latitude value greater than the maximum value will be set to the maximum value.


`--minimum-valid-lon` (default -180.00) is the minimum valid
latitide.  When `--clamp-minimum-lon=FALSE` (the default), a longitude
value less than the minimum value will result in an error.  When `--clamp-minimum-lon=TRUE`,
a longitude value less than the minimum value will be set to the minimum value.


`--maximum-valid-lon` (default 180.00) is the maximum valid
latitide.  When `--clamp-maximum-lon=FALSE` (the default), a longitude
value less than the maximum value will result in an error.  When `--clamp-maximum-lon=TRUE`,
a longitude value greater than the maximum value will be set to the maximum value.

[`kgtk clean`](../clean) can update KGTK latitudes or longitudes with clamped
values.


```bash
kgtk cat -i examples/docs/validate-location-coordinates.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| line1 | valid | @34/118 |
| line2 | valid | @33.9803/118.4517 |
| line3 | invalid | @33.9803/118.4517e1 |
| line4 | invalid | @100/118 |
| line5 | invalid | @-100/118 |
| line6 | invalid | @34/200 |
| line7 | invalid | @34/-200 |

```bash
kgtk validate -i examples/docs/validate-location-coordinates.tsv
```

~~~
Data line 3:
line3	invalid	@33.9803/118.4517e1
col 2 (node2) value '@33.9803/118.4517e1' is an Invalid Location Coordinates
Data line 4:
line4	invalid	@100/118
col 2 (node2) value '@100/118' is an Invalid Location Coordinates
Data line 5:
line5	invalid	@-100/118
col 2 (node2) value '@-100/118' is an Invalid Location Coordinates
Data line 6:
line6	invalid	@34/200
col 2 (node2) value '@34/200' is an Invalid Location Coordinates
Data line 7:
line7	invalid	@34/-200
col 2 (node2) value '@34/-200' is an Invalid Location Coordinates

====================================================
Data lines read: 7
Data lines passed: 2
Data lines excluded due to invalid values: 5
Data errors reported: 5
~~~

### Value Check: Allow Lax Location Coordinates

```bash
kgtk cat -i examples/docs/validate-location-coordinates.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| line1 | valid | @34/118 |
| line2 | valid | @33.9803/118.4517 |
| line3 | invalid | @33.9803/118.4517e1 |
| line4 | invalid | @100/118 |
| line5 | invalid | @-100/118 |
| line6 | invalid | @34/200 |
| line7 | invalid | @34/-200 |

```bash
kgtk validate -i examples/docs/validate-location-coordinates.tsv \
              --allow-lax-coordinates
```

~~~
Data line 3:
line3	invalid	@33.9803/118.4517e1
col 2 (node2) value '@33.9803/118.4517e1' is an Invalid Location Coordinates
Data line 4:
line4	invalid	@100/118
col 2 (node2) value '@100/118' is an Invalid Location Coordinates
Data line 5:
line5	invalid	@-100/118
col 2 (node2) value '@-100/118' is an Invalid Location Coordinates
Data line 6:
line6	invalid	@34/200
col 2 (node2) value '@34/200' is an Invalid Location Coordinates
Data line 7:
line7	invalid	@34/-200
col 2 (node2) value '@34/-200' is an Invalid Location Coordinates

====================================================
Data lines read: 7
Data lines passed: 2
Data lines excluded due to invalid values: 5
Data errors reported: 5
~~~

### Value Check: Allow Out of Range Location Coordinates

```bash
kgtk cat -i examples/docs/validate-location-coordinates.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| line1 | valid | @34/118 |
| line2 | valid | @33.9803/118.4517 |
| line3 | invalid | @33.9803/118.4517e1 |
| line4 | invalid | @100/118 |
| line5 | invalid | @-100/118 |
| line6 | invalid | @34/200 |
| line7 | invalid | @34/-200 |

```bash
kgtk validate -i examples/docs/validate-location-coordinates.tsv \
              --allow-out-of-range-coordinates
```

~~~
Data line 3:
line3	invalid	@33.9803/118.4517e1
col 2 (node2) value '@33.9803/118.4517e1' is an Invalid Location Coordinates

====================================================
Data lines read: 7
Data lines passed: 6
Data lines excluded due to invalid values: 1
Data errors reported: 1
~~~

### Value Check: Clamp Out of Range Location Coordinates

```bash
kgtk cat -i examples/docs/validate-location-coordinates.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| line1 | valid | @34/118 |
| line2 | valid | @33.9803/118.4517 |
| line3 | invalid | @33.9803/118.4517e1 |
| line4 | invalid | @100/118 |
| line5 | invalid | @-100/118 |
| line6 | invalid | @34/200 |
| line7 | invalid | @34/-200 |

```bash
kgtk validate -i examples/docs/validate-location-coordinates.tsv \
              --clamp-minimum-lat --clamp-maximum-lat \
              --clamp-minimum-lon --clamp-maximum-lon
```

~~~
Data line 3:
line3	invalid	@33.9803/118.4517e1
col 2 (node2) value '@33.9803/118.4517e1' is an Invalid Location Coordinates

====================================================
Data lines read: 7
Data lines passed: 6
Data lines excluded due to invalid values: 1
Data errors reported: 1
~~~

### Value Check: Dates with Month or Day Zero

Wikidata uses day 0 on date/time values with coarser than day granularity.
Wikidata uses month 0 on date/time values with coarser than month granularity.
If these date strings are imported into KGTK files without modification, the result is
a date/time string that does not meet KGTK's [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) requirement.

```bash
kgtk cat -i examples/docs/validate-date-with-day-zero.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| john | woke | ^2020-05-00T00:00 |
| john | woke | ^2020-00-00T00:00 |

```bash
kgtk validate -i examples/docs/validate-date-with-day-zero.tsv
```

This results in the following summary:

~~~
Data line 1:
john	woke	^2020-05-00T00:00
col 2 (node2) value '^2020-05-00T00:00' is an Invalid Date and Times
Data line 2:
john	woke	^2020-00-00T00:00
col 2 (node2) value '^2020-00-00T00:00' is an Invalid Date and Times

====================================================
Data lines read: 2
Data lines passed: 0
Data lines excluded due to invalid values: 2
Data errors reported: 2
~~~

### Value Check: Allow Dates with Month or Day Zero

Instruct the validator to accept month or day 00, even though
this is not allowed by [ISO 6801](https://en.wikipedia.org/wiki/ISO_8601).

```bash
kgtk cat -i examples/docs/validate-date-with-day-zero.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| john | woke | ^2020-05-00T00:00 |
| john | woke | ^2020-00-00T00:00 |

```bash
kgtk validate -i examples/docs/validate-date-with-day-zero.tsv \
              --allow-month-or-day-zero
```

This results in no error messages, and the following summary:

~~~

====================================================
Data lines read: 2
Data lines passed: 2
~~~

!!! info
    Wikidata use day 0 on date/time values with coarser than day granularity.
    Wikidata uses month 0 on date/time values with coarser than month granularity.

### Value Check: Dates with End of Day Markers (24:00) Allowed by Dafault

KGTK uses [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) dates.  Prior to
the 2019 revision of this standard, ISO 8601-1:2019, "24:00" could be used to
indicate midnight at the end of a day.  The 2019 revision disallowed this usage, but
KGTK continues to support it, as end-of-day markers may appear in earlier sources,
such as Wikidata.

```bash
kgtk cat -i examples/docs/validate-date-with-end-of-day.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| john | woke | ^2020-05-01T24:00 |

```bash
kgtk validate -i examples/docs/validate-date-with-end-of-day.tsv
```

This results in no error messages, and the following summary:

~~~

====================================================
Data lines read: 1
Data lines passed: 1
~~~

### Value Check: Disallow Dates with End of Day Marker (24:00)

Instruct the validator to disallow the end-of-day marker (24:00),
in conformity to the current (ISO 8601)[https://en.wikipedia.org/wiki/ISO_8601) standard.

```bash
kgtk cat -i examples/docs/validate-date-with-end-of-day.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| john | woke | ^2020-05-01T24:00 |

```bash
kgtk validate -i examples/docs/validate-date-with-end-of-day.tsv \
              --allow-end-of-day False
```

This results in the following summary:

~~~
Data line 1:
john	woke	^2020-05-01T24:00
col 2 (node2) value '^2020-05-01T24:00' is an Invalid Date and Times

====================================================
Data lines read: 1
Data lines passed: 0
Data lines excluded due to invalid values: 1
Data errors reported: 1
~~~

### Value Check: Minimum Valid Year (1583 by Default)

The [KGTK File Specification v2](../../specification) uses [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601)
date format.  ISO 8601 is based on the Gregorian calendar, which started on 15 October 1582.
The default minimum valid year in ISO 8601 is 1583.

Extending the Gregorian calendar before its start date is called
the [proleptic Gregorian calendar](https://en.wikipedia.org/wiki/Proleptic_Gregorian_calendar).
ISO 8601 can be used to represent dates prior to year 1583, and has special
rules for representing the year 1 BC and earlier years.  KGTK generally
follows these rules. The following points should be noted:

  - The year `1 BC` is represented as the year `0000`.
  - An optional `+` may be used in front of year `0000` and later years.
  - The year `2 BC` and earlier years require minus signs (`-`) in front of the year number.
  - The year `2 BC` is represented as year `-0001`
  - KGTK allows dates with more than four digits in the year, but only in ISO 8601 `extended` mode (with dashes (`-`) between date components and colons (`:`) between time components, see the `--force-iso8601-extended` and `--require-iso8601-extended` examples, below)

`--minimum-valid-year` is used to specify the minimum allowed year.  The default value is 1583.

`--ignore-minimum-year`, when TRUE, disables the minimym valid year check.  The default for this option is FALSE.

`--clamp-minimum-year`, when TRUE, forces all years below the minimum value to be set to the minium value.  The default for this option is FALSE.

```bash
kgtk cat -i examples/docs/validate-date-with-minimum-year.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| john | born | ^1583-01-01T00:00 |
| jack | born | ^1582-01-01T00:00 |
| jorge | born | ^0922-01-01T00:00 |
| jerry | born | ^0000-01-01T00:00 |
| jon | born | ^+0000-01-01T00:00 |
| jared | born | ^-0001-01-01T00:00 |
| jimmy | born | ^-10001-01-01T00:00 |

```bash
kgtk validate -i examples/docs/validate-date-with-minimum-year.tsv
```

This results in the following summary:

~~~
Data line 2:
jack	born	^1582-01-01T00:00
col 2 (node2) value '^1582-01-01T00:00' is an Invalid Date and Times
Data line 3:
jorge	born	^0922-01-01T00:00
col 2 (node2) value '^0922-01-01T00:00' is an Invalid Date and Times
Data line 4:
jerry	born	^0000-01-01T00:00
col 2 (node2) value '^0000-01-01T00:00' is an Invalid Date and Times
Data line 5:
jon	born	^+0000-01-01T00:00
col 2 (node2) value '^+0000-01-01T00:00' is an Invalid Date and Times
Data line 6:
jared	born	^-0001-01-01T00:00
col 2 (node2) value '^-0001-01-01T00:00' is an Invalid Date and Times
Data line 7:
jimmy	born	^-10001-01-01T00:00
col 2 (node2) value '^-10001-01-01T00:00' is an Invalid Date and Times

====================================================
Data lines read: 7
Data lines passed: 1
Data lines excluded due to invalid values: 6
Data errors reported: 6
~~~

### Value Check: Change the Minimum Valid Year

Suppose we want to exclude all dates before the year 1000.
Here's our sample data:

```bash
kgtk cat -i examples/docs/validate-date-with-minimum-year.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| john | born | ^1583-01-01T00:00 |
| jack | born | ^1582-01-01T00:00 |
| jorge | born | ^0922-01-01T00:00 |
| jerry | born | ^0000-01-01T00:00 |
| jon | born | ^+0000-01-01T00:00 |
| jared | born | ^-0001-01-01T00:00 |
| jimmy | born | ^-10001-01-01T00:00 |

```bash
kgtk validate -i examples/docs/validate-date-with-minimum-year.tsv \
              --minimum-valid-year 1000
```

This results in the following summary:

~~~
Data line 3:
jorge	born	^0922-01-01T00:00
col 2 (node2) value '^0922-01-01T00:00' is an Invalid Date and Times
Data line 4:
jerry	born	^0000-01-01T00:00
col 2 (node2) value '^0000-01-01T00:00' is an Invalid Date and Times
Data line 5:
jon	born	^+0000-01-01T00:00
col 2 (node2) value '^+0000-01-01T00:00' is an Invalid Date and Times
Data line 6:
jared	born	^-0001-01-01T00:00
col 2 (node2) value '^-0001-01-01T00:00' is an Invalid Date and Times
Data line 7:
jimmy	born	^-10001-01-01T00:00
col 2 (node2) value '^-10001-01-01T00:00' is an Invalid Date and Times

====================================================
Data lines read: 7
Data lines passed: 2
Data lines excluded due to invalid values: 5
Data errors reported: 5
~~~

### Value Check: Clamp the Minimum Valid Year

Suppose we want to validate all records, converting any negative
dates to year 0000.  This will not make a significant difference to
`kgtk validate` compared to ignoring the minimum valid year check
(see the example below), but clamping may be useful in other contexts.

```bash
kgtk cat -i examples/docs/validate-date-with-minimum-year.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| john | born | ^1583-01-01T00:00 |
| jack | born | ^1582-01-01T00:00 |
| jorge | born | ^0922-01-01T00:00 |
| jerry | born | ^0000-01-01T00:00 |
| jon | born | ^+0000-01-01T00:00 |
| jared | born | ^-0001-01-01T00:00 |
| jimmy | born | ^-10001-01-01T00:00 |

```bash
kgtk validate -i examples/docs/validate-date-with-minimum-year.tsv \
              --minimum-valid-year 0000 \
              --clamp-minimum-year
```

This results in the following summary:

~~~

====================================================
Data lines read: 7
Data lines passed: 7
~~~

### Value Check: Ignore the Minimum Valid Year Check

```bash
kgtk cat -i examples/docs/validate-date-with-minimum-year.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| john | born | ^1583-01-01T00:00 |
| jack | born | ^1582-01-01T00:00 |
| jorge | born | ^0922-01-01T00:00 |
| jerry | born | ^0000-01-01T00:00 |
| jon | born | ^+0000-01-01T00:00 |
| jared | born | ^-0001-01-01T00:00 |
| jimmy | born | ^-10001-01-01T00:00 |

```bash
kgtk validate -i examples/docs/validate-date-with-minimum-year.tsv \
              --ignore-minimum-year
```

This results in the following summary:

~~~

====================================================
Data lines read: 7
Data lines passed: 7
~~~

### Value Check: Maximum Valid Year (2100 by Default)

The [KGTK File Specification v 2](../../specification) uses [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601)
date format.  ISO 8601 is based on the Gregorian calendar, which started on 15 October 1582.
The default maximum valid year in ISO 8601 is 9999, although additional digits can be used
incertain circumstances.

KGTK somewhat arbitrarily has a default maximum date of 2100.
The rationale is that dates beyond that are unlikely in
most datasets.


```bash
kgtk cat -i examples/docs/validate-date-with-maximum-year.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| john | date | ^2099-01-01T00:00 |
| jack | date | ^2100-01-01T00:00 |
| jack | date | ^2101-01-01T00:00 |
| jorge | born | ^9999-01-01T00:00 |
| jon | born | ^+9999-01-01T00:00 |
| jared | born | ^10000-01-01T00:00 |
| jared | born | ^+10000-01-01T00:00 |

```bash
kgtk validate -i examples/docs/validate-date-with-maximum-year.tsv
```

This results in the following summary:

~~~
Data line 3:
jack	date	^2101-01-01T00:00
col 2 (node2) value '^2101-01-01T00:00' is an Invalid Date and Times
Data line 4:
jorge	born	^9999-01-01T00:00
col 2 (node2) value '^9999-01-01T00:00' is an Invalid Date and Times
Data line 5:
jon	born	^+9999-01-01T00:00
col 2 (node2) value '^+9999-01-01T00:00' is an Invalid Date and Times
Data line 6:
jared	born	^10000-01-01T00:00
col 2 (node2) value '^10000-01-01T00:00' is an Invalid Date and Times
Data line 7:
jared	born	^+10000-01-01T00:00
col 2 (node2) value '^+10000-01-01T00:00' is an Invalid Date and Times

====================================================
Data lines read: 7
Data lines passed: 2
Data lines excluded due to invalid values: 5
Data errors reported: 5
~~~

### Value Check: Changing the Maximum Valid Year

Let's change the maximum valid year to 9999:

```bash
kgtk cat -i examples/docs/validate-date-with-maximum-year.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| john | date | ^2099-01-01T00:00 |
| jack | date | ^2100-01-01T00:00 |
| jack | date | ^2101-01-01T00:00 |
| jorge | born | ^9999-01-01T00:00 |
| jon | born | ^+9999-01-01T00:00 |
| jared | born | ^10000-01-01T00:00 |
| jared | born | ^+10000-01-01T00:00 |

```bash
kgtk validate -i examples/docs/validate-date-with-maximum-year.tsv \
              --maximum-valid-year 9999
```

This results in the following summary:

~~~
Data line 6:
jared	born	^10000-01-01T00:00
col 2 (node2) value '^10000-01-01T00:00' is an Invalid Date and Times
Data line 7:
jared	born	^+10000-01-01T00:00
col 2 (node2) value '^+10000-01-01T00:00' is an Invalid Date and Times

====================================================
Data lines read: 7
Data lines passed: 5
Data lines excluded due to invalid values: 2
Data errors reported: 2
~~~


### Value Check: Changing the Maximum Valid Year #2

Let's change the maximum valid year to 99999:

```bash
kgtk cat -i examples/docs/validate-date-with-maximum-year.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| john | date | ^2099-01-01T00:00 |
| jack | date | ^2100-01-01T00:00 |
| jack | date | ^2101-01-01T00:00 |
| jorge | born | ^9999-01-01T00:00 |
| jon | born | ^+9999-01-01T00:00 |
| jared | born | ^10000-01-01T00:00 |
| jared | born | ^+10000-01-01T00:00 |

```bash
kgtk validate -i examples/docs/validate-date-with-maximum-year.tsv \
              --maximum-valid-year 99999
```

This results in the following summary:

~~~

====================================================
Data lines read: 7
Data lines passed: 7
~~~


### Value Check: Ignoring the Maximum Valid Year

```bash
kgtk cat -i examples/docs/validate-date-with-maximum-year.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| john | date | ^2099-01-01T00:00 |
| jack | date | ^2100-01-01T00:00 |
| jack | date | ^2101-01-01T00:00 |
| jorge | born | ^9999-01-01T00:00 |
| jon | born | ^+9999-01-01T00:00 |
| jared | born | ^10000-01-01T00:00 |
| jared | born | ^+10000-01-01T00:00 |

```bash
kgtk validate -i examples/docs/validate-date-with-maximum-year.tsv \
              --ignore-maximum-year
```

This results in the following summary:

~~~

====================================================
Data lines read: 7
Data lines passed: 7
~~~

