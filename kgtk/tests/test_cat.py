import shutil
import unittest
import tempfile
import pandas as pd
from kgtk.cli_entry import cli_entry
from kgtk.cli.filter import run
from kgtk.exceptions import KGTKException
from pathlib import Path


class TestKGTKCat(unittest.TestCase):
    def setUp(self) -> None:
        self.file_path = 'data/sample_kgtk_edge_file.tsv'
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def test_kgtk_cat(self):
        cli_entry("kgtk", "cat", "-i", self.file_path, "-o", f'{self.temp_dir}/cat.tsv', "--verbose")

        df_r = pd.read_csv(f'{self.temp_dir}/cat.tsv', sep='\t')

        df = pd.read_csv(f'{self.file_path}', sep='\t')
        self.assertEqual(len(df), len(df_r))
        self.assertEqual(list(df.columns), list(df_r.columns))

        f = open(self.file_path)
        lines = f.readlines()
        f.close()
        for i, row in df_r.iterrows():
            self.assertEqual(row["id"], lines[i + 1].split('\t')[0])
