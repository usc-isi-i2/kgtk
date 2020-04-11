"""
Test the KGTK edge file reader.
"""
from argparse import ArgumentParser
from pathlib import Path
import typing

from kgtk.join.edgereader import EdgeReader
    
def main():
    """
    Test the KGTK edge file reader.
    """
    parser = ArgumentParser()
    parser.add_argument(dest="edge_file", help="The edge file to read", type=Path, default=None)
    parser.add_argument("-v", "--verbose", dest="verbose", help="Print additional progress messages.", action='store_true')
    args = parser.parse_args()

    er: EdgeReader = EdgeReader.open(args.edge_file, verbose=args.verbose)

    line_count: int = 0
    line: typing.List[str]
    for line in er:
        line_count += 1
    print("Read %d lines" % line_count)


if __name__ == "__main__":
    main()

