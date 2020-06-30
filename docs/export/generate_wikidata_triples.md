The `generate_wikidata_triples` command generates triple files from a kgtk file. The generated triple files can then be loaded into a triple store directly.

The triple generator reads a tab-separated kgtk file from standard input. The kgtk file is required to have at least the following 4 fields: `node1`, `label`, `node2` and `id`. The `node1` field is the subject; `label` is the predicate and `node2` is the object. 

## Usage
```{shell}
cat input.tsv | kgtk generate-wikidata-triples OPTIONS > output.ttl
```
or 
```
kgtk generate-wikidata-triples OPTIONS < input.tsv > output.ttl
```


The following tsv file is a minimal sample `input.tsv` file.

```
node1	label	node2	id
Q2140726727_mag_author	P6366	2140726727	id1
Q2140726727_mag_author	label	Zunyou Wu@en	id2
Q2140726727_mag_author	P1416	Q184490438_mag_affiliation	id3
Q184490438_mag_affiliation	label	Chinese Center For Disease Control And Prevention@en	id4
```
The generated triple file (without prefix) is below. The built-in prefix can be found [here](https://github.com/usc-isi-i2/etk/blob/master/etk/wikidata/__init__.py).

```
rdfs:label "Zunyou Wu"@en ;
schema:name "Zunyou Wu"@en ;
skos:prefLabel "Zunyou Wu"@en ;
p:P1416 wds:Q2140726727_mag_author-abcdefg ;
p:P6366 wds:Q2140726727_mag_author-abcdefg ;
wdt:P1416 wd:Q184490438_mag_affiliation ;
wdt:P6366 "2140726727"^^xsd:string .

```

`generate_wikidata_triples` currently supports qualifiers. Reuse the `id` of an edge as next edge's `node1`, then this next edge will be treated as a qualifier for previous edge. For example, the following sample input is legitmate.

```
node1 property  node2 id
Q1  P1  Q2	id1
id1 P2  Q3  id3
id1 P3  Q4  id4
Q2  P5  "string"@en id5
```

However, the following sample input is not legal and will be converted to incorrect triples..

```
node1 property  node2 id
Q1  P1  Q2	id1
id1 P2  Q3  id2
Q2  P5  "string"@en id3
id1 P3  Q4  id4
```
`generate_wikidata_triples` is **memoryless**, the qualifers has to follow the statement **immediately**. In the example above, the `id1` (in column `node1`) in 5th line will be treated as a new subject rather than an id of previous statement. Users should sort the kgtk file in a way such that qualifiers follow corresponding statement immediately. This can be done by creating meaningful ids.

## Options

- `--pf --property-types {str}`: path to the **property file** which contains the property datatype mapping in kgtk format. Default to **NONE**
- `-lp --label-property {str}`: property identifiers which will create labels, separated by comma','. Default to **label**.
- `-ap --alias-property {str}`: alias identifiers which will create labels, separated by comma','. Default to **aliase**.
- `-dp --description-property {str}`: description identifiers which will create labels, separated by comma','. Default to **description**.
- `-gt --generate-truthy {bool}`: the default is to not generate truthy triples. Specify this option to generate truthy triples. Default to **yes**.
- `-w --warning {bool}`: if set to yes, warn various kinds of exceptions and mistakes and log them to a log file with line number in input file. Default to **no**.
- `-n --output-n-lines {number}`: output triples approximately every {n} lines of reading stdin. Default to **1000**.
- `-gz --use-gz {bool}`: if set to yes, read from compressed gz file. Default to **no**.
- `-sid --use-id {bool}`: if set to yes, the id in the edge will be used as statement id when creating statement or truthy statement. Default to **no**.
- `-log --log-path {str}`: set the path of the log file. Default to **warning.log**.
- `-pd --property-declaration-in-file {bool}`: wehther read properties in the kgtk file. If set to yes, use `cat input.tsv input.tsv` to pipe the input file twice. Default to **no**.

### Shared Options

- `--debug` run the command in debug mode.

## Explanation of Options

### **--property-types** 

If set to true, read proprty data_type information from the property file following the format below. It is also a kgtk file. Here is an example file `example_prop.tsv`

```
node1	label	node2
P493	property_type	external-identifier
P494	property_type	external-identifier
P495	property_type	item
P496	property_type	external-identifier
P497	property_type	external-identifier
P498	property_type	external-identifier
P500	property_type	item
P501	property_type	item
P502	property_type	string
```

The header line is necessary. If property *P493* is used in the input kgtk file, then the edge `P493	data_value	external-identifier` must exists in the `example_prop.tsv` to tell triple generator that the object of `P493` is an `external-identifier`. On another hand If `p495` is used in the input kgtk file, then the object of `P495` will be treated as an entity.

Currently the following datatypes are supported. The complete list of possible data types can be found [here](https://www.wikidata.org/wiki/Help:Data_type).

1. Item 
2. Quantity
3. Globe-coordinate
4. Time 
5. Monolingualtext 
6. Url 
7. External identifier 
8. String
9. Property

In ETK, the possible property types are defined [here](https://github.com/usc-isi-i2/etk/blob/9c79a597fa0917b4e4bf78b4acbd863f5a0bb917/etk/wikidata/value.py#L190).

### truthy

If `-gt --generate-truthy` set to `True`, the statement will be truthy. Truthy statements will have an additional spo with propert prefix `wdt`.

### warning

If set to yes, triple generation errors according to specific line will be written to the `warning.log` file or specified path by `-log`.

### n

`n` controls after how many lines of reading the standard input, To achieve optimal performance, you can set n larger to reduce overhead of creating knowledge graph object and frequent serialization. However, large n also requires larger memory.

### gz

Use compressed file as input.

### use-id

If `--use-id` is set to true, the `id` column of the kgtk file will be used as the statement id if the corresponding edge is a statement edge. It is the user's responsiblity to make sure there is no duplicated statement id across the whole knowledge graph then.

### log-path

If using `-log`, the warning `-w` must be set to true.

### property-declaration-in-file

If set to yes, besides reading properties from property file, the generator will read from the input stream to find new properties. The user MUST use `cat input.tsv input.tsv | kgtk generate_wikidata_triples`.  


## How triple generator handles different types of edges

### label, aliases and descriptions

**-lp**, **-ap**, **-dp** defines properties that triple generator should identify as label, description or aliases creation. There can be multiple choices separated by `,`.

For example, if you have `-ap aliases,alias`, then when the following edge is met, both `Alice` and `Alicia` will be treated as aliases to the node `q2020`.

```
node1	property	node2	id
q2020	aliases	Alice@en	id1
q2020	alias	Alicia@sp	id2
```

Another example for `label`:

```
Q123 label ‘Hello’@en
```

The triple will be:

```
wd:Q123 rdfs:label "Hello"@en . 
wd:Q123 skos:prefLabel "Hello"@en . 
wd:Q123 schema:name "Hello"@en .
```

`label` should be unique for the **same** language.

### Property declaration in input kgtk file

User can also define properties in the input kgtk file with the following syntax. The `data_type` syntax indicates a new property is defined. Note that any usage of `P20200101` must appear after the definition in the kgtk file or `P20200101` will be incorrectly treated as `item`.

```
P20200101 data_type string
```

### Regular Edges

Regular edges will be generated according to the data type of the property defined in the property file.

## Examples

### Standard Usage

1. If properties are **only** defined in `example_prop.tsv`

```bash

kgtk generate_wikidata_triples -pf example_prop.tsv -w yes < input_file.tsv > output_file.ttl

```

2. If properties are **only** defined in `input_file.tsv`

```bash

cat input_file.tsv input_file.tsv | kgtk generate_wikidata_triples -w yes -pd yes > output_file.ttl

```
1. If properties are defined in both files.

```bash
cat input_file.tsv input_file.tsv | kgtk generate_wikidata_triples -pf example_prop.tsv -w yes -pd yes > output_file.ttl
```


### Parallel Usage

You can split the input files into several smaller pieces and run the command simultaneuously. 

Let's say you are in a directory which contains the `tsv` files. The following command will generate the `ttl` files with the same file name. 

```bash
ls *tsv | parallel -j+0 --eta 'kgtk generate_wikidata_triples -pf example_props.tsv -n 1000 --debug -gt yes < {} > {.}.ttl'
```

Splitting a large tsv file into small tsv files directly may make qualifier edges statementless and cause serious mistake. **Do** make sure the splited files start with an statement edge rather than qualifier edge. The header `node1 label node2 id` needs to be inserted back at the beginning of splited files as well.


## Branch specific features not yet in dev


#### enhancement/triple_uri

Additional options enable the customization of uri prefix.

- `-prefix --prefix-file {path}` a path to the prefix kgtk file that contains the mapping information.

Below is a sample `prefix.tsv` file.
```
node1	bound	node2
p	bound_to	https://w3id.org/datamart/
pr	bound_to	https://w3id.org/datamart/
wd	bound_to	https://w3id.org/datamart/
```

To use it:

```bash
cat input.tsv | kgtk generate_wikidata_triples -prefix prefix.tsv -pf prop_file.tsv -w yes --debug -n 1000
```
