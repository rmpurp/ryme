#!/usr/bin/env PYTHONIOENCODING=UTF-8 /Users/rpurp/.pyenv/shims/python

import tabulate
import interface
import os
from itertools import zip_longest
from os.path import expanduser
import operator
import datetime
from dateutil import relativedelta
from utils import seconds_to_readable_str

devnull = open(os.devnull, "w")
script = expanduser("~/dev/surveiller/surveiller.py")
titlefont = " | size=14 font=FantasqueSansMonoNerdFontComplete-Bold color=white"
tablefont = " | size=14 font=FantasqueSansMonoNerdFontComplete-Regular color=#00802b"
trackfont = " | size=14 font=FantasqueSansMonoNerdFontComplete-Regular color=yellow"
subfont = " | size=14 font=FantasqueSansMonoNerdFontComplete-Italic color=gray"


def dict_to_table(d):
    return sorted(d.items(), key=operator.itemgetter(1))

def output_table(title, it):
    print('---')
    print(title + titlefont)
    table = tabulate.tabulate(it, tablefmt="plain")
    for line in table.split('\n'):
        if line.strip() == '': continue
        print(line + tablefont)


def splice_tables(title1, title2, it1, it2):
    it1 = dict_to_table(it1)
    it1 = map(lambda item: (item[0], seconds_to_readable_str(item[1])), it1)
    it2 = dict_to_table(it2)
    it2 = map(lambda item: (item[0], seconds_to_readable_str(item[1])), it2)

    print('---')
    print(title1 + titlefont)
    print(title2 + titlefont + " alternate=true")

    table1 = tabulate.tabulate(it1, tablefmt="plain")
    table2 = tabulate.tabulate(it2, tablefmt="plain")
    lines1 = table1.split('\n')
    lines2 = table2.split('\n')
    for l1, l2 in zip_longest(lines1, lines2, fillvalue=""):
        if l1.strip() == '' and l2.strip() == '': continue
        print(l1 + tablefont)
        print(l2 + ' ' + tablefont + ' alternate=true trim=false')


def make_python_call_string(title, *args, font=subfont):
    python_loc = "/Users/rpurp/.pyenv/shims/python"
    # TODO just python 3?

    command = "{} | bash={} ".format(title, python_loc)

    for i, arg in enumerate(args, 1):
        command += 'param{}="{}" '.format(i, arg)

    command += "terminal=false refresh=true"
    command += font
    return command


print(interface.status())
print('---')
print('Track' + titlefont)

for subject in interface.get_subjects():
    print(make_python_call_string(subject, script, "-t", subject, font=trackfont))
print(make_python_call_string("mark", script, "-m"))
print(make_python_call_string("cancel", script, "-c"))
print(make_python_call_string("end", script, "-e"))

print('---')

now = datetime.datetime.now()

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

splice_tables("Last 24 hours", "Today", interface.get_progress(last_24_hours),
              interface.get_progress(last_day))
print(interface.get_total(last_24_hours) + subfont)
print(interface.get_total(last_day) + subfont + " alternate=true")

splice_tables("Last 7 Days", "Last Work Week", interface.get_progress(last_week),
              interface.get_progress(last_workweek))
print(interface.get_total(last_week) + subfont)
print(interface.get_total(last_workweek) + subfont + " alternate=true")

