The cat command combines (concatenates) KGTK files, optionally decompressing
input files and compressing the output file, while managing the KGTK column
headers appropriately. This differs from the zconcat command, which
decompresses and concatenates files without managing their KGTK headers.

Input and output files may be (de)compressed using a algorithm selected
by the file extension: .bz2 .gz .lz4 .xy

When merging the column headers, KGTK's required column aliases are respected,
with the leftmost alias seen taking priority.  For example, if the first
input file has a "node1" column and the second has a "from" column, the two
columns will be combined as the "node1" column in the output file.

Normally, the files being combined must be either all KGTK edge files or all
KGTK node files, but that constraint can be overridded with --mode=NONE.

Optionally, the output can be written in a selection of other formats.

## Usage

```bash
usage: kgtk cat [-h] [-o OUTPUT_FILE_PATH] [--output-format OUTPUT_FORMAT] [-v] input_file_paths [input_file_paths ...]

Concatenate two or more KGTK files, merging the columns appropriately. All files must be KGTK edge files or all files must be KGTK node files (unless overridden with --mode=NONE). 

Additional options are shown in expert help.
kgtk --expert cat --help

positional arguments:
  input_file_paths      The KGTK files to concatenate.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_FILE_PATH, --output-file OUTPUT_FILE_PATH
                        The KGTK file to write (default=-).
  --output-format OUTPUT_FORMAT
                        The file format (default=kgtk)

  -v, --verbose         Print additional progress messages (default=False).
```

## Output Formats

| Format | Extension | Description |
| ------ | --------- | ----------- |
| kgtk   | (default) | KGTK tab separated values file. |
| csv    | .csv      | A simple comma separated value file with doubled quoting and column headers. |
| md	 | .md       | GitHub markdown tables. |
| json   | .json     | JSON list of lists of strings with column header line. |
| json-map | (none)  | JSON list of maps from column names to string values. |
| json-map-compact | (none)  | JSON list of maps from column names to string values with empty values suppressed. |
| jsonl  | .jsonl    | JSON lines of lists of strings  with column header line. |
| jsonl-map | (none)  | JSON lines of maps from column names to string values. |
| jsonl-map-compact | (none)  | JSON lines of maps from column names to string values with empty values suppressed. |

## Examples

Combine two KGTK files, sending the output to standard output.

```bash
kgtk cat file1.tsv file2.tsv
```

Combine two gzipped KGTK files, sending the output to a bzip2 file.

```bash
kgtk cat file1.tsv.gz file2.tsv.gz -o ofile.tsv.bz2
```

Suppose that `file1.tsv` contains the following table in KGTK format:

| node1 | label   | node2 | location |
| ----- | ------- | ----- | -------- |
| john  | zipcode | 12345 | home     |
| john  | zipcode | 12346 | work     |
| peter | zipcode | 12040 | home     |
| peter | zipcode | 12040 | work     |
| steve | zipcode | 45601 | home     |
| steve | zipcode | 45601 | work     |

and `file2.tsv` contains the following table in KGTK format:

| node1 | label    | node2      | years |
| ----- | -------- | ---------- | ----- |
| john  | position | programmer | 3     |
| peter | position | engineer   | 2     |

The result will be the following table in KGTK format:

| node1 | label    | node2      | location | years |
| ----- | -------- | ---------- | -------- | ----- |
| john  | zipcode  | 12345      | home     |       |
| john  | zipcode  | 12346      | work     |       |
| peter | zipcode  | 12040      | home     |       |
| peter | zipcode  | 12040      | work     |       |
| steve | zipcode  | 45601      | home     |       |
| steve | zipcode  | 45601      | work     |       |
| john  | position | programmer |          | 3     |
| peter | position | engineer   |          | 2     |

