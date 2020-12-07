import os
import sys
import json
import utilities as utils


def is_registered(username):
    '''
    Checks whether student is registered by reviewing the information in the
    student json file
    :return: True if student is registered
    :return: False if student is not registered
    '''

    try:
        if not os.stat('data_files/.student.json').st_size == 0:
            with open('data_files/.student.json') as json_file:
                data = json.load(json_file)
                if data != []:
                    students = data['student_info']
                    for student in students:
                        if student['username'] == username:
                            return True
    except FileNotFoundError:
        with open('data_files/.student.json', 'w') as json_file:
            pass
    return False


def is_not_username(word):
    for letter in word:
        if letter.isdigit():
            return True
    return False


def get_username(info):
    '''
    Gets username from command line arguments and adds it to the given dictionary
    :return: Dictionary with username if username in command line arguments
    :return: Empty dictionary if username was not in command line arguments
    '''

    valid_args = ['create', 'cancel', 'register','volunteer', 'patient', 'list-bookings', 'list-open', 'list-slots']
    lst_not_args = list(filter(lambda x: x not in valid_args, sys.argv))
    if lst_not_args:
        lst_username = list(filter(lambda y: 'main.py' not in y, lst_not_args))
        for item in lst_username:
            if not is_not_username(item):
                if (is_registered(item)) or 'register' in sys.argv:
                    info['username'] = item
                    return info
                else:
                    utils.print_output('INVALID: You are not registered.')
    return {}


def get_user_type(info):
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
    Gets command type (create/cancel/list-bookings/list-open/list-slots) from command line
    arguments and adds it to the given dictionary
    :return: Dictionary with command if command specified in command line arguments
    :return: Given dictionary if command was not specified in command line arguments
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
    return info


def get_support(info, criteria):
    '''
    Collects required information for given command to allow the command 
    to be executed by the program
    :return: True if required information was given; Dictionary with required information
    :return: False if required information was not given; Dictionary with required information
    '''

    get_date, get_time, get_id, get_password = criteria[0], criteria[1], criteria[2], criteria[3]
    if get_date:
        if len(sys.argv) >= 5 and utils.check_date_format(sys.argv[4]):
            info['date'] = sys.argv[4]
        elif len(sys.argv) == 4 and utils.check_date_format(sys.argv[3]):
            info['date'] = sys.argv[3]
        else:
            utils.print_output('INVALID: Date format incorrect.\nExpected format: <yyyy-mm-dd>')
            return False, info
    if get_time:
        if len(sys.argv) >= 6 and utils.check_time_format(sys.argv[5]):
            info['start_time'] = sys.argv[5]
        else:
            utils.print_output('INVALID: Time format incorrect.\nExpected format: <hh:mm>')
            return False, info
    if 'date' in info and 'time' in info:
        if utils.date_has_passed(info['date'], info['time']):
            utils.print_output('INVALID: Specified date/time has already passed.')
            return False, info
    if get_id:
        info['UD'] = ''
        if info['command'] == 'create':
            if len(sys.argv[-2]) == 26:
                info['UD'] = sys.argv[-2]
                info['description'] = sys.argv[-1]
                return True, info
        if len(sys.argv[len(sys.argv)-1]) == 26:
            info['UD'] = sys.argv[len(sys.argv)-1]
        else:
            info['UD'] = ''
        return True, info
    if get_password:
        if len(sys.argv) == 4 and len(sys.argv[3]) == 8 and 'username' in info:
            info['password'] = sys.argv[3]
        else:
            utils.print_output('INVALID: Password should be 8 characters long.')
            return False, info
    return True, info


def check_if_support_info_is_present(info):
    '''
    Confirms whether required information was given for the program to execute command
    :return: True if required information present in dictionary
    :return: False if required information present in dictionary
    '''

    if 'user_type' in info:
        if info['user_type'] == 'volunteer':
            if 'date' in info and 'start_time' in info:
                if 'command' in info and (info['command'] == 'create' or info['command'] == 'cancel'):
                    return True
            utils.print_output('INVALID: Enter command in format: <username> volunteer <command> <yyyy-mm-dd> <hh:mm>')
            return False
        if info['user_type'] == 'patient':
            if 'UD' in info:
                if 'command' in info and (info['command'] == 'create' or info['command'] == 'cancel'):
                    return True
            utils.print_output('INVALID: Enter command in format: <username> patient <command> <event_id> <"description">')
            return False
    elif 'command' in info:
        if info['command'] == 'list-open':
            if 'date' in info:
                return True
            utils.print_output('INVALID: Enter command in format: <username> list-bookings')
            return False
        if info['command'] == 'register':
            if sys.argv[1] == 'register':
                if 'password' in info and 'username' in info:
                    return True
            utils.print_output('INVALID: Enter command in format: register <username> <password>')
            return False
        if not (info['command'] == 'cancel' or info['command'] == 'create'):
            return True
    return False


def get_user_commands():
    '''
    Collects required information for the program to execute expected command
    :return: True if valid information was collected; Dictionary with required information
    :return: False if invalid information was collected; Empty Dictionary
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
