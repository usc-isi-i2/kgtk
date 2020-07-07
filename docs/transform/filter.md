The filter command is used to select edges from an edge file. The initial implementation will use a simple language, but we may in the future extend it to be similar to graphy. The initial implementation also ignores reification.

Filters are specified using patterns of the form
    subject-pattern ; predicate-pattern ; object-pattern
Each of the patterns can consist of a list of symbols separated using commas.

## Usage

```
usage: kgtk filter [-h] [-i INPUT_FILE] [-o OUTPUT_FILE] [--reject-file REJECT_FILE] -p
                   PATTERN [--subj SUBJ_COL] [--pred PRED_COL] [--obj OBJ_COL]
                   [--or [True|False]] [--invert [True|False]] [-v]
                   [INPUT_FILE]

Filter KGTK file based on values in the node1 (subject), label (predicate), and node2 (object) fields.

positional arguments:
  INPUT_FILE            The KGTK input file. (May be omitted or '-' for stdin.) (Deprecated,
                        use -i INPUT_FILE)

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK input file. (May be omitted or '-' for stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file for records that pass the filter. (May be
                        omitted or '-' for stdout.)
  --reject-file REJECT_FILE
                        The KGTK reject file for records that fail the filter. (Optional,
                        use '-' for stdout.)
  -p PATTERN, --pattern PATTERN
                        Pattern to filter on, for instance, " ; P154 ; "
  --subj SUBJ_COL       Subject column, default is node1
  --pred PRED_COL       Predicate column, default is label
  --obj OBJ_COL         Object column, default is node2
  --or [True|False]     'Or' the clauses of the pattern. (default=False).
  --invert [True|False]
                        Invert the result of applying the pattern. (default=False).

  -v, --verbose         Print additional progress messages (default=False).
```

## Examples

Select all edges that have property P154. The property is called ‘prop’ in this file

```bash
kgtk filter -p “ ; P154 ; “ --pred ‘prop’ INPUT
```

Select all edges that have properties P154 or P983

```bash
kgtk filter -p “ ; P154, P983 ; “ INPUT
```

Select all edges that have properties P154 or P983 and object Q12

```bash
kgtk filter -p “ ; P154, P983 ; Q12 “ INPUT
```

Select all edges that have subject Q31 or Q45
```bash
kgtk filter -p “ Q32, Q45 ; ; “ INPUT
```
