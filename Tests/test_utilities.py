import unittest
from unittest import mock
import os
import sys
USER_PATHS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../'))
sys.path.insert(0, USER_PATHS)
import utilities


class Test(unittest.TestCase):

    def test_list_slots(self):
        pass


    def test_create_makeshift_event(self):
        result = True
        event = utilities.create_makeshift_event('', '', '', '', '', [])
        keys = ['summary', 'location', 'description', 'start', 'end', 'attendees', 'reminders']
        for key in keys:
            if key not in event:
                result = False
        self.assertEqual(result, True)


    def test_is_leap_year_with_leap_year(self):
        result = utilities.is_leap_year(2020)
        self.assertTrue(result)

    
    def test_is_leap_year_with_year_that_is_not_leap_year(self):
        result = utilities.is_leap_year(2019)
        self.assertFalse(result)


    def test_date_fomat_correct_with_correct_format(self):
        result = utilities.date_fomat_correct('2020-11-14')
        self.assertTrue(result)


    def test_date_fomat_correct_with_incorrect_format_1(self):
        result = utilities.date_fomat_correct('202-11-14')
        self.assertFalse(result)


    def test_date_fomat_correct_with_incorrect_format_2(self):
        result = utilities.date_fomat_correct('20k0-11-')
        self.assertFalse(result)


    def test_get_date_with_valid_input(self):
        original_input = mock.builtins.input
        mock.builtins.input = lambda _: '2020-11-14'
        self.assertEqual(utilities.get_date(), '2020-11-14')


    def test_get_date_with_invalid_then_valid_input(self):
        original_input = mock.builtins.input
        mock.builtins.input = lambda _: '20k0-11-'
        mock.builtins.input = lambda _: '2020-11-14'
        self.assertEqual(utilities.get_date(), '2020-11-14')


    def test_convert_date_and_time_to_rfc_format(self):
        start_datetime, end_datetime = utilities.convert_date_and_time_to_rfc_format('2020-11-14', '13:30', '14:00')
        self.assertEqual(start_datetime, '2020-11-14T13:30:00+02:00')
        self.assertEqual(end_datetime, '2020-11-14T14:00:00+02:00')


if __name__ == "__main__":
    unittest.main()