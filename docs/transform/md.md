Convert a KGTK input file to a GitHub markdown table on output.

## Usage

```
usage: kgtk md [-h] [-o OUTPUT_FILE_PATH] [-v] [input_file_path]

Convert a KGTK input file to a GitHub markdown table on output. 

Use this command to filter the output of any KGTK command: 

kgtk md 

Use it to convert a KGTK file to a GitHub Markdown tableL 

kgtk md file.tsv 

Additional options are shown in expert help.
kgtk --expert md --help

positional arguments:
  input_file_path       The KGTK file to convert to a GitHub markdown table.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_FILE_PATH, --output-file OUTPUT_FILE_PATH
                        The KGTK file to write (default=-).

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
