## Overview

`kgtk filter` selects edges from an edge file. The current implementation uses
a simple pattern language as a filter, and ignores reification.

### Filters and  Patterns

Filters are composed of three patterns separated by semicolons:

`node1-pattern ; label-pattern ; node2-pattern`

| Pattern | Description |
| ------- | ----------- |
| node1-pattern | This pattern applies to the `node1` column (or its alias), unless a different column is selected with the `--node1 SUBJ_COL` option. |
| label-pattern | This pattern applies to the `label` column (or its alias), unless a different column is selected with the `--label PRED_COL` option. |
| node2-pattern | This pattern applies to the `node2` column (or its alias), unless a different column is selected with the `--node2 OBJ_COL` option. |

Each of the patterns in a filter can consist of a list of symbols (words) separated using commas,
or a regular expression (when `--regex` is specified).

A complete filter requires two semicolons (`;;`) with one or more nonempty patterns.  By default,
all nonempty patterns in a filter must match an input edge for the input edge to match the
filter; however, the `--or` option may be specified to allow an input edge to match when any
nonempty pattern matches.  The `--invert` option may be used to invert the
sense of the filter, causing matching input edges to be written to the
reject file, and non-matching edges to be written to the output file.

!!! note
    If semicolon (`;`) is part of what you want to match, you may use
    `--pattern-separator SEPARATOR` to supply a separator other then semicolon.

!!! note
    If comma (`,`) is part of what you want to match, you may use
    `--word-separator SEPARATOR` to supply a separator other then comma.

### Regular Expression Patterns

`--regex` (short for `--regex True` or `--regex=True`) indicates that the patterns in a filter are regular expressions instead of comma-separated lists.
When using regular expressions as patterns, `--match-type MATCH_TYPE` determines the type of
regular expression match that takes place.

| Match Type | Description |
| ---------- | ----------- |
| fullmatch  | The full field must match the regular expression.  <br />It is not necessary to start the regular expression with `^` nor end it with `$`. |
| match      | The regular expression must match the beginning of the field.  It is not necessary for it to match the entire field.  <br />It is not necessary to start the regular expression with `^`. <br />This is the default match type.|
| search     | The regular expression must match somewhere in the field. |

### Multiple Filters

`kgtk filter` reads a single input file. It will write one or more output files and/or a reject file.
When there are multiple output files, each output file must have its own filter.
Output files and filters are paired by order.  We recommend listing each filter
and output file as a pair on the command line, as shown in one of the examples, below.
Input edges that do not match any filter may be written to a reject file
(`--reject-file REJECT_FILE`).

When there are multiple output files, `--first-match-only` determines whether
input edges are copied to the first matching output file (when `True`) or to
all matching output files (when `False`, the default).  When `True`, it can also trigger
the use of an optimized code path, which may produce substantial savings when the
total number of alternatives is large.

### Caveats

!!! note
    At the present time, the `--first-match-only`, `--invert`, `--match-type`, `--node2`, `--or`, `--label`, `--regex`, and `--node1`
    options apply to all filters and patterns in the `kgtk filter` invocation. In particular, there is no support for mixing
    non-regex patterns with regex patterns, other than converting the non-regex pattern to a regex pattern by hand.

## Usage

```
usage: kgtk filter [-h] [-i INPUT_FILE] [-o OUTPUT_FILE [OUTPUT_FILE ...]]
                   [--reject-file REJECT_FILE] -p PATTERNS [PATTERNS ...]
                   [--node1 SUBJ_COL] [--label PRED_COL] [--node2 OBJ_COL]
                   [--or [True|False]] [--invert [True|False]]
                   [--regex [True|False]]
                   [--match-type {fullmatch,match,search}]
                   [--first-match-only [True|False]]
                   [--pattern-separator PATTERN_SEPARATOR]
                   [--word-separator WORD_SEPARATOR]
                   [--show-version [True/False]] [-v [optional True|False]]

Filter KGTK file based on values in the node1 (subject), label (predicate), and node2 (object) fields.  Optionally filter based on regular expressions.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK input file. (May be omitted or '-' for
                        stdin.)
  -o OUTPUT_FILE [OUTPUT_FILE ...], --output-file OUTPUT_FILE [OUTPUT_FILE ...]
                        The KGTK output file for records that pass the filter.
                        Multiple output file may be specified, each with their
                        own pattern. (May be omitted or '-' for stdout.)
  --reject-file REJECT_FILE
                        The KGTK reject file for records that fail the filter.
                        (Optional, use '-' for stdout.)
  -p PATTERNS [PATTERNS ...], --pattern PATTERNS [PATTERNS ...]
                        Pattern to filter on, for instance, " ; P154 ; ".
                        Multiple patterns may be specified when there are
                        mutiple output files.
  --node1 SUBJ_COL, --subj SUBJ_COL
                        The subject column, default is node1 or its alias.
  --label PRED_COL, --pred PRED_COL
                        The predicate column, default is label or its alias.
  --node2 OBJ_COL, --obj OBJ_COL
                        The object column, default is node2 or its alias.
  --or [True|False]     'Or' the clauses of the pattern. (default=False).
  --invert [True|False]
                        Invert the result of applying the pattern.
                        (default=False).
  --regex [True|False]  When True, treat the filter clauses as regular
                        expressions. (default=False).
  --match-type {fullmatch,match,search}
                        Which type of regular expression match: fullmatch,
                        match, search. (default=match).
  --first-match-only [True|False]
                        If true, write only to the file with the first
                        matching pattern. If false, write to all files with
                        matching patterns. (default=False).
  --pattern-separator PATTERN_SEPARATOR
                        The separator between the pattern components.
                        (default=;.
  --word-separator WORD_SEPARATOR
                        The separator between the words in a pattern
                        component. (default=,.
  --show-version [True/False]
                        Print the version of this program. (default=False).

  -v [optional True|False], --verbose [optional True|False]
                        Print additional progress messages (default=False).
```

## Examples

### Sample Data

Let us assume we have a KGTK file with movie data, such as the following
(also available for download [here](https://raw.githubusercontent.com/usc-isi-i2/kgtk/dev/examples/docs/movies_reduced.tsv)):

```bash
kgtk cat -i examples/docs/movies_reduced.tsv
```

| id | node1 | label | node2 |
| -- | -- | -- | -- |
| t1 | terminator | label | 'The Terminator'@en |
| t2 | terminator | instance_of | film |
| t3 | terminator | genre | action |
| t4 | terminator | genre | science_fiction |
| t5 | terminator | publication_date | ^1984-10-26T00:00:00Z/11 |
| t6 | t5 | location | united_states |
| t7 | terminator | publication_date | ^1985-02-08T00:00:00Z/11 |
| t8 | t7 | location | sweden |
| t9 | terminator | director | james_cameron |
| t10 | terminator | cast | arnold_schwarzenegger |
| t11 | t10 | role | terminator |
| t12 | terminator | cast | michael_biehn |
| t13 | t12 | role | kyle_reese |
| t14 | terminator | cast | linda_hamilton |
| t15 | t14 | role | sarah_connor |
| t16 | terminator | duration | 108 |
| t17 | terminator | award | national_film_registry |
| t18 | t17 | point_in_time | ^2008-01-01T00:00:00Z/9 |

Let us use this file (or a close derivative) in the following examples.

### Selecting Edges with a Matching `node1` (Subject)

Select all edges that have the subject `terminator` (in the `node1` column or its alias):

```
kgtk filter -i examples/docs/movies_reduced.tsv \
            -p " terminator; ; "
```
Result:

| id | node1 | label | node2 |
| -- | -- | -- | -- |
| t1 | terminator | label | 'The Terminator'@en |
| t2 | terminator | instance_of | film |
| t3 | terminator | genre | action |
| t4 | terminator | genre | science_fiction |
| t5 | terminator | publication_date | ^1984-10-26T00:00:00Z/11 |
| t7 | terminator | publication_date | ^1985-02-08T00:00:00Z/11 |
| t9 | terminator | director | james_cameron |
| t10 | terminator | cast | arnold_schwarzenegger |
| t12 | terminator | cast | michael_biehn |
| t14 | terminator | cast | linda_hamilton |
| t16 | terminator | duration | 108 |
| t17 | terminator | award | national_film_registry |

### Selecting Edges without a Matching `node1` (Subject)

Select all edges that do not have the subject `terminator` (in the `node1` column or its alias):

```
kgtk filter -i examples/docs/movies_reduced.tsv \
            --invert -p " terminator; ; "
```
Result:

| id | node1 | label | node2 |
| -- | -- | -- | -- |
| t6 | t5 | location | united_states |
| t8 | t7 | location | sweden |
| t11 | t10 | role | terminator |
| t13 | t12 | role | kyle_reese |
| t15 | t14 | role | sarah_connor |
| t18 | t17 | point_in_time | ^2008-01-01T00:00:00Z/9 |

### Selecting Edges with Matching `label` (Predicate)

Select all edges that have property `genre` (in the `label` column or its alias):

```bash
kgtk filter -i examples/docs/movies_reduced.tsv \
            -p " ; genre ; "
```

!!! info
    `examples/docs/movies_reduced.tsv` should be replaced by the path to your .tsv file.

Result:

| id | node1 | label | node2 |
| -- | -- | -- | -- |
| t3 | terminator | genre | action |
| t4 | terminator | genre | science_fiction |

### Selecting Edges by Matching an Alternate Predicate Column

By default, KGTK will assume there is a `label` column for the predicate pattern
However, you can specify any other column to filter.
For example, if we had a column called `genre` in the input file:

```bash
kgtk filter -i examples/docs/movies_reduced_with_genre_column.tsv \
            --label genre  -p " ;action ; "
```

Results:

| id | node1 | label | node2 | genre |
| -- | -- | -- | -- | -- |
| t1 | terminator | label | 'The Terminator'@en | action |

### Selecting Edges with Multiple Possible Predicate Matches

Select all edges that have properties `genre` or `cast`:

```bash
kgtk filter -i examples/docs/movies_reduced.tsv \
            -p " ; genre, cast ; "
```

Result:

| id | node1 | label | node2 |
| -- | -- | -- | -- |
| t3 | terminator | genre | action |
| t4 | terminator | genre | science_fiction |
| t10 | terminator | cast | arnold_schwarzenegger |
| t12 | terminator | cast | michael_biehn |
| t14 | terminator | cast | linda_hamilton |


### Selecting Edges with Multiple Possible Predicate Matches and Custom Separators

Select all edges that have properties `genre` or `cast`,
using `:` to separate the component patterns in the filter
and using '|' to separate the alternative words:

```bash
kgtk filter -i examples/docs/movies_reduced.tsv \
            --pattern-separator : \
	    --word-separator '|' \
            -p " : genre|cast : "
```

Result:

| id | node1 | label | node2 |
| -- | -- | -- | -- |
| t3 | terminator | genre | action |
| t4 | terminator | genre | science_fiction |
| t10 | terminator | cast | arnold_schwarzenegger |
| t12 | terminator | cast | michael_biehn |
| t14 | terminator | cast | linda_hamilton |


### Selecting Edges with a Matching `node2` (Object)

Select all edges that have `arnold_schwarzenegger` as the object (in the `node2` column or its alias):

```bash
kgtk filter -i examples/docs/movies_reduced.tsv \
            -p " ; ; arnold_schwarzenegger"
```

Result:

| id | node1 | label | node2 |
| -- | -- | -- | -- |
| t10 | terminator | cast | arnold_schwarzenegger |


### Selecting Edges with Both a `label` and `node2` Match

Select all edges that have predicate values `role` or `cast` (in the `label` column or its alias)
and object `terminator` (in the `node2` column or its alias):

```bash
kgtk filter -i examples/docs/movies_reduced.tsv \
            -p " ; role, cast ; terminator "
```

Result:

| id | node1 | label | node2 |
| -- | -- | -- | -- |
| t11 | t10 | role | terminator |


### Selecting Edges with a `label` or `node2` Match

Select all edges that have predicate values `role` or `cast` (in the `label` column or its alias),
or object `sweden` (in the `node2` column or its alias):

```bash
kgtk filter -i examples/docs/movies_reduced.tsv \
            --or -p " ; role, cast ; sweden "
```

Result:

| id | node1 | label | node2 |
| -- | -- | -- | -- |
| t8 | t7 | location | sweden |
| t10 | terminator | cast | arnold_schwarzenegger |
| t11 | t10 | role | terminator |
| t12 | terminator | cast | michael_biehn |
| t13 | t12 | role | kyle_reese |
| t14 | terminator | cast | linda_hamilton |
| t15 | t14 | role | sarah_connor |


### Sending Different Edges to Different Files

Send edges with property `cast` to one file, edges with property `genre` to another file, and the remaining edges to a third file:

```bash
kgtk filter -i examples/docs/movies_reduced.tsv \
            -p "; cast ;" -o cast.tsv \
            -p "; genre ;" -o genre.tsv \
            --reject-file others.tsv
```
(No standard output)

Result:

```bash
kgtk cat -i cast.tsv
```

| id | node1 | label | node2 |
| -- | -- | -- | -- |
| t10 | terminator | cast | arnold_schwarzenegger |
| t12 | terminator | cast | michael_biehn |
| t14 | terminator | cast | linda_hamilton |

```bash
kgtk cat -i genre.tsv
```

| id | node1 | label | node2 |
| -- | -- | -- | -- |
| t3 | terminator | genre | action |
| t4 | terminator | genre | science_fiction |

```bash
kgtk cat -i others.tsv
```

| id | node1 | label | node2 |
| -- | -- | -- | -- |
| t1 | terminator | label | 'The Terminator'@en |
| t2 | terminator | instance_of | film |
| t5 | terminator | publication_date | ^1984-10-26T00:00:00Z/11 |
| t6 | t5 | location | united_states |
| t7 | terminator | publication_date | ^1985-02-08T00:00:00Z/11 |
| t8 | t7 | location | sweden |
| t9 | terminator | director | james_cameron |
| t11 | t10 | role | terminator |
| t13 | t12 | role | kyle_reese |
| t15 | t14 | role | sarah_connor |
| t16 | terminator | duration | 108 |
| t17 | terminator | award | national_film_registry |
| t18 | t17 | point_in_time | ^2008-01-01T00:00:00Z/9 |

### Sending Different Edges to Different Files Without First Match

Send edges with `label`  property `genre` to one file,
edges with `node2` object `action` to another file, and ignore other edges.

```bash
kgtk filter -i examples/docs/movies_reduced.tsv \
            -p "; genre ;" -o genre.tsv \
            -p "; ; action" -o action.tsv \
```
(No standard output)

Result:

```bash
kgtk cat -i genre.tsv
```

| id | node1 | label | node2 |
| -- | -- | -- | -- |
| t3 | terminator | genre | action |
| t4 | terminator | genre | science_fiction |

```bash
kgtk cat -i action.tsv
```

| id | node1 | label | node2 |
| -- | -- | -- | -- |

!!! note
    The edge terminator/genre/action appears in both the genre and action output files.

### Sending Different Edges to Different Files with First Match

Send edges with property `genre` to one file, edges with object `action` to another file, ignoring other edges.
Specify `--first-match-only` to ensure that a given edge will be sent to at most one output file.

```bash
kgtk filter -i examples/docs/movies_reduced.tsv \
            --first-match-only \
            -p "; genre ;" -o genre.tsv \
            -p "; ; action" -o action.tsv
```
(No standard output)

Result:

```bash
kgtk cat -i genre.tsv
```

| id | node1 | label | node2 |
| -- | -- | -- | -- |
| t3 | terminator | genre | action |
| t4 | terminator | genre | science_fiction |

```bash
kgtk cat -i action.tsv
```

| id | node1 | label | node2 |
| -- | -- | -- | -- |



!!! note
    The edge terminator/genre/action appears in only the genre output file.


### Sending Different Edges to Diferent Files with Unselected Edges to Standard Output

Send edges with property `genre` to one file, edges with object `action` to another file, and pass the
remaining edges to standard output.  Specify `--first-match-only` to ensure that a given edge will be sent to at most one output file.

```bash
kgtk filter -i examples/docs/movies_reduced.tsv \
            --first-match-only \
            -p "; genre ;" -o genre.tsv \
            -p "; ; action" -o action.tsv \
            --reject-file -
```


Result:

| id | node1 | label | node2 |
| -- | -- | -- | -- |
| t1 | terminator | label | 'The Terminator'@en |
| t2 | terminator | instance_of | film |
| t5 | terminator | publication_date | ^1984-10-26T00:00:00Z/11 |
| t6 | t5 | location | united_states |
| t7 | terminator | publication_date | ^1985-02-08T00:00:00Z/11 |
| t8 | t7 | location | sweden |
| t9 | terminator | director | james_cameron |
| t10 | terminator | cast | arnold_schwarzenegger |
| t11 | t10 | role | terminator |
| t12 | terminator | cast | michael_biehn |
| t13 | t12 | role | kyle_reese |
| t14 | terminator | cast | linda_hamilton |
| t15 | t14 | role | sarah_connor |
| t16 | terminator | duration | 108 |
| t17 | terminator | award | national_film_registry |
| t18 | t17 | point_in_time | ^2008-01-01T00:00:00Z/9 |

```bash
kgtk cat -i genre.tsv
```

| id | node1 | label | node2 |
| -- | -- | -- | -- |
| t3 | terminator | genre | action |
| t4 | terminator | genre | science_fiction |

```bash
kgtk cat -i action.tsv
```

| id | node1 | label | node2 |
| -- | -- | -- | -- |


### Selecting Edges where the Subject Starts with `t1`

Select all edges with a subject value that starts with the letters `t1` (with
unnecessary spaces trimmed out of the filter):

```
kgtk filter -i examples/docs/movies_reduced.tsv \
            --regex --match-type match \
            -p "t1;;"
```
Result:

| id | node1 | label | node2 |
| -- | -- | -- | -- |
| t11 | t10 | role | terminator |
| t13 | t12 | role | kyle_reese |
| t15 | t14 | role | sarah_connor |
| t18 | t17 | point_in_time | ^2008-01-01T00:00:00Z/9 |


### Selecting Edges where the Object Starts with a Digit

Select all edges with an object value that starts with a Digit:

```
kgtk filter -i examples/docs/movies_reduced.tsv \
            --regex --match-type fullmatch \
            -p ';;[0-9].+'
```

Result:

| id | node1 | label | node2 |
| -- | -- | -- | -- |
| t16 | terminator | duration | 108 |
