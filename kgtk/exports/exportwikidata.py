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

    def process_qnode_info(self,
                           qnode: str,
                           qnode_info: typing.List[str],
    )->typing.MutableMapping[str, typing.Any]:
        result: typing.MutableMapping[str, typing.Any] = dict()
        self.add_qnode(result, qnode)
        self.add_type(result, qnode_info[self.node_type_idx])

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
                     qualifiers: typing.List[typing.List[str]]):
        if "sitelinks" not in result:
            result["sitelinks"] = dict()
        sitelinks: typing.MutableMapping[str, typing.Mapping[str, typing.Union[str, typing.List[str]]]] = result["sitelinks"]

        site: str = ""
        title: str = ""
        badges: typing.List[str] = list()

        qualifier: typing.List[str]
        for qualifier in qualifiers:
            label: str = qualifier[self.qual_label_idx]

            if label == "site":
                site = qualifier[self.qual_node2_idx]

            elif label == "title":
                title = KgtkFormat.unstringify(qualifier[self.qual_node2_idx])

            elif label == "badge":
                badges.append(qualifier[self.qual_node2_idx])

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
                           edge_row: typing.List[str]):
        datavalue: typing.MutableMapping[str, typing.Union[str, typing.Mapping[str, typing.Union[str, int]]]] = dict()
        datavalue["type"] = edge_row[self.edge_val_type_idx]

        valuemap: typing.MutableMapping[str, typing.Union[str, int]] = dict()
        datavalue["value"] = valuemap

        entity_type: str = edge_row[self.edge_entity_type_idx]
        if len(entity_type) > 0:
            valuemap["entity-type"] = entity_type
            valuemap["id"] = value
            valuemap["numeric-id"] = int(value[1:])
            return datavalue

        

        return datavalue

    def process_qnode_edge(self,
                           result: typing.MutableMapping[str, typing.Any],
                           qnode: str,
                           prop: str,
                           edge_row: typing.List[str],
                           qualifiers: typing.Optional[typing.List[typing.List[str]]]):
        if "claims" not in result:
            result["claims"] = dict()
        claims = result["claims"]

        if prop not in claims:
            claims[prop] = list()
        proplist: typing.List[typing.Mapping[str, typing.Any]] = claims[prop]

        statement: typing.MutableMapping[str, typing.Any] = dict()
        proplist.append(statement)

        # Fill in the top-level attributes:
        statement["type"] = "statement" # We hope this is correct.
        statement["id"] = edge_row[self.edge_claim_id_idx]
        statement["rank"] = edge_row[self.edge_rank_idx]

        mainsnak: typing.MutableMapping[str, typing.Any] = dict()
        statement["mainsnak"] = mainsnak

        mainsnak["property"] = prop
        mainsnak["datatype"] = edge_row[self.edge_wikidatatype_idx]

        value: str = edge_row[self.edge_node2_idx]
        if value == "somevalue":
            mainsnak["snaktype"] = "somevalue"
        else:
            mainsnak["snaktype"] = "value"
            mainsnak["datavalue"] = self.process_edge_datavalue(value, edge_row)
            

    def process_qnode_edges(self,
                            result: typing.MutableMapping[str, typing.Any],
                            qnode: str,
                            edges: typing.List[typing.List[str]],
                            qualifier_dict: typing.Mapping[str, typing.List[typing.List[str]]]):

        # In case we're not using a node file.
        self.add_qnode(result, qnode)

        edge_id: str
        qualifiers: typing.Optional[typing.List[typing.List[str]]]

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

            elif edge_label == "type":
                self.add_type(result, edge_row[self.edge_node2_idx])

            elif edge_label in ("wikipedia_sitelink", "addl_wikipedia_sitelink"):
                edge_id = edge_row[self.edge_id_idx]
                qualifiers = qualifier_dict.get(edge_id)
                if qualifiers is not None and len(qualifiers) > 0:
                    self.add_sitelink(result, edge_id, qualifiers)

            else:
                edge_id = edge_row[self.edge_id_idx]
                qualifiers = qualifier_dict.get(edge_id)
                self.process_qnode_edge(result, qnode, edge_label, edge_row, qualifiers)
                            

    def process_qnode(self,
                      qnode_info: typing.List[str],
                      egr: GroupedReader,
                      qgr: GroupedReader,
    )->typing.Mapping[str, typing.Any]:
        qnode: str = qnode_info[self.node_qnode_idx]
        if self.verbose:
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
            raise ValueError("The edge file does not have a entity_type column.")

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

        self.qual_val_type_idx = er.column_name_map.get("val_type", -1)
        if self.qual_val_type_idx < 0:
            raise ValueError("The qual file does not have a val_type column.")

        self.qual_entity_type_idx = er.column_name_map.get("entity_type", -1)
        if self.qual_entity_type_idx < 0:
            raise ValueError("The qual file does not have a entity_type column.")

        self.qual_datahash_idx = er.column_name_map.get("datahash", -1)
        if self.qual_datahash_idx < 0:
            raise ValueError("The qual file does not have a datahash column.")

        self.qual_precision_idx = er.column_name_map.get("precision", -1)
        if self.qual_precision_idx < 0:
            raise ValueError("The qual file does not have a precision column.")

        self.qual_calendar_idx = er.column_name_map.get("calendar", -1)
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
