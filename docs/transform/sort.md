## Overview

This command will sort any KGTK file on one or more columns.
If more than one column is given, columns are compared in the order listed (not in the order they appear in the file).
Data is sorted in ascending order by default, but can also be sorted in reverse.
The command expects a KGTK file with a header line which will be included in the sorted output.

## Usage
```
usage: kgtk sort [-h] [-i INPUT] [-o OUTPUT_FILE] [-c [COLUMNS [COLUMNS ...]]]
                 [--locale LOCALE] [-r [True|False]]
                 [--pure-python [True|False]] [-X EXTRA]
                 [-v [optional True|False]]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input-file INPUT
                        Input file to sort. (May be omitted or '-' for stdin.)
  -o OUTPUT_FILE, --out OUTPUT_FILE, --output-file OUTPUT_FILE
                        Output file to write to. (May be omitted or '-' for
                        stdout.)
  -c [COLUMNS [COLUMNS ...]], --column [COLUMNS [COLUMNS ...]], --columns [COLUMNS [COLUMNS ...]]
                        space and/or comma-separated list of column names to
                        sort on. (defaults to id for node files, (node1,
                        label, node2) for edge files without ID, (id, node1,
                        label, node2) for edge files with ID)
  --locale LOCALE       LC_ALL locale controls the sorting order. (default=C)
  -r [True|False], --reverse [True|False]
                        When True, generate output in reverse sort order.
                        (default=False)
  --pure-python [True|False]
                        When True, sort in-memory with Python code.
                        (default=False)
  -X EXTRA, --extra EXTRA
                        extra options to supply to the sort program.
                        (default=None)

  -v [optional True|False], --verbose [optional True|False]
                        Print additional progress messages (default=False).
```

Input files can be piped in from stdin or named explicitly.  They can also be
optionally compressed and will transparently be decompressed.  Columns can be
specified by the names used in the file header line, as 1-based positions, or
through the pre-defined positions of reserved names such as `subject', etc.
Column names found in the header will override any predefined positions.

## Examples

### Sort a file based on label and node2.
```
kgtk sort -c label,node2 \
          -i examples/docs/movies_reduced.tsv
```

| id | node1 | label | node2 |
| -- | -- | -- | -- |
| t17 | terminator | award | national_film_registry |
| t10 | terminator | cast | arnold_schwarzenegger |
| t14 | terminator | cast | linda_hamilton |
| t12 | terminator | cast | michael_biehn |
| t9 | terminator | director | james_cameron |
| t16 | terminator | duration | 108 |
| t3 | terminator | genre | action |
| t4 | terminator | genre | science_fiction |
| t2 | terminator | instance_of | film |
| t1 | terminator | label | 'The Terminator'@en |
| t8 | t7 | location | sweden |
| t6 | t5 | location | united_states |
| t18 | t17 | point_in_time | ^2008-01-01T00:00:00Z/9 |
| t5 | terminator | publication_date | ^1984-10-26T00:00:00Z/11 |
| t7 | terminator | publication_date | ^1985-02-08T00:00:00Z/11 |
| t13 | t12 | role | kyle_reese |
| t15 | t14 | role | sarah_connor |
| t11 | t10 | role | terminator |

### Sort a file piped from another command based on label and node2.
```
kgtk cat -i examples/docs/movies_reduced.tsv.gz / \
     sort -c label,node2
```

| id | node1 | label | node2 |
| -- | -- | -- | -- |
| t17 | terminator | award | national_film_registry |
| t10 | terminator | cast | arnold_schwarzenegger |
| t14 | terminator | cast | linda_hamilton |
| t12 | terminator | cast | michael_biehn |
| t9 | terminator | director | james_cameron |
| t16 | terminator | duration | 108 |
| t3 | terminator | genre | action |
| t4 | terminator | genre | science_fiction |
| t2 | terminator | instance_of | film |
| t1 | terminator | label | 'The Terminator'@en |
| t8 | t7 | location | sweden |
| t6 | t5 | location | united_states |
| t18 | t17 | point_in_time | ^2008-01-01T00:00:00Z/9 |
| t5 | terminator | publication_date | ^1984-10-26T00:00:00Z/11 |
| t7 | terminator | publication_date | ^1985-02-08T00:00:00Z/11 |
| t13 | t12 | role | kyle_reese |
| t15 | t14 | role | sarah_connor |
| t11 | t10 | role | terminator |

### Sort a compressed file to a named output file.
```
kgtk sort -c 'label, id' \
          -i examples/docs/movies_reduced.tsv.gz \
	  -o nodes-sort.tsv
```

### Sort on a larger system using more resources.

Sort on a larger system using 24 threads, 60% of main memory, and
a nonstandard temporary file folder.

```
kgtk sort -i examples/docs/movies_reduced.tsv \
          -o movies_sorted.tsv \
	  -X "--parallel 24 --buffer-size 60% -T /data1/tmp"
```

### Sort in memory using pure Python instead of the system sort program.

```
kgtk sort -i examples/docs/movies_reduced.tsv \
          -o movies_sorted.tsv \
	  --pure-python
```

