## Summary

This command will augmented graph from a KGTK Edge file with numeric value in float (or date) on node2. This command will automatically detect date in wikidata format and transform it to float in year

### Input File

The input file should be a KGTK Edge file with the following columns or their aliases:

- `node1`: the subject column (source node)
- `label`: the predicate column (property name)
- `node2`: the object column (target node)



### The Output File

The output file is an edge file for each mode that contains the following columns:

- `node1`: this column contains each node
- `label`: this column contains only name of intervals
- `node2`: this column contains range (bin) for numeric value


## Usage
```
usage: kgtk augment [-h] [-i INPUT_FILE] [-o OUTPUT_FILE] [--dataset DATASET]
                    [--train-file-name TRAIN_FILE_NAME]
                    [--numerical-literal-name NUM_LITERAL_NAME]
                    [--valid-file-name VALID_FILE_NAME]
                    [--test-file-name TEST_FILE_NAME] [--bins BINS]
                    [--aug_mode AUG_MODE] [--prediction-type PREDICTION_TYPE]
                    [--reverse REVERSE] [--output-path OUTPUT_PATH]
                    [--train-literal-name TRAIN_LITERAL_NAME]
                    [--entity-triple-name ENTITY_TRIPLE_NAME]
                    [--valid-literal-name VALID_LITERAL_NAME]
                    [--test-literal-name TEST_LITERAL_NAME]
                    [--include-original INCLUDE_ORIGINAL]
                    [--old-id-column-name COLUMN_NAME]
                    [--new-id-column-name COLUMN_NAME]
                    [--overwrite-id [optional true|false]]
                    [--verify-id-unique [optional true|false]]
                    [--id-style {compact-prefix,empty,node1-label-node2,node1-label-num,node1-label-node2-num,node1-label-node2-id,prefix###,wikidata,wikidata-with-claim-id}]
                    [--id-prefix PREFIX] [--initial-id INTEGER]
                    [--id-prefix-num-width INTEGER]
                    [--id-concat-num-width INTEGER]
                    [--value-hash-width VALUE_HASH_WIDTH]
                    [--claim-id-hash-width CLAIM_ID_HASH_WIDTH]
                    [--claim-id-column-name CLAIM_ID_COLUMN_NAME]
                    [--id-separator ID_SEPARATOR] [-v [optional True|False]]

Augment Graph File

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK input file. (May be omitted or '-' for
                        stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for
                        stdout.)
  --dataset DATASET     Specify the location of dataset.
  --train-file-name TRAIN_FILE_NAME
                        Specify name for training file
  --numerical-literal-name NUM_LITERAL_NAME
                        Specify name for numerical literal file
  --valid-file-name VALID_FILE_NAME
                        Specify name for valid file
  --test-file-name TEST_FILE_NAME
                        Specify name for test file
  --bins BINS           Specify number of bins to use
  --aug_mode AUG_MODE   Specify name for test file, seperated by comma, or All
                        for using all modes
  --prediction-type PREDICTION_TYPE
                        Specify prediction type to use (lp, np)
  --reverse REVERSE     Specify whether to include reverse links
  --output-path OUTPUT_PATH
                        Specify path to store output files
  --train-literal-name TRAIN_LITERAL_NAME
                        Specify name for training file
  --entity-triple-name ENTITY_TRIPLE_NAME
                        Specify name for entity triple file
  --valid-literal-name VALID_LITERAL_NAME
                        Specify name for valid file
  --test-literal-name TEST_LITERAL_NAME
                        Specify name for test file
  --include-original INCLUDE_ORIGINAL
                        Specify whether to include original edges
  --old-id-column-name COLUMN_NAME
                        The name of the old ID column. (default=id).
  --new-id-column-name COLUMN_NAME
                        The name of the new ID column. (default=id).
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
  --id-style {compact-prefix,empty,node1-label-node2,node1-label-num,node1-label-node2-num,node1-label-node2-id,prefix###,wikidata,wikidata-with-claim-id}
                        The ID generation style. (default=prefix###).
  --id-prefix PREFIX    The prefix for a prefix### ID. (default=E).
  --initial-id INTEGER  The initial numeric value for a prefix### ID.
                        (default=1).
  --id-prefix-num-width INTEGER
                        The width of the numeric value for a prefix### ID.
                        (default=1).
  --id-concat-num-width INTEGER
                        The width of the numeric value for a concatenated ID.
                        (default=4).
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

## Examples


### Default (augment only, without prediction)

The following file will be used to illustrate some of the capabilities of `kgtk augment`.

```bash
head -5 examples/docs/augment-FB15K-sample.tsv
```

| node1 | label | node2 |
| -- | -- | -- | 
|/m/06rf7	|<http://rdf.freebase.com/ns/location.geocode.longitude>|	9.70404945|
|/m/06rf7	|<http://rdf.freebase.com/ns/location.geocode.latitude>|	54.20867775|
|/m/04258w|	<http://rdf.freebase.com/ns/people.person.date_of_birth>|	1912.66666667|
|/m/04258w|	<http://rdf.freebase.com/ns/people.deceased_person.date_of_death>|	1997.83333333|


```bash
kgtk augment --dataset augment-FB15K-sample --output-path fb_augment
```

An example result file

```bash
head -6 fb_augment/augment_output_QOC_8/output.tsv
```

|node1                                        |label|node2    |
|---------------------------------------------|-----|---------|
|/m/06rf7|	Interval-<http://rdf.freebase.com/ns/location.geocode.longitude>_right|	Interval-<http://rdf.freebase.com/ns/location.geocode.longitude>(11.866667999999999_inf)
|/m/04p_hy|	Interval-<http://rdf.freebase.com/ns/location.geocode.longitude>_right|	Interval-<http://rdf.freebase.com/ns/location.geocode.longitude>(-0.00537_-3.603)|
|/m/0c1xm	|Interval-<http://rdf.freebase.com/ns/location.geocode.longitude>_right|	Interval-<http://rdf.freebase.com/ns/location.geocode.longitude>(-0.00537_-3.603)|
|/m/0c5x_	|Interval-<http://rdf.freebase.com/ns/location.geocode.longitude>_right	|Interval-<http://rdf.freebase.com/ns/location.geocode.longitude>(-0.00537_-3.603)|
|/m/0j_1v	|Interval-<http://rdf.freebase.com/ns/location.geocode.longitude>_right|	Interval-<http://rdf.freebase.com/ns/location.geocode.longitude>(-7.999999_11.866667)|
### link / numeric prediction

1. To augment the dataset with link prediction, make sure the directory `data/{dataset}` contains at least four files:
      1. `train.txt`: The training entity triples.
      2. `valid.txt`: The validation entity triples.
      3. `test.txt`: The testing entity triples.
      4. `numerical_literals.txt`: The literal triples.
      5. Once you get the above files, augment the graph with `kgtk augment --dataset {dataset} --bins {bins} --prediction-type lp`.
2. To augment the dataset with numericaprediction, make sure the directory `data/{dataset}` contains at least four files:
      1. `train_kge`: The entity triples.
      2. `train_100`: The training literal triples.
      3. `dev`: The validation literal triples.
      4. `test`: The test literal triples.
      5. Once you get the above files, augment the graph with `kgtk augment --dataset {dataset} --bins {bins} --prediction-type np`.
