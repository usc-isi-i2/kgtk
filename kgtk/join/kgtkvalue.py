"""
Constants and helpers for the KGTK file format.

"""

from argparse import ArgumentParser
import attr
from iso639 import languages # type: ignore
import re
import sys
import typing

from kgtk.join.kgtkformat import KgtkFormat

@attr.s(slots=True, frozen=False)
class KgtkValue(KgtkFormat):
    value: str = attr.ib(validator=attr.validators.instance_of(str))

    
    split_list_re: typing.Pattern = re.compile(r"(?<!\\)" + "\\" + KgtkFormat.LIST_SEPARATOR)

    # Cache the list of values.
    values: typing.Optional[typing.List[str]] = None

    def get_list(self)->typing.List[str]:
        if self.values is None:
            self.values = KgtkValue.split_list_re.split(self.value)
        return self.values

    def get_item(self, idx: typing.Optional[int])-> str:
        if idx is None:
            return self.value
        else:
            return self.get_list()[idx]

    def is_list(self)->bool:
        return len(self.get_list()) > 1

    def get_values(self)->typing.List['KgtkValue']:
        """
        Convert the value into a list of KgtkValues.
        """
        if not self.is_list:
            return [ self ]
        else:
            result: typing.List['KgtkValue'] = [ ]
            v: str
            for v in self.get_list():
                result.append(KgtkValue(v))
            return result

    def is_empty(self, idx: typing.Optional[int] = None)->bool:
        """
        Return False if this value is a list and idx is None.
        Otherwise, return True if the value is empty.
        """
        if self.is_list() and idx is None:
            return False
        
        v: str = self.get_item(idx)
        return len(v) == 0

    def is_number(self, idx: typing.Optional[int] = None)->bool:
        """
        Return False if this value is a list and idx is None.
        Otherwise, return True if the first character is 0-9,_,-,. .
        """
        if self.is_list() and idx is None:
            return False
        
        v: str = self.get_item(idx)
        return v.startswith(("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+", "-", "."))
    
    def is_valid_number(self, idx: typing.Optional[int] = None)->bool:
        """
        Return False if this value is a list and idx is None.
        Otherwise, return True if the first character is 0-9,_,-,.
        and Python can parse it.
        """
        if self.is_list() and idx is None:
            return False
        
        v: str = self.get_item(idx)
        if not v.startswith(("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+", "-", ".")):
            return False
        try:
            i: int = int(v, 0) # The 0 allows prefixes: 0b, 0o, and 0x.
            return True
        except ValueError:
            try:
                f: float = float(v)
                return True
            except ValueError:
                return False
        
    
    def is_string(self, idx: typing.Optional[int] = None)->bool:
        """
        Return False if this value is a list and idx is None.
        Otherwise, return True if the first character  is '"'.
        """
        if self.is_list() and idx is None:
            return False
        
        v: str = self.get_item(idx)
        return v.startswith('"')

    string_re: typing.Pattern = re.compile(r'^"(?:[^"]|\\.)*"$')

    def is_valid_string(self, idx: typing.Optional[int] = None)->bool:
        """
        Return False if this value is a list and idx is None.
        Otherwise, return True if the first character  is '"',
        the last character is '"', and the only internal '"' is
        escaped by backslash.
        """
        if self.is_list() and idx is None:
            return False
        
        v: str = self.get_item(idx)
        if not v.startswith('"'):
            return False
        m: typing.Optional[typing.Match] = KgtkValue.string_re.match(v)
        return m is not None

    def is_structured_literal(self, idx: typing.Optional[int] = None)->bool:
        """
        Return False if this value is a list and idx is None.
        Otherwise, return True if the first character  is ^@'!.
        """
        if self.is_list() and idx is None:
            return False
        
        v: str = self.get_item(idx)
        return v.startswith(("^", "@", "'", "!"))

    def is_symbol(self, idx: typing.Optional[int] = None)->bool:
        """
        Return False if this value is a list and idx is None.
        Otherwise, return True if not a number, string, nor structured literal.
        """
        if self.is_list() and idx is None:
            return False

        return not (self.is_number(idx) or self.is_string(idx) or self.is_structured_literal(idx))

    def is_boolean(self, idx: typing.Optional[int] = None)->bool:
        """
        Return False if this value is a list and idx is None.
        Otherwise, return True if the value matches one of the special boolean symbols..
        """
        if self.is_list() and idx is None:
            return False

        v: str = self.get_item(idx)
        return v == KgtkFormat.TRUE_SYMBOL or v == KgtkFormat.FALSE_SYMBOL

    
    def is_language_qualified_string(self, idx: typing.Optional[int] = None)->bool:
        """
        Return False if this value is a list and idx is None.
        Otherwise, return True if the first character is '
        """
        if self.is_list() and idx is None:
            return False

        v: str = self.get_item(idx)
        return v.startswith("'")

    language_qualified_string_re: typing.Pattern = re.compile(r"^(?P<string>'(?:[^']|\\.)*')@(?P<lang>[a-zA-Z][a-zA-Z])$")

    def is_valid_language_qualified_string(self, idx: typing.Optional[int] = None)->bool:
        """
        Return False if this value is a list and idx is None.
        Otherwise, return True if the value looks like a language-qualified string.
        """
        if self.is_list() and idx is None:
            return False

        v: str = self.get_item(idx)
        m: typing.Optional[typing.Match] = KgtkValue.language_qualified_string_re.match(v)
        if m is None:
            return False

        # Validate the language code:
        lang: str = m.group("lang")
        # print("lang: %s" % lang)
        try:
            languages.get(alpha2=lang.lower())
            return True
        except KeyError:
            return False

    def is_location_coordinates(self, idx: typing.Optional[int] = None)->bool:
        """
        Return False if this value is a list and idx is None.
        Otherwise, return True if the first character is @
        """
        if self.is_list() and idx is None:
            return False

        v: str = self.get_item(idx)
        return v.startswith("@")

    location_coordinates_re: typing.Pattern = re.compile(r"^@[-+]?\d{3}\.\d{5}/[-+]?\d{3}\.\d{5}$")

    def is_valid_location_coordinates(self, idx: typing.Optional[int] = None)->bool:
        """
        Return False if this value is a list and idx is None.
        Otherwise, return True if the value looks like valid location coordinates.
        """
        if self.is_list() and idx is None:
            return False

        v: str = self.get_item(idx)
        m: typing.Optional[typing.Match] = KgtkValue.location_coordinates_re.match(v)
        return m is not None

    def is_date_and_times(self, idx: typing.Optional[int] = None)->bool:
        """
        Return False if this value is a list and idx is None.
        Otherwise, return True if the first character is ^
        """
        if self.is_list() and idx is None:
            return False

        v: str = self.get_item(idx)
        return v.startswith("^")

    date_and_times_re: typing.Pattern = re.compile(r"^\^(?P<year>[0-9]{4})(?P<hyphen>-)?(?P<month>1[0-2]|0[1-9])(?(hyphen)-)(?P<day>3[01]|0[1-9]|[12][0-9])T(?P<hour>2[0-3]|[01][0-9])(?(hyphen):)(?P<minute>[0-5][0-9])(?(hyphen):)(?P<second>[0-5][0-9])(?P<zone>Z|\+[0-9][0-9](?::[0-9][0-9])?)?(?P<precision>/[0-9])?$")

    def is_valid_date_and_times(self, idx: typing.Optional[int] = None)->bool:
        """
        Return False if this value is a list and idx is None.
        Otherwise, return True if the value looks like valid date and times
        literal based on ISO-8601.
        """
        if self.is_list() and idx is None:
            return False

        v: str = self.get_item(idx)
        m: typing.Optional[typing.Match] = KgtkValue.date_and_times_re.match(v)
        return m is not None

    def is_extension(self,  idx: typing.Optional[int] = None)->bool:
        """
        Return False if this value is a list and idx is None.
        Otherwise, return True if the first character is !
        """
        if self.is_list() and idx is None:
            return False

        v: str = self.get_item(idx)
        return v.startswith("!")

        
    def is_valid_literal(self, idx: typing.Optional[int] = None)->bool:
        """
        Return False if this value is a list and idx is None.
        Otherwise, return True if the value looks like a valid literal.
        """
        if self.is_list() and idx is None:
            return False

        if self.is_string(idx):
            return self.is_valid_string(idx)
        elif self.is_number(idx):
            return self.is_valid_number(idx)
        elif self.is_structured_literal(idx):
            if self.is_language_qualified_string(idx):
                return self.is_valid_language_qualified_string(idx)
            elif self.is_location_coordinates(idx):
                return self.is_valid_location_coordinates(idx)
            elif self.is_date_and_times(idx):
                return self.is_valid_date_and_times(idx)
            elif self.is_extension(idx):
                return False # no validation presently available.
            else:
                return False # Quantities will reach here at present.
        else:
            return False

    def is_valid_item(self, idx: typing.Optional[int] = None)->bool:
        if self.is_list() and idx is None:
            return False

        if self.is_empty(idx):
            return True
        elif self.is_valid_literal(idx):
            return True
        else:
            return self.is_symbol(idx) # Should always be True

    def is_valid(self)->bool:
        """
        Is this a valid KGTK cell value?  If the value is a list, are all the
        components valid?
        """        
        result: bool = True
        kv: KgtkValue
        for kv in self.get_values():
            result = result and kv.is_valid_item()
        return result

    def describe(self, idx: typing.Optional[int] = None)->str:
        """
        Return False if this value is a list and idx is None.
        Otherwise, return a string that descrubes the value.
        """
        if self.is_list() and idx is None:
            result: str = ""
            kv: KgtkValue
            first: bool = True
            for kv in self.get_values():
                if first:
                    first = not first
                else:
                    result += KgtkFormat.LIST_SEPARATOR
                result += kv.describe()
            return result

        if self.is_empty(idx):
            return "Empty"
        elif self.is_string(idx):
            if self.is_valid_string(idx):
                return "String"
            else:
                return "Invalid String"
        elif self.is_number(idx):
            if self.is_valid_number(idx):
                return "Number"
            else:
                return "Invalid Number"
        elif self.is_structured_literal(idx):
            if self.is_language_qualified_string(idx):
                if self.is_valid_language_qualified_string(idx):
                    return "Language Qualified String"
                else:
                    return "Invalid Language Qualified String"
            elif self.is_location_coordinates(idx):
                if self.is_valid_location_coordinates(idx):
                    return "Location Coordinates"
                else:
                    return "Invalid Location Coordinates"
            elif self.is_date_and_times(idx):
                if self.is_valid_date_and_times(idx):
                    return "Date and Times"
                else:
                    return "Invalid Date and Times"
            elif self.is_extension(idx):
                return "Extension (unvalidated)"
            else:
                return "Invalid Structured Literal"
        else:
            return "Symbol"

def main():
    """
    Test the KGTK value vparser.
    """
    parser = ArgumentParser()
    parser.add_argument(dest="values", help="The values(s) to test", type=str, nargs="+")
    parser.add_argument("-v", "--verbose", dest="verbose", help="Print additional progress messages.", action='store_true')
    parser.add_argument(      "--very-verbose", dest="very_verbose", help="Print additional progress messages.", action='store_true')
    args = parser.parse_args()

    value: str
    for value in args.values:
        print("%s: %s" % (value, KgtkValue(value).describe()))

if __name__ == "__main__":
    main()
