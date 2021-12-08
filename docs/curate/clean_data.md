## Summary

Validate and clean the data in a KGTK file, optionally decompressing
the input files and compressing the output file.

Input and output files may be (de)compressed using a algorithm selected
by the file extension: .bz2 .gz .lz4 .xy

### Default Rules

By default, the following rules apply:

 - errors that occur while processing a KGTK file's column header line cause an immediate exit:
   - An empty column name
   - A duplicate column name
   - A missing required column name for an edge or node file
   - An ambiguous required column name (e.g., `id` and `ID` are both present)
 - empty data lines are silently ignored and not passed through.
 - data lines containing only whitespace are silently ignored and not passed through.
 - data lines with empty required fields (node1 and node2 for KGTK edge files, id for KGTK node files) are silently ignored and not passed through.
 - data lines that have too few fields cause a complaint to be issued, and are not passed through.
 - data lines that have too many fields cause a complaint to be issued, and are not passed through.
 - lines with data value validation errors cause a complaint to be issued, and are not passed through.

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

## Usage
```
usage: kgtk clean-data [-h] [-i INPUT_FILE] [-o OUTPUT_FILE]
                       [--reject-file REJECT_FILE] [-v [optional True|False]]

Validate a KGTK file and output a clean copy. Empty lines, whitespace lines, comment lines, and lines with empty required fields are silently skipped. Header errors cause an immediate exception. Data value errors are reported and the line containing them skipped. 

Additional options are shown in expert help.
kgtk --expert clean-data --help

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK input file. (May be omitted or '-' for
                        stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for
                        stdout.)
  --reject-file REJECT_FILE
                        Reject file (Optional, use '-' for stdout.)

  -v [optional True|False], --verbose [optional True|False]
                        Print additional progress messages (default=False).
```

## Expert Usage
```
usage: kgtk clean-data [-h] [-i INPUT_FILE] [-o OUTPUT_FILE]
                       [--reject-file REJECT_FILE]
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
                       [--implied-label IMPLIED_LABEL]
                       [--use-graph-cache-envar [optional True|False]]
                       [--graph-cache GRAPH_CACHE]
                       [--graph-cache-fetchmany-size GRAPH_CACHE_FETCHMANY_SIZE]
                       [--graph-cache-filter-batch-size GRAPH_CACHE_FILTER_BATCH_SIZE]
                       [--mode {NONE,EDGE,NODE,AUTO}]
                       [--input-column-names FORCE_COLUMN_NAMES [FORCE_COLUMN_NAMES ...]]
                       [--no-input-header [optional True|False]]
                       [--header-error-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}]
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

Validate a KGTK file and output a clean copy. Empty lines, whitespace lines, comment lines, and lines with empty required fields are silently skipped. Header errors cause an immediate exception. Data value errors are reported and the line containing them skipped. 

Additional options are shown in expert help.
kgtk --expert clean-data --help

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK input file. (May be omitted or '-' for
                        stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for
                        stdout.)
  --reject-file REJECT_FILE
                        Reject file (Optional, use '-' for stdout.)

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
  --implied-label IMPLIED_LABEL
                        When specified, imply a label colum with the specified
                        value (default=None).
  --use-graph-cache-envar [optional True|False]
                        use KGTK_GRAPH_CACHE if --graph-cache is not
                        specified. (default=True).
  --graph-cache GRAPH_CACHE
                        When specified, look for input files in a graph cache.
                        (default=None).
  --graph-cache-fetchmany-size GRAPH_CACHE_FETCHMANY_SIZE
                        Graph cache transfer buffer size. (default=1000).
  --graph-cache-filter-batch-size GRAPH_CACHE_FILTER_BATCH_SIZE
                        Graph cache filter batch size. (default=1000).
  --mode {NONE,EDGE,NODE,AUTO}
                        Determine the KGTK file mode
                        (default=KgtkReaderMode.AUTO).

Header parsing:
  Options affecting header parsing.

  --input-column-names FORCE_COLUMN_NAMES [FORCE_COLUMN_NAMES ...], --force-column-names FORCE_COLUMN_NAMES [FORCE_COLUMN_NAMES ...]
                        Supply input column names when the input file does not
                        have a header record (--no-input-header=True), or
                        forcibly override the column names when a header row
                        exists (--no-input-header=False) (default=None).
  --no-input-header [optional True|False]
                        When the input file does not have a header record,
                        specify --no-input-header=True and --input-column-
                        names. When the input file does have a header record
                        that you want to forcibly override, specify --input-
                        column-names and --no-input-header=False. --no-input-
                        header has no effect when --input-column-names has not
                        been specified. (default=False).
  --header-error-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}
                        The action to take when a header error is detected.
                        Only ERROR or EXIT are supported
                        (default=ValidationAction.EXIT).
  --unsafe-column-name-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}
                        The action to take when a column name is unsafe
                        (default=ValidationAction.REPORT).
  --prohibit-whitespace-in-column-names [optional True|False]
                        Prohibit whitespace in column names. (default=False).

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
  --validate-fromisoformat [VALIDATE_FROMISOFORMAT]
                        Validate that datetime.fromisoformat(...) can parse
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
kgtk cat -i examples/docs/clean-data-file1.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| john | woke | ^2020-05-02T00:00 |
| john | woke | ^2020-05-00T00:00 |
| john | slept | ^2020-05-02T24:00 |
| lionheart | born | ^1157-09-08T00:00 |
| year0001 | starts | ^0001-01-01T00:00 |
| year9999 | ends | ^9999-12-31T11:59:59 |

### Clean the data, using default options

```bash
kgtk clean-data -i examples/docs/clean-data-file1.tsv
```

Standard output will get the following data:

| node1 | label | node2 |
| -- | -- | -- |
| john | woke | ^2020-05-02T00:00 |
| john | slept | ^2020-05-02T24:00 |

The following complaints will be issued on standard error:

    Data line 2:
    john	woke	^2020-05-00T00:00
    col 2 (node2) value '^2020-05-00T00:00' is an Invalid Date and Times
    Data line 4:
    lionheart	born	^1157-09-08T00:00
    col 2 (node2) value '^1157-09-08T00:00' is an Invalid Date and Times
    Data line 5:
    year0001	starts	^0001-01-01T00:00
    col 2 (node2) value '^0001-01-01T00:00' is an Invalid Date and Times
    Data line 6:
    year9999	ends	^9999-12-31T11:59:59
    col 2 (node2) value '^9999-12-31T11:59:59' is an Invalid Date and Times


The second data line was excluded because it contained "00" in the day
field, which violates the ISO 8601 specification.

The fourth data line was excluded because year 1157 is before the
start of the ISO 8601 normal era, year 1583.

The fifth data line was excluded because year 1157 is before the
start of the ISO 8601 normal era, year 1583.

The sixth data line was excluded because year 9999 is after the
sanity check 2100 cutoff.


### Repair Month or Day "00"

Change day "00" to day "01:

```bash
kgtk clean-data -i examples/docs/clean-data-file1.tsv \
                --repair-month-or-day-zero
```

Standard output will get the following data, and other errors will be issued:

| node1 | label | node2 |
| -- | -- | -- |
| john | woke | ^2020-05-02T00:00 |
| john | woke | ^2020-05-01T00:00 |
| john | slept | ^2020-05-02T24:00 |


    Data line 4:
    lionheart	born	^1157-09-08T00:00
    col 2 (node2) value '^1157-09-08T00:00' is an Invalid Date and Times
    Data line 5:
    year0001	starts	^0001-01-01T00:00
    col 2 (node2) value '^0001-01-01T00:00' is an Invalid Date and Times
    Data line 6:
    year9999	ends	^9999-12-31T11:59:59
    col 2 (node2) value '^9999-12-31T11:59:59' is an Invalid Date and Times

### Accept Years from 1 AD


```bash
kgtk clean-data -i examples/docs/clean-data-file1.tsv \
                --repair-month-or-day-zero \
                --minimum-valid-year 1
```

Standard output will get the following data, and other errors will be issued:

| node1 | label | node2 |
| -- | -- | -- |
| john | woke | ^2020-05-02T00:00 |
| john | woke | ^2020-05-01T00:00 |
| john | slept | ^2020-05-02T24:00 |
| lionheart | born | ^1157-09-08T00:00 |
| year0001 | starts | ^0001-01-01T00:00 |


    Data line 6:
    year9999	ends	^9999-12-31T11:59:59
    col 2 (node2) value '^9999-12-31T11:59:59' is an Invalid Date and Times

!!! note
    Year 0001 is the earliest year that can be processed by the Python standard
    library date and time modules.

### Accept Years up to 9999 AD


```bash
kgtk clean-data -i examples/docs/clean-data-file1.tsv \
                --repair-month-or-day-zero \
                --minimum-valid-year 1 \
                --maximum-valid-year 9999
```

Standard output will get the following data, and no other errors will be issued:

| node1 | label | node2 |
| -- | -- | -- |
| john | woke | ^2020-05-02T00:00 |
| john | woke | ^2020-05-01T00:00 |
| john | slept | ^2020-05-02T24:00 |
| lionheart | born | ^1157-09-08T00:00 |
| year0001 | starts | ^0001-01-01T00:00 |
| year9999 | ends | ^9999-12-31T11:59:59 |

!!! note
    Year 9999 is the latest year that can be processed by the Python standard
    library date and time modules.
