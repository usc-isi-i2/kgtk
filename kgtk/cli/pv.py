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

    watch_fds = {}
    rescan: bool = False
    
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
            maybe_watch_process_fd(watch_fds, watch_pid, watch_fd, debug)

        else:
            rescan = True
            watch_pid = int(watch_target)
            if not scan_process_fds(watch_fds, watch_pid, debug):
                if debug:
                    print("Unable to scan process %d for fds" % watch_pid, file=sys.stderr, flush=True)
                return
            
        watch_process_loop(watch_fds, watch_pid, sleep_secs, rescan=rescan, debug=debug)

        for watch_fd in watch_fds.keys():
            watch_info = watch_fds[watch_fd]
            if watch_info["good"]:
                watch_info["file"].close()

    except SystemExit as e:
        raise KGTKException("Exit requested")
    except KGTKException as e:
        raise
    except Exception as e:
        raise KGTKException(str(e))

    if debug:
        print("Done", file=sys.stderr, flush=True)

def scan_process_fds(watch_fds, watch_pid: int, debug: bool)->bool:
    if debug:
        print("Scanning process %d" % watch_pid, file=sys.stderr, flush=True)

    procfd_path: str = "/proc/%d/fd" % watch_pid
    try:
        fd_strs: typing.List[str] = os.listdir(procfd_path)
    except FileNotFoundError as e:
        return False

    fd_str: str
    for fd_str in fd_strs:
        maybe_watch_process_fd(watch_fds, watch_pid, int(fd_str), debug)

    return True

def maybe_watch_process_fd(watch_fds,
                           watch_pid: int,
                           watch_fd: int,
                           debug: bool):

    is_ok: bool = maybe_watch_process_fd2(watch_fds, watch_pid, watch_fd, debug)
    if not is_ok and watch_fd in watch_fds:
        if watch_fds[watch_fd]["good"]:
            # Clean up by closing the file used to monitor progress on the fd.
            watch_fds[watch_fd]["file"].close()
        del watch_fds[watch_fd]

def maybe_watch_process_fd2(watch_fds,
                           watch_pid: int,
                           watch_fd: int,
                           debug: bool)->bool:
    import time

    procfd_fd_path: str = "/proc/%d/fd/%d" % (watch_pid, watch_fd)
    if not os.path.islink(procfd_fd_path):
        return False

    fd_target: str = os.readlink(procfd_fd_path)
    if not fd_target.startswith("/"):
        return False
    if not os.path.isfile(fd_target):
        return False

    try:
        filesize: int = os.path.getsize(fd_target)
    except OSError as e:
        return False

    if filesize <= 0:
        return False

    procfdinfo_path: str = "/proc/%d/fdinfo/%d" % (watch_pid, watch_fd)
    if not os.path.isfile(procfdinfo_path):
        return False

    if watch_fd in watch_fds and watch_fds[watch_fd]["good"]:
        watch_info = watch_fds[watch_fd]
        if watch_info["name"] == fd_target:
            watch_info["size"] == filesize
            return True
        watch_fds[watch_fd]["file"].close()
        watch_fds[watch_fd]["good"] = False

    try:
        procfdinfo_file = open(procfdinfo_path, "r")
    except OSError as e:
        return False

    watch_fds[watch_fd] = {
        "good": True,
        "name": fd_target,
        "isiz": filesize,
        "size": filesize,
        "path": procfdinfo_path,
        "file": procfdinfo_file,
        "ipos": get_fd_pos(procfdinfo_file),
        "itim": time.time(),
    }

    return True



def get_fd_pos(info_file)->int:

    info_file.seek(0)
    for line in info_file:
        if line.startswith("pos:"):
            return int(line[len("pos:"):].strip())

    return -1
            

def watch_process_loop(watch_fds,
                       watch_pid: int,
                       sleep_secs: int,
                       rescan: bool = False,
                       debug: bool = False):
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

            if not watch_info["good"]:
                if debug:
                    print("\033[K%4d:" % target_fd, file=sys.stderr, flush=True)
                    cur_lines += 1
                continue                

            if not os.path.isfile(watch_info["path"]):
                if debug:
                    print("\033[K%4d: closed" % target_fd, file=sys.stderr, flush=True)
                    cur_lines += 1
                watch_info["file"].close()
                watch_info["good"] = False
                continue
                
            name: str = watch_info["name"]
            isiz: int = watch_info["isiz"]
            size: int = watch_info["size"]
            pos: int = get_fd_pos(watch_info["file"])


            size_left: int = size - pos
            pos_progress: int = pos - watch_info["ipos"]
            time_spent: float = time.time() - watch_info["itim"]

            valid: bool = size > 0 and size == isiz and pos <= size

            pct_done_str: str
            if time_spent == 0.0 or not valid:
                pct_done_str = "      "
            else:
                pct_done: float = (float(pos) / float(size)) * 100
                pct_done_str = "%5.1f%%" % pct_done

            time_left_str: str
            if time_spent == 0.0 or pos_progress == 0 or not valid:
                time_left_str = "        "
            else:
                rate: float = float(pos_progress) / time_spent
                time_left: float = size_left / rate
                time_left_str = time.strftime("%H:%M:%S", time.gmtime(time_left))

            print("\033[K%4d: %s %s ETA %s %s" % (target_fd, format_bytes(pos), pct_done_str, time_left_str, name), file=sys.stderr, flush=True)
            cur_lines += 1
            if cur_lines > max_lines:
                max_lines = cur_lines

        while (cur_lines < max_lines):
            print("\033[K", file=sys.stderr, flush=True)
            cur_lines += 1

        time.sleep(sleep_secs)

        if rescan:
            if not scan_process_fds(watch_fds, watch_pid, debug):
                if debug:
                    print("Process %d has vanished" % watch_pid, file=sys.stderr, flush=True)
                return            

    if debug:
        print("Done watching process %d" % watch_pid, file=sys.stderr, flush=True)

def format_bytes(size):
    # from https://stackoverflow.com/questions/12523586/python-format-size-application-converting-b-to-kb-mb-gb-tb
    # with modifications
    from math import floor, log

    power = 0 if size <= 0 else int(floor(log(size, 1024)))
    if power > 4:
        power = 4
    sz = "%5.1f" % round(size / 1024 ** power, 2)
    units = ['B  ', 'KiB', 'MiB', 'GiB', 'TiB'][power]
    return sz + units
