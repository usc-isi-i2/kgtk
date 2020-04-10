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
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


results = get_results(endpoint_url, query)
print(results)

with open("../data/wikidataProps.json","w") as fp:
    json.dump(results,fp)

