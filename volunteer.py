import utilities as utils
import quickstart
import json

slots = [('08:30', '10:00'), ('10:00', '11:30'), ('11:30', '13:00'), ('13:00', '14:30'), ('14:30', '16:00'), ('16:00', '17:30')]

'''
TODO:
Check data from json and check what slots are open
:return: list of slots in above format
'''
def get_open_slots_of_the_day(date):
    slot = slots
    return slot


def get_slot_time(slots):
    print('Choose a slot from the list:')
    i = 1
    chosen_slot = 0
    for slot in slots:
        print(str(i)+'. ' + str(slot[0]) + ' - ' + str(slot[1]))
        i += 1
    chosen_slot = int(input())
    while chosen_slot > len(slots):
        chosen_slot = int(input('Please choose valid slot: '))
    return slots[chosen_slot-1]


def slot_is_available(service, start_datetime, end_datetime):
    if len(utils.get_events(service, start_datetime, end_datetime)) > 0:
            return False
    return True


def create_volunteer_slot(username, volunteer_service, codeclinic_service):
    '''
    :return: True if volunteer slot created succesfully
    '''

    date = utils.get_date()
    slots = get_open_slots_of_the_day(date)
    time = get_slot_time(slots)
    start_datetime, end_datetime = utils.convert_date_and_time_to_rfc_format(date, time[0], time[1])
    if slot_is_available(volunteer_service, start_datetime, end_datetime):
        event_info_volunteer = {'summary': 'VOLUNTEER: ' + str(username), 'start_datetime': start_datetime, 'end_datetime': end_datetime}
        event_info_clinic = {'summary': 'VOLUNTEER: ' + str(username), 'start_datetime': start_datetime, 'end_datetime': end_datetime}
        utils.add_event_to_calendar(event_info_volunteer, volunteer_service, False)
        utils.add_event_to_calendar(event_info_clinic, codeclinic_service, True)
        return True
    return False