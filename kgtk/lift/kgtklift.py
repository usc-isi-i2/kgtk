"""Add label columns for values in the node1, label, and node2 fields.

The input rows are saved in memory, as well as the value-to-label mapping.
This will impose a limit on the size of the input files that can be processed.

TODO: Take a list of properties?

TODO: Optionally save the input rows in an external disk file?

TODO: Optionally reread the input stream insted of saving the input rows?
      With special provision for copying standard input to an external disk file.

TODO: Need KgtkWriterOptions

TODO: Provide seperate reader options for the label file.

"""

from argparse import ArgumentParser, Namespace
import attr
from pathlib import Path
import sys
import typing

from kgtk.kgtkformat import KgtkFormat
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions, KgtkReaderMode
from kgtk.io.kgtkwriter import KgtkWriter
from kgtk.utils.argparsehelpers import optional_bool
from kgtk.value.kgtkvalue import KgtkValue
from kgtk.value.kgtkvalueoptions import KgtkValueOptions

@attr.s(slots=True, frozen=True)
class KgtkLift(KgtkFormat):
    DEFAULT_OUTPUT_LIFTED_COLUMN_SEPARATOR: str = ";"
    DEFAULT_LABEL_SELECT_COLUMN_VALUE: str = "label"
    DEFAULT_OUTPUT_LIFTED_COLUMN_SUFFIX: str = DEFAULT_OUTPUT_LIFTED_COLUMN_SEPARATOR + DEFAULT_LABEL_SELECT_COLUMN_VALUE

    input_file_path: Path = attr.ib(validator=attr.validators.instance_of(Path))
    label_file_path: typing.Optional[Path] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Path)))
    output_file_path: Path = attr.ib(validator=attr.validators.instance_of(Path))
 
    input_select_column_name: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    input_select_column_value: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    input_lifting_column_names: typing.Optional[typing.List[str]] = \
        attr.ib(validator=attr.validators.optional(attr.validators.deep_iterable(member_validator=attr.validators.instance_of(str),
                                                                                 iterable_validator=attr.validators.instance_of(list))),
                default=None)

    output_select_column_value: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    output_lifted_column_suffix: str = attr.ib(validator=attr.validators.instance_of(str), default=DEFAULT_OUTPUT_LIFTED_COLUMN_SUFFIX)
    output_lifted_column_names: typing.Optional[typing.List[str]] = \
        attr.ib(validator=attr.validators.optional(attr.validators.deep_iterable(member_validator=attr.validators.instance_of(str),
                                                                                 iterable_validator=attr.validators.instance_of(list))),
                default=None)

    label_select_disable: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    label_select_column_name: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    label_select_column_value: str = attr.ib(validator=attr.validators.instance_of(str), default=DEFAULT_LABEL_SELECT_COLUMN_VALUE)

    label_match_column_name: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    label_value_column_name: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)

    remove_label_records: bool = attr.ib(validator=attr.validators.instance_of(bool), default=True)
    suppress_duplicate_labels: bool = attr.ib(validator=attr.validators.instance_of(bool), default=True)
    sort_lifted_labels: bool = attr.ib(validator=attr.validators.instance_of(bool), default=True)
    suppress_empty_columns: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    ok_if_no_labels: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    prefilter_labels: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    input_is_presorted: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    labels_are_presorted: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    default_value: str = attr.ib(validator=attr.validators.instance_of(str), default="")

    clear_before_lift: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    overwrite: bool = attr.ib(validator=attr.validators.instance_of(bool), default=True)

    output_only_modified_rows: bool = attr.ib(validator=attr.validators.instance_of(bool), default=True)
    unmodified_row_file_path: typing.Optional[Path] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Path)), default=None)

    matched_label_file_path: typing.Optional[Path] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Path)), default=None)
    unmatched_label_file_path: typing.Optional[Path] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Path)), default=None)

    languages: typing.Optional[typing.List[str]] = \
        attr.ib(validator=attr.validators.optional(attr.validators.deep_iterable(member_validator=attr.validators.instance_of(str),
                                                                                 iterable_validator=attr.validators.instance_of(list))),
                default=None)
    prioritize: bool = attr.ib(validator=attr.validators.instance_of(bool), default=True)

    lift_all_columns: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    force_input_mode_none: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    
    # TODO: add rewind logic here and KgtkReader

    # TODO: find working validators
    # value_options: typing.Optional[KgtkValueOptions] = attr.ib(attr.validators.optional(attr.validators.instance_of(KgtkValueOptions)), default=None)
    input_reader_options: typing.Optional[KgtkReaderOptions]= attr.ib(default=None)
    label_reader_options: typing.Optional[KgtkReaderOptions]= attr.ib(default=None)
    value_options: typing.Optional[KgtkValueOptions] = attr.ib(default=None)

    error_file: typing.TextIO = attr.ib(default=sys.stderr)
    verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    very_verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    def build_lift_column_idxs(self, kr: KgtkReader)->typing.List[int]:
        lift_column_idxs: typing.List[int] = [ ]
        if self.input_lifting_column_names is not None and len(self.input_lifting_column_names) > 0:
            # Process a custom list of columns to be lifted.
            lift_column_name: str
            for lift_column_name in self.input_lifting_column_names:
                if lift_column_name not in kr.column_name_map:
                    raise ValueError("Unknown lift column %s." % lift_column_name)
                lift_column_idxs.append(kr.column_name_map[lift_column_name])

        elif self.lift_all_columns:
            idx: int
            column_name: str
            for idx, column_name in enumerate(kr.column_names):
                if not column_name.endswith(self.output_lifted_column_suffix):
                    lift_column_idxs.append(idx)

        else:
            # Use the edge file key columns if they exist.
            if kr.node1_column_idx >= 0:
                lift_column_idxs.append(kr.node1_column_idx)
            if kr.label_column_idx >= 0:
                lift_column_idxs.append(kr.label_column_idx)
            if kr.node2_column_idx >= 0:
                lift_column_idxs.append(kr.node2_column_idx)

        # Verify that we found some columns to lift:
        if len(lift_column_idxs) == 0:
            raise ValueError("No lift columns found.")

        return lift_column_idxs

    def lookup_input_select_column_idx(self, kr: KgtkReader)->int:
        input_select_column_idx: int
        if self.input_select_column_name is None:
            if kr.label_column_idx < 0:
                raise ValueError("No input select column index.")
            input_select_column_idx = kr.label_column_idx
        else:
            if self.input_select_column_name not in kr.column_name_map:
                raise ValueError("Input select column `%s` not found." % self.input_select_column_name)
            input_select_column_idx = kr.column_name_map[self.input_select_column_name]
        return input_select_column_idx

    def lookup_label_match_column_idx(self, kr: KgtkReader)->int:
        label_match_column_idx: int
        if self.label_match_column_name is None:
            if kr.is_edge_file:
                if self.verbose:
                    print("The label file is an edge file, defaulting to the node1 column (or alias) for the match column.",
                          file=self.error_file, flush=True)
                if kr.node1_column_idx < 0:
                    raise ValueError("Cannot find the label match column (node1) in the label file (an edge file).")
                label_match_column_idx = kr.node1_column_idx
            elif kr.is_node_file:
                if self.verbose:
                    print("The label file is a node file, defaulting to the ID column for the match column.",
                          file=self.error_file, flush=True)
                if kr.id_column_idx < 0:
                    raise ValueError("Cannot find the label match column (id) in the label file (a node file).")
                label_match_column_idx = kr.id_column_idx
            else:
                raise ValueError("No label match column specified and not an edge or node file.")

        else:
            if self.label_match_column_name not in kr.column_name_map:
                raise ValueError("Label match column `%s` not found." % self.label_match_column_name)
            label_match_column_idx = kr.column_name_map[self.label_match_column_name]
        return label_match_column_idx

    def lookup_label_select_column_idx(self, kr: KgtkReader)->int:
        label_select_column_idx: int
        if self.label_select_disable:
            label_select_column_idx = -1
        elif self.label_select_column_name is None:
            if kr.is_edge_file:
                if kr.label_column_idx < 0:
                    raise ValueError("Cannot find the label select column (label) in the label file.")
                label_select_column_idx = kr.label_column_idx
            elif kr.is_node_file:
                if self.verbose:
                    print("The label file is a node file, defaulting to no label select column.", file=self.error_file, flush=True)
                label_select_column_idx = -1 # Special case!
            else:
                raise ValueError("No label match column specified and not an edge or node file.")
        else:
            if self.label_select_column_name not in kr.column_name_map:
                raise ValueError("Label select column `%s` not found." % self.label_select_column_name)
            label_select_column_idx = kr.column_name_map[self.label_select_column_name]
        return label_select_column_idx

    def lookup_label_value_column_idx(self, kr: KgtkReader)->int:
        label_value_column_idx: int
        if self.label_value_column_name is None:
            if kr.is_edge_file:
                if self.verbose:
                    print("The label file is an edge file, defaulting to the node2 column (or alias) for the value column.",
                          file=self.error_file, flush=True)
                if kr.node2_column_idx < 0:
                    raise ValueError("Cannot find the label value column (node2) in the label edge file.")
                label_value_column_idx = kr.node2_column_idx
            elif kr.is_node_file:
                if self.verbose:
                    print("The label file is a node file, defaulting to the label column for the value column.",
                          file=self.error_file, flush=True)
                if kr.label_column_idx < 0:
                    raise ValueError("Cannot find the label value column (label) in the label node file.")
                label_value_column_idx = kr.label_column_idx
        else:
            if self.label_value_column_name not in kr.column_name_map:
                raise ValueError("Label value column `%s` not found in the label file." % self.label_value_column_name)
            label_value_column_idx = kr.column_name_map[self.label_value_column_name]

        return label_value_column_idx

    def lookup_label_table_idxs(self, kr: KgtkReader)->typing.Tuple[int, int, int]:
        label_match_column_idx: int = self.lookup_label_match_column_idx(kr)
        label_select_column_idx: int = self.lookup_label_select_column_idx(kr)
        label_value_column_idx: int = self.lookup_label_value_column_idx(kr)

        return label_match_column_idx, label_select_column_idx, label_value_column_idx

    def load_labels(self,
                    kr: KgtkReader,
                    path: Path,
                    save_input: bool = True,
                    labels_needed: typing.Optional[typing.Set[str]] = None,
                    label_rows: typing.Optional[typing.MutableMapping[str, typing.List[typing.List[str]]]] = None,
                    is_label_file: bool = False,
    )->typing.Tuple[typing.Mapping[str, str], typing.List[typing.List[str]]]:
        input_rows: typing.List[typing.List[str]] = [ ]
        labels: typing.MutableMapping[str, str] = { }

        label_match_column_idx: int
        label_select_column_idx: int
        label_value_column_idx: int
        label_match_column_idx, label_select_column_idx, label_value_column_idx = self.lookup_label_table_idxs(kr)

        # Build the label filter.  We will still do the same filtering steps in code below.
        #
        # TODO: Remove the redundant filtering steps.
        if is_label_file:
            label_filter: typing.MutableMapping[int, typing.Set[str]] = dict()
            if label_select_column_idx >= 0:
                label_filter[label_select_column_idx] = set([self.label_select_column_value])
            if labels_needed is not None and label_match_column_idx >= 0:
                label_filter[label_match_column_idx] = set(labels_needed)
            if len(label_filter) > 0:
                kr.add_input_filter(label_filter)

        if self.verbose:
            print("Loading labels from %s" % path, file=self.error_file, flush=True)
            if labels_needed is not None:
                print("Filtering for needed labels", file=self.error_file, flush=True)
            print("label_match_column_idx=%d (%s)." % (label_match_column_idx, kr.column_names[label_match_column_idx]), file=self.error_file, flush=True)
            if label_select_column_idx < 0:
                print("label_select_column_idx=%d." % (label_select_column_idx), file=self.error_file, flush=True)
            else:
                print("label_select_column_idx=%d (%s)." % (label_select_column_idx, kr.column_names[label_select_column_idx]), file=self.error_file, flush=True)
            print("label_value_column_idx=%d (%s)." % (label_value_column_idx, kr.column_names[label_value_column_idx]), file=self.error_file, flush=True)
            print("label_select_column_value='%s'." % self.label_select_column_value, file=self.error_file, flush=True)

        # Setup for language filtering:
        language_filtering: bool = self.languages is not None and len(self.languages) > 0
        allow_all_strings: bool = False
        allow_all_lqstrings: bool = False
        language_filter: typing.List[str] = list()
        language_filter_tuple: typing.Tuple[str, ...] = ()
        label_priorities: typing.MutableMapping[str, int] = dict()
        if language_filtering:
            for lf in self.languages:
                if lf == 'NONE':
                    if self.prioritize:
                        language_filter.append(lf)
                    else:
                        allow_all_strings = True
                elif lf == 'ANY':
                    if self.prioritize:
                        language_filter.append(lf)
                    else:
                        allow_all_lqstrings = True
                else:
                    language_filter.append("'@" + lf)
            language_filter_tuple = tuple(language_filter)

        key: str
        row: typing.List[str]
        for row in kr:
            if label_select_column_idx < 0 or row[label_select_column_idx] == self.label_select_column_value:
                # This is a label definition row.
                label_key: str = row[label_match_column_idx]
                if labels_needed is not None and label_key not in labels_needed:
                    # We don't need this label.
                    if save_input and not self.remove_label_records:
                        input_rows.append(row.copy())
                    continue # Ignore unneeded labels.

                label_value: str = row[label_value_column_idx]
                if label_value == self.default_value:
                    # We can ignore default values.
                    #
                    # TODO: There might be different semantics to default value handling between
                    # this code and the merge code.
                    if save_input and not self.remove_label_records:
                        input_rows.append(row.copy())
                    continue # Ignore default values.

                process_label: bool
                if language_filtering:
                    sigil: str
                    if len(label_value) == 0:
                        # An empty value is not a valid label when filtering by language.
                        process_label = False

                    elif self.prioritize:
                        current_priority: int = label_priorities.get(label_key, 999999)
                        sigil = label_value[0]
                        priority: int
                        lf: str
                        for priority, lf in enumerate(language_filter):
                            if priority >= current_priority:
                                process_label = False
                                break

                            elif sigil == KgtkFormat.STRING_SIGIL:
                                if lf == "NONE":
                                    process_label = True
                                    break
                                
                            elif sigil == KgtkFormat.LANGUAGE_QUALIFIED_STRING_SIGIL:
                                if (lf == "ANY" or label_value.endswith(lf)):
                                    process_label = True
                                    break

                            else:
                                process_label = False
                                break # Do not allow values that are neither strings nor lqstrings.
                        else:
                            process_label = False


                        if process_label:
                            label_priorities[label_key] = priority
                            if label_key in labels:
                                del labels[label_key] # Remove the prior label
                    else:
                        sigil = label_value[0]
                        if sigil == KgtkFormat.STRING_SIGIL:
                            process_label = allow_all_strings

                        elif sigil == KgtkFormat.LANGUAGE_QUALIFIED_STRING_SIGIL:
                            process_label = allow_all_lqstrings or label_value.endswith(language_filter_tuple)

                        else:
                            # Do not allow values that are neither strings nor lqstrings.
                            process_label = False
                else:
                    process_label = True

                if process_label:
                    if label_key in labels:
                        # This label already exists in the table.
                        if self.suppress_duplicate_labels:
                            # Build a list eliminating duplicate elements.
                            # print("Merge '%s' and '%s'" % (key_value, labels[key]), file=self.error_file, flush=True)
                            labels[label_key] = KgtkValue.merge_values(labels[label_key], label_value)
                        else:
                            labels[label_key] = KgtkFormat.LIST_SEPARATOR.join((labels[label_key], label_value))
                        if label_rows is not None:
                            label_rows[label_key].append(row.copy())
                    else:
                        # This is the first instance of this label definition.
                        labels[label_key] = label_value
                        if label_rows is not None:
                            label_rows[label_key] = [ row.copy() ]
                if save_input and not self.remove_label_records:
                    input_rows.append(row.copy())
            else:
                if save_input:
                    input_rows.append(row.copy())
        return labels, input_rows
                
    def load_input_keeping_label_records(self,
                                         kr: KgtkReader,
                                         path: Path,
    )-> typing.List[typing.List[str]]:
        input_rows: typing.List[typing.List[str]] = [ ]

        if self.verbose:
            print("Loading input rows with labels from %s" % path, file=self.error_file, flush=True)
        row: typing.List[str]
        for row in kr:
            input_rows.append(row)
        return input_rows

    def load_input_removing_label_records(self,
                                          kr: KgtkReader,
                                          path: Path,
    )-> typing.List[typing.List[str]]:
        label_select_column_idx: int = self.lookup_label_select_column_idx(kr)
        if label_select_column_idx < 0:
            return self.load_input_keeping_label_records(kr, path)

        if self.verbose:
            print("Loading input rows without labels from %s" % path, file=self.error_file, flush=True)

        input_rows: typing.List[typing.List[str]] = [ ]
        row: typing.List[str]
        for row in kr:
            if row[label_select_column_idx] != self.label_select_column_value:
                input_rows.append(row)

        return input_rows

    def load_input(self,
                   kr: KgtkReader,
                   path: Path,
                   seperate_label_file: bool = False
    )-> typing.List[typing.List[str]]:
        if seperate_label_file:
            return self.load_input_keeping_label_records(kr, path)
        elif self.remove_label_records:
            return self.load_input_removing_label_records(kr, path)
        else:
            return self.load_input_keeping_label_records(kr, path)

    def build_lifted_column_idxs(self,
                                 kr: KgtkReader,
                                 lift_column_idxs: typing.List[int],
                                 input_rows: typing.List[typing.List[str]],
                                 labels: typing.Mapping[str, str],
                                 label_select_column_idx: int,
                                 input_select_column_idx: int,
    )->typing.List[int]:
        """
        Build the lifted column indexes, suppressing those columns
        for which there are are no label values.  This requires a
        pass through the input data.
        """
        if self.verbose:
            print("Checking for empty columns", file=self.error_file, flush=True)
        lift_column_idxs_empties: typing.List[int] = lift_column_idxs.copy()
        lift_column_idx: int
        # Scan the input file, checking for empty output columns.
        for row in input_rows:
            if label_select_column_idx >= 0:
                if row[label_select_column_idx] == self.label_select_column_value:
                    # Skip label records if they have been saved.
                    continue

            if input_select_column_idx >= 0:
                if self.input_select_column_value is not None and row[input_select_column_idx] != self.input_select_column_value:
                    # Not selected for lifting into.
                    continue
            idx: int
            restart: bool = True
            while restart:
                # The restart mechanism compensates for modifying
                # lift_column_idxs_empties inside the for loop, at the
                # expense of potentially double testing some items.
                restart = False
                for idx, lift_column_idx in enumerate(lift_column_idxs_empties):
                    item: str = row[lift_column_idx]
                    if item in labels:
                        lift_column_idxs_empties.pop(idx)
                        restart = True
                        break
            if len(lift_column_idxs_empties) == 0:
                break

        if self.verbose:
            if len(lift_column_idxs_empties) == 0:
                print("No lifted columns are empty", file=self.error_file, flush=True)
            else:
                input_lifting_column_names_empties: typing.List[str] = [ ]
                for idx in lift_column_idxs_empties:
                    input_lifting_column_names_empties.append(kr.column_names[idx])
                print("Unlifted columns: %s" % " ".join(input_lifting_column_names_empties), file=self.error_file, flush=True)

        lifted_column_idxs: typing.List[int] = [ ]
        for lift_column_idx in lift_column_idxs:
            if lift_column_idx not in lift_column_idxs_empties:
                lifted_column_idxs.append(lift_column_idx)            
        return lifted_column_idxs

    def write_output_row(self,
                         ew: KgtkWriter,
                         row: typing.List[str],
                         new_columns: int,
                         input_select_column_idx: int,
                         label_select_column_idx: int,
                         labels: typing.Mapping[str, str],
                         lifted_column_idxs: typing.List[int],
                         lifted_output_column_idxs: typing.List[int],
                         urkw: typing.Optional[KgtkWriter],
                         mlkw: typing.Optional[KgtkWriter],
                         label_rows: typing.Optional[typing.Mapping[str, typing.List[typing.List[str]]]],
                         matched_labels: typing.Set[str],
        )->typing.Tuple[bool, bool, bool]:
        output_row: typing.List[str] = row.copy()
        if new_columns > 0:
            output_row.extend([self.default_value] * new_columns)
        output_select_column_idx: int = input_select_column_idx
                
        do_write: bool = True
        do_lift: bool = True
        did_lift: bool = False
        modified: bool = False
        skipped: bool = False
        if label_select_column_idx >= 0:
            print("label_select_column_idx %d" % label_select_column_idx)
            if row[label_select_column_idx]  == self.label_select_column_value:
                # Don't lift label columns, if we have stored labels in the input records.
                do_lift = False
                if self.remove_label_records:
                    do_write = False
        if input_select_column_idx >= 0:
            if self.input_select_column_value is not None and row[input_select_column_idx] != self.input_select_column_value:
                # Not selected for lifting into.
                do_lift = False
                skipped = True
        if do_lift:
            # Lift the specified columns in this row.
            lifted_column_idx: int
            for idx, lifted_column_idx in enumerate(lifted_column_idxs):
                lifted_output_column_idx: int = lifted_output_column_idxs[idx]
                if self.clear_before_lift:
                    output_row[lifted_output_column_idx] = self.default_value
                if self.overwrite or output_row[lifted_output_column_idxs[idx]] == self.default_value:
                    label_key: str = row[lifted_column_idx]
                    if label_key in labels:
                        label_value: str = labels[label_key]
                        if label_value != output_row[lifted_output_column_idx]:
                            modified = True
                        output_row[lifted_output_column_idx] = label_value
                        did_lift = True # What if we want to note if we lifted all columns?

                        if label_key not in matched_labels:
                            matched_labels.add(label_key)
                            if label_rows is not None and mlkw is not None:
                                label_row: typing.List[str]
                                for label_row in label_rows[label_key]:
                                    mlkw.write(label_row)

            if did_lift and output_select_column_idx >= 0 and self.output_select_column_value is not None:
                if output_row[output_select_column_idx] != self.output_select_column_value:
                    modified = True
                output_row[output_select_column_idx] = self.output_select_column_value

        if do_write:
            if self.output_only_modified_rows:
                if modified:
                    ew.write(output_row)
            else:
                ew.write(output_row)

        if urkw is not None:
            # The unmodified row output file gets all unmodified input rows,
            # including input rows that are labels or are not selected for lift.
            if not modified:
                urkw.write(row)

        return do_write, modified, skipped

    def build_output_column_names(self, ikr: KgtkReader, lifted_column_idxs: typing.List[int])->typing.Tuple[typing.List[str], typing.List[int]]:
        # Build the output column names.
        output_column_names: typing.List[str] = ikr.column_names.copy()
        lifted_output_column_idxs: typing.List[int] = [ ]
        lifted_idx: int
        column_idx: int
        for lifted_idx, column_idx in enumerate(lifted_column_idxs):
            lifted_column_name: str
            if self.output_lifted_column_names is not None and lifted_idx < len(self.output_lifted_column_names):
                lifted_column_name = self.output_lifted_column_names[lifted_idx]
            else:
                lifted_column_name = ikr.column_names[column_idx] + self.output_lifted_column_suffix

            if lifted_column_name in ikr.column_name_map:
                # Overwrite an existing lifted output column.
                #
                # TODO: DO we want to control whether or not we overwrite existing columns?
                lifted_output_column_idxs.append(ikr.column_name_map[lifted_column_name])
            else:
                # Append a new lifted output column.
                lifted_output_column_idxs.append(len(output_column_names))
                output_column_names.append(lifted_column_name)
        return output_column_names, lifted_output_column_idxs

    def open_output_writer(self,
                           ikr: KgtkReader,
                           lifted_column_idxs: typing.List[int]
    )->typing.Tuple[KgtkWriter, typing.List[int]]:
        # Build the output column names.
        output_column_names: typing.List[str]
        lifted_output_column_idxs: typing.List[int]
        output_column_names, lifted_output_column_idxs = self.build_output_column_names(ikr, lifted_column_idxs)

        if self.verbose:
            print("Opening the output file: %s" % self.output_file_path, file=self.error_file, flush=True)
        ew: KgtkWriter = KgtkWriter.open(output_column_names,
                                         self.output_file_path,
                                         mode=KgtkWriter.Mode[ikr.mode.name],
                                         require_all_columns=False,
                                         prohibit_extra_columns=True,
                                         fill_missing_columns=True,
                                         use_mgzip=False if self.input_reader_options is None else self.input_reader_options.use_mgzip , # Hack!
                                         mgzip_threads=3 if self.input_reader_options is None else self.input_reader_options.mgzip_threads , # Hack!
                                         gzip_in_parallel=False,
                                         verbose=self.verbose,
                                         very_verbose=self.very_verbose)        

        return ew, lifted_output_column_idxs

    def build_labels_needed(self,
                            input_rows: typing.List[typing.List[str]],
                            input_select_column_idx: int,
                            lift_column_idxs: typing.List[int],
    )->typing.Set[str]:
        labels_needed: typing.Set[str] = set()

        row: typing.List[str]
        for row in input_rows:
            if input_select_column_idx >= 0:
                if self.input_select_column_value is not None and row[input_select_column_idx] != self.input_select_column_value:
                    # Not selected for lifting into.
                    continue
            lift_column_idx: int
            for lift_column_idx in lift_column_idxs:
                label_key: str = row[lift_column_idx]
                labels_needed.add(label_key)

        if self.verbose:
            print("Labels needed: %d" % len(labels_needed), file=self.error_file, flush=True)

        return labels_needed

    def process_in_memory(self, ikr: KgtkReader,
                          lkr: typing.Optional[KgtkReader],
                          urkw: typing.Optional[KgtkWriter],
                          mlkw: typing.Optional[KgtkWriter],
                          ulkw: typing.Optional[KgtkWriter],
                          ):
        """
        Process the lift using in-memory buffering.  The labels will added to a
        dict in memory, and depending upon the options selected, the input
        rows may be kept on a list in memory.

        """
        if self.verbose:
            print("Lifting with in-memory buffering.", file=self.error_file, flush=True)
        lift_column_idxs: typing.List[int] = self.build_lift_column_idxs(ikr)

        labels: typing.Mapping[str, str] = { }
        input_rows: typing.Optional[typing.List[typing.List[str]]] = None

        label_rows: typing.Optional[typing.MutableMapping[str, typing.List[typing.List[str]]]]

        if mlkw is None and ulkw is None:
            label_rows = None
        else:
            label_rows = { }
        
        input_select_column_idx: int
        if self.input_select_column_value is not None or self.output_select_column_value is not None:
            input_select_column_idx = self.lookup_input_select_column_idx(ikr)
        else:
            input_select_column_idx = -1

        # Unless told otherwise, assume that label rows won't be saved
        # in the input rows:
        label_select_column_idx: int = -1

        # Extract the labels, and maybe store the input rows.
        if lkr is not None and self.label_file_path is not None:
            labels_needed: typing.Optional[typing.Set[str]] = None
            if self.prefilter_labels:
                if self.verbose:
                    print("Reading input data to prefilter the labels.", file=self.error_file, flush=True)
                input_rows = self.load_input(ikr, self.input_file_path, seperate_label_file=True)
                labels_needed = self.build_labels_needed(input_rows, input_select_column_idx, lift_column_idxs)
            # Read the label file.
            if self.verbose:
                print("Loading labels from the label file.", file=self.error_file, flush=True)
            # We don't need to worry about input rows in the label file.
            labels, _ = self.load_labels(lkr, self.label_file_path, save_input=False, labels_needed=labels_needed, label_rows=label_rows, is_label_file=True)
        else:
            if self.verbose:
                print("Loading labels and reading data from the input file.", file=self.error_file, flush=True)
            # Read the input file, extracting the labels. The label
            # records may or may not be saved in the input rows, depending
            # upon whether we plan to pass them through to the output.
            labels, input_rows = self.load_labels(ikr, self.input_file_path, label_rows=label_rows)

            if not self.remove_label_records:
                # Save the label column index in the input rows:
                label_select_column_idx = self.lookup_label_select_column_idx(ikr)

        label_count: int = len(labels)
        if label_count == 0 and not self.ok_if_no_labels:
            raise ValueError("No labels were found.")

        lifted_column_idxs: typing.List[int]
        if self.suppress_empty_columns:
            if input_rows is None:
                # We need to read the input records now in order to determine
                # which lifted columns must be suppressed.
                if self.verbose:
                    print("Reading input data to suppress empty columns.", file=self.error_file, flush=True)
                input_rows = self.load_input(ikr, self.input_file_path)
            lifted_column_idxs = self.build_lifted_column_idxs(ikr, lift_column_idxs, input_rows, labels, label_select_column_idx, input_select_column_idx)
        else:
            # Lift all the candidate columns.
            lifted_column_idxs = lift_column_idxs.copy()

        ew: KgtkWriter
        lifted_output_column_idxs: typing.List[int]
        ew, lifted_output_column_idxs = self.open_output_writer(ikr, lifted_column_idxs)

        if self.verbose:
            print("Writing output records", file=self.error_file, flush=True)

        matched_labels: typing.Set[str] = set()
        new_columns: int = len(ew.column_names) - len(ikr.column_names)
        input_line_count: int = 0
        input_skipped_count: int = 0
        output_line_count: int = 0
        output_modified_count: int = 0
        if input_rows is None:
            do_write: bool
            modified: bool
            skipped: bool
            # Read the input file and process it in one pass:
            for row in ikr:
                input_line_count += 1
                do_write, modified, skipped = self.write_output_row(ew,
                                                                    row,
                                                                    new_columns,
                                                                    input_select_column_idx,
                                                                    label_select_column_idx,
                                                                    labels,
                                                                    lifted_column_idxs,
                                                                    lifted_output_column_idxs,
                                                                    urkw,
                                                                    mlkw,
                                                                    label_rows,
                                                                    matched_labels,
                                                                    )
                if do_write:
                    output_line_count += 1
                    if modified:
                        output_modified_count += 1
                if skipped:
                    input_skipped_count += 1
        else:
            # Use the stored input records:
            for row in input_rows:
                input_line_count += 1
                do_write, modified, skipped = self.write_output_row(ew,
                                                                    row,
                                                                    new_columns,
                                                                    input_select_column_idx,
                                                                    label_select_column_idx,
                                                                    labels,
                                                                    lifted_column_idxs,
                                                                    lifted_output_column_idxs,
                                                                    urkw,
                                                                    mlkw,
                                                                    label_rows,
                                                                    matched_labels,
                                                                    )
                if do_write:
                    output_line_count += 1
                    if modified:
                        output_modified_count += 1
                if skipped:
                    input_skipped_count += 1

        if ulkw is not None and label_rows is not None:
            label_key: str
            for label_key in sorted(label_rows.keys()):
                if label_key not in matched_labels:
                    label_row: typing.List[str]
                    for label_row in label_rows[label_key]:
                        ulkw.write(label_row)

        if self.verbose:
            print("Read %d non-label input records, %d skipped." % (input_line_count, input_skipped_count), file=self.error_file, flush=True)
            print("%d labels were found, %d matched." % (label_count, len(matched_labels)), file=self.error_file, flush=True)
            print("Wrote %d output records, %d modified." % (output_line_count, output_modified_count), file=self.error_file, flush=True)
        
        ew.close()
    
    def process_as_merge(self, ikr: KgtkReader,
                         lkr: KgtkReader,
                         urkw: typing.Optional[KgtkWriter],
                         mlkw: typing.Optional[KgtkWriter],
                         ulkw: typing.Optional[KgtkWriter],
                         ):
        """
        Process the lift as a merge between two sorted files.

        """
        if self.verbose:
            print("Merging sorted input and label files.", file=self.error_file, flush=True)
        lift_column_idxs: typing.List[int] = self.build_lift_column_idxs(ikr)
        if len(lift_column_idxs) != 1:
            raise ValueError("Expecting exactly one lift_column_idxs, got %d" % len(lift_column_idxs))

        # Setup for language filtering:
        language_filtering: bool = self.languages is not None and len(self.languages) > 0
        allow_all_strings: bool = False
        allow_all_lqstrings: bool = False
        language_filter: typing.List[str] = list()
        language_filter_tuple: typing.Tuple[str, ...] = ()
        if language_filtering:
            for lf in self.languages:
                if lf == 'NONE':
                    if self.prioritize:
                        language_filter.append(lf)
                    else:
                        allow_all_strings = True
                elif lf == 'ANY':
                    if self.prioritize:
                        language_filter.append(lf)
                    else:
                        allow_all_lqstrings = True
                else:
                    language_filter.append("'@" + lf)
            language_filter_tuple = tuple(language_filter)

        ew: KgtkWriter
        lifted_output_column_idxs: typing.List[int]
        ew, lifted_output_column_idxs = self.open_output_writer(ikr, lift_column_idxs)

        new_columns: int = len(ew.column_names) - len(ikr.column_names)
        if new_columns not in (0, 1):
            raise ValueError("Expecting zero or one new columns, got %d" % new_columns)

        lift_column_idx: int = lift_column_idxs[0] # For convenience
        lifted_output_column_idx: int = lifted_output_column_idxs[0] # For convenience

        label_match_column_idx: int
        label_select_column_idx: int
        label_value_column_idx: int
        label_match_column_idx, label_select_column_idx, label_value_column_idx = self.lookup_label_table_idxs(lkr)

        input_select_column_idx: int = -1
        if self.input_select_column_value is not None or self.output_select_column_value is not None:
            input_select_column_idx = self.lookup_input_select_column_idx(ikr)
            
        input_line_count: int = 0
        input_skipped_count: int = 0
        label_line_count: int = 0
        label_match_count: int = 0
        output_line_count: int = 0
        output_modified_count: int = 0

        current_label_row: typing.Optional[typing.List[str]] = None
        more_labels: bool = True
        # Read the first label record.
        try:
            current_label_row = lkr.nextrow()
            label_line_count += 1
        except StopIteration:
            more_labels = False

        # We carry last_value_to_lift and lifted_label_value over
        # iterations in case the input file has multiple records with
        # the same value to lift.
        last_value_to_lift: typing.Optional[str] = None
        lifted_label_value: str = self.default_value

        if self.verbose:
            print("Processing the input records.", file=self.error_file, flush=True)

        output_row: typing.List[str]
        row: typing.List[str]
        for row in ikr:
            input_line_count += 1

            if self.input_select_column_value is not None and input_select_column_idx >= 0:
                # Skip input rows that do not meet the selection criterion.
                if row[input_select_column_idx] != self.input_select_column_value:
                    input_skipped_count += 1
                    if not self.output_only_modified_rows:
                        if new_columns > 0:
                            output_row = row.copy()
                            output_row.append(self.default_value)
                        else:
                            output_row = row
                        ew.write(output_row)
                    continue

            value_to_lift: str = row[lift_column_idx]
            if last_value_to_lift is None or value_to_lift != last_value_to_lift:
                last_value_to_lift = value_to_lift
                lifted_label_value = self.default_value

                # Read label records until we come to the first record that
                # has a node1 value equal to or greater than the value we we want to lift.
                while more_labels and current_label_row is not None and current_label_row[label_match_column_idx] < value_to_lift:
                    if ulkw is not None:
                        ulkw.write(current_label_row)
                    try:
                        current_label_row = lkr.nextrow()
                        label_line_count += 1
                    except StopIteration:
                        more_labels = False
                        break

                # While the label records have node1 values equal to the value we are trying to lift,
                # look for label values from the label file.
                current_priority: int = 9999999 # Large numbers are low priority.
                while more_labels and current_label_row is not None and current_label_row[label_match_column_idx] == value_to_lift:
                    if label_select_column_idx < 0 or current_label_row[label_select_column_idx] == self.label_select_column_value:
                        label_value: str = current_label_row[label_value_column_idx]

                        process_label: bool
                        sigil: str
                        if language_filtering:
                            if len(label_value) == 0:
                                # Empty values are not valid for language filtering.
                                process_label = False
                                
                            elif self.prioritize:
                                # We will not use a label value unless it passes one of
                                # the priority-ordered filters.
                                process_label = False
                                sigil = label_value[0]
                                priority: int
                                lf: str
                                for priority, lf in enumerate(language_filter):
                                    if priority >= current_priority:
                                        # A priori label is higher priority.
                                        break

                                    elif sigil == KgtkFormat.STRING_SIGIL:
                                        # This is a KGTK string without language qualification.
                                        if lf == "NONE":
                                            # We will allow it.
                                            current_priority = priority
                                            process_label = True
                                            break

                                    elif sigil == KgtkFormat.LANGUAGE_QUALIFIED_STRING_SIGIL:
                                        # This is a KGTK language-qualified string.
                                        if lf == "ANY" or label_value.endswith(lf):
                                            # We will allow it.
                                            current_priority = priority
                                            process_label = True
                                            break

                                    else:
                                        # Do not allow values that are neither strings nor lqstrings.
                                        break
                                            
                            else:
                                # Optimized code for non-prioritized langiage selection.
                                sigil = label_value[0]
                                if sigil == KgtkFormat.STRING_SIGIL:
                                    process_label = allow_all_strings

                                elif sigil == KgtkFormat.LANGUAGE_QUALIFIED_STRING_SIGIL:
                                    process_label = allow_all_lqstrings or label_value.endswith(language_filter_tuple)

                                else:
                                    # Do not allow values that are neither strings nor lqstrings.
                                    process_label = False
                        else:
                            process_label = True

                        if process_label:
                            # TODO: is this code positioned correctly?
                            if mlkw is not None:
                                mlkw.write(current_label_row)
                            label_match_count += 1
                                
                            if lifted_label_value != self.default_value:
                                if self.suppress_duplicate_labels:
                                    lifted_label_value = KgtkValue.merge_values(lifted_label_value, label_value)
                                else:
                                    lifted_label_value = KgtkFormat.LIST_SEPARATOR.join((lifted_label_value, label_value))
                            else:
                                lifted_label_value = label_value

                    try:
                        current_label_row = lkr.nextrow()
                        label_line_count += 1
                    except StopIteration:
                        more_labels = False
                        break

            output_row = row.copy()
            modified: bool = False
            if new_columns > 0:
                output_row.append(self.default_value)
            if self.clear_before_lift:
                output_row[lifted_output_column_idx] = self.default_value
            if self.overwrite or output_row[lifted_output_column_idx] != self.default_value:
                if lifted_label_value != self.default_value:
                    if output_row[lifted_output_column_idx] != lifted_label_value:
                        modified = True
                    output_row[lifted_output_column_idx] = lifted_label_value
                    if self.output_select_column_value is not None and input_select_column_idx >= 0:
                        if output_row[input_select_column_idx] != self.output_select_column_value:
                            modified = True
                        output_row[input_select_column_idx] = self.output_select_column_value

            if self.output_only_modified_rows:
                if modified:
                    ew.write(output_row)
                    output_line_count += 1
                    output_modified_count += 1
            else:
                ew.write(output_row)
                output_line_count += 1
                if modified:
                    output_modified_count += 1

            if urkw is not None:
                if not modified:
                    urkw.write(row)

        while more_labels:
            if current_label_row is not None and ulkw is not None:
                ulkw.write(current_label_row)
            try:
                current_label_row = lkr.nextrow()
                label_line_count += 1
            except StopIteration:
                more_labels = False
                break
        lkr.close()

        if self.verbose:
            print("Read %d input records, %d skipped." % (input_line_count, input_skipped_count), file=self.error_file, flush=True)
            print("Read %d label records, %d matched." % (label_line_count, label_match_count), file=self.error_file, flush=True)
            print("Wrote %d output records, %d modified." % (output_line_count, output_modified_count), file=self.error_file, flush=True)
             
        ew.close()

    
    def process(self):
        # Open the input file.
        input_mode: typing.Optional[KgtkReaderMode] = KgtkReaderMode.NONE if self.force_input_mode_none else None
        if self.verbose:
            if self.input_file_path is not None:
                print("Opening the input file: %s" % self.input_file_path, file=self.error_file, flush=True)
            else:
                print("Reading the input data from stdin", file=self.error_file, flush=True)

        ikr: KgtkReader =  KgtkReader.open(self.input_file_path,
                                           error_file=self.error_file,
                                           mode=input_mode,
                                           options=self.input_reader_options,
                                           value_options = self.value_options,
                                           verbose=self.verbose,
                                           very_verbose=self.very_verbose,
        )

        lkr: typing.Optional[KgtkReader] = None
        if self.label_file_path is not None:
            if self.verbose:
                if self.input_file_path is not None:
                    print("Opening the label file: %s" % self.label_file_path, file=self.error_file, flush=True)
                else:
                    print("Reading the label data from stdin", file=self.error_file, flush=True)

            lkr =  KgtkReader.open(self.label_file_path,
                                   error_file=self.error_file,
                                   options=self.label_reader_options,
                                   value_options = self.value_options,
                                   verbose=self.verbose,
                                   very_verbose=self.very_verbose,
            )

        urkw: typing.Optional[KgtkWriter] = None
        if self.unmodified_row_file_path is not None:
            urkw = KgtkWriter.open(ikr.column_names,
                                   self.unmodified_row_file_path,
                                   mode=KgtkWriter.Mode[ikr.mode.name],
                                   require_all_columns=False,
                                   prohibit_extra_columns=True,
                                   fill_missing_columns=True,
                                   use_mgzip=False if self.input_reader_options is None else self.input_reader_options.use_mgzip , # Hack!
                                   mgzip_threads=3 if self.input_reader_options is None else self.input_reader_options.mgzip_threads , # Hack!
                                   gzip_in_parallel=False,
                                   verbose=self.verbose,
                                   very_verbose=self.very_verbose)        
            
        label_column_names: typing.List[str]
        label_file_mode_name: str

        mlkw: typing.Optional[KgtkWriter] = None
        if self.matched_label_file_path is not None:
            label_column_names: typing.List[str]
            label_file_mode_name: str
            if lkr is not None:
                label_column_names = lkr.column_names
                label_file_mode_name = lkr.mode.name
            else:
                label_column_names = ikr.column_names
                label_file_mode_name = ikr.mode.name
            mlkw = KgtkWriter.open(label_column_names,
                                   self.matched_label_file_path,
                                   mode=KgtkWriter.Mode[label_file_mode_name],
                                   require_all_columns=False,
                                   prohibit_extra_columns=True,
                                   fill_missing_columns=True,
                                   use_mgzip=False if self.input_reader_options is None else self.input_reader_options.use_mgzip , # Hack!
                                   mgzip_threads=3 if self.input_reader_options is None else self.input_reader_options.mgzip_threads , # Hack!
                                   gzip_in_parallel=False,
                                   verbose=self.verbose,
                                   very_verbose=self.very_verbose)        
            

        ulkw: typing.Optional[KgtkWriter] = None
        if self.unmatched_label_file_path is not None:
            label_column_names: typing.List[str]
            label_file_mode_name: str
            if lkr is not None:
                label_column_names = lkr.column_names
                label_file_mode_name = lkr.mode.name
            else:
                label_column_names = ikr.column_names
                label_file_mode_name = ikr.mode.name
            ulkw = KgtkWriter.open(label_column_names,
                                   self.unmatched_label_file_path,
                                   mode=KgtkWriter.Mode[label_file_mode_name],
                                   require_all_columns=False,
                                   prohibit_extra_columns=True,
                                   fill_missing_columns=True,
                                   use_mgzip=False if self.input_reader_options is None else self.input_reader_options.use_mgzip , # Hack!
                                   mgzip_threads=3 if self.input_reader_options is None else self.input_reader_options.mgzip_threads , # Hack!
                                   gzip_in_parallel=False,
                                   verbose=self.verbose,
                                   very_verbose=self.very_verbose)        
            
        if self.input_lifting_column_names is not None and len(self.input_lifting_column_names) == 1 and \
           not self.suppress_empty_columns and \
           self.input_is_presorted and \
           self.labels_are_presorted and \
           lkr is not None:
            self.process_as_merge(ikr, lkr, urkw, mlkw, ulkw)
        else:
            self.process_in_memory(ikr, lkr, urkw, mlkw, ulkw)

        if urkw is not None:
            urkw.close()

        if mlkw is not None:
            mlkw.close()

        if ulkw is not None:
            ulkw.close()

def main():
    """
    Test the KGTK lift processor.

    TODO: the unmodified row file path.
    TODO: there are other missing options.
    """
    parser: ArgumentParser = ArgumentParser()

    parser.add_argument(dest="input_file_path", help="The KGTK file with the input data", type=Path, default="-")

    parser.add_argument("-o", "--output-file", dest="output_file_path", help="The KGTK file to write (default=%(default)s).", type=Path, default="-")
    
    parser.add_argument(      "--label-file", dest="label_file_path",
                              help="An optional KGTK file with label records (default=%(default)s).", type=Path, default=None)


    parser.add_argument(      "--input-select-column", "--input-label-column", dest="input_select_column_name",
                              help="If input record selection is enabled by --input-select-value, " +
                              "the name of a column that determines which records received lifted values. " +
                              "The default is the 'label' column or its alias.", default=None)

    parser.add_argument(      "--input-select-value", "--input-label-value", "--target-label-value", dest="input_select_column_value",
                              help="The value in the input select column that identifies a record to receive lifted values. " +
                              "The default is not to perform input record selection, " +
                              "and all input records except label records may receive lifted values. ",
                              default=None)
    
    parser.add_argument(      "--columns-to-lift", dest="input_lifting_column_names",
                              help="The columns for which matching labels are to be lifted. " +
                              "The default is [node1, label, node2] or their aliases.", nargs='*')

    parser.add_argument(      "--columns-to-write", dest="output_lifted_column_names",
                              help="The columns into which to store the lifted values. " +
                              "The default is [node1;label, label;label, node2;label] or their aliases.", nargs='*')

    parser.add_argument(      "--lift-suffix", dest="output_lifted_column_suffix",
                              help="The suffix used for newly created output columns. (default=%(default)s).",
                              default=KgtkLift.DEFAULT_OUTPUT_LIFTED_COLUMN_SUFFIX)

    parser.add_argument(      "--default-value", dest="default_value",
                              help="The value to use if a lifted label is not found. (default=%(default)s)", default="")

    parser.add_argument(      "--update-select-value", "--target-new-label-value", dest="output_select_column_value",
                              help="A new value for the select (label) column for records that received lifted values. " +
                              "The default is not to update the select(label) column.", default=None)
    

    parser.add_argument(      "--label-select-column", "--label-name", dest="label_select_column_name",
                              help="The name of the column that contains a special value that identifies label records. " +
                              "The default is 'label' or its alias.", default=None)

    parser.add_argument("-p", "--label-select-value", "--label-value", "--property", dest="label_select_column_value",
                              help="The special value in the label select column that identifies a label record. " +
                              "(default=%(default)s).", default=KgtkLift.DEFAULT_LABEL_SELECT_COLUMN_VALUE)
    
    parser.add_argument(      "--label-match-column", "--node1-name", dest="label_match_column_name",
                              help="The name of the column in the label records that contains the value " +
                              "that matches the value in a column being lifted in the input records. " +
                              "The default is 'node1' or its alias.", default=None)

    parser.add_argument(      "--label-value-column", "--node2-name", "--lift-from", dest="label_value_column_name",
                              help="The name of the column in the label record that contains the value " +
                              "to be lifted into the input record that is receiving lifted values. " +
                              "The default is 'node2' or its alias.", default=None)

    parser.add_argument(      "--remove-label-records", dest="remove_label_records",
                              help="If true, remove label records from the output. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=True)

    parser.add_argument(      "--sort-lifted-labels", dest="sort_lifted_labels",
                              help="If true, sort lifted labels with lists. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=True)

    parser.add_argument(      "--suppress-duplicate-labels", dest="suppress_duplicate_labels",
                              help="If true, suppress duplicate values in lifted labels with lists (implies sorting). (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=True)

    parser.add_argument(      "--suppress-empty-columns", dest="suppress_empty_columns",
                              help="If true, do not create new columns that would be empty. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--ok-if-no-labels", dest="ok_if_no_labels",
                              help="If true, do not abort if no labels were found. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--prefilter-labels", dest="prefilter_labels",
                              help="If true, read the input file before reading the label file. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--input-file-is-presorted", dest="input_is_presorted",
                              help="If true, the input file is presorted on the column for which values are to be lifted. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--label-file-is-presorted", dest="labels_are_presorted",
                              help="If true, the label file is presorted on the node1 column. (default=%(default)s).",
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
                              type=optional_bool, nargs='?', const=True, default=True)

    KgtkReader.add_debug_arguments(parser)
    # TODO: seperate reader options for the label file.
    KgtkReaderOptions.add_arguments(parser, mode_options=True)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, who="input", defaults=False)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, who="label", defaults=False)
    KgtkValueOptions.add_arguments(parser)

    args: Namespace = parser.parse_args()

    error_file: typing.TextIO = sys.stdout if args.errors_to_stdout else sys.stderr

    # Build the option structures.                                                                                                                          
    input_reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs, who="input", fallback=True)
    label_reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs, who="label", fallback=True)
    value_options: KgtkValueOptions = KgtkValueOptions.from_args(args)

    # Show the final option structures for debugging and documentation.   
    if args.show_options:
        print("input: %s" % str(args.input_file_path), file=error_file, flush=True)
        if args.label_file_path is not None:
            print("--label-file=%s" % str(args.label_file_path), file=error_file, flush=True)
        print("--output-file=%s" % str(args.output_file_path), file=error_file, flush=True)

        if args.input_select_column_name is not None:
            print("--input-select-column=%s" % args.input_select_column_name, file=error_file, flush=True)
        if args.input_select_column_value is not None:
            print("--input-select-value=%s" % args.input_select_column_value, file=error_file, flush=True)
        if args.input_lifting_column_names is not None and len(args.input_lifting_column_names) > 0:
            print("--columns-to-lift %s" % " ".join(args.input_lifting_column_names), file=error_file, flush=True)
        if args.output_lifted_column_names is not None and len(args.output_lifted_column_names) > 0:
            print("--columns-to-write %s" % " ".join(args.output_lifted_column_names), file=error_file, flush=True)

        print("--lift-suffix=%s" % args.output_lifted_column_suffix, file=error_file, flush=True)
        if args.output_select_column_value is not None:
            print("--update-label-value=%s" % args.output_select_column_value, file=error_file, flush=True)

        if args.label_select_column_name is not None:
            print("--label-select-column=%s" % args.label_select_column_name, file=error_file, flush=True)
        if args.label_select_column_value is not None:
            print("--label-select-value=%s" % args.label_select_column_value, file=error_file, flush=True)
        if args.label_match_column_name is not None:
            print("--label-match-column=%s" % args.label_match_column_name, file=error_file, flush=True)
        if args.label_value_column_name is not None:
            print("--label-value-column=%s" % args.label_value_column_name, file=error_file, flush=True)


        print("--default-value=%s" % repr(args.default_value))
        print("--remove-label-records=%s" % repr(args.remove_label_records))
        print("--sort-lifted-labels-labels=%s" % repr(args.sort_lifted_labels))
        print("--suppress-duplicate-labels=%s" % repr(args.suppress_duplicate_labels))
        print("--suppress-empty-columns=%s" % repr(args.suppress_empty_columns))
        print("--ok-if-no-labels=%s" % repr(args.ok_if_no_labels))
        print("--prefilter-labels=%s" % repr(args.prefilter_labels))
        print("--input-file-is-presorted=%s" % repr(args.input_is_presorted))
        print("--label-file-is-presorted=%s" % repr(args.labels_are_presorted))
        print("--clear-before-lift=%s" % repr(args.clear_before_lift))
        print("--overwrite=%s" % repr(args.overwrite))
        print("--output-only-modified-rows=%s" % repr(args.output_only_modified_rows))
        
        input_reader_options.show(out=error_file, who="input")
        label_reader_options.show(out=error_file, who="label")
        value_options.show(out=error_file)

    kl: KgtkLift = KgtkLift(
        input_file_path=args.input_file_path,
        label_file_path=args.label_file_path,
        output_file_path=args.output_file_path,

        input_select_column_name=args.input_select_column_name,
        input_select_column_value=args.input_select_column_value, 
        input_lifting_column_names=args.input_lifting_column_names,

        output_select_column_value=args.output_select_column_value, 
        output_lifted_column_suffix=args.output_lifted_column_suffix,
        output_lifted_column_names=args.output_lifted_column_names,

        label_select_column_name=args.label_select_column_name,
        label_select_column_value=args.label_select_column_value,
        label_match_column_name=args.label_match_column_name,
        label_value_column_name=args.label_value_column_name,

        default_value=args.default_value,
        
        remove_label_records=args.remove_label_records,
        sort_lifted_labels=args.sort_lifted_labels,
        suppress_duplicate_labels=args.suppress_duplicate_labels,
        suppress_empty_columns=args.suppress_empty_columns,
        ok_if_no_labels=args.ok_if_no_labels,
        prefilter_labels=args.prefilter_labels,
        input_is_presorted=args.input_is_presorted,
        labels_are_presorted=args.labels_are_presorted,

        clear_before_lift=args.clear_before_lift,
        overwrite=args.overwrite,

        input_reader_options=input_reader_options,
        label_reader_options=label_reader_options,
        value_options=value_options,
        error_file=error_file,
        verbose=args.verbose,
        very_verbose=args.very_verbose)

    kl.process()

if __name__ == "__main__":
    main()
