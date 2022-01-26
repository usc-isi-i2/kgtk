from kgtk.knowledge_graph.graph import Graph
from kgtk.knowledge_graph.namespacemanager import RDF, OWL


class Ontology(Graph):
    def is_valid(self, s_types, p, o_types):
        return True

    @property
    def object_properties(self):
        """
        Return all the defined ObjectProperty
        :return: Set[URIRef]
        """
        properties = []
        for property_ in self._g.subjects(RDF.type, OWL.ObjectProperty):
            properties.append(property_)
        return set(properties)

    @property
    def datatype_properties(self):
        """
        Return all the defined DatatypeProperty
        :return: Set[URIRef]
        """
        properties = []
        for property_ in self._g.subjects(RDF.type, OWL.DatatypeProperty):
            properties.append(property_)
        return set(properties)
