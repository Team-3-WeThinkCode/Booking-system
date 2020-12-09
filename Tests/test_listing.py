import unittest
from unittest.main import main
from unittest.mock import patch
from io import StringIO
import sys
import os
USER_PATHS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../'))
sys.path.insert(0, USER_PATHS)
from commands import event_listing
from commands import booking
class test_events_listings(unittest.TestCase):

    test_obj = [{'kind': 'calendar#event', 'etag': '"3210204165178000"', 'id': 'lo7ami5f9pu7s4qdlun76h7m2k', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=bG83YW1pNWY5cHU3czRxZGx1bjc2aDdtMmsgY29kZS5jbGluaWMudGVzdEBt', 'created': '2020-11-11T13:41:22.000Z', 'updated': '2020-11-11T13:41:22.589Z', 'summary': 'VOLUNTEER: jroy', 'location': 'WeThinkCode, Victoria & Alfred Waterfront, Cape Town', 'creator': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'organizer': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'start': {'dateTime': '2020-11-12T12:00:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'end': {'dateTime': '2020-11-12T12:30:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'iCalUID': 'lo7ami5f9pu7s4qdlun76h7m2k@google.com', 'sequence': 0, 'attendees': [{'email': 'jroy@student.wethinkcode.co.za', 'responseStatus': 'accepted'}], 'reminders': {'useDefault': True}},
    {'kind': 'calendar#event', 'etag': '"3210204167150000"', 'id': 'rq731nlq01brfe4egl6b9ifu14', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=cnE3MzFubHEwMWJyZmU0ZWdsNmI5aWZ1MTQgY29kZS5jbGluaWMudGVzdEBt', 'created': '2020-11-11T13:41:22.000Z', 'updated': '2020-11-11T13:41:23.575Z', 'summary': 'VOLUNTEER: jroy', 'location': 'WeThinkCode, Victoria & Alfred Waterfront, Cape Town', 'creator': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'organizer': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'start': {'dateTime': '2020-11-12T12:30:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'end': {'dateTime': '2020-11-12T13:00:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'iCalUID': 'rq731nlq01brfe4egl6b9ifu14@google.com', 'sequence': 0, 'attendees': [{'email': 'jroy@student.wethinkcode.co.za', 'responseStatus': 'accepted'}, {'email': 'fake@student.wethinkcode.co.za', 'responseStatus': 'accepted'}], 'reminders': {'useDefault': True}},
    {'kind': 'calendar#event', 'etag': '"3210167844640000"', 'id': 'd9h0im0u6scfdgk98o9kkf7o78', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=ZDloMGltMHU2c2NmZGdrOThvOWtrZjdvNzggY29kZS5jbGluaWMudGVzdEBt', 'created': '2020-11-11T08:38:42.000Z', 'updated': '2020-11-11T08:38:42.320Z', 'summary': 'VOLUNTEER: student', 'location': 'WeThinkCode, Victoria & Alfred Waterfront, Cape Town', 'creator': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'organizer': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'start': {'dateTime': '2020-11-13T10:00:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'end': {'dateTime': '2020-11-13T11:30:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'iCalUID': 'd9h0im0u6scfdgk98o9kkf7o78@google.com', 'sequence': 0, 'attendees': [{'email': 'student@student.wethinkcode.co.za', 'responseStatus': 'needsAction'}], 'reminders': {'useDefault': True}}]

    def test_sort_open_slots(self):
        new_list = event_listing.sort_open_slots(test_events_listings.test_obj, username="student")
        self.assertEqual(new_list, [self.test_obj[0]])


    def test_sort_booked_slots_false(self):
        new_list = event_listing.sort_booked_slots(test_events_listings.test_obj, username="jdoe")
        self.assertEqual(new_list, [])


    def test_sort_booked_slots(self):
        new_list = event_listing.sort_booked_slots(test_events_listings.test_obj, username="jroy")
        self.assertEqual(new_list, [self.test_obj[0], self.test_obj[1]])


    def test_sort_open_slots_false(self):
        new_list = event_listing.sort_open_slots([{"key": "value"}], username="jroy")
        self.assertEqual(new_list, [])




if __name__ == "__main__":
    unittest.main()