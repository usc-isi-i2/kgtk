"""This randomly samples a KGTK file, dividing it into an output file and an optional reject file.

A probability option, `--probability frac`, determines the probability that
an input record is passed to the standard output file. The probability ranges
from 0.0 to 1.0, with 1 being the default.

Alternatively, `--input-count N' and '--desired-count n' may be provided.
The sampling probability will be computed. The number of output records may not
exactly match the desired count.

--mode=NONE is default.

TODO: Need KgtkWriterOptions

"""

from argparse import Namespace, SUPPRESS
import typing

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles

def parser():
    return {
        'help': 'Randomly sample a KGTK file.',
        'description': 'This utility randomly samples a KGTK file, dividing it into an optput file and an optional reject file. ' +
        'The probability of an input record being passed to the output file is controlled by `--probability n`, where ' +
        '`n` ranges from 0 to 1. ' +
        '\n\nThis command defaults to --mode=NONE so it will work with TSV files that do not follow KGTK column naming conventions.' +
        '\n\nAdditional options are shown in expert help.\nkgtk --expert sample --help'
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
    parser.add_output_file(who="The KGTK reject file for records that fail the filter.",
                           dest="reject_file",
                           options=["--reject-file"],
                           metavar="REJECT_FILE",
                           optional=True)

    parser.add_argument("--probability", dest="probability", type=float, default=1.0,
                        help="The probability of passing an input record to the output file (default=%(default)d).")
                        
    parser.add_argument("--seed", dest="seed", type=int,
                        help="The optional random number generator seed (default=None).")

    parser.add_argument("--input-count", dest="input_count", type=int,
                        help="The optional number of input records (default=None).")

    parser.add_argument("--desired-count", dest="desired_count", type=int,
                        help="The optional desired of output records (default=None).")

    parser.add_argument(      "--output-format", dest="output_format", help=h("The file format (default=kgtk)"), type=str,
                              choices=KgtkWriter.OUTPUT_FORMAT_CHOICES)

    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser,
                                    mode_options=True,
                                    default_mode=KgtkReaderMode.NONE,
                                    expert=_expert)
    KgtkValueOptions.add_arguments(parser, expert=_expert)

def run(input_file: KGTKFiles,
        output_file: KGTKFiles,
        reject_file: KGTKFiles,

        probability: float,
        seed: typing.Optional[int],
        input_count: typing.Optional[int],
        desired_count: typing.Optional[int],
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
    import random
    import sys
    import typing
    
    from kgtk.exceptions import KGTKException
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions, KgtkReaderMode
    from kgtk.io.kgtkwriter import KgtkWriter
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    input_file_path: Path = KGTKArgumentParser.get_input_file(input_file)
    output_file_path: Path = KGTKArgumentParser.get_output_file(output_file)
    reject_file_path: typing.Optional[Path] = KGTKArgumentParser.get_optional_output_file(reject_file, who="KGTK reject file")


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
        if reject_file_path is not None:
            print("--reject-file=%s" % str(reject_file_path), file=error_file)
        print("--probability=%s" % str(probability), file=error_file, flush=True)
        if input_count is not None:
            print("--input-count=%d" % input_count, file=error_file, flush=True)
        if desired_count is not None:
            print("--desired-count=%d" % desired_count, file=error_file, flush=True)
        if seed is not None:
            print("--seed=%d" % seed, file=error_file, flush=True)
        reader_options.show(out=error_file)
        value_options.show(out=error_file)
        print("=======", file=error_file, flush=True)

    if input_count is not None and input_count <= 0:
        raise KGTKException("The input count (%d) must be positive." % input_count)

    if desired_count is not None and desired_count <= 0:
        raise KGTKException("The desired count (%d) must be positive." % input_count)

    if input_count is not None and desired_count is not None:
        if desired_count > input_count:
            probability = 1.0
        else:
            probability = desired_count / input_count

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

        rkw: typing.Optional[KgtkWriter] = None
        if reject_file_path is not None:
            rkw = KgtkWriter.open(kr.column_names,
                                  reject_file_path,
                                  use_mgzip=reader_options.use_mgzip, # Hack!
                                  mgzip_threads=reader_options.mgzip_threads, # Hack!
                                  gzip_in_parallel=False,
                                  mode=output_mode,
                                  output_format=output_format,
                                  error_file=error_file,
                                  verbose=verbose,
                                  very_verbose=very_verbose)

        input_count: int = 0
        output_count: int = 0
        reject_count: int = 0

        # Use our own random number generator.  If the seed is not supplied, a
        # system-provided random source will be used, or the clock time as a
        # fallback.
        rg: random.Random = random.Random(seed)

        row: typing.List[str]
        for row in kr:
            input_count += 1

            if probability > rg.random():
                kw.write(row)
                output_count += 1

            elif rkw is not None:
                rkw.write(row)
                reject_count += 1

        kr.close()
        kw.close()
        if rkw is not None:
            rkw.close()
            
        if verbose:
            print("Read %d records, wrote %d records and %d reject records." % (input_count, output_count, reject_count),
                  file=error_file, flush=True)

    except SystemExit as e:
        raise KGTKException("Exit requested")
    except Exception as e:
        raise KGTKException(str(e))

