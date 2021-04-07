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
`kgtk validate-properties` supports the application of constraints to any additional columns
that are present.

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

### Table of Actions

| Action | Description |
| ------ | ----------- |
| datatype | The `node1` symbol of this pattern edge is a property class. |
| equal_to | The `node2` value or field value in the data edge is a number that equals one of the `node2` numbers in the pattern edge(s). |
| equal_to_date | The `node2` value or field value in the data edge is a date that equals one of the `node2` dates in the pattern edge(s). |
| field_blank | The selected field is blank. |
| field_name | The `node2` symbol in the pattern edge is a field name selector. May be repeated (or `node2` may contain a list if permitted). |
| field_not_blank | The selected field is not blank. |
| field_not_pattern | The selected field does not matcn the pattern in the pattern edge `node2` value. |
| field_not_values | The value of the field is not the same as the value in the pattern edge `node2`.  May be repeated (or `node2` may contain a list if permitted).|
| field_pattern | The selected field matches the pattern in the pattern edge `node2` value. |
| field_values | The value of the field is the same as the value in the pattern edge `node2`.  May be repeated (or `node2` may contain a list if permitted). |
| greater_than | The `node2` value or field value in the data edge is a number that is greater than the `node2` number in the pattern edge.  |
| greater_than_date | The `node2` value or field value in the data edge is a date that is greater than the `node2` number in the pattern edge.|
| groupbyprop | When specified, a list of classes that serve as aggregation levels for max/min distinct/occurs calculations. |
| id_allow_list | When the `node2` value of this pattern edge is True, the `id` value for data rows with `label` values in the class of the `node1` value of the pattern edge may be a KGTK list. |
| id_blank | When the `node2` value of this pattern edge is True, the `id` value for data rows with `label` values in the class of the `node1` value of the pattern edge must be empty.  When False, the `id` value for data rows with `label` value in this class must not be empty. |
| id_chain | The `id` value of the data edge with a `label` value matching the `node1` value of the pattern edge must match the `node1` value of a second data edge (the remote data edge), and the remote data edge must match at least one class in the `node2` value of the pattern edge. |
| id_not_blank | When the `node2` value of this pattern edge is True, the `id` value for data rows with `label` values in this class must not be empty.  When False, the `id` value for data rows with `label` value in this class must be empty. |
| id_not_pattern | The `id` value of a data edge with a `label` value in the class of the `node1` value of the pattern edge must not match the regular expression in the `node2` value of the pattern edge.|
| id_pattern | The `id` value of a data edge with a `label` value in the class of the `node1` value of the pattern edge must match the regular expression in the `node2` value of the pattern edge.|
| isa | The class in the `node1` value of the pattern edge is a subclass of the class in the `node2` value of the pattern edge. |
| label_allow_list | For data edges with `label` values matching the `node1` value of the pattern edge, the `label` value of the data edge may be a KGTK list when the `node2` value of the pattern edge is True. When the `node2` value of the pattern edge is False, the `label` value of the data edge must not be a KGTK list. Note that the KGTK File Specification does not allow KGTK lists in KGTK edge files.|
| label_pattern | The `label` value of a data edte with a `label` value in the class of the `node1` value of the pattern edge must match the regular expression in the `node2` value of the pattern edge. |
| less_than | The `node2` value or field value in the data edge is a number that is less than the `node2` number in the pattern edge. |
| less_than_date | The `node2` value or field value in the data edge is a date that is less than the `node2` number in the pattern edge. |
| matches | The `node1` value of the pattern edge is a superclass of any class that matches the regular expresison in the `node2` value of the pattern edge. |
| maxdate | For each data edge attempting to match the class name in the `node1` value of the pattern edge, the `node2` value of the data edge must be a date/time value less than or equal to the date/time `node2` value in the pattern edge. |
| maxoccurs | For each `node1` group in the data file, there must be no more data edges matching the `node1` class of the pattern edge than the `node2` value of the pattern edge. |
| maxval | The `node2` value of each data edge matching the `node1` class in the pattern edge must have a numeric value no greater than the `node2` value of the pattern edge. |
| mindate | For each data edge attempting to match the class name in the `node1` value of the pattern edge, the `node2` value of the data edge must be a date/time value no less than the date/time `node2` value in the pattern edge.  |
| minoccurs | For each `node1` group in the data file, there must be no fewer data edges matching the `node1` class of the pattern edge than the `node2` value of the pattern edge.  |
| minval | The `node2` value of each data edge matching the `node1` class in the pattern edge must have a numeric value no less than the `node2` value of the pattern edge. |
| mustoccur | When the `node2` value of the pattern edge is True, the `node1` value of the pattern edge is a class that must orrure in each `node1` group of the data edges. |
| nextcase | The `node2` value of the pattern edge is the `node1` value of the next case in an ordered switch. |
| node1_type | The `node1` value of the data edge that matches the class in the `label of the pattern edge must be of the KGTK data type listed in the `node2` column of the pattern edge.|
| node1_allow_list | When the `node2` value of the pattern edge is True, any data edge with a clss matching the `label` value of the pattern edge may allow KGTK lists in the `node1` value of the data edge.  When the `node2` value of the pattern edge is False, any data edges in this class must not have KGTK list value in `node2`.  Note: The KGTK File Specificaiton prohibits KGTK lists in the `node1` value of a KGTK edge. |
| node1_values | For data edges in classes that match the `node1` value of the pattern edge, the `node2` value of the data edge must be one of the `node2` values in the pattern edge.  |
| node2_allow_list | When the `node2` value of the pattern edge is True, any data edge with a clss matching the `label` value of the pattern edge may allow KGTK lists in the `node2` value of the data edge.  When the `node2` value of the pattern edge is False, any data edges in this class must not have KGTK list value in `node2`.  Note: The KGTK File Specificaiton prohibits KGTK lists in the `node1` value of a KGTK edge.|
| node2_blank | When the `node2` value of this pattern edge is True, the `node2` value for data rows with `label` values in this class must be empty.  When False, the `node2` value for data rows with `label` value in this class must not be empty. Note: The KGTK File Specification requires that `node2` value be non-empty in KGTK edge files. |
| node2_chain | The `node2` value of the data edge with a `label` value matching the `node1` value of the pattern edge must match the `node1` value of a second data edge (the remote data edge), and the remore data edge must match at least one class in the `node2` value of the pattern edge. |
| node2_column | The `node2` value of the pattern edge specifies a additional column to use instead of `node2`. |
| node2_is_valid | When `node2` of the pattern edge is True, the `node2` value of data edges for this class must be valid KGTK valies. |
| node2_not_blank | When the `node2` value of this pattern edge is True, the `node2` value for data rows with `label` values in this class must not be empty.  When False, the `node2` value for data rows with `label` value in this class must be empty. Note: The KGTK File Specification requires that `node2` value be non-empty in KGTK edge files. |
| node2_not_pattern | |
| node2_not_type | |
| node2_not_values | |
| node2_pattern | |
| node2_type | |
| node2_values | |
| not_equal_to | |
| not_equal_to_date | |
| not_in_columns | |
| node2_field_op | |
| prohibits | |
| property | |
| reject | |
| requires | |
| switch | |
| unknown | |

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
| block3 | colorname | red |  |
| block4 | colorname | green |  |

```bash
kgtk validate-properties \
     --input-file examples/docs/valprop-colored-blocks-good-colornames.tsv \
     --pattern-file examples/docs/valprop-colored-blocks-pattern.tsv \
     --output-file -
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| block3 | colorname | red |  |
| block4 | colorname | green |  |

### Colored Blocks: Unknown Color Name

The color `mauve` is not a known color name.

```bash
kgtk cat -i examples/docs/valprop-colored-blocks-color-mauve.tsv
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| block3 | colorname | red |  |
| block4 | colorname | mauve |  |

```bash
kgtk validate-properties \
     --input-file examples/docs/valprop-colored-blocks-color-mauve.tsv \
     --pattern-file examples/docs/valprop-colored-blocks-pattern.tsv \
     --output-file -
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| block3 | colorname | red |  |

    Row 2: the node2 value 'mauve' is not in the list of allowed node2 values for colorname: blue|green|red|yellow

### Colored Blocks: `--add-isa-column` Reveals Class Membership

When the `--add-isa-column` option is True (the default is False),
a column is added to the output and reject files to display the
class memberships deduced for each edge.

The default ISA column name is `isa;node2`.  The `--isa-column-name COLUMN_NAME`
option may be used to change that.

```bash
kgtk cat -i examples/docs/valprop-colored-blocks-mixed-types.tsv
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| block1 | red | 1.0 |  |
| block1 | green | 0.0 |  |
| block1 | blue | 0.0 |  |
| block2 | red | 0.0 |  |
| block2 | green | 1.0 |  |
| block2 | blue | 0.0 |  |
| block3 | colorname | red |  |
| block4 | colorname | green |  |


```bash
kgtk validate-properties \
     --input-file examples/docs/valprop-colored-blocks-mixed-types.tsv \
     --pattern-file examples/docs/valprop-colored-blocks-pattern.tsv \
     --output-file - \
     --add-isa-column --isa-column-name Classes
```

| node1 | label | node2 | id | Classes |
| -- | -- | -- | -- | -- |
| block1 | red | 1.0 |  | red->rgbcolor->colorclass |
| block1 | green | 0.0 |  | green->rgbcolor->colorclass |
| block1 | blue | 0.0 |  | blue->rgbcolor->colorclass |
| block2 | red | 0.0 |  | red->rgbcolor->colorclass |
| block2 | green | 1.0 |  | green->rgbcolor->colorclass |
| block2 | blue | 0.0 |  | blue->rgbcolor->colorclass |
| block3 | colorname | red |  | colorname->colorclass |
| block4 | colorname | green |  | colorname->colorclass |

### Colored Blocks: Use `matches` Instead of `isa`

Instead of declaring that a subclass isa superclass, you can
say superclass matches <subclass pattern>.

Here is a pattern file using `matches`:

```bash
kgtk cat -i examples/docs/valprop-colored-blocks-pattern-matches.tsv
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| red | property | True |  |
| red | maxoccurs | 1 |  |
| green | property | True |  |
| green | maxoccurs | 1 |  |
| blue | property | True |  |
| blue | maxoccurs | 1 |  |
| rgbcolor | datatype | True |  |
| rgbcolor | node1_type | symbol |  |
| rgbcolor | node2_type | number |  |
| rgbcolor | minval | 0.0 |  |
| rgbcolor | maxval | 1.0 |  |
| rgbcolor | matches | "red\\\|green\\\|blue" |  |
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

```bash
kgtk validate-properties \
     --input-file examples/docs/valprop-colored-blocks-mixed-types.tsv \
     --pattern-file examples/docs/valprop-colored-blocks-pattern-matches.tsv \
     --output-file - \
     --add-isa-column --isa-column-name Classes
```

| node1 | label | node2 | id | Classes |
| -- | -- | -- | -- | -- |
| block1 | red | 1.0 |  | red->rgbcolor->colorclass |
| block1 | green | 0.0 |  | green->rgbcolor->colorclass |
| block1 | blue | 0.0 |  | blue->rgbcolor->colorclass |
| block2 | red | 0.0 |  | red->rgbcolor->colorclass |
| block2 | green | 1.0 |  | green->rgbcolor->colorclass |
| block2 | blue | 0.0 |  | blue->rgbcolor->colorclass |
| block3 | colorname | red |  | colorname->colorclass |
| block4 | colorname | green |  | colorname->colorclass |


### Colored Blocks: Multiple Inheritance

```bash
kgtk cat -i examples/docs/valprop-colored-blocks-with-shapes.tsv
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| block1 | cube | True |  |
| block1 | red | 1.0 |  |
| block1 | green | 0.0 |  |
| block1 | blue | 0.0 |  |
| block2 | red | 0.0 |  |
| block2 | green | 1.0 |  |
| block2 | blue | 0.0 |  |
| block2 | sphere | True |  |
| block3 | red | 0.0 |  |
| block3 | green | 0.0 |  |
| block3 | blue | 1.0 |  |
| block3 | cone | True |  |
| block4 | red | 1.0 |  |
| block4 | green | 1.0 |  |
| block4 | blue | 0.0 |  |
| block4 | pyramid | True |  |

```bash
kgtk cat -i examples/docs/valprop-colored-blocks-pattern-with-shapes.tsv
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
| cube | property | True |  |
| cube | isa | boxshape |  |
| cone | property | True |  |
| cone | isa | pointyshape |  |
| cone | isa | roundshape |  |
| sphere | property | True |  |
| sphere | isa | roundshape |  |
| pyramid | property | True |  |
| pyramid | isa | pointyshape |  |
| cylinder | property | True |  |
| cylinder | isa | roundshape |  |
| boxshape | datatype | True |  |
| boxshape | isa | shape |  |
| pointyshape | datatype | True |  |
| pointyshape | isa | shape |  |
| roundshape | datatype | True |  |
| roundshape | isa | shape |  |
| shape | datatype | True |  |
| shape | mustoccur | True |  |

```bash
kgtk validate-properties \
     --input-file examples/docs/valprop-colored-blocks-with-shapes.tsv \
     --pattern-file examples/docs/valprop-colored-blocks-pattern-with-shapes.tsv \
     --output-file - \
     --add-isa-column --isa-column-name Classes
```

| node1 | label | node2 | id | Classes |
| -- | -- | -- | -- | -- |
| block1 | cube | True |  | cube->boxshape->shape |
| block1 | red | 1.0 |  | red->rgbcolor->colorclass |
| block1 | green | 0.0 |  | green->rgbcolor->colorclass |
| block1 | blue | 0.0 |  | blue->rgbcolor->colorclass |
| block2 | red | 0.0 |  | red->rgbcolor->colorclass |
| block2 | green | 1.0 |  | green->rgbcolor->colorclass |
| block2 | blue | 0.0 |  | blue->rgbcolor->colorclass |
| block2 | sphere | True |  | sphere->roundshape->shape |
| block3 | red | 0.0 |  | red->rgbcolor->colorclass |
| block3 | green | 0.0 |  | green->rgbcolor->colorclass |
| block3 | blue | 1.0 |  | blue->rgbcolor->colorclass |
| block3 | cone | True |  | cone->(pointyshape->shape, roundshape->shape) |
| block4 | red | 1.0 |  | red->rgbcolor->colorclass |
| block4 | green | 1.0 |  | green->rgbcolor->colorclass |
| block4 | blue | 0.0 |  | blue->rgbcolor->colorclass |
| block4 | pyramid | True |  | pyramid->pointyshape->shape |

### Colored Blocks: Unordered Switch

The unordered `switch` statement provides class inheritance on a row-by-row
basis.  The first class that matches the row is selected, but there is no guarantee on the
order in which the list of classes is evaluated.

In this example, the `shape` property has a shape name in `node2`.
We use the `node2` value in each `shape` edge to select a specific
class.

```bash
kgtk cat -i examples/docs/valprop-colored-blocks-for-switch.tsv
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| block1 | colorname | red |  |
| block1 | shape | cube |  |
| block2 | colorname | green |  |
| block2 | shape | sphere |  |
| block3 | colorname | blue |  |
| block3 | shape | cone |  |
| block4 | colorname | yellow |  |
| block4 | shape | pyramid |  |

```bash
kgtk cat -i examples/docs/valprop-colored-blocks-pattern-unordered-switch.tsv
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| colorname | property | True |  |
| colorname | isa | colorclass |  |
| colorname | node1_type | symbol |  |
| colorname | node2_type | symbol |  |
| colorname | node2_values | red |  |
| colorname | node2_values | green |  |
| colorname | node2_values | blue |  |
| colorname | node2_values | yellow |  |
| colorclass | mustoccur | True |  |
| shape | property | True |  |
| shape | node1_type | symbol |  |
| shape | node2_type | symbol |  |
| shape | switch | cube |  |
| shape | switch | cone |  |
| shape | switch | sphere |  |
| shape | switch | pyramid |  |
| shape | switch | cylinder |  |
| cube | datatype | True |  |
| cube | isa | boxshape |  |
| cube | node2_values | cube |  |
| cone | datatype | True |  |
| cone | isa | pointyshape |  |
| cone | isa | roundshape |  |
| cone | node2_values | cone |  |
| sphere | datatype | True |  |
| sphere | isa | roundshape |  |
| sphere | node2_values | sphere |  |
| pyramid | datatype | True |  |
| pyramid | isa | pointyshape |  |
| pyramid | node2_values | pyramid |  |
| cylinder | datatype | True |  |
| cylinder | isa | roundshape |  |
| cylinder | node2_values | cylinder |  |
| boxshape | datatype | True |  |
| boxshape | isa | shapeclass |  |
| pointyshape | datatype | True |  |
| pointyshape | isa | shapeclass |  |
| roundshape | datatype | True |  |
| roundshape | isa | shapeclass |  |
| shapeclass | datatype | True |  |
| shapeclass | mustoccur | True |  |

```bash
kgtk validate-properties \
     --input-file examples/docs/valprop-colored-blocks-for-switch.tsv \
     --pattern-file examples/docs/valprop-colored-blocks-pattern-unordered-switch.tsv \
     --output-file - \
     --add-isa-column --isa-column-name Classes
```

| node1 | label | node2 | id | Classes |
| -- | -- | -- | -- | -- |
| block1 | colorname | red |  | colorname->colorclass |
| block1 | shape | cube |  | shape->cube->boxshape->shapeclass |
| block2 | colorname | green |  | colorname->colorclass |
| block2 | shape | sphere |  | shape->sphere->roundshape->shapeclass |
| block3 | colorname | blue |  | colorname->colorclass |
| block3 | shape | cone |  | shape->cone->(pointyshape->shapeclass, roundshape->shapeclass) |
| block4 | colorname | yellow |  | colorname->colorclass |
| block4 | shape | pyramid |  | shape->pyramid->pointyshape->shapeclass |

### Colored Blocks: Ordered Switch

The ordered `switch` statement provides class inheritance on a row-by-row
basis.  The first class that matches is selected, with a guarantee on the
order in which the list is evaluated.

In this example, the `shape` property has a shape name in `node2`.
We use the `node2` value in each `shape` edge to select a specific
class.

```bash
kgtk cat -i examples/docs/valprop-colored-blocks-for-switch.tsv
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| block1 | colorname | red |  |
| block1 | shape | cube |  |
| block2 | colorname | green |  |
| block2 | shape | sphere |  |
| block3 | colorname | blue |  |
| block3 | shape | cone |  |
| block4 | colorname | yellow |  |
| block4 | shape | pyramid |  |

```bash
kgtk cat -i examples/docs/valprop-colored-blocks-pattern-ordered-switch.tsv
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| colorname | property | True |  |
| colorname | isa | colorclass |  |
| colorname | node1_type | symbol |  |
| colorname | node2_type | symbol |  |
| colorname | node2_values | red |  |
| colorname | node2_values | green |  |
| colorname | node2_values | blue |  |
| colorname | node2_values | yellow |  |
| colorclass | mustoccur | True |  |
| shape | property | True |  |
| shape | node1_type | symbol |  |
| shape | node2_type | symbol |  |
| shape | switch | shapetest1 |  |
| shapetest1 | isa | cube |  |
| shapetest1 | nextcase | shapetest2 |  |
| shapetest2 | isa | cone |  |
| shapetest2 | nextcase | shapetest3 |  |
| shapetest3 | isa | sphere |  |
| shapetest3 | nextcase | shapetest4 |  |
| shapetest4 | isa | pyramid |  |
| shapetedt4 | nextcase | shapetest5 |  |
| shapetest5 | isa | cylinder |  |
| cube | datatype | True |  |
| cube | isa | boxshape |  |
| cube | node2_values | cube |  |
| cone | datatype | True |  |
| cone | isa | pointyshape |  |
| cone | isa | roundshape |  |
| cone | node2_values | cone |  |
| sphere | datatype | True |  |
| sphere | isa | roundshape |  |
| sphere | node2_values | sphere |  |
| pyramid | datatype | True |  |
| pyramid | isa | pointyshape |  |
| pyramid | node2_values | pyramid |  |
| cylinder | datatype | True |  |
| cylinder | isa | roundshape |  |
| cylinder | node2_values | cylinder |  |
| boxshape | datatype | True |  |
| boxshape | isa | shapeclass |  |
| pointyshape | datatype | True |  |
| pointyshape | isa | shapeclass |  |
| roundshape | datatype | True |  |
| roundshape | isa | shapeclass |  |
| shapeclass | datatype | True |  |
| shapeclass | mustoccur | True |  |

```bash
kgtk validate-properties \
     --input-file examples/docs/valprop-colored-blocks-for-switch.tsv \
     --pattern-file examples/docs/valprop-colored-blocks-pattern-ordered-switch.tsv \
     --output-file - \
     --add-isa-column --isa-column-name Classes
```

| node1 | label | node2 | id | Classes |
| -- | -- | -- | -- | -- |
| block1 | colorname | red |  | colorname->colorclass |
| block1 | shape | cube |  | shape->shapetest1->cube->boxshape->shapeclass |
| block2 | colorname | green |  | colorname->colorclass |
| block2 | shape | sphere |  | shape->shapetest3->sphere->roundshape->shapeclass |
| block3 | colorname | blue |  | colorname->colorclass |
| block3 | shape | cone |  | shape->shapetest2->cone->(pointyshape->shapeclass, roundshape->shapeclass) |
| block4 | colorname | yellow |  | colorname->colorclass |
| block4 | shape | pyramid |  | shape->shapetest4->pyramid->pointyshape->shapeclass |
