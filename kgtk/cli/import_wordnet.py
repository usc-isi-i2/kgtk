"""
Import WordNet to KGTK.

"""

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles
from kgtk.exceptions import KGTKException


def parser():
    return {
        'help': 'Import WordNet into KGTK.'
    }


def add_arguments(parser):
    """
    Parse arguments
    Args:
            parser (argparse.ArgumentParser)
    """
    parser.add_output_file()


def run(output_file: KGTKFiles):
    from kgtk.imports.wordnet import ImportWordNet
    from pathlib import Path
    try:

        output_kgtk_file: Path = KGTKArgumentParser.get_output_file(output_file)
        iwn = ImportWordNet(output_kgtk_file=output_kgtk_file)
        iwn.process()

    except Exception as e:
        raise KGTKException(str(e))
