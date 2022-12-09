"""
Import Visual Genome into KGTK.
"""

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles


def parser():
    return {
        'help': 'Import Visual Genome into KGTK.'
    }


def add_arguments(parser: KGTKArgumentParser):
    """
    Parse arguments
    Args:
            parser (argparse.ArgumentParser)
    """
    parser.add_input_file(positional=True, who="Visual Genome scene graph file")
    parser.add_input_file(who="Visual Genome file with attribute synsets.",
                          options=["--attr-synsets"], dest="attr_syn_file", metavar="ATTR_SYN_FILE")
    parser.add_output_file()


def run(input_file: KGTKFiles,
        attr_syn_file: KGTKFiles,
        output_file: KGTKFiles):
    # import modules locally
    from kgtk.exceptions import KGTKException
    from pathlib import Path
    from kgtk.imports.visualgenome import ImportVisualGenome

    try:
        scene_graph_filename: Path = KGTKArgumentParser.get_input_file(input_file)
        attr_synsets_filename: Path = KGTKArgumentParser.get_input_file(attr_syn_file)

        output_kgtk_file: Path = KGTKArgumentParser.get_output_file(output_file)

        ivg = ImportVisualGenome(input_file=scene_graph_filename,
                                 attr_syn_file=attr_synsets_filename,
                                 output_kgtk_file=output_kgtk_file)

        ivg.process()


    except Exception as e:
        raise KGTKException(e)
