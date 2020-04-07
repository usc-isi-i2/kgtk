"""
Sort file based on a column.
"""


import sys

def parser():
    return {
        'help': 'Sort file based on a column.'
    }


def add_arguments(parser):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """
    parser.add_argument('-dt', "--datatype", action="store", type=str, dest="datatype", help="Datatype of the input file, e.g., tsv or csv.", default="tsv")
    parser.add_argument( "-c", "--column", action="store", type=str, dest="column", help="Property/column to sort on.")
    parser.add_argument(metavar="input", dest="input", action="store", default=sys.stdin) 

def run(datatype, column, input): 
    # import modules locally
    import socket
    import sh # type: ignore
    sh.mlr('--%s' % datatype, 'sort', '-f', column, input, _out=sys.stdout, _err=sys.stderr)

