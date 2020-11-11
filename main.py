from quickstart import create_service, check_calendar_connected
import volunteer
import utilities as utils
import event_listing as listings


def get_username():
    username = str(input("Please enter username: "))
    return username


def get_user_input():
    while True:
        command = input('Please choose an option from the list:\n1) Open a volunteer slot\n2) List open slots\n3) Exit')
        if command.isdigit():
            if int(command) >= 1 and int(command) <= 3:
                return int(command)
        print('Please enter a valid command.')


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
    while True:
        if command == 1:
             if not volunteer.create_volunteer_slot(student.username, student.service, codeclinic.service):
                 continue
        elif command == 2:
            listings.list_slots(codeclinic.service, False)
        elif command == 3:
            break
        command = get_user_input()
    print('Exiting program..')

