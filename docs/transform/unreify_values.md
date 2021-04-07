## Summary

`kgtk unreify-values` simplifies data while copying a KGTK file from
input to output, by removing extra nodes caused by RDF value reification. This
type of reification happens when there is a desire to model contextual or
complementary information about a value. A new object is created to hold the
value and additional properties are defined in the new object.


Input Table:

| node1 | label | node2 |
| ----- | ----- | ----- |
| XJAABmv8vGfJZZasjV6DAXY:g1 | rdf:type | ont:ClusterMembership |
| XJAABmv8vGfJZZasjV6DAXY:g1 | ont:cluster | gaia:events/03a41b2b-e0ef-42f9-a192-433e0abc3a70-cluster-projectedFromSingleton |
| XJAABmv8vGfJZZasjV6DAXY:g1 | ont:clusterMember | gaia:events/03a41b2b-e0ef-42f9-a192-433e0abc3a70 |
| XJAABmv8vGfJZZasjV6DAXY:g1 | ont:confidence | XJAABmv8vGfJZZasjV6DAXY:g2 |
| XJAABmv8vGfJZZasjV6DAXY:g2 | rdf:type | ont:Confidence |
| XJAABmv8vGfJZZasjV6DAXY:g2 | ont:confidenceValue | 1.0 |
| XJAABmv8vGfJZZasjV6DAXY:g2 | ont:system | nJAABmv8vGfJZZasjV6DAXY-2: |
| XJAABmv8vGfJZZasjV6DAXY:g1 | ont:system | nJAABmv8vGfJZZasjV6DAXY-2: |

The output of `kgtk unreify-values` is below. The unified table is easier to
understand once the spurious undesired object has been deleted, and its
label/node2 pairs defined as edges on the simplified edge.

Output Table:

| node1 | label | node2 | id |
| ----- | ----- | ----- | -- |
| XJAABmv8vGfJZZasjV6DAXY:g1 | rdf:type | ont:ClusterMembership |  |
| XJAABmv8vGfJZZasjV6DAXY:g1 | ont:cluster | gaia:events/03a41b2b-e0ef-42f9-a192-433e0abc3a70-cluster-projectedFromSingleton |  |
| XJAABmv8vGfJZZasjV6DAXY:g1 | ont:clusterMember | gaia:events/03a41b2b-e0ef-42f9-a192-433e0abc3a70 |  |
| XJAABmv8vGfJZZasjV6DAXY:g1 | ont:system | nJAABmv8vGfJZZasjV6DAXY-2: |  |
| XJAABmv8vGfJZZasjV6DAXY:g1 | ont:confidenceValue | 1.0 | XJAABmv8vGfJZZasjV6DAXY:g2 |
| XJAABmv8vGfJZZasjV6DAXY:g2 | ont:system | nJAABmv8vGfJZZasjV6DAXY-2: | XJAABmv8vGfJZZasjV6DAXY:g2-1 |


### Files

#### Input File

The input file is a KGTK file containing reified RDF data (among other
records), such as might have been imported from an ntriples file (see
`kgtk import_ntriples`).

| node1 | label | node2 |
| -- | -- | -- |
| XJAABmv8vGfJZZasjV6DAXY:g1 | rdf:type | ont:ClusterMembership |
| XJAABmv8vGfJZZasjV6DAXY:g1 | ont:cluster | gaia:events/03a41b2b-e0ef-42f9-a192-433e0abc3a70-cluster-projectedFromSingleton |
| XJAABmv8vGfJZZasjV6DAXY:g1 | ont:clusterMember | gaia:events/03a41b2b-e0ef-42f9-a192-433e0abc3a70 |
| XJAABmv8vGfJZZasjV6DAXY:g1 | ont:confidence | XJAABmv8vGfJZZasjV6DAXY:g2 |
| XJAABmv8vGfJZZasjV6DAXY:g2 | rdf:type | ont:Confidence |
| XJAABmv8vGfJZZasjV6DAXY:g2 | ont:confidenceValue | 1.0 |
| XJAABmv8vGfJZZasjV6DAXY:g2 | ont:system | nJAABmv8vGfJZZasjV6DAXY-2: |
| XJAABmv8vGfJZZasjV6DAXY:g1 | ont:system | nJAABmv8vGfJZZasjV6DAXY-2: |

#### Output File

The output file contains the KGTK data from the input file, with reified RDF statements
and associated edges replaced with an unreified RDF edge and secondary edges.

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | rdf:type | ont:ClusterMembership |  |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:cluster | gaia:events/03a41b2b-e0ef-42f9-a192-433e0abc3a70-cluster-projectedFromSingleton |  |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:clusterMember | gaia:events/03a41b2b-e0ef-42f9-a192-433e0abc3a70 |  |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:system | noBugQcoEt6xNnqGsHDXfTA-2: |  |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:confidenceValue | 1.0 | XoBugQcoEt6xNnqGsHDXfTA:g2 |
| XoBugQcoEt6xNnqGsHDXfTA:g2 | ont:system | noBugQcoEt6xNnqGsHDXfTA-2: | XoBugQcoEt6xNnqGsHDXfTA:g2-1 |


A `ID` column is added to the output file if it is not present in the input file.
This is used to link secondary edges to the newly reconstituted unreified edge.

At the present time, `kgtk unreify-rf_statements` does not generate ID values for
other edges in the file. This feature may be added in the future.

The edges in the output file are not likely to be in the same order as they appeared
in the input file.  If you wish to compare the input to the output files, read the
section below on Difference Comparison.

#### Reified File

This optional file will receive a copy of just the input data records that matched the
reified RDF value pattern.  The records are the same as they were in the input
file, e.g., an ID column might not be present.

#### Unreified File

This optional file will receive a copy of just the output records that were generated
by by unreifying RDF values in the input file.  The records in this file will be in
the output file's format, e.g., an dID column will be present.

#### Uninvolved File

This optional file will receive a copy of the input data recordsa that did not
match the reified RDF value pattern.  The records are the same as they were in the input
file, e.g., an ID column might not be present.

### Pattern Match Parameters

`kgtk unreify-values` does not have a built-in set of pattern match parameters;
the user must supply the following values.  All pattern matches reference the usual
node1, label, and node2 columns or their aliases; there are no options to
override the column names.

The Difference Comparison section, below, describes on use case in which supplying
non-matching pattern match parameters can be beneficial for other uses.

```
  --trigger-label TRIGGER_LABEL_VALUE
                        A value in the label (or its alias) column that identifies the
                        trigger record. (default=None).
  --trigger-node2 TRIGGER_NODE2_VALUE
                        A value in the node2 (or its alias) column that identifies the
                        trigger record. This is a required parameter for which there is
                        no default value. (default=None).
  --value-label VALUE_LABEL_VALUE
                        A value in the label (or its alias) column that identifies the
                        record with the node2 value for the new, unreified edge. This
                        is a required parameter for which there is no default value.
                        (default=None).
  --old-label OLD_LABEL_VALUE
                        A value in the label (or its alias) column that identifies the
                        edge with the node1 value being unreified. The value in the
                        node1 (or its alias) column of this record will be used in the
                        node1 (or its alias) column for the new, unreified edge. This
                        is a required parameter for which there is no default value.
                        (default=None).
  --new-label NEW_LABEL_VALUE
                        The value to be entered in the label (or its alias) column of
                        the new, unreified edge. If not specified (None), the value
                        from --value-label is used. (default=None).
```

For the examples shown above, the following pattern match values were used:

```
--trigger-label rdf:type
--trigger-node2 ont:Confidence
--value-label ont:confidenceValue
--old-label ont:confidence
```

### Multiple Values

`kgtk unreify-values` optionally accepts multiple values from records with the label
field having the ``--value-label` value, forming a vertical bar (pipe) (|) separated
list.

When processing of multiple subjects, predicates, or objects has been disabled,
and multiple subjects, predicates, or objects are encountered in the input
stream, a warning message will be issued (if `--verbose` output is enabled)
and the group of input data will not be unreified.

```
  --allow-multiple-values [ALLOW_MULTIPLE_VALUES]
                        When true, allow multiple values (a '|' list) in the node2 (or
                        its alias) column of the new, unreified edge. (default=False).
```

For example, if the input file looked like this:

| node1 | label | node2 |
| -- | -- | -- |
| XJAABmv8vGfJZZasjV6DAXY:g1 | rdf:type | ont:ClusterMembership |
| XJAABmv8vGfJZZasjV6DAXY:g1 | ont:cluster | gaia:events/03a41b2b-e0ef-42f9-a192-433e0abc3a70-cluster-projectedFromSingleton |
| XJAABmv8vGfJZZasjV6DAXY:g1 | ont:clusterMember | gaia:events/03a41b2b-e0ef-42f9-a192-433e0abc3a70 |
| XJAABmv8vGfJZZasjV6DAXY:g1 | ont:confidence | XJAABmv8vGfJZZasjV6DAXY:g2 |
| XJAABmv8vGfJZZasjV6DAXY:g2 | rdf:type | ont:Confidence |
| XJAABmv8vGfJZZasjV6DAXY:g2 | ont:confidenceValue | 1.0 |
| XJAABmv8vGfJZZasjV6DAXY:g2 | ont:confidenceValue | 2.0 |
| XJAABmv8vGfJZZasjV6DAXY:g2 | ont:system | nJAABmv8vGfJZZasjV6DAXY-2: |
| XJAABmv8vGfJZZasjV6DAXY:g1 | ont:system | nJAABmv8vGfJZZasjV6DAXY-2: |

With `--allow-multiple-values` in its default setting (`False`), unreification
will not take place, and the output will look like this:

| node1 | label | node2 |
| -- | -- | -- |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | rdf:type | ont:ClusterMembership |  |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:cluster | gaia:events/03a41b2b-e0ef-42f9-a192-433e0abc3a70-cluster-projectedFromSingleton |  |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:clusterMember | gaia:events/03a41b2b-e0ef-42f9-a192-433e0abc3a70 |  |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:system | noBugQcoEt6xNnqGsHDXfTA-2: |  |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:confidence | XoBugQcoEt6xNnqGsHDXfTA:g2 |  |
| XoBugQcoEt6xNnqGsHDXfTA:g2 | rdf:type | ont:Confidence |  |
| XoBugQcoEt6xNnqGsHDXfTA:g2 | ont:confidenceValue | 1.0 |  |
| XoBugQcoEt6xNnqGsHDXfTA:g2 | ont:confidenceValue | 2.0 |  |
| XoBugQcoEt6xNnqGsHDXfTA:g2 | ont:system | noBugQcoEt6xNnqGsHDXfTA-2: |  |

With `--allow-multiple-values` is asserted (`True`), unreification will take
place and the output will look like this:

| node1 | label | node2 |
| -- | -- | -- |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | rdf:type | ont:ClusterMembership |  |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:cluster | gaia:events/03a41b2b-e0ef-42f9-a192-433e0abc3a70-cluster-projectedFromSingleton |  |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:clusterMember | gaia:events/03a41b2b-e0ef-42f9-a192-433e0abc3a70 |  |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:system | noBugQcoEt6xNnqGsHDXfTA-2: |  |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:confidenceValue | 1.0\|2.0 | XoBugQcoEt6xNnqGsHDXfTA:g2 |
| XoBugQcoEt6xNnqGsHDXfTA:g2 | ont:system | noBugQcoEt6xNnqGsHDXfTA-2: | XoBugQcoEt6xNnqGsHDXfTA:g2-1 |

### Difference Comparison

`kgtk unreify-values` sorts its input data as part of detecting reified RDF
values. Thus, attempting to look for changes between the input file and the
output file using an ordinary difference utility is not likely to be fruitful.
Instead, employ the following strategy:

 * add an ID column to the input data if it does not already have one, using `kgtk add_id`
   * Perhaps without generating ID values, to remove clutter.
   * kgtk add_id --id-style=empty`
 * sort the resulting data using `kgtk unreify-values` with invalid pattern match parameters:
   * `kgtk unreify-values --trigger-label=XXX --trigger-node2=XXX --value-label=XXX --old-label=XXX -o output1.tsv`
 * Apply `kgtk unreify-values` a second time with the desired pattern match parameters.
   * `kgtk unreify-values --trigger-label rdf:type --trigger-node2 ont:Confidence --value-label ont:confidenceValue --old-label ont:confidence-o output2.tsv`
 * Compare the two output files.

## Usage

```
usage: kgtk unreify-values [-h] [-i INPUT_FILE] [-o OUTPUT_FILE]
                           [--reified-file REIFIED_FILE]
                           [--unreified-file UNREIFIED_FILE]
                           [--uninvolved-file UNINVOLVED_FILE] --trigger-label
                           TRIGGER_LABEL_VALUE --trigger-node2
                           TRIGGER_NODE2_VALUE --value-label VALUE_LABEL_VALUE
                           --old-label OLD_LABEL_VALUE
                           [--new-label NEW_LABEL_VALUE]
                           [--allow-multiple-values [ALLOW_MULTIPLE_VALUES]]
                           [--allow-extra-columns [ALLOW_EXTRA_COLUMNS]]
                           [-v [optional True|False]]

Read a KGTK file, such as might have been created by importing an ntriples file.  Search for reified values and transform them into an unreified form.

An ID column will be added to the output file if not present in the input file.  

--reified-file PATH, if specified, will get a copy of the input records that were identified as reified values. 

--uninvolved-file PATH, if specified, will get a copy of the input records that were  identified as not being reified values. 

--unreified-file PATH, if specified, will get a copy of the unreified output records, which  will still be written to the main output file.

Additional options are shown in expert help.
kgtk --expert unreify-values --help

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK input file with the reified data. It must
                        have node1, label, and node2 columns, or their
                        aliases. It may have an ID column; if it does not, one
                        will be appended to the output file. It may not have
                        any additional columns. (May be omitted or '-' for
                        stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK file to write output records with unreified
                        data. This file may differ in shape from the input
                        file by the addition of an ID column. The records in
                        the output file will not, generally, be in the same
                        order as they appeared in the input file. (May be
                        omitted or '-' for stdout.)
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
                        A value in the label (or its alias) column that
                        identifies the trigger record. (default=None).
  --trigger-node2 TRIGGER_NODE2_VALUE
                        A value in the node2 (or its alias) column that
                        identifies the trigger record. This is a required
                        parameter for which there is no default value.
                        (default=None).
  --value-label VALUE_LABEL_VALUE
                        A value in the label (or its alias) column that
                        identifies the record with the node2 value for the
                        new, unreified edge. This is a required parameter for
                        which there is no default value. (default=None).
  --old-label OLD_LABEL_VALUE
                        A value in the label (or its alias) column that
                        identifies the edge with the node1 value being
                        unreified. The value in the node1 (or its alias)
                        column of this record will be used in the node1 (or
                        its alias) column for the new, unreified edge. This is
                        a required parameter for which there is no default
                        value. (default=None).
  --new-label NEW_LABEL_VALUE
                        The value to be entered in the label (or its alias)
                        column of the new, unreified edge. If not specified
                        (None), the value from --value-label is used.
                        (default=None).
  --allow-multiple-values [ALLOW_MULTIPLE_VALUES]
                        When true, allow multiple values (a '|' list) in the
                        node2 (or its alias) column of the new, unreified
                        edge. (default=False).
  --allow-extra-columns [ALLOW_EXTRA_COLUMNS]
                        When true, allow extra columns (beyond node1, label,
                        node2, and id, or their aliases. Warning: the contents
                        of these columns may be lost silently in unreified
                        statements. (default=False).

  -v [optional True|False], --verbose [optional True|False]
                        Print additional progress messages (default=False).
```

## Examples

### Example 1

```bash
kgtk cat -i examples/docs/unreify-values-file4.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| XJAABmv8vGfJZZasjV6DAXY:g1 | rdf:type | ont:ClusterMembership |
| XJAABmv8vGfJZZasjV6DAXY:g1 | ont:cluster | gaia:events/03a41b2b-e0ef-42f9-a192-433e0abc3a70-cluster-projectedFromSingleton |
| XJAABmv8vGfJZZasjV6DAXY:g1 | ont:clusterMember | gaia:events/03a41b2b-e0ef-42f9-a192-433e0abc3a70 |
| XJAABmv8vGfJZZasjV6DAXY:g1 | ont:confidence | XJAABmv8vGfJZZasjV6DAXY:g2 |
| XJAABmv8vGfJZZasjV6DAXY:g2 | rdf:type | ont:Confidence |
| XJAABmv8vGfJZZasjV6DAXY:g2 | ont:confidenceValue | 1.0 |
| XJAABmv8vGfJZZasjV6DAXY:g2 | ont:system | nJAABmv8vGfJZZasjV6DAXY-2: |
| XJAABmv8vGfJZZasjV6DAXY:g1 | ont:system | nJAABmv8vGfJZZasjV6DAXY-2: |

```bash
kgtk unreify-values -i examples/docs/unreify-values-file4.tsv \
		    --trigger-label rdf:type \
		    --trigger-node2 ont:Confidence \
		    --value-label ont:confidenceValue \
		    --old-label ont:confidence
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| XJAABmv8vGfJZZasjV6DAXY:g1 | rdf:type | ont:ClusterMembership |  |
| XJAABmv8vGfJZZasjV6DAXY:g1 | ont:cluster | gaia:events/03a41b2b-e0ef-42f9-a192-433e0abc3a70-cluster-projectedFromSingleton |  |
| XJAABmv8vGfJZZasjV6DAXY:g1 | ont:clusterMember | gaia:events/03a41b2b-e0ef-42f9-a192-433e0abc3a70 |  |
| XJAABmv8vGfJZZasjV6DAXY:g1 | ont:system | nJAABmv8vGfJZZasjV6DAXY-2: |  |
| XJAABmv8vGfJZZasjV6DAXY:g1 | ont:confidenceValue | 1.0 | XJAABmv8vGfJZZasjV6DAXY:g2 |
| XJAABmv8vGfJZZasjV6DAXY:g2 | ont:system | nJAABmv8vGfJZZasjV6DAXY-2: | XJAABmv8vGfJZZasjV6DAXY:g2-1 |

### Unreifying ont:Confidence

```bash
kgtk cat -i examples/docs/unreify-values-file1.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | rdf:type | ont:Entity |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:informativeJustification | XoBugQcoEt6xNnqGsHDXfTA:b0 |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:justifiedBy | XoBugQcoEt6xNnqGsHDXfTA:b1 |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:privateData | XoBugQcoEt6xNnqGsHDXfTA:g0 |
| XoBugQcoEt6xNnqGsHDXfTA:g0 | rdf:type | ont:PrivateData |
| XoBugQcoEt6xNnqGsHDXfTA:g0 | ont:jsonContent | "{\"fileType\":\"en\"}" |
| XoBugQcoEt6xNnqGsHDXfTA:g0 | ont:system | rpi:fileType |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:system | noBugQcoEt6xNnqGsHDXfTA-1: |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:textValue | "32" |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | rdf:type | ont:ClusterMembership |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:cluster | gaia:events/03a41b2b-e0ef-42f9-a192-433e0abc3a70-cluster-projectedFromSingleton |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:clusterMember | gaia:events/03a41b2b-e0ef-42f9-a192-433e0abc3a70 |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:confidence | XoBugQcoEt6xNnqGsHDXfTA:g2 |
| XoBugQcoEt6xNnqGsHDXfTA:g2 | rdf:type | ont:Confidence |
| XoBugQcoEt6xNnqGsHDXfTA:g2 | ont:confidenceValue | 1.0 |
| XoBugQcoEt6xNnqGsHDXfTA:g2 | ont:system | noBugQcoEt6xNnqGsHDXfTA-2: |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:system | noBugQcoEt6xNnqGsHDXfTA-2: |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | rdf:type | rdf:Statement |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | rdf:object | gaia:entities/d1dcefce-badf-4948-bfcf-5d33116fa12c |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | rdf:predicate | noBugQcoEt6xNnqGsHDXfTA-3:Physical.LocatedNear_Place |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | rdf:subject | gaia:relations/d3e1e4df-6c8c-4fd1-8b93-ee49ef238f72 |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | ont:confidence | XoBugQcoEt6xNnqGsHDXfTA:g4 |
| XoBugQcoEt6xNnqGsHDXfTA:g4 | rdf:type | ont:Confidence |
| XoBugQcoEt6xNnqGsHDXfTA:g4 | ont:confidenceValue | 9.9e-01 |
| XoBugQcoEt6xNnqGsHDXfTA:g4 | ont:system | noBugQcoEt6xNnqGsHDXfTA-1: |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | ont:justifiedBy | XoBugQcoEt6xNnqGsHDXfTA:g5 |
| XoBugQcoEt6xNnqGsHDXfTA:g5 | rdf:type | ont:CompoundJustification |
| XoBugQcoEt6xNnqGsHDXfTA:g5 | ont:confidence | XoBugQcoEt6xNnqGsHDXfTA:g6 |
| XoBugQcoEt6xNnqGsHDXfTA:g6 | rdf:type | ont:Confidence |
| XoBugQcoEt6xNnqGsHDXfTA:g6 | ont:confidenceValue | 0.99 |
| XoBugQcoEt6xNnqGsHDXfTA:g6 | ont:system | noBugQcoEt6xNnqGsHDXfTA-4:compoundJustificationWrapper |
| XoBugQcoEt6xNnqGsHDXfTA:g5 | ont:containedJustification | XoBugQcoEt6xNnqGsHDXfTA:g7 |


```
kgtk unreify-values -i examples/docs/unreify-values-file1.tsv \
		    --trigger-label rdf:type \
		    --trigger-node2 ont:Confidence \
		    --value-label ont:confidenceValue \
		    --old-label ont:confidence
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| XoBugQcoEt6xNnqGsHDXfTA:g0 | rdf:type | ont:PrivateData |  |
| XoBugQcoEt6xNnqGsHDXfTA:g0 | ont:jsonContent | "{\"fileType\":\"en\"}" |  |
| XoBugQcoEt6xNnqGsHDXfTA:g0 | ont:system | rpi:fileType |  |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | rdf:type | ont:ClusterMembership |  |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:cluster | gaia:events/03a41b2b-e0ef-42f9-a192-433e0abc3a70-cluster-projectedFromSingleton |  |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:clusterMember | gaia:events/03a41b2b-e0ef-42f9-a192-433e0abc3a70 |  |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:system | noBugQcoEt6xNnqGsHDXfTA-2: |  |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:confidenceValue | 1.0 | XoBugQcoEt6xNnqGsHDXfTA:g2 |
| XoBugQcoEt6xNnqGsHDXfTA:g2 | ont:system | noBugQcoEt6xNnqGsHDXfTA-2: | XoBugQcoEt6xNnqGsHDXfTA:g2-1 |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | rdf:type | rdf:Statement |  |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | rdf:object | gaia:entities/d1dcefce-badf-4948-bfcf-5d33116fa12c |  |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | rdf:predicate | noBugQcoEt6xNnqGsHDXfTA-3:Physical.LocatedNear_Place |  |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | rdf:subject | gaia:relations/d3e1e4df-6c8c-4fd1-8b93-ee49ef238f72 |  |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | ont:justifiedBy | XoBugQcoEt6xNnqGsHDXfTA:g5 |  |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | ont:confidenceValue | 9.9e-01 | XoBugQcoEt6xNnqGsHDXfTA:g4 |
| XoBugQcoEt6xNnqGsHDXfTA:g4 | ont:system | noBugQcoEt6xNnqGsHDXfTA-1: | XoBugQcoEt6xNnqGsHDXfTA:g4-1 |
| XoBugQcoEt6xNnqGsHDXfTA:g5 | rdf:type | ont:CompoundJustification |  |
| XoBugQcoEt6xNnqGsHDXfTA:g5 | ont:containedJustification | XoBugQcoEt6xNnqGsHDXfTA:g7 |  |
| XoBugQcoEt6xNnqGsHDXfTA:g5 | ont:confidenceValue | 0.99 | XoBugQcoEt6xNnqGsHDXfTA:g6 |
| XoBugQcoEt6xNnqGsHDXfTA:g6 | ont:system | noBugQcoEt6xNnqGsHDXfTA-4:compoundJustificationWrapper | XoBugQcoEt6xNnqGsHDXfTA:g6-1 |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | rdf:type | ont:Entity |  |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:informativeJustification | XoBugQcoEt6xNnqGsHDXfTA:b0 |  |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:justifiedBy | XoBugQcoEt6xNnqGsHDXfTA:b1 |  |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:privateData | XoBugQcoEt6xNnqGsHDXfTA:g0 |  |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:system | noBugQcoEt6xNnqGsHDXfTA-1: |  |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:textValue | "32" |  |

### Unreifying ont:PrivateData:

```bash
kgtk cat -i examples/docs/unreify-values-file1.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | rdf:type | ont:Entity |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:informativeJustification | XoBugQcoEt6xNnqGsHDXfTA:b0 |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:justifiedBy | XoBugQcoEt6xNnqGsHDXfTA:b1 |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:privateData | XoBugQcoEt6xNnqGsHDXfTA:g0 |
| XoBugQcoEt6xNnqGsHDXfTA:g0 | rdf:type | ont:PrivateData |
| XoBugQcoEt6xNnqGsHDXfTA:g0 | ont:jsonContent | "{\"fileType\":\"en\"}" |
| XoBugQcoEt6xNnqGsHDXfTA:g0 | ont:system | rpi:fileType |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:system | noBugQcoEt6xNnqGsHDXfTA-1: |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:textValue | "32" |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | rdf:type | ont:ClusterMembership |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:cluster | gaia:events/03a41b2b-e0ef-42f9-a192-433e0abc3a70-cluster-projectedFromSingleton |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:clusterMember | gaia:events/03a41b2b-e0ef-42f9-a192-433e0abc3a70 |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:confidence | XoBugQcoEt6xNnqGsHDXfTA:g2 |
| XoBugQcoEt6xNnqGsHDXfTA:g2 | rdf:type | ont:Confidence |
| XoBugQcoEt6xNnqGsHDXfTA:g2 | ont:confidenceValue | 1.0 |
| XoBugQcoEt6xNnqGsHDXfTA:g2 | ont:system | noBugQcoEt6xNnqGsHDXfTA-2: |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:system | noBugQcoEt6xNnqGsHDXfTA-2: |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | rdf:type | rdf:Statement |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | rdf:object | gaia:entities/d1dcefce-badf-4948-bfcf-5d33116fa12c |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | rdf:predicate | noBugQcoEt6xNnqGsHDXfTA-3:Physical.LocatedNear_Place |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | rdf:subject | gaia:relations/d3e1e4df-6c8c-4fd1-8b93-ee49ef238f72 |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | ont:confidence | XoBugQcoEt6xNnqGsHDXfTA:g4 |
| XoBugQcoEt6xNnqGsHDXfTA:g4 | rdf:type | ont:Confidence |
| XoBugQcoEt6xNnqGsHDXfTA:g4 | ont:confidenceValue | 9.9e-01 |
| XoBugQcoEt6xNnqGsHDXfTA:g4 | ont:system | noBugQcoEt6xNnqGsHDXfTA-1: |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | ont:justifiedBy | XoBugQcoEt6xNnqGsHDXfTA:g5 |
| XoBugQcoEt6xNnqGsHDXfTA:g5 | rdf:type | ont:CompoundJustification |
| XoBugQcoEt6xNnqGsHDXfTA:g5 | ont:confidence | XoBugQcoEt6xNnqGsHDXfTA:g6 |
| XoBugQcoEt6xNnqGsHDXfTA:g6 | rdf:type | ont:Confidence |
| XoBugQcoEt6xNnqGsHDXfTA:g6 | ont:confidenceValue | 0.99 |
| XoBugQcoEt6xNnqGsHDXfTA:g6 | ont:system | noBugQcoEt6xNnqGsHDXfTA-4:compoundJustificationWrapper |
| XoBugQcoEt6xNnqGsHDXfTA:g5 | ont:containedJustification | XoBugQcoEt6xNnqGsHDXfTA:g7 |

```
kgtk unreify-values -i examples/docs/unreify-values-file1.tsv \
		    --trigger-label rdf:type \
		    --trigger-node2 ont:PrivateData \
		    --value-label ont:jsonContent \
		    --old-label ont:privateData
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:jsonContent | "{\"fileType\":\"en\"}" | XoBugQcoEt6xNnqGsHDXfTA:g0 |
| XoBugQcoEt6xNnqGsHDXfTA:g0 | ont:system | rpi:fileType | XoBugQcoEt6xNnqGsHDXfTA:g0-1 |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | rdf:type | ont:ClusterMembership |  |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:cluster | gaia:events/03a41b2b-e0ef-42f9-a192-433e0abc3a70-cluster-projectedFromSingleton |  |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:clusterMember | gaia:events/03a41b2b-e0ef-42f9-a192-433e0abc3a70 |  |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:confidence | XoBugQcoEt6xNnqGsHDXfTA:g2 |  |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:system | noBugQcoEt6xNnqGsHDXfTA-2: |  |
| XoBugQcoEt6xNnqGsHDXfTA:g2 | rdf:type | ont:Confidence |  |
| XoBugQcoEt6xNnqGsHDXfTA:g2 | ont:confidenceValue | 1.0 |  |
| XoBugQcoEt6xNnqGsHDXfTA:g2 | ont:system | noBugQcoEt6xNnqGsHDXfTA-2: |  |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | rdf:type | rdf:Statement |  |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | rdf:object | gaia:entities/d1dcefce-badf-4948-bfcf-5d33116fa12c |  |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | rdf:predicate | noBugQcoEt6xNnqGsHDXfTA-3:Physical.LocatedNear_Place |  |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | rdf:subject | gaia:relations/d3e1e4df-6c8c-4fd1-8b93-ee49ef238f72 |  |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | ont:confidence | XoBugQcoEt6xNnqGsHDXfTA:g4 |  |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | ont:justifiedBy | XoBugQcoEt6xNnqGsHDXfTA:g5 |  |
| XoBugQcoEt6xNnqGsHDXfTA:g4 | rdf:type | ont:Confidence |  |
| XoBugQcoEt6xNnqGsHDXfTA:g4 | ont:confidenceValue | 9.9e-01 |  |
| XoBugQcoEt6xNnqGsHDXfTA:g4 | ont:system | noBugQcoEt6xNnqGsHDXfTA-1: |  |
| XoBugQcoEt6xNnqGsHDXfTA:g5 | rdf:type | ont:CompoundJustification |  |
| XoBugQcoEt6xNnqGsHDXfTA:g5 | ont:confidence | XoBugQcoEt6xNnqGsHDXfTA:g6 |  |
| XoBugQcoEt6xNnqGsHDXfTA:g5 | ont:containedJustification | XoBugQcoEt6xNnqGsHDXfTA:g7 |  |
| XoBugQcoEt6xNnqGsHDXfTA:g6 | rdf:type | ont:Confidence |  |
| XoBugQcoEt6xNnqGsHDXfTA:g6 | ont:confidenceValue | 0.99 |  |
| XoBugQcoEt6xNnqGsHDXfTA:g6 | ont:system | noBugQcoEt6xNnqGsHDXfTA-4:compoundJustificationWrapper |  |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | rdf:type | ont:Entity |  |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:informativeJustification | XoBugQcoEt6xNnqGsHDXfTA:b0 |  |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:justifiedBy | XoBugQcoEt6xNnqGsHDXfTA:b1 |  |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:system | noBugQcoEt6xNnqGsHDXfTA-1: |  |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:textValue | "32" |  |

### Chaining the two value unreifications
```bash
kgtk cat -i examples/docs/unreify-values-file1.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | rdf:type | ont:Entity |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:informativeJustification | XoBugQcoEt6xNnqGsHDXfTA:b0 |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:justifiedBy | XoBugQcoEt6xNnqGsHDXfTA:b1 |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:privateData | XoBugQcoEt6xNnqGsHDXfTA:g0 |
| XoBugQcoEt6xNnqGsHDXfTA:g0 | rdf:type | ont:PrivateData |
| XoBugQcoEt6xNnqGsHDXfTA:g0 | ont:jsonContent | "{\"fileType\":\"en\"}" |
| XoBugQcoEt6xNnqGsHDXfTA:g0 | ont:system | rpi:fileType |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:system | noBugQcoEt6xNnqGsHDXfTA-1: |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:textValue | "32" |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | rdf:type | ont:ClusterMembership |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:cluster | gaia:events/03a41b2b-e0ef-42f9-a192-433e0abc3a70-cluster-projectedFromSingleton |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:clusterMember | gaia:events/03a41b2b-e0ef-42f9-a192-433e0abc3a70 |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:confidence | XoBugQcoEt6xNnqGsHDXfTA:g2 |
| XoBugQcoEt6xNnqGsHDXfTA:g2 | rdf:type | ont:Confidence |
| XoBugQcoEt6xNnqGsHDXfTA:g2 | ont:confidenceValue | 1.0 |
| XoBugQcoEt6xNnqGsHDXfTA:g2 | ont:system | noBugQcoEt6xNnqGsHDXfTA-2: |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:system | noBugQcoEt6xNnqGsHDXfTA-2: |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | rdf:type | rdf:Statement |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | rdf:object | gaia:entities/d1dcefce-badf-4948-bfcf-5d33116fa12c |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | rdf:predicate | noBugQcoEt6xNnqGsHDXfTA-3:Physical.LocatedNear_Place |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | rdf:subject | gaia:relations/d3e1e4df-6c8c-4fd1-8b93-ee49ef238f72 |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | ont:confidence | XoBugQcoEt6xNnqGsHDXfTA:g4 |
| XoBugQcoEt6xNnqGsHDXfTA:g4 | rdf:type | ont:Confidence |
| XoBugQcoEt6xNnqGsHDXfTA:g4 | ont:confidenceValue | 9.9e-01 |
| XoBugQcoEt6xNnqGsHDXfTA:g4 | ont:system | noBugQcoEt6xNnqGsHDXfTA-1: |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | ont:justifiedBy | XoBugQcoEt6xNnqGsHDXfTA:g5 |
| XoBugQcoEt6xNnqGsHDXfTA:g5 | rdf:type | ont:CompoundJustification |
| XoBugQcoEt6xNnqGsHDXfTA:g5 | ont:confidence | XoBugQcoEt6xNnqGsHDXfTA:g6 |
| XoBugQcoEt6xNnqGsHDXfTA:g6 | rdf:type | ont:Confidence |
| XoBugQcoEt6xNnqGsHDXfTA:g6 | ont:confidenceValue | 0.99 |
| XoBugQcoEt6xNnqGsHDXfTA:g6 | ont:system | noBugQcoEt6xNnqGsHDXfTA-4:compoundJustificationWrapper |
| XoBugQcoEt6xNnqGsHDXfTA:g5 | ont:containedJustification | XoBugQcoEt6xNnqGsHDXfTA:g7 |

```
kgtk unreify-values -i examples/docs/unreify-values-file1.tsv \
                    --trigger-label rdf:type \
                    --trigger-node2 ont:Confidence \
                    --value-label ont:confidenceValue \
                    --old-label ont:confidence \
   / unreify-values \
                    --trigger-label rdf:type \
                    --trigger-node2 ont:PrivateData \
                    --value-label ont:jsonContent \
                    --old-label ont:privateData
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:jsonContent | "{\"fileType\":\"en\"}" | XoBugQcoEt6xNnqGsHDXfTA:g0 |
| XoBugQcoEt6xNnqGsHDXfTA:g0 | ont:system | rpi:fileType | XoBugQcoEt6xNnqGsHDXfTA:g0-1 |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | rdf:type | ont:ClusterMembership |  |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:cluster | gaia:events/03a41b2b-e0ef-42f9-a192-433e0abc3a70-cluster-projectedFromSingleton |  |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:clusterMember | gaia:events/03a41b2b-e0ef-42f9-a192-433e0abc3a70 |  |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:system | noBugQcoEt6xNnqGsHDXfTA-2: |  |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:confidenceValue | 1.0 | XoBugQcoEt6xNnqGsHDXfTA:g2 |
| XoBugQcoEt6xNnqGsHDXfTA:g2 | ont:system | noBugQcoEt6xNnqGsHDXfTA-2: | XoBugQcoEt6xNnqGsHDXfTA:g2-1 |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | rdf:type | rdf:Statement |  |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | rdf:object | gaia:entities/d1dcefce-badf-4948-bfcf-5d33116fa12c |  |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | rdf:predicate | noBugQcoEt6xNnqGsHDXfTA-3:Physical.LocatedNear_Place |  |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | rdf:subject | gaia:relations/d3e1e4df-6c8c-4fd1-8b93-ee49ef238f72 |  |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | ont:justifiedBy | XoBugQcoEt6xNnqGsHDXfTA:g5 |  |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | ont:confidenceValue | 9.9e-01 | XoBugQcoEt6xNnqGsHDXfTA:g4 |
| XoBugQcoEt6xNnqGsHDXfTA:g4 | ont:system | noBugQcoEt6xNnqGsHDXfTA-1: | XoBugQcoEt6xNnqGsHDXfTA:g4-1 |
| XoBugQcoEt6xNnqGsHDXfTA:g5 | rdf:type | ont:CompoundJustification |  |
| XoBugQcoEt6xNnqGsHDXfTA:g5 | ont:containedJustification | XoBugQcoEt6xNnqGsHDXfTA:g7 |  |
| XoBugQcoEt6xNnqGsHDXfTA:g5 | ont:confidenceValue | 0.99 | XoBugQcoEt6xNnqGsHDXfTA:g6 |
| XoBugQcoEt6xNnqGsHDXfTA:g6 | ont:system | noBugQcoEt6xNnqGsHDXfTA-4:compoundJustificationWrapper | XoBugQcoEt6xNnqGsHDXfTA:g6-1 |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | rdf:type | ont:Entity |  |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:informativeJustification | XoBugQcoEt6xNnqGsHDXfTA:b0 |  |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:justifiedBy | XoBugQcoEt6xNnqGsHDXfTA:b1 |  |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:system | noBugQcoEt6xNnqGsHDXfTA-1: |  |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:textValue | "32" |  |

### Unreifying with Extra Columns

```bash
kgtk cat -i examples/docs/unreify-values-file2.tsv
```

| node1 | label | node2 | record# |
| -- | -- | -- | -- |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | rdf:type | ont:Entity | 01 |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:informativeJustification | XoBugQcoEt6xNnqGsHDXfTA:b0 | 02 |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:justifiedBy | XoBugQcoEt6xNnqGsHDXfTA:b1 | 03 |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:privateData | XoBugQcoEt6xNnqGsHDXfTA:g0 | 04 |
| XoBugQcoEt6xNnqGsHDXfTA:g0 | rdf:type | ont:PrivateData | 05 |
| XoBugQcoEt6xNnqGsHDXfTA:g0 | ont:jsonContent | "{\"fileType\":\"en\"}" | 06 |
| XoBugQcoEt6xNnqGsHDXfTA:g0 | ont:system | rpi:fileType | 07 |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:system | noBugQcoEt6xNnqGsHDXfTA-1: | 08 |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:textValue | "32" | 09 |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | rdf:type | ont:ClusterMembership | 10 |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:cluster | gaia:events/03a41b2b-e0ef-42f9-a192-433e0abc3a70-cluster-projectedFromSingleton | 11 |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:clusterMember | gaia:events/03a41b2b-e0ef-42f9-a192-433e0abc3a70 | 12 |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:confidence | XoBugQcoEt6xNnqGsHDXfTA:g2 | 13 |
| XoBugQcoEt6xNnqGsHDXfTA:g2 | rdf:type | ont:Confidence | 14 |
| XoBugQcoEt6xNnqGsHDXfTA:g2 | ont:confidenceValue | 1.0 | 15 |
| XoBugQcoEt6xNnqGsHDXfTA:g2 | ont:system | noBugQcoEt6xNnqGsHDXfTA-2: | 16 |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:system | noBugQcoEt6xNnqGsHDXfTA-2: | 17 |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | rdf:type | rdf:Statement | 18 |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | rdf:object | gaia:entities/d1dcefce-badf-4948-bfcf-5d33116fa12c | 19 |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | rdf:predicate | noBugQcoEt6xNnqGsHDXfTA-3:Physical.LocatedNear_Place | 20 |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | rdf:subject | gaia:relations/d3e1e4df-6c8c-4fd1-8b93-ee49ef238f72 | 21 |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | ont:confidence | XoBugQcoEt6xNnqGsHDXfTA:g4 | 22 |
| XoBugQcoEt6xNnqGsHDXfTA:g4 | rdf:type | ont:Confidence | 23 |
| XoBugQcoEt6xNnqGsHDXfTA:g4 | ont:confidenceValue | 9.9e-01 | 24 |
| XoBugQcoEt6xNnqGsHDXfTA:g4 | ont:system | noBugQcoEt6xNnqGsHDXfTA-1: | 25 |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | ont:justifiedBy | XoBugQcoEt6xNnqGsHDXfTA:g5 | 26 |
| XoBugQcoEt6xNnqGsHDXfTA:g5 | rdf:type | ont:CompoundJustification | 27 |
| XoBugQcoEt6xNnqGsHDXfTA:g5 | ont:confidence | XoBugQcoEt6xNnqGsHDXfTA:g6 | 28 |
| XoBugQcoEt6xNnqGsHDXfTA:g6 | rdf:type | ont:Confidence | 29 |
| XoBugQcoEt6xNnqGsHDXfTA:g6 | ont:confidenceValue | 0.99 | 30 |
| XoBugQcoEt6xNnqGsHDXfTA:g6 | ont:system | noBugQcoEt6xNnqGsHDXfTA-4:compoundJustificationWrapper | 31 |
| XoBugQcoEt6xNnqGsHDXfTA:g5 | ont:containedJustification | XoBugQcoEt6xNnqGsHDXfTA:g7 | 32 |


```
kgtk unreify-values -i examples/docs/unreify-values-file2.tsv \
		    --trigger-label rdf:type \
		    --trigger-node2 ont:Confidence \
		    --value-label ont:confidenceValue \
		    --old-label ont:confidence \
		    --allow-extra-columns
```

| node1 | label | node2 | record# | id |
| -- | -- | -- | -- | -- |
| XoBugQcoEt6xNnqGsHDXfTA:g0 | rdf:type | ont:PrivateData | 05 |  |
| XoBugQcoEt6xNnqGsHDXfTA:g0 | ont:jsonContent | "{\"fileType\":\"en\"}" | 06 |  |
| XoBugQcoEt6xNnqGsHDXfTA:g0 | ont:system | rpi:fileType | 07 |  |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | rdf:type | ont:ClusterMembership | 10 |  |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:cluster | gaia:events/03a41b2b-e0ef-42f9-a192-433e0abc3a70-cluster-projectedFromSingleton | 11 |  |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:clusterMember | gaia:events/03a41b2b-e0ef-42f9-a192-433e0abc3a70 | 12 |  |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:system | noBugQcoEt6xNnqGsHDXfTA-2: | 17 |  |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:confidenceValue | 1.0 |  | XoBugQcoEt6xNnqGsHDXfTA:g2 |
| XoBugQcoEt6xNnqGsHDXfTA:g2 | ont:system | noBugQcoEt6xNnqGsHDXfTA-2: |  | XoBugQcoEt6xNnqGsHDXfTA:g2-1 |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | rdf:type | rdf:Statement | 18 |  |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | rdf:object | gaia:entities/d1dcefce-badf-4948-bfcf-5d33116fa12c | 19 |  |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | rdf:predicate | noBugQcoEt6xNnqGsHDXfTA-3:Physical.LocatedNear_Place | 20 |  |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | rdf:subject | gaia:relations/d3e1e4df-6c8c-4fd1-8b93-ee49ef238f72 | 21 |  |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | ont:justifiedBy | XoBugQcoEt6xNnqGsHDXfTA:g5 | 26 |  |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | ont:confidenceValue | 9.9e-01 |  | XoBugQcoEt6xNnqGsHDXfTA:g4 |
| XoBugQcoEt6xNnqGsHDXfTA:g4 | ont:system | noBugQcoEt6xNnqGsHDXfTA-1: |  | XoBugQcoEt6xNnqGsHDXfTA:g4-1 |
| XoBugQcoEt6xNnqGsHDXfTA:g5 | rdf:type | ont:CompoundJustification | 27 |  |
| XoBugQcoEt6xNnqGsHDXfTA:g5 | ont:containedJustification | XoBugQcoEt6xNnqGsHDXfTA:g7 | 32 |  |
| XoBugQcoEt6xNnqGsHDXfTA:g5 | ont:confidenceValue | 0.99 |  | XoBugQcoEt6xNnqGsHDXfTA:g6 |
| XoBugQcoEt6xNnqGsHDXfTA:g6 | ont:system | noBugQcoEt6xNnqGsHDXfTA-4:compoundJustificationWrapper |  | XoBugQcoEt6xNnqGsHDXfTA:g6-1 |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | rdf:type | ont:Entity | 01 |  |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:informativeJustification | XoBugQcoEt6xNnqGsHDXfTA:b0 | 02 |  |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:justifiedBy | XoBugQcoEt6xNnqGsHDXfTA:b1 | 03 |  |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:privateData | XoBugQcoEt6xNnqGsHDXfTA:g0 | 04 |  |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:system | noBugQcoEt6xNnqGsHDXfTA-1: | 08 |  |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:textValue | "32" | 09 |  |

### Unreifying without Multiple Values

 
```bash
kgtk cat -i examples/docs/unreify-values-file3.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | rdf:type | ont:Entity |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:informativeJustification | XoBugQcoEt6xNnqGsHDXfTA:b0 |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:justifiedBy | XoBugQcoEt6xNnqGsHDXfTA:b1 |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:privateData | XoBugQcoEt6xNnqGsHDXfTA:g0 |
| XoBugQcoEt6xNnqGsHDXfTA:g0 | rdf:type | ont:PrivateData |
| XoBugQcoEt6xNnqGsHDXfTA:g0 | ont:jsonContent | "{\"fileType\":\"en\"}" |
| XoBugQcoEt6xNnqGsHDXfTA:g0 | ont:system | rpi:fileType |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:system | noBugQcoEt6xNnqGsHDXfTA-1: |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:textValue | "32" |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | rdf:type | ont:ClusterMembership |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:cluster | gaia:events/03a41b2b-e0ef-42f9-a192-433e0abc3a70-cluster-projectedFromSingleton |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:clusterMember | gaia:events/03a41b2b-e0ef-42f9-a192-433e0abc3a70 |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:confidence | XoBugQcoEt6xNnqGsHDXfTA:g2 |
| XoBugQcoEt6xNnqGsHDXfTA:g2 | rdf:type | ont:Confidence |
| XoBugQcoEt6xNnqGsHDXfTA:g2 | ont:confidenceValue | 1.0 |
| XoBugQcoEt6xNnqGsHDXfTA:g2 | ont:confidenceValue | 2.0 |
| XoBugQcoEt6xNnqGsHDXfTA:g2 | ont:system | noBugQcoEt6xNnqGsHDXfTA-2: |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:system | noBugQcoEt6xNnqGsHDXfTA-2: |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | rdf:type | rdf:Statement |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | rdf:object | gaia:entities/d1dcefce-badf-4948-bfcf-5d33116fa12c |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | rdf:predicate | noBugQcoEt6xNnqGsHDXfTA-3:Physical.LocatedNear_Place |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | rdf:subject | gaia:relations/d3e1e4df-6c8c-4fd1-8b93-ee49ef238f72 |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | ont:confidence | XoBugQcoEt6xNnqGsHDXfTA:g4 |
| XoBugQcoEt6xNnqGsHDXfTA:g4 | rdf:type | ont:Confidence |
| XoBugQcoEt6xNnqGsHDXfTA:g4 | ont:confidenceValue | 9.9e-01 |
| XoBugQcoEt6xNnqGsHDXfTA:g4 | ont:system | noBugQcoEt6xNnqGsHDXfTA-1: |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | ont:justifiedBy | XoBugQcoEt6xNnqGsHDXfTA:g5 |
| XoBugQcoEt6xNnqGsHDXfTA:g5 | rdf:type | ont:CompoundJustification |
| XoBugQcoEt6xNnqGsHDXfTA:g5 | ont:confidence | XoBugQcoEt6xNnqGsHDXfTA:g6 |
| XoBugQcoEt6xNnqGsHDXfTA:g6 | rdf:type | ont:Confidence |
| XoBugQcoEt6xNnqGsHDXfTA:g6 | ont:confidenceValue | 0.99 |
| XoBugQcoEt6xNnqGsHDXfTA:g6 | ont:system | noBugQcoEt6xNnqGsHDXfTA-4:compoundJustificationWrapper |
| XoBugQcoEt6xNnqGsHDXfTA:g5 | ont:containedJustification | XoBugQcoEt6xNnqGsHDXfTA:g7 |


```
kgtk unreify-values -i examples/docs/unreify-values-file3.tsv \
       --trigger-label rdf:type \
        --trigger-node2 ont:Confidence \
        --value-label ont:confidenceValue \
        --old-label ont:confidence
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| XoBugQcoEt6xNnqGsHDXfTA:g0 | rdf:type | ont:PrivateData |  |
| XoBugQcoEt6xNnqGsHDXfTA:g0 | ont:jsonContent | "{\"fileType\":\"en\"}" |  |
| XoBugQcoEt6xNnqGsHDXfTA:g0 | ont:system | rpi:fileType |  |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | rdf:type | ont:ClusterMembership |  |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:cluster | gaia:events/03a41b2b-e0ef-42f9-a192-433e0abc3a70-cluster-projectedFromSingleton |  |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:clusterMember | gaia:events/03a41b2b-e0ef-42f9-a192-433e0abc3a70 |  |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:system | noBugQcoEt6xNnqGsHDXfTA-2: |  |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:confidence | XoBugQcoEt6xNnqGsHDXfTA:g2 |  |
| XoBugQcoEt6xNnqGsHDXfTA:g2 | rdf:type | ont:Confidence |  |
| XoBugQcoEt6xNnqGsHDXfTA:g2 | ont:confidenceValue | 1.0 |  |
| XoBugQcoEt6xNnqGsHDXfTA:g2 | ont:confidenceValue | 2.0 |  |
| XoBugQcoEt6xNnqGsHDXfTA:g2 | ont:system | noBugQcoEt6xNnqGsHDXfTA-2: |  |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | rdf:type | rdf:Statement |  |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | rdf:object | gaia:entities/d1dcefce-badf-4948-bfcf-5d33116fa12c |  |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | rdf:predicate | noBugQcoEt6xNnqGsHDXfTA-3:Physical.LocatedNear_Place |  |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | rdf:subject | gaia:relations/d3e1e4df-6c8c-4fd1-8b93-ee49ef238f72 |  |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | ont:justifiedBy | XoBugQcoEt6xNnqGsHDXfTA:g5 |  |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | ont:confidenceValue | 9.9e-01 | XoBugQcoEt6xNnqGsHDXfTA:g4 |
| XoBugQcoEt6xNnqGsHDXfTA:g4 | ont:system | noBugQcoEt6xNnqGsHDXfTA-1: | XoBugQcoEt6xNnqGsHDXfTA:g4-1 |
| XoBugQcoEt6xNnqGsHDXfTA:g5 | rdf:type | ont:CompoundJustification |  |
| XoBugQcoEt6xNnqGsHDXfTA:g5 | ont:containedJustification | XoBugQcoEt6xNnqGsHDXfTA:g7 |  |
| XoBugQcoEt6xNnqGsHDXfTA:g5 | ont:confidenceValue | 0.99 | XoBugQcoEt6xNnqGsHDXfTA:g6 |
| XoBugQcoEt6xNnqGsHDXfTA:g6 | ont:system | noBugQcoEt6xNnqGsHDXfTA-4:compoundJustificationWrapper | XoBugQcoEt6xNnqGsHDXfTA:g6-1 |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | rdf:type | ont:Entity |  |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:informativeJustification | XoBugQcoEt6xNnqGsHDXfTA:b0 |  |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:justifiedBy | XoBugQcoEt6xNnqGsHDXfTA:b1 |  |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:privateData | XoBugQcoEt6xNnqGsHDXfTA:g0 |  |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:system | noBugQcoEt6xNnqGsHDXfTA-1: |  |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:textValue | "32" |  |



### Unreifying with Multiple Values

 
```bash
kgtk cat -i examples/docs/unreify-values-file3.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | rdf:type | ont:Entity |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:informativeJustification | XoBugQcoEt6xNnqGsHDXfTA:b0 |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:justifiedBy | XoBugQcoEt6xNnqGsHDXfTA:b1 |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:privateData | XoBugQcoEt6xNnqGsHDXfTA:g0 |
| XoBugQcoEt6xNnqGsHDXfTA:g0 | rdf:type | ont:PrivateData |
| XoBugQcoEt6xNnqGsHDXfTA:g0 | ont:jsonContent | "{\"fileType\":\"en\"}" |
| XoBugQcoEt6xNnqGsHDXfTA:g0 | ont:system | rpi:fileType |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:system | noBugQcoEt6xNnqGsHDXfTA-1: |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:textValue | "32" |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | rdf:type | ont:ClusterMembership |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:cluster | gaia:events/03a41b2b-e0ef-42f9-a192-433e0abc3a70-cluster-projectedFromSingleton |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:clusterMember | gaia:events/03a41b2b-e0ef-42f9-a192-433e0abc3a70 |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:confidence | XoBugQcoEt6xNnqGsHDXfTA:g2 |
| XoBugQcoEt6xNnqGsHDXfTA:g2 | rdf:type | ont:Confidence |
| XoBugQcoEt6xNnqGsHDXfTA:g2 | ont:confidenceValue | 1.0 |
| XoBugQcoEt6xNnqGsHDXfTA:g2 | ont:confidenceValue | 2.0 |
| XoBugQcoEt6xNnqGsHDXfTA:g2 | ont:system | noBugQcoEt6xNnqGsHDXfTA-2: |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:system | noBugQcoEt6xNnqGsHDXfTA-2: |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | rdf:type | rdf:Statement |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | rdf:object | gaia:entities/d1dcefce-badf-4948-bfcf-5d33116fa12c |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | rdf:predicate | noBugQcoEt6xNnqGsHDXfTA-3:Physical.LocatedNear_Place |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | rdf:subject | gaia:relations/d3e1e4df-6c8c-4fd1-8b93-ee49ef238f72 |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | ont:confidence | XoBugQcoEt6xNnqGsHDXfTA:g4 |
| XoBugQcoEt6xNnqGsHDXfTA:g4 | rdf:type | ont:Confidence |
| XoBugQcoEt6xNnqGsHDXfTA:g4 | ont:confidenceValue | 9.9e-01 |
| XoBugQcoEt6xNnqGsHDXfTA:g4 | ont:system | noBugQcoEt6xNnqGsHDXfTA-1: |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | ont:justifiedBy | XoBugQcoEt6xNnqGsHDXfTA:g5 |
| XoBugQcoEt6xNnqGsHDXfTA:g5 | rdf:type | ont:CompoundJustification |
| XoBugQcoEt6xNnqGsHDXfTA:g5 | ont:confidence | XoBugQcoEt6xNnqGsHDXfTA:g6 |
| XoBugQcoEt6xNnqGsHDXfTA:g6 | rdf:type | ont:Confidence |
| XoBugQcoEt6xNnqGsHDXfTA:g6 | ont:confidenceValue | 0.99 |
| XoBugQcoEt6xNnqGsHDXfTA:g6 | ont:system | noBugQcoEt6xNnqGsHDXfTA-4:compoundJustificationWrapper |
| XoBugQcoEt6xNnqGsHDXfTA:g5 | ont:containedJustification | XoBugQcoEt6xNnqGsHDXfTA:g7 |


```
kgtk unreify-values -i examples/docs/unreify-values-file3.tsv \
        --trigger-label rdf:type \
        --trigger-node2 ont:Confidence \
        --value-label ont:confidenceValue \
        --old-label ont:confidence \
	--allow-multiple-values
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| XoBugQcoEt6xNnqGsHDXfTA:g0 | rdf:type | ont:PrivateData |  |
| XoBugQcoEt6xNnqGsHDXfTA:g0 | ont:jsonContent | "{\"fileType\":\"en\"}" |  |
| XoBugQcoEt6xNnqGsHDXfTA:g0 | ont:system | rpi:fileType |  |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | rdf:type | ont:ClusterMembership |  |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:cluster | gaia:events/03a41b2b-e0ef-42f9-a192-433e0abc3a70-cluster-projectedFromSingleton |  |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:clusterMember | gaia:events/03a41b2b-e0ef-42f9-a192-433e0abc3a70 |  |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:system | noBugQcoEt6xNnqGsHDXfTA-2: |  |
| XoBugQcoEt6xNnqGsHDXfTA:g1 | ont:confidenceValue | 2.0\|1.0 | XoBugQcoEt6xNnqGsHDXfTA:g2 |
| XoBugQcoEt6xNnqGsHDXfTA:g2 | ont:system | noBugQcoEt6xNnqGsHDXfTA-2: | XoBugQcoEt6xNnqGsHDXfTA:g2-1 |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | rdf:type | rdf:Statement |  |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | rdf:object | gaia:entities/d1dcefce-badf-4948-bfcf-5d33116fa12c |  |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | rdf:predicate | noBugQcoEt6xNnqGsHDXfTA-3:Physical.LocatedNear_Place |  |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | rdf:subject | gaia:relations/d3e1e4df-6c8c-4fd1-8b93-ee49ef238f72 |  |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | ont:justifiedBy | XoBugQcoEt6xNnqGsHDXfTA:g5 |  |
| XoBugQcoEt6xNnqGsHDXfTA:g3 | ont:confidenceValue | 9.9e-01 | XoBugQcoEt6xNnqGsHDXfTA:g4 |
| XoBugQcoEt6xNnqGsHDXfTA:g4 | ont:system | noBugQcoEt6xNnqGsHDXfTA-1: | XoBugQcoEt6xNnqGsHDXfTA:g4-1 |
| XoBugQcoEt6xNnqGsHDXfTA:g5 | rdf:type | ont:CompoundJustification |  |
| XoBugQcoEt6xNnqGsHDXfTA:g5 | ont:containedJustification | XoBugQcoEt6xNnqGsHDXfTA:g7 |  |
| XoBugQcoEt6xNnqGsHDXfTA:g5 | ont:confidenceValue | 0.99 | XoBugQcoEt6xNnqGsHDXfTA:g6 |
| XoBugQcoEt6xNnqGsHDXfTA:g6 | ont:system | noBugQcoEt6xNnqGsHDXfTA-4:compoundJustificationWrapper | XoBugQcoEt6xNnqGsHDXfTA:g6-1 |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | rdf:type | ont:Entity |  |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:informativeJustification | XoBugQcoEt6xNnqGsHDXfTA:b0 |  |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:justifiedBy | XoBugQcoEt6xNnqGsHDXfTA:b1 |  |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:privateData | XoBugQcoEt6xNnqGsHDXfTA:g0 |  |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:system | noBugQcoEt6xNnqGsHDXfTA-1: |  |
| gaia:entities/e34874a6-a857-4f14-8aee-9947d3e9caaf | ont:textValue | "32" |  |


