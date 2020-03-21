import sys
import importlib
import pkgutil
from argparse import ArgumentParser, RawDescriptionHelpFormatter

from kgtk import cli
from kgtk.exceptions import kgtk_exception_handler
from kgtk import __version__


# module name should NOT start with '__' (double underscore)
handlers = [x.name for x in pkgutil.iter_modules(cli.__path__)
                   if not x.name.startswith('__')]


class KGTKArgumentParser(ArgumentParser):
    def __init__(self, *args, **kwargs):
        if not kwargs.get('formatter_class'):
            kwargs['formatter_class'] = RawDescriptionHelpFormatter

        super(KGTKArgumentParser, self).__init__(*args, **kwargs)


def cli_entry(*args):
    """
    Usage:
        kgtk <command> [options]
    """
    parser = KGTKArgumentParser()
    parser.add_argument(
        '-V', '--version',
        action='version',
        version='KGTK %s' % __version__,
        help="show KGTK version number and exit."
    )

    sub_parsers = parser.add_subparsers(
        metavar='command',
        dest='cmd',
    )
    sub_parsers.required = True

    # load parser of each module
    # TODO: need to optimize with lazy loading method
    for h in handlers:
        mod = importlib.import_module('.{}'.format(h), 'kgtk.cli')
        sub_parser = sub_parsers.add_parser(h, **mod.parser())
        mod.add_arguments(sub_parser)

    if not args:
        args = tuple(sys.argv)
    if len(args) == 1:
        args = args + ('-h',)
    args = parser.parse_args(args[1:])

    # run
    func = None
    if args.cmd:
        mod = importlib.import_module('.{}'.format(args.cmd), 'kgtk.cli')
        func = mod.run
        kwargs = vars(args)
        del kwargs['cmd']
    return kgtk_exception_handler(func, **kwargs)
