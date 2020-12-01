import datetime
import json
import utilities as utils
from prettytable import PrettyTable
import volunteer


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
        print_slots_table(events, user)
    store_slot_data(events, user)
    return events, ''


def list_open_volunteer_slots(clinic_service, username, date):
    open_slots = volunteer.get_open_volunteer_slots_of_the_day(date, username, clinic_service)
    if len(open_slots) == 0:
        return False, 'There are no open slots on this day.'
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
            

def print_slots_table(events, user=False):
    """
    Uses the TableIt module to display data of open slots to the user in tabular form.
    Event name, time, date, id will be sliced from the events objects given and used to display in the table.
    """

    nums = 1
    B = "\033[1m" # Bold
    G = "\033[0;32;40m" # GREEN
    N = "\033[0m" # Reset
    table = PrettyTable([B+'#.'+N, G+B+'Volunteer name.'+N, G+B+'date.'+N, G+B+'time.'+N, G+B+'Unique ID.'+N, G+B+'Patient.'+N])
    if not events:
        if user == False:
            print('No open slots available.')
        else:
            print("You have no upcoming bookings.")
    elif events:
        headers = ['#.', 'Volunteer name.', 'date.', 'time.', 'Unique ID.']
        if user == False:
            print('Displaying all open slots for the next 7 days.')
        else:
            print('Displaying your Code Clinic bookings for the next 7 days')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            start_date = (start[0:10])
            start_time = (start[11:16]+' - '+end[11:16])
            if len(event['attendees']) > 1:
                patient = split_username(event['attendees'][1]['email'])
            else:
                patient = 'Open Slot.'
            table.add_row([B+str(nums)+N,event['summary'], start_date, start_time, event['id'], patient])
            nums += 1
        print(table)


def split_username(email):
    """
    
    """
    return email.split(sep='@', maxsplit=1)[0]
    