from datetime import datetime, time, timedelta

from anpy import AbstractDataHandler, Day
from anpy_lib.data_analysis import get_days, get_per_category_durations
from anpy_lib.data_entry import get_most_recent_day


def create_table_iterable_and_headers(data_handler: AbstractDataHandler,
                                      reference_datetime: datetime = None,
                                      day_start_time: time = None):
    if reference_datetime is None:
        reference_datetime = datetime.now()
    if day_start_time is None:
        day_start_time = time(6, 0)

    # 6 days prior
    week_start_isoweekday = ((reference_datetime - timedelta(
        hours=day_start_time.hour) + timedelta.resolution).isoweekday() + 1) % 7
    week_start = get_most_recent_day(week_start_isoweekday, day_start_time,
                                     reference_datetime)

    days = get_days(data_handler, week_start, 7)

    rows = []
    for day in days:
        rows.append(Row(day))

    average_row = AverageRow(rows)

    headers = ['date',
               'time started',
               'time ended',
               'time total (h)',
               'time working (h)',
               'efficiency'] + [c + ' (min)'
                                for c in average_row.ordered_categories]

    return [*rows, average_row], headers


class Row:
    def __init__(self, day: Day):
        self.day = day
        self.work_start: datetime = day.work_start
        self.work_end: datetime = day.work_end
        self.day_start_time = day.day_start
        self.data = get_per_category_durations(day)
        self.sorted_categories = None

    @property
    def date(self):
        return self.day.day_start.date()

    @property
    def time_total(self):
        if self.work_start is None:
            return 0

        return (self.work_end - self.work_start).seconds / 3600

    @property
    def time_working(self):
        return sum(self.data.values()) / 3600

    @property
    def efficiency(self):
        if self.time_total == 0:
            return None
        return self.time_working / self.time_total / 0.75

    @property
    def categories(self):
        return self.data.keys()

    def get_data(self, ordered_categories):
        return (self.data[c] / 60 for c in ordered_categories)

    def __iter__(self):
        if self.sorted_categories is None:
            raise ValueError

        data = map('{:.1f}'.format, self.get_data(self.sorted_categories))
        return iter([self.date,
                     self.work_start.time().strftime(
                         '%I:%M %p') if self.work_start else None,
                     self.work_end.time().strftime(
                         '%I:%M %p') if self.work_end else None,
                     '{:.1f}'.format(self.time_total),
                     '{:.1f}'.format(self.time_working),
                     '{:.1%}'.format(
                         self.efficiency) if self.efficiency else None] + list(
            data))


class AverageRow:
    def __init__(self, rows):
        self.rows = rows
        ordered_categories = self.ordered_categories
        for row in self.rows:
            row.sorted_categories = ordered_categories

    @property
    def all_categories(self):
        cols = set()
        for row in self.rows:
            cols.update(row.categories)
        return cols

    @property
    def average_data(self):
        d = dict()
        for category in self.all_categories:
            d[category] = average(map(lambda x: x.data[category], self.rows))
        return d

    @property
    def ordered_categories(self):
        average_data = self.average_data
        return sorted(self.all_categories, key=lambda c: average_data[c],
                      reverse=True)

    @property
    def average_time_total(self):
        return average((row.time_total for row in self.rows))

    @property
    def average_time_working(self):
        return average((row.time_working for row in self.rows))

    @property
    def average_efficiency(self):
        return average((row.efficiency for row in self.rows))

    def __iter__(self):
        average_data = self.average_data
        data = [average_data[c] for c in self.ordered_categories]

        return iter(['averages:', None, None,
                     '{:.1f}'.format(self.average_time_total),
                     '{:.1f}'.format(self.average_time_working),
                     '{:.1%}'.format(
                         self.average_efficiency) if self.average_efficiency else None]
                    + ['{:.1f}'.format(d / 60) for d in data])


def average(iterable):
    iterable = list(filter(lambda x: x is not None, iterable))
    if not iterable:
        return None
    return sum(iterable) / len(iterable)
