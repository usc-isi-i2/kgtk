from kgtk.exceptions import KGTKException
import csv
import re
from pathlib import Path
from kgtk.kgtkformat import KgtkFormat
from kgtk.io.kgtkwriter import KgtkWriter


class ImportConceptNetPairs(object):
    def __init__(self,
                 input_file: Path,
                 output_kgtk_file: Path,
                 source: str,
                 relation: str = '/r/RelatedTo'):
        self.input_file = input_file
        self.output_kgtk_file = output_kgtk_file
        self.source = source
        self.relation = relation

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

            with open(self.input_file, 'r') as f:
                reader = csv.reader(f, delimiter=' ', quotechar='"')
                for row in reader:
                    ew.write(self.row_to_edge(row[0], self.relation, row[1], self.source, out_columns))

            # Clean up.
            ew.close()

        except Exception as e:
            raise KGTKException(e)

    @staticmethod
    def make_node_label(node):
        return KgtkFormat.stringify(node[3:])

    @staticmethod
    def split_camel_case(name):
        splitted = re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', name)).split()
        return ' '.join(splitted).lower()

    def make_rel_label(self, rel):
        return KgtkFormat.stringify(self.split_camel_case(rel.split('/')[-1]))

    def row_to_edge(self, node1, rel, node2, source, cols):
        edge = {}
        prefix = source.lower()
        edge['node1'] = prefix + ':' + node1
        edge['relation'] = rel
        edge['node2'] = prefix + ':' + node2
        edge['node1;label'] = self.make_node_label(node1)
        edge['node2;label'] = self.make_node_label(node2)
        edge['relation;label'] = self.make_rel_label(rel)
        edge['relation;dimension'] = ''

        edge['source'] = KgtkFormat.stringify(source)
        edge['sentence'] = ''

        edge_list = [edge[col] for col in cols]
        return edge_list
