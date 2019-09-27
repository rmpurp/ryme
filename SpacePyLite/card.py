import datetime
import json
from utils import calculate_easiness_delta, round_time_delta_to_day


class Card:
    def __init__(self, description, response, metadata=None):
        self.description = description
        self.response = response
        if not metadata:
            self.metadata = {
                'ef': 2.5,
                'iter_num': 0,
                'next_review': datetime.date.today(),
                'iter_length': datetime.timedelta(days=0)
            }
        else:
            try:
                self.metadata = json.loads(metadata)
                self.next_review = datetime.date.fromisoformat(
                    self.next_review)
                self.iteration_length = datetime.timedelta(
                    days=self.iteration_length)

            except (json.decoder.JSONDecodeError, ValueError):
                print("Invalid JSON metadata string for {}: {}".format(
                    response, metadata))
                exit(1)

    def is_reviewable(self, current_date=None):
        if not current_date:
            current_date = datetime.date.today()

        return current_date >= self.next_review

    def __repr__(self):
        return 'Card({!r}, {!r}, {!r})'.format(self.description, self.response,
                                               self.metadata)

    def rate(self, score):
       self.easiness_factor = calculate_easiness_delta(
            score) + self.easiness_factor
        self.easiness_factor = max(self.easiness_factor, 1.3)
        self.iteration_number += 1

        if score < 2:
            self.iteration_number = 0
            self.iteration_length = datetime.timedelta(days=0)
        elif self.iteration_number == 1:
            self.iteration_length = datetime.timedelta(days=1)
        elif self.iteration_number == 2:
            self.iteration_length = datetime.timedelta(days=6)
        else:
            self.iteration_length *= self.easiness_factor
            self.iteration_length = round_time_delta_to_day(
                self.iteration_length)
        self.next_review = datetime.date.today() + self.iteration_length 

    def __str__(self):
        metadata_string_date = dict(self.metadata)
        metadata_string_date['next_review'] = self.next_review.isoformat()
        metadata_string_date['iter_length'] = self.iteration_length.days
        return '\n'.join((self.description, self.response,
                          json.dumps(metadata_string_date)))

    def make_accessors(key):
        def getter(self):
            return self.metadata[key]

        def setter(self, value):
            self.metadata[key] = value
        return getter, setter

    easiness_factor = property(*make_accessors('ef'))
    iteration_number = property(*make_accessors('iter_num'))
    next_review = property(*make_accessors('next_review'))
    iteration_length = property(*make_accessors('iter_length'))
