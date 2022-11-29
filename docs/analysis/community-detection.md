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
                                [--id-style {compact-prefix,empty,node1-label-node2,node1-label-num,node1-label-node2-num,node1-label-node2-id,prefix###,wikidata,wikidata-with-claim-id}]
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


### Default model (blockmodel)

The following file will be used to illustrate some of the capabilities of `kgtk reachable-nodes`.

```bash
head examples/docs/community-detection-arnold.tsv
```

| node1 | label | node2 | node1;label | label;label | node2;label |
| -- | -- | -- | -- | -- | -- |
| Q1086823 | P22 | Q345517 | 'Christopher Lawford'@en | 'father'@en | 'Peter Lawford'@en |
| Q1086823 | P25 | Q432694 | 'Christopher Lawford'@en | 'mother'@en | 'Patricia Kennedy Lawford'@en |
| Q1086823 | P26 | Q75326809 | 'Christopher Lawford'@en | 'spouse'@en | 'Jean Edith Olssen'@en |
| Q1086823 | P3373 | Q75326777 | 'Christopher Lawford'@en | 'sibling'@en | 'Victoria Lawford'@en |
| Q1086823 | P3373 | Q75326779 | 'Christopher Lawford'@en | 'sibling'@en | 'Sydney Lawford'@en |
| Q1086823 | P3373 | Q75326780 | 'Christopher Lawford'@en | 'sibling'@en | 'Robin Lawford'@en |
| Q1086823 | P3448 | Q96079835 | 'Christopher Lawford'@en | 'stepparent'@en | 'Mary Rowan'@en |
| Q1086823 | P3448 | Q96079836 | 'Christopher Lawford'@en | 'stepparent'@en | 'Deborah Gould'@en |
| Q1086823 | P3448 | Q96079838 | 'Christopher Lawford'@en | 'stepparent'@en | 'Patricia Seaton'@en |


Find the communities using blockmodel.

```bash
kgtk community-detection -i examples/docs/community-detection-arnold.tsv --method blockmodel
```

| node1 | label | node2 |
| -- | -- | -- |
| Q1086823 | in | cluster_10 |
| Q345517 | in | cluster_10 |
| Q432694 | in | cluster_26 |
| Q75326809 | in | cluster_10 |
| Q75326777 | in | cluster_10 |
| Q75326779 | in | cluster_10 |
| Q75326780 | in | cluster_10 |
| Q96079835 | in | cluster_10 |
| Q96079836 | in | cluster_10 |
| Q96079838 | in | cluster_10 |
| Q76363382 | in | cluster_10 |
| Q76363384 | in | cluster_10 |
| Q76363386 | in | cluster_10 |
| Q11673 | in | cluster_32 |
| Q467912 | in | cluster_32 |
| Q134549 | in | cluster_27 |
| Q9696 | in | cluster_27 |
| Q313696 | in | cluster_18 |
| Q236540 | in | cluster_18 |
| Q441424 | in | cluster_46 |
| Q7926996 | in | cluster_46 |
| Q25310 | in | cluster_22 |
| Q265595 | in | cluster_18 |
| Q268799 | in | cluster_18 |
| Q272401 | in | cluster_18 |
| Q272908 | in | cluster_26 |
| Q505178 | in | cluster_18 |
| Q2383370 | in | cluster_46 |
| Q3048622 | in | cluster_46 |
| Q948920 | in | cluster_46 |
| Q1352872 | in | cluster_32 |
| Q258661 | in | cluster_32 |
| Q1386420 | in | cluster_32 |
| Q1804720 | in | cluster_32 |
| Q1975383 | in | cluster_32 |
| Q273833 | in | cluster_32 |
| Q467861 | in | cluster_32 |
| Q5112377 | in | cluster_32 |
| Q5178632 | in | cluster_32 |
| Q5301573 | in | cluster_32 |
| Q6794923 | in | cluster_32 |
| Q165421 | in | cluster_46 |
| Q230303 | in | cluster_46 |
| Q316064 | in | cluster_46 |
| Q3290402 | in | cluster_46 |
| Q75326753 | in | cluster_46 |
| Q230654 | in | cluster_53 |
| Q317248 | in | cluster_53 |
| Q2685 | in | cluster_63 |
| Q3436301 | in | cluster_53 |
| Q3529079 | in | cluster_53 |
| Q4773467 | in | cluster_53 |
| Q6769708 | in | cluster_53 |
| Q28109921 | in | cluster_63 |
| Q28109928 | in | cluster_63 |
| Q4521676 | in | cluster_63 |
| Q901541 | in | cluster_63 |
| Q23800185 | in | cluster_63 |
| Q75494768 | in | cluster_63 |
| Q23800370 | in | cluster_63 |
| Q3288486 | in | cluster_63 |
| Q96076900 | in | cluster_63 |
| Q38196234 | in | cluster_63 |
| Q24004771 | in | cluster_63 |
| Q96077739 | in | cluster_53 |
| Q96077740 | in | cluster_53 |
| Q65589427 | in | cluster_53 |
| Q43100988 | in | cluster_63 |
| Q503706 | in | cluster_63 |
| Q4491 | in | cluster_63 |
| Q65589450 | in | cluster_53 |
| Q75496774 | in | cluster_63 |
| Q4616 | in | cluster_46 |


### nested model

```bash
kgtk community-detection -i examples/docs/community-detection-arnold.tsv --method nested
```

| node1 | label | node2 |
| -- | -- | -- |
| Q1086823 | in | cluster_0_4_41 |
| Q345517 | in | cluster_0_0_41 |
| Q432694 | in | cluster_0_4_22 |
| Q75326809 | in | cluster_0_4_41 |
| Q75326777 | in | cluster_0_4_41 |
| Q75326779 | in | cluster_0_4_41 |
| Q75326780 | in | cluster_0_4_41 |
| Q96079835 | in | cluster_0_0_41 |
| Q96079836 | in | cluster_0_4_41 |
| Q96079838 | in | cluster_0_0_41 |
| Q76363382 | in | cluster_0_0_41 |
| Q76363384 | in | cluster_0_4_41 |
| Q76363386 | in | cluster_0_0_41 |
| Q11673 | in | cluster_0_4_20 |
| Q467912 | in | cluster_0_0_20 |
| Q134549 | in | cluster_0_4_24 |
| Q9696 | in | cluster_0_0_24 |
| Q313696 | in | cluster_0_0_37 |
| Q236540 | in | cluster_0_0_37 |
| Q441424 | in | cluster_0_0_13 |
| Q7926996 | in | cluster_0_4_13 |
| Q25310 | in | cluster_0_6_65 |
| Q265595 | in | cluster_0_6_37 |
| Q268799 | in | cluster_0_4_37 |
| Q272401 | in | cluster_0_4_37 |
| Q272908 | in | cluster_0_4_22 |
| Q505178 | in | cluster_0_0_37 |
| Q2383370 | in | cluster_0_4_13 |
| Q3048622 | in | cluster_0_4_13 |
| Q948920 | in | cluster_0_4_13 |
| Q1352872 | in | cluster_0_0_20 |
| Q258661 | in | cluster_0_4_20 |
| Q1386420 | in | cluster_0_4_20 |
| Q1804720 | in | cluster_0_0_20 |
| Q1975383 | in | cluster_0_0_20 |
| Q273833 | in | cluster_0_0_20 |
| Q467861 | in | cluster_0_4_20 |
| Q5112377 | in | cluster_0_4_20 |
| Q5178632 | in | cluster_0_0_20 |
| Q5301573 | in | cluster_0_0_20 |
| Q6794923 | in | cluster_0_4_20 |
| Q165421 | in | cluster_0_0_3 |
| Q230303 | in | cluster_0_0_3 |
| Q316064 | in | cluster_0_0_3 |
| Q3290402 | in | cluster_0_4_3 |
| Q75326753 | in | cluster_0_0_3 |
| Q230654 | in | cluster_0_4_66 |
| Q317248 | in | cluster_0_0_35 |
| Q2685 | in | cluster_0_0_70 |
| Q3436301 | in | cluster_0_0_35 |
| Q3529079 | in | cluster_0_0_35 |
| Q4773467 | in | cluster_0_4_35 |
| Q6769708 | in | cluster_0_0_35 |
| Q28109921 | in | cluster_0_0_70 |
| Q28109928 | in | cluster_0_4_70 |
| Q4521676 | in | cluster_0_4_70 |
| Q901541 | in | cluster_0_0_70 |
| Q23800185 | in | cluster_0_4_70 |
| Q75494768 | in | cluster_0_4_70 |
| Q23800370 | in | cluster_0_0_70 |
| Q3288486 | in | cluster_0_4_70 |
| Q96076900 | in | cluster_0_0_70 |
| Q38196234 | in | cluster_0_0_70 |
| Q24004771 | in | cluster_0_0_70 |
| Q96077739 | in | cluster_0_0_35 |
| Q96077740 | in | cluster_0_4_35 |
| Q65589427 | in | cluster_0_0_35 |
| Q43100988 | in | cluster_0_0_70 |
| Q503706 | in | cluster_0_4_70 |
| Q4491 | in | cluster_0_0_70 |
| Q65589450 | in | cluster_0_0_35 |
| Q75496774 | in | cluster_0_4_70 |
| Q4616 | in | cluster_0_0_13 |


### MCMC model

```bash
kgtk community-detection -i examples/docs/community-detection-arnold.tsv --method mcmc
```

| node1 | label | node2 | node2;prob |
| -- | -- | -- | -- |
| Q1086823 | in | cluster_0 | 1.0 |
| Q345517 | in | cluster_0 | 1.0 |
| Q432694 | in | cluster_1 | 0.8363836383638363 |
| Q75326809 | in | cluster_0 | 1.0 |
| Q75326777 | in | cluster_0 | 1.0 |
| Q75326779 | in | cluster_0 | 1.0 |
| Q75326780 | in | cluster_0 | 1.0 |
| Q96079835 | in | cluster_0 | 0.9998999899989999 |
| Q96079836 | in | cluster_0 | 0.9998999899989999 |
| Q96079838 | in | cluster_0 | 1.0 |
| Q76363382 | in | cluster_0 | 1.0 |
| Q76363384 | in | cluster_0 | 0.9997999799979999 |
| Q76363386 | in | cluster_0 | 1.0 |
| Q11673 | in | cluster_2 | 0.946894689468947 |
| Q467912 | in | cluster_2 | 1.0 |
| Q134549 | in | cluster_3 | 0.9642964296429642 |
| Q9696 | in | cluster_3 | 0.8863886388638864 |
| Q313696 | in | cluster_4 | 0.9994999499949995 |
| Q236540 | in | cluster_4 | 0.9992999299929993 |
| Q441424 | in | cluster_5 | 0.8487848784878488 |
| Q7926996 | in | cluster_5 | 0.5307530753075308 |
| Q25310 | in | cluster_6 | 1.0 |
| Q265595 | in | cluster_4 | 0.9991999199919992 |
| Q268799 | in | cluster_4 | 0.9992999299929993 |
| Q272401 | in | cluster_4 | 0.9995999599959996 |
| Q272908 | in | cluster_1 | 0.9113911391139113 |
| Q505178 | in | cluster_4 | 0.9994999499949995 |
| Q2383370 | in | cluster_5 | 0.8485848584858486 |
| Q3048622 | in | cluster_5 | 0.8487848784878488 |
| Q948920 | in | cluster_5 | 0.8486848684868487 |
| Q1352872 | in | cluster_2 | 1.0 |
| Q258661 | in | cluster_2 | 1.0 |
| Q1386420 | in | cluster_2 | 1.0 |
| Q1804720 | in | cluster_2 | 1.0 |
| Q1975383 | in | cluster_2 | 1.0 |
| Q273833 | in | cluster_2 | 1.0 |
| Q467861 | in | cluster_2 | 1.0 |
| Q5112377 | in | cluster_2 | 1.0 |
| Q5178632 | in | cluster_2 | 1.0 |
| Q5301573 | in | cluster_2 | 1.0 |
| Q6794923 | in | cluster_2 | 1.0 |
| Q165421 | in | cluster_5 | 0.9998999899989999 |
| Q230303 | in | cluster_5 | 1.0 |
| Q316064 | in | cluster_5 | 1.0 |
| Q3290402 | in | cluster_5 | 1.0 |
| Q75326753 | in | cluster_5 | 1.0 |
| Q230654 | in | cluster_8 | 0.9810981098109811 |
| Q317248 | in | cluster_8 | 0.9998999899989999 |
| Q2685 | in | cluster_9 | 1.0 |
| Q3436301 | in | cluster_8 | 1.0 |
| Q3529079 | in | cluster_8 | 0.9998999899989999 |
| Q4773467 | in | cluster_8 | 1.0 |
| Q6769708 | in | cluster_8 | 1.0 |
| Q28109921 | in | cluster_9 | 1.0 |
| Q28109928 | in | cluster_9 | 1.0 |
| Q4521676 | in | cluster_9 | 1.0 |
| Q901541 | in | cluster_9 | 1.0 |
| Q23800185 | in | cluster_9 | 0.9998999899989999 |
| Q75494768 | in | cluster_9 | 1.0 |
| Q23800370 | in | cluster_9 | 1.0 |
| Q3288486 | in | cluster_9 | 1.0 |
| Q96076900 | in | cluster_9 | 0.9860986098609861 |
| Q38196234 | in | cluster_9 | 0.9998999899989999 |
| Q24004771 | in | cluster_9 | 0.9872987298729873 |
| Q96077739 | in | cluster_8 | 0.9916991699169917 |
| Q96077740 | in | cluster_8 | 0.9916991699169917 |
| Q65589427 | in | cluster_8 | 0.9397939793979398 |
| Q43100988 | in | cluster_9 | 0.9841984198419842 |
| Q503706 | in | cluster_9 | 0.9858985898589859 |
| Q4491 | in | cluster_9 | 0.9845984598459846 |
| Q65589450 | in | cluster_8 | 0.9442944294429443 |
| Q75496774 | in | cluster_9 | 0.9880988098809881 |
| Q4616 | in | cluster_5 | 0.5091509150915091 |
