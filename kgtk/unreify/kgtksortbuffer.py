"""
Build a sorting buffer for KGTK rows.  The design is intended to support using
an external sorter for large files.

"""
from argparse import ArgumentParser, Namespace
import attr
from pathlib import Path
import sys
import typing

from kgtk.kgtkformat import KgtkFormat
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderMode, KgtkReaderOptions
from kgtk.io.kgtkwriter import KgtkWriter
from kgtk.utils.argparsehelpers import optional_bool
from kgtk.value.kgtkvalueoptions import KgtkValueOptions

@attr.s(slots=True, frozen=False)
class KgtkSortBuffer(KgtkFormat):
    KEYGEN_TYPE = typing.Callable[['KgtkSortBuffer', typing.List[str]], str]

    DEFAULT_GROUPED: bool = True
    DEFAULT_KEY_FIELD_SEPARATOR: str = KgtkFormat.KEY_FIELD_SEPARATOR
    DEFAULT_ERROR_FILE: typing.TextIO = sys.stderr
    DEFAULT_VERBOSE: bool = False
    DEFAULT_VERY_VERBOSE: bool = False


    node1_column_idx: int = attr.ib(validator=attr.validators.instance_of(int))
    label_column_idx: int = attr.ib(validator=attr.validators.instance_of(int))
    node2_column_idx: int = attr.ib(validator=attr.validators.instance_of(int))
    id_column_idx: int = attr.ib(validator=attr.validators.instance_of(int))

    # Note: keygen is defined below.

    grouped: bool = attr.ib(validator=attr.validators.instance_of(bool), default=DEFAULT_GROUPED)

    # The column separator is normally tab.
    key_field_separator: str = attr.ib(validator=attr.validators.instance_of(str), default=DEFAULT_KEY_FIELD_SEPARATOR)

    error_file: typing.TextIO = attr.ib(default=DEFAULT_ERROR_FILE)
    verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=DEFAULT_VERBOSE)
    very_verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=DEFAULT_VERY_VERBOSE)

    input_count: int = attr.ib(default=0)

    # Tradeoff:
    # The buffer could be a map to a list of rows.
    # Alternatively, we can ensure that the keys to the map are unique and
    # sequenced in input order by adding a suffix to the key.
    # Which will cause more overhead, the longer keys or the many small lists?
    list_buf: typing.MutableMapping[str, typing.List[str]] = attr.ib(factory=dict)
    list_buf_zfill: int = attr.ib(validator=attr.validators.instance_of(int), default=9)

    group_buf: typing.MutableMapping[str, typing.List[typing.List[str]]] = attr.ib(factory=dict)

    @staticmethod
    def node1_keygen(buf: 'KgtkSortBuffer', row: typing.List[str])->str:
        if buf.node1_column_idx < 0:
            raise ValueError("KgtkSortBuffer: no node1 index")
        return row[buf.node1_column_idx]

    @staticmethod
    def label_keygen(buf: 'KgtkSortBuffer', row: typing.List[str])->str:
        if buf.label_column_idx < 0:
            raise ValueError("KgtkSortBuffer: no label index")
        return row[buf.label_column_idx]

    @staticmethod
    def node2_keygen(buf: 'KgtkSortBuffer', row: typing.List[str])->str:
        if buf.node2_column_idx < 0:
            raise ValueError("KgtkSortBuffer: no node2 index")
        return row[buf.node2_column_idx]

    @staticmethod
    def triple_keygen(buf: 'KgtkSortBuffer', row: typing.List[str])->str:
        if buf.node1_column_idx < 0:
            raise ValueError("KgtkSortBuffer: no node1 index")
        if buf.label_column_idx < 0:
            raise ValueError("KgtkSortBuffer: no label index")
        if buf.node2_column_idx < 0:
            raise ValueError("KgtkSortBuffer: no node2 index")
        return row[buf.node1_column_idx] + buf.key_field_separator + \
            row[buf.label_column_idx] + buf.key_field_separator + \
            row[buf.node2_column_idx]

    @staticmethod
    def quad_keygen(buf: 'KgtkSortBuffer', row: typing.List[str])->str:
        if buf.node1_column_idx < 0:
            raise ValueError("KgtkSortBuffer: no node1 index")
        if buf.label_column_idx < 0:
            raise ValueError("KgtkSortBuffer: no label index")
        if buf.node2_column_idx < 0:
            raise ValueError("KgtkSortBuffer: no node2 index")
        if buf.id_column_idx < 0:
            raise ValueError("KgtkSortBuffer: no id index")
        return row[buf.node1_column_idx] + buf.key_field_separator + \
            row[buf.label_column_idx] + buf.key_field_separator + \
            row[buf.node2_column_idx] +  buf.key_field_separator + \
            row[buf.id_column_idx]

    @staticmethod
    def id_keygen(buf: 'KgtkSortBuffer', row: typing.List[str])->str:
        if buf.id_column_idx < 0:
            raise ValueError("KgtkSortBuffer: no id index")
        return row[buf.id_column_idx]

    DEFAULT_KEYGEN: KEYGEN_TYPE = node1_keygen
    keygen: KEYGEN_TYPE = attr.ib(default=DEFAULT_KEYGEN)

    @classmethod
    def new_from_reader(cls,
                        kr: KgtkReader,
                        keygen: 'KgtkSortBuffer.KEYGEN_TYPE'=DEFAULT_KEYGEN,
                        grouped: bool=DEFAULT_GROUPED,
    )->'KgtkSortBuffer':
        return cls(node1_column_idx=kr.node1_column_idx,
                   label_column_idx=kr.label_column_idx,
                   node2_column_idx=kr.node2_column_idx,
                   id_column_idx=kr.id_column_idx,
                   keygen=keygen,
                   grouped=grouped,
                   error_file=kr.error_file,
                   verbose=kr.verbose,
                   very_verbose=kr.very_verbose)

    @classmethod
    def readall(cls,
                kr: KgtkReader,
                keygen: 'KgtkSortBuffer.KEYGEN_TYPE'=DEFAULT_KEYGEN,
                grouped: bool=DEFAULT_GROUPED,
    )->'KgtkSortBuffer':
        ksb: KgtkSortBuffer = cls.new_from_reader(kr, keygen=keygen, grouped=grouped)
        
        row: typing.List[str]
        for row in kr:
            ksb.add(row)

        return ksb

    def add(self, row: typing.List[str]):
        self.input_count += 1
        key: str
        if self.grouped:
            key = self.keygen(self, row)
            if key in self.group_buf:
                self.group_buf[key].append(row)
            else:
                self.group_buf[key] = [row]

        else:
            key = self.keygen(self, row) + " " + str(self.input_count).zfill(self.list_buf_zfill)
            self.list_buf[key] = row

    # We can iterate many times, in sequence or in parallel, but we shouldn't
    # alter the buffer when iterating over it.
    def iterate(self)->typing.Generator[typing.List[str], None, None]:
        key: str
        row: typing.List[str]
        if self.grouped:
            for key in sorted(self.group_buf.keys()):
                rows: typing.List[typing.List[str]] = self.group_buf[key]
                for row in rows:
                    yield row
        else:
            for key in sorted(self.list_buf.keys()):
                row = self.list_buf[key]
                yield row

    def groupiterate(self)->typing.Generator[typing.List[typing.List[str]], None, None]:
        key: str
        if self.grouped:
            for key in sorted(self.group_buf.keys()):
                rows: typing.List[typing.List[str]] = self.group_buf[key]
                yield rows
        else:
            raise ValueError("KgtkSortBuffer.groupiterate() called when not sorted by groups.")

@attr.s(slots=True, frozen=False)
class KgtkSortBufferTest(KgtkFormat):
    input_file_path: Path = attr.ib(validator=attr.validators.instance_of(Path))
    output_file_path: Path = attr.ib(validator=attr.validators.instance_of(Path))

    keygen: str = attr.ib(validator=attr.validators.instance_of(str), default="node1")
    group_sort: bool = attr.ib(validator=attr.validators.instance_of(bool), default=KgtkSortBuffer.DEFAULT_GROUPED)
    group_iterate: bool = attr.ib(validator=attr.validators.instance_of(bool), default=KgtkSortBuffer.DEFAULT_GROUPED)

    # TODO: find working validators
    # value_options: typing.Optional[KgtkValueOptions] = attr.ib(attr.validators.optional(attr.validators.instance_of(KgtkValueOptions)), default=None)
    reader_options: typing.Optional[KgtkReaderOptions]= attr.ib(default=None)
    value_options: typing.Optional[KgtkValueOptions] = attr.ib(default=None)

    error_file: typing.TextIO = attr.ib(default=sys.stderr)
    verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    very_verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    def process(self):
        # Open the input file.
        if self.verbose:
            print("Opening the input file: %s" % str(self.input_file_path), file=self.error_file, flush=True)

        kr: KgtkReader =  KgtkReader.open(self.input_file_path,
                                          error_file=self.error_file,
                                          options=self.reader_options,
                                          value_options = self.value_options,
                                          verbose=self.verbose,
                                          very_verbose=self.very_verbose,
        )

        if self.verbose:
            print("Opening the output file: %s" % str(self.output_file_path), file=self.error_file, flush=True)
        # Open the output file.
        kw: KgtkWriter = KgtkWriter.open(kr.column_names,
                                         self.output_file_path,
                                         mode=KgtkWriter.Mode[kr.mode.name],
                                         require_all_columns=True,
                                         prohibit_extra_columns=True,
                                         fill_missing_columns=False,
                                         gzip_in_parallel=False,
                                         verbose=self.verbose,
                                         very_verbose=self.very_verbose)

        input_group_count: int = 0
        input_line_count: int = 0

        # TODO: use an enum.
        keygen: KgtkSortBuffer.KEYGEN_TYPE
        if self.keygen == "node1":
            keygen = KgtkSortBuffer.node1_keygen
        elif self.keygen == "label":
            keygen = KgtkSortBuffer.label_keygen
        elif self.keygen == "node2":
            keygen = KgtkSortBuffer.node2_keygen
        elif self.keygen == "triple":
            keygen = KgtkSortBuffer.triple_keygen
        elif self.keygen == "quad":
            keygen = KgtkSortBuffer.quad_keygen
        elif self.keygen == "id":
            keygen = KgtkSortBuffer.id_keygen
        else:
            raise ValueError("Unknown keygen '%s'." % self.keygen)

        if self.verbose:
            print("Create the sort buffer.", file=self.error_file, flush=True)
        ksb: KgtkSortBuffer = KgtkSortBuffer.readall(kr, keygen=keygen, grouped=self.group_sort)

        if self.verbose:
            print("Processing the sorted records.", file=self.error_file, flush=True)

        row: typing.List[str]
        if self.group_iterate:
            rows: typing.List[typing.List[str]]
            for rows in ksb.groupiterate():
                input_group_count += 1
                for row in rows:
                    input_line_count += 1
                    kw.write(row)
                
        else:
            for row in ksb.iterate():
                input_line_count += 1
                kw.write(row)

        if self.verbose:
            print("Processed %d records." % (input_line_count), file=self.error_file, flush=True)
            print("Processed %d groups." % (input_group_count), file=self.error_file, flush=True)
        
        kw.close()

            
def main():
    """
    Test the KGTK copy template.
    """
    parser: ArgumentParser = ArgumentParser()

    parser.add_argument("-i", "--input-file", dest="input_file_path",
                        help="The KGTK input file. (default=%(default)s)", type=Path, default="-")

    parser.add_argument("-o", "--output-file", dest="output_file_path",
                        help="The KGTK output file. (default=%(default)s).", type=Path, default="-")
    
    parser.add_argument(      "--keygen", dest="keygen",
                        help="The KGTK key generation procedure. (default=%(default)s).", type=str, default="node1")
    
    parser.add_argument(      "--group-sort", dest="group_sort",
                              help="If true, use the grouped sort and buffer. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--group-iterate", dest="group_iterate",
                              help="If true, us the grouped iteration. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    KgtkReader.add_debug_arguments(parser)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, expert=True)
    KgtkValueOptions.add_arguments(parser)

    args: Namespace = parser.parse_args()

    error_file: typing.TextIO = sys.stdout if args.errors_to_stdout else sys.stderr

    # Build the option structures.                                                                                                                          
    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_args(args)
    value_options: KgtkValueOptions = KgtkValueOptions.from_args(args)

   # Show the final option structures for debugging and documentation.                                                                                             
    if args.show_options:
        print("--input-files %s" % " ".join([str(path) for  path in input_file_paths]), file=error_file, flush=True)
        print("--output-file=%s" % str(args.output_file_path), file=error_file, flush=True)
        print("--keygen=%s" % str(args.keygen), file=error_file, flush=True)
        print("--group-sort=%s" % str(args.group_sort), file=error_file, flush=True)
        print("--group-iterate=%s" % str(args.group_iterate), file=error_file, flush=True)

        reader_options.show(out=error_file)
        value_options.show(out=error_file)

    ksbt: KgtkSortBufferTest = KgtkSortBufferTest(
        input_file_path=args.input_file_path,
        output_file_path=args.output_file_path,
        keygen=args.keygen,
        group_sort=args.group_sort,
        group_iterate=args.group_iterate,
        reader_options=reader_options,
        value_options=value_options,
        error_file=error_file,
        verbose=args.verbose,
        very_verbose=args.very_verbose,
    )

    ksbt.process()
    
if __name__ == "__main__":
    main()
