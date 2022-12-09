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


## Usage
```
usage: kgtk query [-h] [-i INPUT_FILE [INPUT_FILE ...]] [--as NAME]
                  [--comment COMMENT] [-a FILE [FILE ...]] [--query QUERY]
                  [--match PATTERN] [--where CLAUSE] [--opt PATTERN]
                  [--with CLAUSE] [--where: CLAUSE] [--return CLAUSE]
                  [--order-by CLAUSE] [--skip CLAUSE] [--limit CLAUSE]
                  [--multi N] [--para NAME=VAL] [--spara NAME=VAL]
                  [--lqpara NAME=VAL] [--no-header] [--force]
                  [--dont-optimize] [--index MODE [MODE ...]]
                  [--idx SPEC [SPEC ...]] [--explain [MODE]]
                  [--graph-cache DBFILE] [--show-cache]
                  [--aux-cache DBFILE [DBFILE ...]] [--read-only]
                  [--single-user] [--import MODULE_LIST] [-o OUTPUT]

Query one or more KGTK files with Kypher.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE [INPUT_FILE ...], --input-files INPUT_FILE [INPUT_FILE ...]
                        One or more input files to query, maybe compressed
                        (May be omitted or '-' for stdin.)
  --as NAME             alias name to be used for preceding input
  --comment COMMENT     comment string to store for the preceding input
                        (displayed by --show-cache)
  -a FILE [FILE ...], --append FILE [FILE ...]
                        additional data file(s) to append to the specified
                        input
  --query QUERY         complete Kypher query combining all clauses, if
                        supplied, all other specialized clause arguments will
                        be ignored
  --match PATTERN       MATCH pattern of a Kypher query, defaults to universal
                        node pattern `()'
  --where CLAUSE        WHERE clause to a preceding --match, --opt or --with
                        clause
  --opt PATTERN, --optional PATTERN
                        OPTIONAL MATCH pattern(s) of a Kypher query (zero or
                        more)
  --with CLAUSE         WITH clause of a Kypher query (only 'WITH * ...' is
                        currently supported)
  --where: CLAUSE       final global WHERE clause, shorthand for 'WITH * WHERE
                        ...'
  --return CLAUSE       RETURN clause of a Kypher query (defaults to *)
  --order-by CLAUSE     ORDER BY clause of a Kypher query
  --skip CLAUSE         SKIP clause of a Kypher query
  --limit CLAUSE        LIMIT clause of a Kypher query
  --multi N             split each result into N separate edges or output rows
                        of equal number of columns
  --para NAME=VAL       zero or more named value parameters to be passed to
                        the query
  --spara NAME=VAL      zero or more named string parameters to be passed to
                        the query
  --lqpara NAME=VAL     zero or more named LQ-string parameters to be passed
                        to the query
  --no-header           do not generate a header row with column names
  --force               force problematic queries to run against advice
  --dont-optimize       disable query optimizer and process match clause joins
                        in the order listed
  --index MODE [MODE ...], --index-mode MODE [MODE ...]
                        default index creation MODE for all inputs (default:
                        auto); can be overridden with --idx for specific
                        inputs
  --idx SPEC [SPEC ...], --input-index SPEC [SPEC ...]
                        create index(es) according to SPEC for the preceding
                        input only
  --explain [MODE]      explain the query execution and indexing plan
                        according to MODE (plan, full, expert, default: plan).
                        This will not actually run or create anything.
  --graph-cache DBFILE, --gc DBFILE
                        database cache where graphs will be imported before
                        they are queried (defaults to per-user temporary file)
  --show-cache, --sc    describe the current content of the graph cache and
                        exit (does not actually run a query or import data)
  --aux-cache DBFILE [DBFILE ...], --ac DBFILE [DBFILE ...]
                        auxiliary read-only database file(s) to use for cross-
                        graph-cache queries
  --read-only, --ro     do not create or update the graph cache in any way,
                        only run queries against already imported and indexed
                        data
  --single-user         single-user mode blocks concurrent database access
                        from parallel processes for faster data import
  --import MODULE_LIST  Python modules needed to define user extensions to
                        built-in functions
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

* `not/exists` pattern handling
    * if needed can be emulated via query pipelines
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
[**Quoting**](#quoting) for more details).

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
(see [**Built-in functions**](#built-in-functions) for more details):

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
an extra column named `time`.  See [**Edges and properties**](#properties)
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
are documented in more detail here: [**Built-in functions**](#built-in-functions).
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
Kypher - see [**Quoting**](#quoting) for more details).

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
such as the `$PROPS` graph used in [**this example**](#time-machine-use-case).


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
See [**Input and output specifications**](#input-output) on more details of this
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
(see [**Built-in functions**](#built-in-functions)).  The simplest
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


### EXISTS conditions

The pattern in a `--match` clause generates **all** matches that can
be found for it in the data.  The `EXISTS` operator tests for the
existence of a **single** match of a pattern.  This is useful if we
only need to know that such a pattern exists, but we don't care about
the specific values in the data that make the pattern true.  It is
also much more efficient for cases where a pattern has many matches,
and it avoids the cross-product blowup we would get if we tested for
this pattern directly in a `--match` clause.

`EXISTS` conditions are Boolean expressions that can occur anywhere
in a query where an expression is legal (such as in a `--where` clause,
`--return` clause, etc.).  They come in three separate forms (note
that the case of keywords such as `EXISTS` or `WHERE` is insignificant):

* Explicit exists: `EXISTS {<pattern>+ [WHERE <condition>]}`
* Exists function: `EXISTS(<pattern>)`
* Implicit exists: `<pattern>`

Explicit exists conditions are the most general and powerful.  They
specify a bona fide *subquery* that returns true as soon as one
solution to it was generated.  Explicit exists conditions can
introduce new variables that do not exist outside of the subquery (and
reference to them will raise an error).  Most commonly, exists
conditions will reference variables from outside their scope and then
execute for each set of bindings generated by the outer query.
Explicit conditions allow the same pattern language and comma
operators as can be used in a `--match` clause.  This is more general
than the corresponding semantics in Cypher.

The `EXISTS` function and implicit exists conditions are more concise
but also more restrictive.  They only allow the use of a single
connected pattern that can be expressed without any commas, and they
also do not allow the introduction of any new named variables
(anonymous nodes or edges are OK).  These restrictions are following
the semantics in Cypher.  A pattern can be viewed as denoting the list
of edges or paths it generates.  If this list is non-empty, the
pattern evaluates to true, otherwise its value in a condition is
false.  The `EXISTS` function is really only *syntactic sugar* to
emphasize the use of a pattern expression as an exists condition,
otherwise its behavior is identical.

The rationale behind the more restrictive semantics for implicit
exists conditions is that they should be testable with a simple
pattern match on the graph instead of a full subquery.  However,
in our Kypher implementation both implicit and explicit exists
are translated into the same kinds of SQL subqueries.

Let us illustrate these cases with some examples.  We start by
retrieving "people who are loved" by enumerating people and their
names in the `--match` clause and then for each of them test for the
existence of a `loves` edge leading to them using an explicit exists
condition:

```
kgtk query -i $GRAPH \
     --match '(x)-[:name]->(n)' \
     --where 'EXISTS {()-[:loves]->(x)}' \
     --return 'x, n'
```
Result:

| node1 | node2   |
|-------|---------|
| Joe   | "Joe"   |
| Molly | "Molly" |
| Susi  | "Susi"  |


The previous query did not really exercise the full power of an
explicit exists condition.  So let us retrieve "people who are loved
and rich" which requires more machinery.  We enumerate people in
`GRAPH` as before, check for the existence of a `loves` edge as
before, but now we additionally look for a salary specified in
the `WORKS` graph using a comma and second pattern qualified
with the other graph.  Finally we use the `WHERE` clause of the
exists condition to test for a minimum salary:

```
kgtk query -i $GRAPH -i $WORKS \
     --match '(x)-[:name]->(n)' \
     --where 'EXISTS {()-[:loves]->(x), w: (x {salary: s})-[:works]->() \
                      WHERE cast(s, int) >= 10000}' \
     --return 'x, n'
```
Result:

| node1 | node2   |
|-------|---------|
| Joe   | "Joe"   |
| Molly | "Molly" |


The first example above can be rephrased with an `EXISTS` function
expression giving the same result:

```
kgtk query -i $GRAPH \
     --match '(x)-[:name]->(n)' \
     --where 'EXISTS(()-[:loves]->(x))' \
     --return 'x, n'
```
Result:

| node1 | node2   |
|-------|---------|
| Joe   | "Joe"   |
| Molly | "Molly" |
| Susi  | "Susi"  |

Or it can be rephrased even more concisely as a simple pattern expression:

```
kgtk query -i $GRAPH \
     --match '(x)-[:name]->(n)' \
     --where '()-[:loves]->(x)' \
     --return 'x, n'
```
Result:

| node1 | node2   |
|-------|---------|
| Joe   | "Joe"   |
| Molly | "Molly" |
| Susi  | "Susi"  |


Exists condition can occur anywhere an expression is legal.
For example, here we combine two implicit exists conditions
in a `--return` clause:

```
kgtk query -i $GRAPH \
     --match '(x)-[:name]->(n)' \
     --return 'x, n, ()-[:loves]->(x) or ()-[:friend]->(x) as happy'
```
Result:

| node1 | node2     | happy |
|-------|-----------|-------|
| Hans  | 'Hans'@de | 0     |
| Otto  | 'Otto'@de | 1     |
| Joe   | "Joe"     | 1     |
| Molly | "Molly"   | 1     |
| Susi  | "Susi"    | 1     |


Implicit exists conditions and the `EXISTS` function can take more
complex patterns as arguments, as long as they can be expressed with
a single chain.  For example:

```
kgtk query -i $GRAPH \
     --match '(x)-[:name]->(n)' \
     --where '()-[:loves]->(x)-[:friend]->()' \
     --return 'x, n'
```
Result:

| node1 | node2 |
|-------|-------|
| Joe   | "Joe" |


Adding a new variable, however, will trigger an error:

```
kgtk query -i $GRAPH \
     --match '(x)-[:name]->(n)' \
     --where '()-[:loves]->(x)-[:friend]->(f)' \
     --return 'x, n'
Need explicit 'EXISTS' subquery to introduce new pattern variables
```

Finally, since exists conditions are expressions, they can be nested
around other explicit or implicit exists conditions.  For example,
here we again look for people that are loved, but that are missing
certain end date qualifiers on their `works` edges:

```
QUALS=examples/docs/query-quals.tsv

kgtk query -i $GRAPH -i $WORKS -i $QUALS \
     --match '(x)-[:name]->(n)' \
     --where 'EXISTS {()-[:loves]->(x), \
                      w: (x)-[wr:works]->() \
                      WHERE NOT EXISTS {q: (wr)-[:ends]->(e) \
                                        WHERE e < "^2000"}}' \
     --return 'x, n'
```
Result:

| node1 | node2   |
|-------|---------|
| Joe   | "Joe"   |
| Molly | "Molly" |
| Susi  | "Susi"  |


### Optional match

Kypher also supports Cypher's optional match patterns which are useful
to retrieve sparse or incomplete edges and attributes that are common
in real-world knowledge graphs.  Optional patterns are allowed to fail
which will generate NULL values for their respective pattern variables
in such cases instead of making the whole pattern fail.  Optional
patterns are similar to SQL's left joins.

Each Kypher query must have exactly one strict `--match` clause and
can have zero or more optional match clauses introduced by `--opt`.
This is somewhat more restrictive than Cypher which can have any
number of strict and/or optional patterns in any order, but that
should generally not matter in practice.  Each strict and optional
match clause can have its own `--where` clause, so the `query` command
associates each `--where` clause with the (closest) match clause
preceding it.  For optional match clauses the order matters, since
there can be optionals on optionals, which is an important concept to
keep in mind.  The required strict match clause is always interpreted
as the first match clause in the query, regardless of where it is
specified on the command line.  Let us illustrate these concepts with
some examples.

In some of the examples below we use the following edge qualifier
data, which adds start and end times to some of the edges in the
`$WORKS` graph:

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


To illustrate the usefulness of optional patters, let us start with a
strict query first that retrieves company employees, their names and
start dates:

```
kgtk query -i $GRAPH -i $WORKS -i $QUALS \
     --match  'w: (p)-[r:works]->(c), g: (p)-[:name]->(n), q: (r)-[:starts]->(s)' \
     --return 'c as company, p as employee, n as name, s as start'
```
Result:

| company | employee | name      | start                    |
|---------|----------|-----------|--------------------------|
| ACME    | Hans     | 'Hans'@de | ^1984-12-17T00:03:12Z/11 |
| Kaiser  | Joe      | "Joe"     | ^1996-02-23T08:02:56Z/09 |
| Cakes   | Susi     | "Susi"    | ^2008-10-01T12:49:18Z/07 |


The result only lists some of the companies, since not all employment
edges have an associated start date in the edge qualifiers data.  This
means the start date edges are incomplete which in turn makes us miss
some potentially useful employment edges.  If we want to be sure to
retrieve all employment edges and associate them with start dates
where available, we can use the following query that makes start date
qualifier edges optional:

```
kgtk query -i $GRAPH -i $WORKS -i $QUALS \
     --match  'w: (p)-[r:works]->(c), g: (p)-[:name]->(n)' \
     --opt    'q: (r)-[:starts]->(s)' \
     --return 'c as company, p as employee, n as name, s as start'
```
Result:

| company | employee | name      | start                    |
|---------|----------|-----------|--------------------------|
| ACME    | Hans     | 'Hans'@de | ^1984-12-17T00:03:12Z/11 |
| Kaiser  | Otto     | 'Otto'@de |                          |
| Kaiser  | Joe      | "Joe"     | ^1996-02-23T08:02:56Z/09 |
| Renal   | Molly    | "Molly"   |                          |
| Cakes   | Susi     | "Susi"    | ^2008-10-01T12:49:18Z/07 |

Now we get all employment edges, and missing start dates will simply
be empty (or NULL).

An optional match pattern is either fully satisfied for a particular
set of variable bindings established by previous match clauses (the
variable `r` in the example above), or it is considered to have failed
for that set of bindings, so optionals do not generate partial
solutions.  In fact, optional patterns are by themselves run in strict
match mode against the data, it is only in their connection or
intersection with matches from previous clauses where the optional (or
"left join") semantics comes into play.  If for a particular set of
bindings from previous clauses the edge set retrieved by an optional
clause does not have a relevant entry, the variables generated by the
optional clause are considered to be NULL for that case.

In the next example, we use multiple independent optional clauses to
retrieve both start and/or end dates where they are available.  The
optional clauses are independent of each other, but both are dependent
on the `r` variable of the strict match clause.  In general, optional
clauses should always depend on one or more variables of a previous
match clause, otherwise they will generate potentially very large
cross products that are likely unintended:

```
kgtk query -i $GRAPH -i $WORKS -i $QUALS \
     --match  'w: (p)-[r:works]->(c), g: (p)-[:name]->(n)' \
     --opt    'q: (r)-[:starts]->(s)' \
     --opt    'q: (r)-[:ends]->(e)' \
     --return 'c as company, p as employee, n as name, s as start, e as end'
```
Result:

| company | employee | name      | start                    | end                      |
|---------|----------|-----------|--------------------------|--------------------------|
| ACME    | Hans     | 'Hans'@de | ^1984-12-17T00:03:12Z/11 |                          |
| Kaiser  | Otto     | 'Otto'@de |                          | ^1987-11-08T04:56:34Z/10 |
| Kaiser  | Joe      | "Joe"     | ^1996-02-23T08:02:56Z/09 |                          |
| Renal   | Molly    | "Molly"   |                          | ^2001-04-09T06:16:27Z/08 |
| Cakes   | Susi     | "Susi"    | ^2008-10-01T12:49:18Z/07 |                          |


Optional match patterns have the exact same syntax and expressive
power as strict match patterns, so they can have multiple clauses,
reference different graphs, use node and label restrictions, node and
edge properties, etc.  They do not inherit the last graph used by any
preceding match clause, so they start again with the default graph.

For example, in the next query we use a more complex optional pattern
that joins multiple edges and restricts matches with an additional
`--where` clause.  Note that we could have omitted the `g`
specification, since optionals do not inherit the current graph of the
previous match clause.  `kgtk_lqstring_lang` is undefined for values
that aren't language-qualified strings.  For that reason we wrap it
with `kgtk_null_to_empty`, otherwise the condition will always be
false if one of its arguments is NULL (see [**Null
values**](#null-values) for more details):

```
kgtk query -i $GRAPH -i $WORKS \
     --match 'w: (p)-[r:works]->(c)' \
     --opt   'g: (p)-[r2]->(l)-[:name]->(ln)' \
     --where 'r2.label != "name" and kgtk_null_to_empty(kgtk_lqstring_lang(ln)) != "de"' \
     --return 'c as company, p as employee, r2.label as affrel, l as affiliate, ln as name'
```
Result:

| company | employee | affrel | affiliate | name    |
|---------|----------|--------|-----------|---------|
| ACME    | Hans     | loves  | Molly     | "Molly" |
| Kaiser  | Otto     | loves  | Susi      | "Susi"  |
| Kaiser  | Joe      | loves  | Joe       | "Joe"   |
| Renal   | Molly    |        |           |         |
| Cakes   | Susi     |        |           |         |

In the previous query the optional clause was quite restrictive and
only selected edge pairs where the name edge led to a string not
qualified with `de`.  For this reason we do not get `Otto` as an
affiliate.  In the next query we relax this by moving the name edge
pattern into its own optional with associated `--where` clause, and
now we do get `Otto` as an affiliate but without a name:

```
kgtk query -i $GRAPH -i $WORKS \
     --match 'w: (p)-[r:works]->(c)' \
     --opt   'g: (p)-[r2]->(l)' \
     --where 'r2.label != "name"' \
     --opt   'g: (l)-[:name]->(ln)' \
     --where 'kgtk_null_to_empty(kgtk_lqstring_lang(ln)) != "de"' \
     --return 'c as company, p as employee, r2.label as affrel, l as affiliate, ln as name'
```
Result:

| company | employee | affrel | affiliate | name    |
|---------|----------|--------|-----------|---------|
| ACME    | Hans     | loves  | Molly     | "Molly" |
| Kaiser  | Otto     | loves  | Susi      | "Susi"  |
| Kaiser  | Joe      | friend | Otto      |         |
| Kaiser  | Joe      | loves  | Joe       | "Joe"   |
| Renal   | Molly    |        |           |         |
| Cakes   | Susi     |        |           |         |


For completeness, here is another variant of this query that uses a
`--where` clause for each individual match clause (aka "Where Mania"),
but semantically the query is the same as before:

```
kgtk query -i $GRAPH -i $WORKS \
     --match 'w: (p)-[r]->(c)' \
     --where 'r.label = "works"' \
     --opt   'g: (p)-[r2]->(l)' \
     --where 'r2.label != "name"' \
     --opt   'g: (l)-[:name]->(ln)' \
     --where 'kgtk_null_to_empty(kgtk_lqstring_lang(ln)) != "de"' \
     --return 'c as company, p as employee, r2.label as affrel, l as affiliate, ln as name'
```
Result:

| company | employee | affrel | affiliate | name    |
|---------|----------|--------|-----------|---------|
| ACME    | Hans     | loves  | Molly     | "Molly" |
| Kaiser  | Otto     | loves  | Susi      | "Susi"  |
| Kaiser  | Joe      | friend | Otto      |         |
| Kaiser  | Joe      | loves  | Joe       | "Joe"   |
| Renal   | Molly    |        |           |         |
| Cakes   | Susi     |        |           |         |


Each optional match clause is run in strict match mode against the
data, so we cannot test whether any of the variables bound by it are
in fact NULL.  Remember that these NULL values are not coming from the
match clause itself, but from its intersection or joining with the
bindings generated by previous strict or optional matches.  However,
we can test whether a variable from a prior optional clause is NULL.

For example, in the following query we again retrieve an optional
employment start date, but with the second optional clause, we
retrieve a default date for cases where the start date `s` is
undefined.  Here we simply use the date of the first edge `w11` as the
default value.  `coalesce` is an SQLite built-in function that returns
the first non-NULL argument as its value:

```
kgtk query -i $GRAPH -i $WORKS -i $QUALS \
     --match '(p)-[:name]->(n), works: (p)-[r:works]->(c)' \
     --opt   'quals: (r)-[:starts]->(s)' \
     --opt   'quals: (:w11)-[:starts]->(d)' \
     --where 's is NULL' \
     --return 'r as id, p, n as name, c as company, s as start, coalesce(s, d) as defstart'
```
Result:

| id  | node1 | name      | company | start                    | defstart                 |
|-----|-------|-----------|---------|--------------------------|--------------------------|
| w11 | Hans  | 'Hans'@de | ACME    | ^1984-12-17T00:03:12Z/11 | ^1984-12-17T00:03:12Z/11 |
| w12 | Otto  | 'Otto'@de | Kaiser  |                          | ^1984-12-17T00:03:12Z/11 |
| w13 | Joe   | "Joe"     | Kaiser  | ^1996-02-23T08:02:56Z/09 | ^1996-02-23T08:02:56Z/09 |
| w14 | Molly | "Molly"   | Renal   |                          | ^1984-12-17T00:03:12Z/11 |
| w15 | Susi  | "Susi"    | Cakes   | ^2008-10-01T12:49:18Z/07 | ^2008-10-01T12:49:18Z/07 |


But what if we want to test whether a value generated by the last
optional match clause is NULL?  For this purpose Kypher has a special
global `--where:` clause that scopes over all match clauses after they
have been joined (the colon is a mnemonic for "final").  For example,
in the next query we look for all employees and optional affiliates
that do not have a qualifying names.  This query basically emulates a
"not exists" on the pattern defined by the last optional clause:

```
kgtk query -i $GRAPH -i $WORKS \
     --match  'w: (p)-[r]->(c)' \
     --where  'r.label = "works"' \
     --opt    'g: (p)-[r2]->(l)' \
     --where  'r2.label != "name"' \
     --opt    'g: (l)-[:name]->(ln)' \
     --where  'kgtk_null_to_empty(kgtk_lqstring_lang(ln)) != "de"' \
     --where: 'ln is null' \
     --return 'c as company, p as employee, r2.label as affrel, l as affiliate, ln as name'
```
Result:

| company | employee | affrel | affiliate | name    |
|---------|----------|--------|-----------|---------|
| Kaiser  | Joe      | friend | Otto      |         |
| Renal   | Molly    |        |           |         |
| Cakes   | Susi     |        |           |         |


Cypher has a `WITH ... WHERE ...` clause for such and other purposes,
and `--where:` is simply a shorthand for `--with * --where...` in
Kypher.  For example, the next query uses the `--with` syntax for the
same result:

```
kgtk query -i $GRAPH -i $WORKS \
     --match 'w: (p)-[r]->(c)' \
     --where 'r.label = "works"' \
     --opt   'g: (p)-[r2]->(l)' \
     --where 'r2.label != "name"' \
     --opt   'g: (l)-[:name]->(ln)' \
     --where 'kgtk_null_to_empty(kgtk_lqstring_lang(ln)) != "de"' \
     --with  '*' \
     --where 'ln is null' \
     --return 'c as company, p as employee, r2.label as affrel, l as affiliate, ln as name'
```
Result:

| company | employee | affrel | affiliate | name    |
|---------|----------|--------|-----------|---------|
| Kaiser  | Joe      | friend | Otto      |         |
| Renal   | Molly    |        |           |         |
| Cakes   | Susi     |        |           |         |

For now `--with * ...` is all that is supported by Kypher.  A more
comprehensive implementation of the `--with` clause is planned as a
future extension.


For comparison, here is an **incorrect** version of this "not exists"
query pattern.  As described above, we cannot really test for NULL
inside the optional clause that generates the tested value, and
therefore now that clause always fails and all retrieved names are
NULL:

```
kgtk query -i $GRAPH -i $WORKS \
     --match 'w: (p)-[r]->(c)' \
     --where 'r.label = "works"' \
     --opt   'g: (p)-[r2]->(l)' \
     --where 'r2.label != "name"' \
     --opt   'g: (l)-[:name]->(ln)' \
     --where 'kgtk_null_to_empty(kgtk_lqstring_lang(ln)) != "de" and ln is null' \
     --return 'c as company, p as employee, r2.label as affrel, l as affiliate, ln as name'
```
Result:

| company | employee | affrel | affiliate | name    |
|---------|----------|--------|-----------|---------|
| ACME    | Hans     | loves  | Molly     |         |
| Kaiser  | Otto     | loves  | Susi      |         |
| Kaiser  | Joe      | friend | Otto      |         |
| Kaiser  | Joe      | loves  | Joe       |         |
| Renal   | Molly    |        |           |         |
| Cakes   | Susi     |        |           |         |


Finally, here is an example query that marks symmetric edges
in the data if they exist:

```
kgtk query -i $GRAPH \
     --match 'g: (x)-[r]->(y)' \
     --where 'r.label != "name"' \
     --opt   'g: (y)-[r2]->(x)' \
     --where 'r.label = r2.label' \
     --return 'x, r.label, y, r2 is not null as symmetric'
```
Result:

| node1 | label  | node2 | symmetric |
|-------|--------|-------|-----------|
| Hans  | loves  | Molly | 0         |
| Otto  | loves  | Susi  | 0         |
| Joe   | friend | Otto  | 0         |
| Joe   | loves  | Joe   | 1         |


### Returning multiple edges with `--multi`

It is sometimes useful to output query results as a set of separate
edges for each match instead of returning every match as a single row.
For example, we might want to collect separate facets of information
about each node of interest and then output those facets as separate
rows or edges.  The `--multi N` option can be used for this purpose
which simply splits each result row into `N` separate rows of equal
size.  For example, in this query we collect a person's love interest
and place of work and then output those as two separate edges per node
`x` using `--multi 2`.  Note that the formatting of the return clause
used here is simply for readability:

```
kgtk query -i $GRAPH -i $WORKS --multi 2 \
     --match 'g: (x)-[r1:loves]->(y), \
              w: (x)-[r2:works]->(c)' \
     --return 'x, r1.label, y, \
               x, r2.label, c'
```
Result:

| node1 | label  | node2   |
|-------|--------|---------|
| Hans  | loves  | Molly   |
| Hans  | works  | ACME    |
| Otto  | loves  | Susi    |
| Otto  | works  | Kaiser  |
| Joe   | loves  | Joe     |
| Joe   | works  | Kaiser  |

The column headers of the return values constituting the first result
row are used as the headers for all output rows.  Any column headers of
other return values are simply ignored.

We might also want to add optional information, for example, a
person's friend.  In this case `--multi` filters output rows that
contain NULL values leaving only rows with fully defined columns:

```
kgtk query -i $GRAPH -i $WORKS --multi 3 \
     --match 'g: (x)-[r1:loves]->(y), \
              w: (x)-[r2:works]->(c)' \
     --opt   'g: (x)-[r3:friend]->(f)' \
     --return 'x, r1.label, y, \
               x, r2.label, c, \
               x, r3.label, f'
```
Result:

| node1 | label  |  node2   |
|-------|--------|----------|
| Hans  | loves  |  Molly   |
| Hans  | works  |  ACME    |
| Otto  | loves  |  Susi    |
| Otto  | works  |  Kaiser  |
| Joe   | loves  |  Joe     |
| Joe   | works  |  Kaiser  |
| Joe   | friend |  Otto    |

Note that `--multi` is simply an output formatting directive.  All
other processing of return values such as generation of distinct
values, ordering, aggregation, limit, etc., is unaffected and proceeds
as usual applying to the full set of values of the return clause.
This also means one needs to be careful when including multi-valued
edges in a `--multi` result, since the inherent combination of values
that occurs (e.g., a person's love interest combined with all their
friends) might lead to a lot of duplicated edges which then have to be
filtered by subsequent processing.  Since the familiar `--return
distinct...` applies to the whole return clause and not individual
sub-edges or rows, deduplication of `--multi` output rows cannot be
achieved in this way.

In the following example we use a `--limit` clause to limit the number
of return values, but since that limit applies to the set of full
return values, we in fact get twice as many multi-output rows in this
case:

```
kgtk query -i $GRAPH -i $WORKS --multi 2 \
     --match 'g: (x)-[r1:loves]->(y), \
              w: (x)-[r2:works]->(c)' \
     --return 'x, r1.label, y, \
               x, r2.label, c' \
     --limit 2
```
Result:

| node1 | label  | node2   |
|-------|--------|---------|
| Hans  | loves  | Molly   |
| Hans  | works  | ACME    |
| Otto  | loves  | Susi    |
| Otto  | works  | Kaiser  |


### Query pipelines

KGTK has a powerful pipelining feature that allows commands to be
chained into pipelines where the output of one command becomes
the input of the next.  This is also possible for queries which
allows us to chain queries into complex query pipelines.  There
are a number of reason why we might want to do this:

* to intersperse KGTK commands to augment the data, for example,
  use `add-id` to add edge IDs
* to work around certain limitations of the `query` command,
  e.g., to emulate subqueries
* for performance reasons, e.g., to reuse an intermediate but
  otherwise temporary result in multiple queries

Here is an example use case.  Suppose we wanted to filter `GRAPH`
to only output low-frequency edges.  Here we define "low-frequency"
as an edge that has a label that occurs less than 5 times in the data.
To do this we have to first use [**aggregation**](#aggregation) to
count edge labels and then restrict based on those counts.  However,
we cannot currently do that in Kypher, since we do not have subqueries
(yet).  Aggregation is done in the return clause, and there is no way
for us to express an upper or lower bound based on the computed counts.

So let us compute what we want with a query pipeline instead.  The first
query in the command below computes the counts on edge labels as
we've seen before.  Since the resulting count rows will become the
input to a second query, it is important that they are in valid KGTK
format, which is the reason that we express them as `PROP count N`
triples with the appropriate `node1`, `label` and `node2` column
headers.  We then pipe the output of this query into `add-id` which
simply adds an `id` column.  Next we use the output of `add-id` as the
input of the second query with `-i -`.  The dash indicates that this
input comes from standard input of the query command (the output of
`add-id`).  Within the match clause we can refer to this input as
`stdin` (or we could have simply omitted a name, since it is the first
input in the list).  We then select edges from `GRAPH` that have one
of the properties in the list where the count matches the
where-constraint:

```
kgtk query -i $GRAPH \
     --match '(x)-[r]->(y)' \
     --return 'r.label as node1, "count" as label, count(r.label) as node2' \
   / add-id \
   / query -i - -i $GRAPH \
     --match 'stdin:  (prop)-[]->(count), \
              graph:  (x)-[r {label: prop}]->(y)' \
     --where 'cast(count, int) < 5' \
     --return 'x, r.label, y, r'
```
Result:

| node1 | label  | node2 | id  |
|-------|--------|-------|-----|
| Joe   | friend | Otto  | e13 |
| Hans  | loves  | Molly | e11 |
| Otto  | loves  | Susi  | e12 |
| Joe   | loves  | Joe   | e14 |

Here is a minor variant that names the counts input with an alias (see
[**Input and output specifications**](#input-output)) which can make
queries more readable:

```
kgtk query -i $GRAPH \
     --match '(x)-[r]->(y)' \
     --return 'r.label as node1, "count" as label, count(r.label) as node2' \
   / add-id \
   / query -i - --as counts -i $GRAPH \
     --match 'counts: (prop)-[]->(count), \
              graph:  (x)-[r {label: prop}]->(y)' \
     --where 'cast(count, int) < 5' \
     --return 'x, r.label, y, r'
```

Any number of queries can be chained into complex pipelines.  If
intermediate data such as the counts above are not explicitly named
and preserved, it will simply be replaced by the input imported by
the next query in the chain.  This is generally the expected behavior
and avoids accumulation of useless intermediate results.

Query pipelines are powerful, but also can have a lot of complexity.
There are many places where command or query errors may occur.  For
that reason they should be developed and debugged step-by-step instead
of trying to make things work all at once.  Also note that options or
defaults from one query do not carry over to the next one, they all
are processed as if they were independently launched queries in the
shell, the only thing connecting them is the dataflow from stdout of
one query to stdin of the next.


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
    **Important restriction:** if an input is specified to be coming from standard input
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
5. once a handle is matched its matching input is removed from the pool of
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

Example with an input coming from standard input which is implicitly
given a filename using `stdin` as its basename (mapped to the graph
handle `s` here):

```
kgtk cat -i file1.tsv -i file2.tsv / query -i - -i data/works.tsv \
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


### Appending data

Use the `-a` or `--append` option to incrementally append additional data file(s) to
a specified input.  For example:

```
kgtk query -i $GRAPH -a more-graph-edges.tsv --limit 5
```

The `-a` option applies to the previously specified input (`GRAPH` in
this case), and there can be one or more append files specified.  The
appended files must have the same columns as the graph data they are
appended to, but their order can differ (import will be faster if the
column order is also the same).  The main file can also be specified
and imported in the same command.

There are no other checks on the appended data beyond the necessary
columns, the data is treated just as if it had been part of the
original data file, there are no duplicate checks, ID management,
etc., that is all left up to the user.

Any indexes already defined on the original data will be updated
automatically for the appended data.  This is a bit slower than
building the index from scratch for all of the data, but should not
matter for small incremental updates.

After an append there is more than one file pointing to a particular
graph table, and any of them can be used in the `-i` option to
identify that graph.  As with regular inputs, if the data has already
been imported and has not changed, specifying a file is a no-op,
however, one cannot replace an appended file only with new data, in
this case one has to replace the whole graph.

One can also use this mechanism instead of the KGTK `cat` command
if the input data has all the appropriate columns, for example:

```
kgtk query -i file1.tsv -a file2.tsv -a file3.tsv --limit 5
```

!!! note
    Appending data is not supported for vector tables processed by
    [**Kypher-V**](#kypher-v), since ANNS indexing and other processing
    needs to be done collectively for the whole table, and can
    (currently) not be updated incrementally.


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

The location of the cache file can be controlled with the `--graph-cache FILE`
option.  If that is not explicitly specified, the environment variable
KGTK_GRAPH_CACHE will be checked.  If that is not found, the system will
create or reuse a cache file in the computer's temp directory which will look
like this (where `UID` is replaced by the current user name):

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


### Auxiliary graph caches

For very large and complex datasets it can become useful to organize
them into separate graph cache files.  For example, we might want to
keep large stable Wikidata files in one graph cache, embedding vector
data in one or more others, and use yet another for dynamic data such as
query inputs, scenario data, etc.  One advantage for organizing things
this way is that we can easily throw a dynamic more volatile graph
cache away without affecting other more stable ones that took a long
time to import and index.  Another is that we can keep graph cache
file sizes more managable by splitting things up over multiple cache
files.  All this is of course only really useful if we can ask queries
across all these data files, despite their separation into different
cache files.  That's what the `--aux-cache` or `--ac` options are for.

For example, let us start by creating a very small input dataset in
its separate cache.  We first collect all distinct qualifier properties
into a small set `set1`, use the KGTK `add-id` command to add an ID
column to each row, and then pipe the results to a separate query
but giving that a distinct new graph cache file `/tmp/props.db`.
Since we are importing from standard input in that query, we also
use an alias `props` so we can easily refer to that later:

```
kgtk query -i $QUALS \
     --match '(x)-[r]->(y)' \
     --return 'distinct r.label as node1, "member" as label, "set1" as node2' \
     / add-id \
     / query -i - --as props --gc /tmp/props.db
```
Result:

| node1   | label  | node2 | id |
|---------|--------|-------|----|
| starts  | member | set1  | E1 |
| ends    | member | set1  | E2 |


Next we query for all edges in the `WORKS` graph that are qualified by
one or more edges in the `QUALS` graph with a qualifier edge label
from `props`.  To do this we add `/tmp/props.db` as an auxiliary cache
in addition to the default main graph cache file.  There always has to
be exactly one main graph cache and zero or more auxiliary caches:

```
kgtk query --ac /tmp/props.db -i $WORKS -i $QUALS -i props \
     --match 'props: (p)-[]->(), \
              quals: (wr)-[qr {label: p}]->(), \
              works: (x)-[wr {label: wl}]->(y)' \
     --return 'wr as id, x, wl, y'
```
Result:

| id  | node1 | label | node2  |
|-----|-------|-------|--------|
| w11 | Hans  | works | ACME   |
| w12 | Otto  | works | Kaiser |
| w13 | Joe   | works | Kaiser |
| w14 | Molly | works | Renal  |
| w15 | Susi  | works | Cakes  |

!!! note
    **Important:** when one or more auxiliary caches are used in a query
    all graph caches are queries in read-only mode (see below).  This means
    graph caches need to be fully constructed and indexed before they can
    be used in such a query (this restriction might be relaxed in the future).

It is possible to have a graph with the same name defined in more than
one graph cache.  In this case it will be dereferenced to the graph
cache in which it appears first, starting with the main graph cache
and then continuing with auxiliary caches in the order they are
listed on the command line.

At most 10 graph caches (1 main, 9 auxiliary) can be used simultaneously
in a query.  This is a restriction from a default SQLite configuration value
which can only be changed through recompilation.


### Read-only processing

Sometimes it is useful to protect the graph cache from any unintended
updates such as data imports or index creation.  For example, one
might want to debug certain queries without risking any unintended
index creation based on incorrect queries.  For this purpose, the
graph cache can be opened in read-only mode by supplying the
`--read-only` or `--ro` option.  In read-only mode it is assumed that
the graph cache exists, and that all data necessary to run the query
has been previously imported and indexed.

Note that even if the query systems determines that a certain index is
necessary to run the query efficiently, this index will not actually
be built when executing read-only, which in turn could lead to very
long execution times.  For that reason it is useful to run queries
with small result limits first.  Moreover, if the query requires
import of data that is not yet available in the cache, an error will
be raised.  In general, read-only processing can lead to query errors
if data or indexes required to run a query is not available or cannot
be built (for example, full-text indexes).  However, such errors are
harmless, since they cannot lead to any corruption of the graph cache.

Read-only processing can also be used to safely run multiple queries
in parallel over the same graph cache.  Note, however, that disk
access contention from parallel queries might lead to performance
degredation that could completely eliminate any gains from parallel
processing.


### Single-user mode, locking and transactions

By default the database runs in multi-user mode, allowing (at most)
one process to update a graph cache database and any number of other
concurrent processes to simultaneously read it.  This is implemented
by using SQLite's
[**write-ahead-logging**](https://www.sqlite.org/wal.html) mode (or
WAL mode).  While this is generally a preferable configuration option,
it can slow down import of large data files by a factor of 1.5 to 2.

In single-user mode (activated with the `--single-user` option), the
database does not allow any concurrent readers while updates are being
processed.  This is useful to speed up importing and indexing of very
large data files, but can lead to "database is locked" errors with
query pipelines or other parallel invocations, so should be used with care
when it is clear that only one process needs to access a graph cache.
This distinction between single-user and multi-user mode only exists
if one process is currently *modifying* the database.  If there are no
updates, e.g., if all queries use the `--read-only` option, both modes
behave identically and multiple parallel queries over the same graph
cache are possible.

If a graph cache database is currently being updated (because data is
being imported or an index created), any attempt by a second process
to concurrently modify the graph cache database will fail with a
"database is locked" error after a short timeout period.  Once the
first update operation is complete, the second one can be relaunched.

All update operations such as data import, index creation and update
of the `kypher_master` info table are protected by atomic database
transactions.  If an error or user interrupt occurs during such a
transaction, any changes are rolled back to the last consistent state.
It is possible that a rollback journal file persists after a user
interrupt, however, the next query on the same graph cache DB will
make the database consistent based on the journal file before any
further processing occurs.  The journal file will then be
automatically deleted.


### Managing very large datasets

Graph cache files can become quite large when large or a large number
of different data files are being queried over time.  Cache size is
generally around 1-2.5 times the uncompressed size of all imported
KGTK files depending on indexing requirements.  For large datasets it
is often useful to specify dedicated graph caches via the
`--graph-cache` option to keep file sizes manageable.  It is also
possible to spread data files over several graph caches and then
attach them via the `--aux-cache` directive (see [**Auxiliary Graph
Caches**](#auxiliary-graph-caches) for more details).  Note that all
graphs queried in a single query must reside in either the main graph
cache or one of the auxiliary caches.

For best performance, cache files should reside on a local, internal
SSD drive and not be accessed via a USB connection or network share
such as NFS or Samba.  Using a multi-SSD-disk array in RAID-0
configuration can further improve disk access times and cache
performance.  When internal disk space cannot be used or easily
extended, using an external SSD drive with a fast USB-C connection is
also an option, for example, to add budget disk space to an otherwise
constrained laptop.  This will not be as fast as an internal disk but
has worked quite well for some of our KGTK team members.  Finally, the
database itself does not require much RAM, but having plenty of RAM
available (say 30 GB or more) allows the OS to cache more data pages
in memory, which makes repeat accesses faster and can greatly improve
query performance.

When data gets deleted and reimported, freed up space in the cache
file is reused, but unused data pages are not automatically returned
to the file system and the size of the cache file does not shrink.  To
actually free and return any unused space in the cache file to the
file system, one can use the SQLite `vacuum` command (which might take
a significant time to run depending on the size of the cache).  For
example:

```
sqlite3 /tmp/my-graph-cache.sqlite3.db vacuum
```

When the database imports and indexes files, it creates temporary
files in a temp directory, so changes can be rolled back in case
something goes wrong.  The default location of that temporary
directory (see [SQLite manual](https://sqlite.org/tempfiles.html)) is
usually one of the standard temp file locations such as `/var/tmp`,
`/usr/tmp` or `/tmp`) which is often in a separate root partition and
might not have the same amount of disk space available as the location
selected for the graph cache.  For that reason, the query command sets
the temp file location to be the same directory as the graph cache
under the assumption that that's where most space will be available.
That behavior can be overridden if necessary by explicitly setting the
environment variable `SQLITE_TMPDIR` to a different storage area where
there is room (e.g., if the graph cache location is getting close to
capacity).  For example:

```
export SQLITE_TMPDIR=/data/tmp
```

Note that temporary files created by the database are not (easily)
visible so it might seem strange to see a `"database or disk is full"`
error even though there is room available before and after a query
operation that, for example, tried to create new indexes.  If that
happens `SQLITE_TMPDIR` can be used to point to a different location
to allow such an indexing operation to succeed even if there is not
enough room on the disk the graph cache is on.


### Distributing the graph cache

The graph cache file is an SQLite database file which has a very
stable format across database versions and can be compressed and
shipped to others for quick and easy reuse.  In that case it is
advised to first replace any absolute input file names with logical
names using the `--as` option.

The `--show-cache` option can be used to describe the current location
and content of the cache along with any comments specified for inputs
with the `--comment` option.  For example:

```
kgtk query --show-cache
```

Result:
```
Graph Cache:
DB file: /tmp/kgtk-graph-cache-XXX.sqlite3.db
  size:  64.00 KB   	free:  0 Bytes   	modified:  2021-07-16 16:06:45

KGTK File Information:
graph:
  size:  211 Bytes   	modified:  2021-02-08 13:46:39   	graph:  graph_2
quals:
  size:  253 Bytes   	modified:  2021-02-08 13:46:39   	graph:  graph_3
works:
  size:  377 Bytes   	modified:  2021-02-08 13:46:39   	graph:  graph_1
  comment:  Company data

Graph Table Information:
graph_1:
  size:  16.00 KB   	created:  2021-07-16 16:02:33
  header:  ['id', 'node1', 'label', 'node2', 'node1;salary', 'graph']
graph_2:
  size:  12.00 KB   	created:  2021-07-16 16:02:33
  header:  ['id', 'node1', 'label', 'node2']
graph_3:
  size:  16.00 KB   	created:  2021-07-16 16:02:33
  header:  ['id', 'node1', 'label', 'node2', 'graph']
```

This command will ignore all other query-related options and not
actually import any data or run a query.  The only other useful option
is `--graph-cache` to point to a specific graph cache to be described.


## Kypher language features

Kypher is a complex language and the description in this document will
necessarily be somewhat incomplete.  For a more complete description
of the Cypher language it is based on please refer to
[Cypher](https://neo4j.com/developer/cypher/) and
[openCypher](https://www.opencypher.org/resources), but keep in mind
the important differences described [**here**](#differences-to-cypher).
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
kgtk query -i $GRAPH \
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
| concat(x, ...)            | Cocatenate printed representations of the given arguments into a string.                                       |
| instr(x, sub)             | Find the first occurrence of `sub` in string `x`  ([full doc](https://sqlite.org/lang_corefunc.html#instr)).   |
| length(x)                 | Number of characters in a string `x`              ([full doc](https://sqlite.org/lang_corefunc.html#length)).  |
| lower(x)                  | Convert `x` to lower case                         ([full doc](https://sqlite.org/lang_corefunc.html#lower)).   |
| printf(format, ...)       | Build a formatted string from some arguments      ([full doc](https://sqlite.org/lang_corefunc.html#printf)).  |
| replace(x, from, to)      | Replace `from` with `to` in `x`                   ([full doc](https://sqlite.org/lang_corefunc.html#replace)). |
| rowid(x)                  | Implements `rowid` lookup for Kypher query variable `x`, which is the 1-based row ID in the graph table from which the current value of `x` is retrieved.  If `x` is a join variable, the table is ambiguous and the result will be arbitrary, so an unjoined relation variable is generally a good choice. |
| substr(x, start, length)  | Substring of `x` of `length` starting at `start`  ([full doc](https://sqlite.org/lang_corefunc.html#substr)).  |
| substr(x, start)          | Substring of `x` starting at `start` to the end   ([full doc](https://sqlite.org/lang_corefunc.html#substr)).  |
| typeof(x)                 | Return the type of expression `x`                 ([full doc](https://sqlite.org/lang_corefunc.html#typeof)).  |
| upper(x)                  | Convert `x` to upper case                         ([full doc](https://sqlite.org/lang_corefunc.html#upper)).   |


#### SQLite built-in math functions

All of [SQLite3's built-in math
functions](https://www.sqlite.org/lang_mathfunc.html) can be used.
The implementation is either native (once available with version
3.35.0 or later), or through equivalent Python functions.  For a
comprehensive list of those functions please follow the link.  The
only difference is that SQLite's two-argument version of the general
logarithm `log(B, X)` has been renamed into `logb(B, X)`, since the
function registration API cannot support optional arguments.

!!! note
    Some of the built-in math functions use slightly different naming
    or argument order than standard SQL or the Python `math` module,
    so be sure to carefully follow the documentation.


#### SQLite built-in aggregation functions

All of [**SQLite3's built-in aggregate
functions**](https://www.sqlite.org/lang_aggfunc.html) can be used.


#### General KGTK functions

| Function              | Description                                                                                |
|-----------------------|--------------------------------------------------------------------------------------------|
| kgtk_literal(x)       | Return True if `x` is any KGTK literal.  This assumes valid literals and only tests the first character (except for booleans). |
| kgtk_symbol(x)        | Return True if `x` is a KGTK symbol.  This assumes valid literals and only tests the first character (except for booleans).    |
| kgtk_type(x)          | Return a type for the KGTK literal or symbol `x`, which will be one of `string`, `lq_string`, `date_time`, `quantity`, `geo_coord`, `boolean`, `typed_literal` or `symbol`.  This assumes valid literals and only tests the first character (except for booleans). |
| kgtk_regex(x, regex)  | Regex matcher that implements the Cypher `=~` semantics which must match the whole string ([Python regex syntax](https://docs.python.org/3/howto/regex.html)) |
| kgtk_regex_replace(x, regex, repl) | Regex replacer that replaces all occurrances of `regex` in `x` with `repl` ([Python regex syntax](https://docs.python.org/3/howto/regex.html), see Python's `re.sub`) |
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

!!! note
    Functions that return numeric values are restricted to 8-byte integers and 8-byte IEEE floats.
    Values that fall outside those ranges will be mapped onto floats when allowed or clamped to
    the respective data type boundary values.


#### Functions on KGTK geo coordinates

| Function                | Description                                                                  |
|-------------------------|------------------------------------------------------------------------------|
| kgtk_geo_coords(x)      | Return True if `x` is a KGTK geo coordinates literal.                        |
| kgtk_geo_coords_lat(x)  | Return the latitude component of a KGTK geo coordinates literal as a float.  |
| kgtk_geo_coords_long(x) | Return the longitude component of a KGTK geo coordinates literal as a float. |


<A NAME="text-search-functions"></A>
#### Full-text search functions

The following functions support efficient full-text search and
matching based on text indexes.  Full-text search is based on SQLite's
FTS5 module whose implementation, options and match syntax is
described in more detail [here](https://www.sqlite.org/fts5.html).
In the functions below, `x` must be a match variable that can be
uniquely linked to a specific unnamed or named text index.  If no or
multiple indexes are applicable, an error will be raised.  Text indexes
can be built with a `text:` index spec, for example,  `--idx text:node2`.

| Function                          | Description                                                       |
|-----------------------------------|-------------------------------------------------------------------|
| textmatch(x, pat)                 | Return True if `x` matches the full-text MATCH pattern `pat`.     |
| textlike(x, pat)                  | Return True if `x` matches the LIKE pattern `pat`.                |
| textglobl(x, pat)                 | Return True if `x` matches the GLOB pattern `pat`.                |
| matchscore(x)                     | Return the BM25 match score for the text match on `x` (scores are negative, smaller are better). |
| bm25(x)                           | Synonym for `matchscore`.                                         |

For example, here we define a text index on the `node2` column of
`GRAPH` and then use `textmatch` to match against the values of that
column.  For now text indexes need to be explicitly defined before
they can be used.  We also give the index a name using the
`//name=myidx` option which is optional but will allow us to
demonstrate access to named indexes.

```
kgtk query -i $GRAPH --idx auto text:node2//name=myidx \
     --match '(x)-[r]->(y)' \
     --where 'textmatch(y, "ott")' \
     --return 'x, r.label, y, matchscore(y) as score' \
     --order 'score'
```
Result:

| node1 | label  |  node2     |  score               |
|-------|--------|------------|----------------------|
| Joe   | friend |  Otto      |  -1.3605330992115003 |
| Otto  | name   |  'Otto'@de |  -0.8144321029967752 |

Note how all the scores are negative with the best being the smallest
(most negative) which allows the use of default ascending ordering to
get the best matches first.

`textmatch` patterns use a phrase-based language that allows
multi-word phrases, Boolean expressions, multi-column expressions,
suffix patterns, etc.  See
[here](https://www.sqlite.org/fts5.html#full_text_query_syntax) for a
full exposition.  What is handled exactly and efficiently depends on
the options used when the text index was defined (which are
unfortunately somewhat complex).  By default, the `trigram` tokenizer
is used here which supports a large number of different operations
efficiently.

Here is an example of a Boolean expression:

```
kgtk query -i $GRAPH --idx auto text:node2//name=myidx \
     --match '(x)-[r]->(y)' \
     --where 'textmatch(y, "ott OR hans")' \
     --return 'x, r.label, y, matchscore(y) as score' \
     --order 'score'
```
Result:

| node1 | label  |  node2     |  score               |
|-------|--------|------------|----------------------|
| Joe   | friend | Otto       | -1.3605330992115003  |
| Hans  | name   | 'Hans'@de  | -1.2859084137069412  |
| Otto  | name   | 'Otto'@de  | -0.8144321029967752  |

The `trigram` tokenizer also supports case-insensitive SQL `LIKE`
patterns and case-sensitive `GLOB` patterns.  In general, with a
trigram index, a pattern must contain at least one trigram for a
`MATCH` pattern to be successful or for the `LIKE` and `GLOB` patterns
to work efficiently.  Here are some more examples:

```
kgtk query -i $GRAPH --idx auto text:node2//name=myidx \
     --match '(x)-[r]->(y)' \
     --where 'textlike(y, "%ott%")' \
     --return 'x, r.label, y, matchscore(y) as score' \
     --order 'score'
```
Result:

| node1 | label  |  node2     |  score               |
|-------|--------|------------|----------------------|
| Joe   | friend | Otto       | -1.3605330992115003  |
| Otto  | name   | 'Otto'@de  | -0.8144321029967752  |

```
kgtk query -i $GRAPH --idx auto text:node2//name=myidx \
     --match '(x)-[r]->(y)' \
     --where 'textglob(y, "*Ott*")' \
     --return 'x, r.label, y, matchscore(y) as score' \
     --order 'score'
```
Result:

| node1 | label  |  node2     |  score               |
|-------|--------|------------|----------------------|
| Joe   | friend | Otto       | -1.3605330992115003  |
| Otto  | name   | 'Otto'@de  | -0.8144321029967752  |

It is possible to define more than one text index for a particular graph
or column, e.g., to allow differently optimized indexes to coexist for
certain types of fuzzy matching.  In such cases the optional name of an
index can be used to indicate which index should be used.  Such names
must be used as the first element of the match variable.  For example:

```
kgtk query -i $GRAPH --idx auto text:node2//name=myidx \
     --match '(x)-[r]->(y)' \
     --where 'textmatch(myidx.y, "ott")' \
     --return 'x, r.label, y, matchscore(myidx.y) as score' \
     --order 'score'
```
Result:

| node1 | label  |  node2     |  score               |
|-------|--------|------------|----------------------|
| Joe   | friend |  Otto      |  -1.3605330992115003 |
| Otto  | name   |  'Otto'@de |  -0.8144321029967752 |

Finally, a text index may index more than one column in which case the
match expression can use column-specific filters which can be combined
in arbitrary Boolean expressions.  For multi-column matching, the
relation variable must be used as the variable to be matched on (`r`
in the examples below):

```
kgtk query -i $GRAPH --idx auto text:node1,node2//name=multi \
     --match '(x)-[r]->(y)' \
     --where 'textmatch(multi.r, "node1: joe AND node2 : ott")' \
     --return 'x, r.label, y, matchscore(multi.r) as score' \
     --order 'score'
```
Result:

| node1 | label  |  node2     |  score               |
|-------|--------|------------|----------------------|
| Joe   | friend | Otto       | -2.1158081150971633  |

```
kgtk query -i $GRAPH --idx auto text:node1,node2//name=multi \
     --match '(x)-[r]->(y)' \
     --where 'textmatch(multi.r, "node2: ott NOT node1 : joe")' \
     --return 'x, r.label, y, matchscore(multi.r) as score' \
     --order 'score'
```
Result:

| node1 | label  |  node2     |  score               |
|-------|--------|------------|----------------------|
| Otto  | name   | 'Otto'@de  | -0.8763404768201021  |

Finally, full-text indexing is really only necessary on reasonably
large data (e.g., the text labels of Wikidata), on small data like the
example `GRAPH` used here, everything could have been done just as
efficiently with standard regular expression matching.

TO DO: full documentation of all text index definition options


#### Defining and using custom functions

When the built-in functions provided by SQLite and Kypher are not enough, the functions below
can be used to execute arbitrary Python code as part of a Kypher query.  To allow users to
execute their own special-purpose code in such circumstances, the `--import` argument can be
used to import any required library or user modules before the query is exectuted.

| Function               | Description                                                                               |
|------------------------|-------------------------------------------------------------------------------------------|
| pyeval(expression...)  | Python-eval `expression` and return the result (coerce value to string if necessary).  Multiple `expression` arguments will be concatenated first.                             |
| pycall(fun, arg...)    | Python-call `fun(arg...)` and return the result (coerce value to string if necessary).  `fun` must name a function and may be qualified with a module imported by `--import`.  |

Here is an example that uses both of these facilities.  First we are
importing the `uuid` and `math` modules (the latter with an alias), so
we can refer to them in the `pycall` expressions.  The `--import`
argument takes anything that would be a legal argument to a single
Python `import` statement.  Here we used some standard Python modules,
but any user-defined module(s) could be used as long as they are
findable in the current `PYTHONPATH`.  `pyeval` parses and evaluates
an arbitrary Python expression which here we assemble via a `printf`
function call.  `pycall` is slightly more efficient, since it only has
to look up the function object based on the provided (qualified) name:

```
kgtk query -i $GRAPH --import 'uuid, math as m' \
     --match '(x)-[r:name]->(y)' \
     --where 'kgtk_lqstring(y)' \
     --return 'y as name, \
               pyeval(printf($FMT, y)) as swapname, \
               pycall("m.fmod", length(y), 2) as isodd, \
               pycall("uuid.uuid4") as uuid' \
     --para FMT='"%s".swapcase()'
```
Result:

|  name     |  swapname  |  isodd  |   uuid                                |
|-----------|------------|---------|---------------------------------------|
| 'Hans'@de |  'hANS'@DE |  1.0    |  5742f943-9bbe-4c5c-a4ac-98ffda145642 |
| 'Otto'@de |  'oTTO'@DE |  1.0    |  a3d720e8-c331-4a9a-b5db-ab188ccb3e53 |

The values returned by `pyeval` and `pycall` must be simple literals
such as numbers, strings or booleans.  Anything else would cause a
database error and is therefore converted to a string first (e.g., the
`UUID` objects returned by `uuid.uuid4`).

Here is an alternative invocation of `pyeval` that uses multiple arguments
which will be implicitly string-concatenated before evaluation.  The
`char(34)` term produces a double quote to avoid shell quoting issues:

```
kgtk query -i $GRAPH \
     --match '(x)-[r:name]->(y)' \
     --where 'kgtk_lqstring(y)' \
     --return 'y as name, \
               pyeval(char(34), y, char(34), ".swapcase()") as swapname'
```
Result:

| name      | swapname  |
|-----------|-----------|
| 'Hans'@de | 'hANS'@DE |
| 'Otto'@de | 'oTTO'@DE |


!!! note
    Functions will often be executed in the inner loop of a database query
    and are therefore expected to be simple and fast.  Long-running functions
    might lead to very long query times.

Users may also implement their own built-ins directly which will
generally be more efficient than going through the `pyeval`
mechanisms.  For example, suppose the file `mybuiltins.py` has the
following content and is visible in the current `PYTHONPATH` (note
that `num_params` can also be -1 to allow functions with a variable
number of arguments):

```
from kgtk.kypher.sqlstore import SqliteStore

def swapcase(x):
    return str(x).swapcase()

SqliteStore.register_user_function(name='swapcase', num_params=1, func=swapcase)
```

Then we can import it in a query and call the defined function just as any
other Kypher built-in:

```
kgtk query -i $GRAPH --import 'mybuiltins' \
     --match '(x)-[r:name]->(y)' \
     --where 'kgtk_lqstring(y)' \
     --return 'y as name, swapcase(y) as swapname'
```
Result:

|  name     |   swapname   |
|-----------|--------------|
| 'Hans'@de |   'hANS'@DE  |
| 'Otto'@de |   'oTTO'@DE  |


### Virtual graph functions

Virtual graph functions are similar to standard KGTK functions with
the one difference that they can produce more than one result value.
We think of them as computations that generate virtual edges, one
edge for each result generated by a set of inputs.  For this reason
they need to be used in a strict or optional match clause with the
`node1` of the edge (usually) being the first input, the `label`
being the name of the `function`, `node2` (usually) being the main
output, and any additional inputs and outputs associated via edge
properties.

| Function                     | Description                  |
|------------------------------|------------------------------|
| kgtk_values                  | Dynamically generate values from a list literal or Python expression. If the 'format' property is 'auto' (the default) a value ending in any type of parenthesis is considered to be a Python expression which will be evaluated in module 'module' (defaults to 'builtins').  The result is assumed to be a Python collection whose values will be returned in order as the value of node2. Otherwise, the values literal will be split along a number of standard separators. If 'format' is 'python' an evaluation in Python will be forced.  Any other value of 'format' is assumed to be a separator string to split the values literal. This virtual graph will disable query optimization in any match clause it is used in to make sure values are generated at the desired point in the query. |

Here are some examples for the potential use of `kgtk_values`.  Note that these queries specify
an input graph (since that is required), but the graph is not really used by the queries:

```
kgtk query -i $GRAPH \
     --match '(x:`a b c`)-[:kgtk_values]->(v)' \
     --return 'v'
```
Result:

| node2 |
|-------|
| a     |
| b     |
| c     |

```
kgtk query -i $GRAPH \
     --match '(x:`range(3)`)-[:kgtk_values]->(v)' \
     --return 'v'
```
Result:

| node2 |
|-------|
| 0     |
| 1     |
| 2     |

```
kgtk query -i $GRAPH \
    --match '(x)-[:kgtk_values {format: "%%"}]->(v)' \
    --where 'x=$VALUES' \
    --return 'v' \
    --para VALUES='a%%b%%c'
```
Result:

| node2 |
|-------|
| a     |
| b     |
| c     |


<A NAME="differences-to-cypher"></A>
### Important differences to Cypher

* Kypher does not use a property graph data model
* supports querying across multiple graphs
* no graph update commands
* single strict match clause only
* no relationship isomorphism
* no dynamic properties such as `x[fn(y)]`
* lists can only contain literals
* Python regexps instead of Java regexps
* different set of built-in functions

Features that are currently missing but might become available in future versions:

* transitive path range patterns
* `exists` subqueries
    * if needed can be emulated via query pipelines
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
achieved with the `--index [MODE ...]` and `--idx [SPEC ...]` options
(experts only).

`--index` describes one or more default indexing modes or actions that
should be applied to all inputs of the current query (the default is
`mode:auto` or `auto` for short).  `--idx` or its long form
`--input-index` describe one or more indexing modes/specs that should
be applied for the preceding input only which will override any
defaults coming from `--index` for that particular input.

The following pre-defined indexing modes are currently supported:

| Macro Modes               | Description                                                                                            |
|---------------------------|--------------------------------------------------------------------------------------------------------|
| mode:none                 | do not create any new indexes                                                                          |
| mode:auto                 | automatically create indexes needed for good performance (the default)                                 |
| mode:autotext             | automatically create text search indexes as needed (not yet implemented)                               |
| mode:clear                | delete all currently defined indexes                                                                   |
| mode:cleartext            | delete all currently defined text search indexes                                                       |
| mode:expert               | use SQLite's expert mode to determine which indexes to build (deprecated)                              |

| Graph modes               |                                                                                                        |
|---------------------------|--------------------------------------------------------------------------------------------------------|
| mode:graph                | build covering indexes on `node1` and `node2`, single column index on `label` (for general graphs)     |
| mode:monograph            | build covering indexes on `node1` and `node2` (for mono-relational graphs)                             |
| mode:valuegraph           | build a single-column index on `node1` (for mono-relational attribute-value graphs)                    |
| mode:textgraph            | build a single-column index on `node1`, default unnamed text index on `node2` (for mono-relational attribute-value graphs with text values) |

| Legacy modes              |                                                                                                        |
|---------------------------|--------------------------------------------------------------------------------------------------------|
| mode:node1+label          | build single-column indexes on `node1` and `label`                                                     |
| mode:triple               | build single-column indexes on `node1`, `label` and `node2`                                            |
| mode:quad                 | build single-column indexes on `node1`, `label`, `node2` and `id`                                      |

All of the modes listed above except for `mode:clear` and
`mode:cleartext` can be supplied without the `mode:` prefix.  Clearing
modes need to be explicitly qualified to reduce the chance of
accidental deletion of indexes.  Note that these modes will be applied
only locally to the listed input most closely preceding an `--idx`
option, or globally to all listed query inputs if the `--index` option
is used.  If a local indexing option is given for an input, none
of the global default options will be applied to it.

Multiple index options can be supplied locally and globally.
For example, here we first clear any pre-existing indexes on the
qualifiers graph and then create a single-column index on `node1`
using the `valuegraph` mode:

```
kgtk query -i $QUALS --idx mode:clear valuegraph
```

Indexing modes can safely be resupplied over multiple queries.
Indexes will only be built if they are not yet available.  If an index
implied by a mode has already been constructed, it will simply be reused.

Besides high-level modes, a concise more fine-grained language of
index specs is also available to allow highly custom-tailored
specification of graph indexes.  This is particularly useful for text
search indexing which provides a number of different indexing options
(see [**Full text search functions**](#text-search-functions) for
more details).

Index specs are indicated with the `index:` prefix for graph indexes
and the `text:` prefix for text search indexes.  For example, a
two-column unique index starting from `node2` that ignores the label
column can be specified like this:

```
index:node2,node1//unique
```

Options can be supplied with the slash syntax.  Double slashes indicate global
options that apply to the whole index, single slashes indicate column-local
options.  `unique` is the only option currently supported for graph indexes,
it indicates and enforces that the listed columns form a unique key, that is,
there are no two rows in the graph that have the same values for those columns.

Columns containing special characters can be quoted using backtick
syntax.  For example, to index on an extra column do this (but note the
extra quotes necessary to prevent the shell from interpreting those
backticks):

```
--idx 'index:node1,`node1;region`'
```

`index:` is the default prefix implied for specs without a prefix.  For example,
`node1` can be used instead of `index:node1`.  For cases where a column name
matches one of the modes listed above, an explicit qualification is needed,
for example, to index a column named `cleartext` use `index:cleartext`.

Multiple modes and specs can be specified locally and globally and will be
interpreted in sequence.  For example:

```
kgtk query -i $GRAPH --idx mode:clear node1,node2 node2,node1 -i $WORKS --index none ...
```


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
use case.  Note also the next section on covering indexes which can
help with implicit sorting along multiple directions.

Another thing to consider for very large datasets is to split them
into separate files with different sets of edge labels.  This will
keep data tables smaller, improve locality, but for the cost of some
extra query complexity due to the multiple data files.


#### Covering indexes

Several of the indexing modes listed above will generate *covering
indexes* for graphs.  A covering index is an index where the database
can retrieve all the required values in a join directly from the index
as opposed to first looking up a table row from the index and then
accessing that table row to get a relevant value which requires
additional disk accesses and will often break access locality.

For example a `node2` covering index such as `index:node2,label,node1`
will allow the database to join on `node2` and `label` which is useful
for highly ambiguous labels (e.g., Wikidata's `P31`) and then be able
to get `node1` directly from the index entry instead of having to go
back to the data table to look it up.  Such an index also implicitly
sorts the data which greatly improves locality, even if the data is
not sorted in the data table.  Such covering indexes can therefore
greatly speed up complex queries on large graphs.  The price for the
performance gain is the extra disk space needed for such indexes which
might be significant.


### Disabling query optimization

The `--dont-optimize` option can be used to force the SQLite query
optimizer to not optimize the table order in which a join is
processed.  Normally the query optimizer will try to guess the table
with the smallest number of matches given what it knows about table
sizes, indexes and selectional restrictions in the query, generate all
rows for that table according to the given restrictions and then join
other tables for each match using appropriate indexes (this is just
the high-level gist of a complex query planning process).  However,
the determined order might not always be optimal or even be bad and
lead to much longer query run times in certain cases.  One of the reasons
is that the graph tables used by Kypher violate many of the assumptions
that normally hold for standard relational database tables.

If this might be an explanation for overly long query run times,
the `--dont-optimize` can be tried which will execute graph table
joins in the order they appear in strict and optional match clauses.
Be very careful using this, this is an **experts only** option.


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


<A NAME="kypher-v"></A>
## Kypher-V - querying vector data

Kypher-V supports import and queries over vector data.  Kypher-V
extends Kypher to allow work with unstructured data such as text,
images, and so on, represented by embedding vectors.  Kypher-V
provides efficient storage, indexing and querying of large-scale
vector data on a laptop.  It is fully integrated into Kypher to enable
expressive hybrid queries over Wikidata-size structured and
unstructured data.  To the best of our knowledge, this is the first
system providing such a functionality in a query language for
knowledge graphs.

<A NAME="vector-tables"></A>
### Vector tables are regular KGTK files

Kypher-V represents vectors as special kinds of literals that are
linked to KG objects via edges in KGTK format.  For example, the
following KGTK edge with ID `e4925` associates Wikidata node `Q40` (or
Austria) with a text embedding vector stored as the `node2` of the
edge.  The format below is something we commonly use where a `node1`
points to a vector literal in `node2` via an `emb` edge, but there is
nothing special about this particular representation pattern or edge
label, any scheme can be used that associates a node or edge ID with a
vector:

| id    |  node1 | label   |   node2                                        |
|-------|--------|---------|------------------------------------------------|
| e4925 |  Q40   | emb     |   "[0.1642,-0.5445,-0.3673,...,0.3203,0.6090]" |

When vector data is queried, it is imported and cached if necessary
just like any other KGTK data processed by Kypher.  The main
difference is that for faster query processing vector literals get
translated into binary format first before they are stored in the
Kypher graph cache based on an indexing directive.  Various up-front
transformations such as data type conversions, normalization, storage
type, etc. can also be controlled here.  Finally, vector files are
treated as large contiguous and homogeneous arrays, so that vectors can
be referenced and accessed efficiently by vector table row ID instead
of having to use an index.


### Vector literal formats

Kypher-V supports a number of different vector literal formats listed
in the table below.  Not all of them are valid KGTK according to the
current KGTK data model.  The canonical representation we will use in
the documentation here is the "vector as string" format listed in the
first row of the table.  Future versions of KGTK might support a
bonafide vector literal type as shown in row 4.  Also note that any
number of different separator characters from the set `,;:|` and space
can be used in any of the text formats, an example of which is shown
in row 5.  Any extra whitespace is legal and will be ignored.
Finally, Base64 encoding of binary vector data is also supported shown
in the last two rows:

|   vector literal                               | description        | valid KGTK |
|------------------------------------------------|--------------------|------------|
|   "[0.1642,-0.5445,-0.3673,...,0.3203,0.6090]" | vector as string   | yes        |
|   "0.1642,-0.5445,-0.3673,...,0.3203,0.6090"   | list as string     | yes        |
|   0.1642,-0.5445,-0.3673,...,0.3203,0.6090     | list               | no         |
|   [0.1642,-0.5445,-0.3673,...,0.3203,0.6090]   | vector             | not yet    |
|   0.1642 -0.5445 -0.3673 ... 0.3203 0.6090     | space-sep. list    | no         |
|   "1yO6PYj7Gb8KX2i9Pqc+vt...T63OGG92B3cPg=="   | base64 as string   | yes        |
|   1yO6PYj7Gb8KX2i9Pqc+vt...T63OGG92B3cPg==     | base64             | no         |

Binary representation is purely a contiguous set of bytes representing
an array of floating point numbers.  It does not have any
meta-information or header describing number of dimensions or element
type.  For that reason, conversion into an actual vector object will
always require an explit or implict element data type specification
(NumPy's `dtype`) which can come from a number of different sources.


### Vector import

Once we have a KGTK file with vector literals, we can import it just
like any other KGTK file with the `query` command.  In the following
we will use this example dataset of embedding vectors called `EMBED`
which associates a small subset of Wikidata nodes with 100-dimensional
ComplEx embedding vectors:

```
EMBED=examples/docs/query-embed.tsv.gz
 
zcat $EMBED | head -3
```
Result:

| id         |  node1       | label   |   node2                         |
|------------|--------------|---------|---------------------------------|
| e-3bc7d18e |  Q100428034  | emb     |  "[-0.10816555,...,0.44566953]" |
| e-ecf67b59 |  Q10061      | emb     |  "[-0.10639298,...,0.59102327]" |

!!! note
    **Important:** A vector file needs to be homogenous, which
    means that each row has to contain a vector, each vector has to
    have the same element type and number of dimensions, and each
    vector literal uses the same format and separator.  Vector tables
    are treated as large homogenous arrays, which means each row has
    to have the same size and element type.

Next we import the data using a `query` command.  The important option
here is `--idx` which tells the system that this input data contains a
vector column.  We accept the default values for most of the possible
options and only tell Kypher-V that it should use a vector index here
(indicated by the `vector` index type) and that the vector data
resides in the `node2` column.  We also create a standard index on
the `node1` column using the `mode:valuegraph` directive, so we can
quickly look up the embedding vector for a given node:

```
kgtk query -i $EMBED --idx vector:node2 mode:valuegraph --limit 2
```
Result:

| id         |  node1     | label   |   node2                         |
|------------|------------|---------|---------------------------------|
| e-3bc7d18e | Q100428034 | emb     | b'\xe6\x85\xdd....\xcc.\xe4>'   |
| e-ecf67b59 | Q10061     | emb     | b'\x90\xe4\xd9....\x8e=MM\x17?' |

The returned values look identical to the input file except for the
vector column.  Vectors where transformed into byte arrays stored as
SQLite BLOB values, displayed here in a Python byte string format.

!!! note
    **Important:** The byte strings shown here are not a valid KGTK
    vector format, they are usually not output and only used internally.
    One of the vector output functions described below needs to be used
    to convert them into valid KGTK vector literals.
    
Here is a minimal vector import command variant that also leaves out
the column specification, since `node2` is the default value.
**IMPORTANT**: the colon at the end of `vector:` is mandatory here to
designate this as a vector index type prefix, without it, the system
would interpret it as the name of a column to index with a standard
table index:

```
kgtk query -i $EMBED --idx vector: mode:valuegraph --limit 2
```


### Vector storage options

Kypher-V implements scalable and efficient disk-based vector storage
that allows fast vector lookup, indexing and processing without
requiring large amounts of RAM.  After vectors are imported and indexed,
vector queries can be run efficiently from scratch without having to
load large amounts of data into memory.

Kypher-V supports a number of different ways to store vectors in the database.
They could be stored inline as BLOB values in a KGTK graph table, they could
be in memory-mapped NumPy disk files, and an HD5-based disk format is also
available.  At the moment only inline storage is fully supported, and the
NumPy and HD5 storage options are considered experimental and in flux.

When vectors are brought into memory to be processed in some form by a
query, they are first converted to Python's
[NumPy](https://numpy.org/) format.  Vectors are stored on disk in a
binary byte format that mirrors the data in a NumPy vector, so
creating vector objects is a very fast copy operation.  The Faiss
nearest neighbor indexing package uses its own internal vector format
which also can be created very efficiently from NumPy vectors.

The vector index directive takes a number of options to control
storage, preprocessing and indexing of vectors.  These are specified
as column options on the vector column of a vector table.  The first
set of options are storage options which control how vectors are
imported, converted, normalized and stored in the database, they
are described below:

| Storage option            | Description                                                                                                      |
|---------------------------|------------------------------------------------------------------------------------------------------------------|
| fmt                       | Format of the data in the vector column, must be one of `text`, `base64` or `auto` (the default).  `text` is for any text list of numbers separated by one of `,;:|` or space that can be parsed by NumPy's `fromstring` (extra whitespace will be ignored), `base64` is a Base64 encoding of a NumPy vector, `auto` tries to guess the format based on the first vector |
| dtype                     | NumPy element data type to use for the imported vectors, one of `float16`, `float32` (the default) or `float64`  |
| norm                      | whether vectors will be normalized before they are stored and how, one of `true`, `false` (the default) or `l2` (only normalization currently supported).  The norm will be stored as well so it can be used to unnormalize a vector if needed.                                              |
| store                     | controls how imported vectors should be stored, one of `inline` (the default), `numpy` or `hd5`, but only `inline` is fully supported for now and `hd5` will likely go away  |
| ext                       | an external file to use for a NumPy store - experimental, see `store`, experts only                              |

`dtype` can be used to control the precision of the stored vectors as
well as the required storage space.  However, if nearest neighbor
indexing is used it should generally be left at the default value,
since 32-bit float values are used throughout the Faiss indexing
package.  A different dtype will be converted dynamically to 32-bit
whenever vectors are loaded from the database.

In this example we specify a number of these options explicitly with
their default values:

```
kgtk query -i $EMBED \
     --idx vector:node2/fmt=auto/dtype=float32/store=inline/norm=False mode:valuegraph \
     --limit 2
```
Result:

| id         |  node1     | label   |   node2                         |
|------------|------------|---------|---------------------------------|
| e-3bc7d18e | Q100428034 | emb     | b'\xe6\x85\xdd....\xcc.\xe4>'   |
| e-ecf67b59 | Q10061     | emb     | b'\x90\xe4\xd9....\x8e=MM\x17?' |

It is possible to have more than one vector column in a vector table.  In that case a separate
vector index option needs to be supplied for each column, for example:

```
kgtk query ... --idx vector:node2 --idx 'vector:`node1;emb2`/dtype=float16' ...
```

Unless for special circumstances, however, this should be avoided.
Nearest neighbor indexing will sort tables for optimal data locality
which generally can only produce good results for a single vector
column (unless the different vector columns cluster very similarly).


### Vector functions

Vector functions take one or more vectors accessed in a query and
compute a function based on those vectors.  The following example
shows one of the similarity functions available in Kypher-V.  It
accesses embedding vectors for two given Wikidata QNodes `Q868` and
`Q913` in our small `EMBED` dataset, computes cosine similarity
between them and then displays the result with their labels (imported
from the associated `LABELS` graph):

```
LABELS=examples/docs/query-embed-labels.tsv.gz

kgtk query -i $EMBED -i $LABELS \
     --match 'emb:    (x:Q868)-[]->(xv), \
                      (y:Q913)-[]->(yv), \
              labels: (x)-[]->(xl), \
                      (y)-[]->(yl)' \
     --return 'xl as xlabel, yl as ylabel, kvec_cos_sim(xv, yv) as sim'
```
Result:

| xlabel          | ylabel         | sim                |
|-----------------|----------------|--------------------|
| 'Aristotle'@en  | 'Socrates'@en  | 0.6926078796386719 |


<A NAME="builtin-vector-functions"></A>
The following vector functions are available:

| Function                    | Description                                                                                                    |
|-----------------------------|----------------------------------------------------------------------------------------------------------------|
| kvec_plus(x,y)              | Compute elementwise addition `x + y` between two vectors and/or numbers (`numpy.add`). If at least one argument is a vector, the result will also be a vector.               |
| kvec_minus(x,y)             | Compute elementwise subtraction `x - y` between two vectors and/or numbers (`numpy.subtract`). If at least one argument is a vector, the result will also be a vector.       |
| kvec_times(x,y)             | Compute elementwise multiplication `x * y` between two vectors and/or numbers (`numpy.multiply`). If at least one argument is a vector, the result will also be a vector.    |
| kvec_divide(x,y)            | Compute elementwise division `x / y` between two vectors and/or numbers (`numpy.divide`). If at least one argument is a vector, the result will also be a vector.            |
| kvec_l0_norm(x)             | Compute the L0-Norm of vector `x`, counts the number of non-zero elements (see `numpy.linalg.norm(x, ord=0)`)  |
| kvec_l1_norm(x)             | Compute the L1-Norm of a vector, computes the sum of elements in `x`, aka Manhattan distance (see `numpy.linalg.norm(x, ord=1)`)     |
| kvec_l2_norm(x)             | Compute the L2-Norm or Euclidean norm or Euclidean length of vector `x` (see `numpy.linalg.norm(x, ord=2)`)    |
| kvec_dot(x,y)               | Compute the dot product between vectors `x` and `y`.                                                           |
| kvec_cos_sim(x,y)           | Compute cosine similarity between vectors `x` and `y`.  If vectors are known to be L2-normalized, this will automatically substitute `kvec_dot`. |
| kvec_euclid_dist(x,y)       | Compute the Euclidean distance between vectors `x` and `y`.                                                    |
| kvec_stringify(x)           | Convert a vector `x` into text format as a KGTK string.  Calls `kgtk_stringify` for non-vectors.               |
| kvec_unstringify(x)         | Convert a vector `x` from text format to vector bytes.  Return `x` for non-vector strings.                     |
| kvec_to_base64(x,[dtype])   | Convert a vector `x` into base64 format wrapped as a KGTK string.  Returns null for non-vectors.  The optional `dtype` argument specifies the target element dtype before base64 conversion (defaults to `float32`). |
| kvec_from_base64(x,[dtype]) | Convert a vector `x` from base64 format into vector bytes.  Returns null for non-vectors.  The optional `dtype` argument specifies the element dtype of the source vector `x` (defaults to `float32`).             |


#### Vector function notes

* vector inputs must be in internal byte format either coming from an imported vector table
  or from a vector generating function such as `kvec_unstringify`
* functions that take more than one vector as inputs (e.g., `kvec_cos_sim`) assume all
  vectors to have the same dimensions
* functions that produce vectors as their output will use `float32` as the element type
  of the vectors they are producing; it is currently not possible to customize this
  except for import and output via `kvec_to/from_base64`
* input and output functions such as `kvec_unstringify` should only be used in one-off/
  one-time situations, for example, to produce a new dataset, since they are much less
  efficient than using the binary vectors created during a vector table import; importing
  and exporting bytes via `base64` encoding functions is many times faster than using
  their text-based analogs which have to parse and print floating point values
  
For example, here is a query that produces a 100-D unit vector on the fly to compute
a similarity value:

```
kgtk query -i $EMBED -i $LABELS \
     --match 'emb:    (x:Q868)-[]->(xv), \
              labels: (x)-[]->(xl)' \
     --return 'xl as xlabel, kvec_cos_sim(xv, kvec_unstringify(pyeval("[1] * 100"))) as sim'
```
Result:

| xlabel          | sim                  |
|-----------------|----------------------|
| 'Aristotle'@en  | 0.003323602257296443 |

Here we compute a cosine-similarity through combination of vector normalization and dot-product:

```
kgtk query -i $EMBED -i $LABELS \
     --match 'emb:    (x:Q868)-[]->(xv), \
                      (y:Q913)-[]->(yv), \
              labels: (x)-[]->(xl), \
                      (y)-[]->(yl)' \
     --return 'xl as xlabel, yl as ylabel, kvec_dot(kvec_divide(xv, kvec_l2_norm(xv)), kvec_divide(yv, kvec_l2_norm(yv))) as sim'
```
Result:

| xlabel          | ylabel         | sim                |
|-----------------|----------------|--------------------|
| 'Aristotle'@en  | 'Socrates'@en  | 0.6926079392433167 |


### Similarity search

A core functionality provided by Kypher-V is similarity search, which
allows us to find the top-*k* similar nodes for one or more nodes
generated by a query based on embedding vectors linked to those nodes.
Most importantly, these searches can be closely integrated with
structured restriction as in the following high-level example queries:

* Find castle ruins similar to Beaumaris Castle that are located in Austria
* Find dresses similar to this [image] with price <= $50 and free 2-day shipping

For example, we can use one of the Kypher-V similarity functions to compute the
top-*k* similar nodes for a given node in a brute-force way.  To do that we
simply enumerate all embedding vectors in this data and compare each of them
to the one for Socrates (`Q913`), then we sort and report the top-5 results:

```
kgtk query -i $EMBED -i $LABELS \
     --match 'emb:     (x:Q913)-[:emb]->(xv), \
                       (y)-[:emb]->(yv), \
              labels:  (x)-[]->(xl), \
                       (y)-[]->(yl)' \
     --return 'x as x, xl as xlabel, y as y, yl as ylabel, kvec_cos_sim(xv, yv) as sim' \
     --order  'sim desc' \
     --limit 5
```
Result:

| x    | xlabel        | y       | ylabel                     | sim                |
|------|---------------|---------|----------------------------|--------------------|
| Q913 | 'Socrates'@en | Q913    | 'Socrates'@en              | 1.0                |
| Q913 | 'Socrates'@en | Q179149 | 'Antisthenes'@en           | 0.8249946236610413 |
| Q913 | 'Socrates'@en | Q409647 | 'Aeschines of Sphettus'@en | 0.8141517043113708 |
| Q913 | 'Socrates'@en | Q666230 | 'Aristobulus of Paneas'@en | 0.8014461994171143 |
| Q913 | 'Socrates'@en | Q380190 | 'Phaedo of Elis'@en        | 0.7857708930969238 |


Despite the brute-force nature of the search, this query was very
fast, since the dataset is very small and has only about 850 vectors
in total.  On more realistic data - for example all humans in Wikidata
with about 9 million elements - this becomes very inefficient (4
minutes on a laptop) and we will use nearest neighbor indexing
described below to speed things up.


### Indexed similarity search

For much faster similarity search over large datasets, we use an
approximate nearest neighbor search (ANNS) index that can be
constructed with a vector index directive when data is imported, or
sometime later when it is actually needed.

Indexed vector search is expressed via a *virtual* graph edge
`kvec_topk_cos_sim` which is implemented via an SQLite virtual table
(a custom computation that can generate multiple rows and behaves like
a regular table).  Virtual edges are a Kypher-V extension to Cypher
that take a number of user-specified input parameters expressed in
Cypher property syntax.  The parameter shown here is `k` controlling how
many results to return, others are left at their default values.  At this
point, the query generates an error, since no appropriate index has
been constructed yet:

```
kgtk query -i $EMBED -i $LABELS \
     --match 'emb:     (x:Q913)-[]->(xv), \
                       (xv)-[r:kvec_topk_cos_sim {k: 10}]->(y), \
              labels:  (x)-[]->(xl), \
                       (y)-[]->(yl)' \
     --return 'x as x, xl as xlabel, y as y, yl as ylabel, r.similarity as sim' \
     --limit 5
Traceback (most recent call last):
  .....
kgtk.exceptions.KGTKException: no trained nearest neighbor index available for 'kvec_topk_cos_sim_0'
SQL logic error
```

Different from regular graph table indexes which can be built by
Kypher automatically behind the scenes, ANNS indexes can be quite
expensive to generate and might require a number of user-specified
parameters to control index creation time and quality.  For this
reason, an explicit index directive is required (somewhat similar to
what we do for [**text search indexes**](#text-search-functions)).

Let's run this query again but this time create an ANNS index for it
controlled by the `--idx` option on the embedding input.  The relevant
new options controlling ANNS index creation start at `/nn/` (for
nearest neighbor index).  Since it is such a small file, we only
create 8 quantizer cells for it (the value of `nlist`).  We run the
query with the `--debug` option, so we can see what the system is doing
behind the scenes:

```
kgtk --debug query \
     -i $EMBED --idx vector:node2/nn/nlist=8 mode:valuegraph \
     -i $LABELS \
     --match 'emb:     (x:Q913)-[]->(xv), \
                       (xv)-[r:kvec_topk_cos_sim {k: 10}]->(y), \
              labels:  (x)-[]->(xl), \
                       (y)-[]->(yl)' \
     --return 'x as x, xl as xlabel, y as y, yl as ylabel, r.similarity as sim' \
     --limit 5
[2022-11-08 19:15:14 sqlstore]: DROP VECTOR INDEX sdict['type': 'vector', 'columns': sdict['node2': sdict['fmt': 'auto', 'dtype': 'float32', 'norm': None, 'store': 'inline', 'ext': None, 'nn': False, 'ram': None, 'nlist': None, 'niter': None, 'nprobe': None]], 'options': {}]...
[2022-11-08 19:15:14 sqlstore]: CREATE VECTOR INDEX sdict['type': 'vector', 'columns': sdict['node2': sdict['nn': 'faiss', 'nlist': 8, 'fmt': 'auto', 'dtype': 'float32', 'norm': None, 'store': 'inline', 'ext': None, 'ram': None, 'niter': None, 'nprobe': None]], 'options': {}]...
[2022-11-08 19:15:14 sqlstore]: Selecting random sample of 859 training vectors...
[2022-11-08 19:15:14 sqlstore]: Training vector store quantizer:
Clustering 859 points in 100D to 8 clusters, redo 1 times, 10 iterations
  Preprocessing in 0.00 s
  Iteration 9 (0.01 s, search 0.01 s): objective=4772.23 imbalance=1.626 nsplit=0       
[2022-11-08 19:15:14 sqlstore]: 

[2022-11-08 19:15:14 sqlstore]: Quantizing 859 vectors in batches of size 859...
.
[2022-11-08 19:15:14 sqlstore]: Adding quantization index to database...
[2022-11-08 19:15:14 sqlstore]: SORT table 'graph_1' batch 1 of 2...
[2022-11-08 19:15:14 sqlstore]: SORT table 'graph_1' batch 2 of 2...
[2022-11-08 19:15:14 sqlstore]: CREATE INDEX "graph_1_node2;_kgtk_vec_qcell_idx" ON "graph_1" ("node2;_kgtk_vec_qcell")
[2022-11-08 19:15:14 sqlstore]: ANALYZE "graph_1_node2;_kgtk_vec_qcell_idx"
[2022-11-08 19:15:14 query]: SQL Translation:
---------------------------------------------
  SELECT graph_1_c1."node1" "_aLias.x", graph_2_c3."node2" "_aLias.xlabel", kvec_topk_cos_sim_0_c_1."node2" "_aLias.y", graph_2_c4."node2" "_aLias.ylabel", kvec_topk_cos_sim_0_c_1."similarity" "_aLias.sim"
     FROM graph_1 AS graph_1_c1
     CROSS JOIN kvec_topk_cos_sim_0 AS kvec_topk_cos_sim_0_c_1 CROSS JOIN graph_2 AS graph_2_c3 CROSS JOIN graph_2 AS graph_2_c4
     ON graph_1_c1."node1" = graph_2_c3."node1"
        AND graph_1_c1."node2" = kvec_topk_cos_sim_0_c_1."node1"
        AND kvec_topk_cos_sim_0_c_1."node2" = graph_2_c4."node1"
        AND graph_1_c1."node1" = ?
        AND kvec_topk_cos_sim_0_c_1."k" = ?
     LIMIT ?
  PARAS: ['Q913', 10, 5]
---------------------------------------------
```
Result:

| x    | xlabel        | y       | ylabel                     | sim                |
|------|---------------|---------|----------------------------|--------------------|
| Q913 | 'Socrates'@en | Q913    | 'Socrates'@en              | 1.0                |
| Q913 | 'Socrates'@en | Q179149 | 'Antisthenes'@en           | 0.8249946236610413 |
| Q913 | 'Socrates'@en | Q409647 | 'Aeschines of Sphettus'@en | 0.8141517043113708 |
| Q913 | 'Socrates'@en | Q666230 | 'Aristobulus of Paneas'@en | 0.8014461994171143 |
| Q913 | 'Socrates'@en | Q380190 | 'Phaedo of Elis'@en        | 0.7857708930969238 |

In subsequent queries the `--idx` option can be omitted (just as with other index
types).  If the option is identical to previous queries, it will simply be ignored.
If some of the option values changed, however, the index will be rebuilt.

Except for datasets that are very large or very small like this one,
ANNS index options can generally be left unspecified at their default
values.  For a more exhaustive discussion of available indexing
options and the tradeoffs involved see the section on [**ANNS
indexes**](#anns-indexes).


#### Indexed similarity search parameters

The `kvec_topk_cos_sim` computed graph edge takes a number of required
and optional input parameters to control processing and a number of
output parameters to return results.  We further divide these parameters
into those that control search, and a second experimental set that
implements more efficient batched processing for large joins.

We use Kypher's edge property syntax to attach and refer to these
properties.  For example, if we have an edge identified by the
variable `r`, then `r.node1` is that edge's `node1`, `r.node2` is that
edge's `node2`, `r.nprobe` is its `nprobe` value, `r.similarity` the
computed similarity, and so on.  The two tables below list search
input and output parameters:

| Input       | Description                                                                                                                          |
|-------------|--------------------------------------------------------------------------------------------------------------------------------------|
| node1       | input vector (bytes) for which we want to compute the top-`k` similar vectors                                                        |
| k           | **optional**: top-`k` similar vectors will be computed, defaults to 10                                                               |
| maxk        | **optional**: maximum `k` to try for vector joins with dynamic scaling, defaults to 0 which means no dynamic scaling should be used  |
| nprobe      | **optional**: number of closest q-cells to search to find similar vectors, defaults to `nprobe` option in `--idx` spec or 1          |

| Output      | Description                                                                                   |
|-------------|-----------------------------------------------------------------------------------------------|
| label       | canonical name of the virtual graph edge (constant)                                           |
| node2       | `node1` from this similar vector's row in the vector table which will (typically) be its key  |
| vid         | edge ID of this similar vector's row in the vector table                                      |
| vrowid      | row ID of this similar vector's row in the vector table                                       |
| vector      | bytes of this similar vector                                                                  |
| similarity  | cosine similarity of this similar vector to the respective input vector provided in `node1`   |

Let us look at a variant of our previous example that exercises more
of those input and output options.  For example, below we leave `k`
unspecified which will use its default value 10, we set `nprobe` to 8
using property syntax on the edge (but this restriction could also be
supplied in the `--where` clause with `r.nprobe = 8`), we exclude `x`
as a result and constrain the minimum similarity required, and we
return additional output fields `r.vid` and `r.vector` which all come
from the row in the `EMBED` vector table where `y` and `yv` are
defined:

```
kgtk query \
     -i $EMBED --idx vector:node2/nn/nlist=8 mode:valuegraph \
     -i $LABELS \
     --match 'emb:     (x:Q913)-[]->(xv), \
                       (xv)-[r:kvec_topk_cos_sim {nprobe: 8}]->(y), \
              labels:  (x)-[]->(xl), \
                       (y)-[]->(yl)' \
     --where  'x != y and r.similarity >= 0.8' \
     --return 'x as x, xl as xlabel, y as y, yl as ylabel, r.similarity as sim, r.vid as yvid, kvec_to_base64(r.vector) as yv'
```
Result:

| x    | xlabel        | y       | ylabel                     | sim                | yvid       | yv               |
|------|---------------|---------|----------------------------|--------------------|------------|------------------|
| Q913 | 'Socrates'@en | Q179149 | 'Antisthenes'@en           | 0.8249946236610413 | e-ea594b00 | "LDeC....YNPw==" |
| Q913 | 'Socrates'@en | Q409647 | 'Aeschines of Sphettus'@en | 0.8141517043113708 | e-0685ee35 | "5lOZ....BdPw==" |
| Q913 | 'Socrates'@en | Q666230 | 'Aristobulus of Paneas'@en | 0.8014461994171143 | e-2906ba9a | "Ex++....oMPw==" |


### Full vector similarity joins

Suppose we want to ask the following question: Given a set of
philosophers (Plato, Aristotle and Socrates), find the top-5 similar
humans for each of them who are also writers.  We use a small Wikidata
`CLAIMS` graph that has additional information we need for this query.
In Wikidata humans are entities that are instances (`P31`) of human
(`Q5`), and writers are nodes with occupation (`P106`) writer
(`Q36180`).  See [**Wikidata**](https://www.wikidata.org/) for more
information on this data model.  A first attempt to answer this
question might look like this:

```
CLAIMS=examples/docs/query-embed-claims.tsv.gz 

kgtk query \
     -i $EMBED --idx vector:node2/nn/nlist=8 mode:valuegraph \
     -i $LABELS \
     -i $CLAIMS \
     --match 'emb:     (x)-[]->(xv), \
                       (xv)-[r:kvec_topk_cos_sim {k: 5}]->(y), \
              claims:  (y)-[:P31]->(:Q5), \
                       (y)-[:P106]->(:Q36180), \
              labels:  (x)-[]->(xl), \
                       (y)-[]->(yl)' \
     --where  'x in ["Q859", "Q868", "Q913"]' \
     --return 'x as x, xl as xlabel, y as y, yl as ylabel, r.similarity as sim'
```
Result:

| x    | xlabel         | y      | ylabel           | sim                |
|------|----------------|--------|------------------|--------------------|
| Q859 | 'Plato'@en     | Q41155 | 'Heraclitus'@en  | 0.7475227117538452 |
| Q859 | 'Plato'@en     | Q83375 | 'Empedocles'@en  | 0.7423468232154846 |
| Q868 | 'Aristotle'@en | Q868   | 'Aristotle'@en   | 1.0                |
| Q868 | 'Aristotle'@en | Q10261 | 'Pythagoras'@en  | 0.769469141960144  |
| Q868 | 'Aristotle'@en | Q5264  | 'Hippocrates'@en | 0.7553266286849976 |

Surprisingly, the result seems somewhat incomplete.  We only get matches
for two of the three seeds, and for both of them we get less than what we
asked for.  What is going on here?

The answer to the mystery is that `kvec_topk_cos_sim` found the top-5 similar
vectors relative to the *whole universe* of vectors *U* in the `EMBED` dataset.
Once those 5 matches were computed for each seed, they were further filtered
by the additional `P31` and `P106` leaving us with the results we saw above.

What we really want for this query is a true similarity join between
the set *P* of philosophers (Plato, Aristotle and Socrates), and
the set *W* of human writers.  For each node *p* in *P* a similar node *s*
should be in the join result if it is one of the top-5 similar nodes
of *p* in *W*, but not in *U* which is a much larger set.

To find those additional matches we use a process called *dynamic scaling*
which progressively increases *k* until enough results matching the join
condition have been found.  We use the `maxk` property to tell Kypher-V
to use dynamic scaling and also where to stop which is important, since
we might never find enough qualifying matches.  Here we ask the query again
with `maxk: 100` and now we get the results we expect.  Note how the similarities
for Socrates' matches are significantly lower than what we computed in
previous queries, since we now have to go farther down the list to find
matches that also satisfy the additional restrictions:

```
kgtk query \
     -i $EMBED --idx vector:node2/nn/nlist=8 mode:valuegraph \
     -i $LABELS \
     -i $CLAIMS \
     --match 'emb:     (x)-[]->(xv), \
                       (xv)-[r:kvec_topk_cos_sim {k: 5, maxk: 100}]->(y), \
              claims:  (y)-[:P31]->(:Q5), \
                       (y)-[:P106]->(:Q36180), \
              labels:  (x)-[]->(xl), \
                       (y)-[]->(yl)' \
     --where  'x in ["Q859", "Q868", "Q913"]' \
     --return 'x as x, xl as xlabel, y as y, yl as ylabel, r.similarity as sim'
```
Result:

| x    | xlabel         | y       | ylabel               | sim                |
|------|----------------|---------|----------------------|--------------------|
| Q859 | 'Plato'@en     | Q41155  | 'Heraclitus'@en      | 0.7475227117538452 |
| Q859 | 'Plato'@en     | Q83375  | 'Empedocles'@en      | 0.7423468232154846 |
| Q859 | 'Plato'@en     | Q5264   | 'Hippocrates'@en     | 0.7279533743858337 |
| Q859 | 'Plato'@en     | Q868    | 'Aristotle'@en       | 0.7331432104110718 |
| Q859 | 'Plato'@en     | Q1430   | 'Marcus Aurelius'@en | 0.7032168507575989 |
| Q868 | 'Aristotle'@en | Q868    | 'Aristotle'@en       | 1.0                |
| Q868 | 'Aristotle'@en | Q10261  | 'Pythagoras'@en      | 0.769469141960144  |
| Q868 | 'Aristotle'@en | Q5264   | 'Hippocrates'@en     | 0.7553266286849976 |
| Q868 | 'Aristotle'@en | Q41155  | 'Heraclitus'@en      | 0.7392288446426392 |
| Q868 | 'Aristotle'@en | Q271809 | 'Proclus'@en         | 0.7256468534469604 |
| Q913 | 'Socrates'@en  | Q271809 | 'Proclus'@en         | 0.7659962773323059 |
| Q913 | 'Socrates'@en  | Q5264   | 'Hippocrates'@en     | 0.7673165798187256 |
| Q913 | 'Socrates'@en  | Q1430   | 'Marcus Aurelius'@en | 0.7595204710960388 |
| Q913 | 'Socrates'@en  | Q10261  | 'Pythagoras'@en      | 0.751109778881073  |
| Q913 | 'Socrates'@en  | Q83375  | 'Empedocles'@en      | 0.7441204190254211 |

Of course, we could have simply used a much larger `k` to find all
these matches.  But that would have led to very unbalanced result sets
and possibly a lot of unnecessary processing.  We also can't really use
a limit to effectively give us what we want as can be seen in this
query, where Plato's matches dominate and block out others:

```
kgtk query \
     -i $EMBED --idx vector:node2/nn/nlist=8 mode:valuegraph \
     -i $LABELS \
     -i $CLAIMS \
     --match 'emb:     (x)-[]->(xv), \
                       (xv)-[r:kvec_topk_cos_sim {k: 50}]->(y), \
              claims:  (y)-[:P31]->(:Q5), \
                       (y)-[:P106]->(:Q36180), \
              labels:  (x)-[]->(xl), \
                       (y)-[]->(yl)' \
     --where  'x in ["Q859", "Q868", "Q913"]' \
     --return 'x as x, xl as xlabel, y as y, yl as ylabel, r.similarity as sim' \
     --limit 15
```
Result:

| x    | xlabel         | y       | ylabel                               | sim                |
|------|----------------|---------|--------------------------------------|--------------------|
| Q859 | 'Plato'@en     | Q41155  | 'Heraclitus'@en                      | 0.7475227117538452 |
| Q859 | 'Plato'@en     | Q83375  | 'Empedocles'@en                      | 0.7423468232154846 |
| Q859 | 'Plato'@en     | Q868    | 'Aristotle'@en                       | 0.7331432104110718 |
| Q859 | 'Plato'@en     | Q5264   | 'Hippocrates'@en                     | 0.7279533743858337 |
| Q859 | 'Plato'@en     | Q1430   | 'Marcus Aurelius'@en                 | 0.7032168507575989 |
| Q859 | 'Plato'@en     | Q10261  | 'Pythagoras'@en                      | 0.6969254612922668 |
| Q859 | 'Plato'@en     | Q125551 | 'Parmenides'@en                      | 0.6939566135406494 |
| Q859 | 'Plato'@en     | Q47154  | 'Lucretius'@en                       | 0.6934449076652527 |
| Q859 | 'Plato'@en     | Q271809 | 'Proclus'@en                         | 0.6883948445320129 |
| Q859 | 'Plato'@en     | Q59138  | 'Diogenes Laërtius'@en               | 0.6805305480957031 |
| Q859 | 'Plato'@en     | Q313924 | 'Nicolaus of Damascus'@en            | 0.6774346232414246 |
| Q859 | 'Plato'@en     | Q175042 | 'Nigidius Figulus'@en                | 0.6490164995193481 |
| Q859 | 'Plato'@en     | Q561367 | 'Lucius Aelius Stilo Praeconinus'@en | 0.6464878916740417 |
| Q868 | 'Aristotle'@en | Q868    | 'Aristotle'@en                       | 1.0                |
| Q868 | 'Aristotle'@en | Q10261  | 'Pythagoras'@en                      | 0.769469141960144  |

A planned extension to the dynamic scaling mechanism is to allow the
specification of a minimum similarity threshold to control the depth
of the search (instead of `maxk`).  Note that this is different from
using a where-clause restriction such as `r.similarity >= 0.8`.


### Batched vector similarity joins

WRITE ME - Experimental support to compute similar nodes in batches to
better exploit Faiss parallel processing.


### ANNS indexes

Kypher-V uses a custom disk-based ANNS index architecture based on
[Faiss](https://ai.facebook.com/tools/faiss/).  Generic Faiss is
main-memory oriented requiring lots of RAM, which has some disadvantages
for our purposes:

* Very limited support for disk-based indexes
* High startup cost due to initial index-load time which would require
  a server-based architecture to amortize the cost
* To index 180GB of text embedding vectors requires at least that much
  RAM (unless encoding / product quantization / compression is used
  which is also expensive to compute)
* Hosting and using multiple sets of embeddings simultaneously quickly
  becomes very resource intensive and cost prohibitive

Instead we use a database-centric index architecture for Kypher-V
which can be loaded quickly and requires much less RAM and computing
resources.

The basic idea behind ANNS indexing is to partition or *quantize* a
vector space into a set of quantization cells (or *q-cells*), and then
assign each embedding vector to its closest q-cell.  At query time we
then compare a vector only to vectors from its (and a few neighboring
q-cells) instead of every vector in the dataset, which greatly reduces
search time.  See this tutorial on [Faiss ANNS
indexing](https://www.pinecone.io/learn/faiss-tutorial/) for a good
introduction to the topic.  Two important parameters in this process
are `nlist` (the number of q-cells or cluster centroids or inverted
lists to use in the quantization), and `nprobe` (how many neighboring
q-cells to search when looking for similar vectors).  These parameters
are referenced in various places below.

Kypher-V goes through the following steps when creating an ANNS index
(compare to the debug output from the example query above):

1. K-means clustering of vectors with the standard Faiss API which involves:
    * Sampling the vector set to limit memory use (for example, 180GB of
      text embedding vectors can be clustered with 25GB of RAM on a laptop)
    * Clustering the sample, the resulting cluster centroids form the basis of
      the quantization index
    * Save cluster centroids via Faiss to a small file which can be loaded quickly,
      for example, for our largest dataset so far with 16K 1024-D cluster centroids
      this file is 67MB in size which loads in about 50ms
2. Quantization assigns data vectors to their closest q-cell centroid
    * Q-cell IDs are written as extra q-cell column to the vector database table
    * DB indexing of the q-cell column allows quick access to all vectors
      of a q-cell (this implements a DB version of Faiss inverted lists)
3. Sorting of vectors by q-cell ID to improve disk locality
    * Now all vectors of a q-cell can be retrieved via one or few disk accesses
    * Batched sorting reduces temp disk usage (temp space < 50% of table size)

Then at query time, we do the following to load and exploit an ANNS index:

1. Load cluster centroids from saved Faiss file
    * This is one-time only and fast (50ms or less) and can be amortized over multiple
      queries when using the Kypher API
    * Creates a `faiss.IndexFlat` quantizer index object from the centroid vectors
2. Quantize an input vector identified by a query
    * Find the `nprobe` q-cell centroids it is closest to (we usually search in
    `nprobe > 1` q-cells to handle vectors close to a q-cell boundary)
3. Dynamically and incrementally create a size-limited in-memory Faiss search index
   for the vectors of the identified q-cells
    * Create a `faiss.IndexIVFFlat` object using the flat quantizer loaded above
    * Load in all relevant q-cell vectors from the database using a DB index and query
    * Incrementally add the loaded vectors to this search index using Faiss' low-level API,
      this is very fast since we already know the q-cell each vector belongs to
    * Size-limited caching of this index reuses q-cells from prior vector inputs
      in a vector join query or over multiple queries (without using too much RAM)
4. Search top-`k` neighbors of each input vector in the dynamically
   constructed Faiss search index
    * Using the standard Faiss API which uses very fast parallel search


### ANNS indexing options

The following options control ANNS index creation:

| Indexing option | Description                                                                                                      |
|-----------------|------------------------------------------------------------------------------------------------------------------|
| nn              | whether an ANNS index should be built and of what kind, one of `true`, `false` (the default) or `faiss` (only type currently supported) | 
| ram             | the maximum amount of RAM (bytes) to use when training an NN index, supports standard memory units, default is 16G for `faiss`          |
| nlist           | the number of q-cells (centroids, inverted lists) to use for the ANNS index, defaults to closest power of 2 for 4K q-cell size          |
| niter           | how many iterations to use when training the ANNS index quantizer, default is 10 for `faiss`                                            |
| nprobe          | how many quantizer cells to search *by default* during ANNS queries, default is 1 for `faiss` (can be overridden in a query)            |

Except for very large datasets, all of these options can be left at
their default values.  Once datasets do become large (say O(10M) 1K-D
vectors and beyond), the `ram` value should be realistic to allow
clustering on smaller memory machines such as a laptop, or to exploit
available RAM on a large-scale compute server.  Note that this should
not be the total memory available on a machine, but what can be safely
dedicated to a clustering job that might run for several hours.  Below
we discuss in more detail how various dataset characteristics and
indexing options affect run time and quality of the generated ANNS
index.


### Rebuilding an ANNS index

WRITE ME - we can change parameters which will keep the data but rebuild the index


### ANNS indexing considerations

K-means clustering of a large number of high-dimensional vectors is
expensive.  The complexity is *O(ndki)* when *n* (or *ntotal*)
*d*-dimensional (or *ndim*) vectors are clustered into *k* (or
*nlist*) centroids in *i* (or *niter*) iterations (the parameters in
parentheses are the names used by Faiss and Kypher-V).  To keep run
time in check on large datasets, it is important to control these
factors very deliberately and carefully.

**Number of vectors** (*n* or *ntotal*): while this is generally
predetermined by a dataset, it pays to consider whether it would be
feasible to work with just a subset of vectors.  For example, datasets
such as Wikidata have large portions of very sparse nodes for which
graph or text embeddings might not be very informative, or it might be
sufficient to only have embeddings for certain types of nodes.  For a
given *n* Kypher-V will use sampling to cluster a dataset most
efficiently and within the given memory bounds.

**Vector dimension** (*d* or *ndim*): try to use the smallest number
of dimensions possible that provides adequate separation.  For
example, it might be possible to use 768-D instead of 1024-D text
embeddings for 25% savings in run time.

**Cluster centroids** (*k* or *nlist*): each cluster centroid defines
a q-cell in the resulting ANNS quantization index.  The more clusters
the longer it will take for clustering but the shorter search times
will be during queries because of smaller q-cells.  If clusters are
too small, larger `nprobe` values will be needed to consider enough
candidates.  If clusters are too large, the benefits of indexing will
be reduced.  A good value is an average cluster size of 4K which is
what the system will try to approximate if no explicit `nlist` value
is provided.  Moving that up or down a couple of powers of 2 can
adjust for specific dataset conditions.  Note that cluster sizes will
generally not be homogenous with some clusters much larger and others
much smaller than this average size.  This can lead to unbalanced
query times if a very large cluster needs to be searched during a query.

**Iterations** (*i* or *niter*): this controls the quality of the
resulting clusters with larger numbers producing higher quality
for the cost of longer run time.  Improvements from one to the next
iteration quickly diminish, and it is often not necessary to go
for the best possible clustering, since the improvements in average
query run time might be negligible.  For large datasets a single
iteration might take hour(s), so starting with a lower number and
possibly reclustering later if that is not good enough might be
a winning strategy.


### Controlling sampling and memory use

Faiss' K-Means clustering uses a high-performance parallel
implementation that exploits all available CPU cores and requires
vectors to be loaded into memory.  One of our large Wikidata text
embedding datasets has about 40 million 1024-D vectors.  With 32-bit
floats one vector requires 4K bytes to store.  To load all those
vectors into memory would require about 150GB of RAM (on top of any
other memory needs).  To reduce memory consumption and also clustering
run time both Faiss and Kypher-V use sampling (however, Faiss **will
require** all vectors to be loaded into memory to build the final
index, while Kypher-V does not).

Faiss and Kypher-V require between 39 and 256 vectors per desired
q-cell as training data to train the clusters.  Note that this is only
between 1-6% of the total data for a final q-cell size of 4K.  Given
available RAM (specified by the `ram` option), Kypher-V will pick the
maximum training data size in the interval [39,256] that can
comfortably fit into available RAM based on the number of desired
q-cells (the value of `nlist`) and randomly sample the data
accordingly.  If the data is so large that even at the lower end of
the interval it would exceed available RAM, a multi-batch clustering
strategy will be used that runs each clustering iteration in multiple
batches that do fit into available memory.  However, for such very
large datasets, using a large-scale compute server is recommended to
cut down on clustering time.

There is no indexing option available to explicitly control sampling.
To force the system to use a smaller sample size than the maximum of
256 samples per q-cell, a smaller than realistic `ram` value can be
used.  For example: a dataset with 55M 100-D vectors will require
about 6,700 q-cells of size 8K.  At 256 training vectors per q-cell,
this requires `6700 * 256 * 100 * 4 * 1.2 = 785MB` (1.2 is a fudge
factor).  Setting `ram=400M` will force the system to use only about
half of the data points for training which will speed up clustering by
a factor of two.


### Vector data import and indexing times

Here are some example vector data import and clustering times for
several different datasets.  Entries marked with a `*` were imported
from a network drive which added additional time.  All imports and
clusterings were performed on a Lenovo W541 Thinkpad laptop with 8
cores and 30GB of RAM.  DB size is the size of the resulting Kypher
graph cache on disk. NN-Index time combines clustering with vector
quantizing, sorting and DB indexing of the resulting database table.
The last column shows the relevant indexing options used that were
different from their default values.

| Dataset         | Type     | N    | Dim     | DB size | Import     | NN-Index   | Total      | <div style="width:300px"> --idx Options </div>            |
|-----------------|----------|------|---------|---------|------------|------------|------------|-----------------------------------------------------------|
| Wikidata        | ComplEx  | 53M  |  100    |  26GB   | 1.4 hours* | 1.1 hours  | 2.5 hours  | vector:node2/nn/ram=25g/nlist=16k mode:valuegraph         |
| Wikidata        | TransE   | 53M  |  100    |  26GB   | 25 min     | 2 hours    | 2.4 hours  | vector:node2/nn/ram=25g/nlist=16k mode:valuegraph         |
| Wikidata        | Text     | 39M  | 1024    | 182GB   | 8 hours*   | 11.5 hours | 19.5 hours | vector:node2/nn/ram=25g/nlist=16k mode:valuegraph         |
| Short abstracts | Text     | 5.9M |  768    | 24.5GB  | 16 min     | 28 min     | 44 min     | vector:node2/nn/ram=25g/nlist=2k/niter=20 mode:valuegraph |


### Kypher-V tips and tricks

* Start with default ANNS indexing options, then tweak some aspects
  through index redefinition if there are any issues (e.g., increase
  `nlist` and/or `niter`)
* Check imbalanced sizes of q-cells with a query like this:
  ```
  kgtk query ... --match '()-[r]->()' --return 'r.`node2;_kgtk_vec_qcell` as qcell, count(r.`node2;_kgtk_vec_qcell`) as count' --order 'count desc'
  ```
  Some imbalance is expected, but q-cells that contain O(100,000) or
  more vectors might cause performance problems.
* Import large embedding datasets into their own dedicated graph
  caches and then selectively use them in queries with the `--aux-cache`
  (or `--ac`) option.  This makes it easy to manage and throw away
  these very large files without affecting other imported data.
* Once vectors are imported, export smaller dedicated subsets like this:
  ```
  kgtk query ... --match 'emb: (x)-[r]->(xv), claims: (x)-[:P31]->(:Q5)' --return 'r as id, x as node1, "emb" as label, kvec_to_base64(xv) as node2'
  ```
* MORE TO COME
