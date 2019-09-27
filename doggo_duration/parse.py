import re

def all_prefixes(s):
    return [s[:i] for i in range(1, 1 + len(s))]

HOUR_INDICATORS = all_prefixes("hours") + [':']
MINUTE_INDICATORS = all_prefixes("minutes")

    
def sanitize(duration):
    return duration.lower().replace("and", "").strip().replace(" ", "")

def parse_hours_and_minutes(duration):
    if re.search(r"\d\s+\d", duration):
        raise ValueError("Ambiguous consecutive numbers.")

    duration = sanitize(duration)

    matcher = re.compile(r"^((?P<hour>\d+)({}))?((?P<minute>\d+)({})?)?$"
                         .format('|'.join(HOUR_INDICATORS),
                                 '|'.join(MINUTE_INDICATORS)))

    matches = matcher.search(duration)

    if not matches:
        raise ValueError("Invalid syntax")

    hours, minutes = matches.group("hour"), matches.group("minute")

    if hours is None: hours = 0
    if minutes is None: minutes = 0

    return int(hours), int(minutes)


def parse(duration):
    hours, minutes = parse_hours_and_minutes(duration)
    return hours * 60 + minutes

