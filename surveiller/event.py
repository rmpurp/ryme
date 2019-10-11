import datetime

from os.path import isfile, join, dirname
import os
from itertools import groupby, zip_longest
from operator import attrgetter, add
from functools import reduce
import csv
import config
from sortedcontainers import SortedList
import tempfile
import shutil


def grouper(iterable, n, fillvalue=None):
    """Collect data into fixed-length chunks or blocks"""
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


class EventList(SortedList):
    def get_since(self, dt, until=None):
        if not until:
            return filter(lambda x: x.start > dt, self)
        else:
            return filter(lambda x: dt < x.start < until, self)

    def group_by_subject(self, since=None, until=None):
        if since:
            base_events = self.get_since(since, until)
        else:
            base_events = self

        d = dict()

        events = sorted(base_events, key=attrgetter("subject"))
        for k, g in groupby(events, key=attrgetter("subject")):
            d[k] = reduce(add, map(attrgetter("length"), g))
        return d

    def write(self, filepath=None):
        if not filepath:
            filepath = config.FILE

        directory = dirname(filepath)
        temppath = join(directory, "temporary")

        with open(temppath, "w") as temp:

            csv_writer = csv.writer(temp)

            for event in reversed(self):
                csv_writer.writerow(event.to_csv_row())

        shutil.copyfile(temppath, filepath)
        os.remove(temppath)


class Event:
    """A time tracking event"""

    def __init__(self, subject, name, start, end, flag):
        self.subject = subject
        self.name = name
        self.start = start
        self.end = end
        self.flag = flag

    def __lt__(self, other):
        return self.start < other.start

    def __eq__(self, other):
        return repr(self) == repr(other)

    # holy shit change me later

    def __repr__(self):
        return "Event({!r}, {!r}, {!r}, {!r})".format(self.subject,
                                                      self.name,
                                                      self.start,
                                                      self.end)

    @property
    def length(self):
        if self.flag == "marked" or self.flag == "started":
            return self.time_since_start()
        else:
            delta = self.end - self.start
            return delta.seconds + delta.days * 24 * 3600

    def time_since_start(self, now=None):
        if now is None:
            now = datetime.datetime.now()
        delta = now - self.start

        return delta.seconds + delta.days * 24 * 3600

    def time_since_end(self, now=None):

        if now is None:
            now = datetime.datetime.now()
        delta = now - self.end

        return delta.seconds + delta.days * 24 * 3600

    def to_csv_row(self):
        return (self.subject, self.name,
                self.start.isoformat(timespec='seconds'),
                self.end.isoformat(timespec='seconds'), self.flag)


def read_most_recent():
    events = read()
    if not events:
        return None

    return events[-1]


def read_line(line: str):
    return _read([line])


def read():
    events = EventList()

    filepath = config.FILE

    if not isfile(filepath):
        return events

    with open(filepath) as frb:
        return _read(frb)


def _read(f):
    events = EventList()

    csv_reader = csv.reader(f)
    for subject, name, start, end, flag in csv_reader:
        start = datetime.datetime.fromisoformat(start)
        end = datetime.datetime.fromisoformat(end)
        if flag == 'cancelled':
            continue
        events.add(
            Event(subject, name, start, end, flag))
    return events

