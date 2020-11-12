import utilities as utils
import quickstart
import datetime
import event_listing as listings


def get_user_input(slots, username):
    user_choice = input("Please enter the number of the slot you would like to book: ")
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
        return get_user_input()



def make_booking(service_clinic, service_student, username):
    slots = listings.list_slots(service_clinic, fetch=False, user=False)
    print(f"Type 'cancel' if you would like to cancel this action.")
    slot_num = get_user_input(slots, username)
    if slot_num == False:
        return
   
    updated_event, unique_id = create_booking_body(slots[(slot_num - 1)], username)

    updated_event_response = service_clinic.events().update(calendarId='primary', eventId=unique_id, body=updated_event).execute()
    booker_accept_invite(service_clinic, unique_id, username, updated_event_response)
    print(f"Booking succesfully made! You're unique id is: {updated_event_response['id']}")

def booker_accept_invite(service_clinic, unique_id, username, event):
    event['attendees'][1]['responseStatus'] = 'accepted'
    service_clinic.events().update(calendarId='primary', eventId=unique_id, body=event).execute()


def create_booking_body(event, username):
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



# if __name__ == "__main__":
#     service_clinic = quickstart.create_service('codeclinic')
#     service_student = quickstart.create_service('student')
#     make_booking(service_clinic, service_student, 'jroy')