import sys
import attr
import typing
from pathlib import Path
from graph_tool.util import find_edge
from kgtk.kgtkformat import KgtkFormat
from kgtk.io.kgtkwriter import KgtkWriter
from graph_tool.topology import label_components
from kgtk.value.kgtkvalueoptions import KgtkValueOptions
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions


@attr.s(slots=True, frozen=True)
class ConnectedComponents(KgtkFormat):
    input_file_path: typing.Optional[Path] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(Path)))

    output_file_path: typing.Optional[Path] = attr.ib(
        validator=attr.validators.optional(attr.validators.instance_of(Path)), default=None)
    no_header: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    undirected: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    strong: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    properties: str = attr.ib(validator=attr.validators.instance_of(str), default='')

    input_reader_options: typing.Optional[KgtkReaderOptions] = attr.ib(default=None)
    filter_reader_options: typing.Optional[KgtkReaderOptions] = attr.ib(default=None)
    value_options: typing.Optional[KgtkValueOptions] = attr.ib(default=None)

    error_file: typing.TextIO = attr.ib(default=sys.stderr)
    verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    very_verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    def get_edge_key_columns(self, kr: KgtkReader, who: str) -> typing.List[int]:
        if kr.node1_column_idx < 0:
            raise ValueError("The node1 column is missing from the %s edge file." % who)
        if kr.label_column_idx < 0:
            raise ValueError("The label column is missing from the %s edge file." % who)
        if kr.node2_column_idx < 0:
            raise ValueError("The node2 column is missing from the %s edge file." % who)
        return [kr.node1_column_idx, kr.label_column_idx, kr.node2_column_idx]

    def get_key_columns(self, kr: KgtkReader, who: str) -> typing.List[int]:

        if not (kr.is_node_file or kr.is_edge_file):
            raise ValueError("The %s file is a quasi-KGTK file.  Please supply its keys." % who)

        return self.get_edge_key_columns(kr, who)

    def process(self):
        if str(self.input_file_path) == "-":
            # TODO: Copy stdin to a temporary file, then pass the temporary
            # file to KgtkReader and graph_tool.load_graph_from_csv(...).
            # When done, delete the temporary file.
            raise ValueError("connected_components: stdin is not supported.")

        input_kr: KgtkReader = KgtkReader.open(self.input_file_path,
                                               error_file=self.error_file,
                                               who="input",
                                               options=self.input_reader_options,
                                               value_options=self.value_options,
                                               verbose=self.verbose,
                                               very_verbose=self.very_verbose,
                                               )

        input_key_columns: typing.List[int] = self.get_key_columns(input_kr, "input")
        label_col_idx = input_key_columns[1]
        if self.no_header:
            # There is no header, so graph_tool.load_graph_from_csv(...) will
            # name the additional columns c1, c2,...
            #
            # https://graph-tool.skewed.de/static/doc/graph_tool.html?highlight=load_graph_from_csv#graph_tool.load_graph_from_csv
            #
            # Since this implies that columns are numbered from 1, we need to
            # add 1 to the KgtkReader column index, which starts at 0.
            label = 'c{}'.format(label_col_idx + 1)
        else:
            # There is a column header, so graph_tool.load_graph_from_csv(...)
            # will use the name from the header line.
            label = input_kr.column_names[label_col_idx]

        # KGTK strings (or symbols) with internal quotes may cause the CSV reader
        # to be confused, since the CSV reader will expect them to be doubled ("")
        # instead of escaped (\").
        #
        # Also, KGTK string quotes will be lost, and other damage to KGTK datatypes
        # (perhaps language qualified strings) may occur.
        g = load_graph_from_csv(str(input_kr.file_path), not (self.undirected),
                                skip_first=not (self.no_header),
                                hashed=True,
                                csv_options={'delimiter': '\t'}, ecols=(input_key_columns[0], input_key_columns[2]))

        es = []
        header = ['node1', 'label', 'node2']
        if self.properties:
            properties = self.properties.split(',')
            for e in properties:
                es += (find_edge(g, g.edge_properties[label], e))
            g.clear_edges()
            g.add_edge_list(list(set(es)))
        comp, hist = label_components(g, directed=self.strong)

        ew: KgtkWriter = KgtkWriter.open(header,
                                         self.output_file_path,
                                         mode=input_kr.mode,
                                         require_all_columns=False,
                                         prohibit_extra_columns=True,
                                         fill_missing_columns=True,
                                         gzip_in_parallel=False,
                                         verbose=self.verbose,
                                         very_verbose=self.very_verbose)
        for v, c in enumerate(comp):
            ew.write([g.vertex_properties['name'][v], 'connected_component', str(c)])

def load_graph_from_csv(file_name, directed=False, eprop_types=None,
                         eprop_names=None, hashed=True, hash_type="string",
                         skip_first=False, strip_whitespace=True, ecols=(0,1),
                        csv_options={"delimiter": ",", "quotechar": '"'}):
    """Load a graph from a :mod:`csv` file containing a list of edges and edge
    properties.

    Parameters
    ----------
    file_name : ``str`` or file-like object
        File in :mod:``csv`` format, with edges given in each row.
    directed : ``bool`` (optional, default: ``False``)
        Whether or not the graph is directed.
    eprop_types : list of ``str`` (optional, default: ``None``)
        List of edge property types to be read from remaining columns (if this
        is ``None``, all properties will be of type ``string``.
    eprop_names : list of ``str`` (optional, default: ``None``)
        List of edge property names to be used for the remaining columns (if
        this is ``None``, and ``skip_first`` is ``True`` their values will be
        obtained from the first line, otherwise they will be called ``c1, c2,
        ...``).
    hashed : ``bool`` (optional, default: ``True``)
        If ``True`` the vertex values in the edge list are not assumed to
        correspond to vertex indices directly. In this case they will be mapped
        to vertex indices according to the order in which they are encountered,
        and a vertex property map with the vertex values is returned.
    hash_type : ``str`` (optional, default: ``string``)
        If ``hashed == True``, this will determined the type of the vertex values.
        It can be any property map value type (see :class:`PropertyMap`).
    skip_first : ``bool`` (optional, default: ``False``)
        If ``True`` the first line of the file will be skipped.
    strip_whitespace : ``bool`` (optional, default: ``True``)
        If ``True`` whitespace will be striped from the start and end of values,
        before processing them.
    ecols : pair of ``int`` (optional, default: ``(0,1)``)
        Line columns used as source and target for the edges.
    csv_options : ``dict`` (optional, default: ``{"delimiter": ",", "quotechar": '"'}``)
        Options to be passed to the :func:`csv.reader` parser.

    Returns
    -------
    g : :class:`~graph_tool.Graph`
        The loaded graph. It will contain additional columns in the file as
        internal edge property maps. If ``hashed == True``, it will also contain
        an internal vertex property map with the vertex names.

    """
    import bz2
    import csv
    import gzip
    import itertools
    try:
        import lzma
    except ImportError:
        pass
    from graph_tool import Graph

    if isinstance(file_name, str):
        if file_name.endswith(".xz"):
            try:
                file_name = lzma.open(file_name, mode="rt")
            except ImportError:
                raise NotImplementedError("lzma compression is only available in Python >= 3.3")
        elif file_name.endswith(".gz"):
            file_name = gzip.open(file_name, mode="rt")
        elif file_name.endswith(".bz2"):
            file_name = bz2.open(file_name, mode="rt")
        else:
            file_name = open(file_name, "r")
    _csv_options = {"delimiter": ",", "quotechar": '"'}
    if  "dialect" in csv_options:
        _csv_options = csv_options
    else:
        _csv_options.update(csv_options)
    r = csv.reader(file_name, **_csv_options)

    if strip_whitespace:
        def strip(r):
            for row in r:
                yield (x.strip() for x in row)
        r = strip(r)

    if skip_first:
        first_line = list(next(r))

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

    if not hashed:
        def conv(rows):
            for row in rows:
                row = list(row)
                row[0] = int(row[0])
                row[1] = int(row[1])
                yield row
        r = conv(r)

    line = list(next(r))
    g = Graph(directed=directed)

    if eprop_types is None:
        eprops = [g.new_ep("string") for x in line[2:]]
    else:
        eprops = [g.new_ep(t) for t in eprop_types]

    name = g.add_edge_list(itertools.chain([line], r), hashed=hashed,
                           hash_type=hash_type, eprops=eprops)

    if eprop_names is None and skip_first and len(first_line) == len(line):
        eprop_names = list(first_line)
        del eprop_names[min(ecols)]
        del eprop_names[max(ecols)-1]

    for i, p in enumerate(eprops):
        if eprop_names is not None:
            ename = eprop_names[i]
        else:
            ename = "c%d" % i
        g.ep[ename] = p

    if name is not None:
        g.vp.name = name
    return g

