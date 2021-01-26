## Overview

`kgtk md` converts a KGTK input file to a GitHub markdown table on output.

The primary use for this command is to easily produce documentation files.
However, there are instances in which the output of this command is more
readable than a KGTK TSV file, so this command can also be used as a debugging
aid.

This comand is equivalent to `kgtk cat --MODE=NONE --output-format=md`.
However, it is a lot shorter and easier to type.

## Usage

```
usage: kgtk md [-h] [-i INPUT_FILE] [-o OUTPUT_FILE]
               [-v [optional True|False]]

Convert a KGTK input file to a GitHub markdown table on output. 

Use this command to filter the output of any KGTK command: 

kgtk xxx / md 

Use it to convert a KGTK file to a GitHub Markdown table in a file: 

kgtk md -i file.tsv -o file.md

Additional options are shown in expert help.
kgtk --expert md --help

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

### Convert a KGTK Table to a Markdown Table as a Filter

Use this command to filter the standard output of any KGTK command to a Github Markdown table:

```bash
kgtk xxxxx / md
```

### Convert a KGTk file to a Markdown File

Use this command to convert a KGTK file to a GitHub Markdown table in a file:

```bash
kgtk md -i xxx.kgtk -o xxx.md
```
