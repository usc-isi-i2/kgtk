This command loads a TSV edges file into Graph-tool, and exports it to Graph-tool (.gt) format. 

## Usage
```
usage: kgtk export-gt [-h] [-i INPUT_FILE] [-o OUTPUT_FILE] [--directed] [--log LOG_FILE]
                      [INPUT_FILE]

positional arguments:
  INPUT_FILE            The KGTK input file. (May be omitted or '-' for stdin.) (Deprecated,
                        use -i INPUT_FILE)

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK input file. (May be omitted or '-' for stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        Graph tool file to dump the graph too - if empty, it will not be
                        saved. (Optional, use '-' for stdout.)
  --directed            Is the graph directed or not?
  --log LOG_FILE        Log file for summarized statistics of the graph.
```

## Examples

Import a TSV file into Graph-tool, and store the result to disk. We store the statistics to log.txt. 

```
kgtk export-gt --directed --log log.txt --out graph.gt ./data/conceptnet_first10.tsv
```
