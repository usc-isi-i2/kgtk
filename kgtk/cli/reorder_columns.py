"""
Reorder KGTK file columns (while copying)

TODO: Need KgtkWriterOptions

TODO: Make --as-columns modify the preceeding --columns such that
--as-columns can be applied selectively.
"""

from argparse import Namespace, SUPPRESS
import typing

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles

REORDER_COLUMNS_COMMAND: str = 'reorder-columns'
SELECT_COLUMNS_COMMAND: str = 'select-columns'

def parser():
    return {
        'aliases': [ SELECT_COLUMNS_COMMAND ],
        'help': 'Reorder KGTK file columns.',
        'description': 'This command reorders one or more columns in a KGTK file. ' +
        '\n\nReorder all columns using --columns col1 col2' +
        '\nReorder selected columns using --columns col1 col2 ... coln-1 coln' +
        '\nMove a column to the front: --columns col ...' +
        '\nMove a column to the end: --columns ... col' +
        '\nExtract named columns, omitting the rest: --columns col1 col2 --trim' +
        '\nMove a range of columns: --columns coln .. colm ...' +
        '\nIf no input filename is provided, the default is to read standard input. ' +
        '\n\nAdditional options are shown in expert help.\nkgtk --expert reorder-columns --help'
    }


def add_arguments_extended(parser: KGTKArgumentParser, parsed_shared_args: Namespace):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """
    # import modules locally
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions, KgtkReaderMode
    from kgtk.utils.argparsehelpers import optional_bool
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    _expert: bool = parsed_shared_args._expert
    _command: str = parsed_shared_args._command

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

    parser.add_argument(      "--output-format", dest="output_format", help=h("The file format (default=kgtk)"), type=str)

    parser.add_argument('-c', "--columns", "--column", dest="column_names_list", required=True, nargs='+', action="append", default=list(),
                              metavar="COLUMN_NAME",
                              help="The list of reordered column names, optionally containing '...' for column names not explicitly mentioned.")

    parser.add_argument(      "--as", "--as-columns", "--as-column", dest="as_column_names_list", nargs='+', action="append", default=list(),
                              metavar="COLUMN_NAME",
                              help="Replacement column names.")

    parser.add_argument(      "--trim", dest="omit_remaining_columns",
                              help="If true, omit unmentioned columns. (default=%(default)s).",
                              metavar="True|False",
                              type=optional_bool, nargs='?', const=True, default=(_command == SELECT_COLUMNS_COMMAND))

    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser,
                                    mode_options=True,
                                    default_mode=KgtkReaderMode.NONE,
                                    expert=_expert)
    KgtkValueOptions.add_arguments(parser, expert=_expert)

def run(input_file: KGTKFiles,
        output_file: KGTKFiles,
        output_format: typing.Optional[str],

        column_names_list: typing.List[typing.List[str]],
        as_column_names_list: typing.List[typing.List[str]],

        omit_remaining_columns: bool,

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
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions


    # Select where to send error messages, defaulting to stderr.
    error_file: typing.TextIO = sys.stdout if errors_to_stdout else sys.stderr

    input_kgtk_file: Path = KGTKArgumentParser.get_input_file(input_file)
    output_kgtk_file: Path = KGTKArgumentParser.get_output_file(output_file)

    # Build the option structures.
    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs)
    value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)

    # Condense the old and new columns names lists.
    column_names: typing.List[str] = list()
    column_name_list: typing.List[str]
    column_name: str
    if column_names_list is not None:
        for column_name_list in column_names_list:
            for column_name in column_name_list:
                column_names.append(column_name)

    as_column_names: typing.List[str] = list()
    if as_column_names_list is not None:
        for column_name_list in as_column_names_list:
            for column_name in column_name_list:
                as_column_names.append(column_name)

    # Show the final option structures for debugging and documentation.
    if show_options:
        print("--input-file=%s" % str(input_kgtk_file), file=error_file, flush=True)
        print("--output-file=%s" % str(output_kgtk_file), file=error_file, flush=True)
        if output_format is not None:
            print("--output-format=%s" % output_format, file=error_file, flush=True)
        print("--columns %s" % " ".join(column_names), file=error_file, flush=True)
        if len(as_column_names) > 0:
            print("--as-columns %s" % " ".join(as_column_names), file=error_file, flush=True)
        print("--trim=%s" % str(omit_remaining_columns), file=error_file, flush=True)
        reader_options.show(out=error_file)
        value_options.show(out=error_file)
        print("=======", file=error_file, flush=True)

    # Check for consistent options.  argparse doesn't support this yet.
    if len(as_column_names) > 0 and len(as_column_names) != len(column_names):
        raise KGTKException("Both --columns and --as-columns must have the same number of columns when --as-columns is used.")

    try:

        if verbose:
            print("Opening the input file %s" % str(input_kgtk_file), file=error_file, flush=True)
        kr = KgtkReader.open(input_kgtk_file,
                             options=reader_options,
                             value_options = value_options,
                             error_file=error_file,
                             verbose=verbose,
                             very_verbose=very_verbose,
        )

        remaining_names: typing.List[str] = kr.column_names.copy()
        reordered_names: typing.List[str] = [ ]
        save_reordered_names: typing.Optional[typing.List[str]] = None

        ellipses: str = "..." # All unmentioned columns
        ranger: str = ".." # All columns between two columns.

        saw_ranger: bool = False
        idx: int
        column_name: str
        for idx, column_name in enumerate(column_names):
            if column_name == ellipses:
                if len(as_column_names) > 0:
                    raise  KGTKException("The elipses operator ('...') may not appear when --as-columns is specified.")
                if save_reordered_names is not None:
                    raise KGTKException("Elipses may appear only once")

                if saw_ranger:
                    raise KGTKException("Elipses may not appear directly after a range operator ('..').")

                save_reordered_names = reordered_names
                reordered_names = [ ]
                continue

            if column_name == ranger:
                if len(reordered_names) == 0:
                    raise KGTKException("The column range operator ('..') may not appear without a preceeding column name.")
                if len(as_column_names) > 0:
                    raise  KGTKException("The column range operator ('..') may not appear when --as-columns is specified.")
                saw_ranger = True
                continue

            if column_name not in kr.column_names:
                raise KGTKException("Unknown column name '%s'." % column_name)
            if column_name not in remaining_names:
                raise KGTKException("Column name '%s' was duplicated in the list." % column_name)

            if saw_ranger:
                saw_ranger = False
                prior_column_name: str = reordered_names[-1]
                prior_column_idx: int = kr.column_name_map[prior_column_name]
                column_name_idx: int = kr.column_name_map[column_name]
                start_idx: int
                end_idx: int
                idx_inc: int
                if column_name_idx > prior_column_idx:
                    start_idx = prior_column_idx + 1
                    end_idx = column_name_idx - 1
                    idx_inc = 1
                else:
                    start_idx = prior_column_idx - 1
                    end_idx = column_name_idx + 1
                    idx_inc = -1

                idx: int = start_idx
                while idx <= end_idx:
                    idx_column_name: str = kr.column_names[idx]
                    if idx_column_name not in remaining_names:
                        raise KGTKException("Column name '%s' (%s .. %s) was duplicated in the list." % (column_name, prior_column_name, column_name))
                   
                    reordered_names.append(idx_column_name)
                    remaining_names.remove(idx_column_name)
                    idx += idx_inc

            reordered_names.append(column_name)
            remaining_names.remove(column_name)

        if saw_ranger:
            raise KGTKException("The column ranger operator ('..') may not end the list of column names.")

        if len(remaining_names) > 0 and save_reordered_names is None:
            # There are remaining column names and the ellipses was not seen.
            if not omit_remaining_columns:
                raise KGTKException("No ellipses, and the following columns not accounted for: %s" % " ".join(remaining_names))
            else:
                if verbose:
                    print("Omitting the following columns: %s" % " ".join(remaining_names), file=error_file, flush=True)
        if save_reordered_names is not None:
            if len(remaining_names) > 0:
                save_reordered_names.extend(remaining_names)
            if len(reordered_names) > 0:
                save_reordered_names.extend(reordered_names)
            reordered_names = save_reordered_names

        if verbose:
            print("Opening the output file %s" % str(output_kgtk_file), file=error_file, flush=True)
        kw: KgtkWriter = KgtkWriter.open(reordered_names,
                                         output_kgtk_file,
                                         output_column_names=as_column_names,
                                         require_all_columns=True,
                                         prohibit_extra_columns=True,
                                         fill_missing_columns=False,
                                         gzip_in_parallel=False,
                                         mode=KgtkWriter.Mode[kr.mode.name],
                                         output_format=output_format,
                                         verbose=verbose,
                                         very_verbose=very_verbose,
        )

        shuffle_list: typing.List = kw.build_shuffle_list(kr.column_names)

        input_data_lines: int = 0
        row: typing.List[str]
        for row in kr:
            input_data_lines += 1
            kw.write(row, shuffle_list=shuffle_list)

        # Flush the output file so far:
        kw.flush()

        if verbose:
            print("Read %d data lines from file %s" % (input_data_lines, input_kgtk_file), file=error_file, flush=True)

        kw.close()

        return 0

    except SystemExit as e:
        raise KGTKException("Exit requested")
    except Exception as e:
        raise KGTKException(str(e))

