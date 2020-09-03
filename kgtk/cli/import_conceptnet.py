"""
Import ConceptNet into KGTK.

TODO: Add --output-file
"""

import sys
from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles

def parser():
    return {
        'help': 'Import ConceptNet into KGTK.' 
    }

def add_arguments(parser: KGTKArgumentParser):
    """
    Parse arguments
    Args:
            parser (argparse.ArgumentParser)
    """
    parser.add_input_file(positional=True)
    parser.add_argument('--english_only', action="store_true", help="Only english conceptnet?")


def run(input_file: KGTKFiles, english_only):

    # import modules locally
    import sys # type: ignore
    from kgtk.exceptions import kgtk_exception_auto_handler
    import csv
    import json
    import re
    from pathlib import Path
    from kgtk.kgtkformat import KgtkFormat

    def header_to_edge(row):
        row=[r.replace('_', ';') for r in row]
        return '\t'.join(row) + '\n'

    def make_node_label(node):
        return KgtkFormat.stringify(node.strip().split('/')[3].replace('_', ' '))

    def split_camel_case(name):
        splitted = re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', name)).split()
        return ' '.join(splitted).lower()

    def make_rel_label(rel):
        return KgtkFormat.stringify(split_camel_case(rel.split('/')[-1]))

    def row_to_edge(row, cols):

        edge={}
        edge['node1']=row[2]
        edge['relation']=row[1]
        edge['node2']=row[3]
        edge['node1_label']=make_node_label(row[2])
        edge['node2_label']=make_node_label(row[3])
        edge['relation_label']=make_rel_label(row[1])
        edge['relation_dimension']=''

        metadata=json.loads(row[4])
        edge['source']=KgtkFormat.stringify('CN')
        if 'surfaceText' in metadata.keys():
            edge['sentence']=KgtkFormat.stringify(metadata['surfaceText'].replace('\\', ''))
        else:
            edge['sentence']=''
        
        edge_list=[edge[col] for col in cols]
        return '\t'.join(edge_list) + '\n'

    try:
        filename: Path = KGTKArgumentParser.get_input_file(input_file)

        in_columns=['assertion','rel','subj','obj','metadata']
        out_columns=['node1', 'relation', 'node2', 'node1_label', 'node2_label','relation_label', 'relation_dimension', 'source', 'sentence']

        with open(filename, 'r') as f:
            reader = csv.reader(f, delimiter='\t', quotechar='"')
            sys.stdout.write(header_to_edge(out_columns))
            for row in reader:
                if not english_only or (row[2].startswith('/c/en/') and row[3].startswith('/c/en/')):
                    sys.stdout.write(row_to_edge(row, out_columns))

    except Exception as e:
            kgtk_exception_auto_handler(e)
