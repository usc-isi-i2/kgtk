"""Copy records from the first KGTK file to the output file,
compacting repeated items into | lists.

TODO: Need KgtkWriterOptions

TODO:  --columns should list the columns to compact (default: all except the key columns).
       --key-columns should set the key columns.
"""

from argparse import Namespace, SUPPRESS
import typing

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles

DEDUP_COMMAND: str = "deduplicate"

def parser():
    return {
        'aliases': [ DEDUP_COMMAND ],
        'help': 'Copy a KGTK file compacting | lists.',
        'description': 'Copy a KGTK file, compacting multiple records into | lists. ' +
        '\n\nBy default, the input file is sorted in memory to achieve the ' +
        'grouping necessary for the compaction algorithm. This may cause ' +
        ' memory usage issues for large input files. If the input file has ' +
        'already been sorted (or at least grouped), the `--presorted` ' +
        'option may be used.' +
        '\n\nAdditional options are shown in expert help.\nkgtk --expert compact --help'
    }


def add_arguments_extended(parser: KGTKArgumentParser, parsed_shared_args: Namespace):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
    from kgtk.reshape.kgtkidbuilder import KgtkIdBuilder, KgtkIdBuilderOptions
    from kgtk.utils.argparsehelpers import optional_bool
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    _command: str = parsed_shared_args._command
    _expert: bool = parsed_shared_args._expert

    # This helper function makes it easy to suppress options from
    # The help message.  The options are still there, and initialize
    # what they need to initialize.
    def h(msg: str)->str:
        if _expert:
            return msg
        else:
            return SUPPRESS

    parser.add_input_file(positional=True)
    parser.add_output_file()
    parser.add_output_file(who="A KGTK output file that will contain only the rows containing lists." +
                           " This file will have the same columns as the primary output file.",
                           dest="list_output_file",
                           options=["--list-output-file"],
                           metavar="LIST_OUTPUT_FILE",
                           optional=True)

    if _command == DEDUP_COMMAND:

        parser.add_argument(      "--columns", dest="key_column_names",
                                  help=h("The key columns to identify records for compaction. " +
                                  "(default=all columns)."), nargs='+', default=[ ])
    
        parser.add_argument(      "--compact-id", dest="compact_id",
                                  help=h("Indicate that the ID column in KGTK edge files should be compacted. " +
                                  "Normally, if the ID column exists, it is not compacted, " +
                                  "as there are use cases that need to maintain distinct lists of secondary edges for each ID value. (default=%(default)s)."),
                                  type=optional_bool, nargs='?', const=True, default=False, metavar="True|False")

        parser.add_argument(      "--deduplicate", dest="deduplicate",
                                  help=h("Treat all columns as key columns, overriding --columns and --compact-id. " +
                                  "This will remove completely duplicate records without compacting any new lists. " +
                                  "(default=%(default)s)."),
                                  type=optional_bool, nargs='?', const=True, default=True, metavar="True|False")

        parser.add_argument(      "--lists-in-input", dest="lists_in_input",
                                  help=h("Assume that the input file may contain lists (disable when certain it does not). (default=%(default)s)."),
                                  type=optional_bool, nargs='?', const=True, default=True)

        parser.add_argument(      "--keep-first", dest="keep_first_names",
                                  help=h("If compaction results in a list of values for any column on this list, keep only the first value after sorting. " +
                                  "(default=none)."), nargs='+', default=[ ])
    else:
        parser.add_argument(      "--columns", dest="key_column_names",
                                  help="The key columns to identify records for compaction. " +
                                  "(default=id for node files, (node1, label, node2, id) for edge files).", nargs='+', default=[ ])
    
        parser.add_argument(      "--compact-id", dest="compact_id",
                                  help="Indicate that the ID column in KGTK edge files should be compacted. " +
                                  "Normally, if the ID column exists, it is not compacted, " +
                                  "as there are use cases that need to maintain distinct lists of secondary edges for each ID value. (default=%(default)s).",
                                  type=optional_bool, nargs='?', const=True, default=False, metavar="True|False")

        parser.add_argument(      "--deduplicate", dest="deduplicate",
                                  help="Treat all columns as key columns, overriding --columns and --compact-id. " +
                                  "This will remove completely duplicate records without compacting any new lists. " +
                                  "(default=%(default)s).",
                                  type=optional_bool, nargs='?', const=True, default=False, metavar="True|False")

        parser.add_argument(      "--lists-in-input", dest="lists_in_input",
                                  help="Assume that the input file may contain lists (disable when certain it does not). (default=%(default)s).",
                                  type=optional_bool, nargs='?', const=True, default=True)

        parser.add_argument(      "--keep-first", dest="keep_first_names",
                                  help="If compaction results in a list of values for any column on this list, keep only the first value after sorting. " +
                                  "(default=none).", nargs='+', default=[ ])

    parser.add_argument(      "--presorted", dest="sorted_input",
                              help="Indicate that the input has been presorted (or at least pregrouped) (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False, metavar="True|False")

    parser.add_argument(      "--verify-sort", dest="verify_sort",
                              help="If the input has been presorted, verify its consistency (disable if only pregrouped). (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=True, metavar="True|False")

    parser.add_argument(      "--report-lists", dest="report_lists",
                              help="When True, report records with lists to the error output. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--exclude-lists", dest="exclude_lists",
                              help="When True, exclude records with lists from the output. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--output-only-lists", dest="output_only_lists",
                              help="When True, only records containing lists will be written to the primary output file. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--build-id", dest="build_id",
                              help="Build id values in an id column. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False, metavar="True|False")
    
    KgtkIdBuilderOptions.add_arguments(parser, expert=_expert)
    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, expert=_expert)
    KgtkValueOptions.add_arguments(parser, expert=_expert)

def run(input_file: KGTKFiles,
        output_file: KGTKFiles,
        list_output_file: KGTKFiles,
        key_column_names: typing.List[str],
        keep_first_names: typing.List[str],
        compact_id: bool,
        deduplicate: bool,
        sorted_input: bool,
        verify_sort: bool,
        lists_in_input: bool,
        report_lists: bool,
        exclude_lists: bool,
        output_only_lists: bool,
        build_id: bool,

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
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
    from kgtk.io.kgtkwriter import KgtkWriter
    from kgtk.reshape.kgtkcompact import KgtkCompact
    from kgtk.reshape.kgtkidbuilder import KgtkIdBuilder, KgtkIdBuilderOptions
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    input_kgtk_file: Path = KGTKArgumentParser.get_input_file(input_file)
    output_kgtk_file: Path = KGTKArgumentParser.get_output_file(output_file)
    list_output_kgtk_file: typing.Optional[Path] = KGTKArgumentParser.get_optional_output_file(list_output_file, who="KGTK list output file")

    # Select where to send error messages, defaulting to stderr.
    error_file: typing.TextIO = sys.stdout if errors_to_stdout else sys.stderr

    # Build the option structures.
    idbuilder_options: KgtkIdBuilderOptions = KgtkIdBuilderOptions.from_dict(kwargs)
    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs)
    value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)

    # Show the final option structures for debugging and documentation.
    if show_options:
        print("--input-file=%s" % str(input_kgtk_file), file=error_file)
        print("--output-file=%s" % str(output_kgtk_file), file=error_file)
        if list_output_kgtk_file is not None:
            print("--list-output-file=%s" % str(list_output_kgtk_file), file=error_file, flush=True)
        print("--columns=%s" % " ".join(key_column_names), file=error_file)
        print("--keep-first=%s" % " ".join(keep_first_names), file=error_file)
        print("--compact-id=%s" % str(compact_id), file=error_file, flush=True)
        print("--deduplicate=%s" % str(deduplicate), file=error_file, flush=True)
        print("--presorted=%s" % str(sorted_input), file=error_file, flush=True)
        print("--verify-sort=%s" % str(verify_sort), file=error_file, flush=True)
        print("--lists-in-input=%s" % str(lists_in_input), file=error_file, flush=True)
        print("--report-lists=%s" % str(report_lists), file=error_file, flush=True)
        print("--exclude-lists=%s" % str(exclude_lists), file=error_file, flush=True)
        print("--output-only-lists=%s" % str(output_only_lists), file=error_file, flush=True)
        print("--build-id=%s" % str(build_id), file=error_file, flush=True)
        idbuilder_options.show(out=error_file)
        reader_options.show(out=error_file)
        value_options.show(out=error_file)
        KgtkReader.show_debug_arguments(errors_to_stdout=errors_to_stdout,
                                        errors_to_stderr=errors_to_stderr,
                                        show_options=show_options,
                                        verbose=verbose,
                                        very_verbose=very_verbose,
                                        out=error_file)
        print("=======", file=error_file, flush=True)

    if exclude_lists and output_only_lists:
        raise KGTKException("--exclude-lists and --output-only-lists may not be used together.")

    try:
        ex: KgtkCompact = KgtkCompact(
            input_file_path=input_kgtk_file,
            output_file_path=output_kgtk_file,
            list_output_file_path=list_output_kgtk_file,
            key_column_names=key_column_names,
            keep_first_names=keep_first_names,
            compact_id=compact_id,
            deduplicate=deduplicate,
            sorted_input=sorted_input,
            verify_sort=verify_sort,
            lists_in_input=lists_in_input,
            report_lists=report_lists,
            exclude_lists=exclude_lists,
            output_only_lists=output_only_lists,
            build_id=build_id,
            idbuilder_options=idbuilder_options,
            reader_options=reader_options,
            value_options=value_options,
            error_file=error_file,
            verbose=verbose,
            very_verbose=very_verbose,
        )
        
        ex.process()

        return 0

    except SystemExit as e:
        raise KGTKException("Exit requested")
    except Exception as e:
        raise KGTKException(str(e))

