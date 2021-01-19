`kgtk filter` selects edges from an edge file. The initial implementation uses
a simple pattern language as a filter, but we may in the future extend it to be
similar to graphy. The initial implementation also ignores reification.

`kgtk filter` reads a single input file. It will write one or more output files and/or a reject file.
When there are multiple output files, each output file must have its own filter.
Output files and filters are paired by order.  We recommend listing each filter
and output file as a pair on the command line, as shown in one of the examples, below.
Input records that do not match any filter may be written to a reject file
(`--reject-file REJECT_FILE).

When there are multiple output files, `--first-match-only` determines whether
input records are copied to the first matching output file (when `True`) or to
all matching output files (when `False`, the default).  When `True`, it can also trigger
the use of an optimized code path, which may produce substantial savings when the
total number of alternatives is large.

Filters are specified using patterns of the form

> subject-pattern ; predicate-pattern ; object-pattern

Pattern | Description
------- | -----------
subject-pattern | This pattern applies to the `node1` column (or its alias), unless a different column is selected with the `--subj SUBJ_COL` option.
predicate-pattern | This pattern applies to the `label` column (or its alias), unless a different column is selected with the `--pred PRED_COL` option.
object-pattern | This pattern applies to the `node2` column (or its alias), unless a different column is selected with the `--obj OBJ_COL` option.

Each of the patterns in a filter can consist of a list of symbols separated using commas,
or a regular expression (when `--regex` is specified).

A complete filter requires two semicolons (`;;`) with one or more nonempty patterns.  By default,
all nonempty patterns in a filter must match an input record for the input record to match the
filter; however, the `--or` option may be specified to allow an input record to match when any
nonempty pattern matches.  The `--invert` option may be used to invert the
sense of the filter, causing matching input records to be written to the
reject file, and non-matching records to be written to the output file.

When using regular expressions as patterns, `--match-type MATCH_TYPE` determines the type of
regular expression match that takes place.

Match Type | Description
---------- | -----------
fullmatch  | The full field must match the regular expression.  It is not necessary to start the regular expressin with `^` nor end it with `$`.
match      | The regular expression must match the beginning of the field.  It is not necessary for it to match the entire field.  It is not necessary to start the regular expressin with `^`.
search     | The regular expression must match somewhere in the field.

> NOTE: At the present time, semicolon (`;`) is used to separate the patterns of a filter and cannot appear within a pattern.

> NOTE: At the present time, comma (`,`) is used to separate alternatives in a non-regex pattern and cannot appear within a non-regex pattern.

> NOTE: At the present time, the `--first-match-only`, `--invert`, `--match-type`, `--obj`, `--or`, `--pred`, `--regex`, and `--subj`
> options apply to all filters and patterns in the `kgtk filter` invocation.
> In particular, there is no support for mixing non-regex patterns with regex patterns, other than converting the non-regex pattern to a regex pattern.

## Usage

```
usage: kgtk filter [-h] [-i INPUT_FILE] [-o OUTPUT_FILE [OUTPUT_FILE ...]] [--reject-file REJECT_FILE] -p
                   PATTERNS [PATTERNS ...] [--subj SUBJ_COL] [--pred PRED_COL] [--obj OBJ_COL]
                   [--or [True|False]] [--invert [True|False]] [--regex [True|False]]
                   [--match-type {fullmatch,match,search}] [--first-match-only [True|False]]
                   [--show-version [True/False]] [-v [optional True|False]]

Filter KGTK file based on values in the node1 (subject), label (predicate), and node2 (object) fields.  Optionally filter based on regular expressions.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK input file. (May be omitted or '-' for stdin.)
  -o OUTPUT_FILE [OUTPUT_FILE ...], --output-file OUTPUT_FILE [OUTPUT_FILE ...]
                        The KGTK output file for records that pass the filter. Multiple output file may be
                        specified, each with their own pattern. (May be omitted or '-' for stdout.)
  --reject-file REJECT_FILE
                        The KGTK reject file for records that fail the filter. (Optional, use '-' for stdout.)
  -p PATTERNS [PATTERNS ...], --pattern PATTERNS [PATTERNS ...]
                        Pattern to filter on, for instance, " ; P154 ; ". Multiple patterns may be specified
                        when there are mutiple output files.
  --subj SUBJ_COL       Subject column, default is node1
  --pred PRED_COL       Predicate column, default is label
  --obj OBJ_COL         Object column, default is node2
  --or [True|False]     'Or' the clauses of the pattern. (default=False).
  --invert [True|False]
                        Invert the result of applying the pattern. (default=False).
  --regex [True|False]  When True, treat the filter clauses as regular expressions. (default=False).
  --match-type {fullmatch,match,search}
                        Which type of regular expression match: fullmatch, match, search. (default=match).
  --first-match-only [True|False]
                        If true, write only to the file with the first matching pattern. If false, write to all
                        files with matching patterns. (default=False).
  --show-version [True/False]
                        Print the version of this program. (default=False).

  -v [optional True|False], --verbose [optional True|False]
                        Print additional progress messages (default=False).
```

## Examples

Let us assume we have a KGTK file with movie data, such as the following (download the sample file [here](../../examples/docs/movies_reduced.tsv)):

| id  | node1          |          label   |      node2                       |
| --- | -------------- | ---------------- | -------------------------------- |
| t1  | terminator     |      label       |      "The Terminator"@en         |
| t2  | terminator     | instance_of      |  film                            |
| t3  | terminator     | genre            | action                           |
| t4  | terminator     | genre            | science_fiction                  |
| t5  | terminator     | publication_date | ^1984-10-26T00:00:00Z/11         |
| t6  | t5             | location         | united_states                    |
| t7  | terminator     | publication_date | ^1985-02-08T00:00:00Z/11         |
| t8  | t7             | location         | sweden                           |
| t9  | terminator     | director         | james_cameron                    |
| t10 | terminator     | cast             | arnold_schwarzenegger            |
| t11 | t10            | role             | terminator_machine                       |
| t12 | terminator     | cast             | michael_biehn                    |
| t13 | t12            | role             | kyle_reese                       |
| t14 | terminator     | cast             | linda_hamilton                   |
| t15 | t14            | role             | sarah_connor                     |
| t16 | terminator     | duration         | 108minute                        |
| t17 | terminator     | award            | national_film_registry           |
| t18 | t17            | point_in_time    | ^2008-01-01T00:00:00Z/9          |


Now let's perform several filter operations. For example, selecting all edges that have property `genre` (in the `label` column or its alias):

```bash
kgtk filter -p " ; genre ; " -i INPUT
```

Note that `INPUT` refers to the input path of your .tsv file.

Result:

| id | node1      |     label | node2           |
| -- | ---------- | --------- | --------------- |
| t3 | terminator | genre     | action          |
| t4 | terminator | genre     | science_fiction |


By default, KGTK will assume there is a `label` column. However, you can specify any other column to filter. For example, if we had a column called `prop`:

```bash
kgtk filter -p " ;genre ; " --pred prop -i INPUT
```

Select all edges that have properties `genre` or `cast`:

```bash
kgtk filter -p " ; genre, cast ; " -i INPUT
```

Result:

| id  | node1      |      label | node2                 |
| --- | ---------- | ---------- | --------------------- |
| t3  | terminator |  genre     | action                |
| t4  | terminator |  genre     | science_fiction       |
| t10 | terminator |  cast      | arnold_schwarzenegger |
| t12 | terminator |  cast      | michael_biehn         |
| t14 | terminator |  cast      | linda_hamilton        |


Select all edges that have `arnold_schwarzenegger` as object:

```bash
kgtk filter -p " ; ; arnold_schwarzenegger" -i INPUT
```

Result:

| id  | node1      |      label | node2                 |
| --- | ---------- | ---------- | --------------------- |
| t10 | terminator |  cast      | arnold_schwarzenegger |


Select all edges that have properties `role` or `cast` and object `terminator`:

```bash
kgtk filter -p " ; role, cast ; terminator " --pred prop -i INPUT
```

Result:

| id  | node1 | label     | node2              |
| --- | ----- | --------- | ------------------ |
| t11 | t10   |  role     | terminator_machine |


Select all edges that have subject `terminator`:

```
kgtk filter -p " terminator; ; " --pred prop -i INPUT
```
Result:

| id  | node1      | label            | node2                    |
| --- | ---------- | ---------------- | ------------------------ |
| t1  | terminator | label            | "The Terminator"@en      |
| t2  | terminator | instance_of      | film                     |
| t3  | terminator | genre            | action                   |
| t4  | terminator | genre            | science_fiction          |
| t5  | terminator | publication_date | ^1984-10-26T00:00:00Z/11 |
| t7  | terminator | publication_date | ^1985-02-08T00:00:00Z/11 |
| t9  | terminator | director         | james_cameron            |
| t10 | terminator | cast             | arnold_schwarzenegger    |
| t12 | terminator | cast             | michael_biehn            |
| t14 | terminator | cast             | linda_hamilton           |
| t16 | terminator | duration         | 108minute                |
| t17 | terminator | award            | national_film_registry   |

Send records with property `cast` to one file, records with property `genre` to another file, and the remaining records to a third file:

```bash
kgtk filter \
     -p "; cast ;" -o cast.tsv \
     -p "; genre ;" -o role.tsv \
     --reject-file others.tsv -i INPUT
```

Send records with property `cast` to one file, records with property `genre` to another file, and the remaining records to a third file.
Specify `--first-match-only`.  It will not change the results, but may lead to improved performance due to internal optimizations.

```bash
kgtk filter --first-match-only \
     -p "; cast ;" -o cast.tsv \
     -p "; genre ;" -o genre.tsv \
     --reject-file others.tsv -i INPUT
```

Select all records with a subject value that starts with the letters `t1` (with
unnecessary spaces trimmed out of the filter):

```
kgtk filter -p "t1;;" --regex --match-type match -i INPUT
```
Result:

| id  | node1 | label         | node2                   |
| --- | ----- | ------------- | ----------------------- |
| t11 | t10   | role          | terminator              |
| t13 | t12   | role          | kyle_reese              |
| t15 | t14   | role          | sarah_connor            |
| t18 | t17   | point_in_time | ^2008-01-01T00:00:00Z/9 |


Select all records with an object value that starts with a number:

```
kgtk filter -p ';;[0-9].+' --regex --match-type fullmatch -i INPUT
```

Result:

| id  | node1      | label    | node2     |
| --- | ---------- | -------- | --------- |
| t16 | terminator | duration | 108minute |


