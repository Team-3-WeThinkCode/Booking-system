import os
import sys
import datetime
from utils.TableIt import TableIt as tabulate
USER_PATHS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../'))
sys.path.insert(0, USER_PATHS)
import utilities as utils


def is_volunteering_at_specified_time(clinic_service, username, start_datetime, end_datetime):
    '''
    Checks if volunteer is volunteering at specified date/time
    :return: True if the volunteer has a volunteer slot in 
    specified date/time
    '''

    events = utils.get_events(clinic_service, start_datetime, end_datetime)
    events = list(filter(lambda x: x['start'].get('dateTime') == start_datetime, events))
    events = list(filter(lambda y: y['end'].get('dateTime') == end_datetime, events))
    if events:
        if "VOLUNTEER: " + str(username) in events[0]['summary']:
            return True
    return False


def get_open_volunteer_slots_of_the_day(date, username, clinic_service):
    '''
    Checks events in clinic calendar for open slots to add volunteer events
    :return: list (of tuples) of open volunteer slots
    '''

    slots = [('08:30', '10:00'), ('10:00', '11:30'), ('11:30', '13:00'), ('13:00', '14:30'), ('14:30', '16:00'), ('16:00', '17:30')]
    open_slots = []
    for slot in slots:
        start_datetime, end_datetime = utils.convert_date_and_time_to_rfc_format(date, slot[0], slot[1])
        if not is_volunteering_at_specified_time(clinic_service, username, start_datetime, end_datetime):
            open_slots.append(slot)
    return open_slots


def convert_90_min_slot_into_30_min_slots(slot):
    '''
    Converts 90min slots into 30min slots
    :return: list (of tuples) of 30min slots
    '''

    start_hour, start_minute = int(slot[0][:2]), int(slot[0][3:])
    if start_minute == 30:
        return [(slot[0], str(start_hour+1)+':'+'00'), (str(start_hour+1)+':'+'00', str(start_hour+1)+':'+'30'), (str(start_hour+1)+':'+'30', str(start_hour+2)+':'+'00') ]
    elif start_minute == 0:
        return [(slot[0], str(start_hour)+':'+'30'), (str(start_hour)+':'+'30', str(start_hour+1)+':'+'00'), (str(start_hour+1)+':'+'00', str(start_hour+1)+':'+'30') ]
    return []


def print_open_slots_table(list_slots, date, title):
    """
    Prints table with information on the date, start time and end time of events
    """

    table = [
        ['#.', 'date.', 'start time.', 'end time.']
    ]
    nums = 1
    print('\n'+title)
    for slot in list_slots:
        table.append(['', '-------------------------', '-------------------------', '-------------------------', '-------------------------'])
        table.append([nums, date, slot[0], slot[1]])
        nums += 1
    tabulate.printTable(table, useFieldNames=True, color=(255, 0, 255))


def is_slot_available(service, username, start_datetime, end_datetime):
    '''
    Checks if user busy at specified date/time
    :return: True if slot is available (no events during date/time)
    '''
    
    user_email = str(username)+"@student.wethinkcode.co.za"
    body = {
      "timeMin": start_datetime,
      "timeMax": end_datetime,
      "items": [
        {"id": user_email}
      ],
      "timeZone": 'Africa/Johannesburg',
    }
    events = service.freebusy().query(body=body).execute()
    events = events.get('calendars').get(user_email)
    if events.get('busy'):
        return False
    return True


def create_volunteer_slot(username, date, time, volunteer_service, codeclinic_service):
    '''
    Creates volunteer slot if both the clinic and the student's calendar correlates
    to volunteer slot time.
    :return: True if volunteer slot created succesfully, with output to be printed
    '''

    open_slots = get_open_volunteer_slots_of_the_day(date, username, codeclinic_service)
    if not open_slots:
        return False, 'ERROR: There are no open slots on this day.'
    time_slot_lst = list(filter(lambda x : x[0] == time, open_slots))
    if not time_slot_lst:
        utils.print_output('ERROR: Choose a valid/open slot start time.')
        return False
    time_slot = time_slot_lst[0]
    start_datetime, end_datetime = utils.convert_date_and_time_to_rfc_format(date, time_slot[0], time_slot[1])
    if is_slot_available(volunteer_service, username, start_datetime, end_datetime):
        thirty_minute_slots = convert_90_min_slot_into_30_min_slots(time_slot)
        for slot in thirty_minute_slots:
            start_datetime, end_datetime = utils.convert_date_and_time_to_rfc_format(date, slot[0], slot[1])
            event_info = {'summary': 'VOLUNTEER: ' + str(username), 'start_datetime': start_datetime, 'end_datetime': end_datetime, 'attendees': []}
            response = utils.add_event_to_calendar(event_info, codeclinic_service, True, username)
            utils.volunteer_accept_invite(codeclinic_service, response['id'], username, response)
        utils.print_output('Volunteer slots created!')
        return True
    utils.print_output('ERROR: You do not have an open slot in your calendar at the selected time.')
    return False


def get_volunteered_slot(clinic_service, username, date, time):
    '''
    Retrieves slots that the user volunteered for
    :return: list of slots the user volunteered for
    '''

    slots = [('08:30', '10:00'), ('10:00', '11:30'), ('11:30', '13:00'), ('13:00', '14:30'), ('14:30', '16:00'), ('16:00', '17:30')]
    start_datetime, end_datetime = utils.convert_date_and_time_to_rfc_format(date, '08:30', '17:30')
    events = utils.get_events(clinic_service, start_datetime, end_datetime)
    for event in events:
        if event['summary'][11:] == username and len(event['attendees']) == 1:
            start = event['start'].get('dateTime', event['start'].get('date'))
            for slot in slots:
                if start[11:16] == time and time == slot[0]:
                    return slot


def get_event_id(start_datetime, end_datetime, username, clinic_service):
    '''
    Retrieves event id of event in specified date/time
    :return: event id
    '''

    events = utils.get_events(clinic_service, start_datetime, end_datetime)
    volunteered_event = list(filter(lambda x: x['summary'][11:] == username, events))
    if volunteered_event:
        return volunteered_event[0]['id']
    return ''


def delete_slots_on_calendars(list_services, start_datetime, end_datetime, username):
    '''
    Deletes events created in specified times from specified calendars
    '''

    for service in list_services:
        event_id = get_event_id(start_datetime, end_datetime, username, service)
        utils.delete_event(service, event_id)


def delete_volunteer_slot(username, date, time, volunteer_service, clinic_service):
    '''
    Cancels specified volunteer slots created by user
    :return: True if slots were cancelled succesfully, and output to be printed
    '''

    volunteer_slot = get_volunteered_slot(clinic_service, username, date, time)
    if not volunteer_slot:
        utils.print_output('ERROR: No volunteer slot available to delete at specified date/time.')
        return False
    thirty_minute_slots = convert_90_min_slot_into_30_min_slots((volunteer_slot[0], volunteer_slot[1]))
    for slot in thirty_minute_slots:
        start_datetime, end_datetime = utils.convert_date_and_time_to_rfc_format(date, slot[0], slot[1])
        delete_slots_on_calendars([volunteer_service, clinic_service], start_datetime, end_datetime, username)
    utils.print_output('Volunteered slots were succesfully deleted.')
    return True