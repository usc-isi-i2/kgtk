"""Copy records from the first KGTK file to the output file,
imploding data type-specific columns into a single column./

TODO: Add a reject file.

"""

from argparse import ArgumentParser, Namespace
import ast
import attr
from pathlib import Path
import sys
import typing

from kgtk.kgtkformat import KgtkFormat
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
from kgtk.io.kgtkwriter import KgtkWriter
from kgtk.utils.argparsehelpers import optional_bool
from kgtk.value.kgtkvalue import KgtkValue, KgtkValueFields
from kgtk.value.kgtkvalueoptions import KgtkValueOptions, DEFAULT_KGTK_VALUE_OPTIONS

@attr.s(slots=True, frozen=True)
class KgtkImplode(KgtkFormat):
    input_file_path: Path = attr.ib(validator=attr.validators.instance_of(Path))

    output_file_path: typing.Optional[Path] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Path)))

    type_names: typing.List[str] = \
        attr.ib(validator=attr.validators.deep_iterable(member_validator=attr.validators.instance_of(str),
                                                        iterable_validator=attr.validators.instance_of(list)))

    # attr.converters.default_if_none(...) does not seem to work.
    reader_options: KgtkReaderOptions = attr.ib(validator=attr.validators.instance_of(KgtkReaderOptions))
    value_options: KgtkValueOptions = attr.ib(validator=attr.validators.instance_of(KgtkValueOptions))

    column_name: str = attr.ib(validator=attr.validators.instance_of(str), default=KgtkFormat.NODE2)
    overwrite_column: bool = attr.ib(validator=attr.validators.instance_of(bool), default=True)

    prefix: str = attr.ib(validator=attr.validators.instance_of(str), default= KgtkFormat.NODE2 + ";" + KgtkFormat.KGTK_NAMESPACE)
                               
    validate: bool = attr.ib(validator=attr.validators.instance_of(bool), default=True)

    # attr.converters.default_if_none(...) does not seem to work.
    # value_options: KgtkValueOptions = attr.ib(default=None,
    #                                           converter=attr.converters.default_if_none(DEFAULT_KGTK_VALUE_OPTIONS),
    #                                           validator=attr.validators.instance_of(KgtkValueOptions))

    error_file: typing.TextIO = attr.ib(default=sys.stderr)
    verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    very_verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    def process(self):
        if len(self.column_name) == 0:
            raise ValueError("The name of the column to explode is empty.")

        selected_field_names: typing.List[str] = [ ]
        field_name: str

        if self.type_names is not None:
            if self.verbose:
                print("Validate the names of the data types to extract.", file=self.error_file, flush=True)
            type_name: str
            for type_name in self.type_names:
                if type_name not in KgtkValueFields.DEFAULT_DATA_TYPE_FIELDS:
                    raise ValueError("Unknown data type name '%s'." % type_name)
                # Merge this KGTK data type's fields into the list of selected fields:
                for field_name in KgtkValueFields.DEFAULT_DATA_TYPE_FIELDS[type_name]:
                    if field_name not in selected_field_names:
                        selected_field_names.append(field_name)

        if len(selected_field_names) == 0:
            raise ValueError("The list of fields to implode is empty.")

        if KgtkValueFields.DATA_TYPE_FIELD_NAME not in selected_field_names:
            raise ValueError("The data type field '%s' has not been selected." % KgtkValueFields.DATA_TYPE_FIELD_NAME)

        # Open the input file.
        if self.verbose:
            print("Opening the input file: %s" % self.input_file_path, file=self.error_file, flush=True)

        kr: KgtkReader =  KgtkReader.open(self.input_file_path,
                                          error_file=self.error_file,
                                          options=self.reader_options,
                                          value_options = self.value_options,
                                          verbose=self.verbose,
                                          very_verbose=self.very_verbose,
        )

        new_column: bool # True ==> adding the imploded column, False ==> using an existing column
        column_idx: int # The index of the imploded column (new or old).
        output_column_names: typing.List[str] = kr.column_names.copy()
        if self.column_name in kr.column_name_map:
            column_idx = kr.column_name_map[self.column_name]
            new_column = False
            if not self.overwrite_column:
                raise ValueError("Imploded column '%s' (idx %d) already exists and overwrite not allowed." % (self.column_name, column_idx))
            if self.verbose:
                print("Overwriting existing imploded column '%s' (idx %d)." % (self.column_name, column_idx), file=self.error_file, flush=True)
        else:
            column_idx = len(output_column_names)
            new_column = True
            output_column_names.append(self.column_name)
            if self.verbose:
                print("Imploded column '%s' will be created (idx %d)." % (self.column_name, column_idx), file=self.error_file, flush=True)

        if self.verbose:
            print("Build the map of field names to exploded columns", file=self.error_file, flush=True)
        implosion: typing.MutableMapping[str, int] = { }
        missing_columns: typing.List[str] = [ ]
        for field_name in selected_field_names:
            exploded_name: str = self.prefix + field_name
            if self.verbose:
                print("Field '%s' becomes '%s'" % (field_name, exploded_name), file=self.error_file, flush=True)
            if exploded_name in implosion:
                raise ValueError("Field name '%s' is duplicated in the field list.")
            if exploded_name in kr.column_names:
                exploded_idx = kr.column_name_map[exploded_name]
                implosion[field_name] = exploded_idx
                if self.verbose:
                    print("Field '%s' is in column '%s' (idx=%d)" % (field_name, exploded_name, exploded_idx),
                              file=self.error_file, flush=True)
            else:
                if self.verbose:
                    print("Field '%s' eploded column '%s' not found." % (field_name, exploded_name), file=self.error_file, flush=True)
                missing_columns.append(exploded_name)
        if len(missing_columns) > 0:
            raise ValueError("Missing columns: %s" % " ".join(missing_columns))
                
        data_type_idx = implosion[KgtkValueFields.DATA_TYPE_FIELD_NAME]

        ew: typing.Optional[KgtkWriter]
        if self.output_file_path is not None:
            if self.verbose:
                print("Opening output file %s" % str(self.output_file_path), file=self.error_file, flush=True)
            # Open the output file.
            ew: KgtkWriter = KgtkWriter.open(output_column_names,
                                             self.output_file_path,
                                             mode=kr.mode,
                                             require_all_columns=False,
                                             prohibit_extra_columns=True,
                                             fill_missing_columns=False,
                                             gzip_in_parallel=False,
                                             verbose=self.verbose,
                                             very_verbose=self.very_verbose)        
        
        if self.verbose:
            print("Imploding records from %s" % self.input_file_path, file=self.error_file, flush=True)
        input_line_count: int = 0
        imploded_value_count: int = 0
        
        row: typing.List[str]
        for row in kr:
            input_line_count += 1

            value: str = self.implode(input_line_count, row, implosion, data_type_idx)
            if len(value) > 0:
                imploded_value_count += 1
                
            if ew is not None:
                output_row: typing.List[str] = row.copy()
                if new_column:
                    output_row.append(value)
                else:
                    output_row[column_idx] = value
                ew.write(output_row)
                
        if self.verbose:
            print("Processed %d records, imploded %d values." % (input_line_count, imploded_value_count), file=self.error_file, flush=True)
        
        if ew is not None:
            ew.close()
            
    def implode_empty(self,
                      input_line_count: int,
                      row: typing.List[str],
                      implosion: typing.Mapping[str, int],
                      type_name: str,                      
    )->str:
        return ""


    def implode_list(self,
                     input_line_count: int,
                     row: typing.List[str],
                     implosion: typing.Mapping[str, int],
                     type_name: str,                      
    )->str:
        if self.verbose:
            print("Input line %d: data type '%s' is not supported for implode." % (input_line_count, type_name),
                  file=self.error_file, flush=True)
        return ""

    def implode_(self,
                     input_line_count: int,
                     row: typing.List[str],
                     implosion: typing.Mapping[str, int],
                     type_name: str,                      
    )->str:
        pass

    def implode_number(self,
                       input_line_count: int,
                       row: typing.List[str],
                       implosion: typing.Mapping[str, int],
                       type_name: str,                      
    )->str:
        num_idx: int = implosion[KgtkValueFields.NUMBER_FIELD_NAME]
        num_val: str = row[num_idx]
        if len(num_val) == 0:
            if self.verbose:
                print("Input line %d: data type '%s': %s field is empty" % (input_line_count, type_name, KgtkValueFields.NUMBER_FIELD_NAME),
                      file=self.error_file, flush=True)
        value = num_val

        if self.validate:
            kv: KgtkValue = KgtkValue(value, options=self.value_options)
            if not kv.is_number(validate=True):
                if self.verbose:
                    print("Input line %d: data type '%s': imploded value '%s' is not a valid number." % (input_line_count, type_name, value),
                          file=self.error_file, flush=True)
        return value

    def implode_quantity(self,
                         input_line_count: int,
                         row: typing.List[str],
                         implosion: typing.Mapping[str, int],
                         type_name: str,                      
    )->str:
        num_idx2: int = implosion[KgtkValueFields.NUMBER_FIELD_NAME]
        num_val2: str = row[num_idx2]
        if len(num_val2) == 0:
            if self.verbose:
                print("Input line %d: data type '%s': %s field is empty" % (input_line_count, type_name, KgtkValueFields.NUMBER_FIELD_NAME),
                      file=self.error_file, flush=True)
        lt: str = row[implosion[KgtkValueFields.LOW_TOLERANCE_FIELD_NAME]]
        ht: str = row[implosion[KgtkValueFields.HIGH_TOLERANCE_FIELD_NAME]]
        if len(lt) > 0 ^ len(ht) > 0:
            if self.verbose:
                print("Input line %d: data type '%s': low and high tolerance must both be present or absent." % (input_line_count, type_name),
                      file=self.error_file, flush=True)
        si: str = row[implosion[KgtkValueFields.SI_UNITS_FIELD_NAME]]
        un: str = row[implosion[KgtkValueFields.UNITS_NODE_FIELD_NAME]]
        value = num_val2
        if len(lt) > 0 or len(ht) > 0:
            value += "[" + lt + "," + ht + "]"
        value += si + un

        if self.validate:
            kv: KgtkValue = KgtkValue(value, options=self.value_options)
            if not kv.is_quantity(validate=True):
                if self.verbose:
                    print("Input line %d: data type '%s': imploded value '%s' is not a valid quantity." % (input_line_count, type_name, value),
                          file=self.error_file, flush=True)
        return value

    def implode_string(self,
                       input_line_count: int,
                       row: typing.List[str],
                       implosion: typing.Mapping[str, int],
                       type_name: str,                      
    )->str:
        text_idx: int = implosion[KgtkValueFields.TEXT_FIELD_NAME]
        text_val: str = row[text_idx]
        if len(text_val) == 0:
            if self.verbose:
                print("Input line %d: data type '%s': %s field is empty" % (input_line_count, type_name, KgtkValueFields.TEXT_FIELD_NAME),
                      file=self.error_file, flush=True)
        value = text_val

        if self.validate:
            kv: KgtkValue = KgtkValue(value, options=self.value_options)
            if not kv.is_string(validate=True):
                if self.verbose:
                    print("Input line %d: data type '%s': imploded value '%s' is not a valid string." % (input_line_count, type_name, value),
                          file=self.error_file, flush=True)
        return value

    def implode_language_qualified_string(self,
                                          input_line_count: int,
                                          row: typing.List[str],
                                          implosion: typing.Mapping[str, int],
                                          type_name: str,                      
    )->str:
        text_idx2: int = implosion[KgtkValueFields.TEXT_FIELD_NAME]
        text_val2: str = row[text_idx2]
        if len(text_val2) == 0:
            if self.verbose:
                print("Input line %d: data type '%s': %s field is empty" % (input_line_count, type_name, KgtkValueFields.TEXT_FIELD_NAME),
                      file=self.error_file, flush=True)

        if text_val2.startswith('"'):
            # Need to replace the double quotes with single quotes.
            if len(text_val2) < 2:
                text_val2 = "''"
            else:
                # TODO: Need to catch exceptions from ast.literal_eval(...)
                text_val2 = repr(ast.literal_eval(text_val2)).replace('|', '\\|')
        else:
            if self.verbose:
                print("Input line %d: data type '%s': field '%s': text does not begin with a double quote." % (input_line_count, type_name, KgtkValueFields.TEXT_FIELD_NAME),
                      file=self.error_file, flush=True)

        language_idx: int = implosion[KgtkValueFields.LANGUAGE_FIELD_NAME]
        language_val: str = row[language_idx]
        if len(language_val) == 0:
            if self.verbose:
                print("Input line %d: data type '%s': %s field is empty" % (input_line_count, type_name, KgtkValueFields.LANGUAGE_FIELD_NAME),
                      file=self.error_file, flush=True)

        suf: str = row[implosion[KgtkValueFields.LANGUAGE_SUFFIX_FIELD_NAME]]

        value = text_val2 + "@" + language_val
        if len(suf) > 0:
            value += suf            

        if self.validate:
            kv: KgtkValue = KgtkValue(value, options=self.value_options)
            if not kv.is_language_qualified_string(validate=True):
                if self.verbose:
                    print("Input line %d: data type '%s': imploded value '%s' is not a valid language qualified string." % (input_line_count, type_name, value),
                          file=self.error_file, flush=True)
        return value

    def implode_location_coordinates(self,
                                     input_line_count: int,
                                     row: typing.List[str],
                                     implosion: typing.Mapping[str, int],
                                     type_name: str,                      
    )->str:
        latitude_idx: int = implosion[KgtkValueFields.LATITUDE_FIELD_NAME]
        latitude_val: str = row[latitude_idx]
        if len(latitude_val) == 0:
            if self.verbose:
                print("Input line %d: data type '%s': %s field is empty" % (input_line_count, type_name, KgtkValueFields.LATITUDE_FIELD_NAME),
                      file=self.error_file, flush=True)

        longitude_idx: int = implosion[KgtkValueFields.LONGITUDE_FIELD_NAME]
        longitude_val: str = row[longitude_idx]
        if len(longitude_val) == 0:
            if self.verbose:
                print("Input line %d: data type '%s': %s field is empty" % (input_line_count, type_name, KgtkValueFields.LONGITUDE_FIELD_NAME),
                      file=self.error_file, flush=True)
        value = "@" + latitude_val + "/" + longitude_val

        if self.validate:
            kv: KgtkValue = KgtkValue(value, options=self.value_options)
            if not kv.is_location_coordinates(validate=True):
                if self.verbose:
                    print("Input line %d: data type '%s': imploded value '%s' is not a valid location coordinates." % (input_line_count, type_name, value),
                          file=self.error_file, flush=True)
        return value

    def implode_date_and_times(self,
                               input_line_count: int,
                               row: typing.List[str],
                               implosion: typing.Mapping[str, int],
                               type_name: str,                      
    )->str:

        date_and_times_idx: int = implosion[KgtkValueFields.DATE_AND_TIMES_FIELD_NAME]
        date_and_times_val: str = row[date_and_times_idx]
        if len(date_and_times_val) == 0:
            if self.verbose:
                print("Input line %d: data type '%s': %s field is empty" % (input_line_count, type_name, KgtkValueFields.DATE_AND_TIMES_FIELD_NAME),
                      file=self.error_file, flush=True)

        precision_idx: int = implosion[KgtkValueFields.PRECISION_FIELD_NAME]
        precision_val: str = row[precision_idx]

        value = "^" + date_and_times_val
        if len(precision_val) > 0:
            value += "/" + precision_val

        if self.validate:
            kv: KgtkValue = KgtkValue(value, options=self.value_options)
            if not kv.is_date_and_times(validate=True):
                if self.verbose:
                    print("Input line %d: data type '%s': imploded value '%s' is not a valid date and time." % (input_line_count, type_name, value),
                          file=self.error_file, flush=True)
        return value

    def implode_extension(self,
                          input_line_count: int,
                          row: typing.List[str],
                          implosion: typing.Mapping[str, int],
                          type_name: str,                      
    )->str:
        if self.verbose:
            print("Input line %d: data type '%s': extensions are not supported." % (input_line_count, type_name))
        return ""

    def implode_boolean(self,
                        input_line_count: int,
                        row: typing.List[str],
                        implosion: typing.Mapping[str, int],
                        type_name: str,                      
    )->str:
        truth_idx: int = implosion[KgtkValueFields.TRUTH_FIELD_NAME]
        truth_val: str = row[truth_idx]
        if len(truth_val) == 0:
            if self.verbose:
                print("Input line %d: data type '%s': %s field is empty" % (input_line_count, type_name, KgtkValueFields.TRUTH_FIELD_NAME),
                      file=self.error_file, flush=True)

        value = truth_val

        if self.validate:
            kv: KgtkValue = KgtkValue(value, options=self.value_options)
            if not kv.is_boolean(validate=True):
                if self.verbose:
                    print("Input line %d: data type '%s': imploded value '%s' is not a valid boolean." % (input_line_count, type_name, value),
                          file=self.error_file, flush=True)

        return value

    def implode_symbol(self,
                       input_line_count: int,
                       row: typing.List[str],
                       implosion: typing.Mapping[str, int],
                       type_name: str,                      
    )->str:
        symbol_idx: int = implosion[KgtkValueFields.SYMBOL_FIELD_NAME]
        symbol_val: str = row[symbol_idx]
        if len(symbol_val) == 0:
            if self.verbose:
                print("Input line %d: data type '%s': %s field is empty" % (input_line_count, type_name, KgtkValueFields.SYMBOL_FIELD_NAME),
                      file=self.error_file, flush=True)

        value = symbol_val

        if self.validate:
            kv: KgtkValue = KgtkValue(value, options=self.value_options)
            if not kv.is_symbol(validate=True):
                if self.verbose:
                    print("Input line %d: data type '%s': imploded value '%s' is not a valid symbol." % (input_line_count, type_name, value),
                          file=self.error_file, flush=True)

        return value

    # The imploder dispatch table:
    imploders: typing.Mapping[KgtkFormat.DataType, typing.Callable[[KgtkImplode, int, typing.List[str], typing.Mapping[str, int], str], str]] = {
        KgtkFormat.DataType.EMPTY: implode_empty,
        KgtkFormat.DataType.LIST: implode_list,
        KgtkFormat.DataType.NUMBER: implode_number,
        KgtkFormat.DataType.QUANTITY: implode_quantity,
        KgtkFormat.DataType.STRING: implode_string,
        KgtkFormat.DataType.LANGUAGE_QUALIFIED_STRING: implode_language_qualified_string,
        KgtkFormat.DataType.LOCATION_COORDINATES: implode_location_coordinates,
        KgtkFormat.DataType.DATE_AND_TIMES: implode_date_and_times,
        KgtkFormat.DataType.EXTENSION: implode_extension,
        KgtkFormat.DataType.BOOLEAN: implode_boolean,
        KgtkFormat.DataType.SYMBOL: implode_symbol,
    }

    def implode(self,
                input_line_count: int,
                row: typing.List[str],
                implosion: typing.Mapping[str, int],
                data_type_idx: int,
    )->str:
        type_name: str = row[data_type_idx]
        if type_name.lower() not in self.type_names:
            if self.verbose:
                print("Input line %d: unselected data type '%s'." % (input_line_count, type_name), file=self.error_file, flush=True)
            return ""

        if type_name.upper() not in KgtkFormat.DataType.__members__:
            # TODO:  Need warnings.
            if self.verbose:
                print("Input line %d: unrecognized data type '%s'." % (input_line_count, type_name), file=self.error_file, flush=True)
            return ""

        dt: KgtkFormat.DataType = KgtkFormat.DataType[type_name.upper()]
        return self.imploders[dt](self, input_line_count, row, implosion, type_name)

def main():
    """
    Test the KGTK ifempty processor.
    """
    parser: ArgumentParser = ArgumentParser()

    parser.add_argument(dest="input_file_path", help="The KGTK file with the input data. (default=%(default)s)", type=Path, nargs="?", default="-")

    parser.add_argument(      "--column", dest="column_name", help="The name of the column to explode. (default=%(default)s).", default="node2")

    fgroup: ArgumentParser = parser.add_mutually_exclusive_group()

    fgroup.add_argument(      "--types", dest="type_names", nargs='*',
                               help="The KGTK data types for which fields should be imploded. (default=%(default)s).",
                               choices=KgtkFormat.DataType.choices(),
                               default=KgtkFormat.DataType.choices())

    parser.add_argument("-o", "--output-file", dest="output_file_path", help="The KGTK file to write (default=%(default)s).", type=Path, default="-")
    
    parser.add_argument(      "--prefix", dest="prefix", help="The prefix for exploded column names. (default=%(default)s).", default="node2;kgtk:")

    parser.add_argument(      "--overwrite", dest="overwrite_column",
                              help="Indicate that it is OK to overwrite an existing imploded column. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=True)

    parser.add_argument(      "--validate", dest="validate",
                              help="Validate imploded values. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=True)

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
        print("input: %s" % str(args.input_file_path), file=error_file, flush=True)
        print("--column %s" % args.column_name, file=error_file, flush=True)
        print("--prefix %s" % args.prefix, file=error_file, flush=True)
        print("--overwrite %s" % str(args.overwrite_column), file=error_file, flush=True)
        if args.type_names is not None:
            print("--types %s" % " ".join(args.type_names), file=error_file, flush=True)
        print("--output-file=%s" % str(args.output_file_path))
        reader_options.show(out=error_file)
        value_options.show(out=error_file)

    ex: KgtkExplode = KgtkExplode(
        input_file_path=args.input_file_path,
        column_name=args.column_name,
        prefix=args.prefix,
        type_names=args.type_names,
        overwrite_column=args.overwrite_column,
        output_file_path=args.output_file_path,
        reader_options=reader_options,
        value_options=value_options,
        error_file=error_file,
        verbose=args.verbose,
        very_verbose=args.very_verbose)

    ex.process()

if __name__ == "__main__":
    main()
