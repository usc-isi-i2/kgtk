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

# Future:

# Numeric:
ABS_OP: str = "abs" # column
DIV_OP: str = "div" # (column / column) or (column / value)
MOD_OP: str = "mod" # (column mod column) or (column mod value)
POW_OP: str = "pow"
MINUS_OP: str = "minus" # (column - column) or (column - value)
NEGATE_OP: str = "negate"

# String
CENTER_OP: str = "center"
COUNT_OP: str = "count"
ENDSWITH_OP: str = "endswidth"
EXPANDTABS_OP: str = "expandtabs"
FIND_OP: str = "find"
ISALNUM_OP: str = "isalnum"
# ...
LJUST_OP: str = "ljust"
LSTRIP_OP: str = "lstrip"
PARTITION_OP: str = "partition"
REMOVEPREFIX_OP: str = "removeprefix"
REMOVESUFFIX_OP: str = "removesuffix"
RFIND_OP: str = "rfind"
RJUST_OP: str = "rjust"
RPARTITION_OP: str = "rpartition"
RSPLIT_OP: str = "rsplit"
RSTRIP_OP: str = "rstrip"
SPLIT_OP: str = " split"
SPLITLINES_OP: str = "splitlines"
STARTSWITH_OP: str = "startswith"
STRIP_OP: str = "strip"
ZFILL_OP: str = "zfill"

# Implemented:

# Boolean
AND_OP: str = "and" # (boolean, boolean) -> boolean
NAND_OP: str = "nand" # (boolean, boolean) -> boolean
NOR_OP: str = "nor" # (boolean, boolean) -> boolean
NOT_OP: str = "not" # (boolean, ...) -> (boolean, ...)
OR_OP: str = "or" # (boolean, boolean) -> boolean
XOR_OP: str = "xor" # (boolean, boolean) -> boolean

# Numeric
AVERAGE_OP: str = "average"
MAX_OP: str = "max"
MIN_OP: str = "min"
PERCENTAGE_OP: str = "percentage"
SUM_OP: str = "sum" # Sums the columns and the values.
GE_OP: str = "ge" # (column > column) or (column > value) -> boolean
GT_OP: str = "gt" # (column >= column) or (column >= value) -> boolean
LT_OP: str = "lt" # (column < column) or (column < value) -> boolean
LE_OP: str = "le" # (column <= column) or (column <= value) -> boolean
EQ_OP: str = "eq" # (column == column) or (column == value) -> boolean
NE_OP: str = "ne" # (column != column) or (column != value) -> boolean

# String
CAPITALIZE_OP: str = "capitalize"
CASEFOLD_OP: str = "casefold"
JOIN_OP: str = "join"
LOWER_OP: str = "lower"
REPLACE_OP: str = "replace"
SUBSTITUTE_OP: str = "substitute"
SWAPCASE_OP: str = "swapcase"
TITLE_OP: str = "title"
UPPER_OP: str = "upper"

# General
COPY_OP: str = "copy"
IS_OP: str = "is" # (column == column) or (column == value) -> boolean
IS_IN_OP: str = "is_in" # column in values -> boolean
IS_NOT_OP: str = "is_not" # (column != column) or (column != value) -> boolean
SET_OP: str = "set"

# Date/Time
FROMISOFORMAT_OP: str = "fromisoformat"

OPERATIONS: typing.List[str] = [ AND_OP,
                                 AVERAGE_OP,
                                 CAPITALIZE_OP,
                                 CASEFOLD_OP,
                                 COPY_OP,
                                 EQ_OP,
                                 FROMISOFORMAT_OP,
                                 GE_OP,
                                 GT_OP,
                                 IS_OP,
                                 IS_IN_OP,
                                 IS_NOT_OP,
                                 JOIN_OP,
                                 LOWER_OP,
                                 LE_OP,
                                 LT_OP,
                                 MAX_OP,
                                 MIN_OP,
                                 NAND_OP,
                                 NE_OP,
                                 NOR_OP,
                                 NOT_OP,
                                 OR_OP,
                                 PERCENTAGE_OP,
                                 REPLACE_OP,
                                 SET_OP,
                                 SUBSTITUTE_OP,
                                 SUM_OP,
                                 SWAPCASE_OP,
                                 TITLE_OP,
                                 UPPER_OP,
                                 XOR_OP,
                                ]

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

    parser.add_argument('-c', "--columns", dest="column_names_list", nargs='*', metavar="COLUMN_NAME", action='append',
                        help="The list of source column names, optionally containing '..' for column ranges " +
                        "and '...' for column names not explicitly mentioned.")

    parser.add_argument(      "--into", dest="into_column_names_list", nargs='+', metavar="COLUMN_NAME", action='append',
                              help="The name of the column to receive the result of the calculation.",
                              required=True)

    parser.add_argument(      "--do", dest="operation", help="The name of the operation.", required=True,
                              choices=OPERATIONS)

    parser.add_argument(      "--values", dest="values_list", nargs='*', metavar="VALUES", action='append',
                        help="An optional list of values")

    parser.add_argument(      "--with-values", dest="with_values_list", nargs='*', metavar="WITH_VALUES", action='append',
                        help="An optional list of additional values")

    parser.add_argument(      "--limit", dest="limit", type=int,
                              help="A limit count.")

    parser.add_argument(      "--format", dest="format_string", help="The format string for the calculation.")

    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, expert=_expert)
    KgtkValueOptions.add_arguments(parser, expert=_expert)

def flatten_arg_list(arg: typing.Optional[typing.List[typing.List[str]]])->typing.List[str]:
    result: typing.List[str] = [ ]
    if arg is None:
        return result

    arglist: typing.List[str]
    for arglist in arg:
        value: str
        for value in arglist:
            if value is not None:
                result.append(value)

    return result

def run(input_file: KGTKFiles,
        output_file: KGTKFiles,
        output_format: typing.Optional[str],

        column_names_list: typing.List[typing.List[str]],
        into_column_names_list: typing.List[typing.List[str]],
        operation: str,
        values_list: typing.List[typing.List[str]],
        with_values_list: typing.List[typing.List[str]],
        limit: typing.Optional[int],
        format_string: typing.Optional[str],

        errors_to_stdout: bool = False,
        errors_to_stderr: bool = True,
        show_options: bool = False,
        verbose: bool = False,
        very_verbose: bool = False,

        **kwargs # Whatever KgtkFileOptions and KgtkValueOptions want.
)->int:
    # import modules locally
    import datetime as dt
    from pathlib import Path
    import re
    import sys

    from kgtk.exceptions import KGTKException
    from kgtk.kgtkformat import KgtkFormat
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
    from kgtk.io.kgtkwriter import KgtkWriter
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions
    from kgtk.value.kgtkvalue import KgtkValue

    input_kgtk_file: Path = KGTKArgumentParser.get_input_file(input_file)
    output_kgtk_file: Path = KGTKArgumentParser.get_output_file(output_file)

    # Select where to send error messages, defaulting to stderr.
    error_file: typing.TextIO = sys.stdout if errors_to_stdout else sys.stderr

    # Build the option structures.
    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs)
    value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)

    # Flatten the input lists.
    column_names: typing.List[str] = flatten_arg_list(column_names_list)
    into_column_names: typing.List[str] = flatten_arg_list(into_column_names_list)
    values: typing.List[str] = flatten_arg_list(values_list)
    with_values: typing.List[str] = flatten_arg_list(with_values_list)

    # Show the final option structures for debugging and documentation.
    if show_options:
        print("--input-file=%s" % str(input_kgtk_file), file=error_file, flush=True)
        print("--output-file=%s" % str(output_kgtk_file), file=error_file, flush=True)
        if output_format is not None:
            print("--output-format=%s" % output_format, file=error_file, flush=True)
        if len(column_names) > 0:
            print("--columns %s" % " ".join(column_names), file=error_file, flush=True)
        if len(into_column_names) > 0:
            print("--into %s" % " ".join(into_column_names), file=error_file, flush=True)
        print("--operation=%s" % str(operation), file=error_file, flush=True)
        if len(values) > 0:
            print("--values %s" % " ".join(values), file=error_file, flush=True)
        if len(with_values) > 0:
            print("--with-values %s" % " ".join(with_values), file=error_file, flush=True)
        if limit is not None:
            print("--limit %d" % limit, file=error_file, flush=True)
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

        idx: int

        saw_ranger: bool = False
        column_name: str
        for column_name in column_names:
            if column_name == ellipses:
                if save_selected_names is not None:
                    raise KGTKException("Elipses may appear only once")

                if saw_ranger:
                    raise KGTKException("Elipses may not appear directly after a range operator ('..').")

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

                idx = start_idx
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
                print("Omitting the following columns: %s" % " ".join(remaining_names), file=error_file, flush=True)
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

        new_column_count: int = 0
        into_column_idxs: typing.List[int] = [ ]
        into_column_idx: int
        output_column_names: typing.List[str] = kr.column_names.copy()
        into_column_name: str
        for idx, into_column_name in enumerate(into_column_names):
            if into_column_name in kr.column_name_map:
                into_column_idx = kr.column_name_map[into_column_name]
                into_column_idxs.append(into_column_idx)
                if verbose:
                    print("Putting result %d of the calculation into old column %d (%s)." % (idx + 1, into_column_idx, into_column_name), file=error_file, flush=True)
            else:
                new_column_count += 1
                into_column_idx = len(output_column_names)
                into_column_idxs.append(into_column_idx)
                output_column_names.append(into_column_name)
                if verbose:
                    print("Putting result %d of the calculation into new column %d (%s)." % (idx + 1, into_column_idx, into_column_name), file=error_file, flush=True)

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

        if limit is None:
            limit = 0

        substitute_re: typing.Optional[typing.Pattern] = None

        if operation == AND_OP:
            if len(sources) == 0:
                raise KGTKException("And needs at least one source, got %d" % len(sources))
            if len(into_column_idxs) != 1:
                raise KGTKException("And needs 1 destination column, got %d" % len(into_column_idxs))

        elif operation == AVERAGE_OP:
            if len(sources) == 0:
                raise KGTKException("Average needs at least one source, got %d" % len(sources))
            if len(into_column_idxs) != 1:
                raise KGTKException("Average needs 1 destination column, got %d" % len(into_column_idxs))

        elif operation == CAPITALIZE_OP:
            if len(sources) == 0:
                raise KGTKException("Capitalize needs at least one source, got %d" % len(sources))
            if len(sources) != len(into_column_idxs):
                raise KGTKException("Capitalize needs the same number of input columns and into columns, got %d and %d" % (len(sources), len(into_column_idxs)))

        elif operation == CASEFOLD_OP:
            if len(sources) == 0:
                raise KGTKException("Casefold needs at least one source, got %d" % len(sources))
            if len(sources) != len(into_column_idxs):
                raise KGTKException("Casefold needs the same number of input columns and into columns, got %d and %d" % (len(sources), len(into_column_idxs)))

        elif operation == COPY_OP:
            if len(sources) == 0:
                raise KGTKException("Copy needs at least one source, got %d" % len(sources))
            if len(selected_names) != len(into_column_idxs):
                raise KGTKException("Copy needs the same number of input columns and into columns, got %d and %d" % (len(selected_names), len(into_column_idxs)))

        elif operation == EQ_OP:
            if (len(sources) == 2 and len(values) == 0) or (len(sources) == 1 and len(values) == 1):
                raise KGTKException("Eq needs two sources or one source and one value, got %d sources and %d values" % (len(sources), len(values)))
            if len(into_column_idxs) != 1:
                raise KGTKException("Eq needs 1 destination columns, got %d" % len(into_column_idxs))

        elif operation == FROMISOFORMAT_OP:
            if len(sources) != 1:
                raise KGTKException("Fromisoformat needs one source, got %d" % len(sources))
            if len(values) != len(into_column_idxs):
                raise KGTKException("Fromisoformat needs the same number of values and into columns, got %d and %d" % (len(values), len(into_column_idxs)))

        elif operation == GE_OP:
            if (len(sources) == 2 and len(values) == 0) or (len(sources) == 1 and len(values) == 1):
                raise KGTKException("Ge needs two sources or one source and one value, got %d sources and %d values" % (len(sources), len(values)))
            if len(into_column_idxs) != 1:
                raise KGTKException("Ge needs 1 destination columns, got %d" % len(into_column_idxs))

        elif operation == GT_OP:
            if (len(sources) == 2 and len(values) == 0) or (len(sources) == 1 and len(values) == 1):
                raise KGTKException("Gt needs two sources or one source and one value, got %d sources and %d values" % (len(sources), len(values)))
            if len(into_column_idxs) != 1:
                raise KGTKException("Gt needs 1 destination columns, got %d" % len(into_column_idxs))

        elif operation == IS_OP:
            if (len(sources) == 2 and len(values) == 0) or (len(sources) == 1 and len(values) == 1):
                raise KGTKException("Is needs two sources or one source and one value, got %d sources and %d values" % (len(sources), len(values)))
            if len(into_column_idxs) != 1:
                raise KGTKException("Is needs 1 destination columns, got %d" % len(into_column_idxs))

        elif operation == IS_IN_OP:
            if len(sources) != 1:
                raise KGTKException("Is in needs one source, got %d" % len(sources))
            if len(values) == 0:
                raise KGTKException("Is in needs at least one value, got %d" % len(values))
            if len(into_column_idxs) != 1:
                raise KGTKException("Is in needs 1 destination columns, got %d" % len(into_column_idxs))

        elif operation == IS_NOT_OP:
            if (len(sources) == 2 and len(values) == 0) or (len(sources) == 1 and len(values) == 1):
                raise KGTKException("Is not needs two sources or one source and one value, got %d sources and %d values" % (len(sources), len(values)))
            if len(into_column_idxs) != 1:
                raise KGTKException("Is not needs 1 destination columns, got %d" % len(into_column_idxs))

        elif operation == JOIN_OP:
            if len(sources) == 0:
                raise KGTKException("Join needs at least one source, got %d" % len(sources))
            if len(into_column_idxs) != 1:
                raise KGTKException("Join needs 1 destination columns, got %d" % len(into_column_idxs))
            if len(values) != 1:
                raise KGTKException("Join needs 1 value, got %d" % len(values))

        elif operation == LE_OP:
            if (len(sources) == 2 and len(values) == 0) or (len(sources) == 1 and len(values) == 1):
                raise KGTKException("Le needs two sources or one source and one value, got %d sources and %d values" % (len(sources), len(values)))
            if len(into_column_idxs) != 1:
                raise KGTKException("Le needs 1 destination columns, got %d" % len(into_column_idxs))

        elif operation == LT_OP:
            if (len(sources) == 2 and len(values) == 0) or (len(sources) == 1 and len(values) == 1):
                raise KGTKException("Lt needs two sources or one source and one value, got %d sources and %d values" % (len(sources), len(values)))
            if len(into_column_idxs) != 1:
                raise KGTKException("Lt needs 1 destination columns, got %d" % len(into_column_idxs))

        elif operation == LOWER_OP:
            if len(sources) == 0:
                raise KGTKException("Lower needs at least one source, got %d" % len(sources))
            if len(sources) != len(into_column_idxs):
                raise KGTKException("Lower needs the same number of input columns and into columns, got %d and %d" % (len(sources), len(into_column_idxs)))

        elif operation == MAX_OP:
            if len(sources) == 0:
                raise KGTKException("Max needs at least one source, got %d" % len(sources))
            if len(into_column_idxs) != 1:
                raise KGTKException("Max needs 1 destination columns, got %d" % len(into_column_idxs))

        elif operation == MIN_OP:
            if len(sources) == 0:
                raise KGTKException("Min needs at least one source, got %d" % len(sources))
            if len(into_column_idxs) != 1:
                raise KGTKException("Min needs 1 destination columns, got %d" % len(into_column_idxs))

        elif operation == NE_OP:
            if (len(sources) == 2 and len(values) == 0) or (len(sources) == 1 and len(values) == 1):
                raise KGTKException("Ne needs two sources or one source and one value, got %d sources and %d values" % (len(sources), len(values)))
            if len(into_column_idxs) != 1:
                raise KGTKException("Ne needs 1 destination columns, got %d" % len(into_column_idxs))

        elif operation == NOR_OP:
            if len(sources) == 0:
                raise KGTKException("Nor needs at least one source, got %d" % len(sources))
            if len(into_column_idxs) != 1:
                raise KGTKException("Nor needs 1 destination column, got %d" % len(into_column_idxs))

        elif operation == NOT_OP:
            if len(sources) == 0:
                raise KGTKException("Not needs at least one source, got %d" % len(sources))
            if len(into_column_idxs) != len(sources):
                raise KGTKException("Nand needs the same number of input columns and into colums, got %d and %d" % (len(sources), len(into_column_idxs)))

        elif operation == OR_OP:
            if len(sources) == 0:
                raise KGTKException("Or needs at least one source, got %d" % len(sources))
            if len(into_column_idxs) != 1:
                raise KGTKException("Or needs 1 destination column, got %d" % len(into_column_idxs))

        elif operation == PERCENTAGE_OP:
            if len(into_column_idxs) != 1:
                raise KGTKException("Percent needs 1 destination columns, got %d" % len(into_column_idxs))
            if len(selected_names) != 2:
                raise KGTKException("Percent needs 2 input columns, got %d" % len(selected_names))

        elif operation == REPLACE_OP:
            if len(into_column_idxs) != 1:
                raise KGTKException("Replace needs 1 destination column, got %d" % len(into_column_idxs))
            if len(selected_names) != 1:
                raise KGTKException("Replace needs 1 input column, got %d" % len(selected_names))
            if len(values) != 1:
                raise KGTKException("Replace needs one value, got %d" % len(values))
            if len(with_values) != 1:
                raise KGTKException("Replace needs one with-value, got %d" % len(with_values))

        elif operation == SET_OP:
            if len(sources) != 0:
                raise KGTKException("Set needs no sources, got %d" % len(sources))
            if len(into_column_idxs) == 0:
                raise KGTKException("Set needs at least one destination column, got %d" % len(into_column_idxs))
            if len(values) == 0:
                raise KGTKException("Set needs at least one value, got %d" % len(values))
            if len(into_column_idxs) != len(values):
                raise KGTKException("Set needs the same number of destination columns and values, got %d and %d" % (len(into_column_idxs), len(values)))

        elif operation == SUBSTITUTE_OP:
            if len(into_column_idxs) != 1:
                raise KGTKException("Substitute needs 1 destination column, got %d" % len(into_column_idxs))
            if len(selected_names) != 1:
                raise KGTKException("Substitute needs 1 input column, got %d" % len(selected_names))
            if len(values) != 1:
                raise KGTKException("Substitute needs one value, got %d" % len(values))
            if len(with_values) != 1:
                raise KGTKException("Substitute needs one with-value, got %d" % len(with_values))
            substitute_re = re.compile(values[0])

        elif operation == SUM_OP:
            if len(sources) == 0:
                raise KGTKException("Sum needs at least one source, got %d" % len(sources))
            if len(into_column_idxs) != 1:
                raise KGTKException("Sum needs 1 destination columns, got %d" % len(into_column_idxs))

        elif operation == SWAPCASE_OP:
            if len(sources) == 0:
                raise KGTKException("Swapcase needs at least one source, got %d" % len(sources))
            if len(sources) != len(into_column_idxs):
                raise KGTKException("Swapcase needs the same number of input columns and into columns, got %d and %d" % (len(sources), len(into_column_idxs)))

        elif operation == TITLE_OP:
            if len(sources) == 0:
                raise KGTKException("Title needs at least one source, got %d" % len(sources))
            if len(sources) != len(into_column_idxs):
                raise KGTKException("Title needs the same number of input columns and into columns, got %d and %d" % (len(sources), len(into_column_idxs)))

        elif operation == UPPER_OP:
            if len(sources) == 0:
                raise KGTKException("Upper needs at least one source, got %d" % len(sources))
            if len(sources) != len(into_column_idxs):
                raise KGTKException("Upper needs the same number of input columns and into columns, got %d and %d" % (len(sources), len(into_column_idxs)))

        elif operation == XOR_OP:
            if len(sources) == 0:
                raise KGTKException("Xor needs at least one source, got %d" % len(sources))
            if len(into_column_idxs) != 1:
                raise KGTKException("Xor needs 1 destination column, got %d" % len(into_column_idxs))


        fs: str = format_string if format_string is not None else "%5.2f"
        item: str
        item2: str
        kv: KgtkValue
        bresult: bool

        into_column_idx = into_column_idxs[0] # for convenience

        input_data_lines: int = 0
        row: typing.List[str]
        for row in kr:
            input_data_lines += 1

            output_row: typing.List[str] = row.copy()
            for idx in range(new_column_count):
                output_row.append("") # Easiest way to add a new column.

            if operation == AND_OP:
                bresult = True
                for idx in sources:
                    kv = KgtkValue(row[idx])
                    if kv.is_boolean():
                        bresult = bresult and kv.is_true()

                output_row[into_column_idx] = KgtkValue.to_boolean(bresult)

            elif operation == AVERAGE_OP:
                atotal: float = 0
                acount: int = 0
                for idx in sources:
                    item = row[idx]
                    if len(item) > 0:
                        atotal += float(item)
                        acount += 1
                output_row[into_column_idx] = (fs % (atotal / float(acount))) if acount > 0 else ""                

            elif operation == CAPITALIZE_OP:
                for idx in range(len(sources)):
                    output_row[into_column_idxs[idx]] = row[sources[idx]].capitalize()

            elif operation == CASEFOLD_OP:
                for idx in range(len(sources)):
                    output_row[into_column_idxs[idx]] = row[sources[idx]].casefold()

            elif operation == COPY_OP:
                for idx in range(len(sources)):
                    output_row[into_column_idxs[idx]] = row[sources[idx]]

            elif operation == EQ_OP:
                if len(sources) == 1:
                    if len(row[sources[0]]) > 0 and len(row[sources[1]]) > 0:
                        output_row[into_column_idx] = KgtkValue.to_boolean(float(row[sources[0]]) == float(row[sources[1]]))
                    else:
                        output_row[into_column_idx] = ""
                else:
                    if len(row[sources[0]]) > 0 and len(values[0]) > 0:
                        output_row[into_column_idx] = KgtkValue.to_boolean(float(row[sources[0]]) == float(values[0]))
                    else:
                        output_row[into_column_idx] = ""

            elif operation == FROMISOFORMAT_OP:
                dtval: str = row[sources[0]]
                if dtval.startswith(KgtkFormat.DATE_AND_TIMES_SIGIL):
                    kgtkdatestr: str = row[sources[0]][1:] # Strip the leading ^
                    isodatestr: str
                    precisionstr: str
                    if "/" in kgtkdatestr:
                        isodatestr, precisionstr = kgtkdatestr.split("/")
                    else:
                        isodatestr = kgtkdatestr
                        precisionstr = ""
                    if isodatestr.endswith("Z"):
                        isodatestr = isodatestr[:-1]

                    into_idx: int
                    value_name: str
                    try:
                        dtvar: dt.datetime = dt.datetime.fromisoformat(isodatestr)
                        for idx in range(len(values)):
                            value_name = values[idx]
                            into_idx = into_column_idxs[idx]
                            
                            if value_name == "year":
                                output_row[into_idx] = str(dtvar.year)

                            elif value_name == "month":
                                output_row[into_idx] = str(dtvar.month)
                    
                            elif value_name == "day":
                                output_row[into_idx] = str(dtvar.day)

                            elif value_name == "hour":
                                output_row[into_idx] = str(dtvar.hour)
                    
                            elif value_name == "minute":
                                output_row[into_idx] = str(dtvar.minute)
                    
                            elif value_name == "second":
                                output_row[into_idx] = str(dtvar.second)
                    
                            elif value_name == "microsecond":
                                output_row[into_idx] = str(dtvar.microsecond)

                            elif value_name == "error":
                                output_row[into_idx] = ""

                            else:
                                raise KGTKException("Unknown date component %s" % repr(value_name))

                    except ValueError as e:
                        print("Error parsing %s in [%s]: %s" % (repr(isodatestr), "|".join([repr(x) for x in row]), str(e)),
                              file=error_file, flush=True)

                        for idx in range(len(values)):
                            value_name = values[idx]
                            into_idx = into_column_idxs[idx]
                            if value_name == "error":
                                output_row[into_idx] = str(e)
                            else:
                                output_row[into_idx] = ""

                else:
                    # Not a date/time value, clear the result columns.
                    for idx in range(len(values)):
                        output_row[into_column_idxs[idx]] = ""
                    
            elif operation == GE_OP:
                if len(sources) == 1:
                    if len(row[sources[0]]) > 0 and len(row[sources[1]]) > 0:
                        output_row[into_column_idx] = KgtkValue.to_boolean(float(row[sources[0]]) >= float(row[sources[1]]))
                    else:
                        output_row[into_column_idx] = ""
                else:
                    if len(row[sources[0]]) > 0 and len(values[0]) > 0:
                        output_row[into_column_idx] = KgtkValue.to_boolean(float(row[sources[0]]) >= float(values[0]))
                    else:
                        output_row[into_column_idx] = ""

            elif operation == GT_OP:
                if len(sources) == 1:
                    if len(row[sources[0]]) > 0 and len(row[sources[1]]) > 0:
                        output_row[into_column_idx] = KgtkValue.to_boolean(float(row[sources[0]]) > float(row[sources[1]]))
                    else:
                        output_row[into_column_idx] = ""
                else:
                    if len(row[sources[0]]) > 0 and len(values[0]) > 0:
                        output_row[into_column_idx] = KgtkValue.to_boolean(float(row[sources[0]]) > float(values[0]))
                    else:
                        output_row[into_column_idx] = ""

            elif operation == IS_OP:
                if len(sources) == 1:
                    output_row[into_column_idx] = KgtkValue.to_boolean(row[sources[0]] == row[sources[1]])
                else:
                    output_row[into_column_idx] = KgtkValue.to_boolean(row[sources[0]] == values[0])

            elif operation == IS_IN_OP:
                bresult = False
                item = row[sources[0]]
                for item2 in values:
                    if item == item2:
                        bresult = True
                        break
                output_row[into_column_idx] = KgtkValue.to_boolean(bresult)

            elif operation == IS_NOT_OP:
                if len(sources) == 1:
                    output_row[into_column_idx] = KgtkValue.to_boolean(row[sources[0]] != row[sources[1]])
                else:
                    output_row[into_column_idx] = KgtkValue.to_boolean(row[sources[0]] != values[0])

            elif operation == JOIN_OP:
                output_row[into_column_idx] = values[0].join((row[sources[idx]] for idx in range(len(sources))))

            elif operation == LE_OP:
                if len(sources) == 1:
                    if len(row[sources[0]]) > 0 and len(row[sources[1]]) > 0:
                        output_row[into_column_idx] = KgtkValue.to_boolean(float(row[sources[0]]) <= float(row[sources[1]]))
                    else:
                        output_row[into_column_idx] = ""
                else:
                    if len(row[sources[0]]) > 0 and len(values[0]) > 0:
                        output_row[into_column_idx] = KgtkValue.to_boolean(float(row[sources[0]]) <= float(values[0]))
                    else:
                        output_row[into_column_idx] = ""

            elif operation == LT_OP:
                if len(sources) == 1:
                    if len(row[sources[0]]) > 0 and len(row[sources[1]]) > 0:
                        output_row[into_column_idx] = KgtkValue.to_boolean(float(row[sources[0]]) < float(row[sources[1]]))
                    else:
                        output_row[into_column_idx] = ""
                else:
                    if len(row[sources[0]]) > 0 and len(values[0]) > 0:
                        output_row[into_column_idx] = KgtkValue.to_boolean(float(row[sources[0]]) < float(values[0]))
                    else:
                        output_row[into_column_idx] = ""

            elif operation == LOWER_OP:
                for idx in range(len(sources)):
                    output_row[into_column_idxs[idx]] = row[sources[idx]].lower()

            elif operation == MAX_OP:
                max_result: typing.Optional[float] = None
                for idx in sources:
                    item = row[idx]
                    if len(item) > 0:
                        max_value: float = float(item)
                        if max_result is None or max_value > max_result:
                            max_result = max_value
                output_row[into_column_idx] = (fs % max_result) if max_result is not None else ""

            elif operation == MIN_OP:
                min_result: typing.Optional[float] = None
                for idx in sources:
                    item = row[idx]
                    if len(item) > 0:
                        min_value: float = float(item)
                        if min_result is None or min_value < min_result:
                            min_result = min_value
                output_row[into_column_idx] = (fs % min_result) if min_result is not None else ""

            elif operation == NAND_OP:
                bresult = True
                for idx in sources:
                    kv = KgtkValue(row[idx])
                    if kv.is_boolean():
                        bresult = bresult and kv.is_true()

                output_row[into_column_idx] = KgtkValue.to_boolean(not bresult)

            elif operation == NE_OP:
                if len(sources) == 1:
                    if len(row[sources[0]]) > 0 and len(row[sources[1]]) > 0:
                        output_row[into_column_idx] = KgtkValue.to_boolean(float(row[sources[0]]) != float(row[sources[1]]))
                    else:
                        output_row[into_column_idx] = ""
                else:
                    if len(row[sources[0]]) > 0 and len(values[0]) > 0:
                        output_row[into_column_idx] = KgtkValue.to_boolean(float(row[sources[0]]) != float(values[0]))
                    else:
                        output_row[into_column_idx] = ""

            elif operation == NOR_OP:
                bresult = False
                for idx in sources:
                    kv = KgtkValue(row[idx])
                    if kv.is_boolean():
                        bresult = bresult or kv.is_true()

                output_row[into_column_idx] = KgtkValue.to_boolean(not bresult)

            elif operation == NOT_OP:
                for idx in sources:
                    kv = KgtkValue(row[idx])
                    if kv.is_boolean():
                        output_row[into_column_idxs[idx]] = KgtkValue.to_boolean(not kv.is_true())
                    else:
                        output_row[into_column_idxs[idx]] = ""

            elif operation == OR_OP:
                bresult = False
                for idx in sources:
                    kv = KgtkValue(row[idx])
                    if kv.is_boolean():
                        bresult = bresult or kv.is_true()

                output_row[into_column_idx] = KgtkValue.to_boolean(bresult)

            elif operation == PERCENTAGE_OP:
                output_row[into_column_idx] = fs % (float(row[sources[0]]) * 100 / float(row[sources[1]]))

            elif operation == REPLACE_OP:
                if limit == 0:
                    output_row[into_column_idx] = row[sources[0]].replace(values[0], with_values[0])
                else:
                    output_row[into_column_idx] = row[sources[0]].replace(values[0], with_values[0], limit)

            elif operation == SET_OP:
                for idx in range(len(values)):
                    output_row[into_column_idxs[idx]] = values[idx]

            elif operation == SUBSTITUTE_OP and substitute_re is not None:
                output_row[into_column_idx] = substitute_re.sub(with_values[0], row[sources[0]], count=limit)

            elif operation == SUM_OP:
                total: float = 0
                for idx in sources:
                    item = row[idx]
                    if len(item) > 0:
                        total += float(item)
                for item in values:
                    if len(item) > 0:
                        total += float(item)
                output_row[into_column_idx] = fs % total
                
            elif operation == SWAPCASE_OP:
                for idx in range(len(sources)):
                    output_row[into_column_idxs[idx]] = row[sources[idx]].swapcase()

            elif operation == TITLE_OP:
                for idx in range(len(sources)):
                    output_row[into_column_idxs[idx]] = row[sources[idx]].title()

            elif operation == UPPER_OP:
                for idx in range(len(sources)):
                    output_row[into_column_idxs[idx]] = row[sources[idx]].upper()

            elif operation == XOR_OP:
                bresult = False
                for idx in sources:
                    kv = KgtkValue(row[idx])
                    if kv.is_boolean():
                        bresult = bresult != kv.is_true()

                output_row[into_column_idx] = KgtkValue.to_boolean(bresult)

            kw.write(output_row)

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

