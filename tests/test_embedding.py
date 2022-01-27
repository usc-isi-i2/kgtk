import unittest
import sys
from kgtk.cli_entry import cli_entry
import tempfile
import pandas as pd
import shutil


class TestEmbedding(unittest.TestCase):
    def setUp(self) -> None:
        self.edge_file_path = 'data/text_embedding.edges.tsv'
        self.true_output_file_path = 'data/text_embedding.output.tsv'
        self.true_output_w2v_file_path = 'data/text_embedding.output.w2v.txt'
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def test_kgtk_vector(self):
        cli_entry("kgtk", "text-embedding", "-i", self.edge_file_path,
                  "--model", "roberta-large-nli-mean-tokens",
                  "--debug",
                  "--sentence-property", "sentence",
                  "--output-property", "text_embedding",
                  "--batch-size", "-1",
                  "--output-data-format", "kgtk",
                  "-o", f'{self.temp_dir}/text-embedding.tsv')

        df_r = pd.read_csv(self.true_output_file_path, sep='\t')

        df = pd.read_csv(f'{self.temp_dir}/text-embedding.tsv', sep='\t')
        self.assertEqual(len(df), len(df_r))
        self.assertEqual(list(df.columns), list(df_r.columns))

        for temprow1, temprow2 in zip(df_r.iterrows(), df.iterrows()):
            row1, row2 = temprow1[1], temprow2[1]
            self.assertEqual(row1["node1"], row2["node1"])
            self.assertEqual(row1["label"], row2["label"])
            self.assertTrue(len(row2["node2"]) != 0)
            self.assertEqual(len(row1["node2"].split(",")), len(row2["node2"].split(",")))

    def test_w2v_vector(self):
        cli_entry("kgtk", "text-embedding", "-i", self.edge_file_path,
                  "--model", "roberta-large-nli-mean-tokens",
                  "--debug",
                  "--sentence-property", "sentence",
                  "--output-property", "text_embedding",
                  "--batch-size", "-1",
                  "--output-data-format", "w2v",
                  "-o", f'{self.temp_dir}/text-embedding.txt')

        with open(f'{self.temp_dir}/text-embedding.txt') as f1:
            o_lines = f1.readlines()

        with open(self.true_output_w2v_file_path) as f2:
            truth_lines = f2.readlines()
        self.assertEqual(len(o_lines), len(truth_lines))
        self.assertEqual(o_lines[0], truth_lines[0])

        for line1, line2 in zip(o_lines[1:], truth_lines[1:]):
            vals1 = line1.strip().split(" ")
            vals2 = line2.strip().split(" ")
            self.assertEqual(vals1[0], vals2[0])
            self.assertEqual(len(vals1), len(vals2))
