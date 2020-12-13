import os, sys
USER_PATHS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../'))
sys.path.insert(0, USER_PATHS)
from utilities import utilities as utils


def is_volunteering_at_specified_time(clinic_service, username, start_datetime, end_datetime):
    '''
    Sorts through events, occuring within specified datetimes, on the Code
    clinic's calendar to confirm whether student with specified username is
    volunteering during specified date/time.

            Parameters:
                    clinic_service  (obj): Code clinic's Google calendar API
                                           service
                    username        (str): Student's username
                    start_datetime  (str): Datetime (in rfc format) that
                                           volunteer event starts
                    end_datetime    (str): Datetime (in rfc format) that
                                           volunteer event ends

            Returns:
                    True        (boolean): Student is volunteering at
                                           specified datetime
                    False       (boolean): Student is not volunteering at
                                           specified datetime
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
    Sorts through volunteer slot times and confirms whether student is
    volunteering during the slot time. If student is not volunteering
    during the slot time, the slot time is added to the list, open_slots.
    List of available volunteer slots are returned.

            Parameters:
                    date                   (str): Date in format yyyy-mm-dd
                    username               (str): Student's username
                    clinic_service         (obj): Code clinic's Google calendar
                                                  API service

            Returns:
                    open_slots  (list of tuples): Volunteer slot times user is
                                                  not volunteering in
    '''

    slots = [('08:30', '10:00'), ('10:00', '11:30'),('11:30', '13:00'),
             ('13:00', '14:30'), ('14:30', '16:00'), ('16:00', '17:30')]
    open_slots = []
    for slot in slots:
        start_datetime, end_datetime = utils.convert_date_and_time_to_rfc_format(date,
                                                                                 slot[0],
                                                                                 slot[1])
        busy = is_volunteering_at_specified_time(clinic_service,
                                                 username,
                                                 start_datetime,
                                                 end_datetime)
        if not busy:
            open_slots.append(slot)
    return open_slots


def convert_90_min_slot_into_30_min_slots(slot):
    '''
    Converts a 90 minute slot to a list of 30 minute slots. The list consists
    out of tuples with the first tuple value being the start time and the
    second value being the end time of the 30 minute slot.

            Parameters:
                    slot              (tuple): 90 minute time slot

            Returns:
                    *        (list of tuples): 3 x 30 minute slots
                    *            (empty list): if time is not a multiple of
                                               30 minutes
    '''

    start_hour, start_minute = int(slot[0][:2]), int(slot[0][3:])
    if start_minute == 30:
        return [(slot[0], str(start_hour+1)+':'+'00'),
                (str(start_hour+1)+':'+'00', str(start_hour+1)+':'+'30'),
                (str(start_hour+1)+':'+'30', str(start_hour+2)+':'+'00')]
    elif start_minute == 0:
        return [(slot[0], str(start_hour)+':'+'30'),
                (str(start_hour)+':'+'30', str(start_hour+1)+':'+'00'),
                (str(start_hour+1)+':'+'00', str(start_hour+1)+':'+'30')]
    return []


def create_volunteer_slot(username, date, time, volunteer_service, clinic_service):
    '''
    Creates a 90 minute volunteer slot if the student has an open slot in
    their personal calendar during the specified slot time and the student
    does not have a volunteer slot created at the specified slot time in the
    clinic calendar.

            Parameters:
                    username          (str): Student's username
                    date              (str): Slot date in format <yyyy-mm-dd>
                    time              (str): Slot start time in format <hh:mm>
                    volunteer_service (str): Student's (volunteer) Google
                                             calendar API service
                    clinic_service    (str): Code clinic's Google calendar
                                             API service

            Returns:
                    True          (boolean): Volunteer slot succesfully
                                             created
                    False         (boolean): Volunteer slot not created
                    
    '''

    open_slots = get_open_volunteer_slots_of_the_day(date,
                                                     username,
                                                     clinic_service)
    if not open_slots:
        return False, 'ERROR: There are no open slots on this day.'
    time_slot_lst = list(filter(lambda x : x[0] == time, open_slots))
    if not time_slot_lst:
        utils.print_output('ERROR: Choose a valid/open slot start time.')
        return False
    time_slot = time_slot_lst[0]
    start_datetime, end_datetime = utils.convert_date_and_time_to_rfc_format(date,
                                                                             time_slot[0],
                                                                             time_slot[1])
    open = utils.is_slot_available(volunteer_service,
                                   username,
                                   start_datetime,
                                   end_datetime)
    if open:
        thirty_minute_slots = convert_90_min_slot_into_30_min_slots(time_slot)
        for slot in thirty_minute_slots:
            start_datetime, end_datetime = utils.convert_date_and_time_to_rfc_format(date,
                                                                                     slot[0],
                                                                                     slot[1])
            event_info = {'summary': 'VOLUNTEER: ' + str(username),
                          'start_datetime': start_datetime,
                          'end_datetime': end_datetime,
                          'attendees': []}
            response = utils.add_event_to_calendar(event_info,
                                                   clinic_service,
                                                   True,
                                                   username)
            utils.volunteer_accept_invite(clinic_service,
                                          response['id'],
                                          response)
        utils.print_output('Volunteer slots created!')
        return True
    msg = 'ERROR: You do not have an open slot in your calendar '\
                                            +'at the selected time.'
    utils.print_output(msg)
    return False


def get_volunteered_slot(clinic_service, username, date, time):
    '''
    Sorts through possible volunteer slot times to confirm that the specified
    time is a valid volunteer slot time. If the time is a valid volunteer time
    the Code clinic's calendar is used to check whether the student is
    volunteering at the specified date/time and that the volunteer slot has only
    one attendee (slot is not booked). The volunteer slot time is returned if 
    the event fulfills this criteria.

            Parameters:
                    clinic_service  (str): Code clinic's Google calendar
                                           API service
                    username        (str): Student's username
                    date            (str): Slot date in format <yyyy-mm-dd>
                    time            (str): Slot start time in format <hh:mm>

            Returns:
                    chosen_slot   (tuple): Start and end time of 90 min slot                        
    '''

    ninety_min_slots, chosen_slot = [], ''
    events_exist = False
    slots = [('08:30', '10:00'), ('10:00', '11:30'),
             ('11:30', '13:00'), ('13:00', '14:30'),
             ('14:30', '16:00'), ('16:00', '17:30')]
    for slot in slots:
        if time == slot[0]:
            ninety_min_slots = convert_90_min_slot_into_30_min_slots(slot)
            chosen_slot = slot
    if ninety_min_slots:
        for slot in ninety_min_slots:
            start, end = slot[0], slot[1]
            start_datetime, end_datetime = utils\
                .convert_date_and_time_to_rfc_format(date, start, end)
            events = utils.get_events(clinic_service,
                                      start_datetime,
                                      end_datetime)
            if events:
                events_exist = True
            for event in events:
                if event['summary'][11:] == username:
                    if not len(event['attendees']) == 1:
                        return
        if events_exist:
            return chosen_slot
    return
            

def get_event_id(start_datetime, end_datetime, username, clinic_service):
    '''
    Sorts through events, occuring between specified datetimes, to find the
    event UID of the student's volunteered slot.

            Parameters:
                    start_datetime                 (str): Datetime 
                                                          (in rfc format) of
                                                          when slot time starts
                    end_datetime                   (str): Datetime
                                                          (in rfc format) of
                                                          when slot time ends
                    username                       (str): Student's username
                    clinic_service                 (str): Code clinic's Google
                                                          calendar API service

            Returns:
                    volunteered_event[0]['id']     (str): Event UID of
                                                          volunteered event at
                                                          specified datetime
                    ''                       (empty str): If student did not
                                                          volunteer at
                                                          specified datetime                  
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
        event_id = get_event_id(start_datetime,
                                end_datetime,
                                username,
                                service)
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
                    volunteer_service  (str): Student's (volunteer) Google
                                              calendar API service
                    clinic_service     (str): Code clinic's Google calendar
                                              API service

            Returns:
                    True        (boolean): Volunteer slot succesfully deleted
                    False       (boolean): Volunteer slot could not be
                                           deleted/found          
    '''

    msg = ''
    volunteer_slot = get_volunteered_slot(clinic_service,
                                          username,
                                          date,
                                          time)
    if not volunteer_slot:
        msg = 'ERROR: No volunteer slot available to delete at specified date/time.'
        utils.print_output(msg)
        return False
    thirty_minute_slots = convert_90_min_slot_into_30_min_slots((volunteer_slot[0],
                                                                 volunteer_slot[1]))
    for slot in thirty_minute_slots:
        start_datetime, end_datetime = utils.convert_date_and_time_to_rfc_format(date,
                                                                                 slot[0],
                                                                                 slot[1])
        delete_slots_on_calendars([volunteer_service,
                                   clinic_service],
                                   start_datetime,
                                   end_datetime,
                                   username)
    msg = 'Volunteered slots were succesfully deleted.'
    utils.print_output(msg)
    return True