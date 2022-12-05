"""
Import an ATOMIC file to KGTK.

"""

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles


def parser():
    return {
        'help': 'Import ATOMIC into KGTK.'
    }


def add_arguments(parser: KGTKArgumentParser):
    """
    Parse arguments
    Args:
            parser (argparse.ArgumentParser)
    """
    parser.add_input_file(positional=True)
    parser.add_output_file()


def run(input_file: KGTKFiles, output_file: KGTKFiles):
    # import modules locally
    from kgtk.exceptions import KGTKException
    from pathlib import Path
    from kgtk.imports.atomic import ImportAtomic

    try:

        input_file: Path = KGTKArgumentParser.get_input_file(input_file)

        output_kgtk_file: Path = KGTKArgumentParser.get_output_file(output_file)

        ia = ImportAtomic(input_file=input_file,
                          output_kgtk_file=output_kgtk_file)
        ia.process()

    except Exception as e:
        raise KGTKException('Error: ' + str(e))
