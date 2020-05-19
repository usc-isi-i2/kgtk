## KGTK File Format

**Authors:** Hans Chalupsky, Craig Milo Rogers, Pedro Szekely

**Contributors:** Daniel Garijo

**Version:** 2.0


KGTK uses a text-based, columnar file format that aims to be simple, readable, expressive, yet self-describing and easily generatable and parsable by standard tools.  The KGTK file design is focused on being able to represent arbitrary knowledge graphs, but can be used to describe any attributed, labeled or unlabeled hypergraph. 

## Basic File Structure
**Encoding**: KGTK files are text files that use UTF8 encoding for Unicode characters.

**Separator characters**: files are TAB-separated multi-column files, values containing TAB characters need to escape them with the \t escape sequence.

**Comments**: lines that begin with a #-sign are treated as comments and will be ignored, lines consisting of all whitespace will also be ignored.
Headers: the first line of each file is interpreted as a header line which needs to list the names of required and optional columns. Column names must be nonblank and unique within a file. Column names must be symbols. Column names should not contain quoted whitespace.

**Newlines and special characters**: each line ends with an end-of-line character or character sequence (such as CR, LF, or CR LF).  Text values that need to contain a newline character can encode them via `\n` and/or `\r`.  Other escape sequences mirroring those defined by Python are also supported.  Backslash can more generally be used to escape characters with special meaning, for example, `\|` to escape a vertical bar in a values list.  Leading and trailing whitespace in values other than inside quoted strings is disallowed.

**Columns and null values**: each file can have an arbitrary number of columns, however, the number of columns in each content line has to be constant across the file.  Specific required columns are described in more detail below.  Undefined values can be specified by the empty string which is a zero-length field (not the empty quoted string).

**Unordered rows**: Records in a KGTK file may appear in any order, and may be reordered freely, without changing their semantic meaning. Duplicate records may be created or removed without changing the semantic content of the file.  This means that comments and blank lines appearing in a KGTK source file may be removed by certain processing steps that cannot easily preserve them (e.g. with a sort or join operation).

## Representing Graphs
KGTK defines knowledge graphs (or more generally any attributed graph or hypergraph) as a set of nodes and a set of edges between those nodes.  KGTK represents everything of meaning via an edge.  Edges themselves can be attributed by having edges asserted about them, thus, KGTK can in fact represent arbitrary hypergraphs.  KGTK intentionally does not distinguish attributes or qualifiers on nodes and edges from full-fledged edges, tools operating on KGTK graphs can instead interpret edges differently if they so desire.  In KGTK, everything can be a node, and every node can have any type of edge to any other node.
 
Nodes are described in one or more node files, and edges in one or more edge files.  The resulting graph is built from the union of all loaded files.  There is some redundancy of representation between node and edge files.  In fact, all graphs can be described with just an edge file, and some graphs can be described with just a node file.  However, certain aspects can be described more concisely with a node file and others only with an edge file, thus both formats are available for use by an application. 
 
Nodes and edges must have unique IDs, however, IDs can be left implicit and will then be system generated.

## KGTK Data Types
KGTK represents data via nodes and edges between those nodes.  Since edges can themselves serve as nodes, those two sets are not disjoint.

KGTK uses two basic data types to represent nodes and edges: symbols and literals.  Symbols are names such as `Node42` or `a90b-bc8f`, literals are numbers or quoted strings, for example, `3.1415` or `“John Doe”`.  Both symbols and literals may contain internal whitespace (except for unescaped TABs and newline characters).

There is a third type we call structured (or fancy) literals, which are useful to concisely represent things such as dates or locations.  For example, `@043.26193/010.92708` represents the location with latitude `043.26193` and longitude `010.92708`.  However, this is just shorthand for a location node with latitude and longitude edges leading to those numeric values.

To allow us to easily specify (and parse) an object type without a verbose type declaration or other complex syntactic structure, we adopt the convention where the first character of a value tells us its data type.  The table below lists different sets of first characters and the data type they correspond to with some examples.

|First Character | Data Type | Examples|
|----------------|-----------|---------|
|0-9, +, -,.     | Number    |1, 42, 3.14e-10, 0.01, .1, 0xff|
|“ |String|“John Doe”
|^, @, ‘, !|Structured Literal|^10:30, ‘Deutsch’@de
|otherwise|Symbol|Node42, \0ob1
 
Note that in the last symbol example the special meaning of 0 was escaped with the backslash character (which does not itself become part of the symbol’s name).  Without that the value `0ob1` would be interpreted as an illegal octal numeric value.

## Predefined Names
KGTK comes with a small set of predefined column names and edge labels that either need to be used at certain positions in node or edge files, or that are used by KGTK to translate structured literals into their internal representation.  The table below lists those names together with their allowable aliases. Aliases are expensive to process; we may want to define a KGTK file profile that excludes aliases.
The presence of ID as an alias for id implies that the predefined names are sensitive to case We might want to consider making column names insensitive to case, although that can also cause processing inefficiencies.
If a predefined name or allowable alias appears as a column name, no other column name may appear from the same set of equivalent names.

|Predefined Name|Allowable Aliases|Description|
|---------------|-----------------|-----------|
|id|ID|Node and edge IDs|
|node1|from, subject|Start node of an edge|
|node2|to, object|End node of an edge|
|label|predicate, relation, relationship|Node or edge label
|source||Node or edge provenance|
|text, language||Field values for language-qualified strings|
|magnitude, tolerance, unit ||Field values for dimensioned numbers|
latitude, longitude||Field values for locations |
|year, month, day, hour, minute, second, nanosecond, timezone, precision||Field values for times and dates|

## Edge File Format

The edge file is the core representational structure for KGTK graphs.  Everything can be specified in the edge file or files.  Node files only provide a different point of view that makes the representation of node-centric information more concise.

Edge files specify the set of edges in a knowledge graph.  They have three mandatory columns: node1, label, and node2 (or their aliases).  The label might be left blank to represent unlabeled graphs[CMR: I am concerned that blank label values may cause syntactic (not semantic) confusion. I think it would be better to use a special value, such as _.], however, we will ignore lines with blank node1 or node2 (for us that does not correspond to unknown, just missing). [For processing efficiency, we might want to define an edge file profile that disallows comment lines, blank lines, and lines with blank node1 or node2 values.]

An optional edge ID field can be used to name an edge.  All additional columns have a user-defined meaning and are optional.  Here is a small example edge file:
```
node1   label       node2
N1      rdf:type    Person
N1      label       “Moe”
N2      rdf:type    Person
N2      label       “Larry”
N3      rdf:type    Person
N3      label       “Curly”
N1      brotherOf   N3
N1      friendOf    N2
N1      friendOf    N3
N1      diedAtAge   77
```

This file defines three nodes with types and respective labels (all specified via edges), and some relationships between them.  We used here an RDF-ish type label with an rdf: namespace prefix, but there is no requirement for that, any other label could have been used.  Similarly, type names such as Person could be prefixed with a namespace or use a full URI.  Multiple values as for N1’s friends can be specified via multiple entries or via a special list syntax described below.

Any symbol or literal can serve as a node ID or label, so another representation for this information would be the following:

```
node1      label            node2
“Moe”      rdf:type         Person
“Larry”    rdf:type         Person
“Curly”    rdf:type         Person
“Moe”      brotherOf        “Curly”
“Moe”      friendOf         “Larry”
“Moe”      friendOf         “Curly”
77         “death age of”   “Moe”
```

The meaning of a column is defined by its column header, so the order of columns does not matter.  The following would be an equivalent representation of the three node types:

```
label        node1        node2
rdf:type     “Moe”        Person
rdf:type     “Larry”      Person
rdf:type     “Curly”      Person
```

Additional columns can be used to specify edges about an edge.  For example:

```
node1       label       node2   creator     source      
“Moe”       rdf:type    Person  “Hans”      Wikipedia   
“Larry”     rdf:type    Person  “Hans”      Wikipedia
“Curly”     rdf:type    Person  “Hans”      Wikipedia
```

Each edge is uniquely identified by its (node1, label, node2) triple (ignoring the order in which these columns were specified in the file).  So, additional values about a particular edge can be added by repeating the edge and listing the value.  For example:

```
node1     label     node2   creator   source    
“Moe”     rdf:type  Person  “Hans”    Wikipedia
“Larry”   rdf:type  Person  “Hans”    Wikipedia
“Curly”   rdf:type  Person  “Hans”    Wikipedia
# we repeat the edge triple but only list additional
# values where they apply, other columns are left blank:
“Curly”   rdf:type  Person            IMDB
```
To allow us to use edges in both the node1 and node2 positions of an edge or to use them as arguments in an explicit node1/label/node2 triple, we can name or alias them via an explicit id column.  The names or aliases can then be used as stand-ins for the explicit triple.  For example:

```
node1     label     node2   creator   id
“Moe”     rdf:type  Person  “Hans”    E1
“Larry”   rdf:type  Person  “Hans”    E2
“Curly”   rdf:type  Person  “Hans”    E3
E1        source    Wikipedia
E2        source    Wikipedia
E3        source    Wikipedia
E3        source    IMDB
# the first creator edge is equivalent to this one:
E1      creator     “Hans”
```


Column values in the edges table are simply a shorthand for a more explicit line-based edge representation using edge IDs.  However, for edges without explicitly provided IDs, columns are the only way to say something about them.  Column values are only related to the edge they are modifying, they are not related or linked to each other in any way.

Columnar edges can themselves be named via IDs, for example:
```
node1     label     node2     creator     id
“Moe”     rdf:type  Person    “Hans”      E1
E1        creator   “Hans”                E11
```

Note that explicit IDs are simply aliases for the internal edge ID based on the triple, they do not replace that ID, they simply point to it.  In future versions of KGTK, we might allow edge IDs that are only unique within a file which is OK since they will point to a global ID based on the edge triple.  Since edge IDs are simply aliases, an edge can have multiple IDs defined for it, all pointing to the same triple ID.

## Multi-valued Edges
As shown above, multi-valued edges can be represented through separate entries in the edge table.  Alternatively, there is a list syntax available using the | separator.   For example, here is an alternative way to represent the multiple sources for one of the edges:

```
node1      label      node2     creator      source
“Curly”    rdf:type   Person    “Hans”       Wikipedia|IMDB
```

This representation is equivalent to the following:

```
node1       label       node2     creator     source
“Curly”     rdf:type    Person    “Hans”      Wikipedia
“Curly”     rdf:type    Person                IMDB
```
For value lists care must be taken that individual values must either do not contain vertical bars, or if they do, theythat they must be are escaped by backslash escape syntax.

List values will provide a valuable conciseness when records are viewed by humans. However, they may impost complexity on tools that use KGTK files. We may want to define a KGTK profile that excludes list values.

Multiple values are combined without ordering using a set semantics, duplicates will simply be ignored.

List values are not allowed in node1, label and node2 columns of the edge table.  This simplifies parsing and avoids edge IDs being associated with multiple edges.

## Unlabeled and Undirected Edges
Even though unusual for knowledge graphs, edges might be unlabeled to represent purely structural information more common in standard graph representations.  To represent an unlabeled edge, the label column in the edge file can simply be blank.  By default, edges are assumed to be directed from node1 to node2.  To represent a blank, undirected edge, the special predicate label _ (underscore) can be used.  To represent labeled but undirected edges, the edge label needs to start with an _ (underscore), for example, _brotherOf.
Node File Format
Node files allow a more concise node-centric specification of edges.  They have one mandatory column for the node ID (using the predefined name or its alias(es)).  Lines with blank node IDs are ignored. Node files must not contain a node1 column, in order to distinguish node files from edge files, which may contain an id column. We might want to disallow node2 columns from node files, too.All other columns are optional and specify edges where the identified node is node1.  Here is a small example that simply adds labels to our three nodes:

```
id      label     
N1      “Moe”
N2      “Larry”
N3      “Curly”
```

A minimal version of the nodes file above would only contain the id column (e.g., to communicate a set of nodes to some operation).  Here is a more elaborate example adding types, creators and sources:

```
id        label       rdf:type      creator        source
N1        “Moe”       Person        “Hans”        Wikipedia
N2        “Larry”     Person        “Hans”        Wikipedia
N3        “Curly”     Person        “Hans”        Wikipedia|IMDB
```

The equivalent edge file for the above looks like this.  Note that here the creator and source edges are on nodes and not on edges as in our previous examples:

```
node1     label       node2
N1        label       “Moe”
N1        rdf:type    Person
N1        creator     “Hans”
N1        source      Wikipedia
N2        label       “Larry”   
N2        rdf:type    Person
N2        creator     “Hans”
N2        source      Wikipedia
N3        label       “Curly”
N3        rdf:type    Person
N3        creator     “Hans”
N3        source      Wikipedia
N3        source      IMDB
```

This example illustrates that the node table is simply a slightly more concise, node-centric representation that is most useful for dense edges, that is, edges that have values for most or all nodes.

## Edge Collections and Graphs
KGTK does not have a specific graph type to collect or name sets of edges (different from RDF).  Instead, edges can be grouped by linking them to collection nodes using the same edge syntax as used for all other edges.  For example, the following edge table assigns the three type edges to the collection Stooges via a graph edge each:

```
node1     label     node2   graph     
“Moe”     rdf:type  Person  Stooges
“Larry”   rdf:type  Person  Stooges
“Curly”   rdf:type  Person  Stooges
```

There is nothing special about the label graph used for those edges, any other name could have been used (for example, memberOf).  The above corresponds to the following explicit edge representation:

```
node1     label     node2   id
“Moe”     rdf:type  Person  e1
“Larry”   rdf:type  Person  e2
“Curly”   rdf:type  Person  e3
e1        graph     Stooges
e2        graph     Stooges
e3        graph     Stooges
```


By defining collection or graph membership via explicit edges, edges can be in more than one graph.

To make it possible to define such membership edges about columnar edges, without having to list all of them explicitly, we introduce a special syntax `*<label>` that can be used in a node or edge file header.  The syntax means that all edges defined in a row by non-star syntax will be a node1 to the specified `<label>` edge.  For example:

```
node1       label     node2       source          *graph
“Moe”       rdf:type  Person      Wikipedia       Stooges
“Larry”     rdf:type  Person      Wikipedia       Stooges
“Curly”     rdf:type  Person      Wikipedia|IMDB  Stooges
```

The above corresponds to the following non-starred explicit edge representation which requires us to introduce edge IDs for the base edges so we can list the source edges explicitly:

```
node1       label       node2     id      source            graph
“Moe”       rdf:type    Person    e1      Wikipedia         Stooges
“Larry”     rdf:type    Person    e2      Wikipedia         Stooges
“Curly”     rdf:type    Person    e3      Wikipedia|IMDB    Stooges
e1          source      Wikipedia                           Stooges
e2          source      Wikipedia                           Stooges
e3          source      Wikipedia                           Stooges
e3          source      IMDB                                Stooges
```

In this table, the source column is now redundant, we just left it for continuity with the previous example.

Note that there could be multiple starred labels in a file header, but their edges get only introduced on edges from other non-starred labels, not on each other.  If an edge label starts with a * but should not be interpreted in this way, it can either be used in the explicit edge syntax or it can be escaped in the column header.

## Literals
Literals are used to represent data values such as  numbers, dimensioned quantities, times, locations, etc.  They can serve anywhere as node or edge IDs or even edge labels.

To make parsing simple, we use a scheme where the first character of a KGTK value indicates whether it is a symbol or literal, and if so what kind of literal. 

Numbers: dimensionless numeric values must start with a digit, `+`, `-`or decimal point and then follow standard fixed-point or scientific notation.  All legal numeric values allowed in Python (including binary, octal, hexadecimal and long integer values) are allowed.  Insignificant leading or trailing zeros are allowed.

Strings: unqualified strings are enclosed in double quotes, for example `“Foo”`.  Special characters such as newlines, quotes, etc. can be escaped with a backslash, for example, `“this is a \”weird\” st\|ring,\tno?\n”`

Booleans: we use two special symbols True and False to indicate boolean values.  They will be handled just like symbols but interpreted as booleans in contexts where that matters.

## Structured Literals
Structured (or fancy) literals are useful to concisely represent values such as dates or locations that have further internal structure.  For example, `@043.26193/010.92708` represents the location with latitude `043.26193` and longitude `010.92708`.  Structured literals are simply a shorthand that imply additional edges that do not need to be explicitly stated, for example, the latitude and longitude edges leading to the respective numeric values for a location.

**Language-qualified strings**: strings can be qualified with a language tag to indicate the human language used.  We use the RDF convention for this but single quotes to distinguish them from unqualified strings, for example, `‘Sprechen sie deutsch?’@de`.  Language tags are two-letter ISO 639-1 codes.  Example use in edge file:
```
node1       label     node2
N1          label     ‘Curly’@en
# implied edges:
‘Curly’@en  text      “Curly”
‘Curly’@en  language  “en”
```

**Quantities**: numbers can be dimensioned to represent quantities, e.g., a length such as 5 meters or a weight such as 10 pounds.  For quantities we use a variant of the Wikidata format amount~toleranceUxxxx.  A quantity starts with a number, followed by an optional tolerance interval, and then followed by either a combination of standard (SI) units (see Appendix) or a Wikidata node defining the unit, for example, Q11573 which indicates “meter”.  Here are some examples: `10m, +10m/s2, -1.2e+2[-1.0,+1.0]kg.m/s2, +17.2Q494083`

Example use in edge file:

```
node1     label     node2
N1        speed     10.2m/s2
# implied edges:
10.2m/s2  magnitude 10.2
10.2m/s2  unit      “m/s2”
```

**Location coordinates**: we also use the Wikidata format `@LAT/LON`, for example: `@043.26193/010.92708`

Example use in edge file:

```
node1                 label     node2
N1                    location    @043.26193/010.92708
# implied edges:
@043.26193/010.92708  latitude  043.26193
@043.26193/010.92708  longitude 010.92708
```

**Dates and times**: temporal literals are started with a ^ caret character (indicating the tip of a clock hand) and followed by an ISO 8601 date and an optional precision designator, for example: ^1839-00-00T00:00:00Z/9

Example use in edge file:

```
node1                 label     node2
N1                    time      ^2020-02-24T17:05:30
# implied edges:
^2020-02-24T17:05:30  year      2020
^2020-02-24T17:05:30  month     2
^2020-02-24T17:05:30  day       24
^2020-02-24T17:05:30  hour      17
^2020-02-24T17:05:30  minute    5
^2020-02-24T17:05:30  second    30
```

## Notes, Issues:
There is no support for calendar, we could allow it as an optional qnode after the precision designator, eg, `+1839-00-00T00:00:00Z/9/Q12138`
Here is a link to the TIMEX2 annotation format standardized during the DARPA ACE and TIDES programs: TIMEX2  The interesting parts are mostly part of the string that goes into the VAL attribute, page 13 and onwards.  This is probably overkill for what we want to do, but is good to have as a backup in case we run into limitations

Other types: we reserve the !-character as an extension type that will be followed by a literal and then a scheme or arbitrary type indicating the type of literal (inspired by RDF’s typed literals qualified by data type IRIs).  For example:  !P1..3W^timex3, !12345^^dbpedia:NewTaiwanDollar.  

The single-caret notation is to be used for special schemes such as “timex3” (as yet to be defined), which will expand into a special set of edges for this scheme.  For example, timex3 might use a superset of edges as used for date/time literals.

The double-caret notation is used for arbitrary typed literals.  These will always expand to a pair of value/type edges.  For example:

```
node1               label     node2
N1                  price     !1000^^dbpedia:USD
# implied edges:
!1000^^dbpedia:USD  value     1000
!1000^^dbpedia:USD  type      dbpedia:USD
```

## Object Identity
We have to define when two node or edge IDs or labels are the same, so KGTK can know when to add something to an existing node or edge, and when to create a new one.  The following rules apply:

All object types are mutually disjoint, that is, symbols can only be equal to symbols, numbers can only be equal to numbers, dimensioned numbers can only be equal to dimensioned numbers, etc.
Two symbols are the same if their names consist of the exact same sequence of characters (escape characters only used at the surface to support parsing are not counted).

Two literals are identical only if their surface syntax is identical, that is we do not require or assume any kind of normalization (which might be difficult to provide by some non-KGTK components and might also be ambiguous or lossy as for certain floating point numbers).  This means, for example, that 1, 1., 1.0, 01 are all considered to be different literals.  
Two structured literals are identical only if their surface syntax is identical, and again we do not require or assume any normalization.  This means, for example, that @043/053 and @043.0/053.0 are different locations, and similarly, 1m and 100cm while denoting the same length are considered different.

We might consider relaxing this in some form in the future to provide some form of normalization on literals, or to provide tools that would normalize literals according to some rules.

Edge IDs are based on the (node1, label, node2) triple describing an edge.  Two edge IDs are the same if and only if all their components are identical.
Possible Extensions

## Blank IDs
Node and edge IDs will generally have to be globally unique using some UUID standard to allow incremental loading of files without having to worry about name clashes.  Blank IDs (somewhat similar to RDF’s blank nodes) can be used to generate file-local unique IDs that will translate into globally unique IDs looking across files.  A blank ID is guaranteed to refer to the same object within a single node or edge file, but will not clash with the same ID used in a different file.  Blank IDs start with a :-character, for example, :b17.
