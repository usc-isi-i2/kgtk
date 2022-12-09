from pathlib import Path
import re
import sys

from kgtk.exceptions import KGTKException
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
from kgtk.io.kgtkwriter import KgtkWriter
from kgtk.value.kgtkvalueoptions import KgtkValueOptions
from typing import List, Optional, TextIO, Set, Pattern, MutableMapping, Match


class Filter(object):
    def __init__(self,
                 input_kgtk_file: Path,
                 output_kgtk_files: List[Path],
                 patterns: List[List[str]],
                 reject_kgtk_file: Path = None,
                 reader_options: KgtkReaderOptions = None,
                 value_options: KgtkValueOptions = None,
                 subj_col: Optional[str] = 'node1',
                 pred_col: Optional[str] = 'label',
                 obj_col: Optional[str] = 'node2',
                 or_pattern: bool = False,
                 invert: bool = False,
                 regex: bool = False,
                 numeric: bool = False,
                 fancy: bool = False,
                 match_type: str = 'match',
                 first_match_only: bool = False,
                 pass_empty_value: bool = False,
                 pattern_separator: str = ";",
                 word_separator: str = ",",
                 show_version: bool = False,
                 error_file: TextIO = sys.stderr,
                 show_options: bool = False,
                 verbose: bool = False,
                 very_verbose: bool = False):
        self.input_kgtk_file = input_kgtk_file
        self.output_kgtk_files = output_kgtk_files
        self.patterns = patterns
        self.reject_kgtk_file = reject_kgtk_file
        self.reader_options = reader_options
        self.value_options = value_options
        self.subj_col = subj_col
        self.pred_col = pred_col
        self.obj_col = obj_col
        self.or_pattern = or_pattern
        self.invert = invert
        self.regex = regex
        self.numeric = numeric
        self.fancy = fancy
        self.match_type = match_type
        self.first_match_only = first_match_only
        self.pass_empty_value = pass_empty_value
        self.pattern_separator = pattern_separator
        self.word_separator = word_separator
        self.show_version = show_version
        self.error_file = error_file
        self.show_options = show_options
        self.verbose = verbose
        self.very_verbose = very_verbose

    def process(self):
        try:
            if self.regex:
                return self.process_regex()
            else:
                return self.process_plain()
        except Exception as e:
            raise KGTKException(e)

    def prepare_filter(self, pattern: str) -> Set[str]:
        filt: Set[str] = set()
        pattern = pattern.strip()
        if len(pattern) == 0:
            return filt

        target: str
        for target in pattern.split(self.word_separator):
            target = target.strip()
            if len(target) > 0:
                filt.add(target)

        return filt

    @staticmethod
    def prepare_regex(pattern: str) -> Optional[Pattern]:
        pattern = pattern.strip()
        if len(pattern) == 0:
            return None
        else:
            return re.compile(pattern)

    def single_subject_filter(self,
                              kr: KgtkReader,
                              kw: KgtkWriter,
                              rw: Optional[KgtkWriter],
                              subj_idx: int,
                              subj_filter: Set[str],
                              ):
        if self.verbose:
            print("Applying a single subject filter", file=self.error_file, flush=True)

        subj_filter_value: str = list(subj_filter)[0]

        input_line_count: int = 0
        reject_line_count: int = 0
        output_line_count: int = 0

        row: List[str]
        for row in kr:
            input_line_count += 1

            if row[subj_idx] == subj_filter_value:
                kw.write(row)
                output_line_count += 1

            else:
                if rw is not None:
                    rw.write(row)
                reject_line_count += 1

        if self.verbose:
            print("Read %d rows, rejected %d rows, wrote %d rows." % (
                input_line_count, reject_line_count, output_line_count), file=self.error_file, flush=True)

    def single_subject_filter_inverted(self,
                                       kr: KgtkReader,
                                       kw: KgtkWriter,
                                       rw: Optional[KgtkWriter],
                                       subj_idx: int,
                                       subj_filter: Set[str],
                                       ):
        if self.verbose:
            print("Applying a single subject filter inverted", file=self.error_file, flush=True)

        subj_filter_value: str = list(subj_filter)[0]

        input_line_count: int = 0
        reject_line_count: int = 0
        output_line_count: int = 0

        row: List[str]
        for row in kr:
            input_line_count += 1

            if row[subj_idx] != subj_filter_value:
                kw.write(row)
                output_line_count += 1

            else:
                if rw is not None:
                    rw.write(row)
                reject_line_count += 1

        if self.verbose:
            print("Read %d rows, rejected %d rows, wrote %d rows." % (
                input_line_count, reject_line_count, output_line_count), file=self.error_file, flush=True)

    def single_predicate_filter(self,
                                kr: KgtkReader,
                                kw: KgtkWriter,
                                rw: Optional[KgtkWriter],
                                pred_idx: int,
                                pred_filter: Set[str],
                                ):
        if self.verbose:
            print("Applying a single predicate filter", file=self.error_file, flush=True)

        pred_filter_value: str = list(pred_filter)[0]

        input_line_count: int = 0
        reject_line_count: int = 0
        output_line_count: int = 0

        row: List[str]
        for row in kr:
            input_line_count += 1

            if row[pred_idx] == pred_filter_value:
                kw.write(row)
                output_line_count += 1

            else:
                if rw is not None:
                    rw.write(row)
                reject_line_count += 1

        if self.verbose:
            print("Read %d rows, rejected %d rows, wrote %d rows." % (
                input_line_count, reject_line_count, output_line_count), file=self.error_file, flush=True)

    def single_predicate_filter_inverted(self,
                                         kr: KgtkReader,
                                         kw: KgtkWriter,
                                         rw: Optional[KgtkWriter],
                                         pred_idx: int,
                                         pred_filter: Set[str],
                                         ):
        if self.verbose:
            print("Applying a single predicate filter inverted", file=self.error_file, flush=True)

        pred_filter_value: str = list(pred_filter)[0]

        input_line_count: int = 0
        reject_line_count: int = 0
        output_line_count: int = 0

        row: List[str]
        for row in kr:
            input_line_count += 1

            if row[pred_idx] != pred_filter_value:
                kw.write(row)
                output_line_count += 1

            else:
                if rw is not None:
                    rw.write(row)
                reject_line_count += 1

        if self.verbose:
            print("Read %d rows, rejected %d rows, wrote %d rows." % (
                input_line_count, reject_line_count, output_line_count), file=self.error_file, flush=True)

    def single_object_filter(self,
                             kr: KgtkReader,
                             kw: KgtkWriter,
                             rw: Optional[KgtkWriter],
                             obj_idx: int,
                             obj_filter: Set[str],
                             ):
        if self.verbose:
            print("Applying a single object filter", file=self.error_file, flush=True)

        obj_filter_value: str = list(obj_filter)[0]

        input_line_count: int = 0
        reject_line_count: int = 0
        output_line_count: int = 0

        row: List[str]
        for row in kr:
            input_line_count += 1

            if row[obj_idx] == obj_filter_value:
                kw.write(row)
                output_line_count += 1

            else:
                if rw is not None:
                    rw.write(row)
                reject_line_count += 1

        if self.verbose:
            print("Read %d rows, rejected %d rows, wrote %d rows." % (
                input_line_count, reject_line_count, output_line_count), file=self.error_file, flush=True)

    def single_object_filter_inverted(self,
                                      kr: KgtkReader,
                                      kw: KgtkWriter,
                                      rw: Optional[KgtkWriter],
                                      obj_idx: int,
                                      obj_filter: Set[str],
                                      ):
        if self.verbose:
            print("Applying a single object filter inverted", file=self.error_file, flush=True)

        obj_filter_value: str = list(obj_filter)[0]

        input_line_count: int = 0
        reject_line_count: int = 0
        output_line_count: int = 0

        row: List[str]
        for row in kr:
            input_line_count += 1

            if row[obj_idx] != obj_filter_value:
                kw.write(row)
                output_line_count += 1

            else:
                if rw is not None:
                    rw.write(row)
                reject_line_count += 1

        if self.verbose:
            print("Read %d rows, rejected %d rows, wrote %d rows." % (
                input_line_count, reject_line_count, output_line_count), file=self.error_file, flush=True)

    def single_general_filter(self,
                              kr: KgtkReader,
                              kw: KgtkWriter,
                              rw: Optional[KgtkWriter],
                              subj_idx: int,
                              subj_filter: Set[str],
                              pred_idx: int,
                              pred_filter: Set[str],
                              obj_idx: int,
                              obj_filter: Set[str]):
        if self.verbose:
            print("Applying a single general filter", file=self.error_file, flush=True)

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

        row: List[str]
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

            if (keep if self.or_pattern else not reject) ^ self.invert:
                kw.write(row)
                output_line_count += 1
            else:
                if rw is not None:
                    rw.write(row)
                reject_line_count += 1

        if self.verbose:
            print("Read %d rows, rejected %d rows, wrote %d rows." % (
                input_line_count, reject_line_count, output_line_count), file=self.error_file, flush=True)
            print("Keep counts: subject=%d, predicate=%d, object=%d." % (
                subj_filter_keep_count, pred_filter_keep_count, obj_filter_keep_count), file=self.error_file,
                  flush=True)
            print("Reject counts: subject=%d, predicate=%d, object=%d." % (
                subj_filter_reject_count, pred_filter_reject_count, obj_filter_reject_count), file=self.error_file,
                  flush=True)

    def dispatch_subject_filter(self,
                                kr: KgtkReader,
                                kws: List[KgtkWriter],
                                rw: Optional[KgtkWriter],
                                subj_idx: int,
                                subj_filters: List[Set[str]]):
        if self.verbose:
            print("Applying a dispatched multiple-output subject filter", file=self.error_file, flush=True)

        input_line_count: int = 0
        reject_line_count: int = 0
        output_line_count: int = 0

        dispatch: MutableMapping[str, KgtkWriter] = {}
        idx: int
        kw: KgtkWriter
        for idx, kw in enumerate(kws):
            subj_filter: Set[str] = subj_filters[idx]
            keyword: str
            for keyword in subj_filter:
                dispatch[keyword] = kw

        row: List[str]
        for row in kr:
            input_line_count += 1

            kwo: Optional[KgtkWriter] = dispatch.get(row[subj_idx])
            if kwo is not None:
                kwo.write(row)
                output_line_count += 1
            else:
                if rw is not None:
                    rw.write(row)
                reject_line_count += 1

        if self.verbose:
            print("Read %d rows, rejected %d rows, wrote %d rows." % (
                input_line_count, reject_line_count, output_line_count), file=self.error_file, flush=True)

    def dispatch_predicate_filter(self,
                                  kr: KgtkReader,
                                  kws: List[KgtkWriter],
                                  rw: Optional[KgtkWriter],
                                  pred_idx: int,
                                  pred_filters: List[Set[str]]):
        if self.verbose:
            print("Applying a dispatched multiple-output predicate filter", file=self.error_file, flush=True)

        input_line_count: int = 0
        reject_line_count: int = 0
        output_line_count: int = 0

        dispatch: MutableMapping[str, KgtkWriter] = {}
        idx: int
        kw: KgtkWriter
        for idx, kw in enumerate(kws):
            pred_filter: Set[str] = pred_filters[idx]
            keyword: str
            for keyword in pred_filter:
                dispatch[keyword] = kw

        row: List[str]
        for row in kr:
            input_line_count += 1

            kwo: Optional[KgtkWriter] = dispatch.get(row[pred_idx])
            if kwo is not None:
                kwo.write(row)
                output_line_count += 1
            else:
                if rw is not None:
                    rw.write(row)
                reject_line_count += 1

        if self.verbose:
            print("Read %d rows, rejected %d rows, wrote %d rows." % (
                input_line_count, reject_line_count, output_line_count), file=self.error_file, flush=True)

    def dispatch_object_filter(self,
                               kr: KgtkReader,
                               kws: List[KgtkWriter],
                               rw: Optional[KgtkWriter],
                               obj_idx: int,
                               obj_filters: List[Set[str]]):
        if self.verbose:
            print("Applying a dispatched multiple-output object filter", file=self.error_file, flush=True)

        input_line_count: int = 0
        reject_line_count: int = 0
        output_line_count: int = 0

        dispatch: MutableMapping[str, KgtkWriter] = {}
        idx: int
        kw: KgtkWriter
        for idx, kw in enumerate(kws):
            obj_filter: Set[str] = obj_filters[idx]
            keyword: str
            for keyword in obj_filter:
                dispatch[keyword] = kw

        row: List[str]
        for row in kr:
            input_line_count += 1

            kwo: Optional[KgtkWriter] = dispatch.get(row[obj_idx])
            if kwo is not None:
                kwo.write(row)
                output_line_count += 1
            else:
                if rw is not None:
                    rw.write(row)
                reject_line_count += 1

        if self.verbose:
            print("Read %d rows, rejected %d rows, wrote %d rows." % (
                input_line_count, reject_line_count, output_line_count), file=self.error_file, flush=True)

    def multiple_general_filter(self,
                                kr: KgtkReader,
                                kws: List[KgtkWriter],
                                rw: Optional[KgtkWriter],
                                subj_idx: int,
                                subj_filters: List[Set[str]],
                                pred_idx: int,
                                pred_filters: List[Set[str]],
                                obj_idx: int,
                                obj_filters: List[Set[str]]):
        if self.verbose:
            print("Applying a multiple-output general filter", file=self.error_file, flush=True)

        input_line_count: int = 0
        reject_line_count: int = 0
        output_line_count: int = 0
        subj_filter_keep_count: int = 0
        pred_filter_keep_count: int = 0
        obj_filter_keep_count: int = 0
        subj_filter_reject_count: int = 0
        pred_filter_reject_count: int = 0
        obj_filter_reject_count: int = 0

        row: List[str]
        for row in kr:
            input_line_count += 1

            written: bool = False

            idx: int = 0
            for kw in kws:
                subj_filter: Set[str] = subj_filters[idx]
                pred_filter: Set[str] = pred_filters[idx]
                obj_filter: Set[str] = obj_filters[idx]
                idx += 1

                keep: bool = False
                reject: bool = False
                if len(subj_filter) > 0:
                    if row[subj_idx] in subj_filter:
                        keep = True
                        subj_filter_keep_count += 1
                    else:
                        reject = True
                        subj_filter_reject_count += 1

                if len(pred_filter) > 0:
                    if row[pred_idx] in pred_filter:
                        keep = True
                        pred_filter_keep_count += 1
                    else:
                        reject = True
                        pred_filter_reject_count += 1

                if len(obj_filter) > 0:
                    if row[obj_idx] in obj_filter:
                        keep = True
                        obj_filter_keep_count += 1
                    else:
                        reject = True
                        obj_filter_reject_count += 1

                if (keep if self.or_pattern else not reject) ^ self.invert:
                    kw.write(row)
                    if not written:
                        output_line_count += 1  # Count this only once.
                        written = True
                        if self.first_match_only:
                            break

            if not written:
                if rw is not None:
                    rw.write(row)
                reject_line_count += 1

        if self.verbose:
            print("Read %d rows, rejected %d rows, wrote %d rows." % (
                input_line_count, reject_line_count, output_line_count), file=self.error_file, flush=True)
            print("Keep counts: subject=%d, predicate=%d, object=%d." % (
                subj_filter_keep_count, pred_filter_keep_count, obj_filter_keep_count), file=self.error_file,
                  flush=True)
            print("Reject counts: subject=%d, predicate=%d, object=%d." % (
                subj_filter_reject_count, pred_filter_reject_count, obj_filter_reject_count), file=self.error_file,
                  flush=True)

    def numeric_filter_test(self, value: str, threshold: float) -> bool:
        if len(value) == 0:
            return self.pass_empty_value

        # TODO: catch a conversion failure and provide better feedback
        # and other options.
        try:
            numeric_value: float = float(value)
        except ValueError:
            return False

        if self.match_type == "eq":
            return numeric_value == threshold
        elif self.match_type == "ne":
            return numeric_value != threshold
        elif self.match_type == "gt":
            return numeric_value > threshold
        elif self.match_type == "ge":
            return numeric_value >= threshold
        elif self.match_type == "lt":
            return numeric_value < threshold
        elif self.match_type == "le":
            return numeric_value <= threshold
        else:
            raise KGTKException("Unknown match type %s during numeric filter test" % repr(self.match_type))

    def multiple_general_numeric_filter(self,
                                        kr: KgtkReader,
                                        kws: List[KgtkWriter],
                                        rw: Optional[KgtkWriter],
                                        subj_idx: int,
                                        subj_filters: List[Set[str]],
                                        pred_idx: int,
                                        pred_filters: List[Set[str]],
                                        obj_idx: int,
                                        obj_filters: List[Set[str]]):
        if self.verbose:
            print("Applying a multiple general numeric filter", file=self.error_file, flush=True)

        # Convert the string-based filters to numeric filters.
        filter_set: Set[str]
        subj_numeric_filters: List[Optional[float]] = []
        for filter_set in subj_filters:
            if len(filter_set) > 1:
                raise KGTKException("Numeric subject filters must be singleton values.")
            # TODO: Catch a conversion failure and give better feedback.
            if len(filter_set) > 0:
                subj_numeric_filters.append(float(list(filter_set)[0]))
            else:
                subj_numeric_filters.append(None)

        pred_numeric_filters: List[Optional[float]] = []
        for filter_set in pred_filters:
            if len(filter_set) > 1:
                raise KGTKException("Numeric predicate filters must be singleton values.")
            if len(filter_set) > 0:
                # TODO: Catch a conversion failure and give better feedback.
                pred_numeric_filters.append(float(list(filter_set)[0]))
            else:
                pred_numeric_filters.append(None)

        obj_numeric_filters: List[Optional[float]] = []
        for filter_set in obj_filters:
            if len(filter_set) > 1:
                raise KGTKException("Numeric object filters must be singleton values.")
            if len(filter_set) > 0:
                # TODO: Catch a conversion failure and give better feedback.
                obj_numeric_filters.append(float(list(filter_set)[0]))
            else:
                obj_numeric_filters.append(None)

        input_line_count: int = 0
        reject_line_count: int = 0
        output_line_count: int = 0
        subj_filter_keep_count: int = 0
        pred_filter_keep_count: int = 0
        obj_filter_keep_count: int = 0
        subj_filter_reject_count: int = 0
        pred_filter_reject_count: int = 0
        obj_filter_reject_count: int = 0

        row: List[str]
        for row in kr:
            input_line_count += 1

            written: bool = False

            idx: int = 0
            for kw in kws:
                subj_filter: Optional[float] = subj_numeric_filters[idx]
                pred_filter: Optional[float] = pred_numeric_filters[idx]
                obj_filter: Optional[float] = obj_numeric_filters[idx]
                idx += 1

                keep: bool = False
                reject: bool = False
                if subj_filter is not None:
                    if self.numeric_filter_test(row[subj_idx], subj_filter):
                        keep = True
                        subj_filter_keep_count += 1
                    else:
                        reject = True
                        subj_filter_reject_count += 1

                if pred_filter is not None:
                    if self.numeric_filter_test(row[pred_idx], pred_filter):
                        keep = True
                        pred_filter_keep_count += 1
                    else:
                        reject = True
                        pred_filter_reject_count += 1

                if obj_filter is not None:
                    if self.numeric_filter_test(row[obj_idx], obj_filter):
                        keep = True
                        obj_filter_keep_count += 1
                    else:
                        reject = True
                        obj_filter_reject_count += 1

                if (keep if self.or_pattern else not reject) ^ self.invert:
                    kw.write(row)
                    if not written:
                        output_line_count += 1  # Count this only once.
                        written = True
                        if self.first_match_only:
                            break

            if not written:
                if rw is not None:
                    rw.write(row)
                reject_line_count += 1

        if self.verbose:
            print("Read %d rows, rejected %d rows, wrote %d rows." % (
                input_line_count, reject_line_count, output_line_count), file=self.error_file, flush=True)
            print("Keep counts: subject=%d, predicate=%d, object=%d." % (
                subj_filter_keep_count, pred_filter_keep_count, obj_filter_keep_count), file=self.error_file,
                  flush=True)
            print("Reject counts: subject=%d, predicate=%d, object=%d." % (
                subj_filter_reject_count, pred_filter_reject_count, obj_filter_reject_count), file=self.error_file,
                  flush=True)

    def single_general_numeric_filter(self,
                                      kr: KgtkReader,
                                      kws: List[KgtkWriter],
                                      rw: Optional[KgtkWriter],
                                      subj_idx: int,
                                      subj_filter: Set[str],
                                      pred_idx: int,
                                      pred_filter: Set[str],
                                      obj_idx: int,
                                      obj_filter: Set[str]):
        if self.verbose:
            print("Applying a single general numeric filter", file=self.error_file, flush=True)

        # Convert the string-based filter to a numeric filter.
        subj_numeric_filter: Optional[float]
        if len(subj_filter) > 1:
            raise KGTKException("Numeric subject filters must be singleton values.")
        # TODO: Catch a conversion failure and give better feedback.
        elif len(subj_filter) == 1:
            subj_numeric_filter = float(list(subj_filter)[0])
        else:
            subj_numeric_filter = None

        pred_numeric_filter: Optional[float]
        if len(pred_filter) > 1:
            raise KGTKException("Numeric predicate filters must be singleton values.")
        elif len(pred_filter) == 1:
            # TODO: Catch a conversion failure and give better feedback.
            pred_numeric_filter = float(list(pred_filter)[0])
        else:
            pred_numeric_filter = None

        obj_numeric_filter: Optional[float]
        if len(obj_filter) > 1:
            raise KGTKException("Numeric object filters must be singleton values.")
        elif len(obj_filter) == 1:
            # TODO: Catch a conversion failure and give better feedback.
            obj_numeric_filter = float(list(obj_filter)[0])
        else:
            obj_numeric_filter = None

        input_line_count: int = 0
        reject_line_count: int = 0
        output_line_count: int = 0
        subj_filter_keep_count: int = 0
        pred_filter_keep_count: int = 0
        obj_filter_keep_count: int = 0
        subj_filter_reject_count: int = 0
        pred_filter_reject_count: int = 0
        obj_filter_reject_count: int = 0

        kw: KgtkWriter = kws[0]

        row: List[str]
        for row in kr:
            input_line_count += 1

            keep: bool = False
            reject: bool = False
            if subj_numeric_filter is not None:
                if self.numeric_filter_test(row[subj_idx], subj_numeric_filter):
                    keep = True
                    subj_filter_keep_count += 1
                else:
                    reject = True
                    subj_filter_reject_count += 1

            if pred_numeric_filter is not None:
                if self.numeric_filter_test(row[pred_idx], pred_numeric_filter):
                    keep = True
                    pred_filter_keep_count += 1
                else:
                    reject = True
                    pred_filter_reject_count += 1

            if obj_numeric_filter is not None:
                if self.numeric_filter_test(row[obj_idx], obj_numeric_filter):
                    keep = True
                    obj_filter_keep_count += 1
                else:
                    reject = True
                    obj_filter_reject_count += 1

            if (keep if self.or_pattern else not reject) ^ self.invert:
                kw.write(row)
                output_line_count += 1
            else:
                if rw is not None:
                    rw.write(row)
                reject_line_count += 1

        if self.verbose:
            print("Read %d rows, rejected %d rows, wrote %d rows." % (
                input_line_count, reject_line_count, output_line_count), file=self.error_file, flush=True)
            print("Keep counts: subject=%d, predicate=%d, object=%d." % (
                subj_filter_keep_count, pred_filter_keep_count, obj_filter_keep_count), file=self.error_file,
                  flush=True)
            print("Reject counts: subject=%d, predicate=%d, object=%d." % (
                subj_filter_reject_count, pred_filter_reject_count, obj_filter_reject_count), file=self.error_file,
                  flush=True)

    def fancy_filter_test(self, value: str, fancy_filter: Set[str]) -> bool:

        fancy_pattern: str
        for fancy_pattern in fancy_filter:
            # TODO: Optimize so the patterns aren't converted to float every time they're used.

            if fancy_pattern.startswith(":"):
                if value == fancy_pattern[1:]:
                    return True

            elif fancy_pattern.startswith("="):
                if len(value) == 0 and self.pass_empty_value:
                    return True
                try:
                    if float(value) == float(fancy_pattern[1:]):
                        return True
                except ValueError:
                    pass

            elif fancy_pattern.startswith("!="):
                if len(value) == 0 and self.pass_empty_value:
                    return True
                try:
                    if float(value) != float(fancy_pattern[2:]):
                        return True
                except ValueError:
                    pass

            elif fancy_pattern.startswith(">="):
                if len(value) == 0 and self.pass_empty_value:
                    return True
                try:
                    if float(value) >= float(fancy_pattern[2:]):
                        return True
                except ValueError:
                    pass

            elif fancy_pattern.startswith(">"):
                if len(value) == 0 and self.pass_empty_value:
                    return True
                try:
                    if float(value) > float(fancy_pattern[1:]):
                        return True
                except ValueError:
                    pass

            elif fancy_pattern.startswith("<="):
                if len(value) == 0 and self.pass_empty_value:
                    return True
                try:
                    if float(value) <= float(fancy_pattern[2:]):
                        return True
                except ValueError:
                    pass

            elif fancy_pattern.startswith("<"):
                if len(value) == 0 and self.pass_empty_value:
                    return True
                try:
                    if float(value) < float(fancy_pattern[1:]):
                        return True
                except ValueError:
                    pass

            elif fancy_pattern.startswith("~"):
                # TODO: optimize thie code so the regular expressions are not
                # compiled each time they're used.
                if self.match_type == "fullmatch":
                    if re.compile(fancy_pattern[1:]).fullmatch(value):
                        return True
                elif self.match_type == "match":
                    if re.compile(fancy_pattern[1:]).match(value):
                        return True
                elif self.match_type == "seach":
                    if re.compile(fancy_pattern[1:]).search(value):
                        return True
                else:
                    raise KGTKException("Match type %s is not valid for fancy filters." % repr(self.match_type))

            else:
                raise KGTKException("Unknown prefix in fancy pattern %s" % repr(fancy_pattern))

        return False

    def multiple_general_fancy_filter(self,
                                      kr: KgtkReader,
                                      kws: List[KgtkWriter],
                                      rw: Optional[KgtkWriter],
                                      subj_idx: int,
                                      subj_filters: List[Set[str]],
                                      pred_idx: int,
                                      pred_filters: List[Set[str]],
                                      obj_idx: int,
                                      obj_filters: List[Set[str]]):
        if self.verbose:
            print("Applying a multiple general fancy filter", file=self.error_file, flush=True)

        input_line_count: int = 0
        reject_line_count: int = 0
        output_line_count: int = 0
        subj_filter_keep_count: int = 0
        pred_filter_keep_count: int = 0
        obj_filter_keep_count: int = 0
        subj_filter_reject_count: int = 0
        pred_filter_reject_count: int = 0
        obj_filter_reject_count: int = 0

        row: List[str]
        for row in kr:
            input_line_count += 1

            written: bool = False

            idx: int = 0
            for kw in kws:
                subj_filter: Set[str] = subj_filters[idx]
                pred_filter: Set[str] = pred_filters[idx]
                obj_filter: Set[str] = obj_filters[idx]
                idx += 1

                keep: bool = False
                reject: bool = False
                if len(subj_filter) > 0:
                    if self.fancy_filter_test(row[subj_idx], subj_filter):
                        keep = True
                        subj_filter_keep_count += 1
                    else:
                        reject = True
                        subj_filter_reject_count += 1

                if len(pred_filter) > 0:
                    if self.fancy_filter_test(row[pred_idx], pred_filter):
                        keep = True
                        pred_filter_keep_count += 1
                    else:
                        reject = True
                        pred_filter_reject_count += 1

                if len(obj_filter) > 0:
                    if self.fancy_filter_test(row[obj_idx], obj_filter):
                        keep = True
                        obj_filter_keep_count += 1
                    else:
                        reject = True
                        obj_filter_reject_count += 1

                if (keep if self.or_pattern else not reject) ^ self.invert:
                    kw.write(row)
                    if not written:
                        output_line_count += 1  # Count this only once.
                        written = True
                        if self.first_match_only:
                            break

            if not written:
                if rw is not None:
                    rw.write(row)
                reject_line_count += 1

        if self.verbose:
            print("Read %d rows, rejected %d rows, wrote %d rows." % (
                input_line_count, reject_line_count, output_line_count), file=self.error_file, flush=True)
            print("Keep counts: subject=%d, predicate=%d, object=%d." % (
                subj_filter_keep_count, pred_filter_keep_count, obj_filter_keep_count), file=self.error_file,
                  flush=True)
            print("Reject counts: subject=%d, predicate=%d, object=%d." % (
                subj_filter_reject_count, pred_filter_reject_count, obj_filter_reject_count), file=self.error_file,
                  flush=True)

    def process_plain(self) -> int:

        subj_filters: List[Set[str]] = []
        pred_filters: List[Set[str]] = []
        obj_filters: List[Set[str]] = []

        subj_filter: Set[str]
        pred_filter: Set[str]
        obj_filter: Set[str]

        nfilters: int = 0
        pattern_list: List[str]
        pattern: str
        for pattern_list in self.patterns:
            for pattern in pattern_list:
                subpatterns: List[str] = pattern.split(self.pattern_separator)
                if len(subpatterns) != 3:
                    print("Error: The pattern must have three sections separated by %s (two %s total)." % (
                        repr(self.pattern_separator), repr(self.pattern_separator)),
                          file=self.error_file, flush=True)
                    raise KGTKException("Bad pattern")

                subj_filter = self.prepare_filter(subpatterns[0])
                pred_filter = self.prepare_filter(subpatterns[1])
                obj_filter = self.prepare_filter(subpatterns[2])

                if len(subj_filter) == 0 and len(pred_filter) == 0 and len(obj_filter) == 0:
                    if self.verbose:
                        print("Warning: the filter %s is empty." % repr(pattern), file=self.error_file, flush=True)
                else:
                    subj_filters.append(subj_filter)
                    pred_filters.append(pred_filter)
                    obj_filters.append(obj_filter)
                    nfilters += 1

        if nfilters == 0:
            raise KGTKException("No filters found.")

        if nfilters != len(self.output_kgtk_files):
            if self.verbose:
                print("output files: %s" % " ".join([str(x) for x in self.output_kgtk_files]), file=self.error_file,
                      flush=True)
            raise KGTKException("There were %d filters and %d output files." % (nfilters, len(self.output_kgtk_files)))

        if self.verbose:
            print("Opening the input file: %s" % str(self.input_kgtk_file), file=self.error_file, flush=True)
        kr: KgtkReader = KgtkReader.open(self.input_kgtk_file,
                                         options=self.reader_options,
                                         value_options=self.value_options,
                                         error_file=self.error_file,
                                         verbose=self.verbose,
                                         very_verbose=self.very_verbose,
                                         )

        subj_idx: int = kr.get_node1_column_index(self.subj_col)
        pred_idx: int = kr.get_label_column_index(self.pred_col)
        obj_idx: int = kr.get_node2_column_index(self.obj_col)

        # Complain about a missing column only when it is needed by the pattern.
        trouble: bool = False
        if subj_idx < 0 and len(set.union(*subj_filters)) > 0:
            trouble = True
            print("Error: Cannot find the subject column '%s'." % kr.get_node1_canonical_name(self.subj_col),
                  file=self.error_file, flush=True)
        if pred_idx < 0 and len(set.union(*pred_filters)) > 0:
            trouble = True
            print("Error: Cannot find the predicate column '%s'." % kr.get_label_canonical_name(self.pred_col),
                  file=self.error_file, flush=True)
        if obj_idx < 0 and len(set.union(*obj_filters)) > 0:
            trouble = True
            print("Error: Cannot find the object column '%s'." % kr.get_node2_canonical_name(self.obj_col),
                  file=self.error_file,
                  flush=True)
        if trouble:
            # Clean up:
            kr.close()
            raise KGTKException("Missing columns.")

        kw: KgtkWriter
        kws: List[KgtkWriter] = []
        output_kgtk_file: Path
        for output_kgtk_file in self.output_kgtk_files:
            if self.verbose:
                print("Opening the output file: %s" % str(output_kgtk_file), file=self.error_file, flush=True)
            kw = KgtkWriter.open(kr.column_names,
                                 output_kgtk_file,
                                 mode=KgtkWriter.Mode[kr.mode.name],
                                 use_mgzip=self.reader_options.use_mgzip,  # Hack!
                                 mgzip_threads=self.reader_options.mgzip_threads,  # Hack!
                                 error_file=self.error_file,
                                 verbose=self.verbose,
                                 very_verbose=self.very_verbose)
            kws.append(kw)

        rw: Optional[KgtkWriter] = None
        if self.reject_kgtk_file is not None:
            if self.verbose:
                print("Opening the reject file: %s" % str(self.reject_kgtk_file), file=self.error_file, flush=True)
            rw = KgtkWriter.open(kr.column_names,
                                 self.reject_kgtk_file,
                                 mode=KgtkWriter.Mode[kr.mode.name],
                                 use_mgzip=self.reader_options.use_mgzip,  # Hack!
                                 mgzip_threads=self.reader_options.mgzip_threads,  # Hack!
                                 error_file=self.error_file,
                                 verbose=self.verbose,
                                 very_verbose=self.very_verbose)

        try:
            if self.fancy:
                # TODO: add additional optimized cases.
                self.multiple_general_fancy_filter(kr, kws, rw, subj_idx, subj_filters, pred_idx, pred_filters, obj_idx,
                                                   obj_filters)

            elif self.numeric:
                # TODO: add additional optimized cases.

                if nfilters == 1:
                    self.single_general_numeric_filter(kr, kws, rw, subj_idx, subj_filters[0], pred_idx,
                                                       pred_filters[0],
                                                       obj_idx, obj_filters[0])
                else:
                    self.multiple_general_numeric_filter(kr, kws, rw, subj_idx, subj_filters, pred_idx, pred_filters,
                                                         obj_idx, obj_filters)

            elif nfilters == 1:
                subj_filter = subj_filters[0]
                pred_filter = pred_filters[0]
                obj_filter = obj_filters[0]
                kw = kws[0]

                if len(subj_filter) == 1 and len(pred_filter) == 0 and len(obj_filter) == 0:
                    if self.invert:
                        self.single_subject_filter_inverted(kr, kw, rw, subj_idx, subj_filter)
                    else:
                        self.single_subject_filter(kr, kw, rw, subj_idx, subj_filter)

                elif len(subj_filter) == 0 and len(pred_filter) == 1 and len(obj_filter) == 0:
                    if self.invert:
                        self.single_predicate_filter_inverted(kr, kw, rw, pred_idx, pred_filter)
                    else:
                        self.single_predicate_filter(kr, kw, rw, pred_idx, pred_filter)

                elif len(subj_filter) == 0 and len(pred_filter) == 0 and len(obj_filter) == 1:
                    if self.invert:
                        self.single_object_filter_inverted(kr, kw, rw, obj_idx, obj_filter)
                    else:
                        self.single_object_filter(kr, kw, rw, obj_idx, obj_filter)
                else:
                    self.single_general_filter(kr, kw, rw, subj_idx, subj_filter, pred_idx, pred_filter, obj_idx,
                                               obj_filter)

            else:
                n_subj_filters: int = 0
                n_pred_filters: int = 0
                n_obj_filters: int = 0
                fidx: int
                for fidx in range(nfilters):
                    n_subj_filters += len(subj_filters[fidx])
                    n_pred_filters += len(pred_filters[fidx])
                    n_obj_filters += len(obj_filters[fidx])

                if n_subj_filters > 0 and n_pred_filters == 0 and n_obj_filters == 0 and self.first_match_only and not self.invert:
                    self.dispatch_subject_filter(kr, kws, rw, subj_idx, subj_filters)

                elif n_subj_filters == 0 and n_pred_filters > 0 and n_obj_filters == 0 and self.first_match_only and not self.invert:
                    self.dispatch_predicate_filter(kr, kws, rw, pred_idx, pred_filters)

                elif n_subj_filters == 0 and n_pred_filters == 0 and n_obj_filters > 0 and self.first_match_only and not self.invert:
                    self.dispatch_object_filter(kr, kws, rw, obj_idx, obj_filters)

                else:
                    self.multiple_general_filter(kr, kws, rw, subj_idx, subj_filters, pred_idx, pred_filters, obj_idx,
                                                 obj_filters)

        finally:
            if self.verbose:
                print("Closing output files.", file=self.error_file, flush=True)
            for kw in kws:
                kw.close()
            if rw is not None:
                rw.close()
            if self.verbose:
                print("All output files have been closed.", file=self.error_file, flush=True)

        return 0

    def multiple_general_regex_fullmatch(self,
                                         kr: KgtkReader,
                                         kws: List[KgtkWriter],
                                         rw: Optional[KgtkWriter],
                                         subj_idx: int,
                                         subj_filters: List[Optional[Pattern]],
                                         pred_idx: int,
                                         pred_filters: List[Optional[Pattern]],
                                         obj_idx: int,
                                         obj_filters: List[Optional[Pattern]]):
        if self.verbose:
            print("Applying a multiple-output general regex fullmatch filter", file=self.error_file, flush=True)

        input_line_count: int = 0
        reject_line_count: int = 0
        output_line_count: int = 0
        subj_filter_keep_count: int = 0
        pred_filter_keep_count: int = 0
        obj_filter_keep_count: int = 0
        subj_filter_reject_count: int = 0
        pred_filter_reject_count: int = 0
        obj_filter_reject_count: int = 0

        row: List[str]
        for row in kr:
            input_line_count += 1

            written: bool = False

            idx: int = 0
            for kw in kws:
                subj_filter: Optional[Pattern] = subj_filters[idx]
                pred_filter: Optional[Pattern] = pred_filters[idx]
                obj_filter: Optional[Pattern] = obj_filters[idx]
                idx += 1

                keep: bool = False
                reject: bool = False
                if subj_filter is not None:
                    if len(row) <= subj_idx:
                        raise ValueError("Line %d: filter %d: short(len(row)=%d, subj_idx=%d): %s" % (
                            input_line_count, idx, len(row), subj_idx, repr(row)))
                    subj_match: Optional[Match] = subj_filter.fullmatch(row[subj_idx])
                    if subj_match is not None:
                        keep = True
                        subj_filter_keep_count += 1
                    else:
                        reject = True
                        subj_filter_reject_count += 1

                if pred_filter is not None:
                    if len(row) <= pred_idx:
                        raise ValueError("Line %d: filter %d: short(len(row)=%d, pred_idx=%d): %s" % (
                            input_line_count, idx, len(row), pred_idx, repr(row)))
                    pred_match: Optional[Match] = pred_filter.fullmatch(row[pred_idx])
                    if pred_match is not None:
                        keep = True
                        pred_filter_keep_count += 1
                    else:
                        reject = True
                        pred_filter_reject_count += 1

                if obj_filter is not None:
                    if len(row) <= obj_idx:
                        raise ValueError("Line %d: filter %d: short(len(row)=%d, obj_idx=%d): %s" % (
                            input_line_count, idx, len(row), obj_idx, repr(row)))
                    obj_match: Optional[Match] = obj_filter.fullmatch(row[obj_idx])
                    if obj_match is not None:
                        keep = True
                        obj_filter_keep_count += 1
                    else:
                        reject = True
                        obj_filter_reject_count += 1

                if (keep if self.or_pattern else not reject) ^ self.invert:
                    kw.write(row)
                    if not written:
                        output_line_count += 1  # Count this only once.
                        written = True
                        if self.first_match_only:
                            break

            if not written:
                if rw is not None:
                    rw.write(row)
                reject_line_count += 1

        if self.verbose:
            print("Read %d rows, rejected %d rows, wrote %d rows." % (
                input_line_count, reject_line_count, output_line_count), file=self.error_file, flush=True)
            print("Keep counts: subject=%d, predicate=%d, object=%d." % (
                subj_filter_keep_count, pred_filter_keep_count, obj_filter_keep_count), file=self.error_file,
                  flush=True)
            print("Reject counts: subject=%d, predicate=%d, object=%d." % (
                subj_filter_reject_count, pred_filter_reject_count, obj_filter_reject_count), file=self.error_file,
                  flush=True)

    def multiple_general_regex_match(self,
                                     kr: KgtkReader,
                                     kws: List[KgtkWriter],
                                     rw: Optional[KgtkWriter],
                                     subj_idx: int,
                                     subj_filters: List[Optional[Pattern]],
                                     pred_idx: int,
                                     pred_filters: List[Optional[Pattern]],
                                     obj_idx: int,
                                     obj_filters: List[Optional[Pattern]]):
        if self.verbose:
            print("Applying a multiple-output general regex match filter", file=self.error_file, flush=True)

        input_line_count: int = 0
        reject_line_count: int = 0
        output_line_count: int = 0
        subj_filter_keep_count: int = 0
        pred_filter_keep_count: int = 0
        obj_filter_keep_count: int = 0
        subj_filter_reject_count: int = 0
        pred_filter_reject_count: int = 0
        obj_filter_reject_count: int = 0

        row: List[str]
        for row in kr:
            input_line_count += 1

            written: bool = False

            idx: int = 0
            for kw in kws:
                subj_filter: Optional[Pattern] = subj_filters[idx]
                pred_filter: Optional[Pattern] = pred_filters[idx]
                obj_filter: Optional[Pattern] = obj_filters[idx]
                idx += 1

                keep: bool = False
                reject: bool = False
                if subj_filter is not None:
                    if len(row) <= subj_idx:
                        raise ValueError("Line %d: filter %d: short(len(row)=%d, subj_idx=%d): %s" % (
                            input_line_count, idx, len(row), subj_idx, repr(row)))
                    subj_match: Optional[Match] = subj_filter.match(row[subj_idx])
                    if subj_match is not None:
                        keep = True
                        subj_filter_keep_count += 1
                    else:
                        reject = True
                        subj_filter_reject_count += 1

                if pred_filter is not None:
                    if len(row) <= pred_idx:
                        raise ValueError("Line %d: filter %d: short(len(row)=%d, pred_idx=%d): %s" % (
                            input_line_count, idx, len(row), pred_idx, repr(row)))
                    pred_match: Optional[Match] = pred_filter.match(row[pred_idx])
                    if pred_match is not None:
                        keep = True
                        pred_filter_keep_count += 1
                    else:
                        reject = True
                        pred_filter_reject_count += 1

                if obj_filter is not None:
                    if len(row) <= obj_idx:
                        raise ValueError("Line %d: filter %d: short(len(row)=%d, obj_idx=%d): %s" % (
                            input_line_count, idx, len(row), obj_idx, repr(row)))
                    obj_match: Optional[Match] = obj_filter.match(row[obj_idx])
                    if obj_match is not None:
                        keep = True
                        obj_filter_keep_count += 1
                    else:
                        reject = True
                        obj_filter_reject_count += 1

                if (keep if self.or_pattern else not reject) ^ self.invert:
                    kw.write(row)
                    if not written:
                        output_line_count += 1  # Count this only once.
                        written = True
                        if self.first_match_only:
                            break

            if not written:
                if rw is not None:
                    rw.write(row)
                reject_line_count += 1

        if self.verbose:
            print("Read %d rows, rejected %d rows, wrote %d rows." % (
                input_line_count, reject_line_count, output_line_count), file=self.error_file, flush=True)
            print("Keep counts: subject=%d, predicate=%d, object=%d." % (
                subj_filter_keep_count, pred_filter_keep_count, obj_filter_keep_count), file=self.error_file,
                  flush=True)
            print("Reject counts: subject=%d, predicate=%d, object=%d." % (
                subj_filter_reject_count, pred_filter_reject_count, obj_filter_reject_count), file=self.error_file,
                  flush=True)

    def multiple_general_regex_search(self,
                                      kr: KgtkReader,
                                      kws: List[KgtkWriter],
                                      rw: Optional[KgtkWriter],
                                      subj_idx: int,
                                      subj_filters: List[Optional[Pattern]],
                                      pred_idx: int,
                                      pred_filters: List[Optional[Pattern]],
                                      obj_idx: int,
                                      obj_filters: List[Optional[Pattern]]):
        if self.verbose:
            print("Applying a multiple-output general regex search filter", file=self.error_file, flush=True)

        input_line_count: int = 0
        reject_line_count: int = 0
        output_line_count: int = 0
        subj_filter_keep_count: int = 0
        pred_filter_keep_count: int = 0
        obj_filter_keep_count: int = 0
        subj_filter_reject_count: int = 0
        pred_filter_reject_count: int = 0
        obj_filter_reject_count: int = 0

        row: List[str]
        for row in kr:
            input_line_count += 1

            written: bool = False

            idx: int = 0
            for kw in kws:
                subj_filter: Optional[Pattern] = subj_filters[idx]
                pred_filter: Optional[Pattern] = pred_filters[idx]
                obj_filter: Optional[Pattern] = obj_filters[idx]
                idx += 1

                keep: bool = False
                reject: bool = False
                if subj_filter is not None:
                    if len(row) <= subj_idx:
                        raise ValueError("Line %d: filter %d: short(len(row)=%d, subj_idx=%d): %s" % (
                            input_line_count, idx, len(row), subj_idx, repr(row)))
                    subj_match: Optional[Match] = subj_filter.search(row[subj_idx])
                    if subj_match is not None:
                        keep = True
                        subj_filter_keep_count += 1
                    else:
                        reject = True
                        subj_filter_reject_count += 1

                if pred_filter is not None:
                    if len(row) <= pred_idx:
                        raise ValueError("Line %d: filter %d: short(len(row)=%d, pred_idx=%d): %s" % (
                            input_line_count, idx, len(row), pred_idx, repr(row)))
                    pred_match: Optional[Match] = pred_filter.search(row[pred_idx])
                    if pred_match is not None:
                        keep = True
                        pred_filter_keep_count += 1
                    else:
                        reject = True
                        pred_filter_reject_count += 1

                if obj_filter is not None:
                    if len(row) <= obj_idx:
                        raise ValueError("Line %d: filter %d: short(len(row)=%d, obj_idx=%d): %s" % (
                            input_line_count, idx, len(row), obj_idx, repr(row)))
                    obj_match: Optional[Match] = obj_filter.search(row[obj_idx])
                    if obj_match is not None:
                        keep = True
                        obj_filter_keep_count += 1
                    else:
                        reject = True
                        obj_filter_reject_count += 1

                if (keep if self.or_pattern else not reject) ^ self.invert:
                    kw.write(row)
                    if not written:
                        output_line_count += 1  # Count this only once.
                        written = True
                        if self.first_match_only:
                            break

            if not written:
                if rw is not None:
                    rw.write(row)
                reject_line_count += 1

        if self.verbose:
            print("Read %d rows, rejected %d rows, wrote %d rows." % (
                input_line_count, reject_line_count, output_line_count), file=self.error_file, flush=True)
            print("Keep counts: subject=%d, predicate=%d, object=%d." % (
                subj_filter_keep_count, pred_filter_keep_count, obj_filter_keep_count), file=self.error_file,
                  flush=True)
            print("Reject counts: subject=%d, predicate=%d, object=%d." % (
                subj_filter_reject_count, pred_filter_reject_count, obj_filter_reject_count), file=self.error_file,
                  flush=True)

    def process_regex(self) -> int:
        subj_regexes: List[Optional[Pattern]] = []
        pred_regexes: List[Optional[Pattern]] = []
        obj_regexes: List[Optional[Pattern]] = []

        subj_regex: Optional[Pattern]
        pred_regex: Optional[Pattern]
        obj_regex: Optional[Pattern]

        subj_needed: bool = False
        pred_needed: bool = False
        obj_needed: bool = False

        nfilters: int = 0
        pattern_list: List[str]
        pattern: str
        for pattern_list in self.patterns:
            for pattern in pattern_list:
                subpatterns: List[str] = pattern.split(self.pattern_separator)
                if len(subpatterns) != 3:
                    print("Error: The pattern must have three sections separated by %s (two %s total)." % (
                        repr(self.pattern_separator), repr(self.pattern_separator)),
                          file=self.error_file, flush=True)
                    raise KGTKException("Bad pattern")

                subj_regex = self.prepare_regex(subpatterns[0])
                pred_regex = self.prepare_regex(subpatterns[1])
                obj_regex = self.prepare_regex(subpatterns[2])

                if subj_regex is None and pred_regex is None and obj_regex is None:
                    if self.verbose:
                        print("Warning: the filter %s is empty." % repr(pattern), file=self.error_file, flush=True)
                else:
                    subj_regexes.append(subj_regex)
                    pred_regexes.append(pred_regex)
                    obj_regexes.append(obj_regex)
                    nfilters += 1

                    if subj_regex is not None:
                        subj_needed = True
                    if pred_regex is not None:
                        pred_needed = True
                    if obj_regex is not None:
                        obj_needed = True

        if nfilters == 0:
            raise KGTKException("No filters found.")

        if nfilters != len(self.output_kgtk_files):
            if self.verbose:
                print("output files: %s" % " ".join([str(x) for x in self.output_kgtk_files]), file=self.error_file,
                      flush=True)
            raise KGTKException("There were %d filters and %d output files." % (nfilters, len(self.output_kgtk_files)))

        if self.verbose:
            print("Opening the input file: %s" % str(self.input_kgtk_file), file=self.error_file, flush=True)
        kr: KgtkReader = KgtkReader.open(self.input_kgtk_file,
                                         options=self.reader_options,
                                         value_options=self.value_options,
                                         error_file=self.error_file,
                                         verbose=self.verbose,
                                         very_verbose=self.very_verbose,
                                         )

        subj_idx: int = kr.get_node1_column_index(self.subj_col)
        pred_idx: int = kr.get_label_column_index(self.pred_col)
        obj_idx: int = kr.get_node2_column_index(self.obj_col)

        # Complain about a missing column only when it is needed by the pattern.
        trouble: bool = False
        if subj_idx < 0 and subj_needed:
            trouble = True
            print("Error: Cannot find the subject column '%s'." % kr.get_node1_canonical_name(self.subj_col),
                  file=self.error_file, flush=True)
        if pred_idx < 0 and pred_needed:
            trouble = True
            print("Error: Cannot find the predicate column '%s'." % kr.get_label_canonical_name(self.pred_col),
                  file=self.error_file, flush=True)
        if obj_idx < 0 and obj_needed:
            trouble = True
            print("Error: Cannot find the object column '%s'." % kr.get_node2_canonical_name(self.obj_col),
                  file=self.error_file,
                  flush=True)
        if trouble:
            # Clean up:
            kr.close()
            raise KGTKException("Missing columns.")

        kw: KgtkWriter
        kws: List[KgtkWriter] = []
        output_kgtk_file: Path
        for output_kgtk_file in self.output_kgtk_files:
            if self.verbose:
                print("Opening the output file: %s" % str(output_kgtk_file), file=self.error_file, flush=True)
            kw = KgtkWriter.open(kr.column_names,
                                 output_kgtk_file,
                                 mode=KgtkWriter.Mode[kr.mode.name],
                                 use_mgzip=self.reader_options.use_mgzip,  # Hack!
                                 mgzip_threads=self.reader_options.mgzip_threads,  # Hack!
                                 error_file=self.error_file,
                                 verbose=self.verbose,
                                 very_verbose=self.very_verbose)
            kws.append(kw)

        rw: Optional[KgtkWriter] = None
        if self.reject_kgtk_file is not None:
            if self.verbose:
                print("Opening the reject file: %s" % str(self.reject_kgtk_file), file=self.error_file, flush=True)
            rw = KgtkWriter.open(kr.column_names,
                                 self.reject_kgtk_file,
                                 mode=KgtkWriter.Mode[kr.mode.name],
                                 use_mgzip=self.reader_options.use_mgzip,  # Hack!
                                 mgzip_threads=self.reader_options.mgzip_threads,  # Hack!
                                 error_file=self.error_file,
                                 verbose=self.verbose,
                                 very_verbose=self.very_verbose)

        try:
            if self.match_type == "fullmatch":
                self.multiple_general_regex_fullmatch(kr, kws, rw, subj_idx, subj_regexes, pred_idx, pred_regexes,
                                                      obj_idx,
                                                      obj_regexes)
            elif self.match_type == "match":
                self.multiple_general_regex_match(kr, kws, rw, subj_idx, subj_regexes, pred_idx, pred_regexes, obj_idx,
                                                  obj_regexes)
            elif self.match_type == "search":
                self.multiple_general_regex_search(kr, kws, rw, subj_idx, subj_regexes, pred_idx, pred_regexes, obj_idx,
                                                   obj_regexes)
            else:
                raise KGTKException("Unknown match type %s" % repr(self.match_type))

        finally:
            if self.verbose:
                print("Closing output files.", file=self.error_file, flush=True)
            for kw in kws:
                kw.close()
            if rw is not None:
                rw.close()
            if self.verbose:
                print("All output files have been closed.", file=self.error_file, flush=True)

        return 0
