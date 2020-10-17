import shutil
import unittest
import tempfile
import pandas as pd
from kgtk.cli_entry import cli_entry


class TestKGTKQuery(unittest.TestCase):
    def setUp(self) -> None:
        self.file_path = 'data/kypher/graph.tsv'
        self.file_path_gz = 'data/kypher/graph.tsv.gz'
        self.file_path_bz2 = 'data/kypher/graph.tsv.bz2'
        self.quals_path = 'data/kypher/quals.tsv'
        self.works_path = 'data/kypher/works.tsv'
        self.props_path = 'data/kypher/props.tsv'
        self.temp_dir = tempfile.mkdtemp()
        self.sqldb = f'{self.temp_dir}/test.sqlite3.db'
        self.df = pd.read_csv(self.file_path, sep='\t')

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def test_kgtk_query_default(self):
        cli_entry("kgtk", "query", "-i", self.file_path, "-o", f'{self.temp_dir}/out.tsv', '--graph-cache', self.sqldb)
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')
        self.assertTrue(len(df) == 9)

    def test_kgtk_query_default_gzip(self):
        cli_entry("kgtk", "query", "-i", self.file_path_gz, "-o", f'{self.temp_dir}/out.tsv.gz', '--graph-cache',
                  self.sqldb)
        df = pd.read_csv(f'{self.temp_dir}/out.tsv.gz', sep='\t')
        self.assertTrue(len(df) == 9)

    def test_kgtk_query_default_bz2(self):
        cli_entry("kgtk", "query", "-i", self.file_path_bz2, "-o", f'{self.temp_dir}/out.tsv.bz2', '--graph-cache',
                  self.sqldb)
        df = pd.read_csv(f'{self.temp_dir}/out.tsv.bz2', sep='\t')
        self.assertTrue(len(df) == 9)

    def test_kgtk_query_match(self):
        cli_entry("kgtk", "query", "-i", self.file_path, "-o", f'{self.temp_dir}/out.tsv', "--match",
                  "(i)-[:loves]->(c)", '--graph-cache', self.sqldb)
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')
        self.assertTrue(len(df) == 3)
        ids = list(df['id'].unique())
        self.assertTrue('e11' in ids)
        self.assertTrue('e12' in ids)
        self.assertTrue('e14' in ids)

    def test_kgtk_query_limit(self):
        cli_entry("kgtk", "query", "-i", self.file_path, "-o", f'{self.temp_dir}/out.tsv', "--limit",
                  "3", '--graph-cache', self.sqldb)
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')
        self.assertTrue(len(df) == 3)
        ids = list(df['id'].unique())
        self.assertTrue('e11' in ids)
        self.assertTrue('e12' in ids)
        self.assertTrue('e13' in ids)

    def test_kgtk_query_limit_skip(self):
        cli_entry("kgtk", "query", "-i", self.file_path, "-o", f'{self.temp_dir}/out.tsv', "--limit",
                  "3", "--skip", "2", '--graph-cache', self.sqldb)
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')
        self.assertTrue(len(df) == 3)
        ids = list(df['id'].unique())
        self.assertTrue('e13' in ids)
        self.assertTrue('e14' in ids)
        self.assertTrue('e21' in ids)

    def test_kgtk_query_hans_filter(self):
        cli_entry("kgtk", "query", "-i", self.file_path, "-o", f'{self.temp_dir}/out.tsv', "--match",
                  "(:Hans)-[]->()", '--graph-cache', self.sqldb)
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')
        self.assertTrue(len(df) == 2)
        ids = list(df['id'].unique())
        self.assertTrue('e11' in ids)
        self.assertTrue('e21' in ids)

    def test_kgtk_query_otto_name_filter(self):
        cli_entry("kgtk", "query", "-i", self.file_path, "-o", f'{self.temp_dir}/out.tsv', "--match",
                  "(:Otto)-[:name]->()", '--graph-cache', self.sqldb)
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')
        self.assertTrue(len(df) == 1)
        ids = list(df['id'].unique())
        self.assertTrue('e22' in ids)

    def test_kgtk_query_where_double_letter(self):
        cli_entry("kgtk", "query", "-i", self.file_path, "-o", f'{self.temp_dir}/out.tsv', "--match",
                  "(p)-[:name]->(n)", "--where", 'n =~".*(.)\\\\1.*"', '--graph-cache', self.sqldb)
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')
        self.assertTrue(len(df) == 2)
        ids = list(df['id'].unique())
        self.assertTrue('e22' in ids)
        self.assertTrue('e24' in ids)

    def test_kgtk_query_where_IN(self):
        cli_entry("kgtk", "query", "-i", self.file_path, "-o", f'{self.temp_dir}/out.tsv', "--match",
                  "(p)-[:name]->(n)", "--where", 'p IN ["Hans", "Susi"]', '--graph-cache', self.sqldb)
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')
        self.assertTrue(len(df) == 2)
        ids = list(df['id'].unique())
        self.assertTrue('e21' in ids)
        self.assertTrue('e25' in ids)

    def test_kgtk_query_where_upper_substring(self):
        cli_entry("kgtk", "query", "-i", self.file_path, "-o", f'{self.temp_dir}/out.tsv', "--match",
                  "(p)-[:name]->(n)", "--where", "upper(substr(n,2,1)) >= 'J'", '--graph-cache', self.sqldb)
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')
        self.assertTrue(len(df) == 4)
        ids = list(df['id'].unique())
        self.assertTrue('e22' in ids)
        self.assertTrue('e23' in ids)
        self.assertTrue('e24' in ids)
        self.assertTrue('e25' in ids)

    def test_kgtk_query_where_upper_substring_sorted(self):
        cli_entry("kgtk", "query", "-i", self.file_path, "-o", f'{self.temp_dir}/out.tsv', "--match",
                  "(p)-[:name]->(n)", "--where", "upper(substr(n,2,1)) >= 'J'", "--order-by", "substr(n,2,1)",
                  '--graph-cache', self.sqldb)
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')
        self.assertTrue(len(df) == 4)
        ids = list(df['id'].unique())
        self.assertTrue('e23' == ids[0])
        self.assertTrue('e24' == ids[1])
        self.assertTrue('e22' == ids[2])
        self.assertTrue('e25' == ids[3])

    def test_kgtk_query_where_upper_substring_sorted_desc(self):
        cli_entry("kgtk", "query", "-i", self.file_path, "-o", f'{self.temp_dir}/out.tsv', "--match",
                  "(p)-[:name]->(n)", "--where", "upper(substr(n,2,1)) >= 'J'", "--order-by", "substr(n,2,1) desc",
                  '--graph-cache', self.sqldb)
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')
        self.assertTrue(len(df) == 4)
        ids = list(df['id'].unique())
        self.assertTrue('e25' == ids[0])
        self.assertTrue('e22' == ids[1])
        self.assertTrue('e24' == ids[2])
        self.assertTrue('e23' == ids[3])

    def test_kgtk_query_select_columns(self):
        cli_entry("kgtk", "query", "-i", self.file_path, "-o", f'{self.temp_dir}/out.tsv', "--match",
                  "(p)-[:name]->(n)", "--where", "upper(substr(n,2,1)) >= 'J'", "--return", "p,n", '--graph-cache',
                  self.sqldb)
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
                  "(p)-[r:name]->(n)", "--where", "upper(substr(n,2,1)) >= 'J'", "--return", "p,n, r, r.label",
                  '--graph-cache', self.sqldb)
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
                  "(p)-[r:name]->(n)", "--where", "upper(substr(n,2,1)) >= 'J'",
                  "--return", "lower(p) as node1, r.label, n, r",
                  '--graph-cache', self.sqldb)
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')
        self.assertTrue(len(df) == 4)
        columns = list(df.columns)
        self.assertTrue('node1' in columns)
        self.assertTrue('node2' in columns)
        self.assertTrue('id' in columns)
        self.assertTrue('label' in columns)
        node1s = list(df['node1'].unique())
        self.assertTrue('otto' in node1s)
        self.assertTrue('joe' in node1s)
        self.assertTrue('molly' in node1s)
        self.assertTrue('susi' in node1s)

    def test_kgtk_query_kgtk_unstringify(self):
        cli_entry("kgtk", "query", "-i", self.file_path, "-o", f'{self.temp_dir}/out.tsv', "--match",
                  "(p)-[r:name]->(n)", "--where", "upper(substr(n,2,1)) >= 'J'",
                  "--return", "p, r.label, kgtk_unstringify(n) as node2, r",
                  '--graph-cache', self.sqldb)
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')
        self.assertTrue(len(df) == 4)
        columns = list(df.columns)
        self.assertTrue('node2' in columns)
        self.assertTrue('node1' in columns)
        self.assertTrue('id' in columns)
        self.assertTrue('label' in columns)
        vals = list(df['node2'].unique())
        self.assertTrue('Molly' in vals)

    def test_kgtk_query_para(self):
        cli_entry("kgtk", "query", "-i", self.file_path, "-o", f'{self.temp_dir}/out.tsv', "--match",
                  "(p)-[r:name]->(n)", "--where", " n = $name OR n = $name2 OR n = $name3 ",
                  "--para", "name=\"'Hans'@de\"", "--spara", "name2=Susi", "--lqpara", "name3=Otto@de", '--graph-cache',
                  self.sqldb)
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
                  "(p)-[r:name]->(n)", "--where", 'n.kgtk_lqstring_lang = "de"', '--graph-cache', self.sqldb)
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')
        self.assertTrue(len(df) == 2)
        ids = list(df['id'].unique())
        self.assertTrue('e21' in ids)
        self.assertTrue('e22' in ids)

    def test_kgtk_query_reflexive_edges(self):
        cli_entry("kgtk", "query", "-i", self.file_path, "-o", f'{self.temp_dir}/out.tsv', "--match",
                  "(a)-[]->(a)", '--graph-cache', self.sqldb)
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')
        self.assertTrue(len(df) == 1)
        ids = list(df['id'].unique())
        self.assertTrue('e14' in ids)

    def test_kgtk_query_multi_step_path(self):
        cli_entry("kgtk", "query", "-i", self.file_path, "-o", f'{self.temp_dir}/out.tsv', "--match",
                  "(na)<-[:name]-(a)-[r:loves]->(b)-[:name]->(nb)", "--return", "r, na, r.label, nb", '--graph-cache',
                  self.sqldb)
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
                  "--return", "r, na, r.label, nb", '--graph-cache', self.sqldb)
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
                  "g: (x)-[:loves]->(y), w: (y)-[:works]-(c)", '--graph-cache', self.sqldb)
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
                  "(x)-[:loves]->(y), w: (y)-[:works]-(c)", '--graph-cache', self.sqldb)
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
                  "--return", 'r, x, r.label, y as node2, c as `node2;work`', '--graph-cache', self.sqldb)
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')
        self.assertTrue(len(df) == 3)
        for i, row in df.iterrows():
            if row['id'] == 'e11':
                self.assertEqual(row['node1'], 'Hans')
                self.assertEqual(row['node2'], 'Molly')
                self.assertEqual(row['node2;work'], 'Renal')

    def test_kgtk_query_default_multi_graph_join_property_access_restriction_cast_integer(self):
        cli_entry("kgtk", "query", "-i", self.file_path,
                  "-i", self.works_path,
                  "-o", f'{self.temp_dir}/out.tsv', "--match",
                  "g: (x)-[r:loves]->(y), w: (y {salary: s})-[:works]-(c)",
                  "--where", "cast(s, integer) >= 10000",
                  "--return", 'r, x, r.label, y as node2, c as `node2;work`, s as `node2;salary`', '--graph-cache',
                  self.sqldb)
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')

        self.assertTrue(len(df) == 2)
        for i, row in df.iterrows():
            if row['id'] == 'e11':
                self.assertEqual(row['node1'], 'Hans')
                self.assertEqual(row['node2'], 'Molly')
                self.assertEqual(row['node2;work'], 'Renal')

    def test_kgtk_query_max(self):
        cli_entry("kgtk", "query", "-i", self.file_path,
                  "-o", f'{self.temp_dir}/out.tsv', "--match",
                  "g: (x)-[r]->(y)",
                  "--return", 'max(x) as node1, r.label, y, r', '--graph-cache', self.sqldb)
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')
        self.assertTrue(len(df) == 1)
        for i, row in df.iterrows():
            if row['id'] == 'e25':
                self.assertEqual(row['node1'], 'Susi')
                self.assertEqual(row['node2'], 'Susi')

    def test_kgtk_query_max_x_per_r(self):
        cli_entry("kgtk", "query", "-i", self.file_path,
                  "-o", f'{self.temp_dir}/out.tsv', "--match",
                  "g: (x)-[r]->(y)",
                  "--return", 'r, max(x), r.label, y',
                  "--limit", "5", '--graph-cache', self.sqldb)
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')

        self.assertTrue(len(df) == 5)
        ids = list(df['id'].unique())
        self.assertTrue('e11' in ids)
        self.assertTrue('e12' in ids)
        self.assertTrue('e13' in ids)
        self.assertTrue('e14' in ids)
        self.assertTrue('e21' in ids)

    def test_kgtk_query_count(self):
        cli_entry("kgtk", "query", "-i", self.file_path,
                  "-o", f'{self.temp_dir}/out.tsv', "--match",
                  "g: (x)-[r]->(y)",
                  "--where", 'x = "Joe"',
                  "--return", 'count(x) as N', '--graph-cache', self.sqldb)
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')

        self.assertTrue(len(df) == 1)
        for i, row in df.iterrows():
            self.assertEqual(row['N'], 3)

    def test_kgtk_query_count_distinct(self):
        cli_entry("kgtk", "query", "-i", self.file_path,
                  "-o", f'{self.temp_dir}/out.tsv', "--match",
                  "g: (x)-[r]->(y)",
                  "--where", 'x = "Joe"',
                  "--return", 'count(distinct x) as N', '--graph-cache', self.sqldb)
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')
        self.assertTrue(len(df) == 1)
        for i, row in df.iterrows():
            self.assertEqual(row['N'], 1)

    def test_kgtk_query_biggest_salary(self):
        cli_entry("kgtk", "query", "-i", self.works_path,
                  "-o", f'{self.temp_dir}/out.tsv', "--match",
                  "w: (y {salary: s})-[r:works]-(c)",
                  "--return", 'max(cast(s, int)) as `node1;salary`, y, "works" as label, c, r', '--graph-cache',
                  self.sqldb)
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')
        self.assertTrue(len(df) == 1)
        for i, row in df.iterrows():
            self.assertEqual(row['node1;salary'], 20000)
            self.assertEqual(row['node1'], 'Joe')
            self.assertEqual(row['node2'], 'Kaiser')

    def test_kgtk_query_date_filter(self):
        cli_entry("kgtk", "query", "-i", self.quals_path, "-o", f'{self.temp_dir}/out.tsv', "--match",
                  "(eid)-[q]->(time)", "--where", "time.kgtk_date_year < 2005", '--graph-cache', self.sqldb)
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')
        self.assertTrue(len(df) == 4)
        ids = list(df['id'].unique())
        self.assertTrue('m11' in ids)
        self.assertTrue('m12' in ids)
        self.assertTrue('m13' in ids)
        self.assertTrue('m14' in ids)

    def test_kgtk_query_three_graphs(self):
        cli_entry("kgtk", "query", "-i", self.works_path,
                  "-i", self.quals_path,
                  "-i", self.props_path,
                  "-o", f'{self.temp_dir}/out.tsv', "--match",
                  "work: (x)-[r {label: rl}]->(y), qual: (r)-[rp {label: p}]->(time), prop: (p)-[:member]->(:set1)",
                  "--where", 'time.kgtk_date_year <= 2000',
                  "--return", 'r as id, x, rl, y, p as trel, time as time', '--graph-cache', self.sqldb)
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')
        self.assertTrue(len(df) == 3)
        for i, row in df.iterrows():
            if row['id'] == 'w12':
                self.assertEqual(row['node1'], 'Otto')
                self.assertEqual(row['node2'], 'Kaiser')
                self.assertEqual(row['trel'], 'ends')
                self.assertEqual(row['time'], '^1987-11-08T04:56:34Z/10')

    def test_kgtk_query_property_enumeration_list(self):
        cli_entry("kgtk", "query", "-i", self.works_path,
                  "-i", self.quals_path,
                  "-o", f'{self.temp_dir}/out.tsv', "--match",
                  "work: (x)-[r {label: rl}]->(y), qual: (r)-[rp {label: p}]->(time)",
                  "--where", "p in ['starts', 'ends'] and time.kgtk_date_year <= 2000",
                  "--return", 'r as id, x, rl, y, p as trel, time as time', '--graph-cache', self.sqldb)
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')
        self.assertTrue(len(df) == 3)
        for i, row in df.iterrows():
            if row['id'] == 'w12':
                self.assertEqual(row['node1'], 'Otto')
                self.assertEqual(row['node2'], 'Kaiser')
                self.assertEqual(row['trel'], 'ends')
                self.assertEqual(row['time'], '^1987-11-08T04:56:34Z/10')

            if row['id'] == 'w11':
                self.assertEqual(row['node1'], 'Hans')
                self.assertEqual(row['node2'], 'ACME')
                self.assertEqual(row['trel'], 'starts')
                self.assertEqual(row['time'], '^1984-12-17T00:03:12Z/11')

    def test_kgtk_query_multi_graph_regex(self):
        cli_entry("kgtk", "query", "-i", self.works_path,
                  "-i", self.quals_path,
                  "-o", f'{self.temp_dir}/out.tsv', "--match",
                  "work: (x)-[r {label: rl}]->(y), qual: (r)-[rp {label: p}]->(time)",
                  "--where", "p =~ 's.*' and time.kgtk_date_year <= 2000",
                  "--return", 'r as id, x, rl, y, p as trel, time as time',
                  "--order-by", 'p desc, time asc', '--graph-cache', self.sqldb)
        df = pd.read_csv(f'{self.temp_dir}/out.tsv', sep='\t')
        self.assertTrue(len(df) == 2)
        for i, row in df.iterrows():
            if row['id'] == 'w13':
                self.assertEqual(row['node1'], 'Joe')
                self.assertEqual(row['node2'], 'Kaiser')
                self.assertEqual(row['trel'], 'starts')
                self.assertEqual(row['time'], '^1996-02-23T08:02:56Z/09')

            if row['id'] == 'w11':
                self.assertEqual(row['node1'], 'Hans')
                self.assertEqual(row['node2'], 'ACME')
                self.assertEqual(row['trel'], 'starts')
                self.assertEqual(row['time'], '^1984-12-17T00:03:12Z/11')
