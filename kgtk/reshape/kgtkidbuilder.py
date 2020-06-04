from argparse import ArgumentParser, Namespace, SUPPRESS
import attr
from pathlib import Path
import sys
import typing

from kgtk.kgtkformat import KgtkFormat
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
from kgtk.io.kgtkwriter import KgtkWriter
from kgtk.utils.argparsehelpers import optional_bool
from kgtk.value.kgtkvalueoptions import KgtkValueOptions
from kgtk.value.kgtkvalue import KgtkValue

@attr.s(slots=True, frozen=True)
class KgtkIdBuilderOptions(KgtkFormat):
    # TODO: use an enum
    CONCAT_STYLE: str = "concat"
    PREFIXED_STYLE: str = "prefixed"
    STYLES: typing.List[str] = [ CONCAT_STYLE, PREFIXED_STYLE ]

    # Defaults for prefixed style IDs.
    DEFAULT_PREFIX: str = "E"
    DEFAULT_INITIAL_ID: int = 1

    id_column_name: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    overwrite_id: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    verify_id_unique: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    id_style: str = attr.ib(validator=attr.validators.instance_of(str), default=PREFIXED_STYLE)
    id_prefix: str = attr.ib(validator=attr.validators.instance_of(str), default=DEFAULT_PREFIX)
    initial_id: int = attr.ib(validator=attr.validators.instance_of(int), default=DEFAULT_INITIAL_ID)

    @classmethod
    def add_arguments(cls, parser: ArgumentParser, expert: bool = False, overwrite: bool = False):

        # This helper function makes it easy to suppress options from
        # The help message.  The options are still there, and initialize
        # what they need to initialize.
        def h(msg: str)->str:
            if expert:
                return msg
            else:
                return SUPPRESS


        # This one is likely to cause conflicts in the future.
        #
        # The default value is indirect.
        parser.add_argument(      "--id-column-name", dest="id_column_name",
                                  help=h("The name of the id column. (default=id)."))
            
        parser.add_argument(      "--overwrite-id", dest="overwrite_id",
                                  help="Replace existing id values. (default=%(default)s).",
                                  type=optional_bool, nargs='?', const=True, default=overwrite)

        parser.add_argument(      "--verify-id-unique", dest="verify_id_unique",
                                  help="Verify ID uniqueness.  Uses an in-memory set of IDs. (default=%(default)s).",
                                  type=optional_bool, nargs='?', const=True, default=True)

        parser.add_argument(      "--id-style", dest="id_style", default=cls.PREFIXED_STYLE, choices=cls.STYLES,
                                  help=h("The id style. (default=%(default)s)."))

        parser.add_argument(      "--id-prefix", dest="id_prefix", default=cls.DEFAULT_PREFIX,
                                  help=h("The prefix for a prefix/number id. (default=%(default)s)."))

        parser.add_argument(      "--initial-id", dest="initial_id", type=int, default=cls.DEFAULT_INITIAL_ID,
                                  help=h("The initial value for a prefix/number id. (default=%(default)s)."))

    @classmethod
    def from_dict(cls, d: dict)->'KgtkIdBuilderOptions':
        return cls(
            id_column_name=d.get("id_column_name"),
            overwrite_id=d.get("overwrite_id", False),
            verify_id_unique=d.get("verify_id_unique", False),
            id_style=d.get("id_style", cls.PREFIXED_STYLE),
            id_prefix=d.get("id_prefix", cls.DEFAULT_PREFIX),
            initial_id=d.get("initial_id", cls.DEFAULT_INITIAL_ID),
        )

    # Build the value parsing option structure.
    @classmethod
    def from_args(cls, args: Namespace)->'KgtkIdBuilderOptions':
        return cls.from_dict(vars(args))

    def show(self, out: typing.TextIO=sys.stderr):
        if self.id_column_name is not None:
            print("--id-column-name=%s" % str(self.id_column_name), file=out, flush=True)
        print("--overwrite-id=%s" % str(self.overwrite_id), file=out, flush=True)
        print("--verify_id_unique=%s" % str(self.verify_id_unique), file=out, flush=True)
        print("--id-style=%s" % str(self.id_style), file=out, flush=True)
        print("--id-prefix=%s" % str(self.id_prefix), file=out, flush=True)
        print("--initial-id=%s" % str(self.initial_id), file=out, flush=True)


@attr.s(slots=True, frozen=False)
class KgtkIdBuilder(KgtkFormat):
    kr: KgtkReader = attr.ib(validator=attr.validators.instance_of(KgtkReader))
    
    options: KgtkIdBuilderOptions = attr.ib(validator=attr.validators.instance_of(KgtkIdBuilderOptions))

    column_names: typing.List[str]= attr.ib() # TODO: add validator

    id_column_name: str = attr.ib(validator=attr.validators.instance_of(str))
    id_column_idx: int = attr.ib(validator=attr.validators.instance_of(int))
    add_id_column: bool = attr.ib(validator=attr.validators.instance_of(bool))

    current_id: int = attr.ib(validator=attr.validators.instance_of(int))

    id_set: typing.Set[str] =attr.ib(validator=attr.validators.instance_of(set), factory=set)

    @classmethod
    def new(cls,
            kr: KgtkReader,
            options: KgtkIdBuilderOptions,
    )->'KgtkIdBuilder':
        """
        This is the KgtkIdBuilder factory method.
        """
        column_names: typing.List[str] = kr.column_names.copy()

        # Find the ID column.
        id_column_idx: int
        add_id_column: bool
        id_column_name: str
        if options.id_column_name is not None:
            # The ID column was explicitly named.
            id_column_name = options.id_column_name
            if id_column_name in kr.column_name_map:
                # The ID column already exists.
                id_column_idx = kr.column_name_map[id_column_name]
                add_id_column = False
            else:
                # Create a new ID column.
                id_column_idx = len(column_names)
                column_names.append(id_column_name)
                add_id_column = True
        else:
            # The ID column was not explicitly named.
            if kr.id_column_idx >= 0:
                # The input file has an ID column.  Use it.
                id_column_name = kr.column_names[kr.id_column_idx]
                id_column_idx = kr.id_column_idx
                add_id_column = False
            else:
                # Create a new ID column.
                id_column_idx = len(column_names)
                id_column_name = KgtkFormat.ID
                column_names.append(KgtkFormat.ID)
                add_id_column = True

        # Any prerequisites?
        if options.id_style == KgtkIdBuilderOptions.PREFIXED_STYLE:
            if kr.node1_column_idx < 0:
                raise ValueError("No node1 column index")
            if kr.label_column_idx < 0:
                raise ValueError("No label column index")
            if kr.node2_column_idx < 0:
                raise ValueError("No node2 column index")
        
        return cls(kr,
                   options=options,
                   column_names=column_names,
                   id_column_name=id_column_name,
                   id_column_idx=id_column_idx,
                   add_id_column=add_id_column,
                   current_id=options.initial_id
        )

    def verify_uniqueness(self, id_value: str, row: typing.List[str], line_number, who: str):
        if KgtkFormat.LIST_SEPARATOR in id_value:
            # The ID value might be a list.
            id_v: str
            for id_v in KgtkValue.split_list(id_value):
                if id_v in self.id_set:
                    # TODO: Probably want more error handling options, such as
                    # printing the offending row and choosing to continue.
                    raise ValueError("Line %d: %s ID '%s' duplicates a previous ID '%s'." % (line_number, who, id_value, id_v))
                else:
                    self.id_set.add(id_v)
        else:
            # Not a list, we can process this faster.
            if id_value in self.id_set:
                # TODO: Probably want more error handling options, such as
                # printing the offending row and choosing to continue.
                raise ValueError("Line %d: %s ID '%s' duplicates a previous ID '%s'." % (line_number, who, id_value, id_value))
            else:
                self.id_set.add(id_value)
        

    def build(self, row: typing.List[str], line_number: int)->typing.List[str]:
        """
        Build a new ID value if needed.
        """
        if self.add_id_column:
            row = row.copy() # as a precaution
            row.append("")
        else:            
            if row[self.id_column_idx] != "" and not self.options.overwrite_id:
                if self.options.verify_id_unique:
                    self.verify_uniqueness(row[self.id_column_idx], row, line_number, "existing")

                return row
            row = row.copy() # as a precaution

        new_id: str
        if self.options.id_style == KgtkIdBuilderOptions.CONCAT_STYLE:
            new_id = self.build_concat(row)
        elif self.options.id_style == KgtkIdBuilderOptions.PREFIXED_STYLE:
            new_id = self.build_prefixed(row)
        else:
            raise ValueError("Unknown ID style '%s'." % self.options.id_style)

        row[self.id_column_idx] = new_id
        if self.options.verify_id_unique:
            self.verify_uniqueness(new_id, row, line_number, "noew")
        return row

    def build_concat(self, row: typing.List[str])->str:
        return row[self.kr.node1_column_idx] + "-" + row[self.kr.label_column_idx] + "-" + row[self.kr.node2_column_idx]

    def build_prefixed(self, row: typing.List[str])->str:
        new_id: str =  self.options.id_prefix + str(self.current_id)
        self.current_id += 1
        return new_id

    def process(self, kw: KgtkWriter):
        line_number: int = 0
        row: typing.List[str]
        for row in self.kr:
            line_number += 1
            kw.write(self.build(row, line_number))

def main():
    """
    Test the KGTK ID builder.
    """
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument(dest="input_file_path", help="The KGTK file with the input data (default=%(default)s)", type=Path, nargs="?", default="-")
    parser.add_argument("-o", "--output-file", dest="output_file_path", help="The KGTK file to write (default=%(default)s).", type=Path, default="-")

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
        print("input: %s" % str(args.input_file_path), file=error_file, flush=True)
        print("--output-file=%s" % str(args.output_file_path), file=error_file, flush=True)
        idbuilder_options.show(out=error_file)
        reader_options.show(out=error_file)
        value_options.show(out=error_file)

    # First create the KgtkReader.  It provides parameters used by the ID
    # column builder. Next, create the ID column builder, which provides a
    # possibly revised list of column names for the KgtkWriter.  Last, create
    # the KgtkWriter.

    # Open the input file.
    kr: KgtkReader =  KgtkReader.open(args.input_file_path,
                                      error_file=error_file,
                                      options=reader_options,
                                      value_options = value_options,
                                      verbose=args.verbose,
                                      very_verbose=args.very_verbose,
    )

    # Create the ID builder.
    idb: KgtkIdBuilder = KgtkIdBuilder.new(kr, idbuilder_options)

    # Open the output file.
    ew: KgtkWriter = KgtkWriter.open(idb.column_names,
                                     args.output_file_path,
                                     mode=kr.mode,
                                     require_all_columns=True,
                                     prohibit_extra_columns=True,
                                     fill_missing_columns=False,
                                     gzip_in_parallel=False,
                                     verbose=args.verbose,
                                     very_verbose=args.very_verbose)

    # Process the input file, building IDs.
    idb.process(ew)

if __name__ == "__main__":
    main()
