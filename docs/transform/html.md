## Overview

`kgtk html` converts a KGTK input file to an HTML table on output.

The primary uses for this command are to easily produce documentation files
or to easily produce human-readable output in HTML-aware environments.

This comand is equivalent to `kgtk cat --MODE=NONE --output-format=html`.
However, it is a lot shorter and easier to type.

The HTML table is generated as a self-contained HTML document with minimal
formatting.

## Usage

```
usage: kgtk html [-h] [-i INPUT_FILE] [-o OUTPUT_FILE]
               [-v [optional True|False]]

Convert a KGTK input file to an HTML table on output. 

Use this command to filter the output of any KGTK command: 

kgtk xxx / html

Use it to convert a KGTK file to an HTML table in a file: 

kgtk html -i file.tsv -o file.html

Additional options are shown in expert help.
kgtk --expert html --help

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK file to convert to a GitHub markdown table.
                        (May be omitted or '-' for stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The GitHub markdown file to write. (May be omitted or
                        '-' for stdout.)

  -v [optional True|False], --verbose [optional True|False]
                        Print additional progress messages (default=False).
```

## Examples

### Convert a KGTK Table to an HTMLTable as a Filter

Use this command to filter the standard output of any KGTK command to an HTML table:

```bash
kgtk xxxxx / html
```

### Convert a KGTK file to an HTML Table in a File

Use this command to convert a KGTK file to an HTML table in a file:

```bash
kgtk html -i xxx.kgtk -o xxx.html
```
