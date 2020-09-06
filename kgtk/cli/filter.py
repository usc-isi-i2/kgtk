"""
Filter rows by subject, predicate, object values.
"""
from argparse import Namespace, SUPPRESS
import typing

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles

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
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
    from kgtk.utils.argparsehelpers import optional_bool
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    _expert: bool = parsed_shared_args._expert

    # '$label == "/r/DefinedAs" && $node2=="/c/en/number_zero"'
    parser.add_input_file(positional=True)
    parser.add_output_file(who="The KGTK output file for records that pass the filter.")
    parser.add_output_file(who="The KGTK reject file for records that fail the filter.",
                           dest="reject_file",
                           options=["--reject-file"],
                           metavar="REJECT_FILE",
                           optional=True)

    # parser.add_argument('-dt', "--datatype", action="store", type=str, dest="datatype", help="Datatype of the input file, e.g., tsv or csv.", default="tsv")
    parser.add_argument('-p', '--pattern', action="store", type=str, dest="pattern", help="Pattern to filter on, for instance, \" ; P154 ; \" ", required=True)
    parser.add_argument('--subj', action="store", type=str, dest='subj_col', help="Subject column, default is node1")
    parser.add_argument('--pred', action="store", type=str, dest='pred_col', help="Predicate column, default is label")
    parser.add_argument('--obj', action="store", type=str, dest='obj_col', help="Object column, default is node2")

    parser.add_argument(      "--or", dest="or_pattern", metavar="True|False",
                              help="'Or' the clauses of the pattern. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--invert", dest="invert", metavar="True|False",
                              help="Invert the result of applying the pattern. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--show-version", dest="show_version", type=optional_bool, nargs='?', const=True, default=False,
                              help="Print the version of this program. (default=%(default)s).", metavar="True/False")

    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, expert=_expert)
    KgtkValueOptions.add_arguments(parser, expert=_expert)

def run(input_file: KGTKFiles,
        output_file: KGTKFiles,
        reject_file: KGTKFiles,

        pattern: str,
        subj_col: typing.Optional[str],
        pred_col: typing.Optional[str],
        obj_col: typing.Optional[str],

        or_pattern: bool,
        invert: bool,

        show_version: bool,

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
    
    from kgtk.exceptions import kgtk_exception_auto_handler, KGTKException
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
    from kgtk.io.kgtkwriter import KgtkWriter
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    input_kgtk_file: Path = KGTKArgumentParser.get_input_file(input_file)
    output_kgtk_file: Path = KGTKArgumentParser.get_output_file(output_file)
    reject_kgtk_file: typing.Optional[Path] = KGTKArgumentParser.get_optional_output_file(reject_file, who="KGTK reject file")

    # Select where to send error messages, defaulting to stderr.
    error_file: typing.TextIO = sys.stdout if errors_to_stdout else sys.stderr

    # Build the option structures.
    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs)
    value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)

    UPDATE_VERSION: str = "2020-08-06T17:06:06.829542+00:00#Mu9vz3KEPh+beQeSwZ8qGMKrTJzHWZFfZFXY6UrYXJAnNpPSin+5NvkSfxKLMkyJtGyeavgGAz8+74bup7eYaQ=="
    if show_version or verbose:
        print("kgtk filter version: %s" % UPDATE_VERSION, file=error_file, flush=True)

    # Show the final option structures for debugging and documentation.
    if show_options:
        print("--input-file=%s" % str(input_kgtk_file), file=error_file)
        print("--output-file=%s" % str(output_kgtk_file), file=error_file)
        if reject_kgtk_file is not None:
            print("--reject-file=%s" % str(reject_kgtk_file), file=error_file)
        print("--pattern=%s" % str(pattern), file=error_file)
        if subj_col is not None:
            print("--subj=%s" % str(subj_col), file=error_file)
        if pred_col is not None:
            print("--pred=%s" % str(pred_col), file=error_file)
        if obj_col is not None:
            print("--obj=%s" % str(obj_col), file=error_file)
        print("--or=%s" % str(or_pattern), file=error_file)
        print("--invert=%s" % str(invert), file=error_file)
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

    def single_predicate_filter(kr: KgtkReader,
                                kw: KgtkWriter,
                                rw: typing.Optional[KgtkWriter],
                                pred_idx: int,
                                pred_filter: typing.Set[str],
                                ):
        if verbose:
            print("Applying a single predicate filter", file=error_file, flush=True)

        pred_filter_value: str = list(pred_filter)[0]

        input_line_count: int = 0
        reject_line_count: int = 0
        output_line_count: int = 0

        row: typing.List[str]
        for row in kr:
            input_line_count += 1

            if row[pred_idx] == pred_filter_value:
                kw.write(row)
                output_line_count += 1

            else:
                if rw is not None:
                    rw.write(row)
                reject_line_count += 1

        if verbose:
            print("Read %d rows, rejected %d rows, wrote %d rows." % (input_line_count, reject_line_count, output_line_count))

    def single_predicate_filter_inverted(kr: KgtkReader,
                                         kw: KgtkWriter,
                                         rw: typing.Optional[KgtkWriter],
                                         pred_idx: int,
                                         pred_filter: typing.Set[str],
                                         ):
        if verbose:
            print("Applying a single predicate filter inverted", file=error_file, flush=True)

        pred_filter_value: str = list(pred_filter)[0]

        input_line_count: int = 0
        reject_line_count: int = 0
        output_line_count: int = 0

        row: typing.List[str]
        for row in kr:
            input_line_count += 1

            if row[pred_idx] != pred_filter_value:
                kw.write(row)
                output_line_count += 1

            else:
                if rw is not None:
                    rw.write(row)
                reject_line_count += 1

        if verbose:
            print("Read %d rows, rejected %d rows, wrote %d rows." % (input_line_count, reject_line_count, output_line_count))

    def single_object_filter(kr: KgtkReader,
                             kw: KgtkWriter,
                             rw: typing.Optional[KgtkWriter],
                             obj_idx: int,
                             obj_filter: typing.Set[str],
                             ):
        if verbose:
            print("Applying a single object filter", file=error_file, flush=True)

        obj_filter_value: str = list(obj_filter)[0]

        input_line_count: int = 0
        reject_line_count: int = 0
        output_line_count: int = 0

        row: typing.List[str]
        for row in kr:
            input_line_count += 1

            if row[obj_idx] == obj_filter_value:
                kw.write(row)
                output_line_count += 1

            else:
                if rw is not None:
                    rw.write(row)
                reject_line_count += 1

        if verbose:
            print("Read %d rows, rejected %d rows, wrote %d rows." % (input_line_count, reject_line_count, output_line_count))

    def single_object_filter_inverted(kr: KgtkReader,
                                      kw: KgtkWriter,
                                      rw: typing.Optional[KgtkWriter],
                                      obj_idx: int,
                                      obj_filter: typing.Set[str],
                                      ):
        if verbose:
            print("Applying a single object filter inverted", file=error_file, flush=True)

        obj_filter_value: str = list(obj_filter)[0]

        input_line_count: int = 0
        reject_line_count: int = 0
        output_line_count: int = 0

        row: typing.List[str]
        for row in kr:
            input_line_count += 1

            if row[obj_idx] != obj_filter_value:
                kw.write(row)
                output_line_count += 1

            else:
                if rw is not None:
                    rw.write(row)
                reject_line_count += 1

        if verbose:
            print("Read %d rows, rejected %d rows, wrote %d rows." % (input_line_count, reject_line_count, output_line_count))

    def general_filter(kr: KgtkReader,
                       kw: KgtkWriter,
                       rw: typing.Optional[KgtkWriter],
                       subj_idx: int,
                       subj_filter: typing.Set[str],
                       pred_idx: int,
                       pred_filter: typing.Set[str],
                       obj_idx: int,
                       obj_filter: typing.Set[str]):
        if verbose:
            print("Applying a general filter", file=error_file, flush=True)

        apply_subj_filter: bool = len(subj_filter) > 0
        apply_pred_filter: bool = len(pred_filter) > 0
        apply_obj_filter: bool = len(obj_filter) > 0
        input_line_count: int = 0
        reject_line_count: int = 0
        output_line_count: int = 0
        subj_filter_keep_count: int = 0
        pred_filter_keep_count: int = 0
        obj_filter_keep_count: int = 0
        subj_filter_reject_count: int = 0
        pred_filter_reject_count: int = 0
        obj_filter_reject_count: int = 0

        row: typing.List[str]
        for row in kr:
            input_line_count += 1

            keep: bool = False
            reject: bool = False 
            if apply_subj_filter:
                if row[subj_idx] in subj_filter:
                    keep = True
                    subj_filter_keep_count += 1
                else:
                    reject = True
                    subj_filter_reject_count += 1

            if apply_pred_filter:
                if row[pred_idx] in pred_filter:
                    keep = True
                    pred_filter_keep_count += 1
                else:
                    reject = True
                    pred_filter_reject_count += 1

            if apply_obj_filter:
                if row[obj_idx] in obj_filter:
                    keep = True
                    obj_filter_keep_count += 1
                else:
                    reject = True
                    obj_filter_reject_count += 1

            if (not keep ^ invert) if or_pattern else (reject ^ invert):
                if rw is not None:
                    rw.write(row)
                reject_line_count += 1
            else:
                kw.write(row)
                output_line_count += 1

        if verbose:
            print("Read %d rows, rejected %d rows, wrote %d rows." % (input_line_count, reject_line_count, output_line_count))
            print("Keep counts: subject=%d, predicate=%d, object=%d." % (subj_filter_keep_count, pred_filter_keep_count, obj_filter_keep_count))
            print("Reject counts: subject=%d, predicate=%d, object=%d." % (subj_filter_reject_count, pred_filter_reject_count, obj_filter_reject_count))

    try:

        patterns: typing.List[str] = pattern.split(";")
        if len(patterns) != 3:
            print("Error: The pattern must have three sections separated by semicolons (two semicolons total).", file=error_file, flush=True)
            raise KGTKException("Bad pattern")
            
        subj_filter: typing.Set[str] = prepare_filter(patterns[0])
        pred_filter: typing.Set[str] = prepare_filter(patterns[1])
        obj_filter: typing.Set[str] = prepare_filter(patterns[2])

        if verbose and len(subj_filter) == 0 and len(pred_filter) == 0 and len(obj_filter) == 0:
            print("Warning: the filter is empty.", file=error_file, flush=True)

        if verbose:
            print("Opening the input file: %s" % str(input_kgtk_file), file=error_file, flush=True)
        kr: KgtkReader = KgtkReader.open(input_kgtk_file,
                                         options=reader_options,
                                         value_options = value_options,
                                         error_file=error_file,
                                         verbose=verbose,
                                         very_verbose=very_verbose,
        )

        subj_idx: int = kr.get_node1_column_index(subj_col)
        pred_idx: int = kr.get_label_column_index(pred_col)
        obj_idx: int = kr.get_node2_column_index(obj_col)

        # Complain about a missing column only when it is needed by the pattern.
        trouble: bool = False
        if subj_idx < 0 and len(subj_filter) > 0:
            trouble = True
            print("Error: Cannot find the subject column '%s'." % kr.get_node1_canonical_name(subj_col), file=error_file, flush=True)
        if pred_idx < 0 and len(pred_filter) > 0:
            trouble = True
            print("Error: Cannot find the predicate column '%s'." % kr.get_label_canonical_name(pred_col), file=error_file, flush=True)
        if obj_idx < 0 and len(obj_filter) > 0:
            trouble = True
            print("Error: Cannot find the object column '%s'." % kr.get_node2_canonical_name(obj_col), file=error_file, flush=True)
        if trouble:
            raise KGTKException("Missing columns.")

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

        if len(subj_filter) == 0 and len(pred_filter) == 1 and len(obj_filter) == 0:
            if invert:
                single_predicate_filter_inverted(kr, kw, rw, pred_idx, pred_filter)
            else:
                single_predicate_filter(kr, kw, rw, pred_idx, pred_filter)
        elif len(subj_filter) == 0 and len(pred_filter) == 0 and len(obj_filter) == 1:
            if invert:
                single_object_filter_inverted(kr, kw, rw, obj_idx, obj_filter)
            else:
                single_object_filter(kr, kw, rw, obj_idx, obj_filter)
        else:
            general_filter(kr, kw, rw, subj_idx, subj_filter, pred_idx, pred_filter, obj_idx, obj_filter)


        kw.close()
        if rw is not None:
            rw.close()

        return 0

    except Exception as e:
        kgtk_exception_auto_handler(e)
        return 1
