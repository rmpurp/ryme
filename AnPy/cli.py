import argparse
import sqlite3

from tabulate import tabulate

from anpy_lib import file_management
from anpy_lib import table_generator
from anpy_lib.data_handling import SQLDataHandler


def set_up():
    file_management.create_anpy_dir_if_not_exist()
    handler = SQLDataHandler(sqlite3.Connection(file_management.DATABASE_PATH))
    return handler


def create_categories(args):
    handler = set_up()
    print('Creating...')
    for category in args.categories:
        try:
            handler.new_category(category)
        except ValueError:
            print('{} is invalid... skipping.'.format(category))


def start(args):
    requested_category = args.category
    handler = set_up()

    if handler.is_active_session():
        print('An active session is running!')
        return

    if args.create:
        try:
            handler.new_category(requested_category)
            category = requested_category
        except ValueError:
            print('{} is invalid (bad name or already exists)... cancelling.'
                  .format(requested_category))
            return
    elif requested_category in handler.active_categories:
        category = requested_category
    else:
        categories = handler.active_categories
        potential_matches = list(
            filter(lambda x: x.startswith(requested_category), categories))

        if not potential_matches:
            print('{} does not match any category names.'
                  .format(requested_category))
            return

        elif len(potential_matches) > 1:
            print('"{}" is ambiguous: could be {}'
                  .format(requested_category, potential_matches))
            return
        category = potential_matches[0]
    assert category
    handler.start(category)


def end(_):
    handler = set_up()
    if handler.is_active_session():
        handler.complete()
    else:
        print("There's no session running!")


def cancel(_):
    handler = set_up()
    if handler.is_active_session():
        handler.cancel()
    else:
        print('Cannot cancel: No active session.')


def status(_):
    handler = set_up()
    table, headers = table_generator.create_table_iterable_and_headers(
        data_handler=handler)
    print(tabulate(table, headers=headers))
    print()
    print('Active categories: {}'.format(', '.join(handler.active_categories)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers()
    create_parser = subparsers.add_parser('create',
                                          help='Create new categories')
    create_parser.add_argument('categories', metavar='C', nargs='+',
                               help='Categories to create. Active categories'
                                    'that already exist will be ignored.')
    create_parser.set_defaults(func=create_categories)

    start_subparser = subparsers.add_parser('start',
                                            help='Start a time-tracking'
                                                 'session with the given'
                                                 'category.')
    start_subparser.add_argument('category', metavar='C',
                                 help='Category under which timer is started. '
                                      'Abbreviated category name is supported '
                                      'as long as unambiugous (e.g. "w" for '
                                      'work')
    start_subparser.add_argument('-c', '--create', action='store_true',
                                 help='If flag is set, create the category '
                                      'if it does not already exist. If the '
                                      'flag is not set (default), then '
                                      'nothing will happen.')
    start_subparser.set_defaults(func=start)

    status_subparser = subparsers.add_parser('status',
                                             help='Displays the progress of '
                                                  'the previous 7 days and '
                                                  'displays the active '
                                                  'categories.')
    status_subparser.set_defaults(func=status)

    end_subparser = subparsers.add_parser('end', help='Completes the current '
                                                      'time-tracking session.')
    end_subparser.set_defaults(func=end)

    cancel_subparser = subparsers.add_parser('cancel',
                                             help='Cancels the current time-'
                                                  'tracking session.')
    cancel_subparser.set_defaults(func=cancel)

    parser.add_argument('-i', '--interactive', action='store_true')
    # TODO: implement interactive

    args = parser.parse_args()
    args.func(args)
