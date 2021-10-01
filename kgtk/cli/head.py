"""This utility is analogous to the POSIX 'head' command.

When "-n N" is positive, it will pass just the first N data edges of a KGTK
input file to the KGTK output file.

When "-n N" is negative, it will pass all except the last N edges of the KGTK
input file to the KGTK output file.

The header record, cotaining the column names, is always passed and is not
included in N.

Multiplier suffixes are not supported.

Although positive "-n N" has the same effect as KgtkReader's '--record-limit N'
option, this code currently implements the limit itself.

--mode=NONE is default.

TODO: Need KgtkWriterOptions

"""

from argparse import Namespace, SUPPRESS

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles

def parser():
    return {
        'help': 'Pass the head (first records) of a KGTK file.',
        'description': 'This utility is analogous to the POSIX "head" command. ' +
        '\n\nWhen "-n N" is positive, it will pass just the first N data edges of a KGTK input file to the KGTK output file. ' +
        '\n\nWhen "-n N" is negative, it will pass all except the last N edges of the KGTK input file to the KGTK output file. ' +
        '\n\nThe header record, cotaining the column names, is always passed and is not included in N. ' +
        '\n\nMultiplier suffixes are not supported. ' +
        '\n\nUse this command to filter the output of any KGTK command: ' +
        '\n\nkgtk xxx / head -n 20 ' +
        '\n\nUse it to limit the records in a file: ' +
        '\n\nkgtk head -i file.tsv -o file.html' +
        '\n\nThis command defaults to --mode=NONE so it will work with TSV files that do not follow KGTK column naming conventions.' +
        '\n\nAdditional options are shown in expert help.\nkgtk --expert html --help'
    }


def add_arguments_extended(parser: KGTKArgumentParser, parsed_shared_args: Namespace):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions, KgtkReaderMode
    from kgtk.io.kgtkwriter import KgtkWriter
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

    parser.add_input_file()
    parser.add_output_file()

    parser.add_argument("-n", "--edges", dest="edge_limit", type=int, default=10,
                        help="The number of records to pass if positive (default=%(default)d).")
                        
    parser.add_argument(      "--output-format", dest="output_format", help=h("The file format (default=kgtk)"), type=str,
                              choices=KgtkWriter.OUTPUT_FORMAT_CHOICES)

    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, default_mode=KgtkReaderMode.NONE, expert=_expert)
    KgtkValueOptions.add_arguments(parser, expert=_expert)

def run(input_file: KGTKFiles,
        output_file: KGTKFiles,

        edge_limit: int,
        output_format: str,

        errors_to_stdout: bool = False,
        errors_to_stderr: bool = True,
        show_options: bool = False,
        verbose: bool = False,
        very_verbose: bool = False,

        **kwargs # Whatever KgtkFileOptions and KgtkValueOptions want.
)->int:
    # import modules locally
    from collections import deque
    from pathlib import Path
    import sys
    import typing
    
    from kgtk.exceptions import KGTKException
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions, KgtkReaderMode
    from kgtk.io.kgtkwriter import KgtkWriter
    from kgtk.join.kgtkcat import KgtkCat
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    input_file_path: Path = KGTKArgumentParser.get_input_file(input_file)
    output_file_path: Path = KGTKArgumentParser.get_output_file(output_file)

    # Select where to send error messages, defaulting to stderr.
    error_file: typing.TextIO = sys.stdout if errors_to_stdout else sys.stderr

    # TODO: check that at most one input file is stdin?

    # Build the option structures.
    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs, mode=KgtkReaderMode.NONE)
    value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)

    # Show the final option structures for debugging and documentation.
    if show_options:
        print("--input-file=%s" % str(input_file_path), file=error_file, flush=True)
        print("--output-file=%s" % str(output_file_path), file=error_file, flush=True)
        print("--edges=%s" % str(edge_limit), file=error_file, flush=True)
        reader_options.show(out=error_file)
        value_options.show(out=error_file)
        print("=======", file=error_file, flush=True)

    try:
        kr: KgtkReader = KgtkReader.open(input_file_path,
                                         options=reader_options,
                                         value_options = value_options,
                                         error_file=error_file,
                                         verbose=verbose,
                                         very_verbose=very_verbose,
                                         )

        output_mode: KgtkWriter.Mode = KgtkWriter.Mode.NONE
        if kr.is_edge_file:
            output_mode = KgtkWriter.Mode.EDGE
            if verbose:
                print("Opening the output edge file: %s" % str(output_file_path), file=error_file, flush=True)

        elif kr.is_node_file:
            output_mode = KgtkWriter.Mode.NODE
            if verbose:
               print("Opening the output node file: %s" % str(output_file_path), file=error_file, flush=True)

        else:
            if verbose:
                print("Opening the output file: %s" % str(output_file_path), file=error_file, flush=True)

        kw: KgtkWriter = KgtkWriter.open(kr.column_names,
                                         output_file_path,
                                         use_mgzip=reader_options.use_mgzip, # Hack!
                                         mgzip_threads=reader_options.mgzip_threads, # Hack!
                                         gzip_in_parallel=False,
                                         mode=output_mode,
                                         output_format=output_format,
                                         error_file=error_file,
                                         verbose=verbose,
                                         very_verbose=very_verbose)

        edge_count: int = 0
        row: typing.List[str]
        if edge_limit > 0:
            for row in kr:
                edge_count += 1
                if edge_count > edge_limit:
                    break
                kw.write(row)
        else:
            edge_buffer: deque = deque()
            for row in kr:
                edge_buffer.append(row)
                if len(edge_buffer) > - edge_limit:
                    edge_count += 1
                    kw.write(edge_buffer.popleft())

        kw.close()

        if verbose:
            print("Copied %d edges." % edge_count, file=error_file, flush=True)

    except SystemExit as e:
        raise KGTKException("Exit requested")
    except Exception as e:
        raise KGTKException(str(e))

