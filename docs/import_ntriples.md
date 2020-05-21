This command will import an ntriple file into KGTK format

## Usage
```
kgtk import_ntriples OPTIONS
```
**OPTIONS**:

`-i {string}`: The ntriple file that needs to be imported

`-o {string}`: Path to the output KGTK file

`--limit`: The number of lines of the ntriple file to import. Defualt: imports whole file.

### Examples

Import the entire given ntriple file into kgtk format

```
kgtk import_ntriples -i dbpedia_wikipedia_links.ttl -o DbpediaWikipediaLinks.tsv
```
