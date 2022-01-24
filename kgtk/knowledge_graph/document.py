from typing import Dict
from kgtk.knowledge_graph.knowledge_graph import KnowledgeGraph


class Document(object):

    def __init__(self, _document: Dict, kg_schema, doc_id=None) -> None:
        self._document = _document
        if doc_id:
            self._document["doc_id"] = doc_id

        self.kg = KnowledgeGraph(kg_schema, self)
