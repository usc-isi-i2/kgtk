"""
Example CLI module
"""


def parser():
    return {
        'help': 'this is dummy'
    }


def add_arguments(parser):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """
    parser.add_argument("-t", "--test", action="store", type=str, dest="test", required=True)
    parser.add_argument("-i", "--info", action="store", type=str, dest="info")


def run(test, info):
    print(test)
    print(info)
