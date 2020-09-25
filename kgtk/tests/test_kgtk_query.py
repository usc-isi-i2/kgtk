import shutil
import unittest
import tempfile
import pandas as pd
from kgtk.cli_entry import cli_entry


class TestKGTKQuery(unittest.TestCase):
    def setUp(self) -> None:
        self.file_path = 'data/kypher/graph.tsv'
        self.temp_dir = tempfile.mkdtemp()
        self.df = pd.read_csv(self.file_path, sep='\t')

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def test_kgtk_query_default(self):
        cli_entry("kgtk", "query", "-i", self.file_path, "-o", f'{self.temp_dir}/out.tsv')
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')
        self.assertTrue(len(df) == 9)

    def test_kgtk_query_match(self):
        cli_entry("kgtk", "query", "-i", self.file_path, "-o", f'{self.temp_dir}/out.tsv', "--match",
                  "(i)-[:loves]->(c)")
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')
        self.assertTrue(len(df) == 3)
        ids = list(df['id'].unique())
        self.assertTrue('e11' in ids)
        self.assertTrue('e12' in ids)
        self.assertTrue('e14' in ids)

    def test_kgtk_query_limit(self):
        cli_entry("kgtk", "query", "-i", self.file_path, "-o", f'{self.temp_dir}/out.tsv', "--limit",
                  "3")
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')
        print(df)
        self.assertTrue(len(df) == 3)
        ids = list(df['id'].unique())
        self.assertTrue('e11' in ids)
        self.assertTrue('e12' in ids)
        self.assertTrue('e13' in ids)

    def test_kgtk_query_limit_skip(self):
        cli_entry("kgtk", "query", "-i", self.file_path, "-o", f'{self.temp_dir}/out.tsv', "--limit",
                  "3", "--skip", "2")
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')
        print(df)
        self.assertTrue(len(df) == 3)
        ids = list(df['id'].unique())
        self.assertTrue('e13' in ids)
        self.assertTrue('e14' in ids)
        self.assertTrue('e21' in ids)

    def test_kgtk_query_hans_filter(self):
        cli_entry("kgtk", "query", "-i", self.file_path, "-o", f'{self.temp_dir}/out.tsv', "--match",
                  "(:Hans)-[]->()")
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')
        print(df)
        self.assertTrue(len(df) == 2)
        ids = list(df['id'].unique())
        self.assertTrue('e11' in ids)
        self.assertTrue('e21' in ids)

    def test_kgtk_query_otto_name_filter(self):
        cli_entry("kgtk", "query", "-i", self.file_path, "-o", f'{self.temp_dir}/out.tsv', "--match",
                  "(:Otto)-[:name]->()")
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')
        print(df)
        self.assertTrue(len(df) == 1)
        ids = list(df['id'].unique())
        self.assertTrue('e22' in ids)

    def test_kgtk_query_where_double_letter(self):
        cli_entry("kgtk", "query", "-i", self.file_path, "-o", f'{self.temp_dir}/out.tsv', "--match",
                  "(p)-[:name]->(n)", "--where", 'n =~".*(.)\\\\1.*"')
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')
        self.assertTrue(len(df) == 2)
        ids = list(df['id'].unique())
        self.assertTrue('e22' in ids)
        self.assertTrue('e24' in ids)

    def test_kgtk_query_where_IN(self):
        cli_entry("kgtk", "query", "-i", self.file_path, "-o", f'{self.temp_dir}/out.tsv', "--match",
                  "(p)-[:name]->(n)", "--where", 'p IN ["Hans", "Susi"]')
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')
        print(df)
        self.assertTrue(len(df) == 2)
        ids = list(df['id'].unique())
        self.assertTrue('e21' in ids)
        self.assertTrue('e25' in ids)

    def test_kgtk_query_where_upper_substring(self):
        cli_entry("kgtk", "query", "-i", self.file_path, "-o", f'{self.temp_dir}/out.tsv', "--match",
                  "(p)-[:name]->(n)", "--where", "upper(substr(n,2,1)) >= 'J'")
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')
        print(df)
        self.assertTrue(len(df) == 4)
        ids = list(df['id'].unique())
        self.assertTrue('e22' in ids)
        self.assertTrue('e23' in ids)
        self.assertTrue('e24' in ids)
        self.assertTrue('e25' in ids)

    def test_kgtk_query_where_upper_substring_sorted(self):
        cli_entry("kgtk", "query", "-i", self.file_path, "-o", f'{self.temp_dir}/out.tsv', "--match",
                  "(p)-[:name]->(n)", "--where", "upper(substr(n,2,1)) >= 'J'", "--order-by", "substr(n,2,1)")
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')
        print(df)
        self.assertTrue(len(df) == 4)
        ids = list(df['id'].unique())
        self.assertTrue('e23' == ids[0])
        self.assertTrue('e24' == ids[1])
        self.assertTrue('e22' == ids[2])
        self.assertTrue('e25' == ids[3])

    def test_kgtk_query_where_upper_substring_sorted_desc(self):
        cli_entry("kgtk", "query", "-i", self.file_path, "-o", f'{self.temp_dir}/out.tsv', "--match",
                  "(p)-[:name]->(n)", "--where", "upper(substr(n,2,1)) >= 'J'", "--order-by", "substr(n,2,1) desc")
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')
        print(df)
        self.assertTrue(len(df) == 4)
        ids = list(df['id'].unique())
        self.assertTrue('e25' == ids[0])
        self.assertTrue('e22' == ids[1])
        self.assertTrue('e24' == ids[2])
        self.assertTrue('e23' == ids[3])

    def test_kgtk_query_select_columns(self):
        cli_entry("kgtk", "query", "-i", self.file_path, "-o", f'{self.temp_dir}/out.tsv', "--match",
                  "(p)-[:name]->(n)", "--where", "upper(substr(n,2,1)) >= 'J'", "--return", "p,n")
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')
        print(df)
        self.assertTrue(len(df) == 4)
        columns = list(df.columns)
        self.assertTrue('node1' in columns)
        self.assertTrue('node2' in columns)
        node1s = list(df['node1'].unique())
        self.assertTrue('Otto' in node1s)
        self.assertTrue('Joe' in node1s)
        self.assertTrue('Molly' in node1s)
        self.assertTrue('Susi' in node1s)

    def test_kgtk_query_switch_columns(self):
        cli_entry("kgtk", "query", "-i", self.file_path, "-o", f'{self.temp_dir}/out.tsv', "--match",
                  "(p)-[r:name]->(n)", "--where", "upper(substr(n,2,1)) >= 'J'", "--return", "p,n, r, r.label")
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')
        print(df)
        self.assertTrue(len(df) == 4)
        columns = list(df.columns)
        self.assertTrue('node1' in columns)
        self.assertTrue('node2' in columns)
        self.assertTrue('id' in columns)
        self.assertTrue('label' in columns)
        node1s = list(df['node1'].unique())
        self.assertTrue('Otto' in node1s)
        self.assertTrue('Joe' in node1s)
        self.assertTrue('Molly' in node1s)
        self.assertTrue('Susi' in node1s)

    def test_kgtk_query_return_columns_modify_functions(self):
        cli_entry("kgtk", "query", "-i", self.file_path, "-o", f'{self.temp_dir}/out.tsv', "--match",
                  "(p)-[r:name]->(n)", "--where", "upper(substr(n,2,1)) >= 'J'", "--return", "lower(p), r.label, n, r")
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')
        print(df)
        self.assertTrue(len(df) == 4)
        columns = list(df.columns)
        self.assertTrue('lower(graph_1_c1."node1")' in columns)
        self.assertTrue('node2' in columns)
        self.assertTrue('id' in columns)
        self.assertTrue('label' in columns)
        node1s = list(df['lower(graph_1_c1."node1")'].unique())
        self.assertTrue('otto' in node1s)
        self.assertTrue('joe' in node1s)
        self.assertTrue('molly' in node1s)
        self.assertTrue('susi' in node1s)

    def test_kgtk_query_kgtk_unstringify(self):
        cli_entry("kgtk", "query", "-i", self.file_path, "-o", f'{self.temp_dir}/out.tsv', "--match",
                  "(p)-[r:name]->(n)", "--where", "upper(substr(n,2,1)) >= 'J'", "--return",
                  "p, r.label, kgtk_unstringify(n), r")
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')
        print(df)
        self.assertTrue(len(df) == 4)
        columns = list(df.columns)
        self.assertTrue('kgtk_unstringify(graph_1_c1."node2")' in columns)
        self.assertTrue('node1' in columns)
        self.assertTrue('id' in columns)
        self.assertTrue('label' in columns)
        vals = list(df['kgtk_unstringify(graph_1_c1."node2")'].unique())
        self.assertTrue('Molly' in vals)

    def test_kgtk_query_para(self):
        cli_entry("kgtk", "query", "-i", self.file_path, "-o", f'{self.temp_dir}/out.tsv', "--match",
                  "(p)-[r:name]->(n)", "--where", " n = $name OR n = $name2 OR n = $name3 ",
                  "--para", "name=\"'Hans'@de\"", "--spara", "name2=Susi", "--lqpara", "name3=Otto@de")
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')
        print(df)
        self.assertTrue(len(df) == 2)
        columns = list(df.columns)
        self.assertTrue('node2' in columns)
        self.assertTrue('node1' in columns)
        self.assertTrue('id' in columns)
        self.assertTrue('label' in columns)
        ids = list(df['id'].unique())
        self.assertTrue('e25' in ids)
        self.assertTrue('e22' in ids)
