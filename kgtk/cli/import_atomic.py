"""
Import an ATOMIC file to KGTK.
"""

import sys

def parser():
    return {
        'help': 'Import ATOMIC into KGTK.' 
    }

def add_arguments(parser):
    """
    Parse arguments
    Args:
            parser (argparse.ArgumentParser)
    """
    parser.add_argument(action="store", type=str, dest="filename", metavar='filename', help='filename here')


def run(filename):

    # import modules locally
    import sys # type: ignore
    from kgtk.exceptions import kgtk_exception_auto_handler
    import csv
    import re
    import json
    from string import Template
    import pandas as pd

    def header_to_edge(row):
        row=[r.replace('_', ';') for r in row]
        return '\t'.join(row) + '\n'

    def make_node(x):
        und_x=x.replace(' ', '_')
        pref_und_x='at:%s' % und_x
        return pref_und_x

    def remove_people_mentions(event):
        e=event.replace('personx', '').strip()
        e=e.replace('persony', '').strip()
        e=e.replace('person x', '').strip()
        e=e.replace('person y', '').strip()
        e=e.replace('the ___', '')
        e=e.replace('___', '')
        e=e.replace("'s", '')
        e=e.replace('to y', '')
        return e.strip()


    def produce_node_labels(event):
        if '\t' in event:
            event=event.split('\t')[0]
        e1=event.lower()
        e1=e1.rstrip('.').strip()
        e2=remove_people_mentions(e1)
        while '  ' in e2:
            e2=e2.replace('  ', ' ')
        if e1!=e2:
            return '|'.join([e1,e2])
        else:
            return e1

    def produce_rel_label(rel):
        mapping={
                    'xAttr': 'person x has attribute',
                    'oAttr': 'others have attribute',
                    'xReact': 'person x feels',
                    'oReact': 'others feel',
                    'xIntent': 'person x wants',
                    'xWant': 'person x wants',
                    'oWant': 'others want',
                    'xNeed': 'person x needs',
                    'xEffect': 'effect on person x',
                    'oEffect': 'the effect on others'
                }
        return mapping[rel]

    def make_question(n1, lbl):
        return f'If {n1}, then {lbl}?' 

    def make_sentence(node_label, rel_label, value_label):
        return 'If %s, then %s %s.' % (node_label, rel_label, value_label)

    try:

        out_columns=['node1', 'label', 'node2', 'node1_label', 'label_label', 'node2_label', 'label_dimension', 'source', 'weight', 'creator', 'sentence', 'question']

        df = pd.read_csv(filename,index_col=0)
        df.iloc[:,:9] = df.iloc[:,:9].apply(lambda col: col.apply(json.loads))

        df.drop(df.columns[len(df.columns)-1], axis=1, inplace=True)
        df.drop(df.columns[len(df.columns)-1], axis=1, inplace=True)

        sys.stdout.write(header_to_edge(out_columns))

        for event, row in df.iterrows():
            event_label=produce_node_labels(event)

            first_event_label=event_label.split('|')[0] if '|' in event_label else event_label
            n1=make_node(first_event_label)
            for c in df.columns:
                for v in row[c]:
                    if v=='none': continue
                    value_label=produce_node_labels(v)
                    first_value_label=value_label.split('|')[0] if '|' in value_label else value_label
                    n2=make_node(first_value_label)

                    rel_label=produce_rel_label(c)

                    sentence=make_sentence(first_event_label, rel_label, first_value_label)

                    question=make_question(first_event_label, rel_label)

                    label=make_node(c)

                    this_row=[n1, label, n2, event_label, rel_label, value_label, '', 'AT', "1.0", "", sentence, question]

                    sys.stdout.write('\t'.join(this_row) + '\n')

    except Exception as e:
        raise KGTKException('Error: ' + str(e))
