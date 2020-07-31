"""
Normalize KGTK edge file by removing additional columns that match the "lift" pattern..
"""
from argparse import Namespace, SUPPRESS
from pathlib import Path
import sys
import typing

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles
from kgtk.kgtkformat import KgtkFormat
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions, KgtkReaderMode
from kgtk.io.kgtkwriter import KgtkWriter
from kgtk.lift.kgtklift import KgtkLift
from kgtk.utils.argparsehelpers import optional_bool
from kgtk.value.kgtkvalue import KgtkValue
from kgtk.value.kgtkvalueoptions import KgtkValueOptions

def parser():
    return {
        'help': 'Normalize a KGTK edge file by reversing the "lift" pattern.',
        'description': 'Normalize a KGTK edge file by removing columns that match a "lift" pattern.'
    }


def add_arguments_extended(parser: KGTKArgumentParser, parsed_shared_args: Namespace):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """

    _expert: bool = parsed_shared_args._expert

    parser.add_input_file(positional=True)
    parser.add_output_file()
    parser.add_output_file(who="Label file",
                           dest="label_file",
                           options=["--label-file"],
                           metavar="LABEL_FILE",
                           optional=True)


    parser.add_argument(      "--base-columns", dest="base_columns",
                              help="The columns for which matching labels are to be lifted. " +
                              "The default is [node1, label, node2] or their aliases.", nargs='*')

    parser.add_argument(      "--columns-to-remove", action="store", type=str, dest="columns_to_remove", nargs='+',
                              help="Columns to lower and remove as a space-separated list. (default=all columns with the lift pattern)")

    parser.add_argument(      "--label-value", action="store", type=str, dest="label_value",
                              help="The label value to use for lowered values. (default=%(default)s)",
                              default=KgtkLift.DEFAULT_LABEL_SELECT_COLUMN_VALUE)

    parser.add_argument(      "--lift-suffix", dest="lift_suffix",
                              help="The suffix used for lifts. (default=%(default)s).",
                              default=KgtkLift.DEFAULT_OUTPUT_LIFTED_COLUMN_SUFFIX)

    parser.add_argument(      "--deduplicate-labels", dest="deduplicate_labels",
                              help="When True, deduplicate the labels. " +
                              "Note: When new labels are written to a new label file, only theose labels labels will be deduplicated. " +
                              "When labels are written to the output file, existing labels in the input file are deduplicated as well. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=True, metavar="True|False")

    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, default_mode=KgtkReaderMode.EDGE, expert=_expert)
    KgtkValueOptions.add_arguments(parser, expert=_expert)

def run(input_file: KGTKFiles,
        output_file: KGTKFiles,
        label_file: KGTKFiles,

        base_columns: typing.Optional[typing.List[str]] = None,
        columns_to_remove: typing.Optional[typing.List[str]] = None,
        label_value: str = KgtkLift.DEFAULT_LABEL_SELECT_COLUMN_VALUE,
        lift_suffix: str = KgtkLift.DEFAULT_OUTPUT_LIFTED_COLUMN_SUFFIX,
        deduplicate_labels: bool = True,

        errors_to_stdout: bool = False,
        errors_to_stderr: bool = True,
        show_options: bool = False,
        verbose: bool = False,
        very_verbose: bool = False,

        **kwargs # Whatever KgtkFileOptions and KgtkValueOptions want.
)->int:
    # import modules locally
    from kgtk.exceptions import kgtk_exception_auto_handler, KGTKException

    input_kgtk_file: Path = KGTKArgumentParser.get_input_file(input_file)
    output_kgtk_file: Path = KGTKArgumentParser.get_output_file(output_file)
    label_kgtk_file: typing.Optional[Path] = KGTKArgumentParser.get_optional_output_file(label_file, who="Label file")

    # Select where to send error messages, defaulting to stderr.
    error_file: typing.TextIO = sys.stdout if errors_to_stdout else sys.stderr

    # Build the option structures.
    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs)
    value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)

    # Show the final option structures for debugging and documentation.
    if show_options:
        print("--input-file=%s" % str(input_kgtk_file), file=error_file)
        print("--output-file=%s" % str(output_kgtk_file), file=error_file)
        if label_kgtk_file is not None:
            print("--label-file=%s" % str(label_kgtk_file), file=error_file)

        if base_columns is not None:
            print("--base-columns=%s" % " ".join(base_columns), file=error_file)
        if columns_to_remove is not None:
            print("--columns-to-lower=%s" % " ".join(columns_to_remove), file=error_file)
        print("--label-value=%s" % label_value, file=error_file)
        print("--lift-suffix=%s" % lift_suffix, file=error_file)
        print("--deduplicate-labels=%s" % deduplicate_labels, file=error_file)

        reader_options.show(out=error_file)
        value_options.show(out=error_file)
        print("=======", file=error_file, flush=True)


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

        # Map the index of a column being removed to the index of the base column that supplies its node1 value.
        lower_map: typing.MutableMapping[int, int] = dict()

        # These columns will never be removed:
        key_column_idxs: typing.Set[int] = set((kr.node1_column_idx,
                                                kr.label_column_idx,
                                                kr.node2_column_idx,
                                                kr.id_column_idx))
        key_column_idxs.discard(-1)
        key_column_names: typing.Set[str] = set((kr.column_names[idx] for idx in key_column_idxs))

        base_name: str
        column_name: str
        idx: int
        # There are three option patterns.

        if columns_to_remove is not None and len(columns_to_remove) > 0 and base_columns is not None and len(base_columns) > 0:
            # Pattern 1: len(columns_to_remove) > 0 and len(base_columns) == len(columns_to_remove)
            # column_names and base_columns are paired.
            if len(columns_to_remove) != len(base_columns):
                raise KGTKException("There are %d columns to remove but only %d base columns." % (len(columns_to_remove), len(base_columns)))
        
            for idx, column_name in enumerate(columns_to_remove):
                base_name = base_columns[idx]
                if column_name not in kr.column_names:
                    raise KGTKException("Column %s is an unknown column, cannot remove it." % repr(column_name))

                if column_name in key_column_names:
                    raise KGTKException("Column %s is a key column, cannot remove it." % repr(column_name))

                if base_name not in kr.column_names:
                    raise KGTKException("For column name %s, base name %s is unknown" % (repr(column_name), repr(base_name)))

                lower_map[kr.column_name_map[column_name]] = kr.column_name_map[base_name]

        elif columns_to_remove is not None and len(columns_to_remove) > 0 and (base_columns is None or len(base_columns) == 0):
            # Pattern 2: len(columns_to_remove) > 0 and len(base_columns) == 0
            # Each column name is stripped of the lift suffix to determine the base name.
            if len(lift_suffix) == 0:
                raise KGTKException("The --lift-suffix must not be empty.")

            for idx, column_name in enumerate(columns_to_remove):
                if column_name not in kr.column_names:
                    raise KGTKException("Column %s is an unknown column, cannot remove it." % repr(column_name))

                if column_name in key_column_names:
                    raise KGTKException("Column %s is a key column, cannot remove it." % repr(column_name))

                if not column_name.endswith(lift_suffix):
                   raise KGTKException("Unable to parse column name %s." % repr(column_name))

                base_name = column_name[:-len(lift_suffix)]

                if base_name not in kr.column_names:
                    raise KGTKException("For column name %s, base name %s is not known" % (repr(column_name), repr(base_name)))

                lower_map[kr.column_name_map[column_name]] = kr.column_name_map[base_name]

        elif columns_to_remove is None or len(columns_to_remove) == 0:
            # Pattern 3: len(columns_to_remove) == 0.
            if len(lift_suffix) == 0:
                raise KGTKException("The --lift-suffix must not be empty.")

            if base_columns is None or len(base_columns) == 0:
                # The base name list wasn't supplied.  Use [node1, label, node2, id]
                base_columns = list(key_column_names)

            for idx, column_name in enumerate(kr.column_names):
                # Skip the node1, label, node12, and id columns
                if idx in key_column_idxs:
                    continue

                # Does this column match a lifting pattern?
                for base_name in base_columns:
                    if len(base_name) == 0:
                        continue
                    if column_name == base_name + lift_suffix:
                        lower_map[idx] = kr.column_name_map[base_name]

        if len(lower_map) == 0:
            raise KGTKException("There are no columns to lower.")

        if verbose:
            print("The following columns will be lowered", file=error_file, flush=True)
            for idx in sorted(lower_map.keys()):
                column_name = kr.column_names[idx]
                base_name = kr.column_names[lower_map[idx]]
                print(" %s from %s" % (column_name, base_name), file=error_file, flush=True)

        output_column_names: typing.List[str] = list()
        for idx, column_name in enumerate(kr.column_names):
            if idx not in lower_map:
                output_column_names.append(column_name)
        if verbose:
            print("The output columns are: %s" % " ".join(output_column_names), file=error_file, flush=True)

        if verbose:
            print("Opening the output file: %s" % str(output_kgtk_file), file=error_file, flush=True)
        kw: KgtkWriter = KgtkWriter.open(output_column_names,
                                         output_kgtk_file,
                                         mode=KgtkWriter.Mode.EDGE,
                                         require_all_columns = False, # Simplifies writing the labels
                                         verbose=verbose,
                                         very_verbose=very_verbose)
        shuffle_list: typing.List[int] = kw.build_shuffle_list(kr.column_names)

        lkw: typing.Optional[KgtkWriter] = None
        if label_kgtk_file is not None:
            if verbose:
                print("Opening the label output file: %s" % str(label_kgtk_file), file=error_file, flush=True)

            label_column_names = [ KgtkFormat.NODE1, KgtkFormat.LABEL, KgtkFormat.NODE2 ]                
            lkw = KgtkWriter.open(label_column_names,
                                  label_kgtk_file,
                                  mode=KgtkWriter.Mode.EDGE,
                                  verbose=verbose,
                                  very_verbose=very_verbose)
                      

        # Optionally deduplicate the labels
        #  set(node1_value + KgtkFormat.SEPARATOR + node2_value)
        label_set: typing.Set[str] = set()
        label_key: str

        # If labels will be written to the output file and deduplication is enabled:
        check_existing_labels: bool = \
            deduplicate_labels and \
            lkw is None and \
            kr.node1_column_idx >= 0 and \
            kr.label_column_idx >= 0 and \
            kr.node2_column_idx >= 0

        input_line_count: int = 0
        output_line_count: int = 0
        label_line_count: int = 0
        row: typing.List[str]
        for row in kr:
            input_line_count += 1

            if check_existing_labels and row[kr.label_column_idx] == label_value:
                label_key = row[kr.node1_column_idx] + KgtkFormat.COLUMN_SEPARATOR + row[kr.node2_column_idx]
                if label_key in label_set:
                    continue
                else:
                    label_set.add(label_key)

            kw.write(row, shuffle_list=shuffle_list)
            output_line_count += 1

            column_idx: int
            for column_idx in lower_map.keys():
                node1_value: str = row[lower_map[column_idx]]
                if len(node1_value) == 0:
                    continue # TODO: raise an exception

                item: str = row[column_idx]
                if len(item) == 0:
                    continue # Ignore empty node2 values.

                # Ths item might be a KGTK list.  Let's split it, because
                # lists aren't allow in the node2 values we'll generate.
                node2_value: str
                for node2_value in KgtkValue.split_list(item):
                    if len(node2_value) == 0:
                        continue # Ignore empty node2 values.

                    if deduplicate_labels:
                        label_key = node1_value + KgtkFormat.COLUMN_SEPARATOR + node2_value
                        if label_key in label_set:
                            continue
                        else:
                            label_set.add(label_key)

                    output_map: typing.Mapping[str, str] = {
                        KgtkFormat.NODE1: node1_value,
                        KgtkFormat.LABEL: label_value,
                        KgtkFormat.NODE2: node2_value,
                    }
                    if lkw is None:
                        kw.writemap(output_map)
                        label_line_count += 1
                        output_line_count += 1
                    else:
                        lkw.writemap(output_map)
                        label_line_count += 1

        if verbose:
            print("Read %d rows, wrote %d rows with %d labels." % (input_line_count, output_line_count, label_line_count), file=error_file, flush=True)

        kw.close()
        if lkw is not None:
            lkw.close()

        return 0

    except Exception as e:
        kgtk_exception_auto_handler(e)
        return 1
