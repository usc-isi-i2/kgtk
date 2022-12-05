"""
Import concept pairs into KGTK.
"""

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles


def parser():
    return {
        'help': 'Import concept pairs into KGTK.'
    }


def add_arguments(parser: KGTKArgumentParser):
    """
    Parse arguments
    Args:
            parser (argparse.ArgumentParser)
    """
    parser.add_input_file(positional=True)
    parser.add_argument('--relation', action="store", default="/r/RelatedTo", type=str, dest="relation",
                        help="Relation to connect the word pairs with.")
    parser.add_argument('--source', action="store", type=str, dest="source", help="Source identifier")
    parser.add_output_file()


def run(input_file: KGTKFiles, relation, source, output_file: KGTKFiles):
    # import modules locally

    from kgtk.exceptions import KGTKException
    from pathlib import Path
    from kgtk.imports.conceptnetpairs import ImportConceptNetPairs
    try:
        filename: Path = KGTKArgumentParser.get_input_file(input_file)

        output_kgtk_file: Path = KGTKArgumentParser.get_output_file(output_file)

        icnp = ImportConceptNetPairs(input_file=filename,
                                     output_kgtk_file=output_kgtk_file,
                                     source=source,
                                     relation=relation)
        icnp.process()

    except Exception as e:
        raise KGTKException(e)
