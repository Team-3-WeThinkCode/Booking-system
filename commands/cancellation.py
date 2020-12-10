import os, datetime
import sys
from commands import event_listing as listings
USER_PATHS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../'))
sys.path.insert(0, USER_PATHS)
import utilities
import gmail_api as email


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


def cancel_attendee(username, clinic, uid):
    '''
    Cancels booking slot by using the unique event ID and removing student as an attendee to the event. 
    If event cannot be cancelled, then the program outputs an error message with the reason for failure.

            Parameters:
                    username       (str): Patient's (student) username
                    clinic_service (obj): Code clinic's Google calendar API service
                    uid            (str): Unique event id of event

            Returns:
                    True       (boolean): Student removed as an attendee from event (cancelled booked slot)
                    False      (boolean): Student not removed as an attendee from event (events left unchanged)
    '''

    now = datetime.datetime.utcnow().isoformat() + 'Z'
    end_date = ((datetime.datetime.utcnow()) + datetime.timedelta(days=7)).isoformat() + 'Z'
    deletion = False
    slots = utilities.get_events(clinic.service,now, end_date)
    deletion, event = utilities.get_chosen_slot(slots, username, uid)
    if not is_user_valid(event, username):
        utilities.print_output("ERROR: You cannot cancel another users booking")
        return False
    if deletion == True:
        try:
            updated_event = update_booking_body(event, username)
            event = clinic.service.events().update(calendarId='primary', eventId=event['id'], body=updated_event).execute()
            email.send_message('me', email.patient_cancel_text(username, event), clinic.email_service)
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