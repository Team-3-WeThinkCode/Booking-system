import sys
from quickstart import create_service
from validate_user_input import get_user_commands
from commands import registration as register
from validate_user_input import get_user_commands
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
    output = 'INVALID: Input is invalid.\nUse the help command for the correct input format/commands.\nHelp command: [username] [-h]'
    execute = True
    data = ''
    if student.info:
        try:
            utils.update_files(student.service, codeclinic.service, student.username)
        except:
            print("Something went wrong!")
            execute = False
    else:
        execute = False
    if not sys.stdin.isatty():
        data = sys.stdin.readlines()
    if execute:
        if 'user_type' in student.info:
            if student.info['user_type'] == 'volunteer':
                do_commands.do_volunteer_commands(student, codeclinic, output)
            elif student.info['user_type'] == 'patient':
                do_commands.do_patient_commands(student, codeclinic, output)
        elif 'command' in student.info and student.info['command'] == 'register':
            added = register.add_registration_info_to_json(student.info)
        else:
            do_commands.do_event_listing_commands(student, codeclinic, output)
    #utils.print_output(output)
