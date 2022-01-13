import unittest
import tempfile
import numpy as np
import shutil
from kgtk.cli_entry import cli_entry
import faiss


class TestBuildFaiss(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.emb_file = f'{self.temp_dir}/embeddings.tsv'
        self.idx_file_out = f'{self.temp_dir}/idx_file_out.tsv'
        self.id2n_file_out = f'{self.temp_dir}/id2n_file_out.tsv'
        self.dim = 32
        self.words = 100
        self.max_train_examples = 20
        self.idx_str = "HNSW32"  # or can try defaults, but then would be good to increase words to 100000
        self.metric_type_str = "L2"
        self.faiss_metric = faiss.METRIC_L2

    # helper function for creating temporary embedding file to test with
    def create_emb_file(self, format, words, dim, kgtk_header=True):
        with open(self.emb_file, 'w+') as f:
            if format == "w2v":
                f.write(f'{words}\t{dim}\n')
            if format in ["w2v", "glove"]:
                for i in range(words):
                    f.write("q{}\t{}\n".format(i, '\t'.join(str(v) for v in np.random.random(dim))))
            else:  # kgtk
                if kgtk_header:
                    f.write('node1\tlabel\tnode2\n')
                for i in range(words):
                    f.write(f"q{i}\tembedding\t{','.join(str(v) for v in np.random.random(dim))}\n")

    def test_build_faiss(self, fmt, no_input_header=False):
        self.create_emb_file(fmt, self.words, self.dim, kgtk_header=(not no_input_header))
        cli_entry("kgtk", "build_faiss", "-i", self.emb_file, "-o", self.idx_file_out, "-id2n", self.id2n_file_out,
                  "-ef", fmt, "--no_input_header", str(no_input_header), '-te', str(self.max_train_examples),
                  '-is', self.idx_str, '-m', self.metric_type_str)
        # validate idx2node output file
        with open(self.id2n_file_out, 'r') as f:
            data = f.read().splitlines()
            # one line for each word + a header
            self.assertTrue(len(data) == self.words + 1)
            for line in data[1:]:
                idx, _, word = line.split('\t')
                self.assertTrue(word == f'q{idx}')
        # validate index outut file
        index = faiss.read_index(self.idx_file_out)
        self.assertTrue(index.is_trained)
        self.assertTrue(index.ntotal == self.words)
        self.assertTrue(index.d == self.dim)
        self.assertTrue(index.metric_type == self.faiss_metric)

    def test_w2v_format(self):
        self.test_build_faiss("w2v")

    def test_glove_format(self):
        self.test_build_faiss("glove")

    def test_kgtk_format(self):
        self.test_build_faiss("kgtk")

    def test_kgtk_no_header_format(self):
        self.test_build_faiss("kgtk", no_input_header=True)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)
