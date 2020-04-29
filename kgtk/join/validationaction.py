from enum import Enum

class ValidationAction(Enum):
    """
    What should we when a validation check fails?

    TODO: Why can't this be inside class KgtkReader?
    """
    PASS = 0 # Silently ignore the validation problem and continue to process the line.
    REPORT = 1 # Report the validation problem and continue to process the line.
    EXCLUDE = 2 # Silently exclude the line from further processing.
    COMPLAIN = 3 # Report the validation problem and exclude the line from further processing.
    ERROR = 4 # Report the validation problem and immediately raise a ValueError.
    EXIT = 5 # Report the validation problem and immediately exit


