"""
SQLStore and Kypher utilities.
"""

import math
from   odictliteral import odict
import pprint
import re

import sh

from   kgtk.exceptions import KGTKException

pp = pprint.PrettyPrinter(indent=4)


### Utilities

def listify(x):
    return (hasattr(x, '__iter__') and not isinstance(x, str) and list(x)) or (x and [x]) or []

# TO DO: I am sure some form of this already exists somewhere in Craig's code

def open_to_read(file, mode='rt'):
    """Version of 'open' that is smart about different types of compressed files
    and file-like objects that are already open to read.  'mode' has to be a
    valid read mode such as 'r', 'rb' or 'rt'.
    """
    assert mode in ('r', 'rb', 'rt'), 'illegal read mode'
    enc = 't' in mode and 'utf8' or None
    if isinstance(file, str) and file.endswith('.gz'):
        import gzip
        return gzip.open(file, mode, encoding=enc)
    elif isinstance(file, str) and file.endswith('.bz2'):
        import bz2
        return bz2.open(file, mode, encoding=enc)
    elif isinstance(file, str) and file.endswith('.xz'):
        import lzma
        return lzma.open(file, mode, encoding=enc)
    elif hasattr(file, 'read'):
        return file
    else:
        return open(file, mode)

def open_to_write(file, mode='wt'):
    """Version of 'open' that is smart about different types of compressed files
    and file-like objects that are already open to write.  'mode' has to be a
    valid write mode such as 'w', 'wb' or 'wt'.
    """
    assert mode in ('w', 'wb', 'wt'), 'illegal write mode'
    enc = 't' in mode and 'utf8' or None
    if isinstance(file, str) and file.endswith('.gz'):
        import gzip
        return gzip.open(file, mode, encoding=enc)
    elif isinstance(file, str) and file.endswith('.bz2'):
        import bz2
        return bz2.open(file, mode, encoding=enc)
    elif isinstance(file, str) and file.endswith('.xz'):
        import lzma
        return lzma.open(file, mode, encoding=enc)
    elif hasattr(file, 'write'):
        return file
    else:
        return open(file, mode)

def get_cat_command(file, _piped=False):
    """Return a cat-like sh-command to copy the possibly compressed 'file' to stdout.
    """
    # This works around some cross-platform issues with similar functionality in zconcat.
    if file.endswith('.gz'):
        return sh.gunzip.bake('-c', file, _piped=_piped)
    elif file.endswith('.bz2'):
        return sh.bunzip2.bake('-c', file, _piped=_piped)
    elif file.endswith('.xz'):
        return sh.unxz.bake('-c', file, _piped=_piped)
    else:
        return sh.cat.bake(file, _piped=_piped)

def format_memory_size(bytes):
    """Return a human-readable formatting of 'bytes' using powers of 1000.
    """
    units = ('Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
    factor = 1000
    if bytes < factor:
        return '%d %s' % (bytes, units[0])
    else:
        scale = min(math.floor(math.log(bytes, factor)), len(units)-1)
        return "%.2f %s" % (bytes / pow(factor, scale), units[scale])

def parse_memory_size(size):
    """Parse a human-readable 'size' spec into the corresponding number (of bytes).
    If 'size' is already an integer, return it as is.
    """
    if isinstance(size, str):
        try:
            units = 'BKMGTPEZY'
            m = re.match(f'^\s*([0-9.]+)\s*([{units}]?I?B?\s*)$', size.upper())
            number, unit = m.group(1), m.group(2)
            # K and KiB is 1024, KB is 1000 (and similar for other units):
            factor = 1000 if 'B' in unit and 'I' not in unit else 1024
            scale = units.find(unit) if len(unit) <= 1 else units.find(unit[0])
            # only coerce to float if we have to to avoid precision issues:
            number = float(number) if '.' in number else int(number)
            size = number * pow(factor, scale)
        except:
            raise KGTKException(f'illegal size spec: {size}')
    return int(size)

def sql_quote_ident(ident, quote='"'):
    # - standard SQL quoting for identifiers such as table and column names is via double quotes
    # - double quotes within identifiers can be escaped via two double quotes
    # - sqlite also supports MySQL's backtick syntax and SQLServer's [] syntax
    return quote + ident.replace(quote, quote+quote) + quote


class sdict(odict):
    """Ordered schema dict that supports property access of its elements.
    """
    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def __setattr__(self, name, value):
        self[name] = value

    def __repr__(self):
        """Create an eval-able repr that will recreate 'self' identically."""
        if len(self) == 0:
            return "sdict()"
        else:
            return "sdict[%s]" % (", ".join("%s: %s" % (repr(k),repr(v)) for k,v in self.items()),)
