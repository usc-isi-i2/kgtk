import re
import string


white_space_regex = re.compile('\\s+')
punct_trans_table = dict((ord(char), ord(' ')) for char in string.punctuation)


def normalize_whitespace(text):
    """Strip surrounding whitespace and normalize all other whitespace to single spaces.
    """
    text = str(text)
    return re.sub(white_space_regex, ' ', text).strip()


def normalize_punctuation(text):
    """Translate all punctuation chars in `text' to spaces and then whitespace-normalize the result.
    """
    text = str(text)
    text = text.translate(punct_trans_table)
    return normalize_whitespace(text)


def normalize_case(text):
    """Convert `text' to lower case.
    """
    text = str(text)
    return text.lower()


def normalize_text(text):
    """Perform all text normalizations on `text'.
    """
    return normalize_case(normalize_punctuation(text))


def normalize_ontology_type(type):
    """Normalize an ontology type name by substituting all punctuation characters with spaces.
    This will do the right thing for LDC/AIDA ontology types but might have to be generalized.
    """
    return normalize_punctuation(type)
