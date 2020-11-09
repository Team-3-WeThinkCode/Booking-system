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


def is_leap_year(year):
    if (year % 4) == 0:  
        if (year % 100) == 0:  
            if (year % 400) == 0:  
                return True  
            else:  
                return False 
        else:  
            return True 
    else:  
        return False 


def date_fomat_correct(date):
    try:
        year, month, day = int(date[:4]), int(date[5:7]), int(date[8:])
    except:
        return False
    if year > 2021:
        return False
    elif day < 1:
        return False
    elif month == 4 or month == 6 or month == 9:
        if day > 31:
            return False
    elif is_leap_year(year) and month == 2:
        if day > 29:
            return False
    else:
        if day > 30:
            return False
    return True


def get_date():
    date = str(input('Insert date in format (yyyy-mm-dd): '))
    while not date_fomat_correct(date):
        print('Please enter a valid date!')
        date = str(input('Insert date in format (yyyy-mm-dd): '))
    return date


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


def convert_date_and_time_to_rfc_format(date, start_time, end_time):
    '''
    date in format (yyyy-mm-dd)
    time in format (hh:mm)
    :return: start dateTime and end dateTime (30min events) in rfc format
    '''

    year, month, day = date[:4], date[5:7], date[8:]
    start_hour, start_minute = start_time[:2], start_time[3:]
    end_hour, end_minute = end_time[:2], end_time[3:]
    start_dateTime = year+'-'+month+'-'+day+'T'+start_hour+':'+start_minute+':00'+'+02:00'
    end_dateTime = year+'-'+month+'-'+day+'T'+end_hour+':'+end_minute+':00'+'+02:00'
    return start_dateTime, end_dateTime


def add_event_to_calendar(event_info, service):
    people = []
    location = 'WeThinkCode, Victoria & Alfred Waterfront, Cape Town'
    while True:
        add_atendee = str(input("Add atendee via email? (y/n) "))
        print(add_atendee)
        if add_atendee.strip() == 'y':
            atendee_email = str(input('Please enter email address of atendee: '))
            people.append({'email': atendee_email.strip()})
            print(people)
        else:
            break
    event = utils.create_makeshift_event(event_info['summary'], location, '', event_info['start_datetime'], event_info['end_datetime'])
    event = service.events().insert(calendarId='primary', body=event).execute()
    with open('data_files/data.json', 'a+') as outfile:
        json.dump(event, outfile, sort_keys=True, indent=4)


def slots_are_available(list_services, start_datetime, end_datetime):
    new_event = utils.create_makeshift_event('', '', '', start_datetime, end_datetime)
    for service in list_services:
        if utils.already_exists(new_event, service):
            return False
    return True


def create_volunteer_slot(username, volunteer_service, codeclinic_service):
    '''
    :return: True if volunteer slot created succesfully
    '''

    date = get_date()
    slots = get_open_slots_of_the_day(date)
    time = get_slot_time(slots)
    start_datetime, end_datetime = convert_date_and_time_to_rfc_format(date, time[0], time[1])
    event_info_volunteer = {'summary': 'VOLUNTEER: ' + str(username), 'start_datetime': start_datetime, 'end_datetime': end_datetime}
    event_info_clinic = {'summary': 'VOLUNTEER: ' + str(username), 'start_datetime': start_datetime, 'end_datetime': end_datetime}
    if slots_are_available([volunteer_service, codeclinic_service], start_datetime, end_datetime):
        add_event_to_calendar(event_info_volunteer, volunteer_service)
        add_event_to_calendar(event_info_clinic, codeclinic_service)
        return True
    return False