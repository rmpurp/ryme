from abc import ABC, abstractmethod
from datetime import date
from json import dumps
from math import exp

FLOATING_PRIORITY = 0.49


class Task(ABC):
    def __init__(self, name: str, identifier, estimated_num_hours):
        self.name = name
        self.identifier = identifier
        self.hours_remaining = estimated_num_hours

    @abstractmethod
    def priority(self, reference_date: date = None):
        pass

    @abstractmethod
    def to_table_row(self, reference_date=None):
        pass

    @abstractmethod
    def hours_to_do_today(self):
        pass

class FloatingTask(Task):
    def __init__(self, name, identifier, estimated_num_hours):
        self.type = "floating"
        super().__init__(name, identifier, estimated_num_hours)

    def priority(self, reference_date: date = None):
        return FLOATING_PRIORITY

    def to_json(self):
        return_dict = dict(self.__dict__)
        return_dict["__type__"] = "FloatingTask"
        return dumps(return_dict)

    def to_table_row(self, reference_date=None):
        return [self.identifier, self.name, self.priority(reference_date),
                self.hours_to_do_today(), 'FLOATING',
                self.hours_remaining]

    def __repr__(self):
        return 'FloatingTask({}, {})'.format(self.name, self.identifier)

    def hours_to_do_today(self):
        return 'N/A'


class DatedTask(Task):

    def __init__(self, name: str, identifier, due_date, estimated_num_hours):
        self.due_date = due_date
        self.type = "dated"
        super().__init__(name, identifier, estimated_num_hours)

    def priority(self, reference_date: date = None, hour_bias=0):
        if reference_date is None:
            reference_date = date.today()

        hours_remaining = self.hours_remaining - hour_bias

        if hours_remaining <= 0:
            return 0

        days_behind = (self.due_date - reference_date).days

        # Logistic curve
        # changed to be based on 1.5 hours
        # changed back (to change again, switch to hours_remaining / 1.5
        return 1 / (1 + exp(4 * ((days_behind - 1) / (hours_remaining / 1) - 1)))

    def to_table_row(self, reference_date=None):
        row = [self.identifier, self.name,
               self.priority(reference_date=reference_date),
               self.hours_to_do_today(reference_date=reference_date), str(self.due_date),
               self.hours_remaining]
        return row

    def hours_to_do_today(self, reference_date=None):
        num_hours = 0
        while self.priority(hour_bias=num_hours, reference_date=reference_date) >= 0.5:
            num_hours += 0.5
        if num_hours == 0:
            return '0.0'
            # Fixes weird issue in tabulate where 0f
            # combined with ANSI commands caused an extra tab to appear
        return min(num_hours, self.hours_remaining)

    def __repr__(self):
        return 'DatedTask({}, {}, {}, {})'.format(self.name,
                                                  self.identifier,
                                                  self.due_date,
                                                  self.hours_remaining)


if __name__ == '__main__':
    x = DatedTask("adsf", 0, date(2018, 3, 10), 4)
    for i in range(-7, 7):
        print(i, x.priority(date(2018, 3, 10 + i)))
