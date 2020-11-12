from quickstart import create_service, check_calendar_connected
import volunteer
import utilities as utils
import event_listing as listings


def get_username():
    username = str(input("Please enter username: "))
    return username


def get_user_input():
    while True:
        command = input('Please choose an option from the list:\n1) Open a volunteer slot\n2) List open slots\n3) Exit\n')
        if command.isdigit():
            if int(command) >= 1 and int(command) <= 3:
                return int(command)
        print('Please enter a valid command.')

#test
        
class Student:
    username = get_username()
    try:
        service = create_service(username)
        print("Connected...")
    except:
        print("Error!")
        service = None

class CodeClinic:
    username = "codeclinic"
    try:
        service = create_service(username)
    except:
        print("Error!")
        service = None

if __name__ == "__main__":
    loop = True
    student = Student()
    codeclinic = CodeClinic()
    try : 
        utils.update_files(student.service, codeclinic.service)
    except:
        print("Error!")
        loop = False
    while loop == True:
        command = get_user_input()
        if command == 1:
             if not volunteer.create_volunteer_slot(student.username, student.service, codeclinic.service):
                 continue
        elif command == 2:
            user_choice = int(input("Which calendar would you like to view?\n1)Student calendar?\n2)Code clinic calendar\nplease insert choice: "))
            if user_choice == 1:
                listings.list_slots(student.service, False, True)
            elif command == 2:
                listings.list_slots(codeclinic.service, False, False)
        elif command == 3:
            break
        command = get_user_input()
    print('Exiting program..')

