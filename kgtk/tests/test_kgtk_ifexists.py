import shutil
import unittest
import tempfile
import pandas as pd
from kgtk.cli_entry import cli_entry


class TestKGTKFilter(unittest.TestCase):
    def setUp(self) -> None:
        self.file_path = 'data/sample_kgtk_edge_file.tsv'
        self.temp_dir = tempfile.mkdtemp()
        self.df = pd.read_csv(self.file_path, sep='\t')

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def test_kgtk_ifexists(self):
        Q47158_path = 'data/sample_kgtk_edge_Q47158.tsv'
        cli_entry("kgtk", "ifexists", "-i", self.file_path, "--filter-on", Q47158_path, "-o",
                  f'{self.temp_dir}/Q47158.tsv', "--input-keys", "node1", "--filter-keys", "node1", "--show-option",
                  "--verbose")

        df = pd.read_csv(f'{self.temp_dir}/Q47158.tsv', sep='\t')

        self.assertEqual(len(df), 118)

    def test_kgtk_ifexists_mode_none(self):
        Q47158_path = 'data/Q47158_non_edge.tsv'
        cli_entry("kgtk", "ifexists", "-i", self.file_path, "--filter-on", Q47158_path, "-o",
                  f'{self.temp_dir}/Q47158.tsv', "--input-keys", "node1", "--filter-keys", "heading", "--mode", "NONE",
                  "--verbose")

        df = pd.read_csv(f'{self.temp_dir}/Q47158.tsv', sep='\t')

        self.assertEqual(len(df), 118)

    def test_kgtk_ifexists_preserve_order(self):
        Q47158_path = 'data/Q47158_non_edge.tsv'
        cli_entry("kgtk", "ifexists", "-i", self.file_path, "--filter-on", Q47158_path, "-o",
                  f'{self.temp_dir}/Q47158.tsv', "--input-keys", "node1", "--filter-keys", "heading", "--mode", "NONE",
                  "--preserve-order", "--cache-input", "--verbose")

        f = open(f'{self.temp_dir}/Q47158.tsv')
        lines = f.readlines()
        # strip off the \n
        self.assertEqual(lines[1].strip(), "Q47158-P1014-1	Q47158	P1014	300391257	normal")
        self.assertEqual(lines[len(lines) - 1].replace('\n', ''),
                         "Q47158-wikipedia_sitelink-9	Q47158	wikipedia_sitelink	http://et.wikipedia.org/wiki/Triias	")
        f.close()

    def test_kgtk_ifexists_not_preserve_order(self):
        Q47158_path = 'data/Q47158_non_edge.tsv'
        cli_entry("kgtk", "ifexists", "-i", self.file_path, "--filter-on", Q47158_path, "-o",
                  f'{self.temp_dir}/Q47158.tsv', "--input-keys", "node1", "--filter-keys", "heading", "--mode", "NONE",
                  "--cache-input", "--verbose")

        f = open(f'{self.temp_dir}/Q47158.tsv')
        lines = f.readlines()
        # strip off the \n
        self.assertEqual(lines[1].strip(), "Q47158-P1014-1	Q47158	P1014	300391257	normal")
        self.assertEqual(lines[len(lines) - 1].replace('\n', ''),
                         "Q47158-wikipedia_sitelink-9	Q47158	wikipedia_sitelink	http://et.wikipedia.org/wiki/Triias	")
        f.close()

    def test_kgtk_ifnotexists(self):
        Q47158_path = 'data/Q47158_non_edge.tsv'
        cli_entry("kgtk", "ifnotexists", "-i", self.file_path, "--filter-on", Q47158_path, "-o",
                  f'{self.temp_dir}/Q47158.tsv', "--input-keys", "node1", "--filter-keys", "heading", "--mode", "NONE",
                  "--verbose")

        df = pd.read_csv(f'{self.temp_dir}/Q47158.tsv', sep='\t')

        self.assertEqual(len(df), 169)


    def test_kgtk_ifnotexists_preserve_order(self):
        Q47158_path = 'data/Q47158_non_edge.tsv'
        cli_entry("kgtk", "ifnotexists", "-i", self.file_path, "--filter-on", Q47158_path, "-o",
                  f'{self.temp_dir}/Q47158.tsv', "--input-keys", "node1", "--filter-keys", "heading", "--mode", "NONE",
                  "--preserve-order", "--cache-input", "--verbose")

        f = open(f'{self.temp_dir}/Q47158.tsv')
        lines = f.readlines()
        # strip off the \n
        self.assertEqual(lines[1].strip(), "Q1052204-P18-1	Q1052204	P18	Shengjianbao by buncheduptv in San Mateo, CA.jpg	normal")
        self.assertEqual(lines[len(lines) - 1].replace('\n', ''),
                         "Q65695069-label-1	Q65695069	label	Spring Break Forever\t")
        f.close()
