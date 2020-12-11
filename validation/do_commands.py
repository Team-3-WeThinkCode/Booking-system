import os, sys
USER_PATHS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../'))
sys.path.insert(0, USER_PATHS)
from commands import volunteer, booking, login
from commands import event_listing as listings
from commands import registration as register
from commands import help as help_command
import utilities as utils


def do_register_command(username, password):
    '''
    Executes register command.

            Parameters:
                    username (str): Student's username
                    password (str): Student's password
    '''

    register.add_registration_info_to_json(username, password)


def do_login_command(username, password):
    '''
    Executes login command.

            Parameters:
                    username  (str): Student's username
                    password  (str): Student's 8 character password 
    '''

    login.login_details(username, password)


def do_help_command(format):
    '''
    Executes specified help command, namely normal help or format help.

            Parameters:
                    format  (boolean): True if format help command should 
                                       be executed   
    '''

    if format:
        help_command.print_help_format_command()
    else:
        help_command.print_help_functionality()


def do_volunteer_commands(student, clinic):
    '''
    Executes specified volunteer command, namely creating or cancelling a volunteer slot.

            Parameters:
                    student  (obj): Object with information on logged-in student
                    clinic   (obj): Object with information on Code clinic      
    '''

    if student.info['command'] == 'create'and utils.check_date_and_time_format(student.info['date'], student.info['start_time']):
        created = volunteer.create_volunteer_slot(student.username, student.info['date'], student.info['start_time'], student.service, clinic.service)
        listings.print_correlating_table(True, True, student, clinic, created, False)
    elif student.info['command'] == 'cancel':
        created = volunteer.delete_volunteer_slot(student.username, student.info['date'], student.info['start_time'], student.service, clinic.service)
        listings.print_correlating_table(True, False, student, clinic, created, False)


def do_patient_commands(student, clinic):
    '''
    Executes specified patient command, namely creating or cancelling a booked slot.

            Parameters:
                    student  (obj): Object with information on logged-in student
                    clinic   (obj): Object with information on Code clinic     
    '''

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
            created = booking.cancel_attendee(student.username, clinic ,student.info['UD'])
        except(KeyError):
            utils.print_output("ERROR: Please include the correct uid when cancelling a booking.\nFormat: <username> cancel patient <uid>.")
        if not created:    
            listings.print_correlating_table(False, False, student, clinic, False, False)


def do_event_listing_commands(student, clinic):
    '''
    Executes specified event listing command, namely list booking, list slots or list open.

            Parameters:
                    student  (obj): Object with information on logged-in student
                    clinic   (obj): Object with information on Code clinic       
    '''

    if 'command' in student.info and student.info['command'] == 'list-bookings':
        output = listings.print_correlating_table(True, False, student, clinic, False, True)
    elif 'command' in student.info and student.info['command'] == 'list-slots':
        output = listings.print_correlating_table(False, True, student, clinic, False, True)
    elif 'command' in student.info and student.info['command'] == 'list-open':
        output = listings.print_correlating_table(True, True, student, clinic, False, False)