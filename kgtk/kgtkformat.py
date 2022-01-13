"""
Constants and helpers for the KGTK file format.

"""

import ast
import datetime as dt
from enum import Enum, unique
import sys
import typing

class KgtkFormat:
    COLUMN_SEPARATOR: str = "\t"
    COMMENT_INDICATOR: str = "#"
    LIST_SEPARATOR: str = "|"

    # This value will be used to seperate fields when building a composit
    # sorting/grouping key.  It will work so long as \0 does not appear as
    # part of any of the key fields.
    KEY_FIELD_SEPARATOR: str = '\0'

    # These are the required columns in an edge file:
    NODE1_COLUMN_NAMES: typing.List[str] = ["node1", "from", "subject"]
    NODE2_COLUMN_NAMES: typing.List[str] = ["node2", "to", "object"]
    LABEL_COLUMN_NAMES: typing.List[str] = ["label", "predicate", "relation", "relationship"]

    # There is only one required column in a node file:
    ID_COLUMN_NAMES: typing.List[str] = ["id", "ID"]

    # These are the canonical names:
    NODE1: str = "node1"
    LABEL: str = "label"
    NODE2: str = "node2"
    ID: str = "id"

    KGTK_NAMESPACE: str = "kgtk:"

    @unique
    class DataType(Enum):
        EMPTY = 0
        LIST = 1
        NUMBER = 2
        QUANTITY = 3
        STRING = 4
        LANGUAGE_QUALIFIED_STRING = 5
        LOCATION_COORDINATES = 6
        DATE_AND_TIMES = 7
        EXTENSION = 8
        BOOLEAN = 9
        SYMBOL = 10

        def lower(self)->str:
            return self.name.lower()

        @classmethod
        def choices(cls)->typing.List[str]:
            results: typing.List[str] = [ ]
            name: str
            for name in cls.__members__.keys():
                results.append(name.lower())
            return results

    STRING_SIGIL: str = '"'
    LANGUAGE_QUALIFIED_STRING_SIGIL: str = "'"
    DATE_AND_TIMES_SIGIL: str = "^"
    LOCATION_COORDINATES_SIGIL: str = "@"

    TRUE_SYMBOL: str = "True"
    FALSE_SYMBOL: str = "False"

    @classmethod
    def to_boolean(cls, b: bool)->str:
        return cls.TRUE_SYMBOL if b else cls.FALSE_SYMBOL

    @classmethod
    def from_boolean(cls, item: str)->bool:
        return item == cls.TRUE_SYMBOL

    stringify_translate = str.maketrans({
        "\a": "\\a", # alarm (bell) - ASCII <BEL>
        "\b": "\\b", # backspace - ASCII <BS>
        "\f": "\\f", # formfeed - ASCII <FF>
        "\n": "\\n", # newline (linefeed) - ASCII <LF>
        "\r": "\\r", # carriage return -- ASCII <CR>
        "\t": "\\t", # horizontal tab - ASCII <TAB>
        "\v": "\\v", # vertical tab - ASCII <VT>
        "\\" : "\\\\", # backslash  - (\)
        "'": "\\'", # single quote - (')
        '"': '\\"', # double quote - (")
        LIST_SEPARATOR: "\\" + LIST_SEPARATOR, # vertical bar (pipe) - (|)
    })

    @classmethod
    def stringify(cls,
                  s: str,
                  language: str = "",
                  language_suffix: str = "",
    )->str:
        """Convert an internal string into a KGTK format string.  The internal string
        shouldn't have any "\" escaped characters.  For example, <TAB>
        characters should be ASCII tabs, not the two-character sequence
        backslash t ("\t").

        If a language code is provided, then a KGTK language qualified string
        is produced.  Otherwise, an ordinary KGTK string is produced.  In both
        cases, internal single and doublle quotes are both protected by
        backslashes.

        TODO: Should we octal encode <NUL>, <DEL> and any remaining ASCII control characters?
        """
        if len(language) == 0:
            return cls.STRING_SIGIL + s.translate(KgtkFormat.stringify_translate) + cls.STRING_SIGIL
        else:
            return cls.LANGUAGE_QUALIFIED_STRING_SIGIL + s.translate(KgtkFormat.stringify_translate) + "'@" + language + language_suffix

    @classmethod
    def unstringify(cls, s: str, unescape_pipe: bool = True)->str:
        """Convert a KGTK formatted string into an internal string.  The language
        code and suffix are not returned.
        """
        if s.startswith(cls.LANGUAGE_QUALIFIED_STRING_SIGIL):
            language: str
            s, language = s.rsplit("@", 1)
        if unescape_pipe:
            s = s.replace('\\|', '|')
        return ast.literal_eval(s)

    @classmethod
    def destringify(cls, s: str)->typing.Tuple[str, str, str]:
        """Convert a KGTK formatted string into an internal string.  The language
        code and suffix are returned.  Language and language_suffix are returned as empty
        strings when they are not present.

        For the moment, we'll assume that the language and language suffix don't
        conatain any escape sequences.
        """
        language: str = ""
        language_suffix: str = ""
        if s.startswith(cls.LANGUAGE_QUALIFIED_STRING_SIGIL):
            s, language = s.rsplit("@", 1)
            if "-" in language:
                language, language_suffix = language.split("-", 1)
                language_suffix = "-" + language_suffix
        s = s.replace('\\|', '|')
        return (ast.literal_eval(s), language, language_suffix)
    
    @classmethod
    def year(cls, year: typing.Union[int, str])->str:
        """Convert a year (passed as an integer or string) to a KGTK value for the year as a period.
        """
        yearstr: str
        if isinstance(year, int):
            yearstr = str(year)
        else:
            yearstr = year
        return cls.DATE_AND_TIMES_SIGIL + yearstr + "-01-01T00:00:00/9"

    @classmethod
    def year_month(cls,
                   year: typing.Union[int, str],
                   month: typing.Union[int, str])->str:
        """Convert a year and month (passed as integers or strings) to a KGTK value for the period.
        """
        yearstr: str
        if isinstance(year, int):
            yearstr = str(year)
        else:
            yearstr = year

        monthstr: str
        if isinstance(month, int):
            monthstr = str(month)
        else:
            monthstr = month
        if len(monthstr) == 1:
            monthstr = "0" + monthstr
        return cls.DATE_AND_TIMES_SIGIL + yearstr + "-" + monthstr + "-01T00:00:00/10"

    @classmethod
    def year_month_day(cls,
                       year: typing.Union[int, str],
                       month: typing.Union[int, str],
                       day: typing.Union[int, str],
                       )->str:
        """Convert a year, month, and day (passed as integers or strings) to a KGTK value for the period.
        """
        yearstr: str
        if isinstance(year, int):
            yearstr = str(year)
        else:
            yearstr = year

        monthstr: str
        if isinstance(month, int):
            monthstr = str(month)
        else:
            monthstr = month
        if len(monthstr) == 1:
            monthstr = "0" + monthstr

        daystr: str
        if isinstance(day, int):
            daystr = str(day)
        else:
            daystr = day
        if len(daystr) == 1:
            daystr = "0" + daystr

        return cls.DATE_AND_TIMES_SIGIL + yearstr + "-" + monthstr + "-" + daystr + "T00:00:00/11"

    @classmethod
    def from_datetime(cls, d: dt.datetime, precision: typing.Optional[typing.Union[int, str]]=None)->str:
        if precision is None:
            return cls.DATE_AND_TIMES_SIGIL + dt.isoformat()
        else:
            return cls.DATE_AND_TIMES_SIGIL + dt.isoformat() + "/" + str(precision)
            

    @classmethod
    def lat_lon(cls, lat: typing.Union[int, float], lon: typing.Union[int, float])->str:
        return cls.LOCATION_COORDINATES_SIGIL + str(lat) + '/' + str(lon)
