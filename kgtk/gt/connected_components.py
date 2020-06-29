import sys
import attr
import typing
from pathlib import Path
from graph_tool.util import find_edge
from kgtk.kgtkformat import KgtkFormat
from kgtk.io.kgtkwriter import KgtkWriter
from graph_tool import load_graph_from_csv
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
        label = '{}{}'.format('c', label_col_idx)

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
