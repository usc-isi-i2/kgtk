This command will find the connected components in a KGTK edge file. The output file is an edge file which contains the following columns:

- `node1`: this column contains the nodes in the graph
- `label`: this column contains only 'connected_component'
- `node2`: this column contains an integer which represents the component that a node belongs to. Nodes belonging to a connected component will have the same value in this column

## Usage
```
kgtk connected-components filename OPTIONS
```
***OPTIONS***:

`-o {string}`: Path to the output edge file.

`--noheader`: Option to specify that the input file does not contain a header.

`--subj {integer}`: Column in which the subject is given. Default: 0.

`--pred {integer}`: Column in which the predicate is given. Default: 1.

`--obj {integer}`: Column in which the object is given. Default: 2.

`--props {p1, p2, ...}`: Properties to consider while finding connected components. Default: All properties are considered. 

`--undirected`: Option to specify that input file contains undirected graph.

`--strong`: Option to find strongly connected components (If graph is directed), or to treat graph as undirected and find connected components.

### Examples

Find connected URI's that redirect to the same page

```
kgtk connected-components Dbpedia_redirects.tsv -o connected-dbpedia_uris.tsv
```
