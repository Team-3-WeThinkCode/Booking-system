from quickstart import create_service, check_calendar_connected
import volunteer
import utilities as utils


def get_username():
    username = str(input("Please enter username:\n"))
    return username


def get_user_input():
    while True:
        command = input('Please choose an option from the list:\n1) Create calendar event\n2) Delete calendar event\n3) List calendar events\n')
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
    check_calendar_connected()
    command = get_user_input()
    if command == 1:
        utils.create_booking(student.username, student.service)
    elif command == 2:
        utils.delete_event(student.service)
    else:
        utils.list_slots(codeclinic.service)
    volunteer.create_volunteer_slot(student.username, student.service, codeclinic.service)

