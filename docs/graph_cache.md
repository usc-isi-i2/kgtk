## KGTK Graph Cache

The KGTK Graph Cache is a SQLite database containing copies of KGTK edge.
The Graph Cache was introduced with Kypher and the `kgtk query` command.
The Graph Cache may also be used with other KGTK commands (specifically, ones
that use KgtkReader to read KGTK input files).

For more details on the Graph Cache, see the documentation for the
[`kgtk query`](transform/query.md) command.

## Specifying the Location of the Graph Cache

The `--graph-cache grpah-cache-path` option specifies the location of the
Graph Cache to KGTK commands that use it.

If `--graph-cache` is not specified, some KGTK commands will look for the
envar `KGTK_GRAPH_CACHE` to find the path to the Graph Cache.  This behavior
may be suppressed with `--use-graph-cache-envar=false`.  The default value for
this option is `--use-graph-cache-envar=true".

## Stale Graph Cache Data

!!! info
    This section describes the behavior of KGTK commands other than `kgtk query`.

If a Graph Cache has been located and a KGTK input file has been found in the
Graph Cache as well as outside the Graph Cache, the data in the Graph Cache
will be considered stale if the file size or modification time stored for the
file in the Graph Cache do not match the file size or modification time of the
KGTK input file outside the Graph Cache.  The copy of the KGTK input file in the
Graph Cache will be ignored, and the copy outside the Graph Cache will be read.

If the option `--ignore-stale-graph-cache=false` is specified, then KGTK input
files found in the the Graph Cache will be used without performing the staleness
check.  The default value for this option is ``--ignore-stale-graph-cache=true`.
There are limited circumstances in which this option should be used

  * For example, this option might be used in circumstances in which the copy
    of the data in the Graph Cache is trusted more than the copy outside the
    Graph Cache.

## Expert Topic: Tuning Graph Cache I/O

Outside the `kgtk query` command, the performance of KGTK commands that read
data from the Graph Cache may be tuned with certain options.  Normally, it
should not be necessary to adjust the values of these options, but when
running KGTK commands in environments with limited resources (e.g., on some
laptops or in resource-constrained VMs), tuning these option values may
provide some benefit.  The options are shown with their default values:

  * `--graph-cache-fetchmany-size 1000`
  * `--graph-cache-filter-batch-size 100`

