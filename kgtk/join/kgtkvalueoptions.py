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
    
    # If this list gets long, we may want to turn it into a map to make lookup
    # more efficient.
    additional_language_codes: typing.Optional[typing.List[str]] = attr.ib(validator=attr.validators.optional(attr.validators.deep_iterable(member_validator=attr.validators.instance_of(str),
                                                                                                                                            iterable_validator=attr.validators.instance_of(list))),
                                                                           default=None)
    

    @classmethod
    def add_arguments(cls, parser: ArgumentParser):
        parser.add_argument(      "--additional-language-codes", dest="additional_language_codes",
                                  help="Additional language codes.", nargs="*", default=None)

        parser.add_argument(      "--allow-lax-strings", dest="allow_lax_strings",
                                  help="Do not check if double quotes are backslashed inside strings.", action='store_true')

        parser.add_argument(      "--allow-lax-lq-strings", dest="allow_lax_lq_strings",
                                  help="Do not check if single quotes are backslashed inside language qualified strings.", action='store_true')

        parser.add_argument(      "--allow-month-or-day-zero", dest="allow_month_or_day_zero",
                                  help="Allow month or day zero in dates.", action='store_true')

    @classmethod
    # Build the value parsing option structure.
    def from_args(cls, args: Namespace)->'KgtkValueOptions':
        return cls(allow_month_or_day_zero=args.allow_month_or_day_zero,
                   allow_lax_strings=args.allow_lax_strings,
                   allow_lax_lq_strings=args.allow_lax_lq_strings,
                   additional_language_codes=args.additional_language_codes)

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

if __name__ == "__main__":
    main()
