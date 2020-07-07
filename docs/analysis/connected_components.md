This command will find the connected components in a KGTK edge file. The output file is an edge file which contains the following columns:

- `node1`: this column contains the nodes in the graph
- `label`: this column contains only 'connected_component'
- `node2`: this column contains an integer which represents the component that a node belongs to. Nodes belonging to a connected component will have the same value in this column

## Usage
```
usage: kgtk connected-components [-h] [-i INPUT_FILE] [-o OUTPUT_FILE] [--no-header]
                                 [--properties PROPERTIES] [--undirected] [--strong] [-v]
                                 [INPUT_FILE]

Find all the connected components in an undirected or directed Graph.

Additional options are shown in expert help.
kgtk --expert connected-components --help

positional arguments:
  INPUT_FILE            The KGTK file to find connected components in. (May be omitted or
                        '-' for stdin.) (Deprecated, use -i INPUT_FILE)

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK file to find connected components in. (May be omitted or
                        '-' for stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for stdout.)
  --no-header           Specify if the input file does not have a header, default FALSE
  --properties PROPERTIES
                        A comma separated list of properties to traverse while finding
                        connected components, by default all properties will be considered
  --undirected          Specify if the input graph is undirected, default FALSE
  --strong              Treat graph as directed or not, independent of its actual
                        directionality.

  -v, --verbose         Print additional progress messages (default=False).
```
***OPTIONS***:

`-o {string}`: Path to the output edge file.

`--noheader`: Option to specify that the input file does not contain a header.

`--props {p1, p2, ...}`: Properties to consider while finding connected components. Default: All properties are considered. 

`--undirected`: Option to specify that input file contains undirected graph.

`--strong`: Option to find strongly connected components (If graph is directed), or to treat graph as undirected and find connected components.

### Examples

Find connected URI's that redirect to the same page

```
kgtk connected-components Dbpedia_redirects.tsv -o connected-dbpedia_uris.tsv
```
