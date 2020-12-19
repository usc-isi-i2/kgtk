import shutil
import unittest
import tempfile
import pandas as pd
from kgtk.cli_entry import cli_entry
from kgtk.exceptions import KGTKException

class TestImportFrameNet(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir=tempfile.mkdtemp()

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def test_kgtk_import_framenet(self):
        cli_entry("kgtk", "import_framenet", "-o", f'{self.temp_dir}/framenet.tsv')

        df = pd.read_csv(f'{self.temp_dir}/framenet.tsv', sep='\t', na_filter=False)

        self.assertEqual(len(df.columns), 9) # Make sure that the amount of columns is as expected

        self.assertEqual(len(df), 29873) # Make sure that the amount of rows is as expected

