This command will sort any KGTK file on one or more columns. If more than one column is given, columns are compared in the order listed (not in the order they appear in the file).  Data is sorted in ascending order by default, but can also be sorted in reverse.  The command expects a KGTK file with a header line which will be included in the sorted output.

## Usage
```
usage: kgtk sort [-h] [-i INPUT] [-o OUTPUT_FILE] [-c COLUMNS] [-r] [--tsv] [--csv]
                 [--naptime NAPTIME] [--space] [--speed] [-X EXTRA] [-dt _DT]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input-file INPUT
                        Input file to sort. (May be omitted or '-' for stdin.)
  -o OUTPUT_FILE, --out OUTPUT_FILE
                        Output file to write to. (May be omitted or '-' for stdout.)
  -c COLUMNS, --column COLUMNS, --columns COLUMNS
                        comma-separated list of column names or numbers (1-based) to sort
                        on, defaults to 1
  -r, --reverse         generate output in reverse sort order
  --tsv                 assume tab-separated input (default)
  --csv                 assume comma-separated input (for non-KGTK files)
  --naptime NAPTIME     Seconds to nap before starting
  --space               space-optimized configuration for sorting large files
  --speed               speed-optimized configuration for sorting large files
  -X EXTRA, --extra EXTRA
                        extra options to supply to the sort program
  -dt _DT, --datatype _DT
                        Deprecated: datatype of the input file, e.g., tsv (default) or csv.
```

Input files can be piped in from stdin or named explicitly.  They can also be optionally compressed and will transparently be decompressed by zconcat.  Columns can be specified by the names used in the file header line, as 1-based positions, or through the pre-defined positions of reserved names such as `subject', etc.  Column names found in the header will override any predefined positions.

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

Sort a large file with speed optimizations on:
```
cat nodes.tsv.gz | kgtk sort -c 'id, label' --speed -X ' -T /tmp' -o nodes-sorted.tsv
```
