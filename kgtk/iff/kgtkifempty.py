"""Copy records from the first KGTK file to the output file, if one or more
columns are (any/all) (not) empty.  If --only-count is True, report the count
of qualifying records but do not write the output file.

"""

from argparse import ArgumentParser, Namespace
import attr
from pathlib import Path
import sys
import typing

from kgtk.kgtkformat import KgtkFormat
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
from kgtk.io.kgtkwriter import KgtkWriter
from kgtk.utils.argparsehelpers import optional_bool
from kgtk.value.kgtkvalueoptions import KgtkValueOptions

@attr.s(slots=True, frozen=True)
class KgtkIfEmpty(KgtkFormat):
    input_file_path: typing.Optional[Path] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Path)))

    filter_column_names: typing.List[str] = attr.ib(validator=attr.validators.deep_iterable(member_validator=attr.validators.instance_of(str),
                                                                                            iterable_validator=attr.validators.instance_of(list)))

    output_file_path: typing.Optional[Path] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Path)))

    all_are: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    notempty: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    only_count: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    # TODO: find working validators
    # value_options: typing.Optional[KgtkValueOptions] = attr.ib(attr.validators.optional(attr.validators.instance_of(KgtkValueOptions)), default=None)
    reader_options: typing.Optional[KgtkReaderOptions]= attr.ib(default=None)
    value_options: typing.Optional[KgtkValueOptions] = attr.ib(default=None)

    error_file: typing.TextIO = attr.ib(default=sys.stderr)
    verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    very_verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    def filter(self,
               row: typing.List[str],
               filter_idx_list: typing.List[int])->bool:
        idx: int
        if self.notempty == False and self.all_are == False:
            # if any are empty.
            for idx in filter_idx_list:
                if len(row[idx]) == 0:
                    return True
            return False

        elif self.notempty == False and self.all_are == True:
            # if all are empty.
            for idx in filter_idx_list:
                if len(row[idx]) != 0:
                    return False
            return True
            
        elif self.notempty == True and self.all_are == False:
            # If any are not empty.
            for idx in filter_idx_list:
                if len(row[idx]) != 0:
                    return True
            return False
        
        else:
            # if all are not empty:
            for idx in filter_idx_list:
                if len(row[idx]) == 0:
                    return False
            return True

    def process(self):
        # Open the input file.
        if self.verbose:
            if self.input_file_path is not None:
                print("Opening the input file: %s" % self.input_file_path, file=self.error_file, flush=True)
            else:
                print("Reading the input data from stdin", file=self.error_file, flush=True)

        kr: KgtkReader =  KgtkReader.open(self.input_file_path,
                                          error_file=self.error_file,
                                          options=self.reader_options,
                                          value_options = self.value_options,
                                          verbose=self.verbose,
                                          very_verbose=self.very_verbose,
        )

        filter_idx_list: typing.List[int] = [ ]
        column_name: str
        for column_name in self.filter_column_names:
            if column_name not in kr.column_name_map:
                raise ValueError("Column %s is not in the input file" % (column_name))
            filter_idx_list.append(kr.column_name_map[column_name])
            

        if not self.only_count:
            if self.verbose:
                print("Opening the output file: %s" % self.output_file_path, file=self.error_file, flush=True)
            ew: KgtkWriter = KgtkWriter.open(kr.column_names,
                                             self.output_file_path,
                                             mode=kr.mode,
                                             require_all_columns=False,
                                             prohibit_extra_columns=True,
                                             fill_missing_columns=True,
                                             gzip_in_parallel=False,
                                             verbose=self.verbose,
                                             very_verbose=self.very_verbose)        

        if self.verbose:
            print("Filtering records from %s" % self.input_file_path, file=self.error_file, flush=True)
        input_line_count: int = 0
        output_line_count: int = 0;

        row: typing.list[str]
        for row in kr:
            input_line_count += 1
            if self.filter(row, filter_idx_list):
                if not self.only_count:
                    ew.write(row)
                output_line_count += 1


        if self.only_count:
            print("Read %d records, %d records passed the filter." % (input_line_count, output_line_count), file=self.error_file, flush=True)
        else:
            if self.verbose:
                print("Read %d records, wrote %d records." % (input_line_count, output_line_count), file=self.error_file, flush=True)
        
            ew.close()

def main():
    """
    Test the KGTK ifempty processor.
    """
    parser: ArgumentParser = ArgumentParser()

    parser.add_argument(dest="input_file_path", help="The KGTK file with the input data", type=Path, nargs="?")

    parser.add_argument(      "--columns", dest="filter_column_names", help="The columns to filter on (default=None).", nargs='+', required=True)

    parser.add_argument(      "--count", dest="only_count", help="Only count the records, do not copy them. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument("-o", "--output-file", dest="output_file_path", help="The KGTK file to write (default=%(default)s).", type=Path, default="-")
    
    parser.add_argument(      "--all", dest="all_are", help="False: Test if any are, True: test if all are (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--not-empty", dest="notempty", help="False: test if empty, True: test if not empty (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)


    KgtkReader.add_debug_arguments(parser)
    KgtkReaderOptions.add_arguments(parser, mode_options=True)
    KgtkValueOptions.add_arguments(parser)

    args: Namespace = parser.parse_args()

    error_file: typing.TextIO = sys.stdout if args.errors_to_stdout else sys.stderr

    # Build the option structures.                                                                                                                          
    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_args(args)
    value_options: KgtkValueOptions = KgtkValueOptions.from_args(args)

   # Show the final option structures for debugging and documentation.                                                                                             
    if args.show_options:
        # TODO: show ifempty-specific options.
        reader_options.show(out=error_file)
        value_options.show(out=error_file)

    ie: KgtkIfEmpty = KgtkIfEmpty(
        input_file_path=args.input_file_path,
        filter_column_names=args.filter_column_names,
        output_file_path=args.output_file_path,
        all_are=args.all_are,
        notempty=args.notempty,
        only_count = args.only_count,
        reader_options=reader_options,
        value_options=value_options,
        error_file=error_file,
        verbose=args.verbose,
        very_verbose=args.very_verbose)

    ie.process()

if __name__ == "__main__":
    main()
