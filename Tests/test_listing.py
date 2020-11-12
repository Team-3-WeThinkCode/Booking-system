import unittest
from unittest.main import main
from unittest.mock import patch
from io import StringIO
import sys
import os
USER_PATHS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../'))
sys.path.insert(0, USER_PATHS)
import event_listing
import booking

class test_joshua(unittest.TestCase):

    test_obj = [{'kind': 'calendar#event', 'etag': '"3210204165178000"', 'id': 'lo7ami5f9pu7s4qdlun76h7m2k', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=bG83YW1pNWY5cHU3czRxZGx1bjc2aDdtMmsgY29kZS5jbGluaWMudGVzdEBt', 'created': '2020-11-11T13:41:22.000Z', 'updated': '2020-11-11T13:41:22.589Z', 'summary': 'VOLUNTEER: jroy', 'location': 'WeThinkCode, Victoria & Alfred Waterfront, Cape Town', 'creator': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'organizer': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'start': {'dateTime': '2020-11-12T12:00:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'end': {'dateTime': '2020-11-12T12:30:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'iCalUID': 'lo7ami5f9pu7s4qdlun76h7m2k@google.com', 'sequence': 0, 'attendees': [{'email': 'jroy@student.wethinkcode.co.za', 'responseStatus': 'accepted'}], 'reminders': {'useDefault': True}},
    {'kind': 'calendar#event', 'etag': '"3210204167150000"', 'id': 'rq731nlq01brfe4egl6b9ifu14', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=cnE3MzFubHEwMWJyZmU0ZWdsNmI5aWZ1MTQgY29kZS5jbGluaWMudGVzdEBt', 'created': '2020-11-11T13:41:22.000Z', 'updated': '2020-11-11T13:41:23.575Z', 'summary': 'VOLUNTEER: jroy', 'location': 'WeThinkCode, Victoria & Alfred Waterfront, Cape Town', 'creator': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'organizer': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'start': {'dateTime': '2020-11-12T12:30:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'end': {'dateTime': '2020-11-12T13:00:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'iCalUID': 'rq731nlq01brfe4egl6b9ifu14@google.com', 'sequence': 0, 'attendees': [{'email': 'jroy@student.wethinkcode.co.za', 'responseStatus': 'accepted'}, {'email': 'fake@student.wethinkcode.co.za', 'responseStatus': 'accepted'}], 'reminders': {'useDefault': True}},
    {'kind': 'calendar#event', 'etag': '"3210167844640000"', 'id': 'd9h0im0u6scfdgk98o9kkf7o78', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=ZDloMGltMHU2c2NmZGdrOThvOWtrZjdvNzggY29kZS5jbGluaWMudGVzdEBt', 'created': '2020-11-11T08:38:42.000Z', 'updated': '2020-11-11T08:38:42.320Z', 'summary': 'VOLUNTEER: student', 'location': 'WeThinkCode, Victoria & Alfred Waterfront, Cape Town', 'creator': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'organizer': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'start': {'dateTime': '2020-11-13T10:00:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'end': {'dateTime': '2020-11-13T11:30:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'iCalUID': 'd9h0im0u6scfdgk98o9kkf7o78@google.com', 'sequence': 0, 'attendees': [{'email': 'student@student.wethinkcode.co.za', 'responseStatus': 'needsAction'}], 'reminders': {'useDefault': True}}]

    def test_Sort_open_slots(self):
        self.assertEqual(len((event_listing.sort_open_slots(test_joshua.test_obj))), 2)


#     def test_print_stops(self):
#         sys.stdout = StringIO()
#         self.maxDiff = None

#         event_listing.print_slots_table(test_joshua.test_obj)
#         self.assertEqual(sys.stdout.getvalue(),'''Displaying all open slots for the next 7 days.
# +------------------------------------------------------------------------------------------------------------------------------------------------+
# | #.                         | Volunteer name.            | date.                      | time.                      | Unique ID.                 |
# +----------------------------+----------------------------+----------------------------+----------------------------+----------------------------+
# |                            | -------------------------  | -------------------------  | -------------------------  | -------------------------  |
# | 1                          | VOLUNTEER: jroy            | 2020-11-12                 | 12:00 - 12:30              | lo7ami5f9pu7s4qdlun76h7m2k |
# |                            | -------------------------  | -------------------------  | -------------------------  | -------------------------  |
# | 2                          | VOLUNTEER: jroy            | 2020-11-12                 | 12:30 - 13:00              | rq731nlq01brfe4egl6b9ifu14 |
# |                            | -------------------------  | -------------------------  | -------------------------  | -------------------------  |
# | 3                          | VOLUNTEER: student         | 2020-11-13                 | 10:00 - 11:30              | d9h0im0u6scfdgk98o9kkf7o78 |
# +------------------------------------------------------------------------------------------------------------------------------------------------+
# ''')

    @patch("sys.stdin", StringIO("2\n1\n"))
    def test_get_user_input(self):

        response = booking.get_user_input()
        self.assertEqual(response, 2)

        response = booking.get_user_input()
        self.assertEqual(response, 1)

    def test_create_body(self):
        sys.stdout = StringIO()
        response, unique_id = booking.create_booking_body(test_joshua.test_obj[0], 'freal')
        new_body = {
            'summary': 'VOLUNTEER: jroy',
            'location': 'WeThinkCode, Victoria & Alfred Waterfront, Cape Town',
            'start': {'dateTime': '2020-11-12T12:00:00+02:00', 'timeZone': 'Africa/Johannesburg'},
            'end': {'dateTime': '2020-11-12T12:30:00+02:00', 'timeZone': 'Africa/Johannesburg'},
            'attendees': [{'email': 'jroy@student.wethinkcode.co.za', 'responseStatus': 'accepted'}, {'email': 'freal@student.wethinkcode.co.za'}],
            'reminders': {
                'useDefault': True,
            },
     }
        self.assertEqual(response, new_body)
        self.assertEqual(unique_id, 'lo7ami5f9pu7s4qdlun76h7m2k')

    

if __name__ == "__main__":
    unittest.main()