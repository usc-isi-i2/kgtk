"""
Example CLI module
"""


def parser():
    # https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser
    return {
        'help': 'this is dummy',
        'description': 'this is a basic example'
    }


def add_arguments(parser):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """
    parser.add_argument(action="store", type=str, metavar="test", dest="test")
    parser.add_argument("-i", "--info", action="store", type=str, dest="info")


def run(test, info):
    print(test)
    print(info)
