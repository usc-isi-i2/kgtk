"""
Import ConceptNet into KGTK.

"""
from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles


def parser():
    return {
        'help': 'Import ConceptNet into KGTK.'
    }


def add_arguments(parser: KGTKArgumentParser):
    """
    Parse arguments
    Args:
            parser (argparse.ArgumentParser)
    """
    parser.add_input_file(positional=True)
    parser.add_argument('--english_only', action="store_true", help="Only english conceptnet?")
    parser.add_output_file()
    parser.add_output_file(who="A KGTK output file that will contain only the weights.",
                           dest="weights_file",
                           options=["--weights-file"],
                           metavar="WEIGHTS_FILE",
                           optional=True)


def run(input_file: KGTKFiles, english_only, output_file: KGTKFiles, weights_file: KGTKFiles):
    # import modules locally
    from kgtk.exceptions import KGTKException
    from pathlib import Path
    from kgtk.imports.conceptnet import ImportConceptNet

    try:
        input_cn_file: Path = KGTKArgumentParser.get_input_file(input_file)
        output_kgtk_file: Path = KGTKArgumentParser.get_output_file(output_file)
        if weights_file:
            info_kgtk_file = KGTKArgumentParser.get_output_file(weights_file)
        else:
            info_kgtk_file = None

        icn = ImportConceptNet(input_file=input_cn_file,
                               output_kgtk_file=output_kgtk_file,
                               info_kgtk_file=info_kgtk_file,
                               english_only=english_only)
        icn.process()

    except Exception as e:
        raise KGTKException(e)
