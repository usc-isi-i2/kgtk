The `generate-mediawiki-jsons` command is a special command that
generates [JSON Lines](http://jsonlines.org/) files from a kgtk
file. The generated JSON Lines files follow the format of the standard
mediawiki `wbgetentities` json format like this
[one](https://www.wikidata.org/w/api.php?action=wbgetentities&ids=Q42). Those
JSON objects do not exactly follow the format of Wikidata JSON
dumps.

The motivation of this command is to build a
[SQID](https://tools.wmflabs.org/sqid/#/) UI interface for customized
knowledge graph. The generated jsonlines can be loaded into
Elasticsearch to mimic the official wikidata's `wbgetentities` and
`wbsearchentities` API to get the SQID UI up and running.


The JSON generator reads a tab-separated kgtk file from standard
input, by default, or from a given file. The kgtk file is required to
have at least the following 4 fields: `node1`, `label`, `node2` and
`id`. The `node1` field is the subject; `label` is the predicate and
`node2` is the object.

The JSON generator can also optionally accept a `rank` column which
specifies the rank of the statement. Please be aware that if the kgtk
file is created from tranforming a wikidata dump, the sitelink
information will be **lost** since this there is no official property
about the `sitelink` property.

In order to generate the mediawiki JSON Lines, the code needs to know the
Wikidata datatype associated with each Wikidata property (Pxxx).  These
datatypes can be embedded in the main input file so long as each property datatype
declaration preceeds any other appearance of the property.  Alternatively, the
property datatype declarations can be read from an optional input file.


## Usage
```
usage: kgtk generate-mediawiki-jsons [-h] [-i INPUT_FILE] [-pf PROPERTY_FILE] [-lp LABELS]
                                     [-ap ALIASES] [-dp DESCRIPTIONS] [-pd PROP_DECLARATION]
                                     [-pr OUTPUT_PREFIX] [-n N] [-log LOG_PATH] [-w WARNING]
                                     [-r HAS_RANK] [--error-action {log,raise}]
                                     [-pl PROPERTY_DECLARATION_LABEL] [-fp [True/False]]
                                     [-ip [True/False]] [-v [True/False]]

Generating json files that mimic mediawiki *wbgetentities* api call response. This tool assumes statements and qualifiers related to one entity will be bundled close as the `generate-wikidata-triples` function assumes. If this requirement is not met, please set `n` to a number LARGER than the total number of entities in the kgtk file

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK input file. (May be omitted or '-' for stdin.)
  -pf PROPERTY_FILE, --property-file PROPERTY_FILE
                        the file which contains the property datatype mapping in kgtk format
                        (Optional, use '-' for stdin.)
  -lp LABELS, --label-property LABELS
                        property identifiers which will create labels, separated by comma','.
  -ap ALIASES, --alias-property ALIASES
                        alias identifiers which will create labels, separated by comma','.
  -dp DESCRIPTIONS, --description-property DESCRIPTIONS
                        description identifiers which will create labels, separated by comma','.
  -pd PROP_DECLARATION, --property-declaration-in-file PROP_DECLARATION
                        whether to read properties from the input kgtk file. If set to yes, make sure the
                        property declaration happens before its usage. default=False
  -pr OUTPUT_PREFIX, --output-file-prefix OUTPUT_PREFIX
                        set the prefix of the output files. Default to `kgtk`
  -n N, --output-n-lines N
                        output json file when the corresponding dictionary size reaches n.
                        Default to 1000
  -log LOG_PATH, --log-path LOG_PATH
                        set the path of the log file
  -w WARNING, --warning WARNING
                        if set to yes, warn various kinds of exceptions and mistakes and log them
                        to a log file with line number in input file, rather than stopping.
                        logging
  -r HAS_RANK, --rank HAS_RANK
                        Whether the input file contains a rank column. Please refer to the
                        `import_wikidata` command for the header information. Default to False,
                        then all the ranks will be `normal`, therefore `NormalRank`.
  --error-action {log,raise}
                        When errors occur, either log them (`log`) or raise an exception
                        (`raise`). Default='log'.
  -pl PROPERTY_DECLARATION_LABEL, --property-declaration-label PROPERTY_DECLARATION_LABEL
                        The edge label in a property file that indicates a property declaration.
                        default='data_type'
  -fp [True/False], --filter-prop-file [True/False]
                        If true and a property file has been specified, filter the prop file,
                        processing only edges with the property declaration label. (default=True)
  -ip [True/False], --ignore-property-declarations-in-file [True/False]
                        If true, ignore input edges with the property declaration label.
                        (default=True)
  -v [True/False], --verbose [True/False]
                        If true, provide additional feedback. (default=False)
```


```{shell}
cat input.tsv | kgtk generate-mediawiki-jsons OPTIONS
```
or 
```
kgtk generate-mediawiki-jsons OPTIONS < input.tsv
```
or
```
kgtk generate-mediawiki-jsons OPTIONS -i input.tsv
```

By default, `kgtk generate-mediawiki-jsons` doesn't write to standard
output. Instead, it creates a `.jsonl` file with prefix and
numbering. You can specify the prefix of the output file with `-pr
prefix` option. The default prefix is `kgtk`. The numbering start with
`0` and roughly after reading 1000 lines (controlled by `-n N`) of the kgtk file, the
numbering will increase. With a kgtk file with 1500 lines, by default
two files, `kgtk0.jsonl` and `kgtk1.jsonl`, will be generated.

If `-n 0` is speified, only a single file (`kgtk0.jsonl`) will be generated.

However, if the OUTPUT_PREFIX is set to `-` (`-pr -`), then
the output will be sent to standard output.  This functionality is
mainly intended for use in producing documents such as this one,
but it may prove useful in some data processing pipelines.

### Quick effect overview

The following tsv file is a minimal sample `input.tsv` file.

```bash
kgtk cat -i examples/docs/generate-mediawiki-jsons-input.tsv
```



Similar to `generate-wikidata_triples`, we need a `property` file
to declare the properties' data_values. Its content is below:

```bash
kgtk cat -i examples/docs/generate-mediawiki-jsons-properties.tsv
```

Edge File

|id     |node;label|is_country|type|degree|type_missing|population|
|-------|----------|----------|----|------|------------|----------|
|Alice  |‘Alice’@en|0         |human|4     |            |          |
|Susan  |‘Susan’@en|0         |human|4     |            |          |
|John   |‘John’@en |0         |human|4     |            |          |
|Claudia|‘Claudia’@en|0         |human|3     |            |          |
|Ulrich |‘Ulrich’@en|0         |human|4     |            |          |
|Fritz  |‘Fritz’@en|0         |human|4     |            |          |
|USA    |‘USA’@en  |1         |country|5     |country     |300       |
|Germany|‘Germany’@en|1         |country|5     |country     |50        |
|Brazil |‘Brazil’@en|1         |country|2     |country     |200       |



Node File

|node1  |label |node2  |weight|
|-------|------|-------|------|
|Alice  |friend|Susan  |0.9   |
|Susan  |friend|John   |0.3   |
|John   |friend|Claudia|      |
|Ulrich |friend|John   |      |
|Fritz  |friend|Ulrich |      |
|Fritz  |friend|Alice  |      |
|Alice  |born  |USA    |      |
|Susan  |born  |USA    |      |
|John   |born  |USA    |      |
|Claudia|born  |Germany|      |
|Ulrich |born  |Germany|      |
|Fritz  |born  |Germany|      |
|Alice  |lives |Germany|      |
|Susan  |lives |USA    |      |
|John   |lives |Brazil |      |
|Claudia|lives |Germany|      |
|Ulrich |lives |Brazil |      |
|Fritz  |lives |Germany|      |


With the simplest command:

```bash
kgtk generate-mediawiki-jsons \
     -i examples/docs/generate-mediawiki-jsons-input.tsv \
     -pf examples/docs/generate-mediawiki-jsons-properties.tsv \
     -pl property_type \
     -pr -
```

The generated JSON lines file is below:

```{json}
{"Q2140726727_mag_author": {"labels": {"en": {"languange": "en", "value": "Zunyou Wu"}}, "descriptions": {}, "aliases": {}, "claims": {"P6366": [{"mainsnak": {"snaktype": "value", "property": "P6366", "hash": "", "datavalue": {"value": "2140726727", "type": "string"}, "datatype": "external-id"}, "type": "statement", "id": "Q2140726727_mag_authorP63662140726727", "rank": "normal", "references": [], "qualifiers": {}, "qualifiers-order": []}], "P1416": [{"mainsnak": {"snaktype": "value", "property": "P1416", "hash": "", "datavalue": {"value": "Q184490438_mag_affiliation", "type": "string"}, "datatype": "external-id"}, "type": "statement", "id": "Q2140726727_mag_authorP1416Q184490438_mag_affiliation", "rank": "normal", "references": [], "qualifiers": {}, "qualifiers-order": []}]}, "sitelinks": {}, "type": "item", "id": "Q2140726727_mag_author", "pageid": -1, "ns": -1, "title": "Q2140726727_mag_author", "lastrevid": "2000-01-01T00:00:00Z"}}
{"P6366": {"labels": {}, "descriptions": {}, "aliases": {}, "claims": {}, "sitelinks": {}, "datatype": "external-id", "type": "property", "id": "P6366", "pageid": -1, "ns": -1, "title": "Property:P6366", "lastrevid": "2000-01-01T00:00:00Z"}}
{"P1416": {"labels": {}, "descriptions": {}, "aliases": {}, "claims": {}, "sitelinks": {}, "datatype": "external-id", "type": "property", "id": "P1416", "pageid": -1, "ns": -1, "title": "Property:P1416", "lastrevid": "2000-01-01T00:00:00Z"}}
{"Q184490438_mag_affiliation": {"labels": {"en": {"languange": "en", "value": "Chinese Center For Disease Control And Prevention"}}, "descriptions": {}, "aliases": {}, "claims": {}, "sitelinks": {}, "type": "item", "id": "Q184490438_mag_affiliation", "pageid": -1, "ns": -1, "title": "Q184490438_mag_affiliation", "lastrevid": "2000-01-01T00:00:00Z"}}
```

Expanding this for legibility:

```{json}
{
  "Q2140726727_mag_author": {
    "labels": {
      "en": {
        "languange": "en",
        "value": "Zunyou Wu"
      }
    },
    "descriptions": {},
    "aliases": {},
    "claims": {
      "P6366": [
        {
          "mainsnak": {
            "snaktype": "value",
            "property": "P6366",
            "hash": "",
            "datavalue": {
              "value": "2140726727",
              "type": "string"
            },
            "datatype": "external-id"
          },
          "type": "statement",
          "id": "Q2140726727_mag_authorP63662140726727",
          "rank": "normal",
          "references": [],
          "qualifiers": {},
          "qualifiers-order": []
        }
      ],
      "P1416": [
        {
          "mainsnak": {
            "snaktype": "value",
            "property": "P1416",
            "hash": "",
            "datavalue": {
              "value": "Q184490438_mag_affiliation",
              "type": "string"
            },
            "datatype": "external-id"
          },
          "type": "statement",
          "id": "Q2140726727_mag_authorP1416Q184490438_mag_affiliation",
          "rank": "normal",
          "references": [],
          "qualifiers": {},
          "qualifiers-order": []
        }
      ]
    },
    "sitelinks": {},
    "type": "item",
    "id": "Q2140726727_mag_author",
    "pageid": -1,
    "ns": -1,
    "title": "Q2140726727_mag_author",
    "lastrevid": "2000-01-01T00:00:00Z"
  }
}
{
  "P6366": {
    "labels": {},
    "descriptions": {},
    "aliases": {},
    "claims": {},
    "sitelinks": {},
    "datatype": "external-id",
    "type": "property",
    "id": "P6366",
    "pageid": -1,
    "ns": -1,
    "title": "Property:P6366",
    "lastrevid": "2000-01-01T00:00:00Z"
  }
}
{
  "P1416": {
    "labels": {},
    "descriptions": {},
    "aliases": {},
    "claims": {},
    "sitelinks": {},
    "datatype": "external-id",
    "type": "property",
    "id": "P1416",
    "pageid": -1,
    "ns": -1,
    "title": "Property:P1416",
    "lastrevid": "2000-01-01T00:00:00Z"
  }
}
{
  "Q184490438_mag_affiliation": {
    "labels": {
      "en": {
        "languange": "en",
        "value": "Chinese Center For Disease Control And Prevention"
      }
    },
    "descriptions": {},
    "aliases": {},
    "claims": {},
    "sitelinks": {},
    "type": "item",
    "id": "Q184490438_mag_affiliation",
    "pageid": -1,
    "ns": -1,
    "title": "Q184490438_mag_affiliation",
    "lastrevid": "2000-01-01T00:00:00Z"
  }
}
```

`kgtk generate-mediawiki-jsons` supports qualifiers but it is
**memoryless** It has the following requirements of the KGTK file in
addtion to the official KGTK specification:

1. The qualifer edge has to follow the corresponding statement edge **immediately**. Qualifier edge's `node1` needs to be the statement edge's `id`. This is the only way to identify the relationship between statement edge and its qualifier.
2. To avoid duplicated creation of jsons, statements with the same subject should be **close** to each other. The definition of **closeness** here means that they can't exceed the number of edges before two jsonl serializations. If `Q1` is met as a subject in line **1**, and after **1000** lines the json gets serialized into `kgtk0.jsonl`. However, if `Q1` is met again as a subject at line **1200** which will be serialized into `kgtk1.jsonl`. When loading into the Elasticsearch, whichever one has the label or description will be indexed. When querying by id `Q1` both records will be returned. 
3. To achieve this goal, the input KGTK file should have a sorted structure on `node1`, achieving this depends on the creation of the kgtk file from raw data.

## Options
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK input file. (May be omitted or '-' for stdin.)
  -pf PROPERTY_FILE, --property-file PROPERTY_FILE
                        the file which contains the property datatype mapping in kgtk format
                        (Optional, use '-' for stdin.)
  -lp LABELS, --label-property LABELS
                        property identifiers which will create labels, separated by comma','.
  -ap ALIASES, --alias-property ALIASES
                        alias identifiers which will create labels, separated by comma','.
  -dp DESCRIPTIONS, --description-property DESCRIPTIONS
                        description identifiers which will create labels, separated by comma','.
  -pd PROP_DECLARATION, --property-declaration-in-file PROP_DECLARATION
                        whether to read properties in the kgtk file. If set to yes, make sure the
                        property declaration happens before its usage. default=False
  -pr OUTPUT_PREFIX, --output-file-prefix OUTPUT_PREFIX
                        set the prefix of the output files. Default to `kgtk`
  -n N, --output-n-lines N
                        output json file when the corresponding dictionary size reaches n.
                        Default to 1000
  -log LOG_PATH, --log-path LOG_PATH
                        set the path of the log file
  -w WARNING, --warning WARNING
                        if set to yes, warn various kinds of exceptions and mistakes and log them
                        to a log file with line number in input file, rather than stopping.
                        logging
  -r HAS_RANK, --rank HAS_RANK
                        Whether the input file contains a rank column. Please refer to the
                        `import_wikidata` command for the header information. Default to False,
                        then all the ranks will be `normal`, therefore `NormalRank`.
  --error-action {log,raise}
                        When errors occur, either log them (`log`) or raise an exception
                        (`raise`). Default='log'.
  -pl PROPERTY_DECLARATION_LABEL, --property-declaration-label PROPERTY_DECLARATION_LABEL
                        The edge label in a property file that indicates a property declaration.
                        default='data_type'
  -fp [True/False], --filter-prop-file [True/False]
                        If true and a property file has been specified, filter the prop file,
                        processing only edges with the property declaration label. (default=True)
  -ip [True/False], --ignore-property-declarations-in-file [True/False]
                        If true, ignore input edges with the property declaration label.
                        (default=True)
  -v [True/False], --verbose [True/False]
                        If true, provide additional feedback. (default=False)

## Explanation of Options

### -i INPUT_FILE, --input-file INPUT_FILE

The input file should be a standard KGTK edge file.  If this option is not
specified, or is specified as "-", the input file will be read from standard input.

The following columns are required:
 * `node1` or its alias
 * `label` or its alias
 * `node2` or its alias
 * `id` or its alias

### -pf PROPERTY_FILE, --property-file PROPERTY_FILE

This is an optional file.  If specified, it should be a standard KGTK edge file.
It will be used to read proerty datatype declarations.

The following columns are required:
 * `node1` or its alias
 * `label` or its alias
 * `node2` or its alias

By default, only edges with labels matching the property declaration label will
be read from this file.

 * use `-fp False` or `--filter-prop-file FALSE` to read all (node1, node2) pairs from
   this file, ignoring the `label` value on each edge.

 * use `-pl PROPERTY_DECLARATION_LABEL to set the property declaration label
   value.  The default value is `data_type`.

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

### -lp LABELS, -ap ALIASES,  and -dp DESCRIPTIONS

`-lp LABELS`, `-ap ALIASES`, and `-dp DESCRIPTIONS` defines properties
that JSON generator should identify as label, description or aliases,
respectively. LABELS, ALIASES, and DESCRIPTIONS
can be multiple choices separated by `,`. Note that
the concept `label`, as used here, is different from the concept `label` in a KGTK file's header.

Note: Because commans (`,`) are used to separate elemends in LABELS,
ALIASES, and DESCRIPTIONS, a comman may not occur as part of one of
the identifiers in a list.

For example, if you have `-ap aliases,alias`, then when the following edge is met, both `Alice` and `Alicia` will be treated as aliases to the node `Q2020`.

|node1|	label|	node2|	id|
| ----- | ----- | ------------- |------------- |
|Q2020|	aliases|	Alice@en|	id1|
|Q2020|	alias|	Alicia@sp|	id2|

There should be no more than one `label` value per language for an entity.

### -pr OUTPUT_PREFIX, --output-file-prefix OUTPUT_PREFIX

Normally, the output is written to a file path built from the
file prefix and the file sequence number, with a fixed extension of
`.jsonl`.  The default output prefix is `kgtk`, so output records
would be written to:

 * kgtk0.jsonl
 * kgtk1.jsonl
 * kgtk2.jsonl

and so on.  You can use OUTPUT_PREFIX to specify the oath to the folder in which
to write the output, and to chose a different filename prefix.

If OUTPUT_PREFIX is the special value `-`, then the output will be
written to standard output.

### -n N

`-n N` controls after how often new output files are created, based on
how many lines are read from the input file. You can set `N` larger to
create large output file. If the input KGTK file is in good shape such that
statements with the same subject are clustered, `N` can be smaller.

If `N` is 0, then only a single output file will be produced.

### -log LOG_PATH, --log-path LOG_PATH

When specified, LOG_PATH is the path to an output file for warning messages.
If not specified (or if LOG_PATH is the special value `-`), warning output will be sent
to standard error.

### -w WARNING, --warning WARNING

If set to yes, JSON generation errors written to the log file specified by LOG_PATH.
If is "-" when WARNING is yes, then warnings will be sent to standard error.

If set to no (the default), warnng messages will be sent to standard error.

Note: This option and its behavior is expected to change in the future
as `--error-action` gains additional options.

# -r HAS_RANK

This indicates that the input file should have a `rank` column.

### property-declaration-in-file

If set to yes, besides reading properties from property file, the generator will read from the input stream to find property datatype declarations.
A property declaration is an edge with a label value equal to the value of `--property-declaration-label`.

## How json generator handles different types of edges


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
