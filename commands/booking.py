import os, datetime
import sys
from commands import event_listing as listings
USER_PATHS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../'))
sys.path.insert(0, USER_PATHS)
import utilities as utils
        

def get_chosen_slot(events, username, uid):
    '''
    Sorts through list of events on clinic calendar and looks for the specified
    event UID so that it can return event with specified event UID.

            Parameters:
                    events   (list): List of events from clinic calendar
                    username  (str): Patient's (student) username
                    uid       (str): Unique event id of event

            Returns:
                    True  (boolean): Event with specified event UID exists
                    False (boolean): Event with specified event UID does not exist
                    
                    event    (dict): Dictionary with event information
                    *        (dict): Empty dictionary (event was not found)
    '''
    
    for event in events:
        if event['id'] == uid and len(event['attendees']) == 1:
            if "VOLUNTEER: " + str(username) in event['summary']:
                return False, {}
            return True, event
    return False, {}


def make_booking(username, uid, service_student, clinic_service, student_info):
    #TODO: Remove service_student -> not used in function
    '''
    Function will handle the logic for booking an empty slot. Sorts through events occuring in the
    next 7 days to find specified volunteer slot to book. If event is found - the student is added
    as an attendee to volunteered slot.

            Parameters:
                    username       (str): Patient's (student) username
                    uid            (str): Unique event id of event
                    clinic_service (obj): Code clinic's Google calendar API service
                    student_info  (dict): Information on student and given command

            Returns:
                    True       (boolean): Student added as an attendee to specified event (booked slot)
                    False      (boolean): Student not added as an attendee to specified event (slot not booked)
    '''

    now = datetime.datetime.utcnow().isoformat() + 'Z'
    end_date = ((datetime.datetime.utcnow()) + datetime.timedelta(days=7)).isoformat() + 'Z'
    slots = utils.get_events(clinic_service, now, end_date)
    if slots == []:
        utils.print_output('ERROR: This slot is unavailable')
        return False
    available, volunteered_event = get_chosen_slot(slots, username, uid)
    if not available:
        utils.print_output('ERROR: Choose a valid event id.')
        return False
    updated_event, unique_id = create_booking_body(volunteered_event, username, student_info)
    try:
        updated_event_response = clinic_service.events().update(calendarId='primary', eventId=unique_id, body=updated_event).execute()
        booker_accept_invite(clinic_service, unique_id, username, updated_event_response)
        utils.print_output("Booking succesfully made! You're unique id is: "+ str(updated_event_response['id']))
        return True
    except:
        utils.error_handling("ERROR: An error has stopped the booking from being made.\nPlease try again.")


def booker_accept_invite(clinic_service, uid, username, event):
    '''
    Accepts student's invite to event, with specified event UID, and updates 
    event body accordingly.

            Parameters:
                    clinic_service (obj): Code clinic's Google calendar API service
                    uid            (str): Unique event id of event
                    username       (str): Patient's (student) username
                    event         (dict): Event body
    '''

    event['attendees'][1]['responseStatus'] = 'accepted'
    clinic_service.events().update(calendarId='primary', eventId=uid, body=event).execute()


def create_booking_body(event, username, student_info):
    #TODO: Just pass through description not student_info
    '''
    Function will take an event object and sort the relevant data to create a body (for the new booking).
    Student (patient) will be added as an attendee and relevant data will be taken from the event object 
    to update the event body.

            Parameters:
                    event         (dict): Event body
                    username       (str): Patient's (student) username
                    student_info  (dict): Information on student and given command

            Returns:
                    blueprint     (dict): Updated event body
                    event['id']    (str): Unique event of updated event
    '''

    event['attendees'].append({'email': username+'@student.wethinkcode.co.za'})
    event['description'] = student_info['description']

    blueprint = {
            'summary': event['summary'],
            'location': event['location'],
            'start': event['start'],
            'description': event['description'],
            'end': event['end'],
            'attendees':event['attendees'],
            'reminders': {
                'useDefault': True,
            },
     }
    return blueprint, event['id']
  


