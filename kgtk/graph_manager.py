import csv


class GraphManager(object):
    def __init__(self, node_file_path, ontology_node_file_path,
                 edge_file_path, attribute_file_path):

        self.nodes = {}
        self.attributes = {}
        self.edges = {}
        self.reversed_edges = {}

        with open(node_file_path, 'r') as f:
            reader = csv.DictReader(f)
            for r in reader:
                self.nodes[r['identifier']] = {
                    'is_ontology': False,
                    'data_type': r['data_type'] or None,
                    'type': r['type']
                }

        with open(ontology_node_file_path, 'r') as f:
            reader = csv.DictReader(f)
            for r in reader:
                self.nodes[r['identifier']] = {
                    'is_ontology': False,
                    'data_type': r['data_type'] or None,
                    'type': r['type']
                }

        with open(edge_file_path, 'r') as f:
            reader = csv.DictReader(f)
            for r in reader:
                s, p, o = r['node'], r['property'], r['value']

                if s not in self.edges:
                    self.edges[s] = {}
                self.edges[s][p] = o
                if o not in self.reversed_edges:
                    self.reversed_edges[o] = {}
                self.reversed_edges[o][p] = s

        with open(attribute_file_path, 'r') as f:
            reader = csv.DictReader(f)
            for r in reader:
                s, p, o = r['node'], r['property'], r['value']
                if s not in self.attributes:
                    self.attributes[s] = {}
                self.attributes[s][p] = o

    def in_graph(self, id_):
        return id_ in self.nodes[id_]

    def get_node_type(self, id_):
        # event_class, entity_class, event, entity, property
        return self.nodes[id_]['type']

    def is_event_class(self, id_):
        try:
            if self.edges[id_]['rdfs:subClassOf'] == 'aida-item:Event':
                return True
        except:
            pass

        return False

    def is_entity_class(self, id_):
        try:
            if self.edges[id_]['rdfs:subClassOf'] == 'aida-item:Entity':
                return True
        except:
            pass

        return False

    def is_event(self, id_):
        try:
            class_ = self.edges[id_]['rdf:type']
            if self.edges[class_]['rdfs:subClassOf'] == 'aida-item:Event':
                return True
        except:
            pass

        return False

    def is_entity(self, id_):
        try:
            class_ = self.edges[id_]['rdf:type']
            if self.edges[class_]['rdfs:subClassOf'] == 'aida-item:Entity':
                return True
        except:
            pass

        return False

    def get_node_attributes(self, id_):
        return self.attributes[id_]

    def get_node_class(self, id_):
        return self.edges[id_].get('rdf:type')
