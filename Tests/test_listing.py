import unittest
from unittest.main import main
from unittest.mock import patch
import sys
from io import StringIO
from rich.console import Console
import os
USER_PATHS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../'))
sys.path.insert(0, USER_PATHS)
from commands import event_listing

#run the tests with python3 -m unittest Tests/test_listing.py
class test_events_listings(unittest.TestCase):

    test_obj = [{'kind': 'calendar#event', 'etag': '"3210204165178000"', 'id': 'lo7ami5f9pu7s4qdlun76h7m2k', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=bG83YW1pNWY5cHU3czRxZGx1bjc2aDdtMmsgY29kZS5jbGluaWMudGVzdEBt', 'created': '2020-11-11T13:41:22.000Z', 'updated': '2020-11-11T13:41:22.589Z', 'summary': 'VOLUNTEER: jroy', 'location': 'WeThinkCode, Victoria & Alfred Waterfront, Cape Town', 'creator': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'organizer': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'start': {'dateTime': '2020-11-12T12:00:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'end': {'dateTime': '2020-11-12T12:30:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'iCalUID': 'lo7ami5f9pu7s4qdlun76h7m2k@google.com', 'sequence': 0, 'attendees': [{'email': 'jroy@student.wethinkcode.co.za', 'responseStatus': 'accepted'}], 'reminders': {'useDefault': True}},
    {'kind': 'calendar#event', 'etag': '"3210204167150000"', 'id': 'rq731nlq01brfe4egl6b9ifu14', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=cnE3MzFubHEwMWJyZmU0ZWdsNmI5aWZ1MTQgY29kZS5jbGluaWMudGVzdEBt', 'created': '2020-11-11T13:41:22.000Z', 'updated': '2020-11-11T13:41:23.575Z', 'summary': 'VOLUNTEER: jroy', 'location': 'WeThinkCode, Victoria & Alfred Waterfront, Cape Town', 'creator': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'organizer': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'start': {'dateTime': '2020-11-12T12:30:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'end': {'dateTime': '2020-11-12T13:00:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'iCalUID': 'rq731nlq01brfe4egl6b9ifu14@google.com', 'sequence': 0, 'attendees': [{'email': 'jroy@student.wethinkcode.co.za', 'responseStatus': 'accepted'}, {'email': 'fake@student.wethinkcode.co.za', 'responseStatus': 'accepted'}], 'reminders': {'useDefault': True}},
    {'kind': 'calendar#event', 'etag': '"3210167844640000"', 'id': 'd9h0im0u6scfdgk98o9kkf7o78', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=ZDloMGltMHU2c2NmZGdrOThvOWtrZjdvNzggY29kZS5jbGluaWMudGVzdEBt', 'created': '2020-11-11T08:38:42.000Z', 'updated': '2020-11-11T08:38:42.320Z', 'summary': 'VOLUNTEER: student', 'location': 'WeThinkCode, Victoria & Alfred Waterfront, Cape Town', 'creator': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'organizer': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'start': {'dateTime': '2020-11-13T10:00:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'end': {'dateTime': '2020-11-13T11:30:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'iCalUID': 'd9h0im0u6scfdgk98o9kkf7o78@google.com', 'sequence': 0, 'attendees': [{'email': 'student@student.wethinkcode.co.za', 'responseStatus': 'needsAction'}], 'reminders': {'useDefault': True}}]


    def test_get_volunteer_slots_table(self):
        events = [{'kind': 'calendar#event', 'etag': '"3215031116322000"', 'id': 'bi9heprfrg5r2smri2mju16p38', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=Ymk5aGVwcmZyZzVyMnNtcmkybWp1MTZwMzggY29kZS5jbGluaWMudGVzdEBt', 'created': '2020-12-09T12:03:34.000Z', 'updated': '2020-12-09T12:05:58.161Z', 'summary': 'VOLUNTEER: rowen', 'description': 'toets', 'location': 'WeThinkCode, Victoria & Alfred Waterfront, Cape Town', 'creator': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'organizer': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'start': {'dateTime': '2020-12-11T13:00:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'end': {'dateTime': '2020-12-11T13:30:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'iCalUID': 'bi9heprfrg5r2smri2mju16p38@google.com', 'sequence': 0, 'attendees': [{'email': 'rowen@student.wethinkcode.co.za', 'responseStatus': 'accepted'}, {'email': 'rhys@student.wethinkcode.co.za', 'responseStatus': 'accepted'}], 'reminders': {'useDefault': True}}, {'kind': 'calendar#event', 'etag': '"3215212137926000"', 'id': 'e6mvh4crkd77qskg5ebhponfc8', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=ZTZtdmg0Y3JrZDc3cXNrZzVlYmhwb25mYzggY29kZS5jbGluaWMudGVzdEBt', 'created': '2020-12-09T12:03:35.000Z', 'updated': '2020-12-10T13:14:28.963Z', 'summary': 'VOLUNTEER: rowen', 'description': 'tester', 'location': 'WeThinkCode, Victoria & Alfred Waterfront, Cape Town', 'creator': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'organizer': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'start': {'dateTime': '2020-12-11T13:30:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'end': {'dateTime': '2020-12-11T14:00:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'iCalUID': 'e6mvh4crkd77qskg5ebhponfc8@google.com', 'sequence': 0, 'attendees': [{'email': 'rowen@student.wethinkcode.co.za', 'responseStatus': 'accepted'}, {'email': 'rhys@student.wethinkcode.co.za', 'responseStatus': 'accepted'}], 'reminders': {'useDefault': True}}, {'kind': 'calendar#event', 'etag': '"3215032997216000"', 'id': '1bneuds2su1fof321apct652d8', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=MWJuZXVkczJzdTFmb2YzMjFhcGN0NjUyZDggY29kZS5jbGluaWMudGVzdEBt', 'created': '2020-12-09T12:03:36.000Z', 'updated': '2020-12-09T12:21:38.608Z', 'summary': 'VOLUNTEER: rowen', 'description': 'toets', 'location': 'WeThinkCode, Victoria & Alfred Waterfront, Cape Town', 'creator': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'organizer': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'start': {'dateTime': '2020-12-11T14:00:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'end': {'dateTime': '2020-12-11T14:30:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'iCalUID': '1bneuds2su1fof321apct652d8@google.com', 'sequence': 0, 'attendees': [{'email': 'rowen@student.wethinkcode.co.za', 'responseStatus': 'accepted'}, {'email': 'rhys@student.wethinkcode.co.za', 'responseStatus': 'accepted'}], 'reminders': {'useDefault': True}}, {'kind': 'calendar#event', 'etag': '"3215345493074000"', 'id': '0k2uqku5kgm6f5tb0sstjeans4', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=MGsydXFrdTVrZ202ZjV0YjBzc3RqZWFuczQgY29kZS5jbGluaWMudGVzdEBt', 'created': '2020-12-11T06:58:53.000Z', 'updated': '2020-12-11T07:45:46.537Z', 'summary': 'VOLUNTEER: jroy', 'description': 'Recursion', 'location': 'WeThinkCode, Victoria & Alfred Waterfront, Cape Town', 'creator': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'organizer': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'start': {'dateTime': '2020-12-11T16:00:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'end': {'dateTime': '2020-12-11T16:30:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'iCalUID': '0k2uqku5kgm6f5tb0sstjeans4@google.com', 'sequence': 0, 'attendees': [{'email': 'jroy@student.wethinkcode.co.za', 'responseStatus': 'accepted'}, {'email': 'student@student.wethinkcode.co.za', 'responseStatus': 'accepted'}], 'reminders': {'useDefault': True}}, {'kind': 'calendar#event', 'etag': '"3215339868890000"', 'id': 'vutekihkou4smer4clcqo2acrc', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=dnV0ZWtpaGtvdTRzbWVyNGNsY3FvMmFjcmMgY29kZS5jbGluaWMudGVzdEBt', 'created': '2020-12-11T06:58:53.000Z', 'updated': '2020-12-11T06:58:54.445Z', 'summary': 'VOLUNTEER: jroy', 'location': 'WeThinkCode, Victoria & Alfred Waterfront, Cape Town', 'creator': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'organizer': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'start': {'dateTime': '2020-12-11T16:30:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'end': {'dateTime': '2020-12-11T17:00:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'iCalUID': 'vutekihkou4smer4clcqo2acrc@google.com', 'sequence': 0, 'attendees': [{'email': 'jroy@student.wethinkcode.co.za', 'responseStatus': 'accepted'}], 'reminders': {'useDefault': True}}, {'kind': 'calendar#event', 'etag': '"3215339870562000"', 'id': 'njoqgfop1h4e88usmoki249fis', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=bmpvcWdmb3AxaDRlODh1c21va2kyNDlmaXMgY29kZS5jbGluaWMudGVzdEBt', 'created': '2020-12-11T06:58:54.000Z', 'updated': '2020-12-11T06:58:55.281Z', 'summary': 'VOLUNTEER: jroy', 'location': 'WeThinkCode, Victoria & Alfred Waterfront, Cape Town', 'creator': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'organizer': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'start': {'dateTime': '2020-12-11T17:00:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'end': {'dateTime': '2020-12-11T17:30:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'iCalUID': 'njoqgfop1h4e88usmoki249fis@google.com', 'sequence': 0, 'attendees': [{'email': 'jroy@student.wethinkcode.co.za', 'responseStatus': 'accepted'}], 'reminders': {'useDefault': True}}]
        username = "rowen"
        result = event_listing.get_volunteered_slots_table_info(events, username)
        self.assertEqual(result, [('rowen', '2020-12-11', '13:00', 'bi9heprfrg5r2smri2mju16p38', 'rhys')], "There is an issue with the get_volunteer_slots_table function.")
        
    def test_get_booked_slots_table(self):
        events = [{'kind': 'calendar#event', 'etag': '"3215031116322000"', 'id': 'bi9heprfrg5r2smri2mju16p38', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=Ymk5aGVwcmZyZzVyMnNtcmkybWp1MTZwMzggY29kZS5jbGluaWMudGVzdEBt', 'created': '2020-12-09T12:03:34.000Z', 'updated': '2020-12-09T12:05:58.161Z', 'summary': 'VOLUNTEER: rowen', 'description': 'toets', 'location': 'WeThinkCode, Victoria & Alfred Waterfront, Cape Town', 'creator': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'organizer': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'start': {'dateTime': '2020-12-11T13:00:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'end': {'dateTime': '2020-12-11T13:30:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'iCalUID': 'bi9heprfrg5r2smri2mju16p38@google.com', 'sequence': 0, 'attendees': [{'email': 'rowen@student.wethinkcode.co.za', 'responseStatus': 'accepted'}, {'email': 'rhys@student.wethinkcode.co.za', 'responseStatus': 'accepted'}], 'reminders': {'useDefault': True}}, {'kind': 'calendar#event', 'etag': '"3215212137926000"', 'id': 'e6mvh4crkd77qskg5ebhponfc8', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=ZTZtdmg0Y3JrZDc3cXNrZzVlYmhwb25mYzggY29kZS5jbGluaWMudGVzdEBt', 'created': '2020-12-09T12:03:35.000Z', 'updated': '2020-12-10T13:14:28.963Z', 'summary': 'VOLUNTEER: rowen', 'description': 'tester', 'location': 'WeThinkCode, Victoria & Alfred Waterfront, Cape Town', 'creator': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'organizer': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'start': {'dateTime': '2020-12-11T13:30:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'end': {'dateTime': '2020-12-11T14:00:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'iCalUID': 'e6mvh4crkd77qskg5ebhponfc8@google.com', 'sequence': 0, 'attendees': [{'email': 'rowen@student.wethinkcode.co.za', 'responseStatus': 'accepted'}, {'email': 'rhys@student.wethinkcode.co.za', 'responseStatus': 'accepted'}], 'reminders': {'useDefault': True}}, {'kind': 'calendar#event', 'etag': '"3215032997216000"', 'id': '1bneuds2su1fof321apct652d8', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=MWJuZXVkczJzdTFmb2YzMjFhcGN0NjUyZDggY29kZS5jbGluaWMudGVzdEBt', 'created': '2020-12-09T12:03:36.000Z', 'updated': '2020-12-09T12:21:38.608Z', 'summary': 'VOLUNTEER: rowen', 'description': 'toets', 'location': 'WeThinkCode, Victoria & Alfred Waterfront, Cape Town', 'creator': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'organizer': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'start': {'dateTime': '2020-12-11T14:00:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'end': {'dateTime': '2020-12-11T14:30:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'iCalUID': '1bneuds2su1fof321apct652d8@google.com', 'sequence': 0, 'attendees': [{'email': 'rowen@student.wethinkcode.co.za', 'responseStatus': 'accepted'}, {'email': 'rhys@student.wethinkcode.co.za', 'responseStatus': 'accepted'}], 'reminders': {'useDefault': True}}, {'kind': 'calendar#event', 'etag': '"3215349480366000"', 'id': '0k2uqku5kgm6f5tb0sstjeans4', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=MGsydXFrdTVrZ202ZjV0YjBzc3RqZWFuczQgY29kZS5jbGluaWMudGVzdEBt', 'created': '2020-12-11T06:58:53.000Z', 'updated': '2020-12-11T08:19:00.183Z', 'summary': 'VOLUNTEER: jroy', 'description': 'Recursion', 'location': 'WeThinkCode, Victoria & Alfred Waterfront, Cape Town', 'creator': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'organizer': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'start': {'dateTime': '2020-12-11T16:00:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'end': {'dateTime': '2020-12-11T16:30:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'iCalUID': '0k2uqku5kgm6f5tb0sstjeans4@google.com', 'sequence': 0, 'attendees': [{'email': 'jroy@student.wethinkcode.co.za', 'responseStatus': 'accepted'}, {'email': 'student@student.wethinkcode.co.za', 'responseStatus': 'accepted'}], 'reminders': {'useDefault': True}}, {'kind': 'calendar#event', 'etag': '"3215349820158000"', 'id': 'vutekihkou4smer4clcqo2acrc', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=dnV0ZWtpaGtvdTRzbWVyNGNsY3FvMmFjcmMgY29kZS5jbGluaWMudGVzdEBt', 'created': '2020-12-11T06:58:53.000Z', 'updated': '2020-12-11T08:21:50.079Z', 'summary': 'VOLUNTEER: jroy', 'description': 'Recursion', 'location': 'WeThinkCode, Victoria & Alfred Waterfront, Cape Town', 'creator': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'organizer': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'start': {'dateTime': '2020-12-11T16:30:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'end': {'dateTime': '2020-12-11T17:00:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'iCalUID': 'vutekihkou4smer4clcqo2acrc@google.com', 'sequence': 0, 'attendees': [{'email': 'jroy@student.wethinkcode.co.za', 'responseStatus': 'accepted'}, {'email': 'bnkala@student.wethinkcode.co.za', 'responseStatus': 'accepted'}], 'reminders': {'useDefault': True}}, {'kind': 'calendar#event', 'etag': '"3215339870562000"', 'id': 'njoqgfop1h4e88usmoki249fis', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=bmpvcWdmb3AxaDRlODh1c21va2kyNDlmaXMgY29kZS5jbGluaWMudGVzdEBt', 'created': '2020-12-11T06:58:54.000Z', 'updated': '2020-12-11T06:58:55.281Z', 'summary': 'VOLUNTEER: jroy', 'location': 'WeThinkCode, Victoria & Alfred Waterfront, Cape Town', 'creator': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'organizer': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'start': {'dateTime': '2020-12-11T17:00:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'end': {'dateTime': '2020-12-11T17:30:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'iCalUID': 'njoqgfop1h4e88usmoki249fis@google.com', 'sequence': 0, 'attendees': [{'email': 'jroy@student.wethinkcode.co.za', 'responseStatus': 'accepted'}], 'reminders': {'useDefault': True}}]
        username = "rowen"
        result = event_listing.get_booked_slots_table_info(events, username)
        self.assertEqual(result, [])

    def test_get_booked_slots_table2(self):
        events = [{'kind': 'calendar#event', 'etag': '"3215031116322000"', 'id': 'bi9heprfrg5r2smri2mju16p38', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=Ymk5aGVwcmZyZzVyMnNtcmkybWp1MTZwMzggY29kZS5jbGluaWMudGVzdEBt', 'created': '2020-12-09T12:03:34.000Z', 'updated': '2020-12-09T12:05:58.161Z', 'summary': 'VOLUNTEER: rowen', 'description': 'toets', 'location': 'WeThinkCode, Victoria & Alfred Waterfront, Cape Town', 'creator': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'organizer': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'start': {'dateTime': '2020-12-11T13:00:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'end': {'dateTime': '2020-12-11T13:30:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'iCalUID': 'bi9heprfrg5r2smri2mju16p38@google.com', 'sequence': 0, 'attendees': [{'email': 'rowen@student.wethinkcode.co.za', 'responseStatus': 'accepted'}, {'email': 'rhys@student.wethinkcode.co.za', 'responseStatus': 'accepted'}], 'reminders': {'useDefault': True}}, {'kind': 'calendar#event', 'etag': '"3215212137926000"', 'id': 'e6mvh4crkd77qskg5ebhponfc8', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=ZTZtdmg0Y3JrZDc3cXNrZzVlYmhwb25mYzggY29kZS5jbGluaWMudGVzdEBt', 'created': '2020-12-09T12:03:35.000Z', 'updated': '2020-12-10T13:14:28.963Z', 'summary': 'VOLUNTEER: rowen', 'description': 'tester', 'location': 'WeThinkCode, Victoria & Alfred Waterfront, Cape Town', 'creator': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'organizer': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'start': {'dateTime': '2020-12-11T13:30:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'end': {'dateTime': '2020-12-11T14:00:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'iCalUID': 'e6mvh4crkd77qskg5ebhponfc8@google.com', 'sequence': 0, 'attendees': [{'email': 'rowen@student.wethinkcode.co.za', 'responseStatus': 'accepted'}, {'email': 'rhys@student.wethinkcode.co.za', 'responseStatus': 'accepted'}], 'reminders': {'useDefault': True}}, {'kind': 'calendar#event', 'etag': '"3215032997216000"', 'id': '1bneuds2su1fof321apct652d8', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=MWJuZXVkczJzdTFmb2YzMjFhcGN0NjUyZDggY29kZS5jbGluaWMudGVzdEBt', 'created': '2020-12-09T12:03:36.000Z', 'updated': '2020-12-09T12:21:38.608Z', 'summary': 'VOLUNTEER: rowen', 'description': 'toets', 'location': 'WeThinkCode, Victoria & Alfred Waterfront, Cape Town', 'creator': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'organizer': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'start': {'dateTime': '2020-12-11T14:00:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'end': {'dateTime': '2020-12-11T14:30:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'iCalUID': '1bneuds2su1fof321apct652d8@google.com', 'sequence': 0, 'attendees': [{'email': 'rowen@student.wethinkcode.co.za', 'responseStatus': 'accepted'}, {'email': 'rhys@student.wethinkcode.co.za', 'responseStatus': 'accepted'}], 'reminders': {'useDefault': True}}, {'kind': 'calendar#event', 'etag': '"3215350229980000"', 'id': '0k2uqku5kgm6f5tb0sstjeans4', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=MGsydXFrdTVrZ202ZjV0YjBzc3RqZWFuczQgY29kZS5jbGluaWMudGVzdEBt', 'created': '2020-12-11T06:58:53.000Z', 'updated': '2020-12-11T08:25:14.990Z', 'summary': 'VOLUNTEER: jroy', 'description': 'Recursion and other goodies', 'location': 'WeThinkCode, Victoria & Alfred Waterfront, Cape Town', 'creator': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'organizer': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'start': {'dateTime': '2020-12-11T16:00:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'end': {'dateTime': '2020-12-11T16:30:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'iCalUID': '0k2uqku5kgm6f5tb0sstjeans4@google.com', 'sequence': 0, 'attendees': [{'email': 'jroy@student.wethinkcode.co.za', 'responseStatus': 'accepted'}, {'email': 'student@student.wethinkcode.co.za', 'responseStatus': 'accepted'}], 'reminders': {'useDefault': True}}, {'kind': 'calendar#event', 'etag': '"3215349820158000"', 'id': 'vutekihkou4smer4clcqo2acrc', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=dnV0ZWtpaGtvdTRzbWVyNGNsY3FvMmFjcmMgY29kZS5jbGluaWMudGVzdEBt', 'created': '2020-12-11T06:58:53.000Z', 'updated': '2020-12-11T08:21:50.079Z', 'summary': 'VOLUNTEER: jroy', 'description': 'Recursion', 'location': 'WeThinkCode, Victoria & Alfred Waterfront, Cape Town', 'creator': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'organizer': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'start': {'dateTime': '2020-12-11T16:30:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'end': {'dateTime': '2020-12-11T17:00:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'iCalUID': 'vutekihkou4smer4clcqo2acrc@google.com', 'sequence': 0, 'attendees': [{'email': 'jroy@student.wethinkcode.co.za', 'responseStatus': 'accepted'}, {'email': 'bnkala@student.wethinkcode.co.za', 'responseStatus': 'accepted'}], 'reminders': {'useDefault': True}}, {'kind': 'calendar#event', 'etag': '"3215350330738000"', 'id': 'njoqgfop1h4e88usmoki249fis', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=bmpvcWdmb3AxaDRlODh1c21va2kyNDlmaXMgY29kZS5jbGluaWMudGVzdEBt', 'created': '2020-12-11T06:58:54.000Z', 'updated': '2020-12-11T08:26:05.369Z', 'summary': 'VOLUNTEER: jroy', 'description': 'Test', 'location': 'WeThinkCode, Victoria & Alfred Waterfront, Cape Town', 'creator': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'organizer': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'start': {'dateTime': '2020-12-11T17:00:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'end': {'dateTime': '2020-12-11T17:30:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'iCalUID': 'njoqgfop1h4e88usmoki249fis@google.com', 'sequence': 0, 'attendees': [{'email': 'jroy@student.wethinkcode.co.za', 'responseStatus': 'accepted'}, {'email': 'rowen@student.wethinkcode.co.za', 'responseStatus': 'accepted'}], 'reminders': {'useDefault': True}}]
        username = "rowen"
        result = event_listing.get_booked_slots_table_info(events, username)
        self.assertEqual(result, [(' jroy', '2020-12-11', '17:00 - 17:30', 'njoqgfop1h4e88usmoki249fis', 'rowen')], "There is an issue with the get_volunteer_slots_table function.")   


    def test_get_all_booked_slots_table_info(self):
        events = [{'kind': 'calendar#event', 'etag': '"3215031116322000"', 'id': 'bi9heprfrg5r2smri2mju16p38', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=Ymk5aGVwcmZyZzVyMnNtcmkybWp1MTZwMzggY29kZS5jbGluaWMudGVzdEBt', 'created': '2020-12-09T12:03:34.000Z', 'updated': '2020-12-09T12:05:58.161Z', 'summary': 'VOLUNTEER: rowen', 'description': 'toets', 'location': 'WeThinkCode, Victoria & Alfred Waterfront, Cape Town', 'creator': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'organizer': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'start': {'dateTime': '2020-12-11T13:00:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'end': {'dateTime': '2020-12-11T13:30:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'iCalUID': 'bi9heprfrg5r2smri2mju16p38@google.com', 'sequence': 0, 'attendees': [{'email': 'rowen@student.wethinkcode.co.za', 'responseStatus': 'accepted'}, {'email': 'rhys@student.wethinkcode.co.za', 'responseStatus': 'accepted'}], 'reminders': {'useDefault': True}}, {'kind': 'calendar#event', 'etag': '"3215212137926000"', 'id': 'e6mvh4crkd77qskg5ebhponfc8', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=ZTZtdmg0Y3JrZDc3cXNrZzVlYmhwb25mYzggY29kZS5jbGluaWMudGVzdEBt', 'created': '2020-12-09T12:03:35.000Z', 'updated': '2020-12-10T13:14:28.963Z', 'summary': 'VOLUNTEER: rowen', 'description': 'tester', 'location': 'WeThinkCode, Victoria & Alfred Waterfront, Cape Town', 'creator': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'organizer': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'start': {'dateTime': '2020-12-11T13:30:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'end': {'dateTime': '2020-12-11T14:00:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'iCalUID': 'e6mvh4crkd77qskg5ebhponfc8@google.com', 'sequence': 0, 'attendees': [{'email': 'rowen@student.wethinkcode.co.za', 'responseStatus': 'accepted'}, {'email': 'rhys@student.wethinkcode.co.za', 'responseStatus': 'accepted'}], 'reminders': {'useDefault': True}}, {'kind': 'calendar#event', 'etag': '"3215032997216000"', 'id': '1bneuds2su1fof321apct652d8', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=MWJuZXVkczJzdTFmb2YzMjFhcGN0NjUyZDggY29kZS5jbGluaWMudGVzdEBt', 'created': '2020-12-09T12:03:36.000Z', 'updated': '2020-12-09T12:21:38.608Z', 'summary': 'VOLUNTEER: rowen', 'description': 'toets', 'location': 'WeThinkCode, Victoria & Alfred Waterfront, Cape Town', 'creator': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'organizer': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'start': {'dateTime': '2020-12-11T14:00:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'end': {'dateTime': '2020-12-11T14:30:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'iCalUID': '1bneuds2su1fof321apct652d8@google.com', 'sequence': 0, 'attendees': [{'email': 'rowen@student.wethinkcode.co.za', 'responseStatus': 'accepted'}, {'email': 'rhys@student.wethinkcode.co.za', 'responseStatus': 'accepted'}], 'reminders': {'useDefault': True}}, {'kind': 'calendar#event', 'etag': '"3215351422714000"', 'id': '0k2uqku5kgm6f5tb0sstjeans4', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=MGsydXFrdTVrZ202ZjV0YjBzc3RqZWFuczQgY29kZS5jbGluaWMudGVzdEBt', 'created': '2020-12-11T06:58:53.000Z', 'updated': '2020-12-11T08:35:11.357Z', 'summary': 'VOLUNTEER: jroy', 'description': 'bug fixer', 'location': 'WeThinkCode, Victoria & Alfred Waterfront, Cape Town', 'creator': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'organizer': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'start': {'dateTime': '2020-12-11T16:00:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'end': {'dateTime': '2020-12-11T16:30:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'iCalUID': '0k2uqku5kgm6f5tb0sstjeans4@google.com', 'sequence': 0, 'attendees': [{'email': 'jroy@student.wethinkcode.co.za', 'responseStatus': 'accepted'}, {'email': 'cprinsloo@student.wethinkcode.co.za', 'responseStatus': 'accepted'}], 'reminders': {'useDefault': True}}, {'kind': 'calendar#event', 'etag': '"3215350654218000"', 'id': 'vutekihkou4smer4clcqo2acrc', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=dnV0ZWtpaGtvdTRzbWVyNGNsY3FvMmFjcmMgY29kZS5jbGluaWMudGVzdEBt', 'created': '2020-12-11T06:58:53.000Z', 'updated': '2020-12-11T08:28:47.109Z', 'summary': 'VOLUNTEER: jroy', 'location': 'WeThinkCode, Victoria & Alfred Waterfront, Cape Town', 'creator': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'organizer': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'start': {'dateTime': '2020-12-11T16:30:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'end': {'dateTime': '2020-12-11T17:00:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'iCalUID': 'vutekihkou4smer4clcqo2acrc@google.com', 'sequence': 0, 'attendees': [{'email': 'jroy@student.wethinkcode.co.za', 'responseStatus': 'accepted'}], 'reminders': {'useDefault': True}}, {'kind': 'calendar#event', 'etag': '"3215350330738000"', 'id': 'njoqgfop1h4e88usmoki249fis', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=bmpvcWdmb3AxaDRlODh1c21va2kyNDlmaXMgY29kZS5jbGluaWMudGVzdEBt', 'created': '2020-12-11T06:58:54.000Z', 'updated': '2020-12-11T08:26:05.369Z', 'summary': 'VOLUNTEER: jroy', 'description': 'Test', 'location': 'WeThinkCode, Victoria & Alfred Waterfront, Cape Town', 'creator': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'organizer': {'email': 'code.clinic.test@gmail.com', 'self': True}, 'start': {'dateTime': '2020-12-11T17:00:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'end': {'dateTime': '2020-12-11T17:30:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'iCalUID': 'njoqgfop1h4e88usmoki249fis@google.com', 'sequence': 0, 'attendees': [{'email': 'jroy@student.wethinkcode.co.za', 'responseStatus': 'accepted'}, {'email': 'rowen@student.wethinkcode.co.za', 'responseStatus': 'accepted'}], 'reminders': {'useDefault': True}}]
        username = 'rowen'
        result = event_listing.get_all_booked_slots_table_info(events, username)
        self.assertEqual(result, [(' rowen', '2020-12-11', '13:00 - 13:30', 'bi9heprfrg5r2smri2mju16p38', 'rhys'), (' rowen', '2020-12-11', '13:30 - 14:00', 'e6mvh4crkd77qskg5ebhponfc8', 'rhys'), (' rowen', '2020-12-11', '14:00 - 14:30', '1bneuds2su1fof321apct652d8', 'rhys'), (' jroy', '2020-12-11', '17:00 - 17:30', 'njoqgfop1h4e88usmoki249fis', 'rowen')])


    def test_step1_then_off(self):
        console = Console(file=StringIO())
        console.print(event_listing.print_table([(' jroy', '2020-12-11', '16:30 - 17:00', 'vutekihkou4smer4clcqo2acrc', 'Open slot.')], 'Volunteer slots for the next 7 days available for booking:'))
        str_output = console.file.getvalue()

        self.assertEqual(str_output, '''                         Volunteer slots for the next 7 days available for booking:                         
┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ #.           ┃ Volunteer username ┃ Date       ┃ Time          ┃ ID                         ┃ Patient    ┃
┡━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━┩
│ 1            │  jroy              │ 2020-12-11 │ 16:30 - 17:00 │ vutekihkou4smer4clcqo2acrc │ Open slot. │
└──────────────┴────────────────────┴────────────┴───────────────┴────────────────────────────┴────────────┘
''')
    



if __name__ == "__main__":
    unittest.main()