from quickstart import create_service, check_calendar_connected
import volunteer
import cancellation
import utilities as utils
import event_listing as listings
import booking
import sys
import registration as register


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
            elif sys.argv[i] == 'list-open':
                info['command'] = 'list-open'
                info['date'] = sys.argv[3]
            elif sys.argv[i] == 'register' and len(sys.argv) == 5:
                info['command'] = 'register'
                info['password'] = sys.argv[4]
                info['email'] = info['username'] + '@student.wethinkcode.co.za'
                if 'CPT' in sys.argv:
                    info['campus'] = 'Cape Town'
                elif 'JHB' in sys.argv:
                    info['campus'] = 'Johannesburg'
                else:
                    return {'username' : sys.argv[1]}
    if len(sys.argv) == 6 and not info['command'] == 'list-open':
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
    data = ''
    if not sys.stdin.isatty():
        data = sys.stdin.readlines()
    try:
        utils.update_files(student.service, codeclinic.service, student.username)
    except:
        print("Something went wrong!")
        execute = False
    if execute:
        output = 'Invalid input.'
        if 'user_type' in student.info and len(sys.argv) == 6:
            if not utils.check_date_and_time_format(student.info['date'], student.info['start_time']):
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
                    created = cancellation.cancel_attendee(student.username, student.service, codeclinic.service, student.info['start_time'], student.info['date'])
                    output = ''
        elif 'command' in student.info and student.info['command'] == 'register':
            if register.validate_registration_info(student.info):
                added, output = register.add_info_to_json(student.info)
        elif 'command' in student.info and student.info['command'] == 'list-bookings':
            events, output = listings.list_personal_slots(codeclinic.service, False, True, student.username)
        elif 'command' in student.info and student.info['command'] == 'list-slots':
            events, output = listings.list_personal_slots(codeclinic.service, False, False, student.username)
        elif 'command' in student.info and student.info['command'] == 'list-open':
            if 'date' in student.info and utils.check_date_format(student.info['date']):
                executed, output = listings.list_open_volunteer_slots(codeclinic.service, student.info['date'])
        print(output + '\n')
