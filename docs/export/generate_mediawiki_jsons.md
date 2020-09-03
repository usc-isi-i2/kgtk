The `generate-mediawiki-jsons` command is a special command that generates [jsonlines](http://jsonlines.org/) files from a kgtk file. The generated jsonlines file follow the format of the standard mediawiki `wbgetentities` json format like this [one](https://www.wikidata.org/w/api.php?action=wbgetentities&ids=Q42). Those json objects are not exactly following the format of wikidata json dumps.

The motivation of this command is to build a [SQID](https://tools.wmflabs.org/sqid/#/) UI interface for customized knowledge graph. The generated jsonlines can be loaded into Elasticsearch to mimic the official wikidata's `wbgetentities` and `wbsearchentities` API to get the SQID UI up and running.


The JSON generator reads a tab-separated kgtk file from standard input, by default, or from a given file. The kgtk file is required to have at least the following 4 fields: `node1`, `label`, `node2` and `id`. The `node1` field is the subject; `label` is the predicate and `node2` is the object. 

The JSON generator can also optionally accept a `rank` column which specifies the rank of the statement. Please be aware that if the kgtk file is created from tranforming a wikidata dump, the sitelink information will be **lost** since this there is no official property about the `sitelink` property.


## Usage
```
usage: kgtk generate-mediawiki-jsons [-h] [-lp LABELS] [-ap ALIASES] [-dp DESCRIPTIONS]
                                     [-pf PROP_FILE] [-pd PROP_DECLARATION] [-gz USE_GZ]
                                     [-pr OUTPUT_PREFIX] [-n N] [-log LOG_PATH] [-w WARNING]

Generating json files that mimic mediawiki *wbgetentities* api call response. This tool assumes statements and qualifiers related to one entity will be bundled close as the `generate-wikidata-triples` function assumes. If this requirement is not met, please set `n` to a number LARGER than the total number of entities in the kgtk file

optional arguments:
  -h  --help,  show this help message and exit
  -r --rank,  if the input file contains a rank column. Default to False.
  -lp LABELS, --label-property LABELS
                        property identifiers which will create labels, separated by
                        comma','.
  -ap ALIASES, --alias-property ALIASES
                        alias identifiers which will create labels, separated by comma','.
  -dp DESCRIPTIONS, --description-property DESCRIPTIONS
                        description identifiers which will create labels, separated by
                        comma','.
  -pf PROP_FILE, --property-file PROP_FILE
                        path to the file which contains the property datatype mapping in
                        kgtk format.
  -pd PROP_DECLARATION, --property-declaration-in-file PROP_DECLARATION
                        wehther read properties in the kgtk file. If set to yes, make sure
                        the property declaration happens before its usage
  -gz USE_GZ, --use-gz USE_GZ
                        if set to yes, read from compressed gz file
  -pr OUTPUT_PREFIX, --output-file-prefix OUTPUT_PREFIX
                        set the prefix of the output files. Default to `kgtk`
  -n N, --output-n-lines N
                        output json file when the corresponding dictionary size reaches n.
                        Default to 1000
  -log LOG_PATH, --log-path LOG_PATH
                        set the path of the log file
  -w WARNING, --warning WARNING
                        if set to yes, warn various kinds of exceptions and mistakes and log
                        them to a log file with line number in input file, rather than
                        stopping. logging
```


```{shell}
cat input.tsv | kgtk generate-mediawiki-jsons OPTIONS
```
or 
```
kgtk generate-mediawiki-jsons OPTIONS < input.tsv
```

The `generate-mediawiki-jsons` doesn't write to standard output. Instead, it creates a `.jsonl` file with prefix and numbering. You can specify the prefix of the output file with `-pr prefix` option. The default prefix is `kgtk`. The numbering start with `0` and roughly after reading 1000 lines of the kgtk file, the numbering will increase. With a kgtk file with 1500 lines, by default two files `kgtk0.jsonl` and `kgtk1.jsonl` will be generated.

### Quick effect overview

The following tsv file is a minimal sample `input.tsv` file.

|node1|	label|	node2|	id|
| ----- | ----- | ------------- |------------- |
|Q2140726727_mag_author|	P6366|	2140726727|	id1|
|Q2140726727_mag_author|	label|	Zunyou Wu@en|	id2|
|Q2140726727_mag_author|	P1416|	Q184490438_mag_affiliation|	id3|
|Q184490438_mag_affiliation|	label|	Chinese Center For Disease Control And Prevention@en|	id4|

Similar to `generate-wikidata_triples`, we need a `property` file `example_props.tsv` to declare the properties' data_values. Its cotent is below.

|node1|	label|	node2|
| ----- | ----- | ------------- |
|P493|	property_type|	external-identifier|
|P494|	property_type|	external-identifier|
|P495|	property_type|	item|

With the simplest command `kgtk generate-mediawiki-jsons -pf example_props.tsv < input.tsv `, the generated jsonlines file is below.

```{json}
{"Q2140726727_mag_author": {"labels": {"en": {"languange": "en", "value": "Zunyou Wu"}}, "descriptions": {}, "aliases": {}, "claims": {"P6366": [{"mainsnak": {"snaktype": "value", "property": "P6366", "hash": "", "datavalue": {"value": "2140726727", "type": "string"}, "datatype": "external-id"}, "type": "statement", "id": "", "rank": "normal", "references": [], "qualifiers": {}, "qualifiers-order": []}], "P1416": [{"mainsnak": {"snaktype": "value", "property": "P1416", "hash": "", "datavalue": {"value": {"entity-type": "item", "numeric-id": 0, "id": "Q184490438_mag_affiliation"}, "type": "wikibase-entityid"}, "datatype": "wikibase-item"}, "type": "statement", "id": "", "rank": "normal", "references": [], "qualifiers": {}, "qualifiers-order": []}]}, "sitelinks": {}, "type": "item", "id": "Q2140726727_mag_author", "pageid": -1, "ns": -1, "title": "Q2140726727_mag_author", "lastrevid": "2000-01-01T00:00:00Z"}}

{"P6366": {"labels": {}, "descriptions": {}, "aliases": {}, "claims": {}, "sitelinks": {}, "datatype": "external-id", "type": "property", "id": "P6366", "pageid": -1, "ns": -1, "title": "Property:P6366", "lastrevid": "2000-01-01T00:00:00Z"}}

{"P1416": {"labels": {}, "descriptions": {}, "aliases": {}, "claims": {}, "sitelinks": {}, "datatype": "wikibase-item", "type": "property", "id": "P1416", "pageid": -1, "ns": -1, "title": "Property:P1416", "lastrevid": "2000-01-01T00:00:00Z"}}

{"Q184490438_mag_affiliation": {"labels": {"en": {"languange": "en", "value": "Chinese Center For Disease Control And Prevention"}}, "descriptions": {}, "aliases": {}, "claims": {}, "sitelinks": {}, "type": "item", "id": "Q184490438_mag_affiliation", "pageid": -1, "ns": -1, "title": "Q184490438_mag_affiliation", "lastrevid": "2000-01-01T00:00:00Z"}}
```
Both the items and properties are properly identified as `entities`.


`generate-mediawiki-jsons` support qualifiers but it is **memoryless** It has the following requirements of the kgtk file in addtion to the official specification:

1. The qualifer edge has to follow the corresponding statement edge **immediately**. Qualifier edge's `node1` needs to be the statement edge's `id`. This is the only way to identify the relationship between statement edge and its qualifier.
2. To avoid duplicated creation of jsons, statements with the same subject should be **close** to each other. The definition of **closeness** here means that they can't exceed the number of edges before two jsonl serializations. If `Q1` is met as a subject in line **1**, and after **1000** lines the json gets serialized into `kgtk0.jsonl`. However, if `Q1` is met again as a subject at line **1200** which will be serialized into `kgtk1.jsonl`. When loading into the Elasticsearch, whichever one has the label or description will be indexed. When querying by id `Q1` both records will be returned. 
3. To achieve this goal, the input kgtk file should have a sorted structure on `node1`, achieving this depends on the creation of the kgtk file from raw data.

## Options
- `--pf --property-types {str}`: path to the **property file** which contains the property datatype mapping in kgtk format. Default to **NONE**
- `-lp --label-property {str}`: property identifiers which will create labels, separated by comma','. Default to **label**.
- `-ap --alias-property {str}`: alias identifiers which will create labels, separated by comma','. Default to **aliase**.
- `-dp --description-property {str}`: description identifiers which will create labels, separated by comma','. Default to **description**.
- `-w --warning {bool}`: if set to yes, warn various kinds of exceptions and mistakes and log them to a log file with line number in input file
  . Default to **no**.
- `-pr --output-file-prefix`: set the prefix of the outpufile. Default to **kgtk**.
- `-n --output-n-lines {number}`: output triples approximately every {n} lines of reading stdin. Default to **1000**.
- `-gz --use-gz {bool}`: if set to yes, read from compressed gz file. Default to **no**.
- `-log --log-path {str}`: set the path of the log file. Default to **warning.log**.
- `-pd --property-declaration-in-file {bool}`: wehther read properties in the kgtk file. If set to yes, use `cat input.tsv input.tsv` to pipe the input file twice. Default to **no**.
- `-i --input-file {str}`: if this argument is set, kgtk will read from the input file rather than default standard input. If `pd` is also set to `yes`, the file will be loopped twice.

### Shared Options

- `--debug` run the command in debug mode.

## Explanation of Options

### --property-types

If set to true, read proprty data_type information from the property file following the format below. It is also a kgtk file. Here is an example file `example_prop.tsv`


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

### warning

If set to yes, triple generation errors according to specific line will be written to the `warning.log` file or specified path by `-log`.

### n

`n` controls after how many lines of reading the standard input. You can set `n` larger to create a large `jsonl` file. If the kgtk file is in good shape that statements with the same subject are clustered. `n` can be smaller.

### gz

Use compressed file as input.

### log-path

If using `-log`, the warning `-w` must be set to true.

### property-declaration-in-file

If set to yes, besides reading properties from property file, the generator will read from the input stream to find new properties. The user MUST use `cat input.tsv input.tsv | kgtk generate-mediawiki-jsons`.  

### input-file 

If set to a path to a file, kgtk will not read from standard input but open the given file and read from it.


## How json generator handles different types of edges

### label, aliases and descriptions

**-lp**, **-ap**, **-dp** defines properties that triple generator should identify as label, description or aliases creation. There can be multiple choices separated by `,`. Note that the `label` is different from the `label` in a kgtk file's header.

For example, if you have `-ap aliases,alias`, then when the following edge is met, both `Alice` and `Alicia` will be treated as aliases to the node `Q2020`.

|node1|	label|	node2|	id|
| ----- | ----- | ------------- |------------- |
|Q2020|	aliases|	Alice@en|	id1|
|Q2020|	alias|	Alicia@sp|	id2|

`label` should be unique for the **same** language.

### Property Declaration in Input kgtk File

User can also define properties in the input kgtk file with the following syntax. The `data_type` syntax indicates a new property is defined. Note that any usage of `P20200101` must appear after the definition in the kgtk file or `P20200101` will be incorrectly treated as `item`.

|node1|	label|	node2|
| ----- | ----- | -------------|
|P20200101| data_type| string|

### Regular Edges

Regular edges will be generated according to the data type of the property defined in the property file.

## Examples

### Standard Usage

1. If properties are **only** defined in `example_prop.tsv`


```{shell}
kgtk generate_mediawiki_jsons -pf example_prop.tsv -w yes < input_file.tsv
```

1. If properties are **only** defined in `input_file.tsv`


```{shell}
cat input_file.tsv input_file.tsv | kgtk generate_mediawiki_jsons -w yes -pd yes
```

cat input_file.tsv input_file.tsv | kgtk generate-mediawiki-jsons -w yes -pd yes

```
1. If properties are defined in both files.

```bash
cat input_file.tsv input_file.tsv | kgtk generate-mediawiki-jsons -pf example_prop.tsv -w yes -pd yes
>>>>>>> dev
```


### Parallel Usage

You can split the input files into several smaller pieces and run the command simultaneuously. 

Let's say you are in a directory which contains the `tsv` files. The following command will generate the `jsonl` files with the same file name, plus numbering. 

```{shell}
ls *tsv | parallel -j+0 --eta 'kgtk generate_mediawiki_jsons -pf example_props.tsv -n 1000 --debug -gt yes < {}'
```


Splitting a large tsv file into small tsv files directly may make qualifier edges statementless and cause serious mistake. **Do** make sure the splited files start with an statement edge rather than qualifier edge. Again, statemenets with the same entity as Qnodes should be aggregated into the same input file.

The header `node1 label node2 id` needs to be inserted back at the beginning of splited files as well.

## Notes on working with SQID
1. It is recommended to assign label to all entities.
2. Entities including item and properties should have a numeric value immediately following `P` or `Q`. For example, `Paxy` is not legal Pnode but `P00_axy` is a legal Pnode.
3. Many fields are placeholders in the json object for now.

## Notes on differences between Mediawiki `wbgetentities` json and wikidata json dumps.
1. `wbgetentities` take addtional query strings so it is not necessary to return whole json 
2. Mediawiki `wbgetentities` can only query at most 50 ids at once. 
3. Mediawiki json returns have an additonal top-level field `success: 1`.

## Loading into Elasticsearch

The following basic mapping structure is recommended for loading the jsons into Elasticsearch **7.X** . This will enable searching with words in labels and descriptions.

```{python}
mapping_file = {
    "mappings": {
        "dynamic": False,
        "properties": {
            "labels": {
                "dynamic": True,
                "properties": {
                    "en": {
                        "properties": {
                            "language": {"type": "text",
                                         "index": False},
                            "value": {"type": "text",
                                      "analyzer": "english"}
                        }
                    }
                }
            },
            "descriptions": {
                "dynamic": True,
                "properties": {
                    "en": {
                        "properties": {
                            "language": {"type": "text",
                                         "index": False},
                            "value": {"type": "text",
                                      "analyzer": "english"}
                        }
                    }
                }},
            "aliases": {
                "type": "object",
                "enabled": False},
            "claims": {
                "type": "object",
                "enabled": False
            },
            "sitelinks": {
                "type": "object",
                "enabled": False
            },
            "pageid": {
                "type": "integer",
                "index": False
            },
            "ns": {
                "type": "integer",
                "index": False
            },
            "title": {
                "type": "text",
                "index": False
            },
            "lastrevid": {
                "type": "text",
                "index": False
            },
            "type": {
                "type": "text",
                "index": False
            },
            "datatype": {
                "type": "text",
                "index": False
            },
            "id": {
                "type": "keyword"
            }
        }

    }
}
```
