"""Filter a KGTK file based on whether one or more records exist in a second
KGTK file with matching values for one or more fields.
"""

from pathlib import Path
import sys
import typing

from kgtk.kgtkformat import KgtkFormat
from kgtk.io.kgtkreader import KgtkReader
from kgtk.io.kgtkwriter import KgtkWriter
from kgtk.join.ifexists import IfExists
from kgtk.utils.enumnameaction import EnumNameAction
from kgtk.utils.validationaction import ValidationAction
from kgtk.value.kgtkvalueoptions import KgtkValueOptions

def parser():
    return {
        'help': 'Filter a KGTK file based on whether one or more records exist in a second KGTK file with matching values for one or more fields.'
    }


def add_arguments(parser):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """
    parser.add_argument(      "input_kgtk_file", nargs="?", help="The KGTK file to filter ('left' file). May be omitted or '-' for stdin.", type=Path)

    parser.add_argument(      "--filter-on", dest="filter_kgtk_file", help="The KGTK file to filter against ('right' file).", type=Path, required=True)

    parser.add_argument("-o", "--output-file", dest="output_kgtk_file", help="The KGTK file to write", type=Path, default=None)

    parser.add_argument(      "--left-keys", dest="left_keys", help="The key columns in the file being filtered.", nargs='*')

    parser.add_argument(      "--right-keys", dest="right_keys", help="The key columns in the filter-on file.", nargs='*')


    # A subset of common arguments:
    errors_to = parser.add_mutually_exclusive_group()
    errors_to.add_argument(      "--errors-to-stdout", dest="errors_to_stdout",
                              help="Send errors to stdout instead of stderr (default)", action="store_true")
    errors_to.add_argument(      "--errors-to-stderr", dest="errors_to_stderr",
                              help="Send errors to stderr instead of stdout", action="store_true")

    parser.add_argument(      "--error-limit", dest="error_limit",
                              help="The maximum number of errors to report before failing", type=int, default=KgtkReader.ERROR_LIMIT_DEFAULT)

    parser.add_argument(      "--field-separator", dest="field_separator",
                              help="Field separator.", type=str, default=IfExists.FIELD_SEPARATOR_DEFAULT)

    parser.add_argument("-v", "--verbose", dest="verbose", help="Print additional progress messages.", action='store_true')
    
    parser.add_argument(      "--very-verbose", dest="very_verbose", help="Print additional progress messages.", action='store_true')
    


    # Note: Any arguments described by KgtkValueOptions.add_arguments(...)
    # need to be included in the arguments to run(...), below.
    KgtkValueOptions.add_arguments(parser)


def run(input_kgtk_file: typing.Optional[Path],
        filter_kgtk_file: Path,
        output_kgtk_file: typing.Optional[Path],
        left_keys: typing.Optional[typing.List[str]],
        right_keys: typing.Optional[typing.List[str]],
        
        # Some common arguments:
        errors_to_stdout: bool = False,
        errors_to_stderr: bool = False,
        error_limit: int = KgtkReader.ERROR_LIMIT_DEFAULT,
        field_separator: str = IfExists.FIELD_SEPARATOR_DEFAULT,
        verbose: bool = False,
        very_verbose: bool = False,

        **kwargs # Whatever KgtkValueOptions wants.
)->int:
    # import modules locally
    from kgtk.exceptions import KGTKException


    if input_kgtk_file is None:
        input_kgtk_file = Path("-")

    # Select where to send error messages, defaulting to stderr.
    # (Not used yet)
    error_file: typing.TextIO = sys.stderr if errors_to_stderr else sys.stdout

    # Build the value parsing option structure.
    value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)

    try:
        ie: IfExists = IfExists(left_file_path=input_kgtk_file,
                                right_file_path=filter_kgtk_file,
                                output_path=output_kgtk_file,
                                left_keys=left_keys,
                                right_keys=right_keys,
                                field_separator=field_separator,
                                invalid_value_action=ValidationAction.PASS,
                                value_options=value_options,
                                error_limit=error_limit,
                                verbose=verbose,
                                very_verbose=very_verbose)
        
        ie.process()

        return 0

    except SystemExit as e:
        raise KGTKException("Exit requested")
    except Exception as e:
        raise KGTKException(str(e))

