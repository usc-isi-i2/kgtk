"""
This runs the Posix sort command to sort KGTK files.
A backgropund data processing pipeline is initiated that
runs in parallel with the Python process.

1) The data processing pipeline reads stdin or a named file.
   The named file is fed to the data processing pipeline by `cat`,
   avoiding having it read by Python.

2) The header line is stripped out of the input stream by a
   shell `read` command.

3) The header line is then coped to the output stream using a shell
   'printf' command.

4) A copy of the header line is sent via a pipe to the Python control
   process.

5) The data processing pipeline then waits to read sort options
   from a second pipe.

6) The Python control process feeds the header line to KgtkReader and
   and builds the sort key options.

6) The sort key options are sent from Python to the data processing pipeline
   via the second pipe.

7) The data processing pipeline receives the sort command options via
   the shell `read` command, and passes them to the `sort` program.

8) The sort command reads the rest of the input stream,
   sorts it, and writes the sorted data ro the output stream.
"""
import typing

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles
from kgtk.exceptions import KGTKException

def parser():
    return {
        'help': 'Sort file based on one or more columns'
    }

def add_arguments(parser: KGTKArgumentParser):
    parser.add_input_file(positional=True, metavar="INPUT",
                          who="Input file to sort.")
    parser.add_output_file(options=['-o', '--out', '--output-file'],
                           who='Output file to write to.')

    parser.add_argument('-c', '--column', '--columns', action='store', dest='columns', nargs='*',
                        help="comma-separated list of column names to sort on. " +
                        "(defaults to id for node files, " +
                        "(node1, label, node2) for edge files without ID, (id, node1, label, node2) for edge files with ID)")

    parser.add_argument('-r', '--reverse', action='store_true', dest='reverse',
                        help="generate output in reverse sort order")

    parser.add_argument('-X', '--extra', default='', action='store', dest='extra',
                        help="extra options to supply to the sort program")

    parser.add_argument('-v', '--verbose', action='store_true', dest='verbose',
                        help="generate debuigging messages")


def run(input_file: KGTKFiles,
        output_file: KGTKFiles,
        columns: typing.Optional[typing.List[str]] = None,
        reverse: bool =False,
        extra: typing.Optional[str] = None,
        verbose: bool = False
)->int:
    import os
    from pathlib import Path
    import sh # type: ignore
    import sys

    from kgtk.io.kgtkreader import KgtkReader

    input_path: Path = KGTKArgumentParser.get_input_file(input_file)
    output_path: Path = KGTKArgumentParser.get_output_file(output_file)

    error_file = sys.stderr

    try:
        header_read_fd : int
        header_write_fd: int
        header_read_fd, header_write_fd = os.pipe()
        os.set_inheritable(header_write_fd, True)
        if verbose:
            print("header pipe: read_fd=%d write_fd=%d" % (header_read_fd, header_write_fd), file=error_file, flush=True)
        
        sortopt_read_fd : int
        sortopt_write_fd: int
        sortopt_read_fd, sortopt_write_fd = os.pipe()
        os.set_inheritable(sortopt_read_fd, True)
        if verbose:
            print("sort options pipe: read_fd=%d write_fd=%d" % (sortopt_read_fd, sortopt_write_fd), file=error_file, flush=True)

        cmd: str = ""

        if str(input_path) != "-":
            # Feed the named file into the data processing pipeline,
            # otherwise read from standard input.
            cmd += "cat " + repr(str(input_path)) + " | "

        cmd += " { IFS= read -r header ; " # Read the header line
        cmd += " { printf \"%s\\n\" \"$header\" >&" +  str(header_write_fd) + " ; } ; " # Send the header to Python
        cmd += " printf \"%s\\n\" \"$header\" ; " # Send the header to standard output (which may be redirected to a file, below).
        cmd += " IFS= read -u " + str(sortopt_read_fd) + " -r options ; " # Read the sort command options from Python.
        cmd += " LC_ALL=C sort -t '\t' $options ; } " # Sort the remaining input lines using the options read from Python.

        if str(output_path) != "-":
            # Feed the sorted output to the named file.  Otherwise, the sorted
            # output goes to standard output without passing through Python.
            cmd += " > " + repr(str(output_path))

        if verbose:
            print("sort command: %s" % cmd, file=error_file, flush=True)

        # Sh version 1.13 or greater is required for _pass_fds.
        proc = sh.sh("-c", cmd, _in=sys.stdin, _out=sys.stdout, _err=sys.stderr, _bg=True, _pass_fds={header_write_fd, sortopt_read_fd})

        if verbose:
            print("Reading the KGTK input file header line with KgtkReader", file=error_file, flush=True)
        kr: KgtkReader = KgtkReader.open(Path("<%d" % header_read_fd))
        if verbose:
            print("KGTK header: %s" % " ".join(kr.column_names), file=error_file, flush=True)

        sort_options: str = ""
        if reverse:
            sort_options += " --reverse"

        if extra is not None and len(extra) > 0:
            sort_options += " " + extra

        sort_idx: int
        if columns is not None and len(columns) > 0:
            # Process the list of column names, including splitting
            # comma-separated lists of column names.
            column_name: str
            for column_name in columns:
                column_name_2: str
                for column_name_2 in column_name.split(","):
                    column_name_2 = column_name_2.strip()
                    if len(column_name_2) == 0:
                        continue
                    if column_name_2.isdigit():
                        sort_idx = int(column_name_2)
                        if sort_idx > len(kr.column_names):
                            proc.kill_group()
                            raise KGTKException("Invalid column number %d (max %d)." % (sort_idx, len(kr.column_names)))
                    else:
                        if column_name_2 not in kr.column_names:
                            proc.kill_group()
                            raise KGTKException("Unknown column_name %s" % column_name_2)
                        sort_idx = kr.column_name_map[column_name_2] + 1
                    sort_options += " -k %d,%d" % (sort_idx, sort_idx)
        else:
            if kr.is_node_file:
                sort_idx = kr.id_column_idx + 1
                sort_options += " -k %d,%d" % (sort_idx, sort_idx)

            elif kr.is_edge_file:
                if kr.id_column_idx >= 0:
                    sort_idx = kr.id_column_idx + 1
                    sort_options += " -k %d,%d" % (sort_idx, sort_idx)

                sort_idx = kr.node1_column_idx + 1
                sort_options += " -k %d,%d" % (sort_idx, sort_idx)

                sort_idx = kr.label_column_idx + 1
                sort_options += " -k %d,%d" % (sort_idx, sort_idx)

                sort_idx = kr.node2_column_idx + 1
                sort_options += " -k %d,%d" % (sort_idx, sort_idx)
            else:
                proc.kill_group()
                raise KGTKException("Unknown KGTK file mode, please specify the sorting columns.")

        if verbose:
            print("sort options: %s" % sort_options, file=error_file, flush=True)

        kr.close() # We are done with the KgtkReader now.

        # Send the sort options back to the data processing pipeline.
        with open(sortopt_write_fd, "w") as options_file:
            options_file.write(sort_options + "\n")

        proc.wait()

        # Clean up the file descriptors, just in case.
        #
        # Note: Should close these when we raise an exception, too.
        try:
            os.close(header_read_fd)
        except os.error:
            pass
        try:
            os.close(header_write_fd)
        except os.error:
            pass
            
        try:
            os.close(sortopt_read_fd)
        except os.error:
            pass
        try:
            os.close(sortopt_write_fd)
        except os.error:
            pass
            
        return 0

    except Exception as e:
        #import traceback
        #traceback.print_tb(sys.exc_info()[2], 10)
        raise KGTKException('INTERNAL ERROR: ' + type(e).__module__ + '.' + str(e) + '\n')
