import os, sys, datetime
USER_PATHS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../'))
sys.path.insert(0, USER_PATHS)
import API.gmail_api as email
from utilities import utilities as utils
        

def get_chosen_slot(events, username, uid, student_service):
    '''
    Sorts through list of events on clinic calendar and looks for the specified
    event UID. If the student has an available slot in their calendar at the 
    time of the event, with the specified event ID, the event body is returned.

            Parameters:
                    events         (list): List of events from clinic calendar
                    username        (str): Patient's (student) username
                    uid             (str): Unique event id of event
                    student_service (obj): Student's (patient) Google Calendar
                                           API service

            Returns:
                    True  (boolean): Event with specified event UID exists
                    False (boolean): Event with specified event UID does not
                                     exist
                    
                    event    (dict): Dictionary with event information
                    *        (dict): Empty dictionary (event was not found)
    '''
    
    for event in events:
        if event['id'] == uid and len(event['attendees']) == 1:
            start = event['start'].get('dateTime')
            end = event['end'].get('dateTime')
            if "VOLUNTEER: " + str(username) in event['summary']:
                return False, {}
            if not utils.is_slot_available(student_service, username, start, end):
                return False, {}
            return True, event
    return False, {}


def make_booking(username, uid, clinic, student_info, student_service):
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
    end_date = ((datetime.datetime.utcnow())\
        + datetime.timedelta(days=7)).isoformat() + 'Z'
    slots = utils.get_events(clinic.service, now, end_date)
    if slots == []:
        utils.print_output('ERROR: This slot is unavailable')
        return False
    available, volunteered_event = get_chosen_slot(slots,
                                                   username,
                                                   uid,
                                                   student_service)
    if not available:
        utils.print_output('ERROR: Choose a valid event id.')
        return False
    updated_event, unique_id = create_booking_body(volunteered_event,
                                                   username,
                                                   student_info['description'])
    try:
        updated_response = clinic.service.events()\
                                    .update(calendarId='primary',
                                            eventId=unique_id,
                                            body=updated_event).execute()

        booker_accept_invite(clinic.service, unique_id, updated_response)
        email.send_message('me', email.patient_create_text(username,
                                                           updated_response),
                                                           clinic.email_service)
        utils.print_output("Booking succesfully made! You're unique id is: "\
                                                + str(updated_response['id']))
        return True
    except:
        error_msg = 'ERROR: An error has stopped the booking from being made.\n'\
                                                        +'Please try again.'
        utils.error_handling(error_msg)


def booker_accept_invite(service, uid, event):
    '''
    Accepts student's invite to event, with specified event UID, and updates 
    event body accordingly.

            Parameters:
                    service (obj): Code clinic's Google calendar API service
                    uid            (str): Unique event id of event
                    event         (dict): Event body
    '''

    event['attendees'][1]['responseStatus'] = 'accepted'
    service.events().update(calendarId='primary', eventId=uid, body=event)\
                                                                .execute()


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

    msg = ''
    now = datetime.datetime.utcnow().isoformat()+'Z'
    end_date = ((datetime.datetime.utcnow())\
                    + datetime.timedelta(days=7)).isoformat()+'Z'
    deletion = False
    slots = utils.get_events(clinic.service,now, end_date)
    deletion, event = utils.get_chosen_slot(slots, username, uid)
    if not is_user_valid(event, username):
        msg = "ERROR: You cannot cancel another users booking"
        utils.print_output(msg)
        return False
    if deletion == True:
        try:
            updated_event = update_booking_body(event, username)
            event = clinic.service.events().update(calendarId='primary',\
                         eventId=event['id'], body=updated_event).execute()
            email.send_message('me', email.patient_cancel_text(username,event),\
                                                          clinic.email_service)
        except:
            msg = "ERROR: Could not cancel booking."
            utils.error_handling(msg)
        msg = "Booking successfully deleted."
        utils.print_output(msg)
        return True
    else:
        msg = 'ERROR: You cannot cancel selected booking.\n'\
                            +'Use the help command (-h) for more infromation.'
        utils.print_output(msg)
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
