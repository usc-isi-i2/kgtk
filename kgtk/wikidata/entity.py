from kgtk.knowledge_graph.subject import Subject
from kgtk.knowledge_graph.node import URI, Literal
from kgtk.wikidata.statement import Statement, Rank
from kgtk.wikidata.value import Item, Property, Datatype
from uuid import uuid4

change_recorder = set()
revision = None


def revise(enable=False):
    """
    Tracking revision
    :param enable: If False (default), tracking stops. If True, a new revision will be generated.
    """
    global revision

    if not enable:
        revision = None
    else:
        revision = URI('http://www.isi.edu/etk/revision#{}'.format(uuid4().hex))


def serialize_change_record(fp):
    fp.writelines('{}\t{}\n'.format(node, prop) for node, prop in change_recorder)


class Entity(Subject):
    def __init__(self, node, creator):
        super().__init__(URI('wd:' + node))
        self.node_id = node
        self.creator = URI(creator) if creator else None

    def add_label(self, s: str, lang='en'):
        literal = Literal(s, lang=lang)
        self.add_property(URI('rdfs:label'), literal)
        self.add_property(URI('schema:name'), literal)
        self.add_property(URI('skos:prefLabel'), literal)

    def add_alias(self, s: str, lang='en'):
        self.add_property(URI('skos:altLabel'), Literal(s, lang=lang))

    def add_description(self, s: str, lang='en'):
        self.add_property(URI('schema:description'), Literal(s, lang=lang))

    def add_statement(self, p: str, v, rank=Rank.Normal, statement_id=None):
        global revision

        change_recorder.add((self.node_id, p))
        statement = Statement(self.node_id, rank, statement_id=statement_id)
        statement.add_value(p, v)
        statement.add_property(URI('http://www.isi.edu/etk/createdBy'), self.creator)
        if revision:
            statement.add_property(URI('http://www.isi.edu/etk/revision'), revision)
        self.add_property(URI('p:' + p), statement)
        return statement

    def add_truthy_value_node(self, p, v):
        self.add_property(URI('wdt:' + p), v.value)
        if v.normalized_value:
            self.add_property(URI('wdtn:' + p), v.normalized_value)

    def add_truthy_statement(self, p: str, v, statement_id=None):
        statement = self.add_statement(p, v, Rank.BestRank, statement_id)

        self.add_truthy_value_node(p, v)
        return statement


class WDItem(Entity, Item):
    def __init__(self, s: str, creator='http://www.isi.edu/datamart'):
        Entity.__init__(self, s, creator)
        Item.__init__(self, s)
        self.add_property(URI('rdf:type'), URI('wikibase:Item'))


class WDProperty(Entity, Property):
    def __init__(self, s: str, property_type, creator='http://www.isi.edu/datamart'):
        Entity.__init__(self, s, creator)
        Property.__init__(self, s)
        self.add_property(URI('rdf:type'), URI('wikibase:Property'))
        type_uri = property_type if not isinstance(property_type, Datatype) else Datatype(property_type)
        self.add_property(URI('wikibase:propertyType'), type_uri.type)

        self.add_property(URI('wikibase:directClaim'), URI('wdt:' + s))
        self.add_property(URI('wikibase:directClaimNormalized'), URI('wdtn:' + s))
        self.add_property(URI('wikibase:claim'), URI('p:' + s))
        self.add_property(URI('wikibase:statementProperty'), URI('ps:' + s))
        self.add_property(URI('wikibase:statementValue'), URI('psv:' + s))
        self.add_property(URI('wikibase:statementValueNormalized'), URI('psn:' + s))
        self.add_property(URI('wikibase:qualifier'), URI('pq:' + s))
        self.add_property(URI('wikibase:qualifierValue'), URI('pqv:' + s))
        self.add_property(URI('wikibase:qualifierValueNormalized'), URI('pqn:' + s))
        self.add_property(URI('wikibase:reference'), URI('pr:' + s))
        self.add_property(URI('wikibase:referenceValue'), URI('prv:' + s))
        self.add_property(URI('wikibase:referenceValueNormalized'), URI('prn:' + s))
        self.add_property(URI('wikibase:novalue'), URI('wdno:' + s))
