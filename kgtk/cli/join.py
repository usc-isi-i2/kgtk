"""
Join two KGTK edge files or two KGTK node files.

TODO: Need KgtkWriterOptions
"""

from argparse import Namespace, SUPPRESS
import typing

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles

def parser():
    return {
        'help': 'Join two KGTK files',
        'description': """Join two KGTK edge files or two KGTK node files.

Join keys are extracted from one or both input files and stored in memory,
then the data files are processed in a second pass.  stdin will not work as an
input file if join keys are needed from it.

The output file contains the union of the columns in the two
input files, adjusted for predefined name aliasing.

Specify --left-join to get a left outer join.
        The output file will contain all records from the
        left input file, along with records from the right
        input file with matching join column values.

Specify --right-join to get a right outer join.
        The output file will contain all records from the
        right input file, along with records from the left
        input file with matching join column values.

Specify both --left-join and --right-join to get a full outer
join (equivalent to cat or set union).
        The output file will contain all records from both
        the left input file and the right input file.

Specify neither --left-join nor --right-join to get an inner
join.  If there are no columns beyond the join columns, then
this is equivalent to set intersection.
        The output file will contain records from the left
        input file and from the right input file for which
        the join column value match.

By default, node files are joined on the id column, while edge files are joined
on the node1 column. The label and node2 columns may be added to the edge file
join criteria.  Alternatively, the left and right file join columns may be
listed explicitly.

To join an edge file to a node file, or to join quasi-KGTK files, use the
following option (enable expert mode for more information):

--mode=NONE

Expert mode provides additional command arguments.
"""
    }


def add_arguments_extended(parser: KGTKArgumentParser, parsed_shared_args: Namespace):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions, KgtkReaderMode
    from kgtk.join.kgtkjoiner import KgtkJoiner
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

    parser.add_input_file(who="The left-side KGTK file to join (required).",
                          dest="left_file",
                          options=["--left-file"],
                          metavar="LEFT_FILE",
                          positional=True)

    parser.add_input_file(who="The right-side KGTK file to join (required).",
                          dest="right_file",
                          options=["--right-file"],
                          metavar="RIGHT_FILE",
                          positional=True)

    parser.add_output_file()

    parser.add_argument(      "--join-on-id", dest="join_on_id",
                              help="If both input files are edge files, include the id column in the join (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--join-on-label", dest="join_on_label",
                              help="If both input files are edge files, include the label column in the join (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--join-on-node2", dest="join_on_node2",
                              help="If both input files are edge files, include the node2 column in the join (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)
    
    parser.add_argument(      "--left-prefix", dest="left_prefix",
                              help="An optional prefix applied to left file column names in the output file (default=None).")
    
    parser.add_argument(      "--left-file-join-columns", dest="left_join_columns", help="Left file join columns (default=None).", nargs='+')

    parser.add_argument(      "--left-join", dest="left_join", help="Perform a left outer join (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--right-prefix", "--prefix", dest="right_prefix",
                              help="An optional prefix applied to right file column names in the output file (default=None).")
    
    parser.add_argument(      "--right-file-join-columns", dest="right_join_columns", help="Right file join columns (default=None).", nargs='+')
    
    parser.add_argument(      "--right-join", dest="right_join", help="Perform a right outer join (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--field-separator", dest="field_separator",
                              help=h("Separator for multifield keys (default=%(default)s)")
                              , default=KgtkJoiner.FIELD_SEPARATOR_DEFAULT)

    # Build the command arguments. File arguments can be set for individual
    # files, or for all files.
    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser,
                                    mode_options=True,
                                    default_mode=KgtkReaderMode[parsed_shared_args._mode],
                                    expert=_expert)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, who="left", expert=_expert, defaults=False)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, who="right", expert=_expert, defaults=False)
    KgtkValueOptions.add_arguments(parser, expert=_expert)

def run(left_file: KGTKFiles,
        right_file: KGTKFiles,
        output_file: KGTKFiles,

        join_on_id: bool = False,
        join_on_label: bool = False,
        join_on_node2: bool = False,

        left_prefix: typing.Optional[str] = None,
        left_join_columns: typing.Optional[typing.List[str]] = None,
        left_join: bool = False,

        right_prefix: typing.Optional[str] = None,
        right_join_columns: typing.Optional[typing.List[str]] = None,
        right_join: bool = False,

        field_separator: typing.Optional[str] = None,

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
    from kgtk.join.kgtkjoiner import KgtkJoiner
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    left_file_path: Path = KGTKArgumentParser.get_input_file(left_file, who="KGTK left file")
    right_file_path: Path = KGTKArgumentParser.get_input_file(right_file, who="KGTK right file")
    output_file_path: Path = KGTKArgumentParser.get_output_file(output_file)

    field_separator = KgtkJoiner.FIELD_SEPARATOR_DEFAULT if field_separator is None else field_separator

    # Select where to send error messages, defaulting to stderr.
    error_file: typing.TextIO = sys.stdout if errors_to_stdout else sys.stderr

    if not right_join:
        if str(left_file_path) == "-":
            print("The left file may not be stdin when an inner join or left join is requested.", file=error_file, flush=True)
            return 1

    if not left_join:
        if str(right_file_path) == "-":
            print("The right file may not be stdin when an inner join or right join is requested.", file=error_file, flush=True)
            return 1

    if str(left_file_path) == "-" and str(right_file_path) == "-":
        print("The left and right files may not both be stdin.", file=error_file, flush=True)
        return 1

    # Build the option structures.
    left_reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs, who="left", fallback=True)
    right_reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs, who="right", fallback=True)
    value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)

    # Show the final option structures for debugging and documentation.
    if show_options:
        # TODO: left_file_path, right_file_path, --join-on-label, etc.
        print("--left-file=%s" % str(left_file_path), file=error_file)
        print("--right-file=%s" % str(right_file_path), file=error_file)
        print("--output-file=%s" % str(output_file_path), file=error_file)
        
        print("--left-join=%s" % str(left_join), file=error_file)
        print("--right-join=%s" % str(right_join), file=error_file)
        print("--join-on-id=%s" % str(join_on_id), file=error_file)
        print("--join-on-label=%s" % str(join_on_label), file=error_file)
        print("--join-on-node2=%s" % str(join_on_node2), file=error_file)
        if left_join_columns is not None:
            print("--left-join-columns=%s" % " ".join(left_join_columns), file=error_file)
        if right_join_columns is not None:
            print("--right-join-columns=%s" % " ".join(right_join_columns), file=error_file)
        if left_prefix is not None:
            print("--left-prefix=%s" % str(left_prefix), file=error_file)
        if right_prefix is not None:
            print("--right-prefix=%s" % str(right_prefix), file=error_file)
        print("--field-separator=%s" % repr(field_separator), file=error_file)
              
        left_reader_options.show(out=error_file, who="left")
        right_reader_options.show(out=error_file, who="right")
        value_options.show(out=error_file)

    try:
        kr: KgtkJoiner = KgtkJoiner(
            left_file_path=left_file_path,
            right_file_path=right_file_path,
            output_path=output_file_path,
            left_join=left_join,
            right_join=right_join,
            join_on_id=join_on_id,
            join_on_label=join_on_label,
            join_on_node2=join_on_node2,
            left_join_columns=left_join_columns,
            right_join_columns=right_join_columns,
            left_prefix=left_prefix,
            right_prefix=right_prefix,
            field_separator=field_separator,
            left_reader_options=left_reader_options,
            right_reader_options=right_reader_options,
            value_options=value_options,
            error_file=error_file,
            verbose=verbose,
            very_verbose=very_verbose,
        )
        
        kr.process()

        return 0

    except SystemExit as e:
        raise KGTKException("Exit requested")
    except Exception as e:
        raise KGTKException(str(e))

