This command will import Wikidata into KGTK format and generates 3 files.

- A nodes file containing all Qnodes and Pnodes in Wikidata
- An edges file containing all the statements in Wikidata
- A qualifiers file containing all qualifiers on statements in Wikidata

## Usage
```
usage: kgtk import-wikidata [-h] [-i INPUT_FILE] [--procs PROCS] [--node NODE_FILE]
                            [--edge EDGE_FILE] [--qual QUAL_FILE] [--limit LIMIT]
                            [--lang LANG] [--source SOURCE] [--deprecated]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        input path file (May be omitted or '-' for stdin.)
  --procs PROCS         number of processes to run in parallel, default 2
  --node NODE_FILE      path to output node file
  --edge EDGE_FILE      path to output edge file
  --qual QUAL_FILE      path to output qualifier file
  --limit LIMIT         number of lines of input file to run on, default runs on all
  --lang LANG           languages to extract, comma separated, default en
  --source SOURCE       wikidata version number, default: wikidata
  --deprecated          option to include deprecated statements, not included by default
```

### Examples

Import the entire wikidata dump into kgtk format, extracting english labels, descriptions and aliases.

```
kgtk import-wikidata -i wikidata-all-20200504.json.bz2 --node nodefile.tsv --edge edgefile.tsv --qual qualfile.tsv 
```
