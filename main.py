import sys
from quickstart import create_service, check_calendar_connected
import utilities as utils
from commands import registration as register
from validate_user_input import get_user_commands
import do_commands


def command_line_args():
    #format: [username] [user_type] [command] [date] [start_time]
    info = {'username' : sys.argv[1]}
    if len(sys.argv) > 1:
        for i in range(1, len(sys.argv)):
            if sys.argv[i] == 'volunteer':
                info['user_type'] = 'volunteer'
            elif sys.argv[i] == 'patient':
                info['user_type'] = 'patient'
            elif sys.argv[i] == 'create':
                info['command'] = 'create'
            elif sys.argv[i] == 'cancel':
                info['command'] = 'cancel'
            elif sys.argv[i] == 'list-bookings':  #lists user code clinic bookings for next 7 days
                info['command'] = 'list-bookings'
            elif sys.argv[i] == 'list-slots': #lists all opens lots for next 7 days
                info['command'] = 'list-slots'
            if len(sys.argv[i]) == 26:
                info['UD'] = sys.argv[i]
    if len(sys.argv) == 6:
        info['date'] = sys.argv[4]
        info['start_time'] = sys.argv[5]
    return info
  
        
class Student:
    """ Setup student profile """

    def __init__(self):
        valid, self.info = get_user_commands()
        self.username, self.service = '', ''
        if valid:
            self.username = self.info['username']
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
        output = 'INVALID: Input is invalid.\nUse the help command for the correct input format/commands.\nHelp command: [username] [-h]'
        if 'user_type' in student.info:
            if student.info['user_type'] == 'volunteer':
                output = do_commands.do_volunteer_commands(student, codeclinic, output)
            elif student.info['user_type'] == 'patient':
                output = do_commands.do_patient_commands(student, codeclinic, output)
        elif 'command' in student.info and student.info['command'] == 'register':
            added, output = register.add_registration_info_to_json(student.info)
        else:
            output = do_commands.do_event_listing_commands(student, codeclinic, output)
        utils.print_output(output)
