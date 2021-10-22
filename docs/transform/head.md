## Overview

`kgtk head` is analogous to the POSIX 'head' command.  It takes optional input
and output files, and a primary option, `-n N`.
                                                                                                                                                                     
When `-n N` is positive, it will pass just the first N data edges of a KGTK
input file to the KGTK output file.
                                                                                                                                                                     
When `-n N` is negative, it will pass all except the last N edges of the KGTK
input file to the KGTK output file.
                                                                                                                                                                     
The header record, cotaining the column names, is always passed and is not included in the edge limit, N.

Multiplier suffixes are not supported.

This command defaults to `--mode=NONE` since it doesn't attach special meaning
to particular columns.
                                                                                                                                                                     
Although a positive `-n N` has the same effect as KgtkReader's `record_limit`
option, this code currently implements the limit itself.

## Usage

```
usage: kgtk head [-h] [-i INPUT_FILE] [-o OUTPUT_FILE] [-n EDGE_LIMIT]
                 [--output-format {csv,html,json,json-map,json-map-compact,jsonl,jsonl-map,jsonl-map-compact,kgtk,md,table,tsv,tsv-csvlike,tsv-unquoted,tsv-unquoted-ep}]
                 [-v [optional True|False]]

This utility is analogous to the POSIX "head" command. 

When "-n N" is positive, it will pass just the first N data edges of a KGTK input file to the KGTK output file. 

When "-n N" is negative, it will pass all except the last N edges of the KGTK input file to the KGTK output file. 

The header record, cotaining the column names, is always passed and is not included in N. 

Multiplier suffixes are not supported. 

Use this command to filter the output of any KGTK command: 

kgtk xxx / head -N 20 

Use it to limit the records in a file: 

kgtk head -i file.tsv -o file.html

Additional options are shown in expert help.
kgtk --expert html --help

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK file to convert to an HTML table. (May be
                        omitted or '-' for stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The GitHub markdown file to write. (May be omitted or
                        '-' for stdout.)
  -n EDGE_LIMIT, --edges EDGE_LIMIT
                        The number of records to pass if positive
                        (default=10).
  --output-format {csv,html,json,json-map,json-map-compact,jsonl,jsonl-map,jsonl-map-compact,kgtk,md,table,tsv,tsv-csvlike,tsv-unquoted,tsv-unquoted-ep}
                        The file format (default=kgtk)

  -v [optional True|False], --verbose [optional True|False]
                        Print additional progress messages (default=False).
```

## Examples

### See the First 10 Edges

Using the default value for `-n N`:

```bash
kgtk head -i examples/docs/head-example1.tsv
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

### See the First 15 Edges

```bash
kgtk head -n 15 -i examples/docs/head-example1.tsv
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
| rgbcolor | node1_type | symbol |  |
| rgbcolor | node2_type | number |  |
| rgbcolor | minval | 0.0 |  |
| rgbcolor | maxval | 1.0 |  |
| rgbcolor | requires | red |  |

### See All Except the Last 20 Edges

```bash
kgtk head -n -20 -i examples/docs/head-example1.tsv
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
| rgbcolor | node1_type | symbol |  |
| rgbcolor | node2_type | number |  |
| rgbcolor | minval | 0.0 |  |
| rgbcolor | maxval | 1.0 |  |
| rgbcolor | requires | red |  |
| rgbcolor | requires | green |  |
| rgbcolor | requires | blue |  |
| rgbcolor | isa | colorclass |  |
| rgbcolor | prohibits | colorname |  |
| colorname | property | True |  |
| colorname | isa | colorclass |  |
| colorname | node1_type | symbol |  |
| colorname | node2_type | symbol |  |
| colorname | node2_values | red |  |
| colorname | node2_values | green |  |
| colorname | node2_values | blue |  |
| colorname | node2_values | yellow |  |

### See the Complete File

Using a very large number, we can use `kgtk head` to display
the entire file.

```bash
kgtk head -n 999999999 -i examples/docs/head-example1.tsv
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
| rgbcolor | node1_type | symbol |  |
| rgbcolor | node2_type | number |  |
| rgbcolor | minval | 0.0 |  |
| rgbcolor | maxval | 1.0 |  |
| rgbcolor | requires | red |  |
| rgbcolor | requires | green |  |
| rgbcolor | requires | blue |  |
| rgbcolor | isa | colorclass |  |
| rgbcolor | prohibits | colorname |  |
| colorname | property | True |  |
| colorname | isa | colorclass |  |
| colorname | node1_type | symbol |  |
| colorname | node2_type | symbol |  |
| colorname | node2_values | red |  |
| colorname | node2_values | green |  |
| colorname | node2_values | blue |  |
| colorname | node2_values | yellow |  |
| colorclass | mustoccur | True |  |
| cube | property | True |  |
| cube | isa | boxshape |  |
| cone | property | True |  |
| cone | isa | pointyshape |  |
| cone | isa | roundshape |  |
| sphere | property | True |  |
| sphere | isa | roundshape |  |
| pyramid | property | True |  |
| pyramid | isa | pointyshape |  |
| cylinder | property | True |  |
| cylinder | isa | roundshape |  |
| boxshape | datatype | True |  |
| boxshape | isa | shape |  |
| pointyshape | datatype | True |  |
| pointyshape | isa | shape |  |
| roundshape | datatype | True |  |
| roundshape | isa | shape |  |
| shape | datatype | True |  |
| shape | mustoccur | True |  |

