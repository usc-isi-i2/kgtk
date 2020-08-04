"""
Reorder KGTK file columns (while copying)

TODO: Need KgtkWriterOptions
"""

from argparse import Namespace, SUPPRESS
import typing

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles

def parser():
    return {
        'help': 'Perform calculations on KGTK file columns.',
        'description': 'This command performs calculations on one or more columns in a KGTK file. ' +
        '\nIf no input filename is provided, the default is to read standard input. ' +
        '\n\nAdditional options are shown in expert help.\nkgtk --expert rename_columns --help'
    }


def add_arguments_extended(parser: KGTKArgumentParser, parsed_shared_args: Namespace):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """
    # import modules locally
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
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

    parser.add_input_file()
    parser.add_output_file()

    parser.add_argument(      "--output-format", dest="output_format", help=h("The file format (default=kgtk)"), type=str)

    parser.add_argument('-c', "--columns", dest="column_names", required=True, nargs='+',
                        metavar="COLUMN_NAME",
                        help="The list of source column names, optionally containing '..' for column ranges " +
                        "and '...' for column names not explicitly mentioned.")
    parser.add_argument(      "--into", dest="into_column_name", help="The name of the column to receive the result of the calculation.", required=True)
    parser.add_argument(      "--do", dest="operation", help="The name of the operation.", required=True,
                              choices=["percentage"])

    parser.add_argument(      "--format", dest="format_string", help="The format string for the calculation.")

    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, expert=_expert)
    KgtkValueOptions.add_arguments(parser, expert=_expert)

def run(input_file: KGTKFiles,
        output_file: KGTKFiles,
        output_format: typing.Optional[str],

        column_names: typing.List[str],
        into_column_name: str,
        operation: str,
        format_string: typing.Optional[str],

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

    input_kgtk_file: Path = KGTKArgumentParser.get_input_file(input_file)
    output_kgtk_file: Path = KGTKArgumentParser.get_output_file(output_file)

    # Select where to send error messages, defaulting to stderr.
    error_file: typing.TextIO = sys.stdout if errors_to_stdout else sys.stderr

    # Build the option structures.
    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs)
    value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)

    # Show the final option structures for debugging and documentation.
    if show_options:
        print("--input-file=%s" % str(input_kgtk_file), file=error_file, flush=True)
        print("--output-file=%s" % str(output_kgtk_file), file=error_file, flush=True)
        if output_format is not None:
            print("--output-format=%s" % output_format, file=error_file, flush=True)
        print("--columns %s" % " ".join(column_names), file=error_file, flush=True)
        print("--into=%s" % str(into_column_name), file=error_file, flush=True)
        print("--operation=%s" % str(operation), file=error_file, flush=True)
        if format_string is not None:
            print("--format=%s" % format_string, file=error_file, flush=True)

        reader_options.show(out=error_file)
        value_options.show(out=error_file)
        print("=======", file=error_file, flush=True)

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
        selected_names: typing.List[str] = [ ]
        save_selected_names: typing.Optional[typing.List[str]] = None

        ellipses: str = "..." # All unmentioned columns
        ranger: str = ".." # All columns between two columns.

        saw_ranger: bool = False
        column_name: str
        for column_name in column_names:
            if column_name == ellipses:
                if save_selected_names is not None:
                    raise KGTKException("Elipses may appear only once")

                if saw_ranger:
                    raise KGTKException("ELipses may not appear directly after a range operator ('..').")

                save_selected_names = selected_names
                selected_names = [ ]
                continue

            if column_name == ranger:
                if len(selected_names) == 0:
                    raise KGTKException("The column range operator ('..') may not appear without a preceeding column name.")
                saw_ranger = True
                continue

            if column_name not in kr.column_names:
                raise KGTKException("Unknown column name '%s'." % column_name)
            if column_name not in remaining_names:
                raise KGTKException("Column name '%s' was duplicated in the list." % column_name)

            if saw_ranger:
                saw_ranger = False
                prior_column_name: str = selected_names[-1]
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
                   
                    selected_names.append(idx_column_name)
                    remaining_names.remove(idx_column_name)
                    idx += idx_inc

            selected_names.append(column_name)
            remaining_names.remove(column_name)

        if saw_ranger:
            raise KGTKException("The column ranger operator ('..') may not end the list of column names.")

        if len(remaining_names) > 0 and save_selected_names is None:
            if verbose:
                print("Omitting the following columns: %s" % " ".join(remaining_names))
        if save_selected_names is not None:
            if len(remaining_names) > 0:
                save_selected_names.extend(remaining_names)
            if len(selected_names) > 0:
                save_selected_names.extend(selected_names)
            selected_names = save_selected_names

        sources: typing.List[int] = [ ]
        name: str
        for name in selected_names:
            sources.append(kr.column_name_map[name])

        new_column: bool = False
        into_column_idx: int
        output_column_names: typing.List[str] = kr.column_names
        if into_column_name in kr.column_name_map:
            into_column_idx = kr.column_name_map[into_column_name]
            if verbose:
                print("Putting the result of the calculation into old column %d (%s)." % (into_column_idx, into_column_name), file=error_file, flush=True)
        else:
            new_column = True
            output_column_names = output_column_names.copy()
            into_column_idx = len(output_column_names)
            output_column_names.append(into_column_name)
            if verbose:
                print("Putting the result of the calculation into new column %d (%s)." % (into_column_idx, into_column_name), file=error_file, flush=True)

        if verbose:
            print("Opening the output file %s" % str(output_kgtk_file), file=error_file, flush=True)
        kw: KgtkWriter = KgtkWriter.open(output_column_names,
                                         output_kgtk_file,
                                         require_all_columns=True,
                                         prohibit_extra_columns=True,
                                         fill_missing_columns=False,
                                         gzip_in_parallel=False,
                                         mode=KgtkWriter.Mode[kr.mode.name],
                                         output_format=output_format,
                                         verbose=verbose,
                                         very_verbose=very_verbose,
        )

        input_data_lines: int = 0
        row: typing.List[str]
        for row in kr:
            input_data_lines += 1

            output_row: typing.List[str] = row.copy()
            if new_column:
                output_row.append("") # Easiest way to add a new column.

            if operation == "percentage":
                if len(selected_names) != 2:
                    raise KGTKException("Percent needs 2 input columns, got %d" % len(selected_names))
                
                fs: str = format_string if format_string is not None else "%5.2f"
                output_row[into_column_idx] = fs % (float(row[sources[0]]) * 100 / float(row[sources[1]]))

            kw.write(output_row)

        # Flush the output file so far:
        kw.flush()

        if verbose:
            print("Read %d data lines from file %s" % (input_data_lines, input_kgtk_file))

        kw.close()

        return 0

    except SystemExit as e:
        raise KGTKException("Exit requested")
    except Exception as e:
        raise KGTKException(str(e))

