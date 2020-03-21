"""
Example CLI module

Please DON'T import modules globally, import them in `run`.
"""


def parser():
    """
    Initialize sub-parser.
    Parameters: https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser
    """
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
    parser.add_argument(action="store", type=str, metavar="name", dest="name")
    parser.add_argument("-i", "--info", action="store", type=str, dest="info")


def run(name, info):
    """
    Arguments here should be defined in `add_arguments` first.
    The return value (integer) will be the return code in shell. It will set to 0 if no value returns.
    You can either return a non-zero value to indicate error, or raise exceptions defined in kgtk.exceptions.
    """
    # import modules locally
    import socket

    print('name: {}, info: {}\nhost: {}'.format(name, info, socket.gethostname()))
