from quickstart import create_service, check_calendar_connected
import volunteer
import utilities as utils
import event_listing as listings
import booking
import datetime
import sys


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
            elif sys.argv[i] == 'list':
                info['command'] = 'list'
    if len(sys.argv) == 6:
        info['date'] = sys.argv[4]
        info['start_time'] = sys.argv[5]
    return info
  
        
class Student:
    """ Setup student profile """

    def __init__(self):
        self.info = command_line_args()
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
    try:
        utils.update_files(student.service, codeclinic.service)
    except:
        print("Something went wrong!")
        execute = False
    if execute:
        output = 'Invalid input.'
        if 'user_type' in student.info and len(sys.argv) == 6:
            if not check_date_and_time_format(student.info['date'], student.info['start_time']):
                pass
            elif student.info['user_type'] == 'volunteer':
                if student.info['command'] == 'create':
                    created, output = volunteer.create_volunteer_slot(student.username, student.info['date'], student.info['start_time'], student.service, codeclinic.service)
                elif student.info['command'] == 'cancel':
                    created, output = volunteer.delete_volunteer_slot(student.username, student.info['date'], student.info['start_time'], student.service, codeclinic.service)
            elif student.info['user_type'] == 'patient':
                if student.info['command'] == 'create':
                    created, output = booking.make_booking(student.username, student.info['date'], student.info['start_time'], student.service, codeclinic.service)
                elif student.info['command'] == 'cancel':
                    created = booking.cancel_attendee(student.username, student.service, codeclinic.service)
                    output = ''
        elif 'command' in student.info and student.info['command'] == 'list':
                events, output = listings.list_personal_slots(codeclinic.service, False, False, student.username)
                #listings.list_slots(codeclinic.service, False, False)
        print(output + '\n')
