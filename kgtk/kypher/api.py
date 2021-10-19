import sys
from functools import lru_cache
import sqlite3
import threading
import time
import re
import io
import csv

import kgtk.kypher.query as kyquery
import kgtk.cli.query as cliquery
import kgtk.kypher.sqlstore as sqlstore
from   kgtk.exceptions import KGTKException

# avoid KGTK dependency on pandas and only import them if needed:
_have_pandas = False
def _import_pandas():
    global _have_pandas
    mod = sys.modules[__name__]
    import pandas as pd
    setattr(mod, "pd", pd)
    _have_pandas = True


# NOTES:
# - sqlite3 module already caches parsed SQL queries (100 by default),
#   so there is no need for prepared statements
# - executemany cannot be used to handle sets of input parameters,
#   it only works for modification commands, not selects


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


class KypherQuery(object):
    """
    Cachable Kypher query object.  Caches query translations and
    (if requested) query results.  Methods will generally not be called
    directly but through the linked API object.
    """

    def __init__(self, api, **kwargs):
        """Create a query object linked to the KypherApi 'api'.  All other
        arguments are passed to 'KypherQuery._define' (which see).
        """
        if not isinstance(api, KypherApi):
            raise KGTKException('query needs to be linked to existing API object')
        self.api = api
        self.kgtk_query = None
        self.sql = None
        self.parameters = None
        self.exec_wrapper = None
        self.definition_args = kwargs
        self.timestamp = -1
        self._define(**kwargs)

    def _define(self,
                inputs=None, doc=None,
                name=None, maxcache=None,
                query=None,
                match='()', where=None,
                opt=None, owhere=None,
                opt2=None, owhere2=None,
                with_='*', wwhere=None,
                ret='*', order=None,
                skip=None, limit=None,
                parameters={},
                force=False,
                index=None, loglevel=None,
                **kwargs):
        """Internal constructor which generates a cached query translation and a
        LRU-cachable results structure (if requested).  See 'KypherApi.get_query'
        for documentation of arguments.
        """
        
        if self.kgtk_query is not None:
            raise KGTKException('query has already been defined')

        inputs = kyquery.listify(inputs) or self.api.get_all_inputs()
        norm_inputs = []
        for inp in inputs:
            if self.api.get_input_info(inp) is None:
                self.api.add_input(inp)
            norm_inputs.append(self.api.get_input(inp))
        inputs = norm_inputs

        self.docstring = doc
        
        optionals = []
        opt and optionals.append((self._subst_graph_handles(opt, inputs), owhere))
        opt2 and optionals.append((self._subst_graph_handles(opt2, inputs), owhere2))
        # kwargs is an ordered dict, so the actual suffixes do not matter:
        for key, value in kwargs.items():
            if key.startswith('opt'):
                optionals.append([self._subst_graph_handles(value, inputs), None])
            elif key.startswith('owhere'):
                optionals[-1][1] = value
            else:
                raise KGTKException('Unexpected keyword argument: %s' % key)

        store = self.api.get_sql_store()
        if loglevel is None:
            loglevel = self.api.loglevel
        if index is None:
            index = self.api.index_mode
        # since we are loading results into memory, we are not using unlimited as the default:
        if limit is None:
            limit = self.api.max_results
        # -1 forces unlimited results:
        elif limit == -1:
            limit = None
        if maxcache is None:
            maxcache = self.api.max_cache_size
        self.kgtk_query = kyquery.KgtkQuery (
            inputs, store,
            loglevel=loglevel, index=index,
            query=query,
            match=self._subst_graph_handles(match, inputs), where=where,
            optionals=optionals,
            with_=(with_, wwhere),
            ret=ret, order=order,
            skip=skip, limit=limit,
            parameters=parameters,
            force=force)
        
        self.kgtk_query.defer_params = True
        state = self.kgtk_query.translate_to_sql()
        self.sql = state.get_sql()
        self.parameters = state.get_parameters()
        self.kgtk_query.ensure_relevant_indexes(state)
        # create memoizable execution wrapper:
        self.exec_wrapper = lambda q, p, f: q._exec(p, f)
        if maxcache > 0:
            self.exec_wrapper = lru_cache(maxsize=maxcache)(self.exec_wrapper)
        if name is not None:
            self.api.cached_queries[name] = self
        self.timestamp = self.api.timestamp
        return self

    PSEUDO_GRAPH_HANDLE_REGEX = re.compile('`?\$(?P<handle>[^$`:\s]+)`?:')

    def _subst_graph_handles(self, match_pattern, inputs):
        """Substitute any pseudo graph handles in 'match_pattern' that are relevant to one
        of 'inputs' with their canonical input file or alias (backtick quoted if necessary).
        Any backtick quotes around a handle will be dropped automatically first.
        """
        cursor = 0
        out = io.StringIO()
        for match in self.PSEUDO_GRAPH_HANDLE_REGEX.finditer(match_pattern):
            handle = match.group('handle')
            info = self.api.get_input_info(handle)
            if info is not None and info['handle']:
                # we found a match for a pseudo-handle, check whether it is relevant:
                for inp in inputs:
                    if self.api.get_input_info(inp) == info:
                        # handle is for one of the listed 'inputs':
                        out.write(match_pattern[cursor:match.start()])
                        cursor = match.end()
                        out.write('`%s`:' % self.api.get_input(handle))
                        break
        if cursor == 0:
            return match_pattern
        else:
            out.write(match_pattern[cursor:])
            return out.getvalue()

    def clear(self):
        """Clear all currently cached information for this query.
        Subsequent executions will regenerate everything as needed.
        """
        self.kgtk_query = None
        self.sql = None
        self.parameters = None
        self.exec_wrapper = None
        self.timestamp = -1

    def refresh(self):
        """Check whether cached values are still valid relative to the current state of the API.
        If not, regenerate all cached structures according to the stored definition arguments.
        """
        if self.timestamp < self.api.timestamp:
            self.clear()
            self._define(**self.definition_args)

    def _subst_params(self, params, substitutions):
        """Return a copy of the list 'params' modified by any 'substitutions'.
        Placeholder parameters in 'params' are marked as single-element tuples, e.g., ('NODE').
        """
        subst_params = []
        # we can't do this easily with a list comprehension, since False or 0 are valid substitutions:
        for x in params:
            if isinstance(x, tuple):
                subst_params.append(substitutions.get(x[0], x[0]))
            else:
                subst_params.append(x)
        # we return the result as a tuple which can be hashed for memoization:
        return tuple(subst_params)

    def _exec(self, parameters, fmt):
        """Internal query execution wrapper that can easily be memoized.
        """
        # TO DO: abstract some of this better in KgtkQuery API
        kgtk_query = self.kgtk_query
        result = kgtk_query.store.execute(self.sql, parameters)
        if kgtk_query.result_header is None:
            kgtk_query.result_header = [kgtk_query.unalias_column_name(c[0]) for c in result.description]
        if fmt is None:
            # convert to list so we can reuse if we memoize:
            return tuple(result)
        # allow types and their names:
        fmt = hasattr(fmt, '__name__') and fmt.__name__ or str(fmt)
        if fmt == 'iter':
            return result
        elif fmt == 'tuple':
            return tuple(result)
        elif fmt == 'list':
            return list(result)
        elif fmt in ('df', 'dataframe', 'DataFrame'):
            if not _have_pandas:
                _import_pandas()
            return pd.DataFrame(result, columns=kgtk_query.result_header)
        # TO DO: consider supporting namedtuple and/or sqlite3.Row as row_factory types
        #        (for sqlite3.Row we have the issue that aliases become keys())
        else:
            raise KGTKException('unsupported query result format: %s' % fmt)

    def execute(self, fmt=None, **params):
        """Execute this query with the given 'params' and return the result in format 'fmt'. 
        By default the result is a list of tuples (see 'KypherApi.execute_query' for other options).
        'params' should be a list of key/value pairs for the unbound Kypher parameters in the query.
        For example, the Kypher parameter '$NODE' can be bound with 'NODE=<some value>'.
        """
        self.refresh()
        parameters = self._subst_params(self.parameters, params)
        result = self.exec_wrapper(self, parameters, fmt)
        return result

    def execute_to_file(self, file=sys.stdout, noheader=False, **params):
        """Execute this query with the given 'params' and write the result to the file or
        file-like object 'file' in KGTK format.  Output a header unless 'noheader' is true.
        """
        self.refresh()
        if hasattr(self.exec_wrapper, 'cache_clear'):
            # if this is a re-call of a caching query, ensure it is cleared,
            # since the result iterator was used up in the previous call:
            self.exec_wrapper.cache_clear()
        parameters = self._subst_params(self.parameters, params)
        try:
            out = open(file, 'w') if isinstance(file, str) else file
            if not hasattr(out, 'write'):
                raise KGTKException('expected file or file-like object')
            result = self.exec_wrapper(self, parameters, iter)
            csvwriter = csv.writer(out, dialect=None, delimiter='\t',
                                   quoting=csv.QUOTE_NONE, quotechar=None,
                                   lineterminator='\n', escapechar=None)
            if not noheader:
                csvwriter.writerow(self.get_result_header())
            csvwriter.writerows(result)
        finally:
            if isinstance(file, str):
                out.close()

    def get_result_header(self, error=True):
        """Return the list of column names for this query.  This requires the query to have
        run at least once (also again after caches were cleared).
        """
        self.refresh()
        header = self.kgtk_query.result_header
        if header is None and error:
            raise KGTKException('query needs to be run at least once to access its result header')
        return header


class KypherApi(object):
    """
    Kypher query API.  Manages a connection to a single graph cache DB,
    caches translated queries and (if requested) query results.
    The API can be configured with the constructor or by passing in a
    configuration object which can also be used to store additional
    user-defined configuration keys and values.

    Many of the API options are direct analogs of corresponding options of the
    KGTK 'query' command.  Please consult the 'query' manual for more details.
    """

    def __init__(self,
                 graphcache=None,
                 index=None,
                 maxresults=None,
                 maxcache=None,
                 loglevel=None,
                 config=None):
        """Create a new API object and initialize a number of configuration values.
        'graphcache' should be a filename for a Kypher graph cache to create or reuse.
        It uses the same default as the --graph-cache option of the 'query' command.

        'index' specifies the default indexing mode which defaults to the value of the
        'INDEX_MODE' property in the provided user or default configuration.  It uses
        the same default value as the --index option of the 'query' command.  'index'
        can be overridden for individual queries.

        'maxresults' specifies the default maximum number of results to be returned by
        a query which defaults to the 'MAX_RESULTS' property in the provided user or default 
        configuration.  Different from the --limit option of the 'query' command, API query
        results are not unbounded by default (since they might exhaust available RAM).  Use
        -1 to allow unbounded results.  'maxresults' can be overridden for individual queries.

        'maxcache' specifies the default number of per-query results to memoize in an LRU
        cache which defaults to the 'MAX_CACHE_SIZE' property in the provided user or default 
        configuration.  Setting this to 0 disables query result caching.  'maxcache' can be
        overridden for individual queries.

        'loglevel' controls the verbosity of logging output.  It defaults to the value of the
        'LOG_LEVEL' property in the provided user or default configuration.  The default is 0
        and values 1 and 2 correspond to --debug and --expert modes of the 'query' command.
        'loglevel' can be overridden for individual queries.

        'config' can be used to initialize configuration values from a user-provided
        configuration object which may have additional user-defined key/value pairs.
        Standard configuration values for the keys described above will default to their
        values in 'DEFAULT_CONFIG' if no user-defined values are provided.
        """
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
        self.sql_store = None
        self.lock = threading.Lock()
        self.loglevel = loglevel
        if loglevel is None:
            self.loglevel = self.get_config('LOG_LEVEL')
        self.timestamp = -1
        self._initialize()

    def _initialize(self):
        """Re/initialize internal data structures.
        """
        if self.sql_store is not None:
            self.close()
        self.inputs = {}
        self.cached_queries = {}
        self.timestamp += 1

    def close(self):
        """Close the connection to the database and clear all caches and information.
        """
        if self.sql_store is not None:
            self.sql_store.close()
            # avoid recursion in '_initialize':
            self.sql_store = None
        self.clear_caches()
        self._initialize()

    def clear(self):
        """Close the connection to the database and clear all caches and information.
        """
        self.close()

    def clear_caches(self):
        """Clear all query translation and LRU result caches.  Queries that were not given
        a name but were assigned to any variables or slots will rebuild automatically upon next
        execution.  However, to release their storage they will need to be cleared manually
        with 'q.clear()' or disconnected from variables or objects pointing to them.
        """
        klass = type(self)
        for name in dir(klass):
            obj = getattr(klass, name, None)
            if hasattr(obj, 'cache_clear'):
                obj.cache_clear()
        for query in self.cached_queries.values():
            query.clear()
        self.timestamp += 1

    def clear_queries(self):
        """Clear all currently defined queries and any caches depending on them.
        """
        self.clear_caches()
        self.cached_queries = {}
        
    def clear_inputs(self):
        """Clear all currently defined inputs and any caches depending on them.
        """
        self.clear_caches()
        self.inputs = {}


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
        """Output log 'message' if the current log level is at least 'level'.
        """
        if self.loglevel >= level:
            header = '[%s query]:' % time.strftime('%Y-%m-%d %H:%M:%S')
            sys.stderr.write('%s %s\n' % (header, message))
            sys.stderr.flush()
    
    def get_sql_store(self):
        """Create a new SQL store object from the configured graph_cache file or return a cached value.
        """
        if self.sql_store is None:
            conn = sqlite3.connect(self.graph_cache, check_same_thread=False)
            # don't do this for now, since we get the aliases as keys() which would require further mapping:
            #conn.row_factory = sqlite3.Row
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
        """Return the info structure associated with input 'name', which maybe an input file name,
        input file alias or API-local name.
        """
        return self.inputs.get(name)

    def add_input(self, file, alias=None, name=None, handle=False, load=False):
        """Add input 'file' as one of the input files known by this API instance.

        If 'alias' is not None, use it as the name of input inside the graph cache
        (equivalent to the --as option of the 'query' command).  

        If 'name' is given, use it as an additional API-local name to refer to the input.

        If 'handle' is True, allow 'alias' or 'name' to be used as a pseudo-graph handle
        in match patterns using the Kypher parameter syntax.  These handles are 'pseudo'
        only, since they get replaced with their full respective input file name *before*
        any Kypher parsing is done.  For example, if we have the name 'mygraph' defined
        for an input, it can be used as '$mygraph: (x)-[]->(y), ...' in a strict or
        optional match pattern.  The syntax of handle names is less restrictive than for
        real Kypher variables and can contain any character except whitespace and '$`:'.
        
        If 'load' is true, load the input file immediately, unless it is already in the
        graph cache.  Using this function is only needed if an input alias and/or API name
        is desired, or if data loading should be forced.  Otherwise, inputs can be specified 
        directly to 'get_query' (which see).  NOTE: providing an alias implies 'load=True'.
        """
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
        info['handle'] = handle
        if load or info.get('alias') is not None:
            # we have to preload if we use a DB alias, otherwise a rerun of a cached query will fail:
            store = self.get_sql_store()
            store.add_graph(file, alias=info.get('alias'))
        # clear query caches to avoid any file/alias confusions in cached queries:
        self.clear_caches()

    def get_input(self, key):
        """Get the canonical input named by 'key' so it can be used with 'get_query'.
        'key' maybe an input file name, input file alias or API-local name.
        """
        info = self.get_input_info(key)
        if info is None:
            raise KGTKException('no input named by key: %s' % key)
        inp = info.get('alias')
        if inp is None:
            inp = info.get('file')
        return inp

    def get_all_inputs(self):
        """Get the canonical names of all currently defined inputs.
        """
        inputs = set()
        for info in self.inputs.values():
            inputs.add(self.get_input(info['file']))
        return list(inputs)

    def lookup_query(self, name):
        """Return a cached query with 'name' if it exists, otherwise return None.
        This is useful as a cheap check before a fully parameterized call to 'get_query'.
        """
        return self.cached_queries.get(name)

    def _get_query(self, query, error=True):
        """Internal accessor that allows transparent 'query' access via objects or names.
        """
        if isinstance(query, KypherQuery):
            return query
        kypher_query = self.cached_queries.get(query)
        if kypher_query is not None:
            return kypher_query
        elif error:
            raise KGTKException('cannot find query with name: %s' % query)
        else:
            return None

    def get_query(self,
                  inputs=None, doc=None,
                  name=None, maxcache=None,
                  query=None,
                  match='()', where=None,
                  opt=None, owhere=None,
                  opt2=None, owhere2=None,
                  with_='*', wwhere=None,
                  ret='*', order=None,
                  skip=None, limit=None,
                  parameters={},
                  force=False,
                  index=None,
                  loglevel=None,
                  **kwargs):
        
        """Construct or reuse a cached query.  Many of the options here directly correspond
        to one of the options of the KGTK 'query' command, so we only describe core differences.

        'inputs' is a single or list of input file names or aliases just as they would be supplied
        to the 'query' command.  If inputs were defined with aliases or API-internal names, 'get_input'
        should be used to access their canonical name to ensure the proper file name or alias usage.
        All inputs will automatically be added via 'add-input' (which is a no-op if they already exist).
        If 'inputs' is None, the list of all currently defined inputs will be supplied in random order.
        In that case, all match clauses need to explicitly specify the graph they apply to.

        'doc' can be used to attach a documentation string to the query.

        If 'name' is given, the constructed query object will be cached in the API object under that name.
        Methods such as 'execute_query' can then be called with a query name or object.  Even if no name is
        used, the query can still be executed multiple times by saving it to a variable or slot.
        If a cached query with 'name' already exists, 'get_query' returns that query immediately without
        any further translation and processing.  That means a named 'get_query' call can be used in a
        processing loop without incurring any notable overhead after the first call (besides assembling
        and passing the parameters to 'get_query').

        'maxcache' specifies the number of per-query results to memoize in an LRU cache which defaults
        to the number defined during creation of the API object.  To disable LRU caching for this query,
        set 'maxcache' to 0.  NOTE: the number specifies the maximum number of query results to cache,
        but each result may have an arbitrarily large number of rows, so the storage consumed by this
        cache might become potentially much larger than indicated by 'maxcache' alone.

        'query' can be a fully specified Kypher query (just as the --query option of the 'query' command).

        'match' is the strict match clause of a Kypher query (just as the --match option of the 'query'
        command).  Match clauses should be properly qualified with graph handles to refer to the appropriate
        input in 'inputs'.  Use 'get_input' to access the proper canonical input names.  For example:
        ... 'match="`%s`: (n1)-[r]->(n2)" % api.get_input("my_graph")', ...

        'where' is the where clause of a strict match clause (just as --where following --match for 'query').
        
        'opt' is the first optional match clause (just as --opt for 'query').  As with 'match', appropriate
        graph handles should generally be used.

        'owhere' is the where clause of the first optional match clause (just as --where following the first
        --opt clause in 'query').

        'opt2' is the second optional match clause (just as the second --opt for 'query').

        'owhere2' is the where clause of the second optional match clause (just as --where following the
        second --opt clause in 'query').

        Additional optional clauses can be specified with 'opt3', 'owhere3', 'opt4', 'owhere4', etc.  They
        will be ordered in their order of specification, not according to their suffixes which can really be
        arbitrary, as long as they have not been previously used.

        'with_' is the with clause of a Kypher query (just as the --with option of the 'query' command).

        'wwhere' is the where clause of the with clause (or global where) (just as the --where clause following
        --with or the --where: option of the 'query' command).

        'ret' is the return clause of a Kypher query (just as the --return option of the 'query' command).

        'order' is the order-by clause of a Kypher query (just as the --order-by option of the 'query' command).

        'skip' is the skip clause of a Kypher query (just as the --skip option of the 'query' command).

        'limit' is the limit clause of a Kypher query (just as the --limit option of the 'query' command).
        However, the default for 'limit' is not unbounded but the number of 'maxresults' configured during
        creation of the API object.  To specify unlimited results, use -1 as the value for 'limit'.

        'parameters' is a fixed dictionary of Kypher parameter name/value pairs to use in each invocation
        of this query (parameter names do not include the leading dollar sign).  Any parameters whose values
        are not defined in this dictionary will need to be bound in each call to 'execute'.

        'force' specifies the value of the --force option in a 'query' command.

        'index' specifies the indexing mode to use for this query which defaults to the number defined during
        creation of the API object (just like the --index option of the 'query' command).

        'loglevel' controls the verbosity of logging output and defaults to the number defined during
        creation of the API object (similar to the --debug and --expert options of the 'query' command).
        """
        
        kypher_query = self._get_query(name, error=False)
        if kypher_query is not None:
            return kypher_query
        kypher_query = KypherQuery(
            self, inputs=inputs, doc=doc, name=name, maxcache=maxcache,
            query=query, match=match, where=where, opt=opt, owhere=owhere, opt2=opt2, owhere2=owhere2,
            with_=with_, wwhere=wwhere, ret=ret, order=order, skip=skip, limit=limit, parameters=parameters,
            force=force, index=index, loglevel=loglevel,
            **kwargs)
        return kypher_query

    def execute_query(self, query, fmt=None, **params):
        """Execute 'query' with the given 'params' and return the result in format 'fmt'
        ('query' may be a name or object).  By default the result is a tuple of tuples.
        Supported formats are 'iter' (the sqlite result iterator), 'tuple' (a tuple list
        of result tuples), 'list' (a list of tuples), or 'df' (a Pandas dataframe which 
        requires the pandas module to be available - 'dataframe' or 'DataFrame' are also
        supported as format names).  Type objects can also be used if available instead
        of their names.  IMPORTANT: If 'iter' is chosen, the result cannot effectively be
        cached, since the iterator will be exhausted after first traversal.
        'params' should be a list of key/value pairs for the unbound Kypher parameters in
        'query' (those not specified in the 'parameters' argument to 'get_query').
        For example, the Kypher parameter '$NODE' can be bound with 'NODE=<some value>'.
        """
        return self._get_query(query).execute(fmt=fmt, **params)

    def execute_query_to_file(self, query, file=sys.stdout, noheader=False, **params):
        """Execute 'query' with the given 'params' and write the result to the file or
        file-like object 'file' in KGTK format.  Output a header unless 'noheader' is true.
        """
        query.execute_to_file(file=file, noheader=noheader, **params)

    def get_query_result_header(self, query, error=True):
        """Return the list of column names for 'query' (which may be a name or object).
        This requires the query to have run at least once (also again after caches were cleared).
        An error is raised if this is called too early unless 'error' is false.
        """
        return self._get_query(query).get_result_header(error=error)


"""
# Example 1:

>>> import kgtk.kypher.api as kapi

# we don't supply a graph cache file, so the default in /tmp will be used:
>>> api = kapi.KypherApi()

# we define some inputs with API-local names for easy reference, but the
# filenames will be used as the actual input names inside the graph cache:
>>> api.add_input('examples/docs/query-graph.tsv', name='graph', handle=True)
>>> api.add_input('examples/docs/query-works.tsv', name='works', handle=True)
>>> api.add_input('examples/docs/query-quals.tsv', name='quals')

# This defines a query object which we will refer to by its name later.
# Since log level is 1, it displays the SQL translation it produces.
# This call only prepares the query, it does not actually run it.
# We use the Kypher parameter $ORG to later query for different orgs.
# Parameters cannot be used in the match clause, so we use it in 'where':
>>> api.get_query(name='work-info',
                  # we qualify each clause with a graph handle, since all inputs are supplied to the query by default;
                  # we use pseudo graph handles here which is easiest (using handle=True in add_input above):
                  match='$works: (p)-[r:works]->(c), $graph: (p)-[:name]->(n)',
                  where='c=$ORG',
                  # here we splice in the graph handle directly, just for illustration of the separate mechanism;
                  # note how we use backtick quoting to escape special characters in file names:
                  opt=  '`%s`: (r)-[:starts]->(s)' % api.get_input('quals'),
                  ret=  'c as company, p as employee, n as name, s as start',
                  loglevel=1)
... ... ... ... ... 
[2021-06-28 20:51:13 query]: SQL Translation:
---------------------------------------------
  SELECT graph_2_c1."node2" "_aLias.company", graph_2_c1."node1" "_aLias.employee", graph_3_c2."node2" "_aLias.name", graph_1_c3."node2" "_aLias.start"
     FROM graph_2 AS graph_2_c1
     INNER JOIN graph_3 AS graph_3_c2
     ON graph_2_c1."node1" = graph_3_c2."node1"
        AND graph_2_c1."label" = ?
        AND graph_3_c2."label" = ?
        AND (graph_2_c1."node2" = ?)
     LEFT JOIN graph_1 AS graph_1_c3
     ON graph_2_c1."id" = graph_1_c3."node1"
        AND graph_1_c3."label" = ?
     LIMIT ?
  PARAS: ['works', 'name', ('ORG',), 'starts', 100000]
---------------------------------------------
<kgtk.kypher.api.KypherQuery object at 0x7ff099bb0950>

# Now we run the query with a specific binding for $ORG.
# By default, the result is returned as a list of tuples:
>>> api.execute_query('work-info', ORG='ACME')
[('ACME', 'Hans', "'Hans'@de", '^1984-12-17T00:03:12Z/11')]

# Here we ask with a different binding and using a pandas
# dataframe as the result format (requires pandas to be installed):
>>> api.execute_query('work-info', fmt='df', ORG='Kaiser')
  company employee       name                     start
0  Kaiser     Otto  'Otto'@de                      None
1  Kaiser      Joe      "Joe"  ^1996-02-23T08:02:56Z/09

# Here we call 'get_query' with the same arguments as above.
# Since a cached query for 'work-info' already exists, it is used
# without requiring any additional translation (thus no log output).
# Since the query is asked with a binding we queried for before,
# the cached result set is used without any query execution at all.
# This time we use the 'execute' method on the query object directly:
>>> api.get_query(name='work-info',
                  match='$works: (p)-[r:works]->(c), $graph: (p)-[:name]->(n)',
                  where='c=$ORG',
                  opt=  '`%s`: (r)-[:starts]->(s)' % api.get_input('quals'),
                  ret=  'c as company, p as employee, n as name, s as start',
                  loglevel=1).execute(fmt='df', ORG='Kaiser')
... ... ... ... ...   
company employee       name                     start
0  Kaiser     Otto  'Otto'@de                      None
1  Kaiser      Joe      "Joe"  ^1996-02-23T08:02:56Z/09

# if we clear caches first, the query gets translated from scratch:
>>> api.clear_caches()
>>> api.get_query(name='work-info',
                  match='$works: (p)-[r:works]->(c), $graph: (p)-[:name]->(n)',
                  where='c=$ORG',
                  opt=  '`%s`: (r)-[:starts]->(s)' % api.get_input('quals'),
                  ret=  'c as company, p as employee, n as name, s as start',
                  loglevel=1).execute(fmt='df', ORG='Kaiser')
... ... ... ... ... 
[2021-06-29 12:40:01 query]: SQL Translation:
---------------------------------------------
  SELECT graph_2_c1."node2" "_aLias.company", graph_2_c1."node1" "_aLias.employee", graph_3_c2."node2" "_aLias.name", graph_1_c3."node2" "_aLias.start"
     FROM graph_2 AS graph_2_c1
     INNER JOIN graph_3 AS graph_3_c2
     ON graph_2_c1."node1" = graph_3_c2."node1"
        AND graph_2_c1."label" = ?
        AND graph_3_c2."label" = ?
        AND (graph_2_c1."node2" = ?)
     LEFT JOIN graph_1 AS graph_1_c3
     ON graph_2_c1."id" = graph_1_c3."node1"
        AND graph_1_c3."label" = ?
     LIMIT ?
  PARAS: ['works', 'name', ('ORG',), 'starts', 100000]
---------------------------------------------
  company employee       name                     start
0  Kaiser     Otto  'Otto'@de                      None
1  Kaiser      Joe      "Joe"  ^1996-02-23T08:02:56Z/09

# clearing caches preserves query definitions, so we don't have to define them again:
>>> api.clear_caches()
>>> api.execute_query('work-info', fmt='df', ORG='Kaiser')
[2021-06-29 13:10:03 query]: SQL Translation:
---------------------------------------------
  SELECT graph_2_c1."node2" "_aLias.company", graph_2_c1."node1" "_aLias.employee", graph_3_c2."node2" "_aLias.name", graph_1_c3."node2" "_aLias.start"
     FROM graph_2 AS graph_2_c1
     INNER JOIN graph_3 AS graph_3_c2
     ON graph_2_c1."node1" = graph_3_c2."node1"
        AND graph_2_c1."label" = ?
        AND graph_3_c2."label" = ?
        AND (graph_2_c1."node2" = ?)
     LEFT JOIN graph_1 AS graph_1_c3
     ON graph_2_c1."id" = graph_1_c3."node1"
        AND graph_1_c3."label" = ?
     LIMIT ?
  PARAS: ['works', 'name', ('ORG',), 'starts', 100000]
---------------------------------------------
  company employee       name                     start
0  Kaiser     Otto  'Otto'@de                      None
1  Kaiser      Joe      "Joe"  ^1996-02-23T08:02:56Z/09

>>> api.close()
>>>


# Example 2:

# here we supply the location of an existing Wikidata graph cache:
>>> api = kapi.KypherApi(graphcache='..../wikidata-20210215-dwd-browser.sqlite3.db', loglevel=1)

# we know it has a graph named 'claims', so we use that directly in the query instead of 'add_input()':
>>> query = api.get_query(inputs='claims',
                          name='get_node_edges',
                          maxcache=100,
                          match='(n)-[r]->(n2)',
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

# here we query with the query object instead of its name:
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
>>> 
"""
