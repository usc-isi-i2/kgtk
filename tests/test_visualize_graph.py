import shutil
import tempfile
import unittest
from kgtk.cli_entry import cli_entry


class TestVisualizeGraph(unittest.TestCase):
    def setUp(self) -> None:
        self.example_file = 'data/visualize_force_graph_example2.tsv'
        self.node_file = 'data/visualize_force_graph_example2_node.tsv'
        self.node_file_blank_labels = 'data/visualize_graph_node_example_blank_labels.tsv'
        self.ground_truth_default = 'data/visualize_graph_example_1_no_node_default.html'
        self.ground_truth_color_node = 'data/visualize_graph_example_color_by_node_column.html'
        self.ground_truth_color_node_log = 'data/visualize_graph_example_color_by_node_column_log.html'
        self.ground_truth_color_node_missing = 'data/visualize_graph_example_color_by_node_column_log_missing.html'
        self.ground_truth_color_node_hex = 'data/visualize_graph_example_color_by_node_column_hex.html'
        self.ground_truth_color_edge = 'data/visualize_graph_example_color_edge.html'
        self.ground_truth_color_edge_numbers = 'data/visualize_graph_example_color_edge_numbers.html'
        self.ground_truth_color_edge_strings = 'data/visualize_graph_example_color_edge_strings.html'
        self.ground_truth_node_size = 'data/visualize_graph_example_node_size.html'
        self.ground_truth_edge_width = 'data/visualize_graph_example_edge_width.html'
        self.ground_truth_node_text = 'data/visualize_graph_example_node_text.html'
        self.ground_truth_node_text_number_colors = 'data/visualize_graph_example_node_text_number_colors.html'
        self.ground_truth_edge_text = 'data/visualize_graph_example_edge_text.html'
        self.ground_truth_node_edge_text = 'data/visualize_graph_example_node_edge_text.html'
        self.ground_truth_node_text_blank_labels = 'data/visualize_graph_example_node_text_blank_labels.html'
        self.ground_truth_color_node_custom_interpolator = 'data/visualize_graph_example_color_by_node_column_interpolator.html'
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def test_default_no_node_file(self):
        output = f'{self.temp_dir}/test_1.html'
        cli_entry("kgtk", "--debug", "visualize-graph", "-i", self.example_file, "-o", output)

        f = open(self.ground_truth_default)
        f1 = set(f.readlines())
        f.close()
        with open(output) as f2:
            for line in f2:
                self.assertTrue(line in f1)

    def test_color_by_node_column(self):
        output = f'{self.temp_dir}/test_2.html'
        cli_entry("kgtk", "--debug", "visualize-graph",
                  "-i", self.example_file,
                  "-o", f'{output}',
                  "--node-color-column", "is_country",
                  "--node-color-style", "d3.schemeCategory10",
                  "--node-color-numbers", "as-is",
                  "--node-file", f'{self.node_file}'
                  )
        f = open(self.ground_truth_color_node)
        f1 = set(f.readlines())
        f.close()
        with open(output) as f2:
            for line in f2:
                self.assertTrue(line in f1)

    def test_color_by_node_column_log(self):
        output = f'{self.temp_dir}/test_3.html'
        cli_entry("kgtk", "--debug",
                  "visualize-graph",
                  "-i", self.example_file,
                  "-o", f'{output}',
                  "--node-color-column", "degree",
                  "--node-color-style", "d3.schemePastel1",
                  "--node-color-numbers", "log",
                  "--node-file", f'{self.node_file}'
                  )

        f = open(self.ground_truth_color_node_log)
        f1 = set(f.readlines())
        f.close()
        with open(output) as f2:
            for line in f2:
                self.assertTrue(line in f1)

    def test_color_by_node_column_missing(self):
        output = f'{self.temp_dir}/test_4.html'
        cli_entry("kgtk", "--debug",
                  "visualize-graph",
                  "-i", self.example_file,
                  "-o", f'{output}',
                  "--node-color-column", "type_missing",
                  "--node-color-style", "d3.schemeSet3",
                  "--node-file", f'{self.node_file}'
                  )

        f = open(self.ground_truth_color_node_missing)
        f1 = set(f.readlines())
        f.close()
        with open(output) as f2:
            for line in f2:
                self.assertTrue(line in f1)

    def test_color_by_node_column_hex(self):
        output = f'{self.temp_dir}/test_5.html'
        cli_entry("kgtk", "--debug",
                  "visualize-graph",
                  "-i", self.example_file,
                  "-o", f'{output}',
                  "--node-color-column", "hex_color",
                  "--node-color-hex",
                  "--node-file", f'{self.node_file}'
                  )

        f = open(self.ground_truth_color_node_hex)
        f1 = set(f.readlines())
        f.close()
        with open(output) as f2:
            for line in f2:
                self.assertTrue(line in f1)

    def test_color_by_edge_column(self):
        output = f'{self.temp_dir}/test_6.html'
        cli_entry("kgtk", "--debug",
                  "visualize-graph",
                  "-i", self.example_file,
                  "-o", f'{output}',
                  "--edge-color-column", "hex_color",
                  "--edge-color-hex"
                  )

        f = open(self.ground_truth_color_edge)
        f1 = set(f.readlines())
        f.close()
        with open(output) as f2:
            for line in f2:
                self.assertTrue(line in f1)

    def test_node_size(self):
        output = f'{self.temp_dir}/test_7.html'
        cli_entry("kgtk", "--debug",
                  "visualize-graph",
                  "-i", self.example_file,
                  "--node-file", f'{self.node_file}',
                  "-o", f'{output}',
                  "--node-size-column", "population",
                  "--node-size-minimum", "2.0",
                  "--node-size-maximum", "6.0",
                  "--node-size-default", "4.0",
                  "--node-color-column", "hex_color",
                  "--node-color-hex",
                  "--node-size-scale", "log"
                  )
        f = open(self.ground_truth_node_size)
        f1 = set(f.readlines())
        f.close()
        with open(output) as f2:
            for line in f2:
                self.assertTrue(line in f1)

    def test_edge_width(self):
        output = f'{self.temp_dir}/test_8.html'
        cli_entry("kgtk", "--debug",
                  "visualize-graph",
                  "-i", self.example_file,
                  "--node-file", f'{self.node_file}',
                  "-o", f'{output}',
                  "--edge-width-column", "weight",
                  "--edge-width-minimum", "2.0",
                  "--edge-width-maximum", "5.0",
                  "--edge-width-default", "2.0",
                  "--edge-width-scale", "log",
                  "--node-color-column", "degree",
                  "--node-color-style", "d3.schemeDark2",
                  "--node-color-numbers", "linear"
                  )

        f = open(self.ground_truth_edge_width)
        f1 = set(f.readlines())
        f.close()
        with open(output) as f2:
            for line in f2:
                self.assertTrue(line in f1)

    def test_node_text(self):
        output = f'{self.temp_dir}/test_9.html'
        cli_entry("kgtk", "--debug",
                  "visualize-graph",
                  "-i", self.example_file,
                  "--node-file", f'{self.node_file}',
                  "-o", f'{output}',
                  "--node-color-column", "hex_color",
                  "--node-color-hex",
                  "--show-text", "above"
                  )

        f = open(self.ground_truth_node_text)
        f1 = set(f.readlines())
        f.close()
        with open(output) as f2:
            for line in f2:
                self.assertTrue(line in f1)

    def test_edge_text(self):
        output = f'{self.temp_dir}/test_10.html'
        cli_entry("kgtk", "--debug",
                  "visualize-graph",
                  "-i", self.example_file,
                  "-o", f'{output}',
                  "--show-edge-label",
                  "--edge-color-column", "hex_color",
                  "--edge-color-hex"
                  )

        f = open(self.ground_truth_edge_text)
        f1 = set(f.readlines())
        f.close()
        with open(output) as f2:
            for line in f2:
                self.assertTrue(line in f1)

    def test_node_edge_text(self):
        output = f'{self.temp_dir}/test_11.html'
        cli_entry("kgtk", "--debug",
                  "visualize-graph",
                  "-i", self.example_file,
                  "--node-file", f'{self.node_file}',
                  "-o", f'{output}',
                  "--node-color-column", "hex_color",
                  "--node-color-hex",
                  "--show-text", "above",
                  "--show-edge-label",
                  "--edge-color-hex",
                  "--edge-color-column", "hex_color"
                  )

        f = open(self.ground_truth_node_edge_text)
        f1 = set(f.readlines())
        f.close()
        with open(output) as f2:
            for line in f2:
                self.assertTrue(line in f1)

    def test_node_text_blank_labels(self):
        output = f'{self.temp_dir}/test_12.html'
        cli_entry("kgtk", "--debug",
                  "visualize-graph",
                  "-i", self.example_file,
                  "--node-file", f'{self.node_file_blank_labels}',
                  "-o", f'{output}',
                  "--node-color-column", "hex_color",
                  "--node-color-hex",
                  "--show-text", "above",
                  "--show-blank-labels"
                  )

        f = open(self.ground_truth_node_text_blank_labels)
        f1 = set(f.readlines())
        f.close()
        with open(output) as f2:
            for line in f2:
                self.assertTrue(line in f1)

    def test_color_by_node_column_custom_interpolator(self):
        output = f'{self.temp_dir}/test_13.html'
        cli_entry("kgtk", "--debug",
                  "visualize-graph",
                  "-i", self.example_file,
                  "-o", f'{output}',
                  "--node-color-column", "ordinal",
                  "--node-color-numbers", "as-is",
                  "--node-file", f'{self.node_file}',
                  "--node-color-style", "d3.interpolateGreens"
                  )

        f = open(self.ground_truth_color_node_custom_interpolator)
        f1 = set(f.readlines())
        f.close()
        with open(output) as f2:
            for line in f2:
                self.assertTrue(line in f1)

    def test_node_text_numbers_colors(self):
        output = f'{self.temp_dir}/test_14.html'
        cli_entry("kgtk", "--debug",
                  "visualize-graph",
                  "-i", self.example_file,
                  "--node-file", f'{self.node_file}',
                  "-o", f'{output}',
                  "--node-color-column", "ordinal",
                  "--node-color-numbers", "as-is",
                  "--node-color-style", "d3.interpolateGreens",
                  "--show-text", "above"
                  )

        f = open(self.ground_truth_node_text_number_colors)
        f1 = set(f.readlines())
        f.close()
        with open(output) as f2:
            for line in f2:
                self.assertTrue(line in f1)

    def test_color_by_edge_column_color_numbers(self):
        output = f'{self.temp_dir}/test_15.html'
        cli_entry("kgtk", "--debug",
                  "visualize-graph",
                  "-i", self.example_file,
                  "-o", f'{output}',
                  "--edge-color-column", "ordinal",
                  "--edge-color-numbers", "as-is",
                  "--edge-color-style", "d3.interpolateReds"
                  )

        f = open(self.ground_truth_color_edge_numbers)
        f1 = set(f.readlines())
        f.close()
        with open(output) as f2:
            for line in f2:
                self.assertTrue(line in f1)

    def test_color_by_edge_column_color_strings(self):
        output = f'{self.temp_dir}/test_16.html'
        cli_entry("kgtk", "--debug",
                  "visualize-graph",
                  "-i", self.example_file,
                  "-o", f'{output}',
                  "--edge-color-column", "label",
                  "--edge-color-style", "d3.schemeDark2"
                  )

        f = open(self.ground_truth_color_edge_strings)
        f1 = set(f.readlines())
        f.close()
        with open(output) as f2:
            for line in f2:
                self.assertTrue(line in f1)


if __name__ == '__main__':
    unittest.main()
