"""
Constants and helpers for the KGTK file format.

"""

from enum import Enum
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

    class DataTypes(Enum):
        NUMBER = 0
        STRING = 1
        STRUCTURED_LITERAL = 2
        SYMBOL = 3

    TRUE_SYMBOL: str = "True"
    FALSE_SYMBOL: str = "False"
