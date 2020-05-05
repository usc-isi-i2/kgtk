"""
KGTK value processing options.
"""

from argparse import ArgumentParser, Namespace
import attr
import typing

@attr.s(slots=True, frozen=True)
class KgtkValueOptions:
    """
    These options will affect some aspects of value processing. They are in a
    seperate class for efficiency.
    """
    
    # The default minimum and maximum valid year values.
    MINIMUM_VALID_YEAR: int = 1583 # Per ISO 8601, years before this one require special agreement.
    MAXIMUM_VALID_YEAR: int = 2100 # Arbitrarily chosen.

    # Allow month 00 or day 00 in dates?  This isn't really allowed by ISO
    # 8601, but appears in wikidata.
    allow_month_or_day_zero: bool = attr.ib(validator=attr.validators.instance_of(bool), default=False)

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

    # Minimum and maximum year range in dates.
    minimum_valid_year: int = attr.ib(validator=attr.validators.instance_of(int), default=MINIMUM_VALID_YEAR)
    maximum_valid_year: int = attr.ib(validator=attr.validators.instance_of(int), default=MAXIMUM_VALID_YEAR)

    @classmethod
    def add_arguments(cls, parser: ArgumentParser):
        parser.add_argument(      "--additional-language-codes", dest="additional_language_codes",
                                  help="Additional language codes.", nargs="*", default=None)

        lsgroup= parser.add_mutually_exclusive_group()
        lsgroup.add_argument(      "--allow-language-suffixes", dest="allow_language_suffixes",
                                   help="Allow language identifier suffixes starting with a dash.", action='store_true', default=True)

        lsgroup.add_argument(      "--disallow-language-suffixes", dest="allow_language_suffixes",
                                   help="Disallow language identifier suffixes starting with a dash.", action='store_false')

        laxgroup= parser.add_mutually_exclusive_group()
        laxgroup.add_argument(      "--allow-lax-strings", dest="allow_lax_strings",
                                    help="Do not check if double quotes are backslashed inside strings.", action='store_true', default=False)

        laxgroup.add_argument(      "--disallow-lax-strings", dest="allow_lax_strings",
                                    help="Check if double quotes are backslashed inside strings.", action='store_false')

        lqgroup= parser.add_mutually_exclusive_group()
        lqgroup.add_argument(      "--allow-lax-lq-strings", dest="allow_lax_lq_strings",
                                   help="Do not check if single quotes are backslashed inside language qualified strings.", action='store_true', default=False)

        lqgroup.add_argument(      "--disallow-lax-lq-strings", dest="allow_lax_lq_strings",
                                   help="Check if single quotes are backslashed inside language qualified strings.", action='store_false')

        md0group= parser.add_mutually_exclusive_group()
        md0group.add_argument(      "--allow-month-or-day-zero", dest="allow_month_or_day_zero",
                                    help="Allow month or day zero in dates.", action='store_true', default=False)

        md0group.add_argument(      "--disallow-month-or-day-zero", dest="allow_month_or_day_zero",
                                    help="Allow month or day zero in dates.", action='store_false')

        parser.add_argument(      "--minimum-valid-year", dest="minimum_valid_year",
                                  help="The minimum valid year in dates.", type=int, default=cls.MINIMUM_VALID_YEAR)

        parser.add_argument(      "--maximum-valid-year", dest="maximum_valid_year",
                                  help="The maximum valid year in dates.", type=int, default=cls.MAXIMUM_VALID_YEAR)

    @classmethod
    # Build the value parsing option structure.
    def from_args(cls, args: Namespace)->'KgtkValueOptions':
        return cls(allow_month_or_day_zero=args.allow_month_or_day_zero,
                   allow_language_suffixes=args.allow_language_suffixes,
                   allow_lax_strings=args.allow_lax_strings,
                   allow_lax_lq_strings=args.allow_lax_lq_strings,
                   additional_language_codes=args.additional_language_codes,
                   minimum_valid_year=args.minimum_valid_year,
                   maximum_valid_year=args.maximum_valid_year)

DEFAULT_KGTK_VALUE_OPTIONS: KgtkValueOptions = KgtkValueOptions()

def main():
    """
    Test the KGTK value options.
    """
    parser: ArgumentParser = ArgumentParser()
    KgtkValueOptions.add_arguments(parser)
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

if __name__ == "__main__":
    main()
