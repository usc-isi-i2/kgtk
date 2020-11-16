This command will find the connected components in a KGTK edge file. The output file is an edge file which contains the following columns:

- `node1`: this column contains the nodes in the graph
- `label`: this column contains only 'connected_component'
- `node2`: this column contains an integer which represents the component that a node belongs to. Nodes belonging to a connected component will have the same value in this column

## Usage
```
Usage: kgtk connected-components [-h] [-i INPUT_FILE] [-o OUTPUT_FILE] [--properties PROPERTIES] [--undirected] [--strong]
                                 [--cluster-name-method {cat,hash,first,last,shortest,longest,numbered,prefixed,lowest,highest}]
                                 [--cluster-name-separator CLUSTER_NAME_SEPARATOR] [--cluster-name-prefix CLUSTER_NAME_PREFIX]
                                 [--cluster-name-zfill CLUSTER_NAME_ZFILL] [--minimum-cluster-size MINIMUM_CLUSTER_SIZE] [-v]

Find all the connected components in an undirected or directed Graph.

Additional options are shown in expert help.
kgtk --expert connected-components --help

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK file to find connected components in. (May be omitted or '-' for stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for stdout.)
  --properties PROPERTIES
                        A comma separated list of properties to traverse while finding connected components, by default all properties will be considered
  --undirected          Specify if the input graph is undirected, default FALSE
  --strong              Treat graph as directed or not, independent of its actual directionality.
  --cluster-name-method {cat,hash,first,last,shortest,longest,numbered,prefixed,lowest,highest}
                        Determine the naming method for clusters. (default=Method.HASH)
  --cluster-name-separator CLUSTER_NAME_SEPARATOR
                        Specify the separator to be used in cat and hash cluster name methods. (default=+)
  --cluster-name-prefix CLUSTER_NAME_PREFIX
                        Specify the prefix to be used in the prefixed and hash cluster name methods. (default=CLUS)
  --cluster-name-zfill CLUSTER_NAME_ZFILL
                        Specify the zfill to be used in the numbered and prefixed cluster name methods. (default=4)
  --minimum-cluster-size MINIMUM_CLUSTER_SIZE
                        Specify the minimum cluster size. (default=2)

  -v, --verbose         Print additional progress messages (default=False).
```
***OPTIONS***:

`-o {string}`: Path to the output edge file.

`--properties {p1, p2, ...}`: Properties to consider while finding connected components. Default: All properties are considered. 

`--undirected`: Option to specify that input file contains undirected graph.

`--strong`: Option to find strongly connected components (If graph is directed), or to treat graph as undirected and find connected components.

### Examples

Find connected URI's that redirect to the same page

```
kgtk connected-components -i Dbpedia_redirects.tsv -o connected-dbpedia_uris.tsv
```
