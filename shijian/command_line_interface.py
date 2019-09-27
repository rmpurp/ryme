import argparse
import datetime as dt
from datetime import time, datetime, timedelta

from tabulate import tabulate

import fileio
import readline
import task
from date_interpretation import interpret_date
from task_manager import TaskManager

# TODO add help
# TODO Add time travel feature

INVALID_NAME_MSG = 'No/invalid name specified.'
COMPLETE_MSG = 'Task "{}" (ID {}) completed.'
INVALID_ID_MSG = 'No/invalid ID specified.'


def print_completed_tasks(completed_tasks_dict):
    print(tabulate(
        map(lambda x: [x, completed_tasks_dict[x].name], completed_tasks_dict),
        ['ID', 'Completed Tasks']))


def print_table(manager, highlight_row=None):
    print()
    print(get_table(highlight_row, manager))


def get_table(highlight_row, manager):
    date = adjust_date(dt.date.today())
    return tabulate(
        manager.to_table(highlight_row=highlight_row, reference_date=date),
        ['ID', 'Task', 'Priority', 'Todo', 'Due Date', 'Left'],
        floatfmt=(".1f", '.1f', ".2f", '.1f', '.1f', '.1f', '.1f'),
        )


def new_task(args):
    name = ' '.join(args.name)

    if not name:
        print(INVALID_NAME_MSG)
        return

    date_str = args.date

    if date_str:
        try:
            date = interpret_date(date_str)
        except ValueError as e:
            print(e)
            return
    else:
        date = None

    estimated_hours = float(args.est_hours)

    manager = TaskManager(fileio.load())
    id = manager.new_task(name, estimated_hours, date)
    fileio.save(manager.task_dict)

    print_table(manager, id)


def list_tasks(args):
    manager = TaskManager(fileio.load())
    print_table(manager)


def complete_task(args):
    manager = TaskManager(fileio.load())
    ids = args.id
    if not ids:
        print(INVALID_ID_MSG)
    else:
        completed_tasks_dict = dict()
        for i in ids:
            try:
                completed_tasks_dict[i] = manager.task_dict[i]
                manager.complete(i)
                fileio.save(manager.task_dict)
            except KeyError:
                print(INVALID_ID_MSG)
        print_table(manager)
        print()
        print_completed_tasks(completed_tasks_dict)


def modify_task(args):
    manager = TaskManager(fileio.load())
    task_id = args.id
    try:
        old_task: task.Task = manager.task_dict[task_id]
        new_name = args.name if args.name else old_task.name
        if args.date:
            new_date = interpret_date(args.date)
        elif args.floating or isinstance(old_task, task.FloatingTask):
            new_date = None
        else:
            new_date = old_task.due_date
        new_hours_remaining = args.est_hours if args.est_hours else old_task.hours_remaining
        manager.new_task(new_name, new_hours_remaining, new_date, task_id)
        fileio.save(manager.task_dict)
        print_table(manager, task_id)
    except KeyError:
        print(INVALID_ID_MSG)
    except ValueError as e:
        print(e)


def clock(args):
    manager = TaskManager(fileio.load())
    task_id = args.id
    to_deduct = args.to_deduct
    # TODO Complete if less than/eq 0?
    try:
        old_task: task.Task = manager.task_dict[task_id]
        old_task.hours_remaining -= to_deduct

        fileio.save(manager.task_dict)
        print_table(manager, task_id)
    except KeyError:
        print(INVALID_ID_MSG)


def is_float(x):
    try:
        float(x)
        return True
    except ValueError:
        return False


def adjust_date(date):
    if datetime.now().time() < time(6):
        date = date - timedelta(days=1)
    return date


def is_date(x):
    if not x:
        return True
    try:
        interpret_date(x)
        return True
    except ValueError:
        return False


def creation_prompt(args):
    if not args.name:
        name = input('name > ').strip()
        args.name = [name]

    if not args.est_hours:
        est_hours = input('hours to completion > ').strip()
        args.est_hours = float(est_hours)

    if not args.date and not args.floating:
        date = input('date (empty for floating) > ').strip()

        if not date:
            date = None

        args.date = date

    new_task(args)

    '''
    name = input('name > ').strip()
    while not name:
        print(INVALID_NAME_MSG)
        name = input('name > ')

    est_hours = input('hours to completion > ').strip()
    while not is_float(est_hours):
        print('Not a float.')  # Extract to constant?
        est_hours = input('hours to completion > ').strip()
    
    est_hours = float(est_hours)
    
    date = input('date (empty for floating) > ').strip()
    while not is_date(date):
        print('Invalid date') #  get error msg?
        date = input('date (empty for floating) > ').strip()
    '''


def run():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    quick_new_parser = subparsers.add_parser('add',
                                             aliases=['quick_add', 'a', 'qa',
                                                      'q'])
    quick_new_parser.add_argument('name', metavar='N', nargs='*')
    group = quick_new_parser.add_mutually_exclusive_group()
    group.add_argument('-d', '--date', required=False)
    group.add_argument('-f', '--floating', required=False, action='store_true')
    quick_new_parser.add_argument('-e', '--est_hours', required=False,
                                  type=float)
    quick_new_parser.set_defaults(func=creation_prompt)

    ls_parser = subparsers.add_parser('ls', aliases=['l'])
    ls_parser.set_defaults(func=list_tasks)

    complete_parser = subparsers.add_parser('done', aliases=['d', 'rm'])
    complete_parser.add_argument('id', metavar='I', type=int, nargs='+')
    complete_parser.set_defaults(func=complete_task)

    modify_parser = subparsers.add_parser('modify', aliases=['m'])
    modify_parser.add_argument('id', metavar='I', type=int)
    group = modify_parser.add_mutually_exclusive_group()
    group.add_argument('-d', '--date', required=False)
    group.add_argument('-f', '--floating', required=False, action='store_true')
    modify_parser.add_argument('-e', '--est_hours', required=False, type=float)
    modify_parser.add_argument('-n', '--name', required=False)
    modify_parser.set_defaults(func=modify_task)

    clock_parser = subparsers.add_parser('clock', aliases=['c'])
    clock_parser.add_argument('id', metavar='I', type=int)
    clock_parser.add_argument('to_deduct', metavar='T', type=float)
    clock_parser.set_defaults(func=clock)

    args = parser.parse_args()  # input().split())
    # TODO allow specify priority threshold
    if hasattr(args, 'func'):
        args.func(args)
    else:
        list_tasks(None)


if __name__ == '__main__':
    run()
