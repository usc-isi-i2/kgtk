import shutil
import tempfile
import unittest
from pathlib import Path

from kgtk.cli_entry import cli_entry
from kgtk.utils.convert_embeddings_format import ConvertEmbeddingsFormat
from kgtk.exceptions import KGTKException


class TestConvertEmbeddingsFormat(unittest.TestCase):
    def setUp(self) -> None:
        self.edge_file = 'data/convert_embeddings_edge.tsv'
        self.node_file = 'data/convert_embeddings_node.tsv'
        self.ground_truth_w2v = 'data/convert_embeddings_edge_w2v.txt'
        self.ground_truth_gprojector = 'data/convert_embeddings_edge_gprojector.tsv'
        self.ground_truth_gprojector_metadata = 'data/convert_embeddings_edge_gprojector_metadata.tsv'
        self.ground_truth_gprojector_metadata_selective = 'data/convert_embeddings_gprojector_metadata_selective.tsv'
        self.ground_truth_gprojector_metadata_edge = 'data/convert_embeddings_edge_gprojector_edge_metadata.tsv'

        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def test_convert_to_w2v(self):
        output = f'{self.temp_dir}/w2v.txt'
        cli_entry("kgtk", "--debug",
                  "convert-embeddings-format",
                  "-i",
                  self.edge_file,
                  "--input-property", "graph_embeddings",
                  "-o", output)

        f1 = open(self.ground_truth_w2v)
        f1_lines = set(f1.readlines())
        f1.close()
        with open(output) as f2:
            for line in f2:
                self.assertTrue(line in f1_lines)

    def test_convert_to_gprojector(self):
        output = f'{self.temp_dir}/gprojector.tsv'
        metadata_output = f'{self.temp_dir}/gprojector_metadata.tsv'
        cli_entry("kgtk", "--debug",
                  "convert-embeddings-format",
                  "-i",
                  self.edge_file,
                  "--output-format", "gprojector",
                  "--node-file", self.node_file,
                  "--input-property", "graph_embeddings",
                  "--metadata-file", metadata_output,
                  "-o", output)

        f1 = open(self.ground_truth_gprojector)
        f1_lines = set(f1.readlines())
        f1.close()
        with open(output) as f2:
            for line in f2:
                self.assertTrue(line in f1_lines)

        f1_metadata = open(self.ground_truth_gprojector_metadata)
        f1_metadata_lines = f1_metadata.readlines()
        f1_metadata.close()
        with open(metadata_output) as f2:
            for line in f2:
                self.assertTrue(line in f1_metadata_lines)

    def test_convert_to_gprojector_selective_metadata(self):
        output = f'{self.temp_dir}/gprojector.tsv'
        metadata_output = f'{self.temp_dir}/gprojector_metadata_selective.tsv'
        cli_entry("kgtk", "--debug",
                  "convert-embeddings-format",
                  "-i",
                  self.edge_file,
                  "--output-format", "gprojector",
                  "--node-file", self.node_file,
                  "--metadata-columns", "label,type_label",
                  "--input-property", "graph_embeddings",
                  "--metadata-file", metadata_output,
                  "-o", output)

        f1 = open(self.ground_truth_gprojector)
        f1_lines = set(f1.readlines())
        f1.close()
        with open(output) as f2:
            for line in f2:
                self.assertTrue(line in f1_lines)

        f1_metadata = open(self.ground_truth_gprojector_metadata_selective)
        f1_metadata_lines = f1_metadata.readlines()
        f1_metadata.close()
        with open(metadata_output) as f2:
            for line in f2:
                self.assertTrue(line in f1_metadata_lines)

    def test_convert_to_gprojector_metadata_edge_file(self):
        output = f'{self.temp_dir}/gprojector.tsv'
        metadata_output = f'{self.temp_dir}/gprojector_metadata.tsv'
        cli_entry("kgtk", "--debug",
                  "convert-embeddings-format",
                  "-i",
                  self.edge_file,
                  "--output-format", "gprojector",
                  "--metadata-columns", "node1_label,type",
                  "--input-property", "graph_embeddings",
                  "--metadata-file", metadata_output,
                  "-o", output)

        f1 = open(self.ground_truth_gprojector)
        f1_lines = set(f1.readlines())
        f1.close()
        with open(output) as f2:
            for line in f2:
                self.assertTrue(line in f1_lines)

        f1_metadata = open(self.ground_truth_gprojector_metadata_edge)
        f1_metadata_lines = f1_metadata.readlines()
        f1_metadata.close()
        with open(metadata_output) as f2:
            for line in f2:
                self.assertTrue(line in f1_metadata_lines)

    def test_convert_to_gprojector_columns_not_in_node_file(self):
        output = f'{self.temp_dir}/gprojector.tsv'
        metadata_output = f'{self.temp_dir}/gprojector_metadata.tsv'

        cef: ConvertEmbeddingsFormat = ConvertEmbeddingsFormat(input_file=Path(self.edge_file),
                                                               output_file=Path(output),
                                                               node_file=Path(self.node_file),
                                                               output_format='gprojector',
                                                               input_property='graph_embeddings',
                                                               output_metadata_file=Path(metadata_output),
                                                               metadata_columns="blaaah"
                                                               )

        with self.assertRaises(KGTKException):
            cef.process()

    def test_convert_to_gprojector_columns_not_in_edge_file(self):
        output = f'{self.temp_dir}/gprojector.tsv'
        metadata_output = f'{self.temp_dir}/gprojector_metadata.tsv'

        cef: ConvertEmbeddingsFormat = ConvertEmbeddingsFormat(input_file=Path(self.edge_file),
                                                               output_file=Path(output),
                                                               output_format='gprojector',
                                                               input_property='graph_embeddings',
                                                               output_metadata_file=Path(metadata_output),
                                                               metadata_columns="blaaah"
                                                               )

        with self.assertRaises(KGTKException):
            cef.process()
