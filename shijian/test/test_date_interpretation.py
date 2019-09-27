import unittest
import datetime as dt
from date_interpretation import interpret_date


class TestDateInterpretation(unittest.TestCase):

    def test_add_days(self):
        ref_date = dt.date(2018, 10, 30)

        strings_to_results = {
            '+0': ref_date,
            '+1': dt.date(2018, 10, 31),
            '+2': dt.date(2018, 11, 1),
            '+3': dt.date(2018, 11, 2),
            '+32': dt.date(2018, 12, 1),
            '+62': dt.date(2018, 12, 31),
            '+63': dt.date(2019, 1, 1),
            '+64': dt.date(2019, 1, 2)
        }
        for key in strings_to_results:
            self.assertEqual(strings_to_results[key],
                             interpret_date(key, ref_date))

    def test_next_given_weekday(self):
        ref_date = dt.date(2018, 10, 30)

        strings_to_results = {
            'w': dt.date(2018, 10, 31),
            'W': dt.date(2018, 10, 31),
            'th': dt.date(2018, 11, 1),
            'tH': dt.date(2018, 11, 1),
            'Th': dt.date(2018, 11, 1),
            'r': dt.date(2018, 11, 1),
            'R': dt.date(2018, 11, 1),
            'f': dt.date(2018, 11, 2),
            'a': dt.date(2018, 11, 3),
            'sa': dt.date(2018, 11, 3),
            's': dt.date(2018, 11, 4),
            'su': dt.date(2018, 11, 4),
            'm': dt.date(2018, 11, 5),
            't': dt.date(2018, 11, 6),
            'tu': dt.date(2018, 11, 6),
        }

        bad_input = ['asdf', '2345', 'grg234', 'ww', 'wed', 'fri']

        for key in strings_to_results:
            self.assertEqual(strings_to_results[key],
                             interpret_date(key, ref_date))

        for bad in bad_input:
            with self.assertRaises(ValueError):
                interpret_date(bad, ref_date)

    def test_given_mdy(self):
        ref_date = dt.date(2018, 10, 30)
        strings_to_results = {
            '2012-12-30': dt.date(2012, 12, 30),
            '2018-1-1': dt.date(2018, 1, 1),
            '2018.1.1': dt.date(2018, 1, 1),
            '2018/1/1': dt.date(2018, 1, 1),
            '2018-1/1': dt.date(2018, 1, 1),
            '2018-01/1': dt.date(2018, 1, 1),
            '2018-01/01': dt.date(2018, 1, 1),
            '18-01/01': dt.date(2018, 1, 1),
            '2016/2/29': dt.date(2016, 2, 29),
            '18/2/28': dt.date(2018, 2, 28)
        }

        for key in strings_to_results:
            self.assertEqual(strings_to_results[key],
                             interpret_date(key, ref_date))

        bad_input = '2018.2/29 2017.2-29 2011/2/2/2 2013.31/3 18.13.4'.split()

        for bad in bad_input:
            with self.assertRaises(ValueError):
                interpret_date(bad, ref_date)

    def test_given_md(self):
        ref_date = dt.date(2018, 10, 30)
        strings_to_results = {
            '11-30': dt.date(2018, 11, 30),
            '12-30': dt.date(2018, 12, 30),
            '1-1': dt.date(2019, 1, 1),
            '1.1': dt.date(2019, 1, 1),
            '1/1': dt.date(2019, 1, 1),
            '01/1': dt.date(2019, 1, 1),
            '01/02': dt.date(2019, 1, 2),
            '2/28': dt.date(2019, 2, 28)
        }

        for key in strings_to_results:
            self.assertEqual(strings_to_results[key],
                             interpret_date(key, ref_date))

        bad_input = '2/29 2-29 2/2/2 31/3 12.32 13.4'.split()

        for bad in bad_input:
            with self.assertRaises(ValueError):
                interpret_date(bad, ref_date)

    def test_misc(self):
        with self.assertRaises(ValueError):
            interpret_date('', reference_date=dt.date.today())

        with self.assertRaises(ValueError):
            interpret_date(None, reference_date=dt.date.today())

        self.assertEqual(dt.date.today() + dt.timedelta(days=2),
                         interpret_date('+2'))


if __name__ == '__main__':
    unittest.main()
