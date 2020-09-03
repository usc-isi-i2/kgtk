import shutil
import unittest
import tempfile
import pandas as pd
from kgtk.cli_entry import cli_entry


class TestKGTKFilter(unittest.TestCase):
    def setUp(self) -> None:
        self.file_path = 'data/sample_kgtk_edge_file.tsv'
        self.temp_dir = tempfile.mkdtemp()
        self.df = pd.read_csv(self.file_path, sep='\t')

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def test_kgtk_filter_p31(self):
        # create GT from the file itself using pandas
        p31_qnodes = list(self.df.loc[self.df['label'] == 'P31']['node1'].unique())

        cli_entry("kgtk", "filter", "-i", self.file_path, "-o", f'{self.temp_dir}/p31.tsv', "-p", ";P31;")

        df = pd.read_csv(f'{self.temp_dir}/p31.tsv', sep='\t')
        r_qnodes = list(df['node1'].unique())

        for q in r_qnodes:
            self.assertTrue(q in p31_qnodes)
        self.assertEqual(len(df), 10)

    def test_kgtk_filter_Q2447774(self):
        # create GT from the file itself using pandas
        node2s = list(self.df.loc[self.df['node1'] == 'Q2447774']['node2'])

        cli_entry("kgtk", "filter", "-i", self.file_path, "-o", f'{self.temp_dir}/Q2447774.tsv', "-p", "Q2447774;;")

        df = pd.read_csv(f'{self.temp_dir}/Q2447774.tsv', sep='\t')
        r_node2s = list(df['node2'])

        for q in r_node2s:
            self.assertTrue(q in node2s)
        self.assertEqual(len(df), 27)

    def test_kgtk_filter_one_row(self):
        cli_entry("kgtk", "filter", "-i", self.file_path, "-o", f'{self.temp_dir}/one_row.tsv', "-p",
                  "Q65695069;P577;^2019-07-19T00:00:00Z/11")

        df = pd.read_csv(f'{self.temp_dir}/one_row.tsv', sep='\t')

        self.assertEqual(len(df), 1)
