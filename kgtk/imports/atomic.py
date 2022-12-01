from kgtk.exceptions import KGTKException
import json
from pathlib import Path
import pandas as pd
from kgtk.kgtkformat import KgtkFormat
from kgtk.io.kgtkwriter import KgtkWriter


class ImportAtomic(object):
    def __init__(self,
                 input_file: Path,
                 output_kgtk_file: Path):
        self.input_file = input_file
        self.output_kgtk_file = output_kgtk_file

    def process(self):
        try:

            out_columns = ['node1', 'relation', 'node2', 'node1;label', 'node2;label', 'relation;label',
                           'relation;dimension', 'source', 'sentence']

            ew: KgtkWriter = KgtkWriter.open(out_columns,
                                             self.output_kgtk_file,
                                             require_all_columns=False,
                                             prohibit_extra_columns=True,
                                             fill_missing_columns=True,
                                             gzip_in_parallel=False
                                             )

            df = pd.read_csv(self.input_file, index_col=0)
            df.iloc[:, :9] = df.iloc[:, :9].apply(lambda col: col.apply(json.loads))

            df.drop(df.columns[len(df.columns) - 1], axis=1, inplace=True)
            df.drop(df.columns[len(df.columns) - 1], axis=1, inplace=True)

            for event, row in df.iterrows():
                event_label = self.produce_node_labels(event)

                first_event_label = KgtkFormat.unstringify(
                    event_label.split('|')[0] if '|' in event_label else event_label)
                n1 = self.make_node(first_event_label)
                for c in df.columns:
                    for v in row[c]:
                        if v == 'none':
                            continue
                        value_label = self.produce_node_labels(v)
                        first_value_label = KgtkFormat.unstringify(
                            value_label.split('|')[0] if '|' in value_label else value_label)
                        n2 = self.make_node(first_value_label)

                        rel_label = self.produce_rel_label(c)

                        sentence = ''

                        relation = self.make_node(c)

                        this_row = [n1, relation, n2, event_label, value_label, rel_label, '',
                                    KgtkFormat.stringify('AT'), sentence]
                        ew.write(this_row)

            # Clean up.
            ew.close()

        except Exception as e:
            raise KGTKException('Error: ' + str(e))

    @staticmethod
    def make_node(x):
        und_x = x.replace(' ', '_')
        pref_und_x = 'at:%s' % und_x
        return pref_und_x

    @staticmethod
    def remove_people_mentions(event):
        e = event.replace('personx', '').strip()
        e = e.replace('persony', '').strip()
        e = e.replace('person x', '').strip()
        e = e.replace('person y', '').strip()
        e = e.replace('the ___', '')
        e = e.replace('___', '')
        e = e.replace("'s", '')
        e = e.replace('to y', '')
        return e.strip()

    def produce_node_labels(self, event):
        if '\t' in event:
            event = event.split('\t')[0]
        e1 = event.lower()
        e1 = e1.rstrip('.').strip()
        e2 = self.remove_people_mentions(e1)
        while '  ' in e2:
            e2 = e2.replace('  ', ' ')
        if e1 != e2 and e2:
            return '|'.join([KgtkFormat.stringify(e1), KgtkFormat.stringify(e2)])
        else:
            return KgtkFormat.stringify(e1)

    @staticmethod
    def produce_rel_label(rel):
        mapping = {
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
