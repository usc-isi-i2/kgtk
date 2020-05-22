"""
Filter rows by subject, predicate, object values.
"""


import sys

def parser():
    return {
        'help': 'Filter rows by subject, predicate, object values.'
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
    parser.add_argument('--subj', action="store", type=str, dest='subj_col', help="Subject column, default is node1", default="node1")
    parser.add_argument('--pred', action="store", type=str, dest='pred_col', help="Predicate column, default is label", default="label")
    parser.add_argument('--obj', action="store", type=str, dest='obj_col', help="Object column, default is node2", default="node2")
    parser.add_argument("input", nargs="?", action="store") 


def run(datatype, pattern, input, subj_col, pred_col, obj_col):
    # import modules locally
    import sh # type: ignore
    from kgtk.exceptions import kgtk_exception_auto_handler

    props=[subj_col, pred_col, obj_col]

    def prepare_filter(property, prop_pattern):
        prop_pattern=prop_pattern.strip()
        prop_filters=[]
        for value in prop_pattern.split(','):
            value=value.strip()
            value_filter='$%s == "%s"' % (property, value)
            prop_filters.append(value_filter)
        return '(%s)' %  ' || '.join(prop_filters)


    try:
        n1_filter, lbl_filter,n2_filter=pattern.split(';')

        filters=[]
        for i, col_filter in enumerate([n1_filter, lbl_filter, n2_filter]):
            if col_filter.strip():
                ready=prepare_filter(props[i], col_filter)
                filters.append(ready)

        filter_str='\'%s\'' % ' && '.join(filters)

        if filter_str:
            if input:
                sh.mlr('--%slite' % datatype, 'filter', filter_str, input, 
                        _out=sys.stdout, _err=sys.stderr)
            elif not sys.stdin.isatty():
                sh.mlr('--%slite' % datatype, 'filter', filter_str, 
                        _in=sys.stdin, _out=sys.stdout, _err=sys.stderr)
    except Exception as e:
        kgtk_exception_auto_handler(e)
