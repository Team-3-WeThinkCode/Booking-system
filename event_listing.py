from lib.TableIt import tableIt
import datetime


def list_slots(service):
    table = [
        ['Volunteer name.', 'date.', 'time.', 'Unique ID.' ]
    ]
    # Get the UCT time that is current and formats it to allow for google API parameter 
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    # Get the UCT time that is current + 7 days added and formats it to allow for google API parameter 
    end_date = ((datetime.datetime.utcnow()) + datetime.timedelta(days=7)).isoformat() + 'Z'
    print('Displaying all open slots for the next 7 days.')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        timeMax=end_date, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    if not events:
        print('No open slots available.')
    for event in events:
        print(event)
        start = event['start'].get('dateTime', event['start'].get('date'))
        start_date = (start[0:10])
        start_time = (start[11:16])
        table.append([event['summary'], start_date, start_time, event['id']])
        table.append(['------------------------', '------------------------', '-------------------------', '-----------------------'])
    tableIt.printTable(table, useFieldNames=True)
            
