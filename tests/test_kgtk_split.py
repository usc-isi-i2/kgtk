import os
import shutil
import unittest
import tempfile
import pandas as pd
from kgtk.cli_entry import cli_entry


class TestKGTKFilter(unittest.TestCase):
    def setUp(self) -> None:
        self.file_path = 'data/wikidata_sample.tsv'
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def test_kgtk_split_by_qnode(self):
        df = pd.read_csv(self.file_path, sep='\t')
        qnodes = list(df['node1'].unique())

        cli_entry("kgtk", "split", "-i", self.file_path, "--output-path", self.temp_dir, "--split-by-qnode")
        for qnode in qnodes:
            self.assertTrue(os.path.exists(f'{self.temp_dir}/{qnode}.tsv'))
        self.assertEqual(len(pd.read_csv(f'{self.temp_dir}/Q1000133.tsv', sep='\t')), 8)

    def test_kgtk_split_by_lines(self):

        cli_entry("kgtk", "split", "-i", self.file_path, "--output-path", self.temp_dir, "--lines", '5000')

        self.assertTrue(os.path.exists(f'{self.temp_dir}/split_0.tsv'))
        self.assertTrue(os.path.exists(f'{self.temp_dir}/split_1.tsv'))
        qnodes_0 = list(pd.read_csv(f'{self.temp_dir}/split_0.tsv', sep='\t')['node1'].unique())
        qnodes_1 = list(pd.read_csv(f'{self.temp_dir}/split_1.tsv', sep='\t')['node1'].unique())
        for qnode in qnodes_0:
            self.assertTrue(qnode not in qnodes_1)

    def test_kgtk_split_by_lines_gzipped(self):

        cli_entry("kgtk", "split", "-i", self.file_path, "--output-path", self.temp_dir, "--lines", '10000',
                  "--gzipped-output")

        self.assertTrue(os.path.exists(f'{self.temp_dir}/split_0.tsv.gz'))
        df = pd.read_csv(f'{self.temp_dir}/split_0.tsv.gz', sep='\t')
        self.assertEqual(len(df), 9993)
        self.assertEqual(len(list(df['node1'].unique())), 1718)
