from utils.TableIt import TableIt as tabulate
import datetime
import json


def list_slots(service, fetch, user):
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
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        timeMax=end_date, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    if user == False:
        events = sort_open_slots(events)
    if fetch == False:
        print_slots_table(events)
    store_slot_data(events, user)
    return events


def sort_open_slots(events):
    new_events = []
    for event in events:
        if not len(event['attendees']) > 1:
            new_events.append(event)
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
            new_data['events'].append({event['id'] : event})
        with open('data_files/.student_events.json', 'w') as f:
            json.dump(new_data, f, sort_keys=True, indent=4)


def print_slots_table(events):
    """
    Uses the TableIt module to display data of open slots to the user in tabular form.
    Event name, time, date, id will be sliced from the events objects given and used to display in the table.
    """
    table = [
        ['#.', 'Volunteer name.', 'date.', 'time.', 'Unique ID.']
    ]
    nums = 1
    if not events:
        print('No open slots available.')
    elif events:
        print('Displaying all open slots for the next 7 days.')

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        start_date = (start[0:10])
        start_time = (start[11:16]+' - '+end[11:16])
        table.append(['', '-------------------------', '-------------------------', '-------------------------', '-------------------------'])
        table.append([nums, event['summary'], start_date, start_time, event['id']])
        nums += 1
    tabulate.printTable(table, useFieldNames=True, color=(255, 0, 255))


def create_event_body(event):
    blueprint = {
            'summary': event['summary'],
            'location': event['location'],
            'start': event['start'],
            'end': event['end'],
            'attendees':event['attendees'],
            'reminders': {
                'useDefault': True,
            },
     }
    print(blueprint)
            
