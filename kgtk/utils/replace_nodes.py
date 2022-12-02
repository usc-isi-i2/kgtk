from pathlib import Path
import sys

from kgtk.exceptions import KGTKException
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
from kgtk.io.kgtkwriter import KgtkWriter
from kgtk.value.kgtkvalueoptions import KgtkValueOptions
from typing import TextIO, Optional, MutableMapping, List


class ReplaceNodes(object):
    def __init__(self,
                 input_kgtk_file: Path,
                 output_kgtk_file: Path,
                 mapping_kgtk_file: Path,
                 unmodified_edges_kgtk_file: Path = None,
                 activated_mapping_kgtk_file: Path = None,
                 rejected_mapping_kgtk_file: Path = None,
                 input_reader_options: KgtkReaderOptions = None,
                 mapping_reader_options: KgtkReaderOptions = None,
                 value_options: KgtkValueOptions = None,
                 confidence_column_name: str = 'confidence',
                 require_confidence: bool = False,
                 default_confidence_str: str = None,
                 confidence_threshold: float = 1.0,
                 same_as_item_label: str = 'same_as_item',
                 same_as_property_label: str = 'same_as_property',
                 allow_exact_duplicates: bool = False,
                 allow_idempotent_mapping: bool = False,
                 split_output_mode: bool = False,
                 modified_pattern: str = 'node1|label|node2',
                 node1_column_name: str = 'node1',
                 label_column_name: str = 'label',
                 node2_column_name: str = 'node2',
                 mapping_rule_mode: str = 'normal',  # normal|same-as-item|same-as-property"
                 mapping_node1_column_name: str = 'node1',
                 mapping_label_column_name: str = 'label',
                 mapping_node2_column_name: str = 'node2',
                 error_file: TextIO = sys.stderr,
                 show_options: bool = False,
                 verbose: bool = False,
                 very_verbose: bool = False,
                 ):
        self.input_kgtk_file = input_kgtk_file
        self.output_kgtk_file = output_kgtk_file
        self.mapping_kgtk_file = mapping_kgtk_file
        self.unmodified_edges_kgtk_file = unmodified_edges_kgtk_file
        self.activated_mapping_kgtk_file = activated_mapping_kgtk_file
        self.rejected_mapping_kgtk_file = rejected_mapping_kgtk_file
        self.input_reader_options = input_reader_options
        self.mapping_reader_options = mapping_reader_options
        self.value_options = value_options
        self.confidence_column_name = confidence_column_name
        self.require_confidence = require_confidence
        self.default_confidence_str = default_confidence_str
        self.confidence_threshold = confidence_threshold
        self.same_as_item_label = same_as_item_label
        self.same_as_property_label = same_as_property_label
        self.allow_exact_duplicates = allow_exact_duplicates
        self.allow_idempotent_mapping = allow_idempotent_mapping
        self.split_output_mode = split_output_mode
        self.modified_pattern = modified_pattern
        self.node1_column_name = node1_column_name
        self.label_column_name = label_column_name
        self.node2_column_name = node2_column_name
        self.mapping_rule_mode = mapping_rule_mode
        self.mapping_node1_column_name = mapping_node1_column_name
        self.mapping_label_column_name = mapping_label_column_name
        self.mapping_node2_column_name = mapping_node2_column_name
        self.error_file = error_file
        self.show_options = show_options
        self.verbose = verbose
        self.very_verbose = very_verbose

    def process(self):
        if self.show_options:
            print("--input-file=%s" % repr(str(self.input_kgtk_file)), file=self.error_file, flush=True)
            print("--output-file=%s" % repr(str(self.output_kgtk_file)), file=self.error_file, flush=True)
            print("--mapping-file=%s" % repr(str(self.mapping_kgtk_file)), file=self.error_file, flush=True)
            if self.unmodified_edges_kgtk_file is not None:
                print("--unmodified-edges-file=%s" % repr(str(self.unmodified_edges_kgtk_file)), file=self.error_file,
                      flush=True)
            if self.activated_mapping_kgtk_file is not None:
                print("--activated-mapping-edges-file=%s" % repr(str(self.activated_mapping_kgtk_file)),
                      file=self.error_file,
                      flush=True)
            if self.rejected_mapping_kgtk_file is not None:
                print("--rejected-mapping-edges-file=%s" % repr(str(self.rejected_mapping_kgtk_file)),
                      file=self.error_file,
                      flush=True)

            print("--confidence-column=%s" % repr(self.confidence_column_name), file=self.error_file, flush=True)
            print("--require-confidence=%s" % repr(self.require_confidence), file=self.error_file, flush=True)
            if self.default_confidence_str is not None:
                print("--default-confidence-value=%s" % self.default_confidence_str, file=self.error_file, flush=True)
            print("--threshold=%f" % self.confidence_threshold, file=self.error_file, flush=True)

            print("--same-as-item-label=%s" % repr(self.same_as_item_label), file=self.error_file, flush=True)
            print("--same-as-property-label=%s" % repr(self.same_as_property_label), file=self.error_file, flush=True)
            print("--allow-exact-duplicates=%s" % repr(self.allow_exact_duplicates), file=self.error_file, flush=True)
            print("--allow-idempotent-actions=%s" % repr(self.allow_idempotent_mapping), file=self.error_file,
                  flush=True)

            print("--split-output-mode=%s" % repr(self.split_output_mode), file=self.error_file, flush=True)
            print("--modified-pattern=%s" % repr(self.modified_pattern), file=self.error_file, flush=True)

            if self.node1_column_name is not None:
                print("--node1-column-=%s" % repr(self.node1_column_name), file=self.error_file, flush=True)
            if self.label_column_name is not None:
                print("--label-column-=%s" % repr(self.label_column_name), file=self.error_file, flush=True)
            if self.node2_column_name is not None:
                print("--node2-column-=%s" % repr(self.node2_column_name), file=self.error_file, flush=True)
            print("--mapping-rule-mode=%s" % repr(self.mapping_rule_mode), file=self.error_file, flush=True)
            if self.mapping_node1_column_name is not None:
                print("--mapping-node1-column-=%s" % repr(self.mapping_node1_column_name), file=self.error_file,
                      flush=True)
            if self.mapping_label_column_name is not None:
                print("--mapping-label-column-=%s" % repr(self.mapping_label_column_name), file=self.error_file,
                      flush=True)
            if self.mapping_node2_column_name is not None:
                print("--mapping-node2-column-=%s" % repr(self.mapping_node2_column_name), file=self.error_file,
                      flush=True)

            self.input_reader_options.show(out=self.error_file, who="input")
            self.mapping_reader_options.show(out=self.error_file, who="mapping")
            self.value_options.show(out=self.error_file)
            print("=======", file=self.error_file, flush=True)

        default_confidence_value: Optional[float] = None
        if self.default_confidence_str is not None:
            try:
                default_confidence_value = float(self.default_confidence_str)
            except:
                raise KGTKException("--default-confidence-value=%s is invalid" % repr(self.default_confidence_str))

        try:

            if self.verbose:
                print("Opening the mapping file %s." % repr(str(self.mapping_kgtk_file)), file=self.error_file,
                      flush=True)
            mkr: KgtkReader = KgtkReader.open(self.mapping_kgtk_file,
                                              options=self.mapping_reader_options,
                                              value_options=self.value_options,
                                              error_file=self.error_file,
                                              verbose=self.verbose,
                                              very_verbose=self.very_verbose,
                                              )
            trouble = False
            mapping_node1_idx: int = mkr.get_node1_column_index(self.mapping_node1_column_name)
            mapping_label_idx: int = mkr.get_label_column_index(self.mapping_label_column_name)
            mapping_node2_idx: int = mkr.get_node2_column_index(self.mapping_node2_column_name)
            if mapping_node1_idx < 0:
                trouble = True
                print("Error: Cannot find the mapping file node1 column.", file=self.error_file, flush=True)
            if mapping_label_idx < 0 and self.mapping_rule_mode == "normal":
                trouble = True
                print("Error: Cannot find the mapping file label column.", file=self.error_file, flush=True)
            if mapping_node2_idx < 0:
                trouble = True
                print("Error: Cannot find the mapping file node2 column.", file=self.error_file, flush=True)
            if trouble:
                # Clean up:
                mkr.close()
                raise KGTKException("Missing columns in the mapping file.")
            confidence_column_idx: int = mkr.column_name_map.get(self.confidence_column_name, -1)
            if self.require_confidence and confidence_column_idx < 0:
                mkr.close()
                raise KGTKException("The mapping file does not have a confidence column, and confidence is required.")

            rmkw: Optional[KgtkWriter] = None
            if self.rejected_mapping_kgtk_file is not None:
                if self.verbose:
                    print("Opening the rejected mapping edges file %s." % repr(str(self.rejected_mapping_kgtk_file)),
                          file=self.error_file, flush=True)
                rmkw = KgtkWriter.open(mkr.column_names,
                                       self.rejected_mapping_kgtk_file,
                                       mode=KgtkWriter.Mode[mkr.mode.name],
                                       use_mgzip=self.input_reader_options.use_mgzip,  # Hack!
                                       mgzip_threads=self.input_reader_options.mgzip_threads,  # Hack!
                                       error_file=self.error_file,
                                       verbose=self.verbose,
                                       very_verbose=self.very_verbose)

            # Mapping structures:
            item_map: MutableMapping[str, str] = dict()
            item_line_map: MutableMapping[str, int] = dict()
            property_map: MutableMapping[str, str] = dict()
            property_line_map: MutableMapping[str, int] = dict()

            mapping_rows: MutableMapping[int, List[str]] = dict()
            activated_mapping_rows: MutableMapping[int, List[str]] = dict()

            # Read the mapping file.
            if self.verbose:
                print("Processing the mapping file.", file=self.error_file, flush=True)
            mapping_confidence_exclusions: int = 0
            mapping_idempotent_exclusions: int = 0
            mapping_errors: int = 0
            mapping_line_number: int = 0
            mrow: List[str]
            for mrow in mkr:
                mapping_line_number += 1
                mapping_node1: str = mrow[mapping_node1_idx]
                mapping_label: str = mrow[mapping_label_idx] if self.mapping_rule_mode == "normal" else ""
                mapping_node2: str = mrow[mapping_node2_idx]
                mapping_confidence: Optional[float] = default_confidence_value
                if confidence_column_idx >= 0:
                    confidence_value_str: str = mrow[confidence_column_idx]
                    if len(confidence_value_str) == 0:
                        if self.require_confidence:
                            print("In line %d of the mapping file: the required confidence value is missing" % (
                                mapping_line_number),
                                  file=self.error_file, flush=True)
                            mapping_errors += 1
                            continue
                    else:
                        try:
                            mapping_confidence = float(confidence_value_str)
                        except ValueError:
                            print("In line %d of the mapping file: cannot parse confidence value %s" % (
                                mapping_line_number, repr(mrow[confidence_column_idx])),
                                  file=self.error_file, flush=True)
                            mapping_errors += 1
                            continue
                if mapping_confidence is not None and mapping_confidence < self.confidence_threshold:
                    mapping_confidence_exclusions += 1
                    if rmkw is not None:
                        rmkw.write(mrow)
                    continue

                if mapping_node1 == mapping_node2 and not self.allow_idempotent_mapping:
                    mapping_idempotent_exclusions += 1
                    continue

                if self.mapping_rule_mode == "same-as-item" or mapping_label == self.same_as_item_label:
                    if mapping_node1 in item_map:
                        if mapping_node2 != item_map[mapping_node1] or not self.allow_exact_duplicates:
                            print("Duplicate %s for %s at mapping file line %d, originally in line %d" % (mapping_label,
                                                                                                          repr(
                                                                                                              mapping_node1),
                                                                                                          mapping_line_number,
                                                                                                          item_line_map[
                                                                                                              mapping_node1]),
                                  file=self.error_file, flush=True)
                            mapping_errors += 1
                        continue

                    item_map[mapping_node1] = mapping_node2
                    item_line_map[mapping_node1] = mapping_line_number
                    mapping_rows[mapping_line_number] = mrow.copy()

                elif self.mapping_rule_mode == "same-as-property" or mapping_label == self.same_as_property_label:
                    if mapping_node1 in property_map:
                        if mapping_node2 != property_map[mapping_node1] or not self.allow_exact_duplicates:
                            print("Duplicate %s for %s at mapping file line %d, originally in line %d" % (mapping_label,
                                                                                                          repr(
                                                                                                              mapping_node1),
                                                                                                          mapping_line_number,
                                                                                                          property_line_map[
                                                                                                              mapping_node1]),
                                  file=self.error_file, flush=True)
                            mapping_errors += 1
                        continue
                    property_map[mapping_node1] = mapping_node2
                    property_line_map[mapping_node1] = mapping_line_number
                    mapping_rows[mapping_line_number] = mrow.copy()

                else:
                    print("Unknown mapping action %s at line %d of mapping file %s" % (mapping_label,
                                                                                       mapping_line_number,
                                                                                       repr(
                                                                                           str(self.mapping_kgtk_file))),
                          file=self.error_file, flush=True)
                    mapping_errors += 1
                    continue

            # Close the mapping file.
            mkr.close()
            if rmkw is not None:
                rmkw.close()

            if mapping_errors > 0:
                raise KGTKException(
                    "%d errors detected in the mapping file %s" % (mapping_errors, repr(str(self.mapping_kgtk_file))))

            if len(item_map) == 0 and len(property_map) == 0:
                raise KGTKException("Nothing read from the mapping file %s" % repr(str(self.mapping_kgtk_file)))

            if self.verbose:
                print(
                    "%d mapping lines, %d excluded for confidence, %d excluded for idempotency." % (mapping_line_number,
                                                                                                    mapping_confidence_exclusions,
                                                                                                    mapping_idempotent_exclusions),
                    file=self.error_file, flush=True)
                print("%d item mapping rules." % len(item_map), file=self.error_file, flush=True)
                print("%d property mapping rules." % len(property_map), file=self.error_file, flush=True)

            if self.verbose:
                print("Opening the input file %s." % repr(str(self.input_kgtk_file)), file=self.error_file, flush=True)
            ikr: KgtkReader = KgtkReader.open(self.input_kgtk_file,
                                              options=self.input_reader_options,
                                              value_options=self.value_options,
                                              error_file=self.error_file,
                                              verbose=self.verbose,
                                              very_verbose=self.very_verbose,
                                              )
            trouble = False
            input_node1_idx: int = ikr.get_node1_column_index(self.node1_column_name)
            input_label_idx: int = ikr.get_label_column_index(self.label_column_name)
            input_node2_idx: int = ikr.get_node2_column_index(self.node2_column_name)
            if input_node1_idx < 0 and self.mapping_rule_mode in ["normal", "same-as-item"]:
                trouble = True
                print("Error: Cannot find the input file node1 column.", file=self.error_file, flush=True)
            if input_label_idx < 0 and self.mapping_rule_mode in ["normal", "same-as-property"]:
                trouble = True
                print("Error: Cannot find the input file label column.", file=self.error_file, flush=True)
            if input_node2_idx < 0 and self.mapping_rule_mode in ["normal", "same-as-item"]:
                trouble = True
                print("Error: Cannot find the input file node2 column.", file=self.error_file, flush=True)
            if trouble:
                # Clean up:
                ikr.close()
                raise KGTKException("Missing columns in the input file.")

            okw: KgtkWriter = KgtkWriter.open(ikr.column_names,
                                              self.output_kgtk_file,
                                              mode=KgtkWriter.Mode[ikr.mode.name],
                                              use_mgzip=self.input_reader_options.use_mgzip,  # Hack!
                                              mgzip_threads=self.input_reader_options.mgzip_threads,  # Hack!
                                              error_file=self.error_file,
                                              verbose=self.verbose,
                                              very_verbose=self.very_verbose)

            uekw: Optional[KgtkWriter] = None
            if self.unmodified_edges_kgtk_file is not None:
                if self.verbose:
                    print("Opening the unmodified edges file %s." % repr(str(self.unmodified_edges_kgtk_file)),
                          file=self.error_file, flush=True)
                uekw = KgtkWriter.open(ikr.column_names,
                                       self.unmodified_edges_kgtk_file,
                                       mode=KgtkWriter.Mode[ikr.mode.name],
                                       use_mgzip=self.input_reader_options.use_mgzip,  # Hack!
                                       mgzip_threads=self.input_reader_options.mgzip_threads,  # Hack!
                                       error_file=self.error_file,
                                       verbose=self.verbose,
                                       very_verbose=self.very_verbose)

            amkw: Optional[KgtkWriter] = None
            if self.activated_mapping_kgtk_file is not None:
                if self.verbose:
                    print("Opening the activated mapping edges file %s." % repr(str(self.activated_mapping_kgtk_file)),
                          file=self.error_file, flush=True)
                amkw = KgtkWriter.open(mkr.column_names,
                                       self.activated_mapping_kgtk_file,
                                       mode=KgtkWriter.Mode[mkr.mode.name],
                                       use_mgzip=self.input_reader_options.use_mgzip,  # Hack!
                                       mgzip_threads=self.input_reader_options.mgzip_threads,  # Hack!
                                       error_file=self.error_file,
                                       verbose=self.verbose,
                                       very_verbose=self.very_verbose)

            # Process each row of the input file.
            if self.verbose:
                print("Processing the input file.", file=self.error_file, flush=True)
            input_count: int = 0
            modified_edge_count: int = 0
            unmodified_edge_count: int = 0
            row: List[str]
            for row in ikr:
                input_count += 1
                newrow: List[str] = row.copy()

                modified_node1: bool = False
                modified_node2: bool = False
                modified_label: bool = False

                if self.mapping_rule_mode in ["normal", "same-as-item"]:
                    input_node1: str = row[input_node1_idx]
                    if input_node1 in item_map:
                        newrow[input_node1_idx] = item_map[input_node1]
                        modified_node1 = True
                        if amkw is not None:
                            mapping_line_number = item_line_map[input_node1]
                            if mapping_line_number not in activated_mapping_rows:
                                activated_mapping_rows[mapping_line_number] = mapping_rows[mapping_line_number]

                    input_node2: str = row[input_node2_idx]
                    if input_node2 in item_map:
                        newrow[input_node2_idx] = item_map[input_node2]
                        modified_node2 = True
                        if amkw is not None:
                            mapping_line_number = item_line_map[input_node2]
                            if mapping_line_number not in activated_mapping_rows:
                                activated_mapping_rows[mapping_line_number] = mapping_rows[mapping_line_number]

                if self.mapping_rule_mode in ["normal", "same-as-property"]:
                    input_label: str = row[input_label_idx]
                    if input_label in property_map:
                        newrow[input_label_idx] = property_map[input_label]
                        modified_label = True
                        if amkw is not None:
                            mapping_line_number = property_line_map[input_label]
                            if mapping_line_number not in activated_mapping_rows:
                                activated_mapping_rows[mapping_line_number] = mapping_rows[mapping_line_number]

                modified: bool
                if self.modified_pattern == "node1|label|node2":
                    modified = modified_node1 or modified_label or modified_node2
                elif self.modified_pattern == "node1|label":
                    modified = modified_node1 or modified_label
                elif self.modified_pattern == "node1|node2":
                    modified = modified_node1 or modified_node2
                elif self.modified_pattern == "label|node2":
                    modified = modified_label or modified_node2
                elif self.modified_pattern == "node1":
                    modified = modified_node1
                elif self.modified_pattern == "label":
                    modified = modified_label
                elif self.modified_pattern == "node2":
                    modified = modified_node2
                elif self.modified_pattern == "node1&label&node2":
                    modified = modified_node1 and modified_label and modified_node2
                elif self.modified_pattern == "node1&label":
                    modified = modified_node1 and modified_label
                elif self.modified_pattern == "node1&node2":
                    modified = modified_node1 and modified_node2
                elif self.modified_pattern == "label&node2":
                    modified = modified_label and modified_node2
                else:
                    raise KGTKException("Unrecognized modification test pattern %s" % repr(self.modified_pattern))

                if modified:
                    modified_edge_count += 1
                    okw.write(newrow)
                else:
                    unmodified_edge_count += 1
                    if uekw is not None:
                        uekw.write(row)
                    if not self.split_output_mode:
                        okw.write(row)

            # Done!
            ikr.close()
            okw.close()

            if self.verbose:
                print("%d edges read. %d modified, %d unmodified." % (
                    input_count, modified_edge_count, unmodified_edge_count), file=self.error_file, flush=True)

            if uekw is not None:
                uekw.close()

            if amkw is not None:
                activated_count: int = 0
                for mapping_line_number in sorted(activated_mapping_rows.keys()):
                    amkw.write(activated_mapping_rows[mapping_line_number])
                    activated_count += 1
                amkw.close()

                if self.verbose:
                    print("%d activated mapping edges" % activated_count, file=self.error_file, flush=True)



        except SystemExit as e:
            raise KGTKException("Exit requested")
        except Exception as e:
            raise KGTKException(str(e))
