def seconds_to_readable_str(seconds, separator='', use_days=False):
    hours, minutes = seconds // 3600, seconds // 60 % 60
    days = hours // 24
    if days > 0 and use_days:
        hours = hours % 24
        return "{}d {}h".format(days, hours)
    else:
        if separator:
            separator += " "
        return "{}h {}{}m".format(hours, separator, minutes)
