import unittest
import tempfile
import shutil
import pandas as pd
from kgtk.cli_entry import cli_entry
import os

class TestGraphEmbeddings(unittest.TestCase):
    def setUp(self):
        self.file_path = 'data/test_graphemb.tsv' # input file path
        self.temp_dir = tempfile.mkdtemp()

    def test_graph_embeddings_default(self):
        # only execute 1 epoch 
        cli_entry("kgtk", "graph-embeddings", "-i", self.file_path, "-o", f'{self.temp_dir}/out.tsv','-e','1')
        df = pd.read_csv(f'{self.temp_dir}/out.tsv')
        print(df.head(2))

    def test_graph_embeddings_format_w2v(self):
        cli_entry("kgtk", "graph-embeddings", "-i", self.file_path, "-o", f'{self.temp_dir}/out.tsv','-e','1',
        '-ot','w2v')    
        with open(f'{self.temp_dir}/out.tsv') as f :
            data = f.readlines()
        for index,entity_emb in enumerate(data):
            value = entity_emb.split(' ')
            if index == 0:
                self.assertTrue(len(value) == 2 )
            else:
                self.assertTrue(len(value) == 101)

    def test_graph_embeddings_format_glove(self):
        cli_entry("kgtk", "graph-embeddings", "-i", self.file_path, "-o", f'{self.temp_dir}/out.tsv','-e','1',
        '-ot','glove')    
        with open(f'{self.temp_dir}/out.tsv') as f :
            data = f.readlines()
        for entity_emb in data:
            value = entity_emb.split('\t')
            self.assertTrue(len(value) == 101)
            
    def test_graph_embeddings_format_kgtk(self):
        cli_entry("kgtk", "graph-embeddings", "-i", self.file_path, "-o", f'{self.temp_dir}/out.tsv','-e','1',
        '-ot','kgtk')    
        with open(f'{self.temp_dir}/out.tsv') as f :
            data = f.readlines()
        self.assertTrue(len(data) > 0)
        header = data.pop(0).rstrip('\r\n').split('\t')
        self.assertTrue(len(header) == 3)
        self.assertTrue(header[0] == 'node1')
        self.assertTrue(header[1] == 'label')
        self.assertTrue(header[2] == 'node2')
        for entity_emb in data:
            value = entity_emb.rstrip('\r\n').split('\t')
            self.assertTrue(len(value) == 3)
            self.assertTrue(value[1]=='graph_embeddings')

    def test_graph_embeddings_tmp(self):
        cli_entry("kgtk", "graph-embeddings", "-i", self.file_path, "-o", f'{self.temp_dir}/out.tsv',
        '-e','1','-T',f'{self.temp_dir}/outtmp/')  
        self.assertTrue(os.path.exists(f'{self.temp_dir}/outtmp/'))

    """
    def test_graph_embeddings_log(self):
        cli_entry("kgtk", "graph-embeddings", "-i", self.file_path, "-o", f'{self.temp_dir}/out.tsv',
        '-e','1','-l',f'{self.temp_dir}/log.log','-r', False)  
        self.assertTrue(os.path.exists(f'{self.temp_dir}/log.log'))
    """

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

 

if __name__ == '__main__':
    # do some testing
    suite = unittest.TestSuite()
    #  suite.addTest(ClassName(method))
    suite.addTest(TestGraphEmbeddings("test_graph_embeddings_default"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
