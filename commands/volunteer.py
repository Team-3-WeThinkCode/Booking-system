import os
import sys

USER_PATHS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../'))
sys.path.insert(0, USER_PATHS)
import utilities as utils


def is_volunteering_at_specified_time(clinic_service, username, start_datetime, end_datetime):
    '''
    Sorts through events, occuring within specified datetimes, on the Code clinic's calendar
    to confirm whether student with specified username is volunteering during specified date/time.

            Parameters:
                    clinic_service  (obj): Code clinic's Google calendar API service
                    username        (str): Student's username
                    start_datetime  (str): Datetime (in rfc format) that volunteer event starts
                    end_datetime    (str): Datetime (in rfc format) that volunteer event ends

            Returns:
                    True        (boolean): Student is volunteering at specified datetime
                    False       (boolean): Student is not volunteering at specified datetime
    '''

    events = utils.get_events(clinic_service, start_datetime, end_datetime)
    events = list(filter(lambda x: x['start'].get('dateTime') == start_datetime, events))
    events = list(filter(lambda y: y['end'].get('dateTime') == end_datetime, events))
    if events:
        if "VOLUNTEER: " + str(username) in events[0]['summary']:
            return True
    return False


def get_open_volunteer_slots_of_the_day(date, username, clinic_service):
    #TODO add where student busy with other event in own personal calendar
    '''
    Sorts through volunteer slot times and confirms whether student is volunteering during 
    the slot time. If student is not volunteering during the slot time, the slot time is 
    added to the list, open_slots. List of available volunteer slots are returned.

            Parameters:
                    date                   (str): Date in format yyyy-mm-dd
                    username               (str): Student's username
                    clinic_service         (obj): Code clinic's Google calendar API service

            Returns:
                    open_slots  (list of tuples): Volunteer slot times user is not volunteering in
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
    Converts a 90 minute slot to a list of 30 minute slots. The list consists out of
    tuples with the first tuple value being the start time and the second value being
    the end time of the 30 minute slot.

            Parameters:
                    slot              (tuple): 90 minute time slot

            Returns:
                    *        (list of tuples): 3 x 30 minute slots
                    *            (empty list): if time is not a multiple of 30 minutes
    '''

    start_hour, start_minute = int(slot[0][:2]), int(slot[0][3:])
    if start_minute == 30:
        return [(slot[0], str(start_hour+1)+':'+'00'), (str(start_hour+1)+':'+'00', str(start_hour+1)+':'+'30'), (str(start_hour+1)+':'+'30', str(start_hour+2)+':'+'00') ]
    elif start_minute == 0:
        return [(slot[0], str(start_hour)+':'+'30'), (str(start_hour)+':'+'30', str(start_hour+1)+':'+'00'), (str(start_hour+1)+':'+'00', str(start_hour+1)+':'+'30') ]
    return []


def is_slot_available(service, username, start_datetime, end_datetime):
    '''
    Confirms whether student with specified username has an open slot, at the specified
    datetime, in their calendar.

            Parameters:
                    service         (obj): Student's Google calendar API service
                    username        (str): Student's username
                    start_datetime  (str): Datetime (in rfc format) of when slot time starts
                    end_datetime    (str): Datetime (in rfc format) of when slot time ends

            Returns:
                    True        (boolean): Student has an open slot in their calendar
                    False       (boolean): Student does not have an open slot in their calendar
                    
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


def create_volunteer_slot(username, date, time, volunteer_service, clinic_service):
    #TODO: Simplify checking both calendars -> is it necessary?
    '''
    Creates a 90 minute volunteer slot if the student has an open slot in their personal
    calendar during the specified slot time and the student does not have a volunteer slot
    created at the specified slot time in the clinic calendar.

            Parameters:
                    username            (str): Student's username
                    date                (str): Slot date in format <yyyy-mm-dd>
                    time                (str): Slot start time in format <hh:mm>
                    volunteer_service   (str): Student's (volunteer) Google calendar API service
                    clinic_service      (str): Code clinic's Google calendar API service

            Returns:
                    True        (boolean): Volunteer slot succesfully created
                    False       (boolean): Volunteer slot not created
                    
    '''

    open_slots = get_open_volunteer_slots_of_the_day(date, username, clinic_service)
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
            response = utils.add_event_to_calendar(event_info, clinic_service, True, username)
            utils.volunteer_accept_invite(clinic_service, response['id'], username, response)
        utils.print_output('Volunteer slots created!')
        return True
    utils.print_output('ERROR: You do not have an open slot in your calendar at the selected time.')
    return False


def get_volunteered_slot(clinic_service, username, date, time):
    #TODO simplify function
    '''
    Sorts through events occuring between 08:30 and 17:30, as this is the first and last
    volunteer slot start times of each day, and checks whether student is volunteering
    at the specified date and time.

            Parameters:
                    clinic_service  (str): Code clinic's Google calendar API service
                    username        (str): Student's username
                    date            (str): Slot date in format <yyyy-mm-dd>
                    time            (str): Slot start time in format <hh:mm>

            Returns:
                    slot           (tuple): Start and end time of 90 min slot                        
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
    Sorts through events, occuring between specified datetimes, to find the event UID
    of the student's volunteered slot.

            Parameters:
                    start_datetime                 (str): Datetime (in rfc format) of when slot time starts
                    end_datetime                   (str): Datetime (in rfc format) of when slot time ends
                    username                       (str): Student's username
                    clinic_service                 (str): Code clinic's Google calendar API service

            Returns:
                    volunteered_event[0]['id']     (str): Event UID of volunteered event at specified datetime 
                    ''                       (empty str): If student did not volunteer at specified datetime                  
    '''

    events = utils.get_events(clinic_service, start_datetime, end_datetime)
    volunteered_event = list(filter(lambda x: x['summary'][11:] == username, events))
    if volunteered_event:
        return volunteered_event[0]['id']
    return ''


def delete_slots_on_calendars(list_services, start_datetime, end_datetime, username):
    '''
    Deletes events created in specified datetimes from the calendars in the list of 
    Google calendar API services.

            Parameters:
                    list_services   (str): List of Google calendar API services
                    start_datetime  (str): Datetime (in rfc format) of when slot time starts
                    end_datetime    (str): Datetime (in rfc format) of when slot time ends
                    username        (str): Student's username                      
    '''

    for service in list_services:
        event_id = get_event_id(start_datetime, end_datetime, username, service)
        utils.delete_event(service, event_id)


def delete_volunteer_slot(username, date, time, volunteer_service, clinic_service):
    '''
    The volunteer slots, that occur at specified date/time, are removed from the student's 
    calendar and the clinic's calendar. Deletes volunteer slots if:
    - the student's username is in the event summary (is the student's volunteered slot)
    - the student's 30 minute volunteered slots are not booked by another student

            Parameters:
                    username           (str): Student's username
                    date               (str): Slot date in format <yyyy-mm-dd>
                    time               (str): Slot start time in format <hh:mm>
                    volunteer_service  (str): Student's (volunteer) Google calendar API service
                    clinic_service     (str): Code clinic's Google calendar API service

            Returns:
                    True        (boolean): Volunteer slot succesfully deleted
                    False       (boolean): Volunteer slot could not be deleted/found          
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