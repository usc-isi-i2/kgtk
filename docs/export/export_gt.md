This command loads a TSV edges file into Graph-tool, and exports it to Graph-tool (.gt) format. 

## Usage
```
usage: kgtk export-gt [-h] [-i INPUT_FILE] [-o OUTPUT_FILE] [--directed] [--log LOG_FILE]

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
kgtk export-gt -i data/sample_kgtk_edge_file.tsv --directed --log log.txt --out graph.gt 
```

The file `log.txt` has the following content:
```
loading the TSV graph now ...
graph loaded! It has 287 nodes and 287 edges

###Top relations:
wikipedia_sitelink	136
description	10
label	10
P31	10
P646	6
P279	5
P373	5
P18	3
P495	3
P156	3
now saving the graph to graph.gt
```

The file is exported to the file `graph.gt`.
