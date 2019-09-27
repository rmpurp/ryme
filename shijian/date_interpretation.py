import datetime as dt
import re

INVALID_STRING_MSG = 'Invalid date string.'
ADD_PATTERN = '\+\d+'
MONTH_DAY_PATTERN = '\d{1,2}[-/\.]\d{1,2}'
YEAR_MONTH_DAY_PATTERN = '(\d{2}|\d{4})[-/\.]\d{1,2}[-/\.]\d{1,2}'

DAY_NAMES = {
    's': 7,
    'su': 7,
    'm': 1,
    't': 2,
    'tu': 2,
    'w': 3,
    'r': 4,
    'th': 4,
    'f': 5,
    'a': 6,
    'sa': 6
}


def interpret_date(date_str: str, reference_date: dt.date = None) -> dt.date:
    """

    :param date_str:
    :param reference_date:
    """

    if not date_str:
        raise ValueError(INVALID_STRING_MSG)

    if not reference_date:
        reference_date = dt.date.today()

    if re.fullmatch(ADD_PATTERN, date_str):
        days_ahead = int(date_str[1:])
        return reference_date + dt.timedelta(days_ahead)
    elif re.fullmatch(MONTH_DAY_PATTERN, date_str):
        return match_month_day(date_str, reference_date)
    elif re.fullmatch(YEAR_MONTH_DAY_PATTERN, date_str):
        return match_month_day_year(date_str, reference_date)
    elif date_str.lower() in DAY_NAMES:
        return match_closest_given_weekday(date_str, reference_date)

    else:
        raise ValueError(INVALID_STRING_MSG)


def match_closest_given_weekday(date_str, reference_date):
    day_of_week = DAY_NAMES[date_str.lower()]
    ONE_DAY = dt.timedelta(days=1)
    return_date = reference_date + ONE_DAY
    while return_date.isoweekday() != day_of_week:
        return_date = return_date + ONE_DAY
    return return_date


def match_month_day_year(date_str, reference_date):
    year, month, day = map(int, re.split('[/\-.]', date_str))
    if len(str(year)) == 2:
        year = int(str(reference_date.year)[:-2] + str(year))
    return_date = dt.date(year, month, day)
    return return_date


def match_month_day(date_str, reference_date):
    month, day = map(int, re.split('[/\-.]', date_str))
    year = reference_date.year
    return_date = dt.date(year, month, day)
    if return_date < reference_date:
        return_date = dt.date(year + 1, month, day)
    return return_date
