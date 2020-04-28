"""
Generate wikidata triples from two edge files:
1. A statement and qualifier edge file that contains an edge id, node1, label, and node2
2. A kgtk file that contains the mapping information from property identifier to its datatype

"""

def parser():
    """
    Initialize sub-parser.
    Parameters: https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser
    """
    return {
        "help": "Generates wikidata triples from kgtk file",
        "description": "Generating Wikidata triples.",
    }
def str2bool(v):
    import argparse
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def add_arguments(parser):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
        propFile: str, labelSet: str, aliasSet: str, descriptionSet: str, n: str, dest: Any  --output-n-lines --generate-truthy
    """
    parser.add_argument(
        "-lp",
        "--label-property",
        action="store",
        type=str,
        help="property identifiers which will create labels, separated by comma','.",
        dest="labels",
    )
    parser.add_argument(
        "-ap",
        "--alias-property",
        action="store",
        type=str,
        help="alias identifiers which will create labels, separated by comma','.",
        dest="aliases",
    )
    parser.add_argument(
        "-dp",
        "--description-property",
        action="store",
        type=str,
        help="description identifiers which will create labels, separated by comma','.",
        dest="descriptions",
    )
    parser.add_argument(
        "-pf",
        "--property-types",
        action="store",
        type=str,
        help="path to the file which contains the property datatype mapping in kgtk format.",
        dest="propFile",
    )
    parser.add_argument(
        "-n",
        "--output-n-lines",
        action="store",
        type=int,
        help="output triples approximately every {n} lines of reading stdin.",
        dest="n",
    )
    parser.add_argument(
        "-gt",
        "--generate-truthy",
        action="store",
        type=str2bool,
        help="the default is to not generate truthy triples. Specify this option to generate truthy triples. NOTIMPLEMENTED",
        dest="truthy",
    )
    parser.add_argument(
        "-ig",
        "--ig",
        action="store",
        type=str2bool,
        help="if set to yes, ignore various kinds of exceptions and mistakes and log them to a log file with line number in input file, rather than stopping. logging",
        dest="ignore",
    )
    # logging level
    # parser.add_argument('-l', '--logging-level', action='store', dest='logging_level',
    #         default="info", choices=("error", "warning", "info", "debug"),
    #         help="set up the logging level, default is INFO level")


def run(
    labels: str,
    aliases: str,
    descriptions: str,
    propFile: str,
    n: int,
    truthy: bool,
    ignore: bool,
    # logging_level:str
):
    # import modules locally
    import sys
    import warnings
    import re
    import requests
    from typing import TextIO
    import logging
    from etk.wikidata.entity import WDItem, WDProperty
    from kgtk.exceptions import KGTKException

    class TripleGenerator:
        """
        A class to maintain the status of the generator
        """
        def __init__(
            self,
            propFile: str,
            labelSet: str,
            aliasSet: str,
            descriptionSet: str,
            ignore: bool,
            n: int,
            destFp: TextIO = sys.stdout,
            truthy:bool =False
        ):
            from etk.wikidata.statement import Rank
            from etk.etk import ETK
            from etk.knowledge_graph import KGSchema
            from etk.etk_module import ETKModule
            self.ignore = ignore
            self.propTypes = self.__setPropTypes(propFile)
            self.labelSet, self.aliasSet, self.descriptionSet = self.__setSets(
                labelSet, aliasSet, descriptionSet
            )
            self.fp = destFp
            self.n = int(n)
            self.read = 0
            # ignore-logging, if not ignore, log them and move on.
            if not self.ignore:
                self.ignoreFile = open("ignored.log","w")
            # corrupted statement id
            self.corrupted_statement_id = None
            # serialize prfix
            kg_schema = KGSchema()
            kg_schema.add_schema("@prefix : <http://isi.edu/> .", "ttl")
            self.etk = ETK(kg_schema=kg_schema, modules=ETKModule)
            self.doc = self.__setDoc()
            self.__serialize_prefix()
        
        def _node_2_entity(self, node:str):
            '''
            A node can be Qxxx or Pxxx, return the proper entity.
            '''
            if node in self.propTypes:
                entity = WDProperty(node, self.propTypes[node])
            else:
                entity = WDItem(TripleGenerator.replaceIllegalString(node.upper()))
            return entity


        def __setPropTypes(self, propFile: str):
            from etk.wikidata.value import (
            Item,
            StringValue,
            TimeValue,
            QuantityValue,
            MonolingualText,
            GlobeCoordinate,
            ExternalIdentifier,
            URLValue
            )
            dataTypeMappings = {
                "item": Item,
                "time": TimeValue,
                "globe-coordinate": GlobeCoordinate,
                "quantity": QuantityValue,
                "monolingualtext": MonolingualText,
                "string": StringValue,
                "external-identifier":ExternalIdentifier,
                "url":URLValue
            }
            with open(propFile, "r") as fp:
                props = fp.readlines()
            __propTypes = {}
            for line in props[1:]:
                node1, _, node2 = line.split("\t")
                try:
                    __propTypes[node1] = dataTypeMappings[node2.strip()]
                except:
                    if not self.ignore:                    
                        raise KGTKException(
                            "DataType {} of node {} is not supported.\n".format(
                                node2, node1
                            )
                        )
            return __propTypes

        def __setSets(self, labelSet: str, aliasSet: str, descriptionSet: str):
            return (
                set(labelSet.split(",")),
                set(aliasSet.split(",")),
                set(descriptionSet.split(",")),
            )

        def __setDoc(self, doc_id: str = "http://isi.edu/default-ns/projects"):
            """
            reset the doc object and return it. Called at initialization and after outputting triples.
            """
            doc = self.etk.create_document({}, doc_id=doc_id)
            # bind prefixes
            doc.kg.bind("wikibase", "http://wikiba.se/ontology#")
            doc.kg.bind("wd", "http://www.wikidata.org/entity/")
            doc.kg.bind("wdt", "http://www.wikidata.org/prop/direct/")
            doc.kg.bind("wdtn", "http://www.wikidata.org/prop/direct-normalized/")
            doc.kg.bind("wdno", "http://www.wikidata.org/prop/novalue/")
            doc.kg.bind("wds", "http://www.wikidata.org/entity/statement/")
            doc.kg.bind("wdv", "http://www.wikidata.org/value/")
            doc.kg.bind("wdref", "http://www.wikidata.org/reference/")
            doc.kg.bind("p", "http://www.wikidata.org/prop/")
            doc.kg.bind("pr", "http://www.wikidata.org/prop/reference/")
            doc.kg.bind("prv", "http://www.wikidata.org/prop/reference/value/")
            doc.kg.bind(
                "prn", "http://www.wikidata.org/prop/reference/value-normalized/"
            )
            doc.kg.bind("ps", "http://www.wikidata.org/prop/statement/")
            doc.kg.bind("psv", "http://www.wikidata.org/prop/statement/value/")
            doc.kg.bind(
                "psn", "http://www.wikidata.org/prop/statement/value-normalized/"
            )
            doc.kg.bind("pq", "http://www.wikidata.org/prop/qualifier/")
            doc.kg.bind("pqv", "http://www.wikidata.org/prop/qualifier/value/")
            doc.kg.bind(
                "pqn", "http://www.wikidata.org/prop/qualifier/value-normalized/"
            )
            doc.kg.bind("skos", "http://www.w3.org/2004/02/skos/core#")
            doc.kg.bind("prov", "http://www.w3.org/ns/prov#")
            doc.kg.bind("schema", "http://schema.org/")
            return doc

        @staticmethod
        def _process_text_string(string:str)->[str,str]:
            ''' 
            '''
            if "@" in string:
                res = string.split("@")
                textString = "@".join(res[:-1]).replace('"', "").replace("'", "")
                lang = res[-1].replace('"','').replace("'","")
                if len(lang) != 2:
                    lang = "en"
            else:
                textString = string.replace('"', "").replace("'", "")
                lang = "en"
            return [textString, lang]

        def genLabelTriple(self, node1: str, label: str, node2: str) -> bool:
            entity = self._node_2_entity(node1)
            textString, lang = TripleGenerator._process_text_string(node2)
            entity.add_label(textString, lang=lang)
            self.doc.kg.add_subject(entity)
            return True

        def genDescriptionTriple(self, node1: str, label: str, node2: str) -> bool:
            entity = self._node_2_entity(node1)
            textString, lang = TripleGenerator._process_text_string(node2)
            entity.add_description(textString, lang=lang)
            self.doc.kg.add_subject(entity)
            return True

        def genDescriptionTriple(self, node1: str, label: str, node2: str) -> bool:
            entity = self._node_2_entity(node1)
            textString, lang = TripleGenerator._process_text_string(node2)
            entity.add_description(textString, lang=lang)
            self.doc.kg.add_subject(entity)
            return True

        def genAliasTriple(self, node1: str, label: str, node2: str) -> bool:
            entity = self._node_2_entity(node1)
            textString, lang = TripleGenerator._process_text_string(node2)
            entity.add_alias(textString, lang=lang)
            self.doc.kg.add_subject(entity)
            return True

        def genPropDeclarationTriple(self, node1: str, label: str, node2: str) -> bool:
            prop = WDProperty(node1, self.propTypes[node1])
            self.doc.kg.add_subject(prop)
            return True

        def genNormalTriple(
            self, node1: str, label: str, node2: str, isQualifierEdge: bool) -> bool:
            from etk.wikidata.value import (
            Item,
            StringValue,
            TimeValue,
            QuantityValue,
            MonolingualText,
            GlobeCoordinate,
            ExternalIdentifier,
            URLValue,
            Precision
            )

            entity = self._node_2_entity(node1)
            # determine the edge type
            edgeType = self.propTypes[label]
            if edgeType == Item:
                OBJECT = WDItem(TripleGenerator.replaceIllegalString(node2.upper()))
            elif edgeType == TimeValue:
                # https://www.wikidata.org/wiki/Help:Dates
                # ^2013-01-01T00:00:00Z/11
                # ^8000000-00-00T00:00:00Z/3
                if re.compile("[0-9]{4}").match(node2):
                    try:                   
                        dateTimeString = node2 + "-01-01"
                        OBJECT = TimeValue(
                            value=dateTimeString, #TODO
                            calendar=Item("Q1985727"),
                            precision=Precision.year,
                            time_zone=0,
                        )
                    except:
                        return False
                else:
                    try:
                        dateTimeString, precision = node2[1:].split("/")
                        dateTimeString = dateTimeString[:-1] # remove "Z"
                        # 2016-00-00T00:00:00 case
                        if "-00-00" in dateTimeString:
                            dateTimeString = "-01-01".join(dateTimeString.split("-00-00"))
                        elif dateTimeString[8:10] == "00":
                            dateTimeString = dateTimeString[:8]+"01" + dateTimeString[10:]
                        OBJECT = TimeValue(
                            value=dateTimeString,
                            calendar=Item("Q1985727"),
                            precision=precision,
                            time_zone=0,
                        )
                    except: 
                        return False

                #TODO other than that, not supported. Creation of normal triple fails
                

            elif edgeType == GlobeCoordinate:
                latitude, longitude = node2[1:].split("/")
                OBJECT = GlobeCoordinate(
                    latitude, longitude, 0.0001, globe=StringValue("Earth")
                )

            elif edgeType == QuantityValue:
                # +70[+60,+80]Q743895
                res = re.compile("([\+|\-]?[0-9]+\.?[0-9]*)(?:\[([\+|\-]?[0-9]+\.?[0-9]*),([\+|\-]?[0-9]+\.?[0-9]*)\])?([U|Q](?:[0-9]+))?").match(node2).groups()
                amount, lower_bound, upper_bound, unit = res

                # Handle extra small numbers for now. TODO
                if TripleGenerator._is_invalid_decimal_string(amount) or TripleGenerator._is_invalid_decimal_string(lower_bound) or TripleGenerator._is_invalid_decimal_string(upper_bound):
                    return False
                amount = TripleGenerator._clean_number_string(amount)
                lower_bound = TripleGenerator._clean_number_string(lower_bound)
                upper_bound = TripleGenerator._clean_number_string(upper_bound)
                if unit != None:
                    if upper_bound != None and lower_bound != None:
                        OBJECT = QuantityValue(amount, unit=Item(unit),upper_bound=upper_bound,lower_bound=lower_bound)
                    else:
                        OBJECT = QuantityValue(amount, unit=Item(unit))
                else:
                    if upper_bound != None and lower_bound != None:
                        OBJECT = QuantityValue(amount, upper_bound=upper_bound,lower_bound=lower_bound)
                    else:
                        OBJECT = QuantityValue(amount)                   
            elif edgeType == MonolingualText:
                textString, lang = TripleGenerator._process_text_string(node2)
                OBJECT = MonolingualText(textString, lang)
            elif edgeType == ExternalIdentifier:
                OBJECT = ExternalIdentifier(node2)
            elif edge == URLValue:
                OBJECT = URLValue(node2)
            else:
                # treat everything else as stringValue
                OBJECT = StringValue(node2)
            if isQualifierEdge:
                # edge: e8 p9 ^2013-01-01T00:00:00Z/11
                # create qualifier edge on previous STATEMENT and return the updated STATEMENT
                if type(OBJECT) == WDItem:
                    self.doc.kg.add_subject(OBJECT)
                self.STATEMENT.add_qualifier(label.upper(), OBJECT)
                self.doc.kg.add_subject(self.STATEMENT) #TODO maybe can be positioned better for the edge cases.
    
            else:
                # edge: q1 p8 q2 e8
                # create brand new property edge and replace STATEMENT
                if type(OBJECT) == WDItem:
                    self.doc.kg.add_subject(OBJECT)
                if truthy:
                    self.STATEMENT = entity.add_truthy_statement(label.upper(), OBJECT) 
                else:
                    self.STATEMENT = entity.add_statement(label.upper(), OBJECT) 
                self.doc.kg.add_subject(entity)
            return True
        
        @staticmethod
        def _is_invalid_decimal_string(num_string):
            '''
            if a decimal string too small, return True TODO
            '''
            if num_string == None:
                return False
            else:
                if abs(float(num_string)) < 0.0001 and float(num_string) != 0:
                    return True
                return False        

        @staticmethod
        def _clean_number_string(num):
            from numpy import format_float_positional
            if num == None:
                return None
            else:
                return format_float_positional(float(num),trim="-")

        def entryPoint(self, line_number:int , edge: str):
            """
            generates a list of two, the first element is the determination of the edge type using corresponding edge type
            the second element is a bool indicating whether this is a valid property edge or qualifier edge.
            Call corresponding downstream functions
            """
            edgeList = edge.strip().split("\t")
            l = len(edgeList)
            if l!=4:
                return

            [node1, label, node2, eID] = edgeList
            node1, label, node2, eID = node1.strip(),label.strip(),node2.strip(),eID.strip()
            if line_number == 0: #TODO ignore header mode
                # by default a statement edge
                isQualifierEdge = False
                # print("#Debug Info: ",line_number, self.ID, eID, isQualifierEdge,self.STATEMENT)
                self.ID = eID
                self.corrupted_statement_id = None
            else:
                if node1 != self.ID:
                    # also a new statement edge
                    if self.read >= self.n:
                        self.serialize()
                    isQualifierEdge = False
                    # print("#Debug Info: ",line_number, self.ID, node1, isQualifierEdge,self.STATEMENT)
                    self.ID= eID
                    self.corrupted_statement_id = None
                else:
                # qualifier edge or property declaration edge
                    isQualifierEdge = True
                    if self.corrupted_statement_id == eID:
                        # Met a qualifier which associates with a corrupted statement
                        return
                    if label != "type" and node1 != self.ID:
                        # 1. not a property declaration edge and
                        # 2. the current qualifier's node1 is not the latest property edge id, throw errors.
                        if not self.ignore:
                            raise KGTKException(
                                "Node1 {} at line {} doesn't agree with latest property edge id {}.\n".format(
                                    node1, line_number, self.ID
                                )
                            )
            if label in self.labelSet:
                success = self.genLabelTriple(node1, label, node2)
            elif label in self.descriptionSet:
                success= self.genDescriptionTriple(node1, label, node2)
            elif label in self.aliasSet:
                success = self.genAliasTriple(node1, label, node2)
            elif label == "type":
                # special edge of prop declaration
                success = self.genPropDeclarationTriple(node1, label, node2)
            else:
                if label in self.propTypes:
                    success= self.genNormalTriple(node1, label, node2, isQualifierEdge)
                else:
                    if not self.ignore:
                        raise KGTKException(
                            "property {}'s type is unknown at line {}.\n".format(label, line_number)
                        )
                        success = False
            if (not success) and (not isQualifierEdge) and (not self.ignore):
                # We have a corrupted edge here.
                self.ignoreFile.write("Corrupted statement at line number: {} with id {} with current corrupted id {}\n".format(line_number, eID, self.corrupted_statement_id))
                self.ignoreFile.flush()
                self.corrupted_statement_id = eID
            else:
                self.read += 1
                self.corrupted_statement_id = None

        def serialize(self):
            """
            Seriealize the triples. Used a hack to avoid serializing the prefix again.
            """
            docs = self.etk.process_ems(self.doc)
            self.fp.write("\n\n".join(docs[0].kg.serialize("ttl").split("\n\n")[1:]))
            self.fp.flush()
            self.__reset()

        def __serialize_prefix(self):
            """
            This function should be called only once after the doc object is initialized.
            """
            docs = self.etk.process_ems(self.doc)
            self.fp.write(docs[0].kg.serialize("ttl").split("\n\n")[0] + "\n\n")
            self.fp.flush()
            self.__reset()

        def __reset(self):
            self.ID = None
            self.STATEMENT = None
            self.read = 0
            self.doc = self.__setDoc()

        def finalize(self):
            self.serialize()
        
        @staticmethod
        def replaceIllegalString(s:str)->str:
            return s.replace(":","-")

    generator = TripleGenerator(
        propFile=propFile,
        labelSet=labels,
        aliasSet=aliases,
        descriptionSet=descriptions,
        n=n,
        ignore=ignore,
        truthy=truthy
    )
    # process stdin
    num_line = 0
    while True:
        edge = sys.stdin.readline()
        if not edge:
            break
        if edge.startswith("#") or num_line == 0: # TODO First line omit
            num_line += 1
            continue
        else:
            generator.entryPoint(num_line, edge)
            num_line += 1
    generator.finalize()
