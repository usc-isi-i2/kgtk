from graph_tool import Graph
import itertools
import sys
import typing

from kgtk.io.kgtkreader import KgtkReader

def load_graph_from_kgtk(kr: KgtkReader,
                         directed: bool=False,
                         inverted: bool=False,
                         eprop_types: typing.Optional[typing.List[str]]=None,
                         hashed: bool=True,
                         hash_type: str="string", # for future support
                         ecols: typing.Optional[typing.Tuple[int, int]]=None,
                         pcol: typing.Optional[int]=None,
                         pset: typing.Optional[typing.Set[str]]=None,
                         ipset: typing.Optional[typing.Set[str]]=None,
                         upset: typing.Optional[typing.Set[str]]=None,
                         out: typing.TextIO = sys.stderr,
                         verbose: bool = False,
                         ):
    """Load a graph from a `KgtkReader` file containing a list of edges and edge
    properties.  This code is based on load_graph_from_csv(...) in
    `graph-tool/src/graph_tool/__init__.py`, downloaded from git.skewed.de on
    27-Jul-2020.

    Parameters
    ----------
    kr : ``KgtkReader``

    directed : ``bool`` (optional, default: ``False``)
        Whether or not the graph is directed.

    inverted : ``bool`` (optional, default: ``False``)
        Whether or not the links are inverted.

    eprop_types : list of ``str`` (optional, default: ``None``)
        List of edge property types to be read from remaining columns (if this
        is ``None``, all properties will be of type ``string``.

    hashed : ``bool`` (optional, default: ``True``)
        If ``True`` the vertex values in the edge list are not assumed to
        correspond to vertex indices directly. In this case they will be mapped
        to vertex indices according to the order in which they are encountered,
        and a vertex property map with the vertex values is returned.

    hash_type : ``str`` (optional, default: ``string``)
        If ``hashed == True``, this will determined the type of the vertex values.
        It can be any property map value type (see :class:`PropertyMap`).

        Note: As of 29-Jul-2020, this parameter to graph.add_edge_list(...) is
        supported in the git version of graph_tools, but is not mentioned in
        the graph-tools 2.33 documentation.

    ecols : pair of ``int`` (optional, default: ``(0,1)``)
        Line columns used as source and target for the edges.

    pcol : ``int`` (optional, default: ``None``)
        Line column ised as predicate filter with pset.

    pset : set of `str` (optional, default: ``None``)
        When ``pcol`` and ``pset`` are both supplied, the input edges
        will be filtered to inlude only edges (rows) with predicate
        (label) values in ``pset``.

    ipset : set of `str` (optional, default: ``None``)
        When ``pcol``, and ``ipset`` are both supplied, input edges
        (rows) predicate (label) values in ``pset`` will have their
        source and target columns swapped.

    upset : set of `str` (optional, default: ``None``)
        When ``pcol``, and ``ipset`` are both supplied, input edges
        (rows) predicate (label) values in ``pset`` will be duplicated with their
        source and target columns swapped.

    Returns
    -------
    g : :class:`~graph_tool.Graph`
        The loaded graph. It will contain additional columns in the file as
        internal edge property maps. If ``hashed == True``, it will also contain
        an internal vertex property map with the vertex names.

    """
    if ecols is None:
        ecols = (kr.node1_column_idx, kr.node2_column_idx)

    r = kr # R may be wrapped for column reordering and/or non-hashed use.

    if pcol is not None and pset is not None and len(pset) > 0:
        def filter_rows(rows):
            for row in rows:
                if row[pcol] in pset:
                    yield row
        r = filter_rows(r)

    if pcol is not None and ipset is not None and len(ipset) > 0:
        def invert_specific_rows(rows):
            for row in rows:
                if row[pcol] in ipset:
                    row = list(row)
                    row[ecols[0]], row[ecols[1]] = row[ecols[1]], row[ecols[0]]
                    yield row
                else:
                    yield row
        r = invert_specific_rows(r)

    if pcol is not None and upset is not None and len(upset) > 0:
        def duplicate_and_invert_specific_rows(rows):
            for row in rows:
                yield row
                if row[pcol] in upset:
                    row = list(row)
                    row[ecols[0]], row[ecols[1]] = row[ecols[1]], row[ecols[0]]
                    yield row
        r = duplicate_and_invert_specific_rows(r)

    if ecols != (0, 1):
        def reorder(rows):
            for row in rows:
                row = list(row)
                s = row[ecols[0]]
                t = row[ecols[1]]
                del row[min(ecols)]
                del row[max(ecols)-1]
                yield [s, t] + row
        r = reorder(r)

    if inverted:
        def invert(rows):
            for row in rows:
                row = list(row)
                row[0], row[1] = row[1], row[0]
                yield row
        r = invert(r)

    if not hashed:
        def conv(rows):
            for row in rows:
                row = list(row)
                row[0] = int(row[0])
                row[1] = int(row[1])
                yield row
        r = conv(r)

    g = Graph(directed=directed)

    if eprop_types is None:
        if verbose:
            print("eprop_types is None", file=out, flush=True)
        eprops = [g.new_ep("string") for x in kr.column_names[2:]]
    else:
        if verbose:
            print("eprop_types: [%s]" % (", ".join([repr(x) for x in eprop_types])), file=out, flush=True)
        if len(eprop_types) != kr.column_count - 2:
            raise ValueError("There are %d eprop columns and %d eprop types." % (kr.column_count - 2, len(eprop_types)))
        eprops = [g.new_ep(t) for t in eprop_types]

    # 29-Jul-2020: This is supported in the git.skewed.de repository, and
    # presumably will be supported in a future release.  Unfortunately, graph-tool
    # doesn't appear to include a version indicator or API version indicator
    # easily accessible from Python.
    #
    # The graph-tool 2.33 documentation does not include the hash_type parameter.
    #
    # name = g.add_edge_list(itertools.chain([line], r), hashed=hashed,
    #                       hash_type=hash_type, eprops=eprops)
    if verbose:
        print("Adding edges from the input file.", file=out, flush=True)
    name = g.add_edge_list(r, hashed=hashed, eprops=eprops)
    if verbose:
        print("Done adding edges from the input file.", file=out, flush=True)
    g.vp.name = name

    eprop_names: typing.List[str] = list(kr.column_names)
    del eprop_names[min(ecols)]
    del eprop_names[max(ecols)-1]
    if verbose:
        print("eprop_names: [%s]" % (", ".join([repr(x) for x in eprop_names])), file=out, flush=True)

    for i, p in enumerate(eprops):
        ename = eprop_names[i]
        g.ep[ename] = p
        if verbose:
            print("prop %d name=%s" % (i, repr(ename)), file=out, flush=True)

    return g
