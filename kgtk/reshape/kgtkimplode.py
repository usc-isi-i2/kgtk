"""Copy records from the first KGTK file to the output file,
imploding data type-specific columns into a single column./
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
from kgtk.reshape.kgtkidbuilder import KgtkIdBuilder, KgtkIdBuilderOptions
from kgtk.utils.argparsehelpers import optional_bool
from kgtk.value.kgtkvalue import KgtkValue, KgtkValueFields
from kgtk.value.kgtkvalueoptions import KgtkValueOptions, DEFAULT_KGTK_VALUE_OPTIONS

@attr.s(slots=True, frozen=True)
class KgtkImplode(KgtkFormat):
    input_file_path: Path = attr.ib(validator=attr.validators.instance_of(Path))

    output_file_path: typing.Optional[Path] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Path)))

    reject_file_path: typing.Optional[Path] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Path)))

    type_names: typing.List[str] = \
        attr.ib(validator=attr.validators.deep_iterable(member_validator=attr.validators.instance_of(str),
                                                        iterable_validator=attr.validators.instance_of(list)))

    without_fields: typing.List[str] = \
        attr.ib(validator=attr.validators.deep_iterable(member_validator=attr.validators.instance_of(str),
                                                        iterable_validator=attr.validators.instance_of(list)))

    # attr.converters.default_if_none(...) does not seem to work.
    reader_options: KgtkReaderOptions = attr.ib(validator=attr.validators.instance_of(KgtkReaderOptions))
    value_options: KgtkValueOptions = attr.ib(validator=attr.validators.instance_of(KgtkValueOptions))

    column_name: str = attr.ib(validator=attr.validators.instance_of(str), default=KgtkFormat.NODE2)
    overwrite_column: bool = attr.ib(validator=attr.validators.instance_of(bool), default=True)

    prefix: str = attr.ib(validator=attr.validators.instance_of(str), default= KgtkFormat.NODE2 + ";" + KgtkFormat.KGTK_NAMESPACE)
                               
    validate: bool = attr.ib(validator=attr.validators.instance_of(bool), default=True)

    escape_pipes: bool = attr.ib(validator=attr.validators.instance_of(bool), default=True)

    quantities_include_numbers: bool = attr.ib(validator=attr.validators.instance_of(bool), default=True)

    general_strings: bool = attr.ib(validator=attr.validators.instance_of(bool), default=True)

    remove_prefixed_columns: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    ignore_unselected_types: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    retain_unselected_types: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    # Some messages are noisy unless asked to be quiet. Verbose overrides this.
    quiet: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    # attr.converters.default_if_none(...) does not seem to work.
    # value_options: KgtkValueOptions = attr.ib(default=None,
    #                                           converter=attr.converters.default_if_none(DEFAULT_KGTK_VALUE_OPTIONS),
    #                                           validator=attr.validators.instance_of(KgtkValueOptions))

    build_id: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    idbuilder_options: typing.Optional[KgtkIdBuilderOptions] = attr.ib(default=None)

    error_file: typing.TextIO = attr.ib(default=sys.stderr)
    verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    very_verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    def unwrap(self, val: str)->str:
        """
        Remove optional outer string wrappers from a number or symbol
        extracted from an exploded column.

        We do *not* attempt to remove escape characters (\) from the body
        of the value:  they should not appear in numbers, and are
        discouraged in symbols.

        We do *not* attempt to undouble internal quotes (("") or ('')) from the
        body of the value: they should not appear in numbers, and are
        discouraged in symbols.

        We accept the following wrappers:
        triple double quotes
        triple single quotes
        double quotes
        single quotes
        """
        if len(val) >= 6:
            if val.startswith('"""') and val.endswith('"""'):
                return val[3:-3]
            elif val.startswith("'''") and val.endswith("'''"):
                return val[3:-3]
        if len(val) >= 2:
            if val.startswith('"') and val.endswith('"'):
                return val[1:-1]
            elif val.startswith("'") and val.endswith("'"):
                return val[1:-1]
        return val        

    def implode_empty(self,
                      input_line_count: int,
                      row: typing.List[str],
                      implosion: typing.Mapping[str, int],
                      type_name: str,                      
    )->typing.Tuple[str, bool]:
        return "", True


    def implode_list(self,
                     input_line_count: int,
                     row: typing.List[str],
                     implosion: typing.Mapping[str, int],
                     type_name: str,                      
    )->typing.Tuple[str, bool]:
        if self.verbose or not self.quiet:
            print("Input line %d: data type '%s' is not supported for implode." % (input_line_count, type_name),
                  file=self.error_file, flush=True)
        return "", False

    def implode_number(self,
                       input_line_count: int,
                       row: typing.List[str],
                       implosion: typing.Mapping[str, int],
                       type_name: str,                      
    )->typing.Tuple[str, bool]:
        valid: bool = True
        num_idx: int = implosion[KgtkValueFields.NUMBER_FIELD_NAME]
        num_val: str = self.unwrap(row[num_idx])
        if len(num_val) == 0:
            valid = False
            if self.verbose or not self.quiet:
                print("Input line %d: data type '%s': %s field is empty" % (input_line_count, type_name, KgtkValueFields.NUMBER_FIELD_NAME),
                      file=self.error_file, flush=True)
        value: str = num_val

        if valid and self.validate:
            kv: KgtkValue = KgtkValue(value, options=self.value_options)
            valid = kv.is_number(validate=True)
            if not valid:
                if self.verbose or not self.quiet:
                    print("Input line %d: data type '%s': imploded value '%s' is not a valid number." % (input_line_count, type_name, value),
                          file=self.error_file, flush=True)
        return value, valid

    def implode_quantity(self,
                         input_line_count: int,
                         row: typing.List[str],
                         implosion: typing.Mapping[str, int],
                         type_name: str,                      
    )->typing.Tuple[str, bool]:
        valid: bool = True
        num_idx: int = implosion[KgtkValueFields.NUMBER_FIELD_NAME]
        num_val: str = self.unwrap(row[num_idx])
        if len(num_val) == 0:
            valid = False
            if self.verbose or not self.quiet:
                print("Input line %d: data type '%s': %s field is empty" % (input_line_count, type_name, KgtkValueFields.NUMBER_FIELD_NAME),
                      file=self.error_file, flush=True)

        lt_idx: int = implosion[KgtkValueFields.LOW_TOLERANCE_FIELD_NAME]
        lt: str = self.unwrap(row[lt_idx]) if lt_idx >= 0 else ""

        ht_idx: int = implosion[KgtkValueFields.HIGH_TOLERANCE_FIELD_NAME]
        ht: str = self.unwrap(row[ht_idx]) if ht_idx >= 0 else ""

        if len(lt) > 0 ^ len(ht) > 0:
            valid = False
            if self.verbose or not self.quiet:
                print("Input line %d: data type '%s': low and high tolerance must both be present or absent." % (input_line_count, type_name),
                      file=self.error_file, flush=True)

        si_idx: int = implosion[KgtkValueFields.SI_UNITS_FIELD_NAME]
        si: str = self.unwrap(row[si_idx]) if si_idx >= 0 else ""

        un_idx: int = implosion[KgtkValueFields.UNITS_NODE_FIELD_NAME]
        un: str = self.unwrap(row[un_idx]) if un_idx >= 0 else ""

        value: str = num_val
        if len(lt) > 0 or len(ht) > 0:
            value += "[" + lt + "," + ht + "]"
        value += si + un

        if valid and self.validate:
            kv: KgtkValue = KgtkValue(value, options=self.value_options)
            if self.quantities_include_numbers:
                valid = kv.is_number_or_quantity(validate=True)
                if not valid:
                    if self.verbose or not self.quiet:
                        print("Input line %d: data type '%s': imploded value '%s' is not a valid quantity or number." % (input_line_count, type_name, value),
                              file=self.error_file, flush=True)
            else:
                valid = kv.is_quantity(validate=True)
                if not valid:
                    if self.verbose or not self.quiet:
                        print("Input line %d: data type '%s': imploded value '%s' is not a valid quantity." % (input_line_count, type_name, value),
                              file=self.error_file, flush=True)
        return value, valid

    def implode_string(self,
                       input_line_count: int,
                       row: typing.List[str],
                       implosion: typing.Mapping[str, int],
                       type_name: str,                      
    )->typing.Tuple[str, bool]:
        valid: bool = True
        if KgtkValueFields.LANGUAGE_FIELD_NAME in implosion:
            language_idx: int = implosion[KgtkValueFields.LANGUAGE_FIELD_NAME]
            if language_idx >= 0:
                language_val: str = self.unwrap(row[language_idx])
                if len(language_val) > 0:
                    if self.general_strings:
                        return self.implode_language_qualified_string(input_line_count, row, implosion, type_name)
                    else:
                        valid = False
                        if self.verbose or not self.quiet:
                            print("Input line %d: data type '%s': %s field is not empty" % (input_line_count, type_name, KgtkValueFields.LANGUAGE_FIELD_NAME),
                                  file=self.error_file, flush=True)
        
        text_idx: int = implosion[KgtkValueFields.TEXT_FIELD_NAME]
        text_val: str = row[text_idx]
        if len(text_val) == 0:
            valid = False
            if self.verbose or not self.quiet:
                print("Input line %d: data type '%s': %s field is empty" % (input_line_count, type_name, KgtkValueFields.TEXT_FIELD_NAME),
                      file=self.error_file, flush=True)
        elif len(text_val) == 1:
            valid = False
            if self.verbose or not self.quiet:
                print("Input line %d: data type '%s': %s field is too short" % (input_line_count, type_name, KgtkValueFields.TEXT_FIELD_NAME),
                      file=self.error_file, flush=True)
        else:
            if not text_val.startswith('"'):
                valid = False
                if self.verbose or not self.quiet:
                    print("Input line %d: data type '%s': %s field does not start with a double quote" % (input_line_count, type_name, KgtkValueFields.TEXT_FIELD_NAME),
                          file=self.error_file, flush=True)
            if not text_val.endswith('"'):
                valid = False
                if self.verbose or not self.quiet:
                    print("Input line %d: data type '%s': %s field does not end with a double quote" % (input_line_count, type_name, KgtkValueFields.TEXT_FIELD_NAME),
                          file=self.error_file, flush=True)

        value: str = ""
        if valid:
            # This subterfuge uses Python's literal parser to parse the string.
            if not self.escape_pipes:
                # ast.literal_eval(...) doesn't treat backslash pipe (\|) as an escaped pipe (|).
                # (this is documented behavior) so we will remove escaped pipes manually.
                text_val = text_val.replace('\\|', '|')
            value = KgtkFormat.stringify(ast.literal_eval(text_val))

        if valid and self.validate:
            kv: KgtkValue = KgtkValue(value, options=self.value_options)
            valid = kv.is_string(validate=True)
            if not valid:
                if self.verbose or not self.quiet:
                    print("Input line %d: data type '%s': imploded value '%s' is not a valid string." % (input_line_count, type_name, value),
                          file=self.error_file, flush=True)
        return value, valid

    def implode_language_qualified_string(self,
                                          input_line_count: int,
                                          row: typing.List[str],
                                          implosion: typing.Mapping[str, int],
                                          type_name: str,                      
    )->typing.Tuple[str, bool]:
        valid: bool = True
        text_idx: int = implosion[KgtkValueFields.TEXT_FIELD_NAME]
        text_val: str = row[text_idx]
        if len(text_val) == 0:
            valid = False
            if self.verbose or not self.quiet:
                print("Input line %d: data type '%s': %s field is empty" % (input_line_count, type_name, KgtkValueFields.TEXT_FIELD_NAME),
                      file=self.error_file, flush=True)

        elif len(text_val) == 1:
            valid = False
            if self.verbose or not self.quiet:
                print("Input line %d: data type '%s': %s field is too short" % (input_line_count, type_name, KgtkValueFields.TEXT_FIELD_NAME),
                      file=self.error_file, flush=True)
        else:
            if not text_val.startswith('"'):
                valid = False
                if self.verbose or not self.quiet:
                    print("Input line %d: data type '%s': %s field does not start with a double quote" % (input_line_count, type_name, KgtkValueFields.TEXT_FIELD_NAME),
                          file=self.error_file, flush=True)
            if not text_val.endswith('"'):
                valid = False
                if self.verbose or not self.quiet:
                    print("Input line %d: data type '%s': %s field does not end with a double quote" % (input_line_count, type_name, KgtkValueFields.TEXT_FIELD_NAME),
                          file=self.error_file, flush=True)

        language_idx: int = implosion[KgtkValueFields.LANGUAGE_FIELD_NAME]
        language_val: str = self.unwrap(row[language_idx])
        if len(language_val) == 0:
            valid = False
            if self.verbose or not self.quiet:
                print("Input line %d: data type '%s': %s field is empty" % (input_line_count, type_name, KgtkValueFields.LANGUAGE_FIELD_NAME),
                      file=self.error_file, flush=True)

        suf_idx: int = implosion[KgtkValueFields.LANGUAGE_SUFFIX_FIELD_NAME]
        suf: str = self.unwrap(row[suf_idx]) if suf_idx >= 0 else ""
        if len(suf) > 0 and not suf.startswith("-"):
            # As a siecial favor, we'll accept language suffixes that do not
            # start with a dash.  We'll prepend the dash.
            suf = "-" + suf

        value: str = ""
        if valid:
            # This subterfuge uses Python's literal parser to parse the string.
            if not self.escape_pipes:
                # ast.literal_eval(...) doesn't treat backslash pipe (\|) as an escaped pipe (|).
                # (this is documented behavior) so we will remove escaped pipes manually.
                text_val = text_val.replace('\\|', '|')
            value = KgtkFormat.stringify(ast.literal_eval(text_val), language=language_val, language_suffix=suf)

        if valid and self.validate:
            kv: KgtkValue = KgtkValue(value, options=self.value_options)
            valid =  kv.is_language_qualified_string(validate=True)
            if not valid:
                if self.verbose or not self.quiet:
                    print("Input line %d: data type '%s': imploded value '%s' is not a valid language qualified string." % (input_line_count, type_name, value),
                          file=self.error_file, flush=True)
        return value, valid

    def implode_location_coordinates(self,
                                     input_line_count: int,
                                     row: typing.List[str],
                                     implosion: typing.Mapping[str, int],
                                     type_name: str,                      
    )->typing.Tuple[str, bool]:
        valid: bool = True
        latitude_idx: int = implosion[KgtkValueFields.LATITUDE_FIELD_NAME]
        latitude_val: str = self.unwrap(row[latitude_idx])
        if len(latitude_val) == 0:
            valid = False
            if self.verbose or not self.quiet:
                print("Input line %d: data type '%s': %s field is empty" % (input_line_count, type_name, KgtkValueFields.LATITUDE_FIELD_NAME),
                      file=self.error_file, flush=True)

        longitude_idx: int = implosion[KgtkValueFields.LONGITUDE_FIELD_NAME]
        longitude_val: str = self.unwrap(row[longitude_idx])
        if len(longitude_val) == 0:
            valid = False
            if self.verbose or not self.quiet:
                print("Input line %d: data type '%s': %s field is empty" % (input_line_count, type_name, KgtkValueFields.LONGITUDE_FIELD_NAME),
                      file=self.error_file, flush=True)

        value: str = "@" + latitude_val + "/" + longitude_val

        if valid and self.validate:
            kv: KgtkValue = KgtkValue(value, options=self.value_options)
            valid =  kv.is_location_coordinates(validate=True)
            if not valid:
                if self.verbose or not self.quiet:
                    print("Input line %d: data type '%s': imploded value '%s' is not a valid location coordinates." % (input_line_count, type_name, value),
                          file=self.error_file, flush=True)
        return value, valid

    def implode_date_and_times(self,
                               input_line_count: int,
                               row: typing.List[str],
                               implosion: typing.Mapping[str, int],
                               type_name: str,                      
    )->typing.Tuple[str, bool]:
        valid: bool = True

        date_and_times_idx: int = implosion[KgtkValueFields.DATE_AND_TIMES_FIELD_NAME]
        date_and_times_val: str = self.unwrap(row[date_and_times_idx])
        if len(date_and_times_val) == 0:
            valid = False
            if self.verbose or not self.quiet:
                print("Input line %d: data type '%s': %s field is empty" % (input_line_count, type_name, KgtkValueFields.DATE_AND_TIMES_FIELD_NAME),
                      file=self.error_file, flush=True)

        precision_idx: int = implosion[KgtkValueFields.PRECISION_FIELD_NAME]
        precision_val: str = self.unwrap(row[precision_idx]) if precision_idx >= 0 else ""

        value: str = "^" + date_and_times_val
        if len(precision_val) > 0:
            value += "/" + precision_val

        if valid and self.validate:
            kv: KgtkValue = KgtkValue(value, options=self.value_options)
            valid = kv.is_date_and_times(validate=True)
            if not valid:
                if self.verbose or not self.quiet:
                    print("Input line %d: data type '%s': imploded value '%s' is not a valid date and time." % (input_line_count, type_name, value),
                          file=self.error_file, flush=True)
        return value, valid

    def implode_extension(self,
                          input_line_count: int,
                          row: typing.List[str],
                          implosion: typing.Mapping[str, int],
                          type_name: str,                      
    )->typing.Tuple[str, bool]:
        if self.verbose or not self.quiet:
            print("Input line %d: data type '%s': extensions are not supported." % (input_line_count, type_name))
        return "", False

    def implode_boolean(self,
                        input_line_count: int,
                        row: typing.List[str],
                        implosion: typing.Mapping[str, int],
                        type_name: str,                      
    )->typing.Tuple[str, bool]:
        valid: bool = True
        truth_idx: int = implosion[KgtkValueFields.TRUTH_FIELD_NAME]
        truth_val: str = self.unwrap(row[truth_idx])
        if len(truth_val) == 0:
            valid = False
            if self.verbose or not self.quiet:
                print("Input line %d: data type '%s': %s field is empty" % (input_line_count, type_name, KgtkValueFields.TRUTH_FIELD_NAME),
                      file=self.error_file, flush=True)

        value: str = truth_val

        if valid and self.validate:
            kv: KgtkValue = KgtkValue(value, options=self.value_options)
            valid = kv.is_boolean(validate=True)
            if not valid:
                if self.verbose or not self.quiet:
                    print("Input line %d: data type '%s': imploded value '%s' is not a valid boolean." % (input_line_count, type_name, value),
                          file=self.error_file, flush=True)

        return value, valid

    def implode_symbol(self,
                       input_line_count: int,
                       row: typing.List[str],
                       implosion: typing.Mapping[str, int],
                       type_name: str,                      
    )->typing.Tuple[str, bool]:
        valid: bool = True
        symbol_idx: int = implosion[KgtkValueFields.SYMBOL_FIELD_NAME]
        symbol_val: str = self.unwrap(row[symbol_idx])
        if len(symbol_val) == 0:
            valid = False
            if self.verbose or not self.quiet:
                print("Input line %d: data type '%s': %s field is empty" % (input_line_count, type_name, KgtkValueFields.SYMBOL_FIELD_NAME),
                      file=self.error_file, flush=True)

        if self.escape_pipes:
            symbol_val = symbol_val.replace(KgtkFormat.LIST_SEPARATOR, "\\" + KgtkFormat.LIST_SEPARATOR)

        value: str = symbol_val

        if valid and self.validate:
            kv: KgtkValue = KgtkValue(value, options=self.value_options)
            valid = kv.is_symbol(validate=True)
            if not valid:
                if self.verbose or not self.quiet:
                    print("Input line %d: data type '%s': imploded value '%s' is not a valid symbol." % (input_line_count, type_name, value),
                          file=self.error_file, flush=True)

        return value, valid

    # The imploder dispatch table:
    imploders: typing.Mapping[KgtkFormat.DataType,
                              typing.Callable[['KgtkImplode',
                                               int,
                                               typing.List[str],
                                               typing.Mapping[str, int],
                                               str],
                                              typing.Tuple[str, bool]]] = {
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
                existing_column_idx: int,
    )->typing.Tuple[str, bool]:
        type_name: str = row[data_type_idx]
        if type_name.upper() not in KgtkFormat.DataType.__members__:
            if self.verbose or not self.quiet:
                print("Input line %d: unrecognized data type '%s'." % (input_line_count, type_name), file=self.error_file, flush=True)
            return "", False

        if type_name.lower() not in self.type_names:
            if self.retain_unselected_types and existing_column_idx >= 0:
                return row[existing_column_idx], True
            elif self.ignore_unselected_types:
                return "", True
            else:
                if self.verbose or not self.quiet:
                    print("Input line %d: unselected data type '%s'." % (input_line_count, type_name), file=self.error_file, flush=True)
                return "", False

        dt: KgtkFormat.DataType = KgtkFormat.DataType[type_name.upper()]
        return self.imploders[dt](self, input_line_count, row, implosion, type_name)

    def process(self):
        if len(self.column_name) == 0:
            raise ValueError("The name of the column to implode is empty.")

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
                    if field_name == KgtkValueFields.VALID_FIELD_NAME:
                        continue # We don't need the valid field.
                    if field_name == KgtkValueFields.LIST_LEN_FIELD_NAME:
                        continue # We don't need the list length field.
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

        output_column_names = kr.column_names.copy()
        new_column: bool # True ==> adding the imploded column, False ==> using an existing column
        column_idx: int # The index of the imploded column (new or old).
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
            if field_name in self.without_fields:
                if self.verbose:
                    print("We can do without field '%s'." % field_name, file=self.error_file, flush=True)
                implosion[field_name] = -1
                continue
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
                    print("Field '%s' exploded column '%s' not found." % (field_name, exploded_name), file=self.error_file, flush=True)
                missing_columns.append(exploded_name)
        if len(missing_columns) > 0:
            raise ValueError("Missing columns: %s" % " ".join(missing_columns))
                
        data_type_idx = implosion[KgtkValueFields.DATA_TYPE_FIELD_NAME]

        # If requested, create the ID column builder.
        # Assemble the list of output column names.
        idb: typing.Optional[KgtkIdBuilder] = None
        if self.build_id:
            if self.idbuilder_options is None:
                raise ValueError("ID build requested but ID builder options are missing")
            idb = KgtkIdBuilder.from_column_names(output_column_names, self.idbuilder_options)
            id_output_column_names = idb.column_names.copy()
        else:
            id_output_column_names = output_column_names.copy()

        trimmed_output_column_names: typing.List[str]
        if self.remove_prefixed_columns and len(self.prefix) > 0:
            trimmed_output_column_names = [ ]
            if self.verbose:
                print("Removing columns with names that start with '%s'." % self.prefix, file=self.error_file, flush=True)
            column_name: str
            for column_name in id_output_column_names:
                if column_name.startswith(self.prefix):
                    if self.verbose:
                        print("Removing column '%s." % column_name, file=self.error_file, flush=True)
                else:
                    trimmed_output_column_names.append(column_name)
        else:
            trimmed_output_column_names = id_output_column_names

        shuffle_list: typing.List[int] = [ ] # Easier to init than deal with typing.Optional.
        ew: typing.Optional[KgtkWriter] = None
        if self.output_file_path is not None:
            if self.verbose:
                print("Opening output file %s" % str(self.output_file_path), file=self.error_file, flush=True)
            # Open the output file.
            ew: KgtkWriter = KgtkWriter.open(trimmed_output_column_names,
                                             self.output_file_path,
                                             mode=kr.mode,
                                             require_all_columns=False,
                                             prohibit_extra_columns=True,
                                             fill_missing_columns=False,
                                             gzip_in_parallel=False,
                                             verbose=self.verbose,
                                             very_verbose=self.very_verbose)
            shuffle_list = ew.build_shuffle_list(id_output_column_names)


        rw: typing.Optional[KgtkWriter] = None
        if self.reject_file_path is not None:
            if self.verbose:
                print("Opening reject file %s" % str(self.reject_file_path), file=self.error_file, flush=True)
            # Open the reject file.
            rw: KgtkWriter = KgtkWriter.open(kr.column_names,
                                             self.reject_file_path,
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
        invalid_value_count: int = 0
        
        existing_column_idx: int = -1 if new_column else column_idx

        row: typing.List[str]
        for row in kr:
            input_line_count += 1

            value: str
            valid: bool
            value, valid = self.implode(input_line_count, row, implosion, data_type_idx, existing_column_idx)
            if valid:
                imploded_value_count += 1
            else:
                invalid_value_count += 1
                
            if rw is not None and not valid:
                # Reject the row before implosion.
                rw.write(row)
            elif ew is not None:
                output_row: typing.List[str] = row.copy()
                if new_column:
                    output_row.append(value)
                else:
                    output_row[column_idx] = value
                if idb is not None:
                    output_row = idb.build(output_row, input_line_count)
                ew.write(output_row, shuffle_list=shuffle_list)
                
        if self.verbose:
            print("Processed %d records, imploded %d values, %d invalid values." % (input_line_count, imploded_value_count, invalid_value_count),
                  file=self.error_file, flush=True)
        
        if ew is not None:
            ew.close()
            
        if rw is not None:
            rw.close()
            
def main():
    """
    Test the KGTK implode processor.
    """
    parser: ArgumentParser = ArgumentParser()

    parser.add_argument(dest="input_file_path", help="The KGTK file with the input data. (default=%(default)s)", type=Path, nargs="?", default="-")

    parser.add_argument(      "--column", dest="column_name", help="The name of the column to explode. (default=%(default)s).", default="node2")

    parser.add_argument(      "--types", dest="type_names", nargs='*',
                               help="The KGTK data types for which fields should be imploded. (default=%(default)s).",
                               choices=KgtkFormat.DataType.choices(),
                               default=KgtkFormat.DataType.choices())

    parser.add_argument(      "--without", dest="without_fields", nargs='*',
                               help="The KGTK fields to do without. (default=%(default)s).",
                               choices=KgtkValueFields.OPTIONAL_DEFAULT_FIELD_NAMES,
                               default=None)

    parser.add_argument("-o", "--output-file", dest="output_file_path", help="The KGTK file to write (default=%(default)s).", type=Path, default="-")
    
    parser.add_argument(      "--prefix", dest="prefix", help="The prefix for exploded column names. (default=%(default)s).", default="node2;kgtk:")

    parser.add_argument(      "--overwrite", dest="overwrite_column",
                              help="Indicate that it is OK to overwrite an existing imploded column. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=True)

    parser.add_argument(      "--validate", dest="validate",
                              help="Validate imploded values. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=True)

    parser.add_argument(      "--escape-pipes", dest="escape_pipes",
                              help="When true, pipe characters (|) need to be escaped (\\|) per KGTK file format. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--quantities-include-numbers", dest="quantities_include_numbers",
                              help="When true, numbers are acceptable quantities. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=True)

    parser.add_argument(      "--general-strings", dest="general_strings",
                              help="When true, strings may include language qualified strings. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=True)

    parser.add_argument(      "--remove-prefixed-columns", dest="remove_prefixed_columns",
                              help="When true, remove all columns beginning with the prefix from the output file. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--ignore-unselected-types", dest="ignore_unselected_types",
                              help="When true, input records with valid but unselected data types will be passed through to output. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=True)

    parser.add_argument(      "--retain-unselected-types", dest="retain_unselected_types",
                              help="When true, input records with valid but unselected data types will be retain existing data on output. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=True)

    parser.add_argument(      "--build-id", dest="build_id",
                              help="Build id values in an id column. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--reject-file", dest="reject_file_path", help="The KGTK file into which to write rejected records (default=%(default)s).",
                              type=Path, default=None)
    
    parser.add_argument(      "--quiet", dest="quiet",
                              help="When true, suppress certain complaints unless verbose. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    KgtkIdBuilderOptions.add_arguments(parser)
    KgtkReader.add_debug_arguments(parser)
    KgtkReaderOptions.add_arguments(parser, mode_options=True)
    KgtkValueOptions.add_arguments(parser)

    args: Namespace = parser.parse_args()

    error_file: typing.TextIO = sys.stdout if args.errors_to_stdout else sys.stderr

    # Build the option structures.                                                                                                                          
    idbuilder_options: KgtkIdBuilderOptions = KgtkIdBuilderOptions.from_args(args)    
    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_args(args)
    value_options: KgtkValueOptions = KgtkValueOptions.from_args(args)

   # Show the final option structures for debugging and documentation.                                                                                             
    if args.show_options:
        # TODO: show ifempty-specific options.
        print("input: %s" % str(args.input_file_path), file=error_file, flush=True)
        print("--column %s" % args.column_name, file=error_file, flush=True)
        print("--prefix %s" % args.prefix, file=error_file, flush=True)
        print("--overwrite %s" % str(args.overwrite_column), file=error_file, flush=True)
        print("--validate %s" % str(args.validate), file=error_file, flush=True)
        print("--escape-pipes %s" % str(args.escape_pipes), file=error_file, flush=True)
        print("--quantities-include-numbers %s" % str(args.quantities_include_numbers), file=error_file, flush=True)
        print("--general-strings %s" % str(args.general_strings), file=error_file, flush=True)
        print("--remove-prefixed-columns %s" % str(args.remove_prefixed_columns), file=error_file, flush=True)
        print("--ignore-unselected-types %s" % str(args.ignore_unselected_types), file=error_file, flush=True)
        print("--retain-unselected-types %s" % str(args.retain_unselected_types), file=error_file, flush=True)
        print("--quiets %s" % str(args.quiet), file=error_file, flush=True)
        if args.type_names is not None:
            print("--types %s" % " ".join(args.type_names), file=error_file, flush=True)
        if args.without_fields is not None:
            print("--without %s" % " ".join(args.without_fields), file=error_file, flush=True)
        print("--output-file=%s" % str(args.output_file_path), file=error_file, flush=True)
        if args.reject_file_path is not None:
            print("--reject-file=%s" % str(args.reject_file_path), file=error_file, flush=True)
        print("--build-id=%s" % str(args.build_id), file=error_file, flush=True)
        idbuilder_options.show(out=error_file)
        reader_options.show(out=error_file)
        value_options.show(out=error_file)

    without_fields: typing.List[str] = args.without_fields if args.without_fields is not None else list()

    ex: KgtkImplode = KgtkImplode(
        input_file_path=args.input_file_path,
        column_name=args.column_name,
        prefix=args.prefix,
        type_names=args.type_names,
        without_fields=without_fields,
        overwrite_column=args.overwrite_column,
        validate=args.validate,
        escape_pipes=args.escape_pipes,
        quantities_include_numbers=args.quantities_include_numbers,
        general_strings=args.general_strings,
        remove_prefixed_columns=args.remove_prefixed_columns,
        ignore_unselected_types=args.ignore_unselected_types,
        retain_unselected_types=args.retain_unselected_types,
        output_file_path=args.output_file_path,
        reject_file_path=args.reject_file_path,
        quiet=args.quiet,
        build_id=args.build_id,
        idbuilder_options=idbuilder_options,
        reader_options=reader_options,
        value_options=value_options,
        error_file=error_file,
        verbose=args.verbose,
        very_verbose=args.very_verbose)

    ex.process()

    
if __name__ == "__main__":
    main()
