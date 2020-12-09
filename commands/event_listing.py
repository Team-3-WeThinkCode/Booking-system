import datetime
from commands import volunteer
import os
import sys

from rich.console import Console
from rich.table import Table

USER_PATHS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../'))
sys.path.insert(0, USER_PATHS)
import utilities as utils


console = Console()


def get_volunteered_slots_table_info(events, username):
    '''
    The date, start time, event UID and patient username information is gathered
    from the events list if the event is a slot with the user as a volunteer.
    This information is then stored in a list called table_info.

            Parameters:
                    events        (list): Events from the clinic calendar
                    username       (str): Student's username

            Returns:
                    table_info (2D-list): Information on username of the volunteer, 
                                          event date, start time, event UID and 
                                          patient's username for events the user 
                                          volunteered for.
    '''

    table_info = []
    start_times = ['08:30', '10:00', '11:30', '13:00','14:30', '16:00']
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        start_date = (start[0:10])
        start_time = start[11:16]
        patient = 'Open slot.'
        if len(event['attendees']) > 1:
            patient = utils.split_username(event['attendees'][1]['email'])
        if (start_time in start_times) and (event['summary'][11:] == username):
            row = (username,start_date,start_time,event['id'],patient)
            table_info.append(row)
    return table_info


def get_booked_slots_table_info(events, username):
    '''
    The volunteer username, date, start time, event UID and patient username
    information gathered from the events list if the event is a slot the user has
    booked (listed as an attendee). This information is then stored in a list called
    table_info.

            Parameters:
                    events        (list): Events from the clinic calendar
                    username       (str): Student's username

            Returns:
                    table_info (2D-list): Information on username of the volunteer, 
                                          event date, start time, event UID and 
                                          patient's username for events the user 
                                          is listed as an attendee for.
    '''

    table_info = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        start_date = (start[0:10])
        start_time = (start[11:16]+' - '+end[11:16])
        if len(event['attendees']) > 1:
            patient = utils.split_username(event['attendees'][1]['email'])
            if patient == username:
                row = (event['summary'][10:],start_date,start_time,event['id'],patient)
                table_info.append(row)
    return table_info


def get_all_booked_slots_table_info(events, username):
    '''
    The volunteer username, date, start time, event UID and patient username
    information gathered from the events list if the event is a slot the user is
    a patient/volunteer for. This information is then stored in a list called 
    table_info.

            Parameters:
                    events        (list): Events from the clinic calendar
                    username       (str): Student's username

            Returns:
                    table_info (2D-list): Information on username of the volunteer, 
                                          event date, start time, event UID and 
                                          patient's username for events the user 
                                          is listed as an attendee/volunteer for.
    '''

    table_info = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        start_date = (start[0:10])
        start_time = (start[11:16]+' - '+end[11:16])
        if len(event['attendees']) >= 1:
            if len(event['attendees']) > 1:
                patient = utils.split_username(event['attendees'][1]['email'])
            else:
                patient = "Open-slot"
            volunteer = utils.split_username(event['attendees'][0]['email'])
            if patient == username or volunteer == username:
                row = (event['summary'][10:],start_date,start_time,event['id'],patient)
                table_info.append(row)
    return table_info


def get_open_volunteer_slots_table_info(username, volunteer_service, clinic_service, date):
    #TODO: remove clinic_service as a param -> not being used
    #TODO: remove '-' and replace in docstring
    '''
    Returns a list of dates and times where the student has no events in their calendar
    and therefore can create a volunteer slot in. This information is stored in a 2D-list
    called table_info consisting of each 90 min slot's date, start time, and "-"-operand
    for open fields (e.g. volunteer username and patient username).

            Parameters:
                    username          (str): Student's username
                    volunteer_service (obj): Student's Google calendar API service
                    events           (list): Events from the clinic calendar

            Returns:
                    table_info    (2D-list): Information on date and start time, for 90 minute
                                             slot times the student is available in the next 7 days.
    '''

    table_info = []
    ninty_min_slots = [('08:30', '10:00'), ('10:00', '11:30'), ('11:30', '13:00'), ('13:00', '14:30'), ('14:30', '16:00'), ('16:00', '17:30')]
    for slot in ninty_min_slots:
        if utils.date_has_passed(date, slot[0]):
            continue
        start_datetime, end_datetime = utils.convert_date_and_time_to_rfc_format(date, slot[0], slot[1])
        if volunteer.is_slot_available(volunteer_service, username, start_datetime, end_datetime):
            row = ('-', date, slot[0], '-', 'Open slot.')
            table_info.append(row)
    return table_info


def get_open_booking_slots_table_info(events):
    '''
    Returns a list of volunteer usernames, dates, start times and event UIDs of 
    volunteer events that are still open to book by students (patients). This 
    information is gathered by looping through the events list and stored in 
    a 2D-list called table_info.

            Parameters:
                    events           (list): Events from the clinic calendar

            Returns:
                    table_info    (2D-list): Information on volunteer usernames, dates, 
                                             start times and event UIDs of volunteer events
                                             that are still open to book by students (patients)
    '''

    table_info = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        start_date = (start[0:10])
        start_time = (start[11:16]+' - '+end[11:16])
        if not len(event['attendees']) > 1:
            row = (event['summary'][10:],start_date,start_time,event['id'],'Open slot.')
            table_info.append(row)
    return table_info


def get_all_open_booking_slots_table_info(events, username):
    '''
    Returns a list of volunteer usernames, dates, start times and event UIDs of 
    volunteer events that are still open to book by user. This information is 
    gathered by looping through the events list and stored in a 2D-list called table_info.

            Parameters:
                    events           (list): Events from the clinic calendar
                    username          (str): Student's username

            Returns:
                    table_info    (2D-list): Information on volunteer usernames, dates, 
                                             start times and event UIDs of volunteer events
                                             that are still open to book by students (patients)
    '''

    table_info = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        start_date = (start[0:10])
        start_time = (start[11:16]+' - '+end[11:16])
        if not len(event['attendees']) > 1 and utils.split_username(event['attendees'][0]['email']) != username:
            row = (event['summary'][10:],start_date,start_time,event['id'],'Open slot.')
            table_info.append(row)
    return table_info


def print_table(table_info, heading):
    '''
    Prints table with the specified tabe heading and information from the table_info list.
    Table headings: [#, Volunteer name, Date, Time, ID, Patient]

            Parameters:
                    table_info      (list): Information on events correlating with 
                                            the table headings
                    heading          (str): Heading to be displayed above table
    '''

    nums = 1
    index = 0
    table_headings = ['Volunteer username', 'Date', 'Time', 'ID', 'Patient']
    table = Table(title=heading, show_header=True, header_style="bold tan")
    table.add_column('#.', style="dim", width=12)
    for heading in table_headings:
        table.add_column(heading)
    for row in table_info:
        table.add_row(
            str(nums),
            row[0],
            row[1],
            row[2],
            row[3],
            row[4]
        )
        index += 1
        nums += 1
    console.print(table)


def print_correct_table(table_info, heading, error_message):
    '''
    Prints table from information provided. If there is no information provided
    then an error message will be printed and the program will exit

            Parameters:
                    table_info     (2D-list): List of information per table row
                    heading            (str): Heading to be printed above table
                    error_message      (str): Message to output if no information 
                                              provided
    '''

    if table_info:
        print_table(table_info, heading)
    else:
        utils.error_handling(error_message)


def get_events_for_n_days(service):
    '''
    Returns events occuring withing the given amount of days on the user's calendar
    by using the Google calendar API service. If the number of days are not specified,
    the default amount of days to return is 7 days.

            Parameters:
                    service  (obj): Google calendar API service

            Returns:
                    n_days   (int): Number of days
                    events  (list): Events occuring in specified amount of days
    '''

    n_days = 7
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    if sys.argv[-1].isdigit():
        n_days = int(sys.argv[-1])
    end_date = ((datetime.datetime.utcnow()) + datetime.timedelta(days=n_days)).isoformat() + 'Z'
    events = utils.get_events(service, now, end_date)
    return n_days, events


def print_correlating_table(volunteer, create, student, clinic, created, event_list):
    #TODO: Change up params -> too many given
    '''
    Outputs correct table for specific command and information given by user. If, the boolean,
    created is True - no table needs to be printed as output and the program will exit the 
    function and continue with the remainder steps

            Parameters:
                    volunteer  (boolean): True if user is a volunteer
                    create     (boolean): True if user is creating a booking/volunteer slot
                    student        (obj): Object with information on logged-in student
                    clinic         (obj): Object with information on Code clinic
                    created    (boolean): True if user's given command was executed succesfully
                    event_list    (list): List of events occuring in the Code clinic's calendar
    '''

    table_info = []
    heading, error_message = '', ''
    days, events = get_events_for_n_days(clinic.service)
    if created:
        return
    if event_list and volunteer:
        # user list-bookings: print table with all booked slots (volunteer & patient)
        table_info = get_all_booked_slots_table_info(events, student.username)
        heading = f'Your booked slots for the next {days} days:'
        error_message = f'ERROR: You have no booked slots for the next {days} days.'
    elif event_list and not volunteer:
        # user list-slots: print table with all open slots besides the user requesting
        table_info = get_all_open_booking_slots_table_info(events, student.username)
        heading = f'Volunteer slots for the next {days} days available for booking:'
        error_message = 'ERROR: There are no volunteer slots available to book.'
    elif volunteer and create:
        #volunteer create slot: print table with open slot times where can volunteer
        table_info = get_open_volunteer_slots_table_info(student.username, student.service, clinic.service, student.info['date'])
        heading = 'Open volunteer slots for '+student.info['date']+':'
        error_message = 'ERROR: There are no open volunteer slots on '+student.info['date']+'.'
    elif volunteer and not create:
        #volunteer delete slot: print table with volunteered slots
        table_info = get_volunteered_slots_table_info(events, student.username)
        heading = f'Volunteered slots for the next {days} days:'
        error_message = f'ERROR: You have no volunteer slots in the next {days} days.'
    elif create and not volunteer:
        #patient create booking: print table with open volunteer slots to book
        table_info = get_open_booking_slots_table_info(events)
        heading = f'Volunteer slots for the next {days} days available for booking:'
        error_message = 'ERROR: There are no volunteer slots available to book.'
    elif not (volunteer and create):
        #patient delete booking: print table with volunteer slots booked by user
        table_info = get_booked_slots_table_info(events, student.username)
        heading = f'Your booked slots for the next {days} days:'
        error_message = f'ERROR: You have no booked slots for the next {days} days.'
    print_correct_table(table_info, heading, error_message)