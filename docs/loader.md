This command loads a TSV edges file into Graph-tool. Optionally, compute centrality metrics, and, optionally, dump the resulting graph-tool (.gt) object to disk. Prints the resulting edge file to stdout.

## Usage
```
kgtk gt_loader [-h] [--directed] [--degrees] [--pagerank] [--hits]
                      [--log LOG_FILE] [-o OUTPUT]
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
  -o OUTPUT, --out OUTPUT
                        Graph tool file to dump the graph too - if empty, it
                        will not be saved.
```

## Examples

Import a TSV file into Graph-tool, and compute degrees, pagerank and hits. We store the result to disk, and the statistics to log.txt. 

```
kgtk gt_loader --directed --degrees --pagerank --hits --out file.gt --log log.txt ./data/conceptnet_first10.tsv
```
