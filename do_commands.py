from commands import volunteer, booking, cancellation, login
from commands import event_listing as listings
from commands import registration as register
from commands import help as help_command
import utilities as utils


def do_register_command(student_info):
    register.add_registration_info_to_json(student_info)


def do_login_command(username, password):
    login.login_details(username, password)


def do_help_command(format):
    if format:
        help_command.print_help_format_command()
    else:
        help_command.print_help_functionality()


def do_volunteer_commands(student, clinic):
    if student.info['command'] == 'create'and utils.check_date_and_time_format(student.info['date'], student.info['start_time']):
        created = volunteer.create_volunteer_slot(student.username, student.info['date'], student.info['start_time'], student.service, clinic.service)
        listings.print_correlating_table(True, True, student, clinic, created, False)
    elif student.info['command'] == 'cancel':
        created = volunteer.delete_volunteer_slot(student.username, student.info['date'], student.info['start_time'], student.service, clinic.service)
        listings.print_correlating_table(True, False, student, clinic, created, False)


def do_patient_commands(student, clinic):
    created = False
    if student.info['command'] == 'create':
        try:
            created = booking.make_booking(student.username, student.info['UD'], clinic, student.info)
        except(KeyError):
            utils.print_output('ERROR: Please enter a description in enclosed quotes.\ne.g. "Recursion"')
        if not created:
            listings.print_correlating_table(False, True, student, clinic, False, False)
    elif student.info['command'] == 'cancel':
        try:    
            created = cancellation.cancel_attendee(student.username, clinic ,student.info['UD'])
        except(KeyError):
            utils.print_output("ERROR: Please include the correct uid when cancelling a booking.")
        if not created:    
            listings.print_correlating_table(False, False, student, clinic, False, False)


def do_event_listing_commands(student, clinic):
    if 'command' in student.info and student.info['command'] == 'list-bookings':
        output = listings.print_correlating_table(True, False, student, clinic, False, True)
    elif 'command' in student.info and student.info['command'] == 'list-slots':
        output = listings.print_correlating_table(False, True, student, clinic, False, True)
    elif 'command' in student.info and student.info['command'] == 'list-open':
        if 'date' in student.info and utils.check_date_format(student.info['date']):
            output = listings.print_correlating_table(True, True, student, clinic, False, False)