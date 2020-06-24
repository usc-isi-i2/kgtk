The unreify_rdf_statements command simplifies data while copying a KGTK file
from input to output, by removing extra nodes caused by RDF statement
reification.

For example, consider the edges in the following table that result from importing
and AIDA TA1 ntriples file:

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

The output of `kgtk unreify_rdf_statements` is below. The unified table is easier to
understand as it clearly signals that we have an event and we know the place where
the attacu occured.  The secondary edges qualify the main edge, giving us context.

Output Table:
| id | node1 | label | node2 |
| -- | ----- | ----- | ----- |
| XJAABmv8vGfJZZasjV6DAXY:g3 | gaia:relations/d3e1e4df-6c8c-4fd1-8b93-ee49ef238f72 | nJAABmv8vGfJZZasjV6DAXY-3:Physical.LocatedNear_Place | gaia:entities/d1dcefce-badf-4948-bfcf-5d33116fa12c |
| XJAABmv8vGfJZZasjV6DAXY:g3-1 | XJAABmv8vGfJZZasjV6DAXY:g3 |  ont:confidence | XJAABmv8vGfJZZasjV6DAXY:g4 |
| XJAABmv8vGfJZZasjV6DAXY:g3-2 | XJAABmv8vGfJZZasjV6DAXY:g3 | ont:justifiedBy | XJAABmv8vGfJZZasjV6DAXY:g5 |
| XJAABmv8vGfJZZasjV6DAXY:g3-3 | XJAABmv8vGfJZZasjV6DAXY:g3 | ont:system | nJAABmv8vGfJZZasjV6DAXY-1: |

## Usage

```
usage: kgtk unreify_rdf_statements [-h] [-i INPUT_KGTK_FILE] [-o OUTPUT_KGTK_FILE]
                                   [--reified-file REIFIED_KGTK_FILE]
                                   [--unreified-file UNREIFIED_KGTK_FILE]
                                   [--uninvolved-file UNINVOLVED_KGTK_FILE]
                                   [--trigger-label TRIGGER_LABEL_VALUE]
                                   [--trigger-node2 TRIGGER_NODE2_VALUE]
                                   [--node1-role RDF_SUBJECT_LABEL_VALUE]
                                   [--label-role RDF_PREDICATE_LABEL_VALUE]
                                   [--node2-role RDF_OBJECT_LABEL_VALUE]
                                   [--allow-multiple-subjects [ALLOW_MULTIPLE_SUBJECTS]]
                                   [--allow-multiple-predicates [ALLOW_MULTIPLE_PREDICATES]]
                                   [--allow-multiple-objects [ALLOW_MULTIPLE_OBJECTS]] [-v]

Read a KGTK file, such as might have been created by importing an ntriples file.  Search for reified RFD statements and transform them into an unreified form.

An ID column will be added to the output file if not present in the input file.  

--reified-file PATH, if specified, will get a copy of the input records that were identified as reified RDF statements. 

--uninvolved-file PATH, if specified, will get a copy of the input records that were  identified as not being reified RDF statements. 

--unreified-file PATH, if specified, will get a copy of the unreified output records, which  will still be written to the main output file.

Additional options are shown in expert help.
kgtk --expert expand --help

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_KGTK_FILE, --input-file INPUT_KGTK_FILE
                        The KGTK input file with the reified data. (default=-)
  -o OUTPUT_KGTK_FILE, --output-file OUTPUT_KGTK_FILE
                        The KGTK file to write (default=-).
  --reified-file REIFIED_KGTK_FILE
                        A KGTK output file that will contain only the reified RDF
                        statements. (default=None).
  --unreified-file UNREIFIED_KGTK_FILE
                        A KGTK output file that will contain only the unreified RDF
                        statements. (default=None).
  --uninvolved-file UNINVOLVED_KGTK_FILE
                        A KGTK output file that will contain only the uninvolved input
                        records. (default=None).
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
  --allow-multiple-subjects [ALLOW_MULTIPLE_SUBJECTS]
                        When true, allow multiple subjects, resulting in a cartesian
                        product. (default=True).
  --allow-multiple-predicates [ALLOW_MULTIPLE_PREDICATES]
                        When true, allow multiple predicates, resulting in a cartesian
                        product. (default=True).
  --allow-multiple-objects [ALLOW_MULTIPLE_OBJECTS]
                        When true, allow multiple objects, resulting in a cartesian product.
                        (default=True).

  -v, --verbose         Print additional progress messages (default=False).
```

### Files

#### Input File

The input file is a KGTK file containing reified RDF data (among other
records), such as might have been imported from an ntriples file (see
`kgtk import_ntriples`).

```
| node1 | label | node2 |
| -- | -- | -- |
| XJAABmv8vGfJZZasjV6DAXY:g3 | rdf:type | rdf:Statement |
| XJAABmv8vGfJZZasjV6DAXY:g3 | rdf:object | gaia:entities/d1dcefce-badf-4948-bfcf-5d33116fa12c |
| XJAABmv8vGfJZZasjV6DAXY:g3 | rdf:predicate | nJAABmv8vGfJZZasjV6DAXY-3:Physical.LocatedNear_Place |
| XJAABmv8vGfJZZasjV6DAXY:g3 | rdf:subject | gaia:relations/d3e1e4df-6c8c-4fd1-8b93-ee49ef238f72 |
| XJAABmv8vGfJZZasjV6DAXY:g3 | ont:confidence | XJAABmv8vGfJZZasjV6DAXY:g4 |
| XJAABmv8vGfJZZasjV6DAXY:g3 | ont:justifiedBy | XJAABmv8vGfJZZasjV6DAXY:g5 |
| XJAABmv8vGfJZZasjV6DAXY:g3 | ont:system | nJAABmv8vGfJZZasjV6DAXY-1: |


```

#### Output File

The output file contains the KGTK data from the input file, with reified RDF statements
and associated edges replaced with an unreified RDF edge and secondary edges.

```
| node1 | label | node2 | id |
| -- | -- | -- | -- |
| gaia:relations/d3e1e4df-6c8c-4fd1-8b93-ee49ef238f72 | nJAABmv8vGfJZZasjV6DAXY-3:Physical.LocatedNear_Place | gaia:entities/d1dcefce-badf-4948-bfcf-5d33116fa12c |
 XJAABmv8vGfJZZasjV6DAXY:g3 |
| XJAABmv8vGfJZZasjV6DAXY:g3 | ont:confidence | XJAABmv8vGfJZZasjV6DAXY:g4 | XJAABmv8vGfJZZasjV6DAXY:g3-1 |
| XJAABmv8vGfJZZasjV6DAXY:g3 | ont:justifiedBy | XJAABmv8vGfJZZasjV6DAXY:g5 | XJAABmv8vGfJZZasjV6DAXY:g3-2 |
| XJAABmv8vGfJZZasjV6DAXY:g3 | ont:system | nJAABmv8vGfJZZasjV6DAXY-1: | XJAABmv8vGfJZZasjV6DAXY:g3-3 |

```

A `ID` column is added to the output file if it is not present in the input file.
This is used to link secondary edges to the newly reconstituted unreified edge.

At the present time, `kgtk unreify_rf_statements` does not generate ID values for
other edges in the file. This feature may be added in the future.

The edges in the output file are not likely to be in the same order as they appeared
in the input file.  If you wish to compare the input to the output files, read the
section below on Difference Comparison.

#### Reified File

This optional file will receive a copy of just the input data records that matched the
reified RDF statement pattern.  The records are the same as they were in the input
file, e.g., an ID column might not be present.

#### Unreified File

This optional file will receive a copy of just the output records that were generated
by by unreifying RDF statements in the input file.  The records in this file will be in
the output file's format, e.g., an dID column will be present.

#### Uninvolved File

This optional file will receive a copy of the input data recordsa that did not
match the reified RDF statement pattern.  The records are the same as they were in the input
file, e.g., an ID column might not be present.

### Pattern Match Parameters

`kgtk unreify_rdf_statements` has a built-in set of pattern match parameters that
will not change for normal operation.  All pattern matches reference the usual
node1, label, and node2 columns or their aliases; there are no options to
override the column names.

The Difference Comparison section, below, describes on use case in which overriding
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

`kgtk unreify_rdf_statements` processes multiple subject, predicates, and/or
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

## Broken Edges

Unless a Cartesian Crossproduct is being generated, `kgtk unreify_rdf_statements`
uses the node1 value of an input reified RDF statement ("XJAABmv8vGfJZZasjV6DAXY:g3")
as the edge ID of the output unreified RDF edge record, and as the node1 value of the
secondary edges. If for some reason there are other edges that refer to
this symbol ("XJAABmv8vGfJZZasjV6DAXY:g3") in the label or node2 columns, or in
extra columns, they will retain linkage to the unreified edges.

If a Cartesian Crossproduct is being generated, then the node1 value of the input reified
RDF statement as the base for the ID and node1 values used in the generated edges:

XJAABmv8vGfJZZasjV6DAXY:g3-1
XJAABmv8vGfJZZasjV6DAXY:g3-2
...

The width of the suffix is adjusted for the number of crossproduct edges being generated,
i.e. if more than 9 edges were being generated, they would use these ID and node1 values:

XJAABmv8vGfJZZasjV6DAXY:g3-01
XJAABmv8vGfJZZasjV6DAXY:g3-02
...
XJAABmv8vGfJZZasjV6DAXY:g3-10
...

These generated edge/node1 values are designed to keep the generated reified
edges and secondary edges in proximity when sorted by ID, whether Cartesian Crossproducts
are being generated or not.  However, when Cartesian Crossproducts are being generated,
then the new ID and node1 values cannot be as easily linked to esternal nodes referencing them.

## Difference Comparison

`kgtk unreify_rdf_statements` sorts its input data as part of detecting
reified RDF statements. Thus, attempting to look for changes between the input
file and the output file using an ordinary difference utility is not likely to
be fruitful.  Instead, employ the following strategy:

 * add an ID column to the input data if it does not already have one, using `kgtk add_id`
   * Perhaps without generating ID values, to remove clutter.
   * kgtk add_id --id-style=empty`
 * sort the resulting data using `kgtk unreify_rdf_statements` with a disabled pattern match parameter.
   * `kgtk unreify_rdf_statements --trigger-label=XXX -o output1.tsv`
 * Apply `kgtk unreify_rdf_statements` a second time without disabling the pattern match.
   * `kgtk unreify_rdf_statements -o output2.tsv`
 * Compare the two output files.

## Examples

```
kgtk unreify_rdf_statements -i HC00001DO.tsv -o HC00001DO-unreified-statements.tsv
```
