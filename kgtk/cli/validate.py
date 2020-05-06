"""
Validate a KGTK file, producing error messages.

At the present time, validation looks at such things as:
1)      Presence of require columns
2)      Consistent number of columns
3)      Comments, whitespace lines, line s with empty required columns

Certain constraints can be overlooked or repaired.

This program does not validate individual fields.
"""

from pathlib import Path
import sys
import typing

from kgtk.join.enumnameaction import EnumNameAction
from kgtk.join.kgtkformat import KgtkFormat
from kgtk.join.kgtkreader import KgtkReader
from kgtk.join.kgtkvalueoptions import KgtkValueOptions
from kgtk.join.validationaction import ValidationAction

def parser():
    return {
        'help': 'Validate a KGTK file '
    }


def add_arguments(parser):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """
    parser.add_argument(      "kgtk_files", nargs="*", help="The KGTK file(s) to validate. May be omitted or '-' for stdin.", type=Path)

    parser.add_argument(      "--blank-id-line-action", dest="blank_id_line_action",
                              help="The action to take when a blank id field is detected.",
                              type=ValidationAction, action=EnumNameAction, default=None)

    parser.add_argument(      "--blank-node1-line-action", dest="blank_node1_line_action",
                              help="The action to take when a blank node1 field is detected.",
                              type=ValidationAction, action=EnumNameAction, default=None)

    parser.add_argument(      "--blank-node2-line-action", dest="blank_node2_line_action",
                              help="The action to take when a blank node2 field is detected.",
                              type=ValidationAction, action=EnumNameAction, default=None)

    parser.add_argument(      "--blank-required-field-line-action", dest="blank_line_action",
                              help="The action to take when a line with a blank node1, node2, or id field (per mode) is detected.",
                              type=ValidationAction, action=EnumNameAction, default=ValidationAction.COMPLAIN)

    parser.add_argument(      "--column-separator", dest="column_separator",
                              help="Column separator.", type=str, default=KgtkReader.COLUMN_SEPARATOR)

    parser.add_argument(      "--comment-line-action", dest="comment_line_action",
                              help="The action to take when a comment line is detected.",
                              type=ValidationAction, action=EnumNameAction, default=ValidationAction.COMPLAIN)

    parser.add_argument(      "--compression-type", dest="compression_type",
                              help="Specify the input file compression type, otherwise use the extension.")
    
    parser.add_argument(      "--empty-line-action", dest="empty_line_action",
                              help="The action to take when an empty line is detected.",
                              type=ValidationAction, action=EnumNameAction, default=ValidationAction.COMPLAIN)

    errors_to = parser.add_mutually_exclusive_group()
    errors_to.add_argument(      "--errors-to-stdout", dest="errors_to_stdout",
                              help="Send errors to stdout instead of stderr (default)", action="store_true")
    errors_to.add_argument(      "--errors-to-stderr", dest="errors_to_stderr",
                              help="Send errors to stderr instead of stdout", action="store_true")

    parser.add_argument(      "--error-limit", dest="error_limit",
                              help="The maximum number of errors to report before failing", type=int, default=KgtkReader.ERROR_LIMIT_DEFAULT)

    parser.add_argument(      "--fill-short-lines", dest="fill_short_lines",
                              help="Fill missing trailing columns in short lines with empty values.", action='store_true')

    parser.add_argument(      "--force-column-names", dest="force_column_names", help="Force the column names.", nargs='+')

    parser.add_argument(      "--gzip-in-parallel", dest="gzip_in_parallel", help="Execute gzip in parallel.", action='store_true')

    parser.add_argument(      "--gzip-queue-size", dest="gzip_queue_size",
                              help="Queue size for parallel gzip.", type=int, default=KgtkReader.GZIP_QUEUE_SIZE_DEFAULT)

    parser.add_argument(      "--header-error-action", dest="header_error_action",
                              help="The action to take when a header error is detected  Only ERROR or EXIT are supported.",
                              type=ValidationAction, action=EnumNameAction, default=ValidationAction.EXIT)

    parser.add_argument(      "--header-only", dest="header_only",
                              help="Process the only the header of the input file.", action="store_true")

    parser.add_argument(      "--invalid-value-action", dest="invalid_value_action",
                              help="The action to take when a data cell value is invalid.",
                              type=ValidationAction, action=EnumNameAction, default=ValidationAction.REPORT)

    parser.add_argument(      "--long-line-action", dest="long_line_action",
                              help="The action to take when a long line is detected.",
                              type=ValidationAction, action=EnumNameAction, default=ValidationAction.COMPLAIN)

    parser.add_argument(      "--mode", dest="mode",
                              help="Determine the KGTK input file mode.", type=KgtkReader.Mode, action=EnumNameAction, default=KgtkReader.Mode.AUTO)

    parser.add_argument(      "--short-line-action", dest="short_line_action",
                              help="The action to take whe a short line is detected.",
                              type=ValidationAction, action=EnumNameAction, default=ValidationAction.COMPLAIN)

    parser.add_argument(      "--skip-first-record", dest="skip_first_record", help="Skip the first record when forcing column names.", action='store_true')

    parser.add_argument(      "--truncate-long-lines", dest="truncate_long_lines",
                              help="Remove excess trailing columns in long lines.", action='store_true')

    parser.add_argument(      "--unsafe-column-name-action", dest="unsafe_column_name_action",
                              help="The action to take when a column name is unsafe.",
                              type=ValidationAction, action=EnumNameAction, default=ValidationAction.REPORT)

    parser.add_argument("-v", "--verbose", dest="verbose", help="Print additional progress messages.", action='store_true')
    
    parser.add_argument(      "--very-verbose", dest="very_verbose", help="Print additional progress messages.", action='store_true')
    
    parser.add_argument(      "--whitespace-line-action", dest="whitespace_line_action",
                              help="The action to take when a whitespace line is detected.",
                              type=ValidationAction, action=EnumNameAction, default=ValidationAction.EXCLUDE)

    # Note: Any arguments described by KgtkValueOptions.add_arguments(...)
    # need to be included in the arguments to run(...), below.
    KgtkValueOptions.add_arguments(parser)


def run(kgtk_files: typing.Optional[typing.List[typing.Optional[Path]]],
        force_column_names: typing.Optional[typing.List[str]] = None,
        skip_first_record: bool = False,
        fill_short_lines: bool = False,
        truncate_long_lines: bool = False,
        errors_to_stdout: bool = False,
        errors_to_stderr: bool = False,
        error_limit: int = KgtkReader.ERROR_LIMIT_DEFAULT,
        empty_line_action: ValidationAction = ValidationAction.COMPLAIN,
        comment_line_action: ValidationAction = ValidationAction.COMPLAIN,
        whitespace_line_action: ValidationAction = ValidationAction.COMPLAIN,
        blank_line_action: ValidationAction = ValidationAction.COMPLAIN,
        blank_node1_line_action: typing.Optional[ValidationAction] = None,
        blank_node2_line_action: typing.Optional[ValidationAction] = None,
        blank_id_line_action: typing.Optional[ValidationAction] = None,
        short_line_action: ValidationAction = ValidationAction.COMPLAIN,
        long_line_action: ValidationAction = ValidationAction.COMPLAIN,
        invalid_value_action: ValidationAction = ValidationAction.REPORT,
        header_error_action: ValidationAction = ValidationAction.EXIT,
        unsafe_column_name_action: ValidationAction = ValidationAction.REPORT,
        additional_language_codes: typing.Optional[typing.List[str]] = None,
        allow_language_suffixes: bool = False,
        allow_lax_strings: bool = False,
        allow_lax_lq_strings: bool = False,
        allow_month_or_day_zero: bool = False,
        repair_month_or_day_zero: bool = False,
        escape_list_separators: bool = False,
        minimum_valid_year: int = KgtkValueOptions.MINIMUM_VALID_YEAR,
        maximum_valid_year: int = KgtkValueOptions.MAXIMUM_VALID_YEAR,
        compression_type: typing.Optional[str] = None,
        gzip_in_parallel: bool = False,
        gzip_queue_size: int = KgtkReader.GZIP_QUEUE_SIZE_DEFAULT,
        column_separator: str = KgtkFormat.COLUMN_SEPARATOR,
        mode: KgtkReader.Mode = KgtkReader.Mode.AUTO,
        header_only: bool = False,
        verbose: bool = False,
        very_verbose: bool = False,
)->int:
    # import modules locally
    from kgtk.exceptions import KGTKException

    if kgtk_files is None or len(kgtk_files) == 0:
        kgtk_files = [ None ]

    # Select where to send error messages, defaulting to stderr.
    error_file: typing.TextIO = sys.stderr if errors_to_stderr else sys.stdout

    # Build the value parsing option structure.
    value_options: KgtkValueOptions = KgtkValueOptions(allow_month_or_day_zero=allow_month_or_day_zero,
                                                       repair_month_or_day_zero=repair_month_or_day_zero,
                                                       allow_lax_strings=allow_lax_strings,
                                                       allow_lax_lq_strings=allow_lax_lq_strings,
                                                       allow_language_suffixes=allow_language_suffixes,
                                                       additional_language_codes=additional_language_codes,
                                                       minimum_valid_year=minimum_valid_year,
                                                       maximum_valid_year=maximum_valid_year,
                                                       escape_list_separators=escape_list_separators)

    try:
        kgtk_file: typing.Optional[Path]
        for kgtk_file in kgtk_files:
            if verbose:
                print("\n====================================================", flush=True)
                if kgtk_file is not None:
                    print("Validating '%s'" % str(kgtk_file), file=error_file, flush=True)
                else:
                    print ("Validating from stdin", file=error_file, flush=True)

                kr: KgtkReader = KgtkReader.open(kgtk_file,
                                                 force_column_names=force_column_names,
                                                 skip_first_record=skip_first_record,
                                                 fill_short_lines=fill_short_lines,
                                                 truncate_long_lines=truncate_long_lines,
                                                 error_file=error_file,
                                                 error_limit=error_limit,
                                                 empty_line_action=empty_line_action,
                                                 comment_line_action=comment_line_action,
                                                 whitespace_line_action=whitespace_line_action,
                                                 blank_line_action=blank_line_action,
                                                 blank_node1_line_action=blank_node1_line_action,
                                                 blank_node2_line_action=blank_node2_line_action,
                                                 blank_id_line_action=blank_id_line_action,
                                                 short_line_action=short_line_action,
                                                 long_line_action=long_line_action,
                                                 invalid_value_action=invalid_value_action,
                                                 header_error_action=header_error_action,
                                                 unsafe_column_name_action=unsafe_column_name_action,
                                                 compression_type=compression_type,
                                                 value_options=value_options,
                                                 gzip_in_parallel=gzip_in_parallel,
                                                 gzip_queue_size=gzip_queue_size,
                                                 column_separator=column_separator,
                                                 mode=mode,
                                                 verbose=verbose, very_verbose=very_verbose)
        
                if header_only:
                    kr.close()
                    if verbose:
                        print("Validated the header only.", file=error_file, flush=True)
                else:
                    line_count: int = 0
                    row: typing.List[str]
                    for row in kr:
                        line_count += 1
                    if verbose:
                        print("Validated %d data lines" % line_count, file=error_file, flush=True)
        return 0

    except SystemExit as e:
        raise KGTKException("Exit requested")
    except Exception as e:
        raise KGTKException(str(e))

