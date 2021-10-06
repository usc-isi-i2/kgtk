Given a KGTK edge file, this command can compute centrality metrics and connectivity statistics. The set of metrics to compute are specified by the user. 

The statistics for individual nodes are printed as edges, defaulting to stdout. The summary statistics over the entire graph can be written to a summary file.

### Directed vs. Undirected (bidirectional) Edges

`kgtk graph-statistics` defaults to `--undirected false`.  This
treats the KGTK edges as directed edges from node1 to node2:
(`node1`->`node2`).

When `--undirected true` has been specified, the KGTK edges
are treated as undirected (bidirectional): (`node1`<->`node2`).

When computing statistics, directed edges consider (`node1->`node2`)
as an `out-edge` for `node1` and an `in-edge` for `node2`.
On the other hand, when using undirected (bidirectional) edges,
(`node1`<->`node2) is counted an an out-edge for each of `node1` and
`node2`, and there are no in-edge counts.

## Usage
```
usage: kgtk graph-statistics [-h] [-i INPUT_FILE] [-o OUTPUT_FILE]
                             [--undirected [True|False]]
                             [--histogram [True|False]]
                             [--top-relations [True|False]]
                             [--output-degrees [True|False]]
                             [--output-properties [True|False]]
                             [--pagerank [True|False]] [--hits [True|False]]
                             [--log LOG_FILE] [--statistics-only [True|False]]
                             [--vertex-in-degree-property VERTEX_IN_DEGREE]
                             [--vertex-out-degree-property VERTEX_OUT_DEGREE]
                             [--page-rank-property VERTEX_PAGERANK]
                             [--vertex-hits-authority-property VERTEX_AUTH]
                             [--vertex-hits-hubs-property VERTEX_HUBS]
                             [--print-top-n TOP_N] [-v [optional True|False]]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK input file. (May be omitted or '-' for
                        stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for
                        stdout.)
  --undirected [True|False]
                        Is the graph undirected? If false, then the graph is
                        treated as (node1)->(node2). If true, then the graph
                        is treated as (node1)<->(node2). (default=False)
  --histogram [True|False]
                        Whether or not to compute degree distribution and
                        output it to the log file. (default=False)
  --top-relations [True|False]
                        Whether or not to compute top relations and output
                        them to the log file. (default=True)
  --output-degrees [True|False]
                        Whether or not to output degree edges. (default=True)
  --output-properties [True|False]
                        Whether or not to output property edges.
                        (default=True)
  --pagerank [True|False]
                        Whether or not to compute PageRank centraility and
                        output it to the log file. Note: --undirected improves
                        the pagerank calculation. If you want both pagerank
                        and in/out-degrees, you should make two runs.
                        (default=False)
  --hits [True|False]   Whether or not to compute HITS centraility and output
                        it to the log file. (default=False)
  --log LOG_FILE        Summary file for the global statistics of the graph.
  --statistics-only [True|False]
                        If this flag is set, output only the statistics edges.
                        Else, append the statistics to the original graph.
                        (default=False
  --vertex-in-degree-property VERTEX_IN_DEGREE
                        Label for edge: vertex in degree property. Note: If
                        --undirected is True, then the in-degree will be 0.
                        (default=vertex_in_degree
  --vertex-out-degree-property VERTEX_OUT_DEGREE
                        Label for edge: vertex out degree property. Note: if
                        --undirected is True, the the out-degree will be the
                        sum of the values that would have been calculated for
                        in-degree and -out-degree if --undirected were False.
                        (default=vertex_out_degree)
  --page-rank-property VERTEX_PAGERANK
                        Label for pank rank property.
                        (default=vertex_pagerank)
  --vertex-hits-authority-property VERTEX_AUTH
                        Label for edge: vertext hits authority.
                        (default=vertex_auth)
  --vertex-hits-hubs-property VERTEX_HUBS
                        Label for edge: vertex hits hubs.
                        (default=vertex_hubs)
  --print-top-n TOP_N   Number of top centrality nodes to print. (default=5)

  -v [optional True|False], --verbose [optional True|False]
                        Print additional progress messages (default=False).
```

## Examples

Given this file:

```bash
kgtk cat -i examples/docs/graph-statistics-file1.tsv
```

| node1 | label | node2 |
| -- | -- | -- |
| john | zipcode | 12345 |
| john | zipcode | 12346 |
| peter | zipcode | 12040 |
| peter | zipcode | 12040 |
| steve | zipcode | 45601 |

We can use the following command to compute degree and PageRank statistics over the graph:

```
kgtk graph_statistics --log summary.txt --pagerank --statistics-only -i examples/docs/graph-statistics-file1.tsv
```

The output (printed to stdout by default) is as follows:

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
| steve | vertex_out_degree | 1 | steve-vertex_out_degree-16 |
| steve | vertex_pagerank | 0.10471144347252878 | steve-vertex_pagerank-17 |
| 45601 | vertex_in_degree | 1 | 45601-vertex_in_degree-18 |
| 45601 | vertex_out_degree | 0 | 45601-vertex_out_degree-19 |
| 45601 | vertex_pagerank | 0.19371608066233506 | 45601-vertex_pagerank-20 |

Note that the statistics are printed as edges. Also, the original
graph is not printed because we set the flag `statistics-only`.

We also stored a summary of our metrics in `summary.txt`.

### Example: `--undirected true` vs. `--undirected false`

`kgtk graph-statistics` defaults to `--undirected false`.  This treats
the KGTK edges as directed edges from node1 to node2: (`node1`->`node2`).

Conversely, when `--undirected true` has been specified, the KGTK edges
are treated as undirected (bidirectional): (`node1`<->`node2`).

Statistics for directed edges count (`node1->`node2`) as an `out-edge`
for `node1` and an `in-edge` for `node2`.  Statistics for undirected
(bidirectional) edges count it as an `out-edge` for both `node1` and
`node2`; there are no `in-edge` counts for undirected edges.

Consider the following file, which is an extract from Wikidata
focusing on Q5:

```bash
kgtk cat -i examples/docs/graph-statistics-file2.tsv
```

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| Q5 | P1056 | Q3619132 | Q5-P1056-Q3619132-0db1a245-0 |
| Q5 | P1343 | Q19180675 | Q5-P1343-Q19180675-ffcb1070-0 |
| Q5 | P1343 | Q302556 | Q5-P1343-Q302556-2906e8d9-0 |
| Q5 | P1343 | Q4086271 | Q5-P1343-Q4086271-d1995e89-0 |
| Q5 | P1343 | Q4173137 | Q5-P1343-Q4173137-52594afa-0 |
| Q1000048 | P31 | Q5 | Q1000048-P31-Q5-f02d7495-0 |
| Q1001 | P31 | Q5 | Q1001-P31-Q5-7267f250-0 |
| Q100148353 | P31 | Q5 | Q100148353-P31-Q5-09e515e5-0 |
| Q100153947 | P31 | Q5 | Q100153947-P31-Q5-d902cf76-0 |
| Q100153956 | P31 | Q5 | Q100153956-P31-Q5-5eaa68f6-0 |
| Q100252 | P31 | Q5 | Q100252-P31-Q5-0ac8ef53-0 |
| Q100494914 | P31 | Q5 | Q100494914-P31-Q5-73cf7d3e-0 |
| Q100533268 | P31 | Q5 | Q100533268-P31-Q5-a2acf259-0 |
| Q100558585 | P279 | Q5 | Q100558585-P279-Q5-6f0ab653-0 |
| Q100697582 | P31 | Q5 | Q100697582-P31-Q5-34b6cc1d-0 |
| Q100741820 | P31 | Q5 | Q100741820-P31-Q5-1b14161f-0 |
| Q100741824 | P31 | Q5 | Q100741824-P31-Q5-2d5be55e-0 |
| Q100749 | P31 | Q5 | Q100749-P31-Q5-929a71c0-0 |
| Q100753758 | P31 | Q5 | Q100753758-P31-Q5-edadabfb-0 |
| Q100915302 | P31 | Q5 | Q100915302-P31-Q5-78da0ed0-0 |
| Q100937 | P31 | Q5 | Q100937-P31-Q5-0506e8b6-0 |
| Q100948 | P31 | Q5 | Q100948-P31-Q5-c1e8a616-0 |
| Q1010297 | P31 | Q5 | Q1010297-P31-Q5-c2faa644-0 |
| Q101268 | P31 | Q5 | Q101268-P31-Q5-8799eb44-0 |
| Q101410 | P31 | Q5 | Q101410-P31-Q5-41792799-0 |

Let's compute statistics on this file treating the edges
as directed (the default), focusing on the results for `Q5`:

```bash
kgtk graph-statistics \
    -i examples/docs/graph-statistics-file2.tsv \
    --pagerank True \
    --hits False \
    --undirected False \
    --page-rank-property Ppagerank \
    --vertex-in-degree-property Pindegree \
    --vertex-out-degree-property Poutdegree \
    --statistics-only True \
    / filter -p 'Q5;;'
```
| node1 | label | node2 | id |
| -- | -- | -- | -- |
| Q5 | Pindegree | 20 | Q5-Pindegree-0 |
| Q5 | Poutdegree | 5 | Q5-Poutdegree-1 |
| Q5 | Ppagerank | 0.30874598028371614 | Q5-Ppagerank-2 |

Now, let's compute statistics on this file treating the
edges as undirected (bidirectional):

```bash
kgtk graph-statistics \
    -i examples/docs/graph-statistics-file2.tsv \
    --pagerank True \
    --hits False \
    --undirected True \
    --page-rank-property Ppagerank \
    --vertex-in-degree-property Pindegree \
    --vertex-out-degree-property Poutdegree \
    --statistics-only True \
    / filter -p 'Q5;;'
```
| node1 | label | node2 | id |
| -- | -- | -- | -- |
| Q5 | Pindegree | 0 | Q5-Pindegree-0 |
| Q5 | Poutdegree | 25 | Q5-Poutdegree-1 |
| Q5 | Ppagerank | 0.4625751944545934 | Q5-Ppagerank-2 |
