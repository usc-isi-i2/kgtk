"""This argparse type conversion function implements optional boolean arguments.

--arg
--arg=True
--arg=False

and other variations.  A default value of None is allowed for fallback
argument composition.

Sample usage:

parser.add_argument(prefix1 + "gzip-in-parallel",
                    dest=prefix2 + "gzip_in_parallel",
                    help=h(prefix3 + "Execute gzip in parallel (default=%(default)s)."),
                    type=optional_bool, nargs='?', const=True, **d(default=False))

"""

import typing
from kgtk.exceptions import KGTKArgumentParseException


def optional_bool(value) -> typing.Optional[bool]:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if value.lower() in {'false', 'f', '0', 'no', 'n'}:
        return False
    elif value.lower() in {'true', 't', '1', 'yes', 'y'}:
        return True
    raise KGTKArgumentParseException(f'{value} is not a valid boolean value')
