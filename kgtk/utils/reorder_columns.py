from pathlib import Path
import sys

from kgtk.exceptions import KGTKException
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
from kgtk.io.kgtkwriter import KgtkWriter
from kgtk.value.kgtkvalueoptions import KgtkValueOptions
from typing import List, TextIO, Optional


class ReorderColumns(object):
    def __init__(self,
                 input_kgtk_file: Path,
                 output_kgtk_file: Path,
                 output_format: str = 'kgtk',
                 column_names_list: List[List[str]] = None,
                 as_column_names_list: List[List[str]] = None,
                 omit_remaining_columns: bool = False,
                 reader_options: KgtkReaderOptions = None,
                 value_options: KgtkValueOptions = None,
                 error_file: TextIO = sys.stderr,
                 show_options: bool = False,
                 verbose: bool = False,
                 very_verbose: bool = False,
                 ):
        self.input_kgtk_file = input_kgtk_file
        self.output_kgtk_file = output_kgtk_file
        self.output_format = output_format
        self.column_names_list = column_names_list
        self.as_column_names_list = as_column_names_list
        self.omit_remaining_columns = omit_remaining_columns
        self.reader_options = reader_options
        self.value_options = value_options
        self.error_file = error_file
        self.show_options = show_options
        self.verbose = verbose
        self.very_verbose = very_verbose

    def process(self):
        # Condense the old and new columns names lists.
        column_names: List[str] = list()
        column_name_list: List[str]
        column_name: str
        if self.column_names_list is not None:
            for column_name_list in self.column_names_list:
                for column_name in column_name_list:
                    column_names.append(column_name)

        as_column_names: List[str] = list()
        if self.as_column_names_list is not None:
            for column_name_list in self.as_column_names_list:
                for column_name in column_name_list:
                    as_column_names.append(column_name)

        # Show the final option structures for debugging and documentation.
        if self.show_options:
            print("--input-file=%s" % str(self.input_kgtk_file), file=self.error_file, flush=True)
            print("--output-file=%s" % str(self.output_kgtk_file), file=self.error_file, flush=True)
            if self.output_format is not None:
                print("--output-format=%s" % self.output_format, file=self.error_file, flush=True)
            print("--columns %s" % " ".join(column_names), file=self.error_file, flush=True)
            if len(as_column_names) > 0:
                print("--as-columns %s" % " ".join(as_column_names), file=self.error_file, flush=True)
            print("--trim=%s" % str(self.omit_remaining_columns), file=self.error_file, flush=True)
            self.reader_options.show(out=self.error_file)
            self.value_options.show(out=self.error_file)
            print("=======", file=self.error_file, flush=True)

        # Check for consistent options.  argparse doesn't support this yet.
        if len(as_column_names) > 0 and len(as_column_names) != len(column_names):
            raise KGTKException(
                "Both --columns and --as-columns must have the same number of columns when --as-columns is used.")

        try:

            if self.verbose:
                print("Opening the input file %s" % str(self.input_kgtk_file), file=self.error_file, flush=True)
            kr = KgtkReader.open(self.input_kgtk_file,
                                 options=self.reader_options,
                                 value_options=self.value_options,
                                 error_file=self.error_file,
                                 verbose=self.verbose,
                                 very_verbose=self.very_verbose,
                                 )

            remaining_names: List[str] = kr.column_names.copy()
            reordered_names: List[str] = []
            save_reordered_names: Optional[List[str]] = None

            ellipses: str = "..."  # All unmentioned columns
            ranger: str = ".."  # All columns between two columns.

            saw_ranger: bool = False
            idx: int
            column_name: str
            for idx, column_name in enumerate(column_names):
                if column_name == ellipses:
                    if len(as_column_names) > 0:
                        raise KGTKException(
                            "The elipses operator ('...') may not appear when --as-columns is specified.")
                    if save_reordered_names is not None:
                        raise KGTKException("Elipses may appear only once")

                    if saw_ranger:
                        raise KGTKException("Elipses may not appear directly after a range operator ('..').")

                    save_reordered_names = reordered_names
                    reordered_names = []
                    continue

                if column_name == ranger:
                    if len(reordered_names) == 0:
                        raise KGTKException(
                            "The column range operator ('..') may not appear without a preceeding column name.")
                    if len(as_column_names) > 0:
                        raise KGTKException(
                            "The column range operator ('..') may not appear when --as-columns is specified.")
                    saw_ranger = True
                    continue

                if column_name not in kr.column_names:
                    raise KGTKException("Unknown column name '%s'." % column_name)
                if column_name not in remaining_names:
                    raise KGTKException("Column name '%s' was duplicated in the list." % column_name)

                if saw_ranger:
                    saw_ranger = False
                    prior_column_name: str = reordered_names[-1]
                    prior_column_idx: int = kr.column_name_map[prior_column_name]
                    column_name_idx: int = kr.column_name_map[column_name]
                    start_idx: int
                    end_idx: int
                    idx_inc: int
                    if column_name_idx > prior_column_idx:
                        start_idx = prior_column_idx + 1
                        end_idx = column_name_idx - 1
                        idx_inc = 1
                    else:
                        start_idx = prior_column_idx - 1
                        end_idx = column_name_idx + 1
                        idx_inc = -1

                    idx: int = start_idx
                    while idx <= end_idx:
                        idx_column_name: str = kr.column_names[idx]
                        if idx_column_name not in remaining_names:
                            raise KGTKException("Column name '%s' (%s .. %s) was duplicated in the list." % (
                                column_name, prior_column_name, column_name))

                        reordered_names.append(idx_column_name)
                        remaining_names.remove(idx_column_name)
                        idx += idx_inc

                reordered_names.append(column_name)
                remaining_names.remove(column_name)

            if saw_ranger:
                raise KGTKException("The column ranger operator ('..') may not end the list of column names.")

            if len(remaining_names) > 0 and save_reordered_names is None:
                # There are remaining column names and the ellipses was not seen.
                if not self.omit_remaining_columns:
                    raise KGTKException(
                        "No ellipses, and the following columns not accounted for: %s" % " ".join(remaining_names))
                else:
                    if self.verbose:
                        print("Omitting the following columns: %s" % " ".join(remaining_names), file=self.error_file,
                              flush=True)
            if save_reordered_names is not None:
                if len(remaining_names) > 0:
                    save_reordered_names.extend(remaining_names)
                if len(reordered_names) > 0:
                    save_reordered_names.extend(reordered_names)
                reordered_names = save_reordered_names

            if self.verbose:
                print("Opening the output file %s" % str(self.output_kgtk_file), file=self.error_file, flush=True)
            kw: KgtkWriter = KgtkWriter.open(reordered_names,
                                             self.output_kgtk_file,
                                             output_column_names=as_column_names,
                                             require_all_columns=True,
                                             prohibit_extra_columns=True,
                                             fill_missing_columns=False,
                                             gzip_in_parallel=False,
                                             mode=KgtkWriter.Mode[kr.mode.name],
                                             output_format=self.output_format,
                                             verbose=self.verbose,
                                             very_verbose=self.very_verbose,
                                             )

            shuffle_list: List = kw.build_shuffle_list(kr.column_names)

            input_data_lines: int = 0
            row: List[str]
            for row in kr:
                input_data_lines += 1
                kw.write(row, shuffle_list=shuffle_list)

            # Flush the output file so far:
            kw.flush()

            if self.verbose:
                print("Read %d data lines from file %s" % (input_data_lines, self.input_kgtk_file),
                      file=self.error_file,
                      flush=True)

            kw.close()
        except SystemExit as e:
            raise KGTKException("Exit requested")
        except Exception as e:
            raise KGTKException(str(e))
