"""
Import CSV file module
"""


def parser():
    return {
        'help': 'Import a CSV file into KGTK format'
    }


def add_arguments(parser):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """
    parser.add_argument(action="store", type=str, dest="filename", metavar='filename', help='filename here')
    parser.add_argument("-d", "--delimiter", action="store", type=str, dest="delimiter")
    parser.add_argument("-e", "--header", action="store", type=str, dest="delimiter")
    parser.add_argument( "-nc", "--node-columns", action="store", nargs="*", dest="NODE_COLS")
    parser.add_argument("-ec", "--edge-columns", action="store", nargs="*", dest="EDGE_COLS")

def run(filename, delimiter):
    # import modules locally
    import socket
    print(f'Now importing {filename} with a delimiter {delimiter} and header {header}')
