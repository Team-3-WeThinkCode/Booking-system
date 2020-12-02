import os
import sys
from commands import event_listing as listings
USER_PATHS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../'))
sys.path.insert(0, USER_PATHS)
import utilities


def get_chosen_slot(events, username, uid):
    """
    Function will sort throught the list of open slots given as PARAM:
    If the event with UID given is valid the function will return true and the event details:
    :RETURN: BOOL(True if event is valid/False if invalid), DICT(Event details)
    """
    if events == []:
        return False, {}
    for event in events:
        if event['id'] == uid and len(event['attendees']) == 2:
            if "VOLUNTEER: " + str(username) in event['summary']:
                return False, {}
            return True, event
    return False, {}



def update_booking_body(event, volunteer):
    """
    Function will take a event object and sort the relevant data to create a body for the new booking.
    User will be added as an attendee and only relevant data will be taken from the event object for body.
    :RETURN: New event body will be returned with updated information.
    """

    blueprint = {
            'summary': event['summary'],
            'location': event['location'],
            'start': event['start'],
            'end': event['end'],
            'attendees':[event['attendees'][1]],
            'reminders': {
                'useDefault': True,
            },
     }
    return blueprint


def cancel_attendee(username, volunteer_service, codeclinic_service, uid):
    deletion = False
    slots, output = listings.list_personal_slots(codeclinic_service, True, True, username)
    deletion, event = get_chosen_slot(slots, username, uid)
    if deletion == True:
        try:
            updated_event = update_booking_body(event, username)
            codeclinic_service.events().update(calendarId='primary', eventId=event['id'], body=updated_event).execute()
        except:
            return "an error occured"
        return "Booking successfully deleted."
    else:
        return "You have no available sessions to cancel."