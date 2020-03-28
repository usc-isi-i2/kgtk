"""
Merge identical nodes and deduplicate.
"""


import sys

def parser():
    return {
        'help': 'Merge identical nodes and deduplicate.'
    }


def add_arguments(parser):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """
    parser.add_argument( "-nf", "--node-file", action="store", type=str, dest="nodes_file", help="TSV file with node columns.")
    parser.add_argument( "-ef", "--edge-file", action="store", type=str, dest="edges_file", help="TSV file with edge columns.")

def run(nodes_file, edges_file): 
    # import modules locally
    import socket
    import sh
    from kgtk.cskg_utils import collapse_identical_nodes
    new_edges_df, new_nodes_df = collapse_identical_nodes(edges_file, nodes_file)

    print(new_edges_df)

    print(new_nodes_df)

