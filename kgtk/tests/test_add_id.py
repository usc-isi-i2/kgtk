import shutil
import unittest
import tempfile
import pandas as pd
from kgtk.cli_entry import cli_entry
from kgtk.exceptions import KGTKArgumentParseException


class TestKGTKAddID(unittest.TestCase):
    def setUp(self) -> None:
        self.file_path = 'data/sample_kgtk_edge_file_no_id.tsv'
        self.file_path2 = 'data/sample_kgtk_edge_file_with_id.tsv'
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def test_kgtk_add_id_default(self):
        cli_entry("kgtk", "add-id", "-i", self.file_path, "-o", f'{self.temp_dir}/id.tsv',
                  "--verify-id-unique", )
        df = pd.read_csv(f'{self.temp_dir}/id.tsv', sep='\t')
        for i, row in df.iterrows():
            self.assertEqual(row['id'], f'E{i + 1}')

    def test_kgtk_add_id_overwrite_existing_id(self):
        cli_entry("kgtk", "add-id", "-i", self.file_path2, "-o", f'{self.temp_dir}/id.tsv',
                  "--overwrite-id")
        df = pd.read_csv(f'{self.temp_dir}/id.tsv', sep='\t')
        for i, row in df.iterrows():
            self.assertEqual(row['id'], f'E{i + 1}')

    def test_kgtk_add_id_new_id_columns(self):
        cli_entry("kgtk", "add-id", "-i", self.file_path2, "-o", f'{self.temp_dir}/id.tsv',
                  "--new-id-column-name", "id_new")
        df = pd.read_csv(f'{self.temp_dir}/id.tsv', sep='\t')
        for i, row in df.iterrows():
            self.assertEqual(row['id_new'], f'E{i + 1}')

    def test_kgtk_add_id_new_id_column_specify_old_id_column(self):
        file_path = 'data/sample_kgtk_edge_file_with_id.tsv'
        cli_entry("kgtk", "add-id", "-i", file_path, "-o", f'{self.temp_dir}/id.tsv',
                  "--new-id-column-name", "id_new", "--old-id-column-name", "id")
        df = pd.read_csv(f'{self.temp_dir}/id.tsv', sep='\t')
        for i, row in df.iterrows():
            self.assertEqual(row['id_new'], f'E{i + 1}')

    def test_kgtk_add_id_overwrite_style_n1_l_n2(self):
        cli_entry("kgtk", "add-id", "-i", self.file_path2, "-o", f'{self.temp_dir}/id.tsv',
                  "--overwrite-id", "--id-style", "node1-label-node2")
        df = pd.read_csv(f'{self.temp_dir}/id.tsv', sep='\t')
        for i, row in df.iterrows():
            self.assertEqual(row['id'], f'{row["node1"]}-{row["label"]}-{row["node2"]}')

    def test_kgtk_add_id_overwrite_style_n1_l_num(self):
        cli_entry("kgtk", "add-id", "-i", self.file_path2, "-o", f'{self.temp_dir}/id.tsv',
                  "--overwrite-id", "--id-style", "node1-label-num")
        df = pd.read_csv(f'{self.temp_dir}/id.tsv', sep='\t')
        for i, row in df.iterrows():
            self.assertEqual(row['id'], f'{row["node1"]}-{row["label"]}-0000')

    def test_kgtk_add_id_overwrite_style_n1_l_n2_num(self):
        cli_entry("kgtk", "add-id", "-i", self.file_path2, "-o", f'{self.temp_dir}/id.tsv',
                  "--overwrite-id", "--id-style", "node1-label-node2-num")
        df = pd.read_csv(f'{self.temp_dir}/id.tsv', sep='\t')
        for i, row in df.iterrows():
            self.assertEqual(row['id'], f'{row["node1"]}-{row["label"]}-{row["node2"]}-0000')

    def test_kgtk_add_id_overwrite_style_n1_l_n2_id(self):
        cli_entry("kgtk", "add-id", "-i", self.file_path2, "-o", f'{self.temp_dir}/id.tsv',
                  "--overwrite-id", "--id-style", "node1-label-node2-id")
        df = pd.read_csv(f'{self.temp_dir}/id.tsv', sep='\t')
        for i, row in df.iterrows():
            self.assertEqual(row['id'], f'{row["node1"]}-{row["label"]}-{row["node2"]}-{i + 1}')

    def test_kgtk_add_id_overwrite_style_empty(self):
        cli_entry("kgtk", "add-id", "-i", self.file_path2, "-o", f'{self.temp_dir}/id.tsv',
                  "--overwrite-id", "--id-style", "empty")
        df = pd.read_csv(f'{self.temp_dir}/id.tsv', sep='\t').fillna("")
        for i, row in df.iterrows():
            self.assertEqual(row['id'], "")

    def test_kgtk_add_id_overwrite_style_prefix(self):
        cli_entry("kgtk", "add-id", "-i", self.file_path2, "-o", f'{self.temp_dir}/id.tsv',
                  "--overwrite-id", "--id-style", "prefix###", "--id-prefix", "THIS")
        df = pd.read_csv(f'{self.temp_dir}/id.tsv', sep='\t').fillna("")
        for i, row in df.iterrows():
            self.assertEqual(row['id'], f'THIS{i + 1}')
