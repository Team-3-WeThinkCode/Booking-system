from quickstart import create_service, check_calendar_connected
import volunteer
import utilities as utils
import event_listing as listings
import booking


def get_username():
    username = str(input("Enter username: "))
    return username


def get_user_input():
    while True:
        command = input('\nChoose an option from the list:\n1) Open a volunteer slot\n2) List open slots\n3) Book an empty slot\n4) Cancel volunteer slot\n5) Exit\nEnter choice: ')
        print()
        if command.isdigit():
            if int(command) >= 1 and int(command) <= 5:
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
    utils.update_files(student.service, codeclinic.service)
    command = get_user_input()
    while True:
        if command == 1:
             created, output = volunteer.create_volunteer_slot(student.username, student.service, codeclinic.service)
             print(output+'\n')   
        elif command == 2:
            user_choice = int(input("Which calendar would you like to view?\n1)Student calendar?\n2)Code clinic calendar\nplease insert choice: "))
            if user_choice == 1:
                listings.list_slots(student.service, False, True)
            elif command == 2:
                listings.list_slots(codeclinic.service, False, False)
        elif command == 3:
            booking.make_booking(codeclinic.service, student.service, student.username)
        elif command == 4:
            created, output = volunteer.delete_volunteer_slot(student.username, student.service, codeclinic.service)
            print(output+'\n')
        elif command == 5:
            break
        command = get_user_input()
    print('Exiting program..')

