import os, datetime
import sys
from commands import event_listing as listings
USER_PATHS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../'))
sys.path.insert(0, USER_PATHS)
import utilities


def get_chosen_slot(events, username, uid):
    #TODO: Add to utils -> used in create booking and cancel booking
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

    if events == []:
        return False, {}
    for event in events:
        if event['id'] == uid and len(event['attendees']) == 2:
            if "VOLUNTEER: " + str(username) in event['summary']:
                return False, {}
            return True, event
    return False, {}


def update_booking_body(event, volunteer):
    '''
    Function will take an event object and sort the relevant data to create a body (for open booking).
    Student (patient) will be added as an attendee and relevant data will be taken from the event object 
    to update the event body.

            Parameters:
                    event         (dict): Event body
                    username       (str): Patient's (student) username

            Returns:
                    blueprint     (dict): Updated event body
    '''

    blueprint = {
            'summary': event['summary'],
            'location': event['location'],
            'start': event['start'],
            'end': event['end'],
            'attendees':[event['attendees'][0]],
            'reminders': {
                'useDefault': True,
            },
     }
    return blueprint


def cancel_attendee(username, volunteer_service, clinic_service, uid):
    #TODO: Remove volunteer service as param -> not being used
    '''
    Cancels booking slot by using the unique event ID and removing student as an attendee to the event. 
    If event cannot be cancelled, then the program outputs an error message with the reason for failure.

            Parameters:
                    username       (str): Patient's (student) username
                    clinic_service (obj): Code clinic's service
                    uid            (str): Unique event id of event

            Returns:
                    True       (boolean): Student removed as an attendee from event (cancelled booked slot)
                    False      (boolean): Student not removed as an attendee from event (events left unchanged)
    '''

    now = datetime.datetime.utcnow().isoformat() + 'Z'
    end_date = ((datetime.datetime.utcnow()) + datetime.timedelta(days=7)).isoformat() + 'Z'
    deletion = False
    slots = utilities.get_events(clinic_service,now, end_date)
    deletion, event = get_chosen_slot(slots, username, uid)
    if not is_user_valid(event, username):
        utilities.print_output("ERROR: You cannot cancel another users booking")
        return False
    if deletion == True:
        try:
            updated_event = update_booking_body(event, username)
            clinic_service.events().update(calendarId='primary', eventId=event['id'], body=updated_event).execute()
        except:
            utilities.error_handling("ERROR: Could not cancel booking.")
        utilities.print_output("Booking successfully deleted.")
        return True
    else:
        utilities.print_output("ERROR: You cannot cancel selected booking.\nUse the help command (-h) for more infromation.")
        return False


def is_user_valid(event, username):
    '''
    Checks if user has booked specified event by checking if the user's username is listed in
    the list of attendees in the event body.

            Parameters:
                    event         (dict): Event body
                    username       (str): Patient's (student) username

            Returns:
                    True       (boolean): Student is listed as an attendee to specified event
                    False      (boolean): Student is not listed as an attendee to specified event
    '''

    if utilities.split_username(event['attendees'][1]['email']) == username:
        return True
    else:
        return False