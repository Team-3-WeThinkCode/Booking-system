import json
import datetime

def get_user_input():
    while True:
        command = input('Please choose an option from the list:\n1) Create calendar event\n2) Delete calendar event\n3) List calendar events\n')
        if command.isdigit():
            if int(command) >= 1 and int(command) <= 3:
                return int(command)


def create_delete_calendar(service):
    """
    Contacts the google api after an instance is created.
    uses the insert method to create a new calendar.
    uses the Summary as the name of the calendar.
    the delete method will delete a calendar of the given ID as a parameter.
    """

    requests_body = {
        "summary": "Code Clinics"
    }
    user_input = input("To create a calendar event")

    if user_input == "create":
        response = service.calendars().insert(body=requests_body).execute()
        print(response)

    elif user_input == "delete":
        service.calendars().delete(calendarId='c_inb60ai7mdqjrefd2rm3bue4eo@group.calendar.google.com').execute()


def get_event_date_and_time_input():
    '''
    :return: start dateTime and end dateTime (30min events) in rfc format
    '''

    date = input('Insert start date of event in format (yyyy-mm-dd): ')
    time = input('Insert start time of event in format (hh:mm): ')
    year, month, day = date[:4], date[5:7], date[8:]
    hour, minute = time[:2], time[3:]
    end_minute = '00'
    if minute[0] == '0':
        end_minute = '30'
    start_dateTime = year+'-'+month+'-'+day+'T'+hour+':'+minute+':00'+'+02:00'
    end_dateTime = year+'-'+month+'-'+day+'T'+hour+':'+end_minute+':00'+'+02:00'
    return start_dateTime, end_dateTime


def create_booking(username, service):
    start_dateTime, end_dateTime = get_event_date_and_time_input()
    if not already_exists(create_makeshift_event('', '', '', start_dateTime, end_dateTime), service):
        summary = 'Code Clinic - ' + str(username)
        location = 'WeThinkCode, Victoria & Alfred Waterfront, Cape Town'
        description = str(input("Session topic?: "))
        add_people = True
        people = []
        while add_people:
            user_input = str(input("Add atendee via email? "))
            if user_input != 'no':
                people.append({'email': user_input})
                print(people)
            else:
                break
        event = create_makeshift_event(summary, location, description, start_dateTime, end_dateTime)
        event = service.events().insert(calendarId='primary', body=event).execute()
        with open('data_files/data.json', 'a+') as outfile:
            json.dump(event, outfile, sort_keys=True, indent=4)
    else:
        print('Sorry, slot is already booked. Choose another slot.')

#?
def delete_event(service):  
    with open('data_files/data.json', 'r+') as json_file:
        data = json.load(json_file)
    print(data)
    for item in data:
        service.events().delete(calendarId='primary', eventId=item['id'], sendUpdates='all').execute()
    print(data['id'] + ' deleted succesfully')
    update = None
    with open('data_files/data.json', 'w') as outfile:
        json.dump(update, outfile, sort_keys=True, indent=4)
    json_file.close()
    outfile.close()
    

def list_events(service):
    page_token = None
    while True:
        events = service.events().list(calendarId='primary', pageToken=page_token).execute()
        for event in events['items']:
            with open('data_files/events.json', 'a+') as json_file:
                json.dump(event, json_file, sort_keys=True, indent=4)
            json_file.close()
        page_token = events.get('nextPageToken')
        if not page_token:
            break


def get_events(service):
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                               maxResults=500, singleEvents=True,
                                               orderBy='startTime').execute()
    return events_result.get('items', [])


def get_date_events(date, events):
    lst = []
    date = date
    for event in events:
        if event.get('start').get('dateTime'):
            d1 = event['start']['dateTime']
            if d1 == date:
                lst.append(event)
    return lst


def create_makeshift_event(summary, location, description, start_date_time, end_date_time):
    new_event = {
            'summary': summary,
            'location': location,
            'description': description,
            'start': {
                'dateTime': start_date_time,
                'timeZone': 'Africa/Johannesburg',
            },
            'end': {
                'dateTime': end_date_time,
                'timeZone': 'Africa/Johannesburg',
            },
            'reminders': {
                'useDefault': True,
            },
     }
    return new_event


def already_exists(new_event, service):
    events = get_date_events(new_event['start']['dateTime'],get_events(service))
    print(events)
    event_list = [new_event['start']['dateTime'] for new_event in events]
    if new_event['start']['dateTime'] not in event_list:
        return False
    else:
        return True
