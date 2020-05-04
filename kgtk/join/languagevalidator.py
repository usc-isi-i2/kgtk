"""
Validate language qualifiers.
"""

from argparse import ArgumentParser, Namespace
import attr
import iso639 # type: ignore
import pycountry # type: ignore
import re
import sys
import typing

# Problem: pycountry incorporates the Debian team's ISO 639-3 table,
# which as of 03-May-2020 has not been updated in four years!
# Meanwhile, iso639 (from pypi iso-639) has an ISO 639-3 table
# from 2015-05-05.
#
# https://salsa.debian.org/iso-codes-team/iso-codes/-/blob/master/iso_639-3/iso_639_3.tab 
# https://pypi.org/project/iso-639/
#
# Problem: Wikidata may contain obsolete language codes which have been
# removed from the standard indices.
#
# Example: "mo"
#
# Solution: We will keep a list of additional language codes.
@attr.s(slots=True, frozen=True)
class LanguageValidator:

    DEFAULT_ADDITIONAL_LANGUAGE_CODES: typing.List[str] = [
        # New codes:
        "cnr", # Montenegrin.  Added 21-Dec-2017. https://iso639-3.sil.org/code/cnr
        "hyw", # Wester Armenian.  Added 23-Jan-2018. https://iso639-3.sil.org/code/hyw

        # Obsolete codes:
        "mo", # Retired, replaced by the codes for Romanian, but still appearing in wikidata.
        "eml", # Emiliano-Romagnolo. Split and retired 16-Jan-2009. https://iso639-3.sil.org/code/eml
    ]

    @classmethod
    def validate(cls,
                 lang: str,
                 additional_language_codes: typing.Optional[typing.List[str]]=None,
                 verbose: bool = False,
    )->bool:
        # Wikidata contains entries such as:
        # 'panamenha'@pt-br      # language code followed by country code
        # 'Ecuador'@es-formal    # language code followed by dialect name
        #
        # If we see a dash, we'll check the language code by itself.
        if verbose:
            print("Validating '%s'" % lang)

        save_lang: str = lang # for the debug prints below.
        country_or_dialect: str = ""
        if "-" in lang:
            (lang, country_or_dialect) = lang.split("-", 1)
            if verbose:
                print("'%s' split into '%s' and '%s'" % (save_lang, lang, country_or_dialect))

        if len(lang) == 2:
            # Two-character language codes.
            if pycountry.languages.get(alpha_2=lang) is not None:
                if verbose:
                    print("pycountry.languages.get(alpha_2=lang) succeeded")
                return True

        elif len(lang) == 3:
            # Three-character language codes.
            if pycountry.languages.get(alpha_3=lang) is not None:
                if verbose:
                    print("pycountry.languages.get(alpha_3=lang) succeeded")
                return True

        # Perhaps this is a collective (language family) code from ISO 639-5?
        try:
            iso639.languages.get(part5=lang)
            if verbose:
                print("iso639.languages.get(part5=lang) succeeded")
            return True
        except KeyError:
            pass

        # If there's a table of additional language codes, check there:
        if additional_language_codes is None:
            if verbose:
                print("Using the default list of additional language codes.")
            additional_language_codes = LanguageValidator.DEFAULT_ADDITIONAL_LANGUAGE_CODES
        else:
            if verbose:
                print("Using a custom list of %d additional language codes." % len(additional_language_codes))
        if lang in additional_language_codes:
            if verbose:
                print("found in the table of additional languages.")
            return True

        if verbose:
            print("Not found.")
        return False

def main():
    """
    Test the language validator.
    """
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument(dest="values", help="The values(s) to test", type=str, nargs="+")

    parser.add_argument(      "--additional-language-codes", dest="additional_language_codes",
                              help="Additional language codes.", nargs="*", default=None)

    parser.add_argument("-v", "--verbose", dest="verbose", help="Print additional progress messages.", action='store_true')
    args: Namespace = parser.parse_args()

    value: str
    for value in args.values:
        result: bool = LanguageValidator.validate(value,
                                                  additional_language_codes=args.additional_language_codes,
                                                  verbose=args.verbose)
        
        print("%s: %s" % (value, str(result)), flush=True)

if __name__ == "__main__":
    main()
