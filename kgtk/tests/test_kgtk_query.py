import shutil
import unittest
import tempfile
import pandas as pd
from kgtk.cli_entry import cli_entry


class TestKGTKQuery(unittest.TestCase):
    def setUp(self) -> None:
        self.file_path = 'data/kypher/graph.tsv'
        self.quals_path = 'data/kypher/quals.tsv'
        self.works_path = 'data/kypher/works.tsv'
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
        self.assertTrue(len(df) == 3)
        ids = list(df['id'].unique())
        self.assertTrue('e11' in ids)
        self.assertTrue('e12' in ids)
        self.assertTrue('e13' in ids)

    def test_kgtk_query_limit_skip(self):
        cli_entry("kgtk", "query", "-i", self.file_path, "-o", f'{self.temp_dir}/out.tsv', "--limit",
                  "3", "--skip", "2")
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')
        self.assertTrue(len(df) == 3)
        ids = list(df['id'].unique())
        self.assertTrue('e13' in ids)
        self.assertTrue('e14' in ids)
        self.assertTrue('e21' in ids)

    def test_kgtk_query_hans_filter(self):
        cli_entry("kgtk", "query", "-i", self.file_path, "-o", f'{self.temp_dir}/out.tsv', "--match",
                  "(:Hans)-[]->()")
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')
        self.assertTrue(len(df) == 2)
        ids = list(df['id'].unique())
        self.assertTrue('e11' in ids)
        self.assertTrue('e21' in ids)

    def test_kgtk_query_otto_name_filter(self):
        cli_entry("kgtk", "query", "-i", self.file_path, "-o", f'{self.temp_dir}/out.tsv', "--match",
                  "(:Otto)-[:name]->()")
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')
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
        self.assertTrue(len(df) == 2)
        ids = list(df['id'].unique())
        self.assertTrue('e21' in ids)
        self.assertTrue('e25' in ids)

    def test_kgtk_query_where_upper_substring(self):
        cli_entry("kgtk", "query", "-i", self.file_path, "-o", f'{self.temp_dir}/out.tsv', "--match",
                  "(p)-[:name]->(n)", "--where", "upper(substr(n,2,1)) >= 'J'")
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')
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
        self.assertTrue(len(df) == 2)
        columns = list(df.columns)
        self.assertTrue('node2' in columns)
        self.assertTrue('node1' in columns)
        self.assertTrue('id' in columns)
        self.assertTrue('label' in columns)
        ids = list(df['id'].unique())
        self.assertTrue('e25' in ids)
        self.assertTrue('e22' in ids)

    def test_kgtk_query_lgstring_land(self):
        cli_entry("kgtk", "query", "-i", self.file_path, "-o", f'{self.temp_dir}/out.tsv', "--match",
                  "(p)-[r:name]->(n)", "--where", 'n.kgtk_lqstring_lang = "de"')
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')
        self.assertTrue(len(df) == 2)
        ids = list(df['id'].unique())
        self.assertTrue('e21' in ids)
        self.assertTrue('e22' in ids)

    def test_kgtk_query_reflexive_edges(self):
        cli_entry("kgtk", "query", "-i", self.file_path, "-o", f'{self.temp_dir}/out.tsv', "--match",
                  "(a)-[]->(a)")
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')
        self.assertTrue(len(df) == 1)
        ids = list(df['id'].unique())
        self.assertTrue('e14' in ids)

    def test_kgtk_query_multi_step_path(self):
        cli_entry("kgtk", "query", "-i", self.file_path, "-o", f'{self.temp_dir}/out.tsv', "--match",
                  "(na)<-[:name]-(a)-[r:loves]->(b)-[:name]->(nb)", "--return", "r, na, r.label, nb")
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')
        self.assertTrue(len(df) == 3)
        ids = list(df['id'].unique())
        node2s = list(df['node2'].unique())
        node2_1s = list(df['node2.1'].unique())
        self.assertTrue('e14' in ids)
        self.assertTrue('e11' in ids)
        self.assertTrue('e12' in ids)
        self.assertTrue('Joe' in node2s)
        self.assertTrue("'Hans'@de" in node2s)
        self.assertTrue("'Otto'@de" in node2s)
        self.assertTrue('Joe' in node2_1s)
        self.assertTrue('Molly' in node2_1s)
        self.assertTrue('Susi' in node2_1s)

    def test_kgtk_query_multi_step_path_german_lovers(self):
        cli_entry("kgtk", "query", "-i", self.file_path, "-o", f'{self.temp_dir}/out.tsv', "--match",
                  "(na)<-[:name]-(a)-[r:loves]->(b)-[:name]->(nb)",
                  "--where", 'na.kgtk_lqstring_lang = "de" OR nb.kgtk_lqstring_lang = "de"',
                  "--return", "r, na, r.label, nb")
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')
        self.assertTrue(len(df) == 2)
        ids = list(df['id'].unique())
        node2s = list(df['node2'].unique())
        node2_1s = list(df['node2.1'].unique())
        self.assertTrue('e11' in ids)
        self.assertTrue('e12' in ids)
        self.assertTrue("'Hans'@de" in node2s)
        self.assertTrue("'Otto'@de" in node2s)
        self.assertTrue('Molly' in node2_1s)
        self.assertTrue('Susi' in node2_1s)

    def test_kgtk_query__named_multi_graph_join(self):
        cli_entry("kgtk", "query", "-i", self.file_path,
                  "-i", self.works_path,
                  "-o", f'{self.temp_dir}/out.tsv', "--match",
                  "g: (x)-[:loves]->(y), w: (y)-[:works]-(c)")
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')
        self.assertTrue(len(df) == 3)
        for i, row in df.iterrows():
            if row['id'] == 'e14':
                self.assertEqual(row['node1'], 'Joe')
                self.assertEqual(row['node2'], 'Joe')
                self.assertEqual(row['id.1'], 'w13')
                self.assertEqual(row['node1.1'], 'Joe')
                self.assertEqual(row['label.1'], 'works')
                self.assertEqual(row['node2.1'], 'Kaiser')
                self.assertEqual(row['node1;salary'], 20000)
                self.assertEqual(row['graph'], 'employ')

    def test_kgtk_query_default_multi_graph_join(self):
        cli_entry("kgtk", "query", "-i", self.file_path,
                  "-i", self.works_path,
                  "-o", f'{self.temp_dir}/out.tsv', "--match",
                  "(x)-[:loves]->(y), w: (y)-[:works]-(c)")
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')
        self.assertTrue(len(df) == 3)
        for i, row in df.iterrows():
            if row['id'] == 'e14':
                self.assertEqual(row['node1'], 'Joe')
                self.assertEqual(row['node2'], 'Joe')
                self.assertEqual(row['id.1'], 'w13')
                self.assertEqual(row['node1.1'], 'Joe')
                self.assertEqual(row['label.1'], 'works')
                self.assertEqual(row['node2.1'], 'Kaiser')
                self.assertEqual(row['node1;salary'], 20000)
                self.assertEqual(row['graph'], 'employ')

    def test_kgtk_query_default_multi_graph_join_kgtk_compliant(self):
        cli_entry("kgtk", "query", "-i", self.file_path,
                  "-i", self.works_path,
                  "-o", f'{self.temp_dir}/out.tsv', "--match",
                  "g: (x)-[r:loves]->(y), w: (y)-[:works]-(c)",
                  "--return", 'r, x, r.label, y as node2, c as `node2;work`')
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')
        print(df)
        self.assertTrue(len(df) == 3)
        for i, row in df.iterrows():
            if row['id'] == 'e11':
                self.assertEqual(row['node1'], 'Hans')
                self.assertEqual(row['node2'], 'Molly')
                self.assertEqual(row['node2;work'], 'Renal')

    def test_kgtk_query_date_filter(self):
        cli_entry("kgtk", "query", "-i", self.quals_path, "-o", f'{self.temp_dir}/out.tsv', "--match",
                  "(eid)-[q]->(time)", "--where", "time.kgtk_date_year < 2005")
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')
        self.assertTrue(len(df) == 4)
        ids = list(df['id'].unique())
        self.assertTrue('m11' in ids)
        self.assertTrue('m12' in ids)
        self.assertTrue('m13' in ids)
        self.assertTrue('m14' in ids)
