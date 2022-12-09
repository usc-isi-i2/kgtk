import sys
from pathlib import Path
from graph_tool.search import dfs_iterator, bfs_iterator, bfs_search, BFSVisitor
from kgtk.exceptions import KGTKException
from kgtk.gt.gt_load import load_graph_from_kgtk
from kgtk.io.kgtkwriter import KgtkWriter
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
from kgtk.value.kgtkvalueoptions import KgtkValueOptions
from typing import List, TextIO, Set, Any


class ReachableNodes(object):
    def __init__(self,
                 input_kgtk_file: Path,
                 output_kgtk_file: Path,
                 input_reader_options: KgtkReaderOptions = None,
                 root_reader_options: KgtkReaderOptions = None,
                 props_reader_options: KgtkReaderOptions = None,
                 undirected_props_reader_options: KgtkReaderOptions = None,
                 inverted_props_reader_options: KgtkReaderOptions = None,
                 value_options: KgtkValueOptions = None,
                 show_properties: bool = False,
                 show_distance: bool = False,
                 dist_col_name: str = 'distance',
                 label: str = 'reachable',
                 root: List[str] = None,
                 rootfile: str = None,
                 rootfilecolumn: str = 'node1',
                 subject_column_name: str = 'node1',
                 object_column_name: str = 'label',
                 predicate_column_name: str = 'node2',
                 inverted: bool = False,
                 inverted_props_file: str = None,
                 invertedpropsfilecolumn: str = None,
                 props: List[str] = None,
                 props_file: str = None,
                 propsfilecolumn: str = None,
                 undirected_props: List[str] = None,
                 inverted_props: List[str] = None,
                 undirected: bool = False,
                 undirected_props_file: str = None,
                 undirectedpropsfilecolumn: str = None,
                 selflink_bool: bool = False,
                 breadth_first: bool = False,
                 depth_limit: int = None,
                 error_file: TextIO = sys.stderr,
                 verbose: bool = False,
                 very_verbose: bool = False,
                 show_options: bool = False,
                 errors_to_stdout: bool = False,
                 errors_to_stderr: bool = False
                 ):

        self.input_kgtk_file = input_kgtk_file
        self.output_kgtk_file = output_kgtk_file
        self.input_reader_options = input_reader_options

        self.root_reader_options = root_reader_options
        self.props_reader_options = props_reader_options
        self.undirected_props_reader_options = undirected_props_reader_options
        self.inverted_props_reader_options = inverted_props_reader_options

        self.value_options = value_options
        self.show_properties = show_properties
        self.show_distance = show_distance
        self.dist_col_name = dist_col_name

        self.label = label
        self.root = root if root is not None else []
        self.props = props if props is not None else []
        self.undirected_props = undirected_props if undirected_props is not None else []
        self.inverted_props = inverted_props if inverted_props is not None else []

        self.rootfile = rootfile
        self.rootfilecolumn = rootfilecolumn
        self.subject_column_name = subject_column_name
        self.object_column_name = object_column_name
        self.predicate_column_name = predicate_column_name
        self.props_file = props_file
        self.propsfilecolumn = propsfilecolumn

        self.inverted = inverted
        self.inverted_props_file = inverted_props_file
        self.invertedpropsfilecolumn = invertedpropsfilecolumn

        self.undirected = undirected
        self.undirected_props_file = undirected_props_file
        self.undirectedpropsfilecolumn = undirectedpropsfilecolumn

        self.selflink_bool = selflink_bool
        self.breadth_first = breadth_first
        self.depth_limit = depth_limit

        self.error_file = error_file
        self.verbose = verbose
        self.very_verbose = very_verbose
        self.show_options = show_options
        self.errors_to_stdout = errors_to_stdout
        self.errors_to_stderr = errors_to_stderr

    def process(self):

        if self.show_options:
            if self.root is not None:
                print("--root %s" % " ".join(self.root), file=self.error_file)
            if self.rootfile is not None:
                print("--rootfile=%s" % self.rootfile, file=self.error_file)
            if self.rootfilecolumn is not None:
                print("--rootfilecolumn=%s" % self.rootfilecolumn, file=self.error_file)
            if self.subject_column_name is not None:
                print("--subj=%s" % self.subject_column_name, file=self.error_file)
            if self.object_column_name is not None:
                print("--obj=%s" % self.object_column_name, file=self.error_file)
            if self.predicate_column_name is not None:
                print("--pred=%s" % self.predicate_column_name, file=self.error_file)

            if self.props is not None:
                print("--props=%s" % " ".join(self.props), file=self.error_file)
            if self.props_file is not None:
                print("--props-file=%s" % self.props_file, file=self.error_file)
            if self.propsfilecolumn is not None:
                print("--propsfilecolumn=%s" % self.propsfilecolumn, file=self.error_file)

            print("--inverted=%s" % str(self.inverted), file=self.error_file)
            if self.inverted_props is not None:
                print("--inverted-props=%s" % " ".join(self.inverted_props), file=self.error_file)
            if self.inverted_props_file is not None:
                print("--inverted-props-file=%s" % self.inverted_props_file, file=self.error_file)
            if self.invertedpropsfilecolumn is not None:
                print("--invertedpropsfilecolumn=%s" % self.invertedpropsfilecolumn, file=self.error_file)

            print("--undirected=%s" % str(self.undirected), file=self.error_file)
            if self.undirected_props is not None:
                print("--undirected-props=%s" % " ".join(self.undirected_props), file=self.error_file)
            if self.undirected_props_file is not None:
                print("--undirected-props-file=%s" % self.undirected_props_file, file=self.error_file)
            if self.undirectedpropsfilecolumn is not None:
                print("--undirectedpropsfilecolumn=%s" % self.undirectedpropsfilecolumn, file=self.error_file)

            print("--label=%s" % self.label, file=self.error_file)
            print("--selflink=%s" % str(self.selflink_bool), file=self.error_file)
            print("--breadth-first=%s" % str(self.breadth_first), file=self.error_file)
            if self.depth_limit is not None:
                print("--depth-limit=%d" % self.depth_limit, file=self.error_file)
            self.input_reader_options.show(out=self.error_file)
            self.root_reader_options.show(out=self.error_file)
            self.props_reader_options.show(out=self.error_file)
            self.undirected_props_reader_options.show(out=self.error_file)
            self.inverted_props_reader_options.show(out=self.error_file)
            self.value_options.show(out=self.error_file)

            KgtkReader.show_debug_arguments(errors_to_stdout=self.errors_to_stdout,
                                            errors_to_stderr=self.errors_to_stderr,
                                            show_options=self.show_options,
                                            verbose=self.verbose,
                                            very_verbose=self.very_verbose,
                                            out=self.error_file)
            print("=======", file=self.error_file, flush=True)

        if self.inverted and (len(self.inverted_props) > 0 or self.inverted_props_file is not None):
            raise KGTKException("--inverted is not allowed with --inverted-props or --inverted-props-file")

        if self.undirected and (len(self.undirected_props) > 0 or self.undirected_props_file is not None):
            raise KGTKException("--undirected is not allowed with --undirected-props or --undirected-props-file")

        if self.depth_limit is not None:
            if not self.breadth_first:
                raise KGTKException("--depth-limit is not allowed without --breadth-first")
            if self.depth_limit <= 0:
                raise KGTKException("--depth-limit requires a positive argument")

        root_set: Set = set()

        if self.rootfile is not None:
            if self.verbose:
                print("Reading the root file %s" % repr(self.rootfile), file=self.error_file, flush=True)
            try:
                root_kr: KgtkReader = KgtkReader.open(Path(self.rootfile),
                                                      error_file=self.error_file,
                                                      who="root",
                                                      options=self.root_reader_options,
                                                      value_options=self.value_options,
                                                      verbose=self.verbose,
                                                      very_verbose=self.very_verbose,
                                                      )
            except SystemExit:
                raise KGTKException("Exiting.")

            rootcol: int
            if root_kr.is_edge_file:
                rootcol = int(
                    self.rootfilecolumn) \
                    if self.rootfilecolumn is not None and self.rootfilecolumn.isdigit() \
                    else root_kr.get_node1_column_index(self.rootfilecolumn)
            elif root_kr.is_node_file:
                rootcol = int(
                    self.rootfilecolumn) \
                    if self.rootfilecolumn is not None and self.rootfilecolumn.isdigit() \
                    else root_kr.get_id_column_index(self.rootfilecolumn)
            elif self.rootfilecolumn is not None:
                rootcol = int(
                    self.rootfilecolumn) \
                    if self.rootfilecolumn is not None and self.rootfilecolumn.isdigit() \
                    else root_kr.column_name_map.get(self.rootfilecolumn, -1)
            else:
                root_kr.close()
                raise KGTKException(
                    "The root file is neither an edge nor a node file and the root column name was not supplied.")

            if rootcol < 0:
                root_kr.close()
                raise KGTKException("Unknown root column %s" % repr(self.rootfilecolumn))

            for row in root_kr:
                rootnode: str = row[rootcol]
                root_set.add(rootnode)
            root_kr.close()

        if len(self.root) > 0:
            if self.verbose:
                print("Adding root nodes from the command line.", file=self.error_file, flush=True)
            root_group: str
            for root_group in self.root:
                r: str
                for r in root_group.split(','):
                    if self.verbose:
                        print("... adding %s" % repr(r), file=self.error_file, flush=True)
                    root_set.add(r)
        if len(root_set) == 0:
            print("Warning: No nodes in the root set, the output file will be empty.", file=self.error_file, flush=True)
        elif self.verbose:
            print("%d nodes in the root set." % len(root_set), file=self.error_file, flush=True)

        property_set: Set[str] = set()
        if self.props_file is not None:
            if self.verbose:
                print("Reading the root file %s" % repr(self.props_file), file=self.error_file, flush=True)
            try:
                props_kr: KgtkReader = KgtkReader.open(Path(self.props_file),
                                                       error_file=self.error_file,
                                                       who="props",
                                                       options=self.props_reader_options,
                                                       value_options=self.value_options,
                                                       verbose=self.verbose,
                                                       very_verbose=self.very_verbose,
                                                       )
            except SystemExit:
                raise KGTKException("Exiting.")

            propscol: int
            if props_kr.is_edge_file:
                propscol = int(
                    self.propsfilecolumn) \
                    if self.propsfilecolumn is not None and self.propsfilecolumn.isdigit() \
                    else props_kr.get_node1_column_index(self.propsfilecolumn)
            elif props_kr.is_node_file:
                propscol = int(
                    self.propsfilecolumn) \
                    if self.propsfilecolumn is not None and self.propsfilecolumn.isdigit() \
                    else props_kr.get_id_column_index(self.propsfilecolumn)
            elif self.propsfilecolumn is not None:
                propscol = int(
                    self.propsfilecolumn) \
                    if self.propsfilecolumn is not None and self.propsfilecolumn.isdigit() \
                    else props_kr.column_name_map.get(self.propsfilecolumn, -1)
            else:
                props_kr.close()
                raise KGTKException(
                    "The props file is neither an edge nor a node file and the root column name was not supplied.")

            if propscol < 0:
                props_kr.close()
                raise KGTKException("Unknown props column %s" % repr(self.propsfilecolumn))

            for row in props_kr:
                property_name: str = row[propscol]
                property_set.add(property_name)
            props_kr.close()

        if len(self.props) > 0:
            # Filter the graph, G, to include only edges where the predicate (label)
            # column contains one of the selected properties.

            prop_group: str
            for prop_group in self.props:
                prop: str
                for prop in prop_group.split(','):
                    property_set.add(prop)
        if self.verbose and len(property_set) > 0:
            print("property set=%s" % " ".join(sorted(list(property_set))), file=self.error_file, flush=True)

        undirected_property_set: Set[str] = set()
        if self.undirected_props_file is not None:
            if self.verbose:
                print("Reading the undirected properties file %s" % repr(self.undirected_props_file),
                      file=self.error_file,
                      flush=True)
            try:
                undirected_props_kr: KgtkReader = KgtkReader.open(Path(self.undirected_props_file),
                                                                  error_file=self.error_file,
                                                                  who="undirected_props",
                                                                  options=self.undirected_props_reader_options,
                                                                  value_options=self.value_options,
                                                                  verbose=self.verbose,
                                                                  very_verbose=self.very_verbose,
                                                                  )
            except SystemExit:
                raise KGTKException("Exiting.")

            undirected_props_col: int
            if undirected_props_kr.is_edge_file:
                undirected_props_col = int(self.undirectedpropsfilecolumn) \
                    if self.undirectedpropsfilecolumn is not None and self.undirectedpropsfilecolumn.isdigit() \
                    else undirected_props_kr.get_node1_column_index(self.undirectedpropsfilecolumn)
            elif undirected_props_kr.is_node_file:
                undirected_props_col = int(self.undirectedpropsfilecolumn) \
                    if self.undirectedpropsfilecolumn is not None and self.undirectedpropsfilecolumn.isdigit() \
                    else undirected_props_kr.get_id_column_index(self.undirectedpropsfilecolumn)
            elif self.undirectedpropsfilecolumn is not None:
                undirected_props_col = int(self.undirectedpropsfilecolumn) \
                    if self.undirectedpropsfilecolumn is not None and self.undirectedpropsfilecolumn.isdigit() \
                    else undirected_props_kr.column_name_map.get(self.undirectedpropsfilecolumn, -1)
            else:
                undirected_props_kr.close()
                raise KGTKException("The undirected props file is neither an edge nor a node file and the root column "
                                    "name was not supplied.")

            if undirected_props_col < 0:
                undirected_props_kr.close()
                raise KGTKException("Unknown undirected properties column %s" % repr(self.undirectedpropsfilecolumn))

            for row in undirected_props_kr:
                undirected_property_name: str = row[undirected_props_col]
                undirected_property_set.add(undirected_property_name)
            undirected_props_kr.close()
        if len(self.undirected_props) > 0:
            # Edges where the predicate (label) column contains one of the selected
            # properties will be treated as undirected links.

            und_prop_group: str
            for und_prop_group in self.undirected_props:
                und_prop: str
                for und_prop in und_prop_group.split(','):
                    undirected_property_set.add(und_prop)
        if self.verbose and len(undirected_property_set) > 0:
            print("undirected property set=%s" % " ".join(sorted(list(undirected_property_set))), file=self.error_file,
                  flush=True)

        inverted_property_set: Set[str] = set()
        if self.inverted_props_file is not None:
            if self.verbose:
                print("Reading the inverted properties file %s" % repr(self.inverted_props_file), file=self.error_file,
                      flush=True)
            try:
                inverted_props_kr: KgtkReader = KgtkReader.open(Path(self.inverted_props_file),
                                                                error_file=self.error_file,
                                                                who="inverted_props",
                                                                options=self.inverted_props_reader_options,
                                                                value_options=self.value_options,
                                                                verbose=self.verbose,
                                                                very_verbose=self.very_verbose,
                                                                )
            except SystemExit:
                raise KGTKException("Exiting.")

            inverted_props_col: int
            if inverted_props_kr.is_edge_file:
                inverted_props_col = int(self.invertedpropsfilecolumn) \
                    if self.invertedpropsfilecolumn is not None and self.invertedpropsfilecolumn.isdigit() \
                    else inverted_props_kr.get_node1_column_index(self.invertedpropsfilecolumn)
            elif inverted_props_kr.is_node_file:
                inverted_props_col = int(self.invertedpropsfilecolumn) \
                    if self.invertedpropsfilecolumn is not None and self.invertedpropsfilecolumn.isdigit() \
                    else inverted_props_kr.get_id_column_index(self.invertedpropsfilecolumn)
            elif self.invertedpropsfilecolumn is not None:
                inverted_props_col = int(self.invertedpropsfilecolumn) \
                    if self.invertedpropsfilecolumn is not None and self.invertedpropsfilecolumn.isdigit() \
                    else inverted_props_kr.column_name_map.get(self.invertedpropsfilecolumn, -1)
            else:
                inverted_props_kr.close()
                raise KGTKException(
                    "The inverted props file is neither an edge nor a node file and the root column name was not supplied.")

            if inverted_props_col < 0:
                inverted_props_kr.close()
                raise KGTKException("Unknown inverted properties column %s" % repr(self.invertedpropsfilecolumn))

            for row in inverted_props_kr:
                inverted_property_name: str = row[inverted_props_col]
                inverted_property_set.add(inverted_property_name)
            inverted_props_kr.close()

        if len(self.inverted_props) > 0:
            # Edges where the predicate (label) column contains one of the selected
            # properties will have the source and target columns swapped.

            inv_prop_group: str
            for inv_prop_group in self.inverted_props:
                inv_prop: str
                for inv_prop in inv_prop_group.split(','):
                    inverted_property_set.add(inv_prop)
        if self.verbose and len(inverted_property_set):
            print("inverted property set=%s" % " ".join(sorted(list(inverted_property_set))), file=self.error_file,
                  flush=True)

        try:
            kr: KgtkReader = KgtkReader.open(self.input_kgtk_file,
                                             error_file=self.error_file,
                                             who="input",
                                             options=self.input_reader_options,
                                             value_options=self.value_options,
                                             verbose=self.verbose,
                                             very_verbose=self.very_verbose,
                                             )
        except SystemExit:
            raise KGTKException("Exiting.")

        sub: int = kr.get_node1_column_index(self.subject_column_name)
        if sub < 0:
            print("Unknown subject column %s" % repr(self.subject_column_name), file=self.error_file, flush=True)

        pred: int = kr.get_label_column_index(self.predicate_column_name)
        if pred < 0:
            print("Unknown predicate column %s" % repr(self.predicate_column_name), file=self.error_file, flush=True)

        obj: int = kr.get_node2_column_index(self.object_column_name)
        if obj < 0:
            print("Unknown object column %s" % repr(self.object_column_name), file=self.error_file, flush=True)

        if sub < 0 or pred < 0 or obj < 0:
            kr.close()
            raise KGTKException("Exiting due to unknown column.")

        if self.verbose:
            print("special columns: sub=%d pred=%d obj=%d" % (sub, pred, obj), file=self.error_file, flush=True)

        G = load_graph_from_kgtk(kr,
                                 directed=not self.undirected,
                                 inverted=self.inverted,
                                 ecols=(sub, obj),
                                 pcol=pred,
                                 pset=property_set,
                                 upset=undirected_property_set,
                                 ipset=inverted_property_set,
                                 verbose=self.verbose,
                                 out=self.error_file)

        name = G.vp["name"]  # Get the vertex name property map (vertex to ndoe1 (subject) name)

        if self.show_properties:
            print("Graph name=%s" % repr(name), file=self.error_file, flush=True)
            print("Graph properties:", file=self.error_file, flush=True)
            key: Any
            for key in G.properties:
                print("    %s: %s" % (repr(key), repr(G.properties[key])), file=self.error_file, flush=True)

        index_list = []
        for v in G.vertices():
            if name[v] in root_set:
                index_list.append(v)
        if len(index_list) == 0:
            print("Warning: No root nodes found in the graph, the output file will be empty.", file=self.error_file,
                  flush=True)
        elif self.verbose:
            print("%d root nodes found in the graph." % len(index_list), file=self.error_file, flush=True)

        if self.breadth_first and self.show_distance:
            output_header: List[str] = ['node1', 'label', 'node2', self.dist_col_name]
        else:
            output_header: List[str] = ['node1', 'label', 'node2']

        try:
            kw: KgtkWriter = KgtkWriter.open(output_header,
                                             self.output_kgtk_file,
                                             mode=KgtkWriter.Mode.EDGE,
                                             require_all_columns=True,
                                             prohibit_extra_columns=True,
                                             fill_missing_columns=False,
                                             verbose=self.verbose,
                                             very_verbose=self.very_verbose)
        except SystemExit:
            raise KGTKException("Exiting.")

        for index in index_list:
            if self.selflink_bool and self.show_distance:
                kw.writerow([name[index], self.label, name[index], 0])
            elif self.selflink_bool and not self.show_distance:
                kw.writerow([name[index], self.label, name[index]])

            if self.breadth_first:
                if self.depth_limit is None:
                    if self.show_distance:
                        count = 0
                        past = set()
                        for e in bfs_iterator(G, G.vertex(index)):
                            if e.source() in past:
                                count += 1
                                past = set()
                            kw.writerow([name[index], self.label, name[e.target()], count + 1])
                            past.add(e.target())

                    else:
                        for e in bfs_iterator(G, G.vertex(index)):
                            kw.writerow([name[index], self.label, name[e.target()]])

                else:
                    if self.show_distance:
                        class DepthExceeded(Exception):
                            pass

                        class DepthLimitedVisitor(BFSVisitor):
                            def __init__(self, name, pred, dist, depth_limit, label):
                                self.name = name
                                self.pred = pred
                                self.dist = dist
                                self.depth_limit = depth_limit
                                self.label = label

                            def tree_edge(self, e):
                                self.pred[e.target()] = int(e.source())
                                newdist = self.dist[e.source()] + 1

                                if self.depth_limit is not None and newdist > self.depth_limit:
                                    raise DepthExceeded
                                self.dist[e.target()] = newdist

                                kw.writerow([name[index], self.label, name[e.target()], newdist])

                        dist = G.new_vertex_property("int")
                        pred = G.new_vertex_property("int64_t")

                        try:
                            bfs_search(G, G.vertex(index),
                                       DepthLimitedVisitor(name, pred, dist, self.depth_limit, self.label))
                        except DepthExceeded:
                            pass

                    else:
                        class DepthExceeded(Exception):
                            pass

                        class DepthLimitedVisitor(BFSVisitor):
                            def __init__(self, name, pred, dist, depth_limit, label):
                                self.name = name
                                self.pred = pred
                                self.dist = dist
                                self.depth_limit = depth_limit
                                self.label = label

                            def tree_edge(self, e, depth_limit, label):
                                self.pred[e.target()] = int(e.source())
                                newdist = self.dist[e.source()] + 1
                                if self.depth_limit is not None and newdist > self.depth_limit:
                                    raise DepthExceeded
                                self.dist[e.targt()] = newdist
                                kw.writerow([name[index], self.label, name[e.target()]])

                        dist = G.new_vertex_property("int")
                        pred = G.new_vertex_property("int64_t")
                        try:
                            bfs_search(G, G.vertex(index),
                                       DepthLimitedVisitor(name, pred, dist, self.depth_limit, self.label))
                        except DepthExceeded:
                            pass

            else:
                for e in dfs_iterator(G, G.vertex(index)):
                    kw.writerow([name[index], self.label, name[e.target()]])

        kw.close()
        kr.close()
