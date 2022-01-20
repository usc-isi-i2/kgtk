## Overview

`kgtk sample` samples a KGTK file, dividing it into an output file and an optional reject file.

A probability option, `--probability frac`, determines the probability that
an input record is passed to the standard output file. The probability ranges
from 0.0 to 1.0, with 1 being the default.

This command defaults to `--mode=NONE` since it doesn't attach special meaning
to particular columns.

## Usage

```
usage: kgtk head [-h] [-i INPUT_FILE] [-o OUTPUT_FILE] [-n EDGE_LIMIT]
                 [-v [optional True|False]]

This utility is analogous to the POSIX "head" command. 

When "-n N" is positive, it will pass just the first N data edges of a KGTK input file to the KGTK output file. 

When "-n N" is negative, it will pass all except the last N edges of the KGTK input file to the KGTK output file. 

The header record, cotaining the column names, is always passed and is not included in N. 

Multiplier suffixes are not supported. 

Use this command to filter the output of any KGTK command: 

kgtk xxx / head -n 20 

Use it to limit the records in a file: 

kgtk head -i file.tsv -o file.html

This command defaults to --mode=NONE so it will work with TSV files that do not follow KGTK column naming conventions.

Additional options are shown in expert help.
kgtk --expert html --help

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK input file. (May be omitted or '-' for
                        stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for
                        stdout.)
  -n EDGE_LIMIT, --edges EDGE_LIMIT
                        The number of records to pass if positive
                        (default=10).

  -v [optional True|False], --verbose [optional True|False]
                        Print additional progress messages (default=False).
```

## Examples

### Sample 1 Record out of 10

```bash
kgtk sample -i examples/docs/sample-example1.tsv --probability .1
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| red | property | True |  |
| red | isa | rgbcolor |  |
| red | maxoccurs | 1 |  |
| green | property | True |  |
| green | isa | rgbcolor |  |
| green | maxoccurs | 1 |  |
| blue | property | True |  |
| blue | isa | rgbcolor |  |
| blue | maxoccurs | 1 |  |
| rgbcolor | datatype | True |  |

### Sampling with a Fixed Seed

You can specify an integer seed to the random number generator to provide
repeatable sampling.

```bash
kgtk sample -i examples/docs/sample-example1.tsv --probability .1 --seed 123
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| red | property | True |  |
| red | isa | rgbcolor |  |
| red | maxoccurs | 1 |  |
| green | property | True |  |
| green | isa | rgbcolor |  |
| green | maxoccurs | 1 |  |
| blue | property | True |  |
| blue | isa | rgbcolor |  |
| blue | maxoccurs | 1 |  |
| rgbcolor | datatype | True |  |
