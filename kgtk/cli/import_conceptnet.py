"""
Import ConceptNet into KGTK.

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
    parser.add_output_file()
    parser.add_output_file(who="A KGTK output file that will contain only the weights.",
                           dest="weights_file",
                           options=["--weights-file"],
                           metavar="WEIGHTS_FILE",
                           optional=True)

def run(input_file: KGTKFiles, english_only, output_file: KGTKFiles, weights_file: KGTKFiles):

    # import modules locally
    import sys # type: ignore
    from kgtk.exceptions import kgtk_exception_auto_handler
    import csv
    import json
    import re
    from pathlib import Path
    from kgtk.kgtkformat import KgtkFormat
    from kgtk.io.kgtkwriter import KgtkWriter

    def make_node_label(node):
        return KgtkFormat.stringify(node.strip().split('/')[3].replace('_', ' '))

    def split_camel_case(name):
        splitted = re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', name)).split()
        return ' '.join(splitted).lower()

    def make_rel_label(rel):
        return KgtkFormat.stringify(split_camel_case(rel.split('/')[-1]))

    def make_weight_edge(row):

        node1='%s-%s-%s-0000' % (row[2], row[1], row[3])
        rel='weight'
        node2=str(json.loads(row[-1])['weight'])
        return [node1, rel, node2]

    def row_to_edge(row, cols):

        edge={}
        edge['node1']=row[2]
        edge['relation']=row[1]
        edge['node2']=row[3]
        edge['node1;label']=make_node_label(row[2])
        edge['node2;label']=make_node_label(row[3])
        edge['relation;label']=make_rel_label(row[1])
        edge['relation;dimension']=''

        metadata=json.loads(row[4])
        edge['source']=KgtkFormat.stringify('CN')
        if 'surfaceText' in metadata.keys():
            edge['sentence']=KgtkFormat.stringify(metadata['surfaceText'].replace('\\', ''))
        else:
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

        if weights_file:
            info_kgtk_file: Path = KGTKArgumentParser.get_output_file(weights_file)
            ew_aux: KgtkWriter = KgtkWriter.open(out_columns[:3],
                                             info_kgtk_file,
                                             #mode=input_kr.mode,
                                             require_all_columns=False,
                                             prohibit_extra_columns=True,
                                             fill_missing_columns=True,
                                             gzip_in_parallel=False,
                                             #verbose=self.verbose,
                                             #very_verbose=self.very_verbose
                                             )

        with open(filename, 'r') as f:
            reader = csv.reader(f, delimiter='\t', quotechar='"')
            for row in reader:
                if not english_only or (row[2].startswith('/c/en/') and row[3].startswith('/c/en/')):
                    ew.write(row_to_edge(row, out_columns))
                    if weights_file and 'weight' in json.loads(row[-1]).keys():
                        ew_aux.write(make_weight_edge(row))

        # Clean up
        ew.close()
        if weights_file:
            ew_aux.close()

    except Exception as e:
        kgtk_exception_auto_handler(e)
