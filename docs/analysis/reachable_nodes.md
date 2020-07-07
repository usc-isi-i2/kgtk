This command will find all nodes reachable from given root nodes in a KGTK edge file. That is, given a set of nodes N and a set of properties P, this command computes the set of nodes R that can be reached from N via paths containing any of the properties in P.

The output file is an edge file that contains the following columns:

- `node1`: this column contains a root node
- `label`: this column contains only 'reachable'
- `node2`: this column contains node that is reachable from a root node

## Usage
```
usage: kgtk reachable-nodes [-h] [--root ROOT] [--rootfile ROOTFILE]
                            [--rootfilecolumn ROOTFILECOLUMN] [--norootheader] [-o OUTPUT]
                            [--noheader] [--subj SUB] [--obj OBJ] [--pred PRED]
                            [--props PROPS] [--undirected]
                            filename

positional arguments:
  filename              input filename here

optional arguments:
  -h, --help            show this help message and exit
  --root ROOT           Set of root nodes to use, comma-separated string
  --rootfile ROOTFILE   Option to specify a file containing the set of root nodes
  --rootfilecolumn ROOTFILECOLUMN
                        Option to specify column of roots file to use, default 0
  --norootheader        Option to specify that root file has no header
  -o OUTPUT, --out OUTPUT
                        File to output the reachable nodes,if empty will be written out to
                        standard output
  --noheader            Option to specify that file does not have a header
  --subj SUB            Column in which the subject is given, default 0
  --obj OBJ             Column in which the subject is given, default 2
  --pred PRED           Column in which predicate is given, default 1
  --props PROPS         Properties to consider while finding reachable nodes - comma-
                        separated string,default all properties
  --undirected          Option to specify graph as undirected?
```

### Examples

Find all the classes that given root nodes are a subclass of (transitive closure). Root nodes are obtained from node2 of P31.tsv (instance of) file. Command is run on P279.tsv (subclass of) file. Generates P279*.tsv. 

!!! info
    Note that example file P279.tsv contains an initial 'id' column so we need to specify the columns for subject(node1), predicate(label), and object(node2)

```
kgtk reachable-nodes P279.tsv --subj 1 --pred 2 --obj 3 --rootfile P31.tsv --rootfilecolumn 3 -o P279*.tsv
```
