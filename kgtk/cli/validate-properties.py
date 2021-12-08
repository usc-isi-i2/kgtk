"""
Validate property patterns in a KGTK file.

TODO: Need KgtkWriterOptions.
"""

from argparse import Namespace, SUPPRESS
import typing

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles

def parser():
    return {
        'aliases': [ 'filter-properties' ],
        'help': 'Validate property patterns in a KGTK file. ',
        'description': 'Validate property patterns in a KGTK file. ' +
        '\n\nAdditional options are shown in expert help.\nkgtk --expert clean-data --help'
    }


def add_arguments_extended(parser: KGTKArgumentParser, parsed_shared_args: Namespace):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderMode, KgtkReaderOptions
    from kgtk.utils.argparsehelpers import optional_bool
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    _expert: bool = parsed_shared_args._expert

    parser.add_input_file()
    parser.add_input_file(who="The property pattern definitions.", default_stdin=False,
                          options=["--pattern-file"], dest="pattern_file", metavar="PATTERN_FILE")
    parser.add_output_file(optional=True)
    parser.add_output_file(who="The property pattern reject output.", optional=True,
                          options=["--reject-file"], dest="reject_file", metavar="REJECT_FILE")

    parser.add_argument(      "--presorted", dest="grouped_input",
                              help="Indicate that the input has been presorted (or at least pregrouped) on the node1 column. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False, metavar="True|False")

    parser.add_argument(      "--process-node1-groups", dest="reject_node1_groups",
                              help="When True, process all records for a node1 value " +
                              "as a group. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=True, metavar="True|False")

    parser.add_argument(      "--no-complaints", dest="no_complaints",
                              help="When true, do not print complaints (when rejects are expected). (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False, metavar="True|False")

    parser.add_argument(      "--complain-immediately", dest="complain_immediately",
                              help="When true, print complaints immediately (for debugging). (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False, metavar="True|False")

    parser.add_argument(      "--add-isa-column", dest="add_isa_column",
                              help="When true, add an ISA column to the output and reject files. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False, metavar="True|False")

    parser.add_argument(      "--isa-column-name", dest="isa_column_name", default="isa;node2",
                              help="The name for the ISA column. (default %(default)s)")

    parser.add_argument(      "--autovalidate", dest="autovalidate",
                              help="When true, validate node1 and node2 values before testing them. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=True, metavar="True|False")

    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser,
                                    mode_options=True,
                                    default_mode=KgtkReaderMode[parsed_shared_args._mode],
                                    expert=_expert)
    KgtkValueOptions.add_arguments(parser, expert=_expert)


def run(input_file: KGTKFiles,
        pattern_file: KGTKFiles,
        output_file: KGTKFiles,
        reject_file: KGTKFiles,
        grouped_input: bool = False,
        reject_node1_groups: bool = False,
        no_complaints: bool = False,
        complain_immediately: bool = False,
        add_isa_column: bool = False,
        isa_column_name: str = "isa;node2",
        autovalidate: bool = True,
        errors_to_stdout: bool = False,
        errors_to_stderr: bool = False,
        show_options: bool = False,
        verbose: bool = False,
        very_verbose: bool = False,
        **kwargs # Whatever KgtkReaderOptions and KgtkValueOptions want.
)->int:
    # import modules locally
    from pathlib import Path
    import sys
    
    from kgtk.exceptions import KGTKException
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderMode, KgtkReaderOptions
    from kgtk.io.kgtkwriter import KgtkWriter
    from kgtk.value.propertypatternvalidator import PropertyPatterns, PropertyPatternValidator
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    input_kgtk_file: Path = KGTKArgumentParser.get_input_file(input_file)
    pattern_kgtk_file: Path = KGTKArgumentParser.get_input_file(pattern_file, default_stdin=False)
    output_kgtk_file: typing.Optional[Path] = KGTKArgumentParser.get_optional_output_file(output_file)
    reject_kgtk_file: typing.Optional[Path] = KGTKArgumentParser.get_optional_output_file(reject_file)

    # Select where to send error messages, defaulting to stderr.
    error_file: typing.TextIO = sys.stdout if errors_to_stdout else sys.stderr

    # Build the option structures.
    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs)
    value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)

    # Show the final option structures for debugging and documentation.
    if show_options:
        print("--input-file=%s" % str(input_kgtk_file), file=error_file)
        print("--pattern-file=%s" % str(pattern_kgtk_file), file=error_file)
        if output_kgtk_file is not None:
            print("--output-file=%s" % str(output_kgtk_file), file=error_file)
        if reject_kgtk_file is not None:
            print("--reject-file=%s" % str(reject_kgtk_file), file=error_file)
        print("--presorted=%s" % str(grouped_input))
        print("--reject-node1-groups=%s" % str(reject_node1_groups))
        print("--complain-immediately=%s" % str(complain_immediately))
        print("--add-isa-column=%s" % str(add_isa_column))
        print("--isa-column-name=%s" % str(isa_column_name))
        print("--autovalidate=%s" % str(autovalidate))
        reader_options.show(out=error_file)
        value_options.show(out=error_file)
        print("=======", file=error_file, flush=True)

    if verbose:
        print("Reading data from '%s'" % str(input_kgtk_file), file=error_file, flush=True)
        print("Reading patterns from '%s'" % str(pattern_kgtk_file), file=error_file, flush=True)
        if output_kgtk_file is not None:
            print("Writing good data to '%s'" % str(output_kgtk_file), file=error_file, flush=True)
        if reject_kgtk_file is not None:
            print("Writing rejected data to '%s'" % str(reject_kgtk_file), file=error_file, flush=True)
                
    try:
        pkr: KgtkReader = KgtkReader.open(pattern_kgtk_file,
                                          error_file=error_file,
                                          mode=KgtkReaderMode.EDGE,
                                          options=reader_options,
                                          value_options=value_options,
                                          verbose=verbose,
                                          very_verbose=very_verbose)
        
        pps: PropertyPatterns = PropertyPatterns.load(pkr,
                                                      value_options,
                                                      error_file=error_file,
                                                      verbose=verbose,
                                                      very_verbose=very_verbose)
        
        kr: KgtkReader = KgtkReader.open(input_kgtk_file,
                                         error_file=error_file,
                                         options=reader_options,
                                         value_options=value_options,
                                         verbose=verbose,
                                         very_verbose=very_verbose)

        output_column_names: typing.List[str] = [ ]
        isa_column_idx: int = -1
        if output_kgtk_file is not None:
            output_column_names = kr.column_names.copy()
            if add_isa_column:
                if isa_column_name in output_column_names:
                    isa_column_idx = output_column_names.index(isa_column_name)
                else:
                    isa_column_idx = len(output_column_names)
                    output_column_names.append(isa_column_name)

        ppv: PropertyPatternValidator = PropertyPatternValidator.new(pps,
                                                                     kr,
                                                                     grouped_input=grouped_input,
                                                                     reject_node1_groups=reject_node1_groups,
                                                                     no_complaints=no_complaints,
                                                                     complain_immediately=complain_immediately,
                                                                     isa_column_idx=isa_column_idx,
                                                                     autovalidate=autovalidate,
                                                                     value_options=value_options,
                                                                     error_file=error_file,
                                                                     verbose=verbose,
                                                                     very_verbose=very_verbose)

        kw: typing.Optional[KgtkWriter] = None
        if output_kgtk_file is not None:
            kw = KgtkWriter.open(output_column_names,
                                 output_kgtk_file,
                                 verbose=verbose, very_verbose=very_verbose)
        
        rkw: typing.Optional[KgtkWriter] = None
        if reject_kgtk_file is not None:
            rkw = KgtkWriter.open(output_column_names,
                                  reject_kgtk_file,
                                  verbose=verbose, very_verbose=very_verbose)
        
        ppv.process(kr, kw, rkw)

        if verbose:
            print("Read %d rows, %d valid" % (ppv.input_row_count, ppv.valid_row_count), file=error_file, flush=True)
            if kw is not None:
                print("Wrote %d good rows" % ppv.output_row_count, file=error_file, flush=True)
            if rkw is not None:
                print("Wrote %d rejected rows" % ppv.reject_row_count, file=error_file, flush=True)

        if kw is not None:
            kw.close()
        if rkw is not None:
            rkw.close()

        return 0

    except Exception as e:
        raise KGTKException(e)

