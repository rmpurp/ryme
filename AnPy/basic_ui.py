import configparser
import datetime as dt
import os
import sqlite3

from tabulate import tabulate

from anpy import AbstractDataHandler
from anpy_lib import data_entry
from anpy_lib import file_management
from anpy_lib import table_generator
from anpy_lib.data_handling import SQLDataHandler


def prompt_menu(items, message='Select one of the following options.'):
    while True:
        print(message)
        for idx, item in enumerate(items):
            print('{}: {}'.format(idx, item))
        input_str = input('> ')
        try:
            num = int(input_str)
            if 0 <= num < len(items):
                return num
        except ValueError:
            pass
        print('Invalid input')


def create_categories(handler: AbstractDataHandler):
    while True:
        print("Please type the category names separated by commas. " +
              "Type 'quit' to exit prompt.")
        input_str = input('> ')
        if input_str == 'quit':
            return
        elif input_str:
            for category in input_str.split(','):
                handler.new_category(category)
            print('Categories created.')
            return


def prompt_with_default(message, default):
    print(message)
    result = input('[Default={}] > '.format(default))
    if not result:
        return default
    return result


def prompt_date(defaults: dt.datetime):
    year = int(prompt_with_default('Please select a year.', defaults.year))
    month = int(prompt_with_default('Please select a year.', defaults.month))
    day = int(prompt_with_default('Please select a day.', defaults.day))
    hour = int(prompt_with_default('Please select hour [24 hour time].',
                                   defaults.hour))
    minute = int(prompt_with_default('Please select minute.', defaults.minute))
    return dt.datetime(year, month, day, hour, minute)


def confirm(message):
    print(message)
    result = ''
    while not result or result[0] not in ['y', 'n']:
        result = input('Y/N: ').lower()
    return True if result[0] == 'y' else False


def active_session(handler: AbstractDataHandler, path):
    print()
    session = handler.get_most_recent_session()
    print('The session {}, started on {}, is currently running.'.format(
        session.name, session.time_start.strftime('%A at %I:%M %p')))
    action = prompt_menu(
        ['Complete', 'Complete and adjust', 'Adjust Start Time', 'Invalidate',
         'Quit Program'])
    if action == 0:
        print('Completed.')
        handler.complete()
    elif action == 1:
        print('Please enter new completion date and time.')
        date = prompt_date(session.time_start)
        if date < session.time_start:
            print('Invalid date.')
        elif confirm('Is {} correct?'.format(date.strftime('%A at %I:%M %p'))):
            handler.complete(date)
            print('Completed.')
        else:
            print('Cancelled.')
    elif action == 2:
        print('Please enter new start date and time.')
        date = prompt_date(session.time_start)
        if confirm('Is {} correct?'.format(date.strftime('%A at %I:%M %p'))):
            cat = handler.get_most_recent_session().name
            handler.cancel()
            handler.start(cat, date)
    elif action == 3:
        print('Canceled.')
        handler.cancel()
    elif action == 4:
        print('Exiting...')
        exit()


def options(handler: AbstractDataHandler, path):
    print()
    action = prompt_menu(['Add Categories', 'Rename Category',
                          'Archive Categories', 'Change Export Path'])
    if action == 0:
        create_categories(handler)
    elif action == 1:
        print('Action not available yet.')
    elif action == 2:
        print('Action not available yet.')
    elif action == 3:
        create_config(path)


def not_active_session(handler: AbstractDataHandler, path):
    print()
    action = prompt_menu(
        ['Start Session', 'Export to Excel', 'Options', 'Quit Program'])
    if action == 0:
        menu = list(handler.active_categories) + ['Back']
        sub_action = prompt_menu(menu, 'Please select a category.')
        if sub_action == len(menu) - 1:
            return
        else:
            handler.start(handler.active_categories[sub_action])
            print('Session for {} started'.format(
                handler.active_categories[sub_action]))
    elif action == 1:
        wb = data_entry.load_excel_workbook(path)
        ws, date = data_entry.get_relevant_worksheet(wb, None)
        data_entry.enter_week_data(date, handler, ws)
        wb.save(path)
        print('Exported.\n')
    elif action == 2:
        options(handler, path)
    elif action == 3:
        print('Exiting...')
        exit()


def create_config(path):
    config = configparser.ConfigParser()
    excel_path = get_input(message='Please enter path to write Excel file',
                           key=clean_excel_file)
    config['Paths'] = {'LogFile': excel_path}
    with open(path, 'w') as config_file:
        config.write(config_file)


def clean_excel_file(excel_path):
    if os.path.isdir(excel_path):
        excel_path = os.path.join(excel_path, 'log.xlsx')
    elif not (excel_path.endswith('.xlsx') or excel_path.endswith('.xlsm')):
        excel_path += '.xlsx'
    return excel_path


def get_input(message, default=None, key=None, validate=None):
    # Validate is a function that validates the input
    # key is a function whose result replaces the input when being validated
    # and/or returned
    if key is None:
        key = lambda x: x
    if validate is None:
        validate = lambda x: True
    while True:
        try:
            print()
            print(message)
            if default:
                result = input('[default: {}]> '.format(default))
                result = result if result else default
            else:
                result = input('> ')
            if validate(key(result)):
                return key(result)
            print('Invalid input!')
        except ValueError:
            print('Bad input.')


def get_date(default: dt.date = None) -> dt.date:
    date = get_input('Please enter a date according ISO 8601 (YYYY-MM-DD)',
                     str(default) if default is not None else None,
                     key=lambda x: dt.date(
                         *(int(comp) for comp in x.split('-'))))
    return date


def get_time(default: dt.time = None) -> dt.time:
    default = str(default.replace(microsecond=0,
                                  second=default.second + 1)) if default else None
    time = get_input('Please enter a 24 hour time (HH:MM[:SS])',
                     default,
                     key=lambda x: dt.time(
                         *(int(comp) for comp in x.split(':'))))
    return time


def get_datetime(default: dt.datetime) -> dt.datetime:
    date = get_date(default.date() if default is not None else None)
    time = get_time(default.time() if default is not None else None)
    return dt.datetime.combine(date, time)


def get_path(path):
    if not os.path.exists(path):
        create_config(path)
    config = configparser.ConfigParser()
    config.read(path)
    if 'Paths' not in config.sections():
        print('Invalid config file.')
        create_config(path)
        get_path(path)
    elif 'LogFile' not in config['Paths']:
        print('Invalid config file.')
        create_config(path)
        get_path(path)
    else:
        return config['Paths']['LogFile']


prompt_date = get_datetime

if __name__ == '__main__':
    # DATABASE_FILE = 'data.db'
    # CONFIG_FILE = 'config.ini'
    file_management.create_anpy_dir_if_not_exist()
    handler = SQLDataHandler(sqlite3.Connection(file_management.DATABASE_PATH))

    if not handler.active_categories:
        create_categories(handler)

    path = get_path(file_management.CONFIG_PATH)

    table, headers = table_generator.create_table_iterable_and_headers(
        data_handler=handler)

    print(tabulate(table, headers=headers))


    while True:
        if handler.is_active_session():
            active_session(handler, path)
        else:
            not_active_session(handler, path)
