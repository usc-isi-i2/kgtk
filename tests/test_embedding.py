import unittest
import sys
from kgtk.cli_entry import cli_entry
import tempfile
import pandas as pd
import shutil

class TestEmbedding(unittest.TestCase):
    def setUp(self) -> None:
        self.edge_file_path = 'data/text_embedding.edges.tsv'
        self.labels_file_path = 'data/text_embedding.labels.tsv'
        self.true_output_file_path = 'data/text_embedding.output.tsv'
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def testvector(self):
        cli_entry("kgtk", "text-embedding", "-i", self.edge_file_path,
          "--model", "roberta-large-nli-mean-tokens",
          "--property-labels-file", self.labels_file_path,
          "--debug",
          "--isa-properties", "P31", "P279", "P106", "P39", "P1382", "P373", "P452",
          "--save-embedding-sentence", "--out-file", f'{self.temp_dir}/text-embedding.tsv')
		  
        df_r = pd.read_csv(self.true_output_file_path, sep='\t')

        df = pd.read_csv(f'{self.temp_dir}/text-embedding.tsv', sep='\t')
        self.assertEqual(len(df), len(df_r))
        self.assertEqual(list(df.columns), list(df_r.columns))

        for temprow1, temprow2 in zip(df_r.iterrows(), df.iterrows()):
            row1, row2 = temprow1[1], temprow2[1]
            self.assertEqual(row1["node"], row2["node"])
            self.assertEqual(row1["property"], row2["property"])
            self.assertEqual(row1["value"], row2["value"])

if __name__ == '__main__':
    a = TestEmbedding()
    a.setUp()
    a.testvector()
