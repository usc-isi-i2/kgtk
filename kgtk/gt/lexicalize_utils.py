from collections import defaultdict
import logging
from pathlib import Path
import sys
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
                 error_file: typing.TextIO = sys.stderr,
                 verbose: bool = False,
                 very_verbose: bool = False,
                 ):
        self.sentence_label: str = sentence_label
        self.label_properties: typing.List[str] = label_properties
        self.description_properties: typing.List[str] = description_properties
        self.isa_properties: typing.List[str] = isa_properties
        self.has_properties: typing.List[str] = has_properties
        self.property_values: typing.List[str] = property_values

        self.error_file: typing.TextIO = error_file
        self.verbose: bool = verbose
        self.very_verbose: bool = very_verbose

        self._logger = logging.getLogger(__name__)
        self.node_labels: typing.MutableMapping[str, str] = dict()  # this is used to store {node:label} pairs

        self.properties_reversed = self.reverse_properties()

        # assume the input edge file is sorted
        self.add_all_properties: bool = self.get_add_all_properties()


    ATTRIBUTE_TYPES = typing.Union[typing.List, typing.Set]
    EACH_NODE_ATTRIBUTES = typing.MutableMapping[str, ATTRIBUTE_TYPES]

    HAS_PROPERTIES: str = "has_properties"
    ISA_PROPERTIES: str = "isa_properties"
    LABEL_PROPERTIES: str = "label_properties"
    DESCRIPTION_PROPERTIES: str = "description_properties"
    PROPERTY_VALUES: str = "property_values"

    def new_each_node_attributes(self)->EACH_NODE_ATTRIBUTES:
        return {
            self.HAS_PROPERTIES: set(),
            self.ISA_PROPERTIES: set(),
            self.LABEL_PROPERTIES: [],
            self.DESCRIPTION_PROPERTIES: [],
            self.PROPERTY_VALUES: [],
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
            self.HAS_PROPERTIES: set(self.has_properties),
            self.ISA_PROPERTIES: set(self.isa_properties),
            self.LABEL_PROPERTIES: self.label_properties,
            self.DESCRIPTION_PROPERTIES: self.description_properties,
            self.PROPERTY_VALUES: self.property_values,
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
        if self.very_verbose:
            print("Processing row (%s, %s, %s)" % (repr(node_id), repr(node_property), repr(node_value)), file=self.error_file, flush=True)

        # CMR: the following code looks like it was intended to remove
        # any language code and language suffix.  It would have the
        # side effect of removing location coordinates entirely.
        #
        # remove @ mark
        if "@" in node_value and node_value[0] != "@":
            node_value = node_value[:node_value.index("@")]

        # in case we meet an empty value, skip it
        if node_value == "":
            self._logger.warning("""Skip line ({}, {}, {}) because of empty value.""".format(node_id, node_property, node_value))
            return

        # CMR: Better to use KgtkFormat.unstringify(node_value), as it will remove escapes from
        # internal double or single quotes.
        #
        # remove extra double quote " and single quote '
        while len(node_value) >= 3 and node_value[0] == '"' and node_value[-1] == '"':
            node_value = node_value[1:-1]
        while len(node_value) >= 3 and node_value[0] == "'" and node_value[-1] == "'":
            node_value = node_value[1:-1]

        if self.very_verbose:
            print("Revised node_value = %s" % repr(node_value), file=self.error_file, flush=True)

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
            if self.very_verbose:
                print("node_property %s is in self.properties_reversed" % repr(node_property), file=self.error_file, flush=True)
            roles = self.properties_reversed[node_property].copy()
            node_value = self.get_real_label_name(node_value)
            if self.very_verbose:
                print("node_value label = %s" % repr(node_value), file=self.error_file, flush=True)
            # if we get property_values, it should be saved to isa-properties part
            if self.PROPERTY_VALUES in roles:
                if self.very_verbose:
                    print("property_values is in roles", file=self.error_file, flush=True)
                # for property values part, changed to be "{property} {value}"
                node_value_combine = self.get_real_label_name(node_property) + " " + self.get_real_label_name(node_value)
                if self.very_verbose:
                    print("node_value_combine = %s" % repr(node_value_combine), file=self.error_file, flush=True)
                if each_node_attributes is None:
                    raise ValueError("each_node_attributes is missing")

                property_values: typing.Optional[Lexicalize.ATTRIBUTE_TYPES] = each_node_attributes[self.PROPERTY_VALUES]
                if isinstance(property_values, list):
                    property_values.append(node_value_combine)
                else:
                    raise ValueError('each_node_attributes["property_values"] is not a list.')
                if self.very_verbose:
                    print('each_node_attributes["property_values"] = %s' % repr(property_values), file=self.error_file, flush=True)

                # remove those 2 roles in case we have duplicate using of this node later
                roles.discard(self.PROPERTY_VALUES)
                roles.discard(self.HAS_PROPERTIES)
            for each_role in roles:
                attrs: Lexicalize.ATTRIBUTE_TYPES = each_node_attributes[each_role]
                if isinstance(attrs, set):
                    attrs.add(node_value)
                elif isinstance(attrs, list):
                    attrs.append(node_value)
                else:
                    raise ValueError('each_node_attributes[%s] is not a list or set.' % repr(each_role))
                if self.very_verbose:
                    print("%s: %s" % (each_role, repr(attrs)), file=self.error_file, flush=True)

        elif self.add_all_properties:  # add remained properties if need all properties
            if self.very_verbose:
                print("self.add_all_properties is True", file=self.error_file, flush=True)
            attrs2: Lexicalize.ATTRIBUTE_TYPES = each_node_attributes[self.HAS_PROPERTIES]
            if isinstance(attrs2, list):
                attrs2.append(self.get_real_label_name(node_property))
                if self.very_verbose:
                    print("has_properties: %s" % repr(attrs2), file=self.error_file, flush=True)
            else:
                raise ValueError('each_node_attributes["has_properties"] is not a list.')

        return current_process_node_id, each_node_attributes

    def process_input(self, kr: KgtkReader, kw: KgtkWriter):
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

    def add_label_properties_to_sentence(self, attribute_dict: EACH_NODE_ATTRIBUTES, concated_sentence: str)->str:
        label_properties: typing.Optional[Lexicalize.ATTRIBUTE_TYPES]= attribute_dict.get(self.LABEL_PROPERTIES)
        if label_properties is not None and  isinstance(label_properties, list) and len(label_properties) > 0:
            label_properties = sorted(label_properties)
            if self.very_verbose:
                print('attribute_dict["label_properties"][0] = %s' % repr(label_properties[0]), file=self.error_file, flush=True)
            concated_sentence += self.get_real_label_name(label_properties[0])
            if self.very_verbose:
                print('concated_sentence = %s' % repr(concated_sentence), file=self.error_file, flush=True)
        return concated_sentence

    def add_description_properties_to_sentence(self, attribute_dict: EACH_NODE_ATTRIBUTES, concated_sentence: str)->str:
        description_properties: typing.Optional[Lexicalize.ATTRIBUTE_TYPES] = attribute_dict.get(self.DESCRIPTION_PROPERTIES)
        if description_properties is not None and isinstance(description_properties, list) and len(description_properties) > 0:
            description_property: str = sorted(description_properties)[0]
            if self.very_verbose:
                print('attribute_dict["description_properties"][0] = %s' % repr(description_property), file=self.error_file, flush=True)
            if len(description_property) > 0:
                description_label =  self.get_real_label_name(description_property)
                if len(concated_sentence) == 0:
                    concated_sentence = description_label
                elif description_label.startswith("(") and description_label.endswith(")"):
                    if not concated_sentence.endswith(" "):
                        concated_sentence += " "
                    concated_sentence += description_label
                else:
                    concated_sentence += ", " + description_label + ", "

            if self.very_verbose:
                print('concated_sentence = %s' % repr(concated_sentence), file=self.error_file, flush=True)
        return concated_sentence

    def add_isa_properties_to_sentence(self, attribute_dict: EACH_NODE_ATTRIBUTES, concated_sentence: str)->typing.Tuple[str, bool]:
        have_isa_properties: bool = False
        isa_properties: typing.Optional[Lexicalize.ATTRIBUTE_TYPES] = attribute_dict.get(self.ISA_PROPERTIES)
        if isa_properties is not None and isinstance(isa_properties, set) and len(isa_properties) > 0:
            if self.very_verbose:
                print('isa_properties is in attribute_dict', file=self.error_file, flush=True)
            have_isa_properties = True
            temp_str: str = ""
            isa_property_count: int = len(isa_properties)
            for idx, each in enumerate(sorted(isa_properties)):
                orig_each = each
                each = self.get_real_label_name(each)
                if self.very_verbose:
                    print("isa_property %s has label %s" % (repr(orig_each), repr(each)), file=self.error_file, flush=True)
                if "||" in each:
                    if "instance of" in each:
                        each = each.split("||")[1]
                    else:
                        each = each.replace("||", " ")
                if idx == 0:
                    if each.lower().startswith(("a", "e", "i", "o", "u")):
                        temp_str = "an " + each
                    else:
                        temp_str = "a " + each
                        
                elif idx + 1 == isa_property_count:
                    if isa_property_count == 2:
                        temp_str += " and " + each
                    else:
                        temp_str += ", and " + each
                else:
                    temp_str += ", " + each
            if self.very_verbose:
                print('temp_str = %s' % repr(temp_str), file=self.error_file, flush=True)
            if concated_sentence != "" and temp_str != "":
                if self.very_verbose:
                    print("Adding 'is'", file=self.error_file, flush=True)
                if not concated_sentence.endswith(" "):
                    concated_sentence += " "
                concated_sentence += "is "
            elif concated_sentence == "":
                concated_sentence += "It is "
                if self.very_verbose:
                    print("Adding 'It is'", file=self.error_file, flush=True)

            concated_sentence += temp_str
            if self.very_verbose:
                print('concated_sentence = %s' % repr(concated_sentence), file=self.error_file, flush=True)

        return concated_sentence, have_isa_properties

    def mangle_country_name(self, country_phrase: str)->str:
        country_word: str
        country_name: str
        country_word, country_name = country_phrase.split(" ", 1)

        # Refernce:
        # https://everything2.com/title/Countries+that+start+with+the+word+%2522the%2522
        if country_name in ("Bahamas",
                            "Dominican Republic",
                            "Ivory Coast",
                            "Cote d'Ivoire",
                            "Côte d'Ivoire",
                            "Gambia",
                            "Marshall Islands",
                            "Netherlands",
                            "Netherlands Antilles",
                            "Northern Marianas Islands",
                            "Philippines",
                            "Seychelles",
                            "Solomon Islands",
                            "Sudan"
                            "Unitated Arab Emirates"
                            "UAE",
                            "Ukraine",
                            "United Kingdom",
                            "United Kingdom of Great Britain and Northern Ireland",
                            "UK",
                            "United States of America",
                            "United States",
                            "USA"
                            "Vatican City"
                            "Holy See",
                            "Czech Republic"):
            return "in the " + country_name
        else:
            return "in " + country_name

    def add_property_values_to_sentence(self, attribute_dict: EACH_NODE_ATTRIBUTES, concated_sentence: str, have_isa_properties: bool)->str:
        property_values: typing.Optional[Lexicalize.ATTRIBUTE_TYPES] = attribute_dict.get(self.PROPERTY_VALUES)
        if property_values is not None and len(property_values) > 0:
            if self.very_verbose:
                print('property_values is in attribute_dict', file=self.error_file, flush=True)
            temp_list: typing.List[str] = [self.get_real_label_name(each) for each in sorted(property_values)]
            if self.very_verbose:
                print('temp_list = %s' % repr(temp_list), file=self.error_file, flush=True)
            if temp_list[0].startswith("country "):
                temp_list[0] = self.mangle_country_name(temp_list[0])
                if self.very_verbose:
                    print('temp_list after country mangling = %s' % repr(temp_list), file=self.error_file, flush=True)
            if concated_sentence != "":
                if not have_isa_properties:
                    concated_sentence += " "
                else:
                    concated_sentence += ", "
            else:
                if self.very_verbose:
                    print('Starting with "It "', file=self.error_file, flush=True)
                concated_sentence += "It "
            concated_sentence += " and ".join(temp_list)
            if self.very_verbose:
                print('concated_sentence = %s' % repr(concated_sentence), file=self.error_file, flush=True)
        return concated_sentence

    def add_has_properties_to_sentence(self, attribute_dict: EACH_NODE_ATTRIBUTES, concated_sentence: str, have_isa_properties: bool)->str:
        has_properties: typing.Optional[Lexicalize.ATTRIBUTE_TYPES] = attribute_dict.get(self.HAS_PROPERTIES)
        if has_properties is not None and len(has_properties) > 0:
            if self.very_verbose:
                print('has_properties is in attribute_dict', file=self.error_file, flush=True)
            temp_list2: typing.List[str] = [self.get_real_label_name(each) for each in sorted(has_properties)]
            temp_list2 = list(set(temp_list2))
            if self.very_verbose:
                print('temp_list2 = %s' % repr(temp_list2), file=self.error_file, flush=True)
            if concated_sentence != "" and temp_list2[0] != "":
                if have_isa_properties:
                    concated_sentence += ", and has "
                else:
                    concated_sentence += " has "
            elif temp_list2[0] != "":
                concated_sentence += "It has "
            concated_sentence += " and ".join(temp_list2)
            if self.very_verbose:
                print('concated_sentence = %s' % repr(concated_sentence), file=self.error_file, flush=True)
        return concated_sentence

    def attribute_to_sentence(self, attribute_dict: EACH_NODE_ATTRIBUTES, node_id: str)->str:
        if self.very_verbose:
            print("*** Converting attributes to a sentence", file=self.error_file, flush=True)
        concated_sentence: str = ""
        have_isa_properties: bool = False

        concated_sentence = self.add_label_properties_to_sentence(attribute_dict, concated_sentence)
        concated_sentence = self.add_description_properties_to_sentence(attribute_dict, concated_sentence)
        concated_sentence, have_isa_properties = self.add_isa_properties_to_sentence(attribute_dict, concated_sentence)
        concated_sentence = self.add_property_values_to_sentence(attribute_dict, concated_sentence, have_isa_properties)
        concated_sentence = self.add_has_properties_to_sentence(attribute_dict, concated_sentence, have_isa_properties)

        # add ending period
        if concated_sentence != "":
            concated_sentence += "."
        self._logger.debug("Transform node {} --> {}".format(node_id, concated_sentence))
        return concated_sentence

