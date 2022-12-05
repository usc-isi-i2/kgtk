from kgtk.exceptions import KGTKException
import csv
import re
from kgtk.kgtkformat import KgtkFormat
from kgtk.io.kgtkwriter import KgtkWriter
from pathlib import Path
import json


class ImportConceptNet(object):
    def __init__(self,
                 input_file: Path,
                 output_kgtk_file: Path,
                 info_kgtk_file: Path = None,
                 english_only: bool = False
                 ):
        self.input_file = input_file
        self.output_kgtk_file = output_kgtk_file
        self.info_kgtk_file = info_kgtk_file
        self.english_only = english_only

    @staticmethod
    def make_node_label(node):
        return KgtkFormat.stringify(node.strip().split('/')[3].replace('_', ' '))

    @staticmethod
    def split_camel_case(name):
        splitted = re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', name)).split()
        return ' '.join(splitted).lower()

    def make_rel_label(self, rel):
        return KgtkFormat.stringify(self.split_camel_case(rel.split('/')[-1]))

    @staticmethod
    def make_weight_edge(row):

        node1 = '%s-%s-%s-0000' % (row[2], row[1], row[3])
        rel = 'weight'
        node2 = str(json.loads(row[-1])['weight'])
        return [node1, rel, node2]

    def row_to_edge(self, row, cols):

        edge = {
            'node1': row[2],
            'relation': row[1],
            'node2': row[3],
            'node1;label': self.make_node_label(row[2]),
            'node2;label': self.make_node_label(row[3]),
            'relation;label': self.make_rel_label(row[1]),
            'relation;dimension': ''
        }

        metadata = json.loads(row[4])
        edge['source'] = KgtkFormat.stringify('CN')
        if 'surfaceText' in metadata.keys():
            edge['sentence'] = KgtkFormat.stringify(metadata['surfaceText'].replace('\\', ''))
        else:
            edge['sentence'] = ''

        edge_list = [edge[col] for col in cols]
        return edge_list

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

            if self.info_kgtk_file is not None:
                ew_aux: KgtkWriter = KgtkWriter.open(out_columns[:3],
                                                     self.info_kgtk_file,
                                                     require_all_columns=False,
                                                     prohibit_extra_columns=True,
                                                     fill_missing_columns=True,
                                                     gzip_in_parallel=False
                                                     )

            with open(self.input_file, 'r') as f:
                reader = csv.reader(f, delimiter='\t', quotechar='"')
                for row in reader:
                    if not self.english_only or (row[2].startswith('/c/en/') and row[3].startswith('/c/en/')):
                        ew.write(self.row_to_edge(row, out_columns))
                        if self.info_kgtk_file is not None and 'weight' in json.loads(row[-1]).keys():
                            ew_aux.write(self.make_weight_edge(row))

            # Clean up
            ew.close()
            if self.info_kgtk_file is not None:
                ew_aux.close()

        except Exception as e:
            raise KGTKException(e)
