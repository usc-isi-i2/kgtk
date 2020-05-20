Import the entire ConceptNet, or just its English part, into KGTK format. 

## Usage
```
kgtk import_conceptnet [-h] [--english_only] [--sort] filename
```

positional arguments:
```
  filename        filename here
```

optional arguments:
```
  -h, --help      show this help message and exit
  --english_only  Only english conceptnet?
  --sort          Should we sort the file on s-p-o?
```

## Examples

Import the English part of ConceptNet into KGTK, without sorting it. 

```
kgtk import_conceptnet --english_only examples/conceptnet-assertions-5.7.0.csv
```
