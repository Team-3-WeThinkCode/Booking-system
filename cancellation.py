import event_listing as listings
import utilities


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
            'attendees':[{'email': str(volunteer), 'responseStatus': 'accepted'}],
            'reminders': {
                'useDefault': True,
            },
     }
    return blueprint


def booker_accept_invite(service_clinic, unique_id, username, event):
    """
    Function will update the event with the user having already accepted the invite to the event.
    """
    event['attendees'][1]['responseStatus'] = 'accepted'
    service_clinic.events().update(calendarId='primary', eventId=unique_id, body=event).execute()

def cancel_attendee(username, volunteer_service, codeclinic_service, chosen_start_time, chosen_date):

    slots, x = listings.list_personal_slots(codeclinic_service, False, True, username)
    
    for event in slots:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        if chosen_start_time == start[11:16] and chosen_date == start[0:10]:
            if event['attendees'][1]['email'] == username+"@student.wethinkcode.co.za":
                volunteer = event['attendees'][0]['email']
                updated_event = update_booking_body(event, volunteer)
                updated_event_response = codeclinic_service.events().update(calendarId='primary', eventId=event['id'], body=updated_event).execute()
            else:
                print("You are not attending any sessions at this date and time")
        else:
            print("Please choose a valid date and time")