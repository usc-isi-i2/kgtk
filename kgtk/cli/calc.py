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
POW_OP: str = "pow"

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
SUBSTRING_OP: str = "substring"
ZFILL_OP: str = "zfill"

# KgtkValue fields

# Implemented:

# Boolean
AND_OP: str = "and" # (boolean, boolean) -> boolean
NAND_OP: str = "nand" # (boolean, boolean) -> boolean
NOR_OP: str = "nor" # (boolean, boolean) -> boolean
NOT_OP: str = "not" # (boolean, ...) -> (boolean, ...)
OR_OP: str = "or" # (boolean, boolean) -> boolean
XOR_OP: str = "xor" # (boolean, boolean) -> boolean

# Date and times
IS_DATE_OP: str = "is_date" # -> bool
DATE_DATE_OP: str = "date_date"   # -> int (YYYYMMDD) or str ("YYYYMMDD")
DATE_DATE_ISO_OP: str = "date_date_iso" # -> str ("YYYY-MM-DD")
DATE_DAY_OP: str = "date_day"     # -> int or str
DATE_MONTH_OP: str = "date_month" # -> int or str
DATE_YEAR_OP: str = "date_year"   # -> int or str

# Numeric
ABS_OP: str = "abs" # (column, ...)
AVERAGE_OP: str = "average"
DIV_OP: str = "div" # (column / column) or (column / value)
LIST_SUM_OP: str = "list_sum" # column
MAX_OP: str = "max"
MIN_OP: str = "min"
MINUS_OP: str = "minus" # (column1 - column2) or (column - value)
MOD_OP: str = "mod" # (column mod column) or (column mod value)
NEGATE_OP: str = "negate" # (column, ...)
NUMBER_OP: str = "number" # Get a number or the numeric part of a quantity.
PERCENTAGE_OP: str = "percentage"
REVERSE_DIV_OP: str = "reverse_div" # (column2 / column1) or (column / value)
REVERSE_MINUS_OP: str = "reverse_minus" # (column2 - column1) or (value - column)
REVERSE_MOD_OP: str = "reverse_mod" # (column2 mod column1) or (value mod column)
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
IS_LQSTRING_OP: str = "is_lqstring" # -> bool
IS_STRING_OP: str = "is_string" # -> bool
JOIN_OP: str = "join"
LEN_OP: str = "len"
LOWER_OP: str = "lower"
REPLACE_OP: str = "replace"
STRING_LANG_OP: str = "string_lang"
STRING_LANG_SUFFIX_OP: str = "string_lang_suffix"
STRING_SUFFIX_OP: str = "string_suffix"
STRING_TEXT_OP: str = "string_text"
SUBSTITUTE_OP: str = "substitute"
SUBSTRING_OP: str = "substring"
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

OPERATIONS: typing.List[str] = [
    ABS_OP,
    AND_OP,
    AVERAGE_OP,
    CAPITALIZE_OP,
    CASEFOLD_OP,
    COPY_OP,
    DATE_DATE_OP,
    DATE_DATE_ISO_OP,
    DATE_DAY_OP,
    DATE_MONTH_OP,
    DATE_YEAR_OP,
    DIV_OP,
    EQ_OP,
    FROMISOFORMAT_OP,
    GE_OP,
    GT_OP,
    IS_DATE_OP,
    IS_IN_OP,
    IS_LQSTRING_OP,
    IS_NOT_OP,
    IS_OP,
    IS_STRING_OP,
    JOIN_OP,
    LOWER_OP,
    LE_OP,
    LEN_OP,
    LIST_SUM_OP,
    LT_OP,
    MAX_OP,
    MIN_OP,
    MINUS_OP,
    NAND_OP,
    NE_OP,
    NEGATE_OP,
    NOR_OP,
    NOT_OP,
    NUMBER_OP,
    OR_OP,
    PERCENTAGE_OP,
    REPLACE_OP,
    REVERSE_DIV_OP,
    REVERSE_MINUS_OP,
    SET_OP,
    STRING_LANG_OP,
    STRING_LANG_SUFFIX_OP,
    STRING_SUFFIX_OP,
    STRING_TEXT_OP,
    SUBSTRING_OP,
    SUBSTITUTE_OP,
    SUM_OP,
    SWAPCASE_OP,
    TITLE_OP,
    UPPER_OP,
    XOR_OP,
]

OVERWRITE_FALSE_OPERATIONS: typing.List[str] = [
    COPY_OP,
    SET_OP,
    SUBSTRING_OP,
]

TO_STRING_TRUE_OPERATIONS: typing.List[str] = [
    DATE_DATE_OP,
    DATE_DATE_ISO_OP,
    DATE_DAY_OP,
    DATE_MONTH_OP,
    DATE_YEAR_OP,
    NUMBER_OP,
    STRING_LANG_OP,
    STRING_LANG_SUFFIX_OP,
    STRING_SUFFIX_OP,
    SUBSTRING_OP,
]

GROUP_BY_OPERATIONS: typing.List[str] = [
    AVERAGE_OP,
    MIN_OP,
    MAX_OP,
    SUM_OP,
    ]

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
                              help="The name of the column to receive the result of the calculation.")

    parser.add_argument(      "--do", dest="operation", help="The name of the operation.", required=True,
                              choices=OPERATIONS)

    parser.add_argument(      "--values", dest="values_list", nargs='*', metavar="VALUES", action='append',
                        help="An optional list of values")

    parser.add_argument(      "--with-values", dest="with_values_list", nargs='*', metavar="WITH_VALUES", action='append',
                        help="An optional list of additional values")

    parser.add_argument(      "--limit", dest="limit", type=int,
                              help="A limit count.")

    parser.add_argument(      "--format", dest="format_string", help="The format string for the calculation.")

    parser.add_argument(      "--overwrite", dest="overwrite",
                              help="If true, overwrite non-empty values in the result column(s). " +
                              "If false, do not overwrite non-empty values in the result column(s). " +
                              "--overwrite=False may be used with the following operations: " +
                              repr(OVERWRITE_FALSE_OPERATIONS) + " (default=%(default)s).",
                              metavar="True|False",
                              type=optional_bool, nargs='?', const=True, default=True)

    parser.add_argument(      "--to-string", dest="to_string",
                              help="If true, ensure that the result is a string. " +
                              "If false, the result might be a symbol or some other type. " +
                              "--to-string=True may be used with the following operations: " +
                              repr(TO_STRING_TRUE_OPERATIONS) + " (default=%(default)s).",
                              metavar="True|False",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--group-by", dest="group_by_names_list", nargs='*', metavar="COLUMN_NAME", action='append',
                        help="The list of group-by column names, optionally containing '..' for column ranges " +
                              "and '...' for column names not explicitly mentioned. "+
                              "--group-by may be used with the following operations: " + repr(GROUP_BY_OPERATIONS) + ". " +
                              "At the present time, --group-by requires --presorted.")

    parser.add_argument(      "--presorted", dest="presorted",
                              help="If true, the input file is presorted for --group-by. (default=%(default)s).",
                              metavar="True|False",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--group-by-label", dest="group_by_label", type=str,
                              help=h("When specified, add a label column to the group-by output."))

    parser.add_argument(      "--group-by-output-names", dest="group_by_output_names_list", nargs='*', metavar="COLUMN_NAME", action='append',
                              help=h("When specified, rename the --group-by columns on output."))

    parser.add_argument(      "--filter", dest="filter",
                              help="When --filter=True, and an operation is specified with a boolean result, records for which " +
                              "the result is False will not be written to the output stream.  Also, " +
                              "--into is optional when --filter is provided. (default=%(default)s).",
                              metavar="True|False",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--fast", dest="be_fast",
                              help="When --fast=True, use a faster implementation which might not be general. " +
                              "(default=%(default)s).",
                              metavar="True|False",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--as-int", dest="as_int",
                              help="When True, compute numbers as integers.  When False, compute numbers as floats. " +
                              "(default=%(default)s).",
                              metavar="True|False",
                              type=optional_bool, nargs='?', const=True, default=False)

    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser,
                                    mode_options=True,
                                    default_mode=KgtkReaderMode[parsed_shared_args._mode],
                                    expert=_expert)
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
        overwrite: bool,
        to_string: bool,
        group_by_names_list: typing.List[typing.List[str]],
        presorted: bool,
        group_by_label: typing.Optional[str],
        group_by_output_names_list: typing.List[typing.List[str]],
        filter: bool,
        be_fast: bool,
        as_int: bool,

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
    group_by_names: typing.List[str] = flatten_arg_list(group_by_names_list)
    group_by_output_names: typing.List[str] = flatten_arg_list(group_by_output_names_list)
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
        if len(group_by_names) > 0:
            print("--group-by %s" % " ".join(group_by_names), file=error_file, flush=True)
        if len(group_by_output_names) > 0:
            print("--group-by-output-names %s" % " ".join(group_by_output_names), file=error_file, flush=True)
        print("--operation=%s" % str(operation), file=error_file, flush=True)
        if len(values) > 0:
            print("--values %s" % " ".join(values), file=error_file, flush=True)
        if len(with_values) > 0:
            print("--with-values %s" % " ".join(with_values), file=error_file, flush=True)
        if limit is not None:
            print("--limit %d" % limit, file=error_file, flush=True)
        if format_string is not None:
            print("--format=%s" % format_string, file=error_file, flush=True)
        print("--overwrite=%s" % repr(overwrite), file=error_file, flush=True)
        print("--to-string=%s" % repr(to_string), file=error_file, flush=True)
        print("--presorted=%s" % repr(presorted), file=error_file, flush=True)
        if group_by_label is not None:
            print("--group-by-label=%s" % group_by_label, file=error_file, flush=True)
        print("--filter=%s" % repr(filter), file=error_file, flush=True)
        print("--fast=%s" % repr(be_fast), file=error_file, flush=True)
        print("--as-int=%s" % repr(as_int), file=error_file, flush=True)

        reader_options.show(out=error_file)
        value_options.show(out=error_file)
        print("=======", file=error_file, flush=True)

    if not overwrite and operation not in OVERWRITE_FALSE_OPERATIONS:
        raise KGTKException("--overwrite false is not supported by operation %s." % repr(operation))

    if to_string and operation not in TO_STRING_TRUE_OPERATIONS:
        raise KGTKException("--to-string is not supported by operation %s." % repr(operation))

    if len(group_by_names) > 0:
        if operation not in GROUP_BY_OPERATIONS:
            raise KGTKException("--group-by is not supported by operation %s." % repr(operation))
        if not presorted:
            raise KGTKException("--group-by currently requires --presorted input.")

    def parse_column_names_with_ranges(kr: KgtkReader, column_names: typing.List[str])->typing.List[int]:
        """This routine is defined here rather than at the top level to avoid importing KgtkReader at the top level."""
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

        return sources
  
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

        sources: typing.List[int] = parse_column_names_with_ranges(kr, column_names)

        group_by: typing.List[int] = parse_column_names_with_ranges(kr, group_by_names)

        if len(group_by_output_names) > 0:
            if len(group_by_output_names) != len(group_by):
                raise KGTKException("There are %d --group-by-output-names but %d --group-by columns" % (len(group_by_output_names), len(group_by)))

        new_column_count: int = 0
        into_column_idxs: typing.List[int] = [ ]
        into_column_idx: int

        group_by_label_idx: int = -1

        output_column_names: typing.List[str]
        if len(group_by) == 0:
            output_column_names = kr.column_names.copy()
        else:
            if len(group_by_output_names) == 0:
                output_column_names = [ kr.column_names[i] for i in group_by ]
            else:
                output_column_names = group_by_output_names.copy()
            if group_by_label is not None and len(group_by_label) > 0:
                new_column_count += 1
                group_by_label_idx = len(output_column_names)
                output_column_names.append(KgtkFormat.LABEL) # TODO: implement --group-by-label-column-name
                if verbose:
                    print("Adding label %s into new column %d (%s)." % (repr(group_by_label),
                                                                        group_by_label_idx,
                                                                        repr(KgtkFormat.LABEL)), file=error_file, flush=True)

        into_column_name: str
        for idx, into_column_name in enumerate(into_column_names):
            if len(group_by) == 0 and into_column_name in kr.column_name_map:
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

        if limit is None:
            limit = 0

        fs: str = format_string if format_string is not None else "%5.2f"

        row: typing.List[str]
        output_row: typing.List[str]
        opfunc = None

        if len(into_column_idxs) > 0:
            into_column_idx = into_column_idxs[0] # for convenience
        else:
            into_column_idx = -1

        if operation == ABS_OP:
            if len(sources) == 0:
                raise KGTKException("Abs needs at least one source, got %d" % len(sources))
            if len(sources) != len(into_column_idxs):
                raise KGTKException("Abs needs the same number of input columns and into columns, got %d and %d" % (len(sources), len(into_column_idxs)))

            def abs_fast_float_op()->bool:
                # This fast path assumes that the column values are empty or contain numbers,
                # not quantities.
                src_idx: int
                for src_idx in range(len(sources)):
                    strval: str = row[sources[src_idx]]
                    output_row[into_column_idxs[src_idx]] = str(abs(float(strval))) if len(strval) > 0 else ""
                return True

            def abs_fast_int_op()->bool:
                # This fast path assumes that the column values are empty or contain integer numbers,
                # not quantities or float numbers.
                src_idx: int
                for src_idx in range(len(sources)):
                    strval: str = row[sources[src_idx]]
                    output_row[into_column_idxs[src_idx]] = str(abs(int(strval))) if len(strval) > 0 else ""
                return True

            def abs_op()->bool:
                src_idx: int
                for src_idx in range(len(sources)):
                    strval: str = row[sources[src_idx]]
                    if len(strval) == 0:
                        # This is the optimized path for empty values.
                        output_row[into_column_idxs[src_idx]] = ""
                        continue

                    kv: KgtkValue = KgtkValue(strval)
                    if not kv.is_number_or_quantity(validate=True, parse_fields=True):
                        # Not a number or a quantity, just copy the value:
                        #
                        # TODO: a failure indicator might be nice.
                        output_row[into_column_idxs[src_idx]] = strval
                        continue

                    if kv.fields is None or kv.fields.number is None:
                        # This shouldn't happen.  Copy the value and leave.
                        #
                        # TODO: a failure indicator might be nice.
                        output_row[into_column_idxs[src_idx]] = strval
                        continue
                    numberstr: str = str(abs(kv.fields.number))
                       
                    if kv.fields.low_tolerancestr is not None or kv.fields.high_tolerancestr is not None:
                        # TODO: Handle these properly.
                        output_row[into_column_idxs[src_idx]] = strval
                        continue

                    if kv.fields.si_units is not None:
                        output_row[into_column_idxs[src_idx]] = numberstr + kv.fields.si_units
                    elif kv.fields.units_node is not None:
                        output_row[into_column_idxs[src_idx]] = numberstr + kv.fields.units_node
                    else:
                        output_row[into_column_idxs[src_idx]] = numberstr

                return True

            if be_fast:
                opfunc = abs_fast_int_op if as_int else abs_fast_float_op
            else:
                opfunc = abs_op

        elif operation == AND_OP:
            if len(sources) == 0:
                raise KGTKException("And needs at least one source, got %d" % len(sources))
            if filter:
                if len(into_column_idxs) > 1:
                    raise KGTKException("And needs at most 1 destination column, got %d" % len(into_column_idxs))
            else:
                if len(into_column_idxs) != 1:
                    raise KGTKException("And needs 1 destination column, got %d" % len(into_column_idxs))

            def and_op()->bool:
                bresult: bool = True
                src_idx: int
                for src_idx in sources:
                    kv: Kgtkvalue = KgtkValue(row[src_idx])
                    if kv.is_boolean():
                        bresult = bresult and kv.is_true()

                if into_column_idx >= 0:
                    output_row[into_column_idx] = KgtkValue.to_boolean(bresult)
                return bresult if filter else True
            opfunc = and_op

        elif operation == AVERAGE_OP:
            if len(sources) == 0:
                raise KGTKException("Average needs at least one source, got %d" % len(sources))
            if len(into_column_idxs) != 1:
                raise KGTKException("Average needs 1 destination column, got %d" % len(into_column_idxs))

            def average_op()->bool:
                # TODO: support quantities.
                atotal: float = 0
                acount: int = 0
                src_idx: int
                for src_idx in sources:
                    item: str = row[src_idx]
                    if len(item) > 0:
                        atotal += float(item)
                        acount += 1
                output_row[into_column_idx] = (fs % (atotal / float(acount))) if acount > 0 else ""                
                return True

            def group_by_average_op(total: typing.Optional[float],
                                    count: typing.Optional[int],
                                    finish: bool = False)->typing.Tuple[float, int, bool]:
                if finish:
                    if total is None or count is None:
                        return None, None, False
                    output_row[into_column_idx] = fs % (total / count)
                    return None, None, True

                src_idx: int
                item: str
                for src_idx in sources:
                    item = row[src_idx]
                    if len(item) > 0:
                        if total is None:
                            total = 0.0
                        total += float(item)
                        if count is None:
                            count = 0
                        count += 1
                return total, count, False

            if len(group_by) == 0:
                opfunc = average_op
            else:
                opfunc = group_by_average_op

        elif operation == CAPITALIZE_OP:
            if len(sources) == 0:
                raise KGTKException("Capitalize needs at least one source, got %d" % len(sources))
            if len(sources) != len(into_column_idxs):
                raise KGTKException("Capitalize needs the same number of input columns and into columns, got %d and %d" % (len(sources), len(into_column_idxs)))

            def capitalize_op()->bool:
                src_idx: int
                for src_idx in range(len(sources)):
                    output_row[into_column_idxs[src_idx]] = row[sources[src_idx]].capitalize()
                return True
            opfunc = capitalize_op

        elif operation == CASEFOLD_OP:
            if len(sources) == 0:
                raise KGTKException("Casefold needs at least one source, got %d" % len(sources))
            if len(sources) != len(into_column_idxs):
                raise KGTKException("Casefold needs the same number of input columns and into columns, got %d and %d" % (len(sources), len(into_column_idxs)))

            def casefold_op()->bool:
                src_idx: int
                for src_idx in range(len(sources)):
                    output_row[into_column_idxs[src_idx]] = row[sources[src_idx]].casefold()
                return True
            opfunc = casefold_op

        elif operation == COPY_OP:
            if len(sources) == 0:
                raise KGTKException("Copy needs at least one source, got %d" % len(sources))
            if len(sources) != len(into_column_idxs):
                raise KGTKException("Copy needs the same number of source columns and into columns, got %d and %d" % (len(sources), len(into_column_idxs)))
            
            if overwrite:
                def copy_op()->bool:
                    src_idx: int
                    for src_idx in range(len(sources)):
                        output_row[into_column_idxs[src_idx]] = row[sources[src_idx]]
                    return True
            else:
                def copy_op()->bool:
                    src_idx: int
                    for src_idx in range(len(sources)):
                        if len(output_row[into_column_idxs[src_idx]]) == 0:
                            output_row[into_column_idxs[src_idx]] = row[sources[src_idx]]
                    return True
            opfunc = copy_op

        elif operation == DATE_DATE_OP:
            # TODO:  Need date/time parsing options.
            if len(sources) == 0:
                raise KGTKException("date_date needs at least one source, got %d" % len(sources))
            if len(sources) != len(into_column_idxs):
                raise KGTKException("date_date needs the same number of input columns and into columns, got %d and %d" % (len(sources), len(into_column_idxs)))

            if to_string:
                def date_date_op()->bool:
                    src_idx: int
                    for src_idx in range(len(sources)):
                        item: str = row[sources[src_idx]]
                        # TODO: optimize this.
                        kv: KgtkValue = KgtkValue(item) # TODO: Need options!
                        if kv.is_date_and_times(validate=True, parse_fields=True) and kv.fields is not None:
                            output_row[into_column_idxs[src_idx]] = \
                                KgtkFormat.STRING_SIGIL + kv.fields.yearstr + kv.fields.monthstr + kv.fields.daystr + KgtkFormat.STRING_SIGIL
                        else:
                            output_row[into_column_idxs[src_idx]] = ""
                    return True
            else:
                def date_date_op()->bool:
                    src_idx: int
                    for src_idx in range(len(sources)):
                        item: str = row[sources[src_idx]]
                        # TODO: optimize this.
                        kv: KgtkValue = KgtkValue(item) # TODO: Need options!
                        if kv.is_date_and_times(validate=True, parse_fields=True) and kv.fields is not None:
                            output_row[into_column_idxs[src_idx]] = \
                                kv.fields.yearstr + kv.fields.monthstr + kv.fields.daystr
                        else:
                            output_row[into_column_idxs[src_idx]] = ""
                    return True
            opfunc = date_date_op

        elif operation == DATE_DATE_ISO_OP:
            # TODO:  Need date/time parsing options.
            if len(sources) == 0:
                raise KGTKException("date_date_iso needs at least one source, got %d" % len(sources))
            if len(sources) != len(into_column_idxs):
                raise KGTKException("date_date_iso needs the same number of input columns and into columns, got %d and %d" % (len(sources), len(into_column_idxs)))

            def date_date_iso_op()->bool:
                src_idx: int
                for src_idx in range(len(sources)):
                    item: str = row[sources[src_idx]]
                    # TODO: optimize this.
                    kv: KgtkValue = KgtkValue(item) # TODO: Need options!
                    if kv.is_date_and_times(validate=True, parse_fields=True) and kv.fields is not None:
                        output_row[into_column_idxs[src_idx]] = \
                            KgtkFormat.STRING_SIGIL + kv.fields.yearstr + '-' + kv.fields.monthstr + '-' + kv.fields.daystr + KgtkFormat.STRING_SIGIL
                    else:
                        output_row[into_column_idxs[src_idx]] = ""
                return True
    
            opfunc = date_date_iso_op

        elif operation == DATE_DAY_OP:
            # TODO:  Need date/time parsing options.
            if len(sources) == 0:
                raise KGTKException("date_day needs at least one source, got %d" % len(sources))
            if len(sources) != len(into_column_idxs):
                raise KGTKException("date_day needs the same number of input columns and into columns, got %d and %d" % (len(sources), len(into_column_idxs)))

            if to_string:
                def date_day_op()->bool:
                    src_idx: int
                    for src_idx in range(len(sources)):
                        item: str = row[sources[src_idx]]
                        # TODO: optimize this.
                        kv: KgtkValue = KgtkValue(item) # TODO: Need options!
                        if kv.is_date_and_times(validate=True, parse_fields=True) and kv.fields is not None:
                            output_row[into_column_idxs[src_idx]] = KgtkFormat.STRING_SIGIL + kv.fields.daystr + KgtkFormat.STRING_SIGIL
                        else:
                            output_row[into_column_idxs[src_idx]] = ""
                    return True
            else:
                def date_day_op()->bool:
                    src_idx: int
                    for src_idx in range(len(sources)):
                        item: str = row[sources[src_idx]]
                        # TODO: optimize this.
                        kv: KgtkValue = KgtkValue(item) # TODO: Need options!
                        if kv.is_date_and_times(validate=True, parse_fields=True) and kv.fields is not None:
                            output_row[into_column_idxs[src_idx]] = str(kv.fields.day) # Elimiate leading 0
                        else:
                            output_row[into_column_idxs[src_idx]] = ""
                    return True
            opfunc = date_day_op

        elif operation == DATE_MONTH_OP:
            # TODO:  Need date/time parsing options.
            if len(sources) == 0:
                raise KGTKException("date_month needs at least one source, got %d" % len(sources))
            if len(sources) != len(into_column_idxs):
                raise KGTKException("date_month needs the same number of input columns and into columns, got %d and %d" % (len(sources), len(into_column_idxs)))
            if be_fast:
                if to_string:
                    def date_month_op()->bool:
                        src_idx: int
                        for src_idx in range(len(sources)):
                            item: str = row[sources[src_idx]]
                            if item.startswith(KgtkFormat.DATE_AND_TIMES_SIGIL):
                                output_row[into_column_idxs[src_idx]] = KgtkFormat.STRING_SIGIL + item[6:8] + KgtkFormat.STRING_SIGIL
                            else:
                                output_row[into_column_idxs[src_idx]] = ""
                        return True
                else:
                    def date_month_op()->bool:
                        src_idx: int
                        for src_idx in range(len(sources)):
                            item: str = row[sources[src_idx]]
                            if item.startswith(KgtkFormat.DATE_AND_TIMES_SIGIL):
                                output_row[into_column_idxs[src_idx]] = item[6:8]
                            else:
                                output_row[into_column_idxs[src_idx]] = ""
                        return True
            else:
                if to_string:
                    def date_month_op()->bool:
                        src_idx: int
                        for src_idx in range(len(sources)):
                            item: str = row[sources[src_idx]]
                            # TODO: optimize this.
                            kv: KgtkValue = KgtkValue(item) # TODO: Need options!
                            if kv.is_date_and_times(validate=True, parse_fields=True) and kv.fields is not None:
                                output_row[into_column_idxs[src_idx]] = KgtkFormat.STRING_SIGIL + kv.fields.monthstr + KgtkFormat.STRING_SIGIL
                            else:
                                output_row[into_column_idxs[src_idx]] = ""
                        return True
                else:
                    def date_month_op()->bool:
                        src_idx: int
                        for src_idx in range(len(sources)):
                            item: str = row[sources[src_idx]]
                            # TODO: optimize this.
                            kv: KgtkValue = KgtkValue(item) # TODO: Need options!
                            if kv.is_date_and_times(validate=True, parse_fields=True) and kv.fields is not None:
                                output_row[into_column_idxs[src_idx]] = str(kv.fields.month) # Eliminate leading0.
                            else:
                                output_row[into_column_idxs[src_idx]] = ""
                        return True
            opfunc = date_month_op

        elif operation == DATE_YEAR_OP:
            # TODO:  Need date/time parsing options.
            if len(sources) == 0:
                raise KGTKException("date_year needs at least one source, got %d" % len(sources))
            if len(sources) != len(into_column_idxs):
                raise KGTKException("date_year needs the same number of input columns and into columns, got %d and %d" % (len(sources), len(into_column_idxs)))

            if be_fast:
                if to_string:
                    def date_year_op()->bool:
                        src_idx: int
                        for src_idx in range(len(sources)):
                            item: str = row[sources[src_idx]]
                            if item.startswith(KgtkFormat.DATE_AND_TIMES_SIGIL):
                                output_row[into_column_idxs[src_idx]] = KgtkFormat.STRING_SIGIL + item[1:5] + KgtkFormat.STRING_SIGIL
                            else:
                                output_row[into_column_idxs[src_idx]] = ""
                        return True
                else:
                    def date_year_op()->bool:
                        src_idx: int
                        for src_idx in range(len(sources)):
                            item: str = row[sources[src_idx]]

                            if item.startswith(KgtkFormat.DATE_AND_TIMES_SIGIL):
                                output_row[into_column_idxs[src_idx]] = item[1:5]
                            else:
                                output_row[into_column_idxs[src_idx]] = ""
                        return True
            else:
                if to_string:
                    def date_year_op()->bool:
                        src_idx: int
                        for src_idx in range(len(sources)):
                            item: str = row[sources[src_idx]]
                            # TODO: optimize this.
                            kv: KgtkValue = KgtkValue(item) # TODO: Need options!
                            if kv.is_date_and_times(validate=True, parse_fields=True) and kv.fields is not None:
                                output_row[into_column_idxs[src_idx]] = KgtkFormat.STRING_SIGIL + kv.fields.yearstr + KgtkFormat.STRING_SIGIL
                            else:
                                output_row[into_column_idxs[src_idx]] = ""
                        return True
                else:
                    def date_year_op()->bool:
                        src_idx: int
                        for src_idx in range(len(sources)):
                            item: str = row[sources[src_idx]]
                            # TODO: optimize this.
                            kv: KgtkValue = KgtkValue(item) # TODO: Need options!
                            if kv.is_date_and_times(validate=True, parse_fields=True) and kv.fields is not None:
                                output_row[into_column_idxs[src_idx]] = str(kv.fields.year) # Eliminate leading 0.
                            else:
                                output_row[into_column_idxs[src_idx]] = ""
                        return True
            opfunc = date_year_op

        elif operation == DIV_OP:
            if not ((len(sources) == 2 and len(values) == 0) or (len(sources) == 1 and len(values) == 1)):
                raise KGTKException("Divide needs two sources or one source and one value, got %d sources and %d values" % (len(sources), len(values)))
            if len(into_column_idxs) != 1:
                raise KGTKException("Divide needs 1 destination columns, got %d" % len(into_column_idxs))

            def div_op()->bool:
                # TODO: support quantities.
                if len(sources) == 2:
                    output_row[into_column_idx] = str(float(row[sources[0]]) / float(row[sources[1]]))
                else:
                    output_row[into_column_idx] = str(float(row[sources[0]]) / float(values[0]))
                return True
            opfunc = div_op

        elif operation == EQ_OP:
            if not ((len(sources) == 2 and len(values) == 0) or (len(sources) == 1 and len(values) == 1)):
                raise KGTKException("Eq needs two sources or one source and one value, got %d sources and %d values" % (len(sources), len(values)))
            if filter:
                if len(into_column_idxs) > 1:
                    raise KGTKException("Eq needs at most 1 destination column, got %d" % len(into_column_idxs))
            else:
                if len(into_column_idxs) != 1:
                    raise KGTKException("Eq needs 1 destination column, got %d" % len(into_column_idxs))

            def eq_op()->bool:
                bresult: bool = False
                sresult: str = ""
                if len(sources) == 2:
                    if len(row[sources[0]]) > 0 and len(row[sources[1]]) > 0:
                        bresult = float(row[sources[0]]) == float(row[sources[1]])
                        sresult = KgtkValue.to_boolean(bresult)
                else:
                    if len(row[sources[0]]) > 0 and len(values[0]) > 0:
                        bresult = float(row[sources[0]]) == float(values[0])
                        sresult = KgtkValue.to_boolean(bresult)
                if into_column_idx >= 0:
                    output_row[into_column_idx] = sresult
                return bresult if filter else True
            opfunc = eq_op

        elif operation == FROMISOFORMAT_OP:
            if len(sources) != 1:
                raise KGTKException("Fromisoformat needs one source, got %d" % len(sources))
            if len(values) != len(into_column_idxs):
                raise KGTKException("Fromisoformat needs the same number of values and into columns, got %d and %d" % (len(values), len(into_column_idxs)))

            def fromisoformat_op()->bool:
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
                        value_idx: int
                        for value_idx in range(len(values)):
                            value_name: str = values[value_idx]
                            into_idx: int = into_column_idxs[value_idx]
                            
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
                return True
            opfunc = fromisoformat_op

        elif operation == GE_OP:
            if not ((len(sources) == 2 and len(values) == 0) or (len(sources) == 1 and len(values) == 1)):
                raise KGTKException("Ge needs two sources or one source and one value, got %d sources and %d values" % (len(sources), len(values)))
            if filter:
                if len(into_column_idxs) > 1:
                    raise KGTKException("Ge needs at most 1 destination column, got %d" % len(into_column_idxs))
            else:
                if len(into_column_idxs) != 1:
                    raise KGTKException("Ge needs 1 destination column, got %d" % len(into_column_idxs))

            def ge_op()->bool:
                bresult: bool = False
                sresult: str = ""
                if len(sources) == 2:
                    if len(row[sources[0]]) > 0 and len(row[sources[1]]) > 0:
                        bresult = float(row[sources[0]]) >= float(row[sources[1]])
                        sresult = KgtkValue.to_boolean(bresult)
                else:
                    if len(row[sources[0]]) > 0 and len(values[0]) > 0:
                        bresult = float(row[sources[0]]) >= float(values[0])
                        sresult = KgtkValue.to_boolean(bresult)
                if into_columns_idx >= 0:
                    output_row[into_column_idx] = sresult
                return bresult if filter else True
            opfunc = ge_op

        elif operation == GT_OP:
            if not ((len(sources) == 2 and len(values) == 0) or (len(sources) == 1 and len(values) == 1)):
                raise KGTKException("Gt needs two sources or one source and one value, got %d sources and %d values" % (len(sources), len(values)))
            if filter:
                if len(into_column_idxs) > 1:
                    raise KGTKException("Gt needs at most 1 destination column, got %d" % len(into_column_idxs))
            else:
                if len(into_column_idxs) != 1:
                    raise KGTKException("Gt needs 1 destination column, got %d" % len(into_column_idxs))

            def gt_op()->bool:
                bresult: bool = False
                sresult: str = ""
                if len(sources) == 2:
                    if len(row[sources[0]]) > 0 and len(row[sources[1]]) > 0:
                        bresult = float(row[sources[0]]) > float(row[sources[1]])
                        sresult = KgtkValue.to_boolean(bresult)
                else:
                    if len(row[sources[0]]) > 0 and len(values[0]) > 0:
                        bresult = float(row[sources[0]]) > float(values[0])
                        sresult = KgtkValue.to_boolean(bresult)
                if into_column_idx >= 0:
                    output_row[into_column_idx] = sresult
                return bresult if filter else True
            opfunc = gt_op

        elif operation == IS_DATE_OP:
            if filter:
                if len(sources) != 1:
                    raise KGTKException("is_date needs one source when filtering, got %d" % len(sources))
                if len(into_column_idxs) > 1:
                    raise KGTKException("is_date needs at most one destination column when filtering, got %d" % (len(into_column_idxs)))

                if into_column_idx >= 0:
                    def is_date_op()->bool:
                        src_idx: int
                        item: str = row[sources[0]]
                        bresult: bool = True if item.startswith(KgtkFormat.DATE_AND_TIMES_SIGIL) else False
                        output_row[into_column_idx] = KgtkFormat.TRUE_SYMBOL if bresult else KgtkFormat.FALSE_SYMBOL
                        return bresult
                else:
                    def is_date_op()->bool:
                        src_idx: int
                        item: str = row[sources[0]]
                        bresult: bool = True if item.startswith(KgtkFormat.DATE_AND_TIMES_SIGIL) else False
                        return bresult
            else:
                if len(sources) == 0:
                    raise KGTKException("is_date needs at least one source, got %d" % len(sources))
                if len(sources) != len(into_column_idxs):
                    raise KGTKException("is_date needs the same number of input columns and into columns, got %d and %d" % (len(sources), len(into_column_idxs)))
                def is_lqstring_op()->bool:
                    src_idx: int
                    for src_idx in range(len(sources)):
                        item: str = row[sources[src_idx]]
                        bresult: bool = True if item.startswith(KgtkFormat.DATE_AND_TIMES_SIGIL) else False
                        output_row[into_column_idxs[src_idx]] = KgtkFormat.TRUE_SYMBOL if bresult else KgtkFormat.FALSE_SYMBOL
                    return True
            opfunc = is_date_op

        elif operation == IS_IN_OP:
            if len(sources) != 1:
                raise KGTKException("Is in needs one source, got %d" % len(sources))
            if len(values) == 0:
                raise KGTKException("Is in needs at least one value, got %d" % len(values))
            if filter:
                if len(into_column_idxs) > 1:
                    raise KGTKException("Is in needs at most 1 destination column, got %d" % len(into_column_idxs))
            else:
                if len(into_column_idxs) != 1:
                    raise KGTKException("Is in needs 1 destination column, got %d" % len(into_column_idxs))

            def is_in_op()->bool:
                bresult: bool = False
                item: str = row[sources[0]]
                item2: str
                for item2 in values:
                    if item == item2:
                        bresult = True
                        break
                if into_column_idx >= 0:
                    output_row[into_column_idx] = KgtkValue.to_boolean(bresult)
                return bresult if filter else True
            opfunc = is_in_op

        elif operation == IS_LQSTRING_OP:
            if filter:
                if len(sources) != 1:
                    raise KGTKException("is_lqstring needs one source when filtering, got %d" % len(sources))
                if len(into_column_idxs) > 1:
                    raise KGTKException("is_lqstring needs at most one destination column when filtering, got %d" % (len(into_column_idxs)))

                if into_column_idx >= 0:
                    def is_lqstring_op()->bool:
                        src_idx: int
                        item: str = row[sources[0]]
                        bresult: bool = True if item.startswith(KgtkFormat.LANGUAGE_QUALIFIED_STRING_SIGIL) else False
                        output_row[into_column_idx] = KgtkFormat.TRUE_SYMBOL if bresult else KgtkFormat.FALSE_SYMBOL
                        return bresult
                else:
                    def is_lqstring_op()->bool:
                        src_idx: int
                        item: str = row[sources[0]]
                        bresult: bool = True if item.startswith(KgtkFormat.LANGUAGE_QUALIFIED_STRING_SIGIL) else False
                        return bresult
            else:
                if len(sources) == 0:
                    raise KGTKException("is_lqstring needs at least one source, got %d" % len(sources))
                if len(sources) != len(into_column_idxs):
                    raise KGTKException("is_lqstring needs the same number of input columns and into columns, got %d and %d" % (len(sources), len(into_column_idxs)))
                def is_lqstring_op()->bool:
                    src_idx: int
                    for src_idx in range(len(sources)):
                        item: str = row[sources[src_idx]]
                        bresult: bool = True if item.startswith(KgtkFormat.LANGUAGE_QUALIFIED_STRING_SIGIL) else False
                        output_row[into_column_idxs[src_idx]] = KgtkFormat.TRUE_SYMBOL if bresult else KgtkFormat.FALSE_SYMBOL
                    return True
            opfunc = is_lqstring_op

        elif operation == IS_NOT_OP:
            if not ((len(sources) == 2 and len(values) == 0) or (len(sources) == 1 and len(values) == 1)):
                raise KGTKException("Is not needs two sources or one source and one value, got %d sources and %d values" % (len(sources), len(values)))
            if filter:
                if len(into_column_idxs) > 1:
                    raise KGTKException("Is not needs at most 1 destination column, got %d" % len(into_column_idxs))
            else:
                if len(into_column_idxs) != 1:
                    raise KGTKException("Is not needs 1 destination column, got %d" % len(into_column_idxs))

            def is_not_op()->bool:
                bresult: bool
                if len(sources) == 2:
                    bresult = row[sources[0]] != row[sources[1]]
                else:
                    bresult = row[sources[0]] != values[0]
                if into_column_idx >= 0:
                    output_row[into_column_idx] = KgtkValue.to_boolean(bresult)
                return bresult if filter else True
            opfunc = is_not_op

        elif operation == IS_OP:
            if not ((len(sources) == 2 and len(values) == 0) or (len(sources) == 1 and len(values) == 1)):
                raise KGTKException("Is needs two sources or one source and one value, got %d sources and %d values" % (len(sources), len(values)))
            if filter:
                if len(into_column_idxs) > 1:
                    raise KGTKException("Is needs at most 1 destination column, got %d" % len(into_column_idxs))
            else:
                if len(into_column_idxs) != 1:
                    raise KGTKException("Is needs 1 destination column, got %d" % len(into_column_idxs))

            def is_op()->bool:
                bresult: bool
                if len(sources) == 2:
                    bresult = row[sources[0]] == row[sources[1]]
                else:
                    bresult = row[sources[0]] == values[0]
                if into_column_idx >= 0:
                    output_row[into_column_idx] = KgtkValue.to_boolean(bresult)
                return bresult if filter else True
            opfunc = is_op

        elif operation == IS_STRING_OP:
            if filter:
                if len(sources) != 1:
                    raise KGTKException("is_string needs one source when filtering, got %d" % len(sources))
                if len(into_column_idxs) > 1:
                    raise KGTKException("is_string needs at most one destination column when filtering, got %d" % (len(into_column_idxs)))

                if into_column_idx >= 0:
                    def is_string_op()->bool:
                        src_idx: int
                        item: str = row[sources[0]]
                        bresult: bool = True if item.startswith(KgtkFormat.STRING_SIGIL) else False
                        output_row[into_column_idx] = KgtkFormat.TRUE_SYMBOL if bresult else KgtkFormat.FALSE_SYMBOL
                        return bresult
                else:
                    def is_string_op()->bool:
                        src_idx: int
                        item: str = row[sources[0]]
                        bresult: bool = True if item.startswith(KgtkFormat.STRING_SIGIL) else False
                        return bresult
            else:
                if len(sources) == 0:
                    raise KGTKException("is_string needs at least one source, got %d" % len(sources))
                if len(sources) != len(into_column_idxs):
                    raise KGTKException("is_string needs the same number of input columns and into columns, got %d and %d" % (len(sources), len(into_column_idxs)))
                def is_string_op()->bool:
                    src_idx: int
                    for src_idx in range(len(sources)):
                        item: str = row[sources[src_idx]]
                        bresult: bool = True if item.startswith(KgtkFormat.STRING_SIGIL) else False
                        output_row[into_column_idxs[src_idx]] = KgtkFormat.TRUE_SYMBOL if bresult else KgtkFormat.FALSE_SYMBOL
                    return True
            opfunc = is_string_op

        elif operation == JOIN_OP:
            if len(sources) == 0:
                raise KGTKException("Join needs at least one source, got %d" % len(sources))
            if len(into_column_idxs) != 1:
                raise KGTKException("Join needs 1 destination columns, got %d" % len(into_column_idxs))
            if len(values) != 1:
                raise KGTKException("Join needs 1 value, got %d" % len(values))

            def join_op()->bool:
                output_row[into_column_idx] = values[0].join((row[sources[idx]] for idx in range(len(sources))))
                return True
            opfunc = join_op

        elif operation == LE_OP:
            if not ((len(sources) == 2 and len(values) == 0) or (len(sources) == 1 and len(values) == 1)):
                raise KGTKException("Le needs two sources or one source and one value, got %d sources and %d values" % (len(sources), len(values)))
            if filter:
                if len(into_column_idxs) > 1:
                    raise KGTKException("Le needs at most 1 destination column, got %d" % len(into_column_idxs))
            else:
                if len(into_column_idxs) != 1:
                    raise KGTKException("Le needs 1 destination column, got %d" % len(into_column_idxs))

            def le_op()->bool:
                bresult: bool = False
                sresult: str = ""
                if len(sources) == 2:
                    if len(row[sources[0]]) > 0 and len(row[sources[1]]) > 0:
                        bresult = float(row[sources[0]]) <= float(row[sources[1]])
                        sresult = KgtkValue.to_boolean(bresult)
                else:
                    if len(row[sources[0]]) > 0 and len(values[0]) > 0:
                        bresult = float(row[sources[0]]) <= float(values[0])
                        sresult = KgtkValue.to_boolean(bresult)
                if into_column_idx >= 0:
                    output_row[into_column_idx] = sresult
                return bresult if filter else True
            opfunc = le_op

        elif operation == LEN_OP:
            if len(sources) == 0:
                raise KGTKException("Len needs at least one source, got %d" % len(sources))
            if len(sources) != len(into_column_idxs):
                raise KGTKException("Len needs the same number of input columns and into columns, got %d and %d" % (len(sources), len(into_column_idxs)))

            def len_op()->bool:
                src_idx: int
                for src_idx in range(len(sources)):
                    item: str = row[sources[src_idx]]
                    if item.startswith((KgtkFormat.STRING_SIGIL, KgtkFormat.LANGUAGE_QUALIFIED_STRING_SIGIL)):
                        output_row[into_column_idxs[src_idx]] = str(len(KgtkFormat.unstringify(item)))
                    else:
                        output_row[into_column_idxs[src_idx]] = str(len(item))
                return True
            opfunc = len_op


        if operation == LIST_SUM_OP:
            # This code supports summaries of numbers or quantities.
            #
            # Numbers can be added to numbers but not quanties.  Quantities
            # cam be added, but only whn the qualifiers (SI units or Qnodes)
            # match.
            #
            # Sums are computed on float values.
            #
            # TODO: Sum integers without conversion to float?
            if len(sources) == 0:
                raise KGTKException("List sum needs at least one source, got %d" % len(sources))
            if len(sources) != len(into_column_idxs):
                raise KGTKException("List sum needs the same number of input columns and into columns, got %d and %d" % (len(sources), len(into_column_idxs)))

            def list_sum_fast_op()->bool:
                # This fast path assumes that when column values contain
                # lists, the list item values are all numbers.  If this assumption
                # is violated, a Python exception might be thrown.
                #
                # Lists are detected and split assuming that the values are numbers
                # and do not include embedded, quoted '|' characters.
                #
                # TODO: Catch the Python excption and optionally proceed.
                src_idx: int
                for src_idx in range(len(sources)):
                    listval: str = row[sources[src_idx]]
                    if '|' not in listval:
                        # We've seen an empty value or a value without a list.  Copy it:
                        output_row[into_column_idxs[src_idx]] = listval
                    else:
                        # The value is a list, presumably of numbers.  Sum it:
                        output_row[into_column_idxs[src_idx]] = str(sum([float(x) for x in listval.split('|')]))
                return True

            def list_sum_op()->bool:
                # NOTE: numbers and quantities cannot be summed.
                #
                # TODO: allow numbers and quantities to be summed if --combine-numbers-and-quantities
                #
                # TODO: use math.fsum(...) for improved accuracy.
                src_idx: int
                for src_idx in range(len(sources)):
                    listval: str = row[sources[src_idx]]
                    if len(listval) == 0:
                        # This is the optimized path for empty values.
                        output_row[into_column_idxs[src_idx]] = ""
                        continue

                    kv: KgtkValue = KgtkValue(listval)
                    if not kv.is_list():
                        # This is the optimized path for non-list values.  Just copy the value.
                        output_row[into_column_idxs[src_idx]] = listval
                        continue

                    fail: bool = False
                    total: typing.Optional[float] = None
                    is_number: typing.Optinal[bool] = None
                    qualifier: str = ""
                    kvitem: KgtkValue
                    for kvitem in kv.get_list_items():
                        if is_number is None:
                            if kvitem.is_number():
                                is_number = True
                                total = float(kvitem.value) # TODO: Use the parsed fields?
                                continue

                            if not kvitem.is_quantity(validate=True, parse_fields=True):
                                fail = True
                                break

                            is_number = False
                            if kvitem.fields is None:
                                fail = True
                                break
                            if kvitem.fields.number is None:
                                fail = True
                                break
                            total = float(kvitem.fields.number)
                            if kvitem.fields.low_tolerancestr is not None or kvitem.fields.high_tolerancestr is not None:
                                # TODO: handle these properly.
                                fail = True
                                break
                            if kvitem.fields.si_units is not None:
                                qualifier = kvitem.fields.si_units
                            else:
                                qualifier = kvitem.fields.units_node
                            continue

                        if is_number:
                            if kvitem.is_number():
                                total += float(kvitem.value)
                                continue
                            else:
                                fail = True
                                break

                        if not kvitem.is_quantity(validate=True, parse_fields=True):
                            fail = True
                            break

                        if kvitem.fields is None:
                            fail = True
                            break
                        if kvitem.fields.number is None:
                            fail = True
                            break
                        total += float(kvitem.fields.number)
                        if kvitem.fields.low_tolerancestr is not None or kvitem.fields.high_tolerancestr is not None:
                            # TODO: handle these properly.
                            fail = True
                            break
                        if kvitem.fields.si_units is not None:
                            if qualifier is None or qualifier != kvitem.fields.si_units:
                                fail = True
                                break
                        else:
                            if qualifier is None or qualifier != kvitem.fields.units_node:
                                fail = True
                                break                                        

                    if fail:
                        output_row[into_column_idxs[src_idx]] = listval
                    else:
                        if is_number is not None and is_number:
                            output_row[into_column_idxs[src_idx]] = str(total)
                        else:
                            output_row[into_column_idxs[src_idx]] = str(total) + qualifier                                
                return True
            opfunc = list_sum_fast_op if be_fast else list_sum_op

        elif operation == LT_OP:
            if not ((len(sources) == 2 and len(values) == 0) or (len(sources) == 1 and len(values) == 1)):
                raise KGTKException("Lt needs two sources or one source and one value, got %d sources and %d values" % (len(sources), len(values)))
            if filter:
                if len(into_column_idxs) > 1:
                    raise KGTKException("Lt needs at most 1 destination column, got %d" % len(into_column_idxs))
            else:
                if len(into_column_idxs) != 1:
                    raise KGTKException("Lt needs 1 destination column, got %d" % len(into_column_idxs))

            def lt_op()->bool:
                bresult: bool = False
                sresult: str = ""
                if len(sources) == 2:
                    if len(row[sources[0]]) > 0 and len(row[sources[1]]) > 0:
                        bresult = float(row[sources[0]]) < float(row[sources[1]])
                        sresult = KgtkValue.to_boolean(bresult)
                else:
                    if len(row[sources[0]]) > 0 and len(values[0]) > 0:
                        bresult = float(row[sources[0]]) < float(values[0])
                        sresult = KgtkValue.to_boolean(bresult)

                if into_column_idx >= 0:
                    output_row[into_column_idx] = sresult
                return bresult if filter else True
            opfunc = lt_op

        elif operation == LOWER_OP:
            if len(sources) == 0:
                raise KGTKException("Lower needs at least one source, got %d" % len(sources))
            if len(sources) != len(into_column_idxs):
                raise KGTKException("Lower needs the same number of input columns and into columns, got %d and %d" % (len(sources), len(into_column_idxs)))

            def lower_op()->bool:
                src_idx: int
                for src_idx in range(len(sources)):
                    output_row[into_column_idxs[src_idx]] = row[sources[src_idx]].lower()
                return True
            opfunc = lower_op

        elif operation == MAX_OP:
            if len(sources) == 0:
                raise KGTKException("Max needs at least one source, got %d" % len(sources))
            if len(into_column_idxs) != 1:
                raise KGTKException("Max needs 1 destination columns, got %d" % len(into_column_idxs))

            def max_op()->bool:
                # TODO: support quantities.
                max_result: typing.Optional[float] = None
                src_idx: int
                for src_idx in sources:
                    item: str = row[src_idx]
                    if len(item) > 0:
                        max_value: float = float(item)
                        if max_result is None or max_value > max_result:
                            max_result = max_value
                for item in values:
                    if len(item) > 0:
                        item_value = float(item)
                        if max_result is None or item_value < max_result:
                            max_result = item_value
                if max_result is not None:
                    output_row[into_column_idx] = fs % max_result
                return True

            def group_by_max_op(max_value: typing.Optional[float],
                                count: typing.Optional[int],
                                finish: bool = False)->typing.Tuple[float, int, bool]:
                if finish:
                    if max_value is None:
                        return None, None, False
                    output_row[into_column_idx] = fs % max_value
                    return None, None, True

                src_idx: int
                item: str
                for src_idx in sources:
                    item = row[src_idx]
                    if len(item) > 0:
                        item_value: float = float(item)
                        if max_value is None or item_value > max_value:
                            max_value = item_value
                return max_value, None, False

            if len(group_by) == 0:
                opfunc = max_op
            else:
                opfunc = group_by_max_op

        elif operation == MIN_OP:
            if len(sources) == 0:
                raise KGTKException("Min needs at least one source, got %d" % len(sources))
            if len(into_column_idxs) != 1:
                raise KGTKException("Min needs 1 destination columns, got %d" % len(into_column_idxs))

            def min_op()->bool:
                # TODO: support quantites.
                min_result: typing.Optional[float] = None
                src_idx: int
                for src_idx in sources:
                    item: str = row[src_idx]
                    if len(item) > 0:
                        item_value: float = float(item)
                        if min_result is None or item_value < min_result:
                            min_result = item_value
                for item in values:
                    if len(item) > 0:
                        item_value = float(item)
                        if min_result is None or item_value < min_result:
                            min_result = item_value
                if min_result is not None:
                    output_row[into_column_idx] = fs % min_result
                return True

            def group_by_min_op(total: typing.Optional[float],
                                count: typing.Optional[int],
                                finish: bool = False)->typing.Tuple[float, int, bool]:
                if finish:
                    if total is None:
                        return None, None, False
                    output_row[into_column_idx] = fs % total
                    return None, None, True

                src_idx: int
                item: str
                for src_idx in sources:
                    item = row[src_idx]
                    if len(item) > 0:
                        item_value: float = float(item)
                        if total is None or item_value < total:
                            total = item_value
                return total, None, False

            if len(group_by) == 0:
                opfunc = min_op
            else:
                opfunc = group_by_min_op

        elif operation == MINUS_OP:
            if not ((len(sources) == 2 and len(values) == 0) or (len(sources) == 1 and len(values) == 1)):
                raise KGTKException("Minus needs two sources or one source and one value, got %d sources and %d values" % (len(sources), len(values)))
            if len(into_column_idxs) != 1:
                raise KGTKException("Minus needs 1 destination columns, got %d" % len(into_column_idxs))

            def minus_2_float_op()->bool:
                output_row[into_column_idx] = str(float(row[sources[0]]) - float(row[sources[1]]))
                return True

            def minus_1_float_op()->bool:
                output_row[into_column_idx] = str(float(row[sources[0]]) - float(values[0]))
                return True

            def minus_2_int_op()->bool:
                output_row[into_column_idx] = str(int(row[sources[0]]) - int(row[sources[1]]))
                return True

            def minus_1_int_op()->bool:
                output_row[into_column_idx] = str(int(row[sources[0]]) - int(values[0]))
                return True

            def minus_op()->bool:
                # NOTE: quantities and numbers can be combined.
                #
                # TODO: allow numbers and quantities to be summed only if --combine-numbers-and-quantities
                leftstr: str = row[sources[0]]
                if len(leftstr) == 0:
                    leftstr = "0" # Simplify matters.

                rightstr: str = row[sources[1]] if len(sources) == 2 else values[0]
                if len(rightstr) == 0:
                    rightstr = "0" # Simplify matters.

                left_kv: Kgtkvalue = KgtkValue(leftstr)
                if not left_kv.is_number_or_quantity(validate=True, parse_fields=True):
                    # Not a number or quantity, fail.
                    #
                    # TODO: a failure indicator might be nice.
                    output_row[into_column_idx] = ""
                    return True

                left_fields: KgtkValueFields = left_kv.fields

                if left_fields is None or left_fields.number is None:
                    # This shouldn't happen.  Fail.
                    #
                    # TODO: a failure indicator might be nice.
                    output_row[into_column_idx] = ""
                    return True
                
                if left_fields.low_tolerancestr is not None or left_fields.high_tolerancestr is not None:
                    # TODO: Handle these properly.
                    output_row[into_column_idx] = ""
                    return True

                left_qualifier: str
                if left_fields.si_units is not None:
                    left_qualifier = left_fields.si_units
                elif left_fields.units_node is not None:
                    left_qualifier = left_fields.units_node
                else:
                    left_qualifier = ""
                
                right_kv: Kgtkvalue = KgtkValue(rightstr)
                if not right_kv.is_number_or_quantity(validate=True, parse_fields=True):
                    # Not a number or quantity, fail.
                    #
                    # TODO: a failure indicator might be nice.
                    output_row[into_column_idx] = ""
                    return True

                right_fields: KgtkValueFields = right_kv.fields

                if right_fields is None or right_fields.number is None:
                    # This shouldn't happen.  Fail.
                    #
                    # TODO: a failure indicator might be nice.
                    output_row[into_column_idx] = ""
                    return True
                
                if right_fields.low_tolerancestr is not None or right_fields.high_tolerancestr is not None:
                    # TODO: Handle these properly.
                    output_row[into_column_idx] = ""
                    return True

                right_qualifier: str
                if right_fields.si_units is not None:
                    right_qualifier = right_fields.si_units
                elif right_fields.units_node is not None:
                    right_qualifier = right_fields.units_node
                else:
                    right_qualifier = ""

                if len(left_qualifier) > 0 and len(right_qualifier) > 0 and left_qualifier != right_qualifier:
                    # Conflicting qualifiers.  Fail.
                    #
                    # TODO: a failure indicator might be nice.
                    output_row[into_column_idx] = ""
                    return True

                output_row[into_column_idx] = str(left_fields.number - right_fields.number) + (right_qualifier if len(right_qualifier) > 0 else left_qualifier)
                return True

            if be_fast:
                if as_int:
                    opfunc = minus_2_int_op if len(sources) == 2 else minus_1_int_op
                else:
                    opfunc = minus_2_float_op if len(sources) == 2 else minus_1_float_op
            else:
                opfunc = minus_op

        elif operation == MOD_OP:
            if not ((len(sources) == 2 and len(values) == 0) or (len(sources) == 1 and len(values) == 1)):
                raise KGTKException("Mod needs two sources or one source and one value, got %d sources and %d values" % (len(sources), len(values)))
            if len(into_column_idxs) != 1:
                raise KGTKException("Mod needs 1 destination columns, got %d" % len(into_column_idxs))

            def mod_op()->bool:
                # TODO: support quanties.
                if len(sources) == 2:
                    output_row[into_column_idx] = str(float(row[sources[0]]) % float(row[sources[1]]))
                else:
                    output_row[into_column_idx] = str(float(row[sources[0]]) % float(values[0]))
                return True
            opfunc = mod_op

        elif operation == NAND_OP:
            if len(sources) == 0:
                raise KGTKException("Nand needs at least one source, got %d" % len(sources))
            if filter:
                if len(into_column_idxs) > 1:
                    raise KGTKException("Nand needs at most 1 destination column, got %d" % len(into_column_idxs))
            else:
                if len(into_column_idxs) != 1:
                    raise KGTKException("Nand needs 1 destination column, got %d" % len(into_column_idxs))

            def nand_op()->bool:
                bresult: bool = True
                src_idx: int
                for src_idx in sources:
                    kv: KgtkValue = KgtkValue(row[src_idx])
                    if kv.is_boolean():
                        bresult = bresult and kv.is_true()

                if into_column_idx >= 0:
                    output_row[into_column_idx] = KgtkValue.to_boolean(not bresult)
                return bresult if filter else True
            opfunc = nand_op

        elif operation == NE_OP:
            if not ((len(sources) == 2 and len(values) == 0) or (len(sources) == 1 and len(values) == 1)):
                raise KGTKException("Ne needs two sources or one source and one value, got %d sources and %d values" % (len(sources), len(values)))
            if filter:
                if len(into_column_idxs) > 1:
                    raise KGTKException("Ne needs at most 1 destination column, got %d" % len(into_column_idxs))
            else:
                if len(into_column_idxs) != 1:
                    raise KGTKException("Ne needs 1 destination column, got %d" % len(into_column_idxs))

            def ne_op()->bool:
                bresult: bool = False
                sresult: str = ""
                if len(sources) == 2:
                    if len(row[sources[0]]) > 0 and len(row[sources[1]]) > 0:
                        bresult = float(row[sources[0]]) != float(row[sources[1]])
                        sresult = KgtkValue.to_boolean(bresult)
                else:
                    if len(row[sources[0]]) > 0 and len(values[0]) > 0:
                        bresult = float(row[sources[0]]) != float(values[0])
                        sresult = KgtkValue.to_boolean(bresult)
                if into_column_idx >= 0:
                    output_row[into_column_idx] = sresult
                return True
            opfunc = ne_op

        elif operation == NEGATE_OP:
            if len(sources) == 0:
                raise KGTKException("Negate needs at least one source, got %d" % len(sources))
                if len(sources) != len(into_column_idxs):
                    raise KGTKException("Negate needs the same number of input columns and into columns, got %d and %d" % (len(sources), len(into_column_idxs)))

            def negate_op()->bool:
                # TODO: support quantities.
                src_idx: int
                for src_idx in range(len(sources)):
                    output_row[into_column_idxs[src_idx]] = str(- float(row[sources[src_idx]]))
                return True
            opfunc = negate_op

        elif operation == NOR_OP:
            if len(sources) == 0:
                raise KGTKException("Nor needs at least one source, got %d" % len(sources))
            if filter:
                if len(into_column_idxs) > 1:
                    raise KGTKException("Nor needs at most 1 destination column, got %d" % len(into_column_idxs))
            else:
                if len(into_column_idxs) != 1:
                    raise KGTKException("Nor needs 1 destination column, got %d" % len(into_column_idxs))

            def nor_op()->bool:
                bresult: bool = False
                for src_idx in sources:
                    kv: KgtkValue = KgtkValue(row[src_idx])
                    if kv.is_boolean():
                        bresult = bresult or kv.is_true()

                output_row[into_column_idx] = KgtkValue.to_boolean(not bresult)
                return bresult if filter else True
            opfunc = nor_op

        elif operation == NOT_OP:
            if len(sources) == 0:
                raise KGTKException("Not needs at least one source, got %d" % len(sources))
            if filter:
                if len(into_column_idxs) > 0 and len(into_column_idxs) != len(sources):
                    raise KGTKException("Nand needs the same number of input columns and into colums, got %d and %d" % (len(sources), len(into_column_idxs)))
            else:
                if len(into_column_idxs) != len(sources):
                    raise KGTKException("Nand needs the same number of input columns and into colums, got %d and %d" % (len(sources), len(into_column_idxs)))

            def not_op()->bool:
                bresult = False
                src_idx: int
                for src_idx in sources:
                    kv: KgtkValue = KgtkValue(row[src_idx])
                    sresult: str = ""
                    if kv.is_boolean():
                        bresult = not kv.is_true()
                        if len(into_column_idxs) > 0:
                            output_row[into_column_idxs[src_idx]] = ""
                return bresult if filter else True
            opfunc = not_op

        elif operation == NUMBER_OP:
            # Extract a number from a number or quantiy.
            #
            # TODO:  Need number parsing options.
            #
            # TODO:  Need an operator to extract the qualifiers from a quantity.
            if len(sources) == 0:
                raise KGTKException("number needs at least one source, got %d" % len(sources))
            if len(sources) != len(into_column_idxs):
                raise KGTKException("number needs the same number of input columns and into columns, got %d and %d" % (len(sources), len(into_column_idxs)))

            if to_string:
                def number_op()->bool:
                    src_idx: int
                    for src_idx in range(len(sources)):
                        item: str = row[sources[src_idx]]
                        # TODO: optimize this.
                        kv: KgtkValue = KgtkValue(item) # TODO: Need options!
                        if kv.is_number_or_quantity(validate=True, parse_fields=True) and kv.fields is not None:
                            output_row[into_column_idxs[src_idx]] = KgtkFormat.STRING_SIGIL + kv.fields.numberstr + KgtkFormat.STRING_SIGIL
                        else:
                            output_row[into_column_idxs[src_idx]] = ""
                    return True
            else:
                def number_op()->bool:
                    src_idx: int
                    for src_idx in range(len(sources)):
                        item: str = row[sources[src_idx]]
                        # TODO: optimize this.
                        kv: KgtkValue = KgtkValue(item) # TODO: Need options!
                        if kv.is_number_or_quantity(validate=True, parse_fields=True) and kv.fields is not None:
                            output_row[into_column_idxs[src_idx]] = kv.fields.numberstr
                        else:
                            output_row[into_column_idxs[src_idx]] = ""
                    return True
            opfunc = number_op

        elif operation == OR_OP:
            if len(sources) == 0:
                raise KGTKException("Or needs at least one source, got %d" % len(sources))
            if filter:
                if len(into_column_idxs) > 1:
                    raise KGTKException("Or needs at most 1 destination column, got %d" % len(into_column_idxs))
            else:
                if len(into_column_idxs) != 1:
                    raise KGTKException("Or needs 1 destination column, got %d" % len(into_column_idxs))

            def or_op()->bool:
                bresult: bool = False
                src_idx: int
                for src_idx in sources:
                    kv: Kgtkvalue = KgtkValue(row[src_idx])
                    if kv.is_boolean():
                        bresult = bresult or kv.is_true()

                if into_column_idx >= 0:
                    output_row[into_column_idx] = KgtkValue.to_boolean(bresult)
                return bresult if filter else True
            opfunc = or_op

        elif operation == PERCENTAGE_OP:
            if len(into_column_idxs) != 1:
                raise KGTKException("Percent needs 1 destination columns, got %d" % len(into_column_idxs))
            if len(sources) != 2:
                raise KGTKException("Percent needs 2 input columns, got %d" % len(sources))

            def percentage_op()->bool:
                # TODO: Support quantities?
                output_row[into_column_idx] = fs % (float(row[sources[0]]) * 100 / float(row[sources[1]]))
                return True
            opfunc = percentage_op

        elif operation == REPLACE_OP:
            if len(into_column_idxs) != 1:
                raise KGTKException("Replace needs 1 destination column, got %d" % len(into_column_idxs))
            if len(sources) != 1:
                raise KGTKException("Replace needs 1 input column, got %d" % len(sources))
            if len(values) != 1:
                raise KGTKException("Replace needs one value, got %d" % len(values))
            if len(with_values) != 1:
                raise KGTKException("Replace needs one with-value, got %d" % len(with_values))

            def replace_op()->bool:
                if limit == 0:
                    output_row[into_column_idx] = row[sources[0]].replace(values[0], with_values[0])
                else:
                    output_row[into_column_idx] = row[sources[0]].replace(values[0], with_values[0], limit)
                return True
            opfunc = replace_op
            
        elif operation == REVERSE_DIV_OP:
            if not ((len(sources) == 2 and len(values) == 0) or (len(sources) == 1 and len(values) == 1)):
                raise KGTKException("Reverse divide needs two sources or one source and one value, got %d sources and %d values" % (len(sources), len(values)))
            if len(into_column_idxs) != 1:
                raise KGTKException("Reverse divide needs 1 destination columns, got %d" % len(into_column_idxs))

            def reverse_div_op()->bool:
                # TODO: Support quantities.
                if len(sources) == 2:
                    output_row[into_column_idx] = str(float(row[sources[1]]) / float(row[sources[0]]))
                else:
                    output_row[into_column_idx] = str(float(values[0]) / float(row[sources[0]]))
                return True
            opfunc = reverse_div_op

        elif operation == REVERSE_MINUS_OP:
            if not ((len(sources) == 2 and len(values) == 0) or (len(sources) == 1 and len(values) == 1)):
                raise KGTKException("Reverse minus needs two sources or one source and one value, got %d sources and %d values" % (len(sources), len(values)))
            if len(into_column_idxs) != 1:
                raise KGTKException("Reverse minus needs 1 destination columns, got %d" % len(into_column_idxs))

            def reverse_minus_op()->bool:
                # TODO: Support quanties.
                if len(sources) == 2:
                    output_row[into_column_idx] = str(float(row[sources[1]]) - float(row[sources[0]]))
                else:
                    output_row[into_column_idx] = str(float(values[0]) - float(row[sources[0]]))
                return True
            opfunc = reverse_minus_op

        elif operation == REVERSE_MOD_OP:
            if not ((len(sources) == 2 and len(values) == 0) or (len(sources) == 1 and len(values) == 1)):
                raise KGTKException("Reverse mod needs two sources or one source and one value, got %d sources and %d values" % (len(sources), len(values)))
            if len(into_column_idxs) != 1:
                raise KGTKException("Reverse mod needs 1 destination columns, got %d" % len(into_column_idxs))

            def reverse_mod_op()->bool:
                # TODO: support quantities.
                if len(sources) == 2:
                    output_row[into_column_idx] = str(float(row[sources[1]]) % float(row[sources[0]]))
                else:
                    output_row[into_column_idx] = str(float(values[0]) % float(row[sources[0]]))
                return True
            opfunc = reverse_mod_op

        elif operation == SET_OP:
            if len(sources) != 0:
                raise KGTKException("Set needs no sources, got %d" % len(sources))
            if len(into_column_idxs) == 0:
                raise KGTKException("Set needs at least one destination column, got %d" % len(into_column_idxs))
            if len(values) == 0:
                raise KGTKException("Set needs at least one value, got %d" % len(values))
            if len(into_column_idxs) != len(values):
                raise KGTKException("Set needs the same number of destination columns and values, got %d and %d" % (len(into_column_idxs), len(values)))

            if overwrite:
                def set_op()->bool:
                    value_idx: int
                    for value_idx in range(len(values)):
                        output_row[into_column_idxs[value_idx]] = values[value_idx]
                    return True
            else:
                def set_op()->bool:
                    value_idx: int
                    for value_idx in range(len(values)):
                        if len(output_row[into_column_idxs[value_idx]]) == 0:
                            output_row[into_column_idxs[value_idx]] = values[value_idx]
                    return True
            opfunc = set_op

        elif operation == STRING_LANG_OP:
            if len(sources) == 0:
                raise KGTKException("String_lang needs at least one source, got %d" % len(sources))
            if len(sources) != len(into_column_idxs):
                raise KGTKException("String_lang needs the same number of input columns and into columns, got %d and %d" % (len(sources), len(into_column_idxs)))

            if to_string:
                def string_lang_op()->bool:
                    src_idx: int
                    for src_idx in range(len(sources)):
                        item: str = row[sources[src_idx]]
                        if item.startswith((KgtkFormat.STRING_SIGIL, KgtkFormat.LANGUAGE_QUALIFIED_STRING_SIGIL)):
                            # TODO: optimize this.
                            text: str
                            lang: str
                            suffix: str
                            text, lang, suffix = KgtkFormat.destringify(item)
                            output_row[into_column_idxs[src_idx]] = KgtkFormat.stringify(lang)
                        else:
                            output_row[into_column_idxs[src_idx]] = ""
                    return True
            else:
                def string_lang_op()->bool:
                    src_idx: int
                    for src_idx in range(len(sources)):
                        item: str = row[sources[src_idx]]
                        if item.startswith((KgtkFormat.STRING_SIGIL, KgtkFormat.LANGUAGE_QUALIFIED_STRING_SIGIL)):
                            # TODO: optimize this.
                            text: str
                            lang: str
                            suffix: str
                            text, lang, suffix = KgtkFormat.destringify(item)
                            output_row[into_column_idxs[src_idx]] = lang
                        else:
                            output_row[into_column_idxs[src_idx]] = ""
                    return True
            opfunc = string_lang_op

        elif operation == STRING_LANG_SUFFIX_OP:
            if len(sources) == 0:
                raise KGTKException("String_lang_suffix needs at least one source, got %d" % len(sources))
            if len(sources) != len(into_column_idxs):
                raise KGTKException("String_lang_suffix needs the same number of input columns and into columns, got %d and %d" % (len(sources), len(into_column_idxs)))

            if to_string:
                def string_lang_suffix_op()->bool:
                    src_idx: int
                    for src_idx in range(len(sources)):
                        item: str = row[sources[src_idx]]
                        if item.startswith((KgtkFormat.STRING_SIGIL, KgtkFormat.LANGUAGE_QUALIFIED_STRING_SIGIL)):
                            # TODO: optimize this.
                            text: str
                            lang: str
                            suffix: str
                            text, lang, suffix = KgtkFormat.destringify(item)
                            output_row[into_column_idxs[src_idx]] = KgtkFormat.stringify(lang + suffix)
                        else:
                            output_row[into_column_idxs[src_idx]] = ""
                    return True
            else:
                def string_lang_suffix_op()->bool:
                    src_idx: int
                    for src_idx in range(len(sources)):
                        item: str = row[sources[src_idx]]
                        if item.startswith((KgtkFormat.STRING_SIGIL, KgtkFormat.LANGUAGE_QUALIFIED_STRING_SIGIL)):
                            # TODO: optimize this.
                            text: str
                            lang: str
                            suffix: str
                            text, lang, suffix = KgtkFormat.destringify(item)
                            output_row[into_column_idxs[src_idx]] = lang + suffix
                        else:
                            output_row[into_column_idxs[src_idx]] = ""
                    return True
            opfunc = string_lang_suffix_op

        elif operation == STRING_SUFFIX_OP:
            if len(sources) == 0:
                raise KGTKException("String_suffix needs at least one source, got %d" % len(sources))
            if len(sources) != len(into_column_idxs):
                raise KGTKException("String_suffix needs the same number of input columns and into columns, got %d and %d" % (len(sources), len(into_column_idxs)))

            if to_string:
                def string_suffix_op()->bool:
                    src_idx: int
                    for src_idx in range(len(sources)):
                        item: str = row[sources[src_idx]]
                        if item.startswith((KgtkFormat.STRING_SIGIL, KgtkFormat.LANGUAGE_QUALIFIED_STRING_SIGIL)):
                            # TODO: optimize this.
                            text: str
                            lang: str
                            suffix: str
                            text, lang, suffix = KgtkFormat.destringify(item)
                            output_row[into_column_idxs[src_idx]] = KgtkFormat.stringify(suffix)
                        else:
                            output_row[into_column_idxs[src_idx]] = ""
                    return True
            else:
                def string_suffix_op()->bool:
                    src_idx: int
                    for src_idx in range(len(sources)):
                        item: str = row[sources[src_idx]]
                        if item.startswith((KgtkFormat.STRING_SIGIL, KgtkFormat.LANGUAGE_QUALIFIED_STRING_SIGIL)):
                            # TODO: optimize this.
                            text: str
                            lang: str
                            suffix: str
                            text, lang, suffix = KgtkFormat.destringify(item)
                            output_row[into_column_idxs[src_idx]] = suffix
                        else:
                            output_row[into_column_idxs[src_idx]] = ""
                    return True
            opfunc = string_suffix_op

        elif operation == STRING_TEXT_OP:
            if len(sources) == 0:
                raise KGTKException("String_text needs at least one source, got %d" % len(sources))
            if len(sources) != len(into_column_idxs):
                raise KGTKException("String_text needs the same number of input columns and into columns, got %d and %d" % (len(sources), len(into_column_idxs)))

            def string_text_op()->bool:
                src_idx: int
                for src_idx in range(len(sources)):
                    item: str = row[sources[src_idx]]
                    if item.startswith((KgtkFormat.STRING_SIGIL, KgtkFormat.LANGUAGE_QUALIFIED_STRING_SIGIL)):
                        # TODO: optimize this.
                        output_row[into_column_idxs[src_idx]] = KgtkFormat.stringify(KgtkFormat.unstringify(item))
                    else:
                        output_row[into_column_idxs[src_idx]] = ""
                return True
            opfunc = string_text_op

        elif operation == SUBSTRING_OP:
            if len(into_column_idxs) != 1:
                raise KGTKException("Substring needs 1 destination column, got %d" % len(into_column_idxs))
            if len(sources) != 1:
                raise KGTKException("Substring needs 1 input column, got %d" % len(sources))
            if len(values) not in (1, 2):
                raise KGTKException("Substring needs one or two values, got %d" % len(values))

            start_slice: int
            end_slice: typing.Optional[int]
            if len(values) == 1:
                start_slice = int(values[0])
                end_slice = None
            else:
                start_slice = int(values[0])
                end_slice = int(values[1])

            if overwrite:
                def substring_op()->bool:
                    item: str = row[sources[0]]
                    if item.startswith((KgtkFormat.STRING_SIGIL, KgtkFormat.LANGUAGE_QUALIFIED_STRING_SIGIL)):
                        item = KgtkFormat.unstringify(item)
                        if end_slice is None:
                            output_row[into_column_idx] = KgtkFormat.stringify(item[start_slice:])
                        else:
                            output_row[into_column_idx] = KgtkFormat.stringify(item[start_slice:end_slice])
                    else:
                        if end_slice is None:
                            if to_string:
                                output_row[into_column_idx] = KgtkFormat.stringify(item[start_slice:])
                            else:
                                output_row[into_column_idx] = item[start_slice:]
                        else:
                            if to_string:
                                output_row[into_column_idx] = KgtkFormat.stringify(item[start_slice:end_slice])
                            else:
                                output_row[into_column_idx] = item[start_slice:end_slice]
                    return True
            else:
                def substring_op()->bool:
                    if len(output_row[into_column_idx]) >0:
                        return
                    item: str = row[sources[0]]
                    if item.startswith((KgtkFormat.STRING_SIGIL, KgtkFormat.LANGUAGE_QUALIFIED_STRING_SIGIL)):
                        item = KgtkFormat.unstringify(item)
                        if end_slice is None:
                            output_row[into_column_idx] = KgtkFormat.stringify(item[start_slice:])
                        else:
                            output_row[into_column_idx] = KgtkFormat.stringify(item[start_slice:end_slice])
                    else:
                        if end_slice is None:
                            if to_string:
                                output_row[into_column_idx] = KgtkFormat.stringify(item[start_slice:])
                            else:
                                output_row[into_column_idx] = item[start_slice:]
                        else:
                            if to_string:
                                output_row[into_column_idx] = KgtkFormat.stringify(item[start_slice:end_slice])
                            else:
                                output_row[into_column_idx] = item[start_slice:end_slice]
                    return True
            opfunc = substring_op

        elif operation == SUBSTITUTE_OP:
            if len(into_column_idxs) != 1:
                raise KGTKException("Substitute needs 1 destination column, got %d" % len(into_column_idxs))
            if len(sources) != 1:
                raise KGTKException("Substitute needs 1 input column, got %d" % len(sources))
            if len(values) != 1:
                raise KGTKException("Substitute needs one value, got %d" % len(values))
            if len(with_values) != 1:
                raise KGTKException("Substitute needs one with-value, got %d" % len(with_values))
            substitute_re: typing.Pattern = re.compile(values[0])

            def substitute_op()->bool:
                output_row[into_column_idx] = substitute_re.sub(with_values[0], row[sources[0]], count=limit)
                return True
            opfunc = substitute_op

        elif operation == SUM_OP:
            # TODO: Support quantities.
            if len(sources) == 0:
                raise KGTKException("Sum needs at least one source, got %d" % len(sources))
            if len(into_column_idxs) != 1:
                raise KGTKException("Sum needs 1 destination columns, got %d" % len(into_column_idxs))
            if len(group_by) > 0 and len(values) >> 0:
                raise KGTKException("Group-by Sum cannot use values, got %d" % len(values))

            def sum_op()->bool:
                total: float = 0
                src_idx: int
                item: str
                for src_idx in sources:
                    item = row[src_idx]
                    if len(item) > 0:
                        total += float(item)
                for item in values:
                    if len(item) > 0:
                        total += float(item)
                output_row[into_column_idx] = fs % total
                return True

            def group_by_sum_op(total: typing.Optional[float],
                                count: typing.Optional[int],
                                finish: bool = False)->typing.Tuple[float, int, bool]:
                if finish:
                    if total is None:
                        return None, None, False
                    output_row[into_column_idx] = fs % total
                    return None, None, True

                src_idx: int
                item: str
                for src_idx in sources:
                    item = row[src_idx]
                    if len(item) > 0:
                        if total is None:
                            total = 0.0
                        total += float(item)
                return total, None, False

            if len(group_by) == 0:
                opfunc = sum_op
            else:
                opfunc = group_by_sum_op

        elif operation == SWAPCASE_OP:
            if len(sources) == 0:
                raise KGTKException("Swapcase needs at least one source, got %d" % len(sources))
            if len(sources) != len(into_column_idxs):
                raise KGTKException("Swapcase needs the same number of input columns and into columns, got %d and %d" % (len(sources), len(into_column_idxs)))

            def swapcase_op()->bool:
                src_idx: int
                for src_idx in range(len(sources)):
                    output_row[into_column_idxs[src_idx]] = row[sources[src_idx]].swapcase()
                return True
            opfunc = swapcase_op

        elif operation == TITLE_OP:
            if len(sources) == 0:
                raise KGTKException("Title needs at least one source, got %d" % len(sources))
            if len(sources) != len(into_column_idxs):
                raise KGTKException("Title needs the same number of input columns and into columns, got %d and %d" % (len(sources), len(into_column_idxs)))

            def title_op()->bool:
                src_idx: int
                for src_idx in range(len(sources)):
                    output_row[into_column_idxs[src_idx]] = row[sources[src_idx]].title()
                return True
            opfunc = title_op

        elif operation == UPPER_OP:
            if len(sources) == 0:
                raise KGTKException("Upper needs at least one source, got %d" % len(sources))
            if len(sources) != len(into_column_idxs):
                raise KGTKException("Upper needs the same number of input columns and into columns, got %d and %d" % (len(sources), len(into_column_idxs)))

            def upper_op()->bool:
                src_idx: int
                for src_idx in range(len(sources)):
                    output_row[into_column_idxs[src_idx]] = row[sources[src_idx]].upper()
                return True
            opfunc = upper_op

        elif operation == XOR_OP:
            if len(sources) == 0:
                raise KGTKException("Xor needs at least one source, got %d" % len(sources))
            if filter:
                if len(into_column_idxs) > 1:
                    raise KGTKException("Xor needs at most 1 destination column, got %d" % len(into_column_idxs))
            else:
                if len(into_column_idxs) != 1:
                    raise KGTKException("Xor needs 1 destination column, got %d" % len(into_column_idxs))

            def xor_op()->bool:
                bresult: bool = False
                src_idx: int
                for src_idx in sources:
                    kv: KgtkValue = KgtkValue(row[src_idx])
                    if kv.is_boolean():
                        bresult = bresult != kv.is_true()

                if into_column_idx >= 0:
                    output_row[into_column_idx] = KgtkValue.to_boolean(bresult)
                return bresult if filter else True
            opfunc = xor_op

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

        if len(group_by) == 0:
            for row in kr:
                input_data_lines += 1

                output_row = row.copy()
                for idx in range(new_column_count):
                    output_row.append("") # Easiest way to add a new column.

                if opfunc():
                    kw.write(output_row)

        else:
            # TODO: Use objects instead of function references.  The objects
            # can hold the `total` and `count` state as needed.
            previous_group_by_values: typing.List[str] = list()
            total: typing.Optional[float] = None
            count: typing.Optional[int] = None
            do_output: bool
            for row in kr:
                input_data_lines += 1

                finish: bool = False
                if input_data_lines == 1:
                    for in_idx in group_by:
                        previous_group_by_values.append(row[in_idx])
                else:
                    group_by_idx: int
                    for group_by_idx, in_idx in enumerate(group_by):
                        if row[in_idx] != previous_group_by_values[group_by_idx]:
                            finish = True
                            break

                if finish:
                    output_row = previous_group_by_values # no need to copy
                    for new_column_idx in range(new_column_count):
                        output_row.append("") # Easiest way to add a new column.
                    total, count, do_output = opfunc(total, count, finish=True)
                    if do_output:
                        if group_by_label_idx >= 0:
                            output_row[group_by_label_idx] = group_by_label
                        kw.write(output_row)
                    previous_group_by_values = list()
                    for in_idx in group_by:
                        previous_group_by_values.append(row[in_idx])
                total, count, do_output = opfunc(total, count)
            
            output_row = previous_group_by_values # no need to copy
            for new_column_idx in range(new_column_count):
                output_row.append("") # Easiest way to add a new column.
            total, count, do_output = opfunc(total, count, finish=True)
            if do_output:
                if group_by_label_idx >= 0:
                    output_row[group_by_label_idx] = group_by_label
                kw.write(output_row)

        # Flush the output file so far:
        kw.flush()

        if verbose:
            print("Read %d data lines from file %s" % (input_data_lines, input_kgtk_file), file=error_file, flush=True)

        kw.close()

        return 0

    except SystemExit as e:
        raise KGTKException("Exit requested")
    except KGTKException as e:
        raise
    except Exception as e:
        raise KGTKException(str(e))

