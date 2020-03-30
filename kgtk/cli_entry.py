import sys
import importlib
import pkgutil
import itertools
import signal
from argparse import ArgumentParser, RawDescriptionHelpFormatter

from kgtk import cli
from kgtk.exceptions import kgtk_exception_handler
from kgtk import __version__
import sh


# module name should NOT start with '__' (double underscore)
handlers = [x.name for x in pkgutil.iter_modules(cli.__path__)
                   if not x.name.startswith('__')]

signal.signal(signal.SIGPIPE, signal.SIG_DFL)

pipe_delimiter = '/'
ret_code = 0


class KGTKArgumentParser(ArgumentParser):
    def __init__(self, *args, **kwargs):
        if not kwargs.get('formatter_class'):
            kwargs['formatter_class'] = RawDescriptionHelpFormatter

        super(KGTKArgumentParser, self).__init__(*args, **kwargs)


def cmd_done(cmd, success, exit_code):
    global ret_code
    ret_code = exit_code


def cli_entry(*args):
    """
    Usage:
        kgtk <command> [options]
    """
    global ret_code

    parser = KGTKArgumentParser()
    parser.add_argument(
        '-V', '--version',
        action='version',
        version='KGTK %s' % __version__,
        help='show KGTK version number and exit.'
    )

    sub_parsers = parser.add_subparsers(
        metavar='command',
        dest='cmd'
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
    args = args[1:]

    # parse internal pipe
    pipe = [tuple(y) for x, y in itertools.groupby(args, lambda a: a == pipe_delimiter) if not x]
    if len(pipe) == 1:
        cmd_args = pipe[0]
        args = parser.parse_args(cmd_args)

        # load module
        func = None
        if args.cmd:
            mod = importlib.import_module('.{}'.format(args.cmd), 'kgtk.cli')
            func = mod.run
            kwargs = vars(args)
            del kwargs['cmd']

        # run module
        ret_code = kgtk_exception_handler(func, **kwargs)
    else:
        concat_cmd_args = None
        for idx, cmd_args in enumerate(pipe):
            # parse command and options
            cmd_str = ', '.join(['"{}"'.format(c) for c in cmd_args])
            if idx == 0:  # first command
                concat_cmd_args = 'sh.kgtk({}, _in=sys.stdin, _done=cmd_done, _piped=True, _bg_exc=False)'.format(cmd_str)
            elif idx + 1 == len(pipe):  # last command
                concat_cmd_args = 'sh.kgtk({}, {}, _out=sys.stdout, _done=cmd_done, _bg_exc=False)'.format(concat_cmd_args, cmd_str)
            else:
                concat_cmd_args = 'sh.kgtk({}, {}, _done=cmd_done, _piped=True, _bg_exc=False)'.format(concat_cmd_args, cmd_str)
        try:
            eval(concat_cmd_args)
        except sh.SignalException_SIGPIPE:
            pass
        except sh.ErrorReturnCode as e:
            err = '\nRAN: {}\nSTDERR:\n{}\n'.format(e.full_cmd, e.stderr.decode('utf-8'))
            sys.stderr.write(err)

    return ret_code

