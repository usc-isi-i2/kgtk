import datetime
import importlib
import itertools
import pkgutil
import sys
import time

from kgtk import cli
from kgtk.exceptions import KGTKExceptionHandler, KGTKArgumentParseException
from kgtk import __version__
from kgtk.cli_argparse import KGTKArgumentParser, add_shared_arguments, add_default_arguments
import sh # type: ignore


# module name should NOT start with '__' (double underscore)
handlers = [x.name for x in pkgutil.iter_modules(cli.__path__)
                   if not x.name.startswith('__')]

# import signal
# signal.signal(signal.SIGPIPE, signal.SIG_DFL)

pipe_delimiter = '/'
ret_code = 0


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

    # Capture the initial time for timing measurements.
    start_time: float = time.time()
    process_start_time: float = time.process_time()

    # get all arguments
    if not args:
        args = tuple(sys.argv)
    args = args[1:]

    # base parser for shared arguments
    base_parser = KGTKArgumentParser(add_help=False)
    base_parser.add_argument(
        '-V', '--version',
        action='version',
        version='KGTK %s' % __version__,
        help='show KGTK version number and exit.'
    )
    shared_args = base_parser.add_argument_group('shared optional arguments')
    shared_args.add_argument('--debug', dest='_debug', action='store_true', default=False, help='enable debug mode')
    shared_args.add_argument('--expert', dest='_expert', action='store_true', default=False, help='enable expert mode')
    shared_args.add_argument('--pipedebug', dest='_pipedebug', action='store_true', default=False, help='enable pipe debug mode')
    shared_args.add_argument('--timing', dest='_timing', action='store_true', default=False, help='enable timing measurements')
    add_shared_arguments(shared_args)

    # parse shared arguments
    parsed_shared_args, rest_args = base_parser.parse_known_args(args)
    shared_args = tuple(filter(lambda a: a not in rest_args, args))
    args = tuple(rest_args)


    # complete parser, load sub-parser of each module
    parser = KGTKArgumentParser(
        parents=[base_parser], prog='kgtk',
        description='kgtk --- Knowledge Graph Toolkit',
    )
    sub_parsers = parser.add_subparsers(
        metavar='command',
        dest='cmd'
    )
    subparser_lookup = {}
    sub_parsers.required = True
    for h in handlers:
        mod = importlib.import_module('.{}'.format(h), 'kgtk.cli')
        subp = mod.parser()
        # only create sub-parser with sub-command name and defer full build
        cmd: str = h.replace("_", "-")
        sub_parser = sub_parsers.add_parser(cmd, **subp)
        subparser_lookup[cmd] = (mod, sub_parser)
        if 'aliases' in subp:
            for alias in subp['aliases']:
                subparser_lookup[alias] = (mod, sub_parser)

    # add root level usage after sub-parsers are created
    # this won't pollute help info in sub-parsers
    parser.usage = '%(prog)s [options] command [ / command]*'

    # parse internal pipe
    pipe = [list(y) for x, y in itertools.groupby(args, lambda a: a == pipe_delimiter) if not x]
    if len(pipe) == 0:
        parser.print_usage()
        parser.exit(KGTKArgumentParseException.return_code)
    elif len(pipe) == 1:  # single command
        cmd_args = pipe[0]

        cmd_name = cmd_args[0].replace("_", "-")
        cmd_args[0] = cmd_name
        # build sub-parser
        if cmd_name in subparser_lookup:
            mod, sub_parser = subparser_lookup[cmd_name]
            add_default_arguments(sub_parser)  # call this before adding other arguments
            if hasattr(mod, 'add_arguments_extended'):
                mod.add_arguments_extended(sub_parser, parsed_shared_args)
            else:
                mod.add_arguments(sub_parser)
        parsed_args = parser.parse_args(cmd_args)

        # load module
        kwargs = {}
        func = None
        if parsed_args.cmd:
            h = parsed_args.cmd
            func = mod.run

            # remove sub-command name
            kwargs = vars(parsed_args)
            del kwargs['cmd']

            # set shared arguments
            for sa in vars(parsed_shared_args):
                if sa not in sub_parsers.choices[h].shared_arguments:
                    del kwargs[sa]
                else:
                    kwargs[sa] = getattr(parsed_shared_args, sa)

        # run module
        kgtk_exception_handler = KGTKExceptionHandler(debug=parsed_shared_args._debug)
        ret_code = kgtk_exception_handler(func, **kwargs)
    else:  # piped commands
        concat_cmd_str = None
        for idx, cmd_args in enumerate(pipe):
            # add shared arguments
            cmd_str = ', '.join(['"{}"'.format(a) for a in shared_args])
            if cmd_str:
                cmd_str += ', '
            # parse command and options
            cmd_str += ', '.join(['"{}"'.format(a) for a in cmd_args])
            # add other common arguments
            cmd_str += ', _bg_exc=False, _done=cmd_done'  # , _err=sys.stdout
            # add specific arguments
            if idx == 0:  # first command
                concat_cmd_str = 'sh.kgtk({}, _in=sys.stdin, _piped=True, _err=sys.stderr)'.format(cmd_str)
            elif idx + 1 == len(pipe):  # last command
                concat_cmd_str = 'sh.kgtk({}, {}, _out=sys.stdout, _err=sys.stderr)'.format(concat_cmd_str, cmd_str)
            else:
                concat_cmd_str = 'sh.kgtk({}, {}, _piped=True, _err=sys.stderr)'.format(concat_cmd_str, cmd_str)
        try:
            if parsed_shared_args._pipedebug:
                print("eval: %s" % concat_cmd_str, file=sys.stderr, flush=True)
            process = eval(concat_cmd_str)
            process.wait()
        except sh.SignalException_SIGPIPE:
            pass
        except sh.ErrorReturnCode as e:
            # mimic parser exit
            parser.exit(KGTKArgumentParseException.return_code, e.stderr.decode('utf-8'))

    if parsed_shared_args._timing:
        end_time: float = time.time()
        elapsed_seconds: float = end_time - start_time

        process_end_time: float = time.process_time()
        process_elapsed_seconds: float = process_end_time - process_start_time

        cpu_ratio: float = process_elapsed_seconds / elapsed_seconds

        print("Timing: elapsed=%s CPU=%s (%5.1f%%): %s" % (str(datetime.timedelta(seconds=elapsed_seconds)),
                                                           str(datetime.timedelta(seconds=process_elapsed_seconds)),
                                                           cpu_ratio * 100.0,
                                                           " ".join(args)), file=sys.stderr, flush=True)

    return ret_code

