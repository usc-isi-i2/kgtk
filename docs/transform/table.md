## Overview

`kgtk table` converts a KGTK input file to an text table with fixed-width columns on output.

The primary uses for this command are to easily produce documentation files
or to easily produce human-readable output in TABLE-aware environments.

This comand is equivalent to `kgtk cat --MODE=NONE --output-format=table`.
However, it is a lot shorter and easier to type.

## Usage

```
usage: kgtk table [-h] [-i INPUT_FILE] [-o OUTPUT_FILE]
               [-v [optional True|False]]

Convert a KGTK input file to an text table on output. 

Use this command to filter the output of any KGTK command: 

kgtk xxx / table

Use it to convert a KGTK file to an text table in a file: 

kgtk table -i file.tsv -o file.table

Additional options are shown in expert help.
kgtk --expert table --help

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK file to convert to a GitHub markdown table.
                        (May be omitted or '-' for stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The text table file to write. (May be omitted or
                        '-' for stdout.)

  -v [optional True|False], --verbose [optional True|False]
                        Print additional progress messages (default=False).
```

## Examples

### Convert a KGTK Table to an TABLETable as a Filter

Use this command to filter the standard output of any KGTK command to an text table:

```bash
kgtk xxxxx / table
```

### Convert a KGTK file to an TABLE Table in a File

Use this command to convert a KGTK file to an text table in a file:

```bash
kgtk table -i xxx.kgtk -o xxx.table
```
