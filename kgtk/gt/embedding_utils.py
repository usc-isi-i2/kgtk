# TODO: Conver this code to use KgtkFormat and KgtkWriter in various places.
import io
import os
import re
import math
import sys
import time
import redis
from pathlib import Path
import pickle
import typing
import logging
import hashlib
import numpy as np
import pandas as pd  # type: ignore
from tqdm import tqdm  # type: ignore
from ast import literal_eval
from pyrallel import ParallelProcessor
from kgtk.exceptions import KGTKException
from collections import defaultdict, OrderedDict
from sentence_transformers import SentenceTransformer
from SPARQLWrapper import SPARQLWrapper, JSON, POST, URLENCODED  # type: ignore
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
from kgtk.value.kgtkvalueoptions import KgtkValueOptions
from kgtk.kgtkformat import KgtkFormat


class EmbeddingVector:
    def __init__(self, model_name=None, query_server=None, cache_config: dict = None, parallel_count=1):
        self._logger = logging.getLogger(__name__)
        if not model_name:
            self.model_name = 'bert-base-nli-mean-tokens'
        else:
            self.model_name = model_name
        self._logger.info("Using model {}".format(self.model_name))
        self.model = SentenceTransformer(self.model_name)
        # setup redis cache server
        if query_server is None or query_server == "":
            self.wikidata_server = "https://query.wikidata.org/sparql"
        else:
            self.wikidata_server = query_server
        if cache_config and cache_config.get("use_cache", False):
            host = cache_config.get("host", "dsbox01.isi.edu")
            port = cache_config.get("port", 6379)
            self.redis_server = connect_to_redis(host, port)
        else:
            self.redis_server = None
        self._parallel_count = int(parallel_count)
        self._logger.debug("Running with {} processes.".format(parallel_count))
        self.vectors_map = dict()
        self.node_labels = dict()  # this is used to store {node:label} pairs
        self.candidates = defaultdict(dict)  # this is used to store all node {node:dict()} information
        self.vectors_2D = None
        self.vector_dump_file: typing.Optional[str] = None
        self.gt_nodes = set()
        self.metadata = []
        self.gt_indexes = set()
        self.input_format = ""
        self.token_pattern = re.compile(r"(?u)\b\w\w+\b")

    def get_sentences_embedding(self, sentences: typing.List[str], qnodes: typing.List[str]):
        """
            transform a list of sentences to embedding vectors
        """

        if self.redis_server is not None:
            sentence_embeddings = []
            for each_node, each_sentence in zip(qnodes, sentences):
                query_cache_key = each_node + each_sentence
                if self.model_name != "bert-base-wikipedia-sections-mean-tokens":
                    query_cache_key += self.model_name
                cache_res = self.redis_server.get(query_cache_key)
                if cache_res is not None:
                    sentence_embeddings.append(literal_eval(cache_res.decode("utf-8")))
                    # self._logger.error("{} hit!".format(each_node+each_sentence))
                else:
                    each_embedding = self.model.encode([each_sentence], show_progress_bar=False)
                    sentence_embeddings.extend(each_embedding)
                    self.redis_server.set(query_cache_key, str(each_embedding[0].tolist()))
        else:
            sentence_embeddings = self.model.encode(sentences, show_progress_bar=False)
        return sentence_embeddings

    def send_sparql_query(self, query_body: str):
        """
            a simple wrap to send the query and return the returned results
        """
        qm = SPARQLWrapper(self.wikidata_server)
        qm.setReturnFormat(JSON)
        qm.setMethod(POST)
        qm.setRequestMethod(URLENCODED)
        self._logger.debug("Sent query is:")
        self._logger.debug(str(query_body))
        qm.setQuery(query_body)
        try:
            results = qm.query().convert()['results']['bindings']
            return results
        except Exception as e:
            error_message = ("Sending Sparql query to {} failed!".format(self.wikidata_server))
            self._logger.error(error_message)
            self._logger.debug(e, exc_info=True)
            raise KGTKException(error_message)

    def _get_labels(self, nodes: typing.List[str]):
        nodes_need_query = set()
        for each in nodes:
            if each not in self.node_labels:
                nodes_need_query.add(each)
        if nodes_need_query:
            query_nodes = " ".join(["wd:{}".format(each) for each in nodes_need_query])
            query = """
            select ?item ?nodeLabel
            where { 
              values ?item {""" + query_nodes + """}
              ?item rdfs:label ?nodeLabel.
              FILTER(LANG(?nodeLabel) = "en").
            }
            """
            results2 = self.send_sparql_query(query)
            for each_res in results2:
                node_id = each_res['item']['value'].split("/")[-1]
                nodes_need_query.remove(node_id)
                value = each_res['nodeLabel']['value']
                self.node_labels[node_id] = value

            # for those nodes we can't find label, just add this to dict to prevent query again
            for each_node in nodes_need_query:
                self.node_labels[each_node] = each_node

    def _get_labels_and_descriptions(self, query_qnodes: str, need_find_label: bool, need_find_description: bool):
        query_body = """
            select ?item ?itemDescription ?itemLabel
            where {
              values ?item {""" + query_qnodes + """ }
                 SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
            }
        """
        results = self.send_sparql_query(query_body)
        for each in results:
            each_node = each['item']['value'].split("/")[-1]
            if 'itemDescription' in each:
                description = each['itemDescription']['value']
            else:
                description = ""
            if "itemLabel" in each:
                label = each['itemLabel']['value']
            else:
                label = ""
            if need_find_label:
                self.candidates[each_node]["label_properties"] = [label]
            if need_find_description:
                self.candidates[each_node]["description_properties"] = [description]

    def _get_property_values(self, query_qnodes: str, properties: dict, properties_reversed: dict):
        """
        run sparql query to get corresponding property values of given q nodes
        """
        used_p_node_ids = set()
        all_needed_properties = ""
        for part_name, part in properties.items():
            if part_name == "isa_properties":
                self._get_labels(part)

        for each_node, role in properties_reversed.items():
            if role != {"has_properties"} and each_node not in {"label", "description", "all"}:
                all_needed_properties += "wdt:{} ".format(each_node)

        query_body = """
        select ?item ?properties ?eachPropertyValueLabel
        where {{
          values ?item {{{all_nodes}}}
          values ?properties {{{properties}}}
          ?item ?properties ?eachPropertyValue.
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
        }}
        """.format(all_nodes=query_qnodes, properties=all_needed_properties)
        results = self.send_sparql_query(query_body)

        for each_res in results:
            node_id = each_res['item']['value'].split("/")[-1]
            node_property = each_res['properties']['value'].split("/")[-1]
            roles = properties_reversed[node_property]
            value = each_res['eachPropertyValueLabel']['value']
            if node_property in properties["isa_properties"] and self.node_labels[node_property].endswith("of"):
                value = self.node_labels[node_property] + "||" + value
            used_p_node_ids.add(node_property)
            for each_role in roles:
                if each_role != "property_values":
                    if each_role in self.candidates[node_id]:
                        self.candidates[node_id][each_role].add(value)
                    else:
                        self.candidates[node_id][each_role] = {value}
        return used_p_node_ids

    def _get_all_properties(self, query_qnodes: str, used_p_node_ids: set, properties: dict):
        """
        run sparql query to get all properties of given q nodes
        """
        has_properties_set = set(properties["has_properties"])
        query_body3 = """
            select DISTINCT ?item ?p_entity ?p_entityLabel
            where {
              values ?item {""" + query_qnodes + """}
              ?item ?p ?o.
              FILTER regex(str(?p), "^http://www.wikidata.org/prop/P", "i")
              BIND (IRI(REPLACE(STR(?p), "http://www.wikidata.org/prop", "http://www.wikidata.org/entity")) AS ?p_entity) .
              SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
            }
            """
        results3 = self.send_sparql_query(query_body3)
        for each in results3:
            node_name = each['item']['value'].split("/")[-1]
            p_node_id = each['p_entity']['value'].split("/")[-1]
            p_node_label = each['p_entityLabel']['value']
            if p_node_id not in used_p_node_ids:
                if has_properties_set == {"all"} or p_node_id in has_properties_set:
                    if "has_properties" in self.candidates[node_name]:
                        self.candidates[node_name]["has_properties"].add(p_node_label)
                    else:
                        self.candidates[node_name]["has_properties"] = {p_node_label}

    def get_item_description(self, target_properties: dict, properties_reversed: dict,
                             qnodes: typing.Union[set, typing.List[str]]):
        """
            use sparql query to get the descriptions of given Q nodes
        """
        # find_all_properties = False
        if "all" in properties_reversed:
            # find_all_properties = True
            _ = properties_reversed.pop("all")
        self._logger.info("Need to find all properties.")

        hash_generator = hashlib.md5()
        # sort to ensure the hash key same
        target_properties = OrderedDict(sorted(target_properties.items()))
        hash_generator.update(str(target_properties).encode('utf-8'))
        properties_list_hash = "||" + str(hash_generator.hexdigest())

        sentences_cache_dict = {}
        if self.redis_server is not None:
            for each_node in qnodes:
                cache_key = each_node + properties_list_hash
                cache_res = self.redis_server.get(cache_key)
                self._logger.debug("Cached key is: {}".format(cache_key))
                if cache_res is not None:
                    self._logger.debug("Cache hit {}".format(cache_key))
                    sentences_cache_dict[each_node] = cache_res.decode("utf-8")

        self._logger.debug("Cached for those nodes {} / {}".format(len(sentences_cache_dict), len(qnodes)))
        self._logger.debug(str(set(sentences_cache_dict.keys())))
        self._logger.debug(
            "Need run query for those nodes {} / {}:".format(len(qnodes) - len(sentences_cache_dict), len(qnodes)))

        # we do not need to get those node again
        if len(sentences_cache_dict) > 0:
            qnodes = set(qnodes) - set(sentences_cache_dict.keys())
        self._logger.debug(str(qnodes))

        # only need to do query when we still have remained nodes
        if len(qnodes) > 0:
            query_qnodes = ""
            for each in qnodes:
                query_qnodes += "wd:{} ".format(each)

            need_find_label = "label" in target_properties["label_properties"]
            need_find_description = "description" in target_properties["description_properties"]
            # this is used to get corresponding labels / descriptions
            if need_find_label or need_find_description:
                self._get_labels_and_descriptions(query_qnodes, need_find_label, need_find_description)

            # this is used to get corresponding labels of properties values
            used_p_node_ids = self._get_property_values(query_qnodes, target_properties, properties_reversed)

            # if need get all properties, we need to run extra query
            # if find_all_properties:
            self._get_all_properties(query_qnodes, used_p_node_ids, target_properties)

        for each_node_id in qnodes:
            each_sentence = self.attribute_to_sentence(self.candidates[each_node_id], each_node_id)
            self.candidates[each_node_id]["sentence"] = each_sentence
            # add to cache
            if self.redis_server is not None:
                response = self.redis_server.set(each_node_id + properties_list_hash, each_sentence)
                if response:
                    self._logger.debug("Pushed cache for {} success.".format(each_node_id + properties_list_hash))

        for each_node_id, sentence in sentences_cache_dict.items():
            self.candidates[each_node_id]["sentence"] = sentence

    def _process_one(self, args):
        """
        one process for multiprocess calling, should not be used for any other function
        :param args: args to receive from main process
        :return: corresponding node vector and attribute
        """
        node_id = args["node_id"]
        each_node_attributes = args["attribute"]
        concat_sentence = self.attribute_to_sentence(each_node_attributes, node_id)
        vectors = self.get_sentences_embedding([concat_sentence], [node_id])[0]
        return {"v_" + node_id: vectors, "c_" + node_id: each_node_attributes}

    def _multiprocess_collector(self, data):
        for k, v in data.items():
            if k.startswith("v_"):
                k = k.replace("v_", "")
                self.vectors_map[k] = v
            else:
                k = k.replace("c_", "")
                self.candidates[k] = v

    def read_input(self,
                   input_file_path: Path,
                   target_properties: dict,
                   property_labels_dict: dict,
                   skip_nodes_set: set = None,
                   input_format: str = "kgtk_format",
                   black_list_set: typing.Optional[set] = None,
                   error_file: typing.TextIO = sys.stderr,
                   reader_options: typing.Optional[KgtkReaderOptions] = None,
                   value_options: typing.Optional[KgtkValueOptions] = None,
                   verbose: bool = False,
                   ):
        """
            load the input candidates files
        """
        self.node_labels.update(property_labels_dict)
        # reverse sentence property to be {property : role)
        properties_reversed = defaultdict(set)
        pp: typing.Optional[ParallelProcessor] = None

        # This type union becomes painful to work with, below.
        each_node_attributes: typing.Optional[typing.Mapping[str, typing.Union[typing.List, typing.Set]]] = None

        current_process_node_id = None
        node_id = None

        for k, v in target_properties.items():
            for each_property in v:
                properties_reversed[each_property].add(k)

        if input_format == "test_format":
            self.input_format = input_format
            input_file = open(input_file_path, "r") if str(input_file_path) != "-" else sys.stdin
            input_df = pd.read_csv(input_file, dtype=object)
            gt = {}
            count = 0
            if "GT_kg_id" in input_df.columns:
                gt_column_id = "GT_kg_id"
            elif "kg_id" in input_df.columns:
                gt_column_id = "kg_id"
            else:
                raise KGTKException(
                    "Can't find ground truth id column! It should either named as `GT_kg_id` or `kg_id`")

            for _, each in input_df.iterrows():
                temp = []
                if isinstance(each["candidates"], str):
                    temp = str(each['candidates']).split("|")
                elif each['candidates'] is np.nan or math.isnan(each['candidates']):
                    temp = []

                to_remove_q = set()
                if each[gt_column_id] is np.nan:
                    self._logger.warning("Ignore NaN gt value form {}".format(str(each)))
                    each[gt_column_id] = ""
                gt_nodes = each[gt_column_id].split(" ")
                label = str(each["label"])
                if len(gt_nodes) == 0:
                    self._logger.error("Skip a row with no ground truth node given: as {}".format(str(each)))
                    continue
                if label == "":
                    self._logger.error("Skip a row with no label given: as {}".format(str(each)))
                    continue
                temp.extend(gt_nodes)

                for each_q in temp:
                    if skip_nodes_set is not None and each_q in skip_nodes_set:
                        to_remove_q.add(each_q)
                temp = list(set(temp) - to_remove_q)
                count += len(temp)
                self.gt_nodes.add(each[gt_column_id])
                self.get_item_description(target_properties, properties_reversed, temp)

            self._logger.info("Totally {} rows with {} candidates loaded.".format(str(len(gt)), str(count)))

        elif input_format == "kgtk_format":
            # assume the input edge file is sorted
            if "all" in properties_reversed:
                _ = properties_reversed.pop("all")
                add_all_properties = True
            else:
                add_all_properties = False

            self.input_format = input_format

            kr: KgtkReader = KgtkReader.open(input_file_path,
                                             error_file=error_file,
                                             options=reader_options,
                                             value_options=value_options,
                                             verbose=verbose,
                                             )
            if kr.node1_column_idx < 0:
                raise KGTKException("Missing column: node1 or alias")
            if kr.label_column_idx < 0:
                raise KGTKException("Missing column: label or alias")
            if kr.node2_column_idx < 0:
                raise KGTKException("Missing column: node2 or alias")

            self._logger.debug("node1 column index = {}".format(kr.node1_column_idx))
            self._logger.debug("label column index = {}".format(kr.label_column_idx))
            self._logger.debug("node2 column index = {}".format(kr.node2_column_idx))

            # read contents
            each_node_attributes = {
                "has_properties": set(),
                "isa_properties": set(),
                "label_properties": [],
                "description_properties": [],
                "has_properties_values": [],
            }

            if self._parallel_count > 1:
                # need to set with spawn mode to initialize with multiple cuda in multiprocess
                from multiprocessing import set_start_method
                set_start_method('spawn')
                pp = ParallelProcessor(self._parallel_count, self._process_one, collector=self._multiprocess_collector)
                pp.start()

            row: typing.List[str]
            for row in kr:
                node_id = row[kr.node1_column_idx]
                # skip nodes id in black list
                if black_list_set and node_id in black_list_set:
                    continue

                node_property = row[kr.label_column_idx]
                node_value = row[kr.node2_column_idx]

                # CMR: the following code looks like it was intended to remove
                # any language code and language suffix.  It would have the
                # side effect of removing location coordinates entirely.
                #
                # remove @ mark
                if "@" in node_value and node_value[0] != "@":
                    node_value = node_value[:node_value.index("@")]

                # in case we meet an empty value, skip it
                if node_value == "":
                    self._logger.warning("""Skip line "{}" because of empty value.""".format(row))
                    continue

                # CMR: Better to use KgtkFormat.unstringify(node_value), as it will remove escapes from
                # internal double or single quotes.
                #
                # remove extra double quote " and single quote '
                while len(node_value) >= 3 and node_value[0] == '"' and node_value[-1] == '"':
                    node_value = node_value[1:-1]
                while len(node_value) >= 3 and node_value[0] == "'" and node_value[-1] == "'":
                    node_value = node_value[1:-1]

                if current_process_node_id != node_id:
                    if current_process_node_id is None:
                        current_process_node_id = node_id
                    else:
                        # if we get to next id, concat all properties into one sentence to represent the Q node

                        current_process_node_id, each_node_attributes = self.process_qnode(current_process_node_id,
                                                                                           each_node_attributes,
                                                                                           node_id, pp)

                if node_property in properties_reversed:
                    roles = properties_reversed[node_property].copy()
                    node_value = self.get_real_label_name(node_value)
                    # if we get property_values, it should be saved to isa-properties part
                    if "property_values" in roles:
                        # for property values part, changed to be "{property} {value}"
                        node_value_combine = self.get_real_label_name(node_property) + " " + self.get_real_label_name(node_value)
                        if each_node_attributes is None:
                            raise ValueError("each_node_attributes is missing")
                        if not isinstance(each_node_attributes["has_properties_values"], list):
                            raise ValueError('each_node_attributes["has_properties_values"] is not a list.')
                        each_node_attributes["has_properties_values"].append(node_value_combine)
                        # remove those 2 roles in case we have duplicate using of this node later
                        roles.discard("property_values")
                        roles.discard("has_properties")
                    for each_role in roles:
                        attrs: typing.Union[typing.List, typing.Set] = each_node_attributes[each_role]
                        if isinstance(attrs, set):
                            attrs.add(node_value)
                        elif isinstance(attrs, list):
                            attrs.append(node_value)
                        else:
                            raise ValueError('each_node_attributes[%s] is not a list or set.' % repr(each_role))

                elif add_all_properties:  # add remained properties if need all properties
                    attrs2: typing.Union[typing.List, typing.Set] = each_node_attributes["has_properties"]
                    if isinstance(attrs2, list):
                        attrs2.append(self.get_real_label_name(node_property))
                    else:
                        raise ValueError('each_node_attributes["has_properties"] is not a list.')

                # close multiprocess pool
                if self._parallel_count > 1 and pp is not None:
                    pp.task_done()
                    pp.join()
        else:
            raise KGTKException("Unknown input format {}".format(input_format))

        # case where there was a single qnode in the input file
        unprocessed_qnode = False
        if each_node_attributes:
            for k in each_node_attributes:
                if each_node_attributes[k]:
                    unprocessed_qnode = True
                    break
        if unprocessed_qnode:
            a, b = self.process_qnode(current_process_node_id, each_node_attributes, node_id, pp)
        self._logger.info("Totally {} Q nodes loaded.".format(len(self.candidates)))
        try:
            file_path = input_file_path.name
            file_name = file_path[:file_path.rfind(".")]
        except AttributeError:
            file_name = "input_from_memory"
        self.vector_dump_file = "dump_vectors_{}_{}.pkl".format(file_name, self.model_name)
        # self._logger.debug("The cache file name will be {}".format(self.vector_dump_file))

    def process_qnode(self, current_process_node_id, each_node_attributes, node_id, pp):
        # for multi process
        if self._parallel_count > 1:
            each_arg = {"node_id": current_process_node_id, "attribute": each_node_attributes}
            pp.add_task(each_arg)
        # for single process
        else:
            concat_sentence = self.attribute_to_sentence(each_node_attributes, current_process_node_id)
            each_node_attributes["sentence"] = concat_sentence
            self.candidates[current_process_node_id] = each_node_attributes
        # after write down finish, we can clear and start parsing next one
        each_node_attributes = {"has_properties": set(), "isa_properties": set(), "label_properties": [],
                                "description_properties": [], "has_properties_values": []}
        # update to new id
        current_process_node_id = node_id
        return current_process_node_id, each_node_attributes

    def get_real_label_name(self, node: str)->str:
        if node in self.node_labels:
            return self.node_labels[node].replace('"', "")
        else:
            return node

    def attribute_to_sentence(self, attribute_dict: dict, node_id=None):
        concated_sentence = ""
        have_isa_properties = False

        # sort the properties to ensure the sentence always same
        attribute_dict = {key: sorted(list(value)) for key, value in attribute_dict.items() if len(value) > 0}
        if "label_properties" in attribute_dict and len(attribute_dict["label_properties"]) > 0:
            concated_sentence += self.get_real_label_name(attribute_dict["label_properties"][0])
        if "description_properties" in attribute_dict and len(attribute_dict["description_properties"]) > 0:
            if concated_sentence != "" and attribute_dict["description_properties"][0] != "":
                concated_sentence += ", "
            concated_sentence += self.get_real_label_name(attribute_dict["description_properties"][0])
        if "isa_properties" in attribute_dict and len(attribute_dict["isa_properties"]) > 0:
            have_isa_properties = True
            temp_str: str = ""
            for each in attribute_dict["isa_properties"]:
                each = self.get_real_label_name(each)
                if "||" in each:
                    if "instance of" in each:
                        each = each.split("||")[1]
                    else:
                        each = each.replace("||", " ")
                temp_str += each + ", "
            if concated_sentence != "" and temp_str != "":
                concated_sentence += " is "
            elif concated_sentence == "":
                concated_sentence += "It is "
            # remove last ", "
            concated_sentence += temp_str[:-2]
        if "has_properties_values" in attribute_dict and len(attribute_dict["has_properties_values"]) > 0:
            temp_list: typing.List[str] = [self.get_real_label_name(each) for each in attribute_dict["has_properties_values"]]
            if concated_sentence != "":
                if not have_isa_properties:
                    concated_sentence += " "
                else:
                    concated_sentence += ", "
            else:
                concated_sentence += "It "
            concated_sentence += " and ".join(temp_list)
        if "has_properties" in attribute_dict and len(attribute_dict["has_properties"]) > 0:
            temp_list2: typing.List[str] = [self.get_real_label_name(each) for each in attribute_dict["has_properties"]]
            temp_list2 = list(set(temp_list2))
            if concated_sentence != "" and temp_list2[0] != "":
                if have_isa_properties:
                    concated_sentence += ", and has "
                else:
                    concated_sentence += " has "
            elif temp_list2[0] != "":
                concated_sentence += "It has "
            concated_sentence += " and ".join(temp_list2)
        # add ending period
        if concated_sentence != "":
            concated_sentence += "."
        self._logger.debug("Transform node {} --> {}".format(node_id, concated_sentence))
        return concated_sentence

    def get_vectors(self):
        """
            main function to get the vector representations of the descriptions
        """
        if self._parallel_count == 1:
            start_all = time.time()
            self._logger.info("Now generating embedding vector.")
            for q_node, each_item in tqdm(self.candidates.items()):
                # do process for each row(one target)
                sentence = each_item["sentence"]
                if isinstance(sentence, bytes):
                    sentence = sentence.decode("utf-8")
                vectors = self.get_sentences_embedding([sentence], [q_node])
                self.vectors_map[q_node] = vectors[0]
            self._logger.info("Totally used {} seconds.".format(str(time.time() - start_all)))
        else:
            # Skip get vector function because we already get them
            pass

    def dump_vectors(self, file_name, type_=None):
        if file_name.endswith(".pkl"):
            file_name = file_name.replace(".pkl", "")
        if type_ == "2D":
            with open(file_name + ".pkl", "wb") as f:
                pickle.dump(self.vectors_2D, f)
            dimension = len(self.vectors_2D[0])
            # TODO: This should probably be converted to KgtkWriter.
            with open(file_name + ".tsv", "w") as f:
                for each in self.vectors_2D:
                    for i, each_val in enumerate(each):
                        _ = f.write(str(each_val))
                        if i != dimension - 1:
                            _ = f.write("\t")
                    _ = f.write("\n")
        elif type_ == "metadata":
            with open(file_name + "_metadata.tsv", "w") as f:
                for each in self.metadata:
                    _ = f.write(each + "\n")
        else:
            with open(file_name + ".pkl", "wb") as f:
                pickle.dump(self.vectors_map, f)
            # TODO: This should probably be converted to KgtkWriter.
            with open(file_name + ".tsv", "w") as f:
                for each in self.vectors_map.values():
                    for i in each:
                        _ = f.write(str(i) + "\t")
                    _ = f.write("\n")

    def print_vector(self, vectors, output_properties: str = "text_embedding",
                     output_format="kgtk_format", save_embedding_sentence=False):
        self._logger.debug("START printing the vectors")
        if output_format == "kgtk_format":
            # TODO: This should be comverted to use KgtkWriter
            print("node\tproperty\tvalue\n", end="")
            all_nodes = list(self.vectors_map.keys())
            ten_percent_len = math.ceil(len(vectors) / 10)
            for i, each_vector in enumerate(vectors):
                if i % ten_percent_len == 0:
                    percent = i / ten_percent_len * 10
                    self._logger.debug("Finished {}%".format(percent))
                print("{}\t{}\t".format(all_nodes[i], output_properties), end="")
                for each_dimension in each_vector[:-1]:
                    print(str(each_dimension) + ",", end="")
                print(str(each_vector[-1]))
                if save_embedding_sentence:
                    print("{}\t{}\t{}".format(all_nodes[i], "embedding_sentence",
                                              self.candidates[all_nodes[i]]["sentence"]))

        elif output_format == "tsv_format":
            for each_vector in vectors:
                for each_dimension in each_vector[:-1]:
                    print(str(each_dimension) + "\t", end="")
                print(str(each_vector[-1]))
        self._logger.debug("END printing the vectors")

    def plot_result(self, output_properties: dict, input_format="kgtk_format",
                    output_uri: str = "", output_format="kgtk_format",
                    dimensional_reduction="none", dimension_val=2,
                    save_embedding_sentence=False
                    ):
        """
            transfer the vectors to lower dimension so that we can plot
            Then save the 2D vector file for further purpose
        """
        self.vectors_map = {k: v for k, v in sorted(self.vectors_map.items(), key=lambda item: item[0], reverse=True)}
        vectors = list(self.vectors_map.values())
        # reduce dimension if needed
        if dimensional_reduction.lower() == "tsne":
            self._logger.warning("Start running TSNE to reduce dimension. It will take some time.")
            start = time.time()
            from sklearn.manifold import TSNE  # type: ignore
            self.vectors_2D = TSNE(n_components=int(dimension_val), random_state=0).fit_transform(vectors)
            self._logger.info("Totally used {} seconds.".format(time.time() - start))
        elif dimensional_reduction.lower() == "pca":
            self._logger.warning("Start running PCA to reduce dimension. It will take some time.")
            start = time.time()
            from sklearn.decomposition import PCA  # type: ignore
            self.vectors_2D = PCA(n_components=int(dimension_val)).fit_transform(vectors)
            self._logger.info("Totally used {} seconds.".format(time.time() - start))
        elif dimensional_reduction.lower() == "none":
            self._logger.info("Not run dimensional reduction algorithm.")
        else:
            raise KGTKException("Unknown or unsupport dimensional reduction type: {}".format(dimensional_reduction))

        if output_uri not in {"", "none"}:
            if not os.path.exists(output_uri):
                raise ValueError("The given metadata output folder does not exist!")

            if self.vector_dump_file is None:
                raise ValueError("vector_dump_file is None")

            metadata_output_path = os.path.join(output_uri, self.vector_dump_file.split("/")[-1])
            if input_format == "test_format":
                gt_indexes = set()
                vector_map_keys = list(self.vectors_map.keys())
                for each_node in self.gt_nodes:
                    gt_indexes.add(vector_map_keys.index(each_node))

                self.metadata.append("Q_nodes\tType\tLabel\tDescription")
                for i, each in enumerate(self.vectors_map.keys()):
                    label = self.node_labels[each]
                    description = self.candidates[each]["sentence"]
                    if i in gt_indexes:
                        self.metadata.append("{}\tground_truth_node\t{}\t{}".format(each, label, description))
                    else:
                        self.metadata.append("{}\tcandidates\t{}\t{}".format(each, label, description))
                self.gt_indexes = gt_indexes

            elif input_format == "kgtk_format":
                if len(output_properties.get("metadata_properties", [])) == 0:
                    for k, v in self.candidates.items():
                        label = v.get("label_properties", "")
                        if len(label) > 0 and isinstance(label, list):
                            label = label[0]
                        description = v.get("description_properties", "")
                        if len(description) > 0 and isinstance(description, list):
                            description = description[0]
                        self.metadata.append("{}\t\t{}\t{}".format(k, label, description))
                else:
                    required_properties = output_properties["metadata_properties"]
                    self.metadata.append("node\t" + "\t".join(required_properties))
                    for k, v in self.candidates.items():
                        each_metadata = k + "\t"
                        for each in required_properties:
                            each_metadata += v.get(each, " ") + "\t"
                        self.metadata.append(each_metadata)
            self.dump_vectors(metadata_output_path, "metadata")

        output_props: str = output_properties.get("output_properties", "text_embedding")
        if self.vectors_2D is not None:
            self.print_vector(self.vectors_2D,
                              output_props,
                              output_format,
                              save_embedding_sentence)
        else:
            self.print_vector(vectors,
                              output_props,
                              output_format,
                              save_embedding_sentence)

    def evaluate_result(self):
        """
        for the ground truth nodes, evaluate the average distance to the centroid, the lower the average distance,
        the better clustering results should be
        """
        centroid = None
        gt_nodes_vectors = []
        if len(self.gt_indexes) == 0:
            points = set(range(len(self.vectors_map)))
        else:
            points = self.gt_indexes
        for i, each in enumerate(self.vectors_map.keys()):
            if i in points:
                if centroid is None:
                    centroid = np.array(self.vectors_map[each])
                else:
                    centroid += np.array(self.vectors_map[each])
                gt_nodes_vectors.append(self.vectors_map[each])
        centroid = centroid / len(points)

        distance_sum = 0
        for each in gt_nodes_vectors:
            distance_sum += self.calculate_distance(each, centroid)
        self._logger.info(
            "The average distance for the ground truth nodes to centroid is {}".format(distance_sum / len(points)))

    @staticmethod
    def calculate_distance(a, b):
        if len(a) != len(b):
            raise KGTKException("Vector dimension are different!")
        dist = 0
        for v1, v2 in zip(a, b):
            dist += (v1 - v2) ** 2
        dist = dist ** 0.5
        return dist


def connect_to_redis(host, port):
    _logger = logging.getLogger(__name__)
    redis_server = redis.Redis(host=host, port=port, db=0)
    try:
        _ = redis_server.get("foo")
        _logger.debug("Cache server {}:{} connected!".format(host, port))
    except Exception as e:
        _logger.error("Cache server {}:{} is not able to be connected! Will not use cache!".format(host, port))
        _logger.debug(e, exc_info=True)
        redis_server = None
    return redis_server
