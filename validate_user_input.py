import os
import sys
import json
import utilities as utils


def is_registered(username):
    '''
    Checks whether student is registered by retrieving information from the
    ".student_info.json" and sorting through it to find the student's username.
    If username is not found, student is not registered.

            Parameters:
                    username  (str): Student's username

            Returns:
                    True  (boolean): Student is registered
                    False (boolean): Student is not registered             
    '''

    try:
        if not os.stat('student-info/.student.json').st_size == 0:
            with open('student-info/.student.json') as json_file:
                data = json.load(json_file)
                if data != []:
                    students = data['student_info']
                    for student in students:
                        if student['username'] == username:
                            return True
    except FileNotFoundError:
        with open('student-info/.student.json', 'w') as json_file:
            pass
    return False


def contains_digit(arg):
    '''
    Confirms whether given argument contains a digit.  

            Parameters:
                    arg       (str): String to check
 
            Returns:
                    True  (boolean): String contains a digit 
                    False (boolean): String does not contain a digit        
    '''

    for letter in arg:
        if letter.isdigit():
            return True
    return False


def get_username(info):
    '''
    Sorts through the command-line arguments and finds username by filtering
    out commands and "main.py". The filtered list is iterated over to find
    the item of the list without a digit. This item is the username.

            Parameters:
                    info  (dict): Student information
 
            Returns:
                    info  (dict): Student information (includes username)      
    '''

    valid_args = ['create', 'cancel', 'register','volunteer', 'patient', 'list-bookings', 'list-open', 'list-slots', 'help', '-h', 'login', 'format','export']
    lst_not_args = list(filter(lambda x: x not in valid_args, sys.argv))
    if lst_not_args:
        lst_command_arg = list(filter(lambda y: 'main.py' not in y, lst_not_args))
        for item in lst_command_arg:
            if not contains_digit(item):
                if (is_registered(item)) or 'register' in sys.argv:
                        info['username'] = item
                        return info
                else:
                    utils.error_handling('INVALID: You are not registered.')
        utils.error_handling('INVALID: Username not provided or invalid.')


def get_user_type(info):
    '''
    Sorts through the command-line arguments and checks whether user type
    (volunteer/patient) was specified. If user type is present, user type
    is added to the info dictionary

            Parameters:
                    info  (dict): Student information
 
            Returns:
                    info  (dict): Student information (includes user type) 
                    *     (list): Booleans that help to clarify which support 
                                  infomation is needed to execute command     
    '''

    get_date, get_time = False, False
    get_id, get_password = False, False
    if 'volunteer' in sys.argv:
        info['user_type'] = 'volunteer'
        get_date = True
        get_time = True
    if 'patient' in sys.argv:
        info['user_type'] = 'patient'
        get_id = True
    return info, [get_date, get_time, get_id, get_password]


def get_command(info, criteria):
    '''
    Sorts through the command-line arguments and finds command type 
    (create/cancel/list-bookings/list-open/list-slots/help/export) and 
    adds it to the info dictionary.

            Parameters:
                        info  (dict): Student information
                    criteria  (list): Booleans that help to clarify which support 
                                      infomation is needed to execute command 
 
            Returns:
                    info  (dict): Student information (includes command type)   
    '''

    if 'create' in sys.argv:
        info['command'] = 'create'
    if 'cancel' in sys.argv:
        info['command'] = 'cancel'
    if 'list-bookings' in sys.argv:
        info['command'] = 'list-bookings'
    if 'list-slots' in sys.argv:
        info['command'] = 'list-slots'
    if 'list-open' in sys.argv:
        info['command'] = 'list-open'
        criteria[0] = True
    if sys.argv[1] == 'register':
        info['command'] = 'register'
        criteria[3] = True
    if sys.argv[1] == 'login':
        info['command'] = 'login'
        criteria[3] = True
    if 'export' in sys.argv:
        info['command'] = 'export'
    if '-h' in sys.argv or 'help' in sys.argv:
        info['command'] = 'help'
        if 'format' in sys.argv:
            info['command'] = 'format-help'
    return info


def get_support(info, criteria):
    #TODO: Remove True return -> not needed
    '''
    Sorts through the command-line arguments and looks for support information
    (date/start time/UD/description/password) if program needs it to execute
    the given command. The list of booleans, criteria, is used to decide which
    support infomation is required.

            Parameters:
                        info  (dict): Student information
                    criteria  (list): Booleans that help to clarify which support 
                                      infomation is needed to execute command 
 
            Returns:
                    True    (boolean): Required support information was given
                    info       (dict): Student information (includes support information)
    '''

    get_date, get_time, get_id, get_password = criteria[0], criteria[1], criteria[2], criteria[3]
    if get_date:
        if len(sys.argv) >= 5 and utils.check_date_format(sys.argv[4]):
            info['date'] = sys.argv[4]
        elif len(sys.argv) == 4:
            if utils.check_date_format(sys.argv[3]):
                info['date'] = sys.argv[3]
            else:
                utils.error_handling('INVALID: Date is either invalid or format is incorrect.\nEnter date as <yyyy-mm-dd>')
    if get_time:
        if len(sys.argv) >= 6 and utils.check_time_format(sys.argv[5]):
            info['start_time'] = sys.argv[5]
    if get_id:
        info['UD'] = ''
        if info['command'] == 'create':
            if len(sys.argv[-2]) == 26:
                info['UD'] = sys.argv[-2]
                info['description'] = sys.argv[-1]
                return True, info
        if len(sys.argv[len(sys.argv)-1]) == 26:
            info['UD'] = sys.argv[len(sys.argv)-1]
        return True, info
    if get_password:
        if len(sys.argv) == 4 and len(sys.argv[3]) == 8 and 'username' in info:
            info['password'] = sys.argv[3]
        else:
            utils.error_handling('INVALID: Password needs to be at exactly 8 characters long.')
    return True, info


def check_if_support_info_is_present(info):
    '''
    Sorts through the info dictionary and checks if all the information needed
    to execute command is present.

            Parameters:
                    info     (dict): Student information
 
            Returns:
                    True  (boolean): All required information is present in info dictionary
                    False (boolean): All required information is not present in info dictionary
    '''

    if 'user_type' in info:
        if info['user_type'] == 'volunteer':
            if ('date' in info and 'start_time' in info) and utils.date_has_passed(info['date'], info['start_time']):
                utils.error_handling('INVALID: Specified date/time has already passed.')
                return False
            if 'date' in info and 'start_time' in info:
                if 'command' in info and (info['command'] == 'create' or info['command'] == 'cancel'):
                    return True
            utils.error_handling('INVALID: Enter command in format: <username> volunteer <command> <yyyy-mm-dd> <hh:mm>')
        if info['user_type'] == 'patient':
            if 'UD' in info:
                if 'command' in info and (info['command'] == 'create' or info['command'] == 'cancel'):
                    return True
            utils.error_handling('INVALID: Enter command in format: <username> patient <command> <event_id> <"description">')
    elif 'command' in info:
        if info['command'] == 'list-open':
            if 'date' in info:
                return True
            utils.error_handling('INVALID: Enter command in format: <username> list-open <yyyy-mm-dd>')
        if info['command'] == 'register':
            if sys.argv[1] == 'register':
                if 'password' in info and 'username' in info:
                    return True
            utils.error_handling('INVALID: Enter command in format: register <username> <password>')
        if info['command'] == 'login':
            if 'password' in info and 'username' in info:
                return True
            utils.error_handling('INVALID: Enter command in format: login <username> <password>') 
        if not (info['command'] == 'cancel' or info['command'] == 'create'):
            return True
    return False


def get_user_commands():
    '''
    Collects required information from the command-line. If all required information
    is not present - the program will either print an error message to the terminal and exit
    or return an empty dictionary.
 
            Returns:
                    True     (boolean): All required information is present in info dictionary
                    False    (boolean): All required information is not present in info dictionary

                    info        (dict): Student information
                    *     (empty dict): Incorrect information provided by user
    '''

    info = get_username({})
    if info:
        info, criteria = get_user_type(info)
        info = get_command(info, criteria)
        valid_format, info = get_support(info, criteria)
        if valid_format and check_if_support_info_is_present(info):
            return True, info
        else:
            return False, {}
    return False, {}
