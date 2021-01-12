"""
Find reachable nodes given a set of root nodes and properties
"""
from argparse import Namespace
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
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
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
    parser.add_argument("--props", action="store", type=str, dest="props", nargs="*",
                        help='Properties to consider while finding reachable nodes, space- or comma-separated string. (default: all properties)',default=None)
    parser.add_argument('--undirected', dest="undirected",
                        help="When True, specify graph as undirected. (default=%(default)s)",
                        type=optional_bool, nargs='?', const=True, default=False, metavar="True|False")
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

    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, expert=_expert)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, who="input", expert=_expert, defaults=False)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, who="root", expert=_expert, defaults=False)
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
        undirected: bool,
        label: str,
        selflink_bool: bool,
        show_properties: bool,
        breadth_first: bool,

        errors_to_stdout: bool,
        errors_to_stderr: bool,
        show_options: bool,
        verbose: bool,
        very_verbose: bool,

        **kwargs, # Whatever KgtkFileOptions and KgtkValueOptions want.
        ):
    import sys
    import csv
    from pathlib import Path
    import time
    from graph_tool.search import dfs_iterator, bfs_iterator
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
    value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)

    if root is None:
        root = [ ] # This simplifies matters.

    if props is None:
        props = [ ] # This simplifies matters.

    if show_options:
        if root is not None:
            print("--root %s" % " ".join(root), file=error_file)
        if rootfile is not None:
            print("--rootfile=%s" % rootfile, file=error_file)
        if subject_column_name is not None:
            print("--subj=%s" % subject_column_name, file=error_file)
        if object_column_name is not None:
            print("--obj=%s" % object_column_name, file=error_file)
        if predicate_column_name is not None:
            print("--pred=%s" % predicate_column_name, file=error_file)
        if props is not None:
            print("--props=%s" % " ".join(props), file=error_file)
        print("--undirected=%s" % str(undirected), file=error_file)
        print("--label=%s" % label, file=error_file)
        print("--selflink=%s" % str(selflink_bool), file=error_file)
        print("--breadth-first=%s" % str(breadth_first), file=error_file)
        input_reader_options.show(out=error_file)
        root_reader_options.show(out=error_file)
        value_options.show(out=error_file)
        KgtkReader.show_debug_arguments(errors_to_stdout=errors_to_stdout,
                                        errors_to_stderr=errors_to_stderr,
                                        show_options=show_options,
                                        verbose=verbose,
                                        very_verbose=very_verbose,
                                        out=error_file)
        print("=======", file=error_file, flush=True)

    root_set: typing.Set = set()
    property_list: typing.List = list()

    if rootfile is not None:
        if verbose:
            print("Reading the root file %s" % repr(rootfile),  file=error_file, flush=True)
        root_kr: KgtkReader = KgtkReader.open(Path(rootfile),
                                              error_file=error_file,
                                              who="root",
                                              options=root_reader_options,
                                              value_options=value_options,
                                              verbose=verbose,
                                              very_verbose=very_verbose,
                                              )

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


    kr: KgtkReader = KgtkReader.open(input_kgtk_file,
                                     error_file=error_file,
                                     who="input",
                                     options=input_reader_options,
                                     value_options=value_options,
                                     verbose=verbose,
                                     very_verbose=very_verbose,
                                     )
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
    G = load_graph_from_kgtk(kr, directed=not undirected, ecols=(sub, obj), verbose=verbose, out=error_file)

    name = G.vp["name"] # Get the vertix name property map (vertex to ndoe1 (subject) name)

    if show_properties:
        print("Graph name=%s" % name, file=error_file, flush=True)
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

    if len(props) > 0:
        # Since the root file is a KGTK file, the columns will have names.
        # pred_label: str = 'c'+str(find_pred_position(sub, pred, obj))
        pred_label: str = kr.column_names[pred]
        if verbose:
            print("pred_label=%s" % repr(pred_label),  file=error_file, flush=True)
        
        
        property_list =  [ ]
        prop_group: str
        for prop_group in props:
            prop: str
            for prop in prop_group.split(','):
                property_list.append(prop)
        if verbose:
            print("property list=%s" % " ".join(property_list),  file=error_file, flush=True)
        
        edge_filter_set = set()
        for prop in property_list:
            edge_filter_set.update(get_edges_by_edge_prop(G, pred_label, prop))
        G.clear_edges()
        G.add_edge_list(list(edge_filter_set))

    output_header: typing.List[str] = ['node1','label','node2']

    kw: KgtkWriter = KgtkWriter.open(output_header,
                                     output_kgtk_file,
                                     mode=KgtkWriter.Mode.EDGE,
                                     require_all_columns=True,
                                     prohibit_extra_columns=True,
                                     fill_missing_columns=False,
                                     verbose=verbose,
                                     very_verbose=very_verbose)
    for index in index_list:
        if selflink_bool:
            kw.writerow([name[index], label, name[index]])
                
        if breadth_first:
            for e in bfs_iterator(G, G.vertex(index)):
                kw.writerow([name[index], label, name[e.target()]])
        else:
            for e in dfs_iterator(G, G.vertex(index)):
                kw.writerow([name[index], label, name[e.target()]])

    kw.close()
    kr.close()
