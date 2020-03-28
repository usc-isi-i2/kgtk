"""
Import CSV file module
"""


def parser():
    return {
        'help': 'Import Visual Genome into KGTK format'
    }


def add_arguments(parser):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """
    parser.add_argument("-sgf", "--scene-graphs-file", action="store", type=str, dest="scene_graphs_file", required=True, help='scene graphs json file')
    parser.add_argument("-rgf", "--region-graphs-file", action="store", type=str, dest="region_graphs_file", required=True, help='region graphs json file')
    parser.add_argument("-asf", "--attribute-synsets-file", action="store", type=str, dest="attr_synsets_file", required=True, help='attribute synsets json file')
    parser.add_argument("-e", "--header", action="store", type=str, dest="delimiter")
    parser.add_argument( "-nc", "--node-columns", action="store", nargs="*", dest="NODE_COLS")
    parser.add_argument("-ec", "--edge-columns", action="store", nargs="*", dest="EDGE_COLS")

def run(filename, delimiter):
    # import modules locally
    import socket
    print(f'Now importing {filename} with a delimiter {delimiter} and header {header}')
