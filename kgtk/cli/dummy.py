"""
Example CLI module

Please DON'T import specific modules globally, import them in `run`.
Please DON'T initialize resource (e.g., variable) globally.
"""
from kgtk.cli_argparse import KGTKArgumentParser


def parser():
    """
    Initialize sub-parser.
    Parameters: https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser
    """
    return {
        'help': 'this is example',
        'description': 'this is a basic example'
    }


def add_arguments(parser: KGTKArgumentParser):
    """
    Parse arguments
    Args:
        parser (kgtk.cli_argparse.KGTKArgumentParser)
    """
    parser.add_argument(action="store", type=str, metavar="name", dest="name")
    parser.add_argument("-i", "--info", action="store", type=str, dest="info")
    parser.add_argument("-e", "--error", action="store_true", help="raise an error")
    parser.accept_shared_argument('_debug')


def run(name, info, error, _debug):
    """
    Arguments here should be defined in `add_arguments` first.
    The return value (integer) will be the return code in shell. It will set to 0 if no value returns.
    Though you can return a non-zero value to indicate error, raise exceptions defined in kgtk.exceptions is preferred
    since this gives user an unified error code and message.
    """
    # import modules locally
    import socket
    from kgtk.exceptions import KGTKException

    if _debug:
        print('DEBUG MODE')

    if error:
        raise KGTKException('An error here\n')

    print('name: {}, info: {}\nhost: {}'.format(name, info, socket.gethostname()))
