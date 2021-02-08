import shutil
import unittest
import tempfile
import pandas as pd
from kgtk.cli_entry import cli_entry
from kgtk.exceptions import KGTKException

class TestKGTKImportAtomic(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir=tempfile.mkdtemp()

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def test_kgtk_import_atomic(self):
        cli_entry("kgtk", "import-atomic", "-i", "data/atomic.csv", "-o", f'{self.temp_dir}/atomic.tsv')

        df = pd.read_csv(f'{self.temp_dir}/atomic.tsv', sep='\t')

        self.assertEqual(len(df.columns), 9)

        relations = df['relation'].unique()

        self.assertTrue('at:xAttr' in relations)
