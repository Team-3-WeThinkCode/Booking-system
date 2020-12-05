import os, datetime
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
            'attendees':[event['attendees'][0]],
            'reminders': {
                'useDefault': True,
            },
     }
    return blueprint


def cancel_attendee(username, volunteer_service, codeclinic_service, uid):
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    end_date = ((datetime.datetime.utcnow()) + datetime.timedelta(days=7)).isoformat() + 'Z'
    deletion = False
    slots = utilities.get_events(codeclinic_service,now, end_date)
    deletion, event = get_chosen_slot(slots, username, uid)
    if deletion == True:
        try:
            updated_event = update_booking_body(event, username)
            codeclinic_service.events().update(calendarId='primary', eventId=event['id'], body=updated_event).execute()
        except:
            return False, "ERROR: Could not cancel booking."
        return True, "Booking successfully deleted."
    else:
        return False, "ERROR: You cannot cancel selected booking."