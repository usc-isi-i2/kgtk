## Overview

`kgtk table` converts a KGTK input file to an text table with fixed-width columns on output.

The primary uses for this command are to easily produce documentation files
or to easily produce human-readable output in TABLE-aware environments.

This command defaults to `--mode=NONE` since it doesn't attach special meaning
to particular columns.

This comand is equivalent to `kgtk cat --MODE=NONE --output-format=table`.
However, it is a lot shorter and easier to type.

## Usage

```
usage: kgtk table [-h] [-i INPUT_FILE] [-o OUTPUT_FILE]
                  [-v [optional True|False]]

Convert a KGTK input file to an text table with fixed-width columns on output. 

The initial implementation of this command buffers all output rows im memory, and is not suitable for very large files. 

The output from this command is suitable for use as an MD file. 

Use this command to filter the output of any KGTK command: 

kgtk xxx / table 

Use it to convert a KGTK file to a text table in a file: 

kgtk table -i file.tsv -o file.table

This command defaults to --mode=NONE so it will work with TSV files that do not follow KGTK column naming conventions.

Additional options are shown in expert help.
kgtk --expert table --help

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK file to convert to an HTML table. (May be
                        omitted or '-' for stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The GitHub markdown file to write. (May be omitted or
                        '-' for stdout.)

  -v [optional True|False], --verbose [optional True|False]
                        Print additional progress messages (default=False).
```

## Examples

### Convert a KGTK Table to an TABLETable as a Filter

Use this command to filter the standard output of any KGTK command to an text table:

```bash
kgtk cat -i examples/docs/sample-example1.tsv / table
```

~~~
| node1       | label        | node2       | id |
| ----------- | ------------ | ----------- | -- |
| red         | property     | True        |    |
| red         | isa          | rgbcolor    |    |
| red         | maxoccurs    | 1           |    |
| green       | property     | True        |    |
| green       | isa          | rgbcolor    |    |
| green       | maxoccurs    | 1           |    |
| blue        | property     | True        |    |
| blue        | isa          | rgbcolor    |    |
| blue        | maxoccurs    | 1           |    |
| rgbcolor    | datatype     | True        |    |
| rgbcolor    | node1_type   | symbol      |    |
| rgbcolor    | node2_type   | number      |    |
| rgbcolor    | minval       | 0.0         |    |
| rgbcolor    | maxval       | 1.0         |    |
| rgbcolor    | requires     | red         |    |
| rgbcolor    | requires     | green       |    |
| rgbcolor    | requires     | blue        |    |
| rgbcolor    | isa          | colorclass  |    |
| rgbcolor    | prohibits    | colorname   |    |
| colorname   | property     | True        |    |
| colorname   | isa          | colorclass  |    |
| colorname   | node1_type   | symbol      |    |
| colorname   | node2_type   | symbol      |    |
| colorname   | node2_values | red         |    |
| colorname   | node2_values | green       |    |
| colorname   | node2_values | blue        |    |
| colorname   | node2_values | yellow      |    |
| colorclass  | mustoccur    | True        |    |
| cube        | property     | True        |    |
| cube        | isa          | boxshape    |    |
| cone        | property     | True        |    |
| cone        | isa          | pointyshape |    |
| cone        | isa          | roundshape  |    |
| sphere      | property     | True        |    |
| sphere      | isa          | roundshape  |    |
| pyramid     | property     | True        |    |
| pyramid     | isa          | pointyshape |    |
| cylinder    | property     | True        |    |
| cylinder    | isa          | roundshape  |    |
| boxshape    | datatype     | True        |    |
| boxshape    | isa          | shape       |    |
| pointyshape | datatype     | True        |    |
| pointyshape | isa          | shape       |    |
| roundshape  | datatype     | True        |    |
| roundshape  | isa          | shape       |    |
| shape       | datatype     | True        |    |
| shape       | mustoccur    | True        |    |
~~~

### Convert a KGTK file to an TABLE Table in a File

Use this command to convert a KGTK file to an text table in a file:

```bash
kgtk table -i examples/docs/sample-example1.tsv -o sample-example1.table
```
