"""
Constants and helpers for the KGTK file format.

"""

from enum import Enum, unique
import sys
import typing

class KgtkFormat:
    COLUMN_SEPARATOR: str = "\t"
    COMMENT_INDICATOR: str = "#"
    LIST_SEPARATOR: str = "|"

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

    TRUE_SYMBOL: str = "True"
    FALSE_SYMBOL: str = "False"
