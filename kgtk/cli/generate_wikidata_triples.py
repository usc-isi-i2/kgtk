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
        type=bool,
        help="the default is to not generate truthy triples. Specify this option to generate truthy triples. NOTIMPLEMENTED",
        dest="truthy",
    )
    parser.add_argument(
        "-ig",
        "--ig",
        action="store",
        type=bool,
        help="if set to yes, ignore various kinds of exceptions and mistakes and log them to a log file with line number in input file, rather than stopping. logging NOTIMPLEMENTED",
        dest="ignore",
    )


def run(
    labels: str,
    aliases: str,
    descriptions: str,
    propFile: str,
    n: int,
    truthy: bool = False,
    ignore: bool = True,
):
    """
    Arguments here should be defined in `add_arguments` first.
    The return value (integer) will be the return code in shell. It will set to 0 if no value returns.
    Though you can return a non-zero value to indicate error, raise exceptions defined in kgtk.exceptions is preferred
    since this gives user an unified error code and message.
    """
    # import modules locally
    import sys
    import warnings
    import re
    import requests
    from typing import TextIO
    try:
        from etk.etk import ETK
        from etk.knowledge_graph import KGSchema
        from etk.etk_module import ETKModule
        from etk.wikidata.entity import WDItem, WDProperty
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
        from kgtk.exceptions import KGTKException
    except:
        #TODO The only exception not handled by KGTKException.
        print("Please check the etk and spacy libraries.")
        return

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
        ):
            self.ignore = ignore
            self.propTypes = self.__setPropTypes(propFile)
            self.labelSet, self.aliasSet, self.descriptionSet = self.__setSets(
                labelSet, aliasSet, descriptionSet
            )
            # TODO handle standard output
            self.fp = destFp
            self.n = int(n)
            self.read = 0
            # serialize prfix
            kg_schema = KGSchema()
            kg_schema.add_schema("@prefix : <http://isi.edu/> .", "ttl")
            self.etk = ETK(kg_schema=kg_schema, modules=ETKModule)
            self.doc = self.__setDoc()
            self.__serialize_prefix()

        def __setPropTypes(self, propFile: str):
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

        def genLabelTriple(self, node1: str, label: str, node2: str) -> bool:
            if node1 in self.propTypes:
                entity = WDProperty(node1.upper(), self.propTypes[node1])
            else:
                entity = WDItem(node1.upper())
            if "@" in node2:
                node2, lang = node2.split("@")
                if len(lang) != 2:
                    lang="en" #TODO need to fix the ill-formatted language short code
                entity.add_label(node2.replace('"', "").replace("'", ""), lang=lang)
            else:
                entity.add_label(
                    node2.replace('"', "").replace("'", ""), lang="en"
                )  # default
            self.doc.kg.add_subject(entity)
            return True

        def genDescriptionTriple(self, node1: str, label: str, node2: str) -> bool:
            if node1 in self.propTypes:
                entity = WDProperty(node1.upper(), self.propTypes[node1])
            else:
                entity = WDItem(node1.upper())
            if "@" in node2:
                node2, lang = node2.split("@")
                entity.add_description(
                    node2.replace('"', "").replace("'", ""), lang=lang
                )
            else:
                entity.add_description(
                    node2.replace('"', "").replace("'", ""), lang="en"
                )  # default
            self.doc.kg.add_subject(entity)
            return True

        def genDescriptionTriple(self, node1: str, label: str, node2: str) -> bool:
            if node1 in self.propTypes:
                entity = WDProperty(node1.upper(), self.propTypes[node1])
            else:
                entity = WDItem(node1.upper())
            if "@" in node2:
                node2, lang = node2.split("@")
                entity.add_description(
                    node2.replace('"', "").replace("'", ""), lang=lang
                )
            else:
                entity.add_description(
                    node2.replace('"', "").replace("'", ""), lang="en"
                )  # default
            self.doc.kg.add_subject(entity)
            return True

        def genAliasTriple(self, node1: str, label: str, node2: str) -> bool:
            if node1 in self.propTypes:
                entity = WDProperty(node1.upper(), self.propTypes[node1])
            else:
                entity = WDItem(node1.upper())

            if "@" in node2:
                node2, lang = node2.split("@")
                entity.add_alias(node2.replace('"', "").replace("'", ""), lang=lang)
            else:
                entity.add_alias(
                    node2.replace('"', "").replace("'", ""), lang="en"
                )  # default
            self.doc.kg.add_subject(entity)
            return True

        def genPropDeclarationTriple(self, node1: str, label: str, node2: str) -> bool:
            prop = WDProperty(node1.upper(), self.propTypes[node1])
            self.doc.kg.add_subject(prop)
            return True

        def genNormalTriple(
            self, node1: str, label: str, node2: str, isPropEdge: bool
        ) -> bool:
            """
            The normal triple's type is determined by 
            1. label's datatype in prop_types.tsv
            2. kgtk format convention of node2 field

            Update the self.STATEMENT
            """
            # determine the node type [property|item]
            if node1 in self.propTypes:
                entity = WDProperty(node1.upper(), self.propTypes[node1])
            else:
                entity = WDItem(node1.upper())
            # determine the edge type
            edgeType = self.propTypes[label]
            if edgeType == Item:
                OBJECT = Item(node2.upper())

            elif edgeType == TimeValue:
                # https://www.wikidata.org/wiki/Help:Dates
                # ^201301-01T00:00:00Z/11
                dateTimeString, precision = node2[1:].split("/")
                dateString, timeString = dateTimeString.split("T")
                OBJECT = TimeValue(
                    value=dateString,
                    calendar=Item("Q1985727"),
                    precision=precision,
                    time_zone=0,
                )

            elif edgeType == GlobeCoordinate:
                latitude, longitude = node2[1:].split("/")
                OBJECT = GlobeCoordinate(
                    latitude, longitude, 0.0001, globe=StringValue("Earth")
                )

            elif edgeType == QuantityValue:
                try:
                    amount, unit = (
                        re.compile("([\+|\-]?[0-9]+\.?[0-9]*)U([0-9]+)")
                        .match(node2)
                        .groups()
                    )
                    OBJECT = QuantityValue(amount=float(amount), unit=Item(unit))
                except:
                    OBJECT = QuantityValue(amount=float(node2))
            elif edgeType == MonolingualText:
                try:
                    textString, lang = node2.split("@")
                    OBJECT = MonolingualText(textString, lang)
                except:
                    OBJECT = MonolingualText(textString, "en")
            elif edgeType == ExternalIdentifier:
                OBJECT = ExternalIdentifier(node2)
            elif edge == URLValue:
                OBJECT = URLValue(node2)
            else:
                # treat everything else as stringValue
                OBJECT = StringValue(node2)
            if isPropEdge:
                # edge: q1 p8 q2 e8
                # create brand new property edge and replace STATEMENT
                self.STATEMENT = entity.add_statement(label.upper(), OBJECT)
            else:
                # edge: e8 p9 ^2013-01-01T00:00:00Z/11
                # create qualifier edge on previous STATEMENT and return the updated STATEMENT
                self.STATEMENT.add_qualifier(label.upper(), OBJECT)
            self.doc.kg.add_subject(self.STATEMENT)
            return True

        def entryPoint(self, line_number:int , edge: str):
            """
            edge: "p8\tp1\t'hasFather'@en\te5\n", a line in the edges.tsv file
            generates a list of two, the first element is the determination of the edge type using corresponding edge type
            the second element is a bool indicating whether this is a valid property edge or qualifier edge.
            Call corresponding downstream functions
            """
            edgeList = edge.strip().split("\t")
            l = len(edgeList)
            if l == 4:
                # property statement edge
                # try to serialize when a new property statement is encountered.
                if self.read >= self.n:
                    self.serialize()
                isPropEdge = True
                [node1, label, node2, eID] = edgeList
                node1, label, node2, eID = (
                    node1.strip(),
                    label.strip(),
                    node2.strip(),
                    eID.strip(),
                )
                if eID == self.ID:
                    if not self.ignore:
                        raise KGTKException(
                            "id {} of edge {} at line {} duplicates latest property statement id {}.\n".format(
                                eID, edge, line_number, self.ID
                            )
                        )
                    return
                else:
                    self.ID = eID
            elif l == 3:
                # qualifier edge or property declaration edge
                isPropEdge = False
                [node1, label, node2] = edgeList
                node1, label, node2 = node1.strip(), label.strip(), node2.strip()
                if label != "type" and node1 != self.ID:
                    # 1. not a property declaration edge and
                    # 2. the current qualifier's node1 is not the latest property edge id, throw errors.
                    if not self.ignore:
                        raise KGTKException(
                            "Node1 {} of qualifier edge {} at line {} doesn't agree with latest property edge id {}.\n".format(
                                node1, edge, line_number, self.ID
                            )
                        )
                    return
            else:
                if not self.ignore:
                    raise KGTKException("Length {} of edge {} at line {} is not valid.\n".format(l, edge, line_number))
                return

            if label in self.labelSet:
                self.read += self.genLabelTriple(node1, label, node2)
            elif label in self.descriptionSet:
                self.read += self.genDescriptionTriple(node1, label, node2)
            elif label in self.aliasSet:
                self.read += self.genAliasTriple(node1, label, node2)
            elif label == "type":
                # special edge of prop declaration
                self.read += self.genPropDeclarationTriple(node1, label, node2)
            else:
                if label in self.propTypes:
                    self.read += self.genNormalTriple(node1, label, node2, isPropEdge)
                else:
                    if not self.ignore:
                        raise KGTKException(
                            "property {}'s type is unknown as in edge {} at line {}.\n".format(label, edge, line_number)
                        )

        def serialize(self):
            """
            Seriealize the triples. Used a hack to avoid serializing the prefix again.
            """
            docs = self.etk.process_ems(self.doc)
            self.fp.write("\n\n".join(docs[0].kg.serialize("ttl").split("\n\n")[1:]))
            self.__reset()

        def __serialize_prefix(self):
            """
            This function should be called only once after the doc object is initialized.
            """
            docs = self.etk.process_ems(self.doc)
            self.fp.write(docs[0].kg.serialize("ttl").split("\n\n")[0] + "\n\n")
            self.__reset()

        def __reset(self):
            self.ID = None
            self.STATEMENT = None
            self.read = 0
            self.doc = self.__setDoc()

        def finalize(self):
            return

    generator = TripleGenerator(
        propFile=propFile,
        labelSet=labels,
        aliasSet=aliases,
        descriptionSet=descriptions,
        n=n,
        ignore=True
    )
    # process stdin
    for num, edge in enumerate(sys.stdin.readlines()):
        if num == 0:
            continue
        else:
            generator.entryPoint(num, edge)
    generator.serialize()
    generator.finalize()
