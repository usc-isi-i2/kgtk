## Overview

`kgtk lexicalize` builds English sentences from KGTK edge files.

The primary purpose of this command is to ocnstruct inputs for
text-based distance vector analysis.  However, it may also
prove useful for explaining the contents of local subsets of
Knowledge Graphs.

## Usage

```
usage: kgtk lexicalize [-h] [-i INPUT_FILE]
                       [--entity-label-file ENTITY_LABEL_FILE]
                       [-o OUTPUT_FILE]
                       [--label-properties [LABEL_PROPERTIES [LABEL_PROPERTIES ...]]]
                       [--description-properties [DESCRIPTION_PROPERTIES [DESCRIPTION_PROPERTIES ...]]]
                       [--isa-properties [ISA_PROPERTIES [ISA_PROPERTIES ...]]]
                       [--has-properties [HAS_PROPERTIES [HAS_PROPERTIES ...]]]
                       [--property-values [PROPERTY_VALUES [PROPERTY_VALUES ...]]]
                       [--sentence-label SENTENCE_LABEL]
                       [--explain [True|False]] [--presorted [True|False]]
                       [--add-entity-labels-from-input [True|False]]
                       [-v [optional True|False]]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK input file. (May be omitted or '-' for
                        stdin.)
  --entity-label-file ENTITY_LABEL_FILE
                        The entity label file(s) (Optional, use '-' for
                        stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for
                        stdout.)
  --label-properties [LABEL_PROPERTIES [LABEL_PROPERTIES ...]]
                        The label properties. (default=['label'])
  --description-properties [DESCRIPTION_PROPERTIES [DESCRIPTION_PROPERTIES ...]]
                        The description properties. (default=['description'])
  --isa-properties [ISA_PROPERTIES [ISA_PROPERTIES ...]]
                        The isa properties. (default=['P21', 'P31', 'P39',
                        'P106', 'P279'])
  --has-properties [HAS_PROPERTIES [HAS_PROPERTIES ...]]
                        The has properties. (default=[])
  --property-values [PROPERTY_VALUES [PROPERTY_VALUES ...]]
                        The property values. (default=['P17'])
  --sentence-label SENTENCE_LABEL
                        The relationship to write in the output file.
                        (default=sentence)
  --explain [True|False]
                        When true, include an explanation column that tells
                        how the sentence was constructed. (default=False).
  --presorted [True|False]
                        When true, the input file is presorted on node1.
                        (default=False).
  --add-entity-labels-from-input [True|False]
                        When true, extract entity labels from the unsorted
                        input file. (default=False).

  -v [optional True|False], --verbose [optional True|False]
                        Print additional progress messages (default=False).
```

## Examples

