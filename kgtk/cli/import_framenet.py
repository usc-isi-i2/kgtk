"""
Import FrameNet to KGTK.
"""

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles
from kgtk.exceptions import KGTKException


def parser():
    return {
        'help': 'Import FrameNet into KGTK.'
    }


def add_arguments(parser):
    """
    Parse arguments
    Args:
            parser (argparse.ArgumentParser)
    """
    parser.add_output_file()


def run(output_file: KGTKFiles):
    # import modules locally

    from kgtk.imports.framenet import ImportFrameNet
    from pathlib import Path

    try:

        output_kgtk_file: Path = KGTKArgumentParser.get_output_file(output_file)
        ifn = ImportFrameNet(output_kgtk_file=output_kgtk_file)
        ifn.process()

    except Exception as e:
        raise KGTKException(e)
