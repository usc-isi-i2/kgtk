"""Import ntriples into KGTK format.

The W3C document on RDF 1.1 N-Triples is https://www.w3.org/TR/n-triples/.

The W3C document defines optional
comments that may appear after the full stop (".") at the end of a triple. COmments
begin with "#" (after optional white space) and continue ot the end of line or end of file.

At present, `kgtk import-ntriples` strips any comments found, with a summary count at the end
of processing. A more complex option would be to convert N-Triples comments into KGTK comments.


Issue #390: KGTK Needs More General Language Tags

According to the Wikipedia article on N-Triples, N-triples use RFC 3066
language tags. According to the Wikipedia article on IETF language tags,
RFC 3066 has been replaced by RFC 4646 and RFC 5646, with increasingly
more general structure.

According to the W3C document on RDF 1.1 N-triples, language tags are
defined by BCP 47, which references RFC 5646. The Wikipedia article appears
to be obsolete.

To support importing/exporting N-Triples properly, the KGTK specification and
implementation may need some extensions.


"""
from argparse import ArgumentParser, Namespace
import ast
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
    DEFAULT_BUILD_NEW_NAMESPACES: bool = True
    DEFAULT_NEWNODE_PREFIX: str = "kgtk:node"
    DEFAULT_NEWNODE_COUNTER: int = 1
    DEFAULT_NEWNODE_ZFILL: int = 0
    DEFAULT_NEWNODE_USE_UUID: bool = False
    DEFAULT_LOCAL_NAMESPACE_PREFIX: str = "X"
    DEFAULT_LOCAL_NAMESPACE_USE_UUID: bool = True
    DEFAULT_ALLOW_LAX_URI: bool = True
    DEFAULT_BUILD_ID: bool = False
    DEFAULT_VALIDATE: bool = False
    DEFAULT_ALLOW_UNKNOWN_DATATYPE_IRIS: bool = True
    DEFAULT_ALLOW_TURTLE_QUOTES: bool = False
    DEFAULT_ALLOW_LANG_STRING_DATATYPE: bool = False
    DEFAULT_SUMMARY: bool = False
    LANG_STRING_TAG_NONE: str = "-"
    DEFAULT_LANG_STRING_TAG: str = LANG_STRING_TAG_NONE
    DEFAULT_BUILD_DATATYPE_COLUMN: bool = False
    DEFAULT_DATATYPE_COLUMN_NAME: str = "datatype"

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
    STRING_PAT: str = r'(?:"(?:[^\\]|(?:\\.))*")'

    # Single quoted strings with backslash escapes are allowed in RDF Turtle format.
    TURTLE_STRING_PAT: str = r"(?:'(?:[^\\]|(?:\\.))*')"

    # Language tags are sequences of alphanumerics separated by dashes.
    LANGUAGE_TAG_PAT: str = r'(?:[0-9a-zA-Z]+(?:-[0-9a-zA-Z]+)*)'

    STRUCTURED_VALUE_PAT: str = r'(?:(?:{string}|{turtle_string})(?:(?:@{tag})|(?:\^\^{uri}))?)'.format(string=STRING_PAT,
                                                                                                        turtle_string=TURTLE_STRING_PAT,
                                                                                                        tag=LANGUAGE_TAG_PAT,
                                                                                                        uri=URI_PAT)
    FIELD_PAT: str = r'(?:{uri}|{blank_node}|{structured_value}|{numeric})'.format(uri=URI_PAT,
                                                                                   blank_node=BLANK_NODE_PAT,
                                                                                   structured_value=STRUCTURED_VALUE_PAT,
                                                                                   numeric=numeric_pat,
    )
    COMMENT_PAT: str = r'(?:#.*)?'
    ROW_PAT: str = r'\s*(?P<node1>{field})\s+(?P<label>{field})\s+(?P<node2>{field})\s+\.\s*(?P<comment>{comment})'.format(field=FIELD_PAT, comment=COMMENT_PAT)
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

    allow_unknown_datatype_iris: bool = attr.ib(validator=attr.validators.instance_of(bool), default=DEFAULT_ALLOW_UNKNOWN_DATATYPE_IRIS)

    allow_turtle_quotes: bool = attr.ib(validator=attr.validators.instance_of(bool), default=DEFAULT_ALLOW_TURTLE_QUOTES)

    allow_lang_string_datatype: bool = attr.ib(validator=attr.validators.instance_of(bool), default=DEFAULT_ALLOW_LANG_STRING_DATATYPE)
    lang_string_tag: str = attr.ib(validator=attr.validators.instance_of(str), default=DEFAULT_LANG_STRING_TAG)

    local_namespace_prefix: str = attr.ib(validator=attr.validators.instance_of(str), default=DEFAULT_LOCAL_NAMESPACE_PREFIX)
    local_namespace_use_uuid: bool = attr.ib(validator=attr.validators.instance_of(bool), default=DEFAULT_LOCAL_NAMESPACE_USE_UUID)

    namespace_id_prefix: str = attr.ib(validator=attr.validators.instance_of(str), default=DEFAULT_NAMESPACE_ID_PREFIX)
    namespace_id_counter: int = attr.ib(validator=attr.validators.instance_of(int), default=DEFAULT_NAMESPACE_ID_COUNTER)
    namespace_id_zfill: int = attr.ib(validator=attr.validators.instance_of(int), default=DEFAULT_NAMESPACE_ID_ZFILL)
    namespace_id_use_uuid: bool = attr.ib(validator=attr.validators.instance_of(bool), default=DEFAULT_NAMESPACE_ID_USE_UUID)
    output_only_used_namespaces: bool = attr.ib(validator=attr.validators.instance_of(bool), default=DEFAULT_OUTPUT_ONLY_USED_NAMESPACES)
    build_new_namespaces: bool = attr.ib(validator=attr.validators.instance_of(bool), default=DEFAULT_BUILD_NEW_NAMESPACES)

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
    summary: bool = attr.ib(validator=attr.validators.instance_of(bool), default=DEFAULT_SUMMARY)
    value_options: KgtkValueOptions = attr.ib(validator=attr.validators.instance_of(KgtkValueOptions), default=DEFAULT_KGTK_VALUE_OPTIONS)

    override_uuid: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)

    build_datatype_column: bool = attr.ib(validator=attr.validators.instance_of(bool), default=DEFAULT_BUILD_DATATYPE_COLUMN)
    datatype_column_name: str = attr.ib(validator=attr.validators.instance_of(str), default=DEFAULT_DATATYPE_COLUMN_NAME)

    error_file: typing.TextIO = attr.ib(default=sys.stderr)
    verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    very_verbose: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    local_namespace_uuid: str = attr.ib(default="")

    namespace_prefixes: typing.MutableMapping[str, str] = attr.ib(factory=dict)
    namespace_ids: typing.MutableMapping[str, str] = attr.ib(factory=dict)
    used_namespaces: typing.Set[str] = attr.ib(factory=set)

    # These get set as needed:
    converted_string_datatype_uri: str = attr.ib(default="")
    converted_lang_string_datatype_uri: str = attr.ib(default="")
    converted_number_datatype_uri: str = attr.ib(default="")

    output_line_count: int = attr.ib(default=0)
    unknown_datatype_iri_count: int = attr.ib(default=0)
    rejected_lang_string_count: int = attr.ib(default=0)

    def write_row(self, ew: KgtkWriter, node1: str, label: str, node2: str, datatype: str):
        output_row: typing.List[str]
        if self.build_datatype_column:
            output_row = [ node1, label, node2, datatype]
        else:
            output_row = [ node1, label, node2]

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

        if not self.build_new_namespaces:
            # Do not attempt to build a new namespace.
            return body, True

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

    def convert_string(self, item: str, line_number: int)->typing.Tuple[str, bool]:
        # Convert this to a KGTK string.

        s: str = ast.literal_eval(item)
        return KgtkFormat.stringify(s), True
 
    def convert_lq_string(self, item: str, line_number: int)->typing.Tuple[str, bool]:
        # Convert this to a KGTK language qualified string.

        # Split the language qualifier (and optional suffix).
        # This code was copied from KgtkFormat.
        #
        # TODO: There should be only a single copy of this code.
        quoted_string: str
        language: str
        quoted_string, language = item.rsplit("@", 1)
        language_suffix: str = ""
        if "-" in language:
            language, language_suffix = language.split("-", 1)
            language_suffix = "-" + language_suffix

        # Parse the string, processing quoted characters:
        #
        # TODO: check for an error here!
        s: str = ast.literal_eval(quoted_string)

        # Assemble the final language-qualified string:
        return KgtkFormat.stringify(s, language, language_suffix), True

 
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
        

    # https://www.w3.org/2011/rdf-wg/wiki/XSD_Datatypes
    # https://www.w3.org/TR/xmlschema-2/

    NUMERIC_XSD_DATATYPES: typing.Set[str] = {
        '<http://www.w3.org/2001/XMLSchema#decimal>',
        '<http://www.w3.org/2001/XMLSchema#integer>',
        '<http://www.w3.org/2001/XMLSchema#int>',
        '<http://www.w3.org/2001/XMLSchema#short>',
        '<http://www.w3.org/2001/XMLSchema#byte>',
        '<http://www.w3.org/2001/XMLSchema#nonNegativeInteger>',
        '<http://www.w3.org/2001/XMLSchema#positiveInteger>',
        '<http://www.w3.org/2001/XMLSchema#unsignedLong>',
        '<http://www.w3.org/2001/XMLSchema#unsignedInt>',
        '<http://www.w3.org/2001/XMLSchema#unsignedShort>',
        '<http://www.w3.org/2001/XMLSchema#unsignedByte>',
        '<http://www.w3.org/2001/XMLSchema#nonPositiveInteger>',
        '<http://www.w3.org/2001/XMLSchema#negativeInteger>',
        '<http://www.w3.org/2001/XMLSchema#double>',
        '<http://www.w3.org/2001/XMLSchema#float>',
    }

    STRING_XSD_DATATYPES: typing.Set[str] = {
        '<http://www.w3.org/2001/XMLSchema#string>',
        '<http://www.w3.org/2001/XMLSchema#normalizedString>',
        '<http://www.w3.org/2001/XMLSchema#token>',
        '<http://www.w3.org/2001/XMLSchema#language>',
        '<http://www.w3.org/2001/XMLSchema#Name>',
        '<http://www.w3.org/2001/XMLSchema#NCName>',
        '<http://www.w3.org/2001/XMLSchema#ENTITY>',
        '<http://www.w3.org/2001/XMLSchema#ID>',
        '<http://www.w3.org/2001/XMLSchema#IDREF>',
        '<http://www.w3.org/2001/XMLSchema#NMTOKEN>',
    }

    LANG_STRING_DATATYPE_IRI: str = "<http://www.w3.org/1999/02/22-rdf-syntax-ns#langString>"
    STRING_DATATYPE_IRI: str = '<http://www.w3.org/2001/XMLSchema#string>'
    NUMBER_DATATYPE_IRI: str = '<http://www.w3.org/2001/XMLSchema#number>'
                                                 
    def get_converted_string_datatype_uri(self)->str:
        if len(self.converted_string_datatype_uri) == 0 and self.build_datatype_column:
            # Convert the string datatype IRI and cache it:
            converted_string_datatype_uri_is_valid: bool
            self.converted_string_datatype_uri, converted_string_datatype_uri_is_valid = self.convert_uri(self.STRING_DATATYPE_IRI, 0)
            # TODO: fail if converted_string_datatype_uri_is_valid is False
        return self.converted_string_datatype_uri

    def get_converted_lang_string_datatype_uri(self)->str:
        if len(self.converted_lang_string_datatype_uri) == 0 and self.build_datatype_column:
            # Convert the langString datatype IRI and cache it:
            converted_lang_string_datatype_uri_is_valid: bool
            self.converted_lang_string_datatype_uri, converted_lang_string_datatype_uri_is_valid = self.convert_uri(self.LANG_STRING_DATATYPE_IRI, 0)
            # TODO: fail if converted_lang_string_datatype_uri_is_valid is False
        return self.converted_lang_string_datatype_uri

    def get_converted_number_datatype_uri(self)->str:
        if len(self.converted_number_datatype_uri) == 0 and self.build_datatype_column:
            # Convert the number datatype IRI and cache it:
            converted_number_datatype_uri_is_valid: bool
            self.converted_number_datatype_uri, converted_number_datatype_uri_is_valid = self.convert_uri(self.NUMBER_DATATYPE_IRI, 0)
            # TODO: fail if converted_number_datatype_uri_is_valid is False
        return self.converted_number_datatype_uri

    def convert_structured_literal(self, item: str, line_number: int, ew: KgtkWriter)->typing.Tuple[str, bool, str]:
        # This is the subset of strictured literals that fits the
        # pattern "STRING"^^<URI>.

        # Start by splitting on '^^'. We are certain it exists, and that the rightmost
        # instance is the one we want.
        uparrows: int = item.rfind("^^")
        if uparrows < 0:
            # This shouldn't happen!
            if self.verbose:
                print("Line %d: no uparrows in '%s'." % (line_number, item), file=self.error_file, flush=True)
            return item, False, ""

        string: str = item[:uparrows]
        uri: str = item[uparrows+2:]

        converted_uri: str = ""
        valid_uri: bool = True

        if uri in self.STRING_XSD_DATATYPES:
            # Convert this to a KGTK string.
            if self.build_datatype_column:
                converted_uri, valid_uri = self.convert_uri(uri, line_number)
                if not valid_uri:
                    return item, False, ""
            return self.convert_string(string, line_number) + (converted_uri,)

        elif uri in self.NUMERIC_XSD_DATATYPES:
            # Convert this to a KGTK number:
            if self.build_datatype_column:
                converted_uri, valid_uri = self.convert_uri(uri, line_number)
                if not valid_uri:
                    return item, False, ""
            return string[1:-1], True, converted_uri

        elif uri == '<http://www.w3.org/2001/XMLSchema#boolean>':
            # Convert this to a KGTK boolean:
            if self.build_datatype_column:
                converted_uri, valid_uri = self.convert_uri(uri, line_number)
                if not valid_uri:
                    return item, False, ""
            return self.convert_boolean(item, string[1:-1], line_number) + (converted_uri,)

        elif uri == '<http://www.w3.org/2001/XMLSchema#dateTime>':
            # Convert this to a KGTK date-and-time:
            #
            # Note: the W3C XML Schema standard allows the now obsolete
            # end-of-day time "24:00:00".
            if self.build_datatype_column:
                converted_uri, valid_uri = self.convert_uri(uri, line_number)
                if not valid_uri:
                    return item, False, ""
            return '^' + string[1:-1], True, converted_uri

        # TODO: the "date" schema
        # Problem:  it allows timezone offsets after dates without times!

        # Exposed langString datatypes are forbidden by the RDF 1.1 N-Triples
        # specification (and by the RDF 1.1 Turtle specification), but they
        # may occur in the wild anyway.  If we are so inclined, transform the
        # literal to an ordinary KGTK string.
        if uri == self.LANG_STRING_DATATYPE_IRI:
            if self.allow_lang_string_datatype:
                if len(self.lang_string_tag) == 0 or self.lang_string_tag == self.LANG_STRING_TAG_NONE:
                    # Convert this to a KGTK string.
                    return self.convert_string(string, line_number) + (self.get_converted_string_datatype_uri(),)
                else:
                    # Convert this to a KGTK language-qualified string.
                    return self.convert_lq_string(string + "@" + self.lang_string_tag, line_number) + (self.get_converted_lang_string_datatype_uri(),)
            else:
                self.rejected_lang_string_count += 1
                return item, False, ""

        if self.allow_unknown_datatype_iris:
            self.unknown_datatype_iri_count += 1

            converted_uri, valid_uri = self.convert_uri(uri, line_number)
            if not valid_uri:
                return item, False, ""

            if self.build_datatype_column:
                return string, True, converted_uri
            else:
                new_node_symbol: str = self.generate_new_node_symbol()
                self.write_row(ew, new_node_symbol, self.structured_value_label, string, "")
                self.write_row(ew, new_node_symbol, self.structured_uri_label, converted_uri, "")
                return new_node_symbol, True, ""
        
        # Give up on this unrecognized structured literal.
        return item, False, ""

    def convert_numeric(self, item: str, line_number: int, ew: KgtkWriter)->typing.Tuple[str, bool]:
        return item, True

    def convert(self, item: str, line_number: int, ew: KgtkWriter)->typing.Tuple[str, bool, str]:
        """
        Convert an ntriples item to KGTK format.

        TODO: update output_line_count for row written here.
        """
        if item.startswith("_:"):
            return self.convert_blank_node(item) + ("",)
        elif item.startswith("<") and item.endswith(">"):
            return self.convert_uri(item, line_number) + ("",)
        elif item.startswith('"') and item.endswith('"'):
            return self.convert_string(item, line_number) + (self.get_converted_string_datatype_uri(),)
        elif item.startswith('"') and item.endswith(">"):
            return self.convert_structured_literal(item, line_number, ew)
        elif item.startswith('"'):
            return self.convert_lq_string(item, line_number) + (self.get_converted_lang_string_datatype_uri(),)
        elif self.allow_turtle_quotes:
            if item.startswith("'") and item.endswith("'"):
                return self.convert_string(item, line_number) + (self.get_converted_string_datatype_uri(),)
            elif item.startswith("'") and item.endswith(">"):
                return self.convert_structured_literal(item, line_number, ew)
            elif item.startswith("'"):
                return self.convert_lq_string(item, line_number) + (self.get_converted_lang_string_datatype_uri(),)
        elif item[0] in "+-0123456789.":
            return self.convert_numeric(item, line_number, ew) + (self.get_converted_number_datatype_uri(),)

        if self.verbose:
            print("Line %d: unrecognized item '%s'" %(line_number, item), file=self.error_file, flush=True)

        return item, False, ""
    
    def convert_and_validate(self, item: str, line_number: int, ew: KgtkWriter)->typing.Tuple[str, bool, str]:
        result: str
        is_ok: bool
        datatype: str
        result, is_ok, datatype = self.convert(item, line_number, ew)

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
                return result, False, ""
        return result, is_ok, datatype
            

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
            print("Processing namespace file %s" % repr(str(self.namespace_file_path)), file=self.error_file, flush=True)

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
                    self.write_row(ew, namespace_id, self.prefix_expansion_label, '"' + self.namespace_ids[namespace_id] + '"', "")
            else:
                self.write_row(ew, namespace_id, self.prefix_expansion_label, '"' + self.namespace_ids[namespace_id] + '"', "")

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

    def parse(self, line: str, line_number: int)->typing.Tuple[typing.List[str], bool, bool]:
        m: typing.Optional[typing.Match] = self.ROW_RE.match(line)
        if m is None:
            if self.verbose:
                print("Line %d: not parsed.\n%s" % (line_number, line), file=self.error_file, flush=True)
            return [ ], False, False
        return [m.group("node1"), m.group("label"), m.group("node2")], True, len(m.group("comment")) > 0


    def process(self):
        output_column_names: typing.List[str] = self.COLUMN_NAMES.copy()
        if self.build_datatype_column:
            output_column_names.append(self.datatype_column_name)
        if self.build_id and self.idbuilder_options is not None:
            self.idbuilder = KgtkIdBuilder.from_column_names(output_column_names, self.idbuilder_options)
            output_column_names = self.idbuilder.column_names

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
                print("Opening reject file %s" % repr(str(self.reject_file_path)), file=self.error_file, flush=True)
            # Open the reject file. Since the input data is not in KGTK format,
            # we use an ordinary file here.
            if str(self.reject_file_path) == "-":
                rw = sys.stdout
            else:
                rw = open(self.reject_file_path, "wt")


        total_input_line_count: int = 0
        reject_line_count: int = 0
        comment_count: int = 0
        
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
                has_comment: bool
                row, valid, has_comment = self.parse(line, input_line_count)
                if not valid:
                    if rw is not None:
                        rw.write(line)
                    reject_line_count += 1
                    continue

                node1: str
                ok_1: bool
                node1, ok_1, _ = self.convert_and_validate(row[0], input_line_count, ew)

                label: str
                ok_2: bool
                label, ok_2, _ = self.convert_and_validate(row[1], input_line_count, ew)

                node2: str
                ok_3: bool
                datatype: str
                node2, ok_3, datatype = self.convert_and_validate(row[2], input_line_count, ew)

                if ok_1 and ok_2 and ok_3:
                    self.write_row(ew, node1, label, node2, datatype)
                else:
                    if rw is not None:
                        rw.write(line)
                    reject_line_count += 1

                if has_comment:
                    comment_count += 1

            if input_file_path != "-":
                infile.close()


                self.save_namespaces(ew)

        if self.verbose or self.summary:
            print("Processed %d known namespaces." % (namespace_line_count), file=self.error_file, flush=True)
            print("Processed %d records." % (total_input_line_count), file=self.error_file, flush=True)
            print("Rejected %d records." % (reject_line_count), file=self.error_file, flush=True)
            print("Wrote %d records." % (self.output_line_count), file=self.error_file, flush=True)
            print("Ignored %d comments." % (comment_count), file=self.error_file, flush=True)
            print("Rejected %d records with langString IRIs." % (self.rejected_lang_string_count), file=self.error_file, flush=True)
            print("Imported %d records with unknown datatype IRIs." % (self.unknown_datatype_iri_count), file=self.error_file, flush=True)

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

        parser.add_argument(      "--build-new-namespaces", dest="build_new_namespaces",
                                  help="When True, create new namespaces.  When False, use only existing namespaces. (default=%(default)s).",
                                  type=optional_bool, nargs='?', const=True, default=cls.DEFAULT_BUILD_NEW_NAMESPACES)

        parser.add_argument(      "--allow-lax-uri", dest="allow_lax_uri",
                                  help="Allow URIs that don't begin with a http:// or https://. (default=%(default)s).",
                                  type=optional_bool, nargs='?', const=True, default=cls.DEFAULT_ALLOW_LAX_URI)

        parser.add_argument(      "--allow-unknown-datatype-iris", dest="allow_unknown_datatype_iris",
                                  help="Allow unknown datatype IRIs, creating  a qualified record. (default=%(default)s).",
                                  type=optional_bool, nargs='?', const=True, default=cls.DEFAULT_ALLOW_UNKNOWN_DATATYPE_IRIS)

        parser.add_argument(      "--allow-turtle-quotes", dest="allow_turtle_quotes",
                                  help="Allow literals to use single quotes (to support Turtle format). (default=%(default)s).",
                                  type=optional_bool, nargs='?', const=True, default=cls.DEFAULT_ALLOW_TURTLE_QUOTES)

        parser.add_argument(      "--allow-lang-string-datatype", dest="allow_lang_string_datatype",
                                  help="Allow literals to include exposed langString datatype IRIs (which is forbidden by the spec, but occurs anyway). (default=%(default)s).",
                                  type=optional_bool, nargs='?', const=True, default=cls.DEFAULT_ALLOW_LANG_STRING_DATATYPE)

        parser.add_argument(      "--lang-string-tag", dest="lang_string_tag",
                                  help="The tag to use with exposed langString instances. `` or `-` mean to use a string, otherwise use a lanuage-qualified string. (default=%(default)s).",
                                  default=cls.DEFAULT_LANG_STRING_TAG)
    
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

        parser.add_argument(      "--build-datatype-column", dest="build_datatype_column",
                                  help="When True, and --datatype-column-name DATATYPE_COLUMN_NAME is not empty, build a column with RDF datatypes. (default=%(default)s).",
                                  type=optional_bool, nargs='?', const=True, default=cls.DEFAULT_BUILD_DATATYPE_COLUMN)

        parser.add_argument(      "--datatype-column-name", dest="datatype_column_name",
                                  help="The name of the column with RDF datatypes. (default=%(default)s).",
                                  default=cls.DEFAULT_DATATYPE_COLUMN_NAME)
    
        parser.add_argument(      "--validate", dest="validate",
                                  help="When true, validate that the result fields are good KGTK file format. (default=%(default)s).",
                                  type=optional_bool, nargs='?', const=True, default=cls.DEFAULT_VALIDATE)

        parser.add_argument(      "--summary", dest="summary",
                                  help="When true, print summary statistics when done processing (also implied by --verbose). (default=%(default)s).",
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
        print("--input-files %s" % " ".join([repr(str(path)) for path in input_file_paths]), file=error_file, flush=True)
        print("--output-file=%s" % repr(str(args.output_file_path)), file=error_file, flush=True)
        # TODO: show ifempty-specific options.
        if args.reject_file_path is not None:
            print("--reject-file=%s" % repr(str(args.reject_file_path)), file=error_file, flush=True)
        if args.namespace_file_path is not None:
            print("--namespace-file=%s" % repr(str(args.namespace_file_path)), file=error_file, flush=True)
        if args.updated_namespace_file_path is not None:
            print("--updated-namespace-file=%s" % repr(str(args.updated_namespace_file_path)), file=error_file, flush=True)
        print("--namespace-id-prefix %s" % repr(args.namespace_id_prefix), file=error_file, flush=True)
        print("--namespace-id-use-uuid %s" % repr(args.namespace_id_use_uuid), file=error_file, flush=True)
        print("--namespace-id-counter %s" % repr(args.namespace_id_counter), file=error_file, flush=True)
        print("--namespace-id-zfill %s" % repr(args.namespace_id_zfill), file=error_file, flush=True)
        print("--output-only-used-namespaces %s" % repr(args.output_only_used_namespaces), file=error_file, flush=True)
        print("--build-new-namespaces %s" % repr(args.build_new_namespaces), file=error_file, flush=True)
        print("--allow-lax-uri %s" % repr(args.allow_lax_uri), file=error_file, flush=True)
        print("--allow-unknown-datatype-iris %s" % repr(args.allow_unknown_datatype_iris), file=error_file, flush=True)
        print("--allow-turtle-quotes %s" % repr(args.allow_turtle_quotes), file=error_file, flush=True)
        print("--allow-lang-string-datatype %s" % repr(args.allow_lang_string_datatype), file=error_file, flush=True)
        print("--lang-string-tag %s" % repr(args.lang_string_tag), file=error_file, flush=True)
        print("--local-namespace-prefix %s" % repr(args.local_namespace_prefix), file=error_file, flush=True)
        print("--local-namespace-use-uuid %s" % repr(args.local_namespace_use_uuid), file=error_file, flush=True)
        print("--prefix-expansion-label %s" % repr(args.prefix_expansion_label), file=error_file, flush=True)
        print("--structured-value-label %s" % repr(args.structured_value_label), file=error_file, flush=True)
        print("--structured-uri-label %s" % repr(args.structured_uri_label), file=error_file, flush=True)
        print("--newnode-prefix %s" % repr(args.newnode_prefix), file=error_file, flush=True)
        print("--newnode-use-uuid %s" % repr(args.newnode_use_uuid), file=error_file, flush=True)
        print("--newnode-counter %s" % repr(args.newnode_counter), file=error_file, flush=True)
        print("--newnode-zfill %s" % repr(args.newnode_zfill), file=error_file, flush=True)
        print("--build-id=%s" % repr(args.build_id), file=error_file, flush=True)
        print("--build-datatype-column %s" % repr(args.build_datatype_column), file=error_file, flush=True)
        print("--datatype-column-name %s" % repr(args.datatype_column_name), file=error_file, flush=True)
        print("--validate=%s" % repr(args.validate), file=error_file, flush=True)
        print("--summary=%s" % repr(args.summary), file=error_file, flush=True)
        if args.override_uuid is not None:
            print("--override_uuid=%s" % repr(args.override_uuid), file=error_file, flush=True)            

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
        build_new_namespaces=args.build_new_namespaces,
        newnode_prefix=args.newnode_prefix,
        newnode_use_uuid=args.newnode_use_uuid,
        newnode_counter=args.newnode_counter,
        newnode_zfill=args.newnode_zfill,
        allow_lax_uri=args.allow_lax_uri,
        allow_unknown_datatype_iris=args.allow_unknown_datatype_iris,
        allow_turtle_quotes=args.allow_turtle_quotes,
        allow_lang_string_datatype=args.allow_lang_string_datatype,
        lang_string_tag=args.lang_string_tag,
        local_namespace_prefix=args.local_namespace_prefix,
        local_namespace_use_uuid=args.local_namespace_use_uuid,
        prefix_expansion_label=args.prefix_expansion_label,
        structured_value_label=args.structured_value_label,
        structured_uri_label=args.structured_uri_label,
        build_id=args.build_id,
        idbuilder_options=idbuilder_options,
        build_datatype_column=args.build_datatype_column,
        datatype_column_name=args.datatype_column_name,
        validate=args.validate,
        summary=args.summary,
        override_uuid=args.override_uuid,
        reader_options=reader_options,
        value_options=value_options,
        error_file=error_file,
        verbose=args.verbose,
        very_verbose=args.very_verbose)

    kn.process()
    
if __name__ == "__main__":
    main()
