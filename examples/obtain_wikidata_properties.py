# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/

import sys
import json
from SPARQLWrapper import SPARQLWrapper, JSON

endpoint_url = "https://query.wikidata.org/sparql"

query = """SELECT ?property ?propertyType WHERE {
    ?property a wikibase:Property .
  ?property wikibase:propertyType ?propertyType .
    SERVICE wikibase:label {
      bd:serviceParam wikibase:language "en" .
   }
 }
"""


def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (
        sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


dataTypeMappings = {
    "WikibaseItem": "item",
    "Time": "time",
    "GlobeCoordinate": "globe-coordinate",
    "Quantity": "quantity",
    "Monolingualtext": "monolingualtext",
    "String": "string",
    "ExternalId":"external-identifier",
    "Url":"url"
}
results = get_results(endpoint_url, query)

with open("../data/wikidataProps.tsv", "w") as fp:
    for prop in results["results"]["bindings"]:
        pID = prop["property"]["value"].split("/")[-1]
        pType = prop["propertyType"]["value"].split("#")[-1]
        pType = dataTypeMappings.get(pType,"string")
        fp.write(pID + "\tproperty_type\t" + pType+"\n")