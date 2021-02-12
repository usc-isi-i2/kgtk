## Overview

`kgtk lexicalize` builds English sentences from KGTK edge files.

The primary purpose of this command is to construct inputs for
text-based distance vector analysis.  However, it may also
prove useful for explaining the contents of local subsets of
Knowledge Graphs.

### Input Files

`kgtk lexicalize` has a primary input file which contains:

  - `label` properties (entity labels)
  - `description` properties
  - `isa` properties
  - `has` properties
  - property values

There may also be one or more entity input files that contain additional
entity labels.  These files are specified with the `--entity-label-file` option.

### Optimization for Presorted Input

Normally, the primary input file is loaded into memory before
any output is produced. This can lead to performance problems
when the amount of memory required exceeds the amount that is available.

If the primary input file is presorted on `node1`, a presorted processing mode may be used
to minimize memory consumption.  This mode ignores the `--add-entity-labels-from-input` option,
so the primary input file may not contain entity labels when using presorted input.

`--presorted` (default FALSE) is used to indicate that the presorted input
processing mode should be used.  The input file will be checked as it is read
to ensure that it properly sorted.  If it is not, an error will occur and
processing will stop.

### Output File

The output file is a KGTK file containing `sentence` properties
constructed during lexicalization.  An optional `explanation`
column gives a brief summary of how the sentence was constructed.

| node1 | label | node2 | explaination |
| ----- | ----- | ----- | ------------ |
| Q75952970 | sentence | "It is a census in Austria-Hungary." | "isa(\'census\'->\'a census\')+property_values(\'country Austria-Hungary\'->[\'in Austria-Hungary\'])" |
| Q75952971 | sentence | "Philippe Greenway, born 1991, is a human and male." | "label(\'Philippe Greenway\')+description(\'born 1991\')+isa(\'human\',\'male\'->\'a human and male\')" |
| Q75952972 | sentence | "Sir Patrick Hastings, Peerage person ID=426177, is a human and male." | "label(\'Sir Patrick Hastings\')+description(\'Peerage person ID=426177\')+isa(\'human\',\'male\'->\'a human and male\')" |
| Q75952973 | sentence | "Philip Maitland Gore Anley, Peerage person ID=426178, is a human and male." | "label(\'Philip Maitland Gore Anley\')+description(\'Peerage person ID=426178\')+isa(\'human\',\'male\'->\'a human and male\')" |
| Q75952974 | sentence | "It is a star." | "isa(\'star\'->\'a star\')" |
| Q75952975 | sentence | "Sarah Louise Anley, died 2010, is a female and human." | "label(\'Sarah Louise Anley\')+description(\'died 2010\')+isa(\'female\',\'human\'->\'a female and human\')" |


The `--sentence-label` option provides the relationship name
in the `label` column of the output file.  The default value is "sentence".

`--explain` option controls whether or not an explanation column
is included in the output file.  The default is not to include explanations
in the output file.

### Entity Label Loading

When entity label files are provided, thet are read befor the primary
input file is processed.  Edges where the value in the `label` column
matches one if the properties in the `--label-properties` list (default ['label']
are loaded into memory in the entity label dictionary.

When `--add-entity-labels-from-input` is TRUE, and the input file is
not presorted, any edges in the primary input file where the value in
the `label` column matches one of the properties in the `--label-properties`
list will also be added to the entity label dictionary.


| id | node1 | label | node2 |
| -- | -- | -- | -- |
| Q11247242-label-en | Q11247242 | label | 'Steady & Co.'@en |
| Q11247279-label-en | Q11247279 | label | 'Ford'@en |
| Q11247470-label-en | Q11247470 | label | 'commanding officer'@en |
| Q1124841-label-en | Q1124841 | label | 'PFC Lokomotiv Plovdiv'@en |
| Q1124849-label-en | Q1124849 | label | 'Verve Records'@en |

### Entity Label Dictionary and Priority

Entity label edges are used build a dictionary between the `node1` value in
entity label edges and the `node2` value in the entity label edge.

When there are multiple entity label edges for a given `node1` value,
only one `node2` value is retained.  The following priority is used:

  - If there are any `node2` values which are language-qualified strings
     for the English language (language code `en` and *no language suffix*)
     the last-seen such value is retained.
  - Otherwise, the first `node2` value seen is retained.

### Property List Defaults

Sentences are built by assembling labels, descriptions, and other
properties under a hard-coded template.  Each of the property
list options supplies property values into a particular slot in
the sentence generation template.

| Property Option  | Default List |
| ---------------- | ------------ |
| --description-properties | description  |
| --has-properties   |              |
| --isa-properties   | P21 P31 P39 P106 P279 |
| --label-properties | label        |
| --property-values  | P17          |

| Wikidata Property | Label       |
| ----------------- | ----------- |
| P17               | country       |
| P21               | sex or gender |
| P31               | instance of   |
| P39               | position held |
| P106              | occupation    |
| P279              | subclass of   |

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

### One `isa` Property, Seperate Labels

The following input file has a single entity with a single `isa` relationship
(`P31`, `instance of`).

```bash
kgtk cat -i examples/docs/lexicalize-one-isa-input.tsv
```

| id | node1 | label | node2 |
| -- | -- | -- | -- |
| Q75952971-P31-Q5-d020ba0c-0 | Q75952971 | P31 | Q5 |

The following label file has the labels needed by the input file:

```bash
kgtk cat -i examples/docs/lexicalize-one-isa-labels.tsv
```

| id | node1 | label | node2 |
| -- | -- | -- | -- |
| Q75952971-label-en | Q75952971 | label | 'Philippe Greenway'@en |
| Q5-label-en | Q5 | label | 'human'@en |

Convert this data to a sentence:

```bash
kgtk lexicalize --input-file examples/docs/lexicalize-one-isa-input.tsv \
                --entity-label-file examples/docs/lexicalize-one-isa-labels.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| Q75952971 | sentence | "Philippe Greenway is a human." |

### One `isa` Property, a Single File

The following input file has a single entity with a single `isa` relationship.
The matching labels are in the same file.

```bash
kgtk cat -i examples/docs/lexicalize-one-isa-combined.tsv
```

| id | node1 | label | node2 |
| -- | -- | -- | -- |
| Q75952971-P31-Q5-d020ba0c-0 | Q75952971 | P31 | Q5 |
| Q75952971-label-en | Q75952971 | label | 'Philippe Greenway'@en |
| Q5-label-en | Q5 | label | 'human'@en |

Convert this data to a sentence:

```bash
kgtk lexicalize --input-file examples/docs/lexicalize-one-isa-combined.tsv \
                --add-entity-labels-from-input
```

| node1 | label | node2 |
| -- | -- | -- |
| Q75952971 | sentence | "Philippe Greenway is a human." |


### Two `isa` Properties

The following input file has a single entity with two `isa` relationships
(`P31`, `instance of`)

```bash
kgtk cat -i examples/docs/lexicalize-two-isas-input.tsv
```

| id | node1 | label | node2 |
| -- | -- | -- | -- |
| Q75952971-P31-Q5-d020ba0c-0 | Q75952971 | P31 | Q5 |
| Q75952971-P21-Q6581097-018e8019-0 | Q75952971 | P21 | Q6581097 |

Here are the matching labels:

```bash
kgtk cat -i examples/docs/lexicalize-two-isas-labels.tsv
```

| id | node1 | label | node2 |
| -- | -- | -- | -- |
| Q5-label-en | Q5 | label | 'human'@en |
| Q6581097-label-en | Q6581097 | label | 'male'@en |
| Q75952971-label-en | Q75952971 | label | 'Philippe Greenway'@en |

Convert this data to a sentence:

```bash
kgtk lexicalize --input-file examples/docs/lexicalize-two-isas-input.tsv \
                --entity-label-file examples/docs/lexicalize-two-isas-labels.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| Q75952971 | sentence | "Philippe Greenway is a human and male." |

### Two `isa` Properties Reordered

The following input file has a single entity with two `isa` relationships (`P31`, `instance of`).
The order of the `isa` relationships in the input file is different from the order in the example above.

```bash
kgtk cat -i examples/docs/lexicalize-two-isas-reordered.tsv
```

| id | node1 | label | node2 |
| -- | -- | -- | -- |
| Q75952971-P21-Q6581097-018e8019-0 | Q75952971 | P21 | Q6581097 |
| Q75952971-P31-Q5-d020ba0c-0 | Q75952971 | P31 | Q5 |

Convert this data to a sentence:

```bash
kgtk lexicalize --input-file examples/docs/lexicalize-two-isas-reordered.tsv \
                --entity-label-file examples/docs/lexicalize-two-isas-labels.tsv
```

The output sentence is the same, because the properties are collected and
sorted internally during processing.

| node1 | label | node2 |
| -- | -- | -- |
| Q75952971 | sentence | "Philippe Greenway is a human and male." |

### Two `isa` Properties, Presorted Input

When an input file is presorted on the `node1` column, and the labels are
read from an external file, `kgtk lexicalize` can use an optimized
implementation that reduces the amount of memory it requires to process
large files.

The following input file has a single entity with two `isa` relationships (`P31`, `instance of`).
There is only one `node1` value, so we can use this as an example of
presorted input in a degenerate case.

```bash
kgtk cat -i examples/docs/lexicalize-two-isas-input.tsv
```

| id | node1 | label | node2 |
| -- | -- | -- | -- |
| Q75952971-P31-Q5-d020ba0c-0 | Q75952971 | P31 | Q5 |
| Q75952971-P21-Q6581097-018e8019-0 | Q75952971 | P21 | Q6581097 |

Here are the matching labels:

```bash
kgtk cat -i examples/docs/lexicalize-two-isas-labels.tsv
```

| id | node1 | label | node2 |
| -- | -- | -- | -- |
| Q5-label-en | Q5 | label | 'human'@en |
| Q6581097-label-en | Q6581097 | label | 'male'@en |
| Q75952971-label-en | Q75952971 | label | 'Philippe Greenway'@en |

Convert this data to a sentence:

```bash
kgtk lexicalize --input-file examples/docs/lexicalize-two-isas-input.tsv \
                --presorted \
                --entity-label-file examples/docs/lexicalize-two-isas-labels.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| Q75952971 | sentence | "Philippe Greenway is a human and male." |

### Two `isa` Properties and Description

The following input file has a single entity with two `isa` relationships (`P31`, `instance of`)
and a `description` property.  The input file also contains the matching labels.

```bash
kgtk cat -i examples/docs/lexicalize-two-isas-and-description.tsv
```

| id | node1 | label | node2 |
| -- | -- | -- | -- |
| Q75952971-P31-Q5-d020ba0c-0 | Q75952971 | P31 | Q5 |
| Q75952971-P21-Q6581097-018e8019-0 | Q75952971 | P21 | Q6581097 |
| Q5-label-en | Q5 | label | 'human'@en |
| Q6581097-label-en | Q6581097 | label | 'male'@en |
| Q75952971-label-en | Q75952971 | label | 'Philippe Greenway'@en |
| Q75952971-description-en | Q75952971 | description | 'born 1991'@en |

Convert this data to a sentence:

```bash
kgtk lexicalize --input-file examples/docs/lexicalize-two-isas-and-description.tsv \
                --add-entity-labels-from-input
```

| node1 | label | node2 |
| -- | -- | -- |
| Q75952971 | sentence | "Philippe Greenway, born 1991, is a human and male." |

### Two `isa` Properties, a Description, and and Property Value P17

The following input file has a single entity with two `isa` relationships (`P31`, `instance of`)
and a property value (`P17`, `country`).  The input file also contains the matching labels.

```bash
kgtk cat -i examples/docs/lexicalize-two-isas-and-property-value-P17.tsv
```

| id | node1 | label | node2 |
| -- | -- | -- | -- |
| Q75952971-P31-Q5-d020ba0c-0 | Q75952971 | P31 | Q5 |
| Q75952971-P21-Q6581097-018e8019-0 | Q75952971 | P21 | Q6581097 |
| Q5-label-en | Q5 | label | 'human'@en |
| Q6581097-label-en | Q6581097 | label | 'male'@en |
| Q75952971-label-en | Q75952971 | label | 'Philippe Greenway'@en |
| Q75952971-description-en | Q75952971 | description | 'born 1991'@en |
| Q75952971-P17-Q28513-33ddd57d-0 | Q75952971 | P17 | Q28513 |
| Q28513-label-en | Q28513 | label | 'Austria-Hungary'@en |
| P17-label-en | P17 | label | 'country'@en |

Convert this data to a sentence:

```bash
kgtk lexicalize --input-file examples/docs/lexicalize-two-isas-and-property-value-P17.tsv \
                --add-entity-labels-from-input
```

| node1 | label | node2 |
| -- | -- | -- |
| Q75952971 | sentence | "Philippe Greenway, born 1991, is a human and male in Austria-Hungary." |

!!! note
    The code that produces a readable sentence for this example is
    hard coded for property value `P17.` The use of other property
    values might require changes to the code in order to
    produce reasonable sentences.

### Two `isa` Properties and Property Values P569 and P570

The following input file has a single entity with two `isa` relationships (`P31`, `instance of`)
and two property value (`P569`, `date of birth`, and `P570`, `date of death`).
he input file also contains the matching labels.

```bash
kgtk cat -i examples/docs/lexicalize-two-isas-and-property-values-P569-P570.tsv
```

| id | node1 | label | node2 |
| -- | -- | -- | -- |
| Q75952971-P31-Q5-d020ba0c-0 | Q75952971 | P31 | Q5 |
| Q75952971-P21-Q6581097-018e8019-0 | Q75952971 | P21 | Q6581097 |
| Q5-label-en | Q5 | label | 'human'@en |
| Q6581097-label-en | Q6581097 | label | 'male'@en |
| Q75952971-label-en | Q75952971 | label | 'Philippe Greenway'@en |
| Q75952971-P569-52d50d-5fe626e5-0 | Q75952971 | P569 | ^1876-05-07T00:00:00Z/11 |
| Q75952971-P570-5f1346-586e365b-0 | Q75952971 | P570 | ^1957-02-26T00:00:00Z/11 |
| P569-label-en | P569 | label | 'date of birth'@en |
| P570-label-en | P570 | label | 'date of death'@en |

Convert this data to a sentence:

```bash
kgtk lexicalize --input-file examples/docs/lexicalize-two-isas-and-property-values-P569-P570.tsv \
                --add-entity-labels-from-input \
		--property-values P569 P570
```

| node1 | label | node2 |
| -- | -- | -- |
| Q75952971 | sentence | "Philippe Greenway is a human and male date of birth ^1876-05-07T00:00:00Z/11 and date of death ^1957-02-26T00:00:00Z/11." |

!!! note
	At present, changes to the code would be needed to improve the quality
	of the output.

### Complex Example: Q75992564, a Music Track

Here is a more complex looking example.  Most of the work is
done by the description property.

```bash
kgtk cat -i examples/docs/lexicalize-Q75992564.tsv
```

| id | node1 | label | node2 | rank | node2;wikidatatype |
| -- | -- | -- | -- | -- | -- |
| Q75992564-P136-Q83440-5a7171a8-0 | Q75992564 | P136 | Q83440 | normal | wikibase-item |
| Q75992564-P1433-Q2598379-92fd18d2-0 | Q75992564 | P1433 | Q2598379 | normal | wikibase-item |
| Q75992564-P1433-Q75998294-3aa16bcc-0 | Q75992564 | P1433 | Q75998294 | normal | wikibase-item |
| Q75992564-P1476-7e22ec-4db02c7e-0 | Q75992564 | P1476 | 'Because of You'@en | normal | monolingualtext |
| Q75992564-P1552-Q109940-802348fe-0 | Q75992564 | P1552 | Q109940 | normal | wikibase-item |
| Q75992564-P1552-Q155171-582f91ae-0 | Q75992564 | P1552 | Q155171 | normal | wikibase-item |
| Q75992564-P1552-Q15975575-a54239e8-0 | Q75992564 | P1552 | Q15975575 | normal | wikibase-item |
| Q75992564-P162-Q229430-4d2b5fa7-0 | Q75992564 | P162 | Q229430 | normal | wikibase-item |
| Q75992564-P162-Q7821969-674ded3a-0 | Q75992564 | P162 | Q7821969 | normal | wikibase-item |
| Q75992564-P175-Q229430-aefd7965-0 | Q75992564 | P175 | Q229430 | normal | wikibase-item |
| Q75992564-P175-Q483507-a1ad6642-0 | Q75992564 | P175 | Q483507 | normal | wikibase-item |
| Q75992564-P1889-Q400557-94928f8d-0 | Q75992564 | P1889 | Q400557 | normal | wikibase-item |
| Q75992564-P2550-Q868569-cbe8942c-0 | Q75992564 | P2550 | Q868569 | normal | wikibase-item |
| Q75992564-P31-Q55850593-156262eb-0 | Q75992564 | P31 | Q55850593 |  |  |
| Q75992564-P31-Q55850593-156262eb-0 | Q75992564 | P31 | Q55850593 | normal | wikibase-item |
| Q75992564-P4404-69fc83-9222fd1e-0 | Q75992564 | P4404 | "1c5c05d6-dff6-440a-ba1f-54000e2d04bd" | normal | external-id |
| Q75992564-P4404-fa8703-43654e34-0 | Q75992564 | P4404 | "102eb099-3119-4d08-80f5-06511af875a4" | normal | external-id |
| Q75992564-description-en | Q75992564 | description | 'vocal track by Reba in duet with Kelly Clarkson; 2007 studio recording; cover version'@en |  |  |
| Q75992564-directed_pagerank-31405997 | Q75992564 | directed_pagerank | 8.715560990765719e-09 |  |  |
| Q75992564-in_degree-2-0000 | Q75992564 | in_degree | 2 |  |  |
| Q75992564-isa-Q55850593-0000 | Q75992564 | isa | Q55850593 |  |  |
| Q75992564-label-en | Q75992564 | label | 'Because of You'@en |  |  |
| Q75992564-out_degree-16-0000 | Q75992564 | out_degree | 16 |  |  |
| Q75992564-undirected_pagerank-31405997 | Q75992564 | undirected_pagerank | 8.715560990765719e-09 |  |  |
| Q75992564-vertex_in_degree-31405995 | Q75992564 | vertex_in_degree | 2 |  |  |
| Q75992564-vertex_in_degree-31405995 | Q75992564 | vertex_in_degree | 2 |  |  |
| Q75992564-vertex_out_degree-31405996 | Q75992564 | vertex_out_degree | 13 |  |  |
| Q75992564-vertex_out_degree-31405996 | Q75992564 | vertex_out_degree | 13 |  |  |
| Q55850593-label-en | Q55850593 | label | 'music track with vocals'@en |  |  |
| P1552-label-en | P1552 | label | 'has quality'@en |  |  |
| Q109940-label-en | Q109940 | label | 'duet'@en |  |  |
| Q155171-label-en | Q155171 | label | 'cover version'@en |  |  |
| Q15975575-label-en | Q15975575 | label | 'studio recording'@en |  |  |

Convert this data to a sentence:

```bash
kgtk lexicalize --input-file examples/docs/lexicalize-Q75992564.tsv \
                --add-entity-labels-from-input
```

| node1 | label | node2 |
| -- | -- | -- |
| Q75992564 | sentence | "Because of You, vocal track by Reba in duet with Kelly Clarkson; 2007 studio recording; cover version, is a music track with vocals." |

### Complex Example: Q75992564, a Music Track, with `has` Properties and Omitting the Description

Let's try adding `P1552` (`has quality`) to the list of `has` properties
and omit the description property.

```bash
kgtk cat -i examples/docs/lexicalize-Q75992564.tsv
```

| id | node1 | label | node2 | rank | node2;wikidatatype |
| -- | -- | -- | -- | -- | -- |
| Q75992564-P136-Q83440-5a7171a8-0 | Q75992564 | P136 | Q83440 | normal | wikibase-item |
| Q75992564-P1433-Q2598379-92fd18d2-0 | Q75992564 | P1433 | Q2598379 | normal | wikibase-item |
| Q75992564-P1433-Q75998294-3aa16bcc-0 | Q75992564 | P1433 | Q75998294 | normal | wikibase-item |
| Q75992564-P1476-7e22ec-4db02c7e-0 | Q75992564 | P1476 | 'Because of You'@en | normal | monolingualtext |
| Q75992564-P1552-Q109940-802348fe-0 | Q75992564 | P1552 | Q109940 | normal | wikibase-item |
| Q75992564-P1552-Q155171-582f91ae-0 | Q75992564 | P1552 | Q155171 | normal | wikibase-item |
| Q75992564-P1552-Q15975575-a54239e8-0 | Q75992564 | P1552 | Q15975575 | normal | wikibase-item |
| Q75992564-P162-Q229430-4d2b5fa7-0 | Q75992564 | P162 | Q229430 | normal | wikibase-item |
| Q75992564-P162-Q7821969-674ded3a-0 | Q75992564 | P162 | Q7821969 | normal | wikibase-item |
| Q75992564-P175-Q229430-aefd7965-0 | Q75992564 | P175 | Q229430 | normal | wikibase-item |
| Q75992564-P175-Q483507-a1ad6642-0 | Q75992564 | P175 | Q483507 | normal | wikibase-item |
| Q75992564-P1889-Q400557-94928f8d-0 | Q75992564 | P1889 | Q400557 | normal | wikibase-item |
| Q75992564-P2550-Q868569-cbe8942c-0 | Q75992564 | P2550 | Q868569 | normal | wikibase-item |
| Q75992564-P31-Q55850593-156262eb-0 | Q75992564 | P31 | Q55850593 |  |  |
| Q75992564-P31-Q55850593-156262eb-0 | Q75992564 | P31 | Q55850593 | normal | wikibase-item |
| Q75992564-P4404-69fc83-9222fd1e-0 | Q75992564 | P4404 | "1c5c05d6-dff6-440a-ba1f-54000e2d04bd" | normal | external-id |
| Q75992564-P4404-fa8703-43654e34-0 | Q75992564 | P4404 | "102eb099-3119-4d08-80f5-06511af875a4" | normal | external-id |
| Q75992564-description-en | Q75992564 | description | 'vocal track by Reba in duet with Kelly Clarkson; 2007 studio recording; cover version'@en |  |  |
| Q75992564-directed_pagerank-31405997 | Q75992564 | directed_pagerank | 8.715560990765719e-09 |  |  |
| Q75992564-in_degree-2-0000 | Q75992564 | in_degree | 2 |  |  |
| Q75992564-isa-Q55850593-0000 | Q75992564 | isa | Q55850593 |  |  |
| Q75992564-label-en | Q75992564 | label | 'Because of You'@en |  |  |
| Q75992564-out_degree-16-0000 | Q75992564 | out_degree | 16 |  |  |
| Q75992564-undirected_pagerank-31405997 | Q75992564 | undirected_pagerank | 8.715560990765719e-09 |  |  |
| Q75992564-vertex_in_degree-31405995 | Q75992564 | vertex_in_degree | 2 |  |  |
| Q75992564-vertex_in_degree-31405995 | Q75992564 | vertex_in_degree | 2 |  |  |
| Q75992564-vertex_out_degree-31405996 | Q75992564 | vertex_out_degree | 13 |  |  |
| Q75992564-vertex_out_degree-31405996 | Q75992564 | vertex_out_degree | 13 |  |  |
| Q55850593-label-en | Q55850593 | label | 'music track with vocals'@en |  |  |
| P1552-label-en | P1552 | label | 'has quality'@en |  |  |
| Q109940-label-en | Q109940 | label | 'duet'@en |  |  |
| Q155171-label-en | Q155171 | label | 'cover version'@en |  |  |
| Q15975575-label-en | Q15975575 | label | 'studio recording'@en |  |  |

```bash
kgtk lexicalize --input-file examples/docs/lexicalize-Q75992564.tsv \
                --add-entity-labels-from-input \
		--has-properties P1552 \
		--description-properties ""
```

| node1 | label | node2 |
| -- | -- | -- |
| Q75992564 | sentence | "Because of You is a music track with vocals, and has duet and cover version and studio recording." |
