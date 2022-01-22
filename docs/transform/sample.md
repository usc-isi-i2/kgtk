## Overview

`kgtk sample` samples a KGTK file, dividing it into an output file and an optional reject file.

A probability option, `--probability frac`, determines the probability that
an input record is passed to the standard output file. The probability ranges
from 0.0 to 1.0, with 1 being the default.  The sampling probaility is applied
to each record (edge or node) in the input file independently.  The number of
records in the output file might not be exactly the same as the fraction times
the number of records in the input file.

The probability value must not be negative, and it must not be greater than 1.

Alternatively, `--input-size N` and `--sample-size n` may be provided.
The sampling probability will be computed as n/N. The number of output records may not
exactly match the desired countm unless `--exact` is specified. `--exact`
consumes more memory on large input files.

The input count, if specified, must be positive.  The desired count, if specified,
must be positive.

Finally, `--sample-size n` may be provided without `--input-size N`.  Exactly
`n` records will be selected, unless the input file has fewer than `n` records.
The selected records will be buffered in memory as the input file is processed,
so a significant amount of memory may be needed if `n` is large.

This command defaults to `--mode=NONE` since it doesn't attach special meaning
to particular columns.

## Usage

```
usage: kgtk sample [-h] [-i INPUT_FILE] [-o OUTPUT_FILE]
                   [--reject-file REJECT_FILE] [--probability PROBABILITY]
                   [--seed SEED] [--input-size INPUT_SIZE]
                   [--sample-size SAMPLE_SIZE] [--exact [True|False]]
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
  --input-size INPUT_SIZE
                        The optional number of input records (default=None).
  --sample-size SAMPLE_SIZE
                        The optional desired number of output records
                        (default=None).
  --exact [True|False]  Ensure that exactly the desired sample size is
                        extracted when --input-size and --sample-size are
                        supplied. (default=False).

  -v [optional True|False], --verbose [optional True|False]
                        Print additional progress messages (default=False).
```

## Examples

All of the examples in this section specify an integer seed to the random
number generator in order to provide repeatable sampling.  For production
use, you may prefer to omit the seed.


### Sampling .1 Probability with a Fixed Seed

Quickly sample one tenth of the input records.

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

!!! note
  Omit `--seed 123` to obtain a nonrepeatable sample.

### Sampling an Approximate Number of Records Unbuffered

Given the number of input records, quickly sample a specified number of output
records.  The resulting sample might not be the exact size requested.

```bash
kgtk sample -i examples/docs/sample-example1.tsv \
            --input-size 47 --sample-size 5 \
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


!!! note
  Omit `--seed 123` to obtain a nonrepeatable sample.

### Sampling an Exact Number of Records Unbuffered

Given the number of input records, sample an exact number of output records.
Additional time and memory is required to plan which records to include in the
output sample.

```bash
kgtk sample -i examples/docs/sample-example1.tsv \
            --input-size 47 --sample-size 5 --exact \
	    --seed 123
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| green | property | True |  |
| green | maxoccurs | 1 |  |
| blue | property | True |  |
| rgbcolor | isa | colorclass |  |
| colorname | node2_values | yellow |  |


!!! note
  Omit `--seed 123` to obtain a nonrepeatable sample.

### Sampling an Exact Number of Records Buffered

Sample a specified number of output records without knowing the number of
input records.  The sampled records are buffered in memory until the input
file has been read; a large amount of memory may be needed when the sample
size is large.

```bash
kgtk sample -i examples/docs/sample-example1.tsv \
            --sample-size 5 \
	    --seed 123
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| blue | maxoccurs | 1 |  |
| roundshape | datatype | True |  |
| green | isa | rgbcolor |  |
| colorname | isa | colorclass |  |
| colorname | node2_values | blue |  |


!!! note
    The `--exact` option is ignored when `--sample-size n` is specified and
    `--input-size N` is not specified.

!!! note
  Omit `--seed 123` to obtain a nonrepeatable sample.
