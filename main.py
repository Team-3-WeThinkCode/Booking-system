import sys
from utilities import utilities
from validation import validate_user_input
from API.gmail_api import create_email_service
from API.calendar_api import create_service
from commands import export_calendar as export
from commands import login, do_commands

       
class Student:
    '''
    The Student object contains information on the user.

    Attributes:
        info     (dict): Information needed to execute 
                         command.
        username  (str): Student's username
        service   (obj): User's Google Calendar API service
    '''

    def __init__(self):
        valid, self.info = validate_user_input.get_user_commands()
        self.username, self.service = '', ''
        if valid:
            self.username = self.info['username'].strip()
            try:
                self.service = create_service(self.username)
                print("Connected...")
            except:
                print("Student calendar could not connect.")
                self.service = None
        else:
            self.info = {}


class CodeClinic:
    '''
    The CodeClinic object contains information on the Code Clinic.

    Attributes:
        username       (str): Code clinic's username
        service        (obj): Code clinic's Google Calendar API service
        email_service  (obj): Code clinic's Gmail API service
    '''

    def __init__(self):
        self.username = "codeclinic"
        try:
            self.service = create_service(self.username)
            self.email_service = create_email_service()
        except:
            print("Clinic calendar could not connect.")
            self.service = None


def run_program():
    '''
    Executes program
    '''

    data, msg = '', ''
    student = Student()
    codeclinic = CodeClinic()
    #checks if input entered is invalid
    if not student.info:
        msg = 'INVALID: Input invalid. '\
            +'Use the help command for further information.\nHelp command: -h'
        utilities.error_handling(msg)
    #checks if student's login token has expired
    is_auth_command = (student.info['command'] == 'login' \
                    or student.info['command'] == 'register')
    if not is_auth_command:
        login.log_in_expired(student.username)
    #update data files
    utilities.update_files(student.service,
                           codeclinic.service,
                           student.username)
    #ensures piping input accepted
    if not sys.stdin.isatty():
        data = sys.stdin.readlines()
    #execute commands
    if 'user_type' in student.info:
        if student.info['user_type'] == 'volunteer':
            do_commands.do_volunteer_commands(student, codeclinic)
        elif student.info['user_type'] == 'patient':
            do_commands.do_patient_commands(student, codeclinic)
    elif 'command' in student.info:
        if student.info['command'] == 'register':
            do_commands.do_register_command(student.info['username'],
                                            student.info['password'])
        elif student.info['command'] == 'login':
            do_commands.do_login_command(student.info['username'],
                                         student.info['password'])
        elif student.info['command'] == 'help':
            do_commands.do_help_command(False)
        elif student.info['command'] == 'format-help':
            do_commands.do_help_command(True)
        elif student.info['command'] == 'export':
            export.export_calendar()
        else:
            do_commands.do_event_listing_commands(student, codeclinic)


if __name__ == "__main__":
    run_program()