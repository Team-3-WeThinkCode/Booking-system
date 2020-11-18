from quickstart import create_service, check_calendar_connected
import volunteer
import utilities as utils
import event_listing as listings
import booking
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
    info = command_line_args()
    username = info['username']
    try:
        service = create_service(username)
        print("Connected...")
    except:
        print("Student calendar could not connect.")
        service = None


class CodeClinic:
    username = "codeclinic"
    try:
        service = create_service(username)
    except:
        print("Clinic calendar could not connect.")
        service = None


if __name__ == "__main__":
    student = Student()
    codeclinic = CodeClinic()
    execute = True
    try : 
        utils.update_files(student.service, codeclinic.service)
    except:

        print("Something went wrong!")
        execute = False
        
    ''' elif command == 5:
            listings.list_personal_slots(codeclinic.service, False, False, student.username)
        elif command == 6:
            booking.cancel_attendee(student.username, student.username, codeclinic.service)
        elif command == 7:
            break
     '''
    if execute:
        if 'user_type' in student.info:
            if student.info['user_type'] == 'volunteer':
                if student.info['command'] == 'create':
                    created, output = volunteer.create_volunteer_slot(student.username, student.info['date'], student.info['start_time'], student.service, codeclinic.service)
                elif student.info['command'] == 'cancel':
                    created, output = volunteer.delete_volunteer_slot(student.username, student.info['date'], student.info['start_time'], student.service, codeclinic.service)
            elif student.info['user_type'] == 'patient':
                if student.info['command'] == 'create':
                    created, output = booking.make_booking(student.username, student.info['date'], student.info['start_time'], student.service, codeclinic.service)
                elif student.info['command'] == 'cancel':
                    #add cancel booking functionality
                    output = 'Canceled booking'
            print(output+'\n')
        elif 'command' in student.info and student.info['command'] == 'list':
                listings.list_slots(codeclinic.service, False, False)
        else:
            print('Invalid input.')
