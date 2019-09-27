from event import EventList
import datetime as dt


def group_by_week(events: EventList):
    oldest_event = events[0]
    week_beginning: dt.datetime = oldest_event.start - dt.timedelta(
        days=oldest_event.start.weekday())
    # TODO fix if first event is monday before 4 am but after 12 am
    d = dict()
    week_beginning = week_beginning.replace(hour=4, minute=0, second=0,
                                            microsecond=0)
    while True:
        week_end = week_beginning + dt.timedelta(days=7)
        filtered = events.group_by_subject(week_beginning, week_end)
        if len(filtered) == 0:
            break
        d[week_beginning] = filtered
        week_beginning = week_end
    return d
