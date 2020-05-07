## The generate_wikidata_triples command converts a kgtk file to a ttl file that can be loaded into a wikidata Blazegraph.

The triple generator take a tab-separated kgtk file from standard input.
```
node1	property	node2	id
Q2140726727_mag_author	P6366	2140726727	id1
Q2140726727_mag_author	label	Zunyou Wu@en	id2
Q2140726727_mag_author	P1416	Q184490438_mag_affiliation	id3
Q184490438_mag_affiliation	label	Chinese Center For Disease Control And Prevention@en	id4
```
to an rdf file like this.

```
rdfs:label "Zunyou Wu"@en ;
schema:name "Zunyou Wu"@en ;
skos:prefLabel "Zunyou Wu"@en ;
p:P1416 wds:Q2140726727_mag_author-abcdefg ;
p:P6366 wds:Q2140726727_mag_author-abcdefg ;
wdt:P1416 wd:Q184490438_mag_affiliation ;
wdt:P6366 "2140726727"^^xsd:string .

```


## Required Option

- `--pf --property-types {path}`: path to the file which contains the property datatype mapping in kgtk format.

## Optional Options

- `-lp --label-property {str}`: property identifiers which will create labels, separated by comma','. Default to **label**.
- `-ap --alias-property {str}`: alias identifiers which will create labels, separated by comma','. Default to **aliases**.
- `-dp --description-property {str}`: description identifiers which will create labels, separated by comma','. Default to **descriptions**.
- `-gt --generate-truthy {bool}`: the default is to not generate truthy triples. Specify this option to generate truthy triples. Default to **Yes**.
- `-ig --ignore {bool}`: if set to yes, ignore various kinds of exceptions and mistakes and log them to a log file with line number in input file, rather than stopping. logging. Default to **False**.
- `-n --output-n-lines {number}`: output triples approximately every {n} lines of reading stdin. Default to **1000**.
- `-gz --use-gz {number}`: if set to yes, read from compressed gz file. Default to **False**.
- `-sid --use-id {bool}`: if set to yes, the id in the edge will be used as statement id when creating statement or truthy statement. Default to **False**


## Shared Options

- `--debug` run the command in debug mode.

### property-types

**--property-types** is the most important input file. It is also a kgtk file. Here is an example file `example_prop.tsv`

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
The header line is necessary. If property *P493* is used in the input kgtk file, then the edge `P493	property_type	external-identifier` must exists in the `example_prop.tsv` to tell triple generator that the object of `P493` is an external-identifier. If `p495` is used in the input kgtk file, then the object of `P495` will be treated as an entity.

### label, aliases and descriptions

**-lp**, **-ap**, **-dp** defines how you want the triple generator to identify the label, description and aliases. 

For example, if you have `-ap aliases,alias`, then when the following edge is met, both `Alice` and `Alicia` will be treated as aliases to the node `q2020`.

```
node1	property	node2	id
q2020	aliases	Alice@en	id1
q2020	alias	Alicia@sp	id2
```

### truthy

If `-gt --generate-truthy` set to `True`, the statement will be truthy. Truthy statements will have an additional spo with propert prefix `wdt`.

### ignore

ignore allows you to ignore various kind of errors written to the `ignore.log` file.

### n

`n` controls after how many lines of reading the standard input, To achieve optimal performance, you can set n larb b d d d d d d d dger to reduce overhead of creating knowledge graph object and frequent serialization. However, large n also requires larger memory.

### gz

Use compressed file as input.

### use-id

If `--use-id` is set to true, the `id` column of the kgtk file will be used as the statement id if the corresponding edge is a statement edge. It is the user's responsiblity to make sure there is no duplicated statement id across the whole knowledge graph then.

## Usage


### Standard Usage

```bash

kgtk generate_wikidata_triples -pf example_prop.tsv < input_file.tsv > output_file.ttl

```

### Run in parallel

You can split the input files into several smaller pieces and run the command simultaneuously. 

Let's say you are in a directory which contains the `tsv` files. The following command will generate the `ttl` files with the same file name. 

```bash
ls *tsv | parallel -j+0 --eta 'kgtk generate_wikidata_triples -pf example_props.tsv -n 1000 -ig no --debug -gt yes < {} > {.}.ttl'
```
