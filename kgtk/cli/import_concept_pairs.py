"""
Import concept pairs into KGTK.

TODO: Add --output-file
"""

import sys
from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles

def parser():
    return {
        'help': 'Import concept pairs into KGTK.' 
    }

def add_arguments(parser: KGTKArgumentParser):
    """
    Parse arguments
    Args:
            parser (argparse.ArgumentParser)
    """
    parser.add_input_file(positional=True)
    parser.add_argument('--relation', action="store", default="/r/RelatedTo", type=str, dest="relation", help="Relation to connect the word pairs with.")
    parser.add_argument('--source', action="store", type=str, dest="source", help="Source identifier")

def run(input_file: KGTKFiles, relation, source):

    # import modules locally
    import sys # type: ignore
    from kgtk.exceptions import kgtk_exception_auto_handler
    import csv
    import json
    import re
    from pathlib import Path
    from string import Template
    from kgtk.kgtkformat import KgtkFormat

    def header_to_edge(row):
        row=[r.replace('_', ';') for r in row]
        return '\t'.join(row) + '\n'

    def make_node_label(node):
        return KgtkFormat.stringify(node[3:])

    def split_camel_case(name):
        splitted = re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', name)).split()
        return ' '.join(splitted).lower()

    def make_rel_label(rel):
        return KgtkFormat.stringify(split_camel_case(rel.split('/')[-1]))

    def row_to_edge(node1, rel, node2, source, cols):

        edge={}
        prefix=source.lower()
        edge['node1']=prefix + ':' + node1
        edge['relation']=rel
        edge['node2']=prefix + ':' + node2
        edge['node1_label']=make_node_label(node1)
        edge['node2_label']=make_node_label(node2)
        edge['relation_label']=make_rel_label(rel)
        edge['relation_dimension']=''

        edge['source']=KgtkFormat.stringify(source)
        edge['sentence']=''
        
        edge_list=[edge[col] for col in cols]
        return '\t'.join(edge_list) + '\n'

    try:
        filename: Path = KGTKArgumentParser.get_input_file(input_file)

        in_columns=['assertion','rel','subj','obj','metadata']
        out_columns=['node1', 'relation', 'node2', 'node1_label', 'node2_label','relation_label', 'relation_dimension', 'source', 'sentence']

        with open(filename, 'r') as f:
            reader = csv.reader(f, delimiter=' ', quotechar='"')
            sys.stdout.write(header_to_edge(out_columns))
            for row in reader:
                sys.stdout.write(row_to_edge(row[0], relation, row[1], source, out_columns))

    except Exception as e:
        kgtk_exception_auto_handler(e)
