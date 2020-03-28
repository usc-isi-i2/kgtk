"""
Filter rows by a property value.
"""


import sys

def parser():
    return {
        'help': 'Filter rows by a property value.'
    }


def add_arguments(parser):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """
    # '$label == "/r/DefinedAs" && $node2=="/c/en/number_zero"'
    parser.add_argument('-dt', "--datatype", action="store", type=str, dest="datatype", help="Datatype of the input file, e.g., tsv or csv.", default="tsv")
    parser.add_argument('-p', '--pattern', action="store", type=str, dest="pattern", help="Pattern to filter on, for instance, \" ; P154 ; \" ")
    parser.add_argument("input", nargs="?", action="store") 

def run(datatype, pattern, input): 
    # import modules locally
    import socket
    import sh

    props=['node1', 'label', 'node2']

    def prepare_filter(property, prop_pattern):
        prop_pattern=prop_pattern.strip()
        prop_filters=[]
        for value in prop_pattern.split(','):
            value=value.strip()
            value_filter='$%s == "%s"' % (property, value)
            prop_filters.append(value_filter)
        return '(%s)' %  ' || '.join(prop_filters)

    print('helo', pattern)
    n1_filter, lbl_filter,n2_filter=pattern.split(';')

    print('helo')
    filters=[]
    for i, col_filter in enumerate([n1_filter, lbl_filter, n2_filter]):
        if col_filter.strip():
            ready=prepare_filter(props[i], col_filter)
            filters.append(ready)
            print(ready)

    filter_str='\'%s\'' % ' && '.join(filters)

    print(filter_str)
    if filter_str:
        if input:
            sh.mlr('--%s' % datatype, 'filter', filter_str, input, 
                    _out=sys.stdout, _err=sys.stderr)
        elif not sys.stdin.isatty():
            sh.mlr('--%s' % datatype, 'filter', filter_str, 
                    _in=sys.stdin, _out=sys.stdout, _err=sys.stderr)

