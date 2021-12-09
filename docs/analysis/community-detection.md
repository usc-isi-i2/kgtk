## Summary

This command will return a clutering results from the input kgtk file.
The algorithms are provided by graph_tool (blockmodel, nested and mcmc)

### Input File

The input file should be a KGTK Edge file with the following columns or their aliases:

- `node1`: the subject column (source node)
- `label`: the predicate column (property name)
- `node2`: the object column (target node)

### Processing an Input File that is Not a KGTK Edge File

If your input file doesn't have `node1`, `label`, or `node2` columns (or their aliases) at all, then it is
not a valid KGTK Edge file.  In this case, you also have to pass the following command line option:

- `--input-mode=NONE`

### The Output File

The output file is an edge file that contains the following columns:

- `node1`: this column contains each node
- `label`: this column contains only 'in'
- `node2`: this column contains the resulting cluster
- `node2;prob`: this column contains the probability/confidence of clustering


## Usage
```
usage: kgtk community-detection [-h] [-i INPUT_FILE] [-o OUTPUT_FILE]
                                [--method METHOD]
                                [--old-id-column-name COLUMN_NAME]
                                [--new-id-column-name COLUMN_NAME]
                                [--overwrite-id [optional true|false]]
                                [--verify-id-unique [optional true|false]]
                                [--id-style {node1-label-node2,node1-label-num,node1-label-node2-num,node1-label-node2-id,empty,prefix###,wikidata,wikidata-with-claim-id}]
                                [--id-prefix PREFIX] [--initial-id INTEGER]
                                [--id-prefix-num-width INTEGER]
                                [--id-concat-num-width INTEGER]
                                [--value-hash-width VALUE_HASH_WIDTH]
                                [--claim-id-hash-width CLAIM_ID_HASH_WIDTH]
                                [--claim-id-column-name CLAIM_ID_COLUMN_NAME]
                                [--id-separator ID_SEPARATOR]
                                [-v [optional True|False]]

Creating community detection from graph-tool using KGTK file, available options are blockmodel, nested and mcmc

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK input file. (May be omitted or '-' for
                        stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for
                        stdout.)
  --method METHOD       Specify the clustering method to use.
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
  --id-style {node1-label-node2,node1-label-num,node1-label-node2-num,node1-label-node2-id,empty,prefix###,wikidata,wikidata-with-claim-id}
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


### Default model (blockmodel)

The following file will be used to illustrate some of the capabilities of `kgtk reachable-nodes`.

```bash
head arnold_family.tsv
```

| node1 | label | node2 |
| -- | -- | -- | 
| 'Joseph P. Kennedy Jr.'@en     | P3373 | 'Rosemary Kennedy'@en                              | 
| 'Joseph P. Kennedy Jr.'@en     | P3373 | 'Kathleen Cavendish, Marchioness of Hartington'@en | 
| 'Joseph P. Kennedy Jr.'@en     | P3373 | 'Jean Kennedy Smith'@en                            | 
| 'Joseph P. Kennedy Jr.'@en     | P3373 | 'Eunice Kennedy Shriver'@en                        | 
| 'Joseph P. Kennedy Jr.'@en     | P3373 | 'Patricia Kennedy Lawford'@en                      | 
| 'Joseph P. Kennedy Jr.'@en     | P3373 | 'John F. Kennedy'@en                               | 
| 'Christopher G. Kennedy'@en    | P22   | 'Robert F. Kennedy'@en                             | 
| 'Christopher G. Kennedy'@en    | P25   | 'Ethel Skakel Kennedy'@en                          | 
| 'Christopher G. Kennedy'@en    | P3373 | 'Robert F. Kennedy Jr.'@en                         | 
| 'Christopher G. Kennedy'@en    | P3373 | 'Joseph P. Kennedy II'@en                          | 
| 'Christopher G. Kennedy'@en    | P3373 | 'Michael LeMoyne Kennedy'@en                       | 
| 'Christopher G. Kennedy'@en    | P3373 | 'David A. Kennedy'@en                              | 
| 'Christopher G. Kennedy'@en    | P3373 | 'Rory Kennedy'@en                                  | 
| 'Christopher G. Kennedy'@en    | P3373 | 'Kathleen Kennedy Townsend'@en                     | 
| 'Christopher G. Kennedy'@en    | P3373 | 'Kerry Kennedy'@en                                 | 
| 'Christopher G. Kennedy'@en    | P3373 | 'Courtney Kennedy Hill'@en                         | 
| 'Christopher G. Kennedy'@en    | P3373 | 'Douglas Harriman Kennedy'@en                      | 
| 'Christopher G. Kennedy'@en    | P3373 | 'Max Kennedy'@en                                   | 
| 'Courtney Kennedy Hill'@en     | P22   | 'Robert F. Kennedy'@en                             | 
| 'Courtney Kennedy Hill'@en     | P25   | 'Ethel Skakel Kennedy'@en                          | 


Find the communities using blockmodel.

```bash
kgtk community-detection -i arnold_family.tsv --method blockmodel
```

|node1                                        |label|node2    |
|---------------------------------------------|-----|---------|
|Christopher Lawford                          |in   |cluster_6|
|Peter Lawford                                |in   |cluster_2|
|Patricia Kennedy Lawford                     |in   |cluster_7|
|Jean Edith Olssen                            |in   |cluster_13|
|Victoria Lawford                             |in   |cluster_2|
|Sydney Lawford                               |in   |cluster_2|
|Robin Lawford                                |in   |cluster_6|
|Mary Rowan                                   |in   |cluster_6|
|Deborah Gould                                |in   |cluster_6|
|Patricia Seaton                              |in   |cluster_6|
|David Christopher Lawford                    |in   |cluster_13|
|Savannah Rose Lawford                        |in   |cluster_13|
|Matthew Valentine Lawford                    |in   |cluster_13|
|Andrew Cuomo                                 |in   |cluster_31|
|Kerry Kennedy                                |in   |cluster_31|
|Ted Kennedy                                  |in   |cluster_19|
|John F. Kennedy                              |in   |cluster_23|
|Joseph P. Kennedy Sr.                        |in   |cluster_24|
|Rose Kennedy                                 |in   |cluster_24|
|Joan Bennett Kennedy                         |in   |cluster_20|
|Victoria Reggie Kennedy                      |in   |cluster_20|
|Robert F. Kennedy                            |in   |cluster_22|
|Rosemary Kennedy                             |in   |cluster_24|
|Kathleen Cavendish, Marchioness of Hartington|in   |cluster_24|
|Jean Kennedy Smith                           |in   |cluster_24|
|Eunice Kennedy Shriver                       |in   |cluster_23|
|Joseph P. Kennedy Jr.                        |in   |cluster_24|
|Kara Kennedy                                 |in   |cluster_20|
|Edward M. Kennedy Jr.                        |in   |cluster_20|
|Patrick J. Kennedy                           |in   |cluster_20|
|Robert F. Kennedy Jr.                        |in   |cluster_31|
|Ethel Skakel Kennedy                         |in   |cluster_31|
|Joseph P. Kennedy II                         |in   |cluster_31|
|Michael LeMoyne Kennedy                      |in   |cluster_31|
|David A. Kennedy                             |in   |cluster_31|
|Rory Kennedy                                 |in   |cluster_31|
|Kathleen Kennedy Townsend                    |in   |cluster_31|
|Christopher G. Kennedy                       |in   |cluster_31|
|Courtney Kennedy Hill                        |in   |cluster_31|
|Douglas Harriman Kennedy                     |in   |cluster_31|
|Max Kennedy                                  |in   |cluster_31|
|Jacqueline Kennedy Onassis                   |in   |cluster_42|
|Caroline Kennedy                             |in   |cluster_42|
|John F. Kennedy Jr.                          |in   |cluster_42|
|Patrick Bouvier Kennedy                      |in   |cluster_42|
|Arabelle Kennedy                             |in   |cluster_42|
|Maria Shriver                                |in   |cluster_57|
|Sargent Shriver                              |in   |cluster_52|
|Arnold Schwarzenegger                        |in   |cluster_63|
|Bobby Shriver                                |in   |cluster_52|
|Timothy Shriver                              |in   |cluster_48|
|Anthony Shriver                              |in   |cluster_52|
|Mark Shriver                                 |in   |cluster_48|
|Christina Schwarzenegger                     |in   |cluster_58|
|Christopher Schwarzenegger                   |in   |cluster_58|
|Katherine Schwarzenegger                     |in   |cluster_58|
|Patrick Schwarzenegger                       |in   |cluster_63|
|Joseph Baena                                 |in   |cluster_58|
|Mildred Patricia Baena                       |in   |cluster_57|
|Aurelia Schwarzenegger                       |in   |cluster_60|
|Gustav Schwarzenegger                        |in   |cluster_60|
|Jadrny                                       |in   |cluster_60|
|Meinhard Schwarzenegger                      |in   |cluster_60|
|Patrick M. Knapp Schwarzenegger              |in   |cluster_60|
|Robert Sargent Shriver                       |in   |cluster_48|
|Hilda Shriver                                |in   |cluster_48|
|Malissa Feruzzi                              |in   |cluster_48|
|Jack Pratt                                   |in   |cluster_69|
|Chris Pratt                                  |in   |cluster_69|
|Anna Faris                                   |in   |cluster_69|
|Alina Shriver                                |in   |cluster_48|
|Rogelio Baena                                |in   |cluster_48|
|Marilyn Monroe                               |in   |cluster_42|


### nested model

```bash
kgtk community-detection -i arnold_family.tsv --method nested
```

|node1                                        |label|node2    |
|---------------------------------------------|-----|---------|
|Christopher Lawford                          |in   |cluster_0_10_43|
|Peter Lawford                                |in   |cluster_0_2_43|
|Patricia Kennedy Lawford                     |in   |cluster_0_10_0|
|Jean Edith Olssen                            |in   |cluster_0_2_43|
|Victoria Lawford                             |in   |cluster_0_10_43|
|Sydney Lawford                               |in   |cluster_0_2_43|
|Robin Lawford                                |in   |cluster_0_2_43|
|Mary Rowan                                   |in   |cluster_0_2_43|
|Deborah Gould                                |in   |cluster_0_10_43|
|Patricia Seaton                              |in   |cluster_0_7_43|
|David Christopher Lawford                    |in   |cluster_0_2_43|
|Savannah Rose Lawford                        |in   |cluster_0_10_43|
|Matthew Valentine Lawford                    |in   |cluster_0_2_43|
|Andrew Cuomo                                 |in   |cluster_0_7_14|
|Kerry Kennedy                                |in   |cluster_0_7_14|
|Ted Kennedy                                  |in   |cluster_0_10_34|
|John F. Kennedy                              |in   |cluster_0_2_38|
|Joseph P. Kennedy Sr.                        |in   |cluster_0_10_65|
|Rose Kennedy                                 |in   |cluster_0_10_65|
|Joan Bennett Kennedy                         |in   |cluster_0_2_40|
|Victoria Reggie Kennedy                      |in   |cluster_0_7_40|
|Robert F. Kennedy                            |in   |cluster_0_10_35|
|Rosemary Kennedy                             |in   |cluster_0_10_65|
|Kathleen Cavendish, Marchioness of Hartington|in   |cluster_0_7_65|
|Jean Kennedy Smith                           |in   |cluster_0_7_65|
|Eunice Kennedy Shriver                       |in   |cluster_0_10_38|
|Joseph P. Kennedy Jr.                        |in   |cluster_0_2_65|
|Kara Kennedy                                 |in   |cluster_0_2_40|
|Edward M. Kennedy Jr.                        |in   |cluster_0_7_40|
|Patrick J. Kennedy                           |in   |cluster_0_7_40|
|Robert F. Kennedy Jr.                        |in   |cluster_0_10_14|
|Ethel Skakel Kennedy                         |in   |cluster_0_2_14|
|Joseph P. Kennedy II                         |in   |cluster_0_2_14|
|Michael LeMoyne Kennedy                      |in   |cluster_0_2_14|
|David A. Kennedy                             |in   |cluster_0_10_14|
|Rory Kennedy                                 |in   |cluster_0_7_14|
|Kathleen Kennedy Townsend                    |in   |cluster_0_10_14|
|Christopher G. Kennedy                       |in   |cluster_0_2_14|
|Courtney Kennedy Hill                        |in   |cluster_0_4_14|
|Douglas Harriman Kennedy                     |in   |cluster_0_10_14|
|Max Kennedy                                  |in   |cluster_0_10_14|
|Jacqueline Kennedy Onassis                   |in   |cluster_0_10_57|
|Caroline Kennedy                             |in   |cluster_0_2_57|
|John F. Kennedy Jr.                          |in   |cluster_0_10_57|
|Patrick Bouvier Kennedy                      |in   |cluster_0_2_57|
|Arabelle Kennedy                             |in   |cluster_0_7_57|
|Maria Shriver                                |in   |cluster_0_2_51|
|Sargent Shriver                              |in   |cluster_0_10_33|
|Arnold Schwarzenegger                        |in   |cluster_0_10_69|
|Bobby Shriver                                |in   |cluster_0_2_33|
|Timothy Shriver                              |in   |cluster_0_10_33|
|Anthony Shriver                              |in   |cluster_0_2_33|
|Mark Shriver                                 |in   |cluster_0_10_33|
|Christina Schwarzenegger                     |in   |cluster_0_2_69|
|Christopher Schwarzenegger                   |in   |cluster_0_10_69|
|Katherine Schwarzenegger                     |in   |cluster_0_7_69|
|Patrick Schwarzenegger                       |in   |cluster_0_7_69|
|Joseph Baena                                 |in   |cluster_0_2_69|
|Mildred Patricia Baena                       |in   |cluster_0_2_69|
|Aurelia Schwarzenegger                       |in   |cluster_0_4_69|
|Gustav Schwarzenegger                        |in   |cluster_0_10_69|
|Jadrny                                       |in   |cluster_0_2_69|
|Meinhard Schwarzenegger                      |in   |cluster_0_10_69|
|Patrick M. Knapp Schwarzenegger              |in   |cluster_0_2_69|
|Robert Sargent Shriver                       |in   |cluster_0_2_33|
|Hilda Shriver                                |in   |cluster_0_10_33|
|Malissa Feruzzi                              |in   |cluster_0_2_33|
|Jack Pratt                                   |in   |cluster_0_7_69|
|Chris Pratt                                  |in   |cluster_0_7_69|
|Anna Faris                                   |in   |cluster_0_2_69|
|Alina Shriver                                |in   |cluster_0_2_33|
|Rogelio Baena                                |in   |cluster_0_2_69|
|Marilyn Monroe                               |in   |cluster_0_2_65|


### MCMC model

```bash
kgtk community-detection -i arnold_family.tsv --method mcmc
```
|node1                                        |label|node2    |node2;prob         |
|---------------------------------------------|-----|---------|-------------------|
|Christopher Lawford                          |in   |cluster_0|1.0                |
|Peter Lawford                                |in   |cluster_0|1.0                |
|Patricia Kennedy Lawford                     |in   |cluster_1|0.806980698069807  |
|Jean Edith Olssen                            |in   |cluster_0|1.0                |
|Victoria Lawford                             |in   |cluster_0|1.0                |
|Sydney Lawford                               |in   |cluster_0|1.0                |
|Robin Lawford                                |in   |cluster_0|1.0                |
|Mary Rowan                                   |in   |cluster_0|0.9998999899989999 |
|Deborah Gould                                |in   |cluster_0|0.9998999899989999 |
|Patricia Seaton                              |in   |cluster_0|1.0                |
|David Christopher Lawford                    |in   |cluster_0|0.9998999899989999 |
|Savannah Rose Lawford                        |in   |cluster_0|0.9998999899989999 |
|Matthew Valentine Lawford                    |in   |cluster_0|0.9997999799979999 |
|Andrew Cuomo                                 |in   |cluster_2|0.9457945794579458 |
|Kerry Kennedy                                |in   |cluster_2|1.0                |
|Ted Kennedy                                  |in   |cluster_3|0.8140814081408141 |
|John F. Kennedy                              |in   |cluster_3|0.9794979497949795 |
|Joseph P. Kennedy Sr.                        |in   |cluster_4|0.9993999399939995 |
|Rose Kennedy                                 |in   |cluster_4|0.9992999299929993 |
|Joan Bennett Kennedy                         |in   |cluster_5|0.7872787278727873 |
|Victoria Reggie Kennedy                      |in   |cluster_5|0.48514851485148514|
|Robert F. Kennedy                            |in   |cluster_6|1.0                |
|Rosemary Kennedy                             |in   |cluster_4|0.9994999499949995 |
|Kathleen Cavendish, Marchioness of Hartington|in   |cluster_4|0.9991999199919992 |
|Jean Kennedy Smith                           |in   |cluster_4|0.9995999599959996 |
|Eunice Kennedy Shriver                       |in   |cluster_1|0.866986698669867  |
|Joseph P. Kennedy Jr.                        |in   |cluster_4|0.9990999099909991 |
|Kara Kennedy                                 |in   |cluster_5|0.7872787278727873 |
|Edward M. Kennedy Jr.                        |in   |cluster_5|0.7872787278727873 |
|Patrick J. Kennedy                           |in   |cluster_5|0.787078707870787  |
|Robert F. Kennedy Jr.                        |in   |cluster_2|1.0                |
|Ethel Skakel Kennedy                         |in   |cluster_2|1.0                |
|Joseph P. Kennedy II                         |in   |cluster_2|1.0                |
|Michael LeMoyne Kennedy                      |in   |cluster_2|1.0                |
|David A. Kennedy                             |in   |cluster_2|1.0                |
|Rory Kennedy                                 |in   |cluster_2|1.0                |
|Kathleen Kennedy Townsend                    |in   |cluster_2|1.0                |
|Christopher G. Kennedy                       |in   |cluster_2|1.0                |
|Courtney Kennedy Hill                        |in   |cluster_2|1.0                |
|Douglas Harriman Kennedy                     |in   |cluster_2|1.0                |
|Max Kennedy                                  |in   |cluster_2|1.0                |
|Jacqueline Kennedy Onassis                   |in   |cluster_5|1.0                |
|Caroline Kennedy                             |in   |cluster_5|1.0                |
|John F. Kennedy Jr.                          |in   |cluster_5|1.0                |
|Patrick Bouvier Kennedy                      |in   |cluster_5|0.9998999899989999 |
|Arabelle Kennedy                             |in   |cluster_5|1.0                |
|Maria Shriver                                |in   |cluster_7|0.9790979097909791 |
|Sargent Shriver                              |in   |cluster_7|0.9998999899989999 |
|Arnold Schwarzenegger                        |in   |cluster_8|1.0                |
|Bobby Shriver                                |in   |cluster_7|0.9998999899989999 |
|Timothy Shriver                              |in   |cluster_7|0.9998999899989999 |
|Anthony Shriver                              |in   |cluster_7|1.0                |
|Mark Shriver                                 |in   |cluster_7|0.9998999899989999 |
|Christina Schwarzenegger                     |in   |cluster_8|0.9998999899989999 |
|Christopher Schwarzenegger                   |in   |cluster_8|1.0                |
|Katherine Schwarzenegger                     |in   |cluster_8|1.0                |
|Patrick Schwarzenegger                       |in   |cluster_8|1.0                |
|Joseph Baena                                 |in   |cluster_8|1.0                |
|Mildred Patricia Baena                       |in   |cluster_8|0.9997999799979999 |
|Aurelia Schwarzenegger                       |in   |cluster_8|0.9998999899989999 |
|Gustav Schwarzenegger                        |in   |cluster_8|0.9997999799979999 |
|Jadrny                                       |in   |cluster_8|0.987998799879988  |
|Meinhard Schwarzenegger                      |in   |cluster_8|1.0                |
|Patrick M. Knapp Schwarzenegger              |in   |cluster_8|0.98999899989999   |
|Robert Sargent Shriver                       |in   |cluster_7|0.9921992199219922 |
|Hilda Shriver                                |in   |cluster_7|0.9938993899389938 |
|Malissa Feruzzi                              |in   |cluster_7|0.9416941694169417 |
|Jack Pratt                                   |in   |cluster_8|0.9837983798379838 |
|Chris Pratt                                  |in   |cluster_8|0.9858985898589859 |
|Anna Faris                                   |in   |cluster_8|0.9840984098409841 |
|Alina Shriver                                |in   |cluster_7|0.9413941394139413 |
|Rogelio Baena                                |in   |cluster_8|0.9873987398739874 |
|Marilyn Monroe                               |in   |cluster_5|0.49194919491949196|
