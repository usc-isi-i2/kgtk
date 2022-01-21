from etk.extractors.date_extractor import DateExtractor, DateResolution
from kgtk.wikidata.value import Precision


def parse_datetime_string(s, *args, **kwargs):
    """
    Automatically convert string to iso datetime string

    :param s:
    :return: iso format datetime string, wikidata date precision
    """

    kwargs['date_value_resolution'] = DateResolution.SECOND

    de = DateExtractor()
    e = de.extract(s, *args, **kwargs)
    if len(e) == 0:
        raise ValueError('No date / datetime detected')

    dt_str = e[0].value
    orig_resolution = de._last_original_resolution

    wd_precision = None
    if orig_resolution == DateResolution.SECOND:
        wd_precision = Precision.second
    if orig_resolution == DateResolution.MINUTE:
        wd_precision = Precision.minute
    if orig_resolution == DateResolution.HOUR:
        wd_precision = Precision.hour
    elif orig_resolution == DateResolution.DAY:
        wd_precision = Precision.day
    elif orig_resolution == DateResolution.MONTH:
        wd_precision = Precision.month
    elif orig_resolution == DateResolution.YEAR:
        wd_precision = Precision.year

        # TODO: support more fine-grind year precisions

    return dt_str, wd_precision
