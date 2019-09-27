import datetime
from dateutil import relativedelta

if __name__ == '__main__':
    now = datetime.datetime(2019, 4, 22, 3, 59)
    four_hours_ago = now - datetime.timedelta(hours=4)
    last_24_hours = now - datetime.timedelta(days=1)
    last_day = four_hours_ago.replace(hour=4, minute=0, second=0, microsecond=0)

    last_week = now - datetime.timedelta(days=7)

    delta = relativedelta.relativedelta(weekday=relativedelta.MO(-1),
                                        hour=4,
                                        minute=0,
                                        second=0,
                                        microsecond=0)
    last_workweek = four_hours_ago + delta

    print(last_24_hours)
    print(last_day)
    print(last_week)
    print(last_workweek)

