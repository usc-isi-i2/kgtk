
# labels:

#     "P1855": {
#       "type": "property",
#       "datatype": "wikibase-item",
#       "id": "P1855",
#       "labels": {
#         "en": { "language": "en", "value": "Wikidata property example" }
#       }
#     },

#     "Q20898239": {
#       "type": "item",
#       "id": "Q20898239",
#       "labels": {
#         "en": {
#           "language": "en",
#           "value": "The Hitch Hiker's Guide to the Galaxy (1979 edition)"
#         }
#       }
#     },

# info:

#     "Q42": {
#       "pageid": 138,
#       "ns": 0,
#       "title": "Q42",
#       "lastrevid": 1175340593,
#       "modified": "2020-05-06T19:28:31Z",
#       "type": "item",
#       "id": "Q42"
#     }

#     "P31": {
#       "pageid": 3918489,
#       "ns": 120,
#       "title": "Property:P31",
#       "lastrevid": 1179261400,
#       "modified": "2020-05-11T22:37:17Z",
#       "type": "property",
#       "datatype": "wikibase-item",
#       "id": "P31"
#     }

# misc:

#     "Q42": {
#         "pageid": 138,
#         "ns": 0,
#         "title": "Q42",
#         "lastrevid": 1175340593,
#         "modified": "2020-05-06T19:28:31Z",
#         "type": "item",
#         "id": "Q42",
#         "labels": { "en": { "language": "en", "value": "Douglas Adams" } },
#         "descriptions:{},
#         "aliases":{},
#         "claims":{},
#         "sitelinks:{}
#       }








import sys
import re
import json
from kgtk.exceptions import KGTKException

BAD_CHARS = [":", "-", "&", ",", " ",
             "(", ")", "\'", '\"', "/", "\\", "[", "]", ";", "|"]

class JsonGenerator:
    """
    A class to maintain the status of the generator
    """

    def __init__(
            self,
            prop_file: str,
            label_set: str,
            alias_set: str,
            description_set: str,
            use_gz:bool,
            # output_prefix:str="",
            n:int,
    ):
        # indexing files
        self.file_num = 0
        self.output_prefix = "kgtk"
        # current output files
        self.set_json_file_names()
        # curret dictionaries
        self.set_json_dict()
        # TODO no qualifiers or references for version 1
        self.e_ids = set()
        self.set_properties(prop_file)
        self.set_sets(label_set, alias_set, description_set)
        self.order_map = {}
    
    def entry_point(self,line_number, edge):
        # TODO
        # first version only handles statement, not qualifiers

        # serialization
        edge_list = edge.strip().split("\t")
        l = len(edge_list)
        if line_number == 1:
            # initialize the order_map
            edge_list = edge.strip().split("\t")
            node1_index = edge_list.index("node1")
            node2_index = edge_list.index("node2")
            prop_index = edge_list.index("property")
            id_index = edge_list.index("id")
            if not all([node1_index > -1, node2_index > -1, prop_index > -1, id_index > -1]):
                raise KGTKException(
                    "Header of kgtk file misses at least one of required column names: (node1, node2, property and id)")
            else:
                self.order_map["node1"] = node1_index
                self.order_map["node2"] = node2_index
                self.order_map["prop"] = prop_index
                self.order_map["id"] = id_index
                return
        
        node1 = edge_list[self.order_map["node1"]].strip()
        node2 = edge_list[self.order_map["node2"]].strip()
        prop = edge_list[self.order_map["prop"]].strip()
        e_id = edge_list[self.order_map["id"]].strip()
        self.e_ids.add(e_id)
        if node1 in self.e_ids:
            return #TODO not handling qualifiers        
        # update label_json_dict
        if prop in self.label_set:
            self.update_label_json_dict(node1, prop, node2)

        # update info_json_dict
        if node1 in self.prop_types:
            self.update_info_json_dict(node1, self.prop_types[node1])
        else:
            self.update_info_json_dict(node1, None)
        
        if prop in self.prop_types:
            self.update_info_json_dict(prop,self.prop_types[prop])
            if self.prop_types[prop] == "wikibase-item":
                self.update_info_json_dict(node2)
        
        # update alias and descriptions
        if prop in self.description_set:
            self.update_misc_json_dict(node1, prop, node2, "descriptions")
        if prop in self.alias_set:
            self.update_misc_json_dict(node1, prop, node2, "aliases")
        
        # normal update for claims


    def update_info_json_dict(self, node:str,data_type = None):
        # if node in self.info_json_dict:
        #     return
        #TODO, not robust but no easy way to figure it out
        if node.startswith("Q"):
            self.info_json_dict[node] = {
                "pageid":-1,
                "ns":-1,
                "title":node,
                "lastrevid":"2000-01-01T00:00:00Z", #TODO
                "type":"item",
                "id":node}
        elif node.startswith("P"):
            self.info_json_dict[node] = {
                "pageid":-1,
                "ns":-1,
                "title":"Property:"+node,
                "lastrevid":"2000-01-01T00:00:00Z",
                "type":"property",
                "datatype":data_type,
                "id":node}
        else:
            raise KGTKException("node {} is neither an entity nor a property.".format(node))
    
    def update_misc_json_dict(self, node1:str, prop:str, node2:str, field:str):
        if node1 not in self.misc_json_dict:
            self.misc_json_dict[node1] = {**self.label_json_dict[node1], **self.info_json_dict[node1]}
            self.misc_json_dict[node1]["descriptions"] = {}
            self.misc_json_dict[node1]["aliases"] = {}
            self.misc_json_dict[node1]["claims"] = {}
            self.misc_json_dict[node1]["sitelinks"] = {}
        
        if field == "descriptions":
            description_text, lang = JsonGenerator.process_text_string(node2)
            temp_des_dict = {lang:{"languange":lang,"value":description_text}}
            self.misc_json_dict[node1]["descriptions"] = {**self.misc_json_dict[node1]["descriptions"], **temp_des_dict}
        if field == "aliases":
            alias_text, lang = JsonGenerator.process_text_string(node2)
            if lang in self.misc_json_dict[node1]["aliases"]:
                pass
        
        # update claims

 
    def update_label_json_dict(self,node1:str, prop:str, node2:str):
        # for label_dict
        if node1 not in self.prop_types:
            label_type = "item"
            self.label_json_dict[node1] = {
            "type":label_type
            }
        else:
            label_type = "property"
            label_datatype = self.prop_types[node1]
            self.label_json_dict[node1] = {
            "type":label_type,
            "datatype":label_datatype,
            }
        self.label_json_dict[node1]["id"] = node1
        self.label_json_dict[node1]["labels"] = {}
        text_string, lang = JsonGenerator.process_text_string(node2)
        self.label_json_dict[node1]["labels"][lang] = {"language":lang, "value": text_string}


    def set_sets(self, label_set: str, alias_set: str, description_set: str):
        self.label_set, self.alias_set, self.description_set = set(label_set.split(",")), set(alias_set.split(",")), set(description_set.split(","))

    def set_properties(self, prop_file: str):
        datatype_mapping = {
            "item": "wikibase-item",
            "time": "time",
            "globe-coordinate": "globe-coordinate",
            "quantity": "quantity",
            "monolingualtext": "monolingualtext",
            "string": "string",
            "external-identifier": "external-id",
            "url": "url"
        }
        with open(prop_file, "r") as fp:
            props = fp.readlines()
        prop_types = {}
        for line in props[1:]:
            node1, _, node2 = line.split("\t")
            try:
                prop_types[node1] = datatype_mapping[node2.strip()]
            except:
                if not self.ignore:
                    raise KGTKException(
                        "DataType {} of node {} is not supported.\n".format(
                            node2, node1
                        )
                    )
        self.prop_types = prop_types

    def serialize(self):
        '''
        serialize the dictionaries to the file pointer
        '''
        with open(self.label_json_file,"w") as fp:
            json.dump(self.label_json_dict,fp)

        with open(self.misc_json_file,"w") as fp:
            json.dump(self.misc_json_dict,fp)
        
        with open(self.info_json_file,"w") as fp:
            json.dump(self.info_json_dict,fp)
        
        # update dict and files
        self.set_json_file_names()
        self.set_json_dict()

    def finalize(self):
        # finalize the generator
        self.serialize()
        return

    def set_json_dict(self):
        self.label_json_dict = {}
        self.misc_json_dict = {}
        self.info_json_dict = {}
    
    def set_json_file_names(self):
        self.file_num += 1
        prefix = self.output_prefix + "_" + str(self.file_num) + "_"
        self.label_json_file =  prefix + "labels.json"
        self.misc_json_file = prefix + "misc.json"
        self.info_json_file = prefix + "info.json"

    @staticmethod
    def process_text_string(string: str) -> [str, str]:
        ''' 
        Language detection is removed from triple generation. The user is responsible for detect the language
        '''
        if len(string) == 0:
            return ["", "en"]
        if "@" in string:
            res = string.split("@")
            text_string = "@".join(res[:-1]).replace('"', "").replace("'", "")
            lang = res[-1].replace('"', '').replace("'", "")
            if len(lang) > 2:
                lang = "en"
        else:
            text_string = string.replace('"', "").replace("'", "")
            lang = "en"
        return [text_string, lang]