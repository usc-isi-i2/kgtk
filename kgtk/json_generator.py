import sys
import re
from typing import TextIO
from kgtk.exceptions import KGTKException

BAD_CHARS = [":", "-", "&", ",", " ",
             "(", ")", "\'", '\"', "/", "\\", "[", "]", ";", "|"]


class JsonGenerator:
    """
    A class to maintain the status of the generator
    """

    def __init__(
            self,
            prop_file: str,
            use_gz:bool,
    ):
        from etk.wikidata.statement import Rank

    def finalize(self):
        # finalize the generator
        return