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
                                [--method METHOD] [-v [optional True|False]]

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
| Q1086823 | in | cluster_9 |
| Q345517 | in | cluster_9 |
| Q432694 | in | cluster_3 |
| Q75326809 | in | cluster_9 |
| Q75326777 | in | cluster_9 |
| Q75326779 | in | cluster_9 |
| Q75326780 | in | cluster_9 |
| Q96079835 | in | cluster_9 |
| Q96079836 | in | cluster_9 |
| Q96079838 | in | cluster_9 |
| Q76363382 | in | cluster_9 |
| Q76363384 | in | cluster_9 |
| Q76363386 | in | cluster_9 |
| Q11673 | in | cluster_40 |
| Q467912 | in | cluster_40 |
| Q134549 | in | cluster_3 |
| Q9696 | in | cluster_17 |
| Q313696 | in | cluster_18 |
| Q236540 | in | cluster_18 |
| Q441424 | in | cluster_20 |
| Q7926996 | in | cluster_20 |
| Q25310 | in | cluster_22 |
| Q265595 | in | cluster_18 |
| Q268799 | in | cluster_18 |
| Q272401 | in | cluster_18 |
| Q272908 | in | cluster_17 |
| Q505178 | in | cluster_18 |
| Q2383370 | in | cluster_20 |
| Q3048622 | in | cluster_20 |
| Q948920 | in | cluster_20 |
| Q1352872 | in | cluster_40 |
| Q258661 | in | cluster_40 |
| Q1386420 | in | cluster_40 |
| Q1804720 | in | cluster_40 |
| Q1975383 | in | cluster_40 |
| Q273833 | in | cluster_40 |
| Q467861 | in | cluster_40 |
| Q5112377 | in | cluster_40 |
| Q5178632 | in | cluster_40 |
| Q5301573 | in | cluster_40 |
| Q6794923 | in | cluster_40 |
| Q165421 | in | cluster_45 |
| Q230303 | in | cluster_45 |
| Q316064 | in | cluster_45 |
| Q3290402 | in | cluster_45 |
| Q75326753 | in | cluster_45 |
| Q230654 | in | cluster_54 |
| Q317248 | in | cluster_54 |
| Q2685 | in | cluster_58 |
| Q3436301 | in | cluster_54 |
| Q3529079 | in | cluster_54 |
| Q4773467 | in | cluster_54 |
| Q6769708 | in | cluster_54 |
| Q28109921 | in | cluster_58 |
| Q28109928 | in | cluster_58 |
| Q4521676 | in | cluster_58 |
| Q901541 | in | cluster_58 |
| Q23800185 | in | cluster_58 |
| Q75494768 | in | cluster_58 |
| Q23800370 | in | cluster_58 |
| Q3288486 | in | cluster_58 |
| Q96076900 | in | cluster_58 |
| Q38196234 | in | cluster_58 |
| Q24004771 | in | cluster_58 |
| Q96077739 | in | cluster_54 |
| Q96077740 | in | cluster_54 |
| Q65589427 | in | cluster_54 |
| Q43100988 | in | cluster_58 |
| Q503706 | in | cluster_58 |
| Q4491 | in | cluster_58 |
| Q65589450 | in | cluster_54 |
| Q75496774 | in | cluster_58 |
| Q4616 | in | cluster_45 |


### nested model

```bash
kgtk community-detection -i examples/docs/community-detection-arnold.tsv --method nested
```

| node1 | label | node2 |
| -- | -- | -- |
| Q1086823 | in | cluster_0_6_11 |
| Q345517 | in | cluster_0_8_11 |
| Q432694 | in | cluster_0_0_39 |
| Q75326809 | in | cluster_0_6_11 |
| Q75326777 | in | cluster_0_8_11 |
| Q75326779 | in | cluster_0_6_11 |
| Q75326780 | in | cluster_0_8_11 |
| Q96079835 | in | cluster_0_0_11 |
| Q96079836 | in | cluster_0_0_11 |
| Q96079838 | in | cluster_0_8_11 |
| Q76363382 | in | cluster_0_0_11 |
| Q76363384 | in | cluster_0_8_11 |
| Q76363386 | in | cluster_0_6_11 |
| Q11673 | in | cluster_0_6_51 |
| Q467912 | in | cluster_0_8_51 |
| Q134549 | in | cluster_0_6_39 |
| Q9696 | in | cluster_0_6_30 |
| Q313696 | in | cluster_0_0_13 |
| Q236540 | in | cluster_0_8_13 |
| Q441424 | in | cluster_0_8_18 |
| Q7926996 | in | cluster_0_8_18 |
| Q25310 | in | cluster_0_6_22 |
| Q265595 | in | cluster_0_6_13 |
| Q268799 | in | cluster_0_8_13 |
| Q272401 | in | cluster_0_0_13 |
| Q272908 | in | cluster_0_0_30 |
| Q505178 | in | cluster_0_5_13 |
| Q2383370 | in | cluster_0_6_18 |
| Q3048622 | in | cluster_0_6_18 |
| Q948920 | in | cluster_0_0_18 |
| Q1352872 | in | cluster_0_5_51 |
| Q258661 | in | cluster_0_8_51 |
| Q1386420 | in | cluster_0_6_51 |
| Q1804720 | in | cluster_0_0_51 |
| Q1975383 | in | cluster_0_0_51 |
| Q273833 | in | cluster_0_0_51 |
| Q467861 | in | cluster_0_6_51 |
| Q5112377 | in | cluster_0_0_51 |
| Q5178632 | in | cluster_0_0_51 |
| Q5301573 | in | cluster_0_5_51 |
| Q6794923 | in | cluster_0_8_51 |
| Q165421 | in | cluster_0_8_20 |
| Q230303 | in | cluster_0_8_20 |
| Q316064 | in | cluster_0_8_20 |
| Q3290402 | in | cluster_0_8_20 |
| Q75326753 | in | cluster_0_6_20 |
| Q230654 | in | cluster_0_0_46 |
| Q317248 | in | cluster_0_0_70 |
| Q2685 | in | cluster_0_0_47 |
| Q3436301 | in | cluster_0_0_70 |
| Q3529079 | in | cluster_0_8_70 |
| Q4773467 | in | cluster_0_6_70 |
| Q6769708 | in | cluster_0_5_70 |
| Q28109921 | in | cluster_0_8_47 |
| Q28109928 | in | cluster_0_8_47 |
| Q4521676 | in | cluster_0_0_47 |
| Q901541 | in | cluster_0_6_47 |
| Q23800185 | in | cluster_0_8_47 |
| Q75494768 | in | cluster_0_8_47 |
| Q23800370 | in | cluster_0_8_47 |
| Q3288486 | in | cluster_0_0_47 |
| Q96076900 | in | cluster_0_0_47 |
| Q38196234 | in | cluster_0_0_47 |
| Q24004771 | in | cluster_0_0_47 |
| Q96077739 | in | cluster_0_0_70 |
| Q96077740 | in | cluster_0_8_70 |
| Q65589427 | in | cluster_0_6_70 |
| Q43100988 | in | cluster_0_0_47 |
| Q503706 | in | cluster_0_6_47 |
| Q4491 | in | cluster_0_6_47 |
| Q65589450 | in | cluster_0_0_70 |
| Q75496774 | in | cluster_0_0_47 |
| Q4616 | in | cluster_0_6_20 |


### MCMC model

```bash
kgtk community-detection -i examples/docs/community-detection-arnold.tsv --method mcmc
```

| node1 | label | node2 | node2;prob |
| -- | -- | -- | -- |
| Q1086823 | in | cluster_0 | 1.0 |
| Q345517 | in | cluster_0 | 1.0 |
| Q432694 | in | cluster_3 | 0.7686768676867687 |
| Q75326809 | in | cluster_0 | 1.0 |
| Q75326777 | in | cluster_0 | 1.0 |
| Q75326779 | in | cluster_0 | 1.0 |
| Q75326780 | in | cluster_0 | 1.0 |
| Q96079835 | in | cluster_0 | 1.0 |
| Q96079836 | in | cluster_0 | 0.9998999899989999 |
| Q96079838 | in | cluster_0 | 0.9998999899989999 |
| Q76363382 | in | cluster_0 | 0.9998999899989999 |
| Q76363384 | in | cluster_0 | 0.9998999899989999 |
| Q76363386 | in | cluster_0 | 1.0 |
| Q11673 | in | cluster_2 | 0.9456945694569457 |
| Q467912 | in | cluster_2 | 1.0 |
| Q134549 | in | cluster_1 | 0.8934893489348935 |
| Q9696 | in | cluster_1 | 0.8660866086608661 |
| Q313696 | in | cluster_4 | 0.9994999499949995 |
| Q236540 | in | cluster_4 | 0.9994999499949995 |
| Q441424 | in | cluster_7 | 0.8274827482748275 |
| Q7926996 | in | cluster_7 | 0.5159515951595159 |
| Q25310 | in | cluster_6 | 1.0 |
| Q265595 | in | cluster_4 | 0.9995999599959996 |
| Q268799 | in | cluster_4 | 0.9994999499949995 |
| Q272401 | in | cluster_4 | 0.9993999399939995 |
| Q272908 | in | cluster_3 | 0.9943994399439944 |
| Q505178 | in | cluster_4 | 0.9992999299929993 |
| Q2383370 | in | cluster_7 | 0.8272827282728272 |
| Q3048622 | in | cluster_7 | 0.8273827382738274 |
| Q948920 | in | cluster_7 | 0.8272827282728272 |
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
| Q165421 | in | cluster_7 | 1.0 |
| Q230303 | in | cluster_7 | 1.0 |
| Q316064 | in | cluster_7 | 1.0 |
| Q3290402 | in | cluster_7 | 1.0 |
| Q75326753 | in | cluster_7 | 1.0 |
| Q230654 | in | cluster_8 | 0.9826982698269827 |
| Q317248 | in | cluster_8 | 0.9997999799979999 |
| Q2685 | in | cluster_9 | 1.0 |
| Q3436301 | in | cluster_8 | 0.9998999899989999 |
| Q3529079 | in | cluster_8 | 1.0 |
| Q4773467 | in | cluster_8 | 0.9998999899989999 |
| Q6769708 | in | cluster_8 | 1.0 |
| Q28109921 | in | cluster_9 | 1.0 |
| Q28109928 | in | cluster_9 | 1.0 |
| Q4521676 | in | cluster_9 | 1.0 |
| Q901541 | in | cluster_9 | 1.0 |
| Q23800185 | in | cluster_9 | 1.0 |
| Q75494768 | in | cluster_9 | 1.0 |
| Q23800370 | in | cluster_9 | 0.9998999899989999 |
| Q3288486 | in | cluster_9 | 1.0 |
| Q96076900 | in | cluster_9 | 0.987998799879988 |
| Q38196234 | in | cluster_9 | 0.9998999899989999 |
| Q24004771 | in | cluster_9 | 0.9867986798679867 |
| Q96077739 | in | cluster_8 | 0.9931993199319932 |
| Q96077740 | in | cluster_8 | 0.9913991399139914 |
| Q65589427 | in | cluster_8 | 0.9426942694269427 |
| Q43100988 | in | cluster_9 | 0.986998699869987 |
| Q503706 | in | cluster_9 | 0.988998899889989 |
| Q4491 | in | cluster_9 | 0.9871987198719872 |
| Q65589450 | in | cluster_8 | 0.9425942594259425 |
| Q75496774 | in | cluster_9 | 0.9872987298729873 |
| Q4616 | in | cluster_7 | 0.5119511951195119 |
