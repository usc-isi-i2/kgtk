## Overview

`kgtk normalize` removes additional columns from a KGTK edge file.
It implements two column removal patterns:

  * it reverses `kgtk lift`
  * it converts additional columns to secondary edges

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


kgtk lift --input-file examples/docs/lift-file4.tsv -o examples/docs/normalize-file1.tsv

 kgtk normalize -i examples/docs/normalize-file1.tsv
--normalize was requested but the ID column was not found.
944% kgtk normalize -i examples/docs/normalize-file1.tsv --normalize False
node1   label   node2
Q1      P1      Q5
Q1      label   "Elmo"
P1      label   "instance of"
Q5      label   "homo sapiens"
Q5      label   "human"
Q1      P2      Q6
P2      label   "amigo"
P2      label   "friend"
Q6      label   "Fred"
Q6      P1      Q5
945% kgtk normalize -i examples/docs/normalize-file1.tsv --normalize False --new-edges new.tsv
node1   label   node2
Q1      P1      Q5
Q1      P2      Q6
Q6      P1      Q5
946% cat new.tsv
node1   label   node2
Q1      label   "Elmo"
P1      label   "instance of"
Q5      label   "homo sapiens"
Q5      label   "human"
P2      label   "amigo"
P2      label   "friend"
Q6      label   "Fred"
