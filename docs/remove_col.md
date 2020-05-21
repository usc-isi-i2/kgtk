Command to remove a subset of the columns from a TSV file. For instance, remove “id” and “docid” from a Wikidata edges file.

## Usage
```
kgtk remove_columns -c COLUMNS INPUT
INPUT can be a filename or empty if piped from another command
```
## Examples
Remove the columns ‘other’ and ‘pos’ from the conceptnet CSKG file
```
kgtk remove_columns -c "other, pos" data/conceptnet_first10.tsv
```

Remove id and docid from Wikidata edges file
```
kgtk remove_columns -c “id, docid” data/wikidata_edges.tsv
```

Remove id and docid from Wikidata edges file piped from another command

```
gzcat wikidata_edges.tsv.gz | kgtk remove_columns -c “id, docid”
```

