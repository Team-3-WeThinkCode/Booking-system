import unittest
from unittest import mock
import os
import sys
USER_PATHS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../'))
sys.path.insert(0, USER_PATHS)
import utilities

test_obj = [{'kind': 'calendar#event', 'etag': '"3210204165178000"', 'id': 'lo7ami5f9pu7s4qdlun76h7m2k', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=bG83YW1pNWY5cHU3czRxZGx1bjc2aDdtMmsgY29kZS5jbGluaWMudGVzdEBt', 'created': '2020-11-11T13:41:22.000Z', 'updated': '2020-11-11T13:41:22.589Z', 'summary': 'VOLUNTEER: jroy', 'location': 'WeThinkCode, Victoria & Alfred Waterfront, Cape Town', 'creator': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'organizer': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'start': {'dateTime': '2020-11-12T12:00:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'end': {'dateTime': '2020-11-12T12:30:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'iCalUID': 'lo7ami5f9pu7s4qdlun76h7m2k@google.com', 'sequence': 0, 'attendees': [{'email': 'jroy@student.wethinkcode.co.za', 'responseStatus': 'accepted'}], 'reminders': {'useDefault': True}},
    {'kind': 'calendar#event', 'etag': '"3210204167150000"', 'id': 'rq731nlq01brfe4egl6b9ifu14', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=cnE3MzFubHEwMWJyZmU0ZWdsNmI5aWZ1MTQgY29kZS5jbGluaWMudGVzdEBt', 'created': '2020-11-11T13:41:22.000Z', 'updated': '2020-11-11T13:41:23.575Z', 'summary': 'VOLUNTEER: jroy', 'location': 'WeThinkCode, Victoria & Alfred Waterfront, Cape Town', 'creator': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'organizer': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'start': {'dateTime': '2020-11-12T12:30:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'end': {'dateTime': '2020-11-12T13:00:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'iCalUID': 'rq731nlq01brfe4egl6b9ifu14@google.com', 'sequence': 0, 'attendees': [{'email': 'jroy@student.wethinkcode.co.za', 'responseStatus': 'accepted'}, {'email': 'fake@student.wethinkcode.co.za', 'responseStatus': 'accepted'}], 'reminders': {'useDefault': True}},
    {'kind': 'calendar#event', 'etag': '"3210167844640000"', 'id': 'd9h0im0u6scfdgk98o9kkf7o78', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=ZDloMGltMHU2c2NmZGdrOThvOWtrZjdvNzggY29kZS5jbGluaWMudGVzdEBt', 'created': '2020-11-11T08:38:42.000Z', 'updated': '2020-11-11T08:38:42.320Z', 'summary': 'VOLUNTEER: student', 'location': 'WeThinkCode, Victoria & Alfred Waterfront, Cape Town', 'creator': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'organizer': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'start': {'dateTime': '2020-11-13T10:00:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'end': {'dateTime': '2020-11-13T11:30:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'iCalUID': 'd9h0im0u6scfdgk98o9kkf7o78@google.com', 'sequence': 0, 'attendees': [{'email': 'student@student.wethinkcode.co.za', 'responseStatus': 'needsAction'}], 'reminders': {'useDefault': True}}]


class Test(unittest.TestCase):


    #tests the create makeshift function
    def test_create_makeshift_event(self):
        result = True
        event = utilities.create_makeshift_event('', '', '', '', '', [])
        keys = ['summary', 'location', 'description', 'start', 'end', 'attendees', 'reminders']
        for key in keys:
            if key not in event:
                result = False
        self.assertEqual(result, True)

    def test_split_username(self):
        username = utilities.split_username("jdoe@student.wethinkcode.co.za")
        self.assertEqual(username, "jdoe")
        

    # def test_is_leap_year_with_leap_year(self):
    #     result = utilities.is_leap_year(2020)
    #     self.assertTrue(result)

    
    # def test_is_leap_year_with_year_that_is_not_leap_year(self):
    #     result = utilities.is_leap_year(2019)
    #     self.assertFalse(result)

    #tests the check date and time function
    def test_date_fomat_correct_with_correct_format(self):
        result = utilities.check_date_and_time_format('2030-11-14', '16:00')
        self.assertTrue(result)

    
    def test_date_fomat_correct_with_incorrect_format_1(self):
        result = utilities.check_date_format('202-11-14')
        self.assertFalse(result)


    def test_date_fomat_correct_with_incorrect_format_2(self):
        result = utilities.check_date_format('20k0-11-')
        self.assertFalse(result)


    # def test_get_date_with_valid_input(self):
    #     original_input = mock.builtins.input
    #     mock.builtins.input = lambda _: '2020-11-14'
    #     self.assertEqual(utilities.get_date(), '2020-11-14')


    # def test_get_date_with_invalid_then_valid_input(self):
    #     original_input = mock.builtins.input
    #     mock.builtins.input = lambda _: '20k0-11-'
    #     mock.builtins.input = lambda _: '2020-11-14'
    #     self.assertEqual(utilities.get_date(), '2020-11-14')

    # def test_sort_open_slots(self):
        
    #     new_list = utilities.sort_open_slots(test_obj, username="student")
    #     self.assertEqual(new_list, [self.test_obj[0]])


    def test_sort_booked_slots_false(self):
        new_list = utilities.sort_booked_slots(test_obj, username="jdoe")
        self.assertEqual(new_list, [])


    # def test_sort_booked_slots(self):
    #     new_list = utilities.sort_booked_slots(test_obj, username="jroy")
    #     self.assertEqual(new_list, [self.test_obj[0], self.test_obj[1]])

    def test_sort_open_slots_false(self):
        new_list = utilities.sort_open_slots([{"key": "value"}], username="jroy")
        self.assertEqual(new_list, [])

    def test_convert_date_and_time_to_rfc_format(self):
        start_datetime, end_datetime = utilities.convert_date_and_time_to_rfc_format('2020-11-14', '13:30', '14:00')
        self.assertEqual(start_datetime, '2020-11-14T13:30:00+02:00')
        self.assertEqual(end_datetime, '2020-11-14T14:00:00+02:00')


if __name__ == "__main__":
    unittest.main()