"""
Remove columns from a file.
"""


import sys

def parser():
    return {
        'help': 'Remove columns from a file '
    }


def add_arguments(parser):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """
    parser.add_argument('-dt', "--datatype", action="store", type=str, dest="datatype", help="Datatype of the input file, e.g., tsv or csv.", default="tsv")
    parser.add_argument( "-c", "--columns", action="store", type=str, dest="columns", help="Columns to remove as a comma-separated string, e.g., id,docid")
    parser.add_argument('input', nargs='?', action='store') #, action="store", default=sys.stdin) #, required=True)

def run(datatype, columns, input): 
    # import modules locally
    import socket
    import sh

    if input:
        string = open(input).read()
        sh.mlr('--tsv', 'cut', '-x', '-f', columns, string, _out=sys.stdout, _err=sys.stderr)
    elif not sys.stdin.isatty():
        print('reading from stdin')
        sh.mlr('--tsv', 'cut', '-x', '-f', columns, _in=sys.stdin, _out=sys.stdout, _err=sys.stderr, _piped=True,  _iter=True)
    else:
        parser.print_help()

