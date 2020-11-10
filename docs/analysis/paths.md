Given a KGTK edge file, and an auxiliary file with source-target node pairs, this command computes paths between each pair of source-target nodes.

The source-target pair file is expected to be a KGTK file with node1 as the
source column and node2 as the target column.  The source and target columns
can be specified with command options --path-source <source> and --path-target
<target>; --path-mode NONE is needed to disable checks for required columns.

All paths up to a certain length threshold are returned.

The output, printed to stdout by default, is an edge file with the following columns: path identifier (as node1), edge number (as label), edge identifier (as node2), and id. Optionally, the original graph can be printed to stdout too.

## Usage
```
usage: kgtk paths [-h] [-i INPUT_FILE] [-o OUTPUT_FILE] [--path-file PATH_FILE] [--statistics-only [True|False]] [--undirected [True|False]] [--max_hops MAX_HOPS]
                  [--path-source SOURCE_COLUMN_NAME] [--path-target TARGET_COLUMN_NAME] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK input file. (May be omitted or '-' for stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for stdout.)
  --path-file PATH_FILE, --path_file PATH_FILE
                        KGTK file with path start and end nodes. (May be omitted or '-' for stdin.)
  --statistics-only [True|False]
                        If this flag is set, output only the statistics edges. Else, append the statistics to the original graph. (default=False)
  --undirected [True|False]
                        Is the graph undirected or not? (default=False)
  --max_hops MAX_HOPS   Maximum number of hops allowed.
  --path-source SOURCE_COLUMN_NAME
                        Name of the source column in the path file. (default: node1 or its alias)
  --path-target TARGET_COLUMN_NAME
                        Name of the source column in the path file. (default: node2 or its alias)

  -v, --verbose         Print additional progress messages (default=False).

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
| -- | -- |
| a | e |

which means that we are looking for all paths between the nodes 'a' and 'e'. Let's say we restrict the maximum path length to 2. 

We can compute our paths with the following command:

```
kgtk paths --max_hops 2 --path-file examples/sample_data/paths/pairs.tsv --path-mode NONE --path-source source --path-target target -i examples/sample_data/paths/test.tsv --statistics-only
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

1. path p0 is comprised of the edges e1 and e5
2. path p1 spans e2 and e4
3. path p2 spans e3 and e5

