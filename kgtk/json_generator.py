
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
from time import sleep
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
        self.quantity_pattern = re.compile(
            "([\+|\-]?[0-9]+\.?[0-9]*[e|E]?[\-]?[0-9]*)(?:\[([\+|\-]?[0-9]+\.?[0-9]*),([\+|\-]?[0-9]+\.?[0-9]*)\])?([U|Q](?:[0-9]+))?")
        self.yyyy_mm_dd_pattern = re.compile(
            "[12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])")
        self.yyyy_pattern = re.compile("[12]\d{3}")
    
    def entry_point(self,line_number, edge):
        # TODO
        # first version only handles statement, not qualifiers

        # serialization
        edge_list = edge.strip("\n").split("\t")
        l = len(edge_list)
        if line_number == 1:
            # initialize the order_map
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

        # update info_json_dict
        if node1 in self.prop_types:
            self.update_info_json_dict(node1, self.prop_types[node1])
        else:
            self.update_info_json_dict(node1, None)
        
        if prop in self.prop_types:
            self.update_info_json_dict(prop,self.prop_types[prop])
            if self.prop_types[prop] == "wikibase-item":
                self.update_info_json_dict(node2)
        
        # update label_json_dict
        if prop in self.label_set:
            self.update_label_json_dict(node1, prop, node2)
            return
        else :
            # update with empty label
            if node1 not in self.label_json_dict:
                self.update_label_json_dict(node1, prop, None)
        
        # update alias and descriptions
        if prop in self.description_set:
            self.update_misc_json_dict(node1, prop, node2, line_number,"descriptions")
            return

        if prop in self.alias_set:
            self.update_misc_json_dict(node1, prop, node2, line_number,"aliases")
            return
        
        # normal update for claims
        self.update_misc_json_dict(node1,prop,node2,line_number,None)
        return

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
        if node2 != None:
            text_string, lang = JsonGenerator.process_text_string(node2)
            self.label_json_dict[node1]["labels"][lang] = {"language":lang, "value": text_string}
        return

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
    def update_misc_json_dict(self, node1:str, prop:str, node2:str, line_number:int, field:str):
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
            return 
        
        if field == "aliases":
            alias_text, lang = JsonGenerator.process_text_string(node2)
            temp_alias_dict = {lang, {"languange": lang, "value":alias_text}}
            if lang in self.misc_json_dict[node1]["aliases"]:
                self.misc_json_dict[node1]["aliases"][lang].append(temp_alias_dict)
            else:
                self.misc_json_dict[node1]["aliases"][lang] = [temp_alias_dict]
            return

        assert(field==None) #TODO better handling

        if prop not in self.prop_types:
            raise KGTKException("property {} at line {} is not defined.".format(prop,line_number))
        
        if prop not in self.misc_json_dict[node1]["claims"]:
                self.misc_json_dict[node1]["claims"][prop] = []
        try:
            if self.prop_types[prop] == "wikibase-item":
                self.update_misc_json_dict_item(node1,prop,node2)
            elif self.prop_types[prop] == "time":
                self.update_misc_json_dict_time(node1,prop,node2)
            elif self.prop_types[prop] == "globe-coordinate":
                self.update_misc_json_dict_coordinate(node1,prop,node2)
            elif self.prop_types[prop] == "quantity":
                self.update_misc_json_dict_quantity(node1,prop,node2)
            elif self.prop_types[prop] == "monolingualtext":
                self.update_misc_json_dict_monolingualtext(node1,prop,node2)
            elif self.prop_types[prop] == "string":
                self.update_misc_json_dict_string(node1,prop,node2)
            elif self.prop_types[prop] == "external-id":
                self.update_misc_json_dict_external_id(node1,prop,node2)
            elif self.prop_types[prop] == "url":
                self.update_misc_json_dict_url(node1,prop,node2)
            else:
                raise KGTKException("property tyepe {} of property {} at line {} is not defined.".format(self.prop_types[prop],prop,line_number))
        except:
            raise KGTKException("illegal edge at line {}.".format(line_number))
    def update_misc_json_dict_item(self,node1:str,prop:str,node2:str):
        temp_item_dict = {
                "mainsnak":{
                    "snaktype":"value",
                    "property":prop,
                    "hash":"hashplaceholder",
                    "datavalue":{
                        "value":{
                            "entity-type":"item","numeric-id":0,"id":node2 # place holder for numeric id
                        },
                        "type":"wikibase-entityid"
                    },
                    "datatype":"wikibase-item"
                },
                "type":"statement",
                "id":"id-place-holder",
                "rank":"normal", #TODO
                "references":[],
                "qualifiers":{}
            }
        self.misc_json_dict[node1]["claims"][prop].append(temp_item_dict)
        return
    def update_misc_json_dict_time(self,node1,prop,node2):
        if self.yyyy_pattern.match(node2):
            time_string = node2 + "-01-01"
            precision = 9
        elif self.yyyy_mm_dd_pattern.match(node2):
            time_string = node2
            precision = 11
        try:
            time_string, precision = node2.split("/")
            precision = int(precision)
        except:
            return # ignore the illegal time format for now
        temp_time_dict = {
            "mainsnak":{
                "snaktype":"value",
                "property":prop,
                "hash":"hashplaceholder",
                "datavalue":{
                    "value":{
                        "time":time_string,
                        "timezone": 0,
                        "before": 0,
                        "after": 0,
                        "precision": precision,
                        "calendarmodel": "http://www.wikidata.org/entity/Q1985727"    
                    },
                    "type":"time"
                },
                "datatype":"time"
            },
            "type":"statement",
            "id":"id-place-holder",
            "rank":"normal", #TODO
            "references":[],
            "qualifiers":{}
            }
        self.misc_json_dict[node1]["claims"][prop].append(temp_time_dict)          
        return
    def update_misc_json_dict_coordinate(self,node1,prop,node2):
        latitude, longitude = node2[1:].split("/")
        latitude = float(latitude)
        longitude = float(longitude)
        temp_coordinate_dict = {
            "mainsnak":{
                "snaktype":"value",
                "property":prop,
                "hash":"hashplaceholder",
                "datavalue":{
                    "value":{
                        "latitude":latitude,
                        "longitude": longitude,
                        "altitude": None,
                        "precision": 0.00027777777777778, # TODO
                        "globe": "http://www.wikidata.org/entity/Q2"    
                    },
                    "type":"globecoordinate"
                },
                "datatype":"globecoordinate"
            },
            "type":"statement",
            "id":"id-place-holder",
            "rank":"normal", #TODO
            "references":[],
            "qualifiers":{}
            }
        self.misc_json_dict[node1]["claims"][prop].append(temp_coordinate_dict)  
        return
    def update_misc_json_dict_quantity(self,node1,prop,node2):
        res = self.quantity_pattern.match(node2).groups()
        amount, lower_bound, upper_bound, unit = res
        amount = JsonGenerator.clean_number_string(amount)
        lower_bound = JsonGenerator.clean_number_string(lower_bound)
        upper_bound = JsonGenerator.clean_number_string(upper_bound)
        unit = "http://www.wikidata.org/entity/" + unit if unit != None else None
        temp_quantity_dict = {
            "mainsnak":{
                "snaktype":"value",
                "property":prop,
                "hash":"hashplaceholder",
                "datavalue":{
                    "value":{
                        "amount":amount,
                        "unit": unit,  
                        "lowerBound":lower_bound,
                        "UpperBound":upper_bound 
                    },
                    "type":"quantity"
                },
                "datatype":"quantity"
            },
            "type":"statement",
            "id":"id-place-holder",
            "rank":"normal", #TODO
            "references":[],
            "qualifiers":{}
            }
        self.misc_json_dict[node1]["claims"][prop].append(temp_quantity_dict)  
        return
    def update_misc_json_dict_monolingualtext(self,node1,prop,node2):
        text_string, lang = JsonGenerator.process_text_string(node2)
        temp_mono_dict ={
                "mainsnak":{
                    "snaktype":"value",
                    "property":prop,
                    "hash":"hashplaceholder",
                    "datavalue":{
                        "value":{
                            "text":text_string,
                            "language":lang
                        },
                        "type":"monolingualtext"
                    },
                    "datatype":"monolingualtext"
                },
                "type":"statement",
                "id":"id-place-holder",
                "rank":"normal", #TODO
                "references":[],
                "qualifiers":{}
                }
        self.misc_json_dict[node1]["claims"][prop].append(temp_mono_dict)  
        return
    def update_misc_json_dict_string(self,node1,prop,node2):
        string, lang = JsonGenerator.process_text_string(node2)
        temp_string_dict = {
            "mainsnak": {
              "snaktype": "value",
              "property": prop,
              "hash": "hashplaceholder",
              "datavalue": { "value": string, "type": "string" },
              "datatype": "string"
            },
            "type": "statement",
            "id": "id-place-holder",
            "rank": "normal",
            "references":[],
            "qualifiers":{}
            }
        self.misc_json_dict[node1]["claims"][prop].append(temp_string_dict)  
        return
    def update_misc_json_dict_external_id(self,node1,prop,node2):
        temp_e_id_dict = {"mainsnak": {
            "snaktype": "value",
            "property": prop,
            "hash": "hashplaceholder",
            "datavalue": { "value": node2, "type": "string" },
            "datatype": "external-id"
        },
        "type": "statement",
        "id": "id-place-holder",
        "rank": "normal",            
        "references":[],
        "qualifiers":{}}
        self.misc_json_dict[node1]["claims"][prop].append(temp_e_id_dict) 
        return
    def update_misc_json_dict_url(self,node1,prop,node2):
        temp_url_dict ={
        "mainsnak": {
            "snaktype": "value",
            "property": prop,
            "hash": "hashplaceholder",
            "datavalue": {
            "value": node2,
            "type": "string"
            },
            "datatype": "url"
        },
        "type": "statement",
        "id": "id-place-holder",
        "rank": "normal",            
        "references":[],
        "qualifiers":{}
        }
        self.misc_json_dict[node1]["claims"][prop].append(temp_url_dict) 
        return

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
    
    @staticmethod
    def clean_number_string(num):
        from numpy import format_float_positional
        if num == None:
            return None
        else:
            return format_float_positional(float(num), trim="-")