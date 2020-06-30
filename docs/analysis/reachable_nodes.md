This command will find all nodes reachable from given root nodes in a KGTK edge file. That is, given a set of nodes N and a set of properties P, this command computes the set of nodes R that can be reached from N via paths containing any of the properties in P.

The output file is an edge file that contains the following columns:

- `node1`: this column contains a root node
- `label`: this column contains only 'reachable'
- `node2`: this column contains node that is reachable from a root node

## Usage
```
kgtk reachable-nodes filename OPTIONS
```
***OPTIONS***:

`--root {r1, r2, ...}`: Root nodes to be considered specified as a command line argument.

`--rootfile {string}`: edge file that contains the root nodes in some column.

`--rootfilecolumn`: column of the root file that contains the root nodes. Default: 0.

`--norootheader` Option to specify that file containing root nodes does not contain a header.

`-o {string}`: Path to the output edge file.

`--noheader`: Option to specify that the input file does not contain a header.

`--subj {integer}`: Column in which the subject is given. Default: 0.

`--pred {integer}`: Column in which the predicate is given. Default: 1.

`--obj {integer}`: Column in which the object is given. Default: 2.

`--props {p1, p2, ...}`: Properties to consider while finding reachable nodes. Default: All properties are considered. 

`--undirected`: Option to specify that input file contains undirected graph.

### Examples

Find all the classes that given root nodes are a subclass of (transitive closure). Root nodes are obtained from node2 of P31.tsv (instance of) file. Command is run on P279.tsv (subclass of) file. Generates P279*.tsv. 

!!! info
    Note that example file P279.tsv contains an initial 'id' column so we need to specify the columns for subject(node1), predicate(label), and object(node2)

```
kgtk reachable_nodes P279.tsv --subj 1 --pred 2 --obj 3 --rootfile P31.tsv --rootfilecolumn 3 -o P279*.tsv
```
