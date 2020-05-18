This command will generate wikidata triples from two edge files:

- A statement and qualifier edge file that contains an edge id, node1, label, and node2
- A kgtk file that contains the mapping information from property identifier to its datatype

## Usage

```bash
KGTK generate_wikidata_triples OPTIONS
```
**OPTIONS**:

`--uri-prefix {string}`: in this version we will use the wikidata prefixes. In a future version we will allow the user to specify a prefix.

`--label-property {p1, p2, ...}`: the properties that will produce Wikidata labels

`--alias-property {p1, p2, …}`: the properties that will produce Wikidata aliases

`--description-property {p1, p2, …}`: the properties that will produce Wikidata descriptions

`--property-types {file}`: a file that provides the type of each property present in the edge file 

`--generate-truthy`: the default is to not generate truthy triples. Specify this option to generate truthy triples (future version)

`--ignore {yes|no}` :  if set to yes, ignore various kinds of exceptions and mistakes and log them to a log file with line number in input file, rather than stopping.

`--output-n-lines: {int}`: output triples approximately every N lines of reading stdin. Because of the calling of ETK API, it is inefficient or impossible (consider potential statementless qualifier edge) to pipe after reading/processing every line. Set this number to improve the efficiency and the algorithm will make sure there is no stateless qualifier. Note that different n may give slightly different output if label edge, description edge and alias edges happen to be splitted.  

`--generate-truthy -gt {yes|no}` If Set to true, generate the truthy statements

`--line-by-line -lbl {yes|no}`

`--use-gz -gz {yes|no}`


## Properties File
The properties file is an edge file with the following format:
```
node1   label           node2
P1      property_type   item
P2      property_type   quantity
```

The type of a property is called datatype in the json dump. 

The code supports several data type: External identifier and URLValue. Currently the code support 8 property types:

1- Item
2- Quantity
3- Globe-coordinate
4- Time
5- Monolingualtext
6- Url
7- External identifier
8- String

Note: for now, the prop_types.tsv must use the following node2 column values to specify the property type. For example, globe_coordinate will be illegal. It must be globe-coordinate.

```
node1   label               node2
P1      property_type       item
P2      property_type       quantity
P3      property_type       globe-coordinate
P4      property_type       time
P5      property_type       monolingualtext
P6      property_type       string
P7      property_type       url
P8      property_type       external-identifier
```

In ETK the possible property types are defined in 
```
class Datatype(Enum):
    Item = Item
    Property = Property
    ExternalIdentifier = ExternalIdentifier
    QuantityValue = QuantityValue
    TimeValue = TimeValue
    StringValue = StringValue
    URLValue = URLValue
    GlobeCoordinate = GlobeCoordinate
    MonolingualText = MonolingualText
```

## Handling Different Types Of Edges

### Label Properties
This case applies to all edge labels in the label-property option. For example:
```
Q123     label     ‘Hello’@en
```

Expected output that ETK should generate:
```
 wd:Q123 rdfs:label     "Hello"@en .
 wd:Q123 skos:prefLabel "Hello"@en .
 wd:Q123 schema:name    "Hello"@en .
```

Note: should check that there is a single label statement for each language.


### Alias Properties
This case applies to all edge labels in the alias-property option. For example:
```
Q123    alias   ‘Howdy’@en
Q123    alias   ‘Hola’@sp
```
Expected output that ETK should generate:

```
 wd:Q123 skos:altLabel "Howdy"@en .
 wd:Q123 skos:altLabel "Hola"@sp .
```

### Description Properties
This case applies to all edge labels in the description-property option. For example:

```
Q123    description     ‘A form of salutation’@en
Q123    description     ‘Saludo’@sp
```

Expected output that ETK should generate:

```
 wd:Q123 schema:description "A form of salutation"@en .
 wd:Q123 schema:description "Saludo"@sp .
```

### Property Declarations
This case applies to edges whose type is property. For example:

Obtain additional property_type information from property_types.tsv to enhance the output.
```
P22     type    property
```

Expected output that ETK should generate:

```
  wd:P22 a wikibase:Property ;
     wikibase:directClaim wdt:P22 ;
     wikibase:claim p:P22 ;
     wikibase:statementProperty ps:P22 ;
     wikibase:statementValue psv:P22 ;
     wikibase:qualifier pq:P22 ;
     wikibase:qualifierValue pqv:P22 ;
     wikibase:reference pr:P22 ;
     wikibase:referenceValue prv:P22 ;
     wikibase:novalue wdno:P22 .
```

## Regular Edges
This case applies to edges not covered by the previous cases. For example:
```
Q3  P2  Q123
Q3  P7  123[-1.0,+1.0]
Q3  P7  89
```

Expected output that ETK should generate. The highlighted parts are created when the truthy option is set to “yes”.
```
  wd:Q3 
     wdt:P7 "value1", "value2" ;
     wdt:P2 wd:Q3 ;
     p:P2 wds:Q3-4cc1f2d1-490e-c9c7-4560-46c3cce05bb7 ;
     p:P7 wds:Q3-24bf3704-4c5d-083a-9b59-1881f82b6b37,
          wds:Q3-45abf5ca-4ebf-eb52-ca26-811152eb067c .
```

The triples generated for each statement depend on the property type of the property. ETK has an API to handle all the different types of property values. Here are some examples taken from the RDF Dump Format page in the Wikidata documentation.

```
wds:Q3-24bf3704-4c5d-083a-9b59-1881f82b6b37 a wikibase:Statement, wikibase:BestRank ;
     ps:P7 "123"^^xsd:decimal ;
     psv:P7 wdv:382603eaa501e15688076291fc47ae54 ;
     psn:P7 wdv:85374998f22bda54efb44a5617d76e51 .

 wdv:382603eaa501e15688076291fc47ae54 a wikibase:QuantityValue ;
     wikibase:quantityAmount "+123"^^xsd:decimal ;
     wikibase:quantityUpperBound "+124"^^xsd:decimal ;
     wikibase:quantityLowerBound "+122"^^xsd:decimal ;
     wikibase:quantityUnit <http://www.wikidata.org/entity/Q218593> ;
     wikibase:quantityNormalized wdv:85374998f22bda54efb44a5617d76e51.
```






