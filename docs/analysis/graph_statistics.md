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

By default, in-degrees, out-degrees, and pageranks will be computed and
output.  HITS properties will be computed an doutput for directed graphs, but
not for undirected ones.

## Usage
```
usage: kgtk graph-statistics [-h] [-i INPUT_FILE] [-o OUTPUT_FILE]
                             [--undirected [True|False]]
                             [--compute-pagerank [True|False]]
                             [--compute-hits [True|False]]
                             [--output-statistics-only [True|False]]
                             [--output-degrees [True|False]]
                             [--output-pagerank [True|False]]
                             [--output-hits [True|False]]
                             [--log-file LOG_FILE]
                             [--log-top-relations [True|False]]
                             [--log-degrees-histogram [True|False]]
                             [--log-top-pageranks [True|False]]
                             [--log-top-hits [True|False]] [--log-top-n TOP_N]
                             [--vertex-in-degree-property VERTEX_IN_DEGREE]
                             [--vertex-out-degree-property VERTEX_OUT_DEGREE]
                             [--page-rank-property VERTEX_PAGERANK]
                             [--vertex-hits-authority-property VERTEX_AUTH]
                             [--vertex-hits-hubs-property VERTEX_HUBS]
                             [-v [optional True|False]]

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
                        is treated as (node1)<->(node2). Also, HITS will not
                        be computed on undirected graphs. (default=False)
  --compute-pagerank [True|False]
                        Whether or not to compute the PageRank property. Note:
                        --undirected improves the pagerank calculation. If you
                        want both pagerank and in/out-degrees, you should make
                        two runs. (default=True)
  --compute-hits [True|False]
                        Whether or not to compute the HITS properties. Note:
                        --undirected disables HITS calculation. (default=True)
  --output-statistics-only [True|False]
                        If this option is set, write only the statistics edges
                        to the primary output file. Else, write both the
                        statistics and the original graph. (default=False
  --output-degrees [True|False]
                        Whether or not to write degree edges to the primary
                        output file. (default=True)
  --output-pagerank [True|False]
                        Whether or not to write pagerank edges to the primary
                        output file. (default=True)
  --output-hits [True|False]
                        Whether or not to write HITS edges to the primary
                        output file. (default=True)
  --log-file LOG_FILE   Summary file for the global statistics of the graph.
  --log-top-relations [True|False]
                        Whether or not to compute top relations and output
                        them to the log file. (default=True)
  --log-degrees-histogram [True|False]
                        Whether or not to compute degree distribution and
                        output it to the log file. (default=True)
  --log-top-pageranks [True|False]
                        Whether or not to output PageRank centrality top-n to
                        the log file. (default=True)
  --log-top-hits [True|False]
                        Whether or not to output the top-n HITS to the log
                        file. (default=True)
  --log-top-n TOP_N     Number of top centrality nodes to write to the log
                        file. (default=5)
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

### Example: Default Options

By default, all statistics will be computed and written to the log file
and the output KGTK file.  The output KGTK file will contain the input edges
followed by the newly-computed statistics.

```
kgtk graph_statistics \
     -i examples/docs/graph-statistics-file1.tsv \
     --log-file summary.txt
```

The primary output in KGTK format is as follows:

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| john | zipcode | 12345 | john-zipcode-0 |
| john | zipcode | 12346 | john-zipcode-1 |
| peter | zipcode | 12040 | peter-zipcode-2 |
| peter | zipcode | 12040 | peter-zipcode-3 |
| steve | zipcode | 45601 | steve-zipcode-4 |
| john | vertex_in_degree | 0 | john-vertex_in_degree-0 |
| john | vertex_out_degree | 2 | john-vertex_out_degree-1 |
| john | vertex_pagerank | 0.10471144347252878 | john-vertex_pagerank-2 |
| john | vertex_auth | 9.536743164058163e-07 | john-vertex_auth-3 |
| john | vertex_hubs | 0.0 | john-vertex_hubs-4 |
| 12345 | vertex_in_degree | 1 | 12345-vertex_in_degree-5 |
| 12345 | vertex_out_degree | 0 | 12345-vertex_out_degree-6 |
| 12345 | vertex_pagerank | 0.14921376206743192 | 12345-vertex_pagerank-7 |
| 12345 | vertex_auth | 0.0 | 12345-vertex_auth-8 |
| 12345 | vertex_hubs | 9.536743164053826e-07 | 12345-vertex_hubs-9 |
| 12346 | vertex_in_degree | 1 | 12346-vertex_in_degree-10 |
| 12346 | vertex_out_degree | 0 | 12346-vertex_out_degree-11 |
| 12346 | vertex_pagerank | 0.14921376206743192 | 12346-vertex_pagerank-12 |
| 12346 | vertex_auth | 0.0 | 12346-vertex_auth-13 |
| 12346 | vertex_hubs | 9.536743164053826e-07 | 12346-vertex_hubs-14 |
| peter | vertex_in_degree | 0 | peter-vertex_in_degree-15 |
| peter | vertex_out_degree | 2 | peter-vertex_out_degree-16 |
| peter | vertex_pagerank | 0.10471144347252878 | peter-vertex_pagerank-17 |
| peter | vertex_auth | 0.9999999999995453 | peter-vertex_auth-18 |
| peter | vertex_hubs | 0.0 | peter-vertex_hubs-19 |
| 12040 | vertex_in_degree | 2 | 12040-vertex_in_degree-20 |
| 12040 | vertex_out_degree | 0 | 12040-vertex_out_degree-21 |
| 12040 | vertex_pagerank | 0.1937160806623351 | 12040-vertex_pagerank-22 |
| 12040 | vertex_auth | 0.0 | 12040-vertex_auth-23 |
| 12040 | vertex_hubs | 0.9999999999990905 | 12040-vertex_hubs-24 |
| steve | vertex_in_degree | 0 | steve-vertex_in_degree-25 |
| steve | vertex_out_degree | 1 | steve-vertex_out_degree-26 |
| steve | vertex_pagerank | 0.10471144347252878 | steve-vertex_pagerank-27 |
| steve | vertex_auth | 9.094947017725146e-13 | steve-vertex_auth-28 |
| steve | vertex_hubs | 0.0 | steve-vertex_hubs-29 |
| 45601 | vertex_in_degree | 1 | 45601-vertex_in_degree-30 |
| 45601 | vertex_out_degree | 0 | 45601-vertex_out_degree-31 |
| 45601 | vertex_pagerank | 0.19371608066233506 | 45601-vertex_pagerank-32 |
| 45601 | vertex_auth | 0.0 | 45601-vertex_auth-33 |
| 45601 | vertex_hubs | 9.094947017721011e-13 | 45601-vertex_hubs-34 |

Here is what's written to the log file, `summary.txt`:

```
cat summary.txt
```

~~~
graph loaded! It has 7 nodes and 5 edges

###Top relations:
zipcode	5

###Degrees:
in degree stats: mean=0.714286, std=0.264520, max=1
out degree stats: mean=0.714286, std=0.332847, max=1
total degree stats: mean=1.428571, std=0.187044, max=1

###PageRank
Max pageranks
4	12040	0.193716
6	45601	0.193716
1	12345	0.149214
2	12346	0.149214
5	steve	0.104711

###HITS
HITS hubs
4	12040	1.000000
1	12345	0.000001
2	12346	0.000001
6	45601	0.000000
5	steve	0.000000
HITS auth
3	peter	1.000000
0	john	0.000001
5	steve	0.000000
4	12040	0.000000
6	45601	0.000000
~~~

### Example: Output Only Statistics

Compute the statistics and output them, but do not copy the
input edges to the statistics:

```
kgtk graph_statistics \
     -i examples/docs/graph-statistics-file1.tsv \
     --log-file summary.txt \
     --output-statistics-only
```

The output is as follows:

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| john | vertex_in_degree | 0 | john-vertex_in_degree-0 |
| john | vertex_out_degree | 2 | john-vertex_out_degree-1 |
| john | vertex_pagerank | 0.10471144347252878 | john-vertex_pagerank-2 |
| john | vertex_auth | 9.536743164058163e-07 | john-vertex_auth-3 |
| john | vertex_hubs | 0.0 | john-vertex_hubs-4 |
| 12345 | vertex_in_degree | 1 | 12345-vertex_in_degree-5 |
| 12345 | vertex_out_degree | 0 | 12345-vertex_out_degree-6 |
| 12345 | vertex_pagerank | 0.14921376206743192 | 12345-vertex_pagerank-7 |
| 12345 | vertex_auth | 0.0 | 12345-vertex_auth-8 |
| 12345 | vertex_hubs | 9.536743164053826e-07 | 12345-vertex_hubs-9 |
| 12346 | vertex_in_degree | 1 | 12346-vertex_in_degree-10 |
| 12346 | vertex_out_degree | 0 | 12346-vertex_out_degree-11 |
| 12346 | vertex_pagerank | 0.14921376206743192 | 12346-vertex_pagerank-12 |
| 12346 | vertex_auth | 0.0 | 12346-vertex_auth-13 |
| 12346 | vertex_hubs | 9.536743164053826e-07 | 12346-vertex_hubs-14 |
| peter | vertex_in_degree | 0 | peter-vertex_in_degree-15 |
| peter | vertex_out_degree | 2 | peter-vertex_out_degree-16 |
| peter | vertex_pagerank | 0.10471144347252878 | peter-vertex_pagerank-17 |
| peter | vertex_auth | 0.9999999999995453 | peter-vertex_auth-18 |
| peter | vertex_hubs | 0.0 | peter-vertex_hubs-19 |
| 12040 | vertex_in_degree | 2 | 12040-vertex_in_degree-20 |
| 12040 | vertex_out_degree | 0 | 12040-vertex_out_degree-21 |
| 12040 | vertex_pagerank | 0.1937160806623351 | 12040-vertex_pagerank-22 |
| 12040 | vertex_auth | 0.0 | 12040-vertex_auth-23 |
| 12040 | vertex_hubs | 0.9999999999990905 | 12040-vertex_hubs-24 |
| steve | vertex_in_degree | 0 | steve-vertex_in_degree-25 |
| steve | vertex_out_degree | 1 | steve-vertex_out_degree-26 |
| steve | vertex_pagerank | 0.10471144347252878 | steve-vertex_pagerank-27 |
| steve | vertex_auth | 9.094947017725146e-13 | steve-vertex_auth-28 |
| steve | vertex_hubs | 0.0 | steve-vertex_hubs-29 |
| 45601 | vertex_in_degree | 1 | 45601-vertex_in_degree-30 |
| 45601 | vertex_out_degree | 0 | 45601-vertex_out_degree-31 |
| 45601 | vertex_pagerank | 0.19371608066233506 | 45601-vertex_pagerank-32 |
| 45601 | vertex_auth | 0.0 | 45601-vertex_auth-33 |
| 45601 | vertex_hubs | 9.094947017721011e-13 | 45601-vertex_hubs-34 |

Here is what's written to the log file, `summary.txt`:

```
cat summary.txt
```

~~~
graph loaded! It has 7 nodes and 5 edges

###Top relations:
zipcode	5

###Degrees:
in degree stats: mean=0.714286, std=0.264520, max=1
out degree stats: mean=0.714286, std=0.332847, max=1
total degree stats: mean=1.428571, std=0.187044, max=1

###PageRank
Max pageranks
4	12040	0.193716
6	45601	0.193716
1	12345	0.149214
2	12346	0.149214
5	steve	0.104711

###HITS
HITS hubs
4	12040	1.000000
1	12345	0.000001
2	12346	0.000001
6	45601	0.000000
5	steve	0.000000
HITS auth
3	peter	1.000000
0	john	0.000001
5	steve	0.000000
4	12040	0.000000
6	45601	0.000000
~~~
### Example: Rename the Output Relationships

```
kgtk graph_statistics \
     -i examples/docs/graph-statistics-file1.tsv \
     --log-file summary.txt \
     --output-statistics-only \
     --page-rank-property Ppagerank \
     --vertex-in-degree-property Pindegree \
     --vertex-out-degree-property Poutdegree
```

The output (printed to stdout by default) is as follows:

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| john | Pindegree | 0 | john-Pindegree-0 |
| john | Poutdegree | 2 | john-Poutdegree-1 |
| john | Ppagerank | 0.10471144347252878 | john-Ppagerank-2 |
| john | vertex_auth | 9.536743164058163e-07 | john-vertex_auth-3 |
| john | vertex_hubs | 0.0 | john-vertex_hubs-4 |
| 12345 | Pindegree | 1 | 12345-Pindegree-5 |
| 12345 | Poutdegree | 0 | 12345-Poutdegree-6 |
| 12345 | Ppagerank | 0.14921376206743192 | 12345-Ppagerank-7 |
| 12345 | vertex_auth | 0.0 | 12345-vertex_auth-8 |
| 12345 | vertex_hubs | 9.536743164053826e-07 | 12345-vertex_hubs-9 |
| 12346 | Pindegree | 1 | 12346-Pindegree-10 |
| 12346 | Poutdegree | 0 | 12346-Poutdegree-11 |
| 12346 | Ppagerank | 0.14921376206743192 | 12346-Ppagerank-12 |
| 12346 | vertex_auth | 0.0 | 12346-vertex_auth-13 |
| 12346 | vertex_hubs | 9.536743164053826e-07 | 12346-vertex_hubs-14 |
| peter | Pindegree | 0 | peter-Pindegree-15 |
| peter | Poutdegree | 2 | peter-Poutdegree-16 |
| peter | Ppagerank | 0.10471144347252878 | peter-Ppagerank-17 |
| peter | vertex_auth | 0.9999999999995453 | peter-vertex_auth-18 |
| peter | vertex_hubs | 0.0 | peter-vertex_hubs-19 |
| 12040 | Pindegree | 2 | 12040-Pindegree-20 |
| 12040 | Poutdegree | 0 | 12040-Poutdegree-21 |
| 12040 | Ppagerank | 0.1937160806623351 | 12040-Ppagerank-22 |
| 12040 | vertex_auth | 0.0 | 12040-vertex_auth-23 |
| 12040 | vertex_hubs | 0.9999999999990905 | 12040-vertex_hubs-24 |
| steve | Pindegree | 0 | steve-Pindegree-25 |
| steve | Poutdegree | 1 | steve-Poutdegree-26 |
| steve | Ppagerank | 0.10471144347252878 | steve-Ppagerank-27 |
| steve | vertex_auth | 9.094947017725146e-13 | steve-vertex_auth-28 |
| steve | vertex_hubs | 0.0 | steve-vertex_hubs-29 |
| 45601 | Pindegree | 1 | 45601-Pindegree-30 |
| 45601 | Poutdegree | 0 | 45601-Poutdegree-31 |
| 45601 | Ppagerank | 0.19371608066233506 | 45601-Ppagerank-32 |
| 45601 | vertex_auth | 0.0 | 45601-vertex_auth-33 |
| 45601 | vertex_hubs | 9.094947017721011e-13 | 45601-vertex_hubs-34 |

Here is what's written to the log file, `summary.txt`:

```
cat summary.txt
```

~~~
graph loaded! It has 7 nodes and 5 edges

###Top relations:
zipcode	5

###Degrees:
in degree stats: mean=0.714286, std=0.264520, max=1
out degree stats: mean=0.714286, std=0.332847, max=1
total degree stats: mean=1.428571, std=0.187044, max=1

###PageRank
Max pageranks
4	12040	0.193716
6	45601	0.193716
1	12345	0.149214
2	12346	0.149214
5	steve	0.104711

###HITS
HITS hubs
4	12040	1.000000
1	12345	0.000001
2	12346	0.000001
6	45601	0.000000
5	steve	0.000000
HITS auth
3	peter	1.000000
0	john	0.000001
5	steve	0.000000
4	12040	0.000000
6	45601	0.000000
~~~

### Example: Suppress Pageranks

Supress the computation, logging, and output of pageranks.

```
kgtk graph_statistics \
     -i examples/docs/graph-statistics-file1.tsv \
     --log-file summary.txt \
     --output-statistics-only \
     --compute-pagerank False
```

The output is as follows:

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| john | vertex_in_degree | 0 | john-vertex_in_degree-0 |
| john | vertex_out_degree | 2 | john-vertex_out_degree-1 |
| john | vertex_auth | 9.536743164058163e-07 | john-vertex_auth-2 |
| john | vertex_hubs | 0.0 | john-vertex_hubs-3 |
| 12345 | vertex_in_degree | 1 | 12345-vertex_in_degree-4 |
| 12345 | vertex_out_degree | 0 | 12345-vertex_out_degree-5 |
| 12345 | vertex_auth | 0.0 | 12345-vertex_auth-6 |
| 12345 | vertex_hubs | 9.536743164053826e-07 | 12345-vertex_hubs-7 |
| 12346 | vertex_in_degree | 1 | 12346-vertex_in_degree-8 |
| 12346 | vertex_out_degree | 0 | 12346-vertex_out_degree-9 |
| 12346 | vertex_auth | 0.0 | 12346-vertex_auth-10 |
| 12346 | vertex_hubs | 9.536743164053826e-07 | 12346-vertex_hubs-11 |
| peter | vertex_in_degree | 0 | peter-vertex_in_degree-12 |
| peter | vertex_out_degree | 2 | peter-vertex_out_degree-13 |
| peter | vertex_auth | 0.9999999999995453 | peter-vertex_auth-14 |
| peter | vertex_hubs | 0.0 | peter-vertex_hubs-15 |
| 12040 | vertex_in_degree | 2 | 12040-vertex_in_degree-16 |
| 12040 | vertex_out_degree | 0 | 12040-vertex_out_degree-17 |
| 12040 | vertex_auth | 0.0 | 12040-vertex_auth-18 |
| 12040 | vertex_hubs | 0.9999999999990905 | 12040-vertex_hubs-19 |
| steve | vertex_in_degree | 0 | steve-vertex_in_degree-20 |
| steve | vertex_out_degree | 1 | steve-vertex_out_degree-21 |
| steve | vertex_auth | 9.094947017725146e-13 | steve-vertex_auth-22 |
| steve | vertex_hubs | 0.0 | steve-vertex_hubs-23 |
| 45601 | vertex_in_degree | 1 | 45601-vertex_in_degree-24 |
| 45601 | vertex_out_degree | 0 | 45601-vertex_out_degree-25 |
| 45601 | vertex_auth | 0.0 | 45601-vertex_auth-26 |
| 45601 | vertex_hubs | 9.094947017721011e-13 | 45601-vertex_hubs-27 |

Here is what's written to the log file, `summary.txt`:

```
cat summary.txt
```

~~~
graph loaded! It has 7 nodes and 5 edges

###Top relations:
zipcode	5

###Degrees:
in degree stats: mean=0.714286, std=0.264520, max=1
out degree stats: mean=0.714286, std=0.332847, max=1
total degree stats: mean=1.428571, std=0.187044, max=1

###HITS
HITS hubs
4	12040	1.000000
1	12345	0.000001
2	12346	0.000001
6	45601	0.000000
5	steve	0.000000
HITS auth
3	peter	1.000000
0	john	0.000001
5	steve	0.000000
4	12040	0.000000
6	45601	0.000000
~~~

### Example: Suppress HITS

Supress the computation, logging, and output of HITS.

```
kgtk graph_statistics \
     -i examples/docs/graph-statistics-file1.tsv \
     --log-file summary.txt \
     --output-statistics-only \
     --compute-hits False
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

Here is what's written to the log file, `summary.txt`:

```
cat summary.txt
```

~~~
graph loaded! It has 7 nodes and 5 edges

###Top relations:
zipcode	5

###Degrees:
in degree stats: mean=0.714286, std=0.264520, max=1
out degree stats: mean=0.714286, std=0.332847, max=1
total degree stats: mean=1.428571, std=0.187044, max=1

###PageRank
Max pageranks
4	12040	0.193716
6	45601	0.193716
1	12345	0.149214
2	12346	0.149214
5	steve	0.104711
~~~

!!! Note
    HITS will not be computed if the graph is undirected (`--undirected True`).

### Example: Suppress In-degrees and Out-degrees Edges

Suppress the computation and output of in-degrees and out-degrees edges.

```
kgtk graph_statistics \
     -i examples/docs/graph-statistics-file1.tsv \
     --log-file summary.txt \
     --output-statistics-only \
     --output-degrees False
```

The output (printed to stdout by default) is as follows:

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| john | vertex_pagerank | 0.10471144347252878 | john-vertex_pagerank-0 |
| john | vertex_auth | 9.536743164058163e-07 | john-vertex_auth-1 |
| john | vertex_hubs | 0.0 | john-vertex_hubs-2 |
| 12345 | vertex_pagerank | 0.14921376206743192 | 12345-vertex_pagerank-3 |
| 12345 | vertex_auth | 0.0 | 12345-vertex_auth-4 |
| 12345 | vertex_hubs | 9.536743164053826e-07 | 12345-vertex_hubs-5 |
| 12346 | vertex_pagerank | 0.14921376206743192 | 12346-vertex_pagerank-6 |
| 12346 | vertex_auth | 0.0 | 12346-vertex_auth-7 |
| 12346 | vertex_hubs | 9.536743164053826e-07 | 12346-vertex_hubs-8 |
| peter | vertex_pagerank | 0.10471144347252878 | peter-vertex_pagerank-9 |
| peter | vertex_auth | 0.9999999999995453 | peter-vertex_auth-10 |
| peter | vertex_hubs | 0.0 | peter-vertex_hubs-11 |
| 12040 | vertex_pagerank | 0.1937160806623351 | 12040-vertex_pagerank-12 |
| 12040 | vertex_auth | 0.0 | 12040-vertex_auth-13 |
| 12040 | vertex_hubs | 0.9999999999990905 | 12040-vertex_hubs-14 |
| steve | vertex_pagerank | 0.10471144347252878 | steve-vertex_pagerank-15 |
| steve | vertex_auth | 9.094947017725146e-13 | steve-vertex_auth-16 |
| steve | vertex_hubs | 0.0 | steve-vertex_hubs-17 |
| 45601 | vertex_pagerank | 0.19371608066233506 | 45601-vertex_pagerank-18 |
| 45601 | vertex_auth | 0.0 | 45601-vertex_auth-19 |
| 45601 | vertex_hubs | 9.094947017721011e-13 | 45601-vertex_hubs-20 |

Here is what's written to the log file, `summary.txt`:

```
cat summary.txt
```

~~~
graph loaded! It has 7 nodes and 5 edges

###Top relations:
zipcode	5

###Degrees:
in degree stats: mean=0.714286, std=0.264520, max=1
out degree stats: mean=0.714286, std=0.332847, max=1
total degree stats: mean=1.428571, std=0.187044, max=1

###PageRank
Max pageranks
4	12040	0.193716
6	45601	0.193716
1	12345	0.149214
2	12346	0.149214
5	steve	0.104711

###HITS
HITS hubs
4	12040	1.000000
1	12345	0.000001
2	12346	0.000001
6	45601	0.000000
5	steve	0.000000
HITS auth
3	peter	1.000000
0	john	0.000001
5	steve	0.000000
4	12040	0.000000
6	45601	0.000000
~~~

### Example: Compute Pageranks and HITS, but Suppress Pagerank and HITS Edges

Compute pageranks and HITS, but suppress generating output edges for
them.

```
kgtk graph_statistics \
     -i examples/docs/graph-statistics-file1.tsv \
     --log-file summary.txt \
     --output-statistics-only \
     --output-pagerank False \
     --output-hits False
```

The output (printed to stdout by default) is as follows:

| node1 | label | node2 | id |
| -- | -- | -- | -- |
| john | vertex_in_degree | 0 | john-vertex_in_degree-0 |
| john | vertex_out_degree | 2 | john-vertex_out_degree-1 |
| 12345 | vertex_in_degree | 1 | 12345-vertex_in_degree-2 |
| 12345 | vertex_out_degree | 0 | 12345-vertex_out_degree-3 |
| 12346 | vertex_in_degree | 1 | 12346-vertex_in_degree-4 |
| 12346 | vertex_out_degree | 0 | 12346-vertex_out_degree-5 |
| peter | vertex_in_degree | 0 | peter-vertex_in_degree-6 |
| peter | vertex_out_degree | 2 | peter-vertex_out_degree-7 |
| 12040 | vertex_in_degree | 2 | 12040-vertex_in_degree-8 |
| 12040 | vertex_out_degree | 0 | 12040-vertex_out_degree-9 |
| steve | vertex_in_degree | 0 | steve-vertex_in_degree-10 |
| steve | vertex_out_degree | 1 | steve-vertex_out_degree-11 |
| 45601 | vertex_in_degree | 1 | 45601-vertex_in_degree-12 |
| 45601 | vertex_out_degree | 0 | 45601-vertex_out_degree-13 |

Here is what's written to the log file, `summary.txt`:

```
cat summary.txt
```

~~~
graph loaded! It has 7 nodes and 5 edges

###Top relations:
zipcode	5

###Degrees:
in degree stats: mean=0.714286, std=0.264520, max=1
out degree stats: mean=0.714286, std=0.332847, max=1
total degree stats: mean=1.428571, std=0.187044, max=1

###PageRank
Max pageranks
4	12040	0.193716
6	45601	0.193716
1	12345	0.149214
2	12346	0.149214
5	steve	0.104711

###HITS
HITS hubs
4	12040	1.000000
1	12345	0.000001
2	12346	0.000001
6	45601	0.000000
5	steve	0.000000
HITS auth
3	peter	1.000000
0	john	0.000001
5	steve	0.000000
4	12040	0.000000
6	45601	0.000000
~~~

!!! Note
    At this time, it is not possible to suppress the genration of
    just pageranks or just HITS edges.

### Example: `--undirected true` vs. `--undirected false`

`kgtk graph-statistics` defaults to `--undirected false`.  This treats
the KGTK edges as directed edges from node1 to node2: (`node1`->`node2`).

Conversely, when `--undirected true` has been specified, the KGTK edges
are treated as undirected (bidirectional): (`node1`<->`node2`).

Directed edges count (`node1->`node2`) as an `out-edge` for `node1` and an
`in-edge` for `node2`.  Undirected (bidirectional) edges count it as an
`out-edge` for both `node1` and `node2`; there are no `in-edge` counts for
undirected edges.

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
    --undirected False \
    --page-rank-property Ppagerank \
    --vertex-in-degree-property Pindegree \
    --vertex-out-degree-property Poutdegree \
    --output-statistics-only True \
    / filter -p 'Q5;;'
```
| node1 | label | node2 | id |
| -- | -- | -- | -- |
| Q5 | Pindegree | 20 | Q5-Pindegree-0 |
| Q5 | Poutdegree | 5 | Q5-Poutdegree-1 |
| Q5 | Ppagerank | 0.30874598028371614 | Q5-Ppagerank-2 |
| Q5 | vertex_auth | 1.3328003749250113e-08 | Q5-vertex_auth-3 |
| Q5 | vertex_hubs | 0.9999999999999911 | Q5-vertex_hubs-4 |

Here is what's written to the log file, `summary.txt`:

```
cat summary.txt
```

~~~
graph loaded! It has 26 nodes and 25 edges

###Top relations:
P31	19
P1343	4
P1056	1
P279	1

###Degrees:
in degree stats: mean=0.961538, std=0.750701, max=1
out degree stats: mean=0.961538, std=0.176091, max=1
total degree stats: mean=1.923077, std=0.905151, max=1

###PageRank
Max pageranks
0	Q5	0.308746
2	Q19180675	0.069639
1	Q3619132	0.069639
4	Q4086271	0.069639
5	Q4173137	0.069639

###HITS
HITS hubs
0	Q5	1.000000
2	Q19180675	0.000000
1	Q3619132	0.000000
4	Q4086271	0.000000
5	Q4173137	0.000000
HITS auth
9	Q100153947	0.223607
11	Q100252	0.223607
14	Q100558585	0.223607
13	Q100533268	0.223607
25	Q101410	0.223607
~~~

Now, let's compute statistics on this file treating the
edges as undirected (bidirectional):

```bash
kgtk graph-statistics \
    -i examples/docs/graph-statistics-file2.tsv \
    --undirected True \
    --page-rank-property Ppagerank \
    --vertex-in-degree-property Pindegree \
    --vertex-out-degree-property Poutdegree \
    --output-statistics-only True \
    / filter -p 'Q5;;'
```
| node1 | label | node2 | id |
| -- | -- | -- | -- |
| Q5 | Pindegree | 0 | Q5-Pindegree-0 |
| Q5 | Poutdegree | 25 | Q5-Poutdegree-1 |
| Q5 | Ppagerank | 0.4625751944545934 | Q5-Ppagerank-2 |

Here is what's written to the log file, `summary.txt`:

```
cat summary.txt
```

~~~
graph loaded! It has 26 nodes and 25 edges

###Top relations:
P31	19
P1343	4
P1056	1
P279	1

###Degrees:
in degree stats: mean=0.000000, std=0.000000, max=1
out degree stats: mean=1.923077, std=0.905151, max=1
total degree stats: mean=1.923077, std=0.905151, max=1

###PageRank
Max pageranks
0	Q5	0.462575
10	Q100153956	0.021497
9	Q100153947	0.021497
11	Q100252	0.021497
8	Q100148353	0.021497
~~~
