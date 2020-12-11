import os, sys, datetime
from commands import event_listing as listings
USER_PATHS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../'))
sys.path.insert(0, USER_PATHS)
import API.gmail_api as email
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
                    False (boolean): Event with specified event UID does not
                                     exist
                    
                    event    (dict): Dictionary with event information
                    *        (dict): Empty dictionary (event was not found)
    '''
    
    for event in events:
        if event['id'] == uid and len(event['attendees']) == 1:
            if "VOLUNTEER: " + str(username) in event['summary']:
                return False, {}
            return True, event
    return False, {}


def make_booking(username, uid, clinic, student_info):
    '''
    Function will handle the logic for booking an empty slot. Sorts through
    events occuring in the next 7 days to find specified volunteer slot to
    book. If event is found - the student is added
    as an attendee to volunteered slot.

            Parameters:
                    username       (str): Patient's (student) username
                    uid            (str): Unique event id of event
                    clinic.service (obj): Code clinic's Google calendar API
                                          service
                    student_info  (dict): Information on student and given
                                          command

            Returns:
                    True       (boolean): Student added as an attendee to
                                          specified event (booked slot)
                    False      (boolean): Student not added as an attendee
                                          to specified event (slot not booked)
    '''

    now = datetime.datetime.utcnow().isoformat() + 'Z'
    end_date = ((datetime.datetime.utcnow()) + datetime.timedelta(days=7)).isoformat() + 'Z'
    slots = utils.get_events(clinic.service, now, end_date)
    if slots == []:
        utils.print_output('ERROR: This slot is unavailable')
        return False
    available, volunteered_event = get_chosen_slot(slots, username, uid)
    if not available:
        utils.print_output('ERROR: Choose a valid event id.')
        return False
    updated_event, unique_id = create_booking_body(volunteered_event, username, student_info['description'])
    try:
        updated_event_response = clinic.service.events().update(calendarId='primary',eventId=unique_id, body=updated_event).execute()

        booker_accept_invite(clinic.service, unique_id, username, updated_event_response)
        email.send_message('me', email.patient_create_text(username, updated_event_response), clinic.email_service)
        utils.print_output("Booking succesfully made! You're unique id is: "+ str(updated_event_response['id']))
        return True
    except:
        error_message = 'ERROR: An error has stopped the booking from being made.\nPlease try again.'
        utils.error_handling(error_message)


def booker_accept_invite(service, uid, username, event):
    '''
    Accepts student's invite to event, with specified event UID, and updates 
    event body accordingly.

            Parameters:
                    service (obj): Code clinic's Google calendar API service
                    uid            (str): Unique event id of event
                    username       (str): Patient's (student) username
                    event         (dict): Event body
    '''

    event['attendees'][1]['responseStatus'] = 'accepted'
    service.events().update(calendarId='primary', eventId=uid, body=event).execute()


def create_booking_body(event, username, description="General code"):
    '''
    Function will take an event object and sort the relevant data to create a
    body (for the new booking). Student (patient) will be added as an attendee
    and relevant data will be taken from the event object to update the event
    body.

            Parameters:
                    event         (dict): Event body
                    username       (str): Patient's (student) username
                    description  (str): Information on topic

            Returns:
                    blueprint     (dict): Updated event body
                    event['id']    (str): Unique event of updated event
    '''

    event['attendees'].append({'email': username+'@student.wethinkcode.co.za'})
    blueprint = {
            'summary': event['summary'],
            'location': event['location'],
            'start': event['start'],
            'description': description,
            'end': event['end'],
            'attendees':event['attendees'],
            'reminders': {
                'useDefault': True,
            },
     }
    return blueprint, event['id']
  

def update_booking_body(event, volunteer):
    '''
    Function will take an event object and sort the relevant data to create a
    body (for open booking). Student (patient) will be added as an attendee
    and relevant data will be taken from the event object to update the event
    body.

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


def cancel_attendee(username, clinic, uid):
    '''
    Cancels booking slot by using the unique event ID and removing student as
    an attendee to the event. If event cannot be cancelled, then the program
    outputs an error message with the reason for failure.

            Parameters:
                    username       (str): Patient's (student) username
                    clinic_service (obj): Code clinic's Google calendar API
                                          service
                    uid            (str): Unique event id of event

            Returns:
                    True       (boolean): Student removed as an attendee from
                                          event (cancelled booked slot)
                    False      (boolean): Student not removed as an attendee
                                          from event (events left unchanged)
    '''

    now = datetime.datetime.utcnow().isoformat()+'Z'
    end_date = ((datetime.datetime.utcnow()) + datetime.timedelta(days=7)).isoformat()+'Z'
    deletion = False
    slots = utils.get_events(clinic.service,now, end_date)
    deletion, event = utils.get_chosen_slot(slots, username, uid)
    if not is_user_valid(event, username):
        utils.print_output("ERROR: You cannot cancel another users booking")
        return False
    if deletion == True:
        try:
            updated_event = update_booking_body(event, username)
            event = clinic.service.events().update(calendarId='primary', eventId=event['id'], body=updated_event).execute()
            email.send_message('me', email.patient_cancel_text(username,event), clinic.email_service)
        except:
            utils.error_handling("ERROR: Could not cancel booking.")
        utils.print_output("Booking successfully deleted.")
        return True
    else:
        utils.print_output('ERROR: You cannot cancel selected booking.\nUse the help command (-h) for more infromation.')
        return False


def is_user_valid(event, username):
    '''
    Checks if user has booked specified event by checking if the user's
    username is listed in the list of attendees in the event body.

            Parameters:
                    event         (dict): Event body
                    username       (str): Patient's (student) username

            Returns:
                    True       (boolean): Student is listed as an attendee
                                          to specified event
                    False      (boolean): Student is not listed as an 
                                          attendee to specified event
    '''

    if utils.split_username(event['attendees'][1]['email']) == username:
        return True
    else:
        return False
