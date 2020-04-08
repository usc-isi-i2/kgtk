import sys
import sh # type: ignore
import tempfile

from kgtk.exceptions import KGTKException


def parser():
    return {
        'help': 'Concatenate any mixture of plain or gzip/bzip2/xz-compressed files'
    }

def add_arguments(parser):
    parser.add_argument('-o', '--out', default=None, dest='output',
                        help='output file to write to, otherwise output goes to stdout')
    parser.add_argument('--gz', '--gzip', action='store_true', dest='gz',
                        help='compress result with gzip')
    parser.add_argument('--bz2', '--bzip2', action='store_true', dest='bz2',
                        help='compress result with bzip2')
    parser.add_argument('--xz', action='store_true', dest='xz',
                        help='compress result with xz')
    parser.add_argument("inputs", metavar="INPUT", nargs="*", action="store",
                        help="input files to process, if empty or `-' read from stdin")


# this should be configurable:
tmp_dir = '/tmp'

def determine_file_type(file):
    """Determine if `file' is compressed and if so how, and return file and its associated type.
    If `file' is `-' (stdin), we need to pipe part of it to a temp file so we can check its type.
    In that case, the returned file name will be that of the temporary file header.
    """
    if file == '-':
        header = tempfile.mkstemp(dir=tmp_dir, prefix='kgtk-header.')[1]
        sh.head('-c', '1024', _in=sys.stdin.buffer, _out=header)
        file = header
    # tricky: we get a byte sequence here which we have to decode into a string:
    file_type = sh.file('--brief', file).stdout.split()[0].lower().decode()
    return (file, file_type)

def get_cat_command(file_type):
    """Determine a `cat' command based on a `file_type' determined by `determine_file_type'.
    """
    catcmd = sh.cat
    if file_type == 'gzip':
        catcmd = sh.zcat
    elif file_type == 'bzip2':
        catcmd = sh.bzcat
    elif file_type == 'xz':
        catcmd = sh.xzcat
    return catcmd


def run(output, gz, bz2, xz, inputs):
    """Run zconcat according to the provided input arguments.
    """

    if len(inputs) == 0:
        inputs.append('-')

    output = output or sys.stdout.buffer
    if isinstance(output, str):
        output = open(output, "wb")

    compress = None
    if gz:
        compress = sh.gzip
    elif bz2:
        compress = sh.bzip2
    elif xz:
        compress = sh.xz

    try:
        for inp in inputs:
            file, file_type = determine_file_type(inp)
            catcmd = get_cat_command(file_type)
            if inp == '-':
                # process input piped in from stdin:
                try:
                    if compress is not None:
                        compress(catcmd(sh.cat(file, '-', _in=sys.stdin.buffer, _piped=True), _piped=True), '-c', _out=output, _tty_out=False)
                    else:
                        catcmd(sh.cat(file, '-', _in=sys.stdin.buffer, _piped=True), _out=output)
                finally:
                    # remove temporary header file for the data that was piped in from stdin:
                    sh.rm('-f', file)
            else:
                # process a regular named file:
                if compress is not None:
                    compress(catcmd(file, _piped=True, _out=output), '-c', _out=output, _tty_out=False)
                else:
                    catcmd(file, _out=output)

    except sh.SignalException_SIGPIPE:
        # cleanup in case we piped and terminated prematurely:
        output.flush()
        sys.stdout.flush()
    except Exception as e:
        #import traceback
        #traceback.print_tb(sys.exc_info()[2], 10)
        raise KGTKException('INTERNAL ERROR: ' + str(e) + '\n')

"""
# Examples:

> echo hello | kgtk zconcat
hello

> cat <<EOF > /tmp/file1
line1
line2
EOF
> cat <<EOF > /tmp/file2
line3
line4
EOF

> echo hello | kgtk ticker -i / zconcat --gz -o /tmp/out.gz /tmp/file1 - /tmp/file2
> 
> bzip2 /tmp/file1
> echo hello-again | kgtk zconcat /tmp/out.gz - /tmp/file1.bz2 
line1
line2
hello
>2020-04-01 15:57:48.750904
line3
line4
hello-again
line1
line2

> cat /tmp/file1.bz2 | kgtk zconcat
line1
line2

> cat /tmp/out.gz | kgtk zconcat
line1
line2
hello
>2020-04-02 18:36:40.000507
line3
line4
"""
