from pathlib import Path
import sys

from kgtk.exceptions import kgtk_exception_auto_handler, KGTKException
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
from kgtk.io.kgtkwriter import KgtkWriter
from kgtk.value.kgtkvalueoptions import KgtkValueOptions
from typing import List, TextIO


class RemoveColumns(object):
    def __init__(self,
                 input_kgtk_file: Path,
                 output_kgtk_file: Path,
                 columns: List[str],
                 split_on_commas: bool = True,
                 split_on_spaces: bool = False,
                 strip_spaces: bool = True,
                 all_except: bool = False,
                 ignore_missing_columns: bool = False,
                 reader_options: KgtkReaderOptions = None,
                 value_options: KgtkValueOptions = None,
                 error_file: TextIO = sys.stderr,
                 show_options: bool = False,
                 verbose: bool = False,
                 very_verbose: bool = False,
                 ):
        self.input_kgtk_file = input_kgtk_file
        self.output_kgtk_file = output_kgtk_file
        self.columns = columns if columns is not None else []
        self.split_on_commas = split_on_commas
        self.split_on_spaces = split_on_spaces
        self.strip_spaces = strip_spaces
        self.all_except = all_except
        self.ignore_missing_columns = ignore_missing_columns
        self.reader_options = reader_options
        self.value_options = value_options
        self.error_file = error_file
        self.show_options = show_options
        self.verbose = verbose
        self.very_verbose = very_verbose

    def process(self):
        if self.show_options:
            print("--input-file=%s" % str(self.input_kgtk_file), file=self.error_file)
            print("--output-file=%s" % str(self.output_kgtk_file), file=self.error_file)
            if self.columns is not None:
                print("--columns=%s" % " ".join(self.columns), file=self.error_file)
            print("--split-on-commas=%s" % str(self.split_on_commas), file=self.error_file)
            print("--split-on-spaces=%s" % str(self.split_on_spaces), file=self.error_file)
            print("--strip-spaces=%s" % str(self.strip_spaces), file=self.error_file)
            print("--all-except=%s" % str(self.all_except), file=self.error_file)
            print("--ignore-missing-columns=%s" % str(self.ignore_missing_columns), file=self.error_file)
            self.reader_options.show(out=self.error_file)
            self.value_options.show(out=self.error_file)
            print("=======", file=self.error_file, flush=True)

        try:

            if self.split_on_spaces:
                # We will be very lenient, and allow space-seperated arguments
                # *inside* shell quoting, e.g.
                #
                # kgtk remove_columns -c 'name name2 name3'
                #
                # Do not enable this option if spaces are legal inside your
                # column names.
                self.columns = " ".join(self.columns).split()
            remove_columns: List[str] = []
            arg: str
            column_name: str
            for arg in self.columns:
                if self.split_on_commas:
                    for column_name in arg.split(","):
                        if self.strip_spaces:
                            column_name = column_name.strip()
                        if len(column_name) > 0:
                            remove_columns.append(column_name)
                else:
                    if self.strip_spaces:
                        arg = arg.strip()
                    if len(arg) > 0:
                        remove_columns.append(arg)
            if self.verbose:
                if self.all_except:
                    print(
                        "Removing all columns except %d columns: %s" % (len(remove_columns), " ".join(remove_columns)),
                        file=self.error_file, flush=True)
                else:
                    print("Removing %d columns: %s" % (len(remove_columns), " ".join(remove_columns)),
                          file=self.error_file,
                          flush=True)
            if len(remove_columns) == 0:
                raise KGTKException("No columns to remove")

            if self.verbose:
                print("Opening the input file: %s" % str(self.input_kgtk_file), file=self.error_file, flush=True)
            kr: KgtkReader = KgtkReader.open(self.input_kgtk_file,
                                             options=self.reader_options,
                                             value_options=self.value_options,
                                             error_file=self.error_file,
                                             verbose=self.verbose,
                                             very_verbose=self.very_verbose,
                                             )

            output_column_names: List[str]

            trouble_column_names: List[str] = []
            if self.all_except:
                if not self.ignore_missing_columns:
                    for column_name in remove_columns:
                        if column_name not in kr.column_names:
                            print("Error: cannot retain unknown column '%s'." % column_name, file=self.error_file,
                                  flush=True)
                            trouble_column_names.append(column_name)

                output_column_names = []
                for column_name in kr.column_names:
                    if column_name in remove_columns:
                        output_column_names.append(column_name)

            else:
                output_column_names = kr.column_names.copy()
                for column_name in remove_columns:
                    if column_name in output_column_names:
                        output_column_names.remove(column_name)

                    elif not self.ignore_missing_columns:
                        print("Error: cannot remove unknown column '%s'." % column_name, file=self.error_file,
                              flush=True)
                        trouble_column_names.append(column_name)

            if len(trouble_column_names) > 0:
                raise KGTKException("Unknown columns %s" % " ".join(trouble_column_names))

            if self.verbose:
                print("Opening the output file: %s" % str(self.output_kgtk_file), file=self.error_file, flush=True)
            kw: KgtkWriter = KgtkWriter.open(output_column_names,
                                             self.output_kgtk_file,
                                             mode=KgtkWriter.Mode[kr.mode.name],
                                             verbose=self.verbose,
                                             very_verbose=self.very_verbose)

            shuffle_list: List[int] = kw.build_shuffle_list(kr.column_names)

            input_line_count: int = 0
            row: List[str]
            for row in kr:
                input_line_count += 1
                kw.write(row, shuffle_list=shuffle_list)

            if self.verbose:
                print("Processed %d rows." % input_line_count, file=self.error_file, flush=True)

            kw.close()

        except Exception as e:
            kgtk_exception_auto_handler(e)
