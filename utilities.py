import datetime, json
import pytz
from commands import event_listing as listings
from rich.console import Console

console = Console()


def print_output(output):
    output = output + '\n'
    if 'INVALID' in output:
        console.print(output, style="bold red")
    elif 'ERROR' in output:
        console.print(output, style="bold yellow")
    else:
        console.print(output, style="bold green")


def error_handling(output):
    print_output(output)
    exit()


def date_has_passed(date, time):
    year, month, day = int(date[:4]), int(date[5:7]), int(date[8:])
    hour, minute = int(time[:2]), int(time[3:])
    datetime_now = datetime.datetime.now()
    datetime_given = datetime.datetime(year, month, day, hour, minute, 0)
    if datetime_given < datetime_now:
        return True
    else:
        return False


def check_date_and_time_format(date, time):
    '''
    Checks that date and time input is in correct format
    :return: True if date and time in correct format
    '''

    if date_has_passed(date, time):
        return False
    date_format = "%Y-%m-%d"
    time_format = '%H:%M'
    try:
        datetime.datetime.strptime(date, date_format)
        try:
            datetime.datetime.strptime(time, time_format)
            return True
        except:
            return False
    except ValueError:
        return False


def check_date_format(date):
    date_format = "%Y-%m-%d"
    try:
        datetime.datetime.strptime(date, date_format)
        return True
    except ValueError:
        return False


def check_time_format(time):
    if len(time) < 5 or len(time) > 5:
        return False
    time_format = '%H:%M'
    try:
        datetime.datetime.strptime(time, time_format)
        return True
    except ValueError:
        return False


def get_events(service, start_datetime, end_datetime):
    '''
    Retrieves list of events in specified date/time
    :return: list of events
    '''

    events_result = service.events().list(calendarId='primary',  timeMin=start_datetime, timeMax=end_datetime,
                                               maxResults=500, singleEvents=True,
                                               orderBy='startTime').execute()
    return events_result.get('items', [])


def slot_is_available(service, start_datetime, end_datetime):
    '''
    Checks if there are any events in specified date/time
    :return: True if there are no events
    '''

    events = get_events(service, start_datetime, end_datetime)
    if len(events) > 0:
        return False
    return True

    
def create_makeshift_event(summary, location, description, start_date_time, end_date_time, people):
    '''
    Creates body of event similiar to ones used in the Google Calendar API
    :return: event body
    '''

    blueprint = {
            'summary': summary,
            'location': location,
            'start': {
                'dateTime': start_date_time,
                'timeZone': 'Africa/Johannesburg',
            },
            'end': {
                'dateTime': end_date_time,
                'timeZone': 'Africa/Johannesburg',
            },
            'attendees': people,
            'reminders': {
                'useDefault': True,
            }
    }
    blueprint['description'] = description
    return blueprint
    #return new_event


def add_event_to_calendar(event_info, service, clinic, username):
    '''
    Adds event to calendar
    '''
    people = []
    location = 'WeThinkCode, Victoria & Alfred Waterfront, Cape Town'
    if clinic:
        student_email = str(username) + '@student.wethinkcode.co.za'
        people.append({'email': student_email})
    event = create_makeshift_event(event_info['summary'], location, '', event_info['start_datetime'], event_info['end_datetime'], people)
    event = service.events().insert(calendarId='primary', body=event).execute()
    return event


def delete_event(service, event_id):
    '''
    Cancels event with specified event id
    :return: True if event succesfully cancelled
    '''

    try:
        service.events().delete(calendarId='primary', eventId=event_id, sendUpdates='all').execute()
    except:
        return False
    return True


def convert_date_and_time_to_rfc_format(date, start_time, end_time):
    '''
    Converts date/time into rfc format
    Date in format (yyyy-mm-dd)
    Time in format (hh:mm)
    :return: start, and end, date/time in rfc format
    '''
    
    year, month, day = int(date[:4]), int(date[5:7]), int(date[8:])
    start_hr, start_min = int(start_time[:2]), int(start_time[3:])
    end_hr, end_min = int(end_time[:2]), int(end_time[3:])
    tz = pytz.timezone('Africa/Johannesburg')
    start_datetime = tz.localize(datetime.datetime(year, month, day, start_hr, start_min))
    end_datetime = tz.localize(datetime.datetime(year, month, day, end_hr, end_min))
    return start_datetime.isoformat(), end_datetime.isoformat()


def update_files(student_service, codeclinic_service, username):
    '''
    Function will update the json file .student_events.json with the new events data for the students events involving Code Clinic.
    Function will update the json file .open_slots.json with the open slots data from the Code Clinic calendar.
    '''
    try:
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        end_date = ((datetime.datetime.utcnow()) + datetime.timedelta(days=7)).isoformat() + 'Z'
        events = get_events(codeclinic_service, now, end_date)
        personal_data = sort_booked_slots(events, username)
        code_clinic_data = sort_open_slots(events, username)

        personal_data, code_clinic_data = event_data_compactor(personal_data), event_data_compactor(code_clinic_data)

        store_slot_data(personal_data, True)
        store_slot_data(code_clinic_data, False)
    except:
        error_handling('ERROR: Event files could not be updated.')       



def event_data_compactor(events):
    """
    Function will take a event object and sort the relevant data to create a body for the new booking.
    User will be added as an attendee and only relevant data will be taken from the event object for body.
    :RETURN: New event body will be returned with updated information.
    """
    new_data_list = []
    for event in events:
        new_event = {
                'id': event['id'],
                'summary': event['summary'],
                'location': event['location'],
                'start': event['start'],
                'end': event['end'],
                'organizer': event['organizer'],
                'attendees':event['attendees'],
                'reminders': {
                    'useDefault': True,
                },
        }
        new_data_list.append(new_event)
    return new_data_list


def volunteer_accept_invite(service_clinic, unique_id, username, event):
    '''
    Accepts invite for student who books volunteered slot.
    '''

    event['attendees'][0]['responseStatus'] = 'accepted'
    service_clinic.events().update(calendarId='primary', eventId=unique_id, body=event).execute()


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

    
def split_username(email):
    """
    Function will split the users email address to grab the username before the 
    @ symbol.
    """
    return email.split(sep='@', maxsplit=1)[0]