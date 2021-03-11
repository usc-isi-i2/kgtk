Query a KGTK file with the Kypher query language
(a variant of [Cypher](https://neo4j.com/developer/cypher/))
and return the results according to a return specification.  This
command is very flexible and can be used to perform a large number of
data access, aggregation, computation, analysis and transformation
operations.

Input files are assumed to be valid, multi-column KGTK files and can
be piped in from stdin or named explicitly.  Named input files can
also be optionally compressed.  Output goes to stdout or the specified
output file which will be transparently compressed according to its file extension.

!!! note
    <b>Important restriction:</b> Command pipes must contain **at most** one query command
    due to database locking considerations.  Future versions will relax this restriction.


## Usage
```
usage: kgtk query [-h] -i INPUT_FILE [INPUT_FILE ...] [--as NAME]
                  [--query QUERY] [--match PATTERN] [--where CLAUSE]
                  [--return CLAUSE] [--order-by CLAUSE] [--skip CLAUSE]
                  [--limit CLAUSE] [--para NAME=VAL] [--spara NAME=VAL]
                  [--lqpara NAME=VAL] [--no-header] [--index [MODE]]
                  [--explain [MODE]] [--graph-cache GRAPH_CACHE_FILE]
                  [-o OUTPUT]

Query one or more KGTK files with Kypher.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE [INPUT_FILE ...], --input-files INPUT_FILE [INPUT_FILE ...]
                        One or more input files to query (maybe compressed).
                        (Required, use '-' for stdin.)
  --as NAME             alias name to be used for preceding input
  --query QUERY         complete Kypher query combining all clauses, if
                        supplied, all other specialized clause arguments will
                        be ignored
  --match PATTERN       MATCH pattern of a Kypher query, defaults to universal
                        node pattern `()'
  --where CLAUSE        WHERE clause of a Kypher query
  --return CLAUSE       RETURN clause of a Kypher query (defaults to *)
  --order-by CLAUSE     ORDER BY clause of a Kypher query
  --skip CLAUSE         SKIP clause of a Kypher query
  --limit CLAUSE        LIMIT clause of a Kypher query
  --para NAME=VAL       zero or more named value parameters to be passed to
                        the query
  --spara NAME=VAL      zero or more named string parameters to be passed to
                        the query
  --lqpara NAME=VAL     zero or more named LQ-string parameters to be passed
                        to the query
  --no-header           do not generate a header row with column names
  --index [MODE]        control column index creation according to MODE (auto,
                        expert, quad, triple, node1+label, node1, label,
                        node2, none, default: auto)
  --explain [MODE]      explain the query execution and indexing plan
                        according to MODE (plan, full, expert, default: plan).
                        This will not actually run or create anything.
  --graph-cache GRAPH_CACHE_FILE
                        database cache where graphs will be imported before
                        they are queried (defaults to per-user temporary file)
  -o OUTPUT, --out OUTPUT
                        output file to write to, if `-' (the default) output
                        goes to stdout. Files with extensions .gz, .bz2 or .xz
                        will be appropriately compressed.
```

## "Kypher" - a Cypher-inspired query language for KGTK files

[Cypher](https://neo4j.com/developer/cypher/) is a declarative graph
query language originally developed at Neo4j Inc. (see also its
[Wikipedia](https://en.wikipedia.org/wiki/Cypher_(query_language))
entry).  [openCypher](https://www.opencypher.org/) is a corresponding
open-source development effort for Cypher which in turn forms the
basis of the new [Graph Query Language
(GCL)](https://www.gqlstandards.org/) developed by ISO.  Cypher uses a
special ASCII-art pattern language for graph patterns, but is
otherwise very similar to SQL.  We adopted Cypher, since its pattern
language seems to make it relatively easy even for novices to express
complex "join" queries over graph data.

Kypher stands for *KGTK Cypher*.  Kypher adopts Cypher's patterns
and many other aspects of its query language, but has some important
differences that warranted a different name.  Most notably, KGTK
and therefore Kypher does not use a property graph data model assumed
by Cypher.  Kypher only implements a subset of the Cypher commands
(for example, no update commands) and has some minor differences in
syntax, for example, to support naming and querying over multiple graphs.
Kypher also does not allow certain path-range patterns which would be
expensive to support.

To implement Kypher queries, we translate them into SQL and execute
them on a very lightweight file-based SQL database such as SQLite.
Kypher queries are designed to look and feel very similar to other
file-based KGTK commands.  They take tabular file data as input and
produce tabular data as output.  There are no servers and accounts to
set up, and the user does not need to know that there is in fact a
database used underneath to implement the queries.  A cache mechanism
makes multiple queries over the same KGTK files very efficient.
Kypher has been successfully tested on Wikidata-scale graphs with 1.5B
edges and larger where queries executing on a standard laptop run in
milliseconds to minutes depending on selectivity and result sizes.


### Features under development:

* optional match
* `not/exists` pattern handling
* support for chained queries
* `--create` and `--remove` to instantiate and add/remove edge patterns
  from result bindings
* `--with` clause to compute derived values to use by `--create` and `--remove`


## Overview

### Selecting edges with the `--match` clause

At its core the KGTK `query` command either takes a full Kypher
`--query` or individual Kypher clauses such as `--match`, `--return`,
`--limit`, etc. which will be automatically assembled into the proper
order.  Using individual clauses via command options is generally a
bit easier in a Unix shell environment.

Below we show a simple query on a single input graph with an anonymous
edge pattern.  For convenience, we first set up a shell variable
`$GRAPH` to point to a small demo data file and then use that variable
instead of the full file name.  We use quotes around the match pattern
to protect it from interpretation by the shell. The result of the
queries are shown in tables to facilitate readability:

```
GRAPH=examples/docs/query-graph.tsv
 
kgtk query -i $GRAPH --match '()-[]->()'
```
Result:

|     id  | node1 | label  | node2     |
| ------- | ----- | ------ | --------- |
|     e11 | Hans  | loves  | Molly     |
|     e12 | Otto  | loves  | Susi      |
|     e13 | Joe   | friend | Otto      |
|     e14 | Joe   | loves  | Joe       |
|     e21 | Hans  | name   | 'Hans'@de |
|     e22 | Otto  | name   | 'Otto'@de |
|     e23 | Joe   | name   | "Joe"     |
|     e24 | Molly | name   | "Molly"   |
|     e25 | Susi  | name   | "Susi"    |

The match pattern starts with an anonymous node connecting via an
anonymous relation to another anonymous node.  It is matched against
the four core columns specifying an edge in each line of the KGTK
input file.  The from-node is matched against `node1`, the relation is
matched against `id` and `label` (more on that distinction below), and
the to-node is matched against `node2`.  For each KGTK line matching
the pattern, output is generated according to the `--return` clause
specification.  The default for `--return` is `*` which means all
columns of a matching line will be output (including extra columns if
any).  Therefore, the resulting output shows the full content of the
file starting with its KGTK header line.

The following query is equivalent to the above.  The singular
anonymous node pattern will be completed to a full edge by implicitly
adding an anonymous relation and to-node:

```
kgtk query -i $GRAPH --match '()'
```

That pattern is also the default for `--match`, so the following query
is again equivalent to the above and produces the same as running
`cat` on the file:

```
kgtk query -i $GRAPH
```

Especially on larger data, it is always a good idea to restrict a
query to a small result set first to see if the returned result is the
one expected.  This can be done by using `--limit N` so that at most
`N` result rows will be produced (not counting the header line):

```
kgtk query -i $GRAPH --limit 3
```
Result:

|  id     | node1 | label  | node2 |
| ------- | ----- | ------ | ----- |
|     e11 | Hans  | loves  | Molly |
|     e12 | Otto  | loves  | Susi  |
|     e13 | Joe   | friend | Otto  |

Similarly, `--skip N` can be used to skip `N` result rows first before
any of them are output which can then be further limited with `--limit`:

```
kgtk query -i $GRAPH --skip 2 --limit 3
```
Result:

| id      | node1 | label  | node2     |
| ------- | ----- | ------ | --------- |
|     e13 | Joe   | friend | Otto      |
|     e14 | Joe   | loves  | Joe       |
|     e21 | Hans  | name   | 'Hans'@de |


The Unix `head` and `tail` commands can also be used for the same
purpose but may cut off the header row, since they do not understand
the KGTK file format:

```
kgtk query -i $GRAPH | tail +3 | head -3
```

Result:

| e12     | Otto | loves  | Susi |
| ------- | ---- | ------ | ---- |
|     e13 | Joe  | friend | Otto |
|     e14 | Joe  | loves  | Joe  |


More interesting patterns can be formed by restricting some of the
elements of an edge.  For example, here we filter for all edges that
start with `Hans` using Kypher's colon-restriction syntax in the
from-node of the pattern:

```
kgtk query -i $GRAPH --match '(:Hans)-[]->()'
```
Result:

|     id  | node1 | label | node2     |
| ------- | ----- | ----- | --------- |
|     e11 | Hans  | loves | Molly     |
|     e21 | Hans  | name  | 'Hans'@de |

Note that this shows one of the significant differences between Kypher
and Cypher.  In Cypher the restriction label `Hans` would be
interpreted as a node *type* in a property graph.  In KGTK, it is
interpreted as the ID of a particular node which is what the values
in the `node1` and `node2` columns really represent.

We can also filter on the relation of an edge.  For example, here we
select all edges with `label` `name` using the colon-restriction
syntax on the relation part of the pattern:

```
kgtk query -i $GRAPH --match '()-[:name]->()'
```
Result:

| id      | node1 | label | node2     |
| ------- | ----- | ----- | --------- |
|     e21 | Hans  | name  | 'Hans'@de |
|     e22 | Otto  | name  | 'Otto'@de |
|     e23 | Joe   | name  | "Joe"     |
|     e24 | Molly | name  | "Molly"   |
|     e25 | Susi  | name  | "Susi"    |

For relations, the interpretation of restrictions on the label of an
edge (as opposed to its `id`) is more in line with standard Cypher.

Node and relation restrictions can be combined.  For example, here we
select all `name` edges starting from node `Otto`:

```
kgtk query -i $GRAPH --match '(:Otto)-[:name]->()'
```
Result:

| id  | node1 | label | node2     |
| --- | ----- | ----- | --------- |
| e22 | Otto  | name  | 'Otto'@de |


### Filtering with the `--where` clause

The `--where` clause is a possibly complex Boolean expression that gets evaluated
as an additional filter for each edge selected by the `--match` clause.  Only those
edges for which it evaluates to true will be returned.  The `--where` clause can
be used as an alternative to some of the constructs in the `--match` clause, or
to express more complex conditions and computations that cannot be stated in a
match pattern.

In order to get access to values selected by the match pattern that
can then be further restricted, we need match pattern *variables*.
Variables are specified with a simple name in the node or relationship
part of a pattern.  For example, below we use `p` as the variable for
the starting node of the edge pattern which then leads via a `name`
relation to another node.  In the `--where` clause we restrict which
values are allowed for `p`.  In fact, this query is equivalent to the
one above where we restricted the starting node directly in the match
pattern:

```
kgtk query -i $GRAPH \
     --match '(p)-[:name]->()' \
     --where 'p = "Otto"'
```
Result:

|  id     | node1 | label | node2     |
| ------- | ----- | ----- | --------- |
|     e22 | Otto  | name  | 'Otto'@de |

The following query is equivalent but specifies the starting node
restriction twice which is perfectly legal but redundant:

```
kgtk query -i $GRAPH \
     --match '(p:Otto)-[:name]->()' \
     --where 'p = "Otto"'
```

Note that constants such as `Otto` need to be quoted when used in the `--where`
clause very similar to SQL.  This needs to be handled carefully, since we have
to make sure that the quotes will not be ignored by the Unix shell (see
[<b>Quoting</b>](#quoting) for more details).

Next is an example using a regular expression to filter on the names attached to
nodes.  The Kypher `=~` operator matches a value against a regular expression.
Note that Kypher regular expressions use Python regexp syntax, which is different
from the Java regexps used in Cypher.  In the query below we select all `name`
edges that lead to a name that contains a double letter:

```
kgtk query -i $GRAPH \
     --match '(p)-[:name]->(n)' \
     --where 'n =~ ".*(.)\\1.*"'
```
Result:

| id      | node1 | label | node2     |
| ------- | ----- | ----- | --------- |
|     e22 | Otto  | name  | 'Otto'@de |
|     e24 | Molly | name  | "Molly"   |

We can also filter based on a list of values which is one way of specifying disjunction
in Kypher.  In this query, any edge where `p` is equal to one of the listed values will
be returned as a result.  Note that Kypher only allows lists of literals such as strings
or numbers, but not variables or other expressions which is legal in Cypher:

```
kgtk query -i $GRAPH \
     --match '(p)-[:name]->(n)' \
     --where 'p IN ["Hans", "Susi"]'
```
Result:

|    id   | node1 | label | node2     |
| ------- | ----- | ----- | --------- |
|     e21 | Hans  | name  | 'Hans'@de |
|     e25 | Susi  | name  | "Susi"    |

Another way to filter edges is by using a comparison operator
coupled with a computation using built-in functions.  Note that all
columns in a KGTK file are treated as text (even if they contain
numbers), so the expression below filters for names that start with
the letter `J` or later.  Also note that the single and double quotes
of KGTK string literals are part of their value and need to be
appropriately accounted for.  To achieve this we use the built-in
function `substr` to extract the first letter of each name following
the quote character.  `substr` is one of [SQLite3 built-in scalar
functions](https://sqlite.org/lang_corefunc.html), all of which can be
used in `--where` and other Kypher clauses that accept expressions
(see [<b>Built-in functions</b>](#built-in-functions) for more details):

```
kgtk query -i $GRAPH \
     --match '(p)-[:name]->(n)' \
     --where "substr(n,2,1) >= 'J'"
```
Result:

| id      | node1 | label | node2     |
| ------- | ----- | ----- | --------- |
|     e22 | Otto  | name  | 'Otto'@de |
|     e23 | Joe   | name  | "Joe"     |
|     e24 | Molly | name  | "Molly"   |
|     e25 | Susi  | name  | "Susi"    |


### Sorting results with the `--order-by` clause

We can use `--order-by` to sort results just like in Cypher and SQL.
For example, the following query sorts by names in ascending order.

```
kgtk query -i $GRAPH \
     --match '(p)-[:name]->(n)' \
     --where "upper(substr(n,2,1)) >= 'J'" \
     --order-by n
```
Result:

| id      | node1 | label | node2     |
| ------- | ----- | ----- | --------- |
|     e23 | Joe   | name  | "Joe"     |
|     e24 | Molly | name  | "Molly"   |
|     e25 | Susi  | name  | "Susi"    |
|     e22 | Otto  | name  | 'Otto'@de |


Note how the last row in the result is seemingly out of order.  This
is because the quote character of KGTK literals is part of their
value, thus language-qualified strings starting with single quotes
come after regular strings in double quotes.  To avoid that we can
again apply a computation expression, this time in the `--order-by`
clause to only look at the first letter following the quote.  In this
example we also use the `desc` keyword to sort in descending order:

```
kgtk query -i $GRAPH \
     --match '(p)-[:name]->(n)' \
     --where "substr(n,2,1) >= 'J'" \
     --order-by "substr(n,2,1) desc"
```
Result:

|     id  | node1 | label | node2     |
| ------- | ----- | ----- | --------- |
|     e25 | Susi  | name  | "Susi"    |
|     e22 | Otto  | name  | 'Otto'@de |
|     e24 | Molly | name  | "Molly"   |
|     e23 | Joe   | name  | "Joe"     |


### Controlling results with the `--return` clause

So far all examples simply output all columns of a matching edge in a
KGTK input file.  However, we often want to perform some kind of
transformation on the data such as selecting or adding columns,
changing their order, changing values, computing derived values, and
so on.  To do that we can use Kypher's `--return` clause.  By default
its value is `*`, which means all columns of a matching edge will be
output (including extra columns if any).

In the following query, we select only the `node1` and `node2` columns
by referencing their respective pattern variables `p` and `n`.  Kypher
maintains the association between where a particular pattern variable
is used in a match pattern and the corresponding KGTK column names
such as `node1`, `node2`, etc., and uses the relevant column names
upon output.  Note, that the result generated here is not valid KGTK,
since it is missing the `id` and `label` columns:

```
kgtk query -i $GRAPH \
     --match '(p)-[:name]->(n)' \
     --where 'n =~ ".*(.)\\1.*"' \
     --return 'p, n'
```
Result:

|     node1 | node2     |
| --------- | --------- |
|     Otto  | 'Otto'@de |
|     Molly | "Molly"   |

Next we are returning all columns, switching their order.  There is
one extra bit of complexity with respect to the relation variable `r`
of the match pattern.  Due to the difference between the property
graph data model of Cypher and the data model used by KGTK, relation
variables get bound to edge IDs in KGTK's `id` column, since those
represent the unique identities of edges.  All other elements of an
edge such as its `node1`, `node2`, `label` and extra columns can then
be referenced using Kypher's property syntax.  For example, `r.label`
references an edge's label, `r.node1` its starting node, or `r.time`
an extra column named `time`.  See [<b>Edges and properties</b>](#properties)
for more details.  Below is the query which now does produce
valid KGTK as output (the order of columns does not matter):

```
kgtk query -i $GRAPH \
     --match '(p)-[r:name]->(n)' \
     --where 'n =~ ".*(.)\\1.*"' \
     --return 'p, n, r, r.label'
```
Result:

| node1     | node2     | id  | label |
| --------- | --------- | --- | ----- |
|     Otto  | 'Otto'@de | e22 | name  |
|     Molly | "Molly"   | e24 | name  |

Sometimes we want to summarize the data in some way.  For example,
we might want to know all the different relationship labels used.
We can do this with the following query where we use the `distinct`
keyword in the `--return` clause to eliminate any duplicates:

```
kgtk query -i $GRAPH \
     --match '(p)-[r]->(n)' \
     --return 'distinct r.label' \
     --order-by r.label
```
Result:

| label      |
| ---------- |
|     friend |
|     loves  |
|     name   |


One of the most powerful features of Kypher is that we can transform
values into new ones building modified or completely new edges.  Many
useful transformations can be performed by applying built-in functions
to the columns specified in a `--return` clause.  For example, below
we change the names of the selected edges by converting them to
lowercase using another one of SQLite3's built-in functions:

```
kgtk query -i $GRAPH \
     --match '(p)-[r:name]->(n)' \
     --where 'n =~ ".*(.)\\1.*"' \
     --return 'p, r.label, lower(n), r'
```
Result:

| node1     | label | lower(graph_2_c1."node2") | id  |
| --------- | ----- | ------------------------- | --- |
|     Otto  | name  | 'otto'@de                 | e22 |
|     Molly | name  | "molly"                   | e24 |


In the result above, Kypher did not know which KGTK column to
associate the computed value with and simply used the column header
produced by the underlying SQL engine.  However, we can provide
explicit return aliases to map a result column onto whichever KGTK
column name we want.  For example:

```
kgtk query -i $GRAPH \
     --match '(p)-[r:name]->(n)' \
     --where 'n =~ ".*(.)\\1.*"' \
     --return 'p, r.label, lower(n) as node2, r'
```
Result:

| node1     | label | node2     | id  |
| --------- | ----- | --------- | --- |
|     Otto  | name  | 'otto'@de | e22 |
|     Molly | name  | "molly"   | e24 |

Here is another more complex example that uses the built-in function
`kgtk_unstringify` to convert KGTK string literals to regular symbols,
and `kgtk_stringify` to convert regular symbols into strings.
KGTK-specific built-in functions all start with a `kgtk_` prefix and
are documented in more detail here: [<b>Built-in functions</b>](#built-in-functions).
Note below how the language-qualified string `'Otto'@de` stays
unchanged, since `kgtk_unstringify` only modifies values that are in
fact string literals.  Again we use aliases to produce valid KGTK
column names:

```
kgtk query -i $GRAPH \
     --match '(p)-[r:name]->(n)' \
     --where 'n =~ ".*(.)\\1.*"' \
     --return 'kgtk_stringify(p) as node1, r.label, kgtk_unstringify(n) as node2, r'
```
Result: 

| node1       | label | node2     | id  |
| ----------- | ----- | --------- | --- |
|     "Otto"  | name  | 'Otto'@de | e22 |
|     "Molly" | name  | Molly     | e24 |

Since subcomponents of structured literals such as the language field
in a language-qualified string can be interpreted as *virtual*
properties of a value, we also allow the property syntax to be used to
access these fields (in addition to regular function calls).  For
example, in this query we first select edges with language-qualified
names and then use `n.kgtk_lqstring_lang` to retrieve the language
field into a separate column named as `node2;lang` in the return
(which is a path column name that needs to be quoted with backticks in
Kypher - see [<b>Quoting</b>](#quoting) for more details).

```
kgtk query -i $GRAPH \
     --match '(p)-[r:name]->(n)' \
     --where 'kgtk_lqstring(n)' \
     --return 'r, p, r.label, lower(n) as node2, n.kgtk_lqstring_lang as `node2;lang`'
```
Result:

| id      | node1 | label | node2     | node2;lang |
| ------- | ----- | ----- | --------- | ---------- |
|     e21 | Hans  | name  | 'Hans'@de | de         |
|     e22 | Otto  | name  | 'Otto'@de | de         |


### Querying connected edges through graph patterns

So far we have only selected single edges and then filtered them in a number of different ways.
In Knowledge Graphs, however, we will often want to combine multiple edges into a query such
going from a person to their employer to the employer's location, for example.  In database
parlance, such an operation is generally called a *join*, since information from multiple tables
is combined along a common join element.  In Kypher we can express such queries very elegantly
by using Cypher's graph patterns.  For example, in the query below we start from a person
node `a` connected via a `loves` edge `r` to another node `b`, and for each of nodes `a` and `b` we
are following a `name` edge to their respective names.  We express this query here using a
single path following arrows in both directions, but other formulations are possible:

```
kgtk query -i $GRAPH \
     --match '(na)<-[:name]-(a)-[r:loves]->(b)-[:name]->(nb)' \
     --return 'r, na as node1, r.label, nb as node2'
```
Result:

| id      | node1     | label | node2   |
| ------- | --------- | ----- | ------- |
|     e14 | "Joe"     | loves | "Joe"   |
|     e11 | 'Hans'@de | loves | "Molly" |
|     e12 | 'Otto'@de | loves | "Susi"  |

Here is a variant of the above that looks for circular edges so we can
find all people (in this dataset) who are in love with themselves:

```
kgtk query -i $GRAPH \
     --match '(na)<-[:name]-(a)-[r:loves]->(a)-[:name]->(nb)' \
     --return 'r, na as node1, r.label, nb as node2'
```
Result:

| id      | node1 | label | node2 |
| ------- | ----- | ----- | ----- |
|     e14 | "Joe" | loves | "Joe" |

Of course, these path patterns can be combined with `--where` expression for
more elaborate filtering that cannot be described in the graph pattern directly.  For example,
here we only select starting edges where at least one of the nodes has a German name:

```
kgtk query -i $GRAPH \
     --match '(na)<-[:name]-(a)-[r:loves]->(b)-[:name]->(nb)' \
     --where 'na.kgtk_lqstring_lang = "de" OR nb.kgtk_lqstring_lang = "de"' \
     --return 'r, na as node1, r.label, nb as node2'
```
Result:

| id      | node1     | label | node2   |
| ------- | --------- | ----- | ------- |
|     e11 | 'Hans'@de | loves | "Molly" |
|     e12 | 'Otto'@de | loves | "Susi"  |

It is generally a good practice to only name pattern variables that are actually referenced
somewhere else and leave all others anonymous.  Rewriting the above query this way we get
the following:

```
kgtk query -i $GRAPH \
     --match '(na)<-[:name]-()-[r:loves]->()-[:name]->(nb)' \
     --where 'na.kgtk_lqstring_lang = "de" OR nb.kgtk_lqstring_lang = "de"' \
     --return 'r, na as node1, r.label, nb as node2'
```
Result:

|     id  | node1     | label | node2   |
| ------- | --------- | ----- | ------- |
|     e11 | 'Hans'@de | loves | "Molly" |
|     e12 | 'Otto'@de | loves | "Susi"  |


### Querying with disjunctions

There is limited support available for querying with disjunctions as
already used in some of the examples above.  For now these are limited
to `OR` and `IN` expressions in the `--where` clause of a query.  For
example:

```
kgtk query -i $GRAPH \
     --match '(:Joe)-[r]->()' \
     --where 'r.label="friend" OR r.label="loves"'
```
Result:

|  id   |  node1 | label  | node2 |
|-------|--------|--------|-------|
|  e13  |  Joe   | friend | Otto  |
|  e14  |  Joe   | loves  | Joe   |


The same query could be formulated with an `IN` clause:

```
kgtk query -i $GRAPH \
     --match '(:Joe)-[r]->()' \
     --where 'r.label IN ["friend", "loves"]'
```
Result:

|  id   |  node1 | label  | node2 |
|-------|--------|--------|-------|
|  e13  |  Joe   | friend | Otto  |
|  e14  |  Joe   | loves  | Joe   |

Cypher also supports the following idiom which is not yet available in Kypher:

```
kgtk query -i $GRAPH --match '(:Joe)-[:friend|loves]->()'
Multiple relationship labels are not (yet) allowed
```

More comprehensive `union` processing to combine the results of multiple queries
might become available in future versions.  Some kind of that can already
be achieved through pipelines of KGTK commands combining `query` and `cat`, for
example.  Certain cases can also be handled by introducing additional graphs
such as the `$PROPS` graph used in [this example](#time-machine-use-case).

!!! note
    <b>Important:</b> restrictions via `OR` and `IN` defeat any indexing and might
    result in long query times on large graphs in the absence of other direct
    restrictions (such as the `node1` restriction to `Joe` in the examples above).


### Querying connected edges across multiple graphs

Perhaps the most powerful feature of Kypher is that we can combine information
from different graphs represented in separate KGTK files.  This allows us to
mix and match information from different graphs and combine it into new graphs,
or simply represent certain aspects of a graph in a separate file for ease of
manipulation or reuse.

To demonstrate this functionality we use a second example file of employment
data for the people we have seen in the queries so far.  This data also has some
extra columns such as a `salary` for each `node1` and a `graph` qualifier naming
a graph each edge belongs to:

```
WORKS=examples/docs/query-works.tsv

kgtk query -i $WORKS --match '()-[]->()'
```   
Result:

| id      | node1 | label      | node2  | node1;salary | graph  |
| ------- | ----- | ---------- | ------ | ------------ | ------ |
|     w11 | Hans  | works      | ACME   | 10000        | employ |
|     w12 | Otto  | works      | Kaiser | 8000         | employ |
|     w13 | Joe   | works      | Kaiser | 20000        | employ |
|     w14 | Molly | works      | Renal  | 11000        | employ |
|     w15 | Susi  | works      | Cakes  | 9900         | employ |
|     w21 | Hans  | department | R&D    |              | employ |
|     w22 | Otto  | department | Pharm  |              | employ |
|     w23 | Joe   | department | Medic  |              | employ |
|     w24 | Molly | department | Sales  |              | employ |
|     w25 | Susi  | department | Sales  |              | employ |


Let us start with a query that retrieves people and the companies
their love interests work for.  To query across multiple graphs we
need two things: (1) we need to specify multiple KGTK input files
via multiple `-i` options.  (2) we need to be able to associate edges
in a match pattern with a particular input graph.

Cypher does not address multi-graph queries, every query is always
assumed to query a single graph.  To allow this in Kypher we extended
the pattern syntax in the following way: a graph name followed
by a colon preceding a match pattern clause indicates that the clause
and all following clauses are associated with the named graph, either
until the end of the pattern is reached, or until a different graph
variable is introduced.  For example, the pattern:
```
g: (x)-[:loves]->(y)
```
means that the edge should be matched against edges from graph `g`.

Another connection we need is to link such a graph name to one of the
provided input files.  Kypher does this by greedily looking for these
graph names in the file names and paths of the input files specified in
order.  Once a match is found that file is removed from the match pool
and any remaining graph variables are matched against the remaining files.
See [<b>Input and output specifications</b>](#input-output) on more details of this
process.  A simple way of referring to files as graphs is by the initial
character of their file name (as long as they differ), which is what we
do here.  `g` matches the `graphs.tsv` file and `w` matches `works.tsv`.

Finally we can run the query.  Note that multiple edges in the match pattern
are represented by separate pattern elements that are conjoined by commas.
The variable `y` is what joins the edges across graphs.  So, naturally,
this query will only work if bindings found for `y` in graph `g` also
exist as `node1`s in graph `w`:

```
kgtk query -i $GRAPH -i $WORKS \
     --match 'g: (x)-[r:loves]->(y), w: (y)-[:works]->(c)' \
     --return 'r, x, r.label, y, c as `node2;employer`'
```
Result:

| id      | node1 | label | node2 | node2;employer |
| ------- | ----- | ----- | ----- | -------------- |
|     e14 | Joe   | loves | Joe   | Kaiser         |
|     e11 | Hans  | loves | Molly | Renal          |
|     e12 | Otto  | loves | Susi  | Cakes          |

If no initial graph is specified in the match clause, it will be assigned to
the default graph which corresponds to the one defined by the first input file,
so the order in which input files are specified is important:

```
kgtk query -i $GRAPH -i $WORKS \
     --match '(x)-[r:loves]->(y), w: (y)-[:works]->(c)' \
     --return 'r, x, r.label, y, c as `node2;employer`'
```    
Result:

| id      | node1 | label | node2 | node2;employer |
| ------- | ----- | ----- | ----- | -------------- |
|     e14 | Joe   | loves | Joe   | Kaiser         |
|     e11 | Hans  | loves | Molly | Renal          |
|     e12 | Otto  | loves | Susi  | Cakes          |

As before the `--where` clause can be used to restrict matches further, and it
may of course restrict variables from any graph.  Let us query for employees
with a certain minimum salary.  To access the salary of a person which is
represented in an extra column labeled `node1;salary` in the `WORKS` data, we
need to employ node properties.  Recall that edge properties such as `r.label`
could be used to access any qualifier about an edge `r`.  Similarly, for nodes
where an additional edge is specified through a path expression in the header
such as `node1;salary`, the value in the column can be accessed through a node
property.  One way to make this connection in the match pattern is through
the following syntax (which follows Cypher properties but deviates from their
semantics):

```
(y {salary: s})
```

This accesses the `salary` property of `y` (`node1` in graph `w`) which leads
to the values in the `node1;salary` column which in turn get bound to the newly
introduced pattern variable `s`.  We can then use `s` in subsequent match clauses
as well as in where and return specifications to access and restrict those values.

```
kgtk query -i $GRAPH -i $WORKS \
     --match 'g: (x)-[r:loves]->(y), w: (y {salary: s})-[:works]->(c)' \
     --where 's >= 10000' \
     --return 'r, x, r.label, y as node2, c as `node2;work`, s as `node2;salary`'
```
Result:

|   id    | node1 | label | node2 | node2;work | node2;salary |
| ------- | ----- | ----- | ----- | ---------- | ------------ |
|     e14 | Joe   | loves | Joe   | Kaiser     | 20000        |
|     e11 | Hans  | loves | Molly | Renal      | 11000        |
|     e12 | Otto  | loves | Susi  | Cakes      | 9900         |

From the last result row above it looks as if the restriction didn't
really work correctly, since that salary is less than 10000.  The
reason for this is that KGTK values can be type heterogeneous and do
not have a specific data type defined for them, and are therefore all
interpreted as text by the underlying database.  So the comparison
operator restricted lexical order of strings instead of numeric
values.  In order for the comparison to work as intended, we have to
explicitly convert the salary value to a numeric type.  One way to do
this is with the SQLite built-in `cast`:

```
kgtk query -i $GRAPH -i $WORKS \
     --match 'g: (x)-[r:loves]->(y), w: (y {salary: s})-[:works]->(c)' \
     --where 'cast(s, integer) >= 10000' \
     --return 'r, x, r.label, y as node2, c as `node2;work`, s as `node2;salary`'
```
Result:

| id      | node1 | label | node2 | node2;work | node2;salary |
| ------- | ----- | ----- | ----- | ---------- | ------------ |
|     e14 | Joe   | loves | Joe   | Kaiser     | 20000        |
|     e11 | Hans  | loves | Molly | Renal      | 11000        |

Another possibility is to use one of the built-in KGTK literal accessors
which in this case accesses the numeric value of a quantity literal as a number:

```
kgtk query -i $GRAPH -i $WORKS \
     --match 'g: (x)-[r:loves]->(y), w: (y {salary: s})-[:works]->(c)' \
     --where 's.kgtk_quantity_number >= 10000' \
     --return 'r, x, r.label, y as node2, c as `node2;work`, s as `node2;salary`'
```
Result: 

| id      | node1 | label | node2 | node2;work | node2;salary |
| ------- | ----- | ----- | ----- | ---------- | ------------ |
|     e14 | Joe   | loves | Joe   | Kaiser     | 20000        |
|     e11 | Hans  | loves | Molly | Renal      | 11000        |


### Aggregation

Similar to SQL and Cypher, Kypher supports aggregation functions such
as `count`, `min`, `max`, `avg`, etc.
(see [<b>Built-in functions</b>](#built-in-functions)).  The simplest
aggregation operation involves counting rows or values via the `count`
function.  For example, we might want to know how many edges have Joe
as the starting node:

```
kgtk query -i $GRAPH \
     --match '(:Joe)-[r]->()' \
     --return 'count(r) as N'
```
Result:

| N    |
| ---- |
|    3 |

The `count` function counts all rows that would have been output
without the use of count which we can see when we remove it from the
query:

```
kgtk query -i $GRAPH \
     --match '(:Joe)-[r]->()' \
     --return r
```
Result:

| id   |
| ---- |
|  e13 |
|  e14 |
|  e23 |

This would also include any duplicate values.  To exclude duplicates
we can add the `distinct` keyword as the first argument to `count` (in
fact, all aggregation functions take an optional `distinct` argument).
For example, here we count all distinct labels used in the data:

```
kgtk query -i $GRAPH \
     --match '(:Joe)-[r]->()' \
     --return 'count(distinct r.label) as N'
```
Result:

| N    |
| ---- |
|    3 |

Different than SQL, however, Kypher does not have an explicit
`group by` clause and infers proper grouping from clause type and
order in the `return` statement.  Grouping refers to the process of
sorting result rows into groups before an aggregation operation is
applied to each group.  In the count queries above, there was only a
single group containing the full result set.  In the next query we are
grouping by relationship label and then select the maximum `node2`
value for each label group (here `max` is interpreted lexicographically).

```
kgtk query -i $GRAPH \
     --match '(x)-[r]->(y)' \
     --return 'r.label, max(y) as node2, x, r'
```
Result:

| label   |  node2      |  node1  |  id  |
| --------|-------------|---------|------|
| friend  |  Otto       |  Joe    |  e13 |
| loves   |  Susi       |  Otto   |  e12 |
| name    |  'Otto'@de  |  Otto   |  e22 |

In this query the `max` function was applied to groups of result rows
where `r.label` had the same value.  But for this to do what we
intended, we had to move the relation ID variable `r` to the end,
otherwise it would have served as the grouping criterion which is not
what we want.

Looking at our employment data again, let us find the person with the
biggest salary (remember the use of `cast` to convert a textual salary
value to a number).  Since we are aggregating over all employees, the
aggregation function needs to be the first in the `--return` clause:

```
kgtk query -i $WORKS \
     --match 'w: (y {salary: s})-[r:works]->(c)' \
     --return 'max(cast(s, int)) as `node1;salary`, y, "works" as label, c, r'
```
Result:

|  node1;salary  |  node1  |  label  |  node2   |  id   |
|----------------|---------|---------|----------|-------|
|         20000  |    Joe  |  works  |  Kaiser  |  w13  |


Finally, let us compute an average company salary.  Here we use
`count` as well so we can see that only one employer has a non-trivial
average in this data:

```
kgtk query -i $WORKS \
     --match '(x)-[:works]->(c)' \
     --return 'c as company, count(c) as n_empl, avg(cast(x.salary, int)) as avg_salary'
```
Result:

|  company  |  n_empl  |  avg_salary  |
|-----------|----------|--------------|
|     ACME  |       1  |     10000.0  |
|    Cakes  |       1  |      9900.0  |
|   Kaiser  |       2  |     14000.0  |
|    Renal  |       1  |     11000.0  |


<A NAME="input-output"></A>
## Input and output specifications

Kypher can query one or more input graphs specified in KGTK file
format and will generally produce an output graph also in KGTK format.
The output format is very flexible, however, and can really be any
tab-separated format with or without a header row, not just legal
KGTK.  The following command options provide control over query inputs
and outputs:

```
  -i INPUT_FILE [INPUT_FILE ...], --input-files INPUT_FILE [INPUT_FILE ...]
                        One or more input files to query (maybe compressed).
                        (Required, use '-' for stdin.)
  --as NAME             alias name to be used for preceding input
  --no-header           do not generate a header row with column names
  -o OUTPUT, --out OUTPUT
                        output file to write to, if `-' (the default) output
                        goes to stdout. Files with extensions .gz, .bz2 or .xz
                        will be appropriately compressed.
```

Input files can be in plain text or compressed via `gzip`, `bzip2` or `xz`.
Compression type must be indicated with an appropriate file name extension
such as `.gz`, `.bz2` or `.xz`.  Input can also come from standard input
which needs to be specified via `-`, even if only a single input is used.

!!! note
    Input files are assumed to be in valid KGTK format with standard `id`, `node1`, `label`
    and `node2` headers for the core columns.  Additional columns are also allowed.  The
    `query` command will not perform any validation and may fail when given invalid KGTK files.

!!! note
    <b>Important restriction:</b> if an input is specified to be coming from standard input
    none of the commands feeding the query must themselves be query commands due to
    database locking considerations.  Future versions will relax this restriction.

### Input naming

The file names and directory paths of input files serve the following purposes:

1. to identify the KGTK data that needs to be queried
2. to control caching, for example, a file that has previously been queried and
   imported into the cache does not need to be imported again, unless it has changed
3. to name the input graphs so that they can be selectively referenced in match clauses
   which is the focus of this section

If there is only a single input, all match clauses will be matched against that input
only.  If there is more than one, however, we need to be able to specify which match
clause is matched against which input.  There are two things necessary to make this
association.  First we need a way to link a match pattern to the graph it should be
applied to.  Standard Cypher does not support querying across multiple graphs, so we
extended the Kypher match pattern syntax with the following idiom:
```
        name: pattern
```
This means that `pattern` should only be applied to the graph named `name`.  For example,
the following pattern looks for employer edges in the graph named `w`:
```
        w: (x)-[:works]->(c)
```
We call `w` a graph variable or *handle* which follows the same syntactic conventions
as pattern variables for nodes and relations.

The second thing we need is to link these graph handles to the
provided input(s).  Since file names will often be long and unwieldy
and contain special characters, we do not require them to be repeated
literally in match clauses.  Instead we make this association with a
simple greedy match process:

1. graph handles are processed in the order listed in the match pattern.
2. when a graph handle is being matched, it is matched against available
   inputs in the order listed in the query command
3. a handle matches an available input if
    * it matches the full input path name exactly as listed, or
    * it is contained as a substring in the base name (non-directory)
      portion of the input file name, or
    * it has a numeric suffix (e.g., `g42`) and its non-numeric prefix
      is contained as a substring in the base name of the input file
4. if no match can be found for a particular handle, an error will be raised
5. once a handle is matched is matching input is removed from the pool of
   available inputs and the next handle (if any) is matched against the
   remaining ones

Finally, if the first match clause does not have a graph handle, its
handle implicitly becomes the default graph which gets matched to the
first input file.  Clauses that are not directly preceded by a graph
handle inherit theirs from the previous clause, so only changes from
one graph to another need to be explicitly marked in the match
pattern.

If one of the inputs is standard input, its internally associated file
name is (or ends with) `/dev/stdin` which can be used to refer to it
with a graph handle (e.g., via `s` or `stdin`).

Here are some examples with inputs and graph handles referring to them.
We start with a simple case with two graph handles based on the first
letter of the corresponding input file (base name):

```
kgtk query -i data/graph.tsv -i data/works.tsv \
     --match 'g: (x)-[r]->(y), w: (y)-[]->(z)' ...
```

The next example illustrates the greedy matching strategy.  The `r`
handle is ambiguous, since it could be matched to either file, but it
will in fact be matched to the first listed input that matches:

```
kgtk query -i data/graph.tsv -i data/works.tsv \
     --match 'r: (x)-[r]->(y), w: (y)-[]->(z)' ...
```

Next handles are matched in a different order than in which the inputs
are listed:

```
kgtk query -i data/graph.tsv -i data/works.tsv \
     --match 'w: (y)-[]->(z), g: (x)-[r]->(y)' ...
```

Using longer, more descriptive handles:

```
kgtk query -i data/graph.tsv -i data/works.tsv \
     --match 'works: (y)-[]->(z), graph: (x)-[r]->(y)' ...
```

Next we use a full file name as a handle which requires backtick quoting
to guard the special characters:

```
kgtk query -i data/graph.tsv -i data/works.tsv \
     --match '`data/works.tsv`: (y)-[]->(z), g: (x)-[r]->(y)' ...
```

The next example shows how handles are inherited from previous clauses.
For example, here the second match clause inherits the handle `g` from
the previous clause:

```
kgtk query -i data/graph.tsv -i data/works.tsv \
     --match 'g: (x)-[r]->(y), (y)-[]->(z), w: (z)-[]->(s)' ...
```

The next example shows how numeric suffixes in handles can be used to
match to similar file names in order.  For example, after an initial
match attempt for `graph1` fails, its prefix `graph` will be tried in
a second round.  Note that the numeric suffix does not need to occur
in any input file:

```
kgtk query -i data/graph-a.tsv -i data/graph-b.tsv \
     --match 'graph1: (x)-[r]->(y), graph2: (y)-[]->(z)' ...
```

Example with an input coming from standard input.  This currently requires naming
the input via an alias, future versions will implicitly define a filename using `stdin`
as its basename:

```
kgtk cat -i file1.tsv -i file2.tsv / query -i - --as stdin -i data/works.tsv \
     --match 's: (x)-[r]->(y), w: (y)-[]->(z)' ...
```

In the final example, the first match clause is associated with a
default handle based on the first listed input file.  This happens
before any explicit handles are matched with input files.  For that
reason, the second handle `r` which is ambiguous gets assigned to the
second input file, since the first input is already linked (by
default) to the first clause:

```
kgtk query -i data/graph.tsv -i data/works.tsv \
     --match '(x)-[r]->(y), r: (y)-[]->(z)' ...
```


### Renaming inputs

The `query` command expands each input file name into an absolute,
unambiguous file name that dereferences any symbolic links before it
stores it in its internal bookkeeping tables.  When an input is
processed for data import, data reuse or cache update, that expanded
file name defines the identity or name of the data.

It is sometimes useful to have a different name for an input, for
example, to eliminate the specific details of a file name, to name
inputs more logically, or to prevent the specifics of a file system
location to be exposed when a cache database is moved or exported to a
different computer.

For this purpose inputs can be renamed with the `--as NAME` option
where the provided name can be any string, even another absolute or
relative file name.  After an input has been renamed, the new name
will be the internally stored name for the data, which will *replace*
the original file or input name (so this is not an alias that can be
used in addition to the original name).  The new name will then be
used for graph handle matching as well as to identify any previously
cached inputs.

For example, here we first run two simple queries to import and name
two separate graphs, and then run a query over those two graphs using
their newly assigned names.  All of this could be done in a single
command but we split it up here to demonstrate reuse of renamed inputs:

```
kgtk query -i data/graph.tsv --as graph --limit 1
```

|  id   |  node1 | label  |  node2  |
|-------|--------|--------|---------|
|  e11  |  Hans  | loves  |  Molly  |

```
kgtk query -i data/works.tsv --as works --limit 1
```

| id  |   node1 | label | node2 | node1;salary  | graph  |
|-----|---------|-------|-------|---------------|--------|
| w11 |   Hans  | works | ACME  | 10000         | employ |

```
kgtk query -i graph -i works \
     --match 'g: (x)-[]->(y), w: (y)-[r]->(z)' \
     --return 'r, y, r.label, z' --limit 2
```
Result:

| id  |   node1 | label | node2  |
|-----|---------|-------|--------|
| w12 |   Otto  | works | Kaiser |
| w13 |   Joe   | works | Kaiser |


Previously renamed inputs can also be renamed again, for example:

```
kgtk query -i graph -i works --as employer \
     --match 'g: (x)-[]->(y), e: (y)-[r]->(z)' \
     --return 'r, y, r.label, z' --limit 2
```
Result:

| id  |   node1 | label | node2  |
|-----|---------|-------|--------|
| w12 |   Otto  | works | Kaiser |
| w13 |   Joe   | works | Kaiser |


### Output specification

Query output is handled similar to most other commands.  By default, output
is sent to standard output where it can be redirected to a file or piped to
other commands.  The `-o FILE` option can be used to send output to the
specified file (a name of `-` means standard output).  If the file name ends
with one of `.gz`, `.bz2` or `.xz` it will automatically be compressed by
the corresponding compression command.  For example:

```
kgtk query -i graph -i works \
     --match 'g: (x)-[]->(y), w: (y)-[r]->(z)' \
     --return 'r, y, r.label, z' \
     -o /tmp/example-query.tsv.gz
```

The `--no-header` option can be used to suppress output of the column header row.


## Graph cache

When one or more input files are queried, their content is first
imported and stored as a number of database tables before they are
queried by the database engine.  This import is generally very fast
but can take a significant amount of time for large datasets.  For
example, the initial import of a Wikidata edge file with 1 billion
edges (~16 GB compressed) takes about 20 minutes on a standard laptop.

To allow us to amortize this import time over multiple queries, the
resulting database is cached into what we call a *graph cache*.  If
another query references an input file that was previously imported,
the query can execute right away without having to import anything.
Any indexes built by the system to speed up queries are also cached in
the graph cache.

The location of the cache file can be controlled with the
`--graph-cache FILE` option.  If that is not explicitly specified,
the system will create or reuse a cache file in the computer's temp
directory which will look like this (where `UID` is replaced by the
current user name):

```
        /tmp/kgtk-graph-cache-UID.sqlite3.db 
```

It is safe to remove these cache files as long as the underlying
KGTK data files still exist.  The cache will simply be rebuilt during
subsequent queries.

When a file is queried, the following rules guide its import or reuse
from the cache:

* the data file exists but does not exist in the cache: the file will
  be imported into the cache and its full dereferenced path name,
  size and modification time will be recorded.
* the data file exists in the cache with the same size and modification time
  as the file on disk: we have a cache hit and the previously imported data will be reused.
* the data file exists in the cache but with different size and/or modification time
  than the file on disk: we assume that the data is different or has changed,
  the previously imported data will be deleted and the file will be imported
  again with its current data and properties
* the data file exists in the cache but does not exist on disk: this is also
  viewed as a cache hit and the previously imported data will be reused;  this
  is a special case to allow the deletion of large data files without losing
  the ability to query them, and it also allows renaming via the `--as` option
  to names that do not correspond to files on disk
* the data file does not exist in the cache or on disk: this raises an error

Graph cache files can become quite large when large or a large number
of different data files are being queried over time.  Cache size is
generally around 1-2.5 times the uncompressed size of all imported
KGTK files depending on indexing requirements.  For large datasets it
is often useful to specify dedicated graph caches via the
`--graph-cache` option to keep file sizes manageable.  Note that all
graphs queried in a single query must reside in the same graph cache.

For good performance, cache files should be on a local SSD drive and
not be mounted via a USB connection or network share.  When data gets
deleted and reimported, freed up space in the cache file is reused,
but unused data pages are not automatically returned to the file
system and the size of the cache file does not shrink.  To actually
free and return any unused space in the cache file to the file system,
one can use the SQLite `vacuum` command (which might take a
significant time to run depending on the size of the cache).  For
example:

```
sqlite3 /tmp/my-graph-cache.sqlite3.db vacuum
```

The graph cache file is an SQLite database file which has a very
stable format across database versions and can be compressed and
shipped to others for quick and easy reuse.  In that case it is
advised to first replace any absolute input file names with logical
names using the `--as` option.


## Kypher language features

Kypher is a complex language and the description in this document will
necessarily be somewhat incomplete.  For a more complete description
of the Cypher language it is based on please refer to
[Cypher](https://neo4j.com/developer/cypher/) and
[openCypher](https://www.opencypher.org/resources), but keep in mind
the important differences described [here](#differences-to-cypher).
Also both Cypher and the implementation of Kypher are closely related
to SQL which is always another good query language reference to
consider.  Finally, while Kypher has a fairly comprehensive parser of
the Cypher language, it will simply raise an exception when an
unsupported feature is requested.  So if in doubt, there is nothing
wrong with experimenting.


<A NAME="properties"></A>
### Node and edge properties

TO DO: Needs to describe edge as well as node properties and how they
relate to extra columns.


<A NAME="quoting"></A>
### Quoting

#### Quoting of literals

Using string literals in queries can be very tricky since for KGTK's
plain and language-qualified string literals quotes are part of their
value.  To properly communicate these quotes to Kypher, we have to
carefully navigate three interacting levels of quote processing:

1. the constituent quotes of KGTK literals such as "Otto" or 'Deutsch'@de which are
   part of their values
2. quoting of Kypher literal restrictions in the query language where literals must be
   enclosed in single or double quotes to be recognized as literals
3. quote processing by the command shell which affects how quotes are passed through to
   the query engine

For example, what we would like to say is something like this:
```
        --where name='"Otto"'
```

but that becomes challenging in a command shell environment which
interprets those quotes.  Here are two example incantations that would
work in `bash` or `tcsh` but that require various complex backslash
escaping or quote nesting:
```
        --where "name = '\"Otto\"'"        # bash
        --where 'name = '"'"'"Otto"'"'"    # tcsh
```

A better mechanism for passing complex literal strings to Kypher is to
use *parameters* which are dollar variables inside the query string
which are then replaced with values passed in via one of the `--para`,
`--spara` or `--lqpara` options.  This allows us to write a
restriction like this:

```
        --where "x = $VAR" --para VAR=FooBar
```

This defines the value of `VAR` as `FooBar` which is then substituted
appropriately for `$VAR` in the restriction.  `--para` uses the
provided value as is, `--spara` additionally KGTK-string-quotes it and
`--lqpara` KGTK-lq-string-quotes it before passing it on.  This
mechanism might still require command shell quoting (e.g., for spaces,
etc.), but we only have to deal with at most one level of quoting this time.

For example, in the query below we pass in a language-qualified string
once with explicit quoting using `--para` and once without quoting
using `--lqpara` where the command will handle quoting for us, as well as a
regular string parameter via `--spara`:

```
kgtk query -i $GRAPH \
     --match '()-[:name]->(n)' \
     --where ' n = $name OR n = $name2 OR n = $name3 ' \
     --para name="'Hans'@de" --spara name2=Susi --lqpara name3=Otto@de
```
Result:

|  id   |  node1 | label | node2     |
|-------|--------|-------|-----------|
|  e21  |  Hans  | name  | 'Hans'@de |
|  e22  |  Otto  | name  | 'Otto'@de |
|  e25  |  Susi  | name  | "Susi"    |

Note that since the `$`-character is also interpreted by the Unix
shell, query strings containing parameters need to be in single
quotes, or the dollar sign needs to be appropriately escaped.


#### Quoting of variables and schema names

TO DO: describe backtick quoting for graph variables, column names, etc.


### Strings, numbers and literals

TO DO


### Null values

The KGTK file format cannot distinguish empty and `NULL` values, so when
empty fields get imported by the `query` command they are represented
as empty strings which is different from `NULL`.  Built-in functions on
the other hand do return `NULL` for undefined values, errors, etc., and
our KGTK built-in functions behave the same way.  Similarly, once supported,
optional queries will also generate `NULL` values that one might want to
test for.

To handle these cases Kypher supports the `IS [NOT] NULL` operator
similar to Cypher and SQL.  For example, in the queries below we
separate language-qualified name strings from other literals by
testing whether the value of an accessor function is defined or not:

```
kgtk query -i $GRAPH \
     --match '(x)-[r:name]->(y)' \
     --where 'kgtk_lqstring_text(y) IS NULL'
```
Result:

|  id   |  node1  |  label  |  node2    |
|-------|---------|---------|-----------|
|  e23  |  Joe    |  name   |  "Joe"    |
|  e24  |  Molly  |  name   |  "Molly"  |
|  e25  |  Susi   |  name   |  "Susi"   |

```
kgtk query -i $GRAPH \
     --match '(x)-[r:name]->(y)' \
     --where 'kgtk_lqstring_text(y) IS NOT NULL'
```
Result:

|  id   |  node1  |  label  |  node2      |
|-------|---------|---------|-------------|
|  e21  |  Hans   |  name   |  'Hans'@de  |
|  e22  |  Otto   |  name   |  'Otto'@de  |

It is sometimes convenient to handle `NULL` values and empty strings uniformly.
The two built-in functions `kgtk_null_to_empty` and `kgtk_empty_to_null` can be
used for that purpose.  For example:

```
kgtk query -i graph \
     --match '(x)-[r:name]->(y)' \
     --where 'kgtk_null_to_empty(kgtk_lqstring_text(y)) != ""'
```
Result:

|  id   |  node1  |  label  |  node2      |
|-------|---------|---------|-------------|
|  e21  |  Hans   |  name   |  'Hans'@de  |
|  e22  |  Otto   |  name   |  'Otto'@de  |


### Regular expressions

TO DO


<A NAME="built-in-functions"></A>
### Built-in functions

Kypher supports a number of built-in functions that can be used in conditions,
return clauses and any other Kypher clause that accepts expressions.  The Kypher
set of built-ins is different from those of Cypher.  Kypher accepts all of SQLite3's
built-ins plus a set of KGTK-specific functions described in more detail below.

Functions are generally very robust to incorrect inputs and will return 0 (False)
or `NULL` for those cases.  However, it is possible to trigger exceptions in
some situations.  If in doubt, use the `typeof` function or appropriate KGTK type
test to guard the call.


#### SQLite built-in functions

All of [SQLite3's built-in scalar
functions](https://sqlite.org/lang_corefunc.html) can be used.  For a comprehensive
list of those functions please follow the link.  Here we list a small subset of
functions particularly important for Kypher with a short description and a link
to their full documentation.

| Function                  | Description                                                                                                    |
|---------------------------|----------------------------------------------------------------------------------------------------------------|
| cast(x, type)             | Convert `x` into an expression of `type`.                                                                      |
| instr(x, sub)             | Find the first occurrence of `sub` in string `x`  ([full doc](https://sqlite.org/lang_corefunc.html#instr)).   |
| length(x)                 | Number of characters in a string `x`              ([full doc](https://sqlite.org/lang_corefunc.html#length)).  |
| lower(x)                  | Convert `x` to lower case                         ([full doc](https://sqlite.org/lang_corefunc.html#lower)).   |
| printf(format, ...)       | Build a formatted string from some arguments      ([full doc](https://sqlite.org/lang_corefunc.html#printf)).  |
| replace(x, from, to)      | Replace `from` with `to` in `x`                   ([full doc](https://sqlite.org/lang_corefunc.html#replace)). |
| substr(x, start, length)  | Substring of `x` of `length` starting at `start`  ([full doc](https://sqlite.org/lang_corefunc.html#substr)).  |
| substr(x, start)          | Substring of `x` starting at `start` to the end   ([full doc](https://sqlite.org/lang_corefunc.html#substr)).  |
| typeof(x)                 | Return the type of expression `x`                 ([full doc](https://sqlite.org/lang_corefunc.html#typeof)).  |
| upper(x)                  | Convert `x` to upper case                         ([full doc](https://sqlite.org/lang_corefunc.html#upper)).   |


#### SQLite built-in aggregation functions

TO DO


#### General KGTK functions

| Function              | Description                                                                                |
|-----------------------|--------------------------------------------------------------------------------------------|
| kgtk_regex(x, regex)  | Regex matcher that implements the Cypher `=~` semantics which must match the whole string. |
| kgtk_null_to_empty(x) | If `x` is NULL map it onto the empty string, otherwise return `x` unmodified.              |
| kgtk_empty_to_null(x) | If `x` is the empty string, map it onto NULL, otherwise return `x` unmodified.             |

Below we list all functions on the various KGTK literal types.  Note
that all of those can also be invoked via a property syntax, since we
view them as virtual properties on the underlying literal.  For
example, `x.kgtk_lqstring_text` instead of `kgtk_lqstring_text(x)`.


#### Functions on KGTK strings

| Function            | Description                                                  |
|---------------------|--------------------------------------------------------------|
| kgtk_string(x)      | Return True if `x` is a KGTK plain string literal.           |
| kgtk_stringify(x)   | If `x` is not already surrounded by double quotes, add them. |
| kgtk_unstringify(x) | If `x` is surrounded by double quotes, remove them.          |


#### Functions on KGTK language-qualified strings

| Function                     | Description                                                                                     |
|------------------------------|-------------------------------------------------------------------------------------------------|
| kgtk_lqstring(x)             | Return True if `x` is a KGTK language-qualified string literal.                                 |
| kgtk_lqstring_text(x)        | Return the text component of a KGTK language-qualified string literal.                          |
| kgtk_lqstring_text_string(x) | Return the text component of a KGTK language-qualified string literal as a KGTK string literal. |
| kgtk_lqstring_lang(x)        | Return the language component of a KGTK language-qualified string literal. This is the first part not including suffixes such as `en` in `en-us`. |
| kgtk_lqstring_lang_suffix(x) | Return the language+suffix components of a KGTK language-qualified string literal.              |
| kgtk_lqstring_suffix(x)      | Return the suffix component of a KGTK language-qualified string literal. This is the second part if it exists such as `us` in `en-us`, empty otherwise. |


#### Functions on KGTK dates

| Function                 | Description                                                            |
|--------------------------|------------------------------------------------------------------------|
| kgtk_date(x)             | Return True if `x` is a KGTK date literal.                             |
| kgtk_date_date(x)        | Return the date component of a KGTK date literal as a KGTK date.       |
| kgtk_date_time(x)        | Return the time component of a KGTK date literal as a KGTK date.       |
| kgtk_date_and_time(x)    | Return the date+time components of a KGTK date literal as a KGTK date. |
| kgtk_date_year(x)        | Return the year component of a KGTK date literal as an int.            |
| kgtk_date_month(x)       | Return the month component of a KGTK date literal as an int.           |
| kgtk_date_day(x)         | Return the day component of a KGTK date literal as an int.             |
| kgtk_date_hour(x)        | Return the hour component of a KGTK date literal as an int.            |
| kgtk_date_minutes(x)     | Return the minutes component of a KGTK date literal as an int.         |
| kgtk_date_seconds(x)     | Return the seconds component of a KGTK date literal as an int.         |
| kgtk_date_zone(x)        | Return the timezone component of a KGTK date literal.                  |
| kgtk_date_zone_string(x) | Return the time zone component (if any) as a KGTK string.  Zones might look like +10:30, for example, which would be illegal KGTK numbers. |
| kgtk_date_precision(x)   | Return the precision component of a KGTK date literal as an int.       |


#### Functions on KGTK numbers and quantities

| Function                          | Description                                                                      |
|-----------------------------------|----------------------------------------------------------------------------------|
| kgtk_number(x)                    | Return True if `x` is a dimensionless KGTK number literal.                       |
| kgtk_quantity(x)                  | Return True if `x` is a dimensioned KGTK quantity literal.                       |
| kgtk_quantity_numeral(x)          | Return the numeral component of a KGTK quantity literal.                         |
| kgtk_quantity_numeral_string(x)   | Return the numeral component of a KGTK quantity literal as a KGTK string.        |
| kgtk_quantity_number(x)           | Return the number value of a KGTK quantity literal as an int or float.           |
| kgtk_quantity_number_int(x)       | Return the number value of a KGTK quantity literal as an int.                    |
| kgtk_quantity_number_float(x)     | Return the number value component of a KGTK quantity literal as a float.         |
| kgtk_quantity_si_units(x)         | Return the SI-units component of a KGTK quantity literal.                        |
| kgtk_quantity_wd_units(x)         | Return the Wikidata unit node component of a KGTK quantity literal.              |
| kgtk_quantity_tolerance(x)        | Return the full tolerance component of a KGTK quantity literal.                  |
| kgtk_quantity_tolerance_string(x) | Return the full tolerance component of a KGTK quantity literal as a KGTK string. |
| kgtk_quantity_low_tolerance(x)    | Return the low tolerance component of a KGTK quantity literal as a float.        |
| kgtk_quantity_high_tolerance(x)   | Return the high tolerance component of a KGTK quantity literal as a float.       |


#### Functions on KGTK geo coordinates

| Function                | Description                                                                  |
|-------------------------|------------------------------------------------------------------------------|
| kgtk_geo_coords(x)      | Return True if `x` is a KGTK geo coordinates literal.                        |
| kgtk_geo_coords_lat(x)  | Return the latitude component of a KGTK geo coordinates literal as a float.  |
| kgtk_geo_coords_long(x) | Return the longitude component of a KGTK geo coordinates literal as a float. |


<A NAME="differences-to-cypher"></A>
### Important differences to Cypher

* Kypher does not use a property graph data model
* supports querying across multiple graphs
* no graph update commands
* single match clause only
* no (transitive) path range patterns which would be expensive to implement in SQL
* no relationship isomorphism
* no dynamic properties such as `x[fn(y)]`
* lists can only contain literals
* Python regexps instead of Java regexps
* different set of built-in functions

Features that are currently missing but might become available in future versions:

* optional match
* `exists` subqueries
* `with` clause variable bindings
* `union` queries
* patterns with undirected edges


## Tips and tricks

### Adding a column

```
kgtk query -i $GRAPH --return '*, "^20200202" as date'
```

### Reusing cache space

```
kgtk query -i file1 --as data --return '*, "^20200202" as date'
kgtk query -i file2 --as data --return '*, "^20200202" as date'
```


## Advanced topics

### Indexing and query performance

Proper indexing of KGTK graph file columns is important for good query
performance on large files.  Appropriate indexes are created
automatically as needed before a query is run.  However, sometimes
more fine-grained control of index generation is needed which can be
achieved with the `--index [MODE]` option (experts only).  Mode can
be one of `auto` (the default), `expert`, `quad`, `triple`, `node1+label`,
`node1`, `label`, `node2` and `none`.

#### Sorting the data before querying

Knowledge graphs encoded in KGTK files are schema-free tables with often
highly skewed data statistics that violate many assumptions commonly made
by relational database systems such as SQLite.  This can become a problem
with certain types of queries over large Wikidata-style datasets with
O(1B) edges.  In such datasets certain types of edges might have O(1M)
occurrences (e.g., the `P31` instance-of relation), while others only
occur a few times.

If a dataset is sorted by `node1`, such high-frequency edges will be
spread out throughout the corresponding data table, making a query for
all such edges scan a large number of the underlying data pages, even
if a label index is available.  The reason is that each page will
generally only hold a few of the edges sought, while a lot of other
data is read purely because data is read from disk in large blocks.
Sorting a dataset appropriately before importing, for example by the
`label` column, can vastly improve locality and query performance in
such cases.  For example, the following command would sort a Wikidata
claims file (we use some extra Unix-sort options to facilitate sorting
of very large files):

```
kgtk sort -i claims.tsv.gz -c label \
     -X "-T /data/tmp/ --parallel 8 --buffer-size 60%" \
     -o claims.sorted.tsv.gz
```

Of course, sorting by one column will damage locality of another such
as `node1`.  In a Wikidata-style dataset, however, `node1` skew is
generally much less than `label` skew, so `node1` queries will be less
affected by this resorting.  In the end what is the best strategy is
an experimental question that will vary from dataset to dataset and
use case.

Another thing to consider for very large datasets is to split them
into separate files with different sets of edge labels.  This will
keep data tables smaller, improve locality, but for the cost of some
extra query complexity due to the multiple data files.


### Explanation

Before a query is executed the database will produce an optimized query
plan based on available indexes and known statistics of the data.  Before
running potentially expensive queries on large datasets, or when query
times are unexpectedly long, it can be useful to look at these query plans
to see if they behave as expected and have and use all the appropriate
indexes.

To see the query plan the option `--explain [MODE]` can be used, which
accepts one of `plan` (the default), `full` or `expert` as its mode argument.
If `--explain` is used, the query is actually not run and only the requested
explanation will be printed.


### Debugging

Similar to other KGTK commands, `query` accepts the `--debug` and `--expert`
options.  `--debug` can be particularly useful to see the actual SQL query
that gets generated as well as to get log and timing information about data
import and index creation.

For example, here we can see how built-in functions are called directly in
the generated SQL:

```
kgtk --debug query -i $GRAPH \
     --match '(p)-[r:name]->(n)' \
     --where 'n.kgtk_lqstring_lang = "de"'
[2020-10-16 13:37:16 query]: SQL Translation:
---------------------------------------------
  SELECT *
     FROM graph_2 AS graph_2_c1
     WHERE graph_2_c1."label"=?
     AND (kgtk_lqstring_lang(graph_2_c1."node2") = ?)
  PARAS: ['name', 'de']
---------------------------------------------
```
Result:

|  id   |  node1  |  label  |  node2      |
|-------|---------|---------|-------------|
|  e21  |  Hans   |  name   |  'Hans'@de  |
|  e22  |  Otto   |  name   |  'Otto'@de  |


<A NAME="time-machine-use-case"></A>
### Querying based on edge qualifiers

Here we present a slightly more complex query example we call the
"Wikidata time machine use case" which was one of the initial
motivating examples for our work on Kypher.  The time machine use case
tries to select a subset of Wikidata statements that only include
those that contain information known up to a particular time cutoff,
say the year 2000.  For example, it shouldn't include any people that
were born after that time, or that took on a role (say become
president of a country) after that time, etc.  This is generally a
difficult problem, since temporal qualification in Wikidata is very
incomplete, but we won't concern ourselves with all these issues here.

Our basic approach is that we use the data in the `$WORKS` graph we
encountered before, and that we add an additional `$QUALS` graph with
start and end time qualifiers for the statements in `$WORKS`.  In
addition, we have a third graph `$PROPS` that defines the set of
qualifier properties we are interested in.  In this simple example,
they are just `starts` and `ends`.  With that in mind, the query
proceeds in the following steps:

1. look for base edges in the `$WORKS` graph
2. link to qualifiers in the `$QUALS` graph via edge id `r`
3. restrict the qualifiers based on edge labels
   `ql` that are listed in the `$PROPS` graph
4. restrict to edges that have a start or end time with year of at most 2000
5. output the qualifying base edges with their temporal annotations

First let us list the qualifier data and temporal properties used below:

```
QUALS=examples/docs/query-quals.tsv

kgtk query -i $QUALS
```
Result:

|    id   |  node1  |  label   |  node2                     |  graph  |
|---------|---------|----------|----------------------------|---------|
|    m11  |  w11    |  starts  |  ^1984-12-17T00:03:12Z/11  |  quals  |
|    m12  |  w12    |  ends    |  ^1987-11-08T04:56:34Z/10  |  quals  |
|    m13  |  w13    |  starts  |  ^1996-02-23T08:02:56Z/09  |  quals  |
|    m14  |  w14    |  ends    |  ^2001-04-09T06:16:27Z/08  |  quals  |
|    m15  |  w15    |  starts  |  ^2008-10-01T12:49:18Z/07  |  quals  |


```
PROPS=examples/docs/query-props.tsv

kgtk query -i $PROPS
```
Result:

|    id   |  node1   |  label   |  node2  |  graph  |
|---------|----------|----------|---------|---------|
|    p11  |  starts  |  member  |  set1   |  props  |
|    p12  |  ends    |  member  |  set1   |  props  |

Finally, here is the time machine query.  Note that `kgtk_date_year`
returns an integer value, so there is no need to cast the value to an
integer first for proper comparison.  The crucial bit here is how we
use the `id` of the base edge `r` as the `node1` of the qualifier edge
`q` whose label `ql` has to be one of the properties listed in
`$PROPS`:

```
kgtk query -i $WORKS -i $QUALS -i $PROPS  \
     --match "work: (x)-[r {label: rl}]->(y),  \
            qual: (r)-[q {label: ql}]->(time), \
            prop: (ql)-[:member]->(:set1)" \
     --where "time.kgtk_date_year <= 2000" \
     --return "r as id, x, rl, y, ql as trel, time as time"
```
Result:

|    id   |  node1  |  label  |  node2   |  trel    |  time                     |
|---------|---------|---------|----------|----------|---------------------------|
|    w11  |  Hans   |  works  |  ACME    |  starts  |  ^1984-12-17T00:03:12Z/11 |
|    w13  |  Joe    |  works  |  Kaiser  |  starts  |  ^1996-02-23T08:02:56Z/09 |
|    w12  |  Otto   |  works  |  Kaiser  |  ends    |  ^1987-11-08T04:56:34Z/10 |
