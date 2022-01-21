## Overview

`kgtk sample` samples a KGTK file, dividing it into an output file and an optional reject file.

A probability option, `--probability frac`, determines the probability that
an input record is passed to the standard output file. The probability ranges
from 0.0 to 1.0, with 1 being the default.  The sampling probaility is applied
to each record (edge or node) in the input file independently.  The number of
records in the output file might not be exactly the same as the fraction times
the number of records in the input file.

Alternatively, `--input-count N` and `--desired-count n` may be provided.
The sampling probability will be computed. The number of output records may not
exactly match the desired countm unless `--exact` is specified.

This command defaults to `--mode=NONE` since it doesn't attach special meaning
to particular columns.

## Usage

```
usage: kgtk sample [-h] [-i INPUT_FILE] [-o OUTPUT_FILE]
                   [--reject-file REJECT_FILE] [--probability PROBABILITY]
                   [--seed SEED] [--input-count INPUT_COUNT]
                   [--desired-count DESIRED_COUNT] [--exact [True|False]]
                   [-v [optional True|False]]

This utility randomly samples a KGTK file, dividing it into an optput file and an optional reject file. The probability of an input record being passed to the output file is controlled by `--probability n`, where `n` ranges from 0 to 1. 

This command defaults to --mode=NONE so it will work with TSV files that do not follow KGTK column naming conventions.

Additional options are shown in expert help.
kgtk --expert sample --help

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK input file. (May be omitted or '-' for
                        stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for
                        stdout.)
  --reject-file REJECT_FILE
                        The KGTK reject file for records that fail the filter.
                        (Optional, use '-' for stdout.)
  --probability PROBABILITY
                        The probability of passing an input record to the
                        output file (default=1).
  --seed SEED           The optional random number generator seed
                        (default=None).
  --input-count INPUT_COUNT
                        The optional number of input records (default=None).
  --desired-count DESIRED_COUNT
                        The optional desired of output records (default=None).
  --exact [True|False]  Ensure that exactly the desired sample size is
                        extracted when --input-count and --desired-count are
                        supplied. (default=False).

  -v [optional True|False], --verbose [optional True|False]
                        Print additional progress messages (default=False).
```

## Examples

### Sample 1 Record out of 10

```bash
kgtk sample -i examples/docs/sample-example1.tsv \
            --probability .1
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| blue | maxoccurs | 1 |  |
| rgbcolor | datatype | True |  |

### Sampling with a Fixed Seed

You can specify an integer seed to the random number generator to provide
repeatable sampling.

```bash
kgtk sample -i examples/docs/sample-example1.tsv \
            --probability .1 --seed 123
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| red | property | True |  |
| red | isa | rgbcolor |  |
| green | maxoccurs | 1 |  |
| rgbcolor | maxval | 1.0 |  |
| rgbcolor | requires | green |  |
| rgbcolor | isa | colorclass |  |
| colorname | node1_type | symbol |  |
| colorname | node2_values | green |  |

### Sampling an Approximate Number of Records

```bash
kgtk sample -i examples/docs/sample-example1.tsv \
            --input-count 47 --desired-count 5 \
	    --seed 123
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| red | property | True |  |
| red | isa | rgbcolor |  |
| green | maxoccurs | 1 |  |
| rgbcolor | maxval | 1.0 |  |
| rgbcolor | requires | green |  |
| rgbcolor | isa | colorclass |  |
| colorname | node1_type | symbol |  |
| colorname | node2_values | green |  |

### Sampling an ExactNumber of Records

```bash
kgtk sample -i examples/docs/sample-example1.tsv \
            --input-count 47 --desired-count 5 --exact \
	    --seed 123
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| green | property | True |  |
| green | maxoccurs | 1 |  |
| blue | property | True |  |
| rgbcolor | isa | colorclass |  |
| colorname | node2_values | yellow |  |
