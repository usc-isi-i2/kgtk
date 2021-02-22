"""
Run Kypher query engine.
"""

import sys
import os
import os.path
import tempfile
import io
import argparse

from kgtk.exceptions import KGTKException

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles

DEFAULT_GRAPH_CACHE_FILE = os.path.join(
    tempfile.gettempdir(), 'kgtk-graph-cache-%s.sqlite3.db' % os.environ.get('USER', ''))

def parser():
    desc = ('Query one or more KGTK files with Kypher.\n' +
            'IMPORTANT: input can come from stdin but chaining queries is not yet supported.')
    return {
        'help': desc,
        'description': desc,
    }

EXPLAIN_MODES = ('plan', 'full', 'expert')
INDEX_MODES = ('auto', 'expert', 'quad', 'triple', 'node1+label', 'node1', 'label', 'node2', 'none')

class InputOptionAction(argparse.Action):
    """Special-purpose argparse action that associates an input-specific option
    (such as an alias) to the most recently parsed input file.  NOTE: the 'dest'
    value will be used as the key for the specific option in 'input_file_options'.
    """
    def __call__(self, parser, namespace, values, option_string=None):
        input_options = getattr(namespace, 'input_file_options', {}) or {}
        inputs = KGTKArgumentParser.get_input_file_list(getattr(namespace, 'input_files', []))
        if len(inputs) < 1:
            raise KGTKException('out-of-place input option: %s' % option_string)
        # normalize path objects to strings:
        input_file = str(inputs[-1])
        # handle boolean args (also requires nargs=0):
        if self.type == bool:
            values = True
        # we use self.dest as the key for this particular option:
        input_options.setdefault(input_file, {})[self.dest] = values
        setattr(namespace, 'input_file_options', input_options)

def add_arguments_extended(parser: KGTKArgumentParser, parsed_shared_args):
    parser.accept_shared_argument('_debug')
    parser.accept_shared_argument('_expert')

    parser.add_input_file(options=["-i", "--input-files"], dest='input_files', allow_list=True, default_stdin=False, allow_stdin=True,
                        who="One or more input files to query (maybe compressed).")
    parser.add_argument('--as', metavar='NAME', default={}, action=InputOptionAction, dest='alias',
                        help="alias name to be used for preceding input")
    # future extension:
    #parser.add_argument('--in-memory', default=False, type=bool, nargs=0, action=InputOptionAction, dest='in_memory',
    #                    help="load the preceding input into a temporary in-memory table only")
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
    parser.add_argument('--para', metavar='NAME=VAL', action='append', dest='regular_paras',
                        help="zero or more named value parameters to be passed to the query")
    parser.add_argument('--spara', metavar='NAME=VAL', action='append', dest='string_paras',
                        help="zero or more named string parameters to be passed to the query")
    parser.add_argument('--lqpara', metavar='NAME=VAL', action='append', dest='lqstring_paras',
                        help="zero or more named LQ-string parameters to be passed to the query")
    parser.add_argument('--no-header', action='store_true', dest='no_header',
                        help="do not generate a header row with column names")
    parser.add_argument('--index', metavar='MODE', nargs='?', action='store', dest='index',
                        choices=INDEX_MODES, const=INDEX_MODES[0], default=INDEX_MODES[0], 
                        help="control column index creation according to MODE"
                        + " (%(choices)s, default: %(const)s)")
    parser.add_argument('--explain', metavar='MODE', nargs='?', action='store', dest='explain',
                        choices=EXPLAIN_MODES, const=EXPLAIN_MODES[0], 
                        help="explain the query execution and indexing plan according to MODE"
                        + " (%(choices)s, default: %(const)s)."
                        + " This will not actually run or create anything.")
    parser.add_argument('--graph-cache', default=DEFAULT_GRAPH_CACHE_FILE, action='store', dest='graph_cache_file',
                        help="database cache where graphs will be imported before they are queried"
                        + " (defaults to per-user temporary file)")
    parser.add_argument('-o', '--out', default='-', action='store', dest='output',
                        help="output file to write to, if `-' (the default) output goes to stdout."
                        + " Files with extensions .gz, .bz2 or .xz will be appropriately compressed.")

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

def parse_query_parameters(regular=[], string=[], lqstring=[]):
    """Parse and DWIM any supplied parameter values and return as a dictionary.
    """
    para_specs = {'regular': regular, 'string': string, 'lqstring': lqstring}
    parameters = {}
    for ptype in ('regular', 'string', 'lqstring'):
        for pspec in para_specs[ptype]:
            eqpos = pspec.find('=')
            if eqpos < 0:
                raise KGTKException('Illegal parameter spec: %s' % pspec)
            name = pspec[0:eqpos]
            value = pspec[eqpos+1:]
            if ptype == 'string':
                value = kyquery.dwim_to_string_para(value)
            if ptype == 'lqstring':
                value = kyquery.dwim_to_lqstring_para(value)
            parameters[name] = value
    return parameters

def run(input_files: KGTKFiles,
        **options):
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

        # normalize path objects to strings:
        inputs = [str(f) for f in KGTKArgumentParser.get_input_file_list(input_files)]
        if len(inputs) == 0:
            raise KGTKException('At least one input needs to be supplied')

        output = options.get('output')
        if output == '-':
            output = sys.stdout
        if isinstance(output, str):
            output = sqlstore.open_to_write(output, mode='wt')

        parameters = parse_query_parameters(regular=options.get('regular_paras') or [],
                                            string=options.get('string_paras') or [],
                                            lqstring=options.get('lqstring_paras') or [])

        try:
            graph_cache = options.get('graph_cache_file')
            store = sqlstore.SqliteStore(graph_cache, create=not os.path.exists(graph_cache), loglevel=loglevel)
        
            query = kyquery.KgtkQuery(inputs, store, loglevel=loglevel,
                                      options=options.get('input_file_options'),
                                      query=options.get('query'),
                                      match=options.get('match'),
                                      where=options.get('where'),
                                      ret=options.get('return_'),
                                      order=options.get('order'),
                                      skip=options.get('skip'),
                                      limit=options.get('limit'),
                                      parameters=parameters,
                                      index=options.get('index'))
            
            explain = options.get('explain')
            if explain is not None:
                result = query.explain(explain)
                output.write(result)
            else:
                result = query.execute()
                # we are forcing \n line endings here instead of \r\n, since those
                # can be re/imported efficiently with the new SQLite import command;
                # we force `escapechar' back to None to avoid generation of double
                # backslashes as in 'Buffalo \'66', which in turn will now raise errors
                # if separators in fields are encountered (which seems what we want):
                csvwriter = csv.writer(output, dialect=None, delimiter='\t',
                                       quoting=csv.QUOTE_NONE, quotechar=None,
                                       lineterminator='\n',
                                       escapechar=None)
                if not options.get('no_header'):
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
