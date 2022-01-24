from kgtk.knowledge_graph.node import URI
from kgtk.knowledge_graph.subject import Subject
from enum import Enum
import uuid


class Rank(Enum):
    Normal = URI('wikibase:NormalRank')
    Preferred = URI('wikibase:PreferredRank')
    Deprecated = URI('wikibase:DeprecatedRank')

    # never set the rank to BestRank. This is only for truthy statements.
    # Use this only if you are sure of what you are doing
    BestRank = URI('wikibase:BestRank')


class BaseStatement(Subject):
    def __init__(self, uri):
        super().__init__(uri)

    def _add_value_node(self, prefix, p, v):
        self.add_property(URI(prefix + ':' + p), v.value)
        if v.full_value:
            self.add_property(URI(prefix + 'v:' + p), v.full_value)
        if v.normalized_value:
            self.add_property(URI(prefix + 'n:' + p), v.normalized_value)


class Statement(BaseStatement):
    def __init__(self, node_id, rank, statement_id=None):
        statement_id = statement_id or str(uuid.uuid4())
        super().__init__(URI('wds:' + node_id + '-' + statement_id))
        self.add_property(URI('rdf:type'), URI('wikibase:Statement'))
        self.add_property(URI('wikibase:rank'), rank.value)

    def add_value(self, p, v):
        self._add_value_node('ps', p, v)

    def add_qualifier(self, p, v):
        self._add_value_node('pq', p, v)

    def add_reference(self, ref):
        self.add_property(URI('prov:wasDerivedFrom'), ref)


class WDReference(BaseStatement):
    def __init__(self, reference_id=None):
        reference_id = reference_id or str(uuid.uuid4())
        super().__init__(URI('wdref:' + reference_id))
        self.add_property(URI('rdf:type'), URI('wikibase:Reference'))

    def add_value(self, p, v):
        self._add_value_node('pr', p, v)
