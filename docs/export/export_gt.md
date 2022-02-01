This command loads a TSV edges file into Graph-tool, and exports it to Graph-tool (.gt) format. 

## Usage
```
usage: kgtk export-gt [-h] [-i INPUT_FILE] [-o OUTPUT_FILE]
                      [--undirected [True|False]] [--node-file NODE_FILE]
                      [-v [optional True|False]]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK input file. (May be omitted or '-' for
                        stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        Graph tool file to dump the graph too - if empty, it
                        will not be saved. (Optional, use '-' for stdout.)
  --undirected [True|False]
                        When True, the graph is undirected. (default=False)
  --node-file NODE_FILE
                        Specify the location of node file.

  -v [optional True|False], --verbose [optional True|False]
                        Print additional progress messages (default=False).
```

## Examples

Import a TSV file into Graph-tool, and store the result to disk. We store the statistics to log.txt. 

```
kgtk export-gt -i tests/data/sample_kgtk_edge_file.tsv --out graph.gt --verbose
```

The file is exported to the file `graph.gt`.

The following progress messages should appear:

    loading the KGTK input file...
    
    input format: kgtk
    KgtkReader: OK to use the fast read path.
    KgtkReader: File_path.suffix: .tsv
    KgtkReader: reading file tests/data/sample_kgtk_edge_file.tsv
    header: id	node1	label	node2	rank
    node1 column found, this is a KGTK edge file
    KgtkReader: is_edge_file=True is_node_file=False
    KgtkReader: Special columns: node1=1 label=2 node2=3 id=0
    KgtkReader: Reading a kgtk file using the fast path.
    eprop_types is None
    Adding edges from the input file.
    Done adding edges from the input file.
    eprop_names: ['id', 'label', 'rank']
    prop 0 name='id'
    prop 1 name='label'
    prop 2 name='rank'
    graph loaded! It has 287 nodes and 287 edges.
    
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
    
    Now saving the graph to graph.gt
    Done saving the graph.
