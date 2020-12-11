import sys, utilities
from validation import do_commands, validate_user_input
from API.calendar_api import create_service
from API.gmail_api import create_email_service
from commands import login
from commands import export_calendar as export

  
        
class Student:
    """ Setup student profile """

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
    """ Setup Code Clinic profile """

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

    student = Student()
    codeclinic = CodeClinic()
    data = ''
    #check if input entered is invalid
    if not student.info:
        utilities.error_handling('INVALID: Input invalid. Use the help command for further information.\nHelp command: -h')
    #check if student's login token has expired
    if not (student.info['command'] == 'login' or student.info['command'] == 'register'):
        login.log_in_expired(student.username)
    #update data files
    utilities.update_files(student.service, codeclinic.service, student.username)
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
            do_commands.do_register_command(student.info)
        elif student.info['command'] == 'login':
            do_commands.do_login_command(student.info['username'], student.info['password'])
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