import json
import shutil
import unittest
import tempfile
import pandas as pd
from kgtk.cli_entry import cli_entry


class TestKGTKCat(unittest.TestCase):
    def setUp(self) -> None:
        self.file_path = 'data/sample_kgtk_edge_file.tsv'
        self.file_path_node = 'data/sample_kgtk_nodes.tsv'
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def test_kgtk_cat(self):
        cli_entry("kgtk", "cat", "-i", self.file_path, "-o", f'{self.temp_dir}/cat.tsv', "--verbose", "--show-option")

        df_r = pd.read_csv(f'{self.temp_dir}/cat.tsv', sep='\t')

        df = pd.read_csv(f'{self.file_path}', sep='\t')
        self.assertEqual(len(df), len(df_r))
        self.assertEqual(list(df.columns), list(df_r.columns))

        f = open(self.file_path)
        lines = f.readlines()
        f.close()
        for i, row in df_r.iterrows():
            self.assertEqual(row["id"], lines[i + 1].split('\t')[0])

    def test_kgtk_cat_output_csv(self):
        cli_entry("kgtk", "cat", "-i", self.file_path, "-o", f'{self.temp_dir}/cat.csv', "--output-format", "csv")

        df_r = pd.read_csv(f'{self.temp_dir}/cat.csv')

        df = pd.read_csv(f'{self.file_path}', sep='\t')
        self.assertEqual(len(df), len(df_r))
        self.assertEqual(list(df.columns), list(df_r.columns))

        f = open(self.file_path)
        lines = f.readlines()
        f.close()
        for i, row in df_r.iterrows():
            self.assertEqual(row["id"], lines[i + 1].split('\t')[0])

    def test_kgtk_cat_output_json_map(self):
        cli_entry("kgtk", "cat", "-i", self.file_path, "-o", f'{self.temp_dir}/cat.json', "--output-format", "json-map")

        f = open(f'{self.temp_dir}/cat.json')
        obj = json.load(f)
        f.close()
        self.assertEqual(len(obj), 287)
        for x in obj:
            self.assertTrue('id' in x)
            self.assertTrue('node1' in x)
            self.assertTrue('label' in x)
            self.assertTrue('node2' in x)
            self.assertTrue('rank' in x)

    def test_kgtk_cat_output_json_line(self):
        cli_entry("kgtk", "cat", "-i", self.file_path, "-o", f'{self.temp_dir}/cat.jl', "--output-format", "jsonl")

        f = open(f'{self.temp_dir}/cat.jl')
        lines = f.readlines()
        f.close()
        self.assertEqual(len(lines), 288)
        for line in lines:
            self.assertEqual(len(json.loads(line)), 5)

    def test_kgtk_cat_output_json_line_map(self):
        cli_entry("kgtk", "cat", "-i", self.file_path, "-o", f'{self.temp_dir}/cat.jl', "--output-format", "jsonl-map")

        f = open(f'{self.temp_dir}/cat.jl')
        lines = f.readlines()
        f.close()
        self.assertEqual(len(lines), 287)
        for line in lines:
            x = json.loads(line)
            self.assertTrue('id' in x)
            self.assertTrue('node1' in x)
            self.assertTrue('label' in x)
            self.assertTrue('node2' in x)
            self.assertTrue('rank' in x)

    def test_kgtk_cat_edge_node_file(self):
        rc = cli_entry("kgtk", "cat", "-i", self.file_path, self.file_path_node, "-o", f'{self.temp_dir}/cat.tsv')
        # non zero exit code
        self.assertEqual(rc, 1)

    def test_kgtk_cat_two_files(self):
        f1_path = 'data/sample_kgtk_edge_Q47158.tsv'
        f2_path = 'data/sample_kgtk_edge_file_with_id.tsv'
        cli_entry("kgtk", "cat", "-i", f1_path, f2_path, "-o", f'{self.temp_dir}/cat.tsv')
        df = pd.read_csv(f'{self.temp_dir}/cat.tsv', sep='\t')
        self.assertEqual(len(df), 6)
