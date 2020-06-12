"""
Filter rows by subject, predicate, object values.
"""
from argparse import Namespace, SUPPRESS
from pathlib import Path
import sys
import typing

from kgtk.cli_argparse import KGTKArgumentParser
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
from kgtk.io.kgtkwriter import KgtkWriter
from kgtk.value.kgtkvalueoptions import KgtkValueOptions

def parser():
    return {
        'help': 'Filter rows by subject, predicate, object values.',
        'description': 'Filter KGTK file based on values in the node1 (subject), ' +
        'label (predicate), and node2 (object) fields.'
    }


def add_arguments_extended(parser: KGTKArgumentParser, parsed_shared_args: Namespace):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """

    _expert: bool = parsed_shared_args._expert

    # '$label == "/r/DefinedAs" && $node2=="/c/en/number_zero"'
    parser.add_argument(      "input_kgtk_file", nargs="?", help="The KGTK file to filter. May be omitted or '-' for stdin.", type=Path, default="-")
    parser.add_argument("-o", "--output-file", dest="output_kgtk_file", help="The KGTK file to write records that pass the filter (default=%(default)s).",
                        type=Path, default="-")
    parser.add_argument(      "--reject-file", dest="reject_kgtk_file", help="The KGTK file to write records that fail the filter (default=%(default)s).",
                              type=Path, default=None)

    # parser.add_argument('-dt', "--datatype", action="store", type=str, dest="datatype", help="Datatype of the input file, e.g., tsv or csv.", default="tsv")
    parser.add_argument('-p', '--pattern', action="store", type=str, dest="pattern", help="Pattern to filter on, for instance, \" ; P154 ; \" ", required=True)
    parser.add_argument('--subj', action="store", type=str, dest='subj_col', help="Subject column, default is node1")
    parser.add_argument('--pred', action="store", type=str, dest='pred_col', help="Predicate column, default is label")
    parser.add_argument('--obj', action="store", type=str, dest='obj_col', help="Object column, default is node2")

    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, expert=_expert)
    KgtkValueOptions.add_arguments(parser, expert=_expert)

def run(input_kgtk_file: Path,
        output_kgtk_file: Path,
        reject_kgtk_file: typing.Optional[Path],

        pattern: str,
        subj_col: typing.Optional[str],
        pred_col: typing.Optional[str],
        obj_col: typing.Optional[str],

        errors_to_stdout: bool = False,
        errors_to_stderr: bool = True,
        show_options: bool = False,
        verbose: bool = False,
        very_verbose: bool = False,

        **kwargs # Whatever KgtkFileOptions and KgtkValueOptions want.
)->int:
    # import modules locally
    from kgtk.exceptions import kgtk_exception_auto_handler

    # Select where to send error messages, defaulting to stderr.
    error_file: typing.TextIO = sys.stdout if errors_to_stdout else sys.stderr

    # Build the option structures.
    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs)
    value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)

    # Show the final option structures for debugging and documentation.
    if show_options:
        print("input: %s" % str(input_kgtk_file), file=error_file)
        print("--output-file=%s" % str(output_kgtk_file), file=error_file)
        if reject_kgtk_file is not None:
            print("--reject-file=%s" % str(reject_kgtk_file), file=error_file)
        print("--pattern=%s" % str(pattern), file=error_file)
        if subj_col is not None:
            print("--subj_col=%s" % str(subj_col), file=error_file)
        if pred_col is not None:
            print("--pred_col=%s" % str(pred_col), file=error_file)
        if obj_col is not None:
            print("--obj_col=%s" % str(obj_col), file=error_file)
        reader_options.show(out=error_file)
        value_options.show(out=error_file)
        print("=======", file=error_file, flush=True)

    def prepare_filter(pattern: str)->typing.Set[str]:
        filt: typing.Set[str] = set()
        pattern = pattern.strip()
        if len(pattern) == 0:
            return filt

        target: str
        for target in pattern.split(","):
            target=target.strip()
            if len(target) > 0:
                filt.add(target)

        return filt

    try:
        if verbose:
            print("Opening the input file: %s" % str(input_kgtk_file), file=error_file, flush=True)
        kr: KgtkReader = KgtkReader.open(input_kgtk_file,
                                         options=reader_options,
                                         value_options = value_options,
                                         error_file=error_file,
                                         verbose=verbose,
                                         very_verbose=very_verbose,
        )

        patterns: typing.List[str] = pattern.split(";")
        if len(patterns) != 3:
            print("The pattern must have three sections separated by semicolons.", file=error_file, flush=True)
            return 1

        subj_filter: typing.Set[str] = prepare_filter(patterns[0])
        pred_filter: typing.Set[str] = prepare_filter(patterns[1])
        obj_filter: typing.Set[str] = prepare_filter(patterns[2])
        apply_subj_filter: bool = len(subj_filter) > 0
        apply_pred_filter: bool = len(pred_filter) > 0
        apply_obj_filter: bool = len(obj_filter) > 0
        subj_idx: int = kr.get_node1_column_index(subj_col)
        pred_idx: int = kr.get_label_column_index(pred_col)
        obj_idx: int = kr.get_node2_column_index(obj_col)

        if verbose and not (apply_subj_filter or apply_pred_filter or apply_obj_filter):
            print("Warning: the filter is empty.", file=error_file, flush=True)

        trouble: bool = False
        if subj_idx < 0 and len(subj_filter) > 0:
            trouble = True
            print("Cannot find the subject column '%s'." % kr.get_node1_canonical_name(subj_col))
        if pred_idx < 0 and len(pred_filter) > 0:
            trouble = True
            print("Cannot find the predicate column '%s'." % kr.get_label_canonical_name(pred_col))
        if obj_idx < 0 and len(obj_filter) > 0:
            trouble = True
            print("Cannot find the object column '%s'." % kr.get_node2_canonical_name(obj_col))
        if trouble:
            return 1

        if verbose:
            print("Opening the output file: %s" % str(output_kgtk_file), file=error_file, flush=True)
        kw: KgtkWriter = KgtkWriter.open(kr.column_names,
                                         output_kgtk_file,
                                         mode=KgtkWriter.Mode[kr.mode.name],
                                         verbose=verbose,
                                         very_verbose=very_verbose)

        rw: typing.Optional[KgtkWriter] = None
        if reject_kgtk_file is not None:
            if verbose:
                print("Opening the reject file: %s" % str(reject_kgtk_file), file=error_file, flush=True)
            rw = KgtkWriter.open(kr.column_names,
                                 reject_kgtk_file,
                                 mode=KgtkWriter.Mode[kr.mode.name],
                                 verbose=verbose,
                                 very_verbose=very_verbose)

        input_line_count: int = 0
        reject_line_count: int = 0
        output_line_count: int = 0
        subj_filter_reject_count: int = 0
        pred_filter_reject_count: int = 0
        obj_filter_reject_count: int = 0

        row: typing.List[str]
        for row in kr:
            input_line_count += 1

            reject: bool = False
            if apply_subj_filter and row[subj_idx] not in subj_filter:
                subj_filter_reject_count += 1
                reject = True
            if apply_pred_filter and row[pred_idx] not in pred_filter:
                pred_filter_reject_count += 1
                reject = True
            if apply_obj_filter and row[obj_idx] not in obj_filter:
                obj_filter_reject_count += 1
                reject = True
            if reject:
                if rw is not None:
                    rw.write(row)
                reject_line_count += 1
            else:
                kw.write(row)
                output_line_count += 1

        if verbose:
            print("Read %d rows, rejected %d rows, wrote %d rows." % (input_line_count, reject_line_count, output_line_count))
            print("Reject counts: subject=%d, predicate=%d, object=%d." % (subj_filter_reject_count, pred_filter_reject_count, obj_filter_reject_count))

        kw.close()
        if rw is not None:
            rw.close()

        return 0

    except Exception as e:
        kgtk_exception_auto_handler(e)
        return 1
