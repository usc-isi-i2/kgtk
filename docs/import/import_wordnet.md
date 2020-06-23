Import WordNet v3.0 into KGTK format. Currently, four relations are included: hypernymy, membership holonymy, part-of holonymy, and substance meronymy. The resulting KGTK file consists of 12 columns.

## Usage
```
kgtk import_wordnet [-h] 
```

positional arguments:
```
```

optional arguments:
```
  -h, --help      show this help message and exit
```

## Examples

Importing WordNet can be done as follows (no arguments should be provided, as WordNet is read through the NLTK package):

```
kgtk import_wordnet
```
