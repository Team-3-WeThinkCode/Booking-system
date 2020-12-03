import sys
from validate_user_input import get_user_commands
from commands import registration as register
from quickstart import create_service
import utilities as utils
import do_commands
  
        
class Student:
    """ Setup student profile """

    def __init__(self):
        valid, self.info = get_user_commands()
        self.username, self.service  = '', ''
        if valid:
            self.username = self.info['username']
            try:
                self.service = create_service(self.username)
                print("Connected...")
            except:
                print("Student calendar could not connect.")
                self.service = None


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
    execute = True
    output = 'INVALID: Input is invalid.\nUse the help command for the correct input format/commands.\nHelp command: [username] [-h]'
    if not student.info:
        execute = False
        utils.print_output(output)
    if not sys.stdin.isatty():
        data = sys.stdin.readlines()
    if execute:
        try:
            utils.update_files(student.service, codeclinic.service, student.username)
            if 'user_type' in student.info:
                if student.info['user_type'] == 'volunteer':
                    output = do_commands.do_volunteer_commands(student, codeclinic, output)
                elif student.info['user_type'] == 'patient':
                    output = do_commands.do_patient_commands(student, codeclinic, output)
            elif 'command' in student.info and student.info['command'] == 'register':
                if register.validate_registration_info(student.info):
                    added, output = register.add_info_to_json(student.info)
            else:
                output = do_commands.do_event_listing_commands(student, codeclinic, output)
            utils.print_output(output)
        except:
            print("Something went wrong!")
