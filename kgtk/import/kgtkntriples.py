"""Import ntriples into KGTK format.
"""
from argparse import ArgumentParser, Namespace
import attr
import csv
from pathlib import Path
import re
import shortuuid # type: ignore
import sys
import typing

from kgtk.kgtkformat import KgtkFormat
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderMode
from kgtk.io.kgtkwriter import KgtkWriter
from kgtk.reshape.kgtkidbuilder import KgtkIdBuilder, KgtkIdBuilderOptions
from kgtk.utils.argparsehelpers import optional_bool


@attr.s(slots=True, frozen=False)
class KgtkNtriples(KgtkFormat):
    # Class attributes:
    DEFAULT_PREFIX_EXPANSION: str = "prefix_expansion"
    DEFAULT_STRUCTURED_VALUE: str = "kgtk:structured_value"
    DEFAULT_STRUCTURED_URI: str = "kgtk:structured_uri"
    DEFAULT_NAMESPACE_ID_PREFIX: str = "n"
    DEFAULT_NAMESPACE_ID_COUNTER: int = 1
    DEFAULT_NEWNODE_PREFIX: str = "kgtk:node"
    DEFAULT_NEWNODE_COUNTER: int = 1
    DEFAULT_LOCAL_NAMESPACE_PREFIX: str = "X"
    DEFAULT_LOCAL_NAMESPACE_USE_UUID: bool = True
    DEFAULT_ALLOW_LAX_URI: bool = True
    DEFAULT_BUILD_ID: bool = False

    COLUMN_NAMES: typing.List[str] = [KgtkFormat.NODE1, KgtkFormat.LABEL, KgtkFormat.NODE2, KgtkFormat.ID]
    
    # A URI must begin with a scheme per RFC 3986.
    #
    # We don't use this because ISI was inserting some invalid URIs that did
    # not include a scheme, but kept the definition for reference.
    SCHEME_PAT: str = r'^(?:[a-zA_Z][-.+0-9a-zA_Z]*://)'

    # The URI is delimited by matching angle brackets.  Angle brackets
    # cannot appear in a valid URI per RFC 3986.
    URI_PAT: str = r'(?:<[^>]+>)'

    # This is a guess about what may be in a blank node. It's entirely
    # possible that other characters, sych as hyphen, might be allowed.
    BLANK_NODE_PAT: str = r'(?:_:[0-9a-zA-Z]+)'

    # Double quoted strings with backslash escapes.
    STRING_PAT: str = r'"(?:[^\\]|(?:\\.))*"'

    STRUCTURED_VALUE_PAT: str = r'(?:{string}(?:\^\^{uri}))'.format(string=STRING_PAT, uri=URI_PAT)
    FIELD_PAT: str = r'(?:{uri}|{blank_node}|{structured_value})'.format(uri=URI_PAT, blank_node=BLANK_NODE_PAT, structured_value=STRUCTURED_VALUE_PAT)
    ROW_PAT: str = r'(?P<node1>{field})\s(?P<label>{field})\s(?P<node2>{field})\s\.'.format(field=FIELD_PAT)
    ROW_RE: typing.Pattern = re.compile(r'^' + ROW_PAT + r'$')

    # Instance attributes:

    input_file_path: Path = attr.ib(validator=attr.validators.instance_of(Path))

    output_file_path: Path = attr.ib(validator=attr.validators.instance_of(Path))

    reject_file_path: typing.Optional[Path] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Path)))

    namespace_file_path: typing.Optional[Path] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Path)))

    allow_lax_uri: bool = attr.ib(validator=attr.validators.instance_of(bool), default=DEFAULT_ALLOW_LAX_URI)

    local_namespace_prefix: str = attr.ib(validator=attr.validators.instance_of(str), default=DEFAULT_LOCAL_NAMESPACE_PREFIX)
    local_namespace_use_uuid: bool = attr.ib(validator=attr.validators.instance_of(bool), default=DEFAULT_LOCAL_NAMESPACE_USE_UUID)

    namespace_id_prefix: str = attr.ib(validator=attr.validators.instance_of(str), default=DEFAULT_NAMESPACE_ID_PREFIX)
    namespace_id_counter: int = attr.ib(validator=attr.validators.instance_of(int), default=DEFAULT_NAMESPACE_ID_COUNTER)

    prefix_expansion_label: str = attr.ib(validator=attr.validators.instance_of(str), default=DEFAULT_PREFIX_EXPANSION)

    structured_value_label: str = attr.ib(validator=attr.validators.instance_of(str), default=DEFAULT_STRUCTURED_VALUE)
    structured_uri_label: str = attr.ib(validator=attr.validators.instance_of(str), default=DEFAULT_STRUCTURED_URI)

    newnode_prefix: str = attr.ib(validator=attr.validators.instance_of(str), default=DEFAULT_NEWNODE_PREFIX)
    newnode_counter: int = attr.ib(validator=attr.validators.instance_of(int), default=DEFAULT_NEWNODE_COUNTER)

    build_id: bool = attr.ib(validator=attr.validators.instance_of(bool), default=DEFAULT_BUILD_ID)
    idbuilder_options: typing.Optional[KgtkIdBuilderOptions] = attr.ib(default=None)

    error_file: typing.TextIO = attr.ib(default=sys.stderr)
    verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    very_verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    local_namespace_uuid: str = attr.ib(factory=shortuuid.uuid)

    namespace_prefixes: typing.MutableMapping[str, str] = attr.ib(factory=dict)
    namespace_ids: typing.MutableMapping[str, str] = attr.ib(factory=dict)

    output_line_count: int = attr.ib(default=0)

    def write_row(self, ew: KgtkWriter, node1: str, label: str, node2: str):
        # TODO: build an ID

        output_row: typing.List[str] = [ node1, label, node2]
        ew.write(output_row)
        self.output_line_count += 1

    def convert_blank_node(self, item: str)->typing.Tuple[str, bool]:
        body: str = item[1:] # Strip the leading underscore, keep the colon.
        if self.local_namespace_use_uuid:
            return self.local_namespace_prefix + self.local_namespace_uuid + body, True
        else:
            return self.local_namespace_prefix + body, True

    def convert_uri(self, item: str, line_number: int)->typing.Tuple[str, bool]:
        body: str = item[1:-1] # Strip off the enclosing brackets.
        namespace_prefix: str
        suffix: str

        after_slashslash: int
        slashslash: int =  body.rfind("://")
        if slashslash < 1:
            if not self.allow_lax_uri:
                if self.verbose:
                    print("Line %d: invalid URI: '%s'" % (line_number, item), file=self.error_file, flush=True)
                return item, False
            after_slashslash = 0
        else:
            after_slashslash = slashslash + len("://")

        end_of_namespace_prefix: int = -1
        last_hash: int = body.rfind("#", after_slashslash)
        last_slash: int = body.rfind("/", after_slashslash)
        if last_hash >= 0:
            namespace_prefix = body[:last_hash+1]
            suffix = body[last_hash+1:]

        elif last_slash >= 0:
            namespace_prefix = body[:last_slash+1]
            suffix = body[last_slash+1:]
        else:
            namespace_prefix = body
            suffix = ""

        namespace_id: str
        if namespace_prefix in self.namespace_prefixes:
            namespace_id = self.namespace_prefixes[namespace_prefix]
        else:
            while True:
                namespace_id = self.namespace_id_prefix + str(self.namespace_id_counter)
                self.namespace_id_counter += 1
                if namespace_id not in self.namespace_ids:
                    break
            self.namespace_ids[namespace_id] = namespace_prefix
            self.namespace_prefixes[namespace_prefix] = namespace_id

        return namespace_id + ":" + suffix, True

    def escape_pipe(self, item: str)->str:
        # TODO: ensure that vertical bars (pipes) are escaped.
        return item

    def convert_string(self, item: str, line_number: int)->typing.Tuple[str, bool]:
        # Convert this to a KGTK string.
        #
        # Our parser guarantees that double quoted strings use proper
        # escapes... except for vertical bars (pipes).  We have extra work to do to
        # ensure that vertical bars (pipes) are escaped.
        return self.escape_pipe(item), True
 
    def generate_new_node_symbol(self)->str:
        new_node_symbol: str = self.newnode_prefix + str(self.newnode_counter)
        self.newnode_counter += 1
        return new_node_symbol
    
    def convert_structured_literal(self, item: str, line_number: int, ew: KgtkWriter)->typing.Tuple[str, bool]:
        # This is the subset of strictured literals that fits the
        # pattern "STRING"^^<URI>.

        # Start by splitting on '^^'. We are certain it exists, and that the rightmost
        # instance is the one we want.
        uparrows: int = item.rfind("^^")
        if uparrows < 0:
            # This shouldn't happen!
            if self.verbose:
                print("Line %d: no uparrows in '%s'." % (line_number, item), file=self.error_file, flush=True)
            return item, False

        string: str = item[:uparrows]
        uri: str = item[uparrows+2:]

        if uri == '<http://www.w3.org/2001/XMLSchema#string>':
            # Convert this to a KGTK string.
            return self.escape_pipe(string), True
        elif uri == '<http://www.w3.org/2001/XMLSchema#int>':
            # Convert this to a KGTK number:
            return string[1:-1], True
        elif uri == '<http://www.w3.org/2001/XMLSchema#double>':
            # Convert this to a KGTK number:
            return string[1:-1], True
        elif uri == '<http://www.w3.org/2001/XMLSchema#float>':
            # Convert this to a KGTK number:
            return string[1:-1], True
        elif uri == '<http://www.w3.org/2001/XMLSchema#decimal>':
            # Convert this to a KGTK number:
            return string[1:-1], True

        converted_uri: str
        valid: bool
        converted_uri, valid = self.convert_uri(uri, line_number)
        if not valid:
            return item, False

        new_node_symbol: str = self.generate_new_node_symbol()
        self.write_row(ew, new_node_symbol, self.structured_value_label, string)
        self.write_row(ew, new_node_symbol, self.structured_uri_label, converted_uri)

        return new_node_symbol, True

    def convert(self, item: str, line_number: int, ew: KgtkWriter)->typing.Tuple[str, bool]:
        """
        Convert an ntriples item to KGTK format.

        TODO: update output_line_count for row written here.
        """
        if item.startswith("_:"):
            return self.convert_blank_node(item)
        elif item.startswith("<") and item.endswith(">"):
            return self.convert_uri(item, line_number)
        elif item.startswith('"') and item.endswith('"'):
            return self.convert_string(item, line_number)
        elif item.startswith('"') and item.endswith(">"):
            return self.convert_structured_literal(item, line_number, ew)

        if self.verbose:
            print("Line %d: unrecognized item '%s'" %(line_number, item), file=self.error_file, flush=True)

        return item, False
    
    def get_default_namespaces(self)->int:
        namespace_id: str = "xml-schema-type"
        namespace_prefix: str = "http://www.w3.org/2001/XMLSchema#"
        self.namespace_ids[namespace_id] = namespace_prefix
        self.namespace_prefixes[namespace_prefix] = namespace_id
        return 1
    
    def get_initial_namespaces(self)->int:
        # Read the namespaces.  If no file, use a limited internal
        # default.
        if self.namespace_file_path is None:
            return self.get_default_namespaces()

        if self.verbose:
            print("Processing namespace file file %s" % str(self.reject_file_path), file=self.error_file, flush=True)

        kr: KgtkReader =  KgtkReader.open(self.namespace_file_path,
                                          mode=KgtkReaderMode.EDGE,
                                          error_file=self.error_file,
                                          verbose=self.verbose,
                                          very_verbose=self.very_verbose,
        )
        namespace_line_count: int = 0
        namespace_row: typing.List[str]
        for namespace_row in kr:
            namespace_line_count += 1
            if namespace_row[kr.label_column_idx] == self.prefix_expansion_label:
                namespace_id: str = namespace_row[kr.node1_column_idx]
                namespace_prefix: str = namespace_row[kr.node2_column_idx]
                if not (namespace_prefix.startswith('"') and namespace_prefix.endswith('"')):
                    if self.verbose:
                        print("The namespace prefix must be a KGKT string: '%s'" % namespace_prefix, file=self.error_file, flush=True)
                    continue
                
                # Strip the delimiting double quotes from the KGTk string.
                # Per RFC 3986, internal double quotes are not allowed in
                # a URL unless percent-encoded, so we needen't bother looking
                # for them.
                namespace_prefix = namespace_prefix[1:-1]

                if namespace_prefix in self.namespace_prefixes:
                    if self.verbose:
                        print("Duplicate initial namespace prefix '%s'" % namespace_prefix, file=self.error_file, flush=True)
                else:
                    self.namespace_prefixes[namespace_prefix] = namespace_id
                if namespace_id in self.namespace_ids:
                    if self.verbose:
                        print("Duplicate initial namespace id '%s'" % namespace_id, file=self.error_file, flush=True)
                else:
                    self.namespace_ids[namespace_id] = namespace_prefix
            else:
                if self.verbose:
                    print("Ignoring initial namespace label '%s'" % namespace_row[kr.label_column_idx], file=self.error_file, flush=True)

        return namespace_line_count
        
    def write_namespaces(self, ew: KgtkWriter):
        # Append the namespaces to the output file.
        n_id: str
        for n_id in sorted(self.namespace_ids.keys()):
            self.write_row(ew, n_id, self.prefix_expansion_label, '"' + self.namespace_ids[n_id] + '"')

    def parse(self, line: str, line_number: int)->typing.Tuple[typing.List[str], bool]:
        m: typing.Optional[typing.Match] = self.ROW_RE.match(line)
        if m is None:
            if self.verbose:
                print("Line %d: not parsed.\n%s" % (line_number, line), file=self.error_file, flush=True)
            return [ ], False
        return [m.group("node1"), m.group("label"), m.group("node2")], True

    def process(self):
        if self.verbose:
            print("Opening output file %s" % str(self.output_file_path), file=self.error_file, flush=True)
        # Open the output file.
        ew: KgtkWriter = KgtkWriter.open(self.COLUMN_NAMES,
                                         self.output_file_path,
                                         mode=KgtkWriter.Mode.EDGE,
                                         require_all_columns=False,
                                         prohibit_extra_columns=True,
                                         fill_missing_columns=False,
                                         gzip_in_parallel=False,
                                         verbose=self.verbose,
                                         very_verbose=self.very_verbose)

        rw: typing.Optional[KgtkWriter] = None
        if self.reject_file_path is not None:
            if self.verbose:
                print("Opening reject file %s" % str(self.reject_file_path), file=self.error_file, flush=True)
            # Open the reject file.
            rw: KgtkWriter = KgtkWriter.open(self.COLUMN_NAMES,
                                             self.reject_file_path,
                                             mode=KgtkWriter.Mode.NONE,
                                             require_all_columns=False,
                                             prohibit_extra_columns=True,
                                             fill_missing_columns=False,
                                             gzip_in_parallel=False,
                                             verbose=self.verbose,
                                             very_verbose=self.very_verbose)

        input_line_count: int = 0
        reject_line_count: int = 0
        
        namespace_line_count: int = self.get_initial_namespaces()
            
        # Open the input file.
        if self.verbose:
            print("Opening the input file: %s" % self.input_file_path, file=self.error_file, flush=True)
        with open(self.input_file_path, newline='') as infile:
            line: str
            for line in infile:
                input_line_count += 1

                row: typing.List[str]
                valid: bool
                row, valid = self.parse(line, input_line_count)
                if not valid:
                    if rw is not None:
                        rw.write(row)
                    reject_line_count += 1
                    continue

                node1: str
                ok_1: bool
                node1, ok_1 = self.convert(row[0], input_line_count, ew)

                label: str
                ok_2: bool
                label, ok_2 = self.convert(row[1], input_line_count, ew)

                node2: str
                ok_3: bool
                node2, ok_3 = self.convert(row[2], input_line_count, ew)

                if ok_1 and ok_2 and ok_3:
                    self.write_row(ew, node1, label, node2)
                else:
                    if rw is not None:
                        rw.write(row)
                    reject_line_count += 1

        # Append the namespaces to the output file:
        self.write_namespaces(ew)

        if self.verbose:
            print("Processed %d known namespaces." % (namespace_line_count), file=self.error_file, flush=True)
            print("Processed %d records." % (input_line_count), file=self.error_file, flush=True)
            print("Rejected %d records." % (reject_line_count), file=self.error_file, flush=True)
            print("Wrote %d records." % (self.output_line_count), file=self.error_file, flush=True)
        
        if ew is not None:
            ew.close()
            
        if rw is not None:
            rw.close()
            
    @classmethod
    def add_arguments(cls, parser: ArgumentParser):

        parser.add_argument(      "--namespace-id-prefix", dest="namespace_id_prefix",
                                  help="The prefix used to generate new namespaces. (default=%(default)s).",
                                  default=cls.DEFAULT_NAMESPACE_ID_PREFIX)
    
        parser.add_argument(      "--namespace-id-counter", dest="namespace_id_counter",
                                  help="The counter used to generate new namespaces. (default=%(default)s).",
                                  type=int, default=cls.DEFAULT_NAMESPACE_ID_COUNTER)
    
        parser.add_argument(      "--allow-lax-uri", dest="allow_lax_uri",
                                  help="Allow URIs that don't begin with a http:// or https://. (default=%(default)s).",
                                  type=optional_bool, nargs='?', const=True, default=cls.DEFAULT_ALLOW_LAX_URI)

        parser.add_argument(      "--local-namespace-prefix", dest="local_namespace_prefix",
                                  help="The namespace prefix for blank nodes. (default=%(default)s).",
                                  default=cls.DEFAULT_LOCAL_NAMESPACE_PREFIX)

        parser.add_argument(      "--local-namespace-use-uuid", dest="local_namespace_use_uuid",
                                  help="Generate a UUID for the local namespace. (default=%(default)s).",
                                  type=optional_bool, nargs='?', const=True, default=cls.DEFAULT_LOCAL_NAMESPACE_USE_UUID)

        parser.add_argument(      "--prefix-expansion-label", dest="prefix_expansion_label",
                                  help="The label for prefix expansions in the namespace file. (default=%(default)s).",
                                  default=cls.DEFAULT_PREFIX_EXPANSION)
    
        parser.add_argument(      "--structured-value-label", dest="structured_value_label",
                                  help="The label for value records for ntriple structured literals. (default=%(default)s).",
                                  default=cls.DEFAULT_STRUCTURED_VALUE)
    
        parser.add_argument(      "--structured-uri-label", dest="structured_uri_label",
                                  help="The label for URI records for ntriple structured literals. (default=%(default)s).",
                                  default=cls.DEFAULT_STRUCTURED_URI)
    
        parser.add_argument(      "--newnode-prefix", dest="newnode_prefix",
                                  help="The prefix used to generate new nodes for ntriple structured literals. (default=%(default)s).",
                                  default=cls.DEFAULT_NEWNODE_PREFIX)
    
        parser.add_argument(      "--newnode-counter", dest="newnode_counter",
                                  help="The counter used to generate new nodes for ntriple structured literals. (default=%(default)s).",
                                  type=int, default=cls.DEFAULT_NEWNODE_COUNTER)
    
        parser.add_argument(      "--build-id", dest="build_id",
                                  help="Build id values in an id column. (default=%(default)s).",
                                  type=optional_bool, nargs='?', const=True, default=cls.DEFAULT_BUILD_ID)

def main():
    """
    Test the KGTK implode processor.
    """
    parser: ArgumentParser = ArgumentParser()

    parser.add_argument(dest="input_file_path", help="The KGTK file with the input data. (default=%(default)s)", type=Path, nargs="?", default="-")

    parser.add_argument("-o", "--output-file", dest="output_file_path", help="The KGTK file to write (default=%(default)s).", type=Path, default="-")
    
    parser.add_argument(      "--reject-file", dest="reject_file_path", help="The KGTK file into which to write rejected records. (default=%(default)s).",
                              type=Path, default=None)
    
    parser.add_argument(      "--namespace-file", dest="namespace_file_path", help="The KGTK file with known namespaces. (default=%(default)s).",
                              type=Path, default=None)
    

    KgtkNtriples.add_arguments(parser)
    KgtkIdBuilderOptions.add_arguments(parser)
    KgtkReader.add_debug_arguments(parser)

    args: Namespace = parser.parse_args()

    error_file: typing.TextIO = sys.stdout if args.errors_to_stdout else sys.stderr

    # Build the option structures.                                                                                                                          
    idbuilder_options: KgtkIdBuilderOptions = KgtkIdBuilderOptions.from_args(args)

   # Show the final option structures for debugging and documentation.                                                                                             
    if args.show_options:
        print("input: %s" % str(args.input_file_path), file=error_file, flush=True)
        print("--output-file=%s" % str(args.output_file_path), file=error_file, flush=True)
        # TODO: show ifempty-specific options.
        if args.reject_file_path is not None:
            print("--reject-file=%s" % str(args.reject_file_path), file=error_file, flush=True)
        if args.namespace_file_path is not None:
            print("--namespace-file=%s" % str(args.namespace_file_path), file=error_file, flush=True)
        print("--namespace-id-prefix %s" % args.namespace_id_prefix, file=error_file, flush=True)
        print("--namespace-id-counter %s" % args.namespace_id_counter, file=error_file, flush=True)
        print("--allow-lax-uri %s" % args.allow_lax_uri, file=error_file, flush=True)
        print("--local-namespace-prefix %s" % args.local_namespace_prefix, file=error_file, flush=True)
        print("--local-namespace-use-uuid %s" % args.local_namespace_use_uuid, file=error_file, flush=True)
        print("--prefix-expansion-label %s" % args.prefix_expansion_label, file=error_file, flush=True)
        print("--structured-value-label %s" % args.structured_value_label, file=error_file, flush=True)
        print("--structured-uri-label %s" % args.structured_uri_label, file=error_file, flush=True)
        print("--newnode-prefix %s" % args.newnode_prefix, file=error_file, flush=True)
        print("--newnode-counter %s" % args.newnode_counter, file=error_file, flush=True)
        print("--build-id=%s" % str(args.build_id), file=error_file, flush=True)

        idbuilder_options.show(out=error_file)

    kn: KgtkNtriples = KgtkNtriples(
        input_file_path=args.input_file_path,
        output_file_path=args.output_file_path,
        reject_file_path=args.reject_file_path,
        namespace_file_path=args.namespace_file_path,
        namespace_id_prefix=args.namespace_id_prefix,
        namespace_id_counter=args.namespace_id_counter,
        newnode_prefix=args.newnode_prefix,
        newnode_counter=args.newnode_counter,
        allow_lax_uri=args.allow_lax_uri,
        local_namespace_prefix=args.local_namespace_prefix,
        local_namespace_use_uuid=args.local_namespace_use_uuid,
        prefix_expansion_label=args.prefix_expansion_label,
        structured_value_label=args.structured_value_label,
        structured_uri_label=args.structured_uri_label,
        build_id=args.build_id,
        idbuilder_options=idbuilder_options,
        error_file=error_file,
        verbose=args.verbose,
        very_verbose=args.very_verbose)

    kn.process()
    
if __name__ == "__main__":
    main()
