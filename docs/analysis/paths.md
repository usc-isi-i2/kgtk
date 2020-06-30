Given a KGTK edge file, and a set of source and target nodes, this command computes paths between each pair of source and target nodes.

All paths up to a certain length threshold are returned.

The output, printed to stdout, is the input edge file with its primary columns, enriched with a path identifier where applicable.

## Usage
```
kgtk paths [-h] [--i FILENAME] [--directed] [--max_hops MAX_HOPS]
                  [--source_nodes [SOURCE_NODES [SOURCE_NODES ...]]]
                  [--target_nodes [TARGET_NODES [TARGET_NODES ...]]]
                  [--graph_edge GRAPH_EDGE]
```

optional arguments:
  -h, --help            show this help message and exit
  --i FILENAME          Input filename
  --directed            Is the graph directed or not?
  --max_hops MAX_HOPS   Maximum number of hops allowed.
  --source_nodes [SOURCE_NODES [SOURCE_NODES ...]]
                        List of source nodes
  --target_nodes [TARGET_NODES [TARGET_NODES ...]]
                        List of target nodes
  --graph_edge GRAPH_EDGE
                        Name of the secondary edge type that stores the path
                        id, default is 'graph'.

## Examples

Given this file `examples/sample_data/paths/test.tsv`:

| node1 | label | node2 | id | col |
| -- | -- | -- | -- | -- |
| a | r1 | c | e1 | 1 |
| a | r1 | d | e2 | 2 |
| a | r2 | c | e3 | 3 |
| d | r3 | e | e4 | 4 |
| c | r4 | e | e5 | 1 |
| d | r3 | f | e6 | 2 |
| f | r3 | d | e7 | 3 |

Let's say we want to compute all paths between the nodes 'a' and 'e' of length up to 2. We can do so with the following command:

```
kgtk paths --directed --max_hops 2 --source_nodes a --target_nodes e --i examples/sample_data/paths/test.tsv
```

The output (printed to stdout) is as follows:

| node1 | label | node2 | id | graph |
| -- | -- | -- | -- | -- |
| a | r1 | c | e1 | 1 |
| a | r1 | d | e2 | 2 |
| a | r2 | c | e3 | 3 |
| c | r4 | e | e5 | 1\|3 |
| d | r3 | e | e4 | 2 |
| d | r3 | f | e6 |  |
| f | r3 | d | e7 |  |

Essentially, this tells us that there are three paths that connect 'a' and 'e', all of them two hops away:

1. graph 1 is comprised of the edges e1 and e5
2. graph 2 one spans e2 and e4
3. graph 3 spans e3 and e5

Note that this command expects an edge file with an `id` column.

