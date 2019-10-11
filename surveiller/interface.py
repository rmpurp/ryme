#!/usr/bin/env PYTHONIOENCODING=UTF-8 /usr/local/bin/python3.7

import datetime
import config
from event import read_most_recent, read, Event, read_line
from utils import seconds_to_readable_str
import analysis

def get_subjects():
    return config.subjects


def get_progress(since):
    """Get a dictionary containing the amount of time each subject has been
       worked on since the time given in the argument"""
    if isinstance(since, str):
        since = datetime.datetime.fromisoformat(since)

    events = read()
    return events.group_by_subject(since)


def get_weekly():
    events = read()
    weekly_times = analysis.group_by_week(events)

    def get_lines():
        for week_start, times in weekly_times.items():
            times = {topic: seconds_to_readable_str(amount) for topic, amount in times.items()}
            yield f"{week_start}: {times}"

    return "\n".join(get_lines())


def get_total(since):
    d = get_progress(since)
    return "Total: {}".format(seconds_to_readable_str(sum(d.values()), 'and'))


def merge_with(line):
    events = read()
    to_merge = read_line(line)
    for event in to_merge:
        if event not in events:
            events.add(event)
    events.write()


def status(style="text"):
    """Return a one-line status of what the user is currently doing"""
    e = read_most_recent()

    if not e:
        return "No task history"

    if e.flag == "ended" or e.flag == "cancelled":
        seconds = e.time_since_end()
        subject = "Inactive"
    else:
        seconds = e.time_since_start()
        subject = e.subject

    if style == "text":
        return "{}: {}".format(subject,
                               seconds_to_readable_str(seconds, use_days=True))
    elif style == "dict":
        return {'subject': subject, 'time': seconds}


def track(item, task="N/A", start=None):
    """Track the item that is passed in"""
    end()
    
    if start is None:
        now = datetime.datetime.now()
    else:
        if isinstance(start, str):
            now = datetime.datetime.fromisoformat(start)
        else:
            now = start

    events = read()
    events.add(Event(item, task, now, now, "started"))
    events.write()


def mark(when=None):
    """Mark the current task, if it exists.
    A marked event, if cancelled by the user, will instead be considered to
    have ended the last time the user marked the task."""
    events = read()

    if not events:
        return

    if when is None:
        when = datetime.datetime.now()

    latest = events[-1]

    if latest.flag == "ended" or latest.flag == "cancelled":
        return

    latest.end = when
    latest.flag = "marked"
    events.write()


def cancel():
    """Cancel the current event, if it exists. Does nothing if no current event.

    If event is marked, make the last marked time the end time.
    Else, delete the event.
    """
    events = read()
    if not events:
        return

    latest = events[-1]

    if latest.flag == "ended" or latest.flag == "cancelled":
        return
    if latest.flag == "marked":  # If marked, make last marked time the end time
        latest.flag = "ended"
    else:
        latest.end = datetime.datetime.now()  # to determine inactivity
        latest.flag = "cancelled"
    events.write()


def end(when=None):
    """
    End the event
    """
    if when is None:
        when = datetime.datetime.now()
    elif isinstance(when, str):
        when = datetime.datetime.fromisoformat(when)

    events = read()
    if not events:
        return False
    latest = events[-1]
    if latest.flag == "ended" or latest.flag == "cancelled":
        return False

    latest.end = when
    latest.flag = "ended"
    events.write()
    return True

