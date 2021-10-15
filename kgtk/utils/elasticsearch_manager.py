import requests
import json
import gzip
import re
import traceback
import pprint

from requests.auth import HTTPBasicAuth
from unidecode import unidecode
from typing import List, Tuple, Any

valid_context_types = {'i', 'q', 'e', 'm', 'd'}


class ElasticsearchManager(object):
    @staticmethod
    def build_kgtk_search_input(kgtk_file_path,
                                label_fields,
                                mapping_file_path,
                                output_path,
                                alias_fields=None,
                                extra_alias_properties=None,
                                pagerank_fields=None,
                                add_text=False,
                                description_properties=None,
                                separate_languages=True,
                                property_datatype_file=None
                                ):
        """
        builds a json lines file and a mapping file to support retrieval of candidates
        It is assumed that the file is sorted by subject and predicate, in order to be able to process it in a streaming fashion

        Args:
            kgtk_file_path: a file in KGTK format
            label_fields: field in the kgtk file to be used as labels
            mapping_file_path: output mapping file path for elasticsearch
            output_path: output json lines path, converted from the input kgtk file
            alias_fields: field in the kgtk file to be used as aliases
            pagerank_fields: field in the kgtk file to be used as pagerank
            black_list_file_path: path to black list file
        Returns: Nothing

        """

        labels = label_fields.split(',')
        aliases = alias_fields.split(',') if alias_fields else []
        extra_aliases_properties = set(extra_alias_properties.split(',')) if extra_alias_properties else set()
        pagerank = pagerank_fields.split(',') if pagerank_fields else []
        descriptions = description_properties.split(',') if description_properties else []

        # create the property data type dict
        property_datatype_dict = {}
        if property_datatype_file:
            property_datatype_dict = ElasticsearchManager.create_property_metadata_dict(property_datatype_file)

        if kgtk_file_path.endswith(".gz"):
            kgtk_file = gzip.open(kgtk_file_path)
        else:
            kgtk_file = open(kgtk_file_path, "r")

        if output_path.endswith(".gz"):
            output_file = gzip.open(output_path, mode='wt')
        else:
            output_file = open(output_path, 'w')

        _labels = dict()
        _aliases = dict()
        _descriptions = dict()
        _instance_ofs = set()
        data_type = None
        all_langs = set()
        lang = 'en'
        qnode_statement_count = 0
        is_class = False
        _wikitable_anchor_text = {}
        _wikipedia_anchor_text = {}
        _abbreviated_name = {}
        _redirect_text = {}
        _text_embedding = None
        _graph_embeddings_complex = None
        _graph_embeddings_transE = None
        ascii_labels = set()
        all_labels = set()
        property_count = None
        class_count = None
        context = None
        is_human = False
        _extra_aliases = set()
        _properties = set()
        _external_identifiers = set()
        _external_identifiers_pairs = set()

        _pagerank = 0.0

        prev_node = None
        i = 0

        column_header_dict = None
        try:
            for line in kgtk_file:
                i += 1
                if i % 1000000 == 0:
                    print('Processed {} lines...'.format(i))
                if isinstance(line, bytes):
                    line = line.decode('utf-8')
                line = line.replace('\n', '')
                if column_header_dict is None and 'node1' in line and 'id' in line and 'node2' in line:
                    # header line
                    cols = line.replace('\n', '').split('\t')
                    column_header_dict = {
                        'node1': cols.index('node1'),
                        'label': cols.index('label'),
                        'node2': cols.index('node2')
                    }

                # if line.startswith('Q'):
                else:
                    vals = line.split('\t')
                    node1_id = column_header_dict['node1']
                    label_id = column_header_dict['label']
                    node2_id = column_header_dict['node2']
                    node1 = vals[node1_id]
                    if '-' not in node1:  # ignore qualifiers
                        if prev_node is None:
                            prev_node = node1
                        if node1 != prev_node:
                            ElasticsearchManager._write_one_node(_labels=_labels,
                                                                 _aliases=_aliases,
                                                                 _pagerank=_pagerank,
                                                                 prev_node=prev_node,
                                                                 output_file=output_file,
                                                                 _descriptions=_descriptions,
                                                                 add_all_text=add_text,
                                                                 data_type=data_type,
                                                                 instance_ofs=_instance_ofs,
                                                                 qnode_statement_count=qnode_statement_count,
                                                                 is_class=is_class,
                                                                 wikitable_anchor_text=_wikitable_anchor_text,
                                                                 wikipedia_anchor_text=_wikipedia_anchor_text,
                                                                 abbreviated_name=_abbreviated_name,
                                                                 redirect_text=_redirect_text,
                                                                 text_embedding=_text_embedding,
                                                                 graph_embeddings_complex=_graph_embeddings_complex,
                                                                 graph_embeddings_transe=_graph_embeddings_transE,
                                                                 ascii_labels=ascii_labels,
                                                                 property_count=property_count,
                                                                 class_count=class_count,
                                                                 context=context,
                                                                 is_human=is_human,
                                                                 extra_aliases=_extra_aliases,
                                                                 properties=_properties,
                                                                 external_identifiers=_external_identifiers,
                                                                 external_identifiers_pairs=_external_identifiers_pairs
                                                                 )
                            # initialize for next node
                            _labels = dict()
                            _aliases = dict()
                            _descriptions = dict()
                            _instance_ofs = set()
                            data_type = None
                            _pagerank = 0.0
                            prev_node = node1
                            lang = 'en'
                            qnode_statement_count = 0
                            is_class = False
                            _wikitable_anchor_text = {}
                            _wikipedia_anchor_text = {}
                            _abbreviated_name = {}
                            _redirect_text = {}
                            _text_embedding = None
                            _graph_embeddings_complex = None
                            _graph_embeddings_transE = None
                            ascii_labels = set()
                            all_labels = set()
                            property_count = None
                            class_count = None
                            context = None
                            is_human = False
                            _extra_aliases = set()
                            _properties = set()
                            _external_identifiers = set()
                            _external_identifiers_pairs = set()

                        qnode_statement_count += 1
                        if vals[label_id] in labels:
                            if separate_languages:
                                tmp_val, lang = ElasticsearchManager.separate_language_text_tag(vals[node2_id])
                            else:
                                tmp_val = ElasticsearchManager.remove_language_tag(vals[node2_id])
                            if lang not in _labels:
                                _labels[lang] = set()
                                all_langs.add(lang)

                            if tmp_val.strip() != '':
                                _labels[lang].add(tmp_val)
                                all_labels.add(tmp_val)

                                if lang in {'en', 'de', 'es', 'fr', 'it', 'pt'}:
                                    # add transilerated value as well
                                    _ascii_label = ElasticsearchManager.transliterate_label(tmp_val)
                                    if _ascii_label != "" and _ascii_label not in all_labels:
                                        ascii_labels.add(_ascii_label)

                        elif vals[label_id] in aliases:
                            if separate_languages:
                                tmp_val, lang = ElasticsearchManager.separate_language_text_tag(vals[node2_id])
                            else:
                                tmp_val = ElasticsearchManager.remove_language_tag(vals[node2_id])
                            if lang not in _aliases:
                                _aliases[lang] = set()
                                all_langs.add(lang)

                            if tmp_val.strip() != '':
                                _aliases[lang].add(tmp_val)
                                all_labels.add(tmp_val)

                                if lang in {'en', 'de', 'es', 'fr', 'it', 'pt'}:
                                    # add transilerated value as well
                                    _ascii_alias = ElasticsearchManager.transliterate_label(tmp_val)
                                    if _ascii_alias != "" and _ascii_alias not in all_labels:
                                        ascii_labels.add(_ascii_alias)

                        elif vals[label_id] in pagerank:
                            tmp_val = ElasticsearchManager.to_float(vals[node2_id])
                            if tmp_val:
                                _pagerank = tmp_val
                        elif vals[label_id] in descriptions:
                            if separate_languages:
                                tmp_val, lang = ElasticsearchManager.separate_language_text_tag(vals[node2_id])
                            else:
                                tmp_val = ElasticsearchManager.remove_language_tag(vals[node2_id])
                            if lang not in _descriptions:
                                _descriptions[lang] = set()
                                all_langs.add(lang)
                            if tmp_val.strip() != '':
                                _descriptions[lang].add(tmp_val)
                        elif vals[label_id].strip() == 'isa_star' or vals[label_id].strip() == 'P39' \
                                or vals[label_id].strip() == 'P106' or vals[label_id].strip() == 'Pisa_star':
                            _instance_ofs.add(vals[node2_id])
                        elif vals[label_id].strip() == 'datatype':
                            data_type = vals[node2_id]
                        elif node1 in property_datatype_dict:
                            data_type = property_datatype_dict[node1]
                        elif vals[label_id] == 'P279' and vals[node2_id].startswith('Q'):
                            is_class = True
                        elif vals[label_id] == 'wikipedia_table_anchor':
                            tmp_val, lang = ElasticsearchManager.separate_language_text_tag(vals[node2_id])
                            if tmp_val.strip() != "":
                                if lang not in _wikitable_anchor_text:
                                    _wikitable_anchor_text[lang] = set()
                                _wikitable_anchor_text[lang].add(tmp_val)
                        elif vals[label_id] == 'wikipedia_anchor':
                            tmp_val, lang = ElasticsearchManager.separate_language_text_tag(vals[node2_id])
                            if tmp_val.strip() != "":
                                if lang not in _wikipedia_anchor_text:
                                    _wikipedia_anchor_text[lang] = set()
                                _wikipedia_anchor_text[lang].add(tmp_val)
                        elif vals[label_id] == 'redirect_from':
                            tmp_val, lang = ElasticsearchManager.separate_language_text_tag(vals[node2_id])
                            if tmp_val.strip() != "":
                                if lang not in _redirect_text:
                                    _redirect_text[lang] = set()
                                _redirect_text[lang].add(tmp_val)
                        elif vals[label_id] == 'abbreviated_name':
                            tmp_val, lang = ElasticsearchManager.separate_language_text_tag(vals[node2_id])
                            if tmp_val.strip() != "":
                                if lang not in _abbreviated_name:
                                    _abbreviated_name[lang] = set()
                                _abbreviated_name[lang].add(tmp_val)
                        elif vals[label_id] == 'graph_embeddings_complEx':
                            _graph_embeddings_complex = vals[node2_id]
                        elif vals[label_id] == 'graph_embeddings_transE':
                            _graph_embeddings_transE = vals[node2_id]
                        elif vals[label_id] == 'text_embedding':
                            _text_embedding = vals[node2_id]
                        elif vals[label_id] == 'property_count':
                            property_count = vals[node2_id]
                        elif vals[label_id] == 'class_count':
                            class_count = vals[node2_id]
                        elif vals[label_id] == 'context':
                            context_dict = ElasticsearchManager.parse_context_string(node1, vals[node2_id])
                            context = context_dict[node1]
                        elif vals[label_id] == 'P31' and vals[node2_id] == 'Q5':
                            is_human = True
                        elif vals[label_id] in extra_aliases_properties:
                            if separate_languages:
                                tmp_val, lang = ElasticsearchManager.separate_language_text_tag(vals[node2_id])
                            else:
                                tmp_val = ElasticsearchManager.remove_language_tag(vals[node2_id])

                            if tmp_val.strip() != '':
                                _extra_aliases.add(tmp_val)

                                if lang in {'en', 'de', 'es', 'fr', 'it', 'pt'}:
                                    _ascii_label = ElasticsearchManager.transliterate_label(tmp_val)
                                    if _ascii_label != "":
                                        _extra_aliases.add(_ascii_label)

                        if vals[label_id].startswith('P'):  # add to set of properties
                            _properties.add(vals[label_id])

                        if property_datatype_dict.get(vals[label_id], None) == 'external-id':
                            ex_id = vals[node2_id].replace('"', "").strip()
                            _external_identifiers.add(ex_id)
                            _external_identifiers_pairs.add(f"{vals[label_id]}:{ex_id}")

            # do one more write for last node
            ElasticsearchManager._write_one_node(_labels=_labels,
                                                 _aliases=_aliases,
                                                 _pagerank=_pagerank,
                                                 prev_node=prev_node,
                                                 output_file=output_file,
                                                 _descriptions=_descriptions,
                                                 add_all_text=add_text,
                                                 data_type=data_type,
                                                 instance_ofs=_instance_ofs,
                                                 qnode_statement_count=qnode_statement_count,
                                                 is_class=is_class,
                                                 wikitable_anchor_text=_wikitable_anchor_text,
                                                 wikipedia_anchor_text=_wikipedia_anchor_text,
                                                 abbreviated_name=_abbreviated_name,
                                                 redirect_text=_redirect_text,
                                                 text_embedding=_text_embedding,
                                                 graph_embeddings_complex=_graph_embeddings_complex,
                                                 graph_embeddings_transe=_graph_embeddings_transE,
                                                 ascii_labels=ascii_labels,
                                                 property_count=property_count,
                                                 class_count=class_count,
                                                 context=context,
                                                 is_human=is_human,
                                                 extra_aliases=_extra_aliases,
                                                 properties=_properties,
                                                 external_identifiers=_external_identifiers,
                                                 external_identifiers_pairs=_external_identifiers_pairs
                                                 )
        except:
            print(traceback.print_exc())

        mapping_dict = ElasticsearchManager.create_mapping_es(languages=list(all_langs))
        open(mapping_file_path, 'w').write(json.dumps(mapping_dict))
        print('Done!')

    @staticmethod
    def _write_one_node(**kwargs):
        """
        inner function called by build_elasticsearch_file only
        :param kwargs:
        :return:
        """
        labels = kwargs["_labels"]
        aliases = kwargs["_aliases"]
        descriptions = kwargs["_descriptions"]
        _pagerank = kwargs["_pagerank"]
        prev_node = kwargs["prev_node"]
        output_file = kwargs["output_file"]
        add_all_text = kwargs['add_all_text']
        instance_ofs = kwargs['instance_ofs']
        data_type = kwargs['data_type']
        qnode_statement_count = kwargs['qnode_statement_count']
        is_class = kwargs['is_class']
        wikitable_anchor_text = kwargs['wikitable_anchor_text']
        wikipedia_anchor_text = kwargs['wikipedia_anchor_text']
        redirect_text = kwargs['redirect_text']
        text_embedding = kwargs['text_embedding']
        graph_embeddings_complex = kwargs['graph_embeddings_complex']
        graph_embeddings_transe = kwargs['graph_embeddings_transe']
        ascii_labels = list(kwargs['ascii_labels'])
        property_count = kwargs['property_count']
        class_count = kwargs['class_count']
        context = kwargs['context']
        is_human = kwargs['is_human']
        extra_aliases = kwargs['extra_aliases']
        properties = kwargs['properties']
        external_identifiers = kwargs['external_identifiers']
        external_identifiers_pairs = kwargs['external_identifiers_pairs']

        _labels = {}
        _aliases = {}
        _descriptions = {}
        _wikitable_anchor_text = {}
        _wikipedia_anchor_text = {}
        _abbreviated_name = {}
        _redirect_text = {}
        en_labels_aliases = set()

        for k in labels:
            _labels[k] = list(labels[k])
            if is_human:
                if k == 'en':
                    en_labels_aliases.update(_labels[k])

        for k in aliases:
            _aliases[k] = list(aliases[k])
            if is_human:
                if k == 'en':
                    en_labels_aliases.update(_aliases[k])

        for k in descriptions:
            _descriptions[k] = list(descriptions[k])

        for k in wikitable_anchor_text:
            _wikitable_anchor_text[k] = list(wikitable_anchor_text[k])

        for k in wikipedia_anchor_text:
            _wikipedia_anchor_text[k] = list(wikipedia_anchor_text[k])

        # for k in abbreviated_name:
        #     _abbreviated_name[k] = list(abbreviated_name[k])

        for k in redirect_text:
            _redirect_text[k] = list(redirect_text[k])

        abbreviated_names = set()
        for name in en_labels_aliases:
            abbreviated_names.update(ElasticsearchManager.generate_abbreviations(name))

        if len(_labels) > 0 or len(_aliases) > 0 or len(_descriptions) > 0:

            _ = {'id': prev_node,
                 'labels': _labels,
                 'aliases': _aliases,
                 'pagerank': _pagerank,
                 'descriptions': _descriptions,
                 'statements': qnode_statement_count,
                 'wikitable_anchor_text': _wikitable_anchor_text,
                 'wikipedia_anchor_text': _wikipedia_anchor_text,
                 'redirect_text': _redirect_text,
                 'qnode_alias': prev_node
                 }

            if add_all_text:
                _['all_text'] = ElasticsearchManager.create_all_text(_labels, aliases=_aliases,
                                                                     descriptions=_descriptions)

            if len(instance_ofs) > 0:
                _['instance_ofs'] = list(instance_ofs)
            if data_type is not None:
                _['data_type'] = data_type
            if is_class:
                _['is_class'] = 'true'
            if text_embedding:
                _['text_embedding'] = text_embedding
            if graph_embeddings_complex:
                _['graph_embedding_complex'] = graph_embeddings_complex
            if graph_embeddings_transe:
                _['graph_embeddings_transe'] = graph_embeddings_transe
            if len(ascii_labels) > 0:
                _['ascii_labels'] = ascii_labels
            if class_count:
                _['class_count'] = class_count
            if property_count:
                _['property_count'] = property_count
            if context:
                _['context'] = context
            if len(abbreviated_names) > 0:
                _['abbreviated_name'] = {'en': list(abbreviated_names)}
            if len(extra_aliases) > 0:
                _['extra_aliases'] = list(extra_aliases)
            if len(properties) > 0:
                _['properties'] = list(properties)
            if len(external_identifiers) > 0:
                _['external_identifiers'] = list(external_identifiers)
            if len(external_identifiers_pairs) > 0:
                _['external_identifiers_pairs'] = list(external_identifiers_pairs)
            output_file.write(json.dumps(_))

            output_file.write('\n')

    @staticmethod
    def remove_language_tag(label_str):
        return re.sub(r'@.*$', '', label_str).replace("'", "")

    @staticmethod
    def separate_language_text_tag(label_str):
        if len(label_str) == 0:
            return "", "en"
        if "@" in label_str:
            res = label_str.split("@")
            text_string = "@".join(res[:-1]).replace('"', "").replace("'", "")
            lang = res[-1].replace('"', '').replace("'", "")
        else:
            text_string = label_str.replace('"', "").replace("'", "")
            lang = "en"
        return text_string, lang

    @staticmethod
    def create_all_text(labels, aliases, descriptions):
        text = ''
        if 'en' in labels and labels['en']:
            text = text + '\n'.join(labels['en']) + '\n'
        if 'en' in aliases and aliases['en']:
            text = text + '\n'.join(aliases['en']) + '\n'
        if 'en' in descriptions and descriptions['en']:
            text = text + '\n'.join(descriptions['en']) + '\n'
        return text

    @staticmethod
    def to_float(input_str):
        try:
            return float(input_str)
        except:
            return None

    @staticmethod
    def create_mapping_es(languages: List[str] = ['en']):
        fields_to_es_fields_mapping = {
            'abbreviated_name': {
                'field_type': 'text',
                'languages': languages,
                'es_fields': ['keyword_lower'],
                'copy_to': [],
                'enabled': True
            },
            'aliases': {
                'field_type': 'text',
                'languages': languages,
                'es_fields': ['keyword_lower', 'keyword'],
                'copy_to': ['all_labels.{}', 'all_labels_aliases'],
                'enabled': True
            },
            'all_labels': {
                'field_type': 'text',
                'languages': languages,
                'es_fields': ['keyword_lower', 'keyword', 'ngram', 'trigram'],
                'copy_to': [],
                'enabled': True
            },
            'all_labels_aliases': {
                'field_type': 'text',
                'languages': [],
                'es_fields': ['keyword_lower', 'keyword'],
                'copy_to': [],
                'enabled': True
            },
            'anchor_text': {
                'field_type': 'text',
                'languages': languages,
                'es_fields': ['keyword_lower', 'keyword', 'ngram'],
                'copy_to': [],
                'enabled': True
            },
            'ascii_labels': {
                'field_type': 'text',
                'languages': [],
                'es_fields': ['keyword_lower', 'keyword'],
                'copy_to': ['all_labels.en', 'all_labels_aliases'],
                'enabled': True
            },
            'extra_aliases': {
                'field_type': 'text',
                'languages': [],
                'es_fields': ['keyword_lower', 'keyword'],
                'copy_to': ['all_labels.en', 'all_labels_aliases'],
                'enabled': True
            },
            'external_identifiers': {
                'field_type': 'text',
                'languages': [],
                'es_fields': ['keyword_lower', 'keyword'],
                'copy_to': ['all_labels_aliases'],
                'enabled': True
            },
            'external_identifiers_pairs': {
                'field_type': 'text',
                'languages': [],
                'es_fields': ['keyword_lower', 'keyword'],
                'copy_to': [],
                'enabled': True
            },
            'class_count': {
                'enabled': False
            },
            'context': {
                'enabled': False
            },
            'data_type': {
                'field_type': 'text',
                'languages': [],
                'es_fields': ['keyword_lower'],
                'copy_to': [],
                'enabled': True
            },
            'descriptions': {
                'field_type': 'text',
                'languages': languages,
                'es_fields': ['keyword_lower'],
                'copy_to': [],
                'enabled': True
            },
            'graph_embedding_complex': {
                'enabled': False
            }, 'graph_embeddings_transe': {
                'enabled': False
            },
            'id': {
                'field_type': 'text',
                'languages': [],
                'es_fields': ['keyword_lower', 'keyword'],
                'copy_to': [],
                'enabled': True
            },
            'instance_ofs': {
                'field_type': 'text',
                'languages': [],
                'es_fields': ['keyword_lower'],
                'copy_to': [],
                'enabled': True
            },
            'properties': {
                'field_type': 'text',
                'languages': [],
                'es_fields': ['keyword_lower'],
                'copy_to': [],
                'enabled': True
            },
            'is_class': {
                'field_type': 'text',
                'languages': [],
                'es_fields': ['keyword_lower', 'keyword'],
                'copy_to': [],
                'enabled': True
            },
            'labels': {
                'field_type': 'text',
                'languages': languages,
                'es_fields': ['keyword_lower', 'keyword'],
                'copy_to': ['all_labels.{}', 'all_labels_aliases'],
                'enabled': True
            },
            'pagerank': {
                'field_type': 'float',
                'enabled': True
            },
            'property_count': {
                'enabled': False
            },
            'qnode_alias': {
                'field_type': 'text',
                'languages': [],
                'es_fields': ['keyword_lower', 'keyword'],
                'copy_to': ['all_labels.en', 'all_labels_aliases'],
                'enabled': True
            },
            'redirect_text': {
                'field_type': 'text',
                'languages': languages,
                'es_fields': ['keyword_lower'],
                'copy_to': [],
                'enabled': True
            },
            'statements': {
                'field_type': 'integer',
                'enabled': True
            },
            'text_embedding': {
                'enabled': False
            },
            'wikipedia_anchor_text': {
                'field_type': 'text',
                'languages': languages,
                'es_fields': ['keyword_lower'],
                'copy_to': ['anchor_text.{}'],
                'enabled': True
            },
            'wikitable_anchor_text': {
                'field_type': 'text',
                'languages': languages,
                'es_fields': ['keyword_lower'],
                'copy_to': ['anchor_text.{}'],
                'enabled': True
            }

        }

        properties_dict = {}

        for k in fields_to_es_fields_mapping:
            _ = fields_to_es_fields_mapping[k]
            properties_dict.update(ElasticsearchManager.create_mapping_part(field_name=k,
                                                                            field_type=_.get('field_type'),
                                                                            languages=_.get('languages', []),
                                                                            es_fields=_.get('es_fields', []),
                                                                            copy_to=_.get('copy_to', []),
                                                                            enabled=_.get('enabled')))

        settings = {
            "index": {
                "number_of_shards": 6,
                "analysis": {
                    "normalizer": {
                        "lowercase_normalizer": {
                            "filter": [
                                "lowercase"
                            ],
                            "type": "custom"
                        }
                    },
                    "analyzer": {
                        "edge_ngram_analyzer": {
                            "filter": [
                                "lowercase"
                            ],
                            "tokenizer": "edge_ngram_tokenizer"
                        },
                        "edge_ngram_search_analyzer": {
                            "tokenizer": "lowercase"
                        },
                        "trigram_analyzer": {
                            "tokenizer": "trigram_tokenizer",
                            "filter": [
                                "lowercase"
                            ]
                        }
                    },
                    "tokenizer": {
                        "edge_ngram_tokenizer": {
                            "token_chars": [
                                "letter"
                            ],
                            "min_gram": "2",
                            "type": "edge_ngram",
                            "max_gram": "20"
                        },
                        "trigram_tokenizer": {
                            "type": "ngram",
                            "min_gram": 3,
                            "max_gram": 4,
                            "token_chars": [
                                "letter"
                            ]
                        }
                    }
                }
            }
        }

        mapping_dict = {
            "mappings": {
                "properties": properties_dict
            },
            "settings": settings
        }
        return mapping_dict

    @staticmethod
    def load_elasticsearch_index(kgtk_jl_path, es_url, es_index, mapping_file_path=None, es_user=None,
                                 es_pass=None,
                                 batch_size=10000):
        """
         loads a jsonlines file to Elasticsearch index.

        Args:
            kgtk_jl_path: input json lines file, could be output of build_elasticsearch_index
            es_url:  Elasticsearch server url
            es_index: Elasticsearch index to be created/loaded
            mapping_file_path: mapping file for the index
            es_user: Elasticsearch user
            es_pass: Elasticsearch password
            batch_size: batch size to be loaded at once

        Returns: Nothing

        """

        # first create the index
        create_response = ElasticsearchManager.create_index(es_url, es_index, mapping_file_path, es_user, es_pass)
        print('create response: {}'.format(create_response.status_code))

        f = open(kgtk_jl_path)
        load_batch = []
        counter = 0

        for line in f:
            counter += 1

            each_res = line.replace('\n', '')
            if not each_res:
                continue
            json_x = json.loads(each_res)

            load_batch.append(json.dumps({"index": {"_id": json_x['id']}}))
            load_batch.append(line.replace('\n', ''))
            if len(load_batch) % batch_size == 0:
                counter += len(load_batch)
                print('done {} rows'.format(counter))
                response = None
                try:
                    response = ElasticsearchManager.load_index(es_url,
                                                               es_index,
                                                               '{}\n\n'.format('\n'.join(load_batch)),
                                                               es_user=es_user,
                                                               es_pass=es_pass)
                    if response.status_code >= 400:
                        print(response.text)
                except:
                    print('Exception while loading a batch to es')
                    print(response.text)
                    print(response.status_code)
                load_batch = []

        if len(load_batch) > 0:

            response = ElasticsearchManager.load_index(es_url,
                                                       es_index,
                                                       '{}\n\n'.format('\n'.join(load_batch)),
                                                       es_user=es_user,
                                                       es_pass=es_pass)
            if response.status_code >= 400:
                print(response.text)
        print('Finished loading the elasticsearch index')

    @staticmethod
    def load_index(es_url, es_index, payload, es_user=None, es_pass=None):

        es_url_bulk = '{}/{}/_doc/_bulk'.format(es_url, es_index)

        headers = {
            'Content-Type': 'application/x-ndjson',
        }
        if es_user and es_pass:
            return requests.post(es_url_bulk, headers=headers, data=payload, auth=HTTPBasicAuth(es_user, es_pass))
        else:
            return requests.post(es_url_bulk, headers=headers, data=payload)

    @staticmethod
    def create_index(es_url, es_index, mapping_file_path, es_user=None, es_pass=None):
        es_url_index = '{}/{}'.format(es_url, es_index)
        # first check if index exists
        if es_user and es_pass:
            response = requests.get(es_url_index, auth=HTTPBasicAuth(es_user, es_pass))
        else:
            response = requests.get(es_url_index)

        if response.status_code == 200:
            print('Index: {} already exists...'.format(es_index))
        elif response.status_code // 100 == 4:
            if mapping_file_path is not None:
                # no need to create index if mapping file is not specified, it'll be created at load time
                mapping = json.load(open(mapping_file_path))
                if es_user and es_pass:
                    response = requests.put(es_url_index, auth=HTTPBasicAuth(es_user, es_pass), json=mapping)
                else:
                    response = requests.put(es_url_index, json=mapping)
                if response.text and "error" in json.loads(response.text):
                    pp = pprint.PrettyPrinter(indent=4)
                    pp.pprint(json.loads(response.text))
                    raise Exception("Creating new index failed! Please check the error response above!")

        else:
            print('An exception has occurred: ')
            print(response.text)
        return response

    @staticmethod
    def create_property_metadata_dict(property_file_path: str) -> dict:
        _ = {}
        f = gzip.open(property_file_path, 'rt')
        node1_idx = -1
        node2_idx = -1
        for line in f:
            vals = line.strip().split("\t")
            if 'node1' in vals and 'node2' in vals:
                node1_idx = vals.index('node1')
                node2_idx = vals.index('node2')
            else:
                _[vals[node1_idx]] = vals[node2_idx]

        return _

    @staticmethod
    def transliterate_label(label: str) -> str:
        ascii_label = ""
        try:
            ascii_label = unidecode(label)
        except Exception as e:
            print(e, f'input label: {label}')
        return ascii_label

    # noinspection PyTypeChecker
    @staticmethod
    def create_mapping_part(field_name: str,
                            field_type: str,
                            languages: List[str],
                            es_fields: List[str],
                            copy_to: List[str],
                            enabled: bool = True):
        if not enabled:
            return {
                field_name: {
                    "type": "object",
                    "enabled": False
                }
            }

        if field_type in ['integer', 'float']:
            return {
                field_name: {
                    "type": field_type
                }
            }

        _mapping = None
        if field_type == 'text':
            if len(languages) == 0:
                _mapping = {
                    field_name: ElasticsearchManager.create_es_fields_part(field_type, es_fields)
                }

                if len(copy_to) > 0:
                    _mapping[field_name]['copy_to'] = copy_to if isinstance(copy_to, list) else [copy_to]
            else:
                _mapping = {
                    field_name: {
                        'properties': {}
                    }
                }
                for language in languages:
                    _mapping[field_name]['properties'][language] = ElasticsearchManager.create_es_fields_part(
                        field_type, es_fields)
                    if len(copy_to) > 0:
                        _mapping[field_name]['properties'][language]['copy_to'] = [x.format(language)
                                                                                   for x
                                                                                   in copy_to]

        return _mapping

    # noinspection PyTypeChecker
    @staticmethod
    def create_es_fields_part(field_type: str, es_fields: List[str]):
        _mapping = {
            "type": field_type
        }

        if len(es_fields) > 0:
            _mapping['fields'] = {}
            for es_field in es_fields:
                if es_field == 'keyword':
                    _mapping['fields'][es_field] = {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                elif es_field == 'keyword_lower':
                    _mapping['fields'][es_field] = {
                        "type": "keyword",
                        "normalizer": "lowercase_normalizer"
                    }
                elif es_field == 'ngram':
                    _mapping['fields'][es_field] = {
                        "type": "text",
                        "analyzer": "edge_ngram_analyzer",
                        "search_analyzer": "edge_ngram_search_analyzer"
                    }
                elif es_field == "trigram":
                    _mapping['fields'][es_field] = {
                        "type": "text",
                        "analyzer": "trigram_analyzer"
                    }

        return _mapping

    @staticmethod
    def generate_abbreviations(name: str) -> List[str]:
        '''
        Helper function to generate the abbreviation.
        Input: name_split: List of the words in a name
        Output: Abbreviated Name
        '''
        name_split = name.split()
        abbreviated_names = set()

        abbr_label = ''
        for word in name_split[:-1]:
            abbr_label += word[0].upper() + '.' + ' '
        abbr_label += name_split[-1]

        abbreviated_names.add(abbr_label)

        if len(name_split) >= 2:
            abbr_label_end = name_split[-1] + ',' + ' '
            for word in name_split[:-1]:
                abbr_label_end += word[0].upper() + '.' + ' '

            abbreviated_names.add(abbr_label_end)

        for i in range(len(name_split) - 1):
            abbreviated_names.add(ElasticsearchManager._generate_abbr(name_split, i))

        return list(abbreviated_names)

    @staticmethod
    def _generate_abbr(name_split: List[str], word_index: int) -> str:
        abbr_label = ''
        for i in range(len(name_split) - 1):
            if i != word_index:
                abbr_label += name_split[i] + ' '
            else:
                abbr_label += name_split[i][0].upper() + '.' + ' '
        abbr_label += name_split[-1]
        return abbr_label

    @staticmethod
    def remove_text_inside_brackets(text, brackets="()"):
        count = [0] * (len(brackets) // 2)  # count open/close brackets
        saved_chars = []
        for character in text:
            for i, b in enumerate(brackets):
                if character == b:  # found bracket
                    kind, is_close = divmod(i, 2)
                    count[kind] += (-1) ** is_close  # `+1`: open, `-1`: close
                    if count[kind] < 0:  # unbalanced bracket
                        count[kind] = 0  # keep it
                    else:  # found bracket to remove
                        break
            else:  # character is not a [balanced] bracket
                if not any(count):  # outside brackets
                    saved_chars.append(character)
        return ''.join(saved_chars).strip()

    @staticmethod
    def parse_context_string(qnode, context_string: str) -> dict:

        context_dict = {
            qnode: []
        }

        p_v_dict = {}
        try:
            if context_string:
                prop_val_list = re.split(r'(?<!\\)\|', context_string)

                for prop_val in prop_val_list:
                    _type = prop_val[0]

                    assert _type in valid_context_types, f"Invalid context type :{_type} found, Qnode: {qnode}," \
                                                         f" property value string: {prop_val}"

                    values, property, item = ElasticsearchManager.parse_prop_val(qnode, prop_val)

                    if _type == 'd' and values.startswith("^"):
                        values = values.replace("^", "")

                    if item is None:
                        key = property
                        if key not in p_v_dict:
                            p_v_dict[key] = {
                                'p': property,
                                "t": _type,
                                'v': []
                            }
                        p_v_dict[key]['v'].append(values)

                    else:
                        key = f"{property}_{item}"
                        if key not in p_v_dict:
                            p_v_dict[key] = {
                                'p': property,
                                'i': item,
                                'v': [],
                                "t": _type
                            }
                        p_v_dict[key]['v'].append(values)
        except Exception as e:
            raise Exception(e)

        for k in p_v_dict:
            context_dict[qnode].append(p_v_dict[k])

        return context_dict

    @staticmethod
    def parse_prop_val(qnode: str, property_value_string: str) -> Tuple[str, str, Any]:
        line_started = False
        string_value = list()

        property_value_string = property_value_string[1:]

        for i, c in enumerate(property_value_string):
            if i == 0 and c == '"':  # start of the string value:
                line_started = True
            if line_started:
                string_value.append(c)
            if (i > 0 and c == '"' and property_value_string[i - 1] != "\\") \
                    or \
                    (i > 0 and c == '"' and property_value_string[i + 1] == ":" and property_value_string[
                        i + 2] == "P"):
                line_started = False
        string_val = "".join(string_value)
        length_remove = len(string_val) + 1  # ":" eg i"utc+01:00":P421:Q6655
        rem_vals = property_value_string[length_remove:].split(":")
        n = len(string_val)
        string_val = string_val[1: n - 1]

        property = rem_vals[0]

        if not property.startswith('P'):
            raise Exception(
                f"Unexpected format of the context string, Qnode: {qnode}, context string: {property_value_string}. "
                f"Property does not starts with 'P'")

        if len(rem_vals) == 2:
            item = rem_vals[1]
            if not item.startswith('Q'):
                raise Exception(
                    f"Unexpected format of the context string, Qnode: {qnode}, context string: {property_value_string}"
                    f". Item does not start with 'Q'")
            return string_val, property, item

        if len(rem_vals) == 1:
            return string_val, property, None

        if len(rem_vals) > 2:
            raise Exception(
                f"Unexpected format of the context string, Qnode: {qnode}, context string: {property_value_string}")
