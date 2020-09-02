import shutil
import unittest
import tempfile
import pandas as pd
from kgtk.cli_entry import cli_entry


class TestKGTKFilter(unittest.TestCase):
    def setUp(self) -> None:
        self.file_path = 'data/sample_kgtk_edge_file.tsv'
        self.temp_dir = tempfile.mkdtemp()

    def test_kgtk_filter_p31(self):
        cli_entry("kgtk", "filter", "-i", self.file_path, "-o", f'{self.temp_dir}/p31.tsv', "-p", ";P31;")
        df = pd.read_csv(f'{self.temp_dir}/p31.tsv', sep='\t')
        self.assertEqual(len(df), 10)
        shutil.rmtree(self.temp_dir)


