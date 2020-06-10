"""Add label columns for values in the node1, label, and node2 fields.

The input rows are saved in memory, as well as the value-to-label mapping.
This will impose a limit on the size of the input files that can be processed.

TODO: Optionally save the input rows in an external disk file?

TODO: Optionally reread the input stream insted of saving the input rows?
      With special provision for copying standard input to an external disk file.

TODO: Need KgtkWriterOptions
"""

from argparse import Namespace, SUPPRESS
from pathlib import Path
import sys
import typing

from kgtk.cli_argparse import KGTKArgumentParser
from kgtk.lift.kgtklift import KgtkLift
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
from kgtk.io.kgtkwriter import KgtkWriter
from kgtk.utils.argparsehelpers import optional_bool
from kgtk.value.kgtkvalueoptions import KgtkValueOptions

def parser():
    return {
        'help': 'Lift labels from a KGTK file.',
        'description': 'Lift labels for a KGTK file. For each of the items in the (node1, label, node2) columns, look for matching label records. ' +
        'If found, lift the label values into additional columns in the current record. ' +
        'Label records are reoved from the output. ' +
        '\n\nAdditional options are shown in expert help.\nkgtk --expert lift --help'
    }


def add_arguments_extended(parser: KGTKArgumentParser, parsed_shared_args: Namespace):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """

    _expert: bool = parsed_shared_args._expert

    # This helper function makes it easy to suppress options from
    # The help message.  The options are still there, and initialize
    # what they need to initialize.
    def h(msg: str)->str:
        if _expert:
            return msg
        else:
            return SUPPRESS

    parser.add_argument(      "input_kgtk_file", nargs="?", help="The KGTK file to lift. May be omitted or '-' for stdin.", type=Path, default="-")

    parser.add_argument(      "--label-file", dest="label_kgtk_file", help="A KGTK file with label records (default=%(default)s).", type=Path, default=None)

    parser.add_argument(      "--node1-name", dest="node1_column_name",
                              help=h("The name of the node1 column. (default=node1 or alias)."), default=None)

    parser.add_argument(      "--label-name", dest="label_column_name",
                              help=h("The name of the label column. (default=label)."), default=None)

    parser.add_argument(      "--node2-name", dest="node2_column_name",
                              help=h("The name of the node2 column. (default=node2 or alias)."), default=None)

    parser.add_argument(      "--label-value", dest="label_column_value", help=h("The value in the label column. (default=%(default)s)."), default="label")
    parser.add_argument(      "--lift-suffix", dest="lifted_column_suffix",
                              help=h("The suffix used for newly created columns. (default=%(default)s)."), default=";label")

    parser.add_argument(      "--columns-to-lift", dest="lift_column_names", help=h("The columns to lift. (default=[node1, label, node2])."), nargs='*')

    parser.add_argument("-o", "--output-file", dest="output_kgtk_file", help="The KGTK file to write (default=%(default)s).", type=Path, default="-")

    parser.add_argument(      "--remove-label-records", dest="remove_label_records",
                              help=h("If true, remove label records from the output. (default=%(default)s)."),
                              type=optional_bool, nargs='?', const=True, default=True)

    parser.add_argument(      "--sort-lifted-labels", dest="sort_lifted_labels",
                              help=h("If true, sort lifted labels with lists. (default=%(default)s)."),
                              type=optional_bool, nargs='?', const=True, default=True)

    parser.add_argument(      "--suppress-duplicate-labels", dest="suppress_duplicate_labels",
                              help=h("If true, suppress duplicate values in lists in lifted labels (implies sorting). (default=%(default)s)."),
                              type=optional_bool, nargs='?', const=True, default=True)

    parser.add_argument(      "--suppress-empty-columns", dest="suppress_empty_columns",
                              help="If true, do not create new columns that would be empty. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--ok-if-no-labels", dest="ok_if_no_labels",
                              help="If true, do not abort if no labels were found. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--input-file-is-presorted", dest="input_is_presorted",
                              help="If true, the input file is presorted on the column for which values are to be lifted. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--label-file-is-presorted", dest="labels_are_presorted",
                              help="If true, the label file is presorted on the node1 column. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    KgtkReader.add_debug_arguments(parser, expert=_expert)
    # TODO: seperate reader_options for the label file.
    KgtkReaderOptions.add_arguments(parser, mode_options=True, expert=_expert)
    KgtkValueOptions.add_arguments(parser, expert=_expert)

def run(input_kgtk_file: Path,
        label_kgtk_file: typing.Optional[Path],
        output_kgtk_file: Path,
        node1_column_name: typing.Optional[str],
        label_column_name: typing.Optional[str],
        node2_column_name: typing.Optional[str],
        label_column_value: str,
        lifted_column_suffix: str,
        lift_column_names: typing.List[str],
        remove_label_records: bool = False,
        sort_lifted_labels: bool = True,
        suppress_duplicate_labels: bool = True,
        suppress_empty_columns: bool = False,
        ok_if_no_labels: bool = False,
        input_is_presorted: bool = False,
        labels_are_presorted: bool = False,

        errors_to_stdout: bool = False,
        errors_to_stderr: bool = True,
        show_options: bool = False,
        verbose: bool = False,
        very_verbose: bool = False,

        **kwargs # Whatever KgtkFileOptions and KgtkValueOptions want.
)->int:
    # import modules locally
    from kgtk.exceptions import KGTKException

    # Select where to send error messages, defaulting to stderr.
    error_file: typing.TextIO = sys.stdout if errors_to_stdout else sys.stderr

    # Build the option structures.
    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs)
    value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)

    # Show the final option structures for debugging and documentation.
    if show_options:
        print("input: %s" % str(input_kgtk_file), file=error_file, flush=True)
        if label_kgtk_file is not None:
            print("-label-file=%s" % label_kgtk_file, file=error_file, flush=True)
        if node1_column_name is not None:
            print("--node1-name=%s" % node1_column_name, file=error_file, flush=True)
        if label_column_name is not None:
            print("--label-name=%s" % label_column_name, file=error_file, flush=True)
        if node2_column_name is not None:
            print("--node2-name=%s" % node2_column_name, file=error_file, flush=True)
        print("--label-value=%s" % label_column_value, file=error_file, flush=True)
        print("--lift-suffix=%s" % lifted_column_suffix, file=error_file, flush=True)
        if lift_column_names is not None and len(lift_column_names) > 0:
            print("--columns-to-lift %s" % " ".join(lift_column_names), file=error_file, flush=True)
        print("--output-file=%s" % str(output_kgtk_file), file=error_file, flush=True)
        print("--remove-label-records=%s" % str(remove_label_records))
        print("--sort-lifted-labels=%s" % str(sort_lifted_labels))
        print("--suppress-duplicate-labels=%s" % str(suppress_duplicate_labels))
        print("--suppress-empty-columns=%s" % str(suppress_empty_columns))
        print("--ok-if-no-labels=%s" % str(ok_if_no_labels))
        print("--input-file-is-presorted=%s" % str(input_is_presorted))
        print("--label-file-is-presorted=%s" % str(labels_are_presorted))
        reader_options.show(out=error_file)
        value_options.show(out=error_file)
        print("=======", file=error_file, flush=True)

    try:
        kl: KgtkLift = KgtkLift(
            input_file_path=input_kgtk_file,
            label_file_path=label_kgtk_file,
            node1_column_name=node1_column_name,
            label_column_name=label_column_name,
            node2_column_name=node2_column_name,
            label_column_value=label_column_value,
            lifted_column_suffix=lifted_column_suffix,
            lift_column_names=lift_column_names,
            output_file_path=output_kgtk_file,
            remove_label_records=remove_label_records,
            sort_lifted_labels=sort_lifted_labels,
            suppress_duplicate_labels=suppress_duplicate_labels,
            suppress_empty_columns=suppress_empty_columns,
            ok_if_no_labels=ok_if_no_labels,
            input_is_presorted=input_is_presorted,
            labels_are_presorted=labels_are_presorted,
            reader_options=reader_options,
            value_options=value_options,
            error_file=error_file,
            verbose=verbose,
            very_verbose=very_verbose,
        )
        
        kl.process()

        return 0

    except SystemExit as e:
        raise KGTKException("Exit requested")
    except Exception as e:
        raise KGTKException(str(e))

