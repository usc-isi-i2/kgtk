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
    

@attr.s(slots=True, frozen=True)
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

        qnode_idx: int = nr.id_column_idx
        if qnode_idx < 0:
            raise ValueError("The node file is missing an ID column.")

        label_idx: int = nr.column_name_map.get("label", -1)
        if label_idx < 0:
            raise ValueError("The node file is missing a label column.")

        type_idx: int = nr.column_name_map.get("type", -1)
        if type_idx < 0:
            raise ValueError("The node file is missing a type column.")

        description_idx: int = nr.column_name_map.get("description", -1)
        if description_idx < 0:
            raise ValueError("The node file is missing a description column.")

        alias_idx: int = nr.column_name_map.get("alias", -1)
        if alias_idx < 0:
            raise ValueError("The node file is missing a alias column.")

        qnode_count: int = 0
        first: bool = True
        qnode_info: typing.List[str]
        for qnode_info in nr:
            result: typing.Mapping[str, typing.Any] = self.process_qnode(qnode=qnode_info[qnode_idx],
                                                                         label_list=qnode_info[label_idx],
                                                                         qnode_type=qnode_info[type_idx],
                                                                         description_list=qnode_info[description_idx],
                                                                         alias_list=qnode_info[alias_idx],
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

    def build_attr_map(self, attr_list: str, who: str)->typing.Mapping[str, typing.Mapping[str, str]]:
        attr_map: typing.MutableMapping[str, typing.Mapping[str, str]] = { }

        if len(attr_list) == 0:
            return attr_map

        attr: str
        for attr in KgtkValue.split_list(attr_list):
            kv: KgtkValue = KgtkValue(attr, options=self.value_options, parse_fields=True, error_file=self.error_file, verbose=self.verbose)
            if not kv.is_language_qualified_string(validate=True):
                raise ValueError("Invald attr %s in %s" % (attr, who))
            if kv.fields is None:
                raise ValueError("No attr fields in %s in 5s" % (attr, who))
            if kv.fields.text is None:
                raise ValueError("No attr text in %s in %s" % (attr, who))
            text: str = kv.fields.text
            # TODO: destringify the text
            if kv.fields.language is None:
                raise ValueError("No attr language in %s in %s" % (attr, who))
            language: str = kv.fields.language
            if kv.fields.language_suffix is not None:
                language += kv.fields.language_suffix
            attr_map[language] = {
                "language" : language,
                "value": text
            }
        return attr_map
        

    def process_qnode(self,
                      qnode: str,
                      label_list: str,
                      qnode_type: str,
                      description_list: str,
                      alias_list: str,
                      egr: GroupedReader,
                      qgr: GroupedReader)->typing.Mapping[str, typing.Any]:
        if self.verbose:
            print("Processing qnode %s" % qnode)

        result: typing.MutableMapping[str, typing.Any] = {
            "type": qnode_type,
            "id": qnode,
        }

        result["labels"] = self.build_attr_map(label_list, "labels")
        result["descriptions"] = self.build_attr_map(description_list, "descriptions")
        result["aliases"] = self.build_attr_map(alias_list, "aliases")
        
        return result
            
def main():
    """
    Test the Wikidata Exporter.
    """
    pass
    
if __name__ == "__main__":
    main()
