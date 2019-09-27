import datetime as dt
import os
import sqlite3
import unittest

from anpy import Record
from anpy_lib.data_handling import SQLDataHandler

DATABASE_PATH = 'anpy_test_database.db'


class DataInputOutputTest(unittest.TestCase):

    def tearDown(self):
        os.remove(DATABASE_PATH)

    def setUp(self):
        pass

    def test_cancel(self):
        start = dt.datetime(2002, 4, 6, 5, 6)
        handler = SQLDataHandler(sqlite3.Connection(DATABASE_PATH))
        handler.new_category('Test')
        handler.start('Test', start)
        self.assertTrue(handler.is_active_session())
        handler.cancel()
        self.assertFalse(handler.is_active_session())

        records = handler.get_records_between(dt.datetime(2002, 4, 6, 5, 0),
                                              dt.datetime(2002, 4, 6, 5, 10))
        self.assertEquals(records, [])

    def test_multiple_sessions(self):
        start1 = dt.datetime(2010, 1, 1, 10, 10)
        end1 = dt.datetime(2010, 1, 1, 12)
        start2 = dt.datetime(2010, 1, 1, 13, 0)
        end2 = dt.datetime(2010, 1, 1, 15, 0)

        handler = SQLDataHandler(sqlite3.Connection(DATABASE_PATH))
        categories = 'AP Bio,AP Chem,Physics 2,Biology 101,CS 61A'.split(',')

        for cat in categories:
            handler.new_category(cat)

        handler.start('AP Chem', start1)
        self.assertTrue(handler.is_active_session())
        with self.assertRaises(RuntimeError):
            handler.start('Biology 101')
        handler.complete(end1)

        self.assertFalse(handler.is_active_session())

        handler.start('Biology 101', start2)
        self.assertTrue(handler.is_active_session())
        handler.complete(end2)

        self.assertFalse(handler.is_active_session())

        range_begins = [dt.datetime(2010, 1, 1, 10, 0),
                        dt.datetime(2010, 1, 1, 10, 0),
                        dt.datetime(2010, 1, 1, 10, 20),
                        dt.datetime(2010, 1, 1, 13, 5)]

        range_ends = [dt.datetime(2010, 1, 1, 10, 11),
                      dt.datetime(2010, 1, 1, 13, 14),
                      dt.datetime(2010, 1, 1, 13, 14),
                      dt.datetime(2010, 1, 1, 13, 10)]

        er1 = Record('AP Chem', start1, end1)
        er2 = Record('Biology 101', start2, end2)

        expecteds = [[er1], [er1, er2], [er2], []]

        for rb, re, expected in zip(range_begins, range_ends, expecteds):
            with self.subTest(rb=rb, re=re, expected=expected):
                result = list(handler.get_records_between(rb, re))
                self.assertEqual(expected, result)

    def test_basic_session(self):
        start = dt.datetime(2015, 4, 5, 2, 0)
        end = dt.datetime(2015, 4, 5, 3, 30)

        handler = SQLDataHandler(sqlite3.Connection(DATABASE_PATH))
        categories = 'AP Bio,AP Chem,Physics 2,Biology 101,CS 61A'.split(',')

        for cat in categories:
            handler.new_category(cat)

        with self.assertRaises(RuntimeError):
            handler.complete()

        with self.assertRaises(ValueError):
            handler.start(-5, dt.datetime.now())

        handler.start('AP Bio', start)
        self.assertTrue(handler.is_active_session())

        handler.complete(end)
        self.assertFalse(handler.is_active_session())

        range_begins = [dt.datetime(2015, 4, 5, 1, 0),
                        dt.datetime(2015, 4, 5, 1, 0),
                        dt.datetime(2015, 4, 5, 1, 0),
                        dt.datetime(2015, 4, 5, 2, 0),
                        dt.datetime(2015, 4, 5, 3, 0)]

        range_ends = [dt.datetime(2015, 4, 5, 1, 3),
                      dt.datetime(2015, 4, 5, 2, 0),
                      dt.datetime(2015, 4, 5, 2, 30),
                      dt.datetime(2015, 4, 5, 2, 30),
                      dt.datetime(2015, 4, 5, 4, 00)]

        expected_record = Record('AP Bio', start, end)
        successful_findings = [False, False, True, True, False]

        for rb, re, sf in zip(range_begins, range_ends, successful_findings):
            with self.subTest(rb=rb, re=re, sf=sf):
                result = list(handler.get_records_between(rb, re))
                if sf:
                    self.assertEqual(result[0], expected_record)
                else:
                    self.assertEqual(result, [])

    def test_category_activation(self):
        handler = SQLDataHandler(sqlite3.Connection(DATABASE_PATH))
        categories = 'AP Bio,AP Chem,Physics 2,Biology 101,CS 61A'.split(',')
        for subject in categories:
            handler.new_category(subject)
        handler.set_category_activation('AP Bio', False)
        handler.set_category_activation('CS 61A', False)
        expected = [False, True, True, True, False]
        active_categories = handler.active_categories
        for e, cat in zip(expected, categories):
            with self.subTest(e=e, cat=cat):
                self.assertEqual(cat in active_categories, e, cat)

        all_categories = handler.all_categories
        for cat in categories:
            with self.subTest(cat=cat):
                self.assertTrue(cat in all_categories)

        with self.assertRaises(ValueError):
            handler.set_category_activation(-1, False)

    def test_rename(self):
        handler = SQLDataHandler(sqlite3.Connection(DATABASE_PATH))
        handler.new_category('AP Bio')
        handler.new_category('AP French')
        handler.new_category('CS 50')
        handler.rename_category('AP Bio', 'AP Biology')
        categories = handler.active_categories

        self.assertTrue('AP Biology' in categories)

        self.assertFalse('AP Bio' in categories)
        self.assertTrue('AP French' in categories)
        self.assertTrue('CS 50' in categories)

        with self.assertRaises(ValueError):
            handler.rename_category('apple', 'banana')

    def test_category_persistence(self):
        handler = SQLDataHandler(sqlite3.Connection(DATABASE_PATH))
        self.assertEqual(handler.active_categories, ())

        handler = SQLDataHandler(sqlite3.Connection(DATABASE_PATH))
        self.assertEqual(handler.active_categories, ())

        categories = 'AP Bio,AP Chem,Physics 2,Biology 101,CS 61A'.split(',')
        for subject in categories:
            handler.new_category(subject)
        self.assertEqual(set(handler.active_categories), set(categories))

        handler = SQLDataHandler(sqlite3.Connection(DATABASE_PATH))
        self.assertEqual(set(handler.active_categories), set(categories))

    def test_category_creation(self):
        handler = SQLDataHandler(sqlite3.Connection(DATABASE_PATH))
        self.assertEqual(handler.active_categories, ())
        with self.assertRaises(ValueError):
            handler.new_category('')

        categories = 'AP Bio,AP Chem,Physics 2,Biology 101,CS 61A'.split(',')
        added_categories = set()
        for i, subject in enumerate(categories, 1):
            with self.subTest(subject=subject):
                handler.new_category(subject)
                added_categories.add(subject)
                self.assertEqual(set(handler.active_categories),
                                 added_categories)

        with self.assertRaises(ValueError):
            handler.new_category(' ')
        for subject in categories:
            with self.subTest(subject=subject):
                with self.assertRaises(RuntimeError):
                    handler.new_category(subject)
        self.assertEqual(set(handler.active_categories), added_categories)

        handler.new_category('    decal     \t')
        self.assertTrue('decal' in handler.active_categories)


if __name__ == '__main__':
    unittest.main()
