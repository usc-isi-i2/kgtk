!!! warning
    This command is under testing

Given a nodes and an edges file (!) in TSV format, collapse the nodes that are connected with a same-as relation. Reflect these changes both in the nodes and in the edges file. Remove the same-as relations from the edge file.

After the merge, the identical rows are deduplicated.

## Usage
```
kgtk merge_identical_nodes -ef EDGEFILE -nf NODEFILE [-l SAMEASLBL]
EDGEFILE is an edge file in TSV format
NODEFILE is a node file in TSV format
SAMEASLBL is a same-as relation that is used to indicate identity 
```

## Examples
Merge nodes connected with a ‘mw:SameAs’ relation
```
kgtk merge_identical_nodes -ef data/edges.tsv -nf data/nodes.tsv -l “mw:SameAs”
```

