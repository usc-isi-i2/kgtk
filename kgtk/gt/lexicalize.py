import typing
import logging
from kgtk.exceptions import KGTKException
from collections import defaultdict
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
from kgtk.kgtkformat import KgtkFormat


class Lexicalize:
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self.node_labels = dict()  # this is used to store {node:label} pairs
        self.candidates = defaultdict(dict)  # this is used to store all node {node:dict()} information

    def read_input(self,
                   kr: KgtkReader,
                   target_properties: dict,
                   property_labels_dict: dict,
                   ):
        """
            load the input candidates files
        """
        self.node_labels.update(property_labels_dict)
        # reverse sentence property to be {property : role)
        properties_reversed = defaultdict(set)

        current_process_node_id = None
        node_id = None

        for k, v in target_properties.items():
            for each_property in v:
                properties_reversed[each_property].add(k)

        # assume the input edge file is sorted
        if "all" in properties_reversed:
            _ = properties_reversed.pop("all")
            add_all_properties = True
        else:
            add_all_properties = False

        # read contents
        # This type union becomes painful to work with, below.
        each_node_attributes: typing.Mapping[str, typing.Union[typing.List, typing.Set]] = {
            "has_properties": set(),
            "isa_properties": set(),
            "label_properties": [],
            "description_properties": [],
            "has_properties_values": [],
        }

        row: typing.List[str]
        for row in kr:
            node_id = row[kr.node1_column_idx]

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
                                                                                       node_id)

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

        # case where there was a single qnode in the input file
        unprocessed_qnode = False
        if each_node_attributes:
            for k in each_node_attributes:
                if each_node_attributes[k]:
                    unprocessed_qnode = True
                    break
        if unprocessed_qnode:
            a, b = self.process_qnode(current_process_node_id, each_node_attributes, node_id)
        self._logger.info("Totally {} Q nodes loaded.".format(len(self.candidates)))

    def process_qnode(self, current_process_node_id, each_node_attributes, node_id):
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

