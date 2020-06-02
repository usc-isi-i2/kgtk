import unittest
from kgtk.cli_entry import cli_entry


class TestEmbedding(unittest.TestCase):

    def test_vector(self):
        # now just test if it is runnning properly or not
        test_input = 'data/embedding_test_input.tsv'
        assert cli_entry("kgtk", "text_embedding", test_input, "--use-cache", "false", "--embedding-projector-metadata-path", "none", "--property-value", "P1629", "P1466") == 0
