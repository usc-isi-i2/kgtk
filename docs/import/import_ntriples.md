This command will import one or more ntriple files into KGTK format.


## Usage
```
usage: kgtk import-ntriples [-h] [-i INPUT_FILE [INPUT_FILE ...]] [-o OUTPUT_FILE]
                            [--reject-file REJECT_FILE] [--namespace-file NAMESPACE_FILE]
                            [--updated-namespace-file NAMESPACE_FILE]
                            [--namespace-id-prefix NAMESPACE_ID_PREFIX]
                            [--namespace-id-use-uuid [NAMESPACE_ID_USE_UUID]]
                            [--namespace-id-counter NAMESPACE_ID_COUNTER]
                            [--namespace-id-zfill NAMESPACE_ID_ZFILL]
                            [--output-only-used-namespaces [OUTPUT_ONLY_USED_NAMESPACES]]
                            [--allow-lax-uri [ALLOW_LAX_URI]]
                            [--local-namespace-prefix LOCAL_NAMESPACE_PREFIX]
                            [--local-namespace-use-uuid [LOCAL_NAMESPACE_USE_UUID]]
                            [--prefix-expansion-label PREFIX_EXPANSION_LABEL]
                            [--structured-value-label STRUCTURED_VALUE_LABEL]
                            [--structured-uri-label STRUCTURED_URI_LABEL]
                            [--newnode-prefix NEWNODE_PREFIX]
                            [--newnode-use-uuid [NEWNODE_USE_UUID]]
                            [--newnode-counter NEWNODE_COUNTER]
                            [--newnode-zfill NEWNODE_ZFILL] [--build-id [BUILD_ID]]
                            [--escape-pipes [ESCAPE_PIPES]] [--validate [VALIDATE]]
                            [--override-uuid OVERRIDE_UUID]
                            [--overwrite-id [optional true|false]]
                            [--verify-id-unique [optional true|false]] [-v]

Import an ntriples file, writing a KGTK file.

Additional options are shown in expert help.
kgtk --expert import-ntriples --help

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE [INPUT_FILE ...], --input-file INPUT_FILE [INPUT_FILE ...]
                        The ntriples file(s) to import. (May be omitted or '-' for stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for stdout.)
  --reject-file REJECT_FILE
                        The ntriples output file for records that are rejected. (Optional,
                        use '-' for stdout.)
  --namespace-file NAMESPACE_FILE
                        The KGTK input file with known namespaces. (Optional, use '-' for
                        stdin.)
  --updated-namespace-file NAMESPACE_FILE
                        The KGTK output file with updated namespaces. (Optional, use '-' for
                        stdout.)
  --namespace-id-prefix NAMESPACE_ID_PREFIX
                        The prefix used to generate new namespaces. (default=n).
  --namespace-id-use-uuid [NAMESPACE_ID_USE_UUID]
                        Use the local namespace UUID when generating namespaces. When there
                        are multiple input files, each input file gets its own UUID.
                        (default=False).
  --namespace-id-counter NAMESPACE_ID_COUNTER
                        The counter used to generate new namespaces. (default=1).
  --namespace-id-zfill NAMESPACE_ID_ZFILL
                        The width of the counter used to generate new namespaces.
                        (default=0).
  --output-only-used-namespaces [OUTPUT_ONLY_USED_NAMESPACES]
                        Write only used namespaces to the output file. (default=True).
  --allow-lax-uri [ALLOW_LAX_URI]
                        Allow URIs that don't begin with a http:// or https://.
                        (default=True).
  --local-namespace-prefix LOCAL_NAMESPACE_PREFIX
                        The namespace prefix for blank nodes. (default=X).
  --local-namespace-use-uuid [LOCAL_NAMESPACE_USE_UUID]
                        Generate a UUID for the local namespace. When there are multiple
                        input files, each input file gets its own UUID. (default=True).
  --prefix-expansion-label PREFIX_EXPANSION_LABEL
                        The label for prefix expansions in the namespace file.
                        (default=prefix_expansion).
  --structured-value-label STRUCTURED_VALUE_LABEL
                        The label for value records for ntriple structured literals.
                        (default=kgtk:structured_value).
  --structured-uri-label STRUCTURED_URI_LABEL
                        The label for URI records for ntriple structured literals.
                        (default=kgtk:structured_uri).
  --newnode-prefix NEWNODE_PREFIX
                        The prefix used to generate new nodes for ntriple structured
                        literals. (default=kgtk:node).
  --newnode-use-uuid [NEWNODE_USE_UUID]
                        Use the local namespace UUID when generating new nodes for ntriple
                        structured literals. When there are multiple input files, each input
                        file gets its own UUID. (default=False).
  --newnode-counter NEWNODE_COUNTER
                        The counter used to generate new nodes for ntriple structured
                        literals. (default=1).
  --newnode-zfill NEWNODE_ZFILL
                        The width of the counter used to generate new nodes for ntriple
                        structured literals. (default=0).
  --build-id [BUILD_ID]
                        Build id values in an id column. (default=False).
  --escape-pipes [ESCAPE_PIPES]
                        When true, input pipe characters (|) need to be escaped (\|) per
                        KGTK file format. (default=True).
  --validate [VALIDATE]
                        When true, validate that the result fields are good KGTK file
                        format. (default=False).
  --override-uuid OVERRIDE_UUID
                        When specified, override UUID generation for debugging.
                        (default=None).
  --overwrite-id [optional true|false]
                        When true, replace existing ID values. When false, copy existing ID
                        values. When --overwrite-id is omitted, it defaults to False. When
                        --overwrite-id is supplied without an argument, it is True.
  --verify-id-unique [optional true|false]
                        When true, verify ID uniqueness using an in-memory set of IDs. When
                        --verify-id-unique is omitted, it defaults to False. When --verify-
                        id-unique is supplied without an argument, it is True.

  -v, --verbose         Print additional progress messages (default=False).
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
   * The UUID itself has been prefixed, here isht "X", so it will be a
     KGTK symbol, not a KGTK number.
 * The long URIs have been converted into a prefix and suffix.
   * The prefixes are listed in "prefix_expansion" records at the en of the file.
   * Certain well-known URI families have preassigned, short prefixes
   * Other URI families have UUIDs, prefixed by "n", as the prefix

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

The URI standard requires that URIs staart with a schema, such as
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
```

The order is <prefix><uuid>-<counter>, such as `noBugQcoEt6xNnqGsHDXfTA-7`.   By default,
the UUID is omitted, but the examples shown above were generated using the UUID.

### Structured Literal Imports

ntriples files carry many data types as structured literals.  There are two portions
to each structured literal:  a value string, and a URI that identifies the data type.

`kgtk import-ntriples` can import the following ntriples data types to KGTK data types,
resulting in a single KGTK edge in the output file:

| ntriples URI | KGTK Data Type |
| ------------ | -------------- |
| <http://www.w3.org/2001/XMLSchema#string> | string |
| <http://www.w3.org/2001/XMLSchema#int> | number |
| <http://www.w3.org/2001/XMLSchema#double> | number |
| <http://www.w3.org/2001/XMLSchema#float> | number |
| <http://www.w3.org/2001/XMLSchema#decimal> | number |
| <http://www.w3.org/2001/XMLSchema#boolean> | boolean |
| <http://www.w3.org/2001/XMLSchema#dateTime> | date-and-times |

Other ntriples structured literals are processed by:
 * creating a new, unique node ID,
 * substituting the new node ID for the structured literal in the edge being imported,
 * writing an addional edge in the KGTK output file with the value portion of the structured literal,
 * and writing an addional edge in the KGTK output file with the data type URI portion of the structured literal.
   * The outgoing URI is subject to URI prefix replacement, as described above.

For example, if the following record appeared in the input file:
```
_:g38 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://tac.nist.gov/tracks/SM-KBP/2019/ontologies/InterchangeOntology#LDCTimeComponent> .
_:g38 <https://tac.nist.gov/tracks/SM-KBP/2019/ontologies/InterchangeOntology#day> "---19"^^<http://www.w3.org/2001/XMLSchema#gDay> .
_:g38 <https://tac.nist.gov/tracks/SM-KBP/2019/ontologies/InterchangeOntology#month> "--04"^^<http://www.w3.org/2001/XMLSchema#gMonth> .
_:g38 <https://tac.nist.gov/tracks/SM-KBP/2019/ontologies/InterchangeOntology#timeType> "ON"^^<http://www.w3.org/2001/XMLSchema#string> .
_:g38 <https://tac.nist.gov/tracks/SM-KBP/2019/ontologies/InterchangeOntology#year> "2014"^^<http://www.w3.org/2001/XMLSchema#gYear> .
```

Then the output might look like this:
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

### Examples

Import the entire given ntriple file into kgtk format, using default settings.

```
kgtk import-ntriples -i dbpedia_wikipedia_links.nt -o DbpediaWikipediaLinks.tsv
```

Import the HC00001DO file, using UUIDs extensively:

```
kgtk import-ntriples \
     -i ../../HC00001DO.nt \
     -o HC00001DO.tsv \
     --reject-file HC00001DO-rejects.nt \
     --namespace-file kgtk/join/test/initial-ntriple-namespaces.tsv \
     --updated-namespace-file HC00001DO-namespaces.tsv \
     --namespace-id-use-uuid True \
     --newnode-use-uuid True \
```
