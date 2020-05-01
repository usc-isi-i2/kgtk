import typing
from kgtk.exceptions import KGTKException

ALL_EMBEDDING_MODELS_NAMES = [
    "bert-base-nli-cls-token",
    "bert-base-nli-max-tokens",
    "bert-base-nli-mean-tokens",
    "bert-base-nli-stsb-mean-tokens",
    "bert-base-wikipedia-sections-mean-tokens",
    "bert-large-nli-cls-token",
    "bert-large-nli-max-tokens",
    "bert-large-nli-mean-tokens",
    "bert-large-nli-stsb-mean-tokens",
    "distilbert-base-nli-mean-tokens",
    "distilbert-base-nli-stsb-mean-tokens",
    "distiluse-base-multilingual-cased",
    "roberta-base-nli-mean-tokens",
    "roberta-base-nli-stsb-mean-tokens",
    "roberta-large-nli-mean-tokens",
    "roberta-large-nli-stsb-mean-tokens"
]


class EmbeddingVector:
    def __init__(self, model_name=None, query_server=None, cache_config: dict = {}):
        from sentence_transformers import SentenceTransformer, SentencesDataset, LoggingHandler, losses, models  # type: ignore
        import logging
        import re
        self._logger = logging.getLogger(__name__)
        from collections import defaultdict
        if model_name is None:
            self.model_name = 'bert-base-nli-mean-tokens'
        # xlnet need to be trained before using, we can't use this for now
        # elif model_name == "xlnet-base-cased":
        #     word_embedding_model = models.XLNet('xlnet-base-cased')
        # # Apply mean pooling to get one fixed sized sentence vector
        #     pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension(),
        #                                pooling_mode_mean_tokens=True,
        #                                pooling_mode_cls_token=False,
        #                                pooling_mode_max_tokens=False)
        #     self.model = SentenceTransformer(modules=[word_embedding_model, pooling_model])
        else:
            self.model_name = model_name
        self._logger.info("Using model {}".format(self.model_name))
        self.model = SentenceTransformer(self.model_name)
        # setup redis cache server
        if query_server is None or query_server == "":
            self.wikidata_server = "https://query.wikidata.org/sparql"
        else:
            self.wikidata_server = query_server
        use_cache = cache_config.get("use_cache", False)
        if use_cache:
            import redis
            host = cache_config.get("host", "dsbox01.isi.edu")
            port = cache_config.get("port", 6379)
            self.redis_server = redis.Redis(host=host, port=port, db=0)
            try:
                _ = self.redis_server.get("foo")
                self._logger.debug("Cache server {}:{} connected!".format(host, port))
            except:
                self._logger.error("Cache server {}:{} is not able to be connected! Will not use cache!".format(host, port))
                self.redis_server = None
        else:
            self.redis_server = None
        self.qnodes_descriptions = dict()
        self.vectors_map = dict()
        self.property_labels_dict = dict()
        self.q_node_to_label = dict()
        self.node_labels = dict()
        self.vectors_2D = None
        self.vector_dump_file = None
        self.gt_nodes = set()
        self.candidates = defaultdict(dict)
        self.metadata = []
        self.gt_indexes = set()
        self.input_format = ""
        self.token_pattern = re.compile(r"(?u)\b\w\w+\b")

    def get_sentences_embedding(self, sentences: typing.List[str], qnodes: typing.List[str]):
        """
            transform a list of sentences to embedding vectors
        """
        from ast import literal_eval
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
        from SPARQLWrapper import SPARQLWrapper, JSON, POST, URLENCODED  # type: ignore
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
        except:
            raise KGTKException("Sending Sparql query to {} failed!".format(self.wikidata_server))

    def _get_labels(self, nodes: typing.List[str]):
        query_nodes = " ".join(["wd:{}".format(each) for each in nodes])
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
            value = each_res['nodeLabel']['value']
            self.node_labels[node_id] = value

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

    def _get_property_values(self, query_qnodes, query_part_names, query_part_properties):
        used_p_node_ids = set()
        for part_name, part in zip(query_part_names, query_part_properties):
            if part_name == "isa_properties":
                self._get_labels(part)
            for i, each in enumerate(part):
                if each not in {"label", "description", "all"}:
                    query_body2 = """
                    select ?item ?eachPropertyLabel
                    where {{
                      values ?item {{{all_nodes}}}
                    ?item wdt:{qnode} ?eachProperty.
                      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
                    }}
                    """.format(all_nodes=query_qnodes, qnode=each)
                    results2 = self.send_sparql_query(query_body2)

                    for each_res in results2:
                        node_id = each_res['item']['value'].split("/")[-1]
                        value = each_res['eachPropertyLabel']['value']
                        if part_name == "isa_properties" and self.node_labels[each].endswith("of"):
                            value = self.node_labels[each] + "||" + value
                        used_p_node_ids.add(node_id)
                        if part_name in self.candidates[node_id]:
                            self.candidates[node_id][part_name] = value
                        else:
                            self.candidates[node_id][part_name] = {value}
        return used_p_node_ids

    def _get_all_properties(self, query_qnodes, used_p_node_ids, properties_list):
        has_properties_set = set(properties_list[3])
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
                if properties_list[3] == ["all"] or p_node_id in has_properties_set:
                    if "has_properties" in self.candidates[node_name]:
                        self.candidates[node_name]["has_properties"].add(p_node_label)
                    else:
                        self.candidates[node_name]["has_properties"] = {p_node_label}

    def get_item_description(self, qnodes: typing.List[str] = None, target_properties: dict = {}):
        """
            use sparql query to get the descriptions of given Q nodes
        """
        if qnodes is None:
            qnodes = self.candidates
        if "all" in target_properties:
            find_all_properties = True
        else:
            find_all_properties = False
        properties_list = [[] for _ in range(4)]
        names = ["labels", "descriptions", "isa_properties", "has_properties"]
        for k, v in target_properties.items():
            if v == "label_properties":
                properties_list[0].append(k)
            elif v == "description_properties":
                properties_list[1].append(k)
            elif v == "isa_properties":
                properties_list[2].append(k)
            elif v == "has_properties":
                properties_list[3].append(k)

        sentences_cache_dict = {}
        if self.redis_server is not None:
            for each_node in qnodes:
                cache_res = self.redis_server.get(each_node + str(properties_list))
                if cache_res is not None:
                    sentences_cache_dict[each_node] = cache_res.decode("utf-8")

        if len(sentences_cache_dict) > 0:
            qnodes = set(qnodes) - set(sentences_cache_dict.keys())

        # only need to do query when we still have remained nodes
        if len(qnodes) > 0:
            need_find_label = "label" in properties_list[0]
            need_find_description = "description" in properties_list[1]
            query_qnodes = ""
            for each in qnodes:
                query_qnodes += "wd:{} ".format(each)

            # this is used to get corresponding labels / descriptions
            if need_find_label or need_find_description:
                self._get_labels_and_descriptions(query_qnodes, need_find_label, need_find_description)

            if len(properties_list[3]) > len(qnodes):
                # in this condition, we have too many properties need to be queried, it will waste time
                # query to get all properties then filtering would save more times
                find_all_properties = True
                query_part2_names = names[:3]
                query_part2_properties = properties_list[:3]
            else:
                query_part2_names = names
                query_part2_properties = properties_list
            # this is used to get corresponding labels of properties values
            used_p_node_ids = self._get_property_values(query_qnodes, query_part2_names, query_part2_properties)

            # if need get all properties, we need to run extra query
            if find_all_properties:
                self._get_all_properties(query_qnodes, used_p_node_ids, properties_list)

        for each_node_id in qnodes:
            each_sentence = self.attribute_to_sentence(self.candidates[each_node_id], each_node_id)
            self.candidates[each_node_id]["sentence"] = each_sentence
            if self.redis_server is not None:
                self.redis_server.set(each_node_id + str(properties_list), each_sentence)

        for each_node_id, sentence in sentences_cache_dict.items():
            self.candidates[each_node_id]["sentence"] = sentence

    def read_input(self, file_path: str, skip_nodes_set: set = None,
                   input_format: str = "kgtk_format", target_properties: dict = {},
                   property_labels_dict: dict = {}, black_list_set: set = set()
                   ):
        """
            load the input candidates files
        """
        from collections import defaultdict
        import pandas as pd  # type: ignore
        import numpy as np
        import math

        self.property_labels_dict = property_labels_dict

        if input_format == "test_format":
            self.input_format = input_format
            input_df = pd.read_csv(file_path)
            gt = {}
            count = 0
            if "GT_kg_id" in input_df.columns:
                gt_column_id = "GT_kg_id"
            elif "kg_id" in input_df.columns:
                gt_column_id = "kg_id"
            else:
                raise KGTKException("Can't find ground truth id column! It should either named as `GT_kg_id` or `kg_id`")

            for _, each in input_df.iterrows():
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
                    self.q_node_to_label[each_q] = label
                    if skip_nodes_set is not None and each_q in skip_nodes_set:
                        to_remove_q.add(each_q)
                temp = set(temp) - to_remove_q
                count += len(temp)
                self.gt_nodes.add(each[gt_column_id])
                self.get_item_description(temp, target_properties)

            self._logger.info("Totally {} rows with {} candidates loaded.".format(str(len(gt)), str(count)))

        elif input_format == "kgtk_format":
            # assume the input edge file is sorted
            if "all" in target_properties:
                _ = target_properties.pop("all")
                add_all_properties = True
            else:
                add_all_properties = False

            self.input_format = input_format
            with open(file_path, "r") as f:
                # get header
                headers = f.readline().replace("\n", "").split("\t")
                if len(headers) < 3:
                    raise KGTKException(
                        "No enough columns found on given input file. Only {} columns given but at least 3 needed.".format(
                            len(headers)))
                elif "node" in headers and "property" in headers and "value" in headers:
                    column_references = {"node": headers.index("node"),
                                         "property": headers.index("property"),
                                         "value": headers.index("value")}
                elif len(headers) == 3:
                    column_references = {"node": 0,
                                         "property": 1,
                                         "value": 2}
                else:
                    missing_column = {"node", "property", "value"} - set(headers)
                    raise KGTKException("Missing column {}".format(missing_column))
                self._logger.debug("column index information: ")
                self._logger.debug(str(column_references))
                # read contents
                each_node_attributes = {"has_properties": [], "isa_properties": [], "label_properties": [],
                                        "description_properties": []}
                current_process_node_id = None
                for each_line in f:
                    each_line = each_line.replace("\n", "").split("\t")
                    node_id = each_line[column_references["node"]]
                    node_property = each_line[column_references["property"]]
                    node_value = each_line[column_references["value"]]
                    # remove @ mark
                    if "@" in node_value and node_value[0] != "@":
                        node_value_org = node_value
                        node_value = node_value[:node_value.index("@")]

                    # remove extra double quote " and single quote '
                    if node_value[0] == '"' and node_value[-1] == '"':
                        node_value = node_value[1:-1]
                    if node_value[0] == "'" and node_value[-1] == "'":
                        node_value = node_value[1:-1]

                    if current_process_node_id != node_id:
                        if current_process_node_id is None:
                            current_process_node_id = node_id
                        else:
                            # if we get to next id
                            # concate all properties into one sentence to represent the Q node
                            concated_sentence = self.attribute_to_sentence(each_node_attributes, current_process_node_id)
                            each_node_attributes["sentence"] = concated_sentence
                            self.candidates[current_process_node_id] = each_node_attributes
                            # after write down finish, we can cleaer and start parsing next one
                            each_node_attributes = {"has_properties": [], "isa_properties": [], "label_properties": [],
                                                    "description_properties": []}
                            # update to new id
                            current_process_node_id = node_id

                    if node_property in target_properties:
                        each_node_attributes[target_properties[node_property]].append(node_value)
                    if add_all_properties and each_line[column_references["value"]][0] == "P":
                        each_node_attributes["has_properties"].append(node_value)

        else:
            raise KGTKException("Unkonwn input format {}".format(input_format))

        self._logger.info("Totally {} Q nodes loaded.".format(len(self.candidates)))
        self.vector_dump_file = "dump_vectors_{}_{}.pkl".format(file_path[:file_path.rfind(".")], self.model_name)
        # self._logger.debug("The cache file name will be {}".format(self.vector_dump_file))

    def get_real_label_name(self, node):
        if node in self.property_labels_dict:
            return self.property_labels_dict[node]
        else:
            return node

    def attribute_to_sentence(self, v, node_id=None):
        concated_sentence = ""
        have_isa_properties = False
        # sort the properties to ensure the sentence always same
        v = {key: sorted(list(value)) for key, value in v.items() if len(value) > 0}
        if "label_properties" in v and len(v["label_properties"]) > 0:
            concated_sentence += self.get_real_label_name(v["label_properties"][0])
        if "description_properties" in v and len(v["description_properties"]) > 0:
            if concated_sentence != "" and v["description_properties"][0] != "":
                concated_sentence += ", "
            concated_sentence += self.get_real_label_name(v["description_properties"][0])
        if "isa_properties" in v and len(v["isa_properties"]) > 0:
            have_isa_properties = True
            temp = ""
            for each in v["isa_properties"]:
                each = self.get_real_label_name(each)
                if "||" in each:
                    if "instance of" in each:
                        each = each.split("||")[1]
                    else:
                        each = each.replace("||", " ")
                temp += each + ", "
            if concated_sentence != "" and temp != "":
                concated_sentence += " is a "
            elif concated_sentence == "":
                concated_sentence += "It is a "
            concated_sentence += temp[:-2]
        if "has_properties" in v and len(v["has_properties"]) > 0:
            temp = [self.get_real_label_name(each) for each in v["has_properties"]]
            if concated_sentence != "" and temp[0] != "":
                if have_isa_properties:
                    concated_sentence += ", and has "
                else:
                    concated_sentence += " has "
            elif temp[0] != "":
                concated_sentence += "It has "
            concated_sentence += " and ".join(temp)
        self._logger.debug("Transform node {} --> {}".format(node_id, concated_sentence))
        return concated_sentence

    def get_vetors(self):
        """
            main function to get the vector representations of the descriptions
        """
        import os
        import time
        from tqdm import tqdm  # type: ignore

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

    def dump_vectors(self, file_name, type_=None):
        import pickle
        if file_name.endswith(".pkl"):
            file_name = file_name.replace(".pkl", "")
        if type_ == "2D":
            with open(file_name + ".pkl", "wb") as f:
                pickle.dump(self.vectors_2D, f)
            dimension = len(self.vectors_2D[0])
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
            with open(file_name + ".tsv", "w") as f:
                for each in self.vectors_map.values():
                    for i in each:
                        _ = f.write(str(i) + "\t")
                    _ = f.write("\n")

    def print_vector(self, vectors, output_properties: str = "text_embedding", output_format="kgtk_format"):
        if output_format == "kgtk_format":
            print("node\tproperty\tvalue\n", end="")
            if self.input_format == "kgtk_format":
                for i, each_vector in enumerate(vectors):
                    print(str(list(self.candidates.keys())[i]) + "\t", end="")
                    print(output_properties + "\t", end="")
                    for j, each_dimension in enumerate(each_vector):
                        if j != len(each_vector) - 1:
                            print(str(each_dimension) + ",", end="")
                        else:
                            print(str(each_dimension) + "\n", end="")
            elif self.input_format == "test_format":
                all_nodes = list(self.vectors_map.keys())
                for i, each_vector in enumerate(vectors):
                    print(all_nodes[i] + "\t", end="")
                    print(output_properties + "\t", end="")
                    for j, each_dimension in enumerate(each_vector):
                        if j != len(each_vector) - 1:
                            print(str(each_dimension) + ",", end="")
                        else:
                            print(str(each_dimension) + "\n", end="")

        elif output_format == "tsv_format":
            for each_vector in vectors:
                for i, each_dimension in enumerate(each_vector):
                    if i != len(each_vector) - 1:
                        print(str(each_dimension) + "\t", end="")
                    else:
                        print(str(each_dimension) + "\n", end="")

    def plot_result(self, output_properties={}, input_format="kgtk_format",
                    output_uri: str = "", output_format="kgtk_format",
                    run_TSNE=True
                    ):
        """
            transfer the vectors to lower dimension so that we can plot
            Then save the 2D vector file for further purpose
        """
        import os
        import time
        from sklearn.manifold import TSNE  # type: ignore

        self.vectors_map = {k: v for k, v in sorted(self.vectors_map.items(), key=lambda item: item[0], reverse=True)}
        vectors = list(self.vectors_map.values())
        # use tsne to reduce dimension
        if run_TSNE:
            self._logger.warning("Start running TSNE to reduce dimension. It will take a long time.")
            start = time.time()
            self.vectors_2D = TSNE(n_components=2, random_state=0).fit_transform(vectors)
            self._logger.info("Totally used {} seconds.".format(time.time() - start))

        if input_format == "test_format":
            gt_indexes = set()
            vector_map_keys = list(self.vectors_map.keys())
            for each_node in self.gt_nodes:
                gt_indexes.add(vector_map_keys.index(each_node))

            self.metadata.append("Q_nodes\tType\tLabel\tDescription")
            for i, each in enumerate(self.vectors_map.keys()):
                label = self.q_node_to_label[each]
                description = self.candidates[each]["sentence"]
                if i in gt_indexes:
                    self.metadata.append("{}\tground_truth_node\t{}\t{}".format(each, label, description))
                else:
                    self.metadata.append("{}\tcandidates\t{}\t{}".format(each, label, description))
            self.gt_indexes = gt_indexes

        elif input_format == "kgtk_format":
            if len(output_properties.get("metatada_properties", [])) == 0:
                for k, v in self.candidates.items():
                    label = v.get("label_properties", "")
                    if len(label) > 0 and isinstance(label, list):
                        label = label[0]
                    description = v.get("description_properties", "")
                    if len(description) > 0 and isinstance(description, list):
                        description = description[0]
                    self.metadata.append("{}\t\t{}\t{}".format(k, label, description))
            else:
                required_properties = output_properties["metatada_properties"]
                self.metadata.append("node\t" + "\t".join(required_properties))
                for k, v in self.candidates.items():
                    each_metadata = k + "\t"
                    for each in required_properties:
                        each_metadata += v.get(each, " ") + "\t"
                    self.metadata.append(each_metadata)

        metadata_output_path = os.path.join(output_uri, self.vector_dump_file.split("/")[-1])
        if run_TSNE:
            self.print_vector(self.vectors_2D, output_properties.get("output_properties"), output_format)
        else:
            self.print_vector(vectors, output_properties.get("output_properties"), output_format)
        if output_uri != "none":
            self.dump_vectors(metadata_output_path, "metadata")

    def evaluate_result(self):
        """
            for the ground truth nodes, evaluate the average distance to the centroid, the lower the average distance, the better clustering results should be
        """
        import numpy as np
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
        self._logger.info("The average distance for the ground truth nodes to centroid is {}".format(distance_sum / len(points)))

    @staticmethod
    def calculate_distance(a, b):
        if len(a) != len(b):
            raise KGTKException("Vector dimension are different!")
        dist = 0
        for v1, v2 in zip(a, b):
            dist += (v1 - v2) ** 2
        dist = dist ** 0.5
        return dist


def load_property_labels_file(input_files: typing.List[str]):
    labels_dict = {}
    headers = None
    for each_file in input_files:
        with open(each_file, "r") as f:
            for each_line in f.readlines():
                each_line = each_line.replace("\n", "").split("\t")
                if headers is None:
                    headers = each_line
                    if len(headers) < 2:
                        raise KGTKException(
                            "No enough columns found on given input file. Only {} columns given but at least 2 needed.".format(
                                len(headers)))
                    elif "predicate" in headers and "label" in headers:
                        column_references = {"predicate": headers.index("predicate"),
                                             "label": headers.index("label")}
                    elif "label" in headers:
                        column_references = {"predicate": 0,
                                             "label": headers.index("label"),
                                             }
                    else:
                        raise KGTKException("Can't determine which column is label column for label file!")

                else:
                    node_id = each_line[column_references["predicate"]]
                    node_label = each_line[column_references["label"]]
                    if "@en" in node_label:
                        node_label = node_label.replace("'", "").split("@")[0]
                        labels_dict[node_id] = node_label
                    if node_id not in labels_dict:
                        labels_dict[node_id] = node_label
    return labels_dict


def load_black_list_files(file_path):
    import tarfile
    import zipfile
    import gzip
    import logging
    import re
    import numpy as np
    token_pattern = re.compile(r"(?u)\b\w\w+\b")
    qnodes_set = set()
    _logger = logging.getLogger(__name__)
    for each_file in file_path:
        try:
            # tar.gz file
            if each_file.endswith("tar.gz"):
                tar = tarfile.open("filename.tar.gz", "r:gz")
                for member in tar.getmembers():
                    f = tar.extractfile(member)
                    if f:
                        content = f.read()
                        input_data = np.loadtxt(content)
            # gz file
            elif each_file.endswith(".gz"):
                with gzip.open('big_file.txt.gz', 'rb') as f:
                    input_data = f.readlines()
            # zip file
            elif each_file.endswith(".zip"):
                archive = zipfile.ZipFile(each_file, 'r')
                input_data = archive.read(each_file.replace(".zip", "")).decode().split("\n")
            # other file, just read directly
            else:
                with open(each_file, "r") as f:
                    input_data = f.readlines()

            for each in input_data:
                each = each.replace("\n", "")
                for each_part in token_pattern.findall(each):
                    if each_part[0] == "Q" and each_part[1:].isnumeric():
                        qnodes_set.add(each_part)
        except Exception as e:
            _logger.error("Load black list file {} failed!".format(each_file))
            _logger.debug(e, exc_info=True)

    _logger.info("Totally {} black list nodes loadded.".format(len(qnodes_set)))
    return qnodes_set


def main(**kwargs):
    from kgtk.exceptions import KGTKException
    try:
        import logging
        import os
        import time
        from time import strftime
        import torch
        import typing
        import pandas as pd
        import string
        import math
        import re
        import argparse
        import pickle

        do_logging = kwargs.get("_debug", False)
        if do_logging:
            logging_level_class = logging.DEBUG
            logger_path = os.path.join(os.environ.get("HOME"),
                                       "kgtk_text_embedding_log_{}.log".format(strftime("%Y-%m-%d-%H-%M")))
            logging.basicConfig(level=logging_level_class,
                                format="%(asctime)s [%(levelname)s] %(name)s %(lineno)d -- %(message)s",
                                datefmt='%m-%d %H:%M:%S',
                                filename=logger_path,
                                filemode='w')

        _logger = logging.getLogger(__name__)
        _logger.warning("Running with logging level {}".format(_logger.getEffectiveLevel()))

        # get input parameters from kwargs
        output_uri = kwargs.get("output_uri", "")
        black_list_files = kwargs.get("black_list_files", "")
        all_models_names = kwargs.get("all_models_names", ['bert-base-wikipedia-sections-mean-tokens'])
        input_format = kwargs.get("input_format", "kgtk_format")
        input_uris = kwargs.get("input_uris", [])
        output_format = kwargs.get("output_format", "kgtk_format")
        property_labels_files = kwargs.get("property_labels_file_uri", "")
        query_server = kwargs.get("query_server")
        properties = dict()
        all_property_relate_inputs = [kwargs.get("label_properties", ["label"]),
                                      kwargs.get("description_properties", ["description"]),
                                      kwargs.get("isa_properties", ["P31"]),
                                      kwargs.get("has_properties", ["all"]),
                                      ]
        all_required_properties = ["label_properties", "description_properties",
                                   "isa_properties", "has_properties"]
        cache_config = {"use_cache": kwargs.get("use_cache", False),
                        "host": kwargs.get("cache_host", "dsbox01.isi.edu"),
                        "port": kwargs.get("cache_port", 6379)
                        }
        for each_property, each_input in zip(all_required_properties, all_property_relate_inputs):
            for each in each_input:
                properties[each] = each_property

        output_properties = {
            "metatada_properties": kwargs.get("metatada_properties", []),
            "output_properties": kwargs.get("output_properties", "text_embedding")
        }

        if isinstance(all_models_names, str):
            all_models_names = [all_models_names]
        if isinstance(input_uris, str):
            input_uris = [input_uris]
        if len(all_models_names) == 0:
            raise KGTKException("No embedding vector model name given!")
        if len(input_uris) == 0:
            raise KGTKException("No input file path given!")

        if output_uri == "":
            output_uri = os.getenv("HOME")  # os.getcwd()
        if black_list_files != "":
            black_list_set = load_black_list_files(black_list_files)
        else:
            black_list_set = set()
        if property_labels_files:
            property_labels_dict = load_property_labels_file(property_labels_files)
            _logger.info("Totally {} property labels loaded.".format(len(property_labels_dict)))
        else:
            property_labels_dict = {}

        run_TSNE = kwargs.get("run_TSNE", True)

        for each_model_name in all_models_names:
            for each_input_file in input_uris:
                _logger.info("Running {} model on {}".format(each_model_name, each_input_file))
                process = EmbeddingVector(each_model_name, query_server=query_server, cache_config=cache_config)
                process.read_input(file_path=each_input_file, skip_nodes_set=black_list_set,
                                   input_format=input_format, target_properties=properties,
                                   property_labels_dict=property_labels_dict)
                process.get_vetors()
                process.plot_result(output_properties=output_properties,
                                    input_format=input_format, output_uri=output_uri,
                                    run_TSNE=run_TSNE, output_format=output_format)
                process.evaluate_result()
                _logger.info("*" * 20 + "finished" + "*" * 20)
    except Exception as e:
        _logger.debug(e, exc_info=True)
        raise KGTKException(str(e))


def parser():
    return {
        'help': """Produce embedding vectors on given file's nodes."""
    }


def add_arguments(parser):
    import argparse
    def str2bool(v):
        if isinstance(v, bool):
            return v
        if v.lower() in ('yes', 'true', 't', 'y', '1'):
            return True
        elif v.lower() in ('no', 'false', 'f', 'n', '0'):
            return False
        else:
            raise argparse.ArgumentTypeError('Boolean value expected.')

    parser.accept_shared_argument('_debug')
    # logging level, no longer need as there is a global --debug choice for it
    # parser.add_argument('-l', '--logging-level', action='store', dest='logging_level',
    #         default="info", choices=("error", "warning", "info", "debug", "none"),
    #         help="set up the logging level, default is INFO level")
    # parser.add_argument('--debug', dest='_debug', action='store_true', default=False, help='enable debug mode')

    # model name
    all_models_names = ALL_EMBEDDING_MODELS_NAMES
    parser.add_argument('-m', '--model', action='store', nargs='+', dest='all_models_names',
                        default="bert-base-wikipedia-sections-mean-tokens", choices=all_models_names,
                        help="the model to used for embedding")
    # input file
    parser.add_argument('-i', '--input', action='store', nargs='+', dest='input_uris',
                        help="input path", )
    parser.add_argument('-f', '--input-format', action='store', dest='input_format',
                        choices=("test_format", "kgtk_format"), default="kgtk_format",
                        help="the input file format, could either be `test_format` or `kgtk_format`, default is `kgtk_format`", )
    parser.add_argument('-p', '--property-labels-file', action='store', nargs='+',
                        dest='property_labels_file_uri', help="the path to the property labels file.", )
    # properties (only valid for kgtk format input/output data)
    parser.add_argument('--label-properties', action='store', nargs='+',
                        dest='label_properties', default=["label"],
                        help="""The names of the eges for label properties, Default is ["label"]. \n 
                        This argument is only valid for input in kgtk format.""")
    parser.add_argument('--description-properties', action='store', nargs='+',
                        dest='description_properties', default=["description"],
                        help="""The names of the eges for description properties, Default is ["description"].\n 
                        This argument is only valid for input in kgtk format.""")
    parser.add_argument('--isa-properties', action='store', nargs='+',
                        dest='isa_properties', default=["P31"],
                        help="""The names of the eges for `isa` properties, Default is ["P31"] (the `instance of` node in wikidata).\n 
                        This argument is only valid for input in kgtk format.""")
    parser.add_argument('--has-properties', action='store', nargs='+',
                        dest='has_properties', default=["all"],
                        help="""The names of the eges for `has` properties, Default is ["all"] (will automatically append all properties found for each node).\n This argument is only valid for input in kgtk format.""")
    parser.add_argument('--output-property', action='store',
                        dest='output_properties', default="text_embedding",
                        help="""The output property name used to record the embedding. Default is `output_properties`. \nThis argument is only valid for output in kgtk format.""")
    # output
    parser.add_argument('-o', '--embedding-projector-metadata-path', action='store', dest='output_uri', default="",
                        help="output path for the metadata file, default will be current user's home directory")
    parser.add_argument('--output-format', action='store', dest='output_format',
                        default="kgtk", choices=("tsv_format", "kgtk_format"),
                        help="output format, can either be `tsv_format` or `kgtk_format`. \nIf choose `tsv_format`, the output will be a tsv file, with each row contains only the vector representation of a node. Each dimension is separated by a tab")
    parser.add_argument('--embedding-projector-metatada', action='store', nargs='+',
                        dest='metatada_properties', default=[],
                        help="""list of properties used to construct a metadata file for use in the Google Embedding Projector: http://projector.tensorflow.org. \n Default: the label and description of each node.""")
    # black list file
    parser.add_argument('-b', '--black-list', nargs='+', action='store', dest='black_list_files',
                        default="",
                        help="the black list file, contains the Q nodes which should not consider as candidates.")
    # run tsne or not
    parser.add_argument("--run-TSNE", type=str2bool, nargs='?', action='store',
                        default=True, dest="run_TSNE",
                        help="whether to run TSNE or not after the embedding, default is true.")
    # cache config
    parser.add_argument("--use-cache", type=str2bool, nargs='?', action='store',
                        default=False, dest="use_cache",
                        help="whether to use cache to get some embedding vectors quicker, default is False")
    parser.add_argument("--cache-host", nargs='?', action='store',
                        default="dsbox01.isi.edu", dest="cache_host",
                        help="cache host address, default is `dsbox01.isi.edu`"
                        )
    parser.add_argument("--cache-port", nargs='?', action='store',
                        default="6379", dest="cache_port",
                        help="cache server port, default is `6379`"
                        )
    # query server
    parser.add_argument("--query-server", nargs='?', action='store',
                        default="", dest="query_server",
                        help="sparql query endpoint used for test_format input files, default is https://query.wikidata.org/sparql"
                        )


def run(**kwargs):
    main(**kwargs)
