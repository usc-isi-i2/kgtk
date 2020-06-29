Given a KGTK edge file, this command can compute centrality metrics and connectivity statistics. The set of metrics to compute are specified by the user. 

The statistics for individual nodes are printed as edges to stdout. The summary statistics over the entire graph can be written to a summary file.

## Usage
```
kgtk graph_statistics [-h] [--directed] [--degrees] [--pagerank]
                             [--hits] [--log LOG_FILE] [--statistics-only]
                             [--vertex-in-degree-property VERTEX_IN_DEGREE]
                             [--vertex-out-degree-property VERTEX_OUT_DEGREE]
                             [--page-rank-property VERTEX_PAGERANK]
                             [--vertex-hits-authority-property VERTEX_AUTH]
                             [--vertex-hits-hubs-property VERTEX_HUBS]
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
  --log LOG_FILE    Summary file for the global statistics of the graph.
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

Given this file `input.tsv`:

| node1 | label | node2 |
| -- | -- | -- |
| john | zipcode | 12345 |
| john | zipcode | 12346 |
| peter | zipcode | 12040 |
| peter | zipcode | 12040 |
| steve | zipcode | 45601 |
| steve | zipcode | 45601 |

We can use the following command to compute degree and PageRank statistics over the graph:

```
kgtk graph_statistics --directed --log summary.txt --pagerank --statistics-only input.tsv
```

The output (printed to stdout) is as follows:

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| john | vertex_in_degree | 0 | john-vertex_in_degree-0 |
| john | vertex_out_degree | 2 | john-vertex_out_degree-1 |
| john | vertex_pagerank | 0.10471144347252878 | john-vertex_pagerank-2 |
| 12345 | vertex_in_degree | 1 | 12345-vertex_in_degree-3 |
| 12345 | vertex_out_degree | 0 | 12345-vertex_out_degree-4 |
| 12345 | vertex_pagerank | 0.14921376206743192 | 12345-vertex_pagerank-5 |
| 12346 | vertex_in_degree | 1 | 12346-vertex_in_degree-6 |
| 12346 | vertex_out_degree | 0 | 12346-vertex_out_degree-7 |
| 12346 | vertex_pagerank | 0.14921376206743192 | 12346-vertex_pagerank-8 |
| peter | vertex_in_degree | 0 | peter-vertex_in_degree-9 |
| peter | vertex_out_degree | 2 | peter-vertex_out_degree-10 |
| peter | vertex_pagerank | 0.10471144347252878 | peter-vertex_pagerank-11 |
| 12040 | vertex_in_degree | 2 | 12040-vertex_in_degree-12 |
| 12040 | vertex_out_degree | 0 | 12040-vertex_out_degree-13 |
| 12040 | vertex_pagerank | 0.1937160806623351 | 12040-vertex_pagerank-14 |
| steve | vertex_in_degree | 0 | steve-vertex_in_degree-15 |
| steve | vertex_out_degree | 2 | steve-vertex_out_degree-16 |
| steve | vertex_pagerank | 0.10471144347252878 | steve-vertex_pagerank-17 |
| 45601 | vertex_in_degree | 2 | 45601-vertex_in_degree-18 |
| 45601 | vertex_out_degree | 0 | 45601-vertex_out_degree-19 |
| 45601 | vertex_pagerank | 0.1937160806623351 | 45601-vertex_pagerank-20 |

Note that the statistics are printed as edges. Also, the original graph is not printed because we set the flag `statistics-only`. We have also stored a summary of our metrics in `summary.txt`, which looks like this:

```
graph loaded! It has 7 nodes and 6 edges

###Top relations:
zipcode	6

###PageRank
Max pageranks
5	steve	0.104711
1	12345	0.149214
4	12040	0.193716
2	12346	0.149214
6	45601	0.193716
```
