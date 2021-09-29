"""Add label columns for values in the node1, label, and node2 fields.

The input rows are saved in memory, as well as the value-to-label mapping.
This will impose a limit on the size of the input files that can be processed.

TODO: Optionally save the input rows in an external disk file?

TODO: Optionally reread the input stream insted of saving the input rows?
      With special provision for copying standard input to an external disk file.

TODO: Need KgtkWriterOptions
"""

from argparse import Namespace, SUPPRESS
import typing

from kgtk.cli_argparse import KGTKArgumentParser, KGTKFiles

LIFT_COMMAND: str = 'lift'
ADD_LABELS_COMMAND: str = 'add-labels'

def parser():
    return {
        'aliases': [ ADD_LABELS_COMMAND ],
        'help': 'Lift labels from a KGTK file.',
        'description': 'Lift labels for a KGTK file. ' +
        'If called as "kgtk lift", for each of the items in the (node1, label, node2) columns, look for matching label records. ' +
        'If called as "kgtk add-labels", look for matching label records for all input columns. ' +
        'If found, lift the label values into additional columns in the current record. ' +
        'Label records are removed from the output unless --remove-label-records=False. ' +
        '\n\nAdditional options are shown in expert help.\nkgtk --expert lift --help'
    }


def add_arguments_extended(parser: KGTKArgumentParser, parsed_shared_args: Namespace):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """
    from kgtk.exceptions import KGTKException
    from kgtk.lift.kgtklift import KgtkLift
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
    from kgtk.utils.argparsehelpers import optional_bool
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    _expert: bool = parsed_shared_args._expert
    _command: str = parsed_shared_args._command

    # This helper function makes it easy to suppress options from
    # The help message.  The options are still there, and initialize
    # what they need to initialize.
    def h(msg: str)->str:
        if _expert:
            return msg
        else:
            return SUPPRESS

    parser.add_input_file(positional=True)
    parser.add_output_file()

    parser.add_input_file(who="A KGTK file with label records",
                          dest="label_file",
                          options=["--label-file"],
                          optional=True)

    parser.add_output_file(who="A KGTK output file that will contain only unmodified rows." +
                           " This file will have the same columns as the input file.",
                           dest="unmodified_row_file",
                           options=["--unmodified-row-output-file"],
                           metavar="UNMODIFIED_ROW_OUTPUT_FILE",
                           optional=True)

    parser.add_output_file(who="A KGTK output file that will contain matched label edges." +
                           " This file will have the same columns as the source of the labels, either the input file or the label file.",
                           dest="matched_label_file",
                           options=["--matched-label-output-file"],
                           metavar="MATCHED_LABEL_OUTPUT_FILE",
                           optional=True)

    parser.add_output_file(who="A KGTK output file that will contain unmatched label edges." +
                           " This file will have the same columns as the source of the labels, either the input file or the label file.",
                           dest="unmatched_label_file",
                           options=["--unmatched-label-output-file"],
                           metavar="UNMATCHED_LABEL_OUTPUT_FILE",
                           optional=True)

    suppress_empty_columns_default: bool
    prefilter_labels_default: bool
    use_label_enver_default: bool
    lift_all_columns_default: bool
    require_label_file_default: bool
    force_input_mode_none_default: bool
    if _command == LIFT_COMMAND:
        parser.add_argument(      "--columns-to-lift", dest="input_lifting_column_names",
                                  help=h("The columns for which matching labels are to be lifted. " +
                                         "The default is [node1, label, node2] or their aliases."), nargs='*')

        parser.add_argument(      "--columns-to-write", dest="output_lifted_column_names",
                                  help="The columns into which to store the lifted values. " +
                                  "The default is [node1;label, label;label, node2;label] or their aliases.", nargs='*')

        suppress_empty_columns_default = False
        prefilter_labels_default = False
        use_label_envar_default = False
        lift_all_columns_default = False
        require_label_file_default = False
        force_input_mode_none_default = False
       
    elif _command == ADD_LABELS_COMMAND:
        parser.add_argument(      "--columns-to-lift", dest="input_lifting_column_names",
                                  help=h("The columns for which matching labels are to be lifted. " +
                                         "The default is all columns except id or its alias."), nargs='*')

        parser.add_argument(      "--columns-to-write", dest="output_lifted_column_names",
                                  help="The columns into which to store the lifted values. " +
                                  "The default is [node1;label, label;label, node2;label, ...] or their aliases.", nargs='*')

        suppress_empty_columns_default = True
        prefilter_labels_default = True
        use_label_envar_default = True
        lift_all_columns_default = True
        require_label_file_default = True
        force_input_mode_none_default = True

    else:
        raise KGTKException("Unknown command %s" % repr(_command))

    parser.add_argument(      "--input-select-column", "--input-label-column", dest="input_select_column_name",
                              help=h("If input record selection is enabled by --input-select-value, " +
                              "the name of a column that determines which records received lifted values. " +
                              "The default is the 'label' column or its alias."), default=None)

    parser.add_argument(      "--input-select-value", "--input-label-value", "--target-label-value", dest="input_select_column_value",
                              help=h("The value in the input select column that identifies a record to receive lifted values. " +
                              "The default is not to perform input record selection, " +
                              "and all input records except label records may receive lifted values. "),
                              default=None)

    parser.add_argument(      "--lift-suffix", dest="output_lifted_column_suffix",
                              help=h("The suffix used for newly created output columns. (default=%(default)s)."),
                              default=KgtkLift.DEFAULT_OUTPUT_LIFTED_COLUMN_SUFFIX)

    parser.add_argument(      "--default-value", dest="default_value",
                              help="The value to use if a lifted label is not found. (default=%(default)s)", default="")

    parser.add_argument(      "--update-select-value", "--target-new-label-value", dest="output_select_column_value",
                              help=h("A new value for the select (label) column for records that received lifted values. " +
                              "The default is not to update the select(label) column."), default=None)
    

    parser.add_argument(      "--label-select-column", "--label-name", dest="label_select_column_name",
                              help=h("The name of the column that contains a special value that identifies label records. " +
                              "The default is 'label' or its alias."), default=None)

    parser.add_argument("-p", "--label-select-value", "--label-value", "--property", dest="label_select_column_value",
                              help=h("The special value in the label select column that identifies a label record. " +
                              "(default=%(default)s)."), default=KgtkLift.DEFAULT_LABEL_SELECT_COLUMN_VALUE)
    
    parser.add_argument(      "--label-match-column", "--node1-name", dest="label_match_column_name",
                              help=h("The name of the column in the label records that contains the value " +
                              "that matches the value in a column being lifted in the input records. " +
                              "The default is 'node1' or its alias."), default=None)

    parser.add_argument(      "--label-value-column", "--node2-name", "--lift-from", dest="label_value_column_name",
                              help=h("The name of the column in the label record that contains the value " +
                              "to be lifted into the input record that is receiving lifted values. " +
                              "The default is 'node2' or its alias."), default=None)

    parser.add_argument(      "--remove-label-records", dest="remove_label_records",
                              help=h("If true, remove label records from the output. (default=%(default)s)."),
                              metavar="True/False",
                              type=optional_bool, nargs='?', const=True, default=True)

    parser.add_argument(      "--sort-lifted-labels", dest="sort_lifted_labels",
                              help=h("If true, sort lifted labels with lists. (default=%(default)s)."),
                              metavar="True/False",
                              type=optional_bool, nargs='?', const=True, default=True)

    parser.add_argument(      "--suppress-duplicate-labels", dest="suppress_duplicate_labels",
                              help=h("If true, suppress duplicate values in lists in lifted labels (implies sorting). (default=%(default)s)."),
                              metavar="True/False",
                              type=optional_bool, nargs='?', const=True, default=True)

    parser.add_argument(      "--suppress-empty-columns", dest="suppress_empty_columns",
                              help="If true, do not create new columns that would be empty. (default=%(default)s).",
                              metavar="True/False",
                              type=optional_bool, nargs='?', const=True, default=suppress_empty_columns_default)


    parser.add_argument(      "--ok-if-no-labels", dest="ok_if_no_labels",
                              help="If true, do not abort if no labels were found. (default=%(default)s).",
                              metavar="True/False",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--prefilter-labels", dest="prefilter_labels",
                              help="If true, read the input file before reading the label file. (default=%(default)s).",
                              metavar="True/False",
                              type=optional_bool, nargs='?', const=True, default=prefilter_labels_default)

    parser.add_argument(      "--input-file-is-presorted", dest="input_is_presorted",
                              help="If true, the input file is presorted on the column for which values are to be lifted. (default=%(default)s).",
                              metavar="True/False",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--label-file-is-presorted", dest="labels_are_presorted",
                              help="If true, the label file is presorted on the node1 column. (default=%(default)s).",
                              metavar="True/False",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--clear-before-lift", dest="clear_before_lift",
                              help="If true, set columns to write to the default value before lifting. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--overwrite", dest="overwrite",
                              help="If true, overwrite non-default values in the columns to write. " +
                              "If false, do not overwrite non-default values in the columns to write. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=True)

    parser.add_argument(      "--output-only-modified-rows", dest="output_only_modified_rows",
                              help="If true, output only modified edges to the primary output stream. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--use-label-envar", dest="use_label_envar",
                              help="If true, use the KGTK_LABEL_FILE envar for the label file if no --label-file. (default=%(default)s).",
                              metavar="True/False",
                              type=optional_bool, nargs='?', const=True, default=use_label_envar_default)

    parser.add_argument(      "--lift-all-columns", dest="lift_all_columns",
                              help=h("If true, lift all columns. (default=%(default)s)."),
                              metavar="True/False",
                              type=optional_bool, nargs='?', const=True, default=lift_all_columns_default)
        
    parser.add_argument(      "--require-label-file", dest="require_label_file",
                              help=h("If true, a label file must be required explicitly or through an envar. (default=%(default)s)."),
                              metavar="True/False",
                              type=optional_bool, nargs='?', const=True, default=require_label_file_default)
        
    parser.add_argument(      "--force-input-mode-none", dest="force_input_mode_none",
                              help=h("If true, force the input file to mode NONE. (default=%(default)s)."),
                              metavar="True/False",
                              type=optional_bool, nargs='?', const=True, default=force_input_mode_none_default)
        
    KgtkReader.add_debug_arguments(parser, expert=_expert)
    # TODO: seperate reader_options for the label file.
    KgtkReaderOptions.add_arguments(parser, mode_options=True, expert=_expert)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, who="input", expert=_expert, defaults=False)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, who="label", expert=_expert, defaults=False)
    KgtkValueOptions.add_arguments(parser, expert=_expert)

def run(input_file: KGTKFiles,
        output_file: KGTKFiles,
        label_file: KGTKFiles,
        unmodified_row_file: KGTKFiles,
        matched_label_file: KGTKFiles,
        unmatched_label_file: KGTKFiles,

        input_select_column_name: typing.Optional[str],
        input_select_column_value: typing.Optional[str],
        input_lifting_column_names: typing.List[str],

        output_lifted_column_names: typing.List[str],
        output_lifted_column_suffix: str,
        output_select_column_value: str,

        label_select_column_name: typing.Optional[str],
        label_select_column_value: str,
        label_match_column_name: typing.Optional[str],
        label_value_column_name: typing.Optional[str],

        default_value: str,

        remove_label_records: bool = False,
        sort_lifted_labels: bool = True,
        suppress_duplicate_labels: bool = True,
        suppress_empty_columns: bool = False,
        ok_if_no_labels: bool = False,
        prefilter_labels: bool = False,
        input_is_presorted: bool = False,
        labels_are_presorted: bool = False,

        clear_before_lift: bool = False,
        overwrite: bool = False,

        output_only_modified_rows: bool = False,

        use_label_envar: bool = False,
        lift_all_columns: bool = False,
        require_label_file: bool = False,
        force_input_mode_none: bool = False,

        errors_to_stdout: bool = False,
        errors_to_stderr: bool = True,
        show_options: bool = False,
        verbose: bool = False,
        very_verbose: bool = False,

        **kwargs # Whatever KgtkFileOptions and KgtkValueOptions want.
)->int:
    # import modules locally
    import os
    from pathlib import Path
    import sys
    
    from kgtk.exceptions import KGTKException
    from kgtk.lift.kgtklift import KgtkLift
    from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
    from kgtk.io.kgtkwriter import KgtkWriter
    from kgtk.value.kgtkvalueoptions import KgtkValueOptions

    input_kgtk_file: Path = KGTKArgumentParser.get_input_file(input_file)
    output_kgtk_file: Path = KGTKArgumentParser.get_output_file(output_file)
    label_kgtk_file: typing.Optional[Path] = KGTKArgumentParser.get_optional_input_file(label_file, who="KGTK label file")
    unmodified_row_kgtk_file: typing.Optional[Path] = KGTKArgumentParser.get_optional_output_file(unmodified_row_file, who="KGTK unmodified row output file")
    matched_label_kgtk_file: typing.Optional[Path] = KGTKArgumentParser.get_optional_output_file(matched_label_file, who="KGTK matched label output file")
    unmatched_label_kgtk_file: typing.Optional[Path] = KGTKArgumentParser.get_optional_output_file(unmatched_label_file, who="KGTK unmatched label output file")

    # Select where to send error messages, defaulting to stderr.
    error_file: typing.TextIO = sys.stdout if errors_to_stdout else sys.stderr

    # Build the option structures.
    input_reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs, who="input", fallback=True)
    label_reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs, who="label", fallback=True)
    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs)
    value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)

    # Show the final option structures for debugging and documentation.
    if show_options:
        print("--input-file=%s" % str(input_kgtk_file), file=error_file, flush=True)
        print("--output-file=%s" % str(output_kgtk_file), file=error_file, flush=True)
        if label_kgtk_file is not None:
            print("--label-file=%s" % label_kgtk_file, file=error_file, flush=True)
        if unmodified_row_kgtk_file is not None:
            print("--unmodified-row-output-file=%s" % unmodified_row_kgtk_file, file=error_file, flush=True)
        if matched_label_kgtk_file is not None:
            print("--matched-label-output-file=%s" % matched_label_kgtk_file, file=error_file, flush=True)
        if unmatched_label_kgtk_file is not None:
            print("--unmatched-label-output-file=%s" % unmatched_label_kgtk_file, file=error_file, flush=True)

        if input_select_column_name is not None:
            print("--input-select-column=%s" % input_select_column_name, file=error_file, flush=True)
        if input_select_column_value is not None:
            print("--input-select-value=%s" % input_select_column_value, file=error_file, flush=True)
        if input_lifting_column_names is not None and len(input_lifting_column_names) > 0:
            print("--columns-to-lift %s" % " ".join(input_lifting_column_names), file=error_file, flush=True)
        if output_lifted_column_names is not None and len(output_lifted_column_names) > 0:
            print("--columns-to-write %s" % " ".join(output_lifted_column_names), file=error_file, flush=True)

        print("--lift-suffix=%s" % output_lifted_column_suffix, file=error_file, flush=True)
        if output_select_column_value is not None:
            print("--update-select-value=%s" % output_select_column_value, file=error_file, flush=True)


        if label_select_column_name is not None:
            print("--label-select-column=%s" % label_select_column_name, file=error_file, flush=True)
        print("--label-select-value=%s" % label_select_column_value, file=error_file, flush=True)
        if label_match_column_name is not None:
            print("--label-match-column=%s" % label_match_column_name, file=error_file, flush=True)
        if label_value_column_name is not None:
            print("--label-value-column=%s" % label_value_column_name, file=error_file, flush=True)

        print("--default-value=%s" % repr(default_value), file=error_file, flush=True)
        print("--remove-label-records=%s" % repr(remove_label_records), file=error_file, flush=True)
        print("--sort-lifted-labels=%s" % repr(sort_lifted_labels), file=error_file, flush=True)
        print("--suppress-duplicate-labels=%s" % repr(suppress_duplicate_labels), file=error_file, flush=True)
        print("--suppress-empty-columns=%s" % repr(suppress_empty_columns), file=error_file, flush=True)
        print("--ok-if-no-labels=%s" % repr(ok_if_no_labels), file=error_file, flush=True)
        print("--prefilter-labels=%s" % repr(prefilter_labels), file=error_file, flush=True)
        print("--input-file-is-presorted=%s" % repr(input_is_presorted), file=error_file, flush=True)
        print("--label-file-is-presorted=%s" % repr(labels_are_presorted), file=error_file, flush=True)
        print("--clear-before-lift=%s" % repr(clear_before_lift), file=error_file, flush=True)
        print("--overwrite=%s" % repr(overwrite), file=error_file, flush=True)
        print("--output-only-modified-rows=%s" % repr(output_only_modified_rows), file=error_file, flush=True)
        print("--use-label-envar=%s" % repr(use_label_envar), file=error_file, flush=True)
        print("--lift-all-columns=%s" % repr(lift_all_columns), file=error_file, flush=True)
        print("--require-label-files=%s" % repr(require_label_file), file=error_file, flush=True)
        print("--force-input-mode-none=%s" % repr(force_input_mode_none), file=error_file, flush=True)
        input_reader_options.show(out=error_file, who="input")
        label_reader_options.show(out=error_file, who="label")
        value_options.show(out=error_file)
        print("=======", file=error_file, flush=True)

    # Should the following functionality be moved to KgtkLift?
    if label_kgtk_file is None and use_label_envar:
        label_file_envar: str = 'KGTK_LABEL_FILE' # TODO: Move this to a common file.
        label_file_envar_value: typing.Optional[str] = os.getenv(label_file_envar)
        if label_file_envar_value is not None:
            label_kgtk_file = Path(label_file_envar_value)
            if verbose:
                print("Using label file %s from envar %s" % (repr(label_file_envar_value), repr(label_file_envar)), file=error_file, flush=True)

    if require_label_file and label_kgtk_file is None:
        raise KGTKException("A label file must be specified using --label-file or KGTK_LABEL_FILE")

    try:
        kl: KgtkLift = KgtkLift(
            input_file_path=input_kgtk_file,
            label_file_path=label_kgtk_file,
            output_file_path=output_kgtk_file,
            unmodified_row_file_path=unmodified_row_kgtk_file,
            matched_label_file_path=matched_label_kgtk_file,
            unmatched_label_file_path=unmatched_label_kgtk_file,

            input_select_column_name=input_select_column_name,
            input_select_column_value=input_select_column_value,
            input_lifting_column_names=input_lifting_column_names,

            output_lifted_column_suffix=output_lifted_column_suffix,
            output_select_column_value=output_select_column_value,
            output_lifted_column_names=output_lifted_column_names,

            label_select_column_name=label_select_column_name,
            label_select_column_value=label_select_column_value,
            label_match_column_name=label_match_column_name,
            label_value_column_name=label_value_column_name,

            default_value=default_value,

            remove_label_records=remove_label_records,
            sort_lifted_labels=sort_lifted_labels,
            suppress_duplicate_labels=suppress_duplicate_labels,
            suppress_empty_columns=suppress_empty_columns,
            ok_if_no_labels=ok_if_no_labels,
            prefilter_labels=prefilter_labels,
            input_is_presorted=input_is_presorted,
            labels_are_presorted=labels_are_presorted,

            clear_before_lift=clear_before_lift,
            overwrite=overwrite,

            output_only_modified_rows=output_only_modified_rows,

            lift_all_columns=lift_all_columns,
            force_input_mode_none=force_input_mode_none,

            input_reader_options=input_reader_options,
            label_reader_options=label_reader_options,
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

