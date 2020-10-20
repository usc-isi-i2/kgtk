The filter command is used to select edges from an edge file. The initial implementation will use a simple language, but we may in the future extend it to be similar to graphy. The initial implementation also ignores reification.

Filters are specified using patterns of the form
    subject-pattern ; predicate-pattern ; object-pattern
Each of the patterns can consist of a list of symbols separated using commas.

## Usage

```
usage: kgtk filter [-h] [-i INPUT_FILE] [-o OUTPUT_FILE [OUTPUT_FILE ...]] [--reject-file REJECT_FILE] -p PATTERNS [PATTERNS ...] [--subj SUBJ_COL]
                   [--pred PRED_COL] [--obj OBJ_COL] [--or [True|False]] [--invert [True|False]] [--first-match-only [True|False]] [--show-version [True/False]]
                   [-v]

Filter KGTK file based on values in the node1 (subject), label (predicate), and node2 (object) fields.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK input file. (May be omitted or '-' for stdin.)
  -o OUTPUT_FILE [OUTPUT_FILE ...], --output-file OUTPUT_FILE [OUTPUT_FILE ...]
                        The KGTK output file for records that pass the filter. Multiple output file may be specified, each with their own pattern. (May be omitted
                        or '-' for stdout.)
  --reject-file REJECT_FILE
                        The KGTK reject file for records that fail the filter. (Optional, use '-' for stdout.)
  -p PATTERNS [PATTERNS ...], --pattern PATTERNS [PATTERNS ...]
                        Pattern to filter on, for instance, " ; P154 ; ". Multiple patterns may be specified when there are mutiple output files.
  --subj SUBJ_COL       Subject column, default is node1
  --pred PRED_COL       Predicate column, default is label
  --obj OBJ_COL         Object column, default is node2
  --or [True|False]     'Or' the clauses of the pattern. (default=False).
  --invert [True|False]
                        Invert the result of applying the pattern. (default=False).
  --first-match-only [True|False]
                        If true, write only to the file with the first matching pattern. If false, write to all files with matching patterns. (default=False).
  --show-version [True/False]
                        Print the version of this program. (default=False).

```

## Examples

Select all edges that have property P154. The property is called "prop" in this file

```bash
kgtk filter -p " ; P154 ; " --pred prop -i INPUT
```

Select all edges that have properties P154 or P983

```bash
kgtk filter -p " ; P154, P983 ; " --pred prop -i INPUT
```

Select all edges that have properties P154 or P983 and object Q12

```bash
kgtk filter -p " ; P154, P983 ; Q12 " --pred prop -i INPUT
```

Select all edges that have subject Q31 or Q45
```bash
kgtk filter -p " Q32, Q45 ; ; " --pred prop -i INPUT
```

Send P154 records to one file, P983 records to another file, and the remainder to a third file.
```bash
kgtk filter -p "; P154 ;" -o P154.tsv -p "; P983 ;" -o P983.tsv --reject-file others.tsv
```
