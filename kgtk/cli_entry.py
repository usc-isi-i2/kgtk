import sys
import importlib
import pkgutil
import itertools
from argparse import ArgumentParser, RawDescriptionHelpFormatter

from kgtk import cli
from kgtk.exceptions import kgtk_exception_handler, KGTKArgumentParseException
from kgtk import __version__
import sh


# module name should NOT start with '__' (double underscore)
handlers = [x.name for x in pkgutil.iter_modules(cli.__path__)
                   if not x.name.startswith('__')]

# import signal
# signal.signal(signal.SIGPIPE, signal.SIG_DFL)

pipe_delimiter = '/'
ret_code = 0


class KGTKArgumentParser(ArgumentParser):
    def __init__(self, *args, **kwargs):
        if not kwargs.get('formatter_class'):
            kwargs['formatter_class'] = RawDescriptionHelpFormatter

        super(KGTKArgumentParser, self).__init__(*args, **kwargs)

    def exit(self, status=0, message=None):
        if status == 2:
            status = KGTKArgumentParseException.return_code
        super(KGTKArgumentParser, self).exit(status, message)


def cmd_done(cmd, success, exit_code):
    # cmd.cmd -> complete command line
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
        concat_cmd_str = None
        for idx, cmd_args in enumerate(pipe):
            # parse command and options
            cmd_str = ', '.join(['"{}"'.format(c) for c in cmd_args])
            # add common arguments
            cmd_str += ', _bg_exc=False, _done=cmd_done'  # , _err=sys.stdout
            # add specific arguments
            if idx == 0:  # first command
                # concat_cmd_str = 'sh.kgtk("dummy", _bg_exc=False, _in=sys.stdin, _piped=True)'
                # concat_cmd_str = 'sh.kgtk({}, {}, _piped=True)'.format(concat_cmd_str, cmd_str)
                concat_cmd_str = 'sh.kgtk({}, _in=sys.stdin, _piped=True)'.format(cmd_str)
            elif idx + 1 == len(pipe):  # last command
                concat_cmd_str = 'sh.kgtk({}, {}, _out=sys.stdout)'.format(concat_cmd_str, cmd_str)
            else:
                concat_cmd_str = 'sh.kgtk({}, {}, _piped=True)'.format(concat_cmd_str, cmd_str)
        try:
            process = eval(concat_cmd_str)
            process.wait()
        except sh.SignalException_SIGPIPE:
            pass
        except sh.ErrorReturnCode as e:
            # err = '\nRAN: {}\nSTDERR:\n{}\n'.format(e.full_cmd, e.stderr.decode('utf-8'))
            # sys.stderr.write(err)
            # mimic parser exit
            parser.exit(KGTKArgumentParseException.return_code, e.stderr.decode('utf-8'))

    return ret_code

