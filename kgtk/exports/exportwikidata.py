"""Import ntriples into KGTK format.
"""
from argparse import ArgumentParser, Namespace
import attr
import json
from pathlib import Path
import re
import sys
import typing

from kgtk.kgtkformat import KgtkFormat
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderMode, KgtkReaderOptions
from kgtk.value.kgtkvalue import KgtkValue, KgtkValueFields
from kgtk.value.kgtkvalueoptions import KgtkValueOptions, DEFAULT_KGTK_VALUE_OPTIONS

@attr.s(slots=True, frozen=False)
class GroupedReader:
    reader: KgtkReader = attr.ib(validator=attr.validators.instance_of(KgtkReader))

    current_row: typing.Optional[typing.List[str]] = attr.ib(default=None)
    current_qnode: typing.Optional[str] = attr.ib(default=None)

    def fetch(self, qnode: str)->typing.List[typing.List[str]]:
        result: typing.List[typing.List[str]] = [ ]
        while True:
            if self.current_row is None:
                try:
                    self.current_row = self.reader.nextrow()
                except StopIteration:
                    return result

                if self.reader.node1_column_idx < 0:
                    raise ValueError("GroupedReader: no node1 index.")

                current_qnode: str = self.current_row[self.reader.node1_column_idx]
                if "-" in current_qnode:
                    current_qnode, _ = current_qnode.split("-", 1)
                self.current_qnode = current_qnode

            if self.current_qnode is None:
                raise ValueError("GroupedReader: self.current_qunode is unexpectedly missing.")

            if self.current_qnode < qnode:
                self.current_row = None
                continue

            if self.current_qnode > qnode:
                return result

            result.append(self.current_row)
            self.current_row = None
                
@attr.s(slots=True, frozen=False)
class ExportWikidata(KgtkFormat):
    # TODO: write a validator:
    node_file_path: Path = attr.ib(validator=attr.validators.instance_of(Path))
    edge_file_path: Path = attr.ib(validator=attr.validators.instance_of(Path))
    qualifier_file_path: Path = attr.ib(validator=attr.validators.instance_of(Path))

    output_file_path: Path = attr.ib(validator=attr.validators.instance_of(Path))

    reader_options: KgtkReaderOptions = attr.ib(validator=attr.validators.instance_of(KgtkReaderOptions))
    value_options: KgtkValueOptions = attr.ib(validator=attr.validators.instance_of(KgtkValueOptions), default=DEFAULT_KGTK_VALUE_OPTIONS)

    error_file: typing.TextIO = attr.ib(default=sys.stderr)
    verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    very_verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    node_alias_idx: int = attr.ib(default=-1)
    node_description_idx: int = attr.ib(default=-1)
    node_label_idx: int = attr.ib(default=-1)
    node_qnode_idx: int = attr.ib(default=-1)
    node_type_idx: int = attr.ib(default=-1)
    node_datatype_idx: int = attr.ib(default=-1)

    edge_id_idx: int = attr.ib(default=-1)
    edge_node1_idx: int = attr.ib(default=-1)
    edge_label_idx: int = attr.ib(default=-1)
    edge_node2_idx: int = attr.ib(default=-1)
    edge_rank_idx: int = attr.ib(default=-1)
    edge_wikidatatype_idx: int = attr.ib(default=-1)
    edge_claim_id_idx: int = attr.ib(default=-1)
    edge_val_type_idx: int = attr.ib(default=-1)
    edge_entity_type_idx: int = attr.ib(default=-1)
    edge_datahash_idx: int = attr.ib(default=-1)
    edge_precision_idx: int = attr.ib(default=-1)
    edge_calendar_idx: int = attr.ib(default=-1)

    qual_node1_idx: int = attr.ib(default=-1)
    qual_label_idx: int = attr.ib(default=-1)
    qual_node2_idx: int = attr.ib(default=-1)
    qual_wikidatatype_idx: int = attr.ib(default=-1)
    qual_val_type_idx: int = attr.ib(default=-1)
    qual_entity_type_idx: int = attr.ib(default=-1)
    qual_datahash_idx: int = attr.ib(default=-1)
    qual_precision_idx: int = attr.ib(default=-1)
    qual_calendar_idx: int = attr.ib(default=-1)

    def add_attr_to_map(self,
                        attr_map: typing.MutableMapping[str, typing.Mapping[str, str]],
                        attr: str,
                        who: str,
    ):
        kv: KgtkValue = KgtkValue(attr, options=self.value_options, parse_fields=False, error_file=self.error_file, verbose=self.verbose)
        if not kv.is_language_qualified_string(validate=True):
            raise ValueError("Invald attr %s for %s" % (attr, who))

        text: str
        language: str
        language_suffix: str
        text, language, language_suffix = KgtkFormat.destringify(kv.value)
        if len(language) == 0:
            raise ValueError("No attr language in %s for %s" % (attr, who))
        lang: str = language + language_suffix
        attr_map[lang] = {
                "language" : lang,
                "value": text
        }
            

    def add_attr(self,
                 result: typing.MutableMapping[str, typing.Any],
                 attr: str,
                 who: str,
    ):
        attr_map: typing.MutableMapping[str, typing.Mapping[str, str]]
        if who in result:
            attr_map = result[who]
        else:
            attr_map = dict()
            result[who] = attr_map

        self.add_attr_to_map(attr_map, attr, who)

    def build_attr_map(self,
                       result: typing.MutableMapping[str, typing.Any],
                       attr_list: str,
                       who: str,
    ):
        if len(attr_list) == 0:
            return
        
        attr_map: typing.MutableMapping[str, typing.Mapping[str, str]] = { }
        attr: str
        for attr in KgtkValue.split_list(attr_list):
            self.add_attr_to_map(attr_map, attr, who)

        if len(attr_map) > 0:
            result[who] = attr_map

    def add_qnode(self,
                 result: typing.MutableMapping[str, typing.Any],
                 qnode: str):
        result["id"] = qnode

    def add_type(self,
                 result: typing.MutableMapping[str, typing.Any],
                 node_type: str):
        result["type"] = node_type

    def add_datatype(self,
                 result: typing.MutableMapping[str, typing.Any],
                 node_type: str):
        if len(node_type) > 0:
            result["datatype"] = node_type

    def process_qnode_info(self,
                           qnode: str,
                           qnode_info: typing.List[str],
    )->typing.MutableMapping[str, typing.Any]:
        result: typing.MutableMapping[str, typing.Any] = dict()
        self.add_qnode(result, qnode)
        self.add_type(result, qnode_info[self.node_type_idx])
        self.add_datatype(result, qnode_info[self.node_datatype_idx])

        self.build_attr_map(result, qnode_info[self.node_label_idx], "labels")
        self.build_attr_map(result, qnode_info[self.node_description_idx], "descriptions")
        self.build_attr_map(result, qnode_info[self.node_alias_idx], "aliases")
        
        return result

    def build_qualifier_dict(self, qnode: str, qgr: GroupedReader)->typing.Mapping[str, typing.List[typing.List[str]]]:
        result: typing.MutableMapping[str, typing.List[typing.List[str]]] = dict()

        qualifiers: typing.List[typing.List[str]] = qgr.fetch(qnode)
        qualifier: typing.List[str]
        for qualifier in qualifiers:
            edge_id: str = qualifier[self.qual_node1_idx]
            if edge_id not in result:
                result[edge_id] = list()
            result[edge_id].append(qualifier)

        return result

    def add_sitelink(self,
                     result: typing.MutableMapping[str, typing.Any],
                     edge_id: str,
                     qualifier_rows: typing.List[typing.List[str]]):
        if "sitelinks" not in result:
            result["sitelinks"] = dict()
        sitelinks: typing.MutableMapping[str, typing.Mapping[str, typing.Union[str, typing.List[str]]]] = result["sitelinks"]

        site: str = ""
        title: str = ""
        badges: typing.List[str] = list()

        qualifier_row: typing.List[str]
        for qualifier_row in qualifier_rows:
            label: str = qualifier_row[self.qual_label_idx]

            if label == "site":
                site = qualifier_row[self.qual_node2_idx]

            elif label == "title":
                title = KgtkFormat.unstringify(qualifier_row[self.qual_node2_idx])

            elif label == "badge":
                badges.append(qualifier_row[self.qual_node2_idx])

        if len(site) == 0:
            # TODO: give a better error message.
            raise ValueError("Missing sitelink site for %s" % edge_id)

        if len(title) == 0:
            # TODO: give a better error message.
            raise ValueError("Missing sitelink title for %s" % edge_id)

        sitelinks[site] = {
            "site": site,
            "title": title,
            "badges": badges
        }
            

    def process_edge_datavalue(self,
                               value: str,
                               edge_row: typing.List[str],
                               datatype: str):
        datavalue: typing.MutableMapping[str, typing.Union[str, typing.Mapping[str, typing.Optional[typing.Union[str, int, float]]]]] = dict()
        datavalue["type"] = edge_row[self.edge_val_type_idx]

        valuemap: typing.MutableMapping[str, typing.Optional[typing.Union[str, int, float]]] = dict()
        datavalue["value"] = valuemap

        entity_type: str = edge_row[self.edge_entity_type_idx]
        if len(entity_type) > 0:
            valuemap["entity-type"] = entity_type
            valuemap["id"] = value

            # TODO: Is this the right thing to do?
            numeric_id: str = value[1:]
            if "-" in numeric_id:
                numeric_id = numeric_id[:numeric_id.index("-")]
            valuemap["numeric-id"] = int(numeric_id)
            return datavalue

        kv = KgtkValue(value, options=self.value_options, parse_fields=True, error_file=self.error_file, verbose=self.verbose)
        if not kv.validate():
            # raise ValueError("Invalid KGTK value '%s'" % value)
            print("Warning: Invalid KGTK value '%s'" % value, file=self.error_file, flush=True)
        if kv.fields is None:
            raise ValueError("KGTK value '%s' is missing fields." %value)

        if kv.is_number():
            if kv.fields.numberstr is None:
                raise ValueError("number is missing numberstr.")
                
            valuemap["amount"] = kv.fields.numberstr # TODO: add plus sign
            valuemap["unit"] = "1"
            return datavalue

        if kv.is_quantity():
            if kv.fields.numberstr is None:
                raise ValueError("quantity is missing numberstr.")
            valuemap["amount"] = kv.fields.numberstr # TODO: add plus sign

            if kv.fields.units_node is None:
                # TODO: research this further.
                #
                # raise ValueError("quantity is missing units_node for %s." % value)
                valuemap["init"] = "undefined"
            else:
                valuemap["unit"] = "http://www.wikidata.org/entity/" + kv.fields.units_node

            if kv.fields.low_tolerancestr is not None and len(kv.fields.low_tolerancestr) > 0:
                valuemap["lowerBound"] = kv.fields.low_tolerancestr # TODO: add plus sign

            if kv.fields.high_tolerancestr is not None and len(kv.fields.high_tolerancestr) > 0:
                valuemap["higherBound"] = kv.fields.high_tolerancestr # TODO: add plus sign
            return datavalue

        if kv.is_language_qualified_string():
            text: str
            language: str
            language_suffix: str
            text, language, language_suffix = KgtkFormat.destringify(value) # TODO: KgtkValue should do this to text
            language += language_suffix
            valuemap["text"] = text
            valuemap["language"] = language
            return datavalue
        
        if kv.is_string():
            valuemap["type"] = "string"
            valuemap["value"] = KgtkFormat.unstringify(value) # TODO: KgtkValue should do this to text
            return datavalue

        if kv.is_date_and_times():
            if kv.fields.zonestr is None:
                raise ValueError("timezone is missing.")
            if kv.fields.zonestr != "Z":
                raise ValueError("Only Z-time is supported.")

            if kv.fields.date_and_time is None:
                raise ValueError("date_and_time is missing.")
            valuemap["time"] = kv.fields.date_and_time
            valuemap["timezone"] = 0
            valuemap["before"] = 0
            valuemap["after"] = 0
        
            if kv.fields.precision is None:
                raise ValueError("date_and_time precision is missing.")
            valuemap["precision"] = kv.fields.precision

            valuemap["calendarmodel"] = "http://www.wikidata.org/entity/" + edge_row[self.edge_calendar_idx]
            return datavalue

        if kv.is_location_coordinates:
            if kv.fields.latitude is None:
                raise ValueError("latitude is missing")
            valuemap["latitude"] = kv.fields.latitude

            if kv.fields.longitude is None:
                raise ValueError("longitude is missing")
            valuemap["longitude"] = kv.fields.longitude

            valuemap["altitide"] = None # deprecated

            # TODO: Validate that it's OK to have location coordinates without precision.
            precision: str = edge_row[self.edge_precision_idx]
            if len(precision) > 0:
                try:
                    valuemap["precision"] = float(edge_row[self.edge_precision_idx])
                except ValueError:
                    print("Invalid precision '%s'" % precision, file=self.error_file, flush=True)

            valuemap["globe"] = "http://www.wikidata.org/entity/Q2"
            return datavalue


        # Default: treat as string.
        valuemap["type"] = "string"
        valuemap["value"] = KgtkFormat.unstringify(value) # TODO: KgtkValue should do this to text
        return datavalue

    def process_qual_datavalue(self,
                               value: str,
                               qual_row: typing.List[str],
                               datatype: str):
        datavalue: typing.MutableMapping[str, typing.Union[str, typing.Mapping[str, typing.Optional[typing.Union[str, int, float]]]]] = dict()
        datavalue["type"] = qual_row[self.qual_val_type_idx]

        valuemap: typing.MutableMapping[str, typing.Optional[typing.Union[str, int, float]]] = dict()
        datavalue["value"] = valuemap

        entity_type: str = qual_row[self.qual_entity_type_idx]
        if len(entity_type) > 0:
            valuemap["entity-type"] = entity_type
            valuemap["id"] = value

            # TODO: Is this the right thing to do for Q16097-F1?
            numeric_id: str = value[1:]
            if "-" in numeric_id:
                numeric_id = numeric_id[:numeric_id.index("-")]
            valuemap["numeric-id"] = int(numeric_id)
            return datavalue

        kv = KgtkValue(value, options=self.value_options, parse_fields=True, error_file=self.error_file, verbose=self.verbose)
        if not kv.validate():
            # raise ValueError("Invalid KGTK value '%s'" % value)
            print("Warning: Invalid KGTK value '%s'" % value, file=self.error_file, flush=True)
        if kv.fields is None:
            raise ValueError("KGTK value %s is missing fields." % value)

        if kv.is_number():
            if kv.fields.numberstr is None:
                raise ValueError("number is missing numberstr for %s." % value)
                
            valuemap["amount"] = kv.fields.numberstr # TODO: add plus sign
            valuemap["unit"] = "1"
            return datavalue

        if kv.is_quantity():
            if kv.fields.numberstr is None:
                raise ValueError("quantity is missing numberstr for %s." % value)
            valuemap["amount"] = kv.fields.numberstr # TODO: add plus sign

            if kv.fields.units_node is None:
                # TODO: Research this further.  Why did we get here?  Is it because import_wikidata
                # dropped the units?
                #
                # raise ValueError("quantity is missing units_node for %s in: %s" % (value, " ".join(qual_row)))
                valuemap["unit"] = "undefined"
            else:
                valuemap["unit"] = "http://www.wikidata.org/entity/" + kv.fields.units_node

            if kv.fields.low_tolerancestr is not None and len(kv.fields.low_tolerancestr) > 0:
                valuemap["lowerBound"] = kv.fields.low_tolerancestr # TODO: add plus sign

            if kv.fields.high_tolerancestr is not None and len(kv.fields.high_tolerancestr) > 0:
                valuemap["higherBound"] = kv.fields.high_tolerancestr # TODO: add plus sign
            return datavalue

        if kv.is_language_qualified_string():
            text: str
            language: str
            language_suffix: str
            text, language, language_suffix = KgtkFormat.destringify(value) # TODO: KgtkValue should do this to text
            language += language_suffix
            valuemap["text"] = text
            valuemap["language"] = language
            return datavalue
        
        if kv.is_string():
            valuemap["type"] = "string"
            valuemap["value"] = KgtkFormat.unstringify(value) # TODO: KgtkValue should do this to text
            return datavalue

        if kv.is_date_and_times():
            if kv.fields.zonestr is None:
                raise ValueError("timezone is missing from %s." % value)
            if kv.fields.zonestr != "Z":
                raise ValueError("Only Z-time is supported, error in %s." % value)

            if kv.fields.date_and_time is None:
                raise ValueError("date_and_time is missing from %s." % value)
            valuemap["time"] = kv.fields.date_and_time
            valuemap["timezone"] = 0
            valuemap["before"] = 0
            valuemap["after"] = 0
        
            if kv.fields.precision is None:
                raise ValueError("date_and_time precision is missing from %s." % value)
            valuemap["precision"] = kv.fields.precision

            valuemap["calendarmodel"] = "http://www.wikidata.org/entity/" + qual_row[self.qual_calendar_idx]
            return datavalue

        if kv.is_location_coordinates():
            if kv.fields.latitude is None:
                raise ValueError("latitude is missing from %s" % value)
            valuemap["latitude"] = kv.fields.latitude

            if kv.fields.longitude is None:
                raise ValueError("longitude is missing from %s" % value)
            valuemap["longitude"] = kv.fields.longitude

            valuemap["altitide"] = None # deprecated

            valuemap["precision"] = float(qual_row[self.qual_precision_idx])

            valuemap["globe"] = "http://www.wikidata.org/entity/Q2"
            return datavalue


        # Default: convert the symbol to a string.
        valuemap["type"] = "string"
        valuemap["value"] = KgtkFormat.unstringify('"' + value + '"') # TODO: KgtkValue should do this to text
        return datavalue

    def process_qnode_edge_qualifier(self,
                           statement: typing.MutableMapping[str, typing.Any],
                           edge_id: str,
                           qualifier_row: typing.List[str]):
        if "qualifiers" not in statement:
            statement["qualifiers"] = dict()
        qualifiers = statement["qualifiers"]

        prop: str = qualifier_row[self.qual_label_idx]
        if prop not in qualifiers:
            qualifiers[prop] = list()
        proplist: typing.List[typing.Mapping[str, typing.Any]] = qualifiers[prop]

        qualifier: typing.MutableMapping[str, typing.Any] = dict()
        proplist.append(qualifier)

        qualifier["property"] = prop

        datatype: str = qualifier_row[self.qual_wikidatatype_idx]
        qualifier["datatype"] = datatype

        datahash: str = qualifier_row[self.qual_datahash_idx]
        if len(datahash) > 0:
            qualifier["hash"] = KgtkFormat.unstringify(datahash)

        value: str = qualifier_row[self.qual_node2_idx]
        if value == "somevalue":
            qualifier["snaktype"] = "somevalue"
        elif value == "novalue":
            qualifier["snaktype"] = "novalue"
        else:
            qualifier["datavalue"] = self.process_qual_datavalue(value, qualifier_row, datatype)

    def process_qnode_edge_qualifiers(self,
                                      statement: typing.MutableMapping[str, typing.Any],
                                      edge_id: str,
                                      qualifier_rows: typing.List[typing.List[str]]):
        qualifier_row: typing.List[str]
        for qualifier_row in qualifier_rows:
            self.process_qnode_edge_qualifier(statement, edge_id, qualifier_row)

    def process_qnode_edge(self,
                           result: typing.MutableMapping[str, typing.Any],
                           qnode: str,
                           prop: str,
                           edge_id: str,
                           edge_row: typing.List[str],
                           qualifier_rows: typing.Optional[typing.List[typing.List[str]]]):
        if "claims" not in result:
            result["claims"] = dict()
        claims = result["claims"]

        if prop not in claims:
            claims[prop] = list()
        proplist: typing.List[typing.Mapping[str, typing.Any]] = claims[prop]

        try:
            statement: typing.MutableMapping[str, typing.Any] = dict()
            
            # Fill in the top-level attributes:
            statement["type"] = "statement" # We hope this is correct.
            statement["id"] = edge_row[self.edge_claim_id_idx]
            statement["rank"] = edge_row[self.edge_rank_idx]

            mainsnak: typing.MutableMapping[str, typing.Any] = dict()
            statement["mainsnak"] = mainsnak

            mainsnak["property"] = prop

            datatype: str = edge_row[self.edge_wikidatatype_idx]
            mainsnak["datatype"] = datatype

            value: str = edge_row[self.edge_node2_idx]
            if value == "somevalue":
                mainsnak["snaktype"] = "somevalue"
            elif value == "novalue":
                mainsnak["snaktype"] = "novalue"
            else:
                mainsnak["snaktype"] = "value"
                mainsnak["datavalue"] = self.process_edge_datavalue(value, edge_row, datatype)

            if qualifier_rows is not None and len(qualifier_rows) > 0:
                self.process_qnode_edge_qualifiers(result, edge_id, qualifier_rows)

            proplist.append(statement)
        
        except ValueError as e:
            print("Error, skipping statement: %s" % str(e), file=self.error_file, flush=True)

    def process_qnode_edges(self,
                            result: typing.MutableMapping[str, typing.Any],
                            qnode: str,
                            edges: typing.List[typing.List[str]],
                            qualifier_dict: typing.Mapping[str, typing.List[typing.List[str]]]):

        # In case we're not using a node file.
        self.add_qnode(result, qnode)

        edge_id: str
        qualifier_rows: typing.Optional[typing.List[typing.List[str]]]

        edge_row: typing.List[str]
        for edge_row in edges:
            edge_label: str = edge_row[self.edge_label_idx]

            if edge_label == "alias":
                self.add_attr(result, edge_row[self.edge_node2_idx], "alias")

            elif edge_label == "description":
                self.add_attr(result, edge_row[self.edge_node2_idx], "description")
            
            elif edge_label == "label":
                self.add_attr(result, edge_row[self.edge_node2_idx], "label")
            
            elif edge_label == "type":
                self.add_type(result, edge_row[self.edge_node2_idx])

            elif edge_label == "datatype":
                self.add_datatype(result, edge_row[self.edge_node2_idx])

            elif edge_label in ("wikipedia_sitelink", "addl_wikipedia_sitelink"):
                edge_id = edge_row[self.edge_id_idx]
                qualifier_rows = qualifier_dict.get(edge_id)
                if qualifier_rows is not None and len(qualifier_rows) > 0:
                    self.add_sitelink(result, edge_id, qualifier_rows)

            else:
                edge_id = edge_row[self.edge_id_idx]
                qualifier_rows = qualifier_dict.get(edge_id)
                self.process_qnode_edge(result, qnode, edge_label, edge_id, edge_row, qualifier_rows)
                            

    def process_qnode(self,
                      qnode_info: typing.List[str],
                      egr: GroupedReader,
                      qgr: GroupedReader,
    )->typing.Mapping[str, typing.Any]:
        qnode: str = qnode_info[self.node_qnode_idx]
        if self.very_verbose:
            print("Processing qnode %s" % qnode)

        result: typing.MutableMapping[str, typing.Any] =  self.process_qnode_info(qnode, qnode_info)

        edges: typing.List[typing.List[str]] = egr.fetch(qnode)
        qualifier_dict: typing.Mapping[str, typing.List[typing.List[str]]] = self.build_qualifier_dict(qnode, qgr)

        self.process_qnode_edges(result, qnode, edges, qualifier_dict)
        
        return result
            
    def get_required_columns(self, nr: KgtkReader, er: KgtkReader, qr: KgtkReader):
        self.node_qnode_idx = nr.id_column_idx
        if self.node_qnode_idx < 0:
            raise ValueError("The node file is missing an ID column.")

        self.node_label_idx = nr.column_name_map.get("label", -1)
        if self.node_label_idx < 0:
            raise ValueError("The node file is missing a label column.")

        self.node_type_idx = nr.column_name_map.get("type", -1)
        if self.node_type_idx < 0:
            raise ValueError("The node file is missing a type column.")

        self.node_datatype_idx = nr.column_name_map.get("datatype", -1)
        if self.node_datatype_idx < 0:
            raise ValueError("The node file is missing a datatype column.")

        self.node_description_idx = nr.column_name_map.get("description", -1)
        if self.node_description_idx < 0:
            raise ValueError("The node file is missing a description column.")

        self.node_alias_idx = nr.column_name_map.get("alias", -1)
        if self.node_alias_idx < 0:
            raise ValueError("The node file is missing a alias column.")


        self.edge_id_idx = er.id_column_idx
        if self.edge_id_idx < 0:
            raise ValueError("The edge file does not have a id column.")

        self.edge_node1_idx = er.node1_column_idx
        if self.edge_node1_idx < 0:
            raise ValueError("The edge file does not have a node1 column.")

        self.edge_label_idx = er.label_column_idx
        if self.edge_label_idx < 0:
            raise ValueError("The edge file does not have a label column.")

        self.edge_node2_idx = er.node2_column_idx
        if self.edge_node2_idx < 0:
            raise ValueError("The edge file does not have a node2 column.")

        self.edge_rank_idx = er.column_name_map.get("rank", -1)
        if self.edge_rank_idx < 0:
            raise ValueError("The edge file does not have a rank column.")

        self.edge_wikidatatype_idx = er.column_name_map.get("node2;wikidatatype", -1)
        if self.edge_wikidatatype_idx < 0:
            raise ValueError("The edge file does not have a node2:wikidatatype column.")

        self.edge_claim_id_idx = er.column_name_map.get("claim_id", -1)
        if self.edge_claim_id_idx < 0:
            raise ValueError("The edge file does not have a claim_id column.")

        self.edge_val_type_idx = er.column_name_map.get("val_type", -1)
        if self.edge_val_type_idx < 0:
            raise ValueError("The edge file does not have a val_type column.")

        self.edge_entity_type_idx = er.column_name_map.get("entity_type", -1)
        if self.edge_entity_type_idx < 0:
            raise ValueError("The edge file does not have an entity_type column.")

        self.edge_datahash_idx = er.column_name_map.get("datahash", -1)
        if self.edge_datahash_idx < 0:
            raise ValueError("The edge file does not have a datahash column.")

        self.edge_precision_idx = er.column_name_map.get("precision", -1)
        if self.edge_precision_idx < 0:
            raise ValueError("The edge file does not have a precision column.")

        self.edge_calendar_idx = er.column_name_map.get("calendar", -1)
        if self.edge_calendar_idx < 0:
            raise ValueError("The edge file does not have a calendar column.")


        self.qual_node1_idx = qr.node1_column_idx
        if self.qual_node1_idx < 0:
            raise ValueError("The qualifier file does not have a node1 column.")

        self.qual_label_idx = qr.label_column_idx
        if self.qual_label_idx < 0:
            raise ValueError("The qualifier file does not have a label column.")

        self.qual_node2_idx = qr.node2_column_idx
        if self.qual_node2_idx < 0:
            raise ValueError("The qualifier file does not have a node2 column.")

        self.qual_wikidatatype_idx = qr.column_name_map.get("node2;wikidatatype", -1)
        if self.qual_wikidatatype_idx < 0:
            raise ValueError("The qualifier file does not have a node2:wikidatatype column.")

        self.qual_val_type_idx = qr.column_name_map.get("val_type", -1)
        if self.qual_val_type_idx < 0:
            raise ValueError("The qual file does not have a val_type column.")

        self.qual_entity_type_idx = qr.column_name_map.get("entity_type", -1)
        if self.qual_entity_type_idx < 0:
            raise ValueError("The qual file does not have an entity_type column.")

        self.qual_datahash_idx = qr.column_name_map.get("datahash", -1)
        if self.qual_datahash_idx < 0:
            raise ValueError("The qual file does not have a datahash column.")

        self.qual_precision_idx = qr.column_name_map.get("precision", -1)
        if self.qual_precision_idx < 0:
            raise ValueError("The qual file does not have a precision column.")

        self.qual_calendar_idx = qr.column_name_map.get("calendar", -1)
        if self.qual_calendar_idx < 0:
            raise ValueError("The qual file does not have a calendar column.")

    def process(self):

        if self.verbose:
            print("Opening output file %s" % str(self.output_file_path), file=self.error_file, flush=True)
        outfile: typing.TextIO = open(self.output_file_path, "wt")
        outfile.write("[")

        if self.verbose:
            print("Opening the node file: %s" % str(self.node_file_path), file=self.error_file, flush=True)
        nr: KgtkReader = KgtkReader.open(self.node_file_path,
                                         error_file=self.error_file,
                                         options=self.reader_options,
                                         value_options = self.value_options,
                                         verbose=self.verbose,
                                         very_verbose=self.very_verbose,
        )

        if self.verbose:
            print("Opening the edge file: %s" % str(self.edge_file_path), file=self.error_file, flush=True)
        er: KgtkReader = KgtkReader.open(self.edge_file_path,
                                         error_file=self.error_file,
                                         options=self.reader_options,
                                         value_options = self.value_options,
                                         verbose=self.verbose,
                                         very_verbose=self.very_verbose,
        )
        egr: GroupedReader = GroupedReader(reader=er)

        if self.verbose:
            print("Opening the qualifier file: %s" % str(self.qualifier_file_path), file=self.error_file, flush=True)
        qr: KgtkReader = KgtkReader.open(self.qualifier_file_path,
                                         error_file=self.error_file,
                                         options=self.reader_options,
                                         value_options = self.value_options,
                                         verbose=self.verbose,
                                         very_verbose=self.very_verbose,
        )
        qgr: GroupedReader = GroupedReader(reader=qr)

        self.get_required_columns(nr, er, qr)

        qnode_count: int = 0
        first: bool = True
        qnode_info: typing.List[str]
        for qnode_info in nr:
            result: typing.Mapping[str, typing.Any] = self.process_qnode(qnode_info,
                                                                         egr=egr,
                                                                         qgr=qgr)
            if first:
                first = False
                outfile.write("\n")
            else:
                outfile.write(",\n")
            outfile.write(json.dumps(result, indent=None, separators=(',', ':'), sort_keys=True))

        outfile.write("\n]\n")
        outfile.close()

def main():
    """
    Test the Wikidata Exporter.
    """
    pass
    
if __name__ == "__main__":
    main()
