Convert a KGTK input file to a GitHub markdown table on output.

## Usage

```
usage: kgtk md [-h] [-i INPUT_FILE] [-o OUTPUT_FILE] [-v]

Convert a KGTK input file to a GitHub markdown table on output. 

Use this command to filter the output of any KGTK command: 

kgtk md 

Use it to convert a KGTK file to a GitHub Markdown table in a file: 

kgtk md file.tsv 

Additional options are shown in expert help.
kgtk --expert md --help

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK file to convert to a GitHub markdown table. (May be omitted
                        or '-' for stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The GitHub markdown file to write. (May be omitted or '-' for
                        stdout.)

  -v, --verbose         Print additional progress messages (default=False).
```

## Examples

Use this command to filter the output of any KGTK command:
```bash
kgtk xxxxx | kgtk md
```

Use it to convert a KGTK file to a GitHub Markdown table in a file:
```bash
kgtk xxxxx | kgtk md -o xxx.md
```
