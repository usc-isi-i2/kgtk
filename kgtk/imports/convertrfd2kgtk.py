"""Map RDF datatypes into KGTK datatypes.

Maps an RDF value and datatype to a KGTK value.

Custom datatype mappings may be set up.

Mappings to KGTK quantities may have offsets and scaling factors
applied to the value.

"""
from argparse import ArgumentParser, Namespace
import ast
import attr
import typing

from kgtk.kgtkformat import KgtkFormat
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderMode, KgtkReaderOptions
from kgtk.value.kgtkvalue import KgtkValue, KgtkValueFields

@attr.s(slots=True, frozen=True)
class MapEntry():
    BOOLEAN: str = "boolean"
    DATETIME: str = "datetime"
    LANGSTRING: str = "langstring"
    NUMBER: str = "number"
    QUANTITY: str = "quantity"
    STRING: str = "string"

    datatype: str = attr.ib(validator=attr.validators.instance_of(str))
    offset: typing.Optional[float] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(float)), default=None)
    factor: typing.Optional[float] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(float)), default=None)
    units: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)

@attr.s(slots=True, frozen=True)
class Result():
    is_valid: bool = attr.ib(validator=attr.validators.instance_of(bool), default=True)
    value: str = attr.ib(validator=attr.validators.instance_of(str), default="")
    rdf_datatype_uri: str = attr.ib(validator=attr.validators.instance_of(str), default="")
    is_uri: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    is_blank_node: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    is_unknown: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    message: typing.Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
    

@attr.s(slots=True, frozen=False)
class ConvertRdf2Kgtk(KgtkFormat):
    DEFAULT_ALLOW_UNKNOWN_DATATYPE_IRIS: bool = True
    DEFAULT_ALLOW_TURTLE_QUOTES: bool = False
    DEFAULT_ALLOW_LANG_STRING_DATATYPE: bool = False

    LANG_STRING_TAG_NONE: str = "-"
    DEFAULT_LANG_STRING_TAG: str = LANG_STRING_TAG_NONE

    # https://www.w3.org/2011/rdf-wg/wiki/XSD_Datatypes
    # https://www.w3.org/TR/xmlschema-2/

    XSD_DATATYPE_IRI_PREFIX: str = 'http://www.w3.org/2001/XMLSchema#'
 
    STRING_DATATYPE_IRI: str = XSD_DATATYPE_IRI_PREFIX + 'string'
    NUMBER_DATATYPE_IRI: str = XSD_DATATYPE_IRI_PREFIX + 'number'
    BOOLEAN_DATATYPE_IRI: str = XSD_DATATYPE_IRI_PREFIX + 'boolean'
    DATETIME_DATATYPE_IRI: str = XSD_DATATYPE_IRI_PREFIX + 'dateTime'

    NUMERIC_XSD_DATATYPES: typing.List[str] = [
        XSD_DATATYPE_IRI_PREFIX + 'decimal',
        XSD_DATATYPE_IRI_PREFIX + 'integer',
        XSD_DATATYPE_IRI_PREFIX + 'int',
        XSD_DATATYPE_IRI_PREFIX + 'short',
        XSD_DATATYPE_IRI_PREFIX + 'byte',
        XSD_DATATYPE_IRI_PREFIX + 'nonNegativeInteger',
        XSD_DATATYPE_IRI_PREFIX + 'positiveInteger',
        XSD_DATATYPE_IRI_PREFIX + 'unsignedLong',
        XSD_DATATYPE_IRI_PREFIX + 'unsignedInt',
        XSD_DATATYPE_IRI_PREFIX + 'unsignedShort',
        XSD_DATATYPE_IRI_PREFIX + 'unsignedByte',
        XSD_DATATYPE_IRI_PREFIX + 'nonPositiveInteger',
        XSD_DATATYPE_IRI_PREFIX + 'negativeInteger',
        XSD_DATATYPE_IRI_PREFIX + 'double',
        XSD_DATATYPE_IRI_PREFIX + 'float',
    ]

    STRING_XSD_DATATYPES: typing.List[str] = [
        XSD_DATATYPE_IRI_PREFIX + 'string',
        XSD_DATATYPE_IRI_PREFIX + 'normalizedString',
        XSD_DATATYPE_IRI_PREFIX + 'token',
        XSD_DATATYPE_IRI_PREFIX + 'language',
        XSD_DATATYPE_IRI_PREFIX + 'Name',
        XSD_DATATYPE_IRI_PREFIX + 'NCName',
        XSD_DATATYPE_IRI_PREFIX + 'ENTITY',
        XSD_DATATYPE_IRI_PREFIX + 'ID',
        XSD_DATATYPE_IRI_PREFIX + 'IDREF',
        XSD_DATATYPE_IRI_PREFIX + 'NMTOKEN',
    ]

    RDF_DATATYPE_IRI_PREFIX: str = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    LANG_STRING_DATATYPE_IRI: str = RDF_DATATYPE_IRI_PREFIX + "langString"

    datatype_map: typing.MutableMapping[str, MapEntry] = attr.ib(factory=dict)

    allow_unknown_datatype_iris: bool = attr.ib(validator=attr.validators.instance_of(bool), default=DEFAULT_ALLOW_UNKNOWN_DATATYPE_IRIS)

    allow_turtle_quotes: bool = attr.ib(validator=attr.validators.instance_of(bool), default=DEFAULT_ALLOW_TURTLE_QUOTES)

    allow_lang_string_datatype: bool = attr.ib(validator=attr.validators.instance_of(bool), default=DEFAULT_ALLOW_LANG_STRING_DATATYPE)
    lang_string_tag: str = attr.ib(validator=attr.validators.instance_of(str), default=DEFAULT_LANG_STRING_TAG)

    unknown_datatype_iri_count: int = attr.ib(default=0)
    rejected_lang_string_count: int = attr.ib(default=0)

    def convert_numeric(self, item: str, uri: str = ConvertRdf2Kgtk.NUMBER_DATATYPE_IRI)->Result:
        if len(item) == 0:
            return Result(is_valid=False, rdf_datatype_uri=uri, message="Empty numeric value")

        return Result(value=item, rdf_datatype_uri=uri)

    def convert_quantity(self, item: str, entry: MapEntry, uri: str)->Result:
        if len(item) == 0:
            return Result(is_valid=False, rdf_datatype_uri=uri, message="Empty quantity value")

        try:
            # TOTO: verify that this works with integers
            value: float = float(item)
        except:
            return Result(is_valid=False, rdf_datatype_uri=uri, message="Quantity value failed convertion to float")

        if entry.offset is not None:
            value += entry.offset
        if entry.factor is not None:
            value *= entry.factor
        strvalue = str(value)
        if entry.units is not None:
            strvalue += entry.units

        return Result(value=strvalue, rdf_datatype_uri=uri)

    def convert_string(self, item: str, uri: str = ConvertRdf2Kgtk.STRING_DATATYPE_IRI)->Result:
        # Convert this to a KGTK string.

        s: str = ast.literal_eval(item)
        return Result(value=KgtkFormat.stringify(s), rdf_datatype_uri=uri)


    def convert_lq_string(self, item: str, uri = ConvertRdf2Kgtk.LANG_STRING_DATATYPE_IRI)->Result:
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
        return Result(value=KgtkFormat.stringify(s, language, language_suffix), rdf_datatype_uri=uri)

    def convert_boolean(self, value: str, uri=ConvertRdf2Kgtk.BOOLEAN_DATATYPE_IRI)->Result:
        value = value.lower()
        if value == 'true' or value == '1':
            return Result(value=KgtkFormat.TRUE_SYMBOL, rdf_datatype_uri=uri)
        elif value == 'false' or value == '0':
            return Result(value=KgtkFormat.FALSE_SYMBOL, rdf_datatype_uri=uri)
        else:
            return Result(is_valid=False, rdf_datatype_uri=uri, message="Invalid boolean value '%s'" % (value))

    def convert_datetime(self, item: str, uri: str = ConvertRdf2Kgtk.DATETIME_DATATYPE_IRI)->Result:
        # Convert this to a KGTK date-and-time:
        #
        # Note: the W3C XML Schema standard allows the now obsolete
        # end-of-day time "24:00:00".
        if len(item) > 0:
            return Result(value=KgtkFormat.DATE_AND_TIMES_SIGIL + item, rdf_datatype_uri=uri)
        else:
            return Result(is_valid=False, rdf_datatype_uri=uri, message="Empty datetime value")

    def convert_langstring(self, item: str, uri = ConvertRdf2Kgtk.LANG_STRING_DATATYPE_IRI)->Result:
        # Exposed langString datatypes are forbidden by RDF when not
        # accompanied with a language tag.  The RDF 1.1 N-Triples)
        # specification (and the RDF 1.1 Turtle specification) allow a
        # a literal to have a datatype IRI or a language tag, but not
        # both. Nonetheless, langString IRIs have been observed in the
        # wild.  If we are so inclined, transform the literal to a
        # KGTK string or language-qualified string.
        if not self.allow_lang_string_datatype:
            self.rejected_lang_string_count += 1
            return Result(is_valid=False, rdf_datatype_uri=uri, message="langString is not allowed")

        if len(self.lang_string_tag) == 0 or self.lang_string_tag == self.LANG_STRING_TAG_NONE:
            # Convert this to a KGTK string.
            return self.convert_string(item, uri=uri)
        else:
            # Convert this to a KGTK language-qualified string.
            return self.convert_lq_string(item + "@" + self.lang_string_tag, uri=uri)

    def convert_structured_literal(self, item: str)->Result:
        # This is the subset of RDF N-Triples literals that fits the
        # pattern "STRING"^^<URI>.

        # Start by splitting on '^^'. We are certain it exists, and that the rightmost
        # instance is the one we want.
        uparrows: int = item.rfind("^^")
        if uparrows < 0:
            # This shouldn't happen!
            return Result(is_valid=False, message="No uparrows in RDF literal %s" % repr(item))

        value: str = item[:uparrows]
        uri: str = item[uparrows+2:]

        converted_uri: str = ""
        valid_uri: bool = True

        if not uri.startswith("<"):
            return Result(is_valid=False, message="The datatype iri does not start with '<': %s" % repr(item))
        
        if not uri.endswith("<"):
            return Result(is_valid=False, message="The datatype iri does not end with '>': %s" % repr(item))

        uri = uri[1:-1]
        if len(uri) ==0:
            return Result(is_valid=False, message="The datatype iri is empty: %s" % repr(item))
        
        if uri in self.datatype_map:
            entry: MapEntry = self.datatype_map[uri]
            if entry.datatype == MapEntry.NUMBER:
                return self.convert_numeric(value[1:-1], uri=uri)

            elif entry.datatype == MapEntry.QUANTITY:
                return self.convert_quantity(value[1:-1], entry, uri=uri)

            elif entry.datatype == MapEntry.STRING:
                return self.convert_string(value, uri=uri)

            elif entry.datatype == MapEntry.BOOLEAN:
                return self.convert_boolean(value[1:-1], uri=uri)

            elif entry.datatype == MapEntry.DATETIME:
                return self.convert_datetime(value[1:-1], uri=uri)

            elif entry.datatype == MapEntry.LANGSTRING:
                return self.convert_langstring(value, uri=uri)

            else:
                return Result(is_valid=False, message="Unknown datatype %s in map for %s." % (repr(entry.datatype), repr(item)))


        if self.allow_unknown_datatype_iris:
            self.unknown_datatype_iri_count += 1
            s: str = ast.literal_eval(value)
            return Result(value=KgtkFormat.stringify(s), rdf_datatype_uri=uri, is_unknown=True)
        
        # Give up on this unrecognized structured literal.
        return Result(is_valid=False, message="Unrecognized RDF literal %s" % repr(item))

    def convert(self, item: str)->Result:
        if item[0] in "+-0123456789.":
            return self.convert_numeric(item)

        elif item.startswith("_:"):
            return Result(is_blank_node=True, value=item) # Blank node

        elif item.startswith("<") and item.endswith(">"):
            return Result(is_uri=True, value=item)

        elif item.startswith('"') and item.endswith('"'):
            return self.convert_string(item)

        elif item.startswith('"') and item.endswith(">"):
            return self.convert_structured_literal(item)

        elif item.startswith('"'):
            return self.convert_lq_string(item)

        elif self.allow_turtle_quotes:
            if item.startswith("'") and item.endswith("'"):
                return self.convert_string(item)

            elif item.startswith("'") and item.endswith(">"):
                return self.convert_structured_literal(item)

            elif item.startswith("'"):
                return self.convert_lq_string(item)

        return Result(is_valid=False, message="Unrecognized RDF item %s" % repr(item))

    def load_xsd_datatypes(self):
        self.datatype_map[self.STRING_DATATYPE_IRI] = MapEntry(MapEntry.STRING)
        self.datatype_map[self.NUMBER_DATATYPE_IRI] = MapEntry(MapEntry.NUMBER)
        self.datatype_map[self.BOOLEAN_DATATYPE_IRI] = MapEntry(MapEntry.BOOLEAN)
        self.datatype_map[self.DATETIME_DATATYPE_IRI] = MapEntry(MapEntry.DATETIME)

        datatype_uri: str
        for datatype_uri in self.NUMERIC_XSD_DATATYPES:
            self.datatype_map[datatype_uri] = MapEntry(MapEntry.NUMBER)

        for datatype_uri in self.STRING_XSD_DATATYPES:
            self.datatype_map[datatype_uri] = MapEntry(MapEntry.STRING)

    def load_rdf_datatypes(self):
        self.datatype_map[self.LANG_STRING_DATATYPE_IRI] = MapEntry(MapEntry.LANGSTRING)

    def load_standard_datatypes(self):
        self.load_xsd_datatypes()
        self.load_rdf_datatypes()

    def add_custom_datatype(self,
                            url: str,
                            datatype: str,
                            offset: typing.Optional[float] = None,
                            factor: typing.Optional[float] = None,
                            units: typing.Optional[str] = None):
        self.datatype_map[url] = MapEntry(datatype=datatype,
                                          offset=offset,
                                          factor=factor,
                                          units=units)


    DBPEDIA_DATATYPE_IRI_PREFIX: str = '<http://depedia.org/datatype/'
    
    DBPEDIA_DATATYPES_TO_SI_UNITS: typing.Mapping[str, MapEntry] = {
        # http://mappings.dbpedia.org/index.php/DBpedia_Datatypes

        # Area
        'squareMeter': MapEntry(MapEntry.QUANTITY, units="m2"),
        'squareNauticalMile': MapEntry(MapEntry.QUANTITY, factor=3429904, units="m2"),
        'squareMile': MapEntry(MapEntry.QUANTITY, factor=2589988.1103, units='m2'),
        # acre
        # squareYard
        # squareFoot
        # squareInch
        # hectare
        # squareKilometer
        # squareHectometre
        # squareDecametre
        # squareDecimetre
        # squareCentimetre
        # squareMillimetre

        # Currency
        # No equivalent in KGTK quantities

        # Density
        # Datatype:gramPerMillilitre
        # Datatype:gramPerCubicCentimetre
        # Datatype:kilogramPerLitre
        # Datatype:kilogramPerCubicMetre

        # Energy
        # Datatype:footPound
        # Datatype:inchPound
        # Datatype:megacalorie
        # Datatype:kilocalorie
        # Datatype:calorie
        # Datatype:millicalorie
        # Datatype:terawattHour
        # Datatype:gigawattHour
        # Datatype:megawattHour
        # Datatype:kilowattHour
        # Datatype:wattHour
        # Datatype:milliwattHour
        # Datatype:erg
        # Datatype:kilojoule
        # Datatype:joule

        # FlowRate
        # Datatype:cubicFeetPerYear
        # Datatype:cubicMetrePerYear
        # Datatype:cubicFeetPerSecond
        # Datatype:cubicMetrePerSecond

        # Force
        # Datatype:poundal
        # Datatype:millipond
        # Datatype:milligramForce
        # Datatype:pond
        # Datatype:gramForce
        # Datatype:kilopond
        # Datatype:kilogramForce
        # Datatype:megapond
        # Datatype:tonneForce
        # Datatype:giganewton
        # Datatype:meganewton
        # Datatype:kilonewton
        # Datatype:millinewton
        # Datatype:nanonewton
        # Datatype:newton

        # FuelEfficiency
        'kilometresPerLitre': MapEntry(MapEntry.QUANTITY, factor=1, units="m/m3"), # 1000 kilometres per mitre, .001 cubic metres per litre.

        # Frequency

        # InformationUnit
        # no equivalent in KGTK quantities

        # Length

        # LinearMassDensity

        # Mass

        # PopulationDensity

        # Power

        # ElectricCurrent
        # Voltage

        # Pressure

        # Speed

        # Temperature

        # Time

        # Torque

        # Volume

        # Other
        # We don't have a representation for pH.

    }
