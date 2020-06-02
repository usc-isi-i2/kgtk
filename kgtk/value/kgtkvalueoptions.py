"""
KGTK value processing options.

TODO: Instead of clamping invalid lat/lon values, perhaps we'd
want to modulo them?
"""

from argparse import ArgumentParser, Namespace, SUPPRESS
import attr
import sys
import typing

from kgtk.utils.argparsehelpers import optional_bool

@attr.s(slots=True, frozen=True)
class KgtkValueOptions:
    """
    These options control various aspects of value processing. They are in a
    seperate class for code isolation and efficiency.

    """
    
    # Allow a laxer definition of the Qnode suffix in quantities.
    allow_lax_qnodes: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    # Allow month 00 or day 00 in dates?  This isn't really allowed by ISO
    # 8601, but appears in wikidata.
    allow_month_or_day_zero: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    repair_month_or_day_zero: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    # When allow_lax_strings is true, strings will be checked to see if they
    # start and end with double quote ("), but we won't check if internal
    # double quotes are excaped by backslash.
    allow_lax_strings: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    # When allow_lax_lq_strings is true, language qualified strings will be
    # checked to see if they start and end with single quote ('), but we won't
    # check if internal single quotes are excaped by backslash.
    allow_lax_lq_strings: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    
    allow_language_suffixes: bool = attr.ib(validator=attr.validators.instance_of(bool), default=True)

    # If this list gets long, we may want to turn it into a map to make lookup
    # more efficient.
    #
    # TODO: fix this validation
    # additional_language_codes: typing.Optional[typing.List[str]] = attr.ib(validator=attr.validators.deep_iterable(member_validator=attr.validators.instance_of(str),
    #                                                                                              iterable_validator=attr.validators.instance_of(list)))),
    additional_language_codes: typing.Optional[typing.List[str]] = attr.ib(default=None)

    escape_list_separators: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    # When repair_lax_coordinates is true, coordinates using scientific notation
    # will be parsed.
    allow_lax_coordinates: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    # When repair_lax_coordinates is true, coordinates using scientific notation
    # will be parsed, but they will be rewritten to fixed point notation.
    repair_lax_coordinates: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    # Minimum and maximum year range in dates.
    MINIMUM_VALID_YEAR: int = 1583 # Per ISO 8601, years before this one require special agreement.
    minimum_valid_year: int = attr.ib(validator=attr.validators.instance_of(int), default=MINIMUM_VALID_YEAR)
    clamp_minimum_year: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    MAXIMUM_VALID_YEAR: int = 2100 # Arbitrarily chosen.
    maximum_valid_year: int = attr.ib(validator=attr.validators.instance_of(int), default=MAXIMUM_VALID_YEAR)
    clamp_maximum_year: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    MINIMUM_VALID_LAT: float = -90.
    minimum_valid_lat: float = attr.ib(validator=attr.validators.instance_of(float), default=MINIMUM_VALID_LAT)
    clamp_minimum_lat: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    MAXIMUM_VALID_LAT: float = 90.
    maximum_valid_lat: float = attr.ib(validator=attr.validators.instance_of(float), default=MAXIMUM_VALID_LAT)
    clamp_maximum_lat: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    
    MINIMUM_VALID_LON: float = -180.
    minimum_valid_lon: float = attr.ib(validator=attr.validators.instance_of(float), default=MINIMUM_VALID_LON)
    clamp_minimum_lon: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    MAXIMUM_VALID_LON: float = 180.
    maximum_valid_lon: float = attr.ib(validator=attr.validators.instance_of(float), default=MAXIMUM_VALID_LON)
    clamp_maximum_lon: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)
    
    modulo_repair_lon: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

    @classmethod
    def add_arguments(cls,
                      parser: ArgumentParser,
                      who: str = "",
                      desc: str = ".",
                      expert: bool = False,
                      defaults: bool = True,
    ):
        """Add arguments for KgtkValue option processing.

        When "who" is not empty, it prefixes the options, destinations, and
        help messages.  This facilitates constructing command lines with
        multiple sets of KGTKValue options, such as for different input files.
        """
        prefix1: str = "--" # The command line argument prefix.
        prefix2: str = ""   # The destination name prefix.
        prefix3: str = ""   # The help message prefix.

        if len(who) > 0:
            prefix1 = "--" + who + "-"
            prefix2 = who + "_"
            prefix3 = who + ": "
        
        # This helper function makes it easy to suppress options from
        # The help message.  The options are still there, and initialize
        # what they need to initialize.
        def h(msg: str)->str:
            if expert:
                return msg
            else:
                return SUPPRESS

        # This helper function decices whether or not to include defaults
        # in argument declarations. If we plan to make arguments with
        # prefixes and fallbacks, the fallbacks (the ones without prefixes)
        # should get defaults value, while the prefixed arguments should
        # not get defaults.
        #
        # Note: In obscure circumstances (EnumNameAction, I'm looking at you),
        # explicitly setting "default=None" may fail, whereas omitting the
        # "default=" phrase succeeds.
        #
        # TODO: continue researching these issues.
        def d(default: typing.Any)->typing.Mapping[str, typing.Any]:
            if defaults:
                return {"default": default}
            else:
                return { }

        vgroup = parser.add_argument_group(h(prefix3 + "Data value parsing"),
                                           h("Options controlling the parsing and processing of KGTK data values" + desc))
        vgroup.add_argument(      prefix1 + "additional-language-codes", dest=prefix2 + "additional_language_codes",
                                  help=h(prefix3 + "Additional language codes. (default=None)."),
                                  nargs="*", default=None)

        vgroup.add_argument(      prefix1 + "allow-lax-qnodes", dest=prefix2 + "allow_lax_qnodes",
                                  help=h(prefix3 + "Allow qnode suffixes in quantities to include alphas and dash as well as digits. (default=%(default)s)."),
                                  type=optional_bool, nargs='?', const=True, **d(default=False))

        vgroup.add_argument(      prefix1 + "allow-language-suffixes", dest=prefix2 + "allow_language_suffixes",
                                   help=h(prefix3 + "Allow language identifier suffixes starting with a dash. (default=%(default)s)."),
                                   type=optional_bool, nargs='?', const=True, **d(default=False))

        vgroup.add_argument(      prefix1 + "allow-lax-strings", dest=prefix2 + "allow_lax_strings",
                                  help=h(prefix3 + "Do not check if double quotes are backslashed inside strings. (default=%(default)s)."),
                                  type=optional_bool, nargs='?', const=True, **d(default=False))

        vgroup.add_argument(      prefix1 + "allow-lax-lq-strings", dest=prefix2 + "allow_lax_lq_strings",
                                  help=h(prefix3 + "Do not check if single quotes are backslashed inside language qualified strings. (default=%(default)s)."),
                                  type=optional_bool, nargs='?', const=True, **d(default=False))

        vgroup.add_argument(      prefix1 + "allow-month-or-day-zero", dest=prefix2 + "allow_month_or_day_zero",
                                  help=h(prefix3 + "Allow month or day zero in dates. (default=%(default)s)."),
                                  type=optional_bool, nargs='?', const=True, **d(default=False))

        vgroup.add_argument(      prefix1 + "repair-month-or-day-zero", dest=prefix2 + "repair_month_or_day_zero",
                                  help=h(prefix3 + "Repair month or day zero in dates. (default=%(default)s)."),
                                  type=optional_bool, nargs='?', const=True, **d(default=False))

        vgroup.add_argument(      prefix1 + "minimum-valid-year", dest=prefix2 + "minimum_valid_year",
                                  help=h(prefix3 + "The minimum valid year in dates. (default=%(default)d)."),
                                  type=int, **d(default=cls.MINIMUM_VALID_YEAR))

        vgroup.add_argument(      prefix1 + "clamp-minimum-year", dest=prefix2 + "clamp_minimum_year",
                                  help=h(prefix3 + "Clamp years at the minimum value. (default=%(default)s)."),
                                  type=optional_bool, nargs='?', const=True, **d(default=False))

        vgroup.add_argument(      prefix1 + "maximum-valid-year", dest=prefix2 + "maximum_valid_year",
                                  help=h(prefix3 + "The maximum valid year in dates. (default=%(default)d)."),
                                  type=int, **d(default=cls.MAXIMUM_VALID_YEAR))

        vgroup.add_argument(      prefix1 + "clamp-maximum-year", dest=prefix2 + "clamp_maximum_year",
                                  help=h(prefix3 + "Clamp years at the maximum value. (default=%(default)s)."),
                                  type=optional_bool, nargs='?', const=True, **d(default=False))

        vgroup.add_argument(      prefix1 + "allow-lax-coordinates", dest=prefix2 + "allow_lax_coordinates",
                                  help=h(prefix3 + "Allow coordinates using scientific notation. (default=%(default)s)."),
                                  type=optional_bool, nargs='?', const=True, **d(default=False))

        vgroup.add_argument(      prefix1 + "repair-lax-coordinates", dest=prefix2 + "repair_lax_coordinates",
                                  help=h(prefix3 + "Allow coordinates using scientific notation. (default=%(default)s)."),
                                  type=optional_bool, nargs='?', const=True, **d(default=False))

        vgroup.add_argument(      prefix1 + "minimum-valid-lat", dest=prefix2 + "minimum_valid_lat",
                                  help=h(prefix3 + "The minimum valid latitude. (default=%(default)f)."),
                                  type=int, **d(default=cls.MINIMUM_VALID_LAT))

        vgroup.add_argument(      prefix1 + "clamp-minimum-lat", dest=prefix2 + "clamp_minimum_lat",
                                  help=h(prefix3 + "Clamp latitudes at the minimum value. (default=%(default)s)."),
                                  type=optional_bool, nargs='?', const=True, **d(default=False))

        vgroup.add_argument(      prefix1 + "maximum-valid-lat", dest=prefix2 + "maximum_valid_lat",
                                  help=h(prefix3 + "The maximum valid latitude. (default=%(default)f)."),
                                  type=int, **d(default=cls.MAXIMUM_VALID_LAT))

        vgroup.add_argument(      prefix1 + "clamp-maximum-lat", dest=prefix2 + "clamp_maximum_lat",
                                  help=h(prefix3 + "Clamp latitudes at the maximum value. (default=%(default)s)."),
                                  type=optional_bool, nargs='?', const=True, **d(default=False))

        vgroup.add_argument(      prefix1 + "minimum-valid-lon", dest=prefix2 + "minimum_valid_lon",
                                  help=h(prefix3 + "The minimum valid longitude. (default=%(default)f)."),
                                  type=int, **d(default=cls.MINIMUM_VALID_LON))

        vgroup.add_argument(      prefix1 + "clamp-minimum-lon", dest=prefix2 + "clamp_minimum_lon",
                                  help=h(prefix3 + "Clamp longitudes at the minimum value. (default=%(default)s)."),
                                  type=optional_bool, nargs='?', const=True, **d(default=False))

        vgroup.add_argument(      prefix1 + "maximum-valid-lon", dest=prefix2 + "maximum_valid_lon",
                                  help=h(prefix3 + "The maximum valid longitude. (default=%(default)f)."),
                                  type=int, **d(default=cls.MAXIMUM_VALID_LON))

        vgroup.add_argument(      prefix1 + "clamp-maximum-lon", dest=prefix2 + "clamp_maximum_lon",
                                  help=h(prefix3 + "Clamp longitudes at the maximum value. (default=%(default)s)."),
                                  type=optional_bool, nargs='?', const=True, **d(default=False))

        vgroup.add_argument(      prefix1 + "modulo-repair-lon", dest=prefix2 + "modulo_repair_lon",
                                  help=h(prefix3 + "Wrap longitude to (-180.0,180.0]. (default=%(default)s)."),
                                  type=optional_bool, nargs='?', const=True, **d(default=False))

        vgroup.add_argument(      prefix1 + "escape-list-separators", dest=prefix2 + "escape_list_separators",
                                  help=h(prefix3 + "Escape all list separators instead of splitting on them. (default=%(default)s)."),
                                  type=optional_bool, nargs='?', const=True, **d(default=False))

    @classmethod
    # Build the value parsing option structure.
    def from_dict(cls, d: dict, who: str = "")->'KgtkValueOptions':
        prefix: str = ""   # The destination name prefix.
        if len(who) > 0:
            prefix = who + "_"

        return cls(allow_lax_qnodes=d.get(prefix + "allow_lax_qnodes", False),
                   allow_month_or_day_zero=d.get(prefix + "allow_month_or_day_zero", False),
                   repair_month_or_day_zero=d.get(prefix + "repair_month_or_day_zero", False),
                   allow_language_suffixes=d.get(prefix + "allow_language_suffixes", True),
                   allow_lax_strings=d.get(prefix + "allow_lax_strings", False),
                   allow_lax_lq_strings=d.get(prefix + "allow_lax_lq_strings", False),
                   additional_language_codes=d.get(prefix + "additional_language_codes", None),
                   minimum_valid_year=d.get(prefix + "minimum_valid_year", cls.MINIMUM_VALID_YEAR),
                   clamp_minimum_year=d.get(prefix + "clamp_minimum_year", False),
                   maximum_valid_year=d.get(prefix + "maximum_valid_year", cls.MAXIMUM_VALID_YEAR),
                   clamp_maximum_year=d.get(prefix + "clamp_maximum_year", False),

                   allow_lax_coordinates=d.get(prefix + "allow_lax_coordinates", False),
                   repair_lax_coordinates=d.get(prefix + "repair_lax_coordinates", False),

                   minimum_valid_lat=d.get(prefix + "minimum_valid_lat", cls.MINIMUM_VALID_LAT),
                   clamp_minimum_lat=d.get(prefix + "clamp_minimum_lat", False),
                   maximum_valid_lat=d.get(prefix + "maximum_valid_lat", cls.MAXIMUM_VALID_LAT),
                   clamp_maximum_lat=d.get(prefix + "clamp_maximum_lat", False),

                   minimum_valid_lon=d.get(prefix + "minimum_valid_lon", cls.MINIMUM_VALID_LON),
                   clamp_minimum_lon=d.get(prefix + "clamp_minimum_lon", False),
                   maximum_valid_lon=d.get(prefix + "maximum_valid_lon", cls.MAXIMUM_VALID_LON),
                   clamp_maximum_lon=d.get(prefix + "clamp_maximum_lon", False),
                   modulo_repair_lon=d.get(prefix + "modulo_repair_lon", False),

                   escape_list_separators=d.get(prefix + "escape_list_separators", False))

    @classmethod
    # Build the value parsing option structure.
    def from_args(cls, args: Namespace, who: str = "")->'KgtkValueOptions':
        return cls.from_dict(vars(args), who=who)

    def show(self, who: str="", out: typing.TextIO=sys.stderr):
        prefix: str = "--" if len(who) == 0 else "--" + who + "-"
        print("%sallow-lax-qnodes=%s" % (prefix, str(self.allow_lax_qnodes)), file=out)
        print("%sallow-month-or-day-zero=%s" % (prefix, str(self.allow_month_or_day_zero)), file=out)
        print("%srepair-month-or-day-zero=%s" % (prefix, str(self.repair_month_or_day_zero)), file=out)
        print("%sallow-language-suffixes=%s" % (prefix, str(self.allow_language_suffixes)), file=out)
        print("%sallow-lax-strings=%s" % (prefix, str(self.allow_lax_strings)), file=out)
        print("%sallow-lax-lq-strings=%s" % (prefix, str(self.allow_lax_lq_strings)), file=out)
        if self.additional_language_codes is not None:
            print("%sadditional-language-codes=%s" % (prefix, " ".join(self.additional_language_codes)), file=out)

        print("%sminimum-valid-year=%d" % (prefix, self.minimum_valid_year), file=out)
        print("%sclamp-minimum-year=%s" % (prefix, str(self.clamp_minimum_year)), file=out)
        print("%smaximum-valid-year=%d" % (prefix, self.maximum_valid_year), file=out)
        print("%sclamp-maximum-year=%s" % (prefix, str(self.clamp_maximum_year)), file=out)

        print("%sallow-lax-coordinates=%s" % (prefix, str(self.allow_lax_coordinates)), file=out)
        print("%srepair-lax-coordinates=%s" % (prefix, str(self.repair_lax_coordinates)), file=out)

        print("%sminimum-valid-lat=%f" % (prefix, self.minimum_valid_lat), file=out)
        print("%sclamp-minimum-lat=%s" % (prefix, str(self.clamp_minimum_lat)), file=out)
        print("%smaximum-valid-lat=%f" % (prefix, self.maximum_valid_lat), file=out)
        print("%sclamp-maximum-lat=%s" % (prefix, str(self.clamp_maximum_lat)), file=out)

        print("%sminimum-valid-lon=%f" % (prefix, self.minimum_valid_lon), file=out)
        print("%sclamp-minimum-lon=%s" % (prefix, str(self.clamp_minimum_lon)), file=out)
        print("%smaximum-valid-lon=%f" % (prefix, self.maximum_valid_lon), file=out)
        print("%sclamp-maximum-lon=%s" % (prefix, str(self.clamp_maximum_lon)), file=out)
        print("%smodulo-repair-lon=%s" % (prefix, str(self.modulo_repair_lon)), file=out)

        print("%sescape-list-separators=%s" % (prefix, str(self.escape_list_separators)), file=out)

DEFAULT_KGTK_VALUE_OPTIONS: KgtkValueOptions = KgtkValueOptions()

def main():
    """
    Test the KGTK value options.
    """
    parser: ArgumentParser = ArgumentParser()
    KgtkValueOptions.add_arguments(parser, expert=True)
    KgtkValueOptions.add_arguments(parser, who="left", desc=" for the left file.", expert=True)
    KgtkValueOptions.add_arguments(parser, who="right", desc=" for the right file.", expert=True)
    args: Namespace = parser.parse_args()

    # Build the value parsing option structure.
    value_options: KgtkValueOptions = KgtkValueOptions.from_args(args)

    value_options.show()

    # Test prefixed value option processing.
    left_value_options: KgtkValueOptions = KgtkValueOptions.from_args(args, who="left")
    print("left_allow_month_or_day_zero: %s" % str(left_value_options.allow_month_or_day_zero))

    right_value_options: KgtkValueOptions = KgtkValueOptions.from_args(args, who="right")
    print("right_allow_month_or_day_zero: %s" % str(right_value_options.allow_month_or_day_zero))

if __name__ == "__main__":
    main()
