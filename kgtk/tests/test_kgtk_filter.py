import shutil
import unittest
import tempfile
import pandas as pd
from kgtk.cli_entry import cli_entry
from kgtk.cli.filter import run
from kgtk.exceptions import KGTKException
from pathlib import Path


class TestKGTKFilter(unittest.TestCase):
    def setUp(self) -> None:
        self.file_path = 'data/sample_kgtk_edge_file.tsv'
        self.file_path2 = 'data/sample_kgtk_non_edge_file.tsv'
        self.temp_dir = tempfile.mkdtemp()
        self.df = pd.read_csv(self.file_path, sep='\t')
        self.df2 = pd.read_csv(self.file_path2, sep='\t')

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def test_kgtk_filter_p31(self):
        # create GT from the file itself using pandas
        p31_qnodes = list(self.df.loc[self.df['label'] == 'P31']['node1'].unique())

        cli_entry("kgtk", "filter", "-i", self.file_path, "-o", f'{self.temp_dir}/p31.tsv', "-p", ";P31;", "-v",
                  "--reject-file", f'{self.temp_dir}/reject.tsv')

        df = pd.read_csv(f'{self.temp_dir}/p31.tsv', sep='\t')
        r_qnodes = list(df['node1'].unique())

        for q in r_qnodes:
            self.assertTrue(q in p31_qnodes)
        self.assertEqual(len(df), 10)

    def test_kgtk_filter_Q2447774(self):
        # create GT from the file itself using pandas
        node2s = list(self.df.loc[self.df['node1'] == 'Q2447774']['node2'])

        cli_entry("kgtk", "filter", "-i", self.file_path, "-o", f'{self.temp_dir}/Q2447774.tsv', "-p", "Q2447774;;",
                  "--reject-file", f'{self.temp_dir}/reject.tsv')

        df = pd.read_csv(f'{self.temp_dir}/Q2447774.tsv', sep='\t')
        r_node2s = list(df['node2'])

        for q in r_node2s:
            self.assertTrue(q in node2s)
        self.assertEqual(len(df), 27)

    def test_kgtk_filter_one_row(self):
        cli_entry("kgtk", "filter", "-i", self.file_path, "-o", f'{self.temp_dir}/one_row.tsv', "-p",
                  "Q65695069;P577;^2019-07-19T00:00:00Z/11", "-v",
                  "--reject-file", f'{self.temp_dir}/reject.tsv')

        df = pd.read_csv(f'{self.temp_dir}/one_row.tsv', sep='\t')

        self.assertEqual(len(df), 1)

    def test_kgtk_filter_single_pred_inverted(self):
        df = self.df2.loc[self.df2['pred'] != 'P577']
        cli_entry("kgtk", "filter", "-i", self.file_path2, "-o", f'{self.temp_dir}/P577.tsv', "-p",
                  ";P577;", "--subj", "sub", "--pred", "pred", "--obj", "obj", "-v", "--invert",
                  "--reject-file", f'{self.temp_dir}/reject.tsv')

        df_r = pd.read_csv(f'{self.temp_dir}/P577.tsv', sep='\t')

        self.assertEqual(len(df_r), len(df))

    def test_kgtk_filter_single_object(self):
        df = self.df2.loc[self.df2['obj'] == 'Q11365']
        cli_entry("kgtk", "filter", "-i", self.file_path2, "-o", f'{self.temp_dir}/Q11365.tsv', "-p",
                  ";;Q11365", "--subj", "sub", "--pred", "pred", "--obj", "obj", "-v",
                  "--reject-file", f'{self.temp_dir}/reject.tsv')

        df_r = pd.read_csv(f'{self.temp_dir}/Q11365.tsv', sep='\t')

        self.assertEqual(len(df_r), len(df))

    def test_kgtk_filter_single_object_inverted(self):
        df = self.df2.loc[self.df2['obj'] != 'Q11365']
        cli_entry("kgtk", "filter", "-i", self.file_path2, "-o", f'{self.temp_dir}/Q11365.tsv', "-p",
                  ";;Q11365", "--subj", "sub", "--pred", "pred", "--obj", "obj", "--invert",
                  "--reject-file", f'{self.temp_dir}/reject.tsv', "--show-option")

        df_r = pd.read_csv(f'{self.temp_dir}/Q11365.tsv', sep='\t')

        self.assertEqual(len(df_r), len(df))

    def test_kgtk_filter_reject_file(self):
        df = self.df2.loc[self.df2['obj'] == 'Q11365']
        cli_entry("kgtk", "filter", "-i", self.file_path2, "-o", f'{self.temp_dir}/Q11365.tsv', "-p",
                  ";;Q11365", "--subj", "sub", "--pred", "pred", "--obj", "obj", "-v", "--invert", "--reject-file",
                  f'{self.temp_dir}/reject.tsv')

        df_r = pd.read_csv(f'{self.temp_dir}/reject.tsv', sep='\t')

        self.assertEqual(len(df_r), len(df))

    def test_kgtk_filter_bad_pattern(self):
        with self.assertRaises(KGTKException):
            run(input_file=Path(self.file_path), output_files=[[Path(f'{self.temp_dir}/one_row.tsv')]],
                reject_file=None, patterns=[["Q65695069;P577;^2019-07-19T00:00:00Z/11;bla"]],
                subj_col=None, pred_col=None, obj_col=None, or_pattern=False,
                invert=False, match_type="match", first_match_only=False, regex=False, show_version=False)

    def test_kgtk_filter_column_indexes(self):
        run(input_file=Path(self.file_path2), output_files=[[Path(f'{self.temp_dir}/one_row.tsv')]],
            reject_file=None, patterns=[["Q;P;O"]],
            subj_col='1', pred_col='2', obj_col='3', or_pattern=False,
            invert=False, match_type="match", first_match_only=False, regex=False, show_version=False)
        df = pd.read_csv(f'{self.temp_dir}/one_row.tsv', sep='\t')
        self.assertEqual(len(df), 0)
        
