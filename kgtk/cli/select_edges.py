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
    parser.add_argument('-dt', "--datatype", action="store", type=str, dest="datatype", help="Datatype of the input file, e.g., tsv or csv.", default="tsv")
    parser.add_argument( "-p", "--property", action="store", type=str, dest="property", help="Property/column to filter on.")
    parser.add_argument( "-v", "--value", action="store", type=str, dest="value", help="Property/column value to filter on.")
    parser.add_argument(metavar="input", dest="input", action="store", default=sys.stdin) #, required=True)

def run(datatype, property, value, input): 
    # import modules locally
    import socket
    import sh
    filter='$%s == "%s"' % (property, value)
    sh.mlr('--%s' % datatype, 'filter', filter, input, _out=sys.stdout, _err=sys.stderr)

