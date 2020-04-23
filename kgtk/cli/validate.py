"""
Validate a KGTK file, producing error messages.
"""

from pathlib import Path
import sys
import typing

from kgtk.join.enumnameaction import EnumNameAction
from kgtk.join.kgtkformat import KgtkFormat
from kgtk.join.kgtkreader import KgtkReader, KgtkReaderErrorAction

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
    parser.add_argument(      "kgtk_file", nargs="?", help="The KGTK file to read", type=Path)
    
    parser.add_argument(      "--allow-comment-lines", dest="ignore_comment_lines",
                              help="When specified, do not ignore comment lines.", action='store_false')

    parser.add_argument(      "--allow-empty-lines", dest="ignore_empty_lines",
                              help="When specified, do not ignore empty lines.", action='store_false')

    parser.add_argument(      "--allow-long-lines", dest="ignore_long_lines",
                              help="When specified, do not ignore lines with extra columns.", action='store_false')

    parser.add_argument(      "--allow-short-lines", dest="ignore_short_lines",
                              help="When specified, do not ignore lines with missing columns.", action='store_false')
    
    parser.add_argument(      "--allow-whitespace-lines", dest="ignore_whitespace_lines",
                              help="When specified, do not ignore whitespace lines.", action='store_false')

    parser.add_argument(      "--column-separator", dest="column_separator",
                              help="Column separator.", type=str, default=KgtkReader.COLUMN_SEPARATOR)

    parser.add_argument(      "--compression-type", dest="compression_type", help="Specify the compression type.")
    
    parser.add_argument(      "--error-action", dest="error_action",
                              help="The action to take for error input lines",
                              type=KgtkReaderErrorAction, action=EnumNameAction)
    
    parser.add_argument(      "--error-limit", dest="error_limit",
                              help="The maximum number of errors to report before failing", type=int, default=KgtkReader.ERROR_LIMIT_DEFAULT)

    parser.add_argument(      "--fill-short-lines", dest="fill_short_lines",
                              help="Fill missing trailing columns in short lines with empty values.", action='store_true')

    parser.add_argument(      "--force-column-names", dest="force_column_names", help="Force the column names.", nargs='*')
    
    parser.add_argument(      "--gzip-in-parallel", dest="gzip_in_parallel", help="Execute gzip in parallel.", action='store_true')
        
    parser.add_argument(      "--gzip-queue-size", dest="gzip_queue_size",
                              help="Queue size for parallel gzip.", type=int, default=KgtkReader.GZIP_QUEUE_SIZE_DEFAULT)
    
    parser.add_argument(      "--mode", dest="mode",
                              help="Determine the KGTK file mode.", type=KgtkReader.Mode, action=EnumNameAction, default=KgtkReader.Mode.AUTO)

    parser.add_argument(      "--skip-first-record", dest="skip_first_record", help="Skip the first record when forcing column names.", action='store_true')

    parser.add_argument(      "--truncate-long-lines", dest="truncate_long_lines",
                              help="Remove excess trailing columns in long lines.", action='store_true')

    parser.add_argument("-v", "--verbose", dest="verbose", help="Print additional progress messages.", action='store_true')

    parser.add_argument(      "--very-verbose", dest="very_verbose", help="Print additional progress messages.", action='store_true')

def run(kgtk_file: typing.Optional[Path],
        force_column_names: typing.Optional[typing.List[str]] = None,
        skip_first_record: bool = False,
        fill_short_lines: bool = False,
        truncate_long_lines: bool = False,
        error_action: KgtkReaderErrorAction = KgtkReaderErrorAction.STDOUT,
        error_limit: int = KgtkReader.ERROR_LIMIT_DEFAULT,
        ignore_empty_lines: bool = True,
        ignore_comment_lines: bool = True,
        ignore_whitespace_lines: bool = True,
        ignore_blank_node1_lines: bool = True,
        ignore_blank_node2_lines: bool = True,
        ignore_blank_id_lines: bool = True,
        ignore_short_lines: bool = True,
        ignore_long_lines: bool = True,
        compression_type: typing.Optional[str] = None,
        gzip_in_parallel: bool = False,
        gzip_queue_size: int = KgtkReader.GZIP_QUEUE_SIZE_DEFAULT,
        column_separator: str = KgtkFormat.COLUMN_SEPARATOR,
        mode: KgtkReader.Mode = KgtkReader.Mode.AUTO,
        verbose: bool = False,
        very_verbose: bool = False,
)->int:
    # import modules locally
    from kgtk.exceptions import KGTKException

    try:
        if verbose:
            if kgtk_file is not None:
                print("Validating '%s'" % str(kgtk_file))
            else:
                print ("Validating from stdin")
                
        kr: KgtkReader = KgtkReader.open(kgtk_file,
                                         force_column_names=force_column_names,
                                         skip_first_record=skip_first_record,
                                         fill_short_lines=fill_short_lines,
                                         truncate_long_lines=truncate_long_lines,
                                         error_action=error_action,
                                         error_limit=error_limit,
                                         ignore_comment_lines=ignore_comment_lines,
                                         ignore_whitespace_lines=ignore_whitespace_lines,
                                         ignore_blank_node1_lines=ignore_blank_node1_lines,
                                         ignore_blank_node2_lines=ignore_blank_node2_lines,
                                         ignore_blank_id_lines=ignore_blank_id_lines,
                                         ignore_short_lines=ignore_short_lines,
                                         ignore_long_lines=ignore_long_lines,
                                         compression_type=compression_type,
                                         gzip_in_parallel=gzip_in_parallel,
                                         gzip_queue_size=gzip_queue_size,
                                         column_separator=column_separator,
                                         mode=mode,
                                         verbose=verbose, very_verbose=very_verbose)
        
        line_count: int = 0
        line: typing.List[str]
        for line in kr:
            line_count += 1
        if verbose:
            print("Validated %d data lines" % line_count)
        return 0

    except Exception as e:
        raise KGTKException(e)

