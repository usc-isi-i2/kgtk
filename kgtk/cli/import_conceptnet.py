"""
Import ConceptNet file to KGTK.
"""


import sys

def parser():
    return {
        'help': 'Import ConceptNet into KGTK.' 
    }


def add_arguments(parser):
    """
    Parse arguments
    Args:
            parser (argparse.ArgumentParser)
    """
    # '$label == "/r/DefinedAs" && $node2=="/c/en/number_zero"'
    parser.add_argument(action="store", type=str, dest="filename", metavar='filename', help='filename here')
    parser.add_argument('--english_only', action="store_true", help="Only english conceptnet?")
    parser.add_argument('--sort', action="store_true", help="Should we sort the file on s-p-o?")


def run(filename, english_only, sort):
    # import modules locally
    import sys # type: ignore
    from kgtk.exceptions import kgtk_exception_auto_handler
    import csv

    def row_to_edge(row):
        return '\t'.join(row) + '\n'

    try:
        in_columns=['assertion','rel','subj','obj','metadata']
        out_columns=['node1', 'label', 'node2']
        with open(filename, 'r') as f:
            reader = csv.reader(f, delimiter='\t', quotechar='"')
            sys.stdout.write(row_to_edge(out_columns))
            for row in reader:
                new_row=[row[2], row[1], row[3]]
                if not english_only or (new_row[0].startswith('/c/en/') and new_row[2].startswith('/c/en/')):
                    sys.stdout.write(row_to_edge(new_row))

    except Exception as e:
            kgtk_exception_auto_handler(e)
