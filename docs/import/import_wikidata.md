This command will import Wikidata into KGTK format and generates 3 files.

- A nodes file containing all Qnodes and Pnodes in Wikidata
- An edges file containing all the statements in Wikidata
- A qualifiers file containing all qualifiers on statements in Wikidata

## Usage
```
kgtk import-wikidata OPTIONS
```
**OPTIONS**: 

`-i {string}`: The wikidata dump file in bz2 format

`--procs {integer}`: The number of processes to run in parallel. Defualt: 2.

`--node {string}`: The path to the output node file. If not given, nodes will not be written out.

`--edge {string}`: The path to the output edge file. If not given, edges will not be written out.

`--qual {string}`: The path to the output qualifiers file. If not given, qualifiers will not be written out.

`--limit {integer}`: The number of lines of the wikidata dump to import. Defualt: imports whole dump.

`--lang {l1, l2, ...}`: The languages to extract from the wikidata dump, for labels, aliases and descriptions. Default: en

`--deprecated`: Default is not to include deprecated statements. Use this option to include them.

### Examples

Import the entire wikidata dump into kgtk format, extracting english labels, descriptions and aliases.

```
kgtk import-wikidata -i wikidata-all-20200504.json.bz2 --node nodefile.tsv --edge edgefile.tsv --qual qualfile.tsv 
```
