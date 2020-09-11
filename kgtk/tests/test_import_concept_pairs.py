import shutil
import unittest
import tempfile
import pandas as pd
from kgtk.cli_entry import cli_entry
from kgtk.exceptions import KGTKException

class TestKGTKImportConceptPairs(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir=tempfile.mkdtemp()

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def test_kgtk_import_concept_pairs(self):
        cli_entry("kgtk", "import-concept-pairs", "-i", "data/synonyms.txt", "--source", "RG", "--relation", "/r/Synonym", "-o", f'{self.temp_dir}/roget_syn.tsv')

        df = pd.read_csv(f'{self.temp_dir}/roget_syn.tsv', sep='\t')

        self.assertEqual(len(df.columns), 9)

        for i, row in df.iterrows():
            self.assertTrue(row['relation']=='/r/Synonym')
        print('ROGET', df)
