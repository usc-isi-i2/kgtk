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

    parser.add_argument('-c', '--column', '--columns', action='store', dest='columns',
                        help="comma-separated list of column names to sort on. (defaults to id for node files, (node1, label, node2, id) for edge files)")
    parser.add_argument('-r', '--reverse', action='store_true', dest='reverse',
                        help="generate output in reverse sort order")


def run(input_file: KGTKFiles,
        output_file: KGTKFiles,
        columns: typing.Optional[typing.List[str]], =None,
        reverse: bool =False,
)->int:
    import os
    from pathlib import Path
    import sh # type: ignore
    import sys

    # print("Sort running.", file=sys.stderr, flush=True) # ***

    input: Path = str(KGTKArgumentParser.get_input_file(input_file))
    output: Path = str(KGTKArgumentParser.get_output_file(output_file))

    # logging.basicConfig(level=logging.INFO)

    try:
        return 0

    except Exception as e:
        #import traceback
        #traceback.print_tb(sys.exc_info()[2], 10)
        raise KGTKException('INTERNAL ERROR: ' + type(e).__module__ + '.' + str(e) + '\n')
