This command loads a TSV edges file into Graph-tool. Then, it can compute centrality metrics and connectivity statistics. Prints the resulting edge file to stdout.

## Usage
```
kgtk graph_statistics [-h] [--directed] [--degrees] [--pagerank] [--hits]
                      [--log LOG_FILE]
                      filename
```

positional arguments:
```
  filename              filename here
```

optional arguments:
```
  -h, --help            show this help message and exit
  --directed            Is the graph directed or not?
  --degrees             Whether or not to compute degree distribution.
  --pagerank            Whether or not to compute PageRank centraility.
  --hits                Whether or not to compute HITS centraility.
  --summary LOG_FILE    Summary file for the global statistics of the graph.
  --statistics-only     If this flag is set, output only the statistics edges.
                        Else, append the statistics to the original graph.
  --vertex-in-degree-property VERTEX_IN_DEGREE
                        Label for edge: vertex in degree property
  --vertex-out-degree-property VERTEX_OUT_DEGREE
                        Label for edge: vertex out degree property
  --page-rank-property VERTEX_PAGERANK
                        Label for pank rank property
  --vertex-hits-authority-property VERTEX_AUTH
                        Label for edge: vertext hits authority
  --vertex-hits-hubs-property VERTEX_HUBS
                        Label for edge: vertex hits hubs
```

## Examples

Import a TSV file into Graph-tool, and compute degrees, pagerank and hits. We store the global statistics to log.txt. 

```
kgtk graph_statistics --directed --degrees --pagerank --hits --statistics-only --summary log.txt ./data/conceptnet_first10.tsv
```
