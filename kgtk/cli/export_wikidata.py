"""
Export wikidata, mirroring import_wikidata.
"""

from argparse import Namespace, SUPPRESS
import typing

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles

def parser():
    return {
        'help': 'Export wikidata from a set of KGTK files.',
        'description': 'Export wikidata, mirroring import-wikidata. ' +
        '\n\nAdditional options are shown in expert help.\nkgtk --expert lift --help'
    }


def add_arguments_extended(parser: KGTKArgumentParser, parsed_shared_args: Namespace):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions, KgtkReaderMode
    from kgtk.utils.argparsehelpers import optional_bool
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    _expert: bool = parsed_shared_args._expert

    # This helper function makes it easy to suppress options from
    # The help message.  The options are still there, and initialize
    # what they need to initialize.
    def h(msg: str)->str:
        if _expert:
            return msg
        else:
            return SUPPRESS

    parser.add_input_file(who="A KGTK file with node records",
                          dest="node_file",
                          options=["--node-file"],
                          optional=False,
                          default_stdin=False)
    parser.add_input_file(who="A KGTK file with edge records",
                          dest="edge_file",
                          options=["--edge-file"],
                          optional=False,
                          default_stdin=False)
    parser.add_input_file(who="A KGTK file with qualifier records",
                          dest="qualifier_file",
                          options=["--qualifier-file"],
                          optional=False,
                          default_stdin=False)
    parser.add_output_file()


    KgtkReader.add_debug_arguments(parser, expert=_expert)
    # TODO: seperate reader_options for the label file.
    KgtkReaderOptions.add_arguments(parser,
                                    mode_options=True,
                                    default_mode=KgtkReaderMode[parsed_shared_args._mode],
                                    expert=_expert)
    KgtkValueOptions.add_arguments(parser, expert=_expert)

def run(node_file: KGTKFiles,
        edge_file: KGTKFiles,
        qualifier_file: KGTKFiles,
        output_file: KGTKFiles,

        errors_to_stdout: bool = False,
        errors_to_stderr: bool = True,
        show_options: bool = False,
        verbose: bool = False,
        very_verbose: bool = False,

        **kwargs # Whatever KgtkFileOptions and KgtkValueOptions want.
)->int:
    # import modules locally
    from pathlib import Path
    import sys
    
    from kgtk.exceptions import KGTKException
    from kgtk.exports.exportwikidata import ExportWikidata
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    node_kgtk_file: Path = KGTKArgumentParser.get_input_file(node_file, who="KGTK node file", default_stdin=False)
    edge_kgtk_file: Path = KGTKArgumentParser.get_input_file(edge_file, who="KGTK edge file", default_stdin=False)
    qualifier_kgtk_file: Path = KGTKArgumentParser.get_input_file(qualifier_file, who="KGTK qualifier file", default_stdin=False)
    output_kgtk_file: Path = KGTKArgumentParser.get_output_file(output_file)

    # Select where to send error messages, defaulting to stderr.
    error_file: typing.TextIO = sys.stdout if errors_to_stdout else sys.stderr

    # Build the option structures.
    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs)
    value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)

    # Show the final option structures for debugging and documentation.
    if show_options:
        print("--node-file=%s" % str(node_kgtk_file), file=error_file, flush=True)
        print("--edge-file=%s" % str(edge_kgtk_file), file=error_file, flush=True)
        print("--qualifier-file=%s" % str(qualifier_kgtk_file), file=error_file, flush=True)
        print("--output-file=%s" % str(output_kgtk_file), file=error_file, flush=True)

        reader_options.show(out=error_file)
        value_options.show(out=error_file)
        print("=======", file=error_file, flush=True)

    try:
        ew: ExportWikidata = ExportWikidata(
            node_file_path=node_kgtk_file,
            edge_file_path=edge_kgtk_file,
            qualifier_file_path=qualifier_kgtk_file,
            output_file_path=output_kgtk_file,

            reader_options=reader_options,
            value_options=value_options,
            error_file=error_file,
            verbose=verbose,
            very_verbose=very_verbose,
        )
        
        ew.process()

        return 0

    except SystemExit as e:
        raise KGTKException("Exit requested")
    except Exception as e:
        raise KGTKException(str(e))

