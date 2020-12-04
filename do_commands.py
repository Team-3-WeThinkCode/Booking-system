from commands import volunteer, booking, cancellation
from commands import event_listing as listings
import utilities as utils


def do_volunteer_commands(student, clinic, output):
    if student.info['command'] == 'create'and utils.check_date_and_time_format(student.info['date'], student.info['start_time']):
        created, output = volunteer.create_volunteer_slot(student.username, student.info['date'], student.info['start_time'], student.service, clinic.service)
        listings.print_correlating_table(True, True, student, clinic, created)
    elif student.info['command'] == 'cancel':
        created, output = volunteer.delete_volunteer_slot(student.username, student.info['date'], student.info['start_time'], student.service, clinic.service)
        listings.print_correlating_table(True, False, student, clinic, created)
    return output


def do_patient_commands(student, clinic, output):
    created = False
    if student.info['command'] == 'create':
        try:
            created, output = booking.make_booking(student.username, student.info['UD'], student.service, clinic.service)
        except(KeyError):
            output = "ERROR: Please include the correct uid when booking a slot."
        if not created:
            listings.print_correlating_table(False, True, student, clinic, False)
    elif student.info['command'] == 'cancel':
        try:    
            created, output = cancellation.cancel_attendee(student.username, student.service, clinic.service,student.info['UD'])
        except(KeyError):
            output = "ERROR: Please include the correct uid when cancelling a booking."
        if not created:    
            listings.print_correlating_table(False, False, student, clinic, False)
    return output


def do_event_listing_commands(student, clinic, output):
    if 'command' in student.info and student.info['command'] == 'list-bookings':
        events, output = listings.list_personal_slots(clinic.service, False, True, student.username)
    elif 'command' in student.info and student.info['command'] == 'list-slots':
        events, output = listings.list_personal_slots(clinic.service, False, False, student.username)
    elif 'command' in student.info and student.info['command'] == 'list-open':
        if 'date' in student.info and utils.check_date_format(student.info['date']):
            executed, output = listings.list_open_volunteer_slots(clinic.service, student.username,student.info['date'])
    return output