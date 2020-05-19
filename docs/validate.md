Command that will validate that a KGTK file complies with the specification in KGTK File Format v2. Currently, validation is limited to header column names and data column counts. It does not yet validate that headers and cells are compliant with the KGTK data type rules.


## Usage
usage: 
```
kgtk validate [-h]
                     [--blank-id-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}]
                     [--blank-node1-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}]
                     [--blank-node2-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}]
                     [--blank-required-field-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}]
                     [--column-separator COLUMN_SEPARATOR]
                        [--comment-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}]
                     [--compression-type COMPRESSION_TYPE]
                     [--empty-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}]
                     [--errors-to-stdout] [--error-limit ERROR_LIMIT]
                     [--fill-short-lines]
                     [--force-column-names FORCE_COLUMN_NAMES [FORCE_COLUMN_NAMES ...]]
                     [--gzip-in-parallel] [--gzip-queue-size GZIP_QUEUE_SIZE]
                     [--header-error-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}]
                     [--invalid-value-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}]
                        [--long-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}]
                     [--mode {NONE,EDGE,NODE,AUTO}]
                     [--short-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}]
                     [--skip-first-record] [--truncate-long-lines] [-v]
                        [--unsafe-column-name-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}]
                     [--very-verbose]
                     [--whitespace-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}]
                     [kgtk_file [kgtk_file …]]
```

positional arguments:
```
  kgtk_file             The KGTK file(s) to validate. May be omitted or '-' for stdin.
```

optional arguments:
```
  -h, --help            show this help message and exit
  --blank-id-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}
                        The action to take when a blank id field is detected.
  --blank-node1-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}
                        The action to take when a blank node1 field is detected.
  --blank-node2-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}
                        The action to take when a blank node2 field is detected.
  --blank-required-field-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}
                        The action to take when a line with a blank node1, node2, or
                        id field (per mode) is detected.
  --column-separator COLUMN_SEPARATOR
                        Column separator.
  --comment-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}
                        The action to take when a comment line is detected.
  --compression-type COMPRESSION_TYPE
                        Specify the input file compression type, otherwise use the
                        extension.
  --empty-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}
                        The action to take when an empty line is detected.
  --errors-to-stdout    Send errors to stdout instead of stderr
  --error-limit ERROR_LIMIT
                        The maximum number of errors to report before failing
  --fill-short-lines    Fill missing trailing columns in short lines with empty
                        values.
  --force-column-names FORCE_COLUMN_NAMES [FORCE_COLUMN_NAMES ...]
                        Force the column names.
  --gzip-in-parallel    Execute gzip in parallel.
  --gzip-queue-size GZIP_QUEUE_SIZE
                        Queue size for parallel gzip.
  --header-error-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}
                        The action to take when a header error is detected Only ERROR
                        or EXIT are supported.
  --header-only Process only the header of the input file.
  --invalid-value-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}
                        The action to take when a a data cell value is invalid.
  --long-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}
                        The action to take when a long line is detected.
  --mode {NONE,EDGE,NODE,AUTO}
                        Determine the KGTK input file mode.
  --short-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}
                        The action to take whe a short line is detected.
  --skip-first-record   Skip the first record when forcing column names.
  --truncate-long-lines
                        Remove excess trailing columns in long lines.
  --unsafe-column-name-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}
                        The action to take when a column name is unsafe.
  -v, --verbose         Print additional progress messages.
  --very-verbose        Print additional progress messages.
  --whitespace-line-action {PASS,REPORT,EXCLUDE,COMPLAIN,ERROR,EXIT}
                        The action to take when a whitespace line is detected.
```

## Additional Usage Notes
### kgtk_file
The input file may be specified by path.  The file path “-” is reserved for standard input; omitting the input file also defaults to standard input. Multiple files may be specified.

### --blank-id-line-action
KGTK File Format v2 specifies that lines in node files that contain empty values in the id column (or an allowable alias) are to be ignored.

|Action keyword|Action when condition detected|
|--------------|------------------------------|
|PASS|Silently allow the data line to pass through|
|REPORT|Report the data line and let it pass through|
|EXCLUDE|Silently exclude (ignore) the data line|
|COMPLAIN|Report the data line and exclude (ignore) it|
|ERROR|Raise a ValueError|
|EXIT|sys.exit(1)|

### --blank-node1-line-action
KGTK File Format v2 specifies that lines in edge files that contain empty values in the node1 column (or an allowable alias) are to be ignored. 

### --blank-node2-line-action
KGTK File Format v2 specifies that lines in edge files that contain empty values in the node2 column (or an allowable alias) are to be ignored. 

### --blank-required-field-line-action
This option is intended for use in auto detection mode.  It supplies the default value for --blank-id-line-action for node files and the default values for --blank-node1-line-actin and 

### --blank-node2-line-action for edge files.
KGTK File Format v2 specifies that lines containing only whitespace are to be ignored. 

### --column-separator
KGTK File Format v2 specifies that columns are separated by the tab character. The column separator may be overridden to allow a different separator, such as a comma, although there may be complications, such as comma characters inside quoted strings.
### --compression-type
If the input path ends with one of the following extensions, it will be automatically decompressed. Alternatively, the --compression-type option may be specified to force the selection of a specific decompressor.

|Extension|Decompression|
|---------|-------------|
|.bz2|bzip2|
|.gz|gzip|
|.lz4|lz4|
|.xz|lzma|

### --comment-line-action
KGTK File Format v2 specifies that lines beginning with “#” are comment lines.

### --empty-line-action
KGTK File Format v2 specifies that empty lines (a special case of whitespace lines) should be ignored. 

### --errors-to-stdout
Error messages are normally written to stdout. This option causes error messages to be written to stdout, which is occasionally useful when debugging.

### --error-limit
Ths maximum number of errors to report before failing. The default value is 1000.

### --force-column-names
Supply a set of column names to either override the first line of the input file or to supply column headers, when missing from the input file (see --skip-first-record). The column names are a whitespace separated list.

### --gzip-in-parallel
This option runs the select decompressor or compressor in a parallel process. This currently results in degraded performance, but it may be possible to gain a performance advantage with more sophisticated inter-process communication.

### --gzip-queue-size
This is an implementation parameter for the (de)compression parallelization.

### --header-error-action
The action to take if a header error is detected, such as:

- An empty column name
- A duplicate column name
- A missing required column name for an edge or node file
- An ambiguous required column name (e.g., ‘id’ and ‘ID’ are both present)
Only ERROR and EXIT actions are implemented for header errors.

### --invalid-value-action
The action to take if a data cell does not meet the data type requirements given in the KGTK File Format v2.

- Numbers
- Strings
- Language-qualified strings
- Date and times
- Location coordinates
- Symbols
- Quantities are not recognized yet.


The default is to check for valid values, complain about a row with any invalid values, and continue to process the row.  If you select the PASS action, then data cell value validation will be bypassed, with significant performance benefits.

### --long-line-action
KGTK File Format v2 specifies that data lines should have the same number of fields as there are columns.

### --mode
Determine the KGTk input file mode.

|Mode|Meaning|
|----|-------|
|NONE|Do not require node1, node1, or id columns|
|EDGE|Treat the input file as a KGTK edge file and require the |presence of node1 and node2 columns or their allowable aliases.
|NODE|Treat the input file as a KGTK node file and require the presence of an id column or its allowable alias (ID).|
|AUTO|Automatically determine if an input file is an edge file or a node file. If a node1 (or allowable alias) column is present, assume that the file is a KGTK edge file. Otherwise, assume that it is a KGTK node file|

### --short-line-action
KGTK File Format v2 specifies that data lines should have the same number of fields as there are columns. 

### --skip-first-record
When --force-column-names has supplied a set of column names, this option may be supplied to indicate that the forced column names should replace the first (header) line of the input file.

### --unsafe-column-name
The action to take if a header column name contains one of the following:
- Leading white space
- Trailing white space
- Internal white space except in strings or language-qualified strings
- Commas
- Vertical bars
- Semicolons
  
### --whitespace-line-action
KGTK File Format v2 specifies that data lines containing only whitespace characters should be ignored. 

## Examples
In this example, the input file has spaces instead of tabs in the header line.
```bash
python3 -m kgtk validate -v ../../drive/datasets/edges-v2-property-stats-labeled.tsv
Validating '../../drive/datasets/edges-v2-property-stats-labeled.tsv'
KgtkReader: File_path.suffix: .tsv
KgtkReader: reading file ../../drive/datasets/edges-v2-property-stats-labeled.tsv
header: id      count   label
In input header 'id      count   label': Column name 'id      count   label' contains internal white space
node1 column not found, assuming this is a KGTK node file
In input header 'id      count   label': Missing required column: id | ID
Exit requested
```

In this example, some of the data lines are missing columns.
```bash
Validating '../../drive/datasets/edges-v3-short-ids-extra-columns.tsv.gz'
KgtkReader: File_path.suffix: .gz
KgtkReader: reading gzip ../../drive/datasets/edges-v3-short-ids-extra-columns.tsv.gz
header: id      node1   label   node2   magnitude       unit    lower   upper   latitude        longitude       precision       calendar        entity-type
node1 column found, this is a KGTK edge file
KgtkReader: Reading an edge file. node1=1 label=2 node2=3
In input data line 1445572, Required 13 columns, saw 4: '__1445572      Q503323 P3625   &"': __1445572  Q503323 P3625   &"
In input data line 1445582, saw an empty line:
In input data line 1445583, Required 13 columns, saw 1: 'Q503323': Q503323
In input data line 1445584, Required 13 columns, saw 2: '       P2859':         P2859
In input data line 1445585, Required 13 columns, saw 11: '      6"                                                                      ':      6"
In input data line 2237571, Required 13 columns, saw 4: '__2237558      Q864677 P3625   r"': __2237558  Q864677 P3625   r"
In input data line 2237581, saw an empty line:
In input data line 2237582, Required 13 columns, saw 1: 'Q864677': Q864677
In input data line 2237583, Required 13 columns, saw 2: '       P3917':         P3917
In input data line 2237584, Required 13 columns, saw 2: '       +123':  +123
In input data line 2237585, Required 13 columns, saw 2: '       +123':  +123
In input data line 2237594, saw an empty line:
```
In this example, the KGTk file starts with a comment instead of a header line.

```bash
Validating '../../drive/datasets/edges-v2-property-stats.tsv'
KgtkReader: File_path.suffix: .tsv
KgtkReader: reading file ../../drive/datasets/edges-v2-property-stats.tsv
header: # > date; zcat edges-v2.csv.gz | cut -f 3 | sort | uniq -c > property-stats.log; date
In input header '# > date; zcat edges-v2.csv.gz | cut -f 3 | sort | uniq -c > property-stats.log; date': Column name '# > date; zcat edges-v2.csv.gz | cut -f 3 | sort | uniq -c > property-stats.log; date' contains internal white space, Column name '# > date; zcat edges-v2.csv.gz | cut -f 3 | sort | uniq -c > property-stats.log; date' contains a vertical bar (|), Column name '# > date; zcat edges-v2.csv.gz | cut -f 3 | sort | uniq -c > property-stats.log; date' contains a semicolon (;)
node1 column not found, assuming this is a KGTK node file
In input header '# > date; zcat edges-v2.csv.gz | cut -f 3 | sort | uniq -c > property-stats.log; date': Missing required column: id | ID
Command exited with non-zero status 1
```