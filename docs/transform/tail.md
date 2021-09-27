## Overview

`kgtk tail` is analogous to the POSIX 'tail' command.  It takes optional input
and output files, and a primary option, `-n N`.
                                                                                                                                                                     
For `-n N`, it will pass just the last N data edges of a KGTK
input file to the KGTK output file.
                                                                                                                                                                     
The POSIX 'tail' command's notion of '-n +N' is not supported.

The POSIX 'tail' command's notion of waiting for changes to the
input file is not supported.
                                                                                                                                                                     
The header record, cotaining the column names, is always passed and is not included in the edge limit, N.

Multiplier suffixes are not supported.

## Usage

```
usage: kgtk tail [-h] [-i INPUT_FILE] [-o OUTPUT_FILE] [-n EDGE_LIMIT]
                 [-v [optional True|False]]

This utility is analogous to the POSIX "head" command. 

For "-n N", pass just the last N data edges of a KGTK input file to the KGTK output file. 

"-n +N" does not have the special meaning it has in the POSIC "tail" command. 

The header record, cotaining the column names, is always passed and is not included in N. 

Multiplier suffixes are not supported. 

Use this command to filter the output of any KGTK command: 

kgtk xxx / tail -n 20 

Use it to limit the records in a file: 

kgtk tail -i file.tsv -o file.html

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
                        The number of records to pass (default=10).

  -v [optional True|False], --verbose [optional True|False]
                        Print additional progress messages (default=False).
```

## Examples

### See the Last 10 Edges

Using the default value for `-n N`:

```bash
kgtk tail -i examples/docs/tail-example1.tsv
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
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

### See the Last 15 Edges

```bash
kgtk tail -n 15 -i examples/docs/tail-example1.tsv
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
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

### See the Complete File

Using a very large number, we can use `kgtk tail` to display
the entire file.  However, this will buffer the entire file
in memory, which may not be feasible for large files.

```bash
kgtk tail -n 999999999 -i examples/docs/tail-example1.tsv
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

