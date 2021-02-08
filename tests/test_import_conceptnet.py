import shutil
import unittest
import tempfile
import pandas as pd
from kgtk.cli_entry import cli_entry
from kgtk.exceptions import KGTKException

class TestKGTKImportConceptNet(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir=tempfile.mkdtemp()

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def test_kgtk_import_conceptnet(self):
        cli_entry("kgtk", "import-conceptnet", "--english_only", "-i", "data/conceptnet.csv", "-o", f'{self.temp_dir}/conceptnet.tsv')

        df = pd.read_csv(f'{self.temp_dir}/conceptnet.tsv', sep='\t')

        self.assertEqual(len(df), 77) # Make sure that there are 77 rows with English nodes out of the total 100

        self.assertEqual(df['node2'][0], '/c/en/1') # Make sure that the first node2 is the expected one

        self.assertEqual(len(df.columns), 9)

        relations = df['relation'].unique()

