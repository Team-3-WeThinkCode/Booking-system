import sys
from quickstart import create_service
from validate_user_input import get_user_commands
from commands import registration as register
from commands import export_calendar as export
from commands import help as help_command
from commands import login
import utilities as utils
import do_commands
  
        
class Student:
    """ Setup student profile """

    def __init__(self):
        valid, self.info = get_user_commands()
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
        except:
            print("Clinic calendar could not connect.")
            self.service = None


if __name__ == "__main__":
    student = Student()
    codeclinic = CodeClinic()
    data = ''
    if student.info:
        try:
            utils.update_files(student.service, codeclinic.service, student.username)
        except:
            utils.error_handling('ERROR: Event files could not be updated.')
    else:
        utils.error_handling('INVALID: Input invalid. Use the help command for further information.\nHelp command: -h')
    if not (student.info['command'] == 'login' or student.info['command'] == 'register'):
        login.log_in_expired(student.username)
    if not sys.stdin.isatty():
        data = sys.stdin.readlines()
    if 'user_type' in student.info:
        if student.info['user_type'] == 'volunteer':
            do_commands.do_volunteer_commands(student, codeclinic)
        elif student.info['user_type'] == 'patient':
            do_commands.do_patient_commands(student, codeclinic)
    elif 'command' in student.info and student.info['command'] == 'register':
        register.add_registration_info_to_json(student.info)
    elif 'command' in student.info and student.info['command'] == 'login':
        login.login_details(student.info['username'], student.info['password'])
    elif 'command' in student.info and student.info['command'] == 'help':
        help_command.print_help_command()
    elif 'command' in student.info and student.info['command'] == 'format-help':
        help_command.print_help_format_command()
    elif 'command' in student.info and student.info['command'] == 'export':
        export.export_calendar()
    else:
        do_commands.do_event_listing_commands(student, codeclinic)
