from argparse import Action
from enum import Enum

class EnumNameAction(Action):
    """
    Argparse action for handling Enums

    Adapted from:
    https://stackoverflow.com/questions/43968006/support-for-enum-arguments-in-argparse
    """
    def __init__(self, **kwargs):
        # Pop off the type value
        enum = kwargs.pop("type", None)

        # Ensure an Enum subclass is provided
        if enum is None:
            raise ValueError("type must be assigned an Enum when using EnumNameAction")
        if not issubclass(enum, Enum):
            raise TypeError("type must be an Enum when using EnumNameAction")

        # Generate choices from the Enum
        kwargs.setdefault("choices", tuple(e.name for e in enum))

        super().__init__(**kwargs)

        self._enum = enum

    def __call__(self, parser, namespace, values, option_string=None):
        # Convert value back into an Enum
        enum = self._enum[values]
        setattr(namespace, self.dest, enum)

class EnumLowerNameAction(Action):
    """
    Argparse action for handling Enums, presenting the choices in lower case
    but accepting inputs independent of case.  It assumes that the Enum
    member names are upper case.

    Adapted from:
    https://stackoverflow.com/questions/43968006/support-for-enum-arguments-in-argparse
    https://stackoverflow.com/questions/27616778/case-insensitive-argparse-choices

    """
    class cilist(list):
        def __contains__(self, other):
            # Convert to lower case for the comparison, since
            # the list was built in lower case.
            return super().__contains__(other.lower())

    def __init__(self, **kwargs):
        # Pop off the type value
        enum = kwargs.pop("type", None)

        # Ensure an Enum subclass is provided
        if enum is None:
            raise ValueError("type must be assigned an Enum when using EnumNameAction")
        if not issubclass(enum, Enum):
            raise TypeError("type must be an Enum when using EnumNameAction")

        # Generate choices from the Enum, converting the names to lower case:
        kwargs.setdefault("choices", self.cilist(e.name.lower() for e in enum))

        super().__init__(**kwargs)

        self._enum = enum

    def __call__(self, parser, namespace, values, option_string=None):
        # Convert value back into an Enum
        enum = self._enum[values.upper()]
        setattr(namespace, self.dest, enum)

class EnumUpperNameAction(Action):
    """
    Argparse action for handling Enums, presenting the choices in upper case
    but accepting inputs independent of case.  It assumes that the Enum
    member names are upper case.

    Adapted from:
    https://stackoverflow.com/questions/43968006/support-for-enum-arguments-in-argparse
    https://stackoverflow.com/questions/27616778/case-insensitive-argparse-choices

    """
    class cilist(list):
        def __contains__(self, other):
            # Convert to upper case for the comparison, since
            # the list was built in upper case.
            return super().__contains__(other.upper())

    def __init__(self, **kwargs):
        # Pop off the type value
        enum = kwargs.pop("type", None)

        # Ensure an Enum subclass is provided
        if enum is None:
            raise ValueError("type must be assigned an Enum when using EnumNameAction")
        if not issubclass(enum, Enum):
            raise TypeError("type must be an Enum when using EnumNameAction")

        # Generate choices from the Enum, converting the names to upper case:
        kwargs.setdefault("choices", self.cilist(e.name.upper() for e in enum))

        super().__init__(**kwargs)

        self._enum = enum

    def __call__(self, parser, namespace, values, option_string=None):
        # Convert value back into an Enum
        enum = self._enum[values.upper()]
        setattr(namespace, self.dest, enum)
