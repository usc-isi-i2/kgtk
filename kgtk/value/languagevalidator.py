"""
Validate language qualifiers.

TODO: Extend pour language tag recognition to RFC 3066.
https://tools.ietf.org/html/rfc3066

TODO: Cite RDF compliance:  BCP46 Section 2-2-9.
https://tools.ietf.org/html/bcp47#section-2.2.9
https://www.w3.org/TR/2014/REC-rdf11-concepts-20140225/#section-Graph-Literal
"""

from argparse import ArgumentParser, Namespace
import attr
import iso639 # type: ignore
import pycountry # type: ignore
import typing

from kgtk.value.kgtkvalueoptions import KgtkValueOptions, DEFAULT_KGTK_VALUE_OPTIONS

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
    """
    The language code may be a two- or three-character code from ISO
    639-3, which replaces ISO 639-1 and ISO 639-2.  In addition, wikidata
    may include language codes, such as 'mo', that have been retired.  The
    additional_language_codes table supports these codes, when allowed.

    Wikidata may also contain collective language codes, such as "nah",
    referring the the Nahuatl languages. These codes from ISO 639-5 are
    accepted as a fallback when ISO 639-3 lookup fails.

    https://meta.wikimedia.org/wiki/Special_language_codes
    https://en.wikipedia.org/wiki/Template:ISO_639_name_be-tarask
    """

    DEFAULT_ADDITIONAL_LANGUAGE_CODES: typing.List[str] = [
        # New codes:
        "cnr", # Montenegrin.  Added 21-Dec-2017. https://iso639-3.sil.org/code/cnr
        "hyw", # Western Armenian.  Added 23-Jan-2018. https://iso639-3.sil.org/code/hyw
        "szy", # Sakizawa.  Added 25-Jan-2019. https://iso639-3.sil.org/code/szy

        # Obsolete codes:
        "bh", # Bihari lanuages, apparently replaced by "bih".
        "mo", # Moldavian. Retired 3-Nov-2008. Replaced by the codes for Romanian.
              # http://www.personal.psu.edu/ejp10/blogs/gotunicode/2008/11/language-tage-mo-for-moldovan.html
        "eml", # Emiliano-Romagnolo. Split and retired 16-Jan-2009. https://iso639-3.sil.org/code/eml
    ]

    @classmethod
    def validate(cls,
                 lang: str,
                 options: KgtkValueOptions=DEFAULT_KGTK_VALUE_OPTIONS,
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
        if options.allow_language_suffixes and "-" in lang:
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
        additional_language_codes: typing.List[str]
        if options.additional_language_codes is not None:
            additional_language_codes = options.additional_language_codes
            if verbose:
                print("Using a custom list of %d additional language codes." % len(additional_language_codes))
        else:
            if verbose:
                print("Using the default list of additional language codes.")
            additional_language_codes = LanguageValidator.DEFAULT_ADDITIONAL_LANGUAGE_CODES

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
    parser.add_argument("-v", "--verbose", dest="verbose", help="Print additional progress messages.", action='store_true')
    KgtkValueOptions.add_arguments(parser)
    args: Namespace = parser.parse_args()

    # Build the value parsing option structure.
    value_options: KgtkValueOptions = KgtkValueOptions.from_args(args)

    value: str
    for value in args.values:
        result: bool = LanguageValidator.validate(value, options=value_options, verbose=args.verbose)                                   
        print("%s: %s" % (value, str(result)), flush=True)

if __name__ == "__main__":
    main()
