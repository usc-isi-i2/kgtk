"""
Import an ATOMIC file to KGTK.

"""

import sys
from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles

def parser():
    return {
        'help': 'Import ATOMIC into KGTK.' 
    }

def add_arguments(parser: KGTKArgumentParser):
    """
    Parse arguments
    Args:
            parser (argparse.ArgumentParser)
    """
    parser.add_input_file(positional=True)
    parser.add_output_file()

def run(input_file: KGTKFiles, output_file: KGTKFiles):

    # import modules locally
    import sys # type: ignore
    from kgtk.exceptions import kgtk_exception_auto_handler, KGTKException
    import csv
    import re
    import json
    from pathlib import Path
    from string import Template
    import pandas as pd
    from kgtk.kgtkformat import KgtkFormat
    from kgtk.io.kgtkwriter import KgtkWriter

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
        if e1!=e2 and e2:
            return '|'.join([KgtkFormat.stringify(e1),KgtkFormat.stringify(e2)])
        else:
            return KgtkFormat.stringify(e1)

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
        return KgtkFormat.stringify(mapping[rel])

    try:

        filename: Path = KGTKArgumentParser.get_input_file(input_file)

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


        df = pd.read_csv(filename,index_col=0)
        df.iloc[:,:9] = df.iloc[:,:9].apply(lambda col: col.apply(json.loads))

        df.drop(df.columns[len(df.columns)-1], axis=1, inplace=True)
        df.drop(df.columns[len(df.columns)-1], axis=1, inplace=True)

        for event, row in df.iterrows():
            event_label=produce_node_labels(event)

            first_event_label=KgtkFormat.unstringify(event_label.split('|')[0] if '|' in event_label else event_label)
            n1=make_node(first_event_label)
            for c in df.columns:
                for v in row[c]:
                    if v=='none': continue
                    value_label=produce_node_labels(v)
                    first_value_label=KgtkFormat.unstringify(value_label.split('|')[0] if '|' in value_label else value_label)
                    n2=make_node(first_value_label)

                    rel_label=produce_rel_label(c)

                    sentence=''

                    relation=make_node(c)

                    this_row=[n1, relation, n2, event_label, value_label, rel_label, '', KgtkFormat.stringify('AT'), sentence]
                    ew.write(this_row)

        # Clean up.
        ew.close()

    except Exception as e:
        raise KGTKException('Error: ' + str(e))
