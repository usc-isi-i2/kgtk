import shutil
import unittest
import tempfile
import pandas as pd
from kgtk.cli_entry import cli_entry, cli_entry_sequential_commands
from kgtk.cli.filter import run
from kgtk.exceptions import KGTKException
from pathlib import Path


class TestKGTKGraphStatistics(unittest.TestCase):
    def setUp(self) -> None:
        self.file_path = 'data/graph_statistics_zacharys_karate_club.tsv'
        self.undirected_betweenness_path = 'data/graph_statistics_undirected_betweenness_zacharys_karate_club.tsv'
        self.directed_betweenness_path = 'data/graph_statistics_directed_betweenness_zacharys_karate_club.tsv'
        self.undirected_pagerank_path = 'data/graph_statistics_undirected_pagerank_zacharys_karate_club.tsv'
        self.directed_pagerank_path = 'data/graph_statistics_directed_pagerank_zacharys_karate_club.tsv'

        self.temp_dir = Path(tempfile.mkdtemp())

        self.undirected_output_path = self.temp_dir / 'graph_statistics_undirected.tsv'
        self.directed_output_path = self.temp_dir / 'graph_statistics_directed.tsv'

        cli_entry(
            'kgtk', 'graph-statistics', '-i', f'{self.file_path}', '-o', f'{self.undirected_output_path}',
            '--undirected', 'True', '--compute-betweenness')

        cli_entry(
            'kgtk', 'graph-statistics', '-i', f'{self.file_path}', '-o', f'{self.directed_output_path}',
            '--compute-betweenness')

        # Code used to generate test result for comparison
        # self.temp_dir = Path('data')
        # self.undirected_output_path = self.temp_dir / 'graph_statistics_undirected.tsv'
        # self.directed_output_path = self.temp_dir / 'graph_statistics_directed.tsv'
        # cli_entry(
        #     'kgtk', 'graph-statistics', '-i', f'{self.file_path}', '-o', f'{self.undirected_output_path}',
        #     '--undirected', 'True', '--compute-betweenness')
        # cli_entry(
        #     'kgtk', 'graph-statistics', '-i', f'{self.file_path}', '-o', f'{self.directed_output_path}',
        #     '--compute-betweenness')
        # cli_entry(
        #     'kgtk', 'filter', '-i', f'{self.undirected_output_path}', '-p', ';vertex_pagerank;',
        #     '/', 'calc', '--do', 'average', '--columns', 'node2', '--into', 'node2', '--format', '%.4f',
        #     '/', 'sort', '-c', 'node2', '', '-r',
        #     '/', 'remove-columns', '-c', 'id', '-o', f'{self.undirected_pagerank_path}')
        # cli_entry(
        #     'kgtk', 'filter', '-i', f'{self.undirected_output_path}', '-p', ';vertex_betweenness;',
        #     '/', 'calc', '--do', 'average', '--columns', 'node2', '--into', 'node2', '--format', '%.4f',
        #     '/', 'sort', '-c', 'node2', '', '-r',
        #     '/', 'remove-columns', '-c', 'id', '-o', f'{self.undirected_betweenness_path}')
        # cli_entry(
        #     'kgtk', 'filter', '-i', f'{self.directed_output_path}', '-p', ';vertex_pagerank;',
        #     '/', 'calc', '--do', 'average', '--columns', 'node2', '--into', 'node2', '--format', '%.4f',
        #     '/', 'sort', '-c', 'node2', '', '-r',
        #     '/', 'remove-columns', '-c', 'id', '-o', f'{self.directed_pagerank_path}')
        # cli_entry(
        #     'kgtk', 'filter', '-i', f'{self.directed_output_path}', '-p', ';vertex_betweenness;',
        #     '/', 'calc', '--do', 'average', '--columns', 'node2', '--into', 'node2', '--format', '%.4f',
        #     '/', 'sort', '-c', 'node2', '', '-r',
        #     '/', 'remove-columns', '-c', 'id', '-o', f'{self.directed_betweenness_path}')


    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def test_undirected_betweenness(self):
        result_path = self.temp_dir / 'test_undirected_betweenness.tsv'
        cli_entry(
            'kgtk', 'filter', '-i', f'{self.undirected_output_path}', '-p', ';vertex_betweenness;',
            '/', 'calc', '--do', 'average', '--columns', 'node2', '--into', 'node2', '--format', '%.4f',
            '/', 'sort', '-c', 'node2', '', '-r',
            '/', 'remove-columns', '-c', 'id', '-o', f'{result_path}')

        f1 = open(self.undirected_betweenness_path)
        f2 = open(result_path)

        self.assertEqual(f1.readlines(), f2.readlines())
        f1.close()
        f2.close()

    def test_undirected_pagerank(self):
        result_path = self.temp_dir / 'test_undirected_pagerank.tsv'
        cli_entry(
            'kgtk', 'filter', '-i', f'{self.undirected_output_path}', '-p', ';vertex_pagerank;',
            '/', 'calc', '--do', 'average', '--columns', 'node2', '--into', 'node2', '--format', '%.4f',
            '/', 'sort', '-c', 'node2', '', '-r',
            '/', 'remove-columns', '-c', 'id', '-o', f'{result_path}')

        f1 = open(self.undirected_pagerank_path)
        f2 = open(result_path)

        self.assertEqual(f1.readlines(), f2.readlines())
        f1.close()
        f2.close()

    def test_directed_betweenness(self):
        result_path = self.temp_dir / 'test_directed_betweenness.tsv'
        cli_entry(
            'kgtk', 'filter', '-i', f'{self.directed_output_path}', '-p', ';vertex_betweenness;',
            '/', 'calc', '--do', 'average', '--columns', 'node2', '--into', 'node2', '--format', '%.4f',
            '/', 'sort', '-c', 'node2', '', '-r',
            '/', 'remove-columns', '-c', 'id', '-o', f'{result_path}')

        f1 = open(self.directed_betweenness_path)
        f2 = open(result_path)

        self.assertEqual(f1.readlines(), f2.readlines())
        f1.close()
        f2.close()

    def test_directed_pagerank(self):
        result_path = self.temp_dir / 'test_directed_pagerank.tsv'
        cli_entry(
            'kgtk', 'filter', '-i', f'{self.directed_output_path}', '-p', ';vertex_pagerank;',
            '/', 'calc', '--do', 'average', '--columns', 'node2', '--into', 'node2', '--format', '%.4f',
            '/', 'sort', '-c', 'node2', '', '-r',
            '/', 'remove-columns', '-c', 'id', '-o', f'{result_path}')

        f1 = open(self.directed_pagerank_path)
        f2 = open(result_path)

        self.assertEqual(f1.readlines(), f2.readlines())
        f1.close()
        f2.close()
