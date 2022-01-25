from kgtk.knowledge_graph.node import URI, Literal, LiteralType
from kgtk.knowledge_graph.subject import Subject
from enum import Enum


class Precision(Enum):
    # https://www.wikidata.org/wiki/Help:Dates#Time_datatype
    second = Literal('14', type_=LiteralType.integer)
    minute = Literal('13', type_=LiteralType.integer)
    hour = Literal('12', type_=LiteralType.integer)
    # https://www.wikidata.org/wiki/Help:Dates#Precision
    day = Literal('11', type_=LiteralType.integer)
    month = Literal('10', type_=LiteralType.integer)
    year = Literal('9', type_=LiteralType.integer)
    decade = Literal('8', type_=LiteralType.integer)
    century = Literal('7', type_=LiteralType.integer)
    millennium = Literal('6', type_=LiteralType.integer)
    hundred_thousand_years = Literal('4', type_=LiteralType.integer)
    million_years = Literal('3', type_=LiteralType.integer)
    billion_years = Literal('0', type_=LiteralType.integer)


class DataValue:
    value = None
    full_value = None
    normalized_value = None
    type = None

    def _v_name(self):
        raise NotImplemented

    def _create_full_value(self):
        self.full_value = Subject(URI('wdv:' + self._v_name()))


class Item(DataValue):
    type = URI('wikibase:WikibaseItem')

    def __init__(self, s):
        super().__init__()
        self.value = URI('wd:' + s)


class Property(DataValue):
    type = URI('wikibase:WikibaseProperty')

    def __init__(self, s):
        super().__init__()
        self.value = URI('wd:' + s)


class TimeValue(DataValue):
    type = URI('wikibase:Time')

    def __init__(self, value, calendar, precision, time_zone):
        super().__init__()
        self.value = Literal(value, type_=LiteralType.dateTime)
        if not self.value.is_valid():
            raise ValueError('Invalid datetime format')
        self._calendar = calendar
        if isinstance(precision, Precision):
            self._precision = precision.value
        elif isinstance(precision, Literal):
            self._precision = precision
        else:
            self._precision = Literal(str(precision), type_=LiteralType.integer)
        if isinstance(time_zone, Literal):
            self._time_zone = time_zone
        else:
            self._time_zone = Literal(str(time_zone), type_=LiteralType.integer)

        self.__build_full_value()

    def __build_full_value(self):
        self._create_full_value()
        self.full_value.add_property(URI('rdf:type'), URI('wikibase:Time'))
        self.full_value.add_property(URI('wikibase:timePrecision'), self._precision)
        self.full_value.add_property(URI('wikibase:timeTimezone'), self._time_zone)
        self.full_value.add_property(URI('wikibase:timeCalendarModel'), self._calendar.value)
        self.full_value.add_property(URI('wikibase:timeValue'), self.value)
        # TODO fix import bug
        # if not self.value.startswith("+"):
        #     self.full_value.add_property(URI('wikibase:timeValue'), self.value)
        # else:
        #     self.full_value.add_property(URI('wikibase:timeValue'), self.value[1:])

    def _v_name(self):
        time = self.value.value.replace(':', '').replace(' ', '-')
        calendar = self._calendar.value.value[3]
        precision = self._precision.value
        time_zone = self._time_zone.value
        return 'c'.join(('Time', time, calendar, precision, time_zone))


class ExternalIdentifier(DataValue):
    type = URI('wikibase:ExternalId')

    def __init__(self, s, normalized_value=None):
        super().__init__()
        self.value = Literal(s, type_=LiteralType.string)
        if isinstance(normalized_value, URI):
            self.normalized_value = normalized_value
        elif isinstance(normalized_value, str):
            self.normalized_value = URI(normalized_value)


class QuantityValue(DataValue):
    type = URI('wikibase:Quantity')

    def __init__(self, amount, unit=None, upper_bound=None, lower_bound=None, normalized=True,
                 type=LiteralType.decimal):
        self.value = Literal(str(amount), type_=type)
        self.upper_bound = upper_bound is not None and Literal(upper_bound, type_=type)
        self.lower_bound = lower_bound is not None and Literal(lower_bound, type_=type)
        self.unit = unit is not None and unit
        self.__build_full_value()
        if isinstance(normalized, QuantityValue):
            self.normalized_value = normalized.full_value
        else:
            self.normalized_value = self.full_value
        self.full_value.add_property(URI('wikibase:quantityNormalized'), self.normalized_value)

    def __build_full_value(self):
        self._create_full_value()
        self.full_value.add_property(URI('rdf:type'), URI('wikibase:QuantityValue'))
        self.full_value.add_property(URI('wikibase:quantityAmount'), self.value)
        if self.upper_bound:
            self.full_value.add_property(URI('wikibase:quantityUpperBound'), self.upper_bound)
        if self.lower_bound:
            self.full_value.add_property(URI('wikibase:quantityLowerBound'), self.lower_bound)
        if self.unit:
            self.full_value.add_property(URI('wikibase:quantityUnit'), self.unit.value)

    def _v_name(self):
        upper_bound = self.upper_bound.value if self.upper_bound else '0'
        lower_bound = self.lower_bound.value if self.lower_bound else '0'
        unit = self.unit.value.value[3:] if self.unit else '0'
        return 'c'.join(('Quantity', self.value.value.replace('.', '-'), upper_bound, lower_bound, unit))


class StringValue(DataValue):
    type = URI('wikibase:String')

    def __init__(self, s):
        super().__init__()
        self.value = Literal(s, type_=LiteralType.string)


class URLValue(DataValue, URI):
    type = URI('wikibase:Url')

    def __init__(self, s):
        super().__init__(s)
        self.value = URI(s)


class GlobeCoordinate(DataValue):
    type = URI('wikibase:GlobeCoordinate')

    def __init__(self, latitude, longitude, precision, globe=None):
        self.globe = globe
        self.latitude = Literal(str(latitude), type_=LiteralType.decimal)
        self.longitude = Literal(str(longitude), type_=LiteralType.decimal)
        self.precision = Literal(str(precision), type_=LiteralType.decimal)
        s = 'Point({} {})'.format(latitude, longitude)
        if globe:
            s = '<{}> {}'.format(globe.value.value.replace('wd:', 'http://www.wikidata.org/entity/'), s)
        self.value = Literal(s,
                             type_=LiteralType('http://www.opengis.net/ont/geosparql#wktLiteral', common_check=False))
        self.__build_full_value()

    def __build_full_value(self):
        self._create_full_value()
        self.full_value.add_property(URI('rdf:type'), URI('wikibase:GlobecoordinateValue'))
        if self.globe:
            self.full_value.add_property(URI('wikibase:geoGlobe'), self.globe.value)
        self.full_value.add_property(URI('wikibase:geoLatitude'), self.latitude)
        self.full_value.add_property(URI('wikibase:geoLongitude'), self.longitude)
        self.full_value.add_property(URI('wikibase:geoPrecision'), self.precision)

    def _v_name(self):
        latitude = self.latitude.value
        longitude = self.longitude.value
        precision = self.precision.value
        if self.globe:
            globe = self.globe.value.value.replace("wd:", "")
            return 'c'.join(('GlobeCoordinate', globe, latitude, longitude, precision))
        else:
            return 'c'.join(('GlobeCoordinate', latitude, longitude, precision))


class MonolingualText(DataValue):
    type = URI('wikibase:Monolingualtext')

    def __init__(self, s, lang):
        self.value = Literal(s, lang=lang)


class Datatype(Enum):
    Item = Item
    Property = Property
    ExternalIdentifier = ExternalIdentifier
    QuantityValue = QuantityValue
    TimeValue = TimeValue
    StringValue = StringValue
    URLValue = URLValue
    GlobeCoordinate = GlobeCoordinate
    MonolingualText = MonolingualText

    @property
    def type(self):
        return self.value.type
