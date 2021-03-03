## Summary

`kgtk validate-properties` validates and filter property patterns in a KGTK file.

## Usage
```
usage: kgtk validate-properties [-h] [-i INPUT_FILE] --pattern-file
                                PATTERN_FILE [-o OUTPUT_FILE]
                                [--reject-file REJECT_FILE]
                                [--presorted [True|False]]
                                [--process-node1-groups [True|False]]
                                [--no-complaints [True|False]]
                                [--complain-immediately [True|False]]
                                [--add-isa-column [True|False]]
                                [--isa-column-name ISA_COLUMN_NAME]
                                [--autovalidate [True|False]]
                                [-v [optional True|False]]

Validate property patterns in a KGTK file. 

Additional options are shown in expert help.
kgtk --expert clean-data --help

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK input file. (May be omitted or '-' for
                        stdin.)
  --pattern-file PATTERN_FILE
                        The property pattern definitions. (Required, use '-'
                        for stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (Optional, use '-' for stdout.)
  --reject-file REJECT_FILE
                        The property pattern reject output. (Optional, use '-'
                        for stdout.)
  --presorted [True|False]
                        Indicate that the input has been presorted (or at
                        least pregrouped) on the node1 column.
                        (default=False).
  --process-node1-groups [True|False]
                        When True, process all records for a node1 value as a
                        group. (default=True).
  --no-complaints [True|False]
                        When true, do not print complaints (when rejects are
                        expected). (default=False).
  --complain-immediately [True|False]
                        When true, print complaints immediately (for
                        debugging). (default=False).
  --add-isa-column [True|False]
                        When true, add an ISA column to the output and reject
                        files. (default=False).
  --isa-column-name ISA_COLUMN_NAME
                        The name for the ISA column. (default isa;node2)
  --autovalidate [True|False]
                        When true, validate node1 and node2 values before
                        testing them. (default=True).

  -v [optional True|False], --verbose [optional True|False]
                        Print additional progress messages (default=False).
```
