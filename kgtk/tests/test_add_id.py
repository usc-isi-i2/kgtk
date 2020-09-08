import shutil
import unittest
import tempfile
import pandas as pd
from kgtk.cli_entry import cli_entry


class TestKGTKAddID(unittest.TestCase):
    def setUp(self) -> None:
        self.file_path = 'data/sample_kgtk_edge_file_no_id.tsv'
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def test_kgtk_add_id_default(self):
        cli_entry("kgtk", "add-id", "-i", self.file_path, "-o", f'{self.temp_dir}/id.tsv',
                  "--verify-id-unique",)
        df = pd.read_csv(f'{self.temp_dir}/id.tsv',sep='\t')
        for i, row in df.iterrows():
            self.assertEqual(row['id'], f'E{i+1}')
