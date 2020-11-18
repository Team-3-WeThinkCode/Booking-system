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
        command = input('\nChoose an option from the list:\n1) Open a volunteer slot\n2) List open slots\n3) Book an empty slot\n4) Cancel volunteer slot\n5) List my bookings\n6) Cancel my booking\n7) Exit \n Enter choice: ')
        print()
        if command.isdigit():
            if int(command) >= 1 and int(command) <= 6:
                return int(command)
        print('Please enter a valid command.')

#test
        
class Student:
    username = get_username()
    try:
        service = create_service(username)
        print("Connected...")
    except:
        print("Unable to connect..")
        service = None

class CodeClinic:
    username = "codeclinic"
    try:
        service = create_service(username)
    except:
        print("Something went wrong!")
        service = None

if __name__ == "__main__":
    #list open slots: student calendar lists events for the next 7 days - clinic calander lists open volunteer slots
    menu = True
    student = Student()
    codeclinic = CodeClinic()
    try : 
        utils.update_files(student.service, codeclinic.service)
    except:
        print("Something went wrong!")
        menu = False
    if menu:
        command = get_user_input()
    while menu == True:
        if command == 1:
             created, output = volunteer.create_volunteer_slot(student.username, student.service, codeclinic.service)
             print(output+'\n')   
        elif command == 2:
            user_choice = int(input("Which calendar would you like to view?\n1)Student calendar?\n2)Code clinic calendar\nPlease insert choice: "))
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
            listings.list_personal_slots(codeclinic.service, False, False, student.username)
        elif command == 6:
            booking.cancel_attendee(student.username, student.username, codeclinic.service)
        elif command == 7:
            break
        command = get_user_input()
    print('Exiting program..')

