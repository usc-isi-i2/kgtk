import unittest
from kgtk.cli_entry import cli_entry
from kgtk.cli.dummy import run
from kgtk.exceptions import KGTKException

class TestImportWordNet(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir=tempfile.mkdtemp()

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def test_import(self):
        cli_entry("kgtk", "import_wordnet", "-o", f'{self.temp_dir}/wordnet.tsv')

        df = pd.read_csv(f'{self.temp_dir}/wordnet.tsv', sep='\t')

        self.assertEqual(len(df.columns), 9)

        relations = list(df['relation'].unique())

        for r in ['/r/IsA', '/r/PartOf', '/r/MadeOf']:
            self.assertTrue(r in relations)

if __name__ == "__main__":
    unittest.main()
