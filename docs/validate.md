Validate one or more KGTK files, optionally decompressing
the input files.

Input files may be (de)compressed using a algorithm selected
by the file extension: .bz2 .gz .lz4 .xy

The expert option --compression-type may be used to override the
decompression selectin algorithim;  this is useful when reading from piped input.

## Usage
```
usage: kgtk validate [-h] [--header-only [HEADER_ONLY]]
                     [--errors-to-stdout | --errors-to-stderr] [--show-options] [-v]
                     [--very-verbose] [--column-separator COLUMN_SEPARATOR]
                     [--compression-type COMPRESSION_TYPE] [--error-limit ERROR_LIMIT]
                     [--gzip-in-parallel [GZIP_IN_PARALLEL]]
                     [--gzip-queue-size GZIP_QUEUE_SIZE] [--mode {NONE,EDGE,NODE,AUTO}]
                     [--force-column-names FORCE_COLUMN_NAMES [FORCE_COLUMN_NAMES ...]]
                     [--header-error-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}]
                     [--skip-first-record [SKIP_FIRST_RECORD]]
                     [--unsafe-column-name-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}]
                     [--repair-and-validate-lines [REPAIR_AND_VALIDATE_LINES]]
                     [--repair-and-validate-values [REPAIR_AND_VALIDATE_VALUES]]
                     [--blank-required-field-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}]
                     [--comment-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}]
                     [--empty-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}]
                     [--fill-short-lines [FILL_SHORT_LINES]]
                     [--invalid-value-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}]
                     [--long-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}]
                     [--short-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}]
                     [--truncate-long-lines [TRUNCATE_LONG_LINES]]
                     [--whitespace-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}]
                     [--additional-language-codes [ADDITIONAL_LANGUAGE_CODES [ADDITIONAL_LANGUAGE_CODES ...]]]
                     [--allow-language-suffixes [ALLOW_LANGUAGE_SUFFIXES]]
                     [--allow-lax-strings [ALLOW_LAX_STRINGS]]
                     [--allow-lax-lq-strings [ALLOW_LAX_LQ_STRINGS]]
                     [--allow-month-or-day-zero [ALLOW_MONTH_OR_DAY_ZERO]]
                     [--repair-month-or-day-zero [REPAIR_MONTH_OR_DAY_ZERO]]
                     [--minimum-valid-year MINIMUM_VALID_YEAR]
                     [--maximum-valid-year MAXIMUM_VALID_YEAR]
                     [--minimum-valid-lat MINIMUM_VALID_LAT]
                     [--maximum-valid-lat MAXIMUM_VALID_LAT]
                     [--minimum-valid-lon MINIMUM_VALID_LON]
                     [--maximum-valid-lon MAXIMUM_VALID_LON]
                     [--escape-list-separators [ESCAPE_LIST_SEPARATORS]]
                     [kgtk_files [kgtk_files ...]]

Validate a KGTK file. Empty lines, whitespace lines, comment lines, and lines with empty required fields are silently skipped. Header errors cause an immediate exception. Data value errors are reported. 

To validate data and pass clean data to an output file or pipe, use the kgtk clean_data command.

Additional options are shown in expert help.
kgtk --expert validate --help

positional arguments:
  kgtk_files            The KGTK file(s) to validate. May be omitted or '-' for stdin.

optional arguments:
  -h, --help            show this help message and exit
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
  Options affecting processing

  --column-separator COLUMN_SEPARATOR
                        Column separator (default=<TAB>).
  --compression-type COMPRESSION_TYPE
                        Specify the compression type (default=None).
  --error-limit ERROR_LIMIT
                        The maximum number of errors to report before failing (default=1000)
  --gzip-in-parallel [GZIP_IN_PARALLEL]
                        Execute gzip in parallel (default=False).
  --gzip-queue-size GZIP_QUEUE_SIZE
                        Queue size for parallel gzip (default=1000).
  --mode {NONE,EDGE,NODE,AUTO}
                        Determine the KGTK file mode (default=KgtkReaderMode.AUTO).

Header parsing:
  Options affecting header parsing

  --force-column-names FORCE_COLUMN_NAMES [FORCE_COLUMN_NAMES ...]
                        Force the column names (default=None).
  --header-error-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}
                        The action to take when a header error is detected. Only ERROR or EXIT
                        are supported (default=ValidationAction.EXIT).
  --skip-first-record [SKIP_FIRST_RECORD]
                        Skip the first record when forcing column names (default=False).
  --unsafe-column-name-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}
                        The action to take when a column name is unsafe
                        (default=ValidationAction.REPORT).

Line parsing:
  Options affecting data line parsing

  --repair-and-validate-lines [REPAIR_AND_VALIDATE_LINES]
                        Repair and validate lines (default=True).
  --repair-and-validate-values [REPAIR_AND_VALIDATE_VALUES]
                        Repair and validate values (default=True).
  --blank-required-field-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}
                        The action to take when a line with a blank node1, node2, or id field
                        (per mode) is detected (default=ValidationAction.EXCLUDE).
  --comment-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}
                        The action to take when a comment line is detected
                        (default=ValidationAction.EXCLUDE).
  --empty-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}
                        The action to take when an empty line is detected
                        (default=ValidationAction.EXCLUDE).
  --fill-short-lines [FILL_SHORT_LINES]
                        Fill missing trailing columns in short lines with empty values
                        (default=False).
  --invalid-value-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}
                        The action to take when a data cell value is invalid
                        (default=ValidationAction.COMPLAIN).
  --long-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}
                        The action to take when a long line is detected
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
                        Additional language codes (default=None).
  --allow-language-suffixes [ALLOW_LANGUAGE_SUFFIXES]
                        Allow language identifier suffixes starting with a dash
                        (default=False).
  --allow-lax-strings [ALLOW_LAX_STRINGS]
                        Do not check if double quotes are backslashed inside strings
                        (default=False).
  --allow-lax-lq-strings [ALLOW_LAX_LQ_STRINGS]
                        Do not check if single quotes are backslashed inside language qualified
                        strings (default=False).
  --allow-month-or-day-zero [ALLOW_MONTH_OR_DAY_ZERO]
                        Allow month or day zero in dates (default=False).
  --repair-month-or-day-zero [REPAIR_MONTH_OR_DAY_ZERO]
                        Repair month or day zero in dates (default=False).
  --minimum-valid-year MINIMUM_VALID_YEAR
                        The minimum valid year in dates (default=1583).
  --maximum-valid-year MAXIMUM_VALID_YEAR
                        The maximum valid year in dates (default=2100).
  --minimum-valid-lat MINIMUM_VALID_LAT
                        The minimum valid latitude (default=-90.000000).
  --maximum-valid-lat MAXIMUM_VALID_LAT
                        The maximum valid latitude (default=90.000000).
  --minimum-valid-lon MINIMUM_VALID_LON
                        The minimum valid longitude (default=-180.000000).
  --maximum-valid-lon MAXIMUM_VALID_LON
                        The maximum valid longitude (default=180.000000).
  --escape-list-separators [ESCAPE_LIST_SEPARATORS]
                        Escape all list separators instead of splitting on them
                        (default=False).
```

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

## Examples

Suppose that `file1.tsv` contains the following table in KGTK format:

| node1 | label | node2             |
| john  | woke  | ^2020-05-00T00:00 |
| john  | woke  | ^2020-05-02T00:00 |

### Validate the data, using default options

```bash
kgtk clean_data file1.tsv
```

Standard output will get the following data:
```
node1   label   node2
john    woke    ^2020-05-02T00:00
```

The following complaint will be issued on standard error:
```
Data line 1:
john    woke    ^2020-05-00T00:00
col 2 (node2) value '^2020-05-00T00:00'is an Invalid Date and Times
```

The first data line was excluded because it contained "00" in the day
field, which violates the ISO 8601 specification.

### Clean the data, repairing the invalid date/time string
Change day "00" to day "01:

```bash
kgtk clean_data file1.tsv --repair-month-or-day-zero
```

Standard output will get the following data, and no errors will be issued:
```
node1   label   node2
john    woke    ^2020-05-01T00:00
john    woke    ^2020-05-02T00:00
```
