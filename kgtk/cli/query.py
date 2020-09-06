"""
Test driver for KGTK Kypher query engine
"""

import sys
import os
import os.path
import tempfile
import io

from kgtk.exceptions import KGTKException


DEFAULT_GRAPH_CACHE_FILE = os.path.join(
    tempfile.gettempdir(), 'kgtk-graph-cache-%s.sqlite3.db' % os.environ.get('USER', ''))

def parser():
    return {
        'help': 'Query one or more KGTK files with Kypher',
        'description': 'Query one or more KGTK files with Kypher.',
    }

def add_arguments_extended(parser, parsed_shared_args):
    parser.accept_shared_argument('_debug')
    parser.accept_shared_argument('_expert')

    parser.add_argument('--input', '-i', metavar='INPUT', action='append', dest='inputs',
                        help="one or more named input files to query (maybe compressed)")
    parser.add_argument('--query', default=None, action='store', dest='query',
                        help="complete Kypher query combining all clauses," +
                        " if supplied, all other specialized clause arguments will be ignored")
    parser.add_argument('--match', metavar='PATTERN', default='()', action='store', dest='match',
                        help="MATCH pattern of a Kypher query, defaults to universal node pattern `()'")
    parser.add_argument('--where', metavar='CLAUSE', default=None, action='store', dest='where',
                        help="WHERE clause of a Kypher query")
    parser.add_argument('--return', metavar='CLAUSE', default='*', action='store', dest='return_',
                        help="RETURN clause of a Kypher query (defaults to *)")
    parser.add_argument('--order-by', metavar='CLAUSE', default=None, action='store', dest='order',
                        help="ORDER BY clause of a Kypher query")
    parser.add_argument('--skip', metavar='CLAUSE', default=None, action='store', dest='skip',
                        help="SKIP clause of a Kypher query")
    parser.add_argument('--limit', metavar='CLAUSE', default=None, action='store', dest='limit',
                        help="LIMIT clause of a Kypher query")
    parser.add_argument('--graph-cache', default=DEFAULT_GRAPH_CACHE_FILE, action='store', dest='graph_cache_file',
                        help="database cache where graphs will be imported before they are queried"
                        + " (defaults to per-user temporary file)")
    parser.add_argument('-o', '--out', default='-', action='store', dest='output',
                        help="output file to write to, if `-' (the default) output goes to stdout")

def import_modules():
    """Import command-specific modules that are only needed when we actually run.
    """
    mod = sys.modules[__name__]
    import sh
    setattr(mod, "sh", sh)
    import csv
    setattr(mod, "csv", csv)
    import kgtk.kypher.query as kyquery
    setattr(mod, "kyquery", kyquery)
    import kgtk.kypher.sqlstore as sqlstore
    setattr(mod, "sqlstore", sqlstore)

def run(**options):
    """Run Kypher query according to the provided command-line arguments.
    """
    try:
        import_modules()
        debug = options.get('_debug', False)
        expert = options.get('_expert', False)
        loglevel = debug and 1 or 0
        
        if debug and expert:
            loglevel = 2
            print('OPTIONS:', options)
            
        inputs = options.get('inputs') or []
        if len(inputs) == 0:
            raise KGTKException('At least one named input file needs to be supplied')

        output = options.get('output')
        if output == '-':
            output = sys.stdout
        if isinstance(output, str):
            output = open(output, mode='wt')

        try:
            graph_cache = options.get('graph_cache_file')
            store = sqlstore.SqliteStore(graph_cache, create=not os.path.exists(graph_cache), loglevel=loglevel)
        
            query = kyquery.KgtkQuery(inputs, store, loglevel=loglevel,
                                      query=options.get('query'),
                                      match=options.get('match'),
                                      where=options.get('where'),
                                      ret=options.get('return_'),
                                      order=options.get('order'),
                                      skip=options.get('skip'),
                                      limit=options.get('limit'))
            result = query.execute()

            csvwriter = csv.writer(output, dialect=None, delimiter='\t', quoting=csv.QUOTE_NONE, quotechar=None)
            csvwriter.writerow(query.result_header)
            csvwriter.writerows(result)
            output.flush()
        finally:
            store.close()
            if output is not None and output is not sys.stdout:
                output.close()
        
    except sh.SignalException_SIGPIPE:
        # hack to work around Python3 issue when stdout is gone when we try to report an exception;
        # without this we get an ugly 'Exception ignored...' msg when we quit with head or a pager:
        sys.stdout = os.fdopen(1)
    except KGTKException as e:
        raise e
    except Exception as e:
        raise KGTKException(str(e) + '\n')
