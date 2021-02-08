import shutil
import unittest
import tempfile
import pandas as pd
from kgtk.cli_entry import cli_entry
from kgtk.exceptions import KGTKException

class TestImportVG(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir=tempfile.mkdtemp()

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def test_import(self):
        cli_entry("kgtk", "import-visualgenome", "-i", "data/vg10.tsv", "--attr-synsets", "data/attribute_synsets.json", "-o", f'{self.temp_dir}/vg.tsv')

        df = pd.read_csv(f'{self.temp_dir}/vg.tsv', sep='\t')

        self.assertEqual(len(df.columns), 9)

        relations = list(df['relation'].unique())

        self.assertEqual(len(df), 580)
