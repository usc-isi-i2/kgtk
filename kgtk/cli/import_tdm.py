"""
Convert a TDM JSON file and convert it to a KGTK file.

TODO: Need KgtkWriterOptions
"""

from argparse import Namespace, SUPPRESS

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles

def parser():
    return {
        'help': 'Convert a TDM JSON file to a KGTK file.',
        'description': 'Convert a TDM JSON input file to a KGTK file on output.' +
        '\n\nAdditional options are shown in expert help.\nkgtk --expert import-tdm --help'
    }


def add_arguments_extended(parser: KGTKArgumentParser, parsed_shared_args: Namespace):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """
    from kgtk.io.kgtkreader import KgtkReader
    from kgtk.reshape.kgtkidbuilder import KgtkIdBuilder, KgtkIdBuilderOptions

    _expert: bool = parsed_shared_args._expert

    # This helper function makes it easy to suppress options from
    # The help message.  The options are still there, and initialize
    # what they need to initialize.
    def h(msg: str)->str:
        if _expert:
            return msg
        else:
            return SUPPRESS

    parser.add_input_file(who="The TDM JSON file to import.", positional=True)
    parser.add_output_file(who="The KGTK file to write.")

    KgtkIdBuilderOptions.add_arguments(parser, expert=True, default_style=KgtkIdBuilderOptions.EMPTY_STYLE) # Show all the options.
    KgtkReader.add_debug_arguments(parser, expert=_expert)

def run(input_file: KGTKFiles,
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
    import simplejson as json
    import sys
    import typing
    
    from kgtk.exceptions import KGTKException
    from kgtk.io.kgtkwriter import KgtkWriter
    from kgtk.join.kgtkcat import KgtkCat
    from kgtk.reshape.kgtkidbuilder import KgtkIdBuilder, KgtkIdBuilderOptions

    input_file_path: Path = KGTKArgumentParser.get_input_file(input_file)
    output_file_path: Path = KGTKArgumentParser.get_output_file(output_file)

    # Select where to send error messages, defaulting to stderr.
    error_file: typing.TextIO = sys.stdout if errors_to_stdout else sys.stderr

    # Build the option structures:
    idbuilder_options: KgtkIdBuilderOptions = KgtkIdBuilderOptions.from_dict(kwargs)


    # Show the final option structures for debugging and documentation.
    if show_options:
        print("--input-file=%s" % str(input_file_path), file=error_file, flush=True)
        print("--output-file=%s" % str(output_file_path), file=error_file, flush=True)
        idbuilder_options.show(out=error_file)
        print("=======", file=error_file, flush=True)

    try:
        
        with open(input_file_path, "r") as ifp:
            tdm: dict = json.load(ifp)

        # Define our output columns:
        oc: typing.List[str] = ["id", "node1", "label", "node2"]

        # Create the ID builder:
        idb: KgtkIdBuilder = KgtkIdBuilder.from_column_names(oc, idbuilder_options)

        kw: KgtkWriter = KgtkWriter.open(idb.column_names,
                                         output_kgtk_file,
                                         mode=KgtkWriter.Mode.EDGE,
                                         require_all_columns=True,
                                         prohibit_extra_columns=True,
                                         fill_missing_columns=False,
                                         verbose=verbose,
                                         very_verbose=very_verbose)


        

        kw.close()

        return 0

    except SystemExit as e:
        raise KGTKException("Exit requested")
    except Exception as e:
        raise KGTKException(str(e))

