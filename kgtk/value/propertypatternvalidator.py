"""
Validate property patterns..
"""

from argparse import ArgumentParser, Namespace
import attr
from enum import Enum
import re
import typing

from kgtk.value.kgtkvalue import KgtkValue

@attr.s(slots=True, frozen=True)
class PropertyPattern:
    class Action(Enum):
        NODE1_TYPE = "node1_type"
        NODE2_TYPE = "node2_type"
        NOT_IN = "not_in"
        LABEL_COLUM = "label_column"
        NODE1_COLUMN = "node1_column"
        NODE2_COLUMN = "node2_column"
        NODE1_VALUES = "node1_values"
        NODE2_VALUES = "node2_values"
        MINVAL = "minval"
        MAXVAL = "maxval"
        MINOCCURS = "minoccurs"
        MAXOCCURS = "maxoccurs"
        ISA = "isa"
        MATCHES = "matches"
        NODE1_PATTERN = "node1_pattern"
        NODE2_PATTERN = "node2_pattern"
        LABEL_PATTERN = "label_pattern"
        MINDISTINCT = "mindistinct"
        MAXDISTINCT = "maxdistinct"
        REQUIRED_IN = "required_id"
        MINDATE = "mindate"
        MAXDATE = "maxdate"
        
    node1_value: KgtkValue = attr.ib(validator=attr.validators.instance_of(KgtkValue))
    label_value: KgtkValue = attr.ib(validator=attr.validators.instance_of(KgtkValue))
    node2_value: KgtkValue = attr.ib(validator=attr.validators.instance_of(KgtkValue))

    # TODO: create validators:
    action: Action = attr.ib()
    pattern: typing.Optional[typing.Pattern] = attr.ib()
    intval: typing.Optional[int] = attr.ib()
    number: typing.Optional[float] = attr.ib()
    column_names: typing.List[str] = attr.ib()
    value: str = attr.ib()

    @classmethod
    def new(cls, node1_value: KgtkValue, label_value: KgtkValue, node2_value: KgtkValue)->'PropertyPattern':
        action: cls.Action = cls.Action(label_value.value)

        pattern: typing.Optional[typing.Pattern] = None
        if action in (cls.Action.NODE1_PATTERN,
                      cls.Action.NODE2_PATTERN,
                      cls.Action.LABEL_PATTERN,
                      cls.Action.MATCHES):
            if node2_value.fields is None:
                raise ValueError("%s: Node2 has no fields" % (action.value)) # TODO: better complaint
            if node2_value.fields.text is None:
                raise ValueError("%s: Node2 has no text" % (action.value)) # TODO: better complaint
                
            pattern = re.compile(node2_value.fields.text)

        intval: typing.Optional[int] = None
        if action in (cls.Action.MINOCCURS,
                      cls.Action.MAXOCCURS,
                      cls.Action.MINDISTINCT,
                      cls.Action.MAXDISTINCT):
            if node2_value.fields is None:
                raise ValueError("%s: Node2 has no fields" % (action.value)) # TODO: better complaint
            if node2_value.fields.number is None:
                raise ValueError("%s: Node2 has no number" % (action.value)) # TODO: better complaint
            intval = int(node2_value.fields.number)

        number: typing.Optional[float] = None
        if action in(cls.Action.MINVAL,
                     cls.Action.MAXVAL):
            if node2_value.fields is None:
                raise ValueError("%s: Node2 has no fields" % (action.value)) # TODO: better complaint
            if node2_value.fields.number is None:
                raise ValueError("%s: Node2 has no number" % (action.value)) # TODO: better complaint
            number = float(node2_value.fields.number)

        column_names: typing.List[str] = [ ]
        if action in (cls.Action.NOT_IN,):
            if label_value.is_symbol:
                column_names.append(label_value.value)
            elif label_value.is_list:
                kv: KgtkValue
                for kv in label_value.get_list_items:
                    if kv.is_symbol:
                        column_names.append(kv.value)
                    else:
                        raise ValueError("%s: List value is not a symbol" % (action.value)) # TODO: better complaint
            else:
                raise ValueError("%s:Value is not a symbol or list of symbols" % (action.value)) # TODO: better complaint
            # TODO: validate that the column names are valid and get their indexes.

        if action in (cls.Action.LABEL_COLUM,
                      cls.Action.NODE1_COLUMN,
                      cls.Action.NODE2_COLUMN,
                      cls.Action.REQUIRED_IN):
            if label_value.is_symbol:
                column_names.append(label_value.value)
            else:
                raise ValueError("%s:Value is not a symbol" % (action.value)) # TODO: better complaint
            # TODO: validate that the column names are valid and get their indexes.

        value: str = ""
        if action in (cls.Action.NODE1_TYPE,
                      cls.Action.NODE2_TYPE,
                      cls.Action.ISA):
            value = node2_value.value
                        

        return cls(node1_value, label_value, node2_value, action, pattern, intval, number, column_names, value)

@attr.s(slots=True, frozen=True)
class PropertyPatternValidator:
    pass
