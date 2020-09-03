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
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderMode, KgtkReaderOptions
from kgtk.io.kgtkwriter import KgtkWriter
from kgtk.reshape.kgtkidbuilder import KgtkIdBuilder, KgtkIdBuilderOptions
from kgtk.utils.argparsehelpers import optional_bool
from kgtk.value.kgtkvalue import KgtkValue, KgtkValueFields
from kgtk.value.kgtkvalueoptions import KgtkValueOptions, DEFAULT_KGTK_VALUE_OPTIONS

@attr.s(slots=True, frozen=False)
class KgtkNtriples(KgtkFormat):
    # Class attributes:
    DEFAULT_PREFIX_EXPANSION: str = "prefix_expansion"
    DEFAULT_STRUCTURED_VALUE: str = "kgtk:structured_value"
    DEFAULT_STRUCTURED_URI: str = "kgtk:structured_uri"
    DEFAULT_NAMESPACE_ID_PREFIX: str = "n"
    DEFAULT_NAMESPACE_ID_COUNTER: int = 1
    DEFAULT_NAMESPACE_ID_ZFILL: int = 0
    DEFAULT_NAMESPACE_ID_USE_UUID: bool = False
    DEFAULT_OUTPUT_ONLY_USED_NAMESPACES: bool = True
    DEFAULT_NEWNODE_PREFIX: str = "kgtk:node"
    DEFAULT_NEWNODE_COUNTER: int = 1
    DEFAULT_NEWNODE_ZFILL: int = 0
    DEFAULT_NEWNODE_USE_UUID: bool = False
    DEFAULT_LOCAL_NAMESPACE_PREFIX: str = "X"
    DEFAULT_LOCAL_NAMESPACE_USE_UUID: bool = True
    DEFAULT_ALLOW_LAX_URI: bool = True
    DEFAULT_BUILD_ID: bool = False
    DEFAULT_ESCAPE_PIPES: bool = True
    DEFAULT_VALIDATE: bool = False

    COLUMN_NAMES: typing.List[str] = [KgtkFormat.NODE1, KgtkFormat.LABEL, KgtkFormat.NODE2]
    
    # The following lexical analysis is based on:
    # https://docs.python.org/3/reference/lexical_analysis.html

    # The long integer suffix was part of Python 2.  It was dropped in Python 3.
    long_suffix_pat: str = r'[lL]'

    plus_or_minus_pat: str = r'[-+]'

    # Integer literals.
    #
    # Decimal integers, allowing leading zeros.
    digit_pat: str = r'[0-9]'
    decinteger_pat: str = r'(?:{digit}(?:_?{digit})*{long_suffix}?)'.format(digit=digit_pat,
                                                                            long_suffix=long_suffix_pat)
    bindigit_pat: str = r'[01]'
    bininteger_pat: str = r'(?:0[bB](":_?{bindigit})+{long_suffix})'.format(bindigit=bindigit_pat,
                                                                            long_suffix=long_suffix_pat)
    octdigit_pat: str = r'[0-7]'
    octinteger_pat: str = r'(?:0[oO](":_?{octdigit})+{long_suffix})'.format(octdigit=octdigit_pat,
                                                                            long_suffix=long_suffix_pat)
    hexdigit_pat: str = r'[0-7a-fA-F]'
    hexinteger_pat: str = r'(?:0[xX](":_?{hexdigit})+{long_suffix})'.format(hexdigit=hexdigit_pat,
                                                                            long_suffix=long_suffix_pat)
     
    integer_pat: str = r'(?:{decinteger}|{bininteger}|{octinteger}|{hexinteger})'.format(decinteger=decinteger_pat,
                                                                                         bininteger=bininteger_pat,
                                                                                         octinteger=octinteger_pat,
                                                                                         hexinteger=hexinteger_pat)

    # Floating point literals.
    digitpart_pat: str = r'(?:{digit}(?:_?{digit})*)'.format(digit=digit_pat)
    fraction_pat: str = r'(?:\.{digitpart})'.format(digitpart=digitpart_pat)
    pointfloat_pat: str = r'(?:{digitpart}?{fraction})|(?:{digitpart}\.)'.format(digitpart=digitpart_pat,
                                                                                 fraction=fraction_pat)
    exponent_pat: str = r'(?:[eE]{plus_or_minus}?{digitpart})'.format(plus_or_minus=plus_or_minus_pat,
                                                                      digitpart=digitpart_pat)
    exponentfloat_pat: str = r'(?:{digitpart}|{pointfloat}){exponent}'.format(digitpart=digitpart_pat,
                                                                              pointfloat=pointfloat_pat,
                                                                              exponent=exponent_pat)
    floatnumber_pat: str = r'(?:{pointfloat}|{exponentfloat})'.format(pointfloat=pointfloat_pat,
                                                                      exponentfloat=exponentfloat_pat)

    # Imaginary literals.
    imagnumber_pat: str = r'(?:{floatnumber}|{digitpart})[jJ]'.format(floatnumber=floatnumber_pat,
                                                                      digitpart=digitpart_pat)

    # Numeric literals.
    numeric_pat: str = r'(?:{plus_or_minus}?(?:{integer}|{floatnumber}|{imagnumber}))'.format(plus_or_minus=plus_or_minus_pat,
                                                                                              integer=integer_pat,
                                                                                              floatnumber=floatnumber_pat,
                                                                                              imagnumber=imagnumber_pat)

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
    BLANK_NODE_PAT: str = r'(?:_:[0-9a-zA-Z_]+)'

    # Double quoted strings with backslash escapes.
    STRING_PAT: str = r'"(?:[^\\]|(?:\\.))*"'

    STRUCTURED_VALUE_PAT: str = r'(?:{string}(?:\^\^{uri})?)'.format(string=STRING_PAT, uri=URI_PAT)
    FIELD_PAT: str = r'(?:{uri}|{blank_node}|{structured_value}|{numeric})'.format(uri=URI_PAT,
                                                                                   blank_node=BLANK_NODE_PAT,
                                                                                   structured_value=STRUCTURED_VALUE_PAT,
                                                                                   numeric=numeric_pat,
    )
    ROW_PAT: str = r'(?P<node1>{field})\s(?P<label>{field})\s(?P<node2>{field})\s\.'.format(field=FIELD_PAT)
    ROW_RE: typing.Pattern = re.compile(r'^' + ROW_PAT + r'$')

    SLASH_HASH_PAT: str = r'/|#'
    SLASH_HASH_RE: typing.Pattern = re.compile(SLASH_HASH_PAT)

    # Instance attributes:

    # TODO: write a validator:
    input_file_paths: typing.List[Path] = attr.ib()

    output_file_path: Path = attr.ib(validator=attr.validators.instance_of(Path))

    reject_file_path: typing.Optional[Path] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Path)))

    namespace_file_path: typing.Optional[Path] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Path)))

    updated_namespace_file_path: typing.Optional[Path] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(Path)))

    reader_options: KgtkReaderOptions = attr.ib(validator=attr.validators.instance_of(KgtkReaderOptions))

    allow_lax_uri: bool = attr.ib(validator=attr.validators.instance_of(bool), default=DEFAULT_ALLOW_LAX_URI)

    local_namespace_prefix: str = attr.ib(validator=attr.validators.instance_of(str), default=DEFAULT_LOCAL_NAMESPACE_PREFIX)
    local_namespace_use_uuid: bool = attr.ib(validator=attr.validators.instance_of(bool), default=DEFAULT_LOCAL_NAMESPACE_USE_UUID)

    namespace_id_prefix: str = attr.ib(validator=attr.validators.instance_of(str), default=DEFAULT_NAMESPACE_ID_PREFIX)
    namespace_id_counter: int = attr.ib(validator=attr.validators.instance_of(int), default=DEFAULT_NAMESPACE_ID_COUNTER)
    namespace_id_zfill: int = attr.ib(validator=attr.validators.instance_of(int), default=DEFAULT_NAMESPACE_ID_ZFILL)
    namespace_id_use_uuid: bool = attr.ib(validator=attr.validators.instance_of(bool), default=DEFAULT_NAMESPACE_ID_USE_UUID)
    output_only_used_namespaces: bool = attr.ib(validator=attr.validators.instance_of(bool), default=DEFAULT_LOCAL_NAMESPACE_USE_UUID)

    prefix_expansion_label: str = attr.ib(validator=attr.validators.instance_of(str), default=DEFAULT_PREFIX_EXPANSION)

    structured_value_label: str = attr.ib(validator=attr.validators.instance_of(str), default=DEFAULT_STRUCTURED_VALUE)
    structured_uri_label: str = attr.ib(validator=attr.validators.instance_of(str), default=DEFAULT_STRUCTURED_URI)

    newnode_prefix: str = attr.ib(validator=attr.validators.instance_of(str), default=DEFAULT_NEWNODE_PREFIX)
    newnode_counter: int = attr.ib(validator=attr.validators.instance_of(int), default=DEFAULT_NEWNODE_COUNTER)
    newnode_zfill: int = attr.ib(validator=attr.validators.instance_of(int), default=DEFAULT_NEWNODE_ZFILL)
    newnode_use_uuid: bool = attr.ib(validator=attr.validators.instance_of(bool), default=DEFAULT_NEWNODE_USE_UUID)

    build_id: bool = attr.ib(validator=attr.validators.instance_of(bool), default=DEFAULT_BUILD_ID)
    idbuilder_options: typing.Optional[KgtkIdBuilderOptions] = attr.ib(default=None)
    idbuilder: typing.Optional[KgtkIdBuilder] = attr.ib(default=None)

    validate: bool = attr.ib(validator=attr.validators.instance_of(bool), default=DEFAULT_VALIDATE)
    value_options: KgtkValueOptions = attr.ib(validator=attr.validators.instance_of(KgtkValueOptions), default=DEFAULT_KGTK_VALUE_OPTIONS)

    override_uuid: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)

    error_file: typing.TextIO = attr.ib(default=sys.stderr)
    verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    very_verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    local_namespace_uuid: str = attr.ib(default="")

    namespace_prefixes: typing.MutableMapping[str, str] = attr.ib(factory=dict)
    namespace_ids: typing.MutableMapping[str, str] = attr.ib(factory=dict)
    used_namespaces: typing.Set[str] = attr.ib(factory=set)

    escape_pipes: bool = attr.ib(validator=attr.validators.instance_of(bool), default=DEFAULT_ESCAPE_PIPES)

    output_line_count: int = attr.ib(default=0)

    def write_row(self, ew: KgtkWriter, node1: str, label: str, node2: str):
        output_row: typing.List[str] = [ node1, label, node2]
        if self.idbuilder is None:
            ew.write(output_row)
        else:
            ew.write(self.idbuilder.build(output_row, self.output_line_count))
        self.output_line_count += 1

    def convert_blank_node(self, item: str)->typing.Tuple[str, bool]:
        body: str = item[1:] # Strip the leading underscore, keep the colon.
        if self.local_namespace_use_uuid:
            return self.local_namespace_prefix + self.local_namespace_uuid + body, True
        else:
            return self.local_namespace_prefix + body, True

    def convert_uri(self, item: str, line_number: int)->typing.Tuple[str, bool]:
        body: str = item[1:-1] # Strip off the enclosing brackets.

        # First, check for an exact match for the body:
        namespace_id: str
        if body in self.namespace_prefixes:
            # Yes, this prefix exactly matches the body.
            namespace_id = self.namespace_prefixes[body]

            if self.output_only_used_namespaces:
                self.used_namespaces.add(namespace_id)

            # Return the namespace-prefixed URI:
            return namespace_id + ":", True

        # Move past "http://" or "https://":
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

        # Build a left-to-right list of slash- or hash-terminated sections:
        matches: typing.List[int] = [ ]
        m: typing.Match
        for m in self.SLASH_HASH_RE.finditer(body, after_slashslash):
            matches.append(m.end(0))

        # Search right-to-left for the longest match:
        matches.reverse()
        namespace_prefix: str
        suffix: str
        match_end: int
        for match_end in matches:
            namespace_prefix = body[:match_end]
            suffix = body[match_end:]
            if namespace_prefix in self.namespace_prefixes:
                # We have a winner.
                namespace_id = self.namespace_prefixes[namespace_prefix]

                if self.output_only_used_namespaces:
                    self.used_namespaces.add(namespace_id)

                # Return the namespace-prefixed URI:
                return namespace_id + ":" + suffix, True

        # Take the longest possible section, which is now first in the list:
        if len(matches) > 0:
            match_end = matches[0]
            namespace_prefix = body[:match_end]
            suffix = body[match_end:]
        else:
            # Take the entire body:
            namespace_prefix = body
            suffix = ""

        # Build a non-colliding namespace ID.
        while True:
            namespace_id = self.namespace_id_prefix
            if self.namespace_id_use_uuid:
                namespace_id += self.local_namespace_uuid + "-"
            namespace_id += str(self.namespace_id_counter).zfill(self.namespace_id_zfill)
            self.namespace_id_counter += 1
            if namespace_id not in self.namespace_ids:
                # Save the namespace ID for later reuse:
                self.namespace_ids[namespace_id] = namespace_prefix
                self.namespace_prefixes[namespace_prefix] = namespace_id

                if self.output_only_used_namespaces:
                    self.used_namespaces.add(namespace_id)

                # Return the namespace-prefixed URI:
                return namespace_id + ":" + suffix, True

    def escape_pipe(self, item: str)->str:
        # ensure that vertical bars (pipes) are escaped.
        if self.escape_pipes:
            return item.replace('|', '\\|')
        else:
            return item

    def convert_string(self, item: str, line_number: int)->typing.Tuple[str, bool]:
        # Convert this to a KGTK string.
        #
        # Our parser guarantees that double quoted strings use proper
        # escapes... except for vertical bars (pipes).  We have extra work to do to
        # ensure that vertical bars (pipes) are escaped.
        return self.escape_pipe(item), True
 
    def generate_new_node_symbol(self)->str:
        new_node_symbol: str = self.newnode_prefix
        if self.newnode_use_uuid:
            new_node_symbol += self.local_namespace_uuid + "-"
        new_node_symbol += str(self.newnode_counter).zfill(self.newnode_zfill)
        self.newnode_counter += 1
        return new_node_symbol
    
    def convert_boolean(self, item: str, value: str, line_number: int)->typing.Tuple[str, bool]:
        if value == 'true' or value == '1':
            return KgtkFormat.TRUE_SYMBOL, True
        elif value == 'false' or value == '0':
            return KgtkFormat.FALSE_SYMBOL, True
        else:
            if self.verbose:
                print("Line %d: invalid boolean item '%s'>" % (line_number, item), file=self.error_file, flush=True)
            return item, False
        

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
        elif uri == '<http://www.w3.org/2001/XMLSchema#boolean>':
            # Convert this to a KGTK boolean:
            return self.convert_boolean(item, string[1:-1], line_number)

        elif uri == '<http://www.w3.org/2001/XMLSchema#dateTime>':
            # Convert this to a KGTK date-and-time:
            #
            # Note: the W3C XML Schema standard allows the now obsolete
            # end-of-day time "24:00:00".
            return '^' + string[1:-1], True

        # TODO: the "date" schema
        # Problem:  it allows timezone offsets after dates without times!

        converted_uri: str
        valid: bool
        converted_uri, valid = self.convert_uri(uri, line_number)
        if not valid:
            return item, False

        new_node_symbol: str = self.generate_new_node_symbol()
        self.write_row(ew, new_node_symbol, self.structured_value_label, string)
        self.write_row(ew, new_node_symbol, self.structured_uri_label, converted_uri)

        return new_node_symbol, True

    def convert_numeric(self, item: str, line_number: int, ew: KgtkWriter)->typing.Tuple[str, bool]:
        return item, True

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
        elif item[0] in "+-0123456789.":
            return self.convert_numeric(item, line_number, ew)

        if self.verbose:
            print("Line %d: unrecognized item '%s'" %(line_number, item), file=self.error_file, flush=True)

        return item, False
    
    def convert_and_validate(self, item: str, line_number: int, ew: KgtkWriter)->typing.Tuple[str, bool]:
        result: str
        is_ok: bool
        result, is_ok = self.convert(item, line_number, ew)

        # Just a little bit of paranoia here regarding tabs and ends-of-lines:
        #
        # TODO: perform these checks (and repairs!) in KgtkValue.
        if "\t" in result:
            result = result.replace("\t", "\\t")
        if "\n" in result:
            result = result.replace("\n", "\\n")
        if "\r" in result:
            result = result.replace("\r", "\\r")

        if is_ok and self.validate:
            kv: KgtkValue = KgtkValue(result, options=self.value_options)
            if not kv.validate():
                if self.verbose:
                    print("Input line %d: imported value '%s' (from '%s') is invalid." % (line_number, result, item),
                          file=self.error_file, flush=True)
                return result, False
        return result, True
            

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
                                          options=self.reader_options,
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
        
    def write_namespaces_to_output(self, ew: KgtkWriter, count_records: bool = True):
        # Append the namespaces to the output file.
        namespace_id: str
        for namespace_id in sorted(self.namespace_ids.keys()):
            if self.output_only_used_namespaces:
                if namespace_id in self.used_namespaces:
                    self.write_row(ew, namespace_id, self.prefix_expansion_label, '"' + self.namespace_ids[namespace_id] + '"')
            else:
                self.write_row(ew, namespace_id, self.prefix_expansion_label, '"' + self.namespace_ids[namespace_id] + '"')

    def write_updated_namespace_file(self):
        # Is there an updated namespaces file?
        if self.updated_namespace_file_path is None:
            return

        if self.verbose:
            print("Opening updated namespaces file %s" % str(self.updated_namespace_file_path), file=self.error_file, flush=True)
        # Open the updated namespaces file.
        un: KgtkWriter = KgtkWriter.open(self.COLUMN_NAMES,
                                         self.updated_namespace_file_path,
                                         mode=KgtkWriter.Mode.EDGE,
                                         require_all_columns=True,
                                         prohibit_extra_columns=True,
                                         fill_missing_columns=False,
                                         gzip_in_parallel=False,
                                         verbose=self.verbose,
                                         very_verbose=self.very_verbose)
        namespace_id: str
        for namespace_id in sorted(self.namespace_ids.keys()):
            un.write([namespace_id, self.prefix_expansion_label, '"' + self.namespace_ids[namespace_id] + '"'])
        un.close()


    def save_namespaces(self, ew: KgtkWriter):
        self.write_namespaces_to_output(ew)
        self.write_updated_namespace_file()

    def parse(self, line: str, line_number: int)->typing.Tuple[typing.List[str], bool]:
        m: typing.Optional[typing.Match] = self.ROW_RE.match(line)
        if m is None:
            if self.verbose:
                print("Line %d: not parsed.\n%s" % (line_number, line), file=self.error_file, flush=True)
            return [ ], False
        return [m.group("node1"), m.group("label"), m.group("node2")], True


    def process(self):
        output_column_names: typing.List[str]
        if self.build_id and self.idbuilder_options is not None:
            self.idbuilder = KgtkIdBuilder.from_column_names(self.COLUMN_NAMES, self.idbuilder_options)
            output_column_names = self.idbuilder.column_names
        else:
            output_column_names = self.COLUMN_NAMES

        if self.verbose:
            print("Opening output file %s" % str(self.output_file_path), file=self.error_file, flush=True)
        # Open the output file.
        ew: KgtkWriter = KgtkWriter.open(output_column_names,
                                         self.output_file_path,
                                         mode=KgtkWriter.Mode.EDGE,
                                         require_all_columns=False,
                                         prohibit_extra_columns=True,
                                         fill_missing_columns=True,
                                         gzip_in_parallel=False,
                                         verbose=self.verbose,
                                         very_verbose=self.very_verbose)

        rw: typing.Optional[typing.TextIO] = None
        if self.reject_file_path is not None:
            if self.verbose:
                print("Opening reject file %s" % str(self.reject_file_path), file=self.error_file, flush=True)
            # Open the reject file. Since the input data is not in KGTK format,
            # we use an ordinary file here.
            if str(self.reject_file_path) == "-":
                rw = sys.stdout
            else:
                rw = open(self.reject_file_path, "wt")


        total_input_line_count: int = 0
        reject_line_count: int = 0
        
        namespace_line_count: int = self.get_initial_namespaces()
            
        input_file_path: str
        for input_file_path in self.input_file_paths:
            input_line_count: int = 0
            
            if self.local_namespace_use_uuid or self.namespace_id_use_uuid or self.newnode_use_uuid:
                if self.override_uuid is not None:
                    self.local_namespace_uuid = self.override_uuid # for debugging
                else:
                    # Generate a new local namespace UUID.
                    self.local_namespace_uuid = shortuuid.uuid()

            # Open the input file.
            if self.verbose:
                print("Opening the input file: %s" % input_file_path, file=self.error_file, flush=True)
            infile: typing.TextIO
            if str(input_file_path) == "-":
                infile = sys.stdin
            else:
                infile = open(input_file_path, 'rt') 

            line: str
            for line in infile:
                input_line_count += 1
                total_input_line_count += 1

                row: typing.List[str]
                valid: bool
                row, valid = self.parse(line, input_line_count)
                if not valid:
                    if rw is not None:
                        rw.write(line)
                    reject_line_count += 1
                    continue

                node1: str
                ok_1: bool
                node1, ok_1 = self.convert_and_validate(row[0], input_line_count, ew)

                label: str
                ok_2: bool
                label, ok_2 = self.convert_and_validate(row[1], input_line_count, ew)

                node2: str
                ok_3: bool
                node2, ok_3 = self.convert_and_validate(row[2], input_line_count, ew)

                if ok_1 and ok_2 and ok_3:
                    self.write_row(ew, node1, label, node2)
                else:
                    if rw is not None:
                        rw.write(line)
                    reject_line_count += 1

            if input_file_path != "-":
                infile.close()


                self.save_namespaces(ew)

        if self.verbose:
            print("Processed %d known namespaces." % (namespace_line_count), file=self.error_file, flush=True)
            print("Processed %d records." % (total_input_line_count), file=self.error_file, flush=True)
            print("Rejected %d records." % (reject_line_count), file=self.error_file, flush=True)
            print("Wrote %d records." % (self.output_line_count), file=self.error_file, flush=True)
        
        if ew is not None:
            ew.close()
            
        if rw is not None and self.reject_file_path is not None and self.reject_file_path != "-":
            rw.close()
            
    @classmethod
    def add_arguments(cls, parser: ArgumentParser):

        parser.add_argument(      "--namespace-id-prefix", dest="namespace_id_prefix",
                                  help="The prefix used to generate new namespaces. (default=%(default)s).",
                                  default=cls.DEFAULT_NAMESPACE_ID_PREFIX)
    
        parser.add_argument(      "--namespace-id-use-uuid", dest="namespace_id_use_uuid",
                                  help="Use the local namespace UUID when generating namespaces. " +
                                  "When there are multiple input files, each input file gets its own UUID. (default=%(default)s).",
                                  type=optional_bool, nargs='?', const=True, default=cls.DEFAULT_NAMESPACE_ID_USE_UUID)

        parser.add_argument(      "--namespace-id-counter", dest="namespace_id_counter",
                                  help="The counter used to generate new namespaces. (default=%(default)s).",
                                  type=int, default=cls.DEFAULT_NAMESPACE_ID_COUNTER)
    
        parser.add_argument(      "--namespace-id-zfill", dest="namespace_id_zfill",
                                  help="The width of the counter used to generate new namespaces. (default=%(default)s).",
                                  type=int, default=cls.DEFAULT_NAMESPACE_ID_ZFILL)
    
        parser.add_argument(      "--output-only-used-namespaces", dest="output_only_used_namespaces",
                                  help="Write only used namespaces to the output file. (default=%(default)s).",
                                  type=optional_bool, nargs='?', const=True, default=cls.DEFAULT_OUTPUT_ONLY_USED_NAMESPACES)

        parser.add_argument(      "--allow-lax-uri", dest="allow_lax_uri",
                                  help="Allow URIs that don't begin with a http:// or https://. (default=%(default)s).",
                                  type=optional_bool, nargs='?', const=True, default=cls.DEFAULT_ALLOW_LAX_URI)

        parser.add_argument(      "--local-namespace-prefix", dest="local_namespace_prefix",
                                  help="The namespace prefix for blank nodes. (default=%(default)s).",
                                  default=cls.DEFAULT_LOCAL_NAMESPACE_PREFIX)

        parser.add_argument(      "--local-namespace-use-uuid", dest="local_namespace_use_uuid",
                                  help="Generate a UUID for the local namespace. " +
                                  "When there are multiple input files, each input file gets its own UUID. (default=%(default)s).",
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
    
        parser.add_argument(      "--newnode-use-uuid", dest="newnode_use_uuid",
                                  help="Use the local namespace UUID when generating new nodes for ntriple structured literals. " +
                                  "When there are multiple input files, each input file gets its own UUID. (default=%(default)s).",
                                  type=optional_bool, nargs='?', const=True, default=cls.DEFAULT_NEWNODE_USE_UUID)

        parser.add_argument(      "--newnode-counter", dest="newnode_counter",
                                  help="The counter used to generate new nodes for ntriple structured literals. (default=%(default)s).",
                                  type=int, default=cls.DEFAULT_NEWNODE_COUNTER)
    
        parser.add_argument(      "--newnode-zfill", dest="newnode_zfill",
                                  help="The width of the counter used to generate new nodes for ntriple structured literals. (default=%(default)s).",
                                  type=int, default=cls.DEFAULT_NEWNODE_ZFILL)
    
        parser.add_argument(      "--build-id", dest="build_id",
                                  help="Build id values in an id column. (default=%(default)s).",
                                  type=optional_bool, nargs='?', const=True, default=cls.DEFAULT_BUILD_ID)

        parser.add_argument(      "--escape-pipes", dest="escape_pipes",
                                  help="When true, input pipe characters (|) need to be escaped (\\|) per KGTK file format. (default=%(default)s).",
                                  type=optional_bool, nargs='?', const=True, default=cls.DEFAULT_ESCAPE_PIPES)

        parser.add_argument(      "--validate", dest="validate",
                                  help="When true, validate that the result fields are good KGTK file format. (default=%(default)s).",
                                  type=optional_bool, nargs='?', const=True, default=cls.DEFAULT_VALIDATE)

        parser.add_argument(      "--override-uuid", dest="override_uuid",
                                  help="When specified, override UUID generation for debugging. (default=%(default)s).",
                                  default=None)

def main():
    """
    Test the KGTK ntriples importer.
    """
    parser: ArgumentParser = ArgumentParser()

    parser.add_argument("-i", "--input-files", dest="input_file_paths", nargs='*',
                        help="The file(s) with the input ntriples data. (default=%(default)s)", type=Path, default="-")

    parser.add_argument("-o", "--output-file", dest="output_file_path", help="The KGTK file to write (default=%(default)s).", type=Path, default="-")
    
    parser.add_argument(      "--reject-file", dest="reject_file_path", help="The KGTK file into which to write rejected records. (default=%(default)s).",
                              type=Path, default=None)
    
    parser.add_argument(      "--namespace-file", dest="namespace_file_path", help="The KGTK file with known namespaces. (default=%(default)s).",
                              type=Path, default=None)
    
    parser.add_argument(      "--updated-namespace-file", dest="updated_namespace_file_path",
                              help="An updated KGTK file with known namespaces. (default=%(default)s).",
                              type=Path, default=None)
    

    KgtkNtriples.add_arguments(parser)
    KgtkIdBuilderOptions.add_arguments(parser)
    KgtkReader.add_debug_arguments(parser)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, expert=True)
    KgtkValueOptions.add_arguments(parser)

    args: Namespace = parser.parse_args()

    error_file: typing.TextIO = sys.stdout if args.errors_to_stdout else sys.stderr

    # Build the option structures.                                                                                                                          
    idbuilder_options: KgtkIdBuilderOptions = KgtkIdBuilderOptions.from_args(args)
    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_args(args)
    value_options: KgtkValueOptions = KgtkValueOptions.from_args(args)

   # Show the final option structures for debugging and documentation.                                                                                             
    if args.show_options:
        print("--input-files %s" % " ".join([str(path) for  path in input_file_paths]), file=error_file, flush=True)
        print("--output-file=%s" % str(args.output_file_path), file=error_file, flush=True)
        # TODO: show ifempty-specific options.
        if args.reject_file_path is not None:
            print("--reject-file=%s" % str(args.reject_file_path), file=error_file, flush=True)
        if args.namespace_file_path is not None:
            print("--namespace-file=%s" % str(args.namespace_file_path), file=error_file, flush=True)
        if args.updated_namespace_file_path is not None:
            print("--updated-namespace-file=%s" % str(args.updated_namespace_file_path), file=error_file, flush=True)
        print("--namespace-id-prefix %s" % args.namespace_id_prefix, file=error_file, flush=True)
        print("--namespace-id-use-uuid %s" % str(args.namespace_id_use_uuid), file=error_file, flush=True)
        print("--namespace-id-counter %s" % str(args.namespace_id_counter), file=error_file, flush=True)
        print("--namespace-id-zfill %s" % str(args.namespace_id_zfill), file=error_file, flush=True)
        print("--output-only-used-namespaces %s" % str(args.output_only_used_namespaces), file=error_file, flush=True)
        print("--allow-lax-uri %s" % str(args.allow_lax_uri), file=error_file, flush=True)
        print("--local-namespace-prefix %s" % args.local_namespace_prefix, file=error_file, flush=True)
        print("--local-namespace-use-uuid %s" % str(args.local_namespace_use_uuid), file=error_file, flush=True)
        print("--prefix-expansion-label %s" % args.prefix_expansion_label, file=error_file, flush=True)
        print("--structured-value-label %s" % args.structured_value_label, file=error_file, flush=True)
        print("--structured-uri-label %s" % args.structured_uri_label, file=error_file, flush=True)
        print("--newnode-prefix %s" % args.newnode_prefix, file=error_file, flush=True)
        print("--newnode-use-uuid %s" % str(args.newnode_use_uuid), file=error_file, flush=True)
        print("--newnode-counter %s" % str(args.newnode_counter), file=error_file, flush=True)
        print("--newnode-zfill %s" % str(args.newnode_zfill), file=error_file, flush=True)
        print("--build-id=%s" % str(args.build_id), file=error_file, flush=True)
        print("--escape-pipes=%s" % str(args.escape_pipes), file=error_file, flush=True)
        print("--validate=%s" % str(args.validate), file=error_file, flush=True)
        if args.override_uuid is not None:
            print("--override_uuid=%s" % str(args.override_uuid), file=error_file, flush=True)            

        idbuilder_options.show(out=error_file)
        reader_options.show(out=error_file)
        value_options.show(out=error_file)

    kn: KgtkNtriples = KgtkNtriples(
        input_file_paths=args.input_file_paths,
        output_file_path=args.output_file_path,
        reject_file_path=args.reject_file_path,
        namespace_file_path=args.namespace_file_path,
        updated_namespace_file_path=args.updated_namespace_file_path,
        namespace_id_prefix=args.namespace_id_prefix,
        namespace_id_use_uuid=args.namespace_id_use_uuid,
        namespace_id_counter=args.namespace_id_counter,
        namespace_id_zfill=args.namespace_id_zfill,
        output_only_used_namespaces=args.output_only_used_namespaces,
        newnode_prefix=args.newnode_prefix,
        newnode_use_uuid=args.newnode_use_uuid,
        newnode_counter=args.newnode_counter,
        newnode_zfill=args.newnode_zfill,
        allow_lax_uri=args.allow_lax_uri,
        local_namespace_prefix=args.local_namespace_prefix,
        local_namespace_use_uuid=args.local_namespace_use_uuid,
        prefix_expansion_label=args.prefix_expansion_label,
        structured_value_label=args.structured_value_label,
        structured_uri_label=args.structured_uri_label,
        build_id=args.build_id,
        escape_pipes=args.escape_pipes,
        idbuilder_options=idbuilder_options,
        validate=args.validate,
        override_uuid=args.override_uuid,
        reader_options=reader_options,
        value_options=value_options,
        error_file=error_file,
        verbose=args.verbose,
        very_verbose=args.very_verbose)

    kn.process()
    
if __name__ == "__main__":
    main()
