import datetime
import importlib
from io import StringIO
import itertools
import os
import pkgutil
import sh # type: ignore
import shutil # type: ignore
import signal
import sys
import time
import typing

from kgtk import cli
from kgtk.exceptions import KGTKException, KGTKExceptionHandler, KGTKArgumentParseException
from kgtk import __version__
from kgtk.cli_argparse import KGTKArgumentParser, add_shared_arguments, add_default_arguments, CheckDepsAction


# module name should NOT start with '__' (double underscore)
handlers = [(x.name, "kgtk.cli") for x in pkgutil.iter_modules(cli.__path__)
                   if not x.name.startswith('__')]

try:
    from kgtk_extensions import cli as cliext
    ext_handlers = [(x.name, "kgtk_extensions.cli") for x in pkgutil.iter_modules(cliext.__path__)
                    if not x.name.startswith('__')]
    handlers = sorted(handlers + ext_handlers)
except ImportError:
    pass

# import signal
# signal.signal(signal.SIGPIPE, signal.SIG_DFL)

pipe_delimiter = '/'
sequential_delimiter = '/.'
parallel_delimiter = '//'
ret_code = 0

def cmd_done(cmd, success, exit_code):
    # cmd.cmd -> complete command line
    global ret_code
    ret_code = exit_code


_save_progress: bool = False
_save_progress_debug: bool = False
_save_progress_tty: typing.Optional[str] = None
_save_progress_command: typing.Optional[typing.Any] = None
def progress_startup(pid: typing.Optional[int] = None, fd: typing.Optional[int] = None):
    # This can be called multiple times, if it desired to monitor several
    # input files in sequence.
    #
    # If pid is None, the current process will be monitored.  If pid is not
    # None, the specified process will be monitored.
    #
    # If target_fd is None, them all fds will be monitored.  If target is not
    # None, the specific fd will be monitored: it must already be open, and it
    # should be an input file.  There is no option to moitor multiple specific
    # input files other than calling this routine sequentially
    #
    # TODO: use the envar KGTK_PV_COMMAND to get the `pv` command.
    global _save_progress, _save_progress_tty, _save_progress_debug
    if _save_progress and _save_progress_tty is not None:
        global _save_progress_command
        if _save_progress_command is not None:
            # Shut down an existing process monitor.
            try:
                _save_progress_command.terminate()
            except Exception:
                pass
            _save_progress_command = None

        # Give up if cannot find `pv`:
        if shutil.which('pv') is None:
            if _save_progress_debug:
                print("progress_startup: cannot find pv.", file=sys.stderr, flush=True)
            return

        # Start a process monitor.
        if pid is None:
            pid = os.getpid()
        try:
            if fd is None:
                if _save_progress_debug:
                    print("progress_startup: starting pv with pid %d" % pid, file=sys.stderr, flush=True)
                _save_progress_command = sh.pv("-d {}".format(pid), _out=_save_progress_tty, _err=_save_progress_tty, _bg=True)
            else:
                if _save_progress_debug:
                    print("progress_startup: starting pv with pid %d fd %d" % (pid, fd), file=sys.stderr, flush=True)
                _save_progress_command = sh.pv("-d {}:{}".format(pid, fd),
                                               _out=_save_progress_tty, _err=_save_progress_tty, _bg=True)
        except Exception as e:
            # Ignore the exception unless _save_progress_debug is True.
            if _save_progress_debug:
                print("progress_startup: %s" % str(e), file=sys.stderr, flush=True)
                raise

def progress_shutdown():
    global _save_progress_command
    if _save_progress_command is not None:
        try:
            _save_progress_command.terminate()
        except Exception:
            pass
        _save_progress_command = None
    
def split_list(sequence, sep):
    """From stack overflow;
    https://stackoverflow.com/questions/54372218/how-to-split-a-list-into-sublists-based-on-a-separator-similar-to-str-split
    """
    chunk = []
    for val in sequence:
        if val == sep:
            yield chunk
            chunk = []
        else:
            chunk.append(val)
    yield chunk

def cli_single_command(args, parsed_shared_args, shared_args, parser, sub_parsers, subparser_lookup, subparsers_built)->int:
    import copy
    if parsed_shared_args._pipedebug:
        print("pid %d: Executing a single command: %s" % (os.getpid(), repr(args)), file=sys.stderr, flush=True)
    ret_code: int = 0
    cmd_args = copy.deepcopy(args)
    cmd_name = cmd_args[0].replace("_", "-")
    cmd_args[0] = cmd_name
    # build sub-parser
    if cmd_name in subparser_lookup:
        mod, sub_parser = subparser_lookup[cmd_name]
        add_default_arguments(sub_parser)  # call this before adding other arguments
        if cmd_name not in subparsers_built:
            if hasattr(mod, 'add_arguments_extended'):
                psa = copy.deepcopy(parsed_shared_args)
                psa._command = cmd_name
                mod.add_arguments_extended(sub_parser, psa)
            else:
                mod.add_arguments(sub_parser)
            subparsers_built.add(cmd_name)
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
            # Shared arguments that have been accepted by the subcommand
            # (see KGTKArgumentParser.accept_shared_argument(...))
            # will be passed as keyword arguments to the subcommand.
            if sa not in sub_parsers.choices[h].shared_arguments:
                del kwargs[sa]
            else:
                kwargs[sa] = getattr(parsed_shared_args, sa)

    global _save_progress
    _save_progress = parsed_shared_args._progress
    global _save_progress_debug
    _save_progress_debug = parsed_shared_args._progress_debug
    global _save_progress_tty
    _save_progress_tty = parsed_shared_args._progress_tty
    if parsed_shared_args._progress:
        if hasattr(mod, 'custom_progress') and mod.custom_progress():
            pass
        else:
            progress_startup()

    # run module
    try: 
      kgtk_exception_handler = KGTKExceptionHandler(debug=parsed_shared_args._debug)
      ret_code = kgtk_exception_handler(func, **kwargs)
    except KeyboardInterrupt as e:
        print("\nKeyboard interrupt in %s." % " ".join(args), file=sys.stderr, flush=True)
        progress_shutdown()
        if hasattr(mod, 'keyboard_interrupt'):
            mod.keyboard_interrupt()

        # Silently exit instead of re-raising the KeyboardInterrupt.
        # raise
    return ret_code

def cli_piped_commands(parallel_pipes, args, parsed_shared_args, shared_args, parser, sub_parsers, subparser_lookup, subparsers_built)->int:
    ret_code: int = 0
    if parsed_shared_args._pipedebug:
        print("pid %d: Building a KGTK pipe" % (os.getpid()), file=sys.stderr, flush=True)
    processes = [ ]
    try:
        # TODO: Restore the prior signal handler when done.
        def sigterm_handler(signal, frame):
            # This handles pipe shutdowns.
            if parsed_shared_args._pipedebug:
                print("\npipe: sigterm_handler", file=sys.stderr, flush=True)
            raise KeyboardInterrupt

        signal.signal(signal.SIGTERM, sigterm_handler)

        for parallel_idx, pipe in enumerate(parallel_pipes):
            if parallel_idx > 0 and parsed_shared_args._pipedebug:
                print("*** in parallel with ***", file=sys.stderr, flush=True)

            prior_process = None
            for pipe_idx, cmd_args in enumerate(pipe):
                # add shared arguments
                full_args = [ ]
                for shared_arg in shared_args:
                    if (parallel_idx == 0 and pipe_idx == 0) or str(shared_arg) != "--progress":
                        full_args.append(shared_arg)
                full_args.extend(cmd_args)

                kwargs = {
                    "_bg_exc": False,
                    "_done": cmd_done,
                    "_err": sys.stderr,
                    "_bg": True,
                    "_internal_bufsize": 1,
                    "_new_session": False,
                }

                # add specific arguments
                if pipe_idx == 0:  # The first command reads from our STDIN.
                    kwargs["_in"] = sys.stdin

                if pipe_idx + 1 < len(pipe):
                    # All commands but the last pipe their output to the next command.
                    kwargs["_piped"] = True
                else:
                    # The last command writes to our STDOUT.
                    kwargs["_out"] = sys.stdout

                if parsed_shared_args._pipedebug:
                    cmd_str = " ".join(full_args)
                    for key in kwargs:
                        cmd_str += " " + key + "=" + str(kwargs[key])
                    print("pipe[%d][%d]: kgtk %s" % (parallel_idx, pipe_idx, cmd_str), file=sys.stderr, flush=True)

                if prior_process is None:
                    new_process = sh.kgtk(*full_args, **kwargs)
                else:
                    new_process = sh.kgtk(prior_process, *full_args, **kwargs)
                processes.append(new_process)
                prior_process = new_process                
                
        if parsed_shared_args._pipedebug:
            print("*** waiting ***", file=sys.stderr, flush=True)
        for process in processes:
            process.wait()

    except sh.SignalException_SIGPIPE:
        if parsed_shared_args._pipedebug:
            print("\npipe: sh.SignalException_SIGPIPE", file=sys.stderr, flush=True)

    except sh.SignalException_SIGTERM:
        if parsed_shared_args._pipedebug:
            print("\npipe: sh.SignalException_SIGTERM", file=sys.stderr, flush=True)
        if len(processes) > 0:
            for process in processes:
                try:
                    process.terminate()
                except Exception:
                    pass
        # raise

    except KeyboardInterrupt as e:
        if parsed_shared_args._pipedebug:
            print("\npipe: KeyboardInterrupt", file=sys.stderr, flush=True)
        if len(processes) > 0:
            for idx in range(len(processes)):
                process = processes[idx]
                pgid = process.pgid
                print("Killing cmd %d process group %d" % (idx, pgid), file=sys.stderr, flush=True)
                try:
                    process.signal_group(signal.SIGINT)
                except Exception:
                    pass
        return -1

    except sh.ErrorReturnCode as e:
        if parsed_shared_args._pipedebug:
            print("\npipe: sh.ErrorReturnCode", file=sys.stderr, flush=True)
        # mimic parser exit
        parser.exit(KGTKArgumentParseException.return_code, e.stderr.decode('utf-8'))
    return ret_code

def cli_entry_pipe(args, parsed_shared_args, shared_args, parser, sub_parsers, subparser_lookup, subparsers_built)->int:
    if pipe_delimiter not in args and parallel_delimiter not in args:
        return cli_single_command(args, parsed_shared_args, shared_args, parser, sub_parsers, subparser_lookup, subparsers_built)

    # parse internal pipe
    parallel_pipes: typing.List[typing.List[typing.List[str]]] = list()
    pipe: typing.List[typing.List[str]] = list()
    cmd_args: typing.List[str] = list()
    for arg in args:
        if arg == parallel_delimiter:
            if len(cmd_args) > 0:
                pipe.append(cmd_args)
                cmd_args = list()
            if len(pipe) > 0:
                parallel_pipes.append(pipe)
                pipe = list()
        elif arg == pipe_delimiter:
            if len(cmd_args) > 0:
                pipe.append(cmd_args)
                cmd_args = list()
        else:
            cmd_args.append(arg)
    if len(cmd_args) > 0:
        pipe.append(cmd_args)
    if len(pipe) > 0:
        parallel_pipes.append(pipe)

    if len(parallel_pipes) == 0:
        parser.print_usage()
        parser.exit(KGTKArgumentParseException.return_code)
    return cli_piped_commands(parallel_pipes, args, parsed_shared_args, shared_args, parser, sub_parsers, subparser_lookup, subparsers_built)
    
def cli_entry_sequential_commands(args, parsed_shared_args, shared_args, parser, sub_parsers, subparser_lookup, subparsers_built)->int:
    # parse internal sequence of pipes
    ret_code: int = 0
    for sequential_idx, commands in enumerate(split_list(args, sequential_delimiter)):
        if sequential_idx > 0 and parsed_shared_args._pipedebug:
            print("*** followed by ***", file=sys.stderr, flush=True)
        ret_code = cli_entry_pipe(commands, parsed_shared_args, shared_args, parser, sub_parsers, subparser_lookup, subparsers_built)
        if ret_code != 0:
            break

    return ret_code

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
    base_parser.add_argument(
        '--check-deps',
        action=CheckDepsAction,
        help='check dependencies',
    )
    shared_args = base_parser.add_argument_group('shared optional arguments')
    shared_args.add_argument('--debug', dest='_debug', action='store_true',
                             default=os.getenv('KGTK_OPTION_DEBUG', 'False').lower() in ['y', 'yes', 'true'],
                             help='enable debug mode')
    
    shared_args.add_argument('--kgtkmode', dest='_mode', action='store',
                             default=os.getenv('KGTK_OPTION_KGTK_MODE', 'AUTO').upper(),
                             choices=['NONE', 'EDGE', 'NODE', 'AUTO' ],
                             help='KGTK file reading mode (default=AUTO)')
    
    shared_args.add_argument('--expert', dest='_expert', action='store_true',
                             default=os.getenv('KGTK_OPTION_EXPERT', 'False').lower() in ['y', 'yes', 'true'],
                             help='enable expert mode')
    
    shared_args.add_argument('--pipedebug', dest='_pipedebug', action='store_true',
                             default=os.getenv('KGTK_OPTION_PIPEDEBUG', 'False').lower() in ['y', 'yes', 'true'],
                             help='enable pipe debug mode')
    
    shared_args.add_argument('--progress', dest='_progress', action='store_true',
                             default=os.getenv('KGTK_OPTION_PROGRESS', 'False').lower() in ['y', 'yes', 'true'],
                             help='enable progress monitoring')
    
    shared_args.add_argument('--progress-debug', dest='_progress_debug', action='store_true',
                             default=os.getenv('KGTK_OPTION_PROGRESSDEBUG', 'False').lower() in ['y', 'yes', 'true'],
                             help='enable progress debug mode, which will show exceptions occuring during progress monitoring startup')
    
    shared_args.add_argument('--progress-tty', dest='_progress_tty', action='store',
                             default=os.getenv('KGTK_OPTION_PROGRESS_TTY', "/dev/tty"),
                             help='progress monitoring output tty')
    
    shared_args.add_argument('--timing', dest='_timing', action='store_true',
                             default=os.getenv('KGTK_OPTION_TIMING', 'False').lower() in ['y', 'yes', 'true'],
                             help='enable timing measurements')
    
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
    subparsers_built = set()
    subparser_lookup = {}
    sub_parsers.required = True
    for h in handlers:
        hname, hpath = h
        mod = importlib.import_module('.{}'.format(hname), hpath)
        subp = mod.parser()
        # only create sub-parser with sub-command name and defer full build
        cmd: str = hname.replace("_", "-")
        sub_parser = sub_parsers.add_parser(cmd, **subp)
        subparser_lookup[cmd] = (mod, sub_parser)
        if 'aliases' in subp:
            for alias in subp['aliases']:
                subparser_lookup[alias] = (mod, sub_parser)

    # add root level usage after sub-parsers are created
    # this won't pollute help info in sub-parsers
    parser.usage = '%(prog)s [options] command [ / command]*'

    ret_code = cli_entry_sequential_commands(args, parsed_shared_args, shared_args, parser, sub_parsers, subparser_lookup, subparsers_built)

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

