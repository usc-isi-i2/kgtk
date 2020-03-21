"""
Import CSV file module
"""


def parser():
    return {
        'help': 'this is a function to import CSV file'
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

def run(filename, delimiter):
    print(f'Now importing {filename} with a delimiter {delimiter} and header {header}')
