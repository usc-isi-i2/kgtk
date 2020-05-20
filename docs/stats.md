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
  --log LOG_FILE        Log file for summarized statistics of the graph.
```

## Examples

Import a TSV file into Graph-tool, and compute degrees, pagerank and hits. We store the statistics to log.txt. 

```
kgtk graph_statistics --directed --degrees --pagerank --hits --log log.txt ./data/conceptnet_first10.tsv
```
