The filter command is used to select edges from an edge file. The initial implementation will use a simple language, but we may in the future extend it to be similar to graphy. The initial implementation also ignores reification.

Filters are specified using patterns of the form
    subject-pattern ; predicate-pattern ; object-pattern
Each of the patterns can consist of a list of symbols separated using commas.

## Usage

```bash
kgtk filter -p PATTERN OPTIONS INPUT
```
- `OPTIONS` allow the user to specify different column headers for node1/subject (argument: `--subj`), label/predicate (argument: `--pred`), node2/object (argument: `--obj`)
- `INPUT` can be a filename or empty if piped from another command

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
