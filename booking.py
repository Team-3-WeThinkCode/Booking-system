import utilities as utils
import event_listing as listings


def get_user_input(slots, username):
    """
    validates the users input and returns it as an integer.
    Function does not allow users to choose a slot with their own username present.
    """

    #Create conditions to avoid malicious input for "Open slots command"
    user_choice = input("Please enter the number of the slots you would like to book: ")
    if user_choice == 'cancel':
        return False
    if user_choice.isdigit():
        while True:
            if "VOLUNTEER: " + str(username) in slots[int(user_choice) - 1]['summary']:
                print('User cannot book themselves.')
                return get_user_input(slots, username)
            elif "VOLUNTEER: " + str(username) not in slots[int(user_choice) - 1]['summary']:
                break
        return int(user_choice)
    else:
        return get_user_input(slots, username)

def get_user_input_cancellation(slots, username):
    """
    validates the users input and returns it as an integer.
    Function does not allow users to choose a slot with their own username present.
    """

    #Create conditions to avoid malicious input for "Open slots command"
    user_choice = input("Please enter the number of the slot you would like to cancel: ")
    if user_choice == 'cancel':
        return False
    if user_choice.isdigit():
        while True:
            if "VOLUNTEER: " + str(username) in slots[int(user_choice) - 1]['summary']:
                print('User cannot book themselves.')
                return get_user_input(slots, username)
            elif "VOLUNTEER: " + str(username) not in slots[int(user_choice) - 1]['summary']:
                break
        return int(user_choice)
    else:
        return get_user_input(slots, username)

def get_chosen_slot(events, username, chosen_date, chosen_start_time):
    for i in range(0, len(events)):
        event = events[i]
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        start_date = start[0:10]
        if chosen_start_time == start[11:16] and chosen_date == start_date:
            if "VOLUNTEER: " + str(username) in event['summary']:
                return False, {}
            elif len(event["attendees"]) == 1:
                return True, event
    return False, {}


def make_booking(username, date, time, service_student, service_clinic):
    """
    Function will handle the logic for booking a empty slot.
    with a list of events, user input will be he index of the list -1, the event will be updated with the user added as an attendee.

    """
    slots = listings.list_slots(service_clinic, fetch=True, user=False)
    available, volunteered_event = get_chosen_slot(slots, username, date, time)
    if not available:
        return False, 'Cannot book chosen slot.'
    updated_event, unique_id = create_booking_body(volunteered_event, username)
    try:
        updated_event_response = service_clinic.events().update(calendarId='primary', eventId=unique_id, body=updated_event).execute()
        booker_accept_invite(service_clinic, unique_id, username, updated_event_response)
        return True, "Booking succesfully made! You're unique id is: "+ str(updated_event_response['id'])
    except:
        return False, "An error has stopped the booking from being made.\nPlease try again."


def booker_accept_invite(service_clinic, unique_id, username, event):
    """
    Function will update the event with the user having already accepted the invite to the event.
    """
    event['attendees'][1]['responseStatus'] = 'accepted'
    service_clinic.events().update(calendarId='primary', eventId=unique_id, body=event).execute()


def create_booking_body(event, username):
    """
    Function will take a event object and sort the relevant data to create a body for the new booking.
    User will be added as an attendee and only relevant data will be taken from the event object for body.
    :RETURN: New event body will be returned with updated information.
    """
    event['attendees'].append({'email': username+'@student.wethinkcode.co.za'})

    blueprint = {
            'summary': event['summary'],
            'location': event['location'],
            'start': event['start'],
            'end': event['end'],
            'attendees':event['attendees'],
            'reminders': {
                'useDefault': True,
            },
     }
    return blueprint, event['id']
  

def cancel_attendee(username, volunteer_service, codeclinic_service):

    slots = listings.list_personal_slots(codeclinic_service, False, False, username)
    print(f"Type 'cancel' if you would like to cancel this action.")
    slot_num = get_user_input_cancellation(slots, username)
    if slot_num == False:
        return

    #list all events for the next 7 days and allow attendee to delete using number index specific event
    #if there are no events to delete print there are no events to delete
    #delete event
    #return event deleted
    #for event in events if ({'email': username+'@student.wethinkcode.co.za'}) == username+'@student.wethinkcode.co.za'} 

