"""
Constants and helpers for the KGTK file format.

"""

import ast
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
            return '"' + s.translate(KgtkFormat.stringify_translate) + '"'
        else:
            return "'" + s.translate(KgtkFormat.stringify_translate) + "'@" + language + language_suffix

    @classmethod
    def unstringify(cls, s: str, unescape_pipe: bool = True)->str:
        """Convert a KGTK formatted string into an internal string.  The language
        code and suffix are not returned.
        """
        if s.startswith("'"):
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
        if s.startswith("'"):
            s, language = s.rsplit("@", 1)
            if "-" in language:
                language, language_suffix = language.split("-", 1)
                language_suffix = "-" + language_suffix
        s = s.replace('\\|', '|')
        return (ast.literal_eval(s), language, language_suffix)
    
