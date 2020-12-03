"""Copy records from the first ("left") KGTK file to the output file, if
a match is made with records in the second ("right") KGTK input file.

The fields to match may be supplied by the user.  If not supplied,
the following defaults will be used:

Left    Right   Key fields
edge    edge    left.node1 = right.node1 and left.label=right.label and left.node2=right.node2
node    node    left.id = right.id
edge    node    left.node1 = right.id
node    edge    right.id = left.node1

Note: By default, this implementation builds im-memory sets of all the key
values in the second file (the filter file). Optionally, it will cache the
first file (the input file) instead.  If both input files are presorted,
neither file will be cached.

Note: By default, input records are passed in order to the output file.  When
the input file is cached, the output records are order by key value (alpha
sort), then by input order.  However, --preserve-order can be used to retain
the input file's order in the output file.

TODO: Study the time and space tradeoff between process_cacheing_input(...)
and process_cacheing_input_preserving_order(...).  Perhaps there's no reason
for both algorithms?

TODO: The join logic for inverted tests is questionable.

TODO: The join output file gets incomplete output except when using presorted files.
"""

from argparse import ArgumentParser, Namespace
import attr
from pathlib import Path
import sys
import typing

from kgtk.kgtkformat import KgtkFormat
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
from kgtk.io.kgtkwriter import KgtkWriter
from kgtk.join.kgtkmergecolumns import KgtkMergeColumns
from kgtk.utils.argparsehelpers import optional_bool
from kgtk.value.kgtkvalueoptions import KgtkValueOptions

@attr.s(slots=True, frozen=True)
class KgtkIfExists(KgtkFormat):
    input_file_path: typing.Optional[Path] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Path)))
    input_keys: typing.Optional[typing.List[str]] = attr.ib(validator=attr.validators.optional(attr.validators.deep_iterable(member_validator=attr.validators.instance_of(str),
                                                                                                                            iterable_validator=attr.validators.instance_of(list))))

    filter_file_path: Path = attr.ib(validator=attr.validators.instance_of(Path))
    filter_keys: typing.Optional[typing.List[str]] = attr.ib(validator=attr.validators.optional(attr.validators.deep_iterable(member_validator=attr.validators.instance_of(str),
                                                                                                                             iterable_validator=attr.validators.instance_of(list))))

    output_file_path: typing.Optional[Path] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Path)), default=None)
    reject_file_path: typing.Optional[Path] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Path)), default=None)

    matched_filter_file_path: typing.Optional[Path] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Path)), default=None)
    unmatched_filter_file_path: typing.Optional[Path] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Path)), default=None)

    join_file_path: typing.Optional[Path] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Path)), default=None)

    # left_join == False and right_join == False: inner join
    # left_join == True and right_join == False: left join
    # left_join == False and right_join == True: right join
    # left_join = True and right_join == True: outer join
    left_join: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    right_join: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    # The prefix applied to left and right file column names in the output file:
    input_prefix: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    filter_prefix: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)

    # When True, send the results of the join to the primary output stream.
    join_output: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    # When True, send the filter line to join output before the input line on first filter match.
    right_first: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    # The field separator used in multifield joins.
    field_separator: str = attr.ib(validator=attr.validators.instance_of(str), default=KgtkFormat.KEY_FIELD_SEPARATOR)

    invert: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    cache_input: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    preserve_order: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    presorted: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    # TODO: find working validators
    # value_options: typing.Optional[KgtkValueOptions] = attr.ib(attr.validators.optional(attr.validators.instance_of(KgtkValueOptions)), default=None)
    input_reader_options: typing.Optional[KgtkReaderOptions]= attr.ib(default=None)
    filter_reader_options: typing.Optional[KgtkReaderOptions]= attr.ib(default=None)
    value_options: typing.Optional[KgtkValueOptions] = attr.ib(default=None)

    show_version: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    error_file: typing.TextIO = attr.ib(default=sys.stderr)
    verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    very_verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    FIELD_SEPARATOR_DEFAULT: str = KgtkFormat.KEY_FIELD_SEPARATOR
    
    def get_primary_key_column(self, kr: KgtkReader, who: str)->typing.List[int]:
        if kr.is_node_file:
            if kr.id_column_idx < 0:
                raise ValueError("The id column is missing from the %s node file." % who)
            return [ kr.id_column_idx ]
        elif kr.is_edge_file:
            if kr.node1_column_idx < 0:
                raise ValueError("The node1 column is missing from the %s node file." % who)
            return [ kr.node1_column_idx ]
        else:
            raise ValueError("The %s file is neither edge nor node." % who)

    def get_edge_key_columns(self, kr: KgtkReader, who: str)-> typing.List[int]:
        if not kr.is_edge_file:
            raise ValueError("get_edge_keys called on %s at wrong time." % who)
        if kr.node1_column_idx < 0:
            raise ValueError("The node1 column is missing from the %s edge file." % who)
        if kr.label_column_idx < 0:
            raise ValueError("The label column is missing from the %s edge file." % who)
        if kr.node2_column_idx < 0:
            raise ValueError("The node2 column is missing from the %s edge file." % who)
        return [ kr.node1_column_idx, kr.label_column_idx, kr.node2_column_idx ]

    def get_supplied_key_columns(self, supplied_keys: typing.List[str], kr: KgtkReader, who: str)->typing.List[int]:
        result: typing.List[int] = [ ]
        key: str
        for key in supplied_keys:
            if key not in kr.column_name_map:
                raise ValueError("Column %s is not in the %s file" % (key, who))
            result.append(kr.column_name_map[key])
        return result
    
    def get_key_columns(self, supplied_keys: typing.Optional[typing.List[str]], kr: KgtkReader, other_kr: KgtkReader, who: str)->typing.List[int]:
        if supplied_keys is not None and len(supplied_keys) > 0:
            return self.get_supplied_key_columns(supplied_keys, kr, who)

        if not (kr.is_node_file or kr.is_edge_file):
            raise ValueError("The %s file is a quasi-KGTK file.  Please supply its keys." % who)

        if kr.is_node_file or other_kr.is_node_file:
            return self.get_primary_key_column(kr, who)

        return self.get_edge_key_columns(kr, who)

    def build_key(self, row: typing.List[str], key_columns: typing.List[int])->str:
        key: str = ""
        idx: int
        first: bool = True
        for idx in key_columns:
            if first:
                first = False
            else:
                key += self.field_separator
            key += row[idx]
        return key

    def extract_key_set(self, kr: KgtkReader, who: str, key_columns: typing.List[int])->typing.Set[str]:
        key_set: typing.Set[str] = set()
        row: typing.List[str]
        for row in kr:
            key_set.add(self.build_key(row, key_columns))
        return key_set

    def extract_key_set_and_cache(self, kr: KgtkReader, who: str, key_columns: typing.List[int])->typing.Tuple[typing.Set[str], typing.List[typing.List[str]]]:
        key_set: typing.Set[str] = set()
        cache: typing.List[typing.List[str]] = [ ]
        row: typing.List[str]
        for row in kr:
            key_set.add(self.build_key(row, key_columns))
            cache.append(row)
        return key_set, cache

    def process_cacheing_filter(self,
                                input_kr: KgtkReader,
                                filter_kr: KgtkReader,
                                input_key_columns: typing.List[int],
                                filter_key_columns: typing.List[int],
                                ew: typing.Optional[KgtkWriter] = None,
                                rew: typing.Optional[KgtkWriter] = None,
                                mfew: typing.Optional[KgtkWriter] = None, # matched filters
                                ufew: typing.Optional[KgtkWriter] = None, # unmatched filters
                                jw: typing.Optional[KgtkWriter] = None, # unmatched filters
                                join_shuffle_list: typing.Optional[typing.List[int]] = None, # for join output
                                ):
        # TODO: write the matched filter records into the join file.
        # TODO: interleave the filter records in the join file.
        if self.verbose:
            print("Processing by cacheing the filter file's key set.", file=self.error_file, flush=True)

        if self.verbose:
            print("Building the filter key set from %s" % self.filter_file_path, file=self.error_file, flush=True)
        key_set: typing.Set[str]
        filter_cache: typing.List[typing.List[str]]
        unmatched_key_set: typing.Optional[typing.Set[str]]
        if mfew is None  and ufew is None and jw is None:
            key_set = self.extract_key_set(filter_kr, "filter", filter_key_columns)
            filter_cache = list()
            unmatched_key_set = None
        else:
            key_set, filter_cache = self.extract_key_set_and_cache(filter_kr, "filter", filter_key_columns)
            unmatched_key_set = set(key_set)
            
        if self.verbose or self.very_verbose:
            print("There are %d entries in the filter key set." % len(key_set), file=self.error_file, flush=True)
            if self.very_verbose:
                print("Keys: %s" % " ".join(key_set), file=self.error_file, flush=True)

        if self.verbose:
            print("Filtering records from %s" % self.input_file_path, file=self.error_file, flush=True)
        input_line_count: int = 0
        accept_line_count: int = 0
        reject_line_count: int = 0
        joined_line_count: int = 0

        # TODO: join these two code paths using xor?
        row: typing.List[str]
        input_key: str
        if self.invert:
            for row in input_kr:
                input_line_count += 1
                input_key = self.build_key(row, input_key_columns)
                if input_key not in key_set:
                    accept_line_count += 1
                    if ew is not None:
                        ew.write(row)
                    if jw is not None and not self.join_output:
                        joined_line_count += 1
                        jw.write(row)
                else:
                    reject_line_count += 1
                    if rew is not None:
                        rew.write(row)
                    if self.left_join:
                        if self.join_output and ew is not None:
                            joined_line_count += 1
                            ew.write(row)
                        elif jw is not None:
                            joined_line_count += 1
                            jw.write(row)
                    if unmatched_key_set is not None:
                        unmatched_key_set.discard(input_key)
        else:
            for row in input_kr:
                input_line_count += 1
                input_key = self.build_key(row, input_key_columns)
                if input_key in key_set:
                    accept_line_count += 1
                    if ew is not None:
                        ew.write(row)
                    if jw is not None and not self.join_output:
                        joined_line_count += 1
                        jw.write(row)
                    if unmatched_key_set is not None:
                        unmatched_key_set.discard(input_key)
                else:
                    reject_line_count += 1
                    if rew is not None:
                        rew.write(row)
                    if self.left_join:
                        if self.join_output and ew is not None:
                            joined_line_count += 1
                            ew.write(row)
                        elif jw is not None:
                            joined_line_count += 1
                            jw.write(row)

        if self.verbose:
            print("Read %d input records, accepted %d records, rejected %d records." % (input_line_count, accept_line_count, reject_line_count),
                  file=self.error_file, flush=True)

        if unmatched_key_set is not None:
            if self.verbose:
                print("There were %d matched filter keys, %d unmatched filter keys." % (len(key_set) - len(unmatched_key_set),
                                                                                        len(unmatched_key_set)),
                      file=self.error_file, flush=True)

            filter_line_count: int = 0
            matched_filter_line_count: int = 0
            unmatched_filter_line_count: int = 0
            for row in filter_cache:
                filter_line_count += 1
                if self.build_key(row, filter_key_columns) in unmatched_key_set:
                    unmatched_filter_line_count += 1
                    if ufew is not None:
                        ufew.write(row)
                    if self.right_join:
                        if self.join_output and ew is not None:
                            joined_line_count += 1
                            ew.write(row, shuffle_list=join_shuffle_list)
                        elif jw is not None:
                            joined_line_count += 1
                            jw.write(row, shuffle_list=join_shuffle_list)
                else:
                    matched_filter_line_count += 1
                    if mfew is not None:
                        mfew.write(row)
                    if self.join_output and ew is not None:
                        joined_line_count += 1
                        ew.write(row, shuffle_list=join_shuffle_list)
                    elif jw is not None:
                        joined_line_count += 1
                        jw.write(row, shuffle_list=join_shuffle_list)
            if self.verbose:
                print("Read %d filter records, %d found matching input records, %d did not find matches." % (filter_line_count,
                                                                                                             matched_filter_line_count,
                                                                                                             unmatched_filter_line_count),
                      file=self.error_file, flush=True)

        if self.verbose and jw is not None:
            print("Wrote %d joined records." % joined_line_count, file=self.error_file, flush=True)
        

    def process_presorted_files(self,
                                input_kr: KgtkReader,
                                filter_kr: KgtkReader,
                                input_key_columns: typing.List[int],
                                filter_key_columns: typing.List[int],
                                ew: typing.Optional[KgtkWriter] = None,
                                rew: typing.Optional[KgtkWriter] = None,
                                mfew: typing.Optional[KgtkWriter] = None, # matched filters
                                ufew: typing.Optional[KgtkWriter] = None, # unmatched filters
                                jw: typing.Optional[KgtkWriter] = None, # unmatched filters
                                join_shuffle_list: typing.Optional[typing.List[int]] = None, # for join output
    ):
        if self.verbose:
            print("Processing presorted files.", file=self.error_file, flush=True)

        filter_line_count: int = 0
        input_line_count: int = 0
        accept_line_count: int = 0
        reject_line_count: int = 0
        joined_line_count: int = 0

        filter_row: typing.Optional[typing.List[str]] = None
        filter_key: typing.Optional[str] = None
        filter_done: bool = False
        saw_match: bool = False

        matched_filter_line_count: int = 0
        unmatched_filter_line_count: int = 0

        # Used to check if the input and filter files are properly sorted.
        previous_filter_key: typing.Optional[str] = None
        previous_input_key: typing.Optional[str] = None

        row: typing.List[str]
        input_key: str
        for row in input_kr:
            # We have read another row from the input file.
            input_line_count += 1
            input_key = self.build_key(row, input_key_columns)

            if previous_input_key is not None and previous_input_key > input_key:
                raise ValueError("The input file is not in sorted order at row [%s]" % ", ".join([item for item in row]))
            previous_input_key = input_key

            if filter_done:
                if self.very_verbose:
                    print("Draining [%s]" % ", ".join([item for item in row]), file=self.error_file, flush=True)
                # The filter file has run out of rows.
                if self.invert:
                    accept_line_count += 1
                    if ew is not None:
                        ew.write(row)
                    if jw is not None and not self.join_output:
                        joined_line_count += 1
                        jw.write(row)
                else:
                    reject_line_count += 1
                    if rew is not None:
                        rew.write(row)
                    if self.left_join:
                        if self.join_output and ew is not None:
                            joined_line_count += 1
                            ew.write(row)
                        elif jw is not None:
                            joined_line_count += 1
                            jw.write(row)
                continue
                
            if filter_key is None or input_key > filter_key:
                # Either we have not yet read a filter row, or the input
                # row is beyond the current filter row in sorted order.
                if filter_key is not None and filter_row is not None and not saw_match:
                    # We read a filter row, but did not find a match for it.
                    unmatched_filter_line_count += 1
                    if ufew is not None and filter_row is not None:
                        ufew.write(filter_row)
                    if self.right_join:
                        if self.join_output and ew is not None:
                            joined_line_count += 1
                            ew.write(filter_row, shuffle_list=join_shuffle_list)
                        elif jw is not None:
                            joined_line_count += 1
                            jw.write(filter_row, shuffle_list=join_shuffle_list)
                        
                # Read more filter rows.
                for filter_row in filter_kr:
                    filter_line_count += 1
                    filter_key = self.build_key(filter_row, filter_key_columns)
                    saw_match = False

                    if previous_filter_key is not None and previous_filter_key > filter_key:
                        raise ValueError("The filter file is not in sorted order at row [%s]" % ", ".join([item for item in filter_row]))
                    previous_filter_key = filter_key

                    if input_key <= filter_key:
                        # Either we have a match, or the filter row is now beyond
                        # the input row in sorted order.
                        break
                    if self.very_verbose:
                        print("Skipping filter row [%s]" % ", ".join([item for item in filter_row]), file=self.error_file, flush=True)
                    unmatched_filter_line_count += 1
                    if ufew is not None:
                        ufew.write(filter_row)
                    if self.right_join:
                        if self.join_output and ew is not None:
                            joined_line_count += 1
                            ew.write(filter_row, shuffle_list=join_shuffle_list)
                        elif jw is not None:
                            joined_line_count += 1
                            jw.write(filter_row, shuffle_list=join_shuffle_list)

                else:
                    # The filter file has run out of filter rows.
                    if self.very_verbose:
                        print("Out of filter rows", file=self.error_file, flush=True)
                    filter_key = None
                    filter_done = True

            if filter_key is None or input_key < filter_key:
                # Either the filter file has run out of filter rows, or the filter row is
                # beyond the input row in sorted order.
                if self.very_verbose:
                    print("Skip this input row: [%s]" % ", ".join([item for item in row]), file=self.error_file, flush=True)
                if self.invert:
                    accept_line_count += 1
                    if ew is not None:
                        ew.write(row)
                    if jw is not None and not self.join_output:
                        joined_line_count += 1
                        jw.write(row)
                else:
                    reject_line_count += 1
                    if rew is not None:
                        rew.write(row)
                    if self.left_join:
                        if self.join_output and ew is not None:
                            joined_line_count += 1
                            ew.write(row)
                        elif jw is not None:
                            joined_line_count += 1
                            jw.write(row)
                        
            else: # input_key == filter_key
                # If we get here, the input row has a matching filter row.
                if not saw_match and self.right_first:
                    # This is the first match for this filter row.
                    matched_filter_line_count += 1
                    if filter_row is not None:
                        if mfew is not None:
                            mfew.write(filter_row)
                        if self.join_output and ew is not None:
                            joined_line_count += 1
                            ew.write(filter_row, shuffle_list=join_shuffle_list)
                        elif jw is not None:
                            joined_line_count += 1
                            jw.write(filter_row, shuffle_list=join_shuffle_list)
                    saw_match = True

                if self.very_verbose:
                    print("Keep this input row: [%s]" % ", ".join([item for item in row]), file=self.error_file, flush=True)
                if self.invert:
                    reject_line_count += 1
                    if rew is not None:
                        rew.write(row)
                    if self.left_join:
                        if self.join_output and ew is not None:
                            joined_line_count += 1
                            ew.write(row)
                        elif jw is not None:
                            joined_line_count += 1
                            jw.write(row)
                else:
                    accept_line_count += 1
                    if ew is not None:
                        ew.write(row)
                    if jw is not None and not self.join_output:
                        joined_line_count += 1
                        jw.write(row)

                if not saw_match and not self.right_first:
                    # This is the first match for this filter row.
                    matched_filter_line_count += 1
                    if filter_row is not None:
                        if mfew is not None:
                            mfew.write(filter_row)
                        if self.join_output and ew is not None:
                            joined_line_count += 1
                            ew.write(filter_row, shuffle_list=join_shuffle_list)
                        elif jw is not None:
                            joined_line_count += 1
                            jw.write(filter_row, shuffle_list=join_shuffle_list)
                    saw_match = True

        if not filter_done:
            # Drain the filter file, checking for record order.
            for filter_row in filter_kr:
                filter_line_count += 1
                filter_key = self.build_key(filter_row, filter_key_columns)

                if previous_filter_key is not None and previous_filter_key > filter_key:
                    raise ValueError("The filter file is not in sorted order at row [%s]" % ", ".join([item for item in filter_row]))
                previous_filter_key = filter_key

                unmatched_filter_line_count += 1
                if ufew is not None:
                    ufew.write(filter_row)
                if self.right_join:
                    if self.join_output and ew is not None:
                        joined_line_count += 1
                        ew.write(filter_row, shuffle_list=join_shuffle_list)
                    elif jw is not None:
                        joined_line_count += 1
                        jw.write(filter_row, shuffle_list=join_shuffle_list)

        if self.verbose:
            print("Read %d input records, accepted %d records, rejected %d records." % (input_line_count, accept_line_count, reject_line_count),
                  file=self.error_file, flush=True)
            print("Read %d filter records, %d found matching input records, %d did not find matches." % (filter_line_count,
                                                                                                         matched_filter_line_count,
                                                                                                         unmatched_filter_line_count),
                  file=self.error_file, flush=True)

        if self.verbose and (self.join_output or jw is not None):
            print("Wrote %d joined records." % joined_line_count, file=self.error_file, flush=True)


    def process_cacheing_input(self,
                               input_kr: KgtkReader,
                               filter_kr: KgtkReader,
                               input_key_columns: typing.List[int],
                               filter_key_columns: typing.List[int],
                               ew: typing.Optional[KgtkWriter] = None,
                               rew: typing.Optional[KgtkWriter] = None,
                               mfew: typing.Optional[KgtkWriter] = None, # matched filters
                               ufew: typing.Optional[KgtkWriter] = None, # unmatched filters
                               jw: typing.Optional[KgtkWriter] = None, # unmatched filters
                               join_shuffle_list: typing.Optional[typing.List[int]] = None, # for join output
    ):
        if self.verbose:
            print("Processing by cacheing the input file.")
        input_line_count: int = 0
        accept_line_count: int = 0
        reject_line_count: int = 0
        joined_line_count: int = 0
        
        filter_line_count: int = 0
        matched_filter_line_count: int = 0
        unmatched_filter_line_count: int = 0

        # Map key values to lists of input data.
        inputmap: typing.Dict[str, typing.List[typing.List[str]]] = { }

        if self.verbose:
            print("Reading and cacheing the input data from %s" % self.input_file_path, file=self.error_file, flush=True)
        row: typing.List[str]
        for row in input_kr:
            input_line_count += 1
            input_key: str = self.build_key(row, input_key_columns)
            if input_key in inputmap:
                # Append the row to an existing list for that key.
                inputmap[input_key].append(row)
            else:
                # Create a new list of rows for this key.
                inputmap[input_key] = [ row ]

        # Map key values to lists of output data.
        outputmap: typing.MutableMapping[str, typing.List[typing.List[str]]] = inputmap.copy() if self.invert else dict()

        if self.verbose:
            print("Applying the filter from %s" % self.filter_file_path, file=self.error_file, flush=True)
        filter_key: str
        for row in filter_kr:
            filter_line_count += 1
            filter_key = self.build_key(row, filter_key_columns)
            if filter_key in inputmap:
                matched_filter_line_count += 1
                if mfew is not None:
                    mfew.write(row)
                if jw is not None:
                    joined_line_count += 1
                    jw.write(row, shuffle_list=join_shuffle_list)
                if self.invert:
                    if filter_key in outputmap:
                        del outputmap[filter_key]
                else:
                    outputmap[filter_key] = inputmap[filter_key]
            else:
                unmatched_filter_line_count += 1
                if ufew is not None:
                    ufew.write(row)
                if jw is not None and self.right_join:
                    joined_line_count += 1
                    jw.write(row, shuffle_list=join_shuffle_list)

        # To simplify debugging, write the output data in sorted order (keys,
        # then input order).
        if self.verbose and ew is not None:
                print("Writing the output data to %s" % self.output_file_path, file=self.error_file, flush=True)
        key: str
        for key in sorted(outputmap.keys()):
            for row in outputmap[key]:
                accept_line_count += 1
                if ew is not None:
                    ew.write(row)
                if jw is not None:
                    joined_line_count += 1
                    jw.write(row)

        # To simplify debugging, write the reject data in sorted order (keys,
        # then input order).
        if self.verbose and rew is not None:
                print("Writing the reject data to %s" % self.reject_file_path, file=self.error_file, flush=True)
        for key in sorted(inputmap.keys()):
            if key not in outputmap:
                for row in inputmap[key]:
                    reject_line_count += 1
                    if rew is not None:
                        rew.write(row)
                    if jw is not None and self.left_join:
                        joined_line_count += 1
                        jw.write(row)

        if self.verbose:
            print("Read %d input records, accepted %d records, rejected %d records." % (input_line_count, accept_line_count, reject_line_count),
                  file=self.error_file, flush=True)
            print("Read %d filter records, %d found matching input records, %d did not find matches." % (filter_line_count,
                                                                                                         matched_filter_line_count,
                                                                                                         unmatched_filter_line_count),
                  file=self.error_file, flush=True)

        if self.verbose and jw is not None:
            print("Wrote %d joined records." % joined_line_count, file=self.error_file, flush=True)

    def process_cacheing_input_preserving_order(self,
                                                input_kr: KgtkReader,
                                                filter_kr: KgtkReader,
                                                input_key_columns: typing.List[int],
                                                filter_key_columns: typing.List[int],
                                                ew: typing.Optional[KgtkWriter] = None,
                                                rew: typing.Optional[KgtkWriter] = None,
                                                mfew: typing.Optional[KgtkWriter] = None, # matched filters
                                                ufew: typing.Optional[KgtkWriter] = None, # unmatched filters
                                                jw: typing.Optional[KgtkWriter] = None, # unmatched filters
                                                join_shuffle_list: typing.Optional[typing.List[int]] = None, # for join output
                                                ):
        # This algorithm preserves the input file's record order in the output file,
        # at the cost of extra work building keys.

        if self.verbose:
            print("Processing by cacheing the input file while preserving record order.")

        # Step one:  read the input file, cache it, and build the input key set
        if self.verbose:
            print("Building the input key set from %s" % self.input_file_path, file=self.error_file, flush=True)
        input_key_set: typing.Set[str]
        input_cache: typing.List[typing.List[str]]
        input_key_set, input_cache = self.extract_key_set_and_cache(input_kr, "input", input_key_columns)
        input_line_count: int = len(input_cache)
        if self.verbose or self.very_verbose:
            print("There are %d rows in the input cache." % input_line_count, file=self.error_file, flush=True)
            print("There are %d entries in the input key set." % len(input_key_set), file=self.error_file, flush=True)
            if self.very_verbose:
                print("Keys: %s" % " ".join(input_key_set), file=self.error_file, flush=True)

        # Step two: read the filter file and derive the output key set.
        output_key_set: typing.Set[str] = input_key_set.copy() if self.invert else set()

        if self.verbose:
            print("Applying the filter from %s" % self.filter_file_path, file=self.error_file, flush=True)
        filter_key: str
        filter_line_count: int = 0
        matched_filter_line_count: int = 0
        unmatched_filter_line_count: int = 0
        joined_line_count: int = 0
        row: typing.List[str]
        for row in filter_kr:
            filter_line_count += 1
            filter_key = self.build_key(row, filter_key_columns)
            if filter_key in input_key_set:
                matched_filter_line_count += 1
                if mfew is not None:
                    mfew.write(row)
                if jw is not None:
                    joined_line_count += 1
                    jw.write(row, shuffle_list=join_shuffle_list)
                if self.invert:
                    if filter_key in output_key_set:
                        output_key_set.remove(filter_key)
                else:
                    output_key_set.add(filter_key)
            else:
                unmatched_filter_line_count += 1
                if ufew is not None:
                    ufew.write(row)
                if jw is not None and self.right_join:
                    joined_line_count += 1
                    jw.write(row, shuffle_list=join_shuffle_list)

        if self.verbose:
            print("Read %d filter records, %d found matching input records, %d did not find matches." % (filter_line_count,
                                                                                                         matched_filter_line_count,
                                                                                                         unmatched_filter_line_count),
                  file=self.error_file, flush=True)
            print("There are %d entries in the output key set." % len(output_key_set), file=self.error_file, flush=True)

        # Step three: read the input rows from the cache and write only the
        # ones with keys in the output key set.
        accept_line_count: int = 0
        reject_line_count: int = 0
        for row in input_cache:
            input_key: str = self.build_key(row, input_key_columns)
            if input_key in output_key_set:
                accept_line_count += 1
                if ew is not None:
                    ew.write(row)
                if jw is not None:
                    jw.write(row)
            else:
                reject_line_count += 1
                if rew is not None:
                    rew.write(row)
                if jw is not None and self.left_join:
                    jw.write(row)

        if self.verbose:
            print("Read %d input records, accepted %d records, rejected %d records." % (input_line_count, accept_line_count, reject_line_count),
                  file=self.error_file, flush=True)
        
        if self.verbose and jw is not None:
            print("Wrote %d joined records." % joined_line_count, file=self.error_file, flush=True)

    def process(self):
        UPDATE_VERSION: str = "2020-12-03T17:23:24.872146+00:00#U5P2iPrj3w+Az10+UMbGGMcK/SHBl0wuwe3R1sFky9gXILt9e5oSjHFhPMQEWYVnQtoPd7FUqsZZqR3PfFWaAg=="
        if self.show_version or self.verbose:
            print("KgtkIfEfexists version: %s" % UPDATE_VERSION, file=self.error_file, flush=True)

        # Open the input files once.
        if self.verbose:
            if self.input_file_path is not None:
                print("Opening the input file: %s" % self.input_file_path, file=self.error_file, flush=True)
            else:
                print("Reading the input data from stdin", file=self.error_file, flush=True)

        input_kr: KgtkReader =  KgtkReader.open(self.input_file_path,
                                                error_file=self.error_file,
                                                who="input",
                                                options=self.input_reader_options,
                                                value_options = self.value_options,
                                                verbose=self.verbose,
                                                very_verbose=self.very_verbose,
        )

        if self.verbose:
            print("Opening the filter input file: %s" % self.filter_file_path, file=self.error_file, flush=True)
        filter_kr: KgtkReader = KgtkReader.open(self.filter_file_path,
                                                who="filter",
                                                error_file=self.error_file,
                                                options=self.filter_reader_options,
                                                value_options=self.value_options,
                                                verbose=self.verbose,
                                                very_verbose=self.very_verbose,
        )

        input_key_columns: typing.List[int] = self.get_key_columns(self.input_keys, input_kr, filter_kr, "input")
        if self.verbose:
            print("Input  key columns: %s" % " ".join((input_kr.column_names[idx] for idx in input_key_columns)), file=self.error_file, flush=True)
        filter_key_columns: typing.List[int] = self.get_key_columns(self.filter_keys, filter_kr, input_kr, "filter")
        if self.verbose:
            print("Filter key columns: %s" % " ".join((filter_kr.column_names[idx] for idx in filter_key_columns)), file=self.error_file, flush=True)

        if len(input_key_columns) != len(filter_key_columns):
            print("There are %d input key columns but %d filter key columns.  Exiting." % (len(input_key_columns), len(filter_key_columns)),
                  file=self.error_file, flush=True)
            return

        right_column_names: typing.Optional[typing.List[str]] = None
        joined_column_names: typing.Optional[typing.List[str]] = None
        if self.join_file_path is not None or self.join_output:
            if (input_kr.is_edge_file and filter_kr.is_node_file) or (input_kr.is_node_file and filter_kr.is_edge_file):
                raise ValueError("Cannot join an edge file to a node file.")

            kmc: KgtkMergeColumns = KgtkMergeColumns()
            kmc.merge(input_kr.column_names, prefix=self.input_prefix)
            right_column_names = kmc.merge(filter_kr.column_names, prefix=self.filter_prefix)
            joined_column_names = kmc.column_names

            if self.verbose:
                print("       input  columns: %s" % " ".join(input_kr.column_names), file=self.error_file, flush=True)
                print("       filter columns: %s" % " ".join(filter_kr.column_names), file=self.error_file, flush=True)
                print("mapped filter columns: %s" % " ".join(right_column_names), file=self.error_file, flush=True)
                print("       joined columns: %s" % " ".join(joined_column_names), file=self.error_file, flush=True)

        join_shuffle_list: typing.Optional[typing.List[int]] = None

        ew: typing.Optional[KgtkWriter] = None
        if self.output_file_path is not None:
            if self.verbose:
                print("Opening the output file: %s" % self.output_file_path, file=self.error_file, flush=True)

            ew_column_names: typing.List[str]
            if self.join_output and joined_column_names is not None:
                ew_column_names = joined_column_names
            else:
                ew_column_names = input_kr.column_names

            ew = KgtkWriter.open(ew_column_names,
                                 self.output_file_path,
                                 mode=KgtkWriter.Mode[input_kr.mode.name],
                                 require_all_columns=False,
                                 prohibit_extra_columns=True,
                                 fill_missing_columns=True,
                                 use_mgzip=self.input_reader_options.use_mgzip, # Hack!
                                 mgzip_threads=self.input_reader_options.mgzip_threads, # Hack!
                                 gzip_in_parallel=False,
                                 verbose=self.verbose,
                                 very_verbose=self.very_verbose)
            if self.join_output and right_column_names is not None:
                join_shuffle_list = ew.build_shuffle_list(right_column_names)        

            
        rew: typing.Optional[KgtkWriter] = None
        if self.reject_file_path is not None:
            if self.verbose:
                print("Opening the reject file: %s" % self.reject_file_path, file=self.error_file, flush=True)
            rew = KgtkWriter.open(input_kr.column_names,
                                  self.reject_file_path,
                                  mode=KgtkWriter.Mode[input_kr.mode.name],
                                  require_all_columns=False,
                                  prohibit_extra_columns=True,
                                  fill_missing_columns=True,
                                  use_mgzip=self.input_reader_options.use_mgzip, # Hack!
                                  mgzip_threads=self.input_reader_options.mgzip_threads, # Hack!
                                  gzip_in_parallel=False,
                                  verbose=self.verbose,
                                  very_verbose=self.very_verbose)
            
        mfew: typing.Optional[KgtkWriter] = None
        if self.matched_filter_file_path is not None:
            if self.verbose:
                print("Opening the matched filter file: %s" % self.matched_filter_file_path, file=self.error_file, flush=True)
            mfew = KgtkWriter.open(filter_kr.column_names,
                                   self.matched_filter_file_path,
                                   mode=KgtkWriter.Mode[filter_kr.mode.name],
                                   require_all_columns=False,
                                   prohibit_extra_columns=True,
                                   fill_missing_columns=True,
                                   use_mgzip=self.input_reader_options.use_mgzip, # Hack!
                                   mgzip_threads=self.input_reader_options.mgzip_threads, # Hack!
                                   gzip_in_parallel=False,
                                   verbose=self.verbose,
                                   very_verbose=self.very_verbose)
            
        ufew: typing.Optional[KgtkWriter] = None
        if self.unmatched_filter_file_path is not None:
            if self.verbose:
                print("Opening the unmatched filter file: %s" % self.unmatched_filter_file_path, file=self.error_file, flush=True)
            ufew = KgtkWriter.open(filter_kr.column_names,
                                   self.unmatched_filter_file_path,
                                   mode=KgtkWriter.Mode[filter_kr.mode.name],
                                   require_all_columns=False,
                                   prohibit_extra_columns=True,
                                   fill_missing_columns=True,
                                   use_mgzip=self.input_reader_options.use_mgzip, # Hack! 
                                   mgzip_threads=self.input_reader_options.mgzip_threads, # Hack!
                                   gzip_in_parallel=False,
                                   verbose=self.verbose,
                                   very_verbose=self.very_verbose)
            
        jw: typing.Optional[KgtkWriter] = None
        if self.join_file_path is not None and not self.join_output and joined_column_names is not None:
            jw = KgtkWriter.open(joined_column_names,
                                 self.join_file_path,
                                 mode=KgtkWriter.Mode[input_kr.mode.name],
                                 require_all_columns=False,
                                 prohibit_extra_columns=True,
                                 fill_missing_columns=True,
                                 use_mgzip=self.input_reader_options.use_mgzip, # Hack!
                                 mgzip_threads=self.input_reader_options.mgzip_threads, # Hack!
                                 gzip_in_parallel=False,
                                 verbose=self.verbose,
                                 very_verbose=self.very_verbose)
            if right_column_names is not None:
                join_shuffle_list = jw.build_shuffle_list(right_column_names)
            
        if self.presorted:
            self.process_presorted_files(input_kr=input_kr,
                                         filter_kr=filter_kr,
                                         input_key_columns=input_key_columns,
                                         filter_key_columns=filter_key_columns,
                                         ew=ew,
                                         rew=rew,
                                         mfew=mfew,
                                         ufew=ufew,
                                         jw=jw,
                                         join_shuffle_list=join_shuffle_list)
            
        elif self.cache_input:
            if self.preserve_order:
                self.process_cacheing_input_preserving_order(input_kr=input_kr,
                                                             filter_kr=filter_kr,
                                                             input_key_columns=input_key_columns,
                                                             filter_key_columns=filter_key_columns,
                                                             ew=ew,
                                                             rew=rew,
                                                             mfew=mfew,
                                                             ufew=ufew,
                                                             jw=jw,
                                                             join_shuffle_list=join_shuffle_list)
            else:
                self.process_cacheing_input(input_kr=input_kr,
                                            filter_kr=filter_kr,
                                            input_key_columns=input_key_columns,
                                            filter_key_columns=filter_key_columns,
                                            ew=ew,
                                            rew=rew,
                                            mfew=mfew,
                                            ufew=ufew,
                                            jw=jw,
                                            join_shuffle_list=join_shuffle_list)
        else:
            self.process_cacheing_filter(input_kr=input_kr,
                                         filter_kr=filter_kr,
                                         input_key_columns=input_key_columns,
                                         filter_key_columns=filter_key_columns,
                                         ew=ew,
                                         rew=rew,
                                         mfew=mfew,
                                         ufew=ufew,
                                         jw=jw,
                                         join_shuffle_list=join_shuffle_list)

        if ew is not None:
            ew.close()
        if rew is not None:
            rew.close()
        if mfew is not None:
            mfew.close()
        if ufew is not None:
            ufew.close()

def main():
    """
    Test the KGTK file joiner.
    """
    parser: ArgumentParser = ArgumentParser()

    parser.add_argument(dest="input_file_path", help="The KGTK file with the input data", type=Path, nargs="?")

    parser.add_argument(      "--filter-on", dest="filter_file_path", help="The KGTK file with the filter data (required).", type=Path, required=True)

    parser.add_argument("-o", "--output-file", dest="output_file_path", help="The KGTK file for accepted records. (default=%(default)s).", type=Path, default="-")
    
    parser.add_argument(      "--reject-file", dest="reject_file_path", help="The KGTK file for rejected records. (default=%(default)s).", type=Path, default=None)
    
    parser.add_argument(      "--matched-filter-file", dest="matched_filter_file_path", help="The KGTK file for matched filter records. (default=%(default)s).", type=Path, default=None)
    
    parser.add_argument(      "--unmatched-filter-file", dest="unmatched_filter_file_path", help="The KGTK file for unmatched filter records. (default=%(default)s).", type=Path, default=None)
    
    parser.add_argument(      "--join-file", dest="join_file_path", help="The KGTK file for joined output records. (default=%(default)s).", type=Path, default=None)

    parser.add_argument(      "--left-join", dest="left_join", metavar="True|False",
                              help="When True, include all input records in the join (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--right-join", dest="right_join", metavar="True|False",
                              help="When True, include all filter records in the join (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)
    
    parser.add_argument(      "--input-prefix", dest="input_prefix", help="Input file column name prefix for joins. (default=%(default)s)")
    parser.add_argument(      "--filter-prefix", dest="filter_prefix", help="Filter file column name prefix for joins. (default=%(default)s)")

    parser.add_argument(      "--join-output", dest="join_output",  metavar="True|False",
                              help="When True, send the join records to the main output (EXPERIMENTAL). (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--right-join-first", dest="right_first",  metavar="True|False",
                              help="When True, send the filter record to join output before the first matching input record. " +
                              " Otherwise, send the first matching input record, then the filter record, then othe rmatching input records. " +
                              "(EXPERIMENTAL). (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--field-separator", dest="field_separator", help="Separator for multifield keys (default=%(default)s)",
                              default=KgtkIfExists.FIELD_SEPARATOR_DEFAULT)
   
    parser.add_argument(      "--invert", dest="invert", metavar="True|False",
                              help="Invert the test (if not exists) (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--cache-input", dest="cache_input", help="Cache the input file instead of the filter keys. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--preserve-order", dest="preserve_order", metavar="True|False",
                              help="Preserve record order when cacheing the input file. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--presorted", dest="presorted", metavar="True|False",
                              help="When True, assume that the input and filter files are both presorted.  Use a merge-style algorithm that does not require caching either file. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--input-keys", dest="input_keys", help="The key columns in the input file (default=None).", nargs='*')
    parser.add_argument(      "--filter-keys", dest="filter_keys", help="The key columns in the filter file (default=None).", nargs='*')

    KgtkReader.add_debug_arguments(parser)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, who="input")
    KgtkReaderOptions.add_arguments(parser, mode_options=True, who="filter")
    KgtkValueOptions.add_arguments(parser)

    args: Namespace = parser.parse_args()

    error_file: typing.TextIO = sys.stdout if args.errors_to_stdout else sys.stderr

    # Build the option structures.                                                                                                                          
    input_reader_options: KgtkReaderOptions = KgtkReaderOptions.from_args(args, who="input")
    filter_reader_options: KgtkReaderOptions = KgtkReaderOptions.from_args(args, who="filter")
    value_options: KgtkValueOptions = KgtkValueOptions.from_args(args)

   # Show the final option structures for debugging and documentation.                                                                                             
    if args.show_options:
        print("input: %s" % (str(args.input_file_path) if args.input_file_path is not None else "-"), file=error_file)
        print("--filter-on=%s" % str(args.filter_file_path), file=error_file)
        print("--output-file=%s" % str(args.output_file_path), file=error_file)
        if args.reject_file_path is not None:
            print("--reject-file=%s" % str(args.reject_file_path), file=error_file)
        if args.matched_filter_file_path is not None:
            print("--matched-filter-file=%s" % str(args.matched_filter_file_path), file=error_file)
        if args.unmatched_filter_file_path is not None:
            print("--unmatched-filter-file=%s" % str(args.unmatched_filter_file_path), file=error_file)
        if args.join_file_path is not None:
            print("--join-file=%s" % str(args.join_file_path), file=error_file)
        print("--left-join=%s" % str(args.left_join), file=error_file)
        print("--right-join=%s" % str(args.right_join), file=error_file)
        if args.input_prefix is not None:
            print("--input-prefix=%s" % repr(args.input_prefix), file=error_file)
        if args.filter_prefix is not None:
            print("--filter-prefix=%s" % repr(args.filter_prefix), file=error_file)
        print("--join-output=%s" % str(args.join_output), file=error_file)
        print("--left-join-first=%s" % str(args.right_first), file=error_file)
        print("--invert=%s" % str(args.invert), file=error_file)
        print("--cache-input=%s" % str(args.cache_input), file=error_file)
        print("--preserve-order=%s" % str(args.preserve_order), file=error_file)
        print("--presorted=%s" % str(args.presorted), file=error_file)
        if args.input_keys is not None:
            print("--input-keys %s" % " ".join(args.input_keys), file=error_file)
        if args.filter_keys is not None:
            print("--filter-keys %s" % " ".join(args.filter_keys), file=error_file)
        input_reader_options.show(out=error_file, who="input")
        filter_reader_options.show(out=error_file, who="filter")
        value_options.show(out=error_file)

    ie: KgtkIfExists = KgtkIfExists(
        input_file_path=args.input_file_path,
        input_keys=args.input_keys,
        filter_file_path=args.filter_file_path,
        filter_keys=args.filter_keys,
        output_file_path=args.output_file_path,
        reject_file_path=args.reject_file_path,
        matched_filter_file_path=args.matched_filter_file_path,
        unmatched_filter_file_path=args.unmatched_filter_file_path,
        join_file_path=args.join_file_path,
        left_join=args.left_join,
        right_join=args.right_join,
        input_prefix=args.input_prefix,
        filter_prefix=args.filter_prefix,
        join_output=args.join_output,
        right_first=args.right_first,
        field_separator=args.field_separator,
        invert=args.invert,
        cache_input=args.cache_input,
        preserve_order=args.preserve_order,
        presorted=args.presorted,
        input_reader_options=input_reader_options,
        filter_reader_options=filter_reader_options,
        value_options=value_options,
        error_file=error_file,
        verbose=args.verbose,
        very_verbose=args.very_verbose)

    ie.process()

if __name__ == "__main__":
    main()
