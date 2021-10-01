"""
Make a side copy of the input stream.

--mode=NONE is the degault
"""
from argparse import Namespace, SUPPRESS
import typing

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles

def parser():
    return {
        'help': 'Make a side copy of the input/output stream..',
        'description': 'Copy the primary input to the primary output, making a copy to a specified file. This can be used to make a copy of a pipe\'s data.' +
        '\n\nThis command defaults to --mode=NONE so it will work with TSV files that do not follow KGTK column naming conventions.'
        
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

    parser.add_input_file()
    parser.add_output_file()

    parser.add_output_file(who="The tee output file", dest="into_file", options=["--into-file"], metavar="INTO_FILE",
                           optional=False, allow_list=False, allow_stdout=False, default_stdout=False)

    parser.add_argument(      "--enable", dest="enable", help="When True, enable copying the data stream to the --into-file. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=True)

    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, default_mode=KgtkReaderMode.NONE, expert=_expert)
    KgtkValueOptions.add_arguments(parser, expert=_expert)

def run(input_file: KGTKFiles,
        output_file: KGTKFiles,
        into_file: KGTKFiles,

        enable: bool,

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

    from kgtk.exceptions import kgtk_exception_auto_handler, KGTKException
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions, KgtkReaderMode
    from kgtk.io.kgtkwriter import KgtkWriter
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    input_kgtk_file: Path = KGTKArgumentParser.get_input_file(input_file)
    output_kgtk_file: Path = KGTKArgumentParser.get_output_file(output_file)
    into_kgtk_file: Path = KGTKArgumentParser.get_output_file(into_file, who="The tee output file", default_stdout=False)

    # Select where to send error messages, defaulting to stderr.
    error_file: typing.TextIO = sys.stdout if errors_to_stdout else sys.stderr

    # Build the option structures.
    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs)
    value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)

    # Show the final option structures for debugging and documentation.
    if show_options:
        print("--input-file=%s" % str(input_kgtk_file), file=error_file)
        print("--output-file=%s" % str(output_kgtk_file), file=error_file)
        print("--to-file=%s" % str(into_kgtk_file), file=error_file)
        print("--enable=%s" % str(enable), file=error_file)
        reader_options.show(out=error_file)
        value_options.show(out=error_file)
        print("=======", file=error_file, flush=True)

    try:

        if verbose:
            print("Opening the input file: %s" % str(input_kgtk_file), file=error_file, flush=True)
        kr: KgtkReader = KgtkReader.open(input_kgtk_file,
                                         options=reader_options,
                                         value_options = value_options,
                                         error_file=error_file,
                                         verbose=verbose,
                                         very_verbose=very_verbose,
        )

        if verbose:
            print("Opening the output file: %s" % str(output_kgtk_file), file=error_file, flush=True)
        kw: KgtkWriter = KgtkWriter.open(kr.column_names,
                                         output_kgtk_file,
                                         mode=KgtkWriter.Mode[kr.mode.name],
                                         verbose=verbose,
                                         very_verbose=very_verbose)

        tkw: typing.Optional[KgtkWriter] = None
        if enable:
            if verbose:
                print("Opening the tee output file: %s" % str(output_kgtk_file), file=error_file, flush=True)
            tkw = KgtkWriter.open(kr.column_names,
                                  into_kgtk_file,
                                  mode=KgtkWriter.Mode[kr.mode.name],
                                  verbose=verbose,
                                  very_verbose=very_verbose)

        input_line_count: int = 0
        row: typing.List[str]
        for row in kr:
            input_line_count += 1
            kw.write(row)
            if tkw is not None:
                tkw.write(row)

        if verbose:
            print("Processed %d rows." % (input_line_count), file=error_file, flush=True)

        kw.close()
        if tkw is not None:
            tkw.close()

        return 0

    except Exception as e:
        kgtk_exception_auto_handler(e)
        return 1
