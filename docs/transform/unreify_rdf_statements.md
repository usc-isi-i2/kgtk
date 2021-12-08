## Summary

`kgtk unreify-rdf-statements` simplifies data while copying a KGTK file
from input to output, by removing extra nodes caused by RDF statement
reification.

For example, consider the edges in the following table that result from importing
an AIDA TA1 ntriples file:

Input Table:

| node1 | label | node2 |
| ----- | ----- | ----- |
| XJAABmv8vGfJZZasjV6DAXY:g3 | ont:confidence | XJAABmv8vGfJZZasjV6DAXY:g4 |
| XJAABmv8vGfJZZasjV6DAXY:g3 | ont:justifiedBy | XJAABmv8vGfJZZasjV6DAXY:g5 |
| XJAABmv8vGfJZZasjV6DAXY:g3 | ont:system | nJAABmv8vGfJZZasjV6DAXY-1: |
| XJAABmv8vGfJZZasjV6DAXY:g3 | rdf:object | gaia:entities/d1dcefce-badf-4948-bfcf-5d33116fa12c |
| XJAABmv8vGfJZZasjV6DAXY:g3 | rdf:predicate | nJAABmv8vGfJZZasjV6DAXY-3:Physical.LocatedNear_Place |
| XJAABmv8vGfJZZasjV6DAXY:g3 | rdf:subject | gaia:relations/d3e1e4df-6c8c-4fd1-8b93-ee49ef238f72 |
| XJAABmv8vGfJZZasjV6DAXY:g3 | rdf:type | rdf:Statement |

The output of `kgtk unreify-rdf-statements` is below. The unified table is easier to
understand as it clearly signals that we have an event and we know the place where
the attack occured.  The secondary edges qualify the main edge, giving us context.

Output Table:

| id | node1 | label | node2 |
| -- | ----- | ----- | ----- |
| XJAABmv8vGfJZZasjV6DAXY:g3 | gaia:relations/d3e1e4df-6c8c-4fd1-8b93-ee49ef238f72 | nJAABmv8vGfJZZasjV6DAXY-3:Physical.LocatedNear_Place | gaia:entities/d1dcefce-badf-4948-bfcf-5d33116fa12c |
| XJAABmv8vGfJZZasjV6DAXY:g3-1 | XJAABmv8vGfJZZasjV6DAXY:g3 |  ont:confidence | XJAABmv8vGfJZZasjV6DAXY:g4 |
| XJAABmv8vGfJZZasjV6DAXY:g3-2 | XJAABmv8vGfJZZasjV6DAXY:g3 | ont:justifiedBy | XJAABmv8vGfJZZasjV6DAXY:g5 |
| XJAABmv8vGfJZZasjV6DAXY:g3-3 | XJAABmv8vGfJZZasjV6DAXY:g3 | ont:system | nJAABmv8vGfJZZasjV6DAXY-1: |

### Files

#### Input File

The input file is a KGTK file containing reified RDF data (among other
records), such as might have been imported from an ntriples file (see
[`kgtk import-ntriples`](../../import/import_ntriples)).

| node1 | label | node2 |
| -- | -- | -- |
| XJAABmv8vGfJZZasjV6DAXY:g3 | rdf:type | rdf:Statement |
| XJAABmv8vGfJZZasjV6DAXY:g3 | rdf:object | gaia:entities/d1dcefce-badf-4948-bfcf-5d33116fa12c |
| XJAABmv8vGfJZZasjV6DAXY:g3 | rdf:predicate | nJAABmv8vGfJZZasjV6DAXY-3:Physical.LocatedNear_Place |
| XJAABmv8vGfJZZasjV6DAXY:g3 | rdf:subject | gaia:relations/d3e1e4df-6c8c-4fd1-8b93-ee49ef238f72 |
| XJAABmv8vGfJZZasjV6DAXY:g3 | ont:confidence | XJAABmv8vGfJZZasjV6DAXY:g4 |
| XJAABmv8vGfJZZasjV6DAXY:g3 | ont:justifiedBy | XJAABmv8vGfJZZasjV6DAXY:g5 |
| XJAABmv8vGfJZZasjV6DAXY:g3 | ont:system | nJAABmv8vGfJZZasjV6DAXY-1: |

#### Output File

The output file contains the KGTK data from the input file, with reified RDF statements
and associated edges replaced with an unreified RDF edge and secondary edges.

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| gaia:relations/d3e1e4df-6c8c-4fd1-8b93-ee49ef238f72 | nJAABmv8vGfJZZasjV6DAXY-3:Physical.LocatedNear_Place | gaia:entities/d1dcefce-badf-4948-bfcf-5d33116fa12c |
 XJAABmv8vGfJZZasjV6DAXY:g3 |
| XJAABmv8vGfJZZasjV6DAXY:g3 | ont:confidence | XJAABmv8vGfJZZasjV6DAXY:g4 | XJAABmv8vGfJZZasjV6DAXY:g3-1 |
| XJAABmv8vGfJZZasjV6DAXY:g3 | ont:justifiedBy | XJAABmv8vGfJZZasjV6DAXY:g5 | XJAABmv8vGfJZZasjV6DAXY:g3-2 |
| XJAABmv8vGfJZZasjV6DAXY:g3 | ont:system | nJAABmv8vGfJZZasjV6DAXY-1: | XJAABmv8vGfJZZasjV6DAXY:g3-3 |

An `id` column is added to the output file if it is not present in the input file.
This is used to link secondary edges to the newly reconstituted unreified edge.

At the present time, `kgtk unreify-rdf-statements` does not generate `id` values for
other edges in the file. This feature may be added in the future.

The edges in the output file are not likely to be in the same order as they appeared
in the input file.  If you wish to compare the input to the output files, read the
section below on Difference Comparison.

#### Reified File

This optional file will receive a copy of just the input data records that matched the
reified RDF statement pattern.  The records are the same as they were in the input
file, e.g., an `id` column might not be present.

#### Unreified File

This optional file will receive a copy of just the output records that were generated
by by unreifying RDF statements in the input file.  The records in this file will be in
the output file's format, e.g., an `id` column will be present.

#### Uninvolved File

This optional file will receive a copy of the input data records that did not
match the reified RDF statement pattern.  The records are the same as they were in the input
file, e.g., an `id` column might not be present.

### Pattern Match Parameters

`kgtk unreify-rdf-statements` has a built-in set of pattern match parameters that
will not change for normal operation.  All pattern matches reference the usual
`node1`, `label`, and `node2` columns or their aliases; there are no options to
override the column names.

The Difference Comparison section, below, describes one use case in which overriding
the pattern match parameters can be beneficial.

```
  --trigger-label TRIGGER_LABEL_VALUE
                        A value that identifies the trigger label. (default=rdf:type).
  --trigger-node2 TRIGGER_NODE2_VALUE
                        A value that identifies the trigger node2. (default=rdf:Statement).
  --node1-role RDF_SUBJECT_LABEL_VALUE
                        The label that identifies the edge with the node2 value that will
                        serve in the node1 role. (default=rdf:subject).
  --label-role RDF_PREDICATE_LABEL_VALUE
                        The label that identifies the edge with the node2 value that will
                        serve in the label role. (default=rdf:predicate).
  --node2-role RDF_OBJECT_LABEL_VALUE
                        The label that identifies the edge with the node2 value that will
                        serve in the node2 role. (default=rdf:object).
```

### Cartesian Crossproduct

`kgtk unreify-rdf-statements` processes multiple subject, predicates, and/or
objects in the reified input edges by generating one set of unreified edges
(both the unreified data edge and any secondary edges) for each combination
of (subject, predicate, object).  This processing may be disabled by options
to disallow multiple subjects, multiple predicates, and multiple
objects.

When processing of multiple subjects, predicates, or objects has been disabled,
and multiple subjects, predicates, or objects are encountered in the input
stream, a warning message will be issued (if `--verbose` output is enabled)
and the group of input data will not be unreified.

```
  --allow-multiple-subjects [ALLOW_MULTIPLE_SUBJECTS]
                        When true, allow multiple subjects, resulting in a cartesian
                        product. (default=True).
  --allow-multiple-predicates [ALLOW_MULTIPLE_PREDICATES]
                        When true, allow multiple predicates, resulting in a cartesian
                        product. (default=True).
  --allow-multiple-objects [ALLOW_MULTIPLE_OBJECTS]
                        When true, allow multiple objects, resulting in a cartesian product.
                        (default=True).
```

### Broken Edges

Unless a Cartesian Crossproduct is being generated, `kgtk unreify-rdf-statements`
uses the `node1` value of an input reified RDF statement ("XJAABmv8vGfJZZasjV6DAXY:g3")
as the edge `id` of the output unreified RDF edge record, and as the `node1` value of the
secondary edges. If for some reason there are other edges that refer to
this symbol ("XJAABmv8vGfJZZasjV6DAXY:g3") in the `label` or `node2` columns, or in
extra columns, they will retain linkage to the unreified edges.

If a Cartesian Crossproduct is being generated, then the `node1` value of the input reified
RDF statement as the base for the `id` and `node1` values used in the generated edges:

```
XJAABmv8vGfJZZasjV6DAXY:g3-1
XJAABmv8vGfJZZasjV6DAXY:g3-2
...
```

The width of the suffix is adjusted for the number of crossproduct edges being generated,
i.e. if more than 9 edges were being generated, they would use these `id` and `node1` values:

```
XJAABmv8vGfJZZasjV6DAXY:g3-01
XJAABmv8vGfJZZasjV6DAXY:g3-02
...
XJAABmv8vGfJZZasjV6DAXY:g3-10
...
```

These generated edge and `node1` values are designed to keep the generated reified
edges and secondary edges in proximity when sorted by `id`, whether Cartesian Crossproducts
are being generated or not.  However, when Cartesian Crossproducts are being generated,
then the new `id` and `node1` values cannot be as easily linked to esternal nodes referencing them.

### Difference Comparison

`kgtk unreify-rdf-statements` sorts its input data as part of detecting
reified RDF statements. Thus, attempting to look for changes between the input
file and the output file using an ordinary difference utility is not likely to
be fruitful.  Instead, employ the following strategy:

 * add an ID column to the input data if it does not already have one, using [`kgtk add-id`](../add_id)
   * Perhaps without generating ID values, to remove clutter.
   * `kgtk add-id --id-style=empty`
 * sort the resulting data using `kgtk unreify-rdf-statements` with a disabled pattern match parameter.
   * `kgtk unreify-rdf-statements --trigger-label=XXX -o output1.tsv`
 * Apply `kgtk unreify-rdf-statements` a second time without disabling the pattern match.
   * `kgtk unreify-rdf-statements -o output2.tsv`
 * Compare the two output files.

## Usage

```
usage: kgtk unreify-rdf-statements [-h] [-i INPUT_FILE] [-o OUTPUT_FILE]
                                   [--reified-file REIFIED_FILE]
                                   [--unreified-file UNREIFIED_FILE]
                                   [--uninvolved-file UNINVOLVED_FILE]
                                   [--trigger-label TRIGGER_LABEL_VALUE]
                                   [--trigger-node2 TRIGGER_NODE2_VALUE]
                                   [--node1-role RDF_SUBJECT_LABEL_VALUE]
                                   [--label-role RDF_PREDICATE_LABEL_VALUE]
                                   [--node2-role RDF_OBJECT_LABEL_VALUE]
                                   [--allow-multiple-subjects [ALLOW_MULTIPLE_SUBJECTS]]
                                   [--allow-multiple-predicates [ALLOW_MULTIPLE_PREDICATES]]
                                   [--allow-multiple-objects [ALLOW_MULTIPLE_OBJECTS]]
                                   [-v [optional True|False]]

Read a KGTK file, such as might have been created by importing an ntriples file.  Search for reified RFD statements and transform them into an unreified form.

An ID column will be added to the output file if not present in the input file.  

--reified-file PATH, if specified, will get a copy of the input records that were identified as reified RDF statements. 

--uninvolved-file PATH, if specified, will get a copy of the input records that were  identified as not being reified RDF statements. 

--unreified-file PATH, if specified, will get a copy of the unreified output records, which  will still be written to the main output file.

Additional options are shown in expert help.
kgtk --expert unreify-rdb-statements --help

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK input file with the reified data. (May be
                        omitted or '-' for stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for
                        stdout.)
  --reified-file REIFIED_FILE
                        A KGTK output file that will contain only the reified
                        RDF statements. (Optional, use '-' for stdout.)
  --unreified-file UNREIFIED_FILE
                        A KGTK output file that will contain only the
                        unreified RDF statements. (Optional, use '-' for
                        stdout.)
  --uninvolved-file UNINVOLVED_FILE
                        A KGTK output file that will contain only the
                        uninvolved input. (Optional, use '-' for stdout.)
  --trigger-label TRIGGER_LABEL_VALUE
                        A value that identifies the trigger label.
                        (default=rdf:type).
  --trigger-node2 TRIGGER_NODE2_VALUE
                        A value that identifies the trigger node2.
                        (default=rdf:Statement).
  --node1-role RDF_SUBJECT_LABEL_VALUE
                        The label that identifies the edge with the node2
                        value that will serve in the node1 role.
                        (default=rdf:subject).
  --label-role RDF_PREDICATE_LABEL_VALUE
                        The label that identifies the edge with the node2
                        value that will serve in the label role.
                        (default=rdf:predicate).
  --node2-role RDF_OBJECT_LABEL_VALUE
                        The label that identifies the edge with the node2
                        value that will serve in the node2 role.
                        (default=rdf:object).
  --allow-multiple-subjects [ALLOW_MULTIPLE_SUBJECTS]
                        When true, allow multiple subjects, resulting in a
                        cartesian product. (default=True).
  --allow-multiple-predicates [ALLOW_MULTIPLE_PREDICATES]
                        When true, allow multiple predicates, resulting in a
                        cartesian product. (default=True).
  --allow-multiple-objects [ALLOW_MULTIPLE_OBJECTS]
                        When true, allow multiple objects, resulting in a
                        cartesian product. (default=True).

  -v [optional True|False], --verbose [optional True|False]
                        Print additional progress messages (default=False).
```

## Examples

### Example 1

```bash
kgtk cat -i examples/docs/unreify-rdf-statements-file1.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| XJAABmv8vGfJZZasjV6DAXY:g3 | ont:confidence | XJAABmv8vGfJZZasjV6DAXY:g4 |
| XJAABmv8vGfJZZasjV6DAXY:g3 | ont:justifiedBy | XJAABmv8vGfJZZasjV6DAXY:g5 |
| XJAABmv8vGfJZZasjV6DAXY:g3 | ont:system | nJAABmv8vGfJZZasjV6DAXY-1: |
| XJAABmv8vGfJZZasjV6DAXY:g3 | rdf:object | gaia:entities/d1dcefce-badf-4948-bfcf-5d33116fa12c |
| XJAABmv8vGfJZZasjV6DAXY:g3 | rdf:predicate | nJAABmv8vGfJZZasjV6DAXY-3:Physical.LocatedNear_Place |
| XJAABmv8vGfJZZasjV6DAXY:g3 | rdf:subject | gaia:relations/d3e1e4df-6c8c-4fd1-8b93-ee49ef238f72 |
| XJAABmv8vGfJZZasjV6DAXY:g3 | rdf:type | rdf:Statement |


```bash
kgtk unreify-rdf-statements -i examples/docs/unreify-rdf-statements-file1.tsv
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| gaia:relations/d3e1e4df-6c8c-4fd1-8b93-ee49ef238f72 | nJAABmv8vGfJZZasjV6DAXY-3:Physical.LocatedNear_Place | gaia:entities/d1dcefce-badf-4948-bfcf-5d33116fa12c | XJAABmv8vGfJZZasjV6DAXY:g3 |
| XJAABmv8vGfJZZasjV6DAXY:g3 | ont:confidence | XJAABmv8vGfJZZasjV6DAXY:g4 | XJAABmv8vGfJZZasjV6DAXY:g3-1 |
| XJAABmv8vGfJZZasjV6DAXY:g3 | ont:justifiedBy | XJAABmv8vGfJZZasjV6DAXY:g5 | XJAABmv8vGfJZZasjV6DAXY:g3-2 |
| XJAABmv8vGfJZZasjV6DAXY:g3 | ont:system | nJAABmv8vGfJZZasjV6DAXY-1: | XJAABmv8vGfJZZasjV6DAXY:g3-3 |

### Example 2

```bash
kgtk cat -i examples/docs/unreify-rdf-statements-file2.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| _:g2301 | ont:confidence | _:g2302 |
| _:g2301 | ont:justifiedBy | _:g2303 |
| _:g2301 | ont:system | rpi1: |
| _:g2301 | rdf:object | entity:c6f32b90-6038-40c0-97e4-6d3f7fd76c03 |
| _:g2301 | rdf:predicate | ldc:Movement.TransportPerson.SelfMotion_Transporter |
| _:g2301 | rdf:subject | event:03a41b2b-e0ef-42f9-a192-433e0abc3a70 |
| _:g2301 | rdf:type | rdf:Statement |
| _:g3910 | ont:confidence | _:g3911 |
| _:g3910 | ont:justifiedBy | _:g3912 |
| _:g3910 | ont:system | rpi1: |
| _:g3910 | rdf:object | entity:fcb78e77-4962-4fca-977b-aea84bfa3ddd |
| _:g3910 | rdf:predicate | ldc:Movement.TransportPerson.SelfMotion_Destination |
| _:g3910 | rdf:subject | event:03a41b2b-e0ef-42f9-a192-433e0abc3a70 |
| _:g3910 | rdf:type | rdf:Statement |

```bash
kgtk unreify-rdf-statements -i examples/docs/unreify-rdf-statements-file2.tsv
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| event:03a41b2b-e0ef-42f9-a192-433e0abc3a70 | ldc:Movement.TransportPerson.SelfMotion_Transporter | entity:c6f32b90-6038-40c0-97e4-6d3f7fd76c03 | _:g2301 |
| _:g2301 | ont:confidence | _:g2302 | _:g2301-1 |
| _:g2301 | ont:justifiedBy | _:g2303 | _:g2301-2 |
| _:g2301 | ont:system | rpi1: | _:g2301-3 |
| event:03a41b2b-e0ef-42f9-a192-433e0abc3a70 | ldc:Movement.TransportPerson.SelfMotion_Destination | entity:fcb78e77-4962-4fca-977b-aea84bfa3ddd | _:g3910 |
| _:g3910 | ont:confidence | _:g3911 | _:g3910-1 |
| _:g3910 | ont:justifiedBy | _:g3912 | _:g3910-2 |
| _:g3910 | ont:system | rpi1: | _:g3910-3 |
