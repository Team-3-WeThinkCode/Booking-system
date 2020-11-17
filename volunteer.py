import utilities as utils
import datetime
from utils.TableIt import TableIt as tabulate


def get_open_volunteer_slots_of_the_day(date, clinic_service):
    '''
    Checks events in clinic calendar for open slots to add volunteer events
    :return: list (of tuples) of open volunteer slots
    '''

    slots = [('08:30', '10:00'), ('10:00', '11:30'), ('11:30', '13:00'), ('13:00', '14:30'), ('14:30', '16:00'), ('16:00', '17:30')]
    open_slots = []
    for slot in slots:
        start_datetime, end_datetime = utils.convert_date_and_time_to_rfc_format(date, slot[0], slot[1])
        if utils.slot_is_available(clinic_service, start_datetime, end_datetime):
            open_slots.append(slot)
    return open_slots


def convert_to_digital_time_format(hour, minute):
    '''
    Converts hour/minute to digital time format
    :return: digital time
    '''

    str_hour = str(hour)
    str_minute = str(minute)
    if len(str_hour) > 2 or len(str_minute) > 2:
        return '', ''
    if len(str_hour) == 1:
        str_hour = '0' + str_hour
    if len(str_minute) == 1:
        str_minute = '0' + str_minute
    return str_hour+':'+str_minute


def convert_slot_into_30_min_slots(slot):
    '''
    Converts 90min slots into 30min slots
    :return: list (of tuples) of 30min slots
    '''

    start_hour, start_minute = int(slot[0][:2]), int(slot[0][3:])
    times = []
    while True:
        digital_time = convert_to_digital_time_format(start_hour, start_minute)
        times.append(digital_time)
        if len(times) == 4:
            return [(times[0], times[1]), (times[1], times[2]), (times[2], times[3])]
        if start_minute == 0:
            start_minute = 30
        else:
            start_minute = 0
            start_hour += 1


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


def get_volunteer_time(open_slots, time):
    '''
    Prints events in table from which user needs to choose event from.
    :return: event chosen by user
    '''

    for slot in open_slots:
        if slot[0] == time:
            return slot[0], slot[1]
    return '', ''
    

def create_volunteer_slot(username, date, time, volunteer_service, codeclinic_service):
    '''
    Creates volunteer slot if both the clinic and the student's calendar correlates
    to volunteer slot time.
    :return: True if volunteer slot created succesfully, with output to be printed
    '''

    open_slots = get_open_volunteer_slots_of_the_day(date, codeclinic_service)
    if len(open_slots) == 0:
        return False, 'There are no open slots on this day.'
    start_time, end_time = get_volunteer_time(open_slots, time)
    if start_time == '' or end_time == '':
        return False, 'Choose a valid/open slot start time.'
    start_datetime, end_datetime = utils.convert_date_and_time_to_rfc_format(date, start_time, end_time)
    if utils.slot_is_available(volunteer_service, start_datetime, end_datetime):
        thirty_minute_slots = convert_slot_into_30_min_slots((start_time, end_time))
        for slot in thirty_minute_slots:
            start_datetime, end_datetime = utils.convert_date_and_time_to_rfc_format(date, slot[0], slot[1])
            event_info_clinic = {'summary': 'VOLUNTEER: ' + str(username), 'start_datetime': start_datetime, 'end_datetime': end_datetime, 'attendees': []}
            response = utils.add_event_to_calendar(event_info_clinic, codeclinic_service, True, username)
            utils.volunteer_accept_invite(codeclinic_service, response['id'], username, response)
        return True, 'Volunteer slots created!'
    return False, 'You do not have an open slot in your calendar at the selected time.'


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
    return ''


def get_event_id(start_datetime, end_datetime, username, clinic_service):
    '''
    Retrieves event id of event in specified date/time
    :return: event id
    '''

    events = utils.get_events(clinic_service, start_datetime, end_datetime)
    for event in events:
        summary = event['summary']
        if summary[11:] == username:
            return event['id']
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
    if volunteer_slot == '':
        return False, 'No volunteer slot available to delete at specified date/time.'
    thirty_minute_slots = convert_slot_into_30_min_slots((volunteer_slot[0], volunteer_slot[1]))
    for slot in thirty_minute_slots:
        start_datetime, end_datetime = utils.convert_date_and_time_to_rfc_format(date, slot[0], slot[1])
        delete_slots_on_calendars([volunteer_service, clinic_service], start_datetime, end_datetime, username)
    return True, 'Volunteered slots were succesfully deleted.'