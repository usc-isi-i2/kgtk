import typing
# import logging

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

    parser.add_argument('-v', '--verbose', action='store_true', dest='verbose',
                        help="generate debuigging messages")


def run(input_file: KGTKFiles,
        output_file: KGTKFiles,
        columns: typing.Optional[typing.List[str]] = None,
        reverse: bool =False,
        verbose: bool = False
)->int:
    import os
    from pathlib import Path
    import sh # type: ignore
    import sys

    from kgtk.io.kgtkreader import KgtkReader

    # print("Sort running.", file=sys.stderr, flush=True) # ***

    input_path: Path = str(KGTKArgumentParser.get_input_file(input_file))
    output_path: Path = str(KGTKArgumentParser.get_output_file(output_file))

    # logging.basicConfig(level=logging.INFO)

    try:
        header_read_fd : int
        header_write_fd: int
        header_read_fd, header_write_fd = os.pipe()
        os.set_inheritable(header_write_fd, True)
        if verbose:
            print("header read_fd=%d write_fd=%d" % (header_read_fd, header_write_fd))
        
        sortkey_read_fd : int
        sortkey_write_fd: int
        sortkey_read_fd, sortkey_write_fd = os.pipe()
        os.set_inheritable(sortkey_read_fd, True)
        if verbose:
            print("sort key read_fd=%d write_fd=%d" % (sortkey_read_fd, sortkey_write_fd))

        cmd: str = " { IFS= read -r header; { printf \"%s\\n\" \"$header\" >&" + \
            str(header_write_fd) + \
            " ; } ; printf \"%s\\n\" \"$header\" ; " + \
            " IFS= read -u " + str(sortkey_read_fd) + " -r options ; " + \
            " sort -t '\t' $options"
        if reverse:
            cmd += " --reverse"

        cmd += " ; }"

        if str(output_path) != "-":
            cmd += " > " + repr(output_path)

        if str(input_path) != "-":
            cmd = "cat " + repr(input_path) + " | " + cmd

        if verbose:
            print("Cmd: %s" % cmd)

        options_file = open(sortkey_write_fd, "w")

        # sh version 1.13 or greater is required for __pass_fds.
        proc = sh.sh("-c", cmd, _in=sys.stdin, _out=sys.stdout, _err=sys.stderr, _bg=True, _pass_fds={header_write_fd, sortkey_read_fd})

        if verbose:
            print("Opening the header channel")
        kr: KgtkReader = KgtkReader.open(Path("<%d" % header_read_fd))
        if verbose:
            print("header: %s" % " ".join(kr.column_names))

        sort_idx: int
        options: str = ""
        if columns is not None and len(columns) > 0:
            column_name: str
            for column_name in columns:
                if column_name not in kr.column_names:
                    raise KGTKException("Unknown column_name %s" % column_name)
                sort_idx = kr.column_name_map[column_name] + 1
                options += " -k %d,%d" % (sort_idx, sort_idx)
        else:
            if kr.is_node_file:
                sort_idx = kr.id_column_idx + 1
                options += " -k %d,%d" % (sort_idx, sort_idx)
            elif kr.is_edge_file:

                if kr.id_column_idx >= 0:
                    sort_idx = kr.id_column_idx + 1
                    options += " -k %d,%d" % (sort_idx, sort_idx)
                sort_idx = kr.node1_column_idx + 1
                options += " -k %d,%d" % (sort_idx, sort_idx)
                sort_idx = kr.label_column_idx + 1
                options += " -k %d,%d" % (sort_idx, sort_idx)
                sort_idx = kr.node2_column_idx + 1
                options += " -k %d,%d" % (sort_idx, sort_idx)
            else:
                raise KGTKException("Unknown KGTK file mode, please specify the sorting columns.")

        if verbose:
            print("sort keys: %s" % options)
        options_file.write(options + "\n")
        options_file.close()

        proc.wait()

        return 0

    except Exception as e:
        #import traceback
        #traceback.print_tb(sys.exc_info()[2], 10)
        raise KGTKException('INTERNAL ERROR: ' + type(e).__module__ + '.' + str(e) + '\n')
