Command to remove a subset of the columns from a TSV file. For instance, remove 'id' and 'docid' from a Wikidata edges file.

## Usage
```
usage: kgtk remove-columns [-h] [-i INPUT_FILE] [-o OUTPUT_FILE] -c COLUMNS [COLUMNS ...]
                           [--split-on-commas [SPLIT_ON_COMMAS]]
                           [--split-on-spaces [SPLIT_ON_SPACES]]
                           [--strip-spaces [STRIP_SPACES]] [-v]

Remove specific columns from a KGTK file.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        The KGTK input file. (May be omitted or '-' for stdin.)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The KGTK output file. (May be omitted or '-' for stdout.)
  -c COLUMNS [COLUMNS ...], --columns COLUMNS [COLUMNS ...]
                        Columns to remove as a comma- or space-separated strings, e.g.,
                        id,docid or id docid
  --split-on-commas [SPLIT_ON_COMMAS]
                        Parse the list of columns, splitting on commas. (default=True).
  --split-on-spaces [SPLIT_ON_SPACES]
                        Parse the list of columns, splitting on spaces. (default=False).
  --strip-spaces [STRIP_SPACES]
                        Parse the list of columns, stripping whitespace. (default=True).

  -v, --verbose         Print additional progress messages (default=False).

```
## Examples

Remove the columns 'other' and 'pos' from the conceptnet CSKG file
```
kgtk remove-columns -c "other, pos" -i data/conceptnet_first10.tsv
```

Remove id and docid from Wikidata edges file
```
kgtk remove-columns -c 'id, docid' -i data/wikidata_edges.tsv
```

Remove id and docid from Wikidata edges file piped from another command

```
gzcat wikidata_edges.tsv.gz | kgtk remove-columns -c 'id, docid'
```

