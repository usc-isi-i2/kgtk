import attr
import base64
from enum import Enum
import hashlib
from pathlib import Path
import shortuuid # type: ignore
import sys
import typing

from graph_tool.topology import label_components
from graph_tool.util import find_edge

from kgtk.kgtkformat import KgtkFormat
from kgtk.gt.gt_load import load_graph_from_kgtk
from kgtk.io.kgtkwriter import KgtkWriter
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
from kgtk.value.kgtkvalueoptions import KgtkValueOptions

@attr.s(slots=True, frozen=True)
class ConnectedComponents(KgtkFormat):
    class Method(Enum):
        CAT = "cat"              # Concatenate all entity names
        HASH = "hash"            # short hash of the concatenated value
        FIRST = "first"          # first value seen (unstable)
        LAST = "last"            # last value seen (unstable)
        SHORTEST = "shortest"    # shortest value seen, then lowest
        LONGEST = "longest"      # longest value seen, then highest
        NUMBERED = "numbered"    # numberd value produced by gtaph_tool (may not be dense)
        PREFIXED = "prefixed"    # prefixed numbered value
        LOWEST = "lowest"        # lowest value alphabetically
        HIGHEST = "highest"      # highest value alphabetically

    DEFAULT_CLUSTER_NAME_METHOD: Method = Method.HASH
    DEFAULT_CLUSTER_NAME_SEPARATOR: str = "+"
    DEFAULT_CLUSTER_NAME_PREFIX: str = "CLUS"
    DEFAULT_CLUSTER_NAME_ZFILL: int = 4
    DEFAULT_MINIMUM_CLUSTER_SIZE: int = 2

    input_file_path: typing.Optional[Path] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Path)))
    output_file_path: typing.Optional[Path] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Path)), default=None)
    
    undirected: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    strong: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    properties: str = attr.ib(validator=attr.validators.instance_of(str), default='')

    cluster_name_method: Method = attr.ib(default=DEFAULT_CLUSTER_NAME_METHOD)
    cluster_name_separator: str = attr.ib(validator=attr.validators.instance_of(str), default=DEFAULT_CLUSTER_NAME_SEPARATOR)
    cluster_name_prefix: str = attr.ib(validator=attr.validators.instance_of(str), default=DEFAULT_CLUSTER_NAME_PREFIX)
    cluster_name_zfill: int = attr.ib(validator=attr.validators.instance_of(int), default=DEFAULT_CLUSTER_NAME_ZFILL)
    minimum_cluster_size: int = attr.ib(validator=attr.validators.instance_of(int), default=DEFAULT_MINIMUM_CLUSTER_SIZE)

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

    def name_clusters(self, clusters: typing.Mapping[str, typing.List[str]],
    )->typing.Mapping[str, typing.List[str]]:
        if self.cluster_name_method == ConnectedComponents.Method.NUMBERED:
            return clusters

        renamed_clusters: typing.MutableMapping[str, typing.List[str]] = dict()

        cluster_id: str
        for cluster_id in clusters.keys():
            cluster_names: typing.List[str] = clusters[cluster_id]
            new_cluster_id: str
            name: str
            if self.cluster_name_method == ConnectedComponents.Method.PREFIXED:
                new_cluster_id = self.cluster_name_prefix + cluster_id.zfill(self.cluster_name_zfill)

            elif self.cluster_name_method == ConnectedComponents.Method.FIRST:
                new_cluster_id = cluster_names[0]

            elif self.cluster_name_method == ConnectedComponents.Method.LAST:
                new_cluster_id = cluster_names[-1]

            elif self.cluster_name_method == ConnectedComponents.Method.LOWEST:
                new_cluster_id = sorted(cluster_names)[0]

            elif self.cluster_name_method == ConnectedComponents.Method.HIGHEST:
                new_cluster_id = sorted(cluster_names)[-1]

            elif self.cluster_name_method == ConnectedComponents.Method.SHORTEST:
                new_cluster_id = cluster_names[0]
                for name in cluster_names:
                    if len(name) < len(new_cluster_id):
                        new_cluster_id = name
                    elif len(name) == len(new_cluster_id):
                        if name < new_cluster_id:
                            new_cluster_id = name
                
            elif self.cluster_name_method == ConnectedComponents.Method.LONGEST:
                new_cluster_id = cluster_names[0]
                for name in cluster_names:
                    if len(name) > len(new_cluster_id):
                        new_cluster_id = name
                    elif len(name) == len(new_cluster_id):
                        if name > new_cluster_id:
                            new_cluster_id = name

            elif self.cluster_name_method == ConnectedComponents.Method.CAT:
                new_cluster_id = self.cluster_name_separator.join(sorted(list(set(cluster_names))))

            elif self.cluster_name_method == ConnectedComponents.Method.HASH:
                cat_id: str = self.cluster_name_separator.join(sorted(list(set(cluster_names))))
                new_cluster_id = self.cluster_name_prefix + base64.b64encode(hashlib.md5(cat_id.encode()).digest()).decode('utf-8')

            renamed_clusters[new_cluster_id] = cluster_names

        return renamed_clusters

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
        label = input_kr.column_names[label_col_idx]

        g = load_graph_from_kgtk(input_kr, directed=not self.undirected)

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

        clusters: typing.MutableMapping[str, typing.List[str]] = dict()
        cluster_id: str
        name: str

        v: int
        for v, c in enumerate(comp):
            name = g.vertex_properties['name'][v]
            cluster_id = str(c)
            if cluster_id not in clusters:
                clusters[cluster_id] = [ name ]
            else:
                clusters[cluster_id].append(name)

        trimmed_clusters: typing.MutableMapping[str, typing.List[str]] = dict()
        for cluster_id in clusters.keys():
            if len(clusters[cluster_id]) >= self.minimum_cluster_size:
                trimmed_clusters[cluster_id] = clusters[cluster_id]
        
        named_clusters: typing.MutableMapping[str, typing.List[str]] = self.name_clusters(trimmed_clusters)
        for cluster_id in sorted(named_clusters.keys()):
            for name in sorted(named_clusters[cluster_id]):
                ew.write([name, 'connected_component', cluster_id])

        ew.close()
