#/Users/rpurp/.pyenv/shims/python

from sys import argv
from interface import get_progress, mark, end, cancel, track, merge_with, get_weekly
import datetime
from operator import itemgetter
from tabulate import tabulate
from utils import seconds_to_readable_str

def list_events(days):
    events = get_progress(
        datetime.datetime.now() - datetime.timedelta(days=days))
    sorted_events = map(lambda a: (a[0], seconds_to_readable_str(a[1])),
                        sorted(events.items(), key=itemgetter(1)))
    print(tabulate(sorted_events))


if len(argv) == 1 or argv[1] == '-l':
    list_events(1)
elif len(argv) == 3 and argv[1] == '-l':
    list_events(int(argv[2]))
elif len(argv) == 3 and argv[1] == '-t':
    track(argv[2])
elif len(argv) == 3 and argv[1] == '-i':
    merge_with(argv[2])
elif argv[1] == '-m':
    mark()
elif argv[1] == '-c':
    cancel()
elif argv[1] == '-e':
    end()
elif argv[1] == '-w':
    print(get_weekly())
else:
    print("Invalid!")


class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""

    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self):
        return self.impl()


class _GetchUnix:
    def __init__(self):
        pass

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


def menu(l):
    options = '123456789abcdefghijk'
    d = dict(zip(options, l))

    for option in d:
        print(option + ': ' + d[option])

    print("q: Quit\n")
    input_char = ''
    while input_char not in d:
        input_char = getch()
        if input_char == 'q':
            print('Quitting...')
            exit(1)
    return d[input_char]


getch = _Getch()
