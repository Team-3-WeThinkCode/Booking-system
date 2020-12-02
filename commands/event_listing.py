import datetime
import json
from prettytable import PrettyTable
from commands import volunteer
import os
import sys

from rich.console import Console
from rich.table import Table
from rich import print

USER_PATHS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../'))
sys.path.insert(0, USER_PATHS)
import utilities as utils

console = Console()

def list_personal_slots(service, fetch, user, username):
    """
    creates a list of objects, each object will be details for an event.
    the function will retrieve open slots for the next 7 days.
    RETURNS: a list of objects with the keys being the unique id of the event and the value the object for th event.
    funtion will fetch the open slots each time the program is launched to save the slots locally in json files bu calling store_slot_data(events)
    """
    # Get the UCT time that is current and formats it to allow for google API parameter 
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    # Get the UCT time that is current + 7 days added and formats it to allow for google API parameter 
    end_date = ((datetime.datetime.utcnow()) + datetime.timedelta(days=7)).isoformat() + 'Z'
    events = utils.get_events(service, now, end_date)
    if user == True:
        events = sort_booked_slots(events, username)
    if user == False:
        events = sort_open_slots(events, username)
    if fetch == False:
        print_slots_table(events)
    store_slot_data(events, user)
    return events, ''


def list_open_volunteer_slots(clinic_service, username, date):
    open_slots = volunteer.get_open_volunteer_slots_of_the_day(date, username, clinic_service)
    if len(open_slots) == 0:
        return False, 'ERROR: There are no open slots on this day.'
    else:
        volunteer.print_open_slots_table(open_slots, date, 'Open volunteer slots for '+str(date)+':')
        return True, ''
    

def sort_open_slots(events, username):
    """
    Functions will sort a list of events, only events containing 1 attendee will be added to the new list.
    this will be events that are open to be booked by the user.
    """
    new_events = []
    for event in events:
        try:
            if len(event['attendees']) == 1 and event['attendees'][0]['email'] != username+"@student.wethinkcode.co.za":
                new_events.append(event)
        except:
            continue
    return new_events

def sort_booked_slots(events, username):
    """
    Functions will sort a list of events, only events containing 1 attendee will be added to the new list.
    this will be events that are open to be booked by the user.
    """
    new_events = []
    for event in events:
        try:
            for i in range(len(event['attendees'])):
                if (event['attendees'][i]["email"]) == username+'@student.wethinkcode.co.za':
                    new_events.append(event)
                continue
        except:
            continue
    return new_events


def store_slot_data(events, user):
    """
    Function will populate a JSON file with the details of each open slot recieved from google API.
    Old data will be deleted and new data writen to not overpopulate file.
    """
    if user == False:
        new_data = {"open_slots" : []}
        for event in events:
            new_data['open_slots'].append({event['id'] : event})
        with open('data_files/.open_slots.json', 'w') as f:
            json.dump(new_data, f, sort_keys=True, indent=4)
    elif user == True:
        new_data = {"events" : []}
        for event in events:
            if event["organizer"]["email"] ==  "code.clinic.test@gmail.com":
                new_data['events'].append({event['id'] : event})
        with open('data_files/.student_events.json', 'w') as f:
            json.dump(new_data, f, sort_keys=True, indent=4)


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
    table = Table(show_header=True, header_style="bold tan")
    print('\n[bold]'+heading+'\n[/bold]')
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


def get_volunteered_booked_table_info(events):
    '''
    Gets data for table to be displayed
    Data on volunteer's slots
    '''

    table_info = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        start_date = (start[0:10])
        start_time = (start[11:16]+' - '+end[11:16])
        patient = 'Open slot.'
        if len(event['attendees']) > 1:
            patient = split_username(event['attendees'][1]['email'])
        row = (event['summary'][10:],start_date,start_time,event['id'],patient)
        table_info.append(row)
    if table_info:
        return table_info


def print_slots_table(events):
    '''
    Gets and displays volunteer's slot data in table form
    '''
    
    table_info = get_volunteered_booked_table_info(events)
    print_table(table_info, 'Volunteered slots for the next 7 days:')


def split_username(email):
    """
    
    """
    return email.split(sep='@', maxsplit=1)[0]
    