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
    parser.add_argument(metavar="input", dest="input", action="store", default=sys.stdin) #, required=True)

def run(datatype, columns, input): 
    # import modules locally
    import socket
    import sh
    sh.mlr('--tsv', 'cut', '-x', '-f', columns, input, _out=sys.stdout, _err=sys.stderr)
    #sh.mlr('--%s' % datatype, "cut", "-x", '-f', columns, input)

