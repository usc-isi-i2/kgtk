from kgtk import GraphManager, NodeMatcher

gm = GraphManager(
    '../data/maa_m18_node_table_file1.csv',
    '../data/maa_m18_ontology_node_table_file1.csv',
    '../data/maa_m18_edge_table_file1.csv',
    '../data/maa_m18_attribute_table_file1.csv')

nm = NodeMatcher(gm)
print(nm.similarity(
    'aida-entity:4fba8ada-3361-459c-a37f-a0ccc4624ac5',
    'aida-entity:b993cba5-67e3-4e8e-b843-0f8103af98a0'))

