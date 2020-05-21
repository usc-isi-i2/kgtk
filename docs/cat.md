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

## Usage

```bash
kgtk cat [-h] [-o OUTPUT_FILE_PATH] [-v] input_file_paths [input_file_paths ...]
```
- `input_file_paths` are the input file names.  At most one input file may be "-" for data piped from another command.
- `OUTPUT_FILE_PATH` can be a filename or "-" to pipe data to another command (default is "-").
- `-v` gives verbose feedback.

Additional options are described in expert help:
```bash
kgtk --expert cat --help
```

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

