from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore
from rdflib.query import ResultException


class TruthyUpdater:
    def __init__(self, endpoint, dryrun=False, user=None, passwd=None):
        self.endpoint = SPARQLUpdateStore(endpoint,
                                          default_query_method='POST')
        if user:
            self.endpoint.setCredentials(user, passwd)
        self.dryrun = dryrun

    def build_truthy(self, np_list):
        self.insert_truthy_rank(np_list)
        self.delete_normal_rank(np_list)

    def update(self, query):
        if self.dryrun:
            action = 'INSERT' if 'INSERT' in query else 'DELETE'
            query = query.replace(action, 'CONSTRUCT')
            # print(query)
            try:
                res = self.endpoint.query(query)
                print('### About to {} following triples:'.format(action))
                for row in res:
                    print(' '.join(e.n3() for e in row))
            except ResultException:
                pass
        else:
            self.endpoint.update(query)

    def insert_truthy_rank(self, np_list):
        values = ' '.join('( wd:%(node)s p:%(p)s ps:%(p)s psn:%(p)s wdt:%(p)s wdtn:%(p)s )' % {'node': n, 'p': p}
                          for n, p in np_list)
        query = '''
        INSERT {
          ?statement a wikibase:BestRank .
          ?node ?wdt ?psv ;
                ?wdtn ?psnv .
        } WHERE {
          %s
            {
                ?node ?p ?statement .
                ?statement wikibase:rank wikibase:PreferredRank ;
                           ?ps ?psv .
                OPTIONAL { ?statement ?psn ?psnv }
                FILTER NOT EXISTS { ?statement a wikibase:BestRank }
            }
            UNION
            {
              ?node ?p ?statement .
              ?statement wikibase:rank wikibase:NormalRank ;
                         ?ps ?psv .
              OPTIONAL { ?statement ?psn ?psnv }
              FILTER NOT EXISTS { ?statement a wikibase:BestRank }
              FILTER NOT EXISTS { ?node ?p [ wikibase:rank wikibase:PreferredRank ] }
            }
        }
        ''' % ('VALUES (?node ?p ?ps ?psn ?wdt ?wdtn ) { %s }' % values)
        self.update(query)

    def delete_normal_rank(self, np_list):
        values = ' '.join('( wd:%(node)s p:%(p)s wdt:%(p)s wdtn:%(p)s )' % {'node': n, 'p': p} for n, p in np_list)
        query = '''
          DELETE {
            ?statement a wikibase:BestRank .
            ?node ?wdt ?value ;
              ?wdtn ?no .
          } WHERE {
            %s
            ?node ?p ?statement ;
                  ?p [ wikibase:rank wikibase:PreferredRank ] .
            ?statement a wikibase:BestRank ;
                       wikibase:rank wikibase:NormalRank .
          }
        ''' % ('VALUES (?node ?p ?wdt ?wdtn ) { %s }' % values)
        self.update(query)
