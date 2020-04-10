from collections import defaultdict

from kgtk.graph_manager import GraphManager
from kgtk.nomalizer import normalize_text, normalize_ontology_type

import rltk # type: ignore


class Comparator(object):
    @staticmethod
    def get(type_):
        return {
            'aida-property:hasName': Comparator.name_sim,
            'aida-property:linkTarget': Comparator.link_sim,
            'aida-property:start': Comparator.datetime_sim,
            'aida-property:end': Comparator.datetime_sim,
        }[type_]

    @staticmethod
    def name_sim(a, b):

        def _decode(s):
            # en:"label1",ru:"label2"
            r = defaultdict(list)
            for l in s.split(','):
                lang, label = l[:2], l[4:-1]
                r[lang].append(normalize_text(label))
            return r

        if a == b:
            return 1
        if not a or not b:
            return

        # multi-lingual labels0
        ml_l_a, ml_l_b = _decode(a), _decode(b)
        shared_langs = set(ml_l_a.keys()) & set(ml_l_b.keys())
        score = 0
        for lang in shared_langs:
            l_a, l_b = ml_l_a[lang], ml_l_b[lang]
            score += rltk.jaccard_index_similarity(set(l_a), set(l_b)) / len(shared_langs)
        return score

    @staticmethod
    def datetime_sim(a, b):
        return a == b

    @staticmethod
    def link_sim(a, b):
        return a == b


class NodeMatcher(object):
    def __init__(self, graph_manager: GraphManager):
        self._gm = graph_manager

    def similarity(self, id1, id2):
        if not self._gm.in_graph(id1) or not self._gm.in_graph(id2):
            raise ValueError('Invalid id1 or id2')

        if id1 == id2:
            return 1.0

        # node type (item or property)
        cat1 = self._gm.get_node_type(id1)
        cat2 = self._gm.get_node_type(id2)
        if cat1 != cat2:
            return 0.0

        # attributes
        attr1 = self._gm.get_node_attributes(id1)
        attr2 = self._gm.get_node_attributes(id2)
        attr1_keys = set(attr1)
        attr2_keys = set(attr2)

        # comparing on same attributes
        attr_score = 0
        all_keys = attr1_keys & attr2_keys
        for key in all_keys:
            similarity = Comparator.get(key)
            attr_score += similarity(attr1[key], attr2[key]) / len(all_keys)  # weights of different attributes should be configurable

        # weight of overlapped keys (penalty of non-shared keys)
        attr_score *= rltk.jaccard_index_similarity(attr1_keys, attr2_keys)

        # class
        # aida's entity and event types are special
        # need a more general way to compare class similarity
        cls1 = self._gm.get_node_class(id1)
        cls2 = self._gm.get_node_class(id2)
        type1 = set(normalize_ontology_type(cls1).split())
        type2 = set(normalize_ontology_type(cls2).split())
        cls_score = len(type1 & type2) / max(len(type1 | type2), 1)

        return (attr_score + cls_score) / 2
