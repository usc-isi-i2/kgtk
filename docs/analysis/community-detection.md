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
kgtk head -i examples/docs/community-detection-arnold.tsv
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
| Q1086823 | P40 | Q76363382 | 'Christopher Lawford'@en | 'child'@en | 'David Christopher Lawford'@en |


Find the communities using blockmodel.

```bash
kgtk community-detection -i examples/docs/community-detection-arnold.tsv --method blockmodel
```

| node1 | label | node2 |
| -- | -- | -- |
| Q1086823 | in | cluster_7 |
| Q345517 | in | cluster_7 |
| Q432694 | in | cluster_27 |
| Q75326809 | in | cluster_7 |
| Q75326777 | in | cluster_7 |
| Q75326779 | in | cluster_7 |
| Q75326780 | in | cluster_7 |
| Q96079835 | in | cluster_7 |
| Q96079836 | in | cluster_7 |
| Q96079838 | in | cluster_7 |
| Q76363382 | in | cluster_7 |
| Q76363384 | in | cluster_7 |
| Q76363386 | in | cluster_7 |
| Q11673 | in | cluster_41 |
| Q467912 | in | cluster_41 |
| Q134549 | in | cluster_28 |
| Q9696 | in | cluster_27 |
| Q313696 | in | cluster_28 |
| Q236540 | in | cluster_28 |
| Q441424 | in | cluster_28 |
| Q7926996 | in | cluster_28 |
| Q25310 | in | cluster_22 |
| Q265595 | in | cluster_28 |
| Q268799 | in | cluster_28 |
| Q272401 | in | cluster_28 |
| Q272908 | in | cluster_27 |
| Q505178 | in | cluster_28 |
| Q2383370 | in | cluster_28 |
| Q3048622 | in | cluster_28 |
| Q948920 | in | cluster_28 |
| Q1352872 | in | cluster_41 |
| Q258661 | in | cluster_41 |
| Q1386420 | in | cluster_41 |
| Q1804720 | in | cluster_41 |
| Q1975383 | in | cluster_41 |
| Q273833 | in | cluster_41 |
| Q467861 | in | cluster_41 |
| Q5112377 | in | cluster_41 |
| Q5178632 | in | cluster_41 |
| Q5301573 | in | cluster_41 |
| Q6794923 | in | cluster_41 |
| Q165421 | in | cluster_46 |
| Q230303 | in | cluster_46 |
| Q316064 | in | cluster_46 |
| Q3290402 | in | cluster_46 |
| Q75326753 | in | cluster_46 |
| Q230654 | in | cluster_47 |
| Q317248 | in | cluster_47 |
| Q2685 | in | cluster_57 |
| Q3436301 | in | cluster_47 |
| Q3529079 | in | cluster_47 |
| Q4773467 | in | cluster_47 |
| Q6769708 | in | cluster_47 |
| Q28109921 | in | cluster_57 |
| Q28109928 | in | cluster_57 |
| Q4521676 | in | cluster_57 |
| Q901541 | in | cluster_57 |
| Q23800185 | in | cluster_57 |
| Q75494768 | in | cluster_57 |
| Q23800370 | in | cluster_57 |
| Q3288486 | in | cluster_57 |
| Q96076900 | in | cluster_57 |
| Q38196234 | in | cluster_57 |
| Q24004771 | in | cluster_57 |
| Q96077739 | in | cluster_47 |
| Q96077740 | in | cluster_47 |
| Q65589427 | in | cluster_47 |
| Q43100988 | in | cluster_57 |
| Q503706 | in | cluster_57 |
| Q4491 | in | cluster_57 |
| Q65589450 | in | cluster_47 |
| Q75496774 | in | cluster_57 |
| Q4616 | in | cluster_46 |


### nested model

```bash
kgtk community-detection -i examples/docs/community-detection-arnold.tsv --method nested
```

| node1 | label | node2 |
| -- | -- | -- |
| Q1086823 | in | cluster_0_0_27 |
| Q345517 | in | cluster_0_5_27 |
| Q432694 | in | cluster_0_0_61 |
| Q75326809 | in | cluster_0_7_27 |
| Q75326777 | in | cluster_0_0_27 |
| Q75326779 | in | cluster_0_0_27 |
| Q75326780 | in | cluster_0_5_27 |
| Q96079835 | in | cluster_0_5_27 |
| Q96079836 | in | cluster_0_5_27 |
| Q96079838 | in | cluster_0_0_27 |
| Q76363382 | in | cluster_0_5_27 |
| Q76363384 | in | cluster_0_7_27 |
| Q76363386 | in | cluster_0_5_27 |
| Q11673 | in | cluster_0_5_34 |
| Q467912 | in | cluster_0_7_34 |
| Q134549 | in | cluster_0_5_23 |
| Q9696 | in | cluster_0_7_61 |
| Q313696 | in | cluster_0_7_54 |
| Q236540 | in | cluster_0_5_54 |
| Q441424 | in | cluster_0_5_9 |
| Q7926996 | in | cluster_0_0_9 |
| Q25310 | in | cluster_0_7_49 |
| Q265595 | in | cluster_0_5_54 |
| Q268799 | in | cluster_0_0_54 |
| Q272401 | in | cluster_0_5_54 |
| Q272908 | in | cluster_0_5_61 |
| Q505178 | in | cluster_0_5_54 |
| Q2383370 | in | cluster_0_7_9 |
| Q3048622 | in | cluster_0_0_9 |
| Q948920 | in | cluster_0_0_9 |
| Q1352872 | in | cluster_0_5_34 |
| Q258661 | in | cluster_0_5_34 |
| Q1386420 | in | cluster_0_7_34 |
| Q1804720 | in | cluster_0_5_34 |
| Q1975383 | in | cluster_0_0_34 |
| Q273833 | in | cluster_0_7_34 |
| Q467861 | in | cluster_0_0_34 |
| Q5112377 | in | cluster_0_0_34 |
| Q5178632 | in | cluster_0_5_34 |
| Q5301573 | in | cluster_0_5_34 |
| Q6794923 | in | cluster_0_2_34 |
| Q165421 | in | cluster_0_0_32 |
| Q230303 | in | cluster_0_0_32 |
| Q316064 | in | cluster_0_0_32 |
| Q3290402 | in | cluster_0_0_32 |
| Q75326753 | in | cluster_0_0_32 |
| Q230654 | in | cluster_0_5_52 |
| Q317248 | in | cluster_0_7_63 |
| Q2685 | in | cluster_0_0_1 |
| Q3436301 | in | cluster_0_0_63 |
| Q3529079 | in | cluster_0_0_63 |
| Q4773467 | in | cluster_0_7_63 |
| Q6769708 | in | cluster_0_5_63 |
| Q28109921 | in | cluster_0_5_1 |
| Q28109928 | in | cluster_0_0_1 |
| Q4521676 | in | cluster_0_7_1 |
| Q901541 | in | cluster_0_7_1 |
| Q23800185 | in | cluster_0_0_1 |
| Q75494768 | in | cluster_0_5_1 |
| Q23800370 | in | cluster_0_0_1 |
| Q3288486 | in | cluster_0_7_1 |
| Q96076900 | in | cluster_0_2_1 |
| Q38196234 | in | cluster_0_0_1 |
| Q24004771 | in | cluster_0_5_1 |
| Q96077739 | in | cluster_0_7_63 |
| Q96077740 | in | cluster_0_5_63 |
| Q65589427 | in | cluster_0_0_63 |
| Q43100988 | in | cluster_0_7_1 |
| Q503706 | in | cluster_0_0_1 |
| Q4491 | in | cluster_0_7_1 |
| Q65589450 | in | cluster_0_2_63 |
| Q75496774 | in | cluster_0_0_1 |
| Q4616 | in | cluster_0_5_54 |


### MCMC model

```bash
kgtk community-detection -i examples/docs/community-detection-arnold.tsv --method mcmc
```

| node1 | label | node2 | node2;prob |
| -- | -- | -- | -- |
| Q1086823 | in | cluster_0 | 1.0 |
| Q345517 | in | cluster_0 | 1.0 |
| Q432694 | in | cluster_1 | 0.9277927792779278 |
| Q75326809 | in | cluster_0 | 1.0 |
| Q75326777 | in | cluster_0 | 1.0 |
| Q75326779 | in | cluster_0 | 1.0 |
| Q75326780 | in | cluster_0 | 1.0 |
| Q96079835 | in | cluster_0 | 0.9996999699969997 |
| Q96079836 | in | cluster_0 | 1.0 |
| Q96079838 | in | cluster_0 | 1.0 |
| Q76363382 | in | cluster_0 | 0.9998999899989999 |
| Q76363384 | in | cluster_0 | 0.9996999699969997 |
| Q76363386 | in | cluster_0 | 1.0 |
| Q11673 | in | cluster_2 | 0.9451945194519452 |
| Q467912 | in | cluster_2 | 1.0 |
| Q134549 | in | cluster_8 | 0.8317831783178318 |
| Q9696 | in | cluster_8 | 0.8682868286828683 |
| Q313696 | in | cluster_3 | 0.9992999299929993 |
| Q236540 | in | cluster_3 | 0.9993999399939995 |
| Q441424 | in | cluster_4 | 0.7464746474647465 |
| Q7926996 | in | cluster_4 | 0.46274627462746276 |
| Q25310 | in | cluster_5 | 1.0 |
| Q265595 | in | cluster_3 | 0.9992999299929993 |
| Q268799 | in | cluster_3 | 0.9994999499949995 |
| Q272401 | in | cluster_3 | 0.9997999799979999 |
| Q272908 | in | cluster_1 | 0.7459745974597459 |
| Q505178 | in | cluster_3 | 0.9992999299929993 |
| Q2383370 | in | cluster_4 | 0.7464746474647465 |
| Q3048622 | in | cluster_4 | 0.7464746474647465 |
| Q948920 | in | cluster_4 | 0.7465746574657466 |
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
| Q165421 | in | cluster_4 | 1.0 |
| Q230303 | in | cluster_4 | 1.0 |
| Q316064 | in | cluster_4 | 1.0 |
| Q3290402 | in | cluster_4 | 0.9998999899989999 |
| Q75326753 | in | cluster_4 | 1.0 |
| Q230654 | in | cluster_6 | 0.9822982298229823 |
| Q317248 | in | cluster_6 | 1.0 |
| Q2685 | in | cluster_7 | 1.0 |
| Q3436301 | in | cluster_6 | 0.9998999899989999 |
| Q3529079 | in | cluster_6 | 0.9998999899989999 |
| Q4773467 | in | cluster_6 | 1.0 |
| Q6769708 | in | cluster_6 | 1.0 |
| Q28109921 | in | cluster_7 | 0.9998999899989999 |
| Q28109928 | in | cluster_7 | 1.0 |
| Q4521676 | in | cluster_7 | 1.0 |
| Q901541 | in | cluster_7 | 1.0 |
| Q23800185 | in | cluster_7 | 0.9998999899989999 |
| Q75494768 | in | cluster_7 | 0.9996999699969997 |
| Q23800370 | in | cluster_7 | 0.9998999899989999 |
| Q3288486 | in | cluster_7 | 1.0 |
| Q96076900 | in | cluster_7 | 0.9871987198719872 |
| Q38196234 | in | cluster_7 | 1.0 |
| Q24004771 | in | cluster_7 | 0.9858985898589859 |
| Q96077739 | in | cluster_6 | 0.995099509950995 |
| Q96077740 | in | cluster_6 | 0.993999399939994 |
| Q65589427 | in | cluster_6 | 0.9413941394139413 |
| Q43100988 | in | cluster_7 | 0.9896989698969897 |
| Q503706 | in | cluster_7 | 0.9912991299129913 |
| Q4491 | in | cluster_7 | 0.9895989598959896 |
| Q65589450 | in | cluster_6 | 0.938993899389939 |
| Q75496774 | in | cluster_7 | 0.9860986098609861 |
| Q4616 | in | cluster_4 | 0.49294929492949296 |
