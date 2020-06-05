"""Read a KGTK node or edge file in TSV format.

Normally, results are obtained as rows of string values obtained by iteration
on the KgtkReader object.  Alternative iterators are available to return the results
as:

 * concise_rows:                   lists of strings with empty fields converted to None
 * kgtk_values:                    lists of KgtkValue objects
 * concise_kgtk_values:            lists of KgtkValue objects with empty fields converted to None
 * dicts:                          dicts of strings
 * dicts(concise=True):            dicts of strings with empty fields omitted
 * kgtk_value_dicts:               dicts of KgtkValue objects
 * kgtk_value_dicts(concise=True): dicts of KgtkValue objects with empty fields omitted

TODO: Add support for alternative envelope formats, such as JSON.

"""

from argparse import ArgumentParser, _ArgumentGroup, Namespace, SUPPRESS
import attr
import bz2
from enum import Enum
import gzip
import lz4 # type: ignore
import lzma
from multiprocessing import Process, Queue
from pathlib import Path
import sys
import typing

from kgtk.kgtkformat import KgtkFormat
from kgtk.io.kgtkbase import KgtkBase
from kgtk.utils.argparsehelpers import optional_bool
from kgtk.utils.closableiter import ClosableIter, ClosableIterTextIOWrapper
from kgtk.utils.enumnameaction import EnumNameAction
from kgtk.utils.gzipprocess import GunzipProcess
from kgtk.utils.validationaction import ValidationAction
from kgtk.value.kgtkvalue import KgtkValue
from kgtk.value.kgtkvalueoptions import KgtkValueOptions, DEFAULT_KGTK_VALUE_OPTIONS

class KgtkReaderMode(Enum):
    """
    There are four file reading modes:
    """
    NONE = 0 # Enforce neither edge nore node file required columns
    EDGE = 1 # Enforce edge file required columns
    NODE = 2 # Enforce node file require columns
    AUTO = 3 # Automatically decide whether to enforce edge or node file required columns

@attr.s(slots=True, frozen=True)
class KgtkReaderOptions():
    ERROR_LIMIT_DEFAULT: int = 1000
    GZIP_QUEUE_SIZE_DEFAULT: int = GunzipProcess.GZIP_QUEUE_SIZE_DEFAULT

    mode: KgtkReaderMode = attr.ib(validator=attr.validators.instance_of(KgtkReaderMode), default=KgtkReaderMode.AUTO)

    # The column separator is normally tab.
    column_separator: str = attr.ib(validator=attr.validators.instance_of(str), default=KgtkFormat.COLUMN_SEPARATOR)

    # supply a missing header record or override an existing header record.
    force_column_names: typing.Optional[typing.List[str]] = attr.ib(validator=attr.validators.optional(attr.validators.deep_iterable(member_validator=attr.validators.instance_of(str),
                                                                                                                                     iterable_validator=attr.validators.instance_of(list))),
                                                                    default=None)
    skip_header_record: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    # Data record sampling, pre-validation.
    #
    # 1) Optionally read and skip a specific number of initial records, or record_limit - tail_count,
    #    whichever is greater.
    # 2) Optionally pass through every nth record relative to the number of records read.
    # 3) Optionally limit the total number of records read.
    initial_skip_count: int = attr.ib(validator=attr.validators.instance_of(int), default=0)
    every_nth_record: int = attr.ib(validator=attr.validators.instance_of(int), default=1)
    record_limit: typing.Optional[int] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)), default=None)
    tail_count: typing.Optional[int] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)), default=None)

    # How do we handle errors?
    error_limit: int = attr.ib(validator=attr.validators.instance_of(int), default=ERROR_LIMIT_DEFAULT) # >0 ==> limit error reports

    # Top-level validation controls:
    repair_and_validate_lines: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    repair_and_validate_values: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    # Ignore empty lines, comments, and all whitespace lines, etc.?
    empty_line_action: ValidationAction = attr.ib(validator=attr.validators.instance_of(ValidationAction), default=ValidationAction.EXCLUDE)
    comment_line_action: ValidationAction = attr.ib(validator=attr.validators.instance_of(ValidationAction), default=ValidationAction.EXCLUDE)
    whitespace_line_action: ValidationAction = attr.ib(validator=attr.validators.instance_of(ValidationAction), default=ValidationAction.EXCLUDE)

    # Ignore records with empty values in certain fields:
    blank_required_field_line_action: ValidationAction = attr.ib(validator=attr.validators.instance_of(ValidationAction), default=ValidationAction.EXCLUDE)
    
    # Ignore records with too many or too few fields?
    short_line_action: ValidationAction = attr.ib(validator=attr.validators.instance_of(ValidationAction), default=ValidationAction.COMPLAIN)
    long_line_action: ValidationAction = attr.ib(validator=attr.validators.instance_of(ValidationAction), default=ValidationAction.COMPLAIN)

    # How should header errors be processed?
    header_error_action: ValidationAction = attr.ib(validator=attr.validators.instance_of(ValidationAction), default=ValidationAction.EXIT)
    unsafe_column_name_action: ValidationAction = attr.ib(validator=attr.validators.instance_of(ValidationAction), default=ValidationAction.REPORT)

    # Validate data cell values?
    invalid_value_action: ValidationAction = attr.ib(validator=attr.validators.instance_of(ValidationAction), default=ValidationAction.COMPLAIN)
    prohibited_list_action: ValidationAction = attr.ib(validator=attr.validators.instance_of(ValidationAction), default=ValidationAction.COMPLAIN)

    # Repair records with too many or too few fields?
    fill_short_lines: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    truncate_long_lines: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    # Other implementation options?
    compression_type: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None) # TODO: use an Enum
    gzip_in_parallel: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    gzip_queue_size: int = attr.ib(validator=attr.validators.instance_of(int), default=GZIP_QUEUE_SIZE_DEFAULT)

    @classmethod
    def add_arguments(cls,
                      parser: ArgumentParser,
                      mode_options: bool = False,
                      validate_by_default: bool = False,
                      expert: bool = False,
                      defaults: bool = True,
                      who: str = "",
    ):

        # This helper function makes it easy to suppress options from
        # The help message.  The options are still there, and initialize
        # what they need to initialize.
        def h(msg: str)->str:
            if expert:
                return msg
            else:
                return SUPPRESS

        # This helper function decices whether or not to include defaults
        # in argument declarations. If we plan to make arguments with
        # prefixes and fallbacks, the fallbacks (the ones without prefixes)
        # should get default values, while the prefixed arguments should
        # not get defaults.
        #
        # Note: In obscure circumstances (EnumNameAction, I'm looking at you),
        # explicitly setting "default=None" may fail, whereas omitting the
        # "default=" phrase succeeds.
        #
        # TODO: continue researching these issues.
        def d(default: typing.Any)->typing.Mapping[str, typing.Any]:
            if defaults:
                return {"default": default}
            else:
                return { }

        prefix1: str = "--" if len(who) == 0 else "--" + who + "-"
        prefix2: str = "" if len(who) == 0 else who + "_"
        prefix3: str = "" if len(who) == 0 else who + ": "
        prefix4: str = "" if len(who) == 0 else who + " file "

        fgroup: _ArgumentGroup = parser.add_argument_group(h(prefix3 + "File options"),
                                                           h("Options affecting " + prefix4 + "processing."))
        fgroup.add_argument(prefix1 + "column-separator",
                            dest=prefix2 + "column_separator",
                            help=h(prefix3 + "Column separator (default=<TAB>)."), # TODO: provide the default with escapes, e.g. \t
                            type=str, **d(default=KgtkFormat.COLUMN_SEPARATOR))

        # TODO: use an Enum or add choices.
        fgroup.add_argument(prefix1 + "compression-type",
                            dest=prefix2 + "compression_type",
                            help=h(prefix3 + "Specify the compression type (default=%(default)s)."))

        fgroup.add_argument(prefix1 + "error-limit",
                            dest=prefix2 + "error_limit",
                            help=h(prefix3 + "The maximum number of errors to report before failing (default=%(default)s)"),
                            type=int, **d(default=cls.ERROR_LIMIT_DEFAULT))

        fgroup.add_argument(prefix1 + "gzip-in-parallel",
                            dest=prefix2 + "gzip_in_parallel",
                            metavar="optional True|False",
                            help=h(prefix3 + "Execute gzip in parallel (default=%(default)s)."),
                            type=optional_bool, nargs='?', const=True, **d(default=False))

        fgroup.add_argument(prefix1 + "gzip-queue-size",
                            dest=prefix2 + "gzip_queue_size",
                            help=h(prefix3 + "Queue size for parallel gzip (default=%(default)s)."),
                            type=int, **d(default=cls.GZIP_QUEUE_SIZE_DEFAULT))

        if mode_options:
            fgroup.add_argument(prefix1 + "mode",
                                dest=prefix2 + "mode",
                                help=h(prefix3 + "Determine the KGTK file mode (default=%(default)s)."),
                                type=KgtkReaderMode, action=EnumNameAction, **d(KgtkReaderMode.AUTO))
            
        hgroup: _ArgumentGroup = parser.add_argument_group(h(prefix3 + "Header parsing"),
                                                           h("Options affecting " + prefix4 + "header parsing."))

        hgroup.add_argument(prefix1 + "force-column-names",
                            dest=prefix2 + "force_column_names",
                            help=h(prefix3 + "Force the column names (default=None)."),
                            nargs='+')

        hgroup.add_argument(prefix1 + "header-error-action",
                            dest=prefix2 + "header_error_action",
                            help=h(prefix3 + "The action to take when a header error is detected.  Only ERROR or EXIT are supported (default=%(default)s)."),
                            type=ValidationAction, action=EnumNameAction, **d(default=ValidationAction.EXIT))

        hgroup.add_argument(prefix1 + "skip-header-record",
                            dest=prefix2 + "skip_header_record",
                            metavar="optional True|False",
                            help=h(prefix3 + "Skip the first record when forcing column names (default=%(default)s)."),
                            type=optional_bool, nargs='?', const=True, **d(default=False))

        hgroup.add_argument(prefix1 + "unsafe-column-name-action",
                            dest=prefix2 + "unsafe_column_name_action",
                            help=h(prefix3 + "The action to take when a column name is unsafe (default=%(default)s)."),
                            type=ValidationAction, action=EnumNameAction, **d(default=ValidationAction.REPORT))

        sgroup: _ArgumentGroup = parser.add_argument_group(h(prefix3 + "Pre-validation sampling"),
                                                           h("Options affecting " + prefix4 + "pre-validation data line sampling."))
        
        sgroup.add_argument(prefix1 + "initial-skip-count",
                            dest=prefix2 + "initial_skip_count",
                            help=h(prefix3 + "The number of data records to skip initially (default=do not skip)."),
                            type=int, **d(default=0))

        sgroup.add_argument(prefix1 + "every-nth-record",
                            dest=prefix2 + "every_nth_record",
                            help=h(prefix3 + "Pass every nth record (default=pass all records)."),
                            type=int, **d(default=1))

        sgroup.add_argument(prefix1 + "record-limit",
                            dest=prefix2 + "record_limit",
                            help=h(prefix3 + "Limit the number of records read (default=no limit)."),
                            type=int, **d(default=None))

        sgroup.add_argument(prefix1 + "tail-count",
                            dest=prefix2 + "tail_count",
                            help=h(prefix3 + "Pass this number of records (default=no tail processing)."),
                            type=int, **d(default=None))

        lgroup: _ArgumentGroup = parser.add_argument_group(h(prefix3 + "Line parsing"),
                                                           h("Options affecting " + prefix4 + "data line parsing."))

        lgroup.add_argument(prefix1 + "repair-and-validate-lines",
                            dest=prefix2 + "repair_and_validate_lines",
                            metavar="optional True|False",
                            help=h(prefix3 + "Repair and validate lines (default=%(default)s)."),
                            type=optional_bool, nargs='?', const=True, **d(default=validate_by_default))

        lgroup.add_argument(prefix1 + "repair-and-validate-values",
                            dest=prefix2 + "repair_and_validate_values",
                            metavar="optional True|False",
                            help=h(prefix3 + "Repair and validate values (default=%(default)s)."),
                            type=optional_bool, nargs='?', const=True, **d(default=validate_by_default))

        lgroup.add_argument(prefix1 + "blank-required-field-line-action",
                            dest=prefix2 + "blank_required_field_line_action",
                            help=h(prefix3 + "The action to take when a line with a blank node1, node2, or id field (per mode) is detected (default=%(default)s)."),
                            type=ValidationAction, action=EnumNameAction, **d(default=ValidationAction.EXCLUDE))
                                  
        lgroup.add_argument(prefix1 + "comment-line-action",
                            dest=prefix2 + "comment_line_action",
                            help=h(prefix3 + "The action to take when a comment line is detected (default=%(default)s)."),
                            type=ValidationAction, action=EnumNameAction, **d(default=ValidationAction.EXCLUDE))

        lgroup.add_argument(prefix1 + "empty-line-action",
                            dest=prefix2 + "empty_line_action",
                            help=h(prefix3 + "The action to take when an empty line is detected (default=%(default)s)."),
                            type=ValidationAction, action=EnumNameAction, **d(default=ValidationAction.EXCLUDE))

        lgroup.add_argument(prefix1 + "fill-short-lines",
                            dest=prefix2 + "fill_short_lines",
                            metavar="optional True|False",
                            help=h(prefix3 + "Fill missing trailing columns in short lines with empty values (default=%(default)s)."),
                            type=optional_bool, nargs='?', const=True, **d(default=False))

        lgroup.add_argument(prefix1 + "invalid-value-action",
                            dest=prefix2 + "invalid_value_action",
                            help=h(prefix3 + "The action to take when a data cell value is invalid (default=%(default)s)."),
                            type=ValidationAction, action=EnumNameAction, **d(default=ValidationAction.COMPLAIN))

        lgroup.add_argument(prefix1 + "long-line-action",
                            dest=prefix2 + "long_line_action",
                            help=h(prefix3 + "The action to take when a long line is detected (default=%(default)s)."),
                            type=ValidationAction, action=EnumNameAction, **d(default=ValidationAction.COMPLAIN))

        lgroup.add_argument(prefix1 + "prohibited-list-action",
                            dest=prefix2 + "prohibited list_action",
                            help=h(prefix3 + "The action to take when a data cell contains a prohibited list (default=%(default)s)."),
                            type=ValidationAction, action=EnumNameAction, **d(default=ValidationAction.COMPLAIN))

        lgroup.add_argument(prefix1 + "short-line-action",
                            dest=prefix2 + "short_line_action",
                            help=h(prefix3 + "The action to take when a short line is detected (default=%(default)s)."),
                            type=ValidationAction, action=EnumNameAction, **d(default=ValidationAction.COMPLAIN))

        lgroup.add_argument(prefix1 + "truncate-long-lines",
                            dest=prefix2 + "truncate_long_lines",
                            help=h(prefix3 + "Remove excess trailing columns in long lines (default=%(default)s)."),
                            type=optional_bool, nargs='?', const=True, **d(default=False))

        lgroup.add_argument(prefix1 + "whitespace-line-action",
                            dest=prefix2 + "whitespace_line_action",
                            help=h(prefix3 + "The action to take when a whitespace line is detected (default=%(default)s)."),
                            type=ValidationAction, action=EnumNameAction, **d(default=ValidationAction.EXCLUDE))
    
    @classmethod
    # Build the value parsing option structure.
    def from_dict(cls,
                  d: dict,
                  who: str = "",
                  mode: typing.Optional[KgtkReaderMode] = None,
                  fallback: bool = False,
    )->'KgtkReaderOptions':
        prefix: str = ""   # The destination name prefix.
        if len(who) > 0:
            prefix = who + "_"

        # TODO: Figure out how to type check this method.
        def lookup(name: str, default):
            prefixed_name = prefix + name
            if prefixed_name in d and d[prefixed_name] is not None:
                return d[prefixed_name]
            elif fallback and name in d and d[name] is not None:
                return d[name]
            else:
                return default
            
        reader_mode: KgtkReaderMode
        if mode is not None:
            reader_mode = mode
        else:
            reader_mode = lookup("mode", KgtkReaderMode.AUTO)

        return cls(
            blank_required_field_line_action=lookup("blank_required_field_line_action", ValidationAction.EXCLUDE),
            column_separator=lookup("column_separator", KgtkFormat.COLUMN_SEPARATOR),
            comment_line_action=lookup("comment_line_action", ValidationAction.EXCLUDE),
            compression_type=lookup("compression_type", None),
            empty_line_action=lookup("empty_line_action", ValidationAction.EXCLUDE),
            error_limit=lookup("error_limit", cls.ERROR_LIMIT_DEFAULT),
            every_nth_record=lookup("every_nth_record", 1),
            fill_short_lines=lookup("fill_short_lines", False),
            force_column_names=lookup("force_column_names", None),
            gzip_in_parallel=lookup("gzip_in_parallel", False),
            gzip_queue_size=lookup("gzip_queue_size", KgtkReaderOptions.GZIP_QUEUE_SIZE_DEFAULT),
            header_error_action=lookup("header_error_action", ValidationAction.EXCLUDE),
            initial_skip_count=lookup("initial_skip_count", 0),
            invalid_value_action=lookup("invalid_value_action", ValidationAction.REPORT),
            long_line_action=lookup("long_line_action", ValidationAction.EXCLUDE),
            mode=reader_mode,
            prohibited_list_action=lookup("prohibited_list_action", ValidationAction.REPORT),
            record_limit=lookup("record_limit", None),
            repair_and_validate_lines=lookup("repair_and_validate_lines", False),
            repair_and_validate_values=lookup("repair_and_validate_values", False),
            short_line_action=lookup("short_line_action", ValidationAction.EXCLUDE),
            skip_header_record=lookup("skip_header_recordb", False),
            tail_count=lookup("tail_count", None),
            truncate_long_lines=lookup("truncate_long_lines", False),
            unsafe_column_name_action=lookup("unsafe_column_name_action", ValidationAction.REPORT),
            whitespace_line_action=lookup("whitespace_line_action", ValidationAction.EXCLUDE),
        )

    # Build the value parsing option structure.
    @classmethod
    def from_args(cls,
                  args: Namespace,
                  who: str = "",
                  mode: typing.Optional[KgtkReaderMode] = None,
                  fallback: bool = False,
    )->'KgtkReaderOptions':
        return cls.from_dict(vars(args), who=who, mode=mode, fallback=fallback)

    def show(self, who: str="", out: typing.TextIO=sys.stderr):
        prefix: str = "--" if len(who) == 0 else "--" + who + "-"
        print("%smode=%s" % (prefix, self.mode.name), file=out)
        print("%scolumn-separator=%s" % (prefix, repr(self.column_separator)), file=out)
        if self.force_column_names is not None:
            print("%sforce-column-names=%s" % (prefix, " ".join(self.force_column_names)), file=out)
        print("%sskip-header-record=%s" % (prefix, str(self.skip_header_record)), file=out)
        print("%serror-limit=%s" % (prefix, str(self.error_limit)), file=out)
        print("%srepair-and-validate-lines=%s" % (prefix, str(self.repair_and_validate_lines)), file=out)
        print("%srepair-and-validate-values=%s" % (prefix, str(self.repair_and_validate_values)), file=out)
        print("%sempty-line-action=%s" % (prefix, self.empty_line_action.name), file=out)
        print("%scomment-line-action=%s" % (prefix, self.comment_line_action.name), file=out)
        print("%swhitespace-line-action=%s" % (prefix, self.whitespace_line_action.name), file=out)
        print("%sblank-required-field-line-action=%s" % (prefix, self.blank_required_field_line_action.name), file=out)
        print("%sshort-line-action=%s" % (prefix, self.short_line_action.name), file=out)
        print("%slong-line-action=%s" % (prefix, self.long_line_action.name), file=out)
        print("%sheader-error-action=%s" % (prefix, self.header_error_action.name), file=out)
        print("%sunsafe-column-name-action=%s" % (prefix, self.unsafe_column_name_action.name), file=out)
        print("%sinvalid-value-action=%s" % (prefix, self.invalid_value_action.name), file=out)
        print("%sinitial-skip-count=%s" % (prefix, str(self.initial_skip_count)), file=out)
        print("%severy-nth-record=%s" % (prefix, str(self.every_nth_record)), file=out)
        if self.record_limit is not None:
            print("%srecord-limit=%s" % (prefix, str(self.record_limit)), file=out)
        if self.tail_count is not None:
            print("%stail-count=%s" % (prefix, str(self.tail_count)), file=out)
        print("%sinitial-skip-count=%s" % (prefix, str(self.initial_skip_count)), file=out)
        print("%sprohibited-list-action=%s" % (prefix, self.prohibited_list_action.name), file=out)
        print("%sfill-short-lines=%s" % (prefix, str(self.fill_short_lines)), file=out)
        print("%struncate-long-lines=%s" % (prefix, str(self.truncate_long_lines)), file=out)
        if self.compression_type is not None:
            print("%scompression-type=%s" % (prefix, str(self.compression_type)), file=out)
        print("%sgzip-in-parallel=%s" % (prefix, str(self.gzip_in_parallel)), file=out)
        print("%sgzip-queue-size=%s" % (prefix, str(self.gzip_queue_size)), file=out)
              
        

DEFAULT_KGTK_READER_OPTIONS: KgtkReaderOptions = KgtkReaderOptions()


@attr.s(slots=True, frozen=False)
class KgtkReader(KgtkBase, ClosableIter[typing.List[str]]):
    file_path: typing.Optional[Path] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Path)))
    source: ClosableIter[str] = attr.ib() # Todo: validate

    # TODO: Fix this validator:
    # options: KgtkReaderOptions = attr.ib(validator=attr.validators.instance_of(KgtkReaderOptions))
    options: KgtkReaderOptions = attr.ib()

    value_options: KgtkValueOptions = attr.ib(validator=attr.validators.instance_of(KgtkValueOptions))

    column_names: typing.List[str] = attr.ib(validator=attr.validators.deep_iterable(member_validator=attr.validators.instance_of(str),
                                                                                     iterable_validator=attr.validators.instance_of(list)))
    # For convenience, the count of columns. This is the same as len(column_names).
    column_count: int = attr.ib(validator=attr.validators.instance_of(int))
    
    column_name_map: typing.Mapping[str, int] = attr.ib(validator=attr.validators.deep_mapping(key_validator=attr.validators.instance_of(str),
                                                                                               value_validator=attr.validators.instance_of(int)))

    # The actual mode used.
    #
    # TODO: fix the validator.
    # mode: KgtkReaderMode = attr.ib(validator=attr.validators.instance_of(KgtkReaderMode), default=KgtkReaderMode.NONE)
    mode: KgtkReaderMode = attr.ib(default=KgtkReaderMode.NONE)

    # The index of the mandatory/aliased columns.  -1 means missing:
    node1_column_idx: int = attr.ib(validator=attr.validators.instance_of(int), default=-1) # edge file
    label_column_idx: int = attr.ib(validator=attr.validators.instance_of(int), default=-1) # edge file
    node2_column_idx: int = attr.ib(validator=attr.validators.instance_of(int), default=-1) # edge file
    id_column_idx: int = attr.ib(validator=attr.validators.instance_of(int), default=-1) # node file

    data_lines_read: int = attr.ib(validator=attr.validators.instance_of(int), default=0)
    data_lines_skipped: int = attr.ib(validator=attr.validators.instance_of(int), default=0)
    data_lines_passed: int = attr.ib(validator=attr.validators.instance_of(int), default=0)
    data_lines_ignored: int = attr.ib(validator=attr.validators.instance_of(int), default=0)
    data_errors_reported: int = attr.ib(validator=attr.validators.instance_of(int), default=0)

    # Is this an edge file or a node file?
    is_edge_file: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    is_node_file: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    # Feedback and error output:
    error_file: typing.TextIO = attr.ib(default=sys.stderr)
    verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    very_verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    @classmethod
    def _default_options(
            cls,
            options: typing.Optional[KgtkReaderOptions] = None,
            value_options: typing.Optional[KgtkValueOptions] = None,
    )->typing.Tuple[KgtkReaderOptions, KgtkValueOptions]:
        # Supply the default reader and value options:
        if options is None:
            options = DEFAULT_KGTK_READER_OPTIONS
        if value_options is None:
            value_options = DEFAULT_KGTK_VALUE_OPTIONS

        return (options, value_options)

    @classmethod
    def open(cls,
             file_path: typing.Optional[Path],
             who: str = "input",
             error_file: typing.TextIO = sys.stderr,
             mode: typing.Optional[KgtkReaderMode] = None,
             options: typing.Optional[KgtkReaderOptions] = None,
             value_options: typing.Optional[KgtkValueOptions] = None,
             verbose: bool = False,
             very_verbose: bool = False)->"KgtkReader":
        """
        Opens a KGTK file, which may be an edge file or a node file.  The appropriate reader is returned.
        """

        # Supply the default reader and value options:
        (options, value_options) = cls._default_options(options, value_options)

        source: ClosableIter[str] = cls._openfile(file_path, options=options, error_file=error_file, verbose=verbose)

        # Read the kgtk file header and split it into column names.  We get the
        # header back, too, for use in debugging and error messages.
        header: str
        column_names: typing.List[str]
        (header, column_names) = cls._build_column_names(source, options, error_file=error_file, verbose=verbose)
        # Check for unsafe column names.
        cls.check_column_names(column_names,
                               header_line=header,
                               who=who,
                               error_action=options.unsafe_column_name_action,
                               error_file=error_file)

        # Build a map from column name to column index.
        column_name_map: typing.Mapping[str, int] = cls.build_column_name_map(column_names,
                                                                              header_line=header,
                                                                              who=who,
                                                                              error_action=options.header_error_action,
                                                                              error_file=error_file)

        # Should we automatically determine if this is an edge file or a node file?
        if mode is None:
            mode = options.mode
        is_edge_file: bool = False
        is_node_file: bool = False
        if mode is KgtkReaderMode.AUTO:
            # If we have a node1 (or alias) column, then this must be an edge file. Otherwise, assume it is a node file.
            node1_idx: int = cls.get_column_idx(cls.NODE1_COLUMN_NAMES,
                                                column_name_map,
                                                header_line=header,
                                                who=who,
                                                error_action=options.header_error_action,
                                                error_file=error_file,
                                                is_optional=True)
            if node1_idx >= 0:
                is_edge_file = True
                is_node_file = False
                if verbose:
                    print("%s column found, this is a KGTK edge file" % column_names[node1_idx], file=error_file, flush=True)
            else:
                is_edge_file = False
                is_node_file = True
                if verbose:
                    print("node1 column not found, assuming this is a KGTK node file", file=error_file, flush=True)

        elif mode is KgtkReaderMode.EDGE:
            is_edge_file = True
        elif mode is KgtkReaderMode.NODE:
            is_node_file = True
        elif mode is KgtkReaderMode.NONE:
            pass

        # Get the indices of the special columns.
        node1_column_idx: int
        label_column_idx: int
        node2_column_idx: int
        id_column_idx: int
        (node1_column_idx,
         label_column_idx,
         node2_column_idx,
         id_column_idx) = cls.get_special_columns(column_name_map,
                                                  header_line=header,
                                                  who=who,
                                                  error_action=options.header_error_action,
                                                  error_file=error_file,
                                                  is_edge_file=is_edge_file,
                                                  is_node_file=is_node_file)
        
        if verbose:
            print("KgtkReader: Special columns: node1=%d label=%d node2=%d id=%d" % (node1_column_idx,
                                                                                     label_column_idx,
                                                                                     node2_column_idx,
                                                                                     id_column_idx), file=error_file, flush=True)
        if is_edge_file:
            # We'll instantiate an EdgeReader, which is a subclass of KgtkReader.
            # The EdgeReader import is deferred to avoid circular imports.
            from kgtk.io.edgereader import EdgeReader
            
            if verbose:
                print("KgtkReader: Reading an edge file.", file=error_file, flush=True)

            cls = EdgeReader
        
        elif is_node_file:
            # We'll instantiate an NodeReader, which is a subclass of KgtkReader.
            # The NodeReader import is deferred to avoid circular imports.
            from kgtk.io.nodereader import NodeReader
            
            if verbose:
                print("KgtkReader: Reading an node file.", file=error_file, flush=True)

            cls = NodeReader

        return cls(file_path=file_path,
                   source=source,
                   column_names=column_names,
                   column_name_map=column_name_map,
                   column_count=len(column_names),
                   mode=mode,
                   node1_column_idx=node1_column_idx,
                   label_column_idx=label_column_idx,
                   node2_column_idx=node2_column_idx,
                   id_column_idx=id_column_idx,
                   error_file=error_file,
                   options=options,
                   value_options=value_options,
                   is_edge_file=is_edge_file,
                   is_node_file=is_node_file,
                   verbose=verbose,
                   very_verbose=very_verbose,
        )

    @classmethod
    def _open_compressed_file(cls,
                              compression_type: str,
                              file_name: str,
                              file_or_path: typing.Union[Path, typing.TextIO],
                              who: str,
                              error_file: typing.TextIO,
                              verbose: bool)->typing.TextIO:
        
        # TODO: find a better way to coerce typing.IO[Any] to typing.TextIO
        if compression_type in [".gz", "gz"]:
            if verbose:
                print("%s: reading gzip %s" % (who, file_name), file=error_file, flush=True)
            return gzip.open(file_or_path, mode="rt") # type: ignore
        
        elif compression_type in [".bz2", "bz2"]:
            if verbose:
                print("%s: reading bz2 %s" % (who, file_name), file=error_file, flush=True)
            return bz2.open(file_or_path, mode="rt") # type: ignore
        
        elif compression_type in [".xz", "xz"]:
            if verbose:
                print("%s: reading lzma %s" % (who, file_name), file=error_file, flush=True)
            return lzma.open(file_or_path, mode="rt") # type: ignore
        
        elif compression_type in [".lz4", "lz4"]:
            if verbose:
                print("%s: reading lz4 %s" % (who, file_name), file=error_file, flush=True)
            return lz4.frame.open(file_or_path, mode="rt") # type: ignore
        else:
            # TODO: throw a better exception.
                raise ValueError("%s: Unexpected compression_type '%s'" % (who, compression_type))

    @classmethod
    def _openfile(cls,
                  file_path: typing.Optional[Path],
                  options: KgtkReaderOptions, 
                  error_file: typing.TextIO,
                  verbose: bool)->ClosableIter[str]:
        who: str = cls.__name__
        if file_path is None or str(file_path) == "-":
            if options.compression_type is not None and len(options.compression_type) > 0:
                return ClosableIterTextIOWrapper(cls._open_compressed_file(options.compression_type, "-", sys.stdin, who, error_file, verbose))
            else:
                if verbose:
                    print("%s: reading stdin" % who, file=error_file, flush=True)
                return ClosableIterTextIOWrapper(sys.stdin)

        if verbose:
            print("%s: File_path.suffix: %s" % (who, file_path.suffix), file=error_file, flush=True)

        gzip_file: typing.TextIO
        if options.compression_type is not None and len(options.compression_type) > 0:
            gzip_file = cls._open_compressed_file(options.compression_type, str(file_path), file_path, who, error_file, verbose)
        elif file_path.suffix in [".bz2", ".gz", ".lz4", ".xz"]:
            gzip_file = cls._open_compressed_file(file_path.suffix, str(file_path), file_path, who, error_file, verbose)
        else:
            if verbose:
                print("%s: reading file %s" % (who, str(file_path)))
            return ClosableIterTextIOWrapper(open(file_path, "r"))

        if options.gzip_in_parallel:
            gzip_thread: GunzipProcess = GunzipProcess(gzip_file, Queue(options.gzip_queue_size))
            gzip_thread.start()
            return gzip_thread
        else:
            return ClosableIterTextIOWrapper(gzip_file)
            

    @classmethod
    def _build_column_names(cls,
                            source: ClosableIter[str],
                            options: KgtkReaderOptions,
                            error_file: typing.TextIO,
                            verbose: bool = False,
    )->typing.Tuple[str, typing.List[str]]:
        """
        Read the kgtk file header and split it into column names.
        """
        column_names: typing.List[str]
        if options.force_column_names is None:
            # Read the column names from the first line, stripping end-of-line characters.
            #
            # TODO: if the read fails, throw a more useful exception with the line number.
            try:
                header: str = next(source).rstrip("\r\n")
            except StopIteration:
                raise ValueError("No header line in file")
            if verbose:
                print("header: %s" % header, file=error_file, flush=True)

            # Split the first line into column names.
            return header, header.split(options.column_separator)
        else:
            # Skip the first record to override the column names in the file.
            # Do not skip the first record if the file does not hae a header record.
            if options.skip_header_record:
                try:
                    next(source)
                except StopIteration:
                    raise ValueError("No header line to skip")

            # Use the forced column names.
            return options.column_separator.join(options.force_column_names), options.force_column_names

    def close(self):
        self.source.close()

    def exclude_line(self, action: ValidationAction, msg: str, line: str)->bool:
        """
        Take a validation action.  Returns True if the line should be excluded.
        """
        result: bool
        if action == ValidationAction.PASS:
            return False # Silently pass the line through
        elif action == ValidationAction.REPORT:
            result= False # Report the issue then pass the line.
        elif action == ValidationAction.EXCLUDE:
            return True # Silently exclude the line
        elif action == ValidationAction.COMPLAIN:
            result = True # Report the issue then exclude the line.
        elif action == ValidationAction.ERROR:
            # Immediately raise an exception.
            raise ValueError("In input data line %d, %s: %s" % (self.data_lines_read, msg, line))
        elif action == ValidationAction.EXIT:
            print("Data line %d:\n%s\n%s" % (self.data_lines_read, line, msg), file=self.error_file, flush=True)
            sys.exit(1)
            
        # print("In input data line %d, %s: %s" % (self.data_lines_read, msg, line), file=self.error_file, flush=True)
        print("Data line %d:\n%s\n%s" % (self.data_lines_read, line, msg), file=self.error_file, flush=True)
        self.data_errors_reported += 1
        if self.options.error_limit > 0 and self.data_errors_reported >= self.options.error_limit:
            raise ValueError("Too many data errors, exiting.")
        return result

    # Get the next edge values as a list of strings.
    def nextrow(self)-> typing.List[str]:
        row: typing.List[str]

        repair_and_validate_lines: bool = self.options.repair_and_validate_lines
        repair_and_validate_values: bool = self.options.repair_and_validate_values

        # Compute the initial skip count
        skip_count: int = self.options.initial_skip_count
        if self.options.record_limit is not None and self.options.tail_count is not None:
            # Compute the tail count.
            tail_skip_count: int = self.options.record_limit - self.options.tail_count
            if tail_skip_count > skip_count:
                skip_count = tail_skip_count # Take the larger skip count.

        # This loop accomodates lines that are ignored.
        while (True):
            # Has a record limit been specified and have we reached it?
            if self.options.record_limit is not None:
                if self.data_lines_read >= self.options.record_limit:
                    # Close the source and stop the iteration.
                    self.source.close() # Do we need to guard against repeating this call?
                    raise StopIteration

            # Read a line from the source
            line: str
            try:
                
                line = next(self.source) # Will throw StopIteration
            except StopIteration as e:
                # Close the input file!
                #
                # TODO: implement a close() routine and/or whatever it takes to support "with".
                self.source.close() # Do we need to guard against repeating this call?
                raise e

            # Count the data line read.
            self.data_lines_read += 1

            # Data sampling:
            if self.data_lines_read <= skip_count:
                self.data_lines_skipped += 1
                continue
            if self.options.every_nth_record > 1:
                if self.data_lines_read % self.options.every_nth_record != 0:
                    self.data_lines_skipped += 1
                    continue

            # Strip the end-of-line characters:
            line = line.rstrip("\r\n")

            if repair_and_validate_lines:
                # TODO: Use a sepearate option to control this.
                if self.very_verbose:
                    print("'%s'" % line, file=self.error_file, flush=True)
                
                # Ignore empty lines.
                if self.options.empty_line_action != ValidationAction.PASS and len(line) == 0:
                    if self.exclude_line(self.options.empty_line_action, "saw an empty line", line):
                        continue

                # Ignore comment lines:
                if self.options.comment_line_action != ValidationAction.PASS  and line[0] == self.COMMENT_INDICATOR:
                    if self.exclude_line(self.options.comment_line_action, "saw a comment line", line):
                        continue

                # Ignore whitespace lines
                if self.options.whitespace_line_action != ValidationAction.PASS and line.isspace():
                    if self.exclude_line(self.options.whitespace_line_action, "saw a whitespace line", line):
                        continue

            row = line.split(self.options.column_separator)

            if repair_and_validate_lines:
                # Optionally fill missing trailing columns with empty row:
                if self.options.fill_short_lines and len(row) < self.column_count:
                    while len(row) < self.column_count:
                        row.append("")
                    
                # Optionally remove extra trailing columns:
                if self.options.truncate_long_lines and len(row) > self.column_count:
                    row = row[:self.column_count]
                            
                # Optionally validate that the line contained the right number of columns:
                #
                # When we report line numbers in error messages, line 1 is the first line after the header line.
                if self.options.short_line_action != ValidationAction.PASS and len(row) < self.column_count:
                    if self.exclude_line(self.options.short_line_action,
                                         "Required %d columns, saw %d: '%s'" % (self.column_count,
                                                                                len(row),
                                                                                line),
                                         line):
                        continue
                             
                if self.options.long_line_action != ValidationAction.PASS and len(row) > self.column_count:
                    if self.exclude_line(self.options.long_line_action,
                                         "Required %d columns, saw %d (%d extra): '%s'" % (self.column_count,
                                                                                           len(row),
                                                                                           len(row) - self.column_count,
                                                                                           line),
                                         line):
                        continue

                if self._ignore_if_blank_fields(row, line):
                    continue

            if repair_and_validate_values:
                if self.options.invalid_value_action != ValidationAction.PASS:
                    # TODO: find a way to optionally cache the KgtkValue objects
                    # so we don't have to create them a second time in the conversion
                    # and iterator methods below.
                    if self._ignore_invalid_values(row, line):
                        continue

                if self.options.prohibited_list_action != ValidationAction.PASS:
                    if self._ignore_prohibited_lists(row, line):
                        continue

            self.data_lines_passed += 1
            # TODO: User a seperate option to control this.
            # if self.very_verbose:
            #     self.error_file.write(".")
            #    self.error_file.flush()
            
            return row

    # This is both and iterable and an iterator object.
    def __iter__(self)->typing.Iterator[typing.List[str]]:
        return self

    # Get the next row values as a list of strings.
    # TODO: Convert integers, coordinates, etc. to Python types
    def __next__(self)-> typing.List[str]:
        return self.nextrow()

    def concise_rows(self)->typing.Iterator[typing.List[typing.Optional[str]]]:
        """
        Using a generator function, create an iterator that returns rows of fields
        as strings.  Empty fields will be returned as None.

        """
        while True:
            try:
                row: typing.List[str] = self.nextrow()
            except StopIteration:
                return

            # Copy the row, converting empty fields into None:
            results: typing.List[typing.Optional[str]] = [ ]
            field: str
            for field in row:
                if len(field) == 0:
                    results.append(None)
                else:
                    results.append(field)
            yield results
                    

    def to_kgtk_values(self, row: typing.List[str],
                       validate: bool = False,
                       parse_fields: bool = False)->typing.List[KgtkValue]:
        """
        Convert an input row into a list of KgtkValue instances.

        When validate is True, validate each KgtkValue object.
        """
        results: typing.List[KgtkValue] = [ ]
        field: str
        for field in row:
            kv = KgtkValue(field, options=self.value_options, parse_fields=parse_fields)
            if validate:
                kv.validate()
            results.append(kv)
        return results

    def kgtk_values(self,
                    validate: bool = False,
                    parse_fields: bool = False
    )->typing.Iterator[typing.List[KgtkValue]]:
        """
        Using a generator function, create an iterator that returns rows of fields
        as KgtkValue objects.

        When validate is True, validate each KgtkValue object.
        """
        while True:
            try:
                yield self.to_kgtk_values(self.nextrow(), validate=validate, parse_fields=parse_fields)
            except StopIteration:
                return

    def to_concise_kgtk_values(self,
                               row: typing.List[str],
                               validate: bool = False,
                               parse_fields: bool = False
    )->typing.List[typing.Optional[KgtkValue]]:
        """
        Convert an input row into a list of KgtkValue instances.  Empty fields will be returned as None.

        When validate is True, validate each KgtkValue object.
        """
        results: typing.List[typing.Optional[KgtkValue]] = [ ]
        field: str
        for field in row:
            if len(field) == 0:
                results.append(None)
            else:
                kv = KgtkValue(field, options=self.value_options, parse_fields=parse_fields)
                if validate:
                    kv.validate()
                results.append(kv)
        return results

    def concise_kgtk_values(self,
                            validate: bool = False,
                            parse_fields: bool = False
    )->typing.Iterator[typing.List[typing.Optional[KgtkValue]]]:
        """
        Using a generator function, create an iterator that returns rows of fields
        as KgtkValue objects, with empty fields returned as None.

        When validate is True, validate each KgtkValue object.
        """
        while True:
            try:
                yield self.to_concise_kgtk_values(self.nextrow(), validate=validate)
            except StopIteration:
                return

    def to_dict(self, row: typing.List[str], concise: bool=False
    )->typing.Mapping[str, str]:
        """
        Convert an input row into a dict of named fields.

        If concise is True, then empty fields will be skipped.
        """
        results: typing.MutableMapping[str, str] = { }
        field: str
        idx: int = 0

        # We'll use two seperate loops in anticipation of a modest
        # efficiency gain.
        if concise:
            for field in row:
                if len(field) > 0:
                    results[self.column_names[idx]] = field
                idx += 1
        else:
            for field in row:
                results[self.column_names[idx]] = field
                idx += 1
        return results

    def dicts(self, concise: bool=False
    )->typing.Iterator[typing.Mapping[str, str]]:
        """
        Using a generator function, create an iterator that returns each row as a dict of named fields.

        If concise is True, then empty fields will be skipped.

        """
        while True:
            try:
                yield self.to_dict(self.nextrow(), concise=concise)
            except StopIteration:
                return

    def to_kgtk_value_dict(self,
                           row: typing.List[str],
                           validate: bool=False,
                           parse_fields: bool=False,
                           concise: bool=False
    )->typing.Mapping[str, KgtkValue]:
        """
        Convert an input row into a dict of named fields.

        If concise is True, then empty fields will be skipped.

        When validate is True, validate each KgtkValue object.
        """
        results: typing.MutableMapping[str, KgtkValue] = { }
        idx: int = 0
        field: str
        for field in row:
            if concise and len(field) == 0:
                pass # Skip the empty field.
            else:
                kv = KgtkValue(field, options=self.value_options, parse_fields=parse_fields)
                if validate:
                    kv.validate()
                results[self.column_names[idx]] = kv
            idx += 1
        return results

    def kgtk_value_dicts(self,
                         validate: bool=False,
                         parse_fields: bool=False,
                         concise: bool=False
    )->typing.Iterator[typing.Mapping[str, KgtkValue]]:
        """
        Using a generator function, create an iterator that returns each row as a
        dict of named KgtkValue objects.

        If concise is True, then empty fields will be skipped.

        When validate is True, validate each KgtkValue object.
        """
        while True:
            try:
                yield self.to_kgtk_value_dict(self.nextrow(), validate=validate, parse_fields=parse_fields, concise=concise)
            except StopIteration:
                return

    def _ignore_invalid_values(self, row: typing.List[str], line: str)->bool:
        """Give a row of values, validate each value.  If we find one or more
        validation problems, we might want to emit error messages and we might
        want to ignore the entire row.

        Returns True to indicate that the row should be ignored (skipped).

        """
        problems: typing.List[str] = [ ] # Build a list of problems.
        idx: int
        item: str
        for idx, item in enumerate(row):
            if len(item) > 0: # Optimize the common case of empty columns.
                kv: KgtkValue = KgtkValue(item, options=self.value_options)
                if not kv.is_valid():
                    problems.append("col %d (%s) value '%s'is an %s" % (idx, self.column_names[idx], item, kv.describe()))
                if kv.repaired:
                    # If this value was repaired, update the item in the row.
                    #
                    # Warning: We expect this change to be seen by the caller.
                    row[idx] = kv.value

        if len(problems) == 0:
            return False

        return self.exclude_line(self.options.invalid_value_action,
                                 "\n".join(problems),
                                 line)

    def _ignore_prohibited_list(self,
                                idx: int,
                                row: typing.List[str],
                                line: str,
                                problems: typing.List[str],
    ):
        if idx < 0:
            return
        item: str = row[idx]
        if KgtkFormat.LIST_SEPARATOR not in item:
            return
        if len(KgtkValue.split_list(item)) == 1:
            return
        problems.append("col %d (%s) value '%s'is a prohibited list" % (idx, self.column_names[idx], item))

    def _ignore_prohibited_lists(self, row: typing.List[str], line: str)->bool:
        """
        KGTK File Format v2 prohibits "|" lists in the node1, label, and node2 columns.
        """
        problems: typing.List[str] = [ ] # Build a list of problems.

        self._ignore_prohibited_list(self.node1_column_idx, row, line, problems)
        self._ignore_prohibited_list(self.label_column_idx, row, line, problems)
        self._ignore_prohibited_list(self.node2_column_idx, row, line, problems)

        if len(problems) == 0:
            return False

        return self.exclude_line(self.options.invalid_value_action,
                                 "\n".join(problems),
                                 line)

    # May be overridden
    def _ignore_if_blank_fields(self, values: typing.List[str], line: str)->bool:
        return False

    # May be overridden
    def _skip_reserved_fields(self, column_name)->bool:
        return False

    def additional_column_names(self)->typing.List[str]:
        if self.is_edge_file:
            return KgtkBase.additional_edge_columns(self.column_names)
        elif self.is_node_file:
            return KgtkBase.additional_node_columns(self.column_names)
        else:
            # TODO: throw a better exception.
            raise ValueError("KgtkReader: Unknown Kgtk file type.")

    def merge_columns(self, additional_columns: typing.List[str])->typing.List[str]:
        """
        Return a list that merges the current column names with an additional set
        of column names.

        """
        merged_columns: typing.List[str] = self.column_names.copy()

        column_name: str
        for column_name in additional_columns:
            if column_name in self.column_name_map:
                continue
            merged_columns.append(column_name)

        return merged_columns

    @classmethod
    def add_debug_arguments(cls, parser: ArgumentParser, expert: bool = False):
        # This helper function makes it easy to suppress options from
        # The help message.  The options are still there, and initialize
        # what they need to initialize.
        def h(msg: str)->str:
            if expert:
                return msg
            else:
                return SUPPRESS

        egroup: _ArgumentGroup = parser.add_argument_group(h("Error and feedback messages"),
                                                           h("Send error messages and feedback to stderr or stdout, " +
                                                             "control the amount of feedback and debugging messages."))

        # Avoid the argparse bug that prevents these two arguments from having
        # their help messages suppressed directly.
        #
        # TODO: Is there a better fix?
        #
        # TODO: replace --errors-to-stdout and --errors-to-stderr with
        # --errors-to=stdout and --errors-to=stderr, using either an enum
        # or choices.  That will avoid the argparse bug, too.
        if expert:
            errors_to = egroup.add_mutually_exclusive_group()
            errors_to.add_argument(      "--errors-to-stdout", dest="errors_to_stdout",
                                         help="Send errors to stdout instead of stderr",
                                         action="store_true")
            errors_to.add_argument(      "--errors-to-stderr", dest="errors_to_stderr",
                                         help="Send errors to stderr instead of stdout",
                                         action="store_true")
        else:
            egroup.add_argument(      "--errors-to-stderr", dest="errors_to_stderr",
                                      help=h("Send errors to stderr instead of stdout"),
                                      action="store_true")
            egroup.add_argument(      "--errors-to-stdout", dest="errors_to_stdout",
                                      help=h("Send errors to stdout instead of stderr"),
                                      action="store_true")

        egroup.add_argument(      "--show-options", dest="show_options", help=h("Print the options selected (default=%(default)s)."), action='store_true')

        egroup.add_argument("-v", "--verbose", dest="verbose", help="Print additional progress messages (default=%(default)s).", action='store_true')

        egroup.add_argument(      "--very-verbose", dest="very_verbose",
                                  help=h("Print additional progress messages (default=%(default)s)."),
                                  action='store_true')
        
def main():
    """
    Test the KGTK file reader.
    """
    # The EdgeReader import is deferred to avoid circular imports.
    from kgtk.io.edgereader import EdgeReader
    # The NodeReader import is deferred to avoid circular imports.
    from kgtk.io.nodereader import NodeReader

    parser = ArgumentParser()
    parser.add_argument(dest="kgtk_file", help="The KGTK file to read", type=Path, nargs="?")
    KgtkReader.add_debug_arguments(parser, expert=True)
    parser.add_argument(       "--test", dest="test_method", help="The test to perform (default=%(default)s).",
                               choices=["rows", "concise-rows",
                                        "kgtk-values", "concise-kgtk-values",
                                        "dicts", "concise-dicts",
                                        "kgtk-value-dicts", "concise-kgtk-value-dicts"],
                               default="rows")
    parser.add_argument(       "--test-validate", dest="test_validate", help="Validate KgtkValue objects in test (default=%(default)s).",
                               type=optional_bool, nargs='?', const=True, default=False)

    KgtkReaderOptions.add_arguments(parser, mode_options=True, validate_by_default=True, expert=True)
    KgtkValueOptions.add_arguments(parser, expert=True)
    args: Namespace = parser.parse_args()

    error_file: typing.TextIO = sys.stdout if args.errors_to_stdout else sys.stderr

    # Build the option structures.
    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_args(args)
    value_options: KgtkValueOptions = KgtkValueOptions.from_args(args)

    if args.show_options:
        print("--test=%s" % str(args.test), file=error_file)
        print("--test-validate=%s" % str(args.test_validate), file=error_file)
        reader_options.show(out=error_file)
        value_options.show(out=error_file)
        print("=======", file=error_file, flush=True)

    kr: KgtkReader = KgtkReader.open(args.kgtk_file,
                                     error_file = error_file,
                                     options=reader_options,
                                     value_options=value_options,
                                     verbose=args.verbose,
                                     very_verbose=args.very_verbose)

    line_count: int = 0
    row: typing.List[str]
    kgtk_values: typing.List[KgtkValue]
    concise_kgtk_values: typing.List[typing.Optional[KgtkValue]]
    dict_row: typing.Mapping[str, str]
    kgtk_value_dict: typing.Mapping[str, str]
    if args.test_method == "rows":
        if args.verbose:
            print("Testing iterating over rows.", file=error_file, flush=True)
        for row in kr:
            line_count += 1

    elif args.test_method == "concise-rows":
        if args.verbose:
            print("Testing iterating over concise rows.", file=error_file, flush=True)
        for row in kr.concise_rows():
            line_count += 1

    elif args.test_method == "kgtk-values":
        if args.verbose:
            print("Testing iterating over KgtkValue rows.", file=error_file, flush=True)
        for kgtk_values in kr.kgtk_values(validate=args.test_validate):
            line_count += 1

    elif args.test_method == "concise-kgtk-values":
        if args.verbose:
            print("Testing iterating over concise KgtkValue rows.", file=error_file, flush=True)
        for kgtk_values in kr.concise_kgtk_values(validate=args.test_validate):
            line_count += 1
            
    elif args.test_method == "dicts":
        if args.verbose:
            print("Testing iterating over dicts.", file=error_file, flush=True)
        for dict_row in kr.dicts():
            line_count += 1
            
    elif args.test_method == "concise-dicts":
        if args.verbose:
            print("Testing iterating over concise dicts.", file=error_file, flush=True)
        for dict_row in kr.dicts(concise=True):
            line_count += 1
            
    elif args.test_method == "kgtk-value-dicts":
        if args.verbose:
            print("Testing iterating over KgtkValue dicts.", file=error_file, flush=True)
        for kgtk_value_dict in kr.kgtk_value_dicts(validate=args.test_validate):
            line_count += 1
            
    elif args.test_method == "concise-kgtk-value-dicts":
        if args.verbose:
            print("Testing iterating over concise KgtkValue dicts.", file=error_file, flush=True)
        for kgtk_value_dict in kr.kgtk_value_dicts(concise=True, validate=args.test_validate):
            line_count += 1
            
    print("Read %d lines" % line_count, file=error_file, flush=True)

if __name__ == "__main__":
    main()

