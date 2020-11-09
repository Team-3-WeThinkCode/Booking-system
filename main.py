from quickstart import create_service, check_calendar_connected()
import utilities as utils

class Student:
    username, service = create_service()

class CodeClinic:
    username, service = create_service()


if __name__ == "__main__":
    student = Student()
    codeclinic = CodeClinic()
    check_calendar_connected()
    command = utils.get_user_input()
    if command == 1:
        utils.create_booking(username, service)
    elif command == 2:
        utils.delete_event(service)
    else:
        utils.list_calendars()

