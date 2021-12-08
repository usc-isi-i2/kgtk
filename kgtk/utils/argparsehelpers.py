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
                    metavar="True|False",
                    type=optional_bool, nargs='?', const=True, **d(default=False))

type=optional_bool      This says that the argument is an optional boolean.

nargs='?'               This says that the optional boolean can optionally take one
                        argument itself (True or False).

const=True              This says that if the optional boolean is present *without*
                        a following True or False, the value is True.

                        e.g.:
                        --gzip-in-parallel              means True
                        --gzip-in-parallel=True         means True
                        --gzip-in-parallel True         means True
                        --gzip-in-parallel=False        means False
                        --gzip-in-parallel False        means False
                        

default=False           This says that if the optional boolean isn't present at
                        all, the default value is True.

                        e.g.:
                        (--gzip-in-parallel isn't specified) means False

metavar="True|False"    The argument value are True or False (ignoring case).
                        Other values are also supported: f or t, 0 or 1, no or yes,
                        n or y.

In order for optional booleans to work, the following *must* be present:

nargs='?'
const=True
default=False

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
