from collections import defaultdict
import logging
from pathlib import Path
import typing

from kgtk.exceptions import KGTKException
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
from kgtk.io.kgtkwriter import KgtkWriter
from kgtk.kgtkformat import KgtkFormat
from kgtk.value.kgtkvalueoptions import KgtkValueOptions

class Lexicalize:
    def __init__(self,
                 label_properties: typing.List[str],
                 description_properties: typing.List[str],
                 isa_properties: typing.List[str],
                 has_properties: typing.List[str],
                 property_values: typing.List[str],
                 sentence_label: str,
                 ):
        self.sentence_label: str = sentence_label
        self.label_properties: typing.List[str] = label_properties
        self.description_properties: typing.List[str] = description_properties
        self.isa_properties: typing.List[str] = isa_properties
        self. has_properties: typing.List[str] = has_properties
        self.property_values: typing.List[str] = property_values

        self._logger = logging.getLogger(__name__)
        self.node_labels: typing.MutableMapping[str, str] = dict()  # this is used to store {node:label} pairs

        self.properties_reversed = self.reverse_properties()

        # assume the input edge file is sorted
        self.add_all_properties: bool = self.get_add_all_properties()


    ATTRIBUTE_TYPES = typing.Union[typing.List, typing.Set]
    EACH_NODE_ATTRIBUTES = typing.MutableMapping[str, ATTRIBUTE_TYPES]

    def new_each_node_attributes(self)->EACH_NODE_ATTRIBUTES:
        return {
            "has_properties": set(),
            "isa_properties": set(),
            "label_properties": [],
            "description_properties": [],
            "has_properties_values": [],
        }

    def add_entity_label(self, node_id: str, node_label: str):
        text: str
        language: str
        language_suffix: str
        if node_label.startswith(("'", '"')):
            text, language, language_suffix = KgtkFormat.destringify(node_label)
        else:
            text = node_label
            language = ""
            language_suffix = ""

        # The following code will take the last-read English label,
        # otherwise, the first-read non-English label.
        if language == "en" and language_suffix == "":
            if node_id in self.node_labels:
                self.english_labels_reloaded += 1
            else:
                self.english_labels_loaded += 1
            self.node_labels[node_id] = text
        else:
            if node_id not in self.node_labels:
                self.node_labels[node_id] = node_label
                self.non_english_labels_loaded += 1
            else:
                self.non_english_labels_ignored += 1


    def add_entity_if_label(self,
                            node_id: str,
                            relationship: str,
                            node_label: str,
                            label_properties: typing.List[str],
                            )->bool:
        if len(label_properties) > 0:
            if relationship not in label_properties:
                return False

        self.add_entity_label(node_id, node_label)
        return True


    def load_entity_label_file(self,
                               entity_label_file: Path,
                               error_file: typing.TextIO,
                               reader_options: KgtkReaderOptions,
                               value_options: KgtkValueOptions,
                               label_properties: typing.List[str],
                               verbose: bool = False,
                               ):
        """Load entity labels before processing the input file."""
        kr: KgtkReader = KgtkReader.open(entity_label_file,
                                         error_file=error_file,
                                         options=reader_options,
                                         value_options=value_options,
                                         verbose=verbose,
                                         )
        self.english_labels_loaded: int = 0
        self.english_labels_reloaded: int = 0
        self.non_english_labels_loaded: int = 0
        self.non_english_labels_ignored: int = 0
        try:
            fail: bool = False
            if kr.node1_column_idx < 0:
                fail = True
                print("Cannot determine which column is node1 in %s" % repr(str(entity_label_file)), file=error_file, flush=True)
            if len(label_properties) > 0 and kr.label_column_idx < 0:
                fail = True
                print("Cannot determine which column is label in %s" % repr(str(entity_label_file)), file=error_file, flush=True)
            if kr.node2_column_idx < 0:
                fail = True
                print("Cannot determine which column is node2 in %s" % repr(str(entity_label_file)), file=error_file, flush=True)
            if fail:
                raise KGTKException("Cannot identify a required column in %s" % repr(str(entity_label_file)))
    
            row: typing.List[str]
            for row in kr:
                self.add_entity_if_label(row[kr.node1_column_idx],
                                         row[kr.label_column_idx],
                                         row[kr.node2_column_idx],
                                         label_properties
                                         )


        finally:
            kr.close()
            if verbose:
                print("%d English labels loaded, %d reloaded, %d non-English labels loaded, %d ignored from %s" % (self.english_labels_loaded,
                                                                                                                   self.english_labels_reloaded,
                                                                                                                   self.non_english_labels_loaded,
                                                                                                                   self.non_english_labels_ignored,
                                                                                                                   repr(str(entity_label_file))),
                      file=error_file, flush=True)

    def load_entity_label_files(self,
                                entity_label_files: typing.List[Path],
                                error_file: typing.TextIO,
                                reader_options: KgtkReaderOptions,
                                value_options: KgtkValueOptions,
                                label_properties: typing.List[str],
                                verbose: bool = False,
                                ):
        entity_label_file: Path
        for entity_label_file in entity_label_files:
            self.load_entity_label_file(entity_label_file=entity_label_file,
                                        error_file=error_file,
                                        reader_options=reader_options,
                                        value_options=value_options,
                                        label_properties=label_properties,
                                        verbose=verbose)

    def reverse_properties(self):
        # reverse sentence property to be {property : role)
        target_properties = {
            "label_properties": self.label_properties,
            "description_properties": self.description_properties,
            "isa_properties": self.isa_properties,
            "has_properties": self.has_properties,
            "property_values": self.property_values,
        }

        properties_reversed = defaultdict(set)
        for k, v in target_properties.items():
            for each_property in v:
                properties_reversed[each_property].add(k)

        return properties_reversed

    def get_add_all_properties(self)->bool:
        # assume the input edge file is sorted
        if "all" in self.properties_reversed:
            _ = self.properties_reversed.pop("all")
            return True
        else:
            return False
        
                           

    def process_row(self,
                    kw: KgtkWriter,
                    node_id: str,
                    node_property: str,
                    node_value: str,
                    current_process_node_id: typing.Optional[str],
                    each_node_attributes: EACH_NODE_ATTRIBUTES,
                    ):
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
            return

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
                current_process_node_id, each_node_attributes = self.process_qnode(kw,
                                                                                   current_process_node_id,
                                                                                   each_node_attributes,
                                                                                   node_id)

        if node_property in self.properties_reversed:
            roles = self.properties_reversed[node_property].copy()
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
                attrs: Lexicalize.ATTRIBUTE_TYPES = each_node_attributes[each_role]
                if isinstance(attrs, set):
                    attrs.add(node_value)
                elif isinstance(attrs, list):
                    attrs.append(node_value)
                else:
                    raise ValueError('each_node_attributes[%s] is not a list or set.' % repr(each_role))

        elif self.add_all_properties:  # add remained properties if need all properties
            attrs2: Lexicalize.ATTRIBUTE_TYPES = each_node_attributes["has_properties"]
            if isinstance(attrs2, list):
                attrs2.append(self.get_real_label_name(node_property))
            else:
                raise ValueError('each_node_attributes["has_properties"] is not a list.')

        return current_process_node_id, each_node_attributes

    def process_input(self,
                      kr: KgtkReader,
                      kw: KgtkWriter,
                      ):
        """The input file must be sorted by node1."""

        # read contents
        # This type union becomes painful to work with, below.
        each_node_attributes: Lexicalize.EACH_NODE_ATTRIBUTES = self.new_each_node_attributes()

        previous_node_id: typing.Optional[str] = None
        current_process_node_id: typing.Optional[str] = None
        node_id: typing.Optional[str] = None

        rownum: int
        row: typing.List[str]
        for rownum, row in enumerate(kr):
            node_id = row[kr.node1_column_idx]
            node_property: str = row[kr.label_column_idx]
            node_value: str = row[kr.node2_column_idx]

            # Ensure that the input file is sorted (node1 lowest to highest):
            if previous_node_id is not None and previous_node_id > node_id:
                raise KGTKException("Row %d is out of order: %s > %s" % (rownum + 1, previous_node_id, node_id))
            else:
                previous_node_id = node_id

            current_process_node_id, each_node_attributes = self.process_row(kw,
                                                                             node_id,
                                                                             node_property,
                                                                             node_value,
                                                                             current_process_node_id,
                                                                             each_node_attributes)

        if current_process_node_id is None:
            self._logger.info("current_processed_node_id is NONE, no data?")
            return

        if node_id is None:
            self._logger.info("node_id is NONE, no data?")
            return

        # Processing the final qnode in the input file
        unprocessed_qnode = False
        if each_node_attributes:
            for k in each_node_attributes:
                if each_node_attributes[k]:
                    unprocessed_qnode = True
                    break
        if unprocessed_qnode:
            a, b = self.process_qnode(kw, current_process_node_id, each_node_attributes, node_id)


    def process_qnode(self,
                      kw: KgtkWriter,
                      current_process_node_id: str,
                      each_node_attributes: EACH_NODE_ATTRIBUTES,
                      node_id: str):
        concat_sentence: str = self.attribute_to_sentence(each_node_attributes, current_process_node_id)
        kw.write([ current_process_node_id, self.sentence_label, KgtkFormat.stringify(concat_sentence)])

        # after write down finish, we can clear and start parsing next one
        each_node_attributes = self.new_each_node_attributes()
        # update to new id
        current_process_node_id = node_id
        return current_process_node_id, each_node_attributes

    def get_real_label_name(self, node: str)->str:
        if node in self.node_labels:
            return self.node_labels[node].replace('"', "") # Should use KgtkFormat.unstringify(node)
        else:
            return node

    def attribute_to_sentence(self, attribute_dict: EACH_NODE_ATTRIBUTES, node_id: str)->str:
        concated_sentence: str = ""
        have_isa_properties = False

        # sort the properties to ensure the sentence always same
        attribute_dict = {key: sorted(list(value)) for key, value in attribute_dict.items() if len(value) > 0}
        if "label_properties" in attribute_dict and isinstance(attribute_dict["label_properties"], list) and len(attribute_dict["label_properties"]) > 0:
            concated_sentence += self.get_real_label_name(attribute_dict["label_properties"][0])
        if "description_properties" in attribute_dict and isinstance(attribute_dict["description_properties"], list) and len(attribute_dict["description_properties"]) > 0:
            if concated_sentence != "" and attribute_dict["description_properties"][0] != "":
                concated_sentence += ", "
            concated_sentence += self.get_real_label_name(attribute_dict["description_properties"][0])
        if "isa_properties" in attribute_dict and isinstance(attribute_dict["isa_properties"], set) and len(attribute_dict["isa_properties"]) > 0:
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

