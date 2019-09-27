from math import log10

from termcolor import colored

import task


class TaskManager:
    def __init__(self, tasks=None):
        if tasks is None:
            tasks = dict()

        # self.task_dict: dict = {t.identifier: t for t in tasks}
        self.task_dict: dict = {int(x): tasks[x] for x in tasks}

    def head(self):
        return next(iter(self.get_tasks_by_priority()))

    def next_identifier(self):
        if not self.task_dict:
            return 0

        max_id = max(self.task_dict.keys())
        if int(log10(max_id + 1)) > int(
                log10(max_id + 0.1)):  # Prevent taking log(0)
            new_id = 0
            while new_id in self.task_dict.keys():
                new_id += 1
        else:
            new_id = max_id + 1

        return new_id

    def to_table(self, highlight_row=None, reference_date=None):
        priority_threshold = 0

        if highlight_row:
            priority_threshold = min(priority_threshold,
                                     self.task_dict[highlight_row].priority(
                                         reference_date=reference_date))
        rows = map(lambda x: x.to_table_row(reference_date=reference_date),
                   filter(lambda x: x.priority(
                       reference_date=reference_date) >= priority_threshold,
                          self.task_dict.values()))

        return map(get_highlight_func(highlight_row),
                   sorted(rows, key=lambda x: -float(x[2])))

    def new_task(self, name, estimated_num_hours, due_date=None, next_id=None):
        if next_id is None:
            next_id = self.next_identifier()
        if due_date:
            t = task.DatedTask(name, next_id, due_date, estimated_num_hours)
        else:
            t = task.FloatingTask(name, next_id, estimated_num_hours)
        self.task_dict[next_id] = t
        return next_id

    def complete(self, task_id):
        del self.task_dict[task_id]
        # Todo: Trash can?

    def get_tasks_by_priority(self):
        return sorted((self.task_dict.values()),
                      key=lambda x: x.priority())


def get_highlight_func(highlight_id):
    def highlight_if_row_matches(table_row):
        if str(table_row[0]) == str(highlight_id):
            return list(
                map(lambda x: colored(x, 'yellow', attrs=['bold', 'underline']),
                    table_row))
        elif table_row[2] > 0.5:
            return list(map(
                lambda x: colored(x, 'magenta', attrs=['bold', 'underline']),
                table_row))
        elif table_row[2] >= 0.2:
            return list(
                map(lambda x: colored(x, 'red', attrs=['bold']), table_row))
        else:
            return list(table_row)

    return highlight_if_row_matches
