from uuid import uuid4
from datetime import datetime
from kgtk.exceptions import InvalidGraphNodeValueError, UnknownLiteralType
import re


class Node(object):
    def __init__(self, value):
        if not isinstance(value, str):
            raise InvalidGraphNodeValueError()
        self._value = value

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self._value == other._value

    def __hash__(self):
        return hash(self.value)

    @property
    def value(self):
        return self._value

    def is_valid(self):
        raise NotImplementedError('Subclass should implement this.')


class URI(Node):
    def __init__(self, value):
        if isinstance(value, URI):
            super().__init__(value.value)
        else:
            super().__init__(value)

    def __eq__(self, other):
        if not isinstance(other, URI):
            return False
        return super().__eq__(other)

    def __hash__(self):
        return hash(self.value)

    def is_valid(self):
        return self.value is not None


class BNode(Node):
    def __init__(self, value=None):
        if isinstance(value, BNode):
            super().__init__(value.value)
        else:
            if not value:
                value = uuid4().hex
            super().__init__(value)

    def __eq__(self, other):
        if not isinstance(other, BNode):
            return False
        return super().__eq__(other)

    def __hash__(self):
        return hash(self.value)

    def is_valid(self):
        return self.value is not None


class Literal(Node):
    def __init__(self, value, lang=None, type_=None):
        if isinstance(value, Literal):
            super().__init__(value.value)
            self._lang = value.lang
            self._type = value._type
        else:
            super().__init__(value)
            self._lang = lang
            if type_ and isinstance(type_, str):
                type_ = LiteralType(type_)
            self._type = type_

    def __eq__(self, other):
        if not isinstance(other, Literal):
            return False
        return super().__eq__(other) and self.lang == other.lang and self.type == other.type

    def __hash__(self):
        return hash((self.value, self.lang, self.raw_type))

    def __str__(self):
        return self.value

    @property
    def lang(self):
        return self._lang

    @property
    def type(self):
        return self._type

    @property
    def raw_type(self):
        if self._type:
            return self._type.value

    def is_valid(self):
        if self.value is None:
            return False
        if self._type == LiteralType.string and not self._lang:
            return False
        return self._type.is_value_valid(self.value)


class __Type(type):
    def __getattr__(self, item):
        return LiteralType(item)


class LiteralType(URI, metaclass=__Type):
    valid_time_pattern = re.compile(
        r"[\-]?(\d{4})-((0[1-9])|(1[0-2]))-(0[1-9]|[12][0-9]|3[01])T(0[0-9]|1[0-9]|2[0-3])"
        r":(0[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9]):(0[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9])")
    valid_month_pattern = re.compile(r"[\-]?(\d{4})-((0[1-9])|(1[0-2]))-(00)T00:00:00")
    valid_year_decade_millennium_pattern = re.compile(r"[\-]?(\d{4})-(00)-(00)T00:00:00")
    valid_hundred_thousand_years_pattern = re.compile(r"[\-]?(\d{6,7})-(0[0|1])-(0[0|1])T00:00:00")
    valid_million_billion_years = re.compile(r"[\-]?(\d{8}\d+)-(0[0|1])-(0[0|1])T00:00:00")

    def __init__(self, s, common_check=True):
        self.common_check = common_check
        self._type = None
        super().__init__(self._resolve(s))

    def _resolve(self, s):
        if not isinstance(s, str):
            raise UnknownLiteralType()
        if not self.common_check:
            return s
        # complete xsd uri
        if s.startswith(self.xsd) and s[len(self.xsd):] in self.xsd_tokens:
            self._type = s[len(self.xsd):]
            return s
        # complete rdf uri
        elif s.startswith(self.rdf) and s[len(self.rdf)] in self.rdf_tokens:
            self._type = s[len(self.rdf)]
            return s
        # xsd prefix
        elif s.startswith('xsd:'):
            s = s[4:]
            if s in self.xsd_tokens:
                self._type = s
                return self.xsd + s
        # rdf prefix
        elif s.startswith('rdf:'):
            s = s[4:]
            if s in self.rdf_tokens:
                self._type = s
                return self.rdf + s
        # no prefix
        elif self._is_valid_field(s):
            if s in self.xsd_tokens:
                self._type = s
                return self.xsd + s
            elif s in self.rdf_tokens:
                self._type = s
                return self.rdf + s
        raise UnknownLiteralType()

    def _is_valid_field(self, s):
        return s in self.xsd_tokens or s in self.rdf_tokens

    def is_value_valid(self, s):
        """
        If value `s` if valid in current LiteralType
        """
        if self._type in self.value_validator:
            return self.value_validator[self._type](s)

        return True

    @staticmethod
    def _is_valid_date_time(s):

        if isinstance(s, datetime):
            return True

        try:
            # python 3.7
            datetime.fromisoformat(s)
            return True
        except Exception:
            pass

        valid_format = [
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%dT%H:%M:%S.%f%z'
        ]
        try:
            for f in valid_format:
                datetime.strptime(s, f)
                return True
        except Exception:
            pass

        validity_list = [LiteralType.valid_time_pattern.match(s),
                         LiteralType.valid_month_pattern.match(s),
                         LiteralType.valid_year_decade_millennium_pattern.match(s),
                         LiteralType.valid_hundred_thousand_years_pattern.match(s),
                         LiteralType.valid_million_billion_years.match(s)]
        return any(validity_list)

    xsd = 'http://www.w3.org/2001/XMLSchema#'
    rdf = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
    xsd_tokens = {
        'time', 'date', 'dateTime', 'string', 'normalizedString', 'token', 'language', 'boolean', 'decimal', 'integer',
        'nonPositiveInteger', 'long', 'nonNegativeInteger', 'negativeInteger', 'int', 'unsignedLong', 'positiveInteger',
        'short', 'unsignedInt', 'byte', 'unsignedShort', 'unsignedByte', 'float', 'double', 'base64Binary', 'anyURI'
    }
    rdf_tokens = {'XMLLiteral', 'HTML'}
    value_validator = {
        'dateTime': _is_valid_date_time.__func__,
    }
    # to_python_type = {
    #     'time': time,
    #     'date': date,
    #     'dateTime': datetime,
    #     'string': str,
    #     'normalizedString': str,
    #     'token': str,
    #     'language': str,
    #     'boolean': bool,
    #     'decimal': float,
    #     'integer': int,
    #     'nonPositiveInteger': int,
    #     'long': int,
    #     'nonNegativeInteger': int,
    #     'negativeInteger': int,
    #     'int': int,
    #     'unsignedLong': int,
    #     'positiveInteger': int,
    #     'short': int,
    #     'unsignedInt': int,
    #     'byte': int,
    #     'unsignedShort': int,
    #     'unsignedByte': int,
    #     'float': float,
    #     'double': float,
    #     'base64Binary': str,
    #     'anyURI': str,
    #     'XMLLiteral': Document,
    #     'HTML': DocumentFragment
    # }
