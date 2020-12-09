import unittest
from kgtk.cli_entry import cli_entry

# class TestEmbedding(unittest.TestCase):
#
#     def test_vector(self):
#         # now just test if it is runnning properly or not
#         # test_input = 'data/embedding_test_input.tsv'
#         # assert cli_entry("kgtk", "text_embedding", test_input, "--use-cache", "false",
#         #                  "--embedding-projector-metadata-path", "none", "--property-value", "P1629", "P1466") == 0
# v_path = '/Users/amandeep/Github/maa-analysis/MAA_Datasets/v3.2.0'
# cli_entry("kgtk", "text-embedding", f'{v_path}/10000.tsv',
#           "--model", "roberta-large-nli-mean-tokens",
#           "--property-labels-file", f'{v_path}/qnodes-properties-labels-for-V3.2.0_KB.tsv',
#           "--debug",
#           "--property-value-file", f'{v_path}/non-identifier-properties-for-V3.2.0.tsv',
#           "--save-embedding-sentence", "-o", f'{v_path}/text_embeddings_10000.tsv')
