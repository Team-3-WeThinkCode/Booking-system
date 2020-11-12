import utilities as utils
import datetime
from utils.TableIt import TableIt as tabulate


def get_open_volunteer_slots_of_the_day(date, clinic_service):
    slots = [('08:30', '10:00'), ('10:00', '11:30'), ('11:30', '13:00'), ('13:00', '14:30'), ('14:30', '16:00'), ('16:00', '17:30')]
    open_slots = []
    for slot in slots:
        start_datetime, end_datetime = utils.convert_date_and_time_to_rfc_format(date, slot[0], slot[1])
        if utils.slot_is_available(clinic_service, start_datetime, end_datetime):
            open_slots.append(slot)
    return open_slots


def convert_to_digital_time_format(hour, minute):
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
    Uses the TableIt module to display data of open slots to the user in tabular form.
    Event name, time, date, id will be sliced from the events objects given and used to display in the table.
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


def get_volunteer_time(open_slots, date):
    print_open_slots_table(open_slots, date, 'Displaying all open slots for the selected date:')
    chosen_slot = int(input('Choose a slot: '))
    while chosen_slot > len(open_slots):
        chosen_slot = int(input('Please choose valid slot: '))
    return open_slots[chosen_slot-1]


def create_volunteer_slot(username, volunteer_service, codeclinic_service):
    '''
    :return: True if volunteer slot created succesfully
    '''

    date = utils.get_date()
    open_slots = get_open_volunteer_slots_of_the_day(date, codeclinic_service)
    if len(open_slots) == 0:
        return False, 'There are no open slots on this day.'
    time = get_volunteer_time(open_slots, date)
    start_datetime, end_datetime = utils.convert_date_and_time_to_rfc_format(date, time[0], time[1])
    if utils.slot_is_available(volunteer_service, start_datetime, end_datetime):
        thirty_minute_slots = convert_slot_into_30_min_slots(time)
        for slot in thirty_minute_slots:
            start_datetime, end_datetime = utils.convert_date_and_time_to_rfc_format(date, slot[0], slot[1])
            event_info_clinic = {'summary': 'VOLUNTEER: ' + str(username), 'start_datetime': start_datetime, 'end_datetime': end_datetime, 'attendees': []}
            response = utils.add_event_to_calendar(event_info_clinic, codeclinic_service, True, username)
            utils.volunteer_accept_invite(codeclinic_service, response['id'], username, response)
        return True, 'Volunteer slots created!'
    return False, 'You do not have an open slot at the selected time.'


def get_volunteered_slots(clinic_service, username, date):
    slots = [('08:30', '10:00'), ('10:00', '11:30'), ('11:30', '13:00'), ('13:00', '14:30'), ('14:30', '16:00'), ('16:00', '17:30')]
    volunteered_slots = []
    start_datetime, end_datetime = utils.convert_date_and_time_to_rfc_format(date, '08:30', '17:30')
    events_result = clinic_service.events().list(calendarId='primary', timeMin=start_datetime, timeMax=end_datetime, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    for event in events:
        if event['summary'][11:] == username:
            start = event['start'].get('dateTime', event['start'].get('date'))
            for slot in slots:
                if start[11:16] == slot[0]:
                    volunteered_slots.append((slot[0], slot[1]))
    return volunteered_slots


def get_event_id(start_datetime, username, clinic_service):
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    events_result = clinic_service.events().list(calendarId='primary', timeMin=now, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    for event in events:
        summary = event['summary']
        if summary[11:] == username and event['start']['dateTime'] == start_datetime:
            return event['id']
    return ''


def delete_slots_on_calendars(list_services, start_datetime, username):
    for service in list_services:
        event_id = get_event_id(start_datetime, username, service)
        utils.delete_event(service, event_id)


def delete_volunteer_slot(username, volunteer_service, clinic_service):
    date = utils.get_date()
    volunteer_slots = get_volunteered_slots(clinic_service, username, date)
    if len(volunteer_slots) > 0:
        print_open_slots_table(volunteer_slots, date, 'Displaying volunteered events:')
    else:
        return False, 'No volunteer slots available to delete'
    selected = int(input('Choose the volunteered slot you want to delete: '))
    thirty_minute_slots = convert_slot_into_30_min_slots((volunteer_slots[selected-1][0], volunteer_slots[selected-1][1]))
    for slot in thirty_minute_slots:
        start_datetime, end_datetime = utils.convert_date_and_time_to_rfc_format(date, slot[0], slot[1])
        delete_slots_on_calendars([volunteer_service, clinic_service], start_datetime, username)
    return True, 'Volunteered slots were succesfully deleted.'