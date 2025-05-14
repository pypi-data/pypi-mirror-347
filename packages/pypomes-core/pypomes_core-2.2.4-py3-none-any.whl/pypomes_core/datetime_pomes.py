from datetime import date, datetime
from dateutil import parser
from dateutil.parser import ParserError
from enum import StrEnum
from typing import Final
from zoneinfo import ZoneInfo

from .env_pomes import APP_PREFIX, env_get_str

# HAZARD: requires 'tzdata' package installed to work
TIMEZONE_LOCAL: Final[ZoneInfo] = ZoneInfo(key=env_get_str(key=f"{APP_PREFIX}_TIMEZONE_LOCAL",
                                                           def_value="America/Sao_Paulo"))


class DateFormat(StrEnum):
    """
    Some useful date formats.
    """
    STD = "%m/%d/%Y"
    COMPACT = "%Y%m%d"
    INV = "%Y-%m-%d"


class DatetimeFormat(StrEnum):
    """
    Some useful datetime formats.
    """
    STD = "%m/%d/%Y %H:%M:%S"
    COMPACT = "%Y%m%d%H%M%S"
    INV = "%Y-%m-%d %H:%M:%S"


def date_reformat(dt_str: str,
                  to_format: str,
                  **kwargs: any) -> str:
    """
    Convert the date in *dt_str* to the format especified in *to_format*.

    The argument *dt_str* must represent a valid date, with or without time-of-day information.
    The argument *to_format* must be a valid format for *date* ou *datetime*.

    In *kwargs*, it may optionally be specified:
        -   *dayfirst=True*
                - to signal that *day* comes before *month* in an ambiguous 3-integer date
                  (e.g. '01/05/09') - defaults to *False*
        -   *yearfirst=True*
                - to signal that *year* comes before *month* in an ambiguous 3-integer date
                  (e.g. '01/05/09') - defaults to *False*
        -   *fmt=<format>*, to force use of a specific format
    Return *None* se *dt_str* does not contain a valid date.

    :param dt_str: the date to convert
    :param to_format: the format for the conversion
    :param kwargs: optional arguments for the parser in python-dateutil
    :return: the converted date, or *None* if the convertion was not possible
    """
    result: str | None = None
    ts: datetime = parser.parse(timestr=dt_str,
                                **kwargs)
    if ts:
        result = ts.strftime(format=to_format)

    return result


def date_parse(dt_str: str,
               **kwargs: any) -> date:
    """
    Obtain and return the *date* object corresponding to *dt_str*.

    In *kwargs*, it may optionally be specified:
        -   *dayfirst=True*
                - to signal that *day* comes before *month* in an ambiguous 3-integer date
                  (e.g. '01/05/09') - defaults to *False*
        -   *yearfirst=True*
                - to signal that *year* comes before *month* in an ambiguous 3-integer date
                  (e.g. '01/05/09') - defaults to *False*
        -   *fmt=<format>*, to force use of a specific format
    Return *None* se *dt_str* does not contain a valid date.

    :param dt_str: the date, in a supported format
    :param kwargs: optional arguments for the parser in python-dateutil
    :return: the corresponding date object, or None
    """
    # declare the return variable
    result: date | None

    try:
        result = parser.parse(timestr=dt_str,
                              **kwargs).date()
    except (TypeError, ParserError, OverflowError):
        result = None

    return result


def datetime_parse(dt_str: str,
                   **kwargs: any) -> datetime:
    """
    Obtain and return the *datetime* object corresponding to *dt_str*.

    In *kwargs*, it may optionally be specified:
        -   *dayfirst=True*
                - to signal that *day* comes before *month* in an ambiguous 3-integer date
                  (e.g. '01/05/09') - defaults to *False*
        -   *yearfirst=True*
                - to signal that *year* comes before *month* in an ambiguous 3-integer date
                  (e.g. '01/05/09') - defaults to *False*
        -   *fmt=<format>*, to force use of a specific format
    Return *None* if *dt_str* does not contain a valid date.

    :param dt_str: the date, in a supported format
    :param kwargs: optional arguments for the parser in python-dateutil
    :return: the corresponding datetime object, or *None*
    """
    # declare the return variable
    result: datetime | None

    try:
        result = parser.parse(timestr=dt_str,
                              **kwargs)
    except (TypeError, ParserError, OverflowError):
        result = None

    return result
