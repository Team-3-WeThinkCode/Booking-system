from quickstart import create_service, check_calendar_connected
import volunteer
import utilities as utils
import event_listing as listings


def get_username():
    username = str(input("Please enter username:\n"))
    return username


def get_user_input():
    while True:
        command = input('Please choose an option from the list:\n1) Volunteer to open slots\n2) Delete calendar event\n3) List open slots\n')
        if command.isdigit():
            if int(command) >= 1 and int(command) <= 3:
                return int(command)


class Student:
    username = get_username()
    service = create_service(username)

class CodeClinic:
    username = "codeclinic"
    service = create_service(username)


if __name__ == "__main__":
    student = Student()
    codeclinic = CodeClinic()
    command = get_user_input()
    if command == 1:
        if volunteer.create_volunteer_slot(student.username, student.service, codeclinic.service):
            print('Succesful!')
        else:
            print('Oops, slot is not open on your calendar..')
    elif command == 2:
        pass
    elif command == 3:
        listings.list_slots(codeclinic.service)
    # '''check_calendar_connected()
    # command = get_user_input()
    # if command == 1:
    #     utils.create_booking(student.username, student.service)
    # elif command == 2:
    #     utils.delete_event(student.service)
    # else:
    #     utils.list_calendars()'''
    #volunteer.create_volunteer_slot(student.username, student.service, codeclinic.service)

