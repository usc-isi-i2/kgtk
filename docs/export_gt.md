This command loads a TSV edges file into Graph-tool, and exports it to Graph-tool (.gt) format. 

## Usage
```
kgtk export_gt [-h] [--directed]
                [--log LOG_FILE]  [-o OUTPUT] 
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
  -o OUTPUT, --out OUTPUT
						Graph tool file to dump the graph too - if empty, it
                        will not be saved.
  --log LOG_FILE        Log file for summarized statistics of the graph.
```

## Examples

Import a TSV file into Graph-tool, and store the result to disk. We store the statistics to log.txt. 

```
kgtk graph_statistics --directed --log log.txt --out graph.gt ./data/conceptnet_first10.tsv
```
