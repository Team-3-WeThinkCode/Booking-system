import datetime
import event_listing as listings


def check_date_and_time_format(date, time):
    '''
    Checks that date and time input is in correct format
    :return: True if date and time in correct format
    '''

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
    

# def list_slots(service):
#     '''
    
#     '''

#     # Get the UCT time that is current and formats it to allow for google API parameter 
#     now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
#     # Get the UCT time that is current + 7 days added and formats it to allow for google API parameter 
#     end_date = ((datetime.datetime.utcnow()) + datetime.timedelta(days=7)).isoformat() + 'Z'
#     print('Displaying all open slots for the next 7 days.')
#     events_result = service.events().list(calendarId='primary', timeMin=now,
#                                         timeMax=end_date, singleEvents=True,
#                                         orderBy='startTime').execute()
#     events = events_result.get('items', [])
#     print('<' +'-'*80+'>\n')
#     if not events:
#         print('No open slots available.')
#     for event in events:
#         start = event['start'].get('dateTime', event['start'].get('date'))
#         print(event['summary'], start, event['id'])
#         print('<' +'-'*80+'>\n')


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
            'attendees':people,
            'reminders': {
                'useDefault': True,
            },
     }
    return new_event


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


def is_leap_year(year):
    ''' 
    Checks if specified year is a leap year
    :return: True if the year is a leap year
    '''

    if (year % 4) == 0:  
        if (year % 100) == 0:  
            if (year % 400) == 0:  
                return True  
            else:  
                return False 
        else:  
            return True 
    else:  
        return False 


def date_fomat_correct(date):
    '''
    Checks that date is in format yyyy-mm-dd
    :return: True if date is in correct format
    '''

    try:
        year, month, day = int(date[:4]), int(date[5:7]), int(date[8:])
    except:
        return False
    if year > 2021:
        return False
    elif day < 1:
        return False
    elif month == 4 or month == 6 or month == 9:
        if day > 31:
            return False
    elif is_leap_year(year) and month == 2:
        if day > 29:
            return False
    else:
        if day > 30:
            return False
    return True


def get_date():
    '''
    Get date from user
    :return: date (in correct format)
    '''

    date = str(input('Insert date in format (yyyy-mm-dd): '))
    while not date_fomat_correct(date):
        print('Please enter a valid date!')
        date = str(input('Insert date in format (yyyy-mm-dd): '))
    return date


def convert_date_and_time_to_rfc_format(date, start_time, end_time):
    '''
    Converts date/time into rfc format
    Date in format (yyyy-mm-dd)
    Time in format (hh:mm)
    :return: start, and end, date/time in rfc format
    '''

    year, month, day = date[:4], date[5:7], date[8:]
    start_hour, start_minute = start_time[:2], start_time[3:]
    end_hour, end_minute = end_time[:2], end_time[3:]
    start_dateTime = year+'-'+month+'-'+day+'T'+start_hour+':'+start_minute+':00'+'+02:00'
    end_dateTime = year+'-'+month+'-'+day+'T'+end_hour+':'+end_minute+':00'+'+02:00'
    return start_dateTime, end_dateTime


def update_files(service1, service2, username):
    '''
    Function will update the json file .student_events.json with the new events data for the students events involving Code Clinic.
    Function will update the json file .open_slots.json with the open slots data from the Code Clinic calendar.
    '''
    listings.list_personal_slots(service1, True, True, username)
    listings.list_personal_slots(service2, True, False, username)



def volunteer_accept_invite(service_clinic, unique_id, username, event):
    '''

    '''

    event['attendees'][0]['responseStatus'] = 'accepted'
    service_clinic.events().update(calendarId='primary', eventId=unique_id, body=event).execute()