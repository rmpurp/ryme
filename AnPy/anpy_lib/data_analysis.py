import datetime as dt
from collections import defaultdict
from typing import List, Iterable, Dict

from anpy import AbstractDataHandler, Record, Day

DAYS_IN_A_WEEK = 7


def get_day(handler: AbstractDataHandler, day_start: dt.datetime):
    day = Day(day_start)
    day_end = day_start + dt.timedelta(days=1)
    day.extend(handler.get_records_between(day_start, day_end))
    return day


def get_days(handler: AbstractDataHandler,
             first_day_start: dt.datetime,
             num_days: int):
    one_day = dt.timedelta(days=1)
    days = []
    day_start = first_day_start
    for i in range(num_days):
        days.append(get_day(handler, day_start=day_start))
        day_start += one_day
    return days


# TODO: refactor usages to use Day version
def get_records_on_day(handler: AbstractDataHandler,
                       day_start: dt.datetime) -> Iterable[Record]:
    day_end = day_start + dt.timedelta(days=1)
    return handler.get_records_between(day_start, day_end)


# TODO: refactor usages to use Day version
def get_records_on_week(handler: AbstractDataHandler,
                        day_start: dt.datetime) -> List[Iterable[Record]]:
    one_day = dt.timedelta(days=1)
    records = []
    for i in range(DAYS_IN_A_WEEK):
        records.append(get_records_on_day(handler, day_start))
        day_start += one_day
    return records


# TODO: refactor usages to use Day version
def get_total_subject_breakdown(list_of_records: List[Iterable[Record]]) \
        -> List[Dict[str, float]]:
    dicts = [get_per_category_durations(r) for r in list_of_records]
    return dicts


def get_per_category_durations(records: Iterable[Record]) \
        -> defaultdict:
    record_dict = defaultdict(int)
    for record in records:
        seconds = (record.end - record.start).total_seconds()
        record_dict[record.name] = record_dict.get(
            record.name, 0) + seconds
    return record_dict
