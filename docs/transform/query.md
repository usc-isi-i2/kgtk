Query a KGTK file with the Kypher query language (a variant of [Cypher](https://neo4j.com/developer/cypher/))
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
them on a very lightweight file-based SQL database such as SQLite.  Kypher queries are designed to look and feel very similar to other
file-based KGTK commands.  They take tabular file data as input and
produce tabular data as output.  There are no servers and accounts to set up, and the user does not need to know that there is in fact a
database used underneath to implement the queries.  A cache mechanism makes multiple queries over the same KGTK files very efficient.  Kypher has been successfully tested on Wikidata-scale graphs with 1.5B edges and larger where queries executing on a standard laptop run in
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
to protect it from interpretation by the shell. The result of the queries are shown in tables to facilitate readibility:

```
 > DATA_HOME=kgtk/tests/data/kypher
 > GRAPH=$DATA_HOME/graph.tsv
    
 > kgtk query -i $GRAPH --match '()-[]->()'
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
> kgtk query -i $GRAPH --match '()'
```

That pattern is also the default for `--match`, so the following query
is again equivalent to the above and produces the same as running
`cat` on the file:

```
> kgtk query -i $GRAPH
```

Especially on larger data, it is always a good idea to restrict a query to a small result set first to see if the returned result is the one expected.
This can be done by using `--limit N` so that at most `N` result rows
will be produced (not counting the header line):

```
> kgtk query -i $GRAPH --limit 3
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
> kgtk query -i $GRAPH --skip 2 --limit 3
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
> kgtk query -i $GRAPH | tail +3 | head -3
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
> kgtk query -i $GRAPH --match '(:Hans)-[]->()'
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
> kgtk query -i $GRAPH --match '()-[:name]->()'
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
 > kgtk query -i $GRAPH --match '(:Otto)-[:name]->()'
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
> kgtk query -i $GRAPH \
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
 > kgtk query -i $GRAPH \
    --match '(p:Otto)-[:name]->()' \
    --where 'p = "Otto"'
```

Note that constants such as `Otto` need to be quoted when used in the `--where`
clause very similar to SQL.  This needs to be handled carefully, since we have
to make sure that the quotes will not be ignored by the Unix shell (see
[REF <b>Quoting</b>] for more details).

Next is an example using a regular expression to filter on the names attached to
nodes.  The Kypher `=~` operator matches a value against a regular expression.
Note that Kypher regular expressions use Python regexp syntax, which is different
from the Java regexps used in Cypher.  In the query below we select all `name`
edges that lead to a name that contains a double letter:

```
> kgtk query -i $GRAPH \
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
> kgtk query -i $GRAPH \
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
(see [ref <b>Built-in Functions</b>] for more details):

```
> kgtk query -i $GRAPH \
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
> kgtk query -i $GRAPH \
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
> kgtk query -i $GRAPH \
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
> kgtk query -i $GRAPH \
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
an extra column named `time`.  See [ref <b>Edges and properties</b>]
for more details.  Below is the query which now does produce
valid KGTK as output (the order of columns does not matter):

```
> kgtk query -i $GRAPH \
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
We can do this with the following query where we use the `distict`
keyword in the `--return` clause to eliminate any duplicates:

```
> kgtk query -i $GRAPH \
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
> kgtk query -i $GRAPH \
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
> kgtk query -i $GRAPH \
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
are documented in more detail here [ref <b>Built-in Functions</b>].
Note below how the language-qualified string `'Otto'@de` stays
unchanged, since `kgtk_unstringify` only modifies values that are in
fact string literals.  Again we use aliases to produce valid KGTK
column names:

```
> kgtk query -i $GRAPH \
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
Kypher - see [ref <b>Quoting</b>] for more details).

```
> kgtk query -i $GRAPH \
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
> kgtk query -i $GRAPH \
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
> kgtk query -i $GRAPH \
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
> kgtk query -i $GRAPH \
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
> kgtk query -i $GRAPH \
    --match '(na)<-[:name]-()-[r:loves]->()-[:name]->(nb)' \
    --where 'na.kgtk_lqstring_lang = "de" OR nb.kgtk_lqstring_lang = "de"' \
    --return 'r, na as node1, r.label, nb as node2'
```
Result:

|     id  | node1     | label | node2   |
| ------- | --------- | ----- | ------- |
|     e11 | 'Hans'@de | loves | "Molly" |
|     e12 | 'Otto'@de | loves | "Susi"  |


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
> WORKS=$DATA_HOME/works.tsv

> kgtk query -i $WORKS --match '()-[]->()' 
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
See [ref <b>Input and output specifications</b>] on more details of this
process.  A simple way of referring to files as graphs is by the initial
character of their file name (as long as they differ), which is what we
do here.  `g` matches the `graphs.tsv` file and `w` matches `works.tsv`.

Finally we can run the query.  Note that multiple edges in the match pattern
are represented by separate pattern elements that are conjoined by commas.
The variable `y` is what joins the edges across graphs.  So, naturally,
this query will only work if bindings found for `y` in graph `g` also
exist as `node1`s in graph `w`:

```
> kgtk query -i $GRAPH -i $WORKS \
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
> kgtk query -i $GRAPH -i $WORKS \
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
> kgtk query -i $GRAPH -i $WORKS \
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
> kgtk query -i $GRAPH -i $WORKS \
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
> kgtk query -i $GRAPH -i $WORKS \
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
as `count`, `min`, `max`, `avg`, etc.  The simplest aggregation
operation involves counting rows or values via the `count` function.
For example, we might want to know how many edges have Joe as the
starting node:

```
> kgtk query -i $GRAPH \
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
> kgtk query -i $GRAPH \
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
> kgtk query -i $GRAPH \
     --match '(:Joe)-[r]->()' \
     --return 'count(distinct r.label) as N'
```
Result:

| N    |
| ---- |
|    3 |

Different than SQL, however, Kypher does not have an explicit
`group-by` clause and infers proper grouping from clause type and
order in the `return` statement.  Grouping refers to the process of
sorting result rows into groups before an aggregation operation is
applied to each group.  In the count queries above, there was only a
single group containing the full result set.  In the next query we are
grouping by relationship label and then select the maximum `node2`
value for each label group (here `max` is interpreted lexicographically).

```
> kgtk query -i $GRAPH \
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
> kgtk query -i $WORKS \
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
> kgtk query -i $WORKS \
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


<b>================= REVISED UP TO HERE =================</b>


## Input and output specifications

* to join across multiple graphs, match clauses do need to be associated
  with the graph (file) they should be matched against.
* this is done with the following extension to the Cypher syntax, for example:
     `g: (x)-[:loves]->(y)`
  where a variable followed by a colon immediately preceding a match clause
  is interpreted as a graph variable or handle
* graph variables are (currently) associated with files through a simple greedy
  match process.  For example, `g` is matched with the first input file whose
  basename contains a `g`.  Once a file has been matched to a handle, it is
  removed as a candidate for subsequent handle matches.  So, for example, if
  our next handle were `r` it would be matched to `$WORKS` even though `$GRAPH`
  also contains an `r`.  For exact matches, full filenames can be used.
  Finally, handles ending in a number such as `g12` are first matched in full
  and then tried with the prefix only (`g` in this case).  This allows us to
  easily match to files `graph1.tsv` and `graph2.tsv` with handles `g1` and `g2`.
* future versions of the query command might have some dedicated syntax to
  associate input files with their graph handles
* clauses not directly preceded by a graph variable inherit it from the
  previous clause
* if the first clause does not have a graph handle, it gets matched to the
  first input file


## Graph cache

## Edges and properties

TO DO: Needs to describe edge as well as node properties and how they
related to extra columns.


## Kypher query clauses

## Quoting

Usin string literals in queries can be very tricky.  For example, if
if we want to restrict on a string literal, the double quotes are part
of the content.  Unfortunately, there are actually three levels of
quoting that interact:

1. quoting of a KGTK literal such as "Hans" or 'Deutsch'@de which is part of a field's value
2. quoting of literal restrictions in the query language, e.g., a Kypher literal must be
   enclosed in single or double quotes to be recognized as a literal
3. quote processing by the Unix shell which affects how quotes are passed through to
   the query engine

How can it be done:

* We'd like to say  `...WHERE x='"Hans"'...`  but that becomes challenging in a shell
  environment which interprets those quotes
* Here is an incantation that works in `bash` where we use double quotes for
  the whole restriction and then escape them inside: `--where "x = '\"Joe\"' AND..."`
* But the solution looks much worse in `tcsh`: `--where 'x = '"'"'"Joe"'"'"' AND...'`

<pre>
    > kgtk query -i $GRAPH \
         --match '()-[:name]->(n)' \
         --where " n = '\"Joe\"' "
    id	node1	label	node2
    e23	Joe	name	"Joe"
</pre>

Here is a better way that uses Kypher parameters which are dollar variables inside the
query string which will be replaced with values passed in via query parameters:

*  `--para` uses the string as is, `--spara` string-quotes it, `--lqpara` lq-string-quotes it
*  this might still require shell quoting (e.g., for spaces, etc.), but only one level
* in the query below we pass in a language-qualified string once with explicit quoting
  using --para and once without quoting using --lqpara where KGTK will handle quoting for us
* NOTE: since the `$`-character is also interpreted by the Unix shell, query strings containing
  parameters need to be in single quotes, or the dollar sign needs to be escaped, for example,
  by using `\$` in bash

<pre><i>
    > kgtk --debug query -i $GRAPH \
             --match '()-[:name]->(n)' \
             --where ' n = $name OR n = $name2 OR n = $name3 ' \
             --para name="'Hans'@de" --spara name2=Susi --lqpara name3=Otto@de
</i>    [2020-10-16 13:37:15 query]: SQL Translation:
    ---------------------------------------------
      SELECT *
         FROM graph_2 AS graph_2_c1
         WHERE graph_2_c1."label"=?
         AND ((graph_2_c1."node2" = ?) OR ((graph_2_c1."node2" = ?) OR (graph_2_c1."node2" = ?)))
      PARAS: ['name', "'Hans'@de", '"Susi"', "'Otto'@de"]
    ---------------------------------------------
    id	node1	label	node2
    e21	Hans	name	'Hans'@de
    e22	Otto	name	'Otto'@de
    e25	Susi	name	"Susi"
</pre>


## Strings, numbers and literals

## Null values

## Regular expressions

## Tips and tricks

## Built-in Functions

## Important differences to Cypher


## Advanced topics

### Indexing and query performance

### Explanation

### Debugging

Built-in functions are called directly by SQL engine (`--debug` raises
the log level to 1, `--debug` + `--expert` raises it to 2):

<pre><i>
    > kgtk --debug query -i $GRAPH \
         --match '(p)-[r:name]->(n)' \
         --where 'n.kgtk_lqstring_lang = "de"'
</i>    [2020-10-16 13:37:16 query]: SQL Translation:
    ---------------------------------------------
      SELECT *
         FROM graph_2 AS graph_2_c1
         WHERE graph_2_c1."label"=?
         AND (kgtk_lqstring_lang(graph_2_c1."node2") = ?)
      PARAS: ['name', 'de']
    ---------------------------------------------
    id	node1	label	node2
    e21	Hans	name	'Hans'@de
    e22	Otto	name	'Otto'@de
</pre>


### Wikidata time machine use case

This is the full three-graph example, but it also exhibits a difficulty with
property translation.  We'd like to say `--return "r, x, r.label, y"`, but
`r.label` means something different in graph `work` (an edge property) than it
does in `qual` (a node property).  So we have to introduce an additional label
variable `rl` for now.  With that the query proceeds in the following steps:

* first look for the base relation in the `WORKS` graph
* then link to qualifiers in the `QUALS` graph via relation id `r`
* we then further restrict the qualifiers based on relation labels
  `p` that are listed in the `PROPS` graph
* we then restrict relations that have a time with year of at most 2000
* we then output the base relation with temporal annotations

NOTE: here we do not have to cast to integer, since `kgtk_date_year` does the
type conversion for us

TO DO: investigate/eliminate some redundant conditions in the SQL translations below

Qualifier data and temporal properties used below:

<pre><i>
    > kgtk query -i $QUALS
</i>    id	node1	label	node2	graph
    m11	w11	starts	^1984-12-17T00:03:12Z/11	quals
    m12	w12	ends	^1987-11-08T04:56:34Z/10	quals
    m13	w13	starts	^1996-02-23T08:02:56Z/09	quals
    m14	w14	ends	^2001-04-09T06:16:27Z/08	quals
    m15	w15	starts	^2008-10-01T12:49:18Z/07	quals
</pre>

<pre><i>
    > kgtk query -i $PROPS
</i>    id	node1	label	node2	graph
    p11	starts	member	set1	props
    p12	ends	member	set1	props
</pre>

<pre><i>
    > kgtk --debug query -i $WORKS -i $QUALS -i $PROPS  \
         --match "work: (x)-[r {label: rl}]->(y),  \
                  qual: (r)-[rp {label: p}]->(time), \
                  prop: (p)-[:member]->(:set1)" \
         --where "time.kgtk_date_year <= 2000" \
         --return "r as id, x, rl, y, p as trel, time as time"
</i>    [2020-10-16 13:37:20 query]: SQL Translation:
    ---------------------------------------------
      SELECT graph_1_c2."node1" "id", graph_3_c1."node1", graph_3_c1."label", graph_3_c1."node2", graph_4_c3."node1" "trel", graph_1_c2."node2" "time"
         FROM graph_1 AS graph_1_c2, graph_3 AS graph_3_c1, graph_4 AS graph_4_c3
         WHERE graph_1_c2."label"=graph_4_c3."node1"
         AND graph_3_c1."label"=graph_3_c1."label"
         AND graph_4_c3."label"=?
         AND graph_4_c3."node2"=?
         AND graph_1_c2."label"=graph_4_c3."node1"
         AND graph_1_c2."node1"=graph_3_c1."id"
         AND (kgtk_date_year(graph_1_c2."node2") <= ?)
      PARAS: ['member', 'set1', 2000]
    ---------------------------------------------
    [2020-10-16 13:37:20 sqlstore]: CREATE INDEX on table graph_4 column label ...
    [2020-10-16 13:37:20 sqlstore]: ANALYZE INDEX on table graph_4 column label ...
    [2020-10-16 13:37:20 sqlstore]: CREATE INDEX on table graph_1 column label ...
    [2020-10-16 13:37:20 sqlstore]: ANALYZE INDEX on table graph_1 column label ...
    [2020-10-16 13:37:20 sqlstore]: CREATE INDEX on table graph_4 column node2 ...
    [2020-10-16 13:37:21 sqlstore]: ANALYZE INDEX on table graph_4 column node2 ...
    [2020-10-16 13:37:21 sqlstore]: CREATE INDEX on table graph_1 column node1 ...
    [2020-10-16 13:37:21 sqlstore]: ANALYZE INDEX on table graph_1 column node1 ...
    [2020-10-16 13:37:21 sqlstore]: CREATE INDEX on table graph_4 column node1 ...
    [2020-10-16 13:37:21 sqlstore]: ANALYZE INDEX on table graph_4 column node1 ...
    [2020-10-16 13:37:21 sqlstore]: CREATE INDEX on table graph_3 column id ...
    [2020-10-16 13:37:21 sqlstore]: ANALYZE INDEX on table graph_3 column id ...
    id	node1	label	node2	trel	time
    w11	Hans	works	ACME	starts	^1984-12-17T00:03:12Z/11
    w13	Joe	works	Kaiser	starts	^1996-02-23T08:02:56Z/09
    w12	Otto	works	Kaiser	ends	^1987-11-08T04:56:34Z/10
</pre>

Slightly simpler alternative that uses property enumeration via a list:

<pre><i>
    > kgtk --debug query -i $WORKS -i $QUALS  \
         --match "work: (x)-[r {label: rl}]->(y),  \
                  qual: (r)-[rp {label: p}]->(time)" \
         --where "p in ['starts', 'ends'] and time.kgtk_date_year <= 2000" \
         --return "r as id, x, rl, y, p as trel, time as time"
</i>    [2020-10-16 13:37:21 query]: SQL Translation:
    ---------------------------------------------
      SELECT graph_3_c1."id" "id", graph_3_c1."node1", graph_3_c1."label", graph_3_c1."node2", graph_1_c2."label" "trel", graph_1_c2."node2" "time"
         FROM graph_1 AS graph_1_c2, graph_3 AS graph_3_c1
         WHERE graph_1_c2."label"=graph_1_c2."label"
         AND graph_3_c1."label"=graph_3_c1."label"
         AND graph_1_c2."node1"=graph_3_c1."id"
         AND ((graph_1_c2."label" IN (?, ?)) AND (kgtk_date_year(graph_1_c2."node2") <= ?))
      PARAS: ['starts', 'ends', 2000]
    ---------------------------------------------
    id	node1	label	node2	trel	time
    w11	Hans	works	ACME	starts	^1984-12-17T00:03:12Z/11
    w12	Otto	works	Kaiser	ends	^1987-11-08T04:56:34Z/10
    w13	Joe	works	Kaiser	starts	^1996-02-23T08:02:56Z/09
</pre>

Yet another variant with regex selection and sorting:

<pre><i>
    > kgtk --debug query -i $WORKS -i $QUALS  \
         --match "work: (x)-[r {label: rl}]->(y),  \
                  qual: (r)-[rp {label: p}]->(time)" \
         --where "p =~ 's.*' and time.kgtk_date_year <= 2000" \
         --return "r as id, x, rl, y, p as trel, time as time" \
         --order-by "p desc, time asc"
</i>    [2020-10-16 13:37:21 query]: SQL Translation:
    ---------------------------------------------
      SELECT graph_1_c2."node1" "id", graph_3_c1."node1", graph_3_c1."label", graph_3_c1."node2", graph_1_c2."label" "trel", graph_1_c2."node2" "time"
         FROM graph_1 AS graph_1_c2, graph_3 AS graph_3_c1
         WHERE graph_1_c2."label"=graph_1_c2."label"
         AND graph_3_c1."label"=graph_3_c1."label"
         AND graph_1_c2."node1"=graph_3_c1."id"
         AND (KGTK_REGEX(graph_1_c2."label", ?) AND (kgtk_date_year(graph_1_c2."node2") <= ?))
         ORDER BY graph_1_c2."label" DESC, graph_1_c2."node2" ASC
      PARAS: ['s.*', 2000]
    ---------------------------------------------
    id	node1	label	node2	trel	time
    w11	Hans	works	ACME	starts	^1984-12-17T00:03:12Z/11
    w13	Joe	works	Kaiser	starts	^1996-02-23T08:02:56Z/09
</pre>
