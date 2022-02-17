import shutil
import unittest
import tempfile
import pandas as pd
from kgtk.cli_entry import cli_entry
from kgtk.exceptions import KGTKArgumentParseException
import glob


class TestKGTKAugment(unittest.TestCase):
    def setUp(self) -> None:
        self.file_path = 'data/test_augment.tsv'
        self.output_folder_path = 'data/augment_folder'
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def test_kgtk_add_id_default(self):
        cli_entry("kgtk", "augment", "-i", self.file_path, "--output-path", self.output_folder_path,
                  "--verify-id-unique", )
        df = pd.read_csv(self.file_path, sep='\t')
        files = glob.glob(f'{self.output_folder_path}/*/*.tsv')
        
        for file in files:
            df_temp = pd.read_csv(self.file_path, sep='\t')
            self.assertEqual(len(df), len(df_temp))