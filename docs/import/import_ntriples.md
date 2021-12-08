## Overview

This command will import one or more ntriple files into KGTK format.

The input file should adhere to the [RDF N-Triples
specification](https://www.w3.org/TR/n-triples/).

Note: `kgtk import-ntriples` does not currently support comments
in the input file.

Note: An RDF 1.1 N-Triples file may contain language tags that
are more general than the language tags currently supported by
the KGTk File Format Specification v2.

## Usage
```
usage: kgtk import-ntriples [-h] [-i INPUT_FILE [INPUT_FILE ...]]
                            [-o OUTPUT_FILE] [--reject-file REJECT_FILE]
                            [--namespace-file NAMESPACE_FILE]
                            [--updated-namespace-file NAMESPACE_FILE]
                            [--namespace-id-prefix NAMESPACE_ID_PREFIX]
                            [--namespace-id-use-uuid [NAMESPACE_ID_USE_UUID]]
                            [--namespace-id-counter NAMESPACE_ID_COUNTER]
                            [--namespace-id-zfill NAMESPACE_ID_ZFILL]
                            [--output-only-used-namespaces [OUTPUT_ONLY_USED_NAMESPACES]]
                            [--build-new-namespaces [BUILD_NEW_NAMESPACES]]
                            [--allow-lax-uri [ALLOW_LAX_URI]]
                            [--allow-unknown-datatype-iris [ALLOW_UNKNOWN_DATATYPE_IRIS]]
                            [--allow-turtle-quotes [ALLOW_TURTLE_QUOTES]]
                            [--allow-lang-string-datatype [ALLOW_LANG_STRING_DATATYPE]]
                            [--lang-string-tag LANG_STRING_TAG]
                            [--local-namespace-prefix LOCAL_NAMESPACE_PREFIX]
                            [--local-namespace-use-uuid [LOCAL_NAMESPACE_USE_UUID]]
                            [--prefix-expansion-label PREFIX_EXPANSION_LABEL]
                            [--structured-value-label STRUCTURED_VALUE_LABEL]
                            [--structured-uri-label STRUCTURED_URI_LABEL]
                            [--newnode-prefix NEWNODE_PREFIX]
                            [--newnode-use-uuid [NEWNODE_USE_UUID]]
                            [--newnode-counter NEWNODE_COUNTER]
                            [--newnode-zfill NEWNODE_ZFILL]
                            [--build-id [BUILD_ID]]
                            [--build-datatype-column [BUILD_DATATYPE_COLUMN]]
                            [--datatype-column-name DATATYPE_COLUMN_NAME]
                            [--validate [VALIDATE]] [--summary [SUMMARY]]
                            [--override-uuid OVERRIDE_UUID]
                            [--write-namespaces WRITE_NAMESPACES]
                            [--overwrite-id [optional true|false]]
                            [--verify-id-unique [optional true|false]]
                            [--value-hash-width VALUE_HASH_WIDTH]
                            [--claim-id-hash-width CLAIM_ID_HASH_WIDTH]
                            [--claim-id-column-name CLAIM_ID_COLUMN_NAME]
                            [--id-separator ID_SEPARATOR]
                            [-v [optional True|False]]

Import an ntriples file, writing a KGTK file.

Additional options are shown in expert help.
kgtk --expert import-ntriples --help

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE [INPUT_FILE ...], --input-file INPUT_FILE [INPUT_FILE ...]
                        The ntriples file(s) to import. (May be omitted or '-'
                        for stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for
                        stdout.)
  --reject-file REJECT_FILE
                        The ntriples output file for records that are
                        rejected. (Optional, use '-' for stdout.)
  --namespace-file NAMESPACE_FILE
                        The KGTK input file with known namespaces. (Optional,
                        use '-' for stdin.)
  --updated-namespace-file NAMESPACE_FILE
                        The KGTK output file with updated namespaces.
                        (Optional, use '-' for stdout.)
  --namespace-id-prefix NAMESPACE_ID_PREFIX
                        The prefix used to generate new namespaces.
                        (default=n).
  --namespace-id-use-uuid [NAMESPACE_ID_USE_UUID]
                        Use the local namespace UUID when generating
                        namespaces. When there are multiple input files, each
                        input file gets its own UUID. (default=False).
  --namespace-id-counter NAMESPACE_ID_COUNTER
                        The counter used to generate new namespaces.
                        (default=1).
  --namespace-id-zfill NAMESPACE_ID_ZFILL
                        The width of the counter used to generate new
                        namespaces. (default=0).
  --output-only-used-namespaces [OUTPUT_ONLY_USED_NAMESPACES]
                        Write only used namespaces to the output file.
                        (default=True).
  --build-new-namespaces [BUILD_NEW_NAMESPACES]
                        When True, create new namespaces. When False, use only
                        existing namespaces. (default=True).
  --allow-lax-uri [ALLOW_LAX_URI]
                        Allow URIs that don't begin with a http:// or
                        https://. (default=True).
  --allow-unknown-datatype-iris [ALLOW_UNKNOWN_DATATYPE_IRIS]
                        Allow unknown datatype IRIs, creating a qualified
                        record. (default=True).
  --allow-turtle-quotes [ALLOW_TURTLE_QUOTES]
                        Allow literals to use single quotes (to support Turtle
                        format). (default=False).
  --allow-lang-string-datatype [ALLOW_LANG_STRING_DATATYPE]
                        Allow literals to include exposed langString datatype
                        IRIs (which is forbidden by the spec, but occurs
                        anyway). (default=False).
  --lang-string-tag LANG_STRING_TAG
                        The tag to use with exposed langString instances. ``
                        or `-` mean to use a string, otherwise use a lanuage-
                        qualified string. (default=-).
  --local-namespace-prefix LOCAL_NAMESPACE_PREFIX
                        The namespace prefix for blank nodes. (default=X).
  --local-namespace-use-uuid [LOCAL_NAMESPACE_USE_UUID]
                        Generate a UUID for the local namespace. When there
                        are multiple input files, each input file gets its own
                        UUID. (default=True).
  --prefix-expansion-label PREFIX_EXPANSION_LABEL
                        The label for prefix expansions in the namespace file.
                        (default=prefix_expansion).
  --structured-value-label STRUCTURED_VALUE_LABEL
                        The label for value records for ntriple structured
                        literals. (default=kgtk:structured_value).
  --structured-uri-label STRUCTURED_URI_LABEL
                        The label for URI records for ntriple structured
                        literals. (default=kgtk:structured_uri).
  --newnode-prefix NEWNODE_PREFIX
                        The prefix used to generate new nodes for ntriple
                        structured literals. (default=kgtk:node).
  --newnode-use-uuid [NEWNODE_USE_UUID]
                        Use the local namespace UUID when generating new nodes
                        for ntriple structured literals. When there are
                        multiple input files, each input file gets its own
                        UUID. (default=False).
  --newnode-counter NEWNODE_COUNTER
                        The counter used to generate new nodes for ntriple
                        structured literals. (default=1).
  --newnode-zfill NEWNODE_ZFILL
                        The width of the counter used to generate new nodes
                        for ntriple structured literals. (default=0).
  --build-id [BUILD_ID]
                        Build id values in an id column. (default=False).
  --build-datatype-column [BUILD_DATATYPE_COLUMN]
                        When True, and --datatype-column-name
                        DATATYPE_COLUMN_NAME is not empty, build a column with
                        RDF datatypes. (default=False).
  --datatype-column-name DATATYPE_COLUMN_NAME
                        The name of the column with RDF datatypes.
                        (default=datatype).
  --validate [VALIDATE]
                        When true, validate that the result fields are good
                        KGTK file format. (default=False).
  --summary [SUMMARY]   When true, print summary statistics when done
                        processing (also implied by --verbose).
                        (default=False).
  --override-uuid OVERRIDE_UUID
                        When specified, override UUID generation for
                        debugging. (default=None).
  --write-namespaces WRITE_NAMESPACES
                        When true, append namespaces to the output file.
                        (default=True).
  --overwrite-id [optional true|false]
                        When true, replace existing ID values. When false,
                        copy existing ID values. When --overwrite-id is
                        omitted, it defaults to False. When --overwrite-id is
                        supplied without an argument, it is True.
  --verify-id-unique [optional true|false]
                        When true, verify ID uniqueness using an in-memory set
                        of IDs. When --verify-id-unique is omitted, it
                        defaults to False. When --verify-id-unique is supplied
                        without an argument, it is True.
  --value-hash-width VALUE_HASH_WIDTH
                        How many characters should be used in a value hash?
                        (default=6)
  --claim-id-hash-width CLAIM_ID_HASH_WIDTH
                        How many characters should be used to hash the claim
                        ID? 0 means do not hash the claim ID. (default=8)
  --claim-id-column-name CLAIM_ID_COLUMN_NAME
                        The name of the claim_id column. (default=claim_id)
  --id-separator ID_SEPARATOR
                        The separator user between ID subfields. (default=-)

  -v [optional True|False], --verbose [optional True|False]
                        Print additional progress messages (default=False).
```
### Files
There four categories of files:

#### Input files

The input files are listed after the `--input-files` option (the short form is `-i`).
Multiple files may be listed, and will be combined into a single output file.

The input files are not KGTK formatted files.  Here are a few lines from an ntriples file:
```
_:g12 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://tac.nist.gov/tracks/SM-KBP/2019/ontologies/InterchangeOntology#CompoundJustification> .
_:g12 <https://tac.nist.gov/tracks/SM-KBP/2019/ontologies/InterchangeOntology#confidence> _:g13 .
_:g13 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://tac.nist.gov/tracks/SM-KBP/2019/ontologies/InterchangeOntology#Confidence> .
_:g13 <https://tac.nist.gov/tracks/SM-KBP/2019/ontologies/InterchangeOntology#confidenceValue> "0.960368"^^<http://www.w3.org/2001/XMLSchema#double> .
_:g13 <https://tac.nist.gov/tracks/SM-KBP/2019/ontologies/InterchangeOntology#system> <http://www.isi.edu/compoundJustificationWrapper> .
_:g12 <https://tac.nist.gov/tracks/SM-KBP/2019/ontologies/InterchangeOntology#containedJustification> _:g14 .
_:g14 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://tac.nist.gov/tracks/SM-KBP/2019/ontologies/InterchangeOntology#TextJustification> .
_:g14 <https://tac.nist.gov/tracks/SM-KBP/2019/ontologies/InterchangeOntology#confidence> _:g15 .
_:g15 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://tac.nist.gov/tracks/SM-KBP/2019/ontologies/InterchangeOntology#Confidence> .
_:g15 <https://tac.nist.gov/tracks/SM-KBP/2019/ontologies/InterchangeOntology#confidenceValue> "9.60368e-01"^^<http://www.w3.org/2001/XMLSchema#double> .
_:g15 <https://tac.nist.gov/tracks/SM-KBP/2019/ontologies/InterchangeOntology#system> <http://www.rpi.edu> .
_:g14 <https://tac.nist.gov/tracks/SM-KBP/2019/ontologies/InterchangeOntology#endOffsetInclusive> "4076"^^<http://www.w3.org/2001/XMLSchema#int> .
_:g14 <https://tac.nist.gov/tracks/SM-KBP/2019/ontologies/InterchangeOntology#privateData> _:g16 .

```
 * There are four columns, which are separated by spaces.
   * There may be internal spaces in quoted strings.
 * The last column contains a period, which is ignored.
 * Columns may include blank nodes, beginning with "_:", which
   are file-local IDs.
 * Many fields contain URI identifiers, which often contain long, unchanging
   prefixes and shorted unique sections at the end.

Also, comments, beginning with `#`, may appear after the final period,
optionally preceeded by whitespace.  A comment extends from the `#` to
the end of the line.  Comments are used for documentation, such as in
this document, and are stripped on input.

```
_:g14 <https://tac.nist.gov/tracks/SM-KBP/2019/ontologies/InterchangeOntology#privateData> _:g16 . # This is a comment.
```

#### Output File

The output file contains data records have been converted into KGTK File Format.  Here is a sample of an output file:

```
XoBugQcoEt6xNnqGsHDXfTA:g12     rdf:type        ont:CompoundJustification
XoBugQcoEt6xNnqGsHDXfTA:g12     ont:confidence  XoBugQcoEt6xNnqGsHDXfTA:g13
XoBugQcoEt6xNnqGsHDXfTA:g13     rdf:type        ont:Confidence
XoBugQcoEt6xNnqGsHDXfTA:g13     ont:confidenceValue     0.960368
XoBugQcoEt6xNnqGsHDXfTA:g13     ont:system      noBugQcoEt6xNnqGsHDXfTA-4:compoundJustificationWrapper
XoBugQcoEt6xNnqGsHDXfTA:g12     ont:containedJustification      XoBugQcoEt6xNnqGsHDXfTA:g14
XoBugQcoEt6xNnqGsHDXfTA:g14     rdf:type        ont:TextJustification
XoBugQcoEt6xNnqGsHDXfTA:g14     ont:confidence  XoBugQcoEt6xNnqGsHDXfTA:g15
XoBugQcoEt6xNnqGsHDXfTA:g15     rdf:type        ont:Confidence
XoBugQcoEt6xNnqGsHDXfTA:g15     ont:confidenceValue     9.60368e-01
XoBugQcoEt6xNnqGsHDXfTA:g15     ont:system      noBugQcoEt6xNnqGsHDXfTA-1:
XoBugQcoEt6xNnqGsHDXfTA:g14     ont:endOffsetInclusive  4076
XoBugQcoEt6xNnqGsHDXfTA:g14     ont:privateData XoBugQcoEt6xNnqGsHDXfTA:g16
XoBugQcoEt6xNnqGsHDXfTA:g16     rdf:type        ont:PrivateData
XoBugQcoEt6xNnqGsHDXfTA:g16     ont:jsonContent "{\"fileType\":\"en\"}"
XoBugQcoEt6xNnqGsHDXfTA:g16     ont:system      rpi:fileType
XoBugQcoEt6xNnqGsHDXfTA:g14     ont:source      "HC00002Z8"
XoBugQcoEt6xNnqGsHDXfTA:g14     ont:sourceDocument      "HC00001DO"
XoBugQcoEt6xNnqGsHDXfTA:g14     ont:startOffset 4037
XoBugQcoEt6xNnqGsHDXfTA:g14     ont:system      noBugQcoEt6xNnqGsHDXfTA-1:
XoBugQcoEt6xNnqGsHDXfTA:g12     ont:system      noBugQcoEt6xNnqGsHDXfTA-4:compoundJustificationWrapper

```

At the end of the converted file:

```
gaia    prefix_expansion        "http://www.isi.edu/gaia/"
noBugQcoEt6xNnqGsHDXfTA-1       prefix_expansion        "http://www.rpi.edu"
noBugQcoEt6xNnqGsHDXfTA-2       prefix_expansion        "http://www.rpi.edu-projectToSingleton"
noBugQcoEt6xNnqGsHDXfTA-3       prefix_expansion        "https://tac.nist.gov/tracks/SM-KBP/2019/ontologies/LDCOntology#"
noBugQcoEt6xNnqGsHDXfTA-4       prefix_expansion        "http://www.isi.edu/"
noBugQcoEt6xNnqGsHDXfTA-5       prefix_expansion        "http://www.columbia.edu/ColumbiaSentiment/"
noBugQcoEt6xNnqGsHDXfTA-6       prefix_expansion        "http://www.columbia.edu/"
noBugQcoEt6xNnqGsHDXfTA-7       prefix_expansion        "www.isi.edu/"
noBugQcoEt6xNnqGsHDXfTA-8       prefix_expansion        "http://www.usc.edu/AIDA/IRIS/Systems/"
ont     prefix_expansion        "https://tac.nist.gov/tracks/SM-KBP/2019/ontologies/InterchangeOntology#"
rdf     prefix_expansion        "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
rpi     prefix_expansion        "http://www.rpi.edu/"
xml-schema-type prefix_expansion        "http://www.w3.org/2001/XMLSchema#"
```
 * The ntriples entries hav been converted into KGTK File Format.
 * Certain ntriples data types, such as numbers and some date/time formats, have been converted into KGTK data types.
 * The file-local IDs have had the "_ in replaced with a file-local UUID.
   * The UUID itself has been prefixed, here with "X", so it will be a
     KGTK symbol, not a KGTK number.
 * The long URIs have been converted into a prefix and suffix.
   * The prefixes are listed in "prefix_expansion" records at the en of the file.
   * Certain well-known URI families have preassigned, short prefixes
   * Other URI families have UUIDs, prefixed by "n", as the prefix
   * When `--build-new-namespaces=False`, only the prefixes read from
     the namespace file will be used, and nonmatching URLs will not have
     new prefixes assigned.  If the namespace file is not specified, or
     is empty, no new prefixes will be generated.

#### Reject File

If `kgtk import-ntriples` has problems inporting a record, the input record
may be recorded in a reject file.  The reject file has ntriples format, not KGTK File format.

#### URI Namespace Prefix Files

`kgtk import-ntriples` may be provided an input file, in KGTK FIle format,
containing predefined URI namespace prefix expansions.  Here is an example:

| node1 | label | node2 |
| -- | -- | -- |
| gaia | prefix_expansion | "http://www.isi.edu/gaia/" |
| rdf | prefix_expansion | "http://www.w3.org/1999/02/22-rdf-syntax-ns#" |
| ont | prefix_expansion | "https://tac.nist.gov/tracks/SM-KBP/2019/ontologies/InterchangeOntology#" |
| rpi | prefix_expansion | "http://www.rpi.edu/" |
| xml-schema-type | prefix_expansion | "http://www.w3.org/2001/XMLSchema#" |


`kgtk import-ntriples` may optionally write an updated namespace file.
This will facilitate converting a series of ntriples files.
The contents of the file will be the same as was shown fot the end
of the converted file in the output file section, above.

If there are prefix expansions in the namespace input file that are
not used in the import process, then by default they will be passed
through to a namespace output file, if one is specified, but not to
the main output file.  This can be controlled with the following
option, which is normally True:
```
--output-only-used-namespaces=False
```
When set to False, all namespace prefix expansions will be written
to the end of the main output file.

##### prefix_expansion Property

The following option controls the name of the property in which
URI namespace pefixes are stored.  The default value is "prefix_expansion",
as shown in the preceeding examples.
```
--prefix-expansion-label PREFIX_EXPANSION_LABEL
```

##### Lax URIs

The URI standard requires that URIs start with a schema, such as
"http:" or "https:". import-ntriples facilitates processing ntriples records that
do not strictly adhere to the standard, such as having just "www.isi.edu".
This enhancement is controlled with `--allow-lax-uri`, which defaults
to True.

```
  --allow-lax-uri [ALLOW_LAX_URI]
```


### URI Namespace Prefix Generation Controls

The following options control how namespaces are generated for URI
prefixes.

```
  --namespace-id-prefix NAMESPACE_ID_PREFIX
                        The prefix used to generate new namespaces. (default=n).
  --namespace-id-use-uuid [NAMESPACE_ID_USE_UUID]
                        Use the local namespace UUID when generating namespaces. When there are
                        multiple input files, each input file gets its own UUID.
                        (default=False).
  --namespace-id-counter NAMESPACE_ID_COUNTER
                        The counter used to generate new namespaces. (default=1).
  --namespace-id-zfill NAMESPACE_ID_ZFILL
                        The width of the counter used to generate new namespaces. (default=0).
  --build-new-namespaces [BUILD_NEW_NAMESPACES]
                        When True, create new namespaces. When False, use only
                        existing namespaces. (default=True).
  --write-namespaces WRITE_NAMESPACES
                        When true, append namespaces to the output file.
                        (default=True).
```

The order is <prefix><uuid>-<counter>, such as `noBugQcoEt6xNnqGsHDXfTA-7`.   By default,
the UUID is omitted, but the examples shown above were generated using the UUID.

When `--build-new-namespaces=FALSE`, new namespaces will not be generated.  If
the namespace file (`--namespace-file NAMESPACE_FILE`) is not specified or
is empty, URI prefixes will not be generated.

When `--write-namespaces=FALSE`, namespaces will not be written to the primary
output file.

### Language-Qualified Strings

ntriples files may contain language tags after literals.  For example:
```
<http://www.nima.puc-rio.br/lattes/1944208293448093#P690> <http://purl.org/dc/elements/1.1/title> "A Tunísia, o Egito e nós"@pt .
<http://www.nima.puc-rio.br/lattes/6322729232079325#P728> <http://purl.org/dc/elements/1.1/title> "Editorial"@en .

```

`kgtk import-ntriples` will convert the literals and language tags into KGTK language-qualified strings.

Note:  The [RDF N-Triples specification](https://www.w3.org/TR/n-triples/) allows more general
language tags than are currently allowed in the KGTK File Format Specification V2.
This could result in `kgtk import-ntriples --validate` reporting a failure.


### Structured Literal Imports

RDF 1.1 N-Triples files carry many data types as structured literals.  There are two portions
to each structured literal:  a value string, and a URI that identifies the data type.

`kgtk import-ntriples` can import the following ntriples data types to KGTK data types,
resulting in a single KGTK edge in the output file:

| ntriples URI | KGTK Data Type |
| ------------ | -------------- |
| <http://www.w3.org/2001/XMLSchema#boolean> | boolean |
| <http://www.w3.org/2001/XMLSchema#byte> | number |
| <http://www.w3.org/2001/XMLSchema#dateTime> | date-and-times |
| <http://www.w3.org/2001/XMLSchema#decimal> | number |
| <http://www.w3.org/2001/XMLSchema#double> | number |
| <http://www.w3.org/2001/XMLSchema#ENTITY> | string |
| <http://www.w3.org/2001/XMLSchema#float> | number |
| <http://www.w3.org/2001/XMLSchema#ID> | string |
| <http://www.w3.org/2001/XMLSchema#IDREF> | string |
| <http://www.w3.org/2001/XMLSchema#int> | number |
| <http://www.w3.org/2001/XMLSchema#integer> | number |
| <http://www.w3.org/2001/XMLSchema#language> | string |
| <http://www.w3.org/2001/XMLSchema#Name> | string |
| <http://www.w3.org/2001/XMLSchema#NCName> | string |
| <http://www.w3.org/2001/XMLSchema#negativeInteger> | number |
| <http://www.w3.org/2001/XMLSchema#NMTOKEN> | string |
| <http://www.w3.org/2001/XMLSchema#nonNegativeInteger> | number |
| <http://www.w3.org/2001/XMLSchema#nonPositiveInteger> | number |
| <http://www.w3.org/2001/XMLSchema#normalizedString> | string |
| <http://www.w3.org/2001/XMLSchema#positiveInteger> | number |
| <http://www.w3.org/2001/XMLSchema#short> | number |
| <http://www.w3.org/2001/XMLSchema#string> | string |
| <http://www.w3.org/2001/XMLSchema#token> | string |
| <http://www.w3.org/2001/XMLSchema#unsignedByte> | number |
| <http://www.w3.org/2001/XMLSchema#unsignedInt> | number |
| <http://www.w3.org/2001/XMLSchema#unsignedLong> | number |
| <http://www.w3.org/2001/XMLSchema#unsignedShort> | number |

The special RDF datatype `<http://www.w3.org/1999/02/22-rdf-syntax-ns#langString>` should
never explicitly appear in a RDF 1.1 N-Triples file.  However, we have observed files in the
wild that do use this datatype.  Using the `--allow-lang-string-datatype` and
`--lang-string-tag LANG_STRING_TAG` options, this datatype can be imported to
either the KGTK string or language-qualified string datatypes.

Other ntriples structured literals are processed by one of two methods:

 * When `--build-datatype-column=True`:
   * The value portion of the structured literal will be written as a string in
     the `node2` column of the edge in the KGTK output file.
   * A fourth column (by default, `datatype`) in the output edge will be filled with the datatype URI portion of the structured literal.
     * The outgoing URI is subject to URI prefix replacement, as described above.

 * Otherwise, the following steps will take place.
     * A new, unique node ID will be created.
     * The new new node ID will be substituted for the structured literal in the edge being imported,
     * An additional edge in the KGTK output file will be written with the value portion of the structured literal,
     * An additional edge in the KGTK output file will be written with the datatype URI portion of the structured literal.
       * The outgoing URI is subject to URI prefix replacement, as described above.

For example, if the following record appeared in the input file:
```
_:g38 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://tac.nist.gov/tracks/SM-KBP/2019/ontologies/InterchangeOntology#LDCTimeComponent> .
_:g38 <https://tac.nist.gov/tracks/SM-KBP/2019/ontologies/InterchangeOntology#day> "---19"^^<http://www.w3.org/2001/XMLSchema#gDay> .
_:g38 <https://tac.nist.gov/tracks/SM-KBP/2019/ontologies/InterchangeOntology#month> "--04"^^<http://www.w3.org/2001/XMLSchema#gMonth> .
_:g38 <https://tac.nist.gov/tracks/SM-KBP/2019/ontologies/InterchangeOntology#timeType> "ON"^^<http://www.w3.org/2001/XMLSchema#string> .
_:g38 <https://tac.nist.gov/tracks/SM-KBP/2019/ontologies/InterchangeOntology#year> "2014"^^<http://www.w3.org/2001/XMLSchema#gYear> .
```

Then the output might look like this when `--build-datatype-colum=False`:
```
JAABmv8vGfJZZasjV6DAXY:g38     rdf:type        ont:LDCTimeComponent
kgtk:nodeJAABmv8vGfJZZasjV6DAXY-1       kgtk:structured_value   "---19"
kgtk:nodeJAABmv8vGfJZZasjV6DAXY-1       kgtk:structured_uri     xml-schema-type:gDay
XJAABmv8vGfJZZasjV6DAXY:g38     ont:day kgtk:nodeJAABmv8vGfJZZasjV6DAXY-1
kgtk:nodeJAABmv8vGfJZZasjV6DAXY-2       kgtk:structured_value   "--04"
kgtk:nodeJAABmv8vGfJZZasjV6DAXY-2       kgtk:structured_uri     xml-schema-type:gMonth
XJAABmv8vGfJZZasjV6DAXY:g38     ont:month       kgtk:nodeJAABmv8vGfJZZasjV6DAXY-2
XJAABmv8vGfJZZasjV6DAXY:g38     ont:timeType    "ON"
kgtk:nodeJAABmv8vGfJZZasjV6DAXY-3       kgtk:structured_value   "2014"
kgtk:nodeJAABmv8vGfJZZasjV6DAXY-3       kgtk:structured_uri     xml-schema-type:gYear
XJAABmv8vGfJZZasjV6DAXY:g38     ont:year        kgtk:nodeJAABmv8vGfJZZasjV6DAXY-3
```

Then the output might look like this when `--build-datatype-colum=True`:
```
JAABmv8vGfJZZasjV6DAXY:g38     rdf:type        ont:LDCTimeComponent	
XJAABmv8vGfJZZasjV6DAXY:g38     ont:day "---19"	xml-schema-type:gDay
XJAABmv8vGfJZZasjV6DAXY:g38     ont:month       "--04"	xml-schema-type:gMonth
XJAABmv8vGfJZZasjV6DAXY:g38     ont:timeType    "ON"	xml-schema-type:string
XJAABmv8vGfJZZasjV6DAXY:g38     ont:year        "2014"	xml-schema-type:gYear
```

This process is controlled by the following command line options:
```
  --structured-value-label STRUCTURED_VALUE_LABEL
                        The label for value records for ntriple structured literals.
                        (default=kgtk:structured_value).
  --structured-uri-label STRUCTURED_URI_LABEL
                        The label for URI records for ntriple structured literals.
                        (default=kgtk:structured_uri).
  --newnode-prefix NEWNODE_PREFIX
                        The prefix used to generate new nodes for ntriple structured literals.
                        (default=kgtk:node).
  --newnode-use-uuid [NEWNODE_USE_UUID]
                        Use the local namespace UUID when generating new nodes for ntriple
                        structured literals. When there are multiple input files, each input
                        file gets its own UUID. (default=False).
  --newnode-counter NEWNODE_COUNTER
                        The counter used to generate new nodes for ntriple structured literals.
                        (default=1).
  --newnode-zfill NEWNODE_ZFILL
                        The width of the counter used to generate new nodes for ntriple
                        structured literals. (default=0).
  --build-datatype-column [BUILD_DATATYPE_COLUMN]
                        When True, and --datatype-column-name
                        DATATYPE_COLUMN_NAME is not empty, build a column with
                        RDF datatypes. (default=False).
  --datatype-column-name DATATYPE_COLUMN_NAME
                        The name of the column with RDF datatypes.
                        (default=datatype).
```

### ID Management

`kgtk import-ntriples` will optionally build a new ID column or populate an existing
ID column.

```
  --build-id [BUILD_ID]
                        Build id values in an id column. (default=False).
  --overwrite-id [optional true|false]
                        When true, replace existing ID values. When false, copy existing ID
                        values. When --overwrite-id is omitted, it defaults to False. When
                        --overwrite-id is supplied without an argument, it is True.
  --verify-id-unique [optional true|false]
                        When true, verify ID uniqueness using an in-memory set of IDs. When
                        --verify-id-unique is omitted, it defaults to False. When --verify-id-
                        unique is supplied without an argument, it is True.
```

### N-Triples Comments and White Space

Non-canonical RDF N-Triples files may contain optional comments at the end of each data line.
`kgtk import-ntriples` will strip any comments it encounters.  It also strips any non-canonical
white space (multiple adjacent white space characters).


Example comment:
```
_:g38 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://tac.nist.gov/tracks/SM-KBP/2019/ontologies/InterchangeOntology#LDCTimeComponent> .# comment
```

### KGTK File Format Validity

`kgtk import-ntriples` will, by default, add backslashes before any pipe characters (|)
it sees in the input data.

```
  --escape-pipes [ESCAPE_PIPES]
                        When true, input pipe characters (|) need to be escaped (\|) per KGTK
                        file format. (default=True).
```

It also has the option to validate the KGTK data that it generates, to guard against
unexpected import conversion failures.
```
  --validate [VALIDATE]
                        When true, validate that the result fields are good KGTK file format.
                        (default=False).
```
### Import Strategies

 * If you are importing a single file, which will be used in isolation, you may
   wish to forego local namespace (blank node) prefix conversion and forgo
   UUIDs in new nodes and namespace prefixes.
 * If you are importing many files which you intend to combine, you may consider
   converting them in a single command.
 * Otherwise, if you are importing many files, which are either:
   * too many to convert in a single command, and/or
   * not all available at once, then
   * You may wish to use full UUID options and updated namespace files
     for the conversion.

### Importing from Turtle Format

`kgtk import-ntriples` is designed to import edges from RDF 1.1 N-Triples files.
Another RDF representation is RDF 1.1 Turtle format.  Turtle format is more general
than N-Triples format, and `kgtk import-ntriples` does not support most of the
increased complexity of Turtle format.

One feature of Turtle format is the option to use either single quotes
(`'`) instead of double quotes (`"`) to quote literal values.
N-Triples format allows only double quotes (`"`). Turtle files that
differ from N-Triples files only by using single quotes may be
imported using the `--allow-turtle-quotes` option.

To convert Turtle files to N-triple files, the following should work
if the [graphy]( https://graphy.link) program is available:
```
cat dbpedia.ttl | graphy read -c ttl / tree / write -c ntriples > dbpedia.nt
```

## Examples

### Import with Default Settings

Import the entire given ntriple file into kgtk format, using default settings.

```
kgtk import-ntriples \
     -i ./examples/sample_data/aida/HC00001DO.ttl.nt\
     -o HC00001DO.tsv
```

### Import using UUIDs Extensively

Import the HC00001DO file, using UUIDs extensively:

```
kgtk import-ntriples \
     -i ./examples/sample_data/aida/HC00001DO.ttl.nt \
     -o HC00001DO.tsv \
     --reject-file HC00001DO-rejects.nt \
     --namespace-file examples/docs/import-ntriples-namespaces.tsv \
     --updated-namespace-file HC00001DO-namespaces.tsv \
     --namespace-id-use-uuid True \
     --newnode-use-uuid True
```

### Importing Strings

This example demonstrates importing three types of strings:
 * strings with an explicit datatype
 * strings with a language tag
 * strings with neither an explicit datatype nor a language tag
 * strings with various XMLSchema datatypes that cam be mapped to a KGTK string.

Here is the input N-Triples file:

```bash
cat examples/docs/import-ntriples-strings.nt
```

~~~
<http://example.org/vocab/show/218> <http://www.w3.org/2000/01/rdf-schema#label> "That Seventies Show"^^<http://www.w3.org/2001/XMLSchema#string> . # literal with XMLSchema string datatype
<http://example.org/vocab/show/218> <http://www.w3.org/2000/01/rdf-schema#label> "That Seventies Show" . # same again
<http://example.org/vocab/show/218> <http://www.w3.org/2000/01/rdf-schema#label> "That Seventies Show"@en . # literal with a language tag
<http://example.org/vocab/show/218> <http://www.w3.org/2000/01/rdf-schema#label> "That Seventies Show"^^<http://www.w3.org/2001/XMLSchema#normalizedString> . # literal with XMLSchema normalizedString datatype
<http://example.org/vocab/show/218> <http://www.w3.org/2000/01/rdf-schema#label> "That Seventies Show"^^<http://www.w3.org/2001/XMLSchema#token> . # literal with XMLSchema token datatype
<http://example.org/vocab/show/218> <http://www.w3.org/2000/01/rdf-schema#label> "That Seventies Show"^^<http://www.w3.org/2001/XMLSchema#language> . # literal with XMLSchema language datatype
<http://example.org/vocab/show/218> <http://www.w3.org/2000/01/rdf-schema#label> "That Seventies Show"^^<http://www.w3.org/2001/XMLSchema#Name> . # literal with XMLSchema Name datatype
<http://example.org/vocab/show/218> <http://www.w3.org/2000/01/rdf-schema#label> "That Seventies Show"^^<http://www.w3.org/2001/XMLSchema#NCName> . # literal with XMLSchema NCName datatype
<http://example.org/vocab/show/218> <http://www.w3.org/2000/01/rdf-schema#label> "That Seventies Show"^^<http://www.w3.org/2001/XMLSchema#ENTITY> . # literal with XMLSchema ENTITY datatype
<http://example.org/vocab/show/218> <http://www.w3.org/2000/01/rdf-schema#label> "That Seventies Show"^^<http://www.w3.org/2001/XMLSchema#ID> . # literal with XMLSchema ID datatype
<http://example.org/vocab/show/218> <http://www.w3.org/2000/01/rdf-schema#label> "That Seventies Show"^^<http://www.w3.org/2001/XMLSchema#IDREF> . # literal with XMLSchema IDREF datatype
<http://example.org/vocab/show/218> <http://www.w3.org/2000/01/rdf-schema#label> "That Seventies Show"^^<http://www.w3.org/2001/XMLSchema#NMTOKEN> . # literal with XMLSchema NMTOKEN datatype
~~~

Import this file:

```
kgtk import-ntriples \
     -i ./examples/docs/import-ntriples-strings.nt
```

| node1 | label | node2 |
| -- | -- | -- |
| n1:218 | n2:label | "That Seventies Show" |
| n1:218 | n2:label | "That Seventies Show" |
| n1:218 | n2:label | 'That Seventies Show'@en |
| n1:218 | n2:label | "That Seventies Show" |
| n1:218 | n2:label | "That Seventies Show" |
| n1:218 | n2:label | "That Seventies Show" |
| n1:218 | n2:label | "That Seventies Show" |
| n1:218 | n2:label | "That Seventies Show" |
| n1:218 | n2:label | "That Seventies Show" |
| n1:218 | n2:label | "That Seventies Show" |
| n1:218 | n2:label | "That Seventies Show" |
| n1:218 | n2:label | "That Seventies Show" |
| n1 | prefix_expansion | "http://example.org/vocab/show/" |
| n2 | prefix_expansion | "http://www.w3.org/2000/01/rdf-schema#" |

### Importing Numbers

There are various XMLSchema datatypes that may be imported to KGTK numbers.


Here is the input N-Triples file:

```bash
cat examples/docs/import-ntriples-numbers.nt
```

~~~
<http://example.org/vocab/show/218> <http://www.w3.org/2000/01/rdf-schema#label> "123.456"^^<http://www.w3.org/2001/XMLSchema#decimal> .
<http://example.org/vocab/show/218> <http://www.w3.org/2000/01/rdf-schema#label> "123"^^<http://www.w3.org/2001/XMLSchema#integer> .
<http://example.org/vocab/show/218> <http://www.w3.org/2000/01/rdf-schema#label> "123"^^<http://www.w3.org/2001/XMLSchema#int> .
<http://example.org/vocab/show/218> <http://www.w3.org/2000/01/rdf-schema#label> "123"^^<http://www.w3.org/2001/XMLSchema#short> .
<http://example.org/vocab/show/218> <http://www.w3.org/2000/01/rdf-schema#label> "123"^^<http://www.w3.org/2001/XMLSchema#byte> .
<http://example.org/vocab/show/218> <http://www.w3.org/2000/01/rdf-schema#label> "123"^^<http://www.w3.org/2001/XMLSchema#nonNegativeInteger> .
<http://example.org/vocab/show/218> <http://www.w3.org/2000/01/rdf-schema#label> "123"^^<http://www.w3.org/2001/XMLSchema#positiveInteger> .
<http://example.org/vocab/show/218> <http://www.w3.org/2000/01/rdf-schema#label> "123"^^<http://www.w3.org/2001/XMLSchema#unsignedLong> .
<http://example.org/vocab/show/218> <http://www.w3.org/2000/01/rdf-schema#label> "123"^^<http://www.w3.org/2001/XMLSchema#unsignedInt> .
<http://example.org/vocab/show/218> <http://www.w3.org/2000/01/rdf-schema#label> "123"^^<http://www.w3.org/2001/XMLSchema#unsignedShort> .
<http://example.org/vocab/show/218> <http://www.w3.org/2000/01/rdf-schema#label> "123"^^<http://www.w3.org/2001/XMLSchema#unsignedByte> .
<http://example.org/vocab/show/218> <http://www.w3.org/2000/01/rdf-schema#label> "-123"^^<http://www.w3.org/2001/XMLSchema#nonPositiveInteger> .
<http://example.org/vocab/show/218> <http://www.w3.org/2000/01/rdf-schema#label> "-123"^^<http://www.w3.org/2001/XMLSchema#negativeInteger> .
<http://example.org/vocab/show/218> <http://www.w3.org/2000/01/rdf-schema#label> "123.456e20"^^<http://www.w3.org/2001/XMLSchema#double> .
<http://example.org/vocab/show/218> <http://www.w3.org/2000/01/rdf-schema#label> "123.456e20"^^<http://www.w3.org/2001/XMLSchema#float> .
~~~

Import this file:

```
kgtk import-ntriples \
     -i ./examples/docs/import-ntriples-numbers.nt
```

| node1 | label | node2 |
| -- | -- | -- |
| n1:218 | n2:label | 123.456 |
| n1:218 | n2:label | 123 |
| n1:218 | n2:label | 123 |
| n1:218 | n2:label | 123 |
| n1:218 | n2:label | 123 |
| n1:218 | n2:label | 123 |
| n1:218 | n2:label | 123 |
| n1:218 | n2:label | 123 |
| n1:218 | n2:label | 123 |
| n1:218 | n2:label | 123 |
| n1:218 | n2:label | 123 |
| n1:218 | n2:label | -123 |
| n1:218 | n2:label | -123 |
| n1:218 | n2:label | 123.456e20 |
| n1:218 | n2:label | 123.456e20 |
| n1 | prefix_expansion | "http://example.org/vocab/show/" |
| n2 | prefix_expansion | "http://www.w3.org/2000/01/rdf-schema#" |

### Importing Booleans

The XML Schema boolean datatype has four possible values in an N-triples file:
 * true (or 1)
 * false (or 0)
 
Here is the input N-Triples file:

```bash
cat examples/docs/import-ntriples-booleans.nt
```

~~~
<http://example.org/vocab/show/218> <http://www.w3.org/2000/01/rdf-schema#label> "true"^^<http://www.w3.org/2001/XMLSchema#boolean> .
<http://example.org/vocab/show/218> <http://www.w3.org/2000/01/rdf-schema#label> "false"^^<http://www.w3.org/2001/XMLSchema#boolean> .
<http://example.org/vocab/show/218> <http://www.w3.org/2000/01/rdf-schema#label> "0"^^<http://www.w3.org/2001/XMLSchema#boolean> .
<http://example.org/vocab/show/218> <http://www.w3.org/2000/01/rdf-schema#label> "1"^^<http://www.w3.org/2001/XMLSchema#boolean> .
~~~

Import this file:

```
kgtk import-ntriples \
     -i ./examples/docs/import-ntriples-booleans.nt
```

| node1 | label | node2 |
| -- | -- | -- |
| n1:218 | n2:label | True |
| n1:218 | n2:label | False |
| n1:218 | n2:label | False |
| n1:218 | n2:label | True |
| n1 | prefix_expansion | "http://example.org/vocab/show/" |
| n2 | prefix_expansion | "http://www.w3.org/2000/01/rdf-schema#" |

### Importing Dates and Times

There are many XML Schema datatypes related to date/time representation.
Only the `dateTime` datatype is imported and converted to a KGTK date and
time at present.

Here is the input N-Triples file:

```bash
cat examples/docs/import-ntriples-dates.nt
```

~~~
<http://example.org/vocab/show/218> <http://www.w3.org/2000/01/rdf-schema#label> "2021-01-21T23:04:00"^^<http://www.w3.org/2001/XMLSchema#dateTime> .
~~~

Import this file:

```
kgtk import-ntriples \
     -i ./examples/docs/import-ntriples-dates.nt
```

| node1 | label | node2 |
| -- | -- | -- |
| n1:218 | n2:label | ^2021-01-21T23:04:00 |
| n1 | prefix_expansion | "http://example.org/vocab/show/" |
| n2 | prefix_expansion | "http://www.w3.org/2000/01/rdf-schema#" |

### Importing with `--allow-lang-string-datatype`

The RDF langString datatype corresponds to KGKT's language-qualified strings datatype.
RDF N-Triples langString literals must include a language tag (prefixed by `@`), and
may not include a datatype IRI (`^^<http://www.w3.org/1999/02/22-rdf-syntax-ns#langString>`).

However, DBpedia data dumps contains instances of the langString IRI, in spite of the
RDF 1.1 Turtle and N-Triples specifications.  To support this, the `--allow-lang-string-datatype`
option supports importing literals with langString IRIs as KGTK strings or KGTK language-qualified strings.


Here is the input N-Triples file:

```bash
cat examples/docs/import-ntriples-langstrings.nt
```

~~~
<http://example.org/vocab/show/218> <http://www.w3.org/2000/01/rdf-schema#label> "That Seventies Show"^^<http://www.w3.org/1999/02/22-rdf-syntax-ns#langString> .
~~~

Importing this file without `--allow-lang-string-datatype`:

```
kgtk import-ntriples \
     -i ./examples/docs/import-ntriples-langstrings.nt
```

| node1 | label | node2 |
| -- | -- | -- |
| n1 | prefix_expansion | "http://example.org/vocab/show/" |
| n2 | prefix_expansion | "http://www.w3.org/2000/01/rdf-schema#" |

Importing this file with `--allow-lang-string-datatype`:

```
kgtk import-ntriples \
     -i ./examples/docs/import-ntriples-langstrings.nt \
     --allow-lang-string-datatype
```

| node1 | label | node2 |
| -- | -- | -- |
| n1:218 | n2:label | "That Seventies Show" |
| n1 | prefix_expansion | "http://example.org/vocab/show/" |
| n2 | prefix_expansion | "http://www.w3.org/2000/01/rdf-schema#" |

### Importing with `--allow-lang-string-datatype` and `--lang-string-tag TAG`

To import a value with a langString IRI as a KGTK language-qualified string,
use the `--lang-string-tag TAG` option, where `TAG` is the language-qualified tag
(language and suffix).  Specifying an empty `TAG`, or a `TAG` of `-`, results in
the default behavior of importing the value as a KGTK string.

To import as English:

```
kgtk import-ntriples \
     -i ./examples/docs/import-ntriples-langstrings.nt \
     --allow-lang-string-datatype --lang-string-tag en
```

| node1 | label | node2 |
| -- | -- | -- |
| n1:218 | n2:label | 'That Seventies Show'@en |
| n1 | prefix_expansion | "http://example.org/vocab/show/" |
| n2 | prefix_expansion | "http://www.w3.org/2000/01/rdf-schema#" |

To import as Mexican Spanish:

```
kgtk import-ntriples \
     -i ./examples/docs/import-ntriples-langstrings.nt \
     --allow-lang-string-datatype --lang-string-tag es-MX
```

| node1 | label | node2 |
| -- | -- | -- |
| n1:218 | n2:label | 'That Seventies Show'@es-MX |
| n1 | prefix_expansion | "http://example.org/vocab/show/" |
| n2 | prefix_expansion | "http://www.w3.org/2000/01/rdf-schema#" |

To import as a KGTK string (the default behavior when `--lang-string-tag TAG`
is not specified):

```
kgtk import-ntriples \
     -i ./examples/docs/import-ntriples-langstrings.nt \
     --allow-lang-string-datatype --lang-string-tag -
```

| node1 | label | node2 |
| -- | -- | -- |
| n1:218 | n2:label | "That Seventies Show" |
| n1 | prefix_expansion | "http://example.org/vocab/show/" |
| n2 | prefix_expansion | "http://www.w3.org/2000/01/rdf-schema#" |

### Importing Without Generating New Namespace Prefixes

When `--build-new-namespaces=False`, only the prefixes read from
the namespace file will be used, and nonmatching URLs will not have
new prefixes assigned.  If the namespace file is not specified, or
s empty, no new prefixes will be generated.

Reusing the date/times input N-Triples file:

```bash
cat examples/docs/import-ntriples-dates.nt
```

~~~
<http://example.org/vocab/show/218> <http://www.w3.org/2000/01/rdf-schema#label> "2021-01-21T23:04:00"^^<http://www.w3.org/2001/XMLSchema#dateTime> .
~~~

Import this file, generating new namespace prefixes (the default setting):

```
kgtk import-ntriples \
     -i ./examples/docs/import-ntriples-dates.nt
```

| node1 | label | node2 |
| -- | -- | -- |
| n1:218 | n2:label | ^2021-01-21T23:04:00 |
| n1 | prefix_expansion | "http://example.org/vocab/show/" |
| n2 | prefix_expansion | "http://www.w3.org/2000/01/rdf-schema#" |

Import this file, without generating new namespace prefixes:

```
kgtk import-ntriples \
     -i ./examples/docs/import-ntriples-dates.nt \
     --build-new-namespaces=False
```

| node1 | label | node2 |
| -- | -- | -- |
| http://example.org/vocab/show/218 | http://www.w3.org/2000/01/rdf-schema#label | ^2021-01-21T23:04:00 |

Here is a namespace file with one entry for the `rdf-schema` namespace:

```
kgtk cat -i ./examples/docs/import-ntriples-rdf-schema-namespace.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| rdf-schema | prefix_expansion | "http://www.w3.org/2000/01/rdf-schema#" |

Importing the input file with the rdf-schema defined, but without
generating any additional namespace prefixes:

```
kgtk import-ntriples \
     -i ./examples/docs/import-ntriples-dates.nt \
     --namespace-file ./examples/docs/import-ntriples-rdf-schema-namespace.tsv \
     --build-new-namespaces=False
```

| node1 | label | node2 |
| -- | -- | -- |
| http://example.org/vocab/show/218 | rdf-schema:label | ^2021-01-21T23:04:00 |
| rdf-schema | prefix_expansion | "http://www.w3.org/2000/01/rdf-schema#" |


### Importing Without Writing Namespace Prefixes

When `--write-namespaces=False`, namespace prefixes will not be written to the
primary output file.

Reusing the date/times input N-Triples file:

```bash
cat examples/docs/import-ntriples-dates.nt
```

~~~
<http://example.org/vocab/show/218> <http://www.w3.org/2000/01/rdf-schema#label> "2021-01-21T23:04:00"^^<http://www.w3.org/2001/XMLSchema#dateTime> .
~~~

Import this file, writing namespace prefixes (the default setting):

```
kgtk import-ntriples \
     -i ./examples/docs/import-ntriples-dates.nt
```

| node1 | label | node2 |
| -- | -- | -- |
| n1:218 | n2:label | ^2021-01-21T23:04:00 |
| n1 | prefix_expansion | "http://example.org/vocab/show/" |
| n2 | prefix_expansion | "http://www.w3.org/2000/01/rdf-schema#" |

Import this file, without writing namespace prefixes:

```
kgtk import-ntriples \
     -i ./examples/docs/import-ntriples-dates.nt \
     --write-namespaces=False
```

| node1 | label | node2 |
| -- | -- | -- |
| n1:218 | n2:label | ^2021-01-21T23:04:00 |
| n1 | prefix_expansion | "http://example.org/vocab/show/" |
| n2 | prefix_expansion | "http://www.w3.org/2000/01/rdf-schema#" |

### Importing with `--summary`

The `--summary` option provides feedback on how many recods were processed,
such as the number of records read, how many were
rejected, and how many were output.

```
kgtk import-ntriples --summary \
     -i ./examples/docs/import-ntriples-langstrings.nt \
     -o ntriples-langstrings.tsv
```

The following summary is produced:

    Processed 1 known namespaces.
    Processed 1 records.
    Rejected 1 records.
    Wrote 2 records.
    Ignored 0 comments.
    Rejected 1 records with langString IRIs.
    Imported 0 records with unknown datatype IRIs.

Adding `--allow-lang-string-datatype`:

```
kgtk import-ntriples --summary \
     -i ./examples/docs/import-ntriples-langstrings.nt \
     -o ntriples-langstrings.tsv \
     --allow-lang-string-datatype
```

    Processed 1 known namespaces.
    Processed 1 records.
    Rejected 0 records.
    Wrote 3 records.
    Ignored 0 comments.
    Rejected 0 records with langString IRIs.
    Imported 0 records with unknown datatype IRIs.

### Importing with `--verbose`

The `--verbose` option provides feedback on how many recods which
were rejected.  It also procudes the `--summary` feedback.

```
kgtk import-ntriples --verbose \
     -i ./examples/docs/import-ntriples-langstrings.nt \
     -o ntriples-langstrings.tsv
```

The following summary is produced:

    Opening output file ntriples-langstrings.tsv
    File_path.suffix: .tsv
    KgtkWriter: writing file ntriples-langstrings.tsv
    header: node1	label	node2
    Opening the input file: examples/docs/import-ntriples-langstrings.nt
    Processed 1 known namespaces.
    Processed 1 records.
    Rejected 1 records.
    Wrote 2 records.
    Ignored 0 comments.
    Rejected 1 records with langString IRIs.
    Imported 0 records with unknown datatype IRIs.
