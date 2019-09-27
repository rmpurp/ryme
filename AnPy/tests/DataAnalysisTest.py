import datetime as dt
import os
import random
import sqlite3
import unittest

from anpy import Record
from anpy_lib import data_analysis
from anpy_lib.data_handling import SQLDataHandler

DATABASE_PATH = 'anpy_test_database.db'


class DataAnalysisTest(unittest.TestCase):

    def tearDown(self):
        os.remove(DATABASE_PATH)

    def setUp(self):
        pass

    def test_get_records_week(self):
        handler = SQLDataHandler(sqlite3.Connection(DATABASE_PATH))
        subjects = 'a b c d e'.split(' ')

        for s in subjects:
            handler.new_category(s)

        categories = handler.active_categories

        start_date = dt.datetime(2000, 5, 1, 4, 30)

        for i in range(500):
            handler.start(random.choice(list(categories)), start_date)
            duration = dt.timedelta(seconds=random.randint(30, 60) * 60)
            handler.complete(start_date + duration)
            advance = dt.timedelta(seconds=random.randint(0, 60) * 60)
            start_date = start_date + advance + duration

        day = dt.datetime(2000, 5, 1, 6, 0)
        tuesday = data_analysis.get_records_on_day(handler,
                                                   day + dt.timedelta(days=1))
        thursday = data_analysis.get_records_on_day(handler,
                                                    day + dt.timedelta(days=3))

        actuals = data_analysis.get_records_on_week(handler,
                                                    day_start=day)

        self.assertEqual(actuals[1], tuesday)
        self.assertEqual(actuals[3], thursday)

    def test_get_records_day(self):
        handler = SQLDataHandler(sqlite3.Connection(DATABASE_PATH))
        subjects = 'a b c'.split(' ')
        for s in subjects:
            handler.new_category(s)

        start0 = dt.datetime(2002, 4, 6, 3, 0)
        end0 = dt.datetime(2002, 4, 6, 10, 0)

        start1 = dt.datetime(2002, 4, 6, 11, 0)
        end1 = dt.datetime(2002, 4, 6, 12, 0)

        start2 = dt.datetime(2002, 4, 6, 13, 0)
        end2 = dt.datetime(2002, 4, 6, 13, 30)

        start3 = dt.datetime(2002, 4, 7, 1, 0)
        end3 = dt.datetime(2002, 4, 7, 8, 0)

        day1 = dt.datetime(2002, 4, 5, 6, 0)
        day2 = dt.datetime(2002, 4, 6, 6, 0)
        day3 = dt.datetime(2002, 4, 7, 6, 0)

        starts = [start0, start1, start2, start3]
        ends = [end0, end1, end2, end3]

        categories = handler.active_categories
        cats = 'a c a a'.split(' ')

        for c, s, e in zip(cats, starts, ends):
            handler.start(c, s)
            handler.complete(e)

        day_one_stats = list(data_analysis.get_records_on_day(handler, day1))
        day_two_stats = list(data_analysis.get_records_on_day(handler, day2))
        day_three_stats = list(data_analysis.get_records_on_day(handler, day3))

        self.assertEqual(len(day_one_stats), 1)
        self.assertEqual(len(day_two_stats), 3)
        self.assertEqual(len(day_three_stats), 0)

        record_0 = Record('a', start0, end0)
        record_1 = Record('c', start1, end1)
        record_2 = Record('a', start2, end2)
        record_3 = Record('a', start3, end3)

        self.assertEqual(day_one_stats[0], record_0)
        self.assertEqual(day_two_stats[0], record_1)
        self.assertEqual(day_two_stats[1], record_2)
        self.assertEqual(day_two_stats[2], record_3)

        '''
        self.assertEqual(
            len(data_analysis.get_subject_breakdown(day_one_stats)), 1)
        self.assertEqual(
            len(data_analysis.get_subject_breakdown(day_two_stats)), 2)
        self.assertEqual(
            len(data_analysis.get_subject_breakdown(day_three_stats)), 0)

        self.assertTrue(
            day1_a_stat in data_analysis.get_subject_breakdown(day_one_stats))
        self.assertTrue(
            day2_c_stat in data_analysis.get_subject_breakdown(day_two_stats))
        self.assertTrue(
            day2_a_stat in data_analysis.get_subject_breakdown(day_two_stats))
        '''

if __name__ == '__main__':
    unittest.main()
