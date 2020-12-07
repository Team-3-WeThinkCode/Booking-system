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


def split_username(email):
    """
    Function will split the users email address to grab the username before the 
    @ symbol.
    """
    return email.split(sep='@', maxsplit=1)[0]


def print_correlating_table(volunteer, create, student, clinic, created, event_list):
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    end_date = ((datetime.datetime.utcnow()) + datetime.timedelta(days=7)).isoformat() + 'Z'
    events = utils.get_events(clinic.service, now, end_date)
    if created:
        return
    if event_list and volunteer:
        # user list-bookings: print table with all booked slots (volunteer & patient)
        print_all_booked_slots_table(events, student.username)
    elif event_list and not volunteer:
        # user list-slots: print table with all open slots besides the user requesting
        print_all_available_booking_slots_table(events, student.username)
    elif volunteer and create:
        #volunteer create slot: print table with open slot times where can volunteer
        print_open_volunteer_slots_table(student.username, student.service, clinic.service, student.info['date'])
    elif volunteer and not create:
        #volunteer delete slot: print table with volunteered slots
        print_volunteered_slots_table(events, student.username)
    elif create and not volunteer:
        #patient create booking: print table with open volunteer slots to book
        print_available_booking_slots_table(events)
    elif not (volunteer and create):
        #patient delete booking: print table with volunteer slots booked by user
        print_booked_slots_table(events, student.username)
    

def list_open_volunteer_slots(clinic_service, username, date):
    open_slots = volunteer.get_open_volunteer_slots_of_the_day(date, username, clinic_service)
    if len(open_slots) == 0:
        return False, 'ERROR: There are no open slots on this day.'
    else:
        volunteer.print_open_slots_table(open_slots, date, 'Open volunteer slots for '+str(date)+':')
        return True, ''


def print_table(table_info, heading):
    '''
    Prints table with event information
    Table headings: #, Volunteer name, Date, Time, ID, Patient
    table_info : list of tuples; correlates with table headings
    heading : heading displayed above table
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


def get_volunteered_slots_table_info(events, username):
    '''
    Gets data for table to be displayed
    Data on volunteer's slots
    '''

    table_info = []
    start_times = ['08:30', '10:00', '11:30', '13:00','14:30', '16:00']
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        start_date = (start[0:10])
        start_time = start[11:16]
        patient = 'Open slot.'
        if len(event['attendees']) > 1:
            patient = split_username(event['attendees'][1]['email'])
        print(start_time)
        if (start_time in start_times) and (event['summary'][11:] == username):
            row = (username,start_date,start_time,event['id'],patient)
            table_info.append(row)
    return table_info


def get_booked_slots_table_info(events, username):
    table_info = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        start_date = (start[0:10])
        start_time = (start[11:16]+' - '+end[11:16])
        if len(event['attendees']) > 1:
            patient = split_username(event['attendees'][1]['email'])
            if patient == username:
                row = (event['summary'][10:],start_date,start_time,event['id'],patient)
                table_info.append(row)
    return table_info


def get_all_booked_slots_table_info(events, username):
    table_info = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        start_date = (start[0:10])
        start_time = (start[11:16]+' - '+end[11:16])
        if len(event['attendees']) >= 1:
            if len(event['attendees']) > 1:
                patient = split_username(event['attendees'][1]['email'])
            else:
                patient = "Open-slot"
            volunteer = split_username(event['attendees'][0]['email'])
            if patient == username or volunteer == username:
                row = (event['summary'][10:],start_date,start_time,event['id'],patient)
                table_info.append(row)
    return table_info


def get_open_volunteer_slots_table_info(username, volunteer_service, clinic_service, date):
    table_info = []
    ninty_min_slots = [('08:30', '10:00'), ('10:00', '11:30'), ('11:30', '13:00'), ('13:00', '14:30'), ('14:30', '16:00'), ('16:00', '17:30')]
    for slot in ninty_min_slots:
        start_datetime, end_datetime = utils.convert_date_and_time_to_rfc_format(date, slot[0], slot[1])
        if volunteer.is_slot_available(volunteer_service, username, start_datetime, end_datetime):
            row = ('-', date, slot[0], '-', 'Open slot.')
            table_info.append(row)
    return table_info


def get_open_booking_slots_table_info(events):
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
    table_info = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        start_date = (start[0:10])
        start_time = (start[11:16]+' - '+end[11:16])
        if not len(event['attendees']) > 1 and split_username(event['attendees'][0]['email']) != username:
            row = (event['summary'][10:],start_date,start_time,event['id'],'Open slot.')
            table_info.append(row)
    return table_info


def print_volunteered_slots_table(events, username):
    '''
    Gets and displays volunteer's slot data in table form
    '''
    
    table_info = get_volunteered_slots_table_info(events, username)
    if table_info:
        print_table(table_info, 'Volunteered slots for the next 7 days:')
    else:
        utils.print_output('ERROR: You have no volunteer slots in the next 7 days.')


def print_open_volunteer_slots_table(username, volunteer_service, clinic_service, date):
    table_info = get_open_volunteer_slots_table_info(username, volunteer_service, clinic_service, date)
    if table_info:
        print_table(table_info, 'Open volunteer slots for '+str(date)+':')
    else:
        utils.print_output('ERROR: There are no open volunteer slots on '+str(date)+':')


def print_booked_slots_table(events, username):
    table_info = get_booked_slots_table_info(events, username)
    if table_info:
        print_table(table_info, 'Your booked slots for the next 7 days:')
    else:
        utils.print_output('ERROR: You have no booked slots for the next 7 days.')


def print_all_booked_slots_table(events, username):
    table_info = get_all_booked_slots_table_info(events, username)
    if table_info:
        print_table(table_info, 'Your booked slots for the next 7 days:')
    else:
        utils.print_output('ERROR: You have no booked slots for the next 7 days.')


def print_available_booking_slots_table(events):
    table_info = get_open_booking_slots_table_info(events)
    if table_info:
        print_table(table_info, 'Volunteer slots available for bookings:')
    else:
        utils.print_output('ERROR: There are no volunteer slots available to book.')


def print_all_available_booking_slots_table(events, username):
    table_info = get_all_open_booking_slots_table_info(events, username)
    if table_info:
        print_table(table_info, 'Volunteer slots available for bookings:')
    else:
        utils.print_output('ERROR: There are no volunteer slots available to book.')
    