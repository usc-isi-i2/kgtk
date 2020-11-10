"""
Import concept pairs into KGTK.
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
    parser.add_output_file()

def run(input_file: KGTKFiles, relation, source, output_file: KGTKFiles):

    # import modules locally
    import sys # type: ignore
    from kgtk.exceptions import kgtk_exception_auto_handler
    import csv
    import json
    import re
    from pathlib import Path
    from string import Template
    from kgtk.kgtkformat import KgtkFormat
    from kgtk.io.kgtkwriter import KgtkWriter

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
        edge['node1;label']=make_node_label(node1)
        edge['node2;label']=make_node_label(node2)
        edge['relation;label']=make_rel_label(rel)
        edge['relation;dimension']=''

        edge['source']=KgtkFormat.stringify(source)
        edge['sentence']=''
        
        edge_list=[edge[col] for col in cols]
        return edge_list

    try:
        filename: Path = KGTKArgumentParser.get_input_file(input_file)

        in_columns=['assertion','rel','subj','obj','metadata']
        out_columns=['node1', 'relation', 'node2', 'node1;label', 'node2;label','relation;label', 'relation;dimension', 'source', 'sentence']

        output_kgtk_file: Path = KGTKArgumentParser.get_output_file(output_file)
        ew: KgtkWriter = KgtkWriter.open(out_columns,
                                         output_kgtk_file,
                                         #mode=input_kr.mode,
                                         require_all_columns=False,
                                         prohibit_extra_columns=True,
                                         fill_missing_columns=True,
                                         gzip_in_parallel=False,
                                         #verbose=self.verbose,
                                         #very_verbose=self.very_verbose
                                         )

        with open(filename, 'r') as f:
            reader = csv.reader(f, delimiter=' ', quotechar='"')
            #sys.stdout.write(header_to_edge(out_columns))
            for row in reader:
                ew.write(row_to_edge(row[0], relation, row[1], source, out_columns))

        # Clean up.
        ew.close()

    except Exception as e:
        kgtk_exception_auto_handler(e)
