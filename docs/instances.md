Given a set of nodes C that represent classes, compute the set of all instances of every member in C.

## Usage:
```
kgtk instances OPTIONS
```
## Options:
```
--isa-file: the name of the isa file, if different from the default.
--classes: identifiers of classes, comma-separated. The set of classes can be provided in the standard input or chained from the previous command in the pipeline
```

## Examples

instances of the subclasses of two classes
```
kgtk instances --transitive --class Q13442814,Q12345678
```
