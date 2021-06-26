import sys
from functools import lru_cache
import sqlite3
import threading
import time

import pandas as pd

import kgtk.kypher.query as kyquery
import kgtk.cli.query as cliquery
import kgtk.kypher.sqlstore as sqlstore
from   kgtk.exceptions import KGTKException


DEFAULT_GRAPH_CACHE_FILE = cliquery.DEFAULT_GRAPH_CACHE_FILE
DEFAULT_INDEX_MODE = 'auto'
DEFAULT_LOG_LEVEL = 0
DEFAULT_MAX_RESULTS = 100000
DEFAULT_MAX_CACHE_SIZE = 1000

DEFAULT_CONFIG = {
    # defaults for API configuration parameters:
    'GRAPH_CACHE'        : DEFAULT_GRAPH_CACHE_FILE,
    'INDEX_MODE'         : DEFAULT_INDEX_MODE,
    'MAX_RESULTS'        : DEFAULT_MAX_RESULTS,
    'MAX_CACHE_SIZE'     : DEFAULT_MAX_CACHE_SIZE,
    'LOG_LEVEL'          : DEFAULT_LOG_LEVEL,
}


class KypherApi(object):
    """
    Kypher query API.  Manages a connection to a single graph cache DB,
    caches translated queries and (if requested) query results.
    The API can be configured with the constructor or by passing in a
    configuration object which can also be used to store additional
    user-defined configuration keys and values.
    """

    def __init__(self, config=None,
                 graphcache=None,
                 index=None,
                 maxresults=None,
                 maxcache=None,
                 loglevel=None):
        self.config = config or {}
        self.graph_cache = graphcache
        if graphcache is None:
            self.graph_cache = self.get_config('GRAPH_CACHE')
        self.index_mode = index
        if index is None:
            self.index_mode = self.get_config('INDEX_MODE')
        self.max_results = maxresults
        if maxresults is None:
            self.max_results = self.get_config('MAX_RESULTS')
        self.max_cache_size = maxcache
        if maxcache is None:
            self.max_cache_size = self.get_config('MAX_CACHE_SIZE')
        self.inputs = {}
        self.sql_store = None
        self.lock = threading.Lock()
        self.loglevel = loglevel
        if loglevel is None:
            self.loglevel = self.get_config('LOG_LEVEL')
        self.initialize()

    def initialize(self):
        if self.sql_store is not None:
            self.close()
        self.cached_queries = {}

    def close(self):
        if self.sql_store is not None:
            self.sql_store.close()
            self.sql_store = None
        self.clear_caches()

    def clear_caches(self):
        """Wipeout all query and LRU caches.
        """
        klass = type(self)
        for name in dir(klass):
            obj = getattr(klass, name, None)
            if hasattr(obj, 'cache_clear'):
                obj.cache_clear()
        self.initialize()

    def get_config(self, key, dflt=None):
        """Access a configuration value for 'key' with default 'dflt'.
        """
        dflt = dflt or DEFAULT_CONFIG.get(key)
        return self.config.get(key, dflt)

    def set_config(self, key, value):
        """Set the configuration value for 'key' to 'value'.
        This will also reset all query and LRU caches, since they might be specific
        to a particular configuration value.
        """
        self.clear_caches()
        self.config[key] = value

    def log(self, level, message):
        if self.loglevel >= level:
            header = '[%s query]:' % time.strftime('%Y-%m-%d %H:%M:%S')
            sys.stderr.write('%s %s\n' % (header, message))
            sys.stderr.flush()
    
    def get_sql_store(self):
        """Create a new SQL store object from the configured graph_cache file or return a cached value.
        """
        if self.sql_store is None:
            conn = sqlite3.connect(self.graph_cache, check_same_thread=False)
            self.sql_store = sqlstore.SqliteStore(dbfile=self.graph_cache, conn=conn, loglevel=self.loglevel)
        return self.sql_store

    def get_lock(self):
        """Return the lock object.
        """
        return self.lock

    def __enter__(self):
        """Lock context manager for 'with ... as api:' idiom.
        """
        if self.get_lock().locked():
            # for now for debugging:
            print('Waiting for Kypher API lock...')
        self.get_lock().acquire()
        return self

    def __exit__(self, *_exc):
        self.get_lock().release()

    def get_input_info(self, name):
        return self.inputs.get(name)

    def add_input(self, file, alias=None, name=None, load=False):
        info = self.get_input_info(file) or self.get_input_info(alias) or self.get_input_info(name)
        info = info or {}
        info['file'] = file
        self.inputs[file] = info
        if alias is not None:
            info['alias'] = alias
            self.inputs[alias] = info
        if name is not None:
            info['name'] = name
            self.inputs[name] = info
        if load or info.get('alias') is not None:
            # we have to preload if we use a DB alias, otherwise a rerun of a cached query will fail:
            store = self.get_sql_store()
            store.add_graph(file, alias=info.get('alias'))
        # clear query caches to avoid any file/alias confusions in cached queries:
        self.clear_caches()

    def get_input(self, key):
        info = self.get_input_info(key)
        if info is None:
            raise KGTKException('no input named by key: %s' % key)
        inp = info.get('alias')
        if inp is None:
            inp = info.get('file')
        return inp

    def get_all_inputs(self):
        inputs = set()
        for info in self.inputs.values():
            inputs.add(self.get_input(info['file']))
        return list(inputs)

    def clear_all_inputs(self):
        self.inputs = {}
        self.clear_caches()

    def lookup_query(self, name):
        return self.cached_queries.get(name)

    def get_query(self,
                  inputs=None,
                  name=None, maxcache=None,
                  loglevel=None,
                  index=None,
                  query=None,
                  match='()', where=None,
                  opt=None, owhere=None,
                  opt2=None, owhere2=None,
                  with_='*', wwhere=None,
                  ret='*', order=None,
                  skip=None, limit=None,
                  parameters={},
                  force=False,
                  **kwargs):
        """WRITE ME.
        """
        
        query = self.cached_queries.get(name)
        if query is not None:
            return query
        
        optionals = []
        opt and optionals.append((opt, owhere))
        opt2 and optionals.append((opt2, owhere2))
        # kwargs is an ordered dict, so the actual suffixes do not matter:
        for key, value in kwargs.items():
            if key.startwith('opt'):
                optionals.append([value, None])
            elif key.startwith('owhere'):
                optionals[-1][1] = value
            else:
                raise KGTKException('Unexpected keyword argument: %s' % key)

        inputs = kyquery.listify(inputs) or self.get_all_inputs()
        for inp in inputs:
            if self.get_input_info(inp) is None:
                self.add_input(inp)
        
        store = self.get_sql_store()
        if loglevel is None:
            loglevel = self.loglevel
        if index is None:
            index = self.index_mode
        if limit is None:
            limit = self.max_results
        if maxcache is None:
            maxcache = self.max_cache_size
        query = kyquery.KgtkQuery(inputs, store,
                                  loglevel=loglevel, index=index,
                                  query=query,
                                  match=match, where=where,
                                  optionals=optionals,
                                  with_=(with_, wwhere),
                                  ret=ret, order=order,
                                  skip=skip, limit=limit,
                                  parameters=parameters,
                                  force=force)
        
        query.defer_params = True
        sql, parameters = query.translate_to_sql()
        query.ensure_relevant_indexes(sql)
        # create memoizable execution wrapper:
        exec_wrapper = lambda api, q, s, p, f: api._exec_query(q, s, p, f)
        if maxcache > 0:
            exec_wrapper = lru_cache(maxsize=maxcache)(exec_wrapper)
        query = (query, sql, parameters, exec_wrapper)
        if name is not None:
            self.cached_queries[name] = query
        return query

    def _subst_params(self, params, substitutions):
        """Return a copy of the list 'params' modified by any 'substitutions'.
        Placeholder parameters in 'params' are marked as single-element tuples, e.g., ('NODE').
        """
        return tuple([isinstance(x, tuple) and substitutions.get(x[0], x[0]) or x for x in params])

    def _exec_query(self, query, sql, parameters, fmt):
        # TO DO: abstract this better in Kypher query API
        result = query.store.execute(sql, parameters)
        query.result_header = [query.unalias_column_name(c[0]) for c in result.description]
        if fmt in ('df', 'dataframe'):
            return pd.DataFrame(result, columns=query.result_header)
        else:
            # convert to list so we can reuse if we memoize:
            return list(result)

    def execute_query(self, query, fmt=None, **params):
        """Execute 'query' with the given 'params' and return the result in format 'fmt'. 
        By default the result is a list of tuples.  If format is 'df' a Pandas dataframe
        will be returned instead.  'query' must be an object generated by 'get_query'.
        """
        query, sql, parameters, exec_wrapper = query
        parameters = self._subst_params(parameters, params)
        result = exec_wrapper(self, query, sql, parameters, fmt)
        return result


"""
>>> import kgtk.kypher.api as kapi
>>> api = kapi.KypherApi(graphcache='..../wikidata-20210215-dwd-browser.sqlite3.db', loglevel=1)
>>> query = api.get_query(inputs='claims',
                          name='get_node_edges',
                          maxcache=100,
                          match='`%s`: (n)-[r]->(n2)' % 'claims',
                          where='n=$NODE',
                          ret='r as id, n as node1, r.label as label, n2 as node2')
... ... ... ... ... 
[2021-06-26 12:03:40 query]: SQL Translation:
---------------------------------------------
  SELECT graph_1_c1."id" "_aLias.id", graph_1_c1."node1" "_aLias.node1", graph_1_c1."label" "_aLias.label", graph_1_c1."node2" "_aLias.node2"
     FROM graph_1 AS graph_1_c1
     WHERE (graph_1_c1."node1" = ?)
     LIMIT ?
  PARAS: [('NODE',), 100000]
---------------------------------------------
>>> 
>>> api.execute_query(query, NODE='Q40', fmt='df')
                              id node1  label                                   node2
0    Q40-P1036-084620-8193d4f9-0   Q40  P1036                                "2--436"
1    Q40-P1081-0811b0-4f8b4eb7-0   Q40  P1081                                  +0.747
2    Q40-P1081-0937d9-77e2a41e-0   Q40  P1081                                  +0.861
3    Q40-P1081-132349-a529cefe-0   Q40  P1081                                  +0.835
4    Q40-P1081-1af44c-dacd9580-0   Q40  P1081                                  +0.764
..                           ...   ...    ...                                     ...
572   Q40-P949-f04fc2-1eaa977b-0   Q40   P949                             "000013315"
573   Q40-P950-3672f3-53465804-0   Q40   P950                              "XX450936"
574   Q40-P982-59891e-540db01d-0   Q40   P982  "caac77d1-a5c8-3e6e-8e27-90b44dcc1446"
575   Q40-P984-d87d6b-e2308567-0   Q40   P984                                   "AUT"
576   Q40-P998-05a2ec-b33435af-0   Q40   P998              "Regional/Europe/Austria/"

[577 rows x 4 columns]
>>> api.execute_query(query, NODE='Q41', fmt='df')
                              id node1  label                                   node2
0    Q41-P1036-682e2c-8ed5cb13-0   Q41  P1036                                "2--495"
1    Q41-P1081-02c2ed-926e1bf2-0   Q41  P1081                                  +0.866
2    Q41-P1081-0d7cc4-44b73d12-0   Q41  P1081                                  +0.762
3    Q41-P1081-11fb19-e2b6d2a2-0   Q41  P1081                                  +0.789
4    Q41-P1081-132349-6855d15e-0   Q41  P1081                                  +0.835
..                           ...   ...    ...                                     ...
594   Q41-P948-fc515d-8ee9b292-0   Q41   P948    "Kompsatos river bridge, Thrace.jpg"
595   Q41-P949-935996-53ecc964-0   Q41   P949                             "000979098"
596   Q41-P982-031a25-5b7e2e1a-0   Q41   P982  "803db0ca-b6ed-3bbc-aeb8-f89efd0a2168"
597   Q41-P984-f048da-9b23a812-0   Q41   P984                                   "GRE"
598   Q41-P998-b58b57-13f3de7d-0   Q41   P998               "Regional/Europe/Greece/"

[599 rows x 4 columns]
>>> api.execute_query(query, NODE='Q52353442')
[('Q52353442-P1006-235de5-5b24a9cf-0', 'Q52353442', 'P1006', '"321658140"'), ('Q52353442-P1015-cd5f62-c7e646d4-0', 'Q52353442', 'P1015', '"2100657"'), ('Q52353442-P106-Q82594-28c48a6c-0', 'Q52353442', 'P106', 'Q82594'), ('Q52353442-P108-Q37548-61855425-0', 'Q52353442', 'P108', 'Q37548'), ('Q52353442-P108-Q4614-dbb39b28-0', 'Q52353442', 'P108', 'Q4614'), ('Q52353442-P1153-bef441-003e2488-0', 'Q52353442', 'P1153', '"7004618158"'), ('Q52353442-P1416-Q6030821-708a6b3e-0', 'Q52353442', 'P1416', 'Q6030821'), ('Q52353442-P166-Q18748039-fc276466-0', 'Q52353442', 'P166', 'Q18748039'), ('Q52353442-P166-Q18748042-3c446357-0', 'Q52353442', 'P166', 'Q18748042'), ('Q52353442-P184-Q6123694-2032855e-0', 'Q52353442', 'P184', 'Q6123694'), ('Q52353442-P185-Q102343472-373f0ed5-0', 'Q52353442', 'P185', 'Q102343472'), ('Q52353442-P19-Q2807-92d8e80c-0', 'Q52353442', 'P19', 'Q2807'), ('Q52353442-P1960-601bc1-1d1f5261-0', 'Q52353442', 'P1960', '"NDmGsCgAAAAJ"'), ('Q52353442-P21-Q6581072-f653b32c-0', 'Q52353442', 'P21', 'Q6581072'), ('Q52353442-P213-49066c-8fc0d32c-0', 'Q52353442', 'P213', '"0000 0000 3762 2146"'), ('Q52353442-P214-1c576a-648c3580-0', 'Q52353442', 'P214', '"18334143"'), ('Q52353442-P244-5d352f-f85a8c96-0', 'Q52353442', 'P244', '"nb2005019080"'), ('Q52353442-P2456-b325a5-5b751548-0', 'Q52353442', 'P2456', '"88/2686"'), ('Q52353442-P2671-2e7fe8-0a9466a9-0', 'Q52353442', 'P2671', '"/g/11grpt57xn"'), ('Q52353442-P27-Q29-1c7b6b5c-0', 'Q52353442', 'P27', 'Q29'), ('Q52353442-P31-Q5-b46dfbd7-0', 'Q52353442', 'P31', 'Q5'), ('Q52353442-P496-8da475-0e4b3f94-0', 'Q52353442', 'P496', '"0000-0001-8465-8341"'), ('Q52353442-P549-828a1d-27c6ad2a-0', 'Q52353442', 'P549', '"50269"'), ('Q52353442-P569-5069f4-2d4c6716-0', 'Q52353442', 'P569', '^1960-01-01T00:00:00Z/7'), ('Q52353442-P69-Q190080-0c0aa4a5-0', 'Q52353442', 'P69', 'Q190080'), ('Q52353442-P69-Q25864-c80df10a-0', 'Q52353442', 'P69', 'Q25864'), ('Q52353442-P735-Q21045740-8683ff36-0', 'Q52353442', 'P735', 'Q21045740'), ('Q52353442-P7859-05a463-a41340d1-0', 'Q52353442', 'P7859', '"lccn-nb2005019080"'), ('Q52353442-P864-a1d270-2d5566dc-0', 'Q52353442', 'P864', '"81100348498"'), ('Q52353442-P949-cf102a-4130dc7e-0', 'Q52353442', 'P949', '"002253159"')]
>>> api.close()
"""
