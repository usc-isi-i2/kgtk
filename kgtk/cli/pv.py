"""
Show progress bars.

"""

from argparse import Namespace, SUPPRESS
import os
from pathlib import Path
import sys
import typing

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles

def parser():
    return {
        'help': 'Show progress bars.',
        'description': 'Show progress bars for running processes.'
    }


def add_arguments_extended(parser: KGTKArgumentParser, parsed_shared_args: Namespace):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """
    from kgtk.utils.argparsehelpers import optional_bool

    _expert: bool = parsed_shared_args._expert

    # This helper function makes it easy to suppress options from
    # The help message.  The options are still there, and initialize
    # what they need to initialize.
    def h(msg: str)->str:
        if _expert:
            return msg
        else:
            return SUPPRESS

    parser.add_argument("-d", "--watchfd", dest="watch_target", help="The process and optional file descriptor to monitor.", type=str, required=True)

    parser.add_argument("--pv-debug", dest="debug", metavar="True|False",
                        help="If true, add debugging.",
                        type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument("--sleep", dest="sleep_secs", help="The sleep time between updates.", type=int, default=1)

def run(watch_target: int,
        sleep_secs: int,
        debug: bool,
)->int:
    # import modules locally
    from kgtk.exceptions import KGTKException

    try:
        # Parse the optional file description in the watch target.
        watch_pid: int
        watch_fd: typing.Optional[int] = None
        if ":" in watch_target:
            watch_process_str: str
            watch_fd_str: str
            watch_process_str, watch_fd_str = watch_target.split(":", 1)
            watch_pid = int(watch_process_str)
            watch_fd = int(watch_process_str)
            watch_process_loop(watch_pid, [watch_fd], sleep_secs, debug)

        else:
            watch_pid = int(watch_target)
            watch_process(watch_pid, sleep_secs, debug)
            

    except SystemExit as e:
        raise KGTKException("Exit requested")
    except KGTKException as e:
        raise
    except Exception as e:
        raise KGTKException(str(e))

    if debug:
        print("Done", file=sys.stderr, flush=True)

def watch_process(watch_pid: int, sleep_secs: int, debug: bool):
    if debug:
        print("Watching process %d" % watch_pid, file=sys.stderr, flush=True)

    procfd_path: str = "/proc/%d/fd" % watch_pid

    watch_fds = {}
    
    fd_str: str
    for fd_str in os.listdir(procfd_path):
        maybe_watch_process_fd(watch_fds, watch_pid, int(fd_str), debug)
    watch_process_loop(watch_pid, watch_fds, sleep_secs, debug)

def watch_process_fd(watch_pid: int,
                     watch_fd: int,
                     debug: bool):
    watch_fds = {}
    maybe_watch_process_fd(watch_fds, watch_pid, watch_fd, debug)
    watch_process_loop(watch_pid, watch_fds, debug)

def maybe_watch_process_fd(watch_fds,
                           watch_pid: int,
                           watch_fd: int,
                           debug: bool):
    import time

    procfd_fd_path: str = "/proc/%d/fd/%d" % (watch_pid, watch_fd)
    if not os.path.islink(procfd_fd_path):
        return

    fd_target: str = os.readlink(procfd_fd_path)
    if not fd_target.startswith("/"):
        return
    if not os.path.isfile(fd_target):
        return

    try:
        filesize: int = os.path.getsize(fd_target)
    except OSError as e:
        return

    if filesize <= 0:
        return

    procfdinfo_path: str = "/proc/%d/fdinfo/%d" % (watch_pid, watch_fd)
    if not os.path.isfile(procfdinfo_path):
        return

    procfdinfo_file = open(procfdinfo_path, "r")

    watch_fds[watch_fd] = {
        "name": fd_target,
        "size": filesize,
        "path": procfdinfo_path,
        "file": procfdinfo_file,
        "ipos": get_fd_pos(procfdinfo_file),
        "itim": time.time(),
    }



def get_fd_pos(info_file)->int:

    info_file.seek(0)
    for line in info_file:
        if line.startswith("pos:"):
            return int(line[len("pos:"):].strip())

    return -1
            

def watch_process_loop(watch_pid: int,
                       watch_fds,
                       sleep_secs: int,
                       debug: bool):
    import time

    if debug:
        print("Watching process %d file descriptors %s" % (watch_pid, repr(watch_fds.keys())), file=sys.stderr, flush=True)

    cur_lines: int = 0
    max_lines: int = 0

    while len(watch_fds) > 0:
        while cur_lines > 0:
            print("\033[F", end="", file=sys.stderr, flush=True)
            cur_lines -= 1

        if debug:
            print("\033[K%d fds remaining" % len(watch_fds), file=sys.stderr, flush=True)
            cur_lines += 1

        for target_fd in sorted(watch_fds.keys()):
            watch_info = watch_fds[target_fd]
            if not os.path.isfile(watch_info["path"]):
                if debug:
                    print("\033[Kfd %d has vanished" % target_fd, file=sys.stderr, flush=True)
                    cur_lines += 1
                watch_info["file"].close()
                del watch_fds[target_fd]
                continue
                
            name: str = watch_info["name"]
            size: int = watch_info["size"]
            pos: int = get_fd_pos(watch_info["file"])


            size_left: int = size - pos
            pos_progress: int = pos - watch_info["ipos"]
            if size_left > 0 and pos_progress > 0:
                rate: float = float(pos_progress) / ( time.time() - watch_info["itim"])
                pct_done: float = (float(pos) / float(size)) * 100
                time_left = size_left / rate
                time_left_str: str = time.strftime("%H:%M:%S", time.gmtime(time_left))

                print("\033[K%4d: %s %5.1f%% ETA %s %s" % (target_fd, format_bytes(pos), pct_done, time_left_str, name), file=sys.stderr, flush=True)
                cur_lines += 1
                if cur_lines > max_lines:
                    max_lines = cur_lines

        while (cur_lines < max_lines):
            print("\033[K", file=sys.stderr, flush=True)
            cur_lines += 1

        time.sleep(sleep_secs)

    if debug:
        print("Done watching process %d" % watch_pid, file=sys.stderr, flush=True)

def format_bytes(size):
    # from https://stackoverflow.com/questions/12523586/python-format-size-application-converting-b-to-kb-mb-gb-tb
    # with modifications
    from math import floor, log

    power = 0 if size <= 0 else int(floor(log(size, 1024)))
    if power > 4:
        power = 4
    return f"{round(size / 1024 ** power, 2)} {['B', 'KiB', 'MiB', 'GiB', 'TiB'][power]}"
