## Summary

`kgtk validate-properties` validates and filter property patterns in a KGTK file.

### Problem Statement

The [`kgtk validate`](../validate) command cannot detect problems such as:

 * date ranges at granularities finer than ayear
 * numbers out of range
 * a number where a quantity was expected
 * a symbol where a string was expected
 * the presence of one property requires another property
 * The presense of one property excludes another property

We want to be able to detect violations of various constraint patterns.

An existing system, CHACL, is an RDF-based constraint system.  We'd like
KGTK to have something that is both easier for new users than RDF and more efficient to run.

### Approach

KGTK edges have `node1`, `label`, and `node2` fields as their core.
`id` fields are optional, and additional fields may also appear.

The `node1` field usually represents an object being described by
the edges.  The edges for that object represent properties or attributes
of the object, with the `label` field naming the property and the `node2`
field containing an associated value.  Properties may be qualified, using
the `id` field of an edge as the linkage to qualifier edges.

Generally, patterns of constraints are applied to classes of objects and properties,
rather than specific individual objects or properties.  `kgtk validate-properties` includes
tools for identifying the class heirarchy to which an object or property belongs.

In addition to focusing on constraints applicable to edges grouped around objects,
`kgtk validate-properties` supports the application of constraints to additional columns.

### Pattern Files

`kgtk validate-properties` describes its declarations and constraints using KGTK edges with `id` fields
as needed, but without additional columns.  These edges are typically in a seperate file, called
a `property pattern file` or `pattern file`.

Here is a brief sample of a property pattern file:
| node1 | label | node2 | id |
| ----- | ----- | ----- | -- |
| red | `isa` | rgbcolor |
| green | `isa` | rgbcolor |
| blue | `isa` | rgbcolor |


### Property Classes

The values in the `label` column are property names.  Each property
name is itself a property class.  Each property class may be a member of
one or more parent property classes, as indicated by `isa` and `matches`
declarations.

For example, suppose we have a KGTK file that describes the properties of a
set of blocks.  One property we want to describe is the RCG color.  This
property itself has three components, `red`, `green`, and `blue`, each of
which takes a floating point value that ranges from 0..1 inclusive.

Here are two blocks and their colors:

| node1 | label | node2 | id |
| ----- | ----- | ----- | -- |
| block1 | red | 1.0 | |
| block1 | green | 0.0 | |
| block1 | blue  | 0.0 | |
| block2 | red | 0.0 | |
| block2 | green | 1.0 | |
| block2 | blue  | 0.0 | |

Here are the constraints that name `red`, `green`, and `blue` as RGB color
components, and which constrain the values of each component to be numbers in
the range 0..1 inclusive.

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
| colorclass | mustoccur | True |  |

 * `property` declares that the property class is a property
   that may appear in the `label` column of a data file.
   Although these eentries are mainly documentation, they also
   prevent the specied property from being considered `unknown`.
 * `isa` says that the `node1` class is a subclass of the `node2` class.
 * `maxoccurs` indicates that properties of the specified class may
   occur a maximum number of times per `node1` group.
 * `datatype` declares that the property class is a superclass
   that may not appear in the `label` column of a data file.
   At present, this constraint is not enforced.
 * `node`_type` says that data records with `label` values that
   belong to this class must have `node1` values with a KGTK datatype
   in the list in the `node2` column of the pattern edge, e.g.
     * In this specific case, the `node1` value of an RGB color
       component must be a KGTK `symbol`.
 * `node2_type` says that data records with `label` values that
   belong to this class must have `node2` values with a KGTK datatype
   in the list in the `node2` column of the pattern edge, e.g.
     * In this specific case, the `node2` value of an RGB color
       component must be a KGTK `number`.
 * `minval` supplies a minimum value for the `node2` column of
    matching data records.
 * `maxval` supplies a maximum value for the `node2` column of
    matching data records.
 * `requires` says that each data row that contains at least
   one property or class of the pattern's `node1` value must have
   a property or class of the `node2` value.  In this instance,
   we state that if an object has at least one RCB color component,
   it must have all three RGB color components.
 * `prohibits` says that if a `node1` data group contains an instance of
   the class in the `node1` of the pattern, then the `node1` data group must
   not contain an instance of a property in the `node2` of the pattern.
 * `mustoccur` says that each `node1` data group must contain at least
   one property of the specified class.

### Processing `node1` Groups

When `---process-node1-groups` is True (the default value is True),
edges are processed as groups with the same node1 value.  If any
edge in a group fails validation, the entire group is rejected.

When `--process-node1-groups` is False, edges are processed individually.
Only the edges that fail validation are rejected.

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

## Examples

### Colored Blocks: Property Pattern

```bash
kgtk cat -i examples/docs/valprop-colored-blocks-pattern.tsv
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

### Colored Blocks: Good Data

```bash
kgtk cat -i examples/docs/valprop-colored-blocks-good-data.tsv
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| block1 | red | 1.0 |  |
| block1 | green | 0.0 |  |
| block1 | blue | 0.0 |  |
| block2 | red | 0.0 |  |
| block2 | green | 1.0 |  |
| block2 | blue | 0.0 |  |

```bash
kgtk validate-properties \
     --input-file examples/docs/valprop-colored-blocks-good-data.tsv \
     --pattern-file examples/docs/valprop-colored-blocks-pattern.tsv \
     --output-file -
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| block1 | red | 1.0 |  |
| block1 | green | 0.0 |  |
| block1 | blue | 0.0 |  |
| block2 | red | 0.0 |  |
| block2 | green | 1.0 |  |
| block2 | blue | 0.0 |  |

### Colored Blocks: Node1 is a String

```bash
kgtk cat -i examples/docs/valprop-colored-blocks-node1-strings.tsv
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| "block1" | red | 1.0 |  |
| "block1" | green | 0.0 |  |
| "block1" | blue | 0.0 |  |
| block2 | red | 0.0 |  |
| block2 | green | 1.0 |  |
| block2 | blue | 0.0 |  |

```bash
kgtk validate-properties \
     --input-file examples/docs/valprop-colored-blocks-node1-strings.tsv \
     --pattern-file examples/docs/valprop-colored-blocks-pattern.tsv \
     --output-file - \
     --reject-file rejects.tsv
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| block2 | red | 0.0 |  |
| block2 | green | 1.0 |  |
| block2 | blue | 0.0 |  |

    Row 1: the node1 KGTK datatype 'string' is not in the list of allowed node1 types for rgbcolor: symbol
    Row 2: the node1 KGTK datatype 'string' is not in the list of allowed node1 types for rgbcolor: symbol
    Row 3: the node1 KGTK datatype 'string' is not in the list of allowed node1 types for rgbcolor: symbol

```bash
kgtk cat -i rejects.tsv
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| "block1" | red | 1.0 |  |
| "block1" | green | 0.0 |  |
| "block1" | blue | 0.0 |  |

### Colored Blocks: Node2 is a String

```bash
kgtk cat -i examples/docs/valprop-colored-blocks-node2-strings.tsv
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| block1 | red | "1.0" |  |
| block1 | green | "0.0" |  |
| block1 | blue | "0.0" |  |
| block2 | red | 0.0 |  |
| block2 | green | 1.0 |  |
| block2 | blue | 0.0 |  |

```bash
kgtk validate-properties \
     --input-file examples/docs/valprop-colored-blocks-node2-strings.tsv \
     --pattern-file examples/docs/valprop-colored-blocks-pattern.tsv \
     --output-file - \
     --reject-file rejects.tsv
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| block2 | red | 0.0 |  |
| block2 | green | 1.0 |  |
| block2 | blue | 0.0 |  |

    Row 1: the node2 KGTK datatype 'string' is not in the list of allowed node2 types for rgbcolor: number
    Row 2: the node2 KGTK datatype 'string' is not in the list of allowed node2 types for rgbcolor: number
    Row 3: the node2 KGTK datatype 'string' is not in the list of allowed node2 types for rgbcolor: number

```bash
kgtk cat -i rejects.tsv
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| block1 | red | "1.0" |  |
| block1 | green | "0.0" |  |
| block1 | blue | "0.0" |  |

### Colored Blocks: Color Values Out of Range: Grouped

```bash
kgtk cat -i examples/docs/valprop-colored-blocks-bad-values.tsv
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| block1 | red | 1.1 |  |
| block1 | green | -0.1 |  |
| block1 | blue | 0.0 |  |
| block2 | red | 0.0 |  |
| block2 | green | 1.0 |  |
| block2 | blue | 0.0 |  |

```bash
kgtk validate-properties \
     --input-file examples/docs/valprop-colored-blocks-bad-values.tsv \
     --pattern-file examples/docs/valprop-colored-blocks-pattern.tsv \
     --output-file - \
     --reject-file rejects.tsv \
     --process-node1-groups True
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| block2 | red | 0.0 |  |
| block2 | green | 1.0 |  |
| block2 | blue | 0.0 |  |

    Row 1: prop_or_datatype rgbcolor value 1.100000 is greater than maxval 1.000000.
    Row 2: prop_or_datatype rgbcolor value -0.100000 is less than minval 0.000000.

```bash
kgtk cat -i rejects.tsv
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| block1 | red | 1.1 |  |
| block1 | green | -0.1 |  |
| block1 | blue | 0.0 |  |

!!! note
    The default value for `--process-node1-groups` is True.  The option was
    included on the command line as an explicit contrast to the ungrouped example.

!!! note
    The entire `block1` group of edges was rejected, even though the `blue` edge
    was valid.

### Colored Blocks: Color Values Out of Range: Ungrouped

```bash
kgtk cat -i examples/docs/valprop-colored-blocks-bad-values.tsv
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| block1 | red | 1.1 |  |
| block1 | green | -0.1 |  |
| block1 | blue | 0.0 |  |
| block2 | red | 0.0 |  |
| block2 | green | 1.0 |  |
| block2 | blue | 0.0 |  |

```bash
kgtk validate-properties \
     --input-file examples/docs/valprop-colored-blocks-bad-values.tsv \
     --pattern-file examples/docs/valprop-colored-blocks-pattern.tsv \
     --output-file - \
     --reject-file rejects.tsv \
     --process-node1-groups False
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| block1 | blue | 0.0 |  |
| block2 | red | 0.0 |  |
| block2 | green | 1.0 |  |
| block2 | blue | 0.0 |  |

    Row 1: prop_or_datatype rgbcolor value 1.100000 is greater than maxval 1.000000.
    Row 2: prop_or_datatype rgbcolor value -0.100000 is less than minval 0.000000.

```bash
kgtk cat -i rejects.tsv
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| block1 | red | 1.1 |  |
| block1 | green | -0.1 |  |

!!! note
    Only the specific invalid edges were rejected.


### Colored Blocks: Missing Property: Grouped

```bash
kgtk cat -i examples/docs/valprop-colored-blocks-missing-red.tsv
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| block1 | red | 1.0 |  |
| block1 | green | 0.0 |  |
| block1 | blue | 0.0 |  |
| block2 | green | 1.0 |  |
| block2 | blue | 0.0 |  |

```bash
kgtk validate-properties \
     --input-file examples/docs/valprop-colored-blocks-missing-red.tsv \
     --pattern-file examples/docs/valprop-colored-blocks-pattern.tsv \
     --output-file - \
     --reject-file rejects.tsv \
     --process-node1-groups True
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| block1 | red | 1.0 |  |
| block1 | green | 0.0 |  |
| block1 | blue | 0.0 |  |

    Node 'block2': Property or datatype 'rgbcolor' requires red.

```bash
kgtk cat -i rejects.tsv
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| block2 | green | 1.0 |  |
| block2 | blue | 0.0 |  |

!!! note
    The default value for `--process-node1-groups` is True.  The option was
    included on the command line as an explicit contrast to the ungrouped example.

!!! note
    The entire `block2` group of edges was rejected.

### Colored Blocks: Missing Property: Ungrouped

```bash
kgtk cat -i examples/docs/valprop-colored-blocks-missing-red.tsv
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| block1 | red | 1.0 |  |
| block1 | green | 0.0 |  |
| block1 | blue | 0.0 |  |
| block2 | green | 1.0 |  |
| block2 | blue | 0.0 |  |

```bash
kgtk validate-properties \
     --input-file examples/docs/valprop-colored-blocks-missing-red.tsv \
     --pattern-file examples/docs/valprop-colored-blocks-pattern.tsv \
     --output-file - \
     --reject-file rejects.tsv \
     --process-node1-groups False
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| block1 | red | 1.0 |  |
| block1 | green | 0.0 |  |
| block1 | blue | 0.0 |  |
| block2 | green | 1.0 |  |
| block2 | blue | 0.0 |  |

    Node 'block2': Property or datatype 'rgbcolor' requires red.

```bash
kgtk cat -i rejects.tsv
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |


!!! note
    The missing property was detected.  However, the remaining`block2` edges were
    not rejected, since they individually passed validation.

!!! note
    A future enhancement will add an optional output file that lists the `node1`
    values with validation errors.

### Colored Blocks: Too Many Values

In the following example, `block` has two `red` values attributed to it.

```bash
kgtk cat -i examples/docs/valprop-colored-blocks-multiple-values.tsv
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| block1 | red | 0.0 |  |
| block1 | red | 1.0 |  |
| block1 | green | 0.0 |  |
| block1 | blue | 0.0 |  |
| block2 | red | 0.0 |  |
| block2 | green | 1.0 |  |
| block2 | blue | 0.0 |  |

```bash
kgtk validate-properties \
     --input-file examples/docs/valprop-colored-blocks-multiple-values.tsv \
     --pattern-file examples/docs/valprop-colored-blocks-pattern.tsv \
     --output-file - \
     --reject-file rejects.tsv
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| block2 | red | 0.0 |  |
| block2 | green | 1.0 |  |
| block2 | blue | 0.0 |  |

    Property or datatype 'red' occured 2 times for node1 'block1', maximum is 1.

```bash
kgtk cat -i rejects.tsv
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| block1 | red | 0.0 |  |
| block1 | red | 1.0 |  |
| block1 | green | 0.0 |  |
| block1 | blue | 0.0 |  |

### Colored Blocks: Missing Property Class

In this example, one of the blocks is missing its rgbcolor properties.

```bash
kgtk cat -i examples/docs/valprop-colored-blocks-missing-rgbcolor.tsv
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| block1 | red | 1.0 |  |
| block1 | green | 0.0 |  |
| block1 | blue | 0.0 |  |
| block1 | shape | cube |  |
| block2 | shape | cylinder |  |

```bash
kgtk validate-properties \
     --input-file examples/docs/valprop-colored-blocks-missing-rgbcolor.tsv \
     --pattern-file examples/docs/valprop-colored-blocks-pattern.tsv \
     --output-file - \
     --reject-file rejects.tsv
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| block1 | red | 1.0 |  |
| block1 | green | 0.0 |  |
| block1 | blue | 0.0 |  |
| block1 | shape | cube |  |

    Property or datatype 'colorclass' did not occur for node1 'block2'.

```bash
kgtk cat -i rejects.tsv
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| block2 | shape | cylinder |  |

### Colored Blocks: Prohibited Class Co-occurance

In this example, one of the blocks nas both `rgbcolor` and
`colorname`.  Only one of the two is allowed.

```bash
kgtk cat -i examples/docs/valprop-colored-blocks-prohibited-colorname.tsv
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| block1 | red | 1.0 |  |
| block1 | green | 0.0 |  |
| block1 | blue | 0.0 |  |
| block1 | colorname | red |  |
| block2 | red | 0.0 |  |
| block2 | green | 1.0 |  |
| block2 | blue | 0.0 |  |

```bash
kgtk validate-properties \
     --input-file examples/docs/valprop-colored-blocks-prohibited-colorname.tsv \
     --pattern-file examples/docs/valprop-colored-blocks-pattern.tsv \
     --output-file - \
     --reject-file rejects.tsv
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| block2 | red | 0.0 |  |
| block2 | green | 1.0 |  |
| block2 | blue | 0.0 |  |

    Node 'block1': Property or datatype 'rgbcolor' prohibits colorname.

```bash
kgtk cat -i rejects.tsv
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| block1 | red | 1.0 |  |
| block1 | green | 0.0 |  |
| block1 | blue | 0.0 |  |
| block1 | colorname | red |  |

### Colored Blocks: Good Named Colors

The colorname values must match one of the names on a list
in the pattern file.

```bash
kgtk cat -i examples/docs/valprop-colored-blocks-good-colornames.tsv
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| block1 | colorname | red |  |
| block2 | colorname | green |  |

```bash
kgtk validate-properties \
     --input-file examples/docs/valprop-colored-blocks-good-colornames.tsv \
     --pattern-file examples/docs/valprop-colored-blocks-pattern.tsv \
     --output-file -
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| block1 | colorname | red |  |
| block2 | colorname | green |  |

### Colored Blocks: Unknown Color Name

The color `mauve` is not a known color name.

```bash
kgtk cat -i examples/docs/valprop-colored-blocks-color-mauve.tsv
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| block1 | colorname | red |  |
| block2 | colorname | mauve |  |

```bash
kgtk validate-properties \
     --input-file examples/docs/valprop-colored-blocks-color-mauve.tsv \
     --pattern-file examples/docs/valprop-colored-blocks-pattern.tsv \
     --output-file -
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| block1 | colorname | red |  |

    Row 2: the node2 value 'mauve' is not in the list of allowed node2 values for colorname: blue|green|red|yellow

