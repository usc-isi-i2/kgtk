import shutil
import unittest
import tempfile
import pandas as pd
from kgtk.cli_entry import cli_entry
from kgtk.exceptions import KGTKException
import time

class TestKGTKImportCSV(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir=tempfile.mkdtemp()

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def test_kgtk_import_csv_basic(self):
        cli_entry("kgtk", "import-csv", 
            "-i", "data/cities.csv", 
            "-o", f'{self.temp_dir}/cities.tsv',
            "--id-column", "geonameid",
        )

        df = pd.read_csv(f'{self.temp_dir}/cities.tsv', sep='\t')

        self.assertEqual(len(df.columns), 3)
        self.assertEqual(len(df), 23018 * 3)

        labels = df['label'].unique()

        expected_labels = ['name', 'country', 'subcountry']

        for expected_label in expected_labels:
            self.assertTrue(expected_label in labels)


        for expected_label in expected_labels:
            self.assertTrue(expected_label in labels)

    def test_kgtk_import_csv_with_add_id(self):
        cli_entry("kgtk", "import-csv", 
            "-i", "data/Paintings.csv", 
            "-o", f'{self.temp_dir}/Paintings.tsv',
            "--add-id",
        )

        df = pd.read_csv(f'{self.temp_dir}/Paintings.tsv', sep='\t')

        self.assertEqual(len(df.columns), 3)

        ids = df['node1'].unique()
        self.assertEqual(len(ids), 55)

        labels = df['label'].unique()

        expected_labels = [
            'Painting', 'Artist', 'Year of Painting', 'Adjusted Price', 'Original Price', 
            'Date of Sale', 'Year of Sale', 'Seller', 'Buyer', 'Auction House', 'Image', 
            'Painting Wikipedia Profile', 'Artist Wikipedia Profile', 'Description'
        ]

        for expected_label in expected_labels:
            self.assertTrue(expected_label in labels)

    def test_kgtk_import_csv_column_separator(self):
        cli_entry("kgtk", "import-csv", 
            "-i", "data/Calendar_2018_geopoint.csv", 
            "-o", f'{self.temp_dir}/Calendar_2018_geopoint.tsv',
            "--add-id",
            "--column-separator", ";",
        )

        df = pd.read_csv(f'{self.temp_dir}/Calendar_2018_geopoint.tsv', sep='\t')

        self.assertEqual(len(df.columns), 3)
        self.assertEqual(len(df), 23 * 5)

        labels = df['label'].unique()

        expected_labels = ['Bulan', 'Nama_Event', 'Nama_Sirkuit', 'Lat', 'Long']

        for expected_label in expected_labels:
            self.assertTrue(expected_label in labels)

