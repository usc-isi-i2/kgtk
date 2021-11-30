"""
Find reachable nodes given a set of root nodes and properties

TODO: the --subj, --pred, and --obj options should perhaps be renamed to
      --node1-column-name, --label-column-name, and --node2-column-name, with
      the old options kept as synonyms.

TODO: the root file name should be parsed with parser.add_input_file(...)
"""
from argparse import Namespace, _MutuallyExclusiveGroup
import typing

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles

def parser():
    return {
        'help': 'Find reachable nodes in a graph.'
    }


def add_arguments_extended(parser: KGTKArgumentParser, parsed_shared_args: Namespace):
    """
    Parse arguments
    Args:
            parser (argparse.ArgumentParser)
    """
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions, KgtkReaderMode
    from kgtk.utils.argparsehelpers import optional_bool
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    _expert: bool = parsed_shared_args._expert

    parser.add_input_file(positional=True, who="The KGTK file to find connected components in.")
    parser.add_output_file()

    # parser.add_argument(action="store", type=str, dest="filename", metavar='filename', help='input filename here')
    # parser.add_argument('-o', '--out', action='store', type=str, dest='output', help='File to output the reachable nodes,if empty will be written out to standard output',default=None)

    parser.add_argument('--root',action='store',dest='root',type=str, nargs="*",
                        help='Set of root nodes to use, space- or comma-separated strings. (default=None)')
    parser.add_argument('--root-file', '--rootfile',action='store',dest='rootfile',help='Option to specify a file containing the set of root nodes',default=None)
    parser.add_argument('--rootfilecolumn',action='store',type=str,dest='rootfilecolumn',
                        help='Specify the name or number of the root file column with the root nodes.  (default=node1 or its alias if edge file, id if node file)')
    parser.add_argument("--subj", action="store", type=str, dest="subject_column_name", help='Name of the subject column. (default: node1 or its alias)')
    parser.add_argument("--obj", action="store", type=str, dest="object_column_name", help='Name of the object column. (default: label or its alias)')
    parser.add_argument("--pred",action="store" ,type=str, dest="predicate_column_name",help='Name of the predicate column. (default: node2 or its alias)')

    parser.add_argument("--prop", "--props", action="store", type=str, dest="props", nargs="*",
                        help='Properties to consider while finding reachable nodes, space- or comma-separated string. (default: all properties)',default=None)
    parser.add_argument('--props-file', action='store', dest='props_file',
                        help='Option to specify a file containing the set of properties',default=None)
    parser.add_argument('--propsfilecolumn', action='store', type=str, dest='propsfilecolumn', default=None,
                        help='Specify the name or number of the props file column with the property names.  (default=node1 or its alias if edge file, id if node file)')

    parser.add_argument('--inverted', dest="inverted",
                        help="When True, and when --undirected is False, invert the source and target nodes in the graph. (default=%(default)s)",
                        type=optional_bool, nargs='?', const=True, default=False, metavar="True|False")

    parser.add_argument("--inverted-prop", "--inverted-props", action="store", type=str, dest="inverted_props", nargs="*",
                        help='Properties to invert, space- or comma-separated string. (default: no properties)',default=None)
    parser.add_argument('--inverted-props-file', action='store', dest='inverted_props_file',
                        help='Option to specify a file containing the set of inverted properties',default=None)
    parser.add_argument('--invertedpropsfilecolumn', action='store', type=str, dest='invertedpropsfilecolumn', default=None,
                        help='Specify the name or number of the inverted props file column with the property names.  (default=node1 or its alias if edge file, id if node file)')

    parser.add_argument('--undirected', dest="undirected",
                        help="When True, specify graph as undirected. (default=%(default)s)",
                        type=optional_bool, nargs='?', const=True, default=False, metavar="True|False")

    parser.add_argument("--undirected-prop", "--undirected-props", action="store", type=str, dest="undirected_props", nargs="*",
                        help='Properties to treat as undirected, space- or comma-separated string. (default: no properties)',default=None)
    parser.add_argument('--undirected-props-file', action='store', dest='undirected_props_file',
                        help='Option to specify a file containing the set of undirected properties',default=None)
    parser.add_argument('--undirectedpropsfilecolumn', action='store', type=str, dest='undirectedpropsfilecolumn', default=None,
                        help='Specify the name or number of the undirected props file column with the property names.  (default=node1 or its alias if edge file, id if node file)')

    parser.add_argument('--label', action='store', type=str, dest='label', help='The label for the reachable relationship. (default: %(default)s)',default="reachable")
    parser.add_argument('--selflink',dest='selflink_bool',
                        help='When True, include a link from each output node to itself. (default=%(default)s)',
                        type=optional_bool, nargs='?', const=True, default=False, metavar="True|False")

    parser.add_argument('--show-properties',dest='show_properties',
                        help='When True, show the graph properties. (default=%(default)s)',
                        type=optional_bool, nargs='?', const=True, default=False, metavar="True|False")

    parser.add_argument('--breadth-first',dest='breadth_first',
                        help='When True, search the graph breadth first.  When false, search depth first. (default=%(default)s)',
                        type=optional_bool, nargs='?', const=True, default=False, metavar="True|False")

    parser.add_argument('--depth-limit',dest='depth_limit',
                        help='An optional depth limit for breadth-first searches. (default=%(default)s)',
                        type=int, default=None)

    parser.add_argument('--show-distance',dest='show_distance',
                        help='When True, also given breadth first true, append another column showing the shortest distance, default col name is distance',
                        type=optional_bool, nargs='?', const=True, default=False, metavar="True|False")

    parser.add_argument('--dist-col-name', action='store', type=str, dest='dist_col_name', help='The column name for distance, default is distance',default="distance")

    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser,
                                    mode_options=True,
                                    default_mode=KgtkReaderMode[parsed_shared_args._mode],
                                    expert=_expert)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, who="input", expert=_expert, defaults=False)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, who="root", expert=_expert, defaults=False)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, who="props", expert=_expert, defaults=False)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, who="undirected_props", expert=_expert, defaults=False)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, who="inverted_props", expert=_expert, defaults=False)
    KgtkValueOptions.add_arguments(parser, expert=_expert)

def run(input_file: KGTKFiles,
        output_file: KGTKFiles,

        root: typing.Optional[typing.List[str]],
        rootfile,
        rootfilecolumn,
        subject_column_name: typing.Optional[str],
        object_column_name: typing.Optional[str],
        predicate_column_name: typing.Optional[str],

        props: typing.Optional[typing.List[str]],
        props_file: typing.Optional[str],
        propsfilecolumn: typing.Optional[str],

        inverted: bool,
        inverted_props: typing.Optional[typing.List[str]],
        inverted_props_file: typing.Optional[str],
        invertedpropsfilecolumn: typing.Optional[str],

        undirected: bool,
        undirected_props: typing.Optional[typing.List[str]],
        undirected_props_file: typing.Optional[str],
        undirectedpropsfilecolumn: typing.Optional[str],

        label: str,
        selflink_bool: bool,
        show_properties: bool,
        breadth_first: bool,
        depth_limit: typing.Optional[int],

        errors_to_stdout: bool,
        errors_to_stderr: bool,
        show_options: bool,
        verbose: bool,
        very_verbose: bool,
        show_distance: bool,
        dist_col_name: str,

        **kwargs, # Whatever KgtkFileOptions and KgtkValueOptions want.
        ):
    import sys
    import csv
    from pathlib import Path
    import time
    from graph_tool.search import dfs_iterator, bfs_iterator, bfs_search, BFSVisitor
    # from graph_tool import load_graph_from_csv
    from graph_tool.util import find_edge
    from kgtk.exceptions import KGTKException
    from kgtk.cli_argparse import KGTKArgumentParser

    from kgtk.gt.gt_load import load_graph_from_kgtk
    from kgtk.io.kgtkwriter import KgtkWriter
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    #Graph-tool names columns that are not subject or object c0, c1... This function finds the number that graph tool assigned to the predicate column
    def find_pred_position(sub,pred,obj):
        if pred < sub and pred < obj:
            return pred
        elif (pred > sub and pred < obj) or (pred<sub and pred>obj):
            return pred-1
        else:
            return pred-2

    def get_edges_by_edge_prop(g, p, v):
        return find_edge(g, prop=g.properties[('e', p)], match=v)


    input_kgtk_file: Path = KGTKArgumentParser.get_input_file(input_file)
    output_kgtk_file: Path = KGTKArgumentParser.get_output_file(output_file)

    # Select where to send error messages, defaulting to stderr.
    error_file: typing.TextIO = sys.stdout if errors_to_stdout else sys.stderr

    # Build the option structures.
    input_reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs, who="input", fallback=True)
    root_reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs, who="root", fallback=True)
    props_reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs, who="props", fallback=True)
    undirected_props_reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs, who="undirected_props", fallback=True)
    inverted_props_reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs, who="inverted_props", fallback=True)
    value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)

    if root is None:
        root = [ ] # This simplifies matters.

    if props is None:
        props = [ ] # This simplifies matters.

    if undirected_props is None:
        undirected_props = [ ] # This simplifies matters.

    if inverted_props is None:
        inverted_props = [ ] # This simplifies matters.

    if show_options:
        if root is not None:
            print("--root %s" % " ".join(root), file=error_file)
        if rootfile is not None:
            print("--rootfile=%s" % rootfile, file=error_file)
        if rootfilecolumn is not None:
            print("--rootfilecolumn=%s" % rootfilecolumn, file=error_file)
        if subject_column_name is not None:
            print("--subj=%s" % subject_column_name, file=error_file)
        if object_column_name is not None:
            print("--obj=%s" % object_column_name, file=error_file)
        if predicate_column_name is not None:
            print("--pred=%s" % predicate_column_name, file=error_file)

        if props is not None:
            print("--props=%s" % " ".join(props), file=error_file)
        if props_file is not None:
            print("--props-file=%s" % props_file, file=error_file)
        if propsfilecolumn is not None:
            print("--propsfilecolumn=%s" % propsfilecolumn, file=error_file)

        print("--inverted=%s" % str(inverted), file=error_file)
        if inverted_props is not None:
            print("--inverted-props=%s" % " ".join(inverted_props), file=error_file)
        if inverted_props_file is not None:
            print("--inverted-props-file=%s" % inverted_props_file, file=error_file)
        if invertedpropsfilecolumn is not None:
            print("--invertedpropsfilecolumn=%s" % invertedpropsfilecolumn, file=error_file)

        print("--undirected=%s" % str(undirected), file=error_file)
        if undirected_props is not None:
            print("--undirected-props=%s" % " ".join(undirected_props), file=error_file)
        if undirected_props_file is not None:
            print("--undirected-props-file=%s" % undirected_props_file, file=error_file)
        if undirectedpropsfilecolumn is not None:
            print("--undirectedpropsfilecolumn=%s" % undirectedpropsfilecolumn, file=error_file)

        print("--label=%s" % label, file=error_file)
        print("--selflink=%s" % str(selflink_bool), file=error_file)
        print("--breadth-first=%s" % str(breadth_first), file=error_file)
        if depth_limit is not None:
            print("--depth-limit=%d" % depth_limit, file=error_file)
        input_reader_options.show(out=error_file)
        root_reader_options.show(out=error_file)
        props_reader_options.show(out=error_file)
        undirected_props_reader_options.show(out=error_file)
        inverted_props_reader_options.show(out=error_file)
        value_options.show(out=error_file)
        KgtkReader.show_debug_arguments(errors_to_stdout=errors_to_stdout,
                                        errors_to_stderr=errors_to_stderr,
                                        show_options=show_options,
                                        verbose=verbose,
                                        very_verbose=very_verbose,
                                        out=error_file)
        print("=======", file=error_file, flush=True)

    if inverted and (len(inverted_props) > 0 or inverted_props_file is not None):
        raise KGTKException("--inverted is not allowed with --inverted-props or --inverted-props-file")

    if undirected and (len(undirected_props) > 0 or undirected_props_file is not None):
        raise KGTKException("--undirected is not allowed with --undirected-props or --undirected-props-file")

    if depth_limit is not None:
        if not breadth_first:
            raise KGTKException("--depth-limit is not allowed without --breadth-first")
        if depth_limit <= 0:
            raise KGTKException("--depth-limit requires a positive argument")

    root_set: typing.Set = set()

    if rootfile is not None:
        if verbose:
            print("Reading the root file %s" % repr(rootfile),  file=error_file, flush=True)
        try:
            root_kr: KgtkReader = KgtkReader.open(Path(rootfile),
                                                  error_file=error_file,
                                                  who="root",
                                                  options=root_reader_options,
                                                  value_options=value_options,
                                                  verbose=verbose,
                                                  very_verbose=very_verbose,
                                                  )
        except SystemExit:
            raise KGTKException("Exiting.")

        rootcol: int
        if root_kr.is_edge_file:
            rootcol = int(rootfilecolumn) if rootfilecolumn is not None and rootfilecolumn.isdigit() else root_kr.get_node1_column_index(rootfilecolumn)
        elif root_kr.is_node_file:
            rootcol = int(rootfilecolumn) if rootfilecolumn is not None and rootfilecolumn.isdigit() else root_kr.get_id_column_index(rootfilecolumn)
        elif rootfilecolumn is not None:
            rootcol = int(rootfilecolumn) if rootfilecolumn is not None and rootfilecolumn.isdigit() else root_kr.column_name_map.get(rootfilecolumn, -1)
        else:
            root_kr.close()
            raise KGTKException("The root file is neither an edge nor a node file and the root column name was not supplied.")

        if rootcol < 0:
            root_kr.close()
            raise KGTKException("Unknown root column %s" % repr(rootfilecolumn))

        for row in root_kr:
            rootnode: str = row[rootcol]
            root_set.add(rootnode)
        root_kr.close()
        
    if len(root) > 0:
        if verbose:
            print ("Adding root nodes from the command line.",  file=error_file, flush=True)
        root_group: str
        for root_group in root:
            r: str
            for r in root_group.split(','):
                if verbose:
                    print("... adding %s" % repr(r), file=error_file, flush=True)
                root_set.add(r)
    if len(root_set) == 0:
        print("Warning: No nodes in the root set, the output file will be empty.", file=error_file, flush=True)
    elif verbose:
        print("%d nodes in the root set." % len(root_set), file=error_file, flush=True)


    property_set: typing.Set[str] = set()
    if props_file is not None:
        if verbose:
            print("Reading the root file %s" % repr(props_file),  file=error_file, flush=True)
        try:
            props_kr: KgtkReader = KgtkReader.open(Path(props_file),
                                                   error_file=error_file,
                                                   who="props",
                                                   options=props_reader_options,
                                                   value_options=value_options,
                                                   verbose=verbose,
                                                   very_verbose=very_verbose,
                                                   )
        except SystemExit:
            raise KGTKException("Exiting.")

        propscol: int
        if props_kr.is_edge_file:
            propscol = int(propsfilecolumn) if propsfilecolumn is not None and propsfilecolumn.isdigit() else props_kr.get_node1_column_index(propsfilecolumn)
        elif props_kr.is_node_file:
            propscol = int(propsfilecolumn) if propsfilecolumn is not None and propsfilecolumn.isdigit() else props_kr.get_id_column_index(propsfilecolumn)
        elif propsfilecolumn is not None:
            propscol = int(propsfilecolumn) if propsfilecolumn is not None and propsfilecolumn.isdigit() else props_kr.column_name_map.get(propsfilecolumn, -1)
        else:
            props_kr.close()
            raise KGTKException("The props file is neither an edge nor a node file and the root column name was not supplied.")

        if propscol < 0:
            props_kr.close()
            raise KGTKException("Unknown props column %s" % repr(propsfilecolumn))

        for row in props_kr:
            property_name: str = row[propscol]
            property_set.add(property_name)
        props_kr.close()
        
    if len(props) > 0:
        # Filter the graph, G, to include only edges where the predicate (label)
        # column contains one of the selected properties.

        prop_group: str
        for prop_group in props:
            prop: str
            for prop in prop_group.split(','):
                property_set.add(prop)
    if verbose and len(property_set) > 0:
        print("property set=%s" % " ".join(sorted(list(property_set))),  file=error_file, flush=True)
        

    undirected_property_set: typing.Set[str] = set()
    if undirected_props_file is not None:
        if verbose:
            print("Reading the undirected properties file %s" % repr(undirected_props_file),  file=error_file, flush=True)
        try:
            undirected_props_kr: KgtkReader = KgtkReader.open(Path(undirected_props_file),
                                                              error_file=error_file,
                                                              who="undirected_props",
                                                              options=undirected_props_reader_options,
                                                              value_options=value_options,
                                                              verbose=verbose,
                                                              very_verbose=very_verbose,
            )
        except SystemExit:
            raise KGTKException("Exiting.")

        undirected_props_col: int
        if undirected_props_kr.is_edge_file:
            undirected_props_col = int(undirectedpropsfilecolumn) if undirectedpropsfilecolumn is not None and undirectedpropsfilecolumn.isdigit() else undirected_props_kr.get_node1_column_index(undirectedpropsfilecolumn)
        elif undirected_props_kr.is_node_file:
            undirected_props_col = int(undirectedpropsfilecolumn) if undirectedpropsfilecolumn is not None and undirectedpropsfilecolumn.isdigit() else undirected_props_kr.get_id_column_index(undirectedpropsfilecolumn)
        elif undirectedpropsfilecolumn is not None:
            undirected_props_col = int(undirectedpropsfilecolumn) if undirectedpropsfilecolumn is not None and undirectedpropsfilecolumn.isdigit() else undirected_props_kr.column_name_map.get(undirectedpropsfilecolumn, -1)
        else:
            undirected_props_kr.close()
            raise KGTKException("The undirected props file is neither an edge nor a node file and the root column name was not supplied.")

        if undirected_props_col < 0:
            undirected_props_kr.close()
            raise KGTKException("Unknown undirected properties column %s" % repr(undirectedpropsfilecolumn))

        for row in undirected_props_kr:
            undirected_property_name: str = row[undirected_props_col]
            undirected_property_set.add(undirected_property_name)
        undirected_props_kr.close()
    if len(undirected_props) > 0:
        # Edges where the predicate (label) column contains one of the selected
        # properties will be treated as undirected links.

        und_prop_group: str
        for und_prop_group in undirected_props:
            und_prop: str
            for und_prop in und_prop_group.split(','):
                undirected_property_set.add(und_prop)
    if verbose and len(undirected_property_set) > 0:
        print("undirected property set=%s" % " ".join(sorted(list(undirected_property_set))),  file=error_file, flush=True)
        

    inverted_property_set: typing.Set[str] = set()
    if inverted_props_file is not None:
        if verbose:
            print("Reading the inverted properties file %s" % repr(inverted_props_file),  file=error_file, flush=True)
        try:
            inverted_props_kr: KgtkReader = KgtkReader.open(Path(inverted_props_file),
                                                            error_file=error_file,
                                                            who="inverted_props",
                                                            options=inverted_props_reader_options,
                                                            value_options=value_options,
                                                            verbose=verbose,
                                                            very_verbose=very_verbose,
            )
        except SystemExit:
            raise KGTKException("Exiting.")

        inverted_props_col: int
        if inverted_props_kr.is_edge_file:
            inverted_props_col = int(invertedpropsfilecolumn) if invertedpropsfilecolumn is not None and invertedpropsfilecolumn.isdigit() else inverted_props_kr.get_node1_column_index(invertedpropsfilecolumn)
        elif inverted_props_kr.is_node_file:
            inverted_props_col = int(invertedpropsfilecolumn) if invertedpropsfilecolumn is not None and invertedpropsfilecolumn.isdigit() else inverted_props_kr.get_id_column_index(invertedpropsfilecolumn)
        elif invertedpropsfilecolumn is not None:
            inverted_props_col = int(invertedpropsfilecolumn) if invertedpropsfilecolumn is not None and invertedpropsfilecolumn.isdigit() else inverted_props_kr.column_name_map.get(invertedpropsfilecolumn, -1)
        else:
            inverted_props_kr.close()
            raise KGTKException("The inverted props file is neither an edge nor a node file and the root column name was not supplied.")

        if inverted_props_col < 0:
            inverted_props_kr.close()
            raise KGTKException("Unknown inverted properties column %s" % repr(invertedpropsfilecolumn))

        for row in inverted_props_kr:
            inverted_property_name: str = row[inverted_props_col]
            inverted_property_set.add(inverted_property_name)
        inverted_props_kr.close()
        
    if len(inverted_props) > 0:
        # Edges where the predicate (label) column contains one of the selected
        # properties will have the source and target columns swapped.

        inv_prop_group: str
        for inv_prop_group in inverted_props:
            inv_prop: str
            for inv_prop in inv_prop_group.split(','):
                inverted_property_set.add(inv_prop)
    if verbose and len(inverted_property_set):
        print("inverted property set=%s" % " ".join(sorted(list(inverted_property_set))),  file=error_file, flush=True)
        

    try:
        kr: KgtkReader = KgtkReader.open(input_kgtk_file,
                                         error_file=error_file,
                                         who="input",
                                         options=input_reader_options,
                                         value_options=value_options,
                                         verbose=verbose,
                                         very_verbose=very_verbose,
                                         )
    except SystemExit:
        raise KGTKException("Exiting.")
        
    sub: int = kr.get_node1_column_index(subject_column_name)
    if sub < 0:
        print("Unknown subject column %s" % repr(subject_column_name), file=error_file, flush=True)

    pred: int = kr.get_label_column_index(predicate_column_name)
    if pred < 0:
        print("Unknown predicate column %s" % repr(predicate_column_name), file=error_file, flush=True)

    obj: int = kr.get_node2_column_index(object_column_name)
    if obj < 0:
        print("Unknown object column %s" % repr(object_column_name), file=error_file, flush=True)

    if sub < 0 or pred < 0 or obj < 0:
        kr.close()
        raise KGTKException("Exiting due to unknown column.")

    if verbose:
        print("special columns: sub=%d pred=%d obj=%d" % (sub, pred, obj),  file=error_file, flush=True)

    # G = load_graph_from_csv(filename,not(undirected),skip_first=not(header_bool),hashed=True,csv_options={'delimiter': '\t'},ecols=(sub,obj))
    G = load_graph_from_kgtk(kr,
                             directed=not undirected,
                             inverted=inverted,
                             ecols=(sub, obj),
                             pcol=pred,
                             pset=property_set,
                             upset=undirected_property_set,
                             ipset=inverted_property_set,
                             verbose=verbose,
                             out=error_file)

    name = G.vp["name"] # Get the vertex name property map (vertex to ndoe1 (subject) name)

    if show_properties:
        print("Graph name=%s" % repr(name), file=error_file, flush=True)
        print("Graph properties:" , file=error_file, flush=True)
        key: typing.Any
        for key in G.properties:
            print("    %s: %s" % (repr(key), repr(G.properties[key])), file=error_file, flush=True)

    index_list = []
    for v in G.vertices():
        if name[v] in root_set:
            index_list.append(v)
    if len(index_list) == 0:
        print("Warning: No root nodes found in the graph, the output file will be empty.", file=error_file, flush=True)
    elif verbose:
        print("%d root nodes found in the graph." % len(index_list), file=error_file, flush=True)

    if breadth_first and show_distance:
        output_header: typing.List[str] = ['node1','label','node2', dist_col_name]
    else:
        output_header: typing.List[str] = ['node1','label','node2']

    try:
        kw: KgtkWriter = KgtkWriter.open(output_header,
                                         output_kgtk_file,
                                         mode=KgtkWriter.Mode.EDGE,
                                         require_all_columns=True,
                                         prohibit_extra_columns=True,
                                         fill_missing_columns=False,
                                         verbose=verbose,
                                         very_verbose=very_verbose)
    except SystemExit:
        raise KGTKException("Exiting.")

    for index in index_list:
        if selflink_bool and show_distance:
            kw.writerow([name[index], label, name[index], 0])
        elif selflink_bool and not show_distance:
            kw.writerow([name[index], label, name[index]])
                
        if breadth_first:
            if depth_limit is None:
                if show_distance:
                    count = 0
                    past = set()
                    for e in bfs_iterator(G, G.vertex(index)):
                        if e.source() in past:
                            count += 1
                            past = set()
                        kw.writerow([name[index], label, name[e.target()], count+1])
                        past.add(e.target())

                else:
                    for e in bfs_iterator(G, G.vertex(index)):
                        kw.writerow([name[index], label, name[e.target()]])

            else:
                if show_distance:
                    class DepthExceeded(Exception):
                        pass

                    class DepthLimitedVisitor(BFSVisitor):
                        def __init__(self, name, pred, dist):
                            self.name = name
                            self.pred = pred
                            self.dist = dist

                        def tree_edge(self, e):
                            self.pred[e.target()] = int(e.source())
                            newdist = self.dist[e.source()] + 1

                            if depth_limit is not None and newdist > depth_limit:
                               raise DepthExceeded
                            self.dist[e.target()] = newdist

                            kw.writerow([name[index], label, name[e.target()], newdist])

                    dist = G.new_vertex_property("int")
                    pred = G.new_vertex_property("int64_t")

                    try:
                        bfs_search(G, G.vertex(index), DepthLimitedVisitor(name, pred, dist))
                    except DepthExceeded:
                        pass

                else:
                    class DepthExceeded(Exception):
                        pass

                    class DepthLimitedVisitor(BFSVisitor):
                        def __init__(self, name, pred, dist):
                            self.name = name
                            self.pred = pred
                            self.dist = dist

                        def tree_edge(self, e):
                            self.pred[e.target()] = int(e.source())
                            newdist = self.dist[e.source()] + 1
                            if depth_limit is not None and newdist > depth_limit:
                               raise DepthExceeded
                            self.dist[e.targt()] = newdist
                            kw.writerow([name[index], label, name[e.target()]])

                    dist = G.new_vertex_property("int")
                    pred = G.new_vertex_property("int64_t")
                    try:
                        bfs_search(G, G.vertex(index), DepthLimitedVisitor(name, pred, dist))
                    except DepthExceeded:
                        pass

        else:
            for e in dfs_iterator(G, G.vertex(index)):
                kw.writerow([name[index], label, name[e.target()]])

    kw.close()
    kr.close()

