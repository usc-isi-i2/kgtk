Validate one or more KGTK files, optionally decompressing
the input files.

Input files may be (de)compressed using a algorithm selected
by the file extension: .bz2 .gz .lz4 .xy

The expert option --compression-type may be used to override the
decompression selectin algorithim;  this is useful when reading from piped input.

## Usage
```
usage: kgtk validate [-h] [-i INPUT_FILE [INPUT_FILE ...]] [--header-only [HEADER_ONLY]]
                     [-v]

Validate one or more KGTK files. Empty lines, whitespace lines, comment lines, and lines with empty required fields are silently skipped. Header errors cause an immediate exception. Data value errors are reported. 

To validate data and pass clean data to an output file or pipe, use the kgtk clean_data command.

Additional options are shown in expert help.
kgtk --expert validate --help

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE [INPUT_FILE ...], --input-files INPUT_FILE [INPUT_FILE ...]
                        The KGTK file(s) to validate. (May be omitted or '-' for stdin.)
  --header-only [HEADER_ONLY]
                        Process the only the header of the input file (default=False).

  -v, --verbose         Print additional progress messages (default=False).
```

Expert help:

```
usage: kgtk validate [-h] [-i INPUT_FILE [INPUT_FILE ...]] [--header-only [HEADER_ONLY]]
                     [--errors-to-stdout | --errors-to-stderr] [--show-options] [-v]
                     [--very-verbose] [--column-separator COLUMN_SEPARATOR]
                     [--compression-type COMPRESSION_TYPE] [--error-limit ERROR_LIMIT]
                     [--gzip-in-parallel [optional True|False]]
                     [--gzip-queue-size GZIP_QUEUE_SIZE] [--mode {NONE,EDGE,NODE,AUTO}]
                     [--force-column-names FORCE_COLUMN_NAMES [FORCE_COLUMN_NAMES ...]]
                     [--header-error-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}]
                     [--skip-header-record [optional True|False]]
                     [--unsafe-column-name-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}]
                     [--initial-skip-count INITIAL_SKIP_COUNT]
                     [--every-nth-record EVERY_NTH_RECORD] [--record-limit RECORD_LIMIT]
                     [--tail-count TAIL_COUNT]
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
                     [--allow-month-or-day-zero [ALLOW_MONTH_OR_DAY_ZERO]]
                     [--repair-month-or-day-zero [REPAIR_MONTH_OR_DAY_ZERO]]
                     [--allow-end-of-day [ALLOW_END_OF_DAY]]
                     [--minimum-valid-year MINIMUM_VALID_YEAR]
                     [--clamp-minimum-year [CLAMP_MINIMUM_YEAR]]
                     [--maximum-valid-year MAXIMUM_VALID_YEAR]
                     [--clamp-maximum-year [CLAMP_MAXIMUM_YEAR]]
                     [--allow-lax-coordinates [ALLOW_LAX_COORDINATES]]
                     [--repair-lax-coordinates [REPAIR_LAX_COORDINATES]]
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
                        The KGTK file(s) to validate. (May be omitted or '-' for stdin.)
  --header-only [HEADER_ONLY]
                        Process the only the header of the input file (default=False).

Error and feedback messages:
  Send error messages and feedback to stderr or stdout, control the amount of feedback and debugging messages.

  --errors-to-stdout    Send errors to stdout instead of stderr
  --errors-to-stderr    Send errors to stderr instead of stdout
  --show-options        Print the options selected (default=False).
  -v, --verbose         Print additional progress messages (default=False).
  --very-verbose        Print additional progress messages (default=False).

File options:
  Options affecting processing.

  --column-separator COLUMN_SEPARATOR
                        Column separator (default=<TAB>).
  --compression-type COMPRESSION_TYPE
                        Specify the compression type (default=None).
  --error-limit ERROR_LIMIT
                        The maximum number of errors to report before failing (default=1000)
  --gzip-in-parallel [optional True|False]
                        Execute gzip in parallel (default=False).
  --gzip-queue-size GZIP_QUEUE_SIZE
                        Queue size for parallel gzip (default=1000).
  --mode {NONE,EDGE,NODE,AUTO}
                        Determine the KGTK file mode (default=KgtkReaderMode.AUTO).

Header parsing:
  Options affecting header parsing.

  --force-column-names FORCE_COLUMN_NAMES [FORCE_COLUMN_NAMES ...]
                        Force the column names (default=None).
  --header-error-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}
                        The action to take when a header error is detected. Only ERROR or
                        EXIT are supported (default=ValidationAction.EXIT).
  --skip-header-record [optional True|False]
                        Skip the first record when forcing column names (default=False).
  --unsafe-column-name-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}
                        The action to take when a column name is unsafe
                        (default=ValidationAction.REPORT).

Pre-validation sampling:
  Options affecting pre-validation data line sampling.

  --initial-skip-count INITIAL_SKIP_COUNT
                        The number of data records to skip initially (default=do not skip).
  --every-nth-record EVERY_NTH_RECORD
                        Pass every nth record (default=pass all records).
  --record-limit RECORD_LIMIT
                        Limit the number of records read (default=no limit).
  --tail-count TAIL_COUNT
                        Pass this number of records (default=no tail processing).

Line parsing:
  Options affecting data line parsing.

  --repair-and-validate-lines [optional True|False]
                        Repair and validate lines (default=True).
  --repair-and-validate-values [optional True|False]
                        Repair and validate values (default=True).
  --blank-required-field-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}
                        The action to take when a line with a blank node1, node2, or id
                        field (per mode) is detected (default=ValidationAction.EXCLUDE).
  --comment-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}
                        The action to take when a comment line is detected
                        (default=ValidationAction.EXCLUDE).
  --empty-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}
                        The action to take when an empty line is detected
                        (default=ValidationAction.EXCLUDE).
  --fill-short-lines [optional True|False]
                        Fill missing trailing columns in short lines with empty values
                        (default=False).
  --invalid-value-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}
                        The action to take when a data cell value is invalid
                        (default=ValidationAction.COMPLAIN).
  --long-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}
                        The action to take when a long line is detected
                        (default=ValidationAction.COMPLAIN).
  --prohibited-list-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}
                        The action to take when a data cell contains a prohibited list
                        (default=ValidationAction.COMPLAIN).
  --short-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}
                        The action to take when a short line is detected
                        (default=ValidationAction.COMPLAIN).
  --truncate-long-lines [TRUNCATE_LONG_LINES]
                        Remove excess trailing columns in long lines (default=False).
  --whitespace-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}
                        The action to take when a whitespace line is detected
                        (default=ValidationAction.EXCLUDE).

Data value parsing:
  Options controlling the parsing and processing of KGTK data values.

  --additional-language-codes [ADDITIONAL_LANGUAGE_CODES [ADDITIONAL_LANGUAGE_CODES ...]]
                        Additional language codes. (default=None).
  --allow-lax-qnodes [ALLOW_LAX_QNODES]
                        Allow qnode suffixes in quantities to include alphas and dash as
                        well as digits. (default=False).
  --allow-language-suffixes [ALLOW_LANGUAGE_SUFFIXES]
                        Allow language identifier suffixes starting with a dash.
                        (default=False).
  --allow-lax-strings [ALLOW_LAX_STRINGS]
                        Do not check if double quotes are backslashed inside strings.
                        (default=False).
  --allow-lax-lq-strings [ALLOW_LAX_LQ_STRINGS]
                        Do not check if single quotes are backslashed inside language
                        qualified strings. (default=False).
  --allow-month-or-day-zero [ALLOW_MONTH_OR_DAY_ZERO]
                        Allow month or day zero in dates. (default=False).
  --repair-month-or-day-zero [REPAIR_MONTH_OR_DAY_ZERO]
                        Repair month or day zero in dates. (default=False).
  --allow-end-of-day [ALLOW_END_OF_DAY]
                        Allow 24:00:00 to represent the end of the day. (default=True).
  --minimum-valid-year MINIMUM_VALID_YEAR
                        The minimum valid year in dates. (default=1583).
  --clamp-minimum-year [CLAMP_MINIMUM_YEAR]
                        Clamp years at the minimum value. (default=False).
  --maximum-valid-year MAXIMUM_VALID_YEAR
                        The maximum valid year in dates. (default=2100).
  --clamp-maximum-year [CLAMP_MAXIMUM_YEAR]
                        Clamp years at the maximum value. (default=False).
  --allow-lax-coordinates [ALLOW_LAX_COORDINATES]
                        Allow coordinates using scientific notation. (default=False).
  --repair-lax-coordinates [REPAIR_LAX_COORDINATES]
                        Allow coordinates using scientific notation. (default=False).
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
                        Clamp longitudes at the minimum value. (default=False).
  --maximum-valid-lon MAXIMUM_VALID_LON
                        The maximum valid longitude. (default=180.000000).
  --clamp-maximum-lon [CLAMP_MAXIMUM_LON]
                        Clamp longitudes at the maximum value. (default=False).
  --modulo-repair-lon [MODULO_REPAIR_LON]
                        Wrap longitude to (-180.0,180.0]. (default=False).
  --escape-list-separators [ESCAPE_LIST_SEPARATORS]
                        Escape all list separators instead of splitting on them.
                        (default=False).
```

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

### --header-error-action
The action to take if a header error is detected, such as:

- An empty column name
- A duplicate column name
- A missing required column name for an edge or node file
- An ambiguous required column name (e.g., ‘id’ and ‘ID’ are both present)
Only ERROR and EXIT actions are implemented for header errors.

### --unsafe-column-name
The action to take if a header column name contains one of the following:
- Leading white space
- Trailing white space
- Internal white space except in strings or language-qualified strings
- Commas
- Vertical bars

### --error-limit
Execution will stop if the error limit is exceeded.  To avoid that, either
raise the error limit or set it to zero:

  --error-limit=0

### KGTK File Mode

|Mode|Meaning|
|----|-------|
|NONE|Do not require node1, node1, or id columns|
|EDGE|Treat the input file as a KGTK edge file and require the |presence of node1 and node2 columns or their allowable aliases.
|NODE|Treat the input file as a KGTK node file and require the presence of an id column or its allowable alias (ID).|
|AUTO|Automatically determine if an input file is an edge file or a node file. If a node1 (or allowable alias) column is present, assume that the file is a KGTK edge file. Otherwise, assume that it is a KGTK node file|

## Examples

Suppose that `file1.tsv` contains the following table in KGTK format:

| node1 | label | node2             |
| john  | woke  | ^2020-05-00T00:00 |
| john  | woke  | ^2020-05-02T00:00 |

### Validate the data, using default options

```bash
kgtk validate -i file1.tsv
```

The following complaint will be issued:
```
Data line 1:
john    woke    ^2020-05-00T00:00
col 2 (node2) value '^2020-05-00T00:00'is an Invalid Date and Times
```

The first data line was flagged because it contained "00" in the day
field, which violates the ISO 8601 specification.

### Allow month or day zero
Instruct the validator to accept month or day 00, even though
this is not allowed in ISO 6801.

```bash
kgtk validate -i file1.tsv --allow-month-or-day-zero
```
This results in no error messages.

### Validate with verbose feedback

Sometimes you may wish to get more feedback about what kgtk verbose is
doing.

```bash
kgtk validate -i file1.tsv --allow-month-or-day-zero --verbose
```

This results in the following output:
```
====================================================
Validating 'kgtk/join/test/clean_data-file1.tsv'
KgtkReader: File_path.suffix: .tsv
KgtkReader: reading file kgtk/join/test/clean_data-file1.tsv
header: node1   label   node2
node1 column found, this is a KGTK edge file
KgtkReader: Special columns: node1=0 label=1 node2=2 id=-1
KgtkReader: Reading an edge file.
Validated 2 data lines

```
