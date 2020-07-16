Given a KGTK edge file, and an auxiliary file with source-target node pairs, this command computes paths between each pair of source-target nodes.

All paths up to a certain length threshold are returned.

The output, printed to stdout, is an edge file with the following columns: path identifier (as node1), edge number (as label), edge identifier (as node2), and id. Optionally, the original graph can be printed to stdout too.

## Usage
```
usage: kgtk paths [-h] [-i INPUT_FILE] [--path_file PATH_FILE]
                  [--statistics-only] [--directed] [--max_hops MAX_HOPS]
                  [INPUT_FILE]

positional arguments:
  INPUT_FILE            The KGTK input file. (May be omitted or '-' for
                        stdin.) (Deprecated, use -i INPUT_FILE)

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK input file. (May be omitted or '-' for
                        stdin.)
  --path_file PATH_FILE
                        KGTK file with path start and end nodes. (May be
                        omitted or '-' for stdin.)
  --statistics-only     If this flag is set, output only the statistics edges.
                        Else, append the statistics to the original graph.
  --directed            Is the graph directed or not?
  --max_hops MAX_HOPS   Maximum number of hops allowed.
```

## Examples

Given the file `examples/sample_data/paths/test.tsv`:

| node1 | label | node2 | id | col |
| -- | -- | -- | -- | -- |
| a | r1 | c | e1 | 1 |
| a | r1 | d | e2 | 2 |
| a | r2 | c | e3 | 3 |
| d | r3 | e | e4 | 4 |
| c | r4 | e | e5 | 1 |
| d | r3 | f | e6 | 2 |
| f | r3 | d | e7 | 3 |

Let's say we want to compute all paths between a set of pairs stored in `examples/sample_data/paths/pairs.tsv`. The file for now has the following data:
| source | target |
| ------ | ------ |
|   a    |   e    |

which means that we are looking for all paths between the nodes 'a' and 'e'. Let's say we restrict the maximum path length to 2. 

We can compute our paths with the following command:

```
kgtk paths --directed --max_hops 2 --path_file examples/sample_data/paths/pairs.tsv -i examples/sample_data/paths/test.tsv --statistics-only
```

The output (printed to stdout) is as follows:

| node1 | label | node2 | id |
| -- | -- | -- | -- | 
| p0 |  0 |	e1 | p0-0-0 |
| p0 |	1 |	e5 | p0-1-1 |
| p1 |	0 |	e2 | p1-0-2 |
| p1 |	1 |	e4 | p1-1-3 |
| p2 |	0 |	e3 | p2-0-4 |
| p2 |	1 |	e5 | p2-1-5 |

Essentially, this tells us that there are three paths that connect 'a' and 'e', all of them two hops away:

1. path 0 is comprised of the edges e1 and e5
2. path 2 one spans e2 and e4
3. path 3 spans e3 and e5

