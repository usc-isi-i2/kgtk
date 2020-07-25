"""
Different methods for concatenating a set of files and sending the result
to an output file.
"""

import platform
import os
import sys
import time
import typing

def python_cat(infiles: typing.List[str],
               outfile: str,
               remove: bool=False,
               error_file: typing.TextIO=sys.stderr,
               verbose: bool=False):
    """
    This is very plain Python, except for the os.remove() call.
    """
    start_time: float = 0
    if verbose:
        print('Using python_cat.', file=error_file, flush=True)
        start_time = time.time()
    filename: str
    with open(outfile, "wt") as ofile:
        for filename in infiles:
            if verbose:
                print('Copying {}.'.format(filename), file=error_file, flush=True)
            with open(filename, "rt") as ifile:
                line: str
                for line in ifile:
                    ofile.write(line)
    if remove:
        for filename in infiles:
            if verbose:
                print('Removing {}.'.format(filename), file=error_file, flush=True)
            os.remove(filename)

    if verbose:
        print('Done with python_cat.', file=error_file, flush=True)
        print('Time taken : {}s'.format(time.time() - start_time), file=error_file, flush=True)

def sh_cat(infiles: typing.List[str],
           outfile: str,
           remove: bool=False,
               error_file: typing.TextIO=sys.stderr,
           verbose: bool=False):
    """Unfortunately, the performance of this code is not very good.
    Apparently the output from the cat command is read into Python
    before being written to the output file. This produces a bottleneck.

    Another option would be to start a subshell and use it to perform output
    redirection for the result of `cat`.  This will be higher performing than
    the present implementation.  It may or may not be the simplest solution,
    depending upon whether it is necessary to outwit features such as .login
    files producing output.

    """
    import sh
    start_time: float = 0
    if verbose:
        print('Using sh_cat.', file=error_file, flush=True)
        start_time = time.time()
    sh.cat(*infiles, _out=outfile)

    if remove:
        if verbose:
            print('Removing files.', file=error_file, flush=True)
        sh.rm(*infiles)

    if verbose:
        print('Done with sh_cat.', file=error_file, flush=True)
        print('Time taken : {}s'.format(time.time() - start_time), file=error_file, flush=True)

def sendfile_cat(infiles: typing.List[str],
                 outfile: str,
                 remove: bool=False,
                 preremove: bool=True,
                 error_file: typing.TextIO=sys.stderr,
                 verbose: bool=False):
    """
    Use the superfast sendfile method to copy file data. This works on Linux.
    It won't work on MacOS because sendfile will send only to a socket on that
    operating system. Sendfile isn't implemented at all on Python for Windows.
    """
    start_time: float = 0
    if verbose:
        print('Using sendfile_cat.', file=error_file, flush=True)
        start_time = time.time()
    
    if preremove:
        try:
            # This can be faster then truncating an existing file.
            #
            # TODO: We might get even better performance if we
            # removed existing output files on a thread before the start of
            # whatever we are doing. We'd have to wait for the thread to
            # complete before we start to write the new files.
            os.remove(outfile)
        except FileNotFoundError:
            pass
    ofd: int = os.open(outfile, os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
    totallen: int = 0
    filename: str
    for filename in infiles:
        if verbose:
            print('Copying {}.'.format(filename), file=error_file, flush=True)
        ifd: int = os.open(filename, os.O_RDONLY)

        # This is chunk size is chosen to be less than the limit in
        # the 32-bit system call.
        count: int = 1024 * 1024 * 1024

        offset: int = 0
        while True:
            copycount: int = os.sendfile(ofd, ifd, offset, count)
            if copycount == 0:
                break
            offset += copycount
            totallen += copycount
        os.close(ifd)
    os.close(ofd)

    if remove:
        for filename in infiles:
            if verbose:
                print('Removing {}.'.format(filename), file=error_file, flush=True)
            os.remove(filename)

    if verbose:
        print('Done with sendfile_cat. len=%d' % totallen, file=error_file, flush=True)
        print('Time taken : {}s'.format(time.time() - start_time), file=error_file, flush=True)

def platform_cat(infiles: typing.List[str],
                 outfile: str,
                 remove: bool=False,
                 use_python_cat: bool=False,
                 error_file: typing.TextIO=sys.stderr,
                 verbose: bool=False):
    """
    On Linux, use sendfile_cat.  Otherwise, use a plainer Python version.
    """
    if platform.system() == 'Linux' and not use_python_cat:
        sendfile_cat(infiles, outfile, remove=remove, error_file=error_file, verbose=verbose)
    else:
        python_cat(infiles, outfile, remove=remove, error_file=error_file, verbose=verbose)
