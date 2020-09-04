import shutil
import unittest
import tempfile
import pandas as pd
from kgtk.cli_entry import cli_entry


class TestKGTKFilter(unittest.TestCase):
    def setUp(self) -> None:
        self.file_path = 'data/sample_kgtk_edge_file.tsv'
        self.Q47158_path = 'data/sample_kgtk_edge_Q47158.tsv'
        self.temp_dir = tempfile.mkdtemp()
        self.df = pd.read_csv(self.file_path, sep='\t')

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def test_kgtk_ifexists(self):
        cli_entry("kgtk", "ifexists", "-i", self.file_path, "--filter-on", self.Q47158_path, "-o",
                  f'{self.temp_dir}/Q47158.tsv', "--input-keys", "node1", "--filter-keys", "node1", "--show-option")

        df = pd.read_csv(f'{self.temp_dir}/Q47158.tsv', sep='\t')

        self.assertEqual(len(df), 118)
