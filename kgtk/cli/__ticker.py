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
        'help': 'this is ticker',
        'description': 'it attaches current datetime to stdin'
    }


def add_arguments(parser: KGTKArgumentParser):
    """
    Parse arguments
    """
    parser.add_argument('-i', '--indent', action='count', default=0, help='indentation')


def run(indent):
    """
    Arguments here should be defined in `add_arguments` first.
    The return value (integer) will be the return code in shell. It will set to 0 if no value returns.
    You can either return a non-zero value to indicate error, or raise exceptions defined in kgtk.exceptions.
    """
    # import modules locally
    import sys
    from datetime import datetime
    sys.stdout.write(sys.stdin.read())
    sys.stdout.write('{}{}\n'.format('>' * indent, datetime.now()))
