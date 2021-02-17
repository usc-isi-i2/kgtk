## Overview

This command will sort any KGTK file on one or more columns.
If more than one column is given, columns are compared in the order listed (not in the order they appear in the file).
Data is sorted in ascending order by default, but can also be sorted in reverse.
The command expects a KGTK file with a header line which will be included in the sorted output.

## Usage
```
usage: kgtk sort [-h] [-i INPUT] [-o OUTPUT_FILE] [-c [COLUMNS [COLUMNS ...]]]
                 [--locale LOCALE] [-r [True|False]]
                 [--reverse-columns [REVERSE_COLUMNS [REVERSE_COLUMNS ...]]]
                 [--numeric [True|False]]
                 [--numeric-columns [NUMERIC_COLUMNS [NUMERIC_COLUMNS ...]]]
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
                        sort on (the key columns). (defaults to id for node
                        files, (node1, label, node2) for edge files without
                        ID, (id, node1, label, node2) for edge files with ID)
  --locale LOCALE       LC_ALL locale controls the sorting order. (default=C)
  -r [True|False], --reverse [True|False]
                        When True, generate output in reverse (descending)
                        sort order. All key columns are sorted in reverse
                        order. (default=False)
  --reverse-columns [REVERSE_COLUMNS [REVERSE_COLUMNS ...]]
                        List specific key columns for reverse (descending)
                        sorting. Overidden by --reverse. (default=none)
  --numeric [True|False]
                        When True, generate output in numeric sort order. All
                        key columns are sorted in numeric order.
                        (default=False)
  --numeric-columns [NUMERIC_COLUMNS [NUMERIC_COLUMNS ...]]
                        List specific key columns for numeric sorting.
                        Overridden by --numeric. (default=none)
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

### Sort a file with the default keys:
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

### Sort a file based on `node1`, `label`, and `node2`, ignoring `id`
```
kgtk sort -i examples/docs/movies_reduced.tsv \
          -c node1 label node2
```

| id | node1 | label | node2 |
| -- | -- | -- | -- |
| t11 | t10 | role | terminator |
| t13 | t12 | role | kyle_reese |
| t15 | t14 | role | sarah_connor |
| t18 | t17 | point_in_time | ^2008-01-01T00:00:00Z/9 |
| t6 | t5 | location | united_states |
| t8 | t7 | location | sweden |
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
| t5 | terminator | publication_date | ^1984-10-26T00:00:00Z/11 |
| t7 | terminator | publication_date | ^1985-02-08T00:00:00Z/11 |

### Sort a file piped from another command based on `node1`, `label`, and `node2`.
```
kgtk cat -i examples/docs/movies_reduced.tsv.gz / \
     sort -c node1,label,node2
```

| id | node1 | label | node2 |
| -- | -- | -- | -- |
| t11 | t10 | role | terminator |
| t13 | t12 | role | kyle_reese |
| t15 | t14 | role | sarah_connor |
| t18 | t17 | point_in_time | ^2008-01-01T00:00:00Z/9 |
| t6 | t5 | location | united_states |
| t8 | t7 | location | sweden |
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
| t5 | terminator | publication_date | ^1984-10-26T00:00:00Z/11 |
| t7 | terminator | publication_date | ^1985-02-08T00:00:00Z/11 |

!!! note
    This example also used commas in the list of column names.

### Sort a compressed file to a named output file.
```
kgtk sort -i examples/docs/movies_reduced.tsv.gz \
	  -o movies_sorted.tsv
```

### Sort on a larger system using more resources.

Sort on a larger system using 24 threads, 60% of main memory, and
a nonstandard temporary file folder.

```
kgtk sort -i examples/docs/movies_reduced.tsv \
	  -X "--parallel 24 --buffer-size 60% -T /data1/tmp"
```

| id | node1 | label | node2 |
| -- | -- | -- | -- |
| t1 | terminator | label | 'The Terminator'@en |
| t10 | terminator | cast | arnold_schwarzenegger |
| t11 | t10 | role | terminator |
| t12 | terminator | cast | michael_biehn |
| t13 | t12 | role | kyle_reese |
| t14 | terminator | cast | linda_hamilton |
| t15 | t14 | role | sarah_connor |
| t16 | terminator | duration | 108 |
| t17 | terminator | award | national_film_registry |
| t18 | t17 | point_in_time | ^2008-01-01T00:00:00Z/9 |
| t2 | terminator | instance_of | film |
| t3 | terminator | genre | action |
| t4 | terminator | genre | science_fiction |
| t5 | terminator | publication_date | ^1984-10-26T00:00:00Z/11 |
| t6 | t5 | location | united_states |
| t7 | terminator | publication_date | ^1985-02-08T00:00:00Z/11 |
| t8 | t7 | location | sweden |
| t9 | terminator | director | james_cameron |

### Sort in memory using pure Python instead of the system sort program.

```
kgtk sort -i examples/docs/movies_reduced.tsv \
	  --pure-python
```

| id | node1 | label | node2 |
| -- | -- | -- | -- |
| t1 | terminator | label | 'The Terminator'@en |
| t10 | terminator | cast | arnold_schwarzenegger |
| t11 | t10 | role | terminator |
| t12 | terminator | cast | michael_biehn |
| t13 | t12 | role | kyle_reese |
| t14 | terminator | cast | linda_hamilton |
| t15 | t14 | role | sarah_connor |
| t16 | terminator | duration | 108 |
| t17 | terminator | award | national_film_registry |
| t18 | t17 | point_in_time | ^2008-01-01T00:00:00Z/9 |
| t2 | terminator | instance_of | film |
| t3 | terminator | genre | action |
| t4 | terminator | genre | science_fiction |
| t5 | terminator | publication_date | ^1984-10-26T00:00:00Z/11 |
| t6 | t5 | location | united_states |
| t7 | terminator | publication_date | ^1985-02-08T00:00:00Z/11 |
| t8 | t7 | location | sweden |
| t9 | terminator | director | james_cameron |


### Reverse sort using the system sort program.

```
kgtk sort -i examples/docs/movies_reduced.tsv \
          --reverse
```

| id | node1 | label | node2 |
| -- | -- | -- | -- |
| t9 | terminator | director | james_cameron |
| t8 | t7 | location | sweden |
| t7 | terminator | publication_date | ^1985-02-08T00:00:00Z/11 |
| t6 | t5 | location | united_states |
| t5 | terminator | publication_date | ^1984-10-26T00:00:00Z/11 |
| t4 | terminator | genre | science_fiction |
| t3 | terminator | genre | action |
| t2 | terminator | instance_of | film |
| t18 | t17 | point_in_time | ^2008-01-01T00:00:00Z/9 |
| t17 | terminator | award | national_film_registry |
| t16 | terminator | duration | 108 |
| t15 | t14 | role | sarah_connor |
| t14 | terminator | cast | linda_hamilton |
| t13 | t12 | role | kyle_reese |
| t12 | terminator | cast | michael_biehn |
| t11 | t10 | role | terminator |
| t10 | terminator | cast | arnold_schwarzenegger |
| t1 | terminator | label | 'The Terminator'@en |

### Reverse sort in memory using pure Python.

```
kgtk sort -i examples/docs/movies_reduced.tsv \
          --reverse \
          --pure-python
```

| id | node1 | label | node2 |
| -- | -- | -- | -- |
| t9 | terminator | director | james_cameron |
| t8 | t7 | location | sweden |
| t7 | terminator | publication_date | ^1985-02-08T00:00:00Z/11 |
| t6 | t5 | location | united_states |
| t5 | terminator | publication_date | ^1984-10-26T00:00:00Z/11 |
| t4 | terminator | genre | science_fiction |
| t3 | terminator | genre | action |
| t2 | terminator | instance_of | film |
| t18 | t17 | point_in_time | ^2008-01-01T00:00:00Z/9 |
| t17 | terminator | award | national_film_registry |
| t16 | terminator | duration | 108 |
| t15 | t14 | role | sarah_connor |
| t14 | terminator | cast | linda_hamilton |
| t13 | t12 | role | kyle_reese |
| t12 | terminator | cast | michael_biehn |
| t11 | t10 | role | terminator |
| t10 | terminator | cast | arnold_schwarzenegger |
| t1 | terminator | label | 'The Terminator'@en |

### Reverse sort a list of columns using the system sort program.

```
kgtk sort -i examples/docs/movies_reduced.tsv \
          --columns node1 label node2 \
	  --reverse
```

| id | node1 | label | node2 |
| -- | -- | -- | -- |
| t7 | terminator | publication_date | ^1985-02-08T00:00:00Z/11 |
| t5 | terminator | publication_date | ^1984-10-26T00:00:00Z/11 |
| t1 | terminator | label | 'The Terminator'@en |
| t2 | terminator | instance_of | film |
| t4 | terminator | genre | science_fiction |
| t3 | terminator | genre | action |
| t16 | terminator | duration | 108 |
| t9 | terminator | director | james_cameron |
| t12 | terminator | cast | michael_biehn |
| t14 | terminator | cast | linda_hamilton |
| t10 | terminator | cast | arnold_schwarzenegger |
| t17 | terminator | award | national_film_registry |
| t8 | t7 | location | sweden |
| t6 | t5 | location | united_states |
| t18 | t17 | point_in_time | ^2008-01-01T00:00:00Z/9 |
| t15 | t14 | role | sarah_connor |
| t13 | t12 | role | kyle_reese |
| t11 | t10 | role | terminator |

### Reverse sort a specific column using the system sort program.

```
kgtk sort -i examples/docs/movies_reduced.tsv \
          --columns node1 label node2 \
          --reverse-column node2
```

| id | node1 | label | node2 |
| -- | -- | -- | -- |
| t11 | t10 | role | terminator |
| t13 | t12 | role | kyle_reese |
| t15 | t14 | role | sarah_connor |
| t18 | t17 | point_in_time | ^2008-01-01T00:00:00Z/9 |
| t6 | t5 | location | united_states |
| t8 | t7 | location | sweden |
| t17 | terminator | award | national_film_registry |
| t12 | terminator | cast | michael_biehn |
| t14 | terminator | cast | linda_hamilton |
| t10 | terminator | cast | arnold_schwarzenegger |
| t9 | terminator | director | james_cameron |
| t16 | terminator | duration | 108 |
| t4 | terminator | genre | science_fiction |
| t3 | terminator | genre | action |
| t2 | terminator | instance_of | film |
| t1 | terminator | label | 'The Terminator'@en |
| t7 | terminator | publication_date | ^1985-02-08T00:00:00Z/11 |
| t5 | terminator | publication_date | ^1984-10-26T00:00:00Z/11 |

### Filter certain records and numeric sort a specific column using the system sort program.

```
kgtk filter -i examples/docs/movies_full.tsv \
            -p ';duration;' / \
     sort --columns node2 node1 \
          --numeric-column node2
```

| id | node1 | label | node2 |
| -- | -- | -- | -- |
| t16 | terminator | duration | 108 |
| s18 | terminator2_jd | duration | 137 |

### Filter certain records and reverse numeric sort a specific column using the system sort program.

```
kgtk filter -i examples/docs/movies_full.tsv \
            -p ';duration;' / \
     sort --columns node2 node1 \
          --numeric-column node2 \
	  --reverse-column node2
```

| id | node1 | label | node2 |
| -- | -- | -- | -- |
| s18 | terminator2_jd | duration | 137 |
| t16 | terminator | duration | 108 |

### Bad Example: Filter certain records and reverse numeric sort a specific column without listing the columns.

In the example below, `node2` is allowable as a reverse numerid sort column because
it is part of the default key for this file (`id`, `node1`, `label`, `node2`).
However, the `id` field at the start of the key sequence dominates the sorting
order, since each record in this input file has a unique `id` value.

```
kgtk filter -i examples/docs/movies_full.tsv \
            -p ';duration;' / \
     sort --numeric-column node2 \
	  --reverse-column node2
```

| id | node1 | label | node2 |
| -- | -- | -- | -- |
| s18 | terminator2_jd | duration | 137 |
| t16 | terminator | duration | 108 |

### Filter certain records and sort a single column using the system sort program.

In this example, we will sort on just the `node2` column, which we list explicitly.

```
kgtk filter -i examples/docs/movies_full.tsv \
            -p ';duration;' / \
     sort --columns node2
```

| id | node1 | label | node2 |
| -- | -- | -- | -- |
| t16 | terminator | duration | 108 |
| s18 | terminator2_jd | duration | 137 |

!!! note
    Ties should retain the order of the input file, but the present sample data
    does not demonstrate this.

### Filter certain records and reverse numeric sort a single column using the system sort program.

In this example we will list just a single column to sort on, then use `--numeric` and `--reverse`.

```
kgtk filter -i examples/docs/movies_full.tsv \
            -p ';duration;' / \
     sort --columns node2 \
          --numeric \
	  --reverse
```

| id | node1 | label | node2 |
| -- | -- | -- | -- |
| s18 | terminator2_jd | duration | 137 |
| t16 | terminator | duration | 108 |

!!! note
    Ties should retain the order of the input file, but the present sample data
    does not demonstrate this.

### Filter certain records and reverse numeric sort a single column using the pure Python sort.

In this example we will list just a single column to sort on, then use `--numeric` and `--reverse`.

```
kgtk filter -i examples/docs/movies_full.tsv \
            -p ';duration;' / \
     sort --columns node2 \
          --numeric \
	  --reverse \
	  --pure-python
```

| id | node1 | label | node2 |
| -- | -- | -- | -- |
| s18 | terminator2_jd | duration | 137 |
| t16 | terminator | duration | 108 |

!!! note
    Ties should retain the order of the input file, but the present sample data
    does not demonstrate this.

### Bad Example: Filter certain records and reverse sort a specific column using the pure Python sort.

The pure Python sorting code does not currently support the `--reverse-column` option.

```
kgtk filter -i examples/docs/movies_full.tsv \
            -p ';duration;' / \
     sort --columns node2 \
	  --reverse-column node2 \
	  --pure-python
```

    Error: the pure Python sorter does not currently support reverse column sorts.

### Bad Example: Filter certain records and numeric sort a specific column using the pure Python sort.

The pure Python sorting code does not currently support the `--numeric-column` option.

```
kgtk filter -i examples/docs/movies_full.tsv \
            -p ';duration;' / \
     sort --columns node2 \
          --numeric-column node2 \
	  --pure-python
```

    Error: the pure Python sorter does not currently support numeric column sorts.
