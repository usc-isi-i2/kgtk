"""
KGTK value processing options.
"""

from argparse import ArgumentParser, Namespace
import attr
import typing

@attr.s(slots=True, frozen=True)
class KgtkValueOptions:
    """
    These options control various aspects of value processing. They are in a
    seperate class for code isolation and efficiency.

    """
    
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

    # Minimum and maximum year range in dates.
    MINIMUM_VALID_YEAR: int = 1583 # Per ISO 8601, years before this one require special agreement.
    minimum_valid_year: int = attr.ib(validator=attr.validators.instance_of(int), default=MINIMUM_VALID_YEAR)
    MAXIMUM_VALID_YEAR: int = 2100 # Arbitrarily chosen.
    maximum_valid_year: int = attr.ib(validator=attr.validators.instance_of(int), default=MAXIMUM_VALID_YEAR)

    MINIMUM_VALID_LAT: float = -90.
    minimum_valid_lat: float = attr.ib(validator=attr.validators.instance_of(float), default=MINIMUM_VALID_LAT)
    MAXIMUM_VALID_LAT: float = 90.
    maximum_valid_lat: float = attr.ib(validator=attr.validators.instance_of(float), default=MAXIMUM_VALID_LAT)
    
    MINIMUM_VALID_LON: float = -180.
    minimum_valid_lon: float = attr.ib(validator=attr.validators.instance_of(float), default=MINIMUM_VALID_LON)
    MAXIMUM_VALID_LON: float = 180.
    maximum_valid_lon: float = attr.ib(validator=attr.validators.instance_of(float), default=MAXIMUM_VALID_LON)
    

    @classmethod
    def add_arguments(cls, parser: ArgumentParser, who: str = "", desc: str = "."):
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
        
        vgroup = parser.add_argument_group(prefix3 + "Data value parsing", "Options controlling the parsing and processing of KGTK data values" + desc)
        vgroup.add_argument(      prefix1 + "additional-language-codes", dest=prefix2 + "additional_language_codes",
                                  help=prefix3 + "Additional language codes.", nargs="*", default=None)

        lsgroup= vgroup.add_mutually_exclusive_group()
        lsgroup.add_argument(      prefix1 + "allow-language-suffixes", dest=prefix2 + "allow_language_suffixes",
                                   help=prefix3 + "Allow language identifier suffixes starting with a dash.", action='store_true', default=True)

        lsgroup.add_argument(      prefix1 + "disallow-language-suffixes", dest=prefix2 + "allow_language_suffixes",
                                   help=prefix3 + "Disallow language identifier suffixes starting with a dash.", action='store_false')

        laxgroup= vgroup.add_mutually_exclusive_group()
        laxgroup.add_argument(      prefix1 + "allow-lax-strings", dest=prefix2 + "allow_lax_strings",
                                    help=prefix3 + "Do not check if double quotes are backslashed inside strings.", action='store_true', default=False)

        laxgroup.add_argument(      prefix1 + "disallow-lax-strings", dest=prefix2 + "allow_lax_strings",
                                    help=prefix3 + "Check if double quotes are backslashed inside strings.", action='store_false')

        lqgroup= vgroup.add_mutually_exclusive_group()
        lqgroup.add_argument(      prefix1 + "allow-lax-lq-strings", dest=prefix2 + "allow_lax_lq_strings",
                                   help=prefix3 + "Do not check if single quotes are backslashed inside language qualified strings.",
                                   action='store_true', default=False)

        lqgroup.add_argument(      prefix1 + "disallow-lax-lq-strings", dest=prefix2 + "allow_lax_lq_strings",
                                   help=prefix3 + "Check if single quotes are backslashed inside language qualified strings.",
                                   action='store_false')

        amd0group= vgroup.add_mutually_exclusive_group()
        amd0group.add_argument(      prefix1 + "allow-month-or-day-zero", dest=prefix2 + "allow_month_or_day_zero",
                                    help=prefix3 + "Allow month or day zero in dates.", action='store_true', default=False)

        amd0group.add_argument(      prefix1 + "disallow-month-or-day-zero", dest=prefix2 + "allow_month_or_day_zero",
                                    help=prefix3 + "Allow month or day zero in dates.", action='store_false')

        rmd0group= vgroup.add_mutually_exclusive_group()
        rmd0group.add_argument(      prefix1 + "repair-month-or-day-zero", dest=prefix2 + "repair_month_or_day_zero",
                                    help=prefix3 + "Repair month or day zero in dates.", action='store_true', default=False)

        rmd0group.add_argument(      prefix1 + "no-repair-month-or-day-zero", dest=prefix2 + "repair_month_or_day_zero",
                                    help=prefix3 + "Do not repair month or day zero in dates.", action='store_false')

        vgroup.add_argument(      prefix1 + "minimum-valid-year", dest=prefix2 + "minimum_valid_year",
                                  help=prefix3 + "The minimum valid year in dates.", type=int, default=cls.MINIMUM_VALID_YEAR)

        vgroup.add_argument(      prefix1 + "maximum-valid-year", dest=prefix2 + "maximum_valid_year",
                                  help=prefix3 + "The maximum valid year in dates.", type=int, default=cls.MAXIMUM_VALID_YEAR)

        vgroup.add_argument(      prefix1 + "minimum-valid-lat", dest=prefix2 + "minimum_valid_lat",
                                  help=prefix3 + "The minimum valid latitude.", type=int, default=cls.MINIMUM_VALID_LAT)

        vgroup.add_argument(      prefix1 + "maximum-valid-lat", dest=prefix2 + "maximum_valid_lat",
                                  help=prefix3 + "The maximum valid latitude.", type=int, default=cls.MAXIMUM_VALID_LAT)

        vgroup.add_argument(      prefix1 + "minimum-valid-lon", dest=prefix2 + "minimum_valid_lon",
                                  help=prefix3 + "The minimum valid longitude.", type=int, default=cls.MINIMUM_VALID_LON)

        vgroup.add_argument(      prefix1 + "maximum-valid-lon", dest=prefix2 + "maximum_valid_lon",
                                  help=prefix3 + "The maximum valid longitude.", type=int, default=cls.MAXIMUM_VALID_LON)

        elsgroup= vgroup.add_mutually_exclusive_group()
        elsgroup.add_argument(      prefix1 + "escape-list-separators", dest=prefix2 + "escape_list_separators",
                                    help=prefix3 + "Escape all list separators instead of splitting on them.", action='store_true', default=False)

        elsgroup.add_argument(      prefix1 + "no-escape-list-separators", dest=prefix2 + "escape_list_separators",
                                    help=prefix3 + "Do not escape list separators.", action='store_false')

    @classmethod
    # Build the value parsing option structure.
    def from_dict(cls, d: dict, who: str = "")->'KgtkValueOptions':
        prefix: str = ""   # The destination name prefix.
        if len(who) > 0:
            prefix = who + "_"

        return cls(allow_month_or_day_zero=d.get(prefix + "allow_month_or_day_zero", False),
                   repair_month_or_day_zero=d.get(prefix + "repair_month_or_day_zero", False),
                   allow_language_suffixes=d.get(prefix + "allow_language_suffixes", True),
                   allow_lax_strings=d.get(prefix + "allow_lax_strings", False),
                   allow_lax_lq_strings=d.get(prefix + "allow_lax_lq_strings", False),
                   additional_language_codes=d.get(prefix + "additional_language_codes", None),
                   minimum_valid_year=d.get(prefix + "minimum_valid_year", cls.MINIMUM_VALID_YEAR),
                   maximum_valid_year=d.get(prefix + "maximum_valid_year", cls.MAXIMUM_VALID_YEAR),
                   escape_list_separators=d.get(prefix + "escape_list_separators", False))

    @classmethod
    # Build the value parsing option structure.
    def from_args(cls, args: Namespace, who: str = "")->'KgtkValueOptions':
        return cls.from_dict(vars(args), who=who)

DEFAULT_KGTK_VALUE_OPTIONS: KgtkValueOptions = KgtkValueOptions()

def main():
    """
    Test the KGTK value options.
    """
    parser: ArgumentParser = ArgumentParser()
    KgtkValueOptions.add_arguments(parser)
    KgtkValueOptions.add_arguments(parser, who="left", desc=" for the left file.")
    KgtkValueOptions.add_arguments(parser, who="right", desc=" for the right file.")
    args: Namespace = parser.parse_args()

    # Build the value parsing option structure.
    value_options: KgtkValueOptions = KgtkValueOptions.from_args(args)

    print("allow_month_or_day_zero: %s" % str(value_options.allow_month_or_day_zero))
    print("allow_lax_strings: %s" % str(value_options.allow_lax_strings))
    print("allow_lax_lq_strings: %s" % str(value_options.allow_lax_lq_strings))
    print("allow_language_suffixes: %s" % str(value_options.allow_language_suffixes))
    if value_options.additional_language_codes is None:
        print("additional_language_codes: None")
    else:
        print("additional_language_codes: [ %s ]" % ", ".join(value_options.additional_language_codes))
    
    # Test prefixed value option processing.
    left_value_options: KgtkValueOptions = KgtkValueOptions.from_args(args, who="left")
    print("left_allow_month_or_day_zero: %s" % str(left_value_options.allow_month_or_day_zero))

    right_value_options: KgtkValueOptions = KgtkValueOptions.from_args(args, who="right")
    print("right_allow_month_or_day_zero: %s" % str(right_value_options.allow_month_or_day_zero))

if __name__ == "__main__":
    main()
