This command will sort any KGTK file on one or more columns. If more than one column is given, columns are compared in the order listed (not in the order they appear in the file).  Data is sorted in ascending order by default, but can also be sorted in reverse.  The command expects a KGTK file with a header line which will be included in the sorted output.

## Usage
```
usage: kgtk sort [-h] [-i INPUT] [-o OUTPUT_FILE] [-c [COLUMNS [COLUMNS ...]]] [--locale LOCALE] [-r [True|False]] [--pure-python [True|False]] [-X EXTRA]
                 [-v [optional True|False]]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input-file INPUT
                        Input file to sort. (May be omitted or '-' for stdin.)
  -o OUTPUT_FILE, --out OUTPUT_FILE, --output-file OUTPUT_FILE
                        Output file to write to. (May be omitted or '-' for stdout.)
  -c [COLUMNS [COLUMNS ...]], --column [COLUMNS [COLUMNS ...]], --columns [COLUMNS [COLUMNS ...]]
                        comma-separated list of column names to sort on. (defaults to id for node files, (node1, label, node2) for edge files without ID, (id,
                        node1, label, node2) for edge files with ID)
  --locale LOCALE       LC_ALL locale controls the sorting order. (default=C)
  -r [True|False], --reverse [True|False]
                        When True, generate output in reverse sort order. (default=False)
  --pure-python [True|False]
                        When True, sort in-memory with Python code. (default=False)
  -X EXTRA, --extra EXTRA
                        extra options to supply to the sort program. (default=None)

  -v [optional True|False], --verbose [optional True|False]
                        Print additional progress messages (default=False).
```

Input files can be piped in from stdin or named explicitly.  They can also be optionally compressed and will transparently be decompressed.  Columns can be specified by the names used in the file header line, as 1-based positions, or through the pre-defined positions of reserved names such as `subject', etc.  Column names found in the header will override any predefined positions.

## Examples
Sort the conceptnet CSKG file based on label and node2
```
kgtk sort -c label,node2 -i data/conceptnet_first10.tsv
```

Sort a file piped from another command based on label and node2 
```
gzcat wikidata_edges.tsv.gz | kgtk sort -c label,node2
```

Sort a compressed file to a named output file:
```
kgtk sort -c 'label, id' -o nodes-sort.tsv -i nodes-shuf.tsv.gz
```

Sort a compressed file from stdin to stdout:
```
cat nodes-shuf.tsv.gz | kgtk sort -c 'label, id' | head -5
id    label    type    descriptions    aliases    document_id
Q28415        item    'railway station'@en        wikidata-20200203
Q45582        item    'Polish literary award'@en        wikidata-20200203
Q45877        item    'television series'@en        wikidata-20200203
Q45886        item            wikidata-20200203
```
