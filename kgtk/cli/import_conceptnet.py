"""
Import ConceptNet file to KGTK.
"""


import sys

def parser():
    return {
        'help': 'Import ConceptNet into KGTK.' 
    }


def add_arguments(parser):
    """
    Parse arguments
    Args:
            parser (argparse.ArgumentParser)
    """
    # '$label == "/r/DefinedAs" && $node2=="/c/en/number_zero"'
    parser.add_argument(action="store", type=str, dest="filename", metavar='filename', help='filename here')
    parser.add_argument('--english_only', action="store_true", help="Only english conceptnet?")


def run(filename, english_only):

    # import modules locally
    import sys # type: ignore
    from kgtk.exceptions import kgtk_exception_auto_handler
    import csv
    import re
    import json
    from string import Template

    def header_to_edge(row):
        row=[r.replace('_', ';') for r in row]
        return '\t'.join(row) + '\n'

    def make_node_label(node):
        return node.strip().split('/')[3].replace('_', ' ')

    def split_camel_case(name):
        splitted = re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', name)).split()
        return ' '.join(splitted).lower()

    def make_rel_label(rel):
        return split_camel_case(rel.split('/')[-1])

    def get_template(label):
        t={
            'antonym': Template('What is the opposite from $node1?'),
            'at location': Template('At what location is $node1?'),
            'capable of': Template('What is $node1 capable of?'),
            'causes': Template('What is caused by $node1?'),
            'causes desire': Template('What desire is caused by $node1?'),
            'created by': Template('What can create $node1?'),
            'defined as': Template('How can $node1 be defined?'),
            'derived from': Template('From which word is $node1 derived?'),
            'desires': Template('What does $node1 desire?'),
            'distinct from': Template('What is $node1 distinct from?'),
            'etymologically derived from': Template('What is $node1 etymologically derived from?'),
            'symbol of': Template('What is $node1 symbol of?'),
            'synonym': Template('What is a synonym of $node1?'),
            'manner of': Template('$node1 is a manner of what?'),
            'located near': Template('What is $node1 located near to?'),
            'has context': Template('What is a context of $node1?'),
            'similar to': Template('What is $node1 similar to?'),
            'etymologically related to': Template("What is $node1 etymologically related to?"),
            'made of': Template('What is $node1 made of?'),
            'receives action': Template('What can be done to $node1?'),
            'obstructed by': Template('What is $node1 obstructed by?'),
            'motivated by goal': Template('What goal motivates $node1?'),
            'has property': Template('What is a property of $node1?'),
            'has prerequisite': Template('What is a prerequisite for $node1?'),
            'has first subevent': Template('What is the first subevent of $node1?'),
            'has last subevent': Template('What is the last subevent of $node1?'),
            'has subevent': Template('What is a subevent of $node1?'),
            'used for': Template('What is $node1 used for?'),
            'has a': Template('What belongs to $node1?'),
            'is a': Template('What is a $node1?'),
            'form of': Template('What is $node1 a form of?'),
            'related to': Template('What is $node1 related to?')
            }
        if label in t.keys():
            return t[label]
        else:
            return None

    def make_question(node1, label, node2):
        t=get_template(label)
        return t.substitute(node1=node1)

    def row_to_edge(row, cols):

        edge={}
        edge['node1']=row[2]
        edge['label']=row[1]
        edge['node2']=row[3]
        edge['node1_label']=make_node_label(row[2])
        edge['node2_label']=make_node_label(row[3])
        edge['label_label']=make_rel_label(row[1])
        edge['label_dimension']=''

        metadata=json.loads(row[4])
        edge['weight']=str(metadata['weight'])
        edge['source']='CN'
        edge['creator']=metadata['dataset']
        if 'surfaceText' in metadata.keys():
            edge['sentence']=metadata['surfaceText']
        else:
            edge['sentence']=''
        
        t=get_template(edge['label_label'])
        if t:
            edge['question']=t.substitute(node1=edge['node1_label'])
        else:
            return ''

        edge_list=[edge[col] for col in cols]
        return '\t'.join(edge_list) + '\n'

    try:
        in_columns=['assertion','rel','subj','obj','metadata']
        out_columns=['node1', 'label', 'node2', 'node1_label', 'label_label', 'node2_label', 'label_dimension', 'source', 'weight', 'creator', 'sentence', 'question']

        with open(filename, 'r') as f:
            reader = csv.reader(f, delimiter='\t', quotechar='"')
            sys.stdout.write(header_to_edge(out_columns))
            for row in reader:
                if not english_only or (row[2].startswith('/c/en/') and row[3].startswith('/c/en/')):
                    sys.stdout.write(row_to_edge(row, out_columns))

    except Exception as e:
            kgtk_exception_auto_handler(e)
