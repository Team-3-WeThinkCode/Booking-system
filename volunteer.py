import utilities as utils
from utils.TableIt import TableIt as tabulate


def get_open_slots_of_the_day(date, clinic_service):
    slots = [('08:30', '10:00'), ('10:00', '11:30'), ('11:30', '13:00'), ('13:00', '14:30'), ('14:30', '16:00'), ('16:00', '17:30')]
    open_slots = []
    for slot in slots:
        start_datetime, end_datetime = utils.convert_date_and_time_to_rfc_format(date, slot[0], slot[1])
        if utils.slot_is_available(clinic_service, start_datetime, end_datetime):
            open_slots.append(slot)
    return open_slots


def print_slots_table(slots, date):
    """
    Uses the TableIt module to display data of open slots to the user in tabular form.
    Event name, time, date, id will be sliced from the events objects given and used to display in the table.
    """
    table = [
        ['#.', 'date.', 'start time.', 'end time.']
    ]
    nums = 1
    print()
    print('Displaying all open slots for the selected date:')
    for slot in slots:
        table.append(['', '-------------------------', '-------------------------', '-------------------------', '-------------------------'])
        table.append([nums, date, slot[0], slot[1]])
        nums += 1
    tabulate.printTable(table, useFieldNames=True, color=(255, 0, 255))


def get_slot_time(slots, date):
    print_slots_table(slots, date)
    chosen_slot = int(input('Choose a slot: '))
    while chosen_slot > len(slots):
        chosen_slot = int(input('Please choose valid slot: '))
    return slots[chosen_slot-1]


def create_volunteer_slot(username, volunteer_service, codeclinic_service):
    '''
    :return: True if volunteer slot created succesfully
    '''

    date = utils.get_date()
    open_slots = get_open_slots_of_the_day(date, codeclinic_service)
    if len(open_slots) == 0:
        print('There are no open slots on this day.')
        return False
    time = get_slot_time(open_slots, date)
    start_datetime, end_datetime = utils.convert_date_and_time_to_rfc_format(date, time[0], time[1])
    if utils.slot_is_available(volunteer_service, start_datetime, end_datetime):
        event_info_clinic = {'summary': 'VOLUNTEER: ' + str(username), 'start_datetime': start_datetime, 'end_datetime': end_datetime, 'attendees': []}
        utils.add_event_to_calendar(event_info_clinic, codeclinic_service, True, username)
        print('Volunteer slot created!')
        return True
    print('You do not have an open slot at the selected time.')
    return False


def delete_volunteer_slot():
    pass