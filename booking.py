import utilities as utils
import quickstart
import datetime


def convert_hour_and_minute_to_time_format(hour, minute):
    str_hour = str(hour)
    str_minute = str(minute)
    if len(str_hour) > 2 or len(str_minute) > 2:
        return '', ''
    if len(str_hour) == 1:
        str_hour = '0' + str_hour
    if len(str_minute) == 1:
        str_minute = '0' + str_minute
    return str_hour, str_minute


def get_30_minute_booking_slot_times():
    times, slots = [], []
    hour, minute = 8, 30
    count = 0
    while hour < 18:
        str_hour, str_minute = convert_hour_and_minute_to_time_format(hour, minute)
        times.append(str_hour +':'+str_minute)
        if count < 2:
            slots.append((times[len(times)-2], times[len(times)-1]))
            count = 0
        if minute == 0:
            minute = 30
        elif minute == 30:
            minute = 0
            hour += 1
        count += 1
    return slots


def list_slots(service, fetch):
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
    events = sort_open_slots(events)
    if fetch == False:
        print_slots_table(events)
    #store_slot_data(events)
    return events


def sort_open_slots(events):
    new_events = []
    for event in events:
        try: 
            if not len(event['attendees']) > 1:
                new_events.append(event)
        except:
            'NO EVENTS'
    return new_events


def get_open_slots_of_the_day(clinic_service):
    slots = get_30_minute_booking_slot_times()
    open_slots = []
    events = list_slots(clinic_service, True)
    print(sort_open_slots(events))


def make_booking():
    #slot available - volunteered
    #describe what help nee
    pass


if __name__ == "__main__":
    service = quickstart.create_service('cprinsloo')
    get_open_slots_of_the_day(service)