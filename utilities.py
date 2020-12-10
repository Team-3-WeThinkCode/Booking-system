import datetime, json
import pytz
from commands import event_listing as listings
from rich.console import Console

console = Console()


def print_output(output):
    '''
    Prints output in bold colour. The following colours are used:
    - Red: If the given string has the word 'INVALID' in.
    - Yellow: If the given string has the word 'ERROR' in.
    - Green: If the string has neither 'INVALID' nor 'ERROR' in.

            Parameters:
                    output  (str): Sentence to be printed to the 
                                   terminal as output
    '''

    output = output + '\n'
    if 'INVALID' in output:
        console.print(output, style="bold red")
    elif 'ERROR' in output:
        console.print(output, style="bold yellow")
    else:
        console.print(output, style="bold green")


def error_handling(output):
    '''
    Prints output in bold colour using the print_output function and 
    then exits the program.

            Parameters:
                    output  (str): Sentence to be printed to the 
                                   terminal as output
    '''

    print_output(output)
    exit()


def date_has_passed(date, time):
    '''
    Sorts through list of events on clinic calendar and looks for the specified
    event UID so that it can return event with specified event UID.

            Parameters:
                    date      (str): Date in format <yyyy-mm-dd>
                    time      (str): Time in format <hh:mm>

            Returns:
                    True  (boolean): Date has already passed
                    False (boolean): Date has not passed yet
    '''

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
    Checks that the specified date and time is in the correct format
    and that it has not passed. Date's correct format is <yyyy-mm-dd>.
    Time's correct format is <hh:mm>.

            Parameters:
                    date      (str): Date input by user
                    time      (str): Time input by user

            Returns:
                    True  (boolean): Date and time format is correct
                                     and has not passed yet.
                    False (boolean): Date and time format is incorrect
                                     or has passed already.
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
    '''
    Checks that the specified date is in the correct format. 
    Date's correct format is <yyyy-mm-dd>.

            Parameters:
                    date      (str): Date input by user

            Returns:
                    True  (boolean): Date format is correct
                    False (boolean): Date format is incorrect
    '''

    date_format = "%Y-%m-%d"
    try:
        datetime.datetime.strptime(date, date_format)
        return True
    except ValueError:
        return False


def check_time_format(time):
    '''
    Checks that the specified time is in the correct format. 
    Time's correct format is <hh:mm>.

            Parameters:
                    time      (str): Time input by user

            Returns:
                    True  (boolean): Time format is correct
                    False (boolean): Time format is incorrect
    '''

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
    Returns all events occuring from the start_datetime to the end_datetime in
    the service's Google calendar. The events information is stored in a list
    of dictionaries.

            Parameters:
                    service                (obj): Google calendar API service
                    start_datetime         (str): Datetime (in rfc format) of start time
                    end_datetime           (str): Datetime (in rfc format) of end time

            Returns:
                    events_result (list of dict): Events occuring in specified date/time
    '''

    events_result = service.events().list(calendarId='primary',  timeMin=start_datetime, timeMax=end_datetime,
                                               maxResults=500, singleEvents=True,
                                               orderBy='startTime').execute()
    return events_result.get('items', [])


def slot_is_available(service, start_datetime, end_datetime):
    #TODO change name of function to something more descriptive
    '''
    Confirms whether service's Google calendar has any events occuring in the 
    duration of specified datetimes.

            Parameters:
                    service         (obj): Google calendar API service
                    start_datetime  (str): Datetime (in rfc format) of start time
                    end_datetime    (str): Datetime (in rfc format) of end time

            Returns:
                    True        (boolean): No events are occuring in the duration of
                                           specified datetimes
                    False       (boolean): Events are occuring in the duration of the 
                                           specified datetimes
    '''

    events = get_events(service, start_datetime, end_datetime)
    if len(events) > 0:
        return False
    return True

    
def create_makeshift_event(summary, location, description, start_datetime, end_datetime, people):
    #TODO: Another duplicate of this function?
    '''
    Creates body of event similiar to ones used in the Google Calendar API.

            Parameters:
                    summary        (str): Heading of the event
                    location       (str): Location of the event
                    description    (str): Description of the event
                    start_datetime (str): Start date/time of the event
                    end_datetime   (str): End date/time of the event
                    people        (list): Attendees to the event

            Returns:
                    blueprint     (dict): Event body similiar to the Google
                                          Calendar API event body.
    '''

    blueprint = {
            'summary': summary,
            'location': location,
            'start': {
                'dateTime': start_datetime,
                'timeZone': 'Africa/Johannesburg',
            },
            'end': {
                'dateTime': end_datetime,
                'timeZone': 'Africa/Johannesburg',
            },
            'attendees': people,
            'reminders': {
                'useDefault': True,
            }
    }
    blueprint['description'] = description
    return blueprint


def add_event_to_calendar(event_info, service, clinic, username):
    '''
    Creates event in service's Google Calendar calendar.

            Parameters:
                    event_info  (dict): Event body
                    service      (obj): Google Calendar API service
                    clinic       (obj): Object with information on Code clinic
                    username     (str): Student's username

            Returns:
                    event        (obj): Event created
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
    Removes event, with specified event UID, from service's Google Calendar
    calendar.

            Parameters:
                    service      (obj): Google Calendar API service
                    event_id     (str): Unique event id of event

            Returns:
                    True     (boolean): Event was removed from calendar
                    False    (boolean): Event could not be removed from calendar
    '''

    try:
        service.events().delete(calendarId='primary', eventId=event_id, sendUpdates='all').execute()
    except:
        return False
    return True


def convert_date_and_time_to_rfc_format(date, start_time, end_time):
    '''
    Converts date (yyyy-mm-dd) and time (hh:mm) to rfc format.

            Parameters:
                    date        (str): Date in format <yyyy-mm-dd>
                    start_time  (str): Start time of slot in format <hh:mm>
                    end_time    (str): End time of slot in format <hh:mm>

            Returns:
                    start_datetime  (str): Start date/time in rfc format
                    end_datetime    (str): End date/time in rfc format
    '''
    
    year, month, day = int(date[:4]), int(date[5:7]), int(date[8:])
    start_hr, start_min = int(start_time[:2]), int(start_time[3:])
    end_hr, end_min = int(end_time[:2]), int(end_time[3:])
    tz = pytz.timezone('Africa/Johannesburg')
    start_datetime = tz.localize(datetime.datetime(year, month, day, start_hr, start_min))
    end_datetime = tz.localize(datetime.datetime(year, month, day, end_hr, end_min))
    return start_datetime.isoformat(), end_datetime.isoformat()


def update_files(student_service, clinic_service, username):
    '''
    Json data files updated:
    - ".student_events.json" updated with the new events data for the students events involving Code Clinic.
    - ".open_slots.json" updated with the open slots data from the Code Clinic calendar.

            Parameters:
                    student_service  (obj): Student's Google Calendar API service
                    clinic_service   (obj): Code clinic's Google Calendar API service
                    username         (str): Student's username
    '''

    try:
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        end_date = ((datetime.datetime.utcnow()) + datetime.timedelta(days=7)).isoformat() + 'Z'
        events = get_events(clinic_service, now, end_date)
        personal_data = sort_booked_slots(events, username)
        code_clinic_data = sort_open_slots(events, username)

        personal_data, code_clinic_data = event_data_compactor(personal_data), event_data_compactor(code_clinic_data)
        store_slot_data(personal_data, True)
        store_slot_data(code_clinic_data, False)
    except:
        error_handling('ERROR: Event files could not be updated.')       



def event_data_compactor(events):
    '''
    Function will take a event object and sort the relevant data to create a body for the new booking.
    User will be added as an attendee and only relevant data will be taken from the event object for body.

            Parameters:
                    events        (list of dict): Events occuring in calendar

            Returns:
                    new_data_list (list of dict): Events occuring in calendar with customised event body
                                                  for each event
    '''

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


def volunteer_accept_invite(clinic_service, unique_id, username, event):
    '''
    Makes user, with specified username, an attendee to the event, with specified event UID,
    by accepting attendee invite on user's behalf.

            Parameters:
                    clinic_service (obj): Code clinic's Google Calendar API service
                    unique_id      (str): Unique event id of event
                    username       (str): Student's username
                    event         (dict): Event body of event with specified event UID
    '''

    event['attendees'][0]['responseStatus'] = 'accepted'
    clinic_service.events().update(calendarId='primary', eventId=unique_id, body=event).execute()


def sort_open_slots(events, username):
    '''
    Sorts through a list of events to locate volunteered events that don't have a patient 
    attending (not booked) and adds these events' bodies to a list. Slots volunteered by
    student, specified by username, are not added to the list.

            Parameters:
                    events    (list of dict): List of events from calendar
                    username           (str): Student's username

            Returns:
                    new_events (list of dict): Volunteered events that are not booked
    '''
 
    new_events = []
    for event in events:
        try:
            if len(event['attendees']) == 1 and event['attendees'][0]['email'] != username+"@student.wethinkcode.co.za":
                new_events.append(event)
        except:
            continue
    return new_events


def sort_booked_slots(events, username):
    '''
    Sorts through a list of events to locate events that the student, specified by username,
    either volunteered or booked. This is done by locating the student's email in the list
    of event attendees in the event body. These events are added to a list and returned.

            Parameters:
                    events    (list of dict): List of events from calendar
                    username           (str): Student's username

            Returns:
                    new_events (list of dict): Events volunteered or booked by user with
                                               specified username
    '''

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
    '''
    Populates a json file with the details of each open slot recieved from Google 
    Calendar API. Old data will be deleted from the json file and new data written
    to the json file, to prevent overpopulating the file.

            Parameters:
                    events    (list of dict): List of events from calendar

                    user           (boolean): True if events should be added
                                              to the ".student_events.json" file.

                                              False if events should be added
                                              to the ".open_slots.json" file.
    '''

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
    '''
    Function will split the users email address to grab the username before the 
    @ symbol.

            Parameters:
                    email  (str): Email address

            Returns:
                    *      (str): Username derived from email address                
    '''

    return email.split(sep='@', maxsplit=1)[0]