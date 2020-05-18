Given a set of nodes N and a set of properties P, this command computes the set of nodes R that can be reached from N via paths containing any of the properties in P.

The output is an edge file with three columns:
- subject: a node in the input set N
- property: reachable, or whatever property is provided as the closure property
- object: a node reachable from N via the input properties

## Usage:
```
kgtk reachable_nodes OPTIONS
Options:
--root {n1, n2, …}: the starting nodes
--property {p1, p2, …}: properties to traverse to compute closure. A property preceded with a minus sign (e.g., -p1) must be followed in the reverse direction.
--output-property {p}: the name of the property to represent the closure, default reachable.
--output-object: when supplied, the output will contain only the distinct values in the third column (object).
```

## Examples

All nodes reachable vi p1 and p2 starting from n1, n2, n3
```
kgtk reachable_nodes --property p1,p2 --root n1,n2,n3
```

Closure of the subclass property starting from every node in roots.tsv
```
kgtk reachable_nodes --property kgtk:subclass-of <(cat roots.tsv)
```

